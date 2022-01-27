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

#%%
# Load the edge list
edgelist=np.loadtxt('/Users/hukaiyu/Desktop/Y3/Y3 Project/edgelist.txt')
# Convert edgelist into networkx graph
G = nx.from_edgelist(edgelist)
for i in range (0,1021):
    G.add_node(i) # Add all the "isolated" physicists
# Load the adjacency list
df=pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle")  
df=pd.DataFrame(df) 

#%%
# Determine the degree of each node 
name=[]
k=[]
node=list(G.nodes)
degree=list(G.degree)
for i in range (0,1021): # make sure name mataches degree
    name.append(df['Source'][node[i]])
    k.append(degree[i][1])

#%%
# save it to excel
df2 = pd.DataFrame(
    {'name' : name,
     'degree (k)' : k})
df2.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/name_degree.xls')

#%% Plot P(k) distribution
k_nk=pd.value_counts(k) #count the number of occurrences of different values of k
k2=list(k_nk.index)
nk=np.array(k_nk)
N=sum(nk)
P_k=nk/N #calculate the probability
plt.plot(k2,P_k,'x')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.yscale('log')
plt.xscale('log')
