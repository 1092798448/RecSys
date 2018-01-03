# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 13:04:07 2018

@author: lanlandetian
"""

import math

def GetRecommendation(result, user, N = 5000):
    rank = result[user]
    ret = []
    if len(rank)  > N:
        for item,rating in rank:
            ret.append((item,rating))
    else:
        ret = rank
    return ret
    
def Recall(train,test,result,N = 5000):
    hit = 0
    all = 0
    for user in test.keys():
        tu = test[user]
        rank = GetRecommendation(result, user, N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)
    
def Precision(train, test,result, N = 5000):
    hit = 0
    all = 0
    for user in test.keys():
        tu = test[user]
        rank = GetRecommendation(result,user,N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += len(rank)
    return hit / (all * 1.0)
    
def Coverage(train, test, result, N = 5000):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user].keys():
            all_items.add(item)
            
    for user in test.keys():
        rank = GetRecommendation(result,user,N)
        for item , pui in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)
    
    
def Popularity(train, test, result, N = 5000):
    item_popularity = dict()
    for user, items in train.items():
        for item in items.keys():
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    
    ret = 0
    n = 0
    for user in test.keys():
        rank = GetRecommendation(result,user,N)
        for item,pui in rank:
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret