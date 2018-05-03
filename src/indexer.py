import re
import gc
import os
from collections import defaultdict
from array import array

# Custom modules
from docReader import DocReader

# library
from porterStemmer import PorterStemmer

reader = DocReader()
porter = PorterStemmer()


class Indexer:
    '''
    Parses the file content and creates indexes after stemming.
    This creates indexes with posting list which includes document frequency and term position 
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.index = defaultdict(list)    # The inverted index
        self.stopwordsFile = '../meta/stop-word-list'  # Path of stop words list file
        self.indexFile = "../meta/index"    # Path of the file where index will be stored

    def readStopwordsFile(self):
        '''Get stopwords from the stopwords file'''
        f = open(self.stopwordsFile, 'r')   # Open stop words file
        stopwords = [line.rstrip() for line in f]
        self.sw = dict.fromkeys(stopwords)  # Get the list of stop words
        f.close()

    def getTerms(self, line):
        '''Given a stream of text, get the terms from the text'''
        line = line.lower()
        # put spaces instead of non-alphanumeric characters
        line = re.sub(r'[^a-z0-9 ]', ' ', line)
        line = line.split()
        line = [x for x in line if x not in self.sw]  # eliminate the stopwords
        line = [porter.stem(word, 0, len(word)-1) for word in line]
        return line

    def parseCollection(self, file_path, file_name):
        '''
        Extract text from MS docx file.
        Returns the id and text of the next page in the collection
        '''

        if file_name == None or file_path == None:
            return {}

        doc_text = reader.get_docx_text(os.path.join(file_path, file_name))

        if doc_text == None:
            return {}

        d = {}
        d['id'] = file_name
        d['text'] = doc_text

        return d

    def writeIndexToFile(self):
        '''write the inverted index to the file'''
        f = open(self.indexFile, 'w')
        for term in self.index.keys():
            postinglist = []
            for p in self.index[term]:
                docID = p[0]
                positions = p[1]
                postinglist.append(':'.join([str(docID), ','.join(map(str, positions))]))
            # print(''.join((term, '|', ';'.join(postinglist))))
            f.write(''.join((term, '|', ';'.join(postinglist))))    # Each term and it's posting list
            f.write('\n')

        f.close()

    def createIndex(self, file_path, file_names):
        '''Create index for the files in the given path'''
        print('Indexing process has stareted...')
        self.filePath = file_path   # Directory path where doc files are present
        self.fileNames = file_names # List of doc file names
        print('Fetching the list of stop words from ' + self.stopwordsFile + '...')
        self.readStopwordsFile()

        # bug in python garbage collector!
        # appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        gc.disable()

        pagedict = {}
        for name in file_names:
            # Read the file content
            print('Reading the file content of ' + name + '...')
            pagedict = self.parseCollection(file_path, name)

            if pagedict != {}:
                print('Indexing the file content of ' + name + '...')
                pageid = pagedict['id']
                terms = self.getTerms(pagedict['text'])

                # build the index for the current page
                termdictPage = {}
                for position, term in enumerate(terms):
                    try:
                        termdictPage[term][1].append(position)
                    except:
                        termdictPage[term] = [pageid, array('I', [position])]

                # merge the current page index with the main index
                for termpage, postingpage in termdictPage.items():
                    self.index[termpage].append(postingpage)

        gc.enable()

        print('Writing index to file...')
        self.writeIndexToFile()
        print('Indexing process completed.')