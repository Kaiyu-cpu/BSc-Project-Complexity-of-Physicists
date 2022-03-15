#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:43:57 2022

@author: hukaiyu
"""

import networkx as nx
import codecs
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import rankdata  

def rescale (x):
    x=np.array(x)
    Max=max(x)
    return (x/Max)*100
#%%
# Load the adjacency list
df = pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle")  
df = pd.DataFrame(df) 

for i in range (len(df['Source'])):
    df['Source'][i]=df['Source'][i].replace('_',' ') #convert name to formal format

#%%
# Load the clusters list
df2 = pd.read_excel("/Users/hukaiyu/Desktop/Y3/Y3 Project/Grouped File 2.xlsx")  
df2 = pd.DataFrame(df2)

#%% Combining two dataframe
df_tot = pd.merge(df, df2, how='inner', on='Source')


#%% Define the network

G = nx.Graph() # create a directed network

for i in range (len(df_tot['Source'])): # add the name of physicists as node
    G.add_node(df_tot['Source'][i], cluster_no=df_tot['Cluster'][i]) # adding cluster number that the physicist belongs

# add an edge if there is a hyperlink between tow physicists' websites (no direction)
for i in range (len(df_tot['Source'])): 
    for j in range (len(df_tot['Neighbour'][i])):
        G.add_edge(df_tot['Source'][i],df_tot['Neighbour'][i][j].replace('_',' '))
        
# largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)

#%% Centrality measures
degree = dict(H.degree())
closeness = nx.closeness_centrality(H)
betweenness = nx.betweenness_centrality(H)
eigenvector = nx.eigenvector_centrality(H)
pagerank = nx.pagerank(H)
name=list(degree.keys())

k=list(degree.values())
c=list(closeness.values())
b=list(betweenness.values())
ev=list(eigenvector.values())
pr=list(pagerank.values())

k_rescaled=rescale(k)
c_rescaled=rescale(c)
b_rescaled=rescale(b)
ev_rescaled=rescale(ev)
pr_rescaled=rescale(pr)

average_mark=sum([k_rescaled,c_rescaled,b_rescaled,ev_rescaled,pr_rescaled])/5

cluster=nx.get_node_attributes(H,'cluster_no')
cluster=list(cluster.values())

#%% Define a new network for visulization D
# If A has a higher value in every centrality measure than B does, a directed edge from A to B will be added
D = nx.DiGraph()
for i in range (len(name)):
    if average_mark[i]>=34.3:
        D.add_node(name[i],cluster_no=cluster[i])
#D.remove_edges_from(list(D.edges))
for i in range (len(name)):
    edges=list(H.edges(name[i]))
    for j in range (len(edges)):
        index=name.index(edges[j][1])
        if (k[i]>k[index] and c[i]>c[index] and b[i]>b[index] and ev[i]>ev[index] and pr[i]>pr[index] and average_mark[i]>=34.3 and average_mark[index]>=34.3):
            # print(name[i],name[index])
            D.add_edge(name[i],name[index])
            

#%% relabeling the nodes with the index
name2=list(dict(D.degree()).keys())
mapping=dict(map(reversed, enumerate(name2)))
D2=nx.relabel_nodes(D,mapping)
TR = nx.transitive_reduction(D2)

#%%
nx.write_edgelist(TR,'/Users/hukaiyu/Desktop/Y3/Y3 Project/DLCC_edgelist.txt',delimiter=' ', data=['weight'])

#%%
a,b=np.loadtxt('/Users/hukaiyu/Desktop/Y3/Y3 Project/DLCC_edgelist.txt',unpack=True)
ud=[]
weight=[]
for i in range (len(a)):
    ud.append('directed')
    weight.append(1)
df3 = pd.DataFrame(
    {'Source' : a,
     'Target': b,
     'Type': ud,
     'Weight': weight
    })
     
df3.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/visulization/DLCC edges.xls') 

#%%
ID=list(dict(TR.degree()).keys())
for i in range (len(name2)):
    if name2[i]=='Albert Einstein':
        top=i
        
level=np.zeros(30)
level[top]=1
for i in range (len(name2)):
    if i!=top:
        level[i]=len(max(nx.all_simple_paths(TR, top, i), key=lambda x: len(x)))

cluster2=nx.get_node_attributes(D,'cluster_no')
cluster2=list(cluster2.values())
df4 = pd.DataFrame(
     {'Id' : ID,
      'Name': name2,
      'level': level,
      'cluster': cluster2
     })
      
df4.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/visulization/DLCC nodes.xls')  













