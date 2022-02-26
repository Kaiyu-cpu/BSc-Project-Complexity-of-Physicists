#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:24:29 2022

@author: fanchao
"""

import codecs
from bs4 import BeautifulSoup
import os
import glob
import pandas as pd
import urllib.parse
import re

def doc_extract(path, to_pickle = False):
    '''
    Parameters
    ----------
    path : TYPE str
        the path of your files.
    to_pickle : TYPE Bool, optional
        Choose whether to save the output to pickle file. The default is False.

    Returns
    -------
    df: Pandas Dataframe that contains the names, main body wikipedia texts 
        and hyperlinks contained of physicists.

    '''
    Text = []
    Name = []
    URL = []

    for filename in glob.glob(os.path.join(path, '*.html')):
        
        html = codecs.open(filename,"r","utf-8")
        soup = BeautifulSoup(html, features="html.parser")
        url = []        
        
        #cut all the sidebars off
        for sb in soup.find_all(class_='sidebar-content'): 
            sb.decompose()
            
            
        # remove all script and style elements
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
        # remove irrelavent parts to main body texts
        head,sep,tail = text.partition('Jump to search')
        prefix,text = head,tail
        # extract the names of the pages
        for i, line in enumerate(prefix.splitlines()):
            if i == 1:
                Name.append(line)
                break
        
        # cut everything after and including references, only keep main body texts
        head,sep,tail = text.partition('Publications[edit]')
        if sep != '':
            head = head.replace('[edit]', '')
        else:
            head,sep,tail = head.partition('See also[edit]')

            if sep != '':
                head = head.replace('[edit]', '')
            else:
                head, sep, tail = head.partition('Books[edit]')

                if sep != '':
                    head = head.replace('[edit]','')
                else:
                    head,sep,tail = head.partition('Bibliography[edit]')

                    if sep != '':
                        head = head.replace('[edit]','')
                    else:
                        head,sep,tail = head.partition('References[edit]')

                        if sep != '':
                            head,sep,tail = head.partition('Sources[edit]')

                            if sep != '':
                                head = head.replace('[edit]','')
                            else:
                                head,sep,tail = head.partition('Notes[edit]')

                                if sep != '':
                                    head = head.replace('[edit]','')
                                else:
                                    head,sep,tail = head.partition('References and notes[edit]')

                                    if sep != '':
                                        head = head.replace('[edit]','')
                                    else:
                                        head,sep,tail = head.partition('External links[edit]')


        # remove words between 1 and 3
        shortword= re.compile(r'\W*\b\w{1,2}\b')
        head = shortword.sub('', head)
        Text.append(head)

        
        # cut references/sources/notes/external_links/references_and_notes off 
        string = str(soup)
        string1,string2,string3 = string.partition(
            '<span class="mw-headline" id="References">')

        if string2!='':
            soup = BeautifulSoup(string1,features="html.parser")
        else:
            string1,string2,string3 = string.partition(
                '<span class="mw-headline" id="Sources">')

            if string2!='':
                soup = BeautifulSoup(string1,features="html.parser")
            else:
                string1,string2,string3 = string.partition(
                    '<span class="mw-headline" id="Notes">')

                if string2!='':
                    soup = BeautifulSoup(string1,features="html.parser")
                else:
                    string1,string2,string3 = string.partition(
                        '<span class="mw-headline" id="References_and_notes">')

                    if string2!='':
                        soup = BeautifulSoup(string1,features="html.parser")
                    else:
                        string1,string2,string3 = string.partition(
                            '<span class="mw-headline" id="External_links">')
                        soup = BeautifulSoup(string1,features="html.parser")
    
    
        # find all the anchor tags with "href" 
        for link in soup.find_all('a'): #find all the hyperlinks in the website
            # append the actual urls
            url.append(link.get("href"))
            
        URL.append(url)
        
        
    df = pd.DataFrame(
        {'Name' : Name,
         'Text' : Text,
         'Hyperlink'  : URL})
    
    if to_pickle == True:       
        # store all the extracted information to pickle file
        df.to_pickle('cleaned_dataframe.pickle')
        
    return df



def get_adjacency(df, to_pickle='False'):
    '''
    

    Parameters
    ----------
    df : TYPE Pandas DataFrame
        Input dataframe which should contain names and links cleared using doc_extract.
    to_pickle : TYPE Bool, optional
        Choose whether to store output to pickle file. The default is 'False'.

    Returns
    -------
    df_output : TYPE Pandas DataFrame
        Output Dataframe that contains source and neibours.

    '''

    # Relace the space in names by underscore to fit the format 
    Source=[]
    for i in range (len(df['Name'])):
        t=df['Name'][i]
        t=t.replace(' ','_')
        Source.append(t)
        
    # Extract the text of name in url
    # Determine if the name is in the list of physicists
    # If so, add an unweighted edge
    Neighbours=[]
    for i in range (len(Source)):
        name_list=[]
        for j in range (len(df['Hyperlink'][i])):
            if type(df['Hyperlink'][i][j]) == str:
                last=df['Hyperlink'][i][j].split('/')[-1]
                last=urllib.parse.unquote(last) # convert to utf-8 
                if (last in Source and last != Source[i]): 
                    #excluding the physicists tehmselves
                    name_list.append(last)
        Neighbours.append(name_list)
    
    
    # Eliminate repeating names
    Neighbour=[]
    for i in range (len(Source)):
        k=Neighbours[i]
        k=list(set(k))
        Neighbour.append(k)
        
    df_output = pd.DataFrame(
         {'Source' : Source,
          'Neighbour' : Neighbour})
        
    #Save to pickle file
    if to_pickle == True:
        df_output.to_pickle('adjacency_list.pickle')
    
    
    return df_output

path = "WikipediaPhysicistsTSE210909/output210909/"
doc_extract(path,to_pickle=True)

    
    
    
    
    
    
    
