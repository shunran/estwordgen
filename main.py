#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on Feb 19, 2013

@author: lauri
'''
from collections import OrderedDict
from extract.digraph  import *
from extract.trigraph  import *
from extract.length import *
from extract.starttrigraph import *
import pickle
import random
import cgitb
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Main:
    #cgitb.enable()
    diGraphFreq  = None
    triGraphFreq = None
    lengthFreq   = None
    startFreq   = None

    def run(self):
        ##print ("Content-type:text/html;encoding=UTF-8\n\n")
        '''
        print('Digraafid:')
        for i in range(8):
            print ("Sõna: %s" % self.getNaiveDigraph(8))

        print("\nTrigraafid:")
        for i in range(8):
            print ("Sõna: %s" % self.getNaiveTrigraph(8))
            
        print("\nJuhusliku pikkusega trigrammid:")
        for i in range(8):
            wordlen = random.choice(self.lengthFreq)
            print ("Pikkus: %s Sõna: %s" % (wordlen, self.getNaiveTrigraph(wordlen)))      
        '''
        print("\nPseudojuhusliku pikkusega ja kaalutud algusega trigrammid:")
        for i in range(8):
            wordlen = random.choice(self.lengthFreq)
            print ("Pikkus: %s Sõna: %s" % (wordlen, self.getNaiveTrigraph(wordlen, True)))

    def getNaiveDigraph(self, length):
        string = random.choice(self.diGraphFreq)
        err = None
        for i in range(length - 2):
            limitedChoice = []
            for word in self.diGraphFreq:
                '''bugfix for bad frequency list '''
                if word[0] == string[-1] and len(word) == 2:
                    limitedChoice += [word]
            a = random.choice(limitedChoice)
            string = string[:-1] + a
            #print ("string: %s valik: %s" % (string, a))
        return string
    
    def getNaiveTrigraph(self, length, weightedStart = False):
            string = self.getStart(weightedStart)
            for j in range(length - 3):
                limitedChoice = []
                for word in self.triGraphFreq:
                    if word[0] == string[-2] and word[1] == string[-1]:
                        limitedChoice += [word]
                string = string[:-2] + random.choice(limitedChoice)
            return  string

    def getStart(self, weightedStart):
        if weightedStart:
            return random.choice(self.startFreq)
        return random.choice(self.triGraphFreq)

    def save(self):
        lemmad = 'resource/lemmad.txt'
        '''
        print ("salvestan Digraafid")
        digraph = DiGraph(lemmad)
        digraph.scanWords()
        digraph.saveFrequency('resource/digraph.pck')
        
        print ("salvestan Trigraafid")
        trigraph = TriGraph(lemmad)
        trigraph.scanWords()
        trigraph.saveFrequency('resource/trigraph.pck')
        
        print ("salvestan Sõnapikkused")
        wordlen = Length(lemmad)
        wordlen.scanWords()
        wordlen.saveFrequency('resource/length.pck')
        '''
        print ("salvestan sõnade alguse trigraafid")
        start = StartTriGraph(lemmad)
        start.scanWords()
        start.saveFrequency('resource/start.pck')
        
    def load(self):
        #print ("laen Digraafid")
        inFile = open('resource/digraph.pck', 'rb')
        self.diGraphFreq = pickle.load(inFile)
        
        #print ("laen Trigraafid")
        inFile = open('resource/trigraph.pck', 'rb')
        self.triGraphFreq = pickle.load(inFile)
        
        #print ("laen Sõnapikkused")
        inFile = open('resource/length.pck', 'rb')
        self.lengthFreq = pickle.load(inFile)
        
        #print ("laen sõnade alguse trigraafid")
        inFile = open('resource/start.pck', 'rb')
        self.startFreq = pickle.load(inFile)
        
    def getRandomLength(self):
        return random.choice(self.lengthFreq)

        
if __name__ == '__main__':
    app = Main()
    #app.save()
    app.load()
    app.run()
