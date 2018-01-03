# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 20:36:48 2018

@author: lanlandetian
"""

import UserCF
import UserCF_IIF
import ItemCF
import ItemCF_IUF
import random
import Evaluation

import imp
imp.reload(UserCF)
imp.reload(ItemCF)
imp.reload(ItemCF_IUF)
imp.reload(Evaluation)

def readData():
    data = []
    fileName = 'u.data'
    fr = open(fileName,'r')
    for line in fr.readlines():
        lineArr = line.strip().split()
        data.append([lineArr[0], lineArr[1], 1.0])
    return data
    
    
def SplitData(data,M,k,seed):
    test = []
    train = []
    random.seed(seed)
    for user, item,rating in data:
        if random.randint(0,M-1) == k:
            test.append([user,item,rating])
        else:
            train.append([user, item,rating])
    return train, test
        
    
# 将列表形式数据转换为dict形式
def transform(oriData):
    ret = dict()
    for user,item,rating in oriData:
        if user not in ret:
            ret[user] = dict()
        ret[user][item] = rating
    return ret
    
if __name__ == '__main__':
    data = readData()
    M = 5
    precision =0
    recall = 0
    coverage = 0
    popularity =0
    for i in range(0,M):
        [oriTrain,oriTest] = SplitData(data,M,i,0)
        train = transform(oriTrain)
        test = transform(oriTest)
        W = UserCF.UserSimilarity(train)
    #    rank = UserCF.Recommend('1',train,W)
        result = UserCF.Recommendation(test.keys(), train, W)
    
#        W = UserCF_IIF.UserSimilarity(train)
    #    rank = UserCF_IIF.Recommend('1',train,W)
#        result = UserCF_IIF.Recommendation(test.keys(), train, W)
        
    #    W = ItemCF.ItemSimilarity(train)
    #    rank = ItemCF.Recommend('1',train,W)
#        result =  ItemCF_IUF.Recommendation(test.keys(),train, W)
        
#        W = ItemCF_IUF.ItemSimilarity(train)
    #    rank = ItemCF_IUF.Recommend('1',train,W)
#        result =  ItemCF_IUF.Recommendation(test.keys(),train, W)
    
        precision += Evaluation.Precision(train,test, result)
        recall += Evaluation.Recall(train,test,result)
        coverage += Evaluation.Coverage(train, test, result)
        popularity += Evaluation.Popularity(train, test, result)
       
    precision /= M
    recall /= M
    coverage /= M
    popularity /= M
    
     #运行完标志
    print('Done!')
