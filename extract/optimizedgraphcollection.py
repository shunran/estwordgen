#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013
@author: lauri
'''
from extract.graph import *
from collections import Counter
import re
import pickle
from collections import OrderedDict

class OptimizedGraphCollection():
    def __init__(self, wordFile = None, length = None):
        self.wordFile = wordFile
        self.length = length

    def openWords(self):
        return open(self.wordFile, 'r', encoding="latin1") # encoding="utf-8"
    
    def scanWords(self):
        stream = self.openWords()
        tempArr = Counter()
        for word in stream:
            lastChar = None
            for char in word:
                # '!' and '\n' should always be final chars in word, so everything is reset anyway
                # \' is considered omittable so let's go continue as it was nonexistant
                if re.match('[\n\!\']', char):
                    continue
                if re.match('[\ \-]', char):
                    lastChar = None
                    continue
                '''
                sõnavahe on - ja tühik
                selle sõnaga on ühel pool \n ja \!
                '''
                if re.match('\!', char):
                    print (word)
                if not re.match("[a-zA-Z0-9\xF5\xE4\xF6\xFC\xF0\xFE\xD0\xE9\-\_\ \!\'\n]", char):
                    '''
                    -\
                    õ = F5, '0x151'
                    ä = E4
                    ö = F6
                    ü = FC
                    Õ = ..
                    Ä = ..
                    Ö = ..
                    Ü = ..
                    š = F0
                    ž = FE
                    - = 2D
                    space = 20
                    ! = 21
                    Š = D0
                    ' = 27
                    é = E9
                    '''
                    print ("Mingi imelik sõna: %s ja täht '%s' koodiga %s" % (word, char, ord(char)))
                if lastChar:
                    tempArr[lastChar + char] += 1
                else:
                    pass
                    #tempArr[char] += 1
                lastChar = char
        self.calculateWeightedTotal(tempArr)

    def calculateWeightedTotal(self, counter):
        # TODO: should we do all letter and two-letter dictionaries?
        # TODO: for bisect we'd rather use sorted lists of lists
        total = sum(counter.values())
        # in case we need counters ordered, but probably not
        #counter = OrderedDict(sorted(counter.items(), key=lambda t: t[1], reverse=False))
        tempGeneratorDict= {}
        tempProbabilityDict = {}
        runningTotal = 0
        for item in counter.items():
            runningTotal += item[1]
            probability = item[1] / total * 100
            '''tempGeneratorDict[runningTotal] = { 'value' : item[0],
                                       'count' : item[1], 
                                       'probability' : probability }
            '''
            tempGeneratorDict[runningTotal] = item[0]
            tempProbabilityDict[item[0]] = probability
        self.probabilityDict = OrderedDict(sorted(tempProbabilityDict.items(), key=lambda t: t[0], reverse=False))
        self.generatorDict = OrderedDict(sorted(tempGeneratorDict.items(), key=lambda t: t[0], reverse=False))

    def save(self, fileName, collection):
        outStream = open(fileName, 'wb')
        pickle.dump(collection, outStream)
        outStream.close()

    def loadGenerator(self, fileName):
        self.generatorDict = pickle.load(fileName)

    def loadProbability(self, fileName):
        self.probabilityDict = pickle.load(fileName)

    def findProbability(self, chars):
        return (self.probabilityDict[chars] if chars in 
                            self.probabilityDict else None)

    def findWord(self, len):
        total = next(reversed(self.generatorDict))
        import random
        import bisect
        rnd = random.random() * total
        print('keys: %s' % list(self.generatorDict.keys() ))
        key = bisect.bisect_right(list(self.generatorDict.keys()), rnd)
        print('bisect random: %s' % key)
        return self.generatorDict[key]

    def writeWords(self, fileName):
        stream = self.openWords()
        outStream = open(fileName, 'w')
        for word in stream:
            outStream.write(word)
