# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:31:18 2018

@author: QITAO SHEN
"""

import os
import nltk
from nltk.tokenize import word_tokenize
import string
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
import numpy as np
import json
from nltk.stem import PorterStemmer
ps = PorterStemmer()

Newspath='D:\pythonCode\\20news-18828'
folders=[f for f in os.listdir(Newspath)]
#print(folders)



files=[]
for folderName in folders:
    folderPath=os.path.join(Newspath,folderName)
    files.append([f for f in os.listdir(folderPath)])   
#print(sum(len(files[i])for i in range(20)))
    
pathname_list=[]
for fo in range(len(folders)):
    for fi in files[fo]:
        pathname_list.append(os.path.join(Newspath,os.path.join(folders[fo],fi)))
#print(len(pathname_list))

Y=[]
for folderName in folders:
    folderPath=os.path.join(Newspath,folderName)
    for i in range(len(os.listdir(folderPath))):
        Y.append(folderName)
#print(len(Y))
 
doc_train, doc_test, Y_train, Y_test = train_test_split(pathname_list, Y, random_state=0, test_size=0.25)
    
def tokenize(path):
    f=open(path,'r',encoding='UTF-8',errors='ignore').read()
    sents=nltk.sent_tokenize(f)
    doc_words=[]
    for sent in sents:
        doc_words.append(tokenize_sentence(sent))
    return doc_words
        
def tokenize_sentence(sent):
    words=nltk.word_tokenize(sent)
    words=process(words)
    return words

def process(words):
     table = str.maketrans('', '', '\t')
     words = [word.translate(table) for word in words]
     punctuations = (string.punctuation).replace("'", "")
     trans_table = str.maketrans('', '', punctuations)
#     print(words)
     stripped_words = [word.translate(trans_table) for word in words]
#     print(words)
     words = [str for str in stripped_words if str]
     p_words = []
     for word in words:
         if(word[0] and word[-1]=="'"):
             word=word[1:-1]
         elif(word[0]=="'"):
             word=word[1:len(word)]
         else:
             word=word
         p_words.append(word)
     words=p_words.copy()  
  

     words = [word for word in words if not word.isdigit()]
#     print(words)
     words = [word for word in words if not len(word) == 1]
#     print(words)
     words = [str for str in words if str]
#     print(words)
     words = [word for word in words if len(word) > 2]
#     print(words)
     words = [word.lower() for word in words]
#     print(words)
     for word in words:
         word=ps.stem(word)
     stopWords=set(stopwords.words('english'))
     words=[word for word in words if not word in stopWords]
#     print(words)
     return words
 
def flatten(list):
    new_list=[]
    for i in list:
        for j in i:
            new_list.append(j)
            
    return new_list

list_of_words = []
for document in pathname_list:
#        print(document)
        list_of_words.append(flatten(tokenize(document)))

np_list_of_words=np.asarray(flatten(list_of_words))
words,counts=np.unique(np_list_of_words,return_counts=True)
freq,wrds=(list(i)for i in zip(*(sorted(zip(counts,words),reverse=True))))
features=[]

for i in range(len(wrds)):
    if freq[i]<=7000 and freq[i]>=10:
        features.append(wrds[i])

dictionary = {}
doc_num = 1
for doc_words in list_of_words:
    np_doc_words=np.asarray(doc_words)
    w,c=np.unique(np_doc_words,return_counts=True)
    dictionary[doc_num]={}
    for i in range(len(w)):
        dictionary[doc_num][w[i]]=c[i]
    doc_num=doc_num+1

#homework1
Train=[]
for k in dictionary.keys():
    row=[]
    for f in features:
        if(f in dictionary[k].keys()):
            row.append(dictionary[k][f])
        else:
            row.append(0)
    Train.append(row)
'''
for doc_words in list_of_words:
    #print(doc_words)
    #np_doc_words = np.asarray(doc_words)
    #w, c = np.unique(np_doc_words, return_counts=True)
    #w,c=np.unique(doc_words,return_counts=True)
    freq_dist=nltk.FreqDist(doc_words)
    num_words=len(freq_dist.values())
    dictionary[doc_num] = {}
    #for i in range(len(w)):
     #   dictionary[doc_num][w[i]] = c[i]
    for k in freq_dist:
        dictionary[doc_num][k]=freq_dist[k]
    js=json.dumps(dictionary[doc_num])
    #file=open('D:\\dictionary\\'+os.path.basename(pathname_list[doc_num-1])+'dic.txt','w')
    str1=pathname_list[doc_num-1]
    str2=str1.replace(Newspath,'D:\pythonCode\pythondic')
    str3=str2.replace(os.path.basename(pathname_list[doc_num-1]),'')
    folder=os.path.exists(str3)
    if not folder:
        os.makedirs(str3)
    file=open(str3+os.path.basename(pathname_list[doc_num-1])+'dic.txt','w')
    file.write(js)
    file.close()
    print(doc_num,'/',len(list_of_words))
    doc_num = doc_num + 1
'''
    


















    
