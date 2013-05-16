'''
Created on Feb 19, 2013
@author: lauri
'''
from extract.graph import Graph
import re

class StartTriGraph(Graph):
    
    def scanWords(self):
        stream = self.openWords()
        for word in stream:
            #startChars = (word[:3]).replace('\s', '')
            startChars = re.sub('\s', '', word[:3] )
            if len(startChars) is not 3:
                continue
            #if re.match('^\d.*', startChars):
            #    print (startChars) 
            self.frequency[word[:3]] += 1
        print(self.frequency)
