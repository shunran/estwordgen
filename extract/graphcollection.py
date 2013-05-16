#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013
@author: lauri
'''
from extract.graph import *
from extract.frequencytree import FrequencyTree
from collections import Counter
import re
import pickle
from collections import OrderedDict
import random
import bisect

class GraphCollection():
    frequencyTree = FrequencyTree()

    def openWords(self, fileName):
        return open(fileName, 'r', encoding="utf-8")
    
    def isAllowedChar(self, character):
        ''' latin2 charset:
            -\;õ = F5, '0x151'; ä = E4; ö = F6; ü = FC; Õ = ..;
              Ä = ..; Ö = ..; Ü = ..; š = F0; ž = FE; - = 2D;
              space = 20; ! = 21; Š = D0; ' = 27; é = E9
        '''
        if re.match("[a-zA-Z0-9\xF5\xE4\xF6\xFC\xF0\xFE\xD0\xE9\-\_\ \!\'\n]", character):
            return True
        return False

    def isWordEnd(self, character):
        # this is agreed word ending without newline
        if re.match('[\ \-\_\!]', character):
            return True
        return False
    
    def isOmittableChar(self, character):
        # apostrophe is considered omittable so let's go continue as it was nonexistant
        if re.match('[\']', character):
            return True
        return False

    def scanWords(self, fileName, length):
        from collections import deque
        stream = self.openWords(fileName)
        freqDict = {}
        self.dict = freqDict
        for word in stream:
            word = word.rstrip('\n')
            charQue = deque('#' * length, maxlen = length)
            for character in word:
                if self.isOmittableChar(character):
                    print ('isomittable: %s' % character)
                    continue
                if self.isWordEnd(character):
                    charQue = deque('#' * length, maxlen = length)
                    continue
                if not self.isAllowedChar(character):
                    raise Exception("Mingi imelik sõna: %s ja täht '%s' koodiga %s" % (word, character, ord(character)))
                charQue.append(character)
                self.recursiveScan(list(charQue), freqDict)
        self.createSets(freqDict)
        #from pprint import pprint
        #pprint(freqDict)

    def recursiveScan(self, charList, dictPart):
        if not charList:
            return
        else:
            key = charList[0]
            #print ('Characters: %s Key: %s' % (charList,key))
            if key in dictPart.keys():
                #print("key oli olemas")
                dictPart[key]['count'] +=1
                #print('saime: %s' % self.dict)
            else:
                #print("lisame: %s siia: %s" % (key, dictPart))
                dictPart[key] = { 'count' : 1, 'next' : {} }
                #print('saime: %s' % self.dict)
            return self.recursiveScan(charList[1:], dictPart[key]['next'])

    def createSets(self,freqDict):
        result = {}
        for key in freqDict:
            if len(freqDict[key]['next']):
                total = sum( v['count'] for v in freqDict[key]['next'].values())
                charName  = []
                charCount = []
                runningTotal = 0
                for k, v in freqDict[key]['next'].items():
                    runningTotal += v['count']
                    charCount.append(runningTotal)
                    charName.append(k)
            result[key] = (total, charName, charCount)
        self.generateStart(result)
        return result
    
    def generateStart(self, quickDict):
        print(quickDict['#'])
        startTuple = quickDict['#']
        print('startTuple: %s' % startTuple)
        random = random.random() * startTuple[0]
        print("random: %s" % random)
        letter = startTuple[2][bisect.bisect_right(startTuple[1])]
        print(letter)
                              
    
    def generateWord(self, quickDict):
        pass
    

    def recursiveSet(self, freqDict, set = []):
        return set
    def calculateWeightedTotal(self, counter):

        # TODO: should we do all letter and two-letter (for trigraphs) dictionaries?
        # TODO: for bisect we'd maybe rather use sorted lists of lists?
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
