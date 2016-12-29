import os
import sys
import networkx as nx
import pandas as pd
import regex
import pickle
from collections import Counter
# My addition
from glob import glob
 
#inpath = "/Users/mos/twitterdb/2015_totalUsertweets/"
#files_2015 = pickle.load(open("./files_2015.pickle","rb")) # totalUsertweet-files >10 rows in ~/twitterdb/2015_totalUsertweets

# Assume that files_2015 is a list of file names in inpath
inpath = sys.argv[1] + '/' #"./small/"
graph_name = sys.argv[2]
files = [os.path.basename(x) for x in glob(inpath+'/*.txt')]
screen_names = set([name[:-4] for name in files])
print("Number of accounts: ", len(screen_names))
#regex_2015 = regex.compile(r'2015-') # Skipping this requirement - probably Mattias had date info on each tweet
mention_pattern = regex.compile(r'@(\w+)')

G = nx.DiGraph() 
filectr = 0
for index, file in enumerate(files):
    filectr += 1
    if filectr % 1000 == 0:
        print(filectr)
    infile = open(inpath + file)
    source = file[:-4]
    user_targets = []
    target_counter = Counter()

    for line in infile:
        if mention_pattern.findall(line) != []:
            user_targets.extend(mention_pattern.findall(line))
            target_counter.update(user_targets)
    
    for target, count in target_counter.items():
        if target in screen_names:
            G.add_edge(source,target,w=count)
    
pickle.dump(G,open(graph_name+".pickle","wb"))
