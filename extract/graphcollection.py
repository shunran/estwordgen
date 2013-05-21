#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013
@author: lauri
'''

import re
import pickle
import random
import bisect
from pprint import pprint
from collections import deque, OrderedDict, Counter

class GraphCollection():

    quickDict = None
    """ dictionary of weighted averages for quick binary search
        {'char': (total, ['next character', ...], 
                     [next character weight, ...], 
                     [next character possibility, ...]),
    """
    freqTrie = None
    """ Markov chain trie of character following possibility and probability.
        '#' key marks word beginning
     'a': {'count': 2,
       'next': {'p': {'count': 3, 'next': {'e': {'count': 5, 'next': {'i': ...}}}},
                'v': {'count': 1, 'next': {'e': {'count': 1, 'next': {}}}}}},...

    """

    def openWordFile(self, fileName):
            return open(fileName, 'r', encoding="utf-8")

    def isAllowedChar(self, character):
        ''' latin2 charset:
            -\;õ = F5, '0x151'; ä = E4; ö = F6; ü = FC; Õ = ..;
              Ä = ..; Ö = ..; Ü = ..; š = F0; ž = FE; - = 2D;
              space = 20; ! = 21; Š = D0; ' = 27; é = E9
        '''
        if re.match("[\w\-\_\ \!\'\n]", character):
            return True
        return False

    def isWordEnd(self, character):
        """this is agreed virtual word ending without newline"""
        if re.match('[\ \-\_\!]', character):
            return True
        return False

    def isOmittableChar(self, character):
        """ letter that are considered omittable,
        to continue as if it was non-existant
        """
        if re.match('[\']', character):
            return True
        return False

    def createTrie(self, fileName, depth):
        charLength = depth + 1
        
        def recursiveScan(charList, dictPart):
            if not charList:
                return
            else:
                key = charList[0]
                if key in dictPart.keys():
                    if key != "#":
                        dictPart[key]['count'] +=1
                else:
                    count = 1
                    if key == "#":
                        count = 0
                    dictPart[key] = { 'count' : count, 'next' : {} }
                return recursiveScan(charList[1:], dictPart[key]['next'])

        """ Main part of the method """
        stream = self.openWordFile(fileName)
        freqTrie = {}
        for word in stream:
            word = word.rstrip('\n')
            charQue = deque('#' * depth, maxlen = charLength)
            for character in word:
                if self.isOmittableChar(character):
                    continue
                if self.isWordEnd(character):
                    charQue = deque('#' * depth, maxlen = charLength)
                    continue
                if not self.isAllowedChar(character):
                    raise Exception("Mingi imelik sõna: %s ja täht '%s' koodiga %s" % (word, character, ord(character)))
                charQue.append(character)
                if len(charQue) == charLength:
                    recursiveScan(list(charQue), freqTrie)
        self.freqTrie = freqTrie
        return freqTrie

    def createLengthQuickArr(self, fileName):
        def countLenghts(stream):
            lengths = Counter()
            for word in stream:
                word = word.rstrip('\n')
                length = 0
                for char in word:
                    if self.isOmittableChar(char):
                        continue
                    if self.isWordEnd(char):
                        lengths[length] += 1
                        length = 0
                        continue
                    length += 1
                if length:
                    lengths[length] += 1
            return lengths
        
        def createQD(counter):
            total = sum(v for v in counter.values())
            count = []
            value = []
            runningTotal = 0
            for k,v in counter.items():
                runningTotal += v
                count.append(runningTotal)
                value.append(k)
            return total, count, value
        
        stream = self.openWordFile(fileName)
        lengths = countLenghts(stream)
        return createQD(lengths)

    def findLength(self, quickList):
        rnd = random.random() * quickList[0]
        pos = bisect.bisect_left(quickList[1], rnd)
        return quickList[2][pos]

    def createQuickDict(self, freqTrie, keyLength = 1):
        ''' keylength must be same or smaller than trie depth '''
        def recTrieScan(trieSlice, depth, keyChars = '', result = {}):
            depth -= 1
            if depth > 0:
                for char, item in trieSlice.items():
                    recTrieScan(item['next'], depth, keyChars + char, result)
                return result
            else:
                for char, item in trieSlice.items():
                    result[keyChars + char] = createQDRow(item) 
                return result

        def createQDRow(freqDictSlice):
            total = sum(v['count'] for k,v in freqDictSlice['next'].items())
            charName = []
            charCount = []
            charProbability = []
            runningTotal = 0
            for k, v in freqDictSlice['next'].items():
                if k != '#':
                    runningTotal += v['count']
                    charProbability.append(v['count'] / total)
                    charCount.append(runningTotal)
                    charName.append(k)
            return total, charName, charCount, charProbability

        #### MAIN PART OF THE createQuickDict ###
        result = recTrieScan(freqTrie, keyLength)
        return result
    
    def findStart(self, quickDict, depth):
        charQue = deque('#' * depth, maxlen = depth)
        for i in range(depth):
            try:
                ''' TODO: sometimes key not found '''
                charQue.append(self.findCharacter(quickDict[''.join(l for l in charQue)]))
            except KeyError as e:
                break
        chars = ''.join(l for l in charQue )
        return chars
    
    def findCharacter(self, qdSlice):
        rnd = random.random() * qdSlice[0]
        character = qdSlice[1][bisect.bisect_left(qdSlice[2], rnd)]
        return character

    def findWord(self, quickDict, depth, length):
        word = self.findStart(quickDict, depth)
        while len(word) < length:
            # TODO: sometimes key not found
            try:
                prevSlice = quickDict[word[len(word) - depth :]]
                nextChar = self.findCharacter(prevSlice)
                word += nextChar
            except KeyError as e:
                break
        return word
    
    def findWordProbability(self, word, quickDict, depth):
        word = "#" + word
        probability = 1
        for position in range(len(word)):
            if position + depth < len(word):
                wordPart = word[position:depth + position]
                try:
                    qd = quickDict[wordPart]
                    nextChar = word[depth + position]
                    probability = probability * qd[3][qd[1].index(nextChar)]
                except Exception as e:
                    ''' This happens when quickDict has no such combination '''
                    #raise e
        return probability

    def save(self, fileName, collection):
        outStream = open(fileName, 'wb')
        pickle.dump(collection, outStream)
        outStream.close()
     
    def load(self, fileName):
        inFile = open(fileName, 'rb')
        return pickle.load(inFile)   
