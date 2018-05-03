import sys
from indexer import Indexer
from queryIndex import QueryIndex

FILE_DIR_PATH = '../docs/'
FILE_NAMES = ['Doc1.docx', 'Doc2.docx', 'Doc3.docx',
              'Doc4.docx', 'Doc5.docx', 'Doc6.docx']

i = Indexer()

# Start indexing
i.createIndex(FILE_DIR_PATH, FILE_NAMES)
# Indexing completed

# Read input query
q = QueryIndex()
print('\n\nHello,\nEnter your search query and hit Enter key. Wrap your query in "" for searching a phrase.\nIf you want to exit, just hit Enter key')
while True:
  query = input('\nYour search query: ')
  # q = sys.stdin.readline()
  if query == '':
    print('No input provided. Exiting the program.')
    print('\nBye, Have a great day!')
    break
  else:
    resultList = q.query(query)
    length = len(resultList)
    if length > 0:
      print('Showing ' + str(length) + ' results for "' + query + '"')
      # Just formatting the output
      for doc in resultList:
        print(' - ' + doc)
    else:
      print('No matching results found for "' + query + '"')
