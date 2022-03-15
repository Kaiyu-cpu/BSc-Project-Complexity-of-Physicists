#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 17:58:12 2022

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

def add_and_remove_edges(G, p_new_connection, p_remove_connection):    
    '''    
    for each node,    
      add a new connection to random other node, with prob p_new_connection,    
      remove a connection, with prob p_remove_connection    

    operates on G in-place    
    '''                
    new_edges = []    
    rem_edges = []    

    for node in G.nodes():    
        # find the other nodes this one is connected to    
        connected = [to for (fr, to) in G.edges(node)]    
        # and find the remainder of nodes, which are candidates for new edges   
        unconnected = [n for n in G.nodes() if not n in connected]    

        # probabilistically add a random edge    
        if len(unconnected): # only try if new edge is possible    
            if random.random() < p_new_connection:    
                new = random.choice(unconnected)    
                G.add_edge(node, new)    
                #print ("\tnew edge:\t {} -- {}".format(node, new))    
                new_edges.append( (node, new) )    
                # book-keeping, in case both add and remove done in same cycle  
                unconnected.remove(new)    
                connected.append(new)    

        # probabilistically remove a random edge    
        if len(connected): # only try if an edge exists to remove    
            if random.random() < p_remove_connection:    
                remove = random.choice(connected)    
                G.remove_edge(node, remove)    
                #print ("\tedge removed:\t {} -- {}".format(node, remove))    
                rem_edges.append( (node, remove) )    
                # book-keeping, in case lists are important later?    
                connected.remove(remove)    
                unconnected.append(remove)    
    return rem_edges, new_edges
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

p_new_connection = 0.05
p_remove_connection = 0.05
n=100 #number of simulations

for i in range (n):
    H_unfrozen=H.copy()
    rem_edges, new_edges = add_and_remove_edges(H_unfrozen, p_new_connection, p_remove_connection)
    H2 = H_unfrozen
    H2.remove_edges_from(rem_edges)
    H2.add_edges_from(new_edges)
    
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
df_mark.to_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/noise_rank_scheme_1_simple.xls')



 











#%%