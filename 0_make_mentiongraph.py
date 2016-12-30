import os
import sys
import networkx as nx
import regex
import pickle
from collections import Counter
from glob import glob

if len(sys.argv) < 3:
    sys.exit('python ' + sys.argv[0] + ' <path to directory of tweet files> <name of graph to write to file>')

# inpath should point to a directory containing *.txt files where each file is named after an account and contains tweets from that account
inpath = sys.argv[1] + '/' 
graph_name = sys.argv[2]
files = [os.path.basename(x) for x in glob(inpath+'/*.txt')]
screen_names = set([name[:-4] for name in files])
print("Number of accounts: ", len(screen_names))
#regex_2015 = regex.compile(r'2015-') 
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
