#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 22:08:32 2022

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

# get cluster number
cluster_no=nx.get_node_attributes(H,'cluster_no')
cluster_no=list(cluster_no.values())

#%% relabeling the nodes with the index

degree = dict(H.degree())
name=list(degree.keys())
mapping=dict(map(reversed, enumerate(name)))
H2=nx.relabel_nodes(H,mapping)

#%%
nx.write_edgelist(H2,'/Users/hukaiyu/Desktop/Y3/Y3 Project/LCC_edgelist.txt',delimiter=' ', data=['weight'])
#%%
a,b=np.loadtxt('/Users/hukaiyu/Desktop/Y3/Y3 Project/LCC_edgelist.txt',unpack=True)
ud=[]
weight=[]
for i in range (len(a)):
    ud.append('Undirected')
    weight.append(1)
df3 = pd.DataFrame(
    {'Source' : a,
     'Target': b,
     'Type': ud,
     'Weight': weight
    })
     
df3.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/visulization/edges.xls')   

#%%
degree2 = dict(H2.degree())
ID=list(degree2.keys())
df4 = pd.DataFrame(
     {'Id' : ID,
      'Name': name,
      'Cluster': cluster_no
     })
      
df4.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/visulization/nodes.xls')   
     





















     
     
     
     
 