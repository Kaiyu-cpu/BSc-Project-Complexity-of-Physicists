#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:41:46 2022

@author: fanchao
"""
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer #try lemma instead of stem!
import re


# download required resources from nltk
#only run for the first time using this code!
#nltk.download('punkt')
#nltk.download('stopwords')

def get_stopwords():
    stopwords = nltk.corpus.stopwords.words('english')

    #I will define some of my own stopwords
    extra = ['James','Robert','John','George','William','Prize','awards','theory','theoretical','der','des',
             'van','von','research','professor','Biography','Sciences','became','books','also','Institute','Physics',
             'edit','physicist']
    stopwords.extend(extra)
    
    return stopwords

# load nltk's SnowballStemmer as variabled 'stemmer', returns words without tense and grammar
stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

def tokenize(text,stem=False,lemmatize=True):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    if stem == True:
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems
    else:
        if lemmatize == True:
            lemmas = [lemmatizer.lemmatize(t,pos='v') for t in filtered_tokens]
            lemmas = [lemmatizer.lemmatize(t, pos='n') for t in lemmas]
            return lemmas
        else:
            return filtered_tokens

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        