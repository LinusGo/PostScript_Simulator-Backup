import re
# from HW4_part1 import *
# --------Part 1--------
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


# --------Part 2--------

def tokenize(s):
    return re.findall(
        "/?[a-zA-Z][a-zA-Z0-9_]*|[\[][a-zA-Z-?0-9_\s\(\)!][a-zA-Z-?0-9_\s\(\)!]*[\]]|[\()][a-zA-Z-?0-9_\s!][a-zA-Z-?0-9_\s!]*[\)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]",
        s)


# COMPLETE THIS FUNCTION
# The it argument is an iterator.
# The tokens between '{' and '}' is included as a sub code-array (dictionary). If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatch(it):
    res = []
    for c in it:
        if c == '}':
            return {'codearray': res}
        elif c == '{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code-array for the inner 
            # parenthesis, it will be appended to the list we are constructing 
            # as a whole.
            res.append(groupMatch(it))
        else:
            if isinstance(c, str):
                if c.isdigit() | c.startswith('-'):
                    res.append(int(c))
                elif c.startswith('['):
                    list = []
                    d = c[1:-1].split()
                    for i in d:
                        if i.isdigit() | i.startswith('-'):
                            list.append(int(i))
                        else:
                            list.append(i)
                    res.append(list)
                elif c == 'True':
                    res.append(True)
                elif c == 'False':
                    res.append(False)
                else:
                    res.append(c)

    return False


# COMPLETE THIS FUNCTION
# Function to parse a list of tokens and arrange the tokens between { and } braces 
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested dictionaries.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c == '}':  # non matching closing parenthesis; return false since there is
            # a syntax error in the Postscript code.
            return False
        elif c == '{':
            res.append(groupMatch(it))
        else:
            if isinstance(c, str) | c.startswith('-'):
                if c.isdigit():
                    res.append(int(c))
                elif c.startswith('['):
                    list = []
                    d = c[1:-1].split()
                    for i in d:
                        if i.isdigit() | i.startswith('-'):
                            list.append(int(i))
                        else:
                            list.append(i)
                    res.append(list)
                elif c == 'True':
                    res.append(True)
                elif c == 'False':
                    res.append(False)
                else:
                    res.append(c)
    return {'codearray': res}


# COMPLETE THIS FUNCTION
# This will probably be the largest function of the whole project, 
# but it will have a very regular and obvious structure if you've followed the plan of the assignment.
# Write additional auxiliary functions if you need them.

def psIf():
    codearray = opPop()
    booleanValue = opPop()
    if isinstance(booleanValue, bool):
        if booleanValue == True:
            interpretSPS(codearray)
    else:
        print("Error. Wrong input!")


def psIfelse():
    codearray_1 = opPop()
    codearray_2 = opPop()
    booleanValue = opPop()
    if isinstance(booleanValue, bool):
        if booleanValue == True:
            interpretSPS(codearray_2)
        else:
            interpretSPS(codearray_1)
    else:
        print("Error. Wrong input!")


def psFor():
    codearray = opPop()
    finalValue = opPop()
    stepValue = opPop()
    initialValue = opPop()
    if finalValue > initialValue:
        for i in range(initialValue, finalValue + 1, stepValue):
            opPush(i)
            interpretSPS(codearray)
    else:
        for i in range(initialValue, finalValue - 1, stepValue):
            opPush(i)
            interpretSPS(codearray)


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
    "end": end,
    "if": psIf,
    "ifelse": psIfelse,
    "for": psFor
}


def interpretSPS(code):  # code is a code array
    for token in code['codearray']:
        if isinstance(token, int) or isinstance(token, bool) or isinstance(token, dict):
            opPush(token)
        elif isinstance(token, list):
            opPush(evaluateArray(token))
        elif isinstance(token, str):
            if (len(token) >= 2 and (token[0] == '(') and (token[-1] == ')')) or (
                    len(token) >= 1 and (token[0] == '/')):
                opPush(token)
            elif token in operations.keys():  # Built-in operation
                operations[token]()
            else:
                v = lookup(token)
                if v is not None:
                    if isinstance(v, dict):
                        interpretSPS(v)
                    else:
                        opPush(v)
                else:
                    print("Error: Couldn't find the token")
        else:
            print("Error: Wrong input")


def interpreter(s):  # s is a string
    interpretSPS(parse(tokenize(s)))


# clear opstack and dictstack
def clearStacks():
    opstack[:] = []
    dictstack[:] = []


input1 = """
            /square {dup mul} def   
            [3 -2 1]  aload pop
            /total 0 def 
            1 1 3 {pop square total add /total exch def} for 
            total 14 eq stack
         """

input2 = """
            /x 1 def
            /y 2 def
            /x 10 def
            /y 20 def
            0 x 1 y {add} for
            stack
        """
input3 = """
            /f {dup length} def
            [1 2 (322) (451) length]
            [1 -2 4 5 add (long) length]
            (123456)  f
            stack
         """
input4 = """
            /x 1 def
            /y 2 def
            1 dict begin
            /x 10 def
            1 dict begin /y 3 def x y end
            /y 20 def
            x y
            end
            x y
         """
input5 = """
            /sumArray 
            {0 exch aload pop count n sub -1 1 {pop add} for /n n 1 add def } def
            /x 5 def
            /y 10 def
            /n 1 def
            [1 2 3 4 x] sumArray
            [x 7 8 9 y] sumArray
            [y 11 12] sumArray
            [0 0 0] astore
            stack        
         """

input6 = """
            1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
            stack        
         """
input7 = """
            (CptS322 HW1_CptS355 HW2)
            dup /myclass exch def
            myclass 16 3 getinterval /c exch def
            myclass 4 c putinterval
            myclass
            stack
        """

input8 = """
           (COVID-19 Vaccine)
            dup
            ( ) search pop exch pop
            (-19) search
            {
                pop pop pop (Vaccine) eq
                { (yay) }
                { (???)  }
                ifelse
            } if
            stack
         """

input9 = """
           [1 2 3 4 5] aload /myA exch def
            count copy [0 0 0 0 0] astore
            myA eq
            stack
         """
input10 = """
            /n 5 def
            /fact {
                0 dict begin
                /n exch def
                n 2 lt
                { 1}
                {n 1 sub fact n mul }
                ifelse
                end 
            } def
            n fact
         """

input11 = """
          /fact{
                0 dict
                begin
                    /n exch def
                    1
                    n -1 1 {mul /n n 1 sub def} for 
                end
            } def
            6 fact
         """

input12 = """
            /x 111 def
            x
            5 dict begin
            /x 222 def
            x
            end
            x
            stack
        """

input13 = """
            /x 4 def
            x 3 eq
            {x 1 add /result exch def}
            {x 4 eq
            {x 2 add /result exch def}
            {x 3 add /result exch def}
            ifelse }
            ifelse
            result
        """

input14 = """
            /x 5 def
            /y 10 def
            /x 15 def
            /y 20 def
            0 x 1 y {sub} for
            stack
        """

input15 = """
            /result 10 def
            /fact {
                0 dict begin
                /result exch def
                result 2 lt
                { 1}
                {result 1 sub fact result add }
                ifelse
                end 
            } def
            result fact
         """

input16 = """
        /x 10 def
        /y 20 def
        /myf {
            /y y 2 mul def
            1 dict
            begin
                /x x y add def
                x
            end
        } def
        x y add myf x y add
        """

dictstack.append({})
interpreter(input16)
print(parse(tokenize(input16)))
print(opstack)
print(dictstack)
