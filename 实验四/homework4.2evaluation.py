# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 08:18:56 2018

@author: QITAO SHEN
"""


import os
import nltk
import string
import numpy as np
import json
import math
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords

from bs4 import BeautifulSoup

def process(words):
    table = str.maketrans('', '', '\t')
    words = [word.translate(table) for word in words]
    punctuations = (string.punctuation).replace("'", "")
    trans_table = str.maketrans('', '', punctuations)
    stripped_words = [word.translate(trans_table) for word in words]
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
    words = [word for word in words if not len(word) == 1]
    words = [str for str in words if str]
    words = [word for word in words if len(word) > 1]
    words = [word.lower() for word in words]
    for word in words:
         word=ps.stem(word)
    stopWords=set(stopwords.words('english'))
    words=[word for word in words if not word in stopWords]

    return words
    
def tokenize_sentence(sent):
    words=nltk.word_tokenize(sent)
    words=process(words)
    return words

def flatten(list):
    new_list=[]
    for i in list:
        for j in i:
            new_list.append(j)
    return new_list


def getQuery(qid):
    qid=str(qid)
    queryPath=r'D:\pythonCode\eval_hw4\eval_hw4\querys.txt'
    qfile=open(queryPath,'r',encoding='UTF-8',errors='ignore')
    soup=BeautifulSoup(qfile,"lxml")
    num_list=soup.find_all('num')
    oquery_list=soup.find_all('query')
    query_list=[]
    for q in oquery_list:
        q=str(q).replace("<query>","")
        q=str(q).replace("</query>","")
        query_list.append(q)
    for i in range(len(query_list)):
        if qid in str(num_list[i]):
            return query_list[i]
    
    
    
        
def VSM(q):
    query=getQuery(q)
    b=0.5
    k=3#事后删除
    tweetword=[]
    tweetword=tokenize_sentence(query)
    score=[]
    count=0
    for doc in doc_word:
        tempscore=0
        for word in tweetword:
            if word in doc:
                tempscore+=(k+1)*doc.count(word)/(doc.count(word)+k*(1-b+b*(len(doc)/avg_length)))*math.log((doc_number+1)/word_dic[word][1])
#                tempscore+=math.log(1+math.log(1+doc.count(word)))/(1-b+b*len(doc)/avg_length)*math.log(doc_number/word_dic[word][1])
        if(tempscore!=0):
            A=(count,tempscore)
            score.append(A)
        count+=1
        
    score.sort(key=lambda x:x[1],reverse=True)
    count=0
    scorelist=score[:100]
    return scorelist
        
def BM25(query):
    b=0.5
    k=3
    tweetword=[]
    tweetword=tokenize_sentence(query)
    score=[]
    count=0
    for doc in doc_word:
        tempscore=0
        for word in tweetword:
            if word in doc:
                tempscore+=(k+1)*doc.count(word)/(doc.count(word)+k*(1-b+b*(len(doc)/avg_length)))*math.log((doc_number+1)/word_dic[word][1])
        if (tempscore!=0):
            A=(count,tempscore)
            score.append(A)
        count+=1
        
    score.sort(key=lambda x:x[1],reverse=True)
    count=0
    for tweet in score:
        print(tweet)
        count+=1
        if count>100:
            break
                
    
tweetsPath='D:\\pythonCode\\实验4VSMtoBM25\\tweets.txt'
file=open(tweetsPath,'r',encoding='UTF-8',errors='ignore')
tweets=[]
count=0
for line in file:
    tweets.append(json.loads(line))

#count=0
doc_text=[]
doc_word=[]
for dictionary in tweets:
    doc_text.append(dictionary['text'])
    doc_word.append(tokenize_sentence(dictionary['text']))
#    count+=1
#    print(count)
word_bag=[]
word_bag=flatten(doc_word)
word_dic={}
posting={}
tweet_num=0
for tweet in doc_word:
    tempword=[]
    for word in tweet:
          #创建word_dic
        if word in word_dic.keys():
            #列表的第一个值为频数,第二个数为包含这个词的文档的数量
            if word not in tempword:
                word_dic[word][1]+=1
            word_dic[word][0]+=1
            tempword.append(word)
        else:
            word_dic[word]=[]
            word_dic[word].append(1)
            word_dic[word].append(1)
            tempword.append(word)
           
        #创建posting
        if word not in posting.keys():
            posting[word]={}
            posting[word][tweet_num]=1
        else:
            if tweet_num not in posting[word].keys():
                posting[word][tweet_num]=1
            else:
                posting[word][tweet_num]+=1

    tweet_num+=1
    
total_length=0
doc_length=[]
for doc in doc_word:
    doc_length.append(len(doc))
    total_length+=len(doc)
doc_number=len(doc_word)
avg_length=total_length/len(doc_word)

id_list=[]
for q in range(171,226):
    scorelist=VSM(q)
    idlist=[x[0] for x in scorelist]
    for i in idlist:
        thisID= str(q)+' '+str(tweets[i]['tweetId'])
        id_list.append(thisID)
        
fp=open('D:\\pythonCode\\eval_hw4\\eval_hw4\\MYresult2.txt','w+')
for line in id_list:
    fp.write(line+'\n')





























#dic=json.loads(js)
#print(dic)
#file.close()
