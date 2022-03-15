#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 21:53:21 2022

@author: hukaiyu

Vertex is the index of name of physicists.
An unweighted edge is added if there is at least one hyperlink between two physicists' websites.

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

#%%
# Load the adjacency list
df = pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle")  
df = pd.DataFrame(df) 

#%% Define the network

G = nx.Graph() # create a directed network

for i in range (len(df['Source'])): # add the name of physicists as node
    G.add_node(df['Source'][i])

# add an edge if there is a hyperlink between tow physicists' websites (no direction)
for i in range (len(df['Source'])): 
    for j in range (len(df['Neighbour'][i])):
        G.add_edge(df['Source'][i],df['Neighbour'][i][j])

#%%
# Rank physicists by their degree
degree=list(G.degree())

name=[]
k=[]

for i in range (0,1019):
    name.append(degree[i][0])
    k.append(degree[i][1])
    
df2 = pd.DataFrame(
    {'name' : name,
     'k' : k})

#%%
# save it to excel
df2.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/name_degree_simple.xls')

#%% Closeness and betweenness

# largest connected component
components = nx.connected_components(G)
largest_component = max(components, key=len)
H = G.subgraph(largest_component)

closeness=nx.closeness_centrality(H)
betweenness=nx.betweenness_centrality(H)

#%%
# Rank physicists by their closeness and betweenness

name=list(closeness.keys())
c=list(closeness.values())
b=list(betweenness.values())
    
df3 = pd.DataFrame(
    {'name' : name,
     'closeness' : c,
     'betweenness' : b})

#%%
# save it to excel
df3.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/name_c_b_simple.xls')

