import sys
import re
import copy
from functools import reduce 
from porterStemmer import PorterStemmer

porter = PorterStemmer()


class QueryIndex:

    def __init__(self):
        self.index = {}
        self.stopwordsFile = '../meta/stop-word-list'  # Path of stop words list file
        self.indexFile = "../meta/index"    # Path of the file where index will be stored
        self.readIndex()
        self.readStopwordsFile()

    def intersectLists(self, lists):
        if len(lists) == 0:
            return []
        # start intersecting from the smaller list
        lists.sort(key=len)
        return list(reduce(lambda x, y: set(x) & set(y), lists))

    def readStopwordsFile(self):
        f = open(self.stopwordsFile, 'r')
        stopwords = [line.rstrip() for line in f]
        self.sw = dict.fromkeys(stopwords)
        f.close()

    def getTerms(self, line):
        line = line.lower()
        # put spaces instead of non-alphanumeric characters
        line = re.sub(r'[^a-z0-9 ]', ' ', line)
        line = line.split()
        line = [x for x in line if x not in self.sw]
        line = [porter.stem(word, 0, len(word)-1) for word in line]
        return line

    def getPostings(self, terms):
        # all terms in the list are guaranteed to be in the index
        return [self.index[term] for term in terms]

    def getDocsFromPostings(self, postings):
        # no empty list in postings
        return [[x[0] for x in p] for p in postings]

    def readIndex(self):
        f = open(self.indexFile, 'r')
        for line in f:
            line = line.rstrip()
            # term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            term, postings = line.split('|')
            # postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings = postings.split(';')
            # postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            postings = [x.split(':') for x in postings]
            postings = [[x[0], map(int, x[1].split(','))]
                        for x in postings]  # final postings list
            self.index[term] = postings
        f.close()

    def queryType(self, q):
        '''Find the type query'''
        if '"' in q:    # If "" is used in query, then it's phras query
            return 'PQ'
        elif len(q.split()) > 1:    # If more than one word, it's free text query
            return 'FTQ'
        else:
            return 'OWQ'    # One word query

    def owq(self, q):
        '''One Word Query'''
        originalQuery = q
        q = self.getTerms(q)
        if len(q) == 0:
            # print('')
            return([])
        elif len(q) > 1:
            return self.ftq(originalQuery)

        # q contains only 1 term
        q = q[0]
        if q not in self.index:
            # print('')
            return([])
        else:
            p = self.index[q]
            p = [x[0] for x in p]
            # print(' '.join(p))
            return p

    def ftq(self, q):
        '''Free Text Query'''
        q = self.getTerms(q)
        if len(q) == 0:
            # print('')
            return([])

        li = set()
        for term in q:
            try:
                p = self.index[term]
                p = [x[0] for x in p]
                li = li | set(p)
            except:
                #term not in index
                pass

        li = list(li)
        li.sort()
        # print(' '.join(li))
        return li

    def pq(self, q):
        '''Phrase Query'''
        originalQuery = q
        q = self.getTerms(q)
        if len(q) == 0:
            # print('')
            return([])
        elif len(q) == 1:
            return self.owq(originalQuery)

        phraseDocs = self.pqDocs(q)

        # prints empty line if no matching docs
        # print(' '.join(phraseDocs))
        return phraseDocs

    def pqDocs(self, q):
        """ here q is not the query, it is the list of terms """
        # phraseDocs = []
        # length = len(q)
        # first find matching docs
        for term in q:
            if term not in self.index:
                # if a term doesn't appear in the index
                # there can't be any document maching it
                return []

        postings = self.getPostings(q)  # all the terms in q are in the index
        docs = self.getDocsFromPostings(postings)
        # docs are the documents that contain every term in the query
        docs = self.intersectLists(docs)
        # postings are the postings list of the terms in the documents docs only
        for i in range(len(postings)):
            postings[i] = [x for x in postings[i] if x[0] in docs]

        # check whether the term ordering in the docs is like in the phrase query

        # subtract i from the ith terms location in the docs
        # this is important since we are going to modify the postings list
        postings = copy.deepcopy(postings)

        for i in range(len(postings)):
            for j in range(len(postings[i])):
                postings[i][j][1] = [x-i for x in postings[i][j][1]]

        # intersect the locations
        result = []
        for i in range(len(postings[0])):
            li = self.intersectLists([x[i][1] for x in postings])
            if li == []:
                continue
            else:
                # append the docid to the result
                result.append(postings[0][i][0])

        return result

    def query(self, q):
        qt = self.queryType(q)
        if qt == 'OWQ':
            return self.owq(q)
        elif qt == 'FTQ':
            return self.ftq(q)
        elif qt == 'PQ':
            return self.pq(q)
