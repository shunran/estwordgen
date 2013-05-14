'''
Created on Apr 7, 2013
@author: lauri
'''
from extract.graph import Graph

class Length(Graph):
    def scanWords(self):
        stream = self.openWords()
        for word in stream:
            self.frequency[len(word)] += 1