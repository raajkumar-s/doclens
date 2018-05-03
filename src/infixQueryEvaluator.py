def unique(a):
    """ Return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ Return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ Return the union of two lists """
    return list(set(a) | set(b))

def difference(a, b):
    """ Return the difference between lists a and b """
    return list(set(a) - set(b))

def isQueryToken(token):
  if (token == '&') or (token == '|') or (token == '!'):
    return False
  else:
    return True

def evaluate_querylist(query_list, file_names):
  # print(query_list)
  stack = []
  i = 0
  length = len(query_list)
  while i < length:
    token = query_list[i]
    if isQueryToken(token):
      stack.append(token)

    elif (token == '&') or (token == '|'):
      # if there is an item in stack and if there is an item available in token_list
      # then process those two items and put it in stack for further processing
      # if not, ignore this operator as the query is not properly formatted

      # Continue only if we did not reach end of list and stack is not empty
      if ((i + 1) < length) and (len(stack) > 0) :
        # Get the last item from stack
        operandA = stack[len(stack) - 1]
        # Get the next item from query_list
        operandB = query_list[i + 1]
        if isQueryToken(operandA) and isQueryToken(operandB):
          # increment index by 1 as we have already picked the next item as operandB
          i = i + 1
          # remove the last item from stack as we will populate with the computed list
          stack.pop()

          if (token == '&'):
            # If logical AND, compute A INTERSECTION B and put it back in to stack
            stack.append(intersect(operandA, operandB))
          else:
            # If logical OR, compute A UNION B and put it back in to stack
            stack.append(union(operandA, operandB))

        else:
          pass  # Either operand A or B is invalid, just ignore

    else: # token == '!'
      # Continue only if we did not reach end of list
      if (i + 1) < length:
        # Get the next item from query_list
        operand = query_list[i + 1]
        if isQueryToken(operand):
          # increment index by 1 as we have already picked the next item as operand
          i = i + 1
          # Get the list of docs which does not contain the query
          # !(1 0 1 1 0) = (0 1 0 0 1)
          diff = difference(file_names, operand)

          if (len(stack) > 0):
            # If there is an item in stack, perform intersection to complete the current operation
            # Get the last item from stack
            operandA = stack[len(stack) - 1]
            if isQueryToken(operandA):
              # remove the last item from stack as we will populate with the computed list
              stack.pop()
              # If logical AND, compute A INTERSECTION B and put it back in to stack
              stack.append(intersect(operandA, diff))
          else:
            # If there is not item in stack, just add the current list to stack
            stack.append(diff)

    i = i + 1

  # Remaining item in the stack is always the resultant list
  # print('Resulting list')
  # print(stack[0])
  return stack[0]