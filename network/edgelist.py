#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 19:02:51 2022

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

# Load the adjacency list
df=pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle")  
df=pd.DataFrame(df) 

#Convert the adjacency list into edge list
vertex=list(df['Source'])
n=len(df['Source']) #number of vertices
M=np.zeros((n,n)) #adjacency matrix
edgelist=[] 
for i in range (0, n):
    for j in range (len(df['Neighbour'][i])):
        vertex1=vertex.index(df['Source'][i])
        vertex2=vertex.index(df['Neighbour'][i][j])
        t=tuple([vertex1,vertex2])
        if M[vertex1][vertex2] == 0 and M[vertex2][vertex1] == 0: #make sure only one edge between a pair of vertices
            edgelist.append(t)
        M[vertex1][vertex2]=1
        
#%% Save to txt
np.savetxt('/Users/hukaiyu/Desktop/Y3/Y3 Project/edgelist.txt',edgelist)



        

