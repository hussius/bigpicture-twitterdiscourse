from gensim import corpora, models, similarities
import glob
import os
import sys

if len(sys.argv) < 3:
    sys.exit('python content_analysis.py <user tweet file dir> <infomap tree file>')

nclus = 15

clusterId = {} # dictionary for looking up cluster ID for user ID
userId = {} # dictionary for looking up user IDs for a certain cluster ID
clusterFile = sys.argv[2]
with open(clusterFile) as inFile:
    for line in inFile:
        [fullClusID, score, numId, uName] = line.strip().split()
        #twoLevelClusID = ':'.join(fullClusID.split(":")[:2])
        clusId = fullClusID.split(":")[0]
        #clusterId[uName]=twoLevelClusID
        clusterId[uName]=clusId
        if not clusId in userId:
            userId[clusId] = [uName]
        else:
            userId[clusId].append(uName)
        #if not twoLevelClusID in userId:
        #    userId[twoLevelClusID] = [uName]
        #else:
        #    userId[twoLevelClusID].append(uName)

# Find largest clusters
clusBySize = sorted(userId.items(), key=lambda x: len(x[1]), reverse=True)
biggestClusters = clusBySize[0:nclus]

userTweets = {}
textPath = sys.argv[1]

# If you want the work with certain selected clusters
#sel = ['1','4']

#selectedClusters = []
#for i in userId.items():
#    if i[0] in sel:
#        selectedClusters.append(i)

#print(selectedClusters)

# Read tweets for users in each of 20 biggest clusters and put in userTweets dictionary
for clus in biggestClusters:
#for clus in selectedClusters:
    print('Reading tweets for cluster ' + clus[0])
    print('Number of accounts: ' + str(len(clus[1])))
    for user in clus[1]:
        fname = textPath + '/' + user + '.txt'
        userTweets[user]=open(fname).readlines()

# List of words per cluster (this is slightly different from before)
clusterTweets = []
#for clu in selectedClusters: 
for clu in biggestClusters:
    string = ''
    for user in userId[clu[0]]:
        if user in userTweets:
            for word in userTweets[user]: string += word
    clusterTweets.append(string)

print("Removing stop words")
stoplist = set('och i att för med så är det från på som jag rt inte om the den men vi ni du en har av till de man ett kan var ska'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in clusterTweets]

print("Removing tokens that appear only once")
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
        for token in text:
             frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1] for text in texts]

print("Removing twitter handles")
texts = [[token for token in text if token[0]!='@'] for text in texts]
print(texts[0][:25])
print("Length of texts:" + str(len(texts)))

# Make dictionary of all the tweets
print("Making dictionary")
dictionary = corpora.Dictionary(texts)
print(dictionary)
print("Making bag of words representation of each user")
corpus = [dictionary.doc2bow(text) for text in texts]
print("Making TF-IDF model")
tfidf = models.TfidfModel(corpus)

for clu in range(0,nclus):
#    print("Cluster ", biggestClusters[clu][0], biggestClusters[clu][1][:5])
    print("Cluster ", selectedClusters[clu][0], selectedClusters[clu][1][:5])
    print("=========")
    textInputList = texts[clu]
    subset_tfidf = tfidf[dictionary.doc2bow(textInputList)]
    # Top terms
    topt = sorted(subset_tfidf, key=lambda x: x[1], reverse=True)[:20]
    # print(topt)
    for i in topt:
        print(dictionary[i[0]])
    print('\n')
