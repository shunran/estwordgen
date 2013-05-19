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

from pprint import pprint
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
    qd2g = None
    qd3g = None
    prob = None
    length = None
    
    def run(self):
        ##print ("Content-type:text/html;encoding=UTF-8\n\n")
        def avg(list):
            return float(sum(list)) / len(list)
        '''
        probabilityFilename = 'resource/digraph_probability.pck'
        inFile = open(probabilityFilename, 'rb')
        oc.loadProbability(inFile)
        self.probabilityDict = oc.probabilityDict
        lemmad = 'resource/lemmad_utf.txt'
        inFile = open(lemmad, 'r')
        for i in range(8):
            word = self.random_line(inFile)
            prob = self.findStringProbability(word)
            print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
            print ("uus tõenäosus %.5f" % (10**8 * oc.findWordProbability(word, self.prob , 1)))
        '''

        def timeIt(f, *args):
            import time
            start = time.clock()
            m = f(*args)
            return m, (time.clock() - start)*10

        def digraph():
            words = []
            for i in range(1000):
                #word = self.getNaiveTrigraph(8)
                len = random.choice(self.lengthFreq)
                word = self.getNaiveTrigraph(len, True)
                #prob = self.findStringProbability(word)
                #probTotal.append(prob)
                words.append(word)
                #print(word)
                #print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
                #print ("uus tõenäosus %.10f" % (10^6 * oc.findWordProbability(word, self.prob , 1)))
                #print('keskmine tõenäosus: %.5f' % avg(probTotal))
            return ', '.join(words)
        
        def qdTrigraph():
            words = []
            for i in range(10):
                len = self.gc.findLength(self.length)
                word = self.gc.findWord(self.qd3g, 3, len)
                #prob = self.findStringProbability(word)
                #probTotal.append(prob)
                words.append(word)
                #print(word)
                #print ("Sõna: %s Tõenäosus: %.5f" % (word, prob))
                #print ("uus tõenäosus %.10f" % (10^6 * oc.findWordProbability(word, self.prob , 1)))
                #print('keskmine tõenäosus: %.5f' % avg(probTotal))
            return ', '.join(words)
        
        def compareMethods(afile, oc, qd3g, prob):
            probTotal1 = []
            probTotal2 = []
            probTotal3 = []
            print("\nPseudojuhusliku pikkusega ja kaalutud algusega trigrammid:")
            for i in range(10):
                word1 = self.random_line(afile) #originaal
                wordlen = len(word1)
                word2 = self.getNaiveTrigraph(wordlen, True) #naiivne
                word3 = oc.findWord(qd3g, 3, wordlen) # optimeeritud
                prob1 = oc.findWordProbability(word1,prob,1) * 10**6
                prob2 = oc.findWordProbability(word2,prob,1) * 10**6
                prob3 = oc.findWordProbability(word3,prob,1) * 10**6
                probTotal1.append(prob1)
                probTotal2.append(prob2)
                probTotal3.append(prob3)
                print ("Sõna1: %s Tõenäosus: %.10f" % (word1, prob1))
                print ("Sõna2: %s Tõenäosus: %.10f" % (word2, prob2))
                print ("Sõna3: %s Tõenäosus: %.10f" % (word3, prob3))
            print('min, avg, max tõenäosus 1: %.5f, %.5f, %.5f' % (min(probTotal1),avg(probTotal1),max(probTotal1)))
            print('min, avg, max tõenäosus 2: %.5f, %.5f, %.5f' % (min(probTotal2),avg(probTotal2),max(probTotal2)))
            print('min, avg, max tõenäosus 3: %.5f, %.5f, %.5f' % (min(probTotal3),avg(probTotal3),max(probTotal3)))
        
        print(timeIt(digraph))
        #compareMethods('resource/lemmad_utf.txt', oc, self.qd3g, self.prob)
        #print(time_it(digraph));

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

        def scanAndSave():
            qd = GraphCollection()
            fileName = 'resource/lemmad_utf.txt'
            trie = qd.createTrie(fileName, 3)
            length       = qd.createLengthQuickArr(fileName)
            probability  = qd.createQuickDict(trie, 1)
            generator    = qd.createQuickDict(trie ,3)

            qd.save('resource/qd3g.pck', generator)
            qd.save('resource/qd1g.pck', probability)
            qd.save('resource/lngt.pck', length)

        scanAndSave()


    def load(self):
        def loadNaive():
            inFile = open('resource/digraph.pck', 'rb')
            self.diGraphFreq = pickle.load(inFile)
            inFile = open('resource/trigraph.pck', 'rb')
            self.triGraphFreq = pickle.load(inFile)

            inFile = open('resource/length.pck', 'rb')
            self.lengthFreq = pickle.load(inFile)

            inFile = open('resource/start.pck', 'rb')
            self.startFreq = pickle.load(inFile)

        def loadOptimized(self):
            gc = GraphCollection()
            qd1g = gc.load('resource/qd1g.pck')
            qd2g = gc.load('resource/qd2g.pck')
            qd3g = gc.load('resource/qd3g.pck')
            length = gc.load('resource/lngt.pck')
            #a.quickDict = self.qd2g
            self.gc   = gc
            self.prob = qd1g
            self.qd2g = qd2g
            self.qd3g = qd3g
            self.length = length

        loadNaive()
        loadOptimized(self)

    def random_line(self,afile):
        return random.choice(list(open(afile))).rstrip('\n')

    def getRandomLength(self, lengthList):
        return random.choice(lengthList)

if __name__ == '__main__':

    app = Main()
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        app.save()
    else:
        app.load()
        app.run()
