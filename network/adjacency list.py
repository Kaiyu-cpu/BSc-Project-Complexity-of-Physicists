#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 12:05:28 2022

@author: hukaiyu
"""

import codecs
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import re
import numpy as np

# Load the file
df=pd.read_pickle("/Users/hukaiyu/Desktop/Y3/Y3 Project/name_hyperlinks.pickle")  
df=pd.DataFrame(df)   
a=df['hyperlink'][0]        

#%%
# Relace the space in names by underscore to fit the format 
Source=[]
for i in range (len(df['name'])):
    t=df['name'][i]
    t=t.replace(' ','_')
    Source.append(t)
    
#%%
# Extract the text of name in url
# Determine if the name is in the list of physisits
# If so, add an unweighted edge
Neighbours=[]
for i in range (len(Source)):
    name_list=[]
    for j in range (len(df['hyperlink'][i])):
        if type(df['hyperlink'][i][j]) == str:
            last=df['hyperlink'][i][j].split('/')[-1]
            if (last in Source and last != Source[i]): #excluding the physisit himeself/herself
                name_list.append(last)
    Neighbours.append(name_list)
    
#%%
# Eliminate repeating names
Neighbour=[]
for i in range (len(Source)):
    k=Neighbours[i]
    k=list(set(k))
    Neighbour.append(k)
    
#%%
#Save to pickle file
df = pd.DataFrame(
    {'Source' : Source,
     'Neighbour' : Neighbour})
df.to_pickle('/Users/hukaiyu/Desktop/Y3/Y3 Project/adjacency_list.pickle')
    
                
                
