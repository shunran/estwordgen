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

class DiGraph(Graph):
    #frequency = {}
    frequency = Counter()
    firstChar = Counter()
    lastChar = Counter()

    def __init__(self, wordFile):
        self.wordFile = wordFile

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
                    tempArr[char] += 1
                lastChar = char
        self.frequency = tempArr
    
    def printWords(self):
        stream = self.openWords()
        for word in stream:
            print (word)
    
    def writeWords(self, fileName):
        stream = self.openWords()
        outStream = open(fileName, 'w')
        for word in stream:
            outStream.write(word)

