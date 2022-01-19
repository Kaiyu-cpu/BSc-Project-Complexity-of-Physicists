#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 12:59:40 2022

@author: fanchao
"""

import codecs
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd



#read local html file and parse it to beautiful soup
path = "/Users/fanchao/Desktop/Year 3/Project/WikipediaPhysicistsTSE210909/output210909/"


Text = []
Name = []


for filename in glob.glob(os.path.join(path, '*.html')):
    html = codecs.open(filename,"r","utf-8")
#html = codecs.open(
    #"/Users/fanchao/Desktop/Year 3/Project/WikipediaPhysicistsTSE210909/output210909/Aage_Bohr.html", 
    #"r", "utf-8")
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    Text.append(text)
    
    #extract the names of the pages
    for i, line in enumerate(text.splitlines()):
        if i == 1:
            Name.append(line)
            break

# store all the extracted information to pickle file
df = pd.DataFrame(
    {'Name' : Name,
     'Text' : Text})

df.to_pickle('/Users/fanchao/Desktop/Year 3/Project/pickle.pickle')
