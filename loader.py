#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 16:07:20 2022

@author: fanchao
"""

import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
import re

nltk.download('punkt')

# load nltk's English stopwords as variable called 'stopwords'

nltk.download('stopwords') 

stopwords = nltk.corpus.stopwords.words('english')


# read the dataset
df = pd.read_pickle('pickle.pickle')

# load nltk's SnowballStemmer as variabled 'stemmer', returns words without tense and grammar
stemmer = SnowballStemmer("english")

def tokenize(text,stem=False):
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
        return filtered_tokens

