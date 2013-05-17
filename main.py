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
from extract.graphcollection import GraphCollection
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
    diGraphCollection = None
    triGraphCollection = None
    diGraphCounter = Counter()
    
    def run(self):               
        a = self.diGraphCollection
        probabilityFilename = 'resource/digraph_probability.pck'
        inFile = open(probabilityFilename, 'rb')
        a.loadProbability(inFile)
        self.probabilityDict = a.probabilityDict
        self.randomChoiceRun()

    def optimizedRun(self):
        print('Digraafid:')
        for i in range(8):
            print ("Sõna: %s" % self.getOptimizedDigraph(8))

    def randomChoiceRun(self):
        ##print ("Content-type:text/html;encoding=UTF-8\n\n")
        def avg(list):
            return float(sum(list)) / len(list)
        '''
        print('Digraafid:')
        probTotal = []
        for i in range(8):
            word = self.getNaiveDigraph(8)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
        probTotal = []
        print("\nTrigraafid:")
        for i in range(8):
            word = self.getNaiveTrigraph(8)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Sõna: %s  Tõenäosus: %.5f" % (word, prob) )
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
        probTotal = []           
        print("\nJuhusliku pikkusega trigrammid:")
        for i in range(8):
            wordlen = random.choice(self.lengthFreq)
            word = self.getNaiveTrigraph(wordlen)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Pikkus: %s Sõna: %s Tõenäosus: %.5f" % (wordlen, word, prob))      
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
        probTotal = []        
        print("\nPseudojuhusliku pikkusega ja kaalutud algusega trigrammid:")
        for i in range(8):
            wordlen = random.choice(self.lengthFreq)
            word = self.getNaiveTrigraph(wordlen, True)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Pikkus: %s Sõna: %s Tõenäosus: %.5f" % (wordlen, word, prob))
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
        '''
        ## NEW CODE ###
        print("Optimeeritud algoritmiga digrammid:")
        probTotal = []
        for i in range(8):
            word = self.diGraphCollection.generateWord(8)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
        
        print("Optimeeritud algoritmiga  trigrammid:")
        probTotal = []
        for i in range(8):
            word = self.triGraphCollection.generateWord(8)
            prob = self.findStringProbability(word)
            probTotal.append(prob)
            print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
        print('keskmine tõenäosus: %.5f' % avg(probTotal))
    def getOptimizedDigraph(self, length):
        summary = sum(self.diGraphCounter.values())
        a = Counter()
        pass

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
            #import binascii

            
            string = self.getStart(weightedStart)
            for j in range(length - 3):
                limitedChoice = []
                for word in self.triGraphFreq:
                    #print("- %s-%s-" % (word, string))
                    try:
                        if word[0] == string[-2] and word[1] == string[-1]:
                            limitedChoice += [word]
                    except TypeError as err:
                        pass
                        #print("=%s=%s=%s" % (word, string, length))
                string = string[:-2] + random.choice(limitedChoice)
            return  string

    def getStart(self, weightedStart):
        if weightedStart:
            return random.choice(self.startFreq)
        return random.choice(self.triGraphFreq)

    def save(self):
        def saveOptimized():
            lemmad = 'resource/lemmad_comp.txt'
            print ("salvestan Digraafid")
            digraph = DiGraph(lemmad)
            digraph.scanWords()
            digraph.saveCounter('resource/digraph_comp.pck')
            #digraph.('resource/digraph_comp.pck')

        def saveNaive():
            lemmad = 'resource/lemmad_utf.txt'
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

        def scanAndSave():
            a = GraphCollection()
            a.scanWords('resource/lemmad_utf.txt', 3)
            quickDict = a.create2GQuickDict()
            a.save('resource/qd2g.pck', quickDict)
            quickDict = a.create3GQuickDict()
            a.save('resource/qd3g.pck', quickDict)

        scanAndSave()
        #self.saveNaive()
        
        
    def load(self):
        def loadNaive():
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

        def loadOptimized():
            a = GraphCollection()
            b = GraphCollection()
            inFile = open('resource/qd2g.pck', 'rb')
            a.quickDict = pickle.load(inFile)
            inFile = open('resource/qd2g.pck', 'rb')
            b.quickDict = pickle.load(inFile)
            #a.quickDict = self.qd2g
            self.diGraphCollection = a
            self.triGraphCollection = b
        
        loadNaive()
        loadOptimized()
        
    def getRandomLength(self):
        return random.choice(self.lengthFreq)

    def findStringProbability(self, word):
        i = 0
        probability = 1
        while i <= len(word):
            chars = word[i:i+2]
            if len(chars) == 2:
                chProb = self.findCharsProbability(word[i:i+2])
                # workaround for wrong encoding perhaps
                if chProb:
                    probability *= chProb
            i += 2
        return probability

    def findCharsProbability(self, chars):
        prob = (self.probabilityDict[chars] if chars in 
                    self.probabilityDict else None)
        
        if not prob:
            #outStream = open('dictissue.txt', 'wb')
            print(chars)
            print(list(self.probabilityDict.keys()))
            #outStream.close()

        return prob

if __name__ == '__main__':
    
    app = Main()
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        app.save()
    elif True:
        app.load()
        app.run()
    else:
        app.optimize()
