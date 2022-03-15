#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:07:14 2022

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

#%%
# Load the adjacency list
df = pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle")  
df = pd.DataFrame(df) 

#%% Define the network

G = nx.DiGraph() # create a directed network

for i in range (len(df['Source'])): # add the name of physicists as node
    G.add_node(df['Source'][i])

# add an edge if there is a hyperlink between tow physicists' websites (direction matters)
for i in range (len(df['Source'])): 
    for j in range (len(df['Neighbour'][i])):
        G.add_edge(df['Source'][i],df['Neighbour'][i][j])

#%%
# Rank physicists by their degree
in_degree=list(G.in_degree())  
out_degree=list(G.out_degree())
degree=list(G.degree())

name=[]
k_in=[]
k_out=[]
k=[]

for i in range (0,1019):
    name.append(in_degree[i][0])
    k_in.append(in_degree[i][1])
    k_out.append(out_degree[i][1])
    k.append(degree[i][1])
    
df2 = pd.DataFrame(
    {'name' : name,
     'k' : k,
     'k_in' : k_in,
     'k_out' : k_out})

#%% Save to excel
df2.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/name_degree_directed.xls')

#%% Degree distribution
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

#%% save to excel
df3 = pd.DataFrame(
    {'k' : k2,
     'P(k)' : P_k})
df3.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/degree_distribution.xls')

#%% log binning
bin_n=30 #number of bins
b_max=max(k2)

b=[]
exp_del=1.23
for i in range (bin_n):
    b.append(b_max/(exp_del**i))
b=np.sort(b)
k_b=[]
Pk_b=[]
judge=np.zeros(len(k2))
for i in range (bin_n):
    temp=[]
    for j in range (len(k2)):
        if k2[j]<=b[i] and judge[j]==0:
            judge[j]=1
            temp.append(P_k[j])
    if(i==0):
        Pk_b.append(sum(temp)/(b[i]))
        k_b.append(0)
    else:
        Pk_b.append(sum(temp)/(b[i]-b[i-1]))
        k_b.append(np.sqrt(b[i]*b[i-1]))

plt.plot(k2,P_k,'x')
plt.plot(k_b,Pk_b,'o')
plt.xlabel('k')
plt.ylabel('P(k)')
plt.yscale('log')
plt.xscale('log')
database=['original data','log binned data']
plt.legend(database, loc='best')

#%% CDF
df4 = pd.read_excel("/Users/hukaiyu/Desktop/Y3/Y3 Project/degree distribution.xls")  
df4 = pd.DataFrame(df4) 
CP=[]
for i in range (len(df4['k'])):
    CP.append(sum(df4['P(k)'][:i]))
plt.plot(list(df4['k']),CP,'x')
plt.xlabel('k')
plt.ylabel('P<(k)')
plt.yscale('log')
plt.xscale('log')

#%% Zipf plot
r=[]
for i in range (len(df4['k'])):
    r.append(sum(df4['P(k)'][i:]))
plt.plot(r,list(df4['k']),'x')
plt.xlabel('rank')
plt.ylabel('k')
plt.yscale('log')
plt.xscale('log')


#%% Calculate closeness
in_closeness=nx.closeness_centrality(G)
out_closeness=nx.closeness_centrality(G.reverse())
    

   


