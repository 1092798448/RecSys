# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:51:55 2018

@author: lanlandetian
"""

import random
import operator

allItemSet = set()
def InitAllItemSet(user_items):
    allItemSet.clear()
    for user, items in user_items.items():
        for i, r in items.items():
            allItemSet.add(i)

def InitItems_Pool(items):
    interacted_items = set(items.keys())
    items_pool = list(allItemSet - interacted_items)
#    items_pool = list(allItemSet)
    return items_pool

def RandSelectNegativeSample(items):
    ret = dict()
    for i in items.keys():
        ret[i] = 1
    n = 0
    for i in range(0,len(items) * 3):
        items_pool = InitItems_Pool(items)
        item = items_pool[random.randint(0,len(items_pool) - 1 )]
        if item in ret:
            continue
        ret[item] = 0
        n += 1
        if n > len(items):
            break
    return ret

def Predict(user,item,P,Q):
    rate = 0
    for f,puf in P[user].items():
        qif = Q[item][f]
        rate += puf * qif
    return rate


def InitModel(user_items,F):
    P = dict()
    Q = dict()
    for user, items in user_items.items():
        P[user] = dict()
        for f in range(0,F):
            P[user][f] = random.random()
        for i,r in items.items():
            if i not in Q:
                Q[i] = dict()
                for f in range(0,F):
                    Q[i][f] = random.random()
    return P,Q



def LatentFactorModel(user_items, F,T, alpha, lamb):
    InitAllItemSet(user_items)
    [P,Q] = InitModel(user_items, F)
    for step in range(0,T):
        for user, items in user_items.items():
            samples = RandSelectNegativeSample(items)
            for item, rui in samples.items():
                eui = rui - Predict(user, item, P,Q)
                for f in range(0,F):
                    P[user][f] += alpha * (eui * Q[item][f] - \
                        lamb * P[user][f])
                    Q[item][f] += alpha * (eui * P[user][f] - \
                        lamb * Q[item][f])
        alpha *= 0.9
    return P,Q
        
def Recommend(user,train,P,Q):
    rank = dict()
    interacted_items = train[user]
    for i in Q:
        if i in interacted_items.keys():
            continue
        rank.setdefault(i,0)
        for f,qif in Q[i].items():
            puf = P[user][f]
            rank[i] += puf * qif
    return rank
    
def Recommendation(users, train,P,Q):
    result = dict()
    for user in users:
        rank = Recommend(user,train,P,Q)
        R = sorted(rank.items(), key = operator.itemgetter(1), \
                   reverse = True)
        result[user] = R
    return result