# WRITE YOUR NAME and YOUR COLLABORATORS HERE

# ------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
import math
from functools import reduce

opstack = []  # assuming top of the stack is the end of the list


# Now define the HELPER FUNCTIONS to push and pop values on the opstack
# Remember that there is a Postscript operator called "pop" so we choose 
# different names for these functions.
# Recall that `pass` in Python is a no-op: replace it with your code.

def opPop():
    if len(opstack) > 0:
        popped = opstack[-1]
        opstack.pop()
        return popped
    else:
        print("No element in opstack")
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.


def opPush(value):
    return opstack.append(value)


# -------------------------- 16% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  # assuming top of the stack is the end of the list


# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    if len(dictstack) > 0:
        return dictstack.pop()
    else:
        print("No element in dictstack")
    # dictPop pops the top dictionary from the dictionary stack.


def dictPush(d):
    return dictstack.append(d)
    # dictPush pushes the dictionary ‘d’ to the dictstack.
    # Note that, your interpreter will call dictPush only when Postscript
    # “begin” operator is called. “begin” should pop the empty dictionary from
    # the opstack and push it onto the dictstack by calling dictPush.


def define(name, value):
    dictstack[-1][name] = value
    # add name:value pair to the top dictionary in the dictionary stack.
    # Keep the '/' in the name constant.
    # Your psDef function should pop the name and value from operand stack and
    # call the “define” function.


def lookup(name):
    defname = '/' + name
    for n in reversed(dictstack):
        if defname in n:
            return n[defname]
    return None


# return the value associated with name
# What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.


# --------------------------- 10% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, eq, lt, gt 
# Make sure to check the operand stack has the correct number of parameters 
# and types of the parameters are correct.
def add():
    sum = opstack[-1] + opstack[-2]
    opstack.pop()
    opstack.pop()
    opstack.append(sum)


def sub():
    difference = opstack[-2] - opstack[-1]
    opstack.pop()
    opstack.pop()
    opstack.append(difference)


def mul():
    product = opstack[-2] * opstack[-1]
    opstack.pop()
    opstack.pop()
    opstack.append(product)


def eq():
    result = opstack[-2] == opstack[-1]
    opstack.pop()
    opstack.pop()
    opstack.append(result)


def lt():
    result = opstack[-2] < opstack[-1]
    opstack.pop()
    opstack.pop()
    opstack.append(result)


def gt():
    result = opstack[-2] > opstack[-1]
    opstack.pop()
    opstack.pop()
    opstack.append(result)


# --------------------------- 20% -------------------------------------
# String operators: define the string operators length, get, getinterval,  putinterval, search
def length():
    if opstack[-1].startswith('('):
        length = len(opstack[-1]) - 2
        opstack.pop()
        opstack.append(length)


def get():
    j = 0
    index = opstack[-1]
    opstack.pop()
    str = opstack[-1]
    opstack.pop()
    if str.startswith('('):
        for i in list(str):
            j += 1
            if j == index + 2:
                opstack.append(ord(i))


def getinterval():
    if len(opstack) > 2:
        j = 0
        count = opstack[-1]
        opstack.pop()
        index = opstack[-1]
        opstack.pop()
        target = opstack[-1]
        opstack.pop()
        if isinstance(index, int):
            if isinstance(count, int):
                if isinstance(target, str) | isinstance(target, list):
                    for i in list(target):
                        j += 1
                        if j == index + 1:
                            opstack.append('(' + target[j:j + count] + ')')
                else:
                    print("This should be a String or an Array" + target)
            else:
                print("This should be an int" + count)
        else:
            print("This should be an int" + index)
    else:
        print("Missing elements")


def putinterval():
    if len(opstack) > 2:
        target = opstack[-1][1:-1]
        opstack.pop()
        location = opstack[-1]
        opstack.pop()
        s1 = opstack[-1]
        opstack.pop()
        newstr = s1[:location + 1] + target + s1[len(target) + 1 + location:]
        opstackindex = 0
        if isinstance(target, str):
            if isinstance(location, int):
                if isinstance(s1, str):
                    for i in opstack:
                        if i is s1:
                            opstack[opstackindex] = newstr
                        opstackindex += 1
                    dictstackindex = 0
                    for j in dictstack:
                        thatstring = list(j.items())[0][1]
                        if thatstring is s1:
                            dictstack[dictstackindex][list(dictstack[dictstackindex])[0]] = newstr
                        dictstackindex += 1
                else:
                    print("This should be a String" + s1)
            else:
                print("This should be an int" + location)
        else:
            print("This should be an int" + target)
    else:
        print("Missing elements")


def search():
    target = opstack[-1]
    opstack.pop()
    str = opstack[-1]
    opstack.pop()
    index = str.find(target[1:-1])
    if index == -1:
        opstack.append(str)
        opstack.append(False)
    else:
        opstack.append('(' + str[index + 1:])
        opstack.append(target)
        opstack.append(str[:index] + ')')
        opstack.append(True)


# --------------------------- 18% -------------------------------------
# Array functions and operators:
#      define the helper function evaluateArray
#      define the array operators aload, astore

def aload():
    array = opstack[-1]
    opstack.pop()
    for item in array:
        opstack.append(item)
    opstack.append(array)


def astore():
    emptyarray = opstack[-1]
    opstack.pop()
    array = []
    for i in range(len(emptyarray)):
        array.append(opstack[-i - 1])
    del opstack[len(opstack) - len(emptyarray):]
    opstack.append(list(reversed(array)))


# --------------------------- 6% -------------------------------------
# Define the stack manipulation and print operators: dup, copy, count, pop, clear, exch, stack
def dup():
    opstack.append(opstack[-1])


def copy():
    index = opstack[-1]
    opstack.pop()
    for i in range(index):
        opstack.append(opstack[-(index)])


def count():
    opstack.append(len(opstack))


def pop():
    opPop()


def clear():
    opstack.clear()


def exch():
    first = opstack[-1]
    second = opstack[-2]
    opstack.pop()
    opstack.pop()
    opstack.append(first)
    opstack.append(second)


def stack():
    return opstack


# --------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.
def psDict():
    dictlength = opstack[-1]
    opstack.pop()
    opstack.append({})


def begin():
    dictPush(opPop())


def end():
    dictPop()


def psDef():
    if len(opstack) > 1:
        value = opPop()
        name = opPop()
        define(name, value)
    else:
        print("Need at least 2 elements")


operations = {
    "add": add,
    "sub": sub,
    "mul": mul,
    "eq": eq,
    "lt": lt,
    "gt": gt,
    "length": length,
    "get": get,
    "getinterval": getinterval,
    "putinterval": putinterval,
    "search": search,
    "aload": aload,
    "astore": astore,
    "dup": dup,
    "exch": exch,
    "copy": copy,
    "count": count,
    "pop": pop,
    "def": psDef,
    "stack": stack,
    "begin": begin,
    "dict": psDict,
    "end": end
}



def evaluateArray(aInput):
    array = []
    mark = 'mark'
    opstack.append(mark)
    keys = [key[1:] for item in dictstack for key in item]
    for item in aInput:
        if item in keys:
            opstack.append(lookup(item))
        elif item in operations.keys():
            operations[item]()
        else:
            opstack.append(item)
    for item in reversed(opstack):
        if item != mark:
            array.append(item)
            opPop()
        else:
            opPop()
            break
    return list(reversed(array))

