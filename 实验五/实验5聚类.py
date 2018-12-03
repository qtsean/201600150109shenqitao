# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 15:41:47 2018

@author: QITAO SHEN
"""

import nltk
import numpy as np
import json
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords

from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture

from sklearn import metrics

def flatten(list_):
    new_list=[]
    for i in list_:
        for j in i:
            new_list.append(j)
            
    words=[]
    for word in new_list:
        if word not in words:
            words.append(word)
    return words

def tokenize_sentence(sent):
    words=nltk.word_tokenize(sent)
    return words

def vectorize_sequences(sequences,dimension=10000):
    results=np.zeros((len(sequences),dimension))
    for i,sequence in enumerate(sequences):
        results[i,sequence]=1
    return results

tweetsPath='D:\\pythonCode\\实验5tweets\\Homework5Tweets.txt'
file=open(tweetsPath,'r',encoding='UTF-8',errors='ignore')
tweets=[]
count=0
for line in file:
    tweets.append(json.loads(line))
    
doc_text=[]
doc_word=[]
label_true=[]
for dictionary in tweets:
    doc_text.append(dictionary['text'])
    doc_word.append(tokenize_sentence(dictionary['text']))
    label_true.append(dictionary['cluster'])

word_bag=flatten(doc_word)

doc_vector=[]
for doc in doc_word:
    current_doc=[]
    for word in doc:
        current_doc.append(word_bag.index(word))
    doc_vector.append(current_doc)

data=vectorize_sequences(doc_vector,len(word_bag))

cluster_num=max(label_true)





##############################################################################
#compute area

#KMeans
#estimator = KMeans(n_clusters=cluster_num)
#estimator.fit(data)
#label_pred = estimator.labels_
#centroids = estimator.cluster_centers_
#print('cluster_number: ',len(centroids))

#affinity propagation
#af = AffinityPropagation().fit(data)
#cluster_centers_indices = af.cluster_centers_indices_
#label_pred = af.labels_
#n_clusters_ = len(cluster_centers_indices)
#print('cluster_number: ',n_clusters_)

#MeanShift
bandwidth = estimate_bandwidth(data)
ms = MeanShift(bandwidth=bandwidth)
ms.fit(data)
label_pred = ms.labels_
cluster_centers = ms.cluster_centers_
labels_unique = np.unique(label_pred)
n_clusters_ = len(labels_unique)
print("cluster_number: ",n_clusters_)

#spectral clustering
#label_pred = SpectralClustering().fit_predict(data)
#print("cluter number: ",len(np.unique(label_pred)))

#Ward hierarchical clustering
#n_clusters = cluster_num  
#ward = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
#ward.fit(data)
#label_pred=ward.labels_
#print ("cluster number: ", np.unique(label_pred).size)

#Agglomerative clustering
#model = AgglomerativeClustering(linkage='ward',n_clusters=cluster_num)
#model.fit(data)
#label_pred=model.labels_
#print("cluster number: ",len(np.unique(model.labels_)))

#DBSCAN
#model=DBSCAN()
#model.fit(data)
#label_pred=model.labels_
#print("cluster number: ",len(np.unique(model.labels_)))

#Gaussian mixtures
#model=GaussianMixture(n_components=6, covariance_type='full')
#model.fit(data)
#label_pred=model.predict(data)
#
#print("cluster number: ",len(np.unique(label_pred)))


##############################################################################

print('meanShift score: ',metrics.normalized_mutual_info_score(label_true, label_pred))

























