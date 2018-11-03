# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 18:37:25 2018

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
#    stopWords=set(stopwords.words('english'))
#    words=[word for word in words if not word in stopWords]
    Words=[]
    for w in words:
        if w not in Words:
            Words.append(w)
    return Words
    
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

def merge(query):
    words=nltk.word_tokenize(query)
    words=process(words)
    if 'and' in query:
#        w1=process(words[0])
        w1=words[0]
#        w2=process(words[2])
        w2=words[2]
        return mergeAnd(w1,w2)
    elif 'or' in query:
#        w1=process(words[0])
        w1=words[0]
#        w2=process(words[2])
        w2=words[2]
        return mergeOr(w1,w2)
    elif 'not' in query:
#        w1=process(words[1])
        w1=words[1]
        return mergeNot(w1)
    else:
        print('wrong query')
    
    
def mergeAnd(w1,w2):
    if w1 not in word_bag or w2 not in word_bag:
        print('No result')
        return
    lst=[]
    p1=1
    p2=1
    while True:
        if p1==len(word_dic[w1]):
            break
        if p2==len(word_dic[w2]):
            break
        if word_dic[w1][p1]<word_dic[w2][p2]:
            p1+=1
        elif word_dic[w1][p1]>word_dic[w2][p2]:
            p2+=1
        elif word_dic[w1][p1]==word_dic[w2][p2]:
            lst.append(word_dic[w1][p1])
            p1+=1
            p2+=1
        else:
            pass
    return lst
def mergeOr(w1,w2):
    if w1 not in word_bag and w2 not in word_bag:
        print('No result')
        return
    lst=[]
    p1=1
    p2=1
    while True:
        if word_dic[w1][p1]<word_dic[w2][p2]:
            lst.append(word_dic[w1][p1])
            p1+=1
            if p1==len(word_dic[w1]):
                while p2<len(word_dic[w2]):
                    lst.append(word_dic[w2][p2])
                    p2+=1
                return lst
        if word_dic[w1][p1]>word_dic[w2][p2]:
            lst.append(word_dic[w2][p2])
            p2+=1
            if p2==len(word_dic[w2]):
                while p1<len(word_dic[w1]):
                    lst.append(word_dic[w1][p1])
                    p1+=1
                return lst
        if word_dic[w1][p1]==word_dic[w2][p2]:
            lst.append(word_dic[w1][p1])
            p1+=1
            p2+=1
            if p1==len(word_dic[w1]):
                while p2<len(word_dic[w2]):
                    lst.append(word_dic[w2][p2])
                    p2+=1
                return lst
            if p2==len(word_dic[w2]):
                while p1<len(word_dic[w1]):
                    lst.append(word_dic[w1][p1])
                    p1+=1
                return lst
def mergeNot(w1):
    lst=[]
    if w1 not in word_bag:
        for i in range(1,len(doc_word)):
            lst.append(i)
        return lst
    newlst=[]
    for i in range(1,len(word_dic[w1])):
        newlst.append(word_dic[w1][i])
    for i in range(1,len(doc_word)+1):
        if i not in word_dic[w1]:
            lst.append(i)
    return lst
    
    
    

    
tweetsPath='D:\\pythonCode\\Homework3-tweets\\tweets.txt'
file=open(tweetsPath,'r',encoding='UTF-8',errors='ignore')
#js=file.read()
tweets=[]
count=0
for line in file:
#    count+=1
#    print(count)
    tweets.append(json.loads(line))

#count=0
doc_word=[]
for dictionary in tweets:
    doc_word.append(tokenize_sentence(dictionary['text']))
#    count+=1
#    print(count)
word_bag=[]
word_bag=flatten(doc_word)
word_dic={}
tweet_num=0
for tweet in doc_word:
    tweet_num+=1
    for word in tweet:
        if word in word_dic.keys():
            #列表的第一个值为频数
            word_dic[word][0]+=1
            word_dic[word].append(tweet_num)
        else:
            word_dic[word]=[]
            word_dic[word].append(1)
            word_dic[word].append(tweet_num)
           


































#dic=json.loads(js)
#print(dic)
#file.close()
