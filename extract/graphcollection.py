#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013
@author: lauri
'''

''' 
Äkki peaks vana koodi põhjal mingid sõnad genereerima ja koodi ise minema viskama
tõenäosusprotsent ikkagi tähendab just protsenti, et mingile tähele või täheühendile järgneb
just see kindel täht. Kogu sõna peale tehakse diskreetne jaatus kõikide tähtede järgnevuse peale e. korrutatakse nad läbi.
Rekursiivne täheühendite pikkusest sõltumatu skänner

# TODO:
jääda trigraafide juurde, kuidas põhjendada?
sõnaalguse algoritm viia kahetäheliseks
'''
import re
import pickle
import random
import bisect
from pprint import pprint
from collections import deque, OrderedDict

class GraphCollection():

    quickDict = None
    """ dictionary for quick binary search of weighted averages
        {'char': (total, ['next character', ...], 
                     [next character weight, ...], 
                     [next character possibility, ...]),
    """
    freqDict = None
    """ Markov Chain tree of character following possibility and probability.
        '#' key marks word beginning
     'a': {'count': 2,
       'next': {'p': {'count': 1, 'next': {'e': {'count': 1, 'next': {}}}},
                'v': {'count': 1, 'next': {'e': {'count': 1, 'next': {}}}}}},

    """

    def scanWords(self, fileName, length):
        def openWordFile(fileName):
            return open(fileName, 'r', encoding="utf-8")
    
        def isAllowedChar(character):
            ''' latin2 charset:
                -\;õ = F5, '0x151'; ä = E4; ö = F6; ü = FC; Õ = ..;
                  Ä = ..; Ö = ..; Ü = ..; š = F0; ž = FE; - = 2D;
                  space = 20; ! = 21; Š = D0; ' = 27; é = E9
            '''
            if re.match("[a-zA-Z0-9\xF5\xE4\xF6\xFC\xF0\xFE\xD0\xE9\-\_\ \!\'\n]", character):
                return True
            return False

        def isWordEnd(character):
            """this is agreed virtual word ending without newline"""
            if re.match('[\ \-\_\!]', character):
                return True
            return False
    
        def isOmittableChar(character):
            """ letter that are considered omittable,
            to continue as if it was non-existant
            """
            if re.match('[\']', character):
                return True
            return False
        """ Main part of the method """
        stream = openWordFile(fileName)
        freqDict = {}
        for word in stream:
            word = word.rstrip('\n')
            charQue = deque('#', maxlen = length)
            for character in word:
                if isOmittableChar(character):
                    print ('isomittable: %s' % character)
                    continue
                if isWordEnd(character):
                    charQue = deque('#', maxlen = length)
                    continue
                if not isAllowedChar(character):
                    raise Exception("Mingi imelik sõna: %s ja täht '%s' koodiga %s" % (word, character, ord(character)))
                charQue.append(character)
                if len(charQue) == length:
                    self.recursiveScan(list(charQue), freqDict)
        self.freqDict = freqDict
        #self.create2GQuickDict(freqDict)
        #self.create3GQuickDict(freqDict)

    def recursiveScan(self, charList, dictPart):
        if not charList:
            return
        else:
            key = charList[0]
            if key in dictPart.keys():
                dictPart[key]['count'] +=1
            else:
                dictPart[key] = { 'count' : 1, 'next' : {} }
            return self.recursiveScan(charList[1:], dictPart[key]['next'])

    def createQDRow(self, freqDictSlice):
        total = sum(v['count'] for v in freqDictSlice['next'].values())
        charName = []
        charCount = []
        charProbability = []
        runningTotal = 0
        for k, v in freqDictSlice['next'].items():
            runningTotal += v['count']
            charProbability.append(v['count'] / total * 100)
            charCount.append(runningTotal)
            charName.append(k)  
        return total, charName, charCount, charProbability

    def create2GQuickDict(self):
        freqDict = self.freqDict
        result = {}
        for char1, item in freqDict.items():
            total, charName, charCount, charProbability = self.createQDRow(item)
            result[char1] = total, charName, charCount, charProbability
        return result
    
    def create3GQuickDict(self):
        freqDict = self.freqDict
        result = {}
        for char1, item1 in freqDict.items():
                for char2, item2 in item1['next'].items():
                    result[char1 + char2] = self.createQDRow(item2)
        return result
    
    def findRandomStart(self, quickDict):
        return self.findRandomCharacter(quickDict['#'])
    
    def findRandomCharacter(self, qdSlice):
        rnd = random.random() * qdSlice[0]
        character = qdSlice[1][bisect.bisect_right(qdSlice[2], rnd)]
        return character

    def generateWord(self, length):
        quickDict = self.quickDict
        word = self.findRandomStart(quickDict)
        prevSlice = quickDict[word]
        for i in range(length):
            nextChar = self.findRandomCharacter(prevSlice)
            word += nextChar
            prevSlice = quickDict[nextChar]
        return word

    def save(self, fileName, collection):
        outStream = open(fileName, 'wb')
        pickle.dump(collection, outStream)
        outStream.close()

    def load(self, fileName):
        return pickle.load(fileName)

    ''' FROM HERE FORWARD OLD NOT REFACTORED CODE '''
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
        stream = self.openWordFile()
        outStream = open(fileName, 'w')
        for word in stream:
            outStream.write(word)
