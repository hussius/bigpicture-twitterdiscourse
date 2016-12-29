import os
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
inpath = "./small/"
files = [os.path.basename(x) for x in glob(inpath+'/*.txt')]
screen_names = set([name[:-4] for name in files])

#regex_2015 = regex.compile(r'2015-') # Skipping this requirement - probably Mattias had date info on each tweet
mention_pattern = regex.compile(r'@(\w+)')

G = nx.DiGraph() 

for index, file in enumerate(files):
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
    
pickle.dump(G,open("./G.pickle","wb"))
