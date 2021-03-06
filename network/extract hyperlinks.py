#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 19:21:37 2022

@author: hukaiyu
"""


import codecs
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import re



#read local html file and parse it to beautiful soup
path = "/Users/hukaiyu/Desktop/Y3/Y3 Project/WikipediaPhysicistsTSE210909/output210909/"


Name = []
URL = []



for filename in glob.glob(os.path.join(path, '*.html')):
    url = []
    html = codecs.open(filename,"r","utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    
    #cut all the sidebars off
    
    for sb in soup.find_all(class_='sidebar-content'): 
        sb.decompose()


    # cut references/sources/notes/external_links/references_and_notes off 
    
    string = str(soup)
    string1,string2,string3 = string.partition('<span class="mw-headline" id="References">')
    
    if string2!='':
        soup = BeautifulSoup(string1)
    else:
        string1,string2,string3 = string.partition('<span class="mw-headline" id="Sources">')
        
        if string2!='':
            soup = BeautifulSoup(string1)
        else:
            string1,string2,string3 = string.partition('<span class="mw-headline" id="Notes">')
            
            if string2!='':
                soup = BeautifulSoup(string1)
            else:
                string1,string2,string3 = string.partition('<span class="mw-headline" id="References_and_notes">')
                
                if string2!='':
                    soup = BeautifulSoup(string1)
                else:
                    string1,string2,string3 = string.partition('<span class="mw-headline" id="External_links">')
                    soup = BeautifulSoup(string1)
                

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
    
    #extract the names of the pages
    for i, line in enumerate(text.splitlines()):
        if i == 1:
            Name.append(line)
            break
    
    # find all the anchor tags with "href" 
    for link in soup.find_all('a'): #find all the hyperlinks in the website
        # append the actual urls
        url.append(link.get("href"))
    URL.append(url)

# store all the extracted information to pickle file
df = pd.DataFrame(
    {'name' : Name,
     'hyperlink' : URL})

#%%
df.to_pickle('/Users/hukaiyu/Desktop/Y3/Y3 Project/name_hyperlinks.pickle')