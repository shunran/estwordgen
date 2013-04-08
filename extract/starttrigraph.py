'''
Created on Feb 19, 2013
@author: lauri
'''
from extract.graph import Graph

class StartTriGraph(Graph):
    
    def scanWords(self):
        stream = self.openWords()
        for word in stream:
            if len(word[:3].strip()) is not 3:
                continue
            self.frequency[word[:3]] += 1
