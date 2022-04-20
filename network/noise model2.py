#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:29:25 2022

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
import random

def rescale (x):
    x=np.array(x)
    Max=max(x)
    return (x/Max)*100

def add_and_remove_random_edges(graph):
    edges = list(graph.edges)
    nonedges = list(nx.non_edges(graph))
    
    p=0.05
    n=len(edges)
    for i in range (int(n*p)):
        # random edge choice
        chosen_edge = random.choice(edges)
        edges.remove(chosen_edge)
        chosen_nonedge = random.choice([x for x in nonedges if chosen_edge[0] == x[0]])
        nonedges.remove(chosen_nonedge)
    
        # delete chosen edge
        graph.remove_edge(chosen_edge[0], chosen_edge[1])
        # add new edge
        graph.add_edge(chosen_nonedge[0], chosen_nonedge[1])

    return graph
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

#%% Original network
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

k_rescaled_0=rescale(k)
c_rescaled_0=rescale(c)
b_rescaled_0=rescale(b)
ev_rescaled_0=rescale(ev)
pr_rescaled_0=rescale(pr)
average_mark_0=sum([k_rescaled_0,c_rescaled_0,b_rescaled_0,ev_rescaled_0,pr_rescaled_0])/5

#%% For each measure, create a list of simulations
k_list=[]
c_list=[]
b_list=[]
ev_list=[]
pr_list=[]
average_mark_list=[]

n=100 #number of simulations

for i in range (n):
    H_unfrozen=H.copy()
    H2 = add_and_remove_random_edges(H_unfrozen)

    
    degree = dict(H2.degree())
    closeness = nx.closeness_centrality(H2)
    betweenness = nx.betweenness_centrality(H2)
    eigenvector = nx.eigenvector_centrality(H2)
    pagerank = nx.pagerank(H2)

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
    
    k_list.append(k_rescaled)
    c_list.append(c_rescaled)
    b_list.append(b_rescaled)
    ev_list.append(ev_rescaled)
    pr_list.append(pr_rescaled)
    average_mark_list.append(average_mark)

#%%
k_std=[]
c_std=[]
b_std=[]
ev_std=[]
pr_std=[]
average_mark_std=[]
for i in range(len(name)):
    t1=[]
    t2=[]
    t3=[]
    t4=[]
    t5=[]
    t6=[]
    for j in range (n):
        t1.append(k_list[j][i])
        t2.append(c_list[j][i])
        t3.append(b_list[j][i])
        t4.append(ev_list[j][i])
        t5.append(pr_list[j][i])
        t6.append(average_mark_list[j][i])
    k_std.append(np.std(t1))
    c_std.append(np.std(t2))
    b_std.append(np.std(t3))
    ev_std.append(np.std(t4))
    pr_std.append(np.std(t5))
    average_mark_std.append(np.std(t6)) 
  
#%%
df_mark = pd.DataFrame(
    {'name' : name,
     'cluster': cluster_no,
     'rescaled degree': k_rescaled_0,
     'k_std': k_std,
     'rescaled closeness': c_rescaled_0,
     'c_std': c_std,
     'rescaled betweenness': b_rescaled_0,
     'b_std': b_std,
     'rescaled eigenvector': ev_rescaled_0,
     'ev_std': ev_std,
     'rescaled pagerank': pr_rescaled_0,
     'pr_std': pr_std,
     'average mark': average_mark_0,
     'std':average_mark_std
     })
#%%
df_mark.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/noise2_rank_scheme_1_simple.xls')
#%%
df_simu = pd.DataFrame(
    {'k': k_list,
     'c': c_list,
     'b': b_list,
     'ev': ev_list,
     'pr': pr_list,
     'average mark': average_mark_list
    })
#%%
df_simu.to_pickle('/Users/hukaiyu/Desktop/Y3/Y3 Project/noise2_data.pkl')



 











#%%