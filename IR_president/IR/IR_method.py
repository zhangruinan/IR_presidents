'''
Created on May 1, 2017

@author: yangr
'''
import json
from pprint import pprint
import math

class IR_method:
    '''
    classdocs
    '''
    def __init__(self, path=None):
        '''
        Constructor
        '''
        if path is None:
            raise Exception('Need at least corpus or path to initilaze!')
        self.corpus = Corpus(path).getCorpus()
    
    def readFile(self, path):
        with open(path) as json_data:
            d = json.loads(json_data)
            json_data.close()
        self.corpus = d
    
    def print_corpus(self, data):
        pprint(data)
    
    def search(self, query, fullRank=False):
        pass
    
    def setCorpus(self, corpus):
        self.corpus = corpus
    
class Corpus:
    def __init__(self, path, N = None, avdl = None):
        with open(path) as f:
            self.corpus = json.load(f)
        
        corpus = {}
        for key in self.corpus.keys():
            k = str(key)
            '''
            Anchor tags are appened with the file text
            '''
            content = (self.corpus[key]).encode('utf-8').split()
            title = [k[:-2]]
            try:
                corpus[title].append(content)
            except KeyError:
                corpus[title] = content
        self.corpus = corpus
        
        if N is None:
            self.N = self.countDocuments()
        else:
            self.N = N
        if avdl is None:
            self.avdl = self.getAvdl()
        else:
            self.avdl = avdl

    def countDocuments(self):
        return len(self.corpus)

    def getAvdl(self):
        keys = self.corpus.keys()
        total = 0.0
        for key in keys:
            total += len(self.corpus[key].split())
        return total / self.N
    
    def get_n(self):
        pass
    
    def get_frequency_from_d(self, doc, qi):
        return 
        pass

    def printFile(self):
        pprint(self.corpus)

class BM25(IR_method):
    # doc is the list of word in the document
    def __init__(self, path, k1=1.2, b=0.75):
        # super(BM25, self).__init__(path)
        IR_method.__init__(self, path)
        self.k1 = k1
        self.b = b

    def search(self, q_list, fullRank=False):
        result = []
        for i in range(self.corpus.N):
            pass
#         keys = self.corpus.keys()
#         for key in keys:
#             k = str(key)
#             if k.endswith('p'):
#                 doc = self.corpus[key].split()
#                 score = self.score(doc, q_list)
#                 result += [(key, score)]
#         
#         result = sorted(result, key = lambda val: val[1], reverse=True)
#         if fullRank:
#             return result
#         else:
#             return result[0]

    def get_idf(self, q, base=10):
        n = self.get_n(q)
        top = self.corpus.N - n + 0.5
        bottom = n + 0.5
        return math.log(top / bottom, base)

    def single_score(self, q, doc):
        idf = self.get_idf(q)
        freq = self.get_frequence(q, doc)
        top = freq * (self.k1 + 1.0)
        bottom = freq + self.k1 * (1.0 - self.b + self.b * (len(doc) / self.corpus.avdl))
        return idf * (top / bottom)

    def score(self, doc, q_list):
        total_score = sum(self.single_score(q, doc) for q in q_list)
        return total_score

    # Word occurs in N documents
    def get_n(self, q):
        keys = self.corpus.keys()
        total = 0.0
        for key in keys:
            k = str(key)
            if k.endswith('p') and q in self.corpus[key]:
                total += 1
        return total

    def get_frequence(self, q, doc):
        return doc.count(q)

class SkipBigram(IR_method):
    
    def search(self, query, fullRank=False):
        IR_method.search(self, query, fullRank=fullRank)
