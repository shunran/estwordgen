#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 20, 2013
@author: lauri
'''
from collections import OrderedDict
from collections import Counter
import pickle

class Graph:
    frequency = Counter()
    firstChar = Counter()
    lastChar = Counter()

    wordFile = None

    def __init__(self, params):
        self.wordFile = params


    def openWords(self):
        return open(self.wordFile, 'r', encoding="latin2") # encoding="utf-8"
    
    def saveFrequency(self, fileName):
        choiceArr = []
        for x in self.frequency.keys():
            choiceArr += self.frequency[x] * [x]
        outStream = open(fileName, 'wb')
        pickle.dump(choiceArr, outStream)
        outStream.close()
        
    def loadFrequency(self, fileName):
        return pickle.load(fileName)

    def sortByValue(self, reverse = False):
        self.frequency = OrderedDict(sorted(self.frequency.items(),
                                            key=lambda t: t[1], reverse=reverse))

        