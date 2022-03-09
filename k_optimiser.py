#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 21:04:24 2022

@author: fanchao
"""

from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import numpy as np


def elbow(tfidf_matrix):
    model = KMeans()
    # k is range of number of clusters.
    K = []
    for i in range(10):
        visualizer = KElbowVisualizer(model, k=(2,10), timings= False)
        visualizer.fit(tfidf_matrix)        # Fit data to visualizer   
        #visualizer.show()                                # Finalize and render figure
        k = visualizer.elbow_value_
        K.append(k)
    
    return np.mean(K),np.std(K)


def silhouette(X):
    range_nclusters = []
    for i in range(2,10):
        range_nclusters.append(i)
    
    Silhouette = []
    for n_clusters in range_nclusters:
        clusterer = KMeans(n_clusters=n_clusters)
        cluster_labels = clusterer.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        Silhouette.append(silhouette_avg)
        
    return Silhouette
        
    
