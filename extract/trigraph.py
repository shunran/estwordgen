#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013
@author: lauri
'''
from collections import OrderedDict
from extract.graph import *

class TriGraph(Graph):

    frequency = {}
    
    def scanWords(self):
        '''
        TODO: tühikud minema lastChar või char kohtade pealt
        '''
        stream = self.openWords()
        for word in stream:
            lastChar, beforeLastChar = None, None
            for char in word.strip():
                if not lastChar:
                    beforeLastChar = None
                    lastChar = char
                    continue

                if not beforeLastChar:
                    #print ("lastChar: %s, sõna: %s täht: %s" % (lastChar, word, char))
                    beforeLastChar = lastChar
                    lastChar = char
                    continue

                '''if (beforeLastChar + lastChar + char) == 'kkk':
                    print("Kolm %s k-d: %s" % (beforeLastChar + lastChar + char, word))
                '''
                if beforeLastChar + lastChar + char in self.frequency:
                    self.frequency[beforeLastChar + lastChar + char] += 1
                else:
                    self.frequency[beforeLastChar + lastChar + char] = 1
                beforeLastChar = lastChar
                lastChar = char

    def sort(self):
        self.frequency = OrderedDict(sorted(self.frequency.items(),
                                            key=lambda t: t[1], reverse=True))
        #self.frequency = list(sorted(self.frequency, key=self.frequency.__getitem__, reverse=True))

    def printFrequency(self):
        print (self.frequency)
    
    def printWords(self):
        stream = self.openWords()
        for word in stream:
            print (word)
    
    def writeWords(self, fileName):
        stream = self.openWords()
        outStream = open(fileName, 'w')
        for word in stream:
            outStream.write(word)

