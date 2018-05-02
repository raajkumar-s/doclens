import DocReader as reader

FILE_DIR_PATH = '../docs/'
FILE_NAMES = ['Doc1.docx', 'Doc2.docx', 'Doc3.docx', 'Doc4.docx', 'Doc5.docx', 'Doc6.docx']

for file_name in FILE_NAMES:
  # Read the file content
  print('--'*80)
  doc_text = reader.get_docx_text(FILE_DIR_PATH+file_name)
  print(doc_text)

# Start indexing