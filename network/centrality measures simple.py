#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 08:16:12 2022

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

#%% Crate a table of all centrlity methods
# ranking scheme 1:
# Rescale centrality method new=old/max_of_this_measure and then times by 100
# Sum up all measures to give a final "mark" 

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
cluster_no=nx.get_node_attributes(H,'cluster_no')
cluster_no=list(cluster_no.values())

df_mark = pd.DataFrame(
    {'name' : name,
     'cluster': cluster_no,
     'degree': k,
     'rescaled degree': k_rescaled,
     'closeness' : c,
     'rescaled closeness': c_rescaled,
     'betweenness' : b,
     'rescaled betweenness': b_rescaled,
     'eigenvector': ev,
     'rescaled eigenvector': ev_rescaled,
     'pagerank': pr,
     'rescaled pagerank': pr_rescaled,
     'average mark': average_mark
     })
#%%
df_mark.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/rank_scheme_1_simple.xls')


#%%
# ranking scheme 2:
# find the rank of the physicist in each centrality measre
# The mean of ranks is used as the final "rank"

k_rank=dict(zip(degree.keys(), rankdata([-i for i in degree.values()], method='min')))
c_rank=dict(zip(closeness.keys(), rankdata([-i for i in closeness.values()], method='min')))
b_rank=dict(zip(betweenness.keys(), rankdata([-i for i in betweenness.values()], method='min')))
ev_rank=dict(zip(eigenvector.keys(), rankdata([-i for i in eigenvector.values()], method='min')))
pr_rank=dict(zip(pagerank.keys(), rankdata([-i for i in pagerank.values()], method='min')))

k_rank=np.array(list(k_rank.values()))
c_rank=np.array(list(c_rank.values()))
b_rank=np.array(list(b_rank.values()))
ev_rank=np.array(list(ev_rank.values()))
pr_rank=np.array(list(pr_rank.values()))
average=[]
for i in range (len(name)): 
    average.append((k_rank[i] + c_rank[i] + b_rank[i] + ev_rank[i] + pr_rank[i])/5)
    
df_rank = pd.DataFrame(
    {'name' : name,
     'cluster': cluster_no,
     'degree rank': k_rank,
     'closeness rank' : c_rank,
     'betweenness rank' : b_rank,
     'eigenvector rank': ev_rank,
     'pagerank rank': pr_rank,
     'average rank': average
     })

#%%
df_rank.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/rank_scheme_2_simple.xls')

#%% put people in the same cluster to excels
group=[]
for i in range (list(df2['Cluster'])[-1]+1):
    group.append(df_rank.loc[df_rank["cluster"]==i])
#%%
writer = pd.ExcelWriter('/Users/hukaiyu/Desktop/Y3/Y3 Project/group/clusters.xls')
for i in range (list(df2['Cluster'])[-1]+1):
    group[i].to_excel(writer,sheet_name='%i'%i)
writer.save()














