#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:34:22 2022

@author: fanchao
"""
#external libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

#self-written libraries
import doc_extractor as de
import language_processor as lp


path = "WikipediaPhysicistsTSE210909/output210909/"
df = de.doc_extract(path = path)
df2 = de.get_adjacency(df)
stopwords = lp.get_stopwords()

texts = df['Text']

tokens = []
stems = []
for i in texts:
    tokens.extend(lp.tokenize(i,stem=False))
    stems.extend(lp.tokenize(i))
 
stop_stems =[]    
for i in stopwords:
    stop_stems.append(lp.tokenize(i,stem=True)[0])

word_frame = pd.DataFrame({'words':tokens},index=stems)


#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words=stop_stems,
                                 use_idf=True, tokenizer=lp.tokenize, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(texts) #fit the vectorizer to synopses

num_clusters = 14

terms = tfidf_vectorizer.get_feature_names_out()

dist = 1 - cosine_similarity(tfidf_matrix)


km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

#save and reload the model here
#joblib.dump(km,  'doc_cluster.pkl')
#km = joblib.load('doc_cluster.pkl')
#clusters = km.labels_.tolist()

name = df['Name'].tolist()
text = df['Text'].tolist()
frame={'Name':name,'Text':text,'Cluster':clusters}
frame = pd.DataFrame(frame,index=[clusters],columns=['Name','Text','Cluster'])

#sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

cluster_words = []
for i in range(num_clusters):
    tem_list = []
    for ind in order_centroids[i, :8]: #replace 6 with n words per cluster
        keyword = word_frame.loc[terms[ind].split(
            ' ')].values.tolist()[0][0].encode('utf-8','ignore').decode()
        tem_list.append(keyword)
    
    cluster_words.append(tem_list)


frame = frame.sort_values(by=['Cluster'])
insert_colname = 'Cluster Keywords'
frame['Cluster Keywords']='--'
frame['Cluster Keywords'] = frame['Cluster Keywords'].astype('object')
frame.reset_index(inplace=True)

for i in range(num_clusters):
    for j in range(len(frame)):
        if frame['Cluster'][j] != i:
            continue
        elif frame['Cluster'][j] == i:           
            frame.at[j,'Cluster Keywords'] = cluster_words[i]
            break
            
frame.to_excel('Grouped File.xlsx') #output to file




















