#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:59:59 2022

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

df = pd.read_excel('/Users/hukaiyu/Desktop/Y3/Y3 Project/noise_rank_scheme_1_simple.xls')

#%% put people in the same cluster to excels
group=[]
for i in range (5):
    group.append(df.loc[df["cluster"]==i])
#%%
writer = pd.ExcelWriter('/Users/hukaiyu/Desktop/Y3/Y3 Project/group/clusters.xls')
for i in range (5):
    group[i].to_excel(writer,sheet_name='%i'%i)
writer.save()