from math import inf
'''
  Utility module to tokenize the query string by parsing the string considering 
  $ | and ! as boolean query operators
'''
def minimum_non_negative(*args):
  min = +inf
  for num in args:
    # print('num='+str(num)+', min='+str(min))
    if (num < min) and (num != -1):
      min = num
  return min

def get_tokens(query):
  # print('Query string to be tokenized:', query)
  tokens = []
  initIdx = 0
  chosenIdx = -1
  andIdx = query.find('&')
  orIdx = query.find('|')
  notIdx = query.find('!')

  while(andIdx > -1 or orIdx > -1 or notIdx > -1):
    # print(initIdx, chosenIdx, andIdx, orIdx, notIdx)
    chosenIdx = minimum_non_negative(andIdx, orIdx, notIdx)
    # print('chosenIdx=' + str(chosenIdx))

    if (chosenIdx > -1) or (chosenIdx == inf):
      if query[initIdx:chosenIdx].strip() != '':
        tokens.append(query[initIdx:chosenIdx].strip())

      tokens.append(query[chosenIdx:chosenIdx+1].strip())
      initIdx = chosenIdx + 1

      andIdx = query.find('&', initIdx)
      orIdx = query.find('|', initIdx)
      notIdx = query.find('!', initIdx)

    else:
      andIdx = orIdx = notIdx = -1

  # Pick the remaining string
  if query[initIdx:].strip() != '':
    tokens.append(query[initIdx:].strip())

  # print('Tokenized query:', tokens)
  return tokens


# Test
# str1 = 'abcd & defg | hijk ! lmop'
# str2 = '& abcd | defg | hijk ! lmop &'
# str3 = 'lmop'
# get_tokens(str2)