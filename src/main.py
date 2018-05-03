import sys
import os
from indexer import Indexer
from queryIndex import QueryIndex

# Get the document collection path from command line args, if provided
doc_coll_path = ''
args_len = len(sys.argv)
if args_len > 2:
  print('Too many arguments provided')
elif args_len == 2:
  doc_coll_path = sys.argv[1]
else:
  doc_coll_path = '../docs'  # Default set of doc collection

print(doc_coll_path)
if not os.path.exists(doc_coll_path):
  print(doc_coll_path + ' does not exist. Exiting application.')
  sys.exit()
if not os.path.isdir(doc_coll_path):
  print(doc_coll_path + ' is not a directory. Exiting application.')
  sys.exit()

# Iterate the directory and fetch all .docx files
file_names = []
for root, directories, files in os.walk(doc_coll_path):
    for file in files:
        if ".docx" in file:
          file_names.append(file)
          # print(os.path.join(root, file))
if len(file_names) < 1:
  print('No "docx" file found in ' + doc_coll_path + ' directory for indexing. Exiting application.')
  sys.exit()
else:
  print('List of files found for indexing are:')
  for name in file_names:
    print(name, end=' ')
print('\n\n')

# Start indexing
i = Indexer()
i.createIndex(doc_coll_path, file_names)
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
