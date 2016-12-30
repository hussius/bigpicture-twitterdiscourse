# bigpicture-twitterdiscourse
Companion repository to upcoming blog post "The big picture of public discourse" where we analyze Swedish Twitter data from 2015.
To illustrate what we did, a couple of Python scripts are provided. You need to have the networkx library for the first two, and the gensim library for the third one.
You also need to have a working installation of Infomap (the standalone version). We use the standalone version because we have been unable to make the Python Infomap library generate the same results as the standalone.

The first script, 0_make_mentiongraph.py, is not meant to be run unless necessary. It is used to process a large number of tweets to generate a networkx graph, which is stored as a pickle file.
Example call:

```python 0_make_mentiongraph.py small small_graph```

We will provide "ready-made" pickle files so that you should hopefully be able to skip this step.

The second script, 1_pickle_to_communities.py, does the actual community detection analysis by using Infomap. 

```python 1_pickle_to_communities.py small_graph```

The third script, 2_content_analysis.py, calculates the most distinctive words for each of the largest communities (using TF-IDF) and gives some information on each cluster.

```python 2_content_analysis.py small small_graph_trees```
