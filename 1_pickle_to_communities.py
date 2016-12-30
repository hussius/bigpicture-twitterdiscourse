#!/usr/bin/env python
import sys
import os
import networkx as nx
import pickle
import operator
import subprocess

if len(sys.argv) < 2:
    sys.exit('python ' + sys.argv[0] + ' <base name of pickle file (i e without the .pickle suffix)>')

## Change this!
infomap_path='/Users/mikaelhuss/apps/infomap/Infomap'

# Read pickle file
base=sys.argv[1]
print('Reading file...')
pkl = base + '.pickle'
# Read undirected graph
gd = pickle.load(open(pkl,"rb"))
# Convert to undirected reciprocal graph
print('Converting to reciprocal...')
gud = gd.to_undirected(reciprocal=True)
# Convert to numbered edges
numbered = {}
counter = 0
outf = open('numeric_edgelist.txt','w')
for edge in gud.edges():
    [source, target] = edge
    if not source in numbered:
        numbered[source]=counter
        counter += 1
    if not target in numbered:
        numbered[target]=counter
        counter += 1
    outf.write(str(numbered[source]) + '\t' + str(numbered[target])+'\n')
outf.close()

# Write vertex mapping table
mapf = open('vertex_mapping.txt','w')
for n in numbered:
    mapf.write(str(numbered[n]) + '\t' + n + '\n')
mapf.close()

# Run Infomap
tree_dir = base+'_trees'
try:
    os.mkdir(tree_dir)
except:
    print("Directory exists? Proceeding...")

subprocess.call([infomap_path, '-z', '-2', '-u', 'numeric_edgelist.txt', tree_dir])

# Assign names to nodes
tfile = open(tree_dir + "/numeric_edgelist.tree")
vfile = open('vertex_mapping.txt')
ofile = open(tree_dir + "/numeric_edgelist_named.tree","w")

vname = {}
for line in vfile:
    [idx, name] = line.strip().split()
    vname[idx] = name

tfile.readline() # Header 1
tfile.readline() # Header 2

for line in tfile:
    [clus, score, tag, id] = line.strip().split(' ')
    ofile.write(clus + '\t' + score + '\t' + id + '\t' + vname[id] + '\n')
