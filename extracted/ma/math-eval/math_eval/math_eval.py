#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import operator
from decimal import Decimal
from fractions import Fraction
from ast import literal_eval
from math import inf, e, pi
import logging
logging.basicConfig(level = logging.WARN)
ComputeLogger = logging.getLogger('ComputeLogger')

def negpow(x, y): return -x**y

function = type(negpow)

def coercive_floor(x): return int(float(x)//1)

def contained_by(x, y): return x in y

def astype_int(x):
    '''x: numpy array or pandas Series. Returns x.astype(int)'''
    return x.astype(int)
def astype_float(x): return x.astype(float)
def astype_str(x): return x.astype(str)

def getitem(arr, key_or_index):
    if isinstance(key_or_index, IntRange):
        return arr[key_or_index.slice]
    return arr[key_or_index]

def neg_getitem(arr, key_or_index):
    '''Equivalent to -arr[key_or_index]'''
    return -getitem(arr, key_or_index)

    
def has_pattern(string, pat):
    '''string: str, or pandas.Series containing strings.
If string is str, returns True if string contains the regular expression pat.
Else, return a boolean pandas.Series where each entry is bool("The corresponding 
    entry in string matches the regular expression pat.")'''
    if isinstance(string, str):
        return re.search(pat, string) is not None
    # the only alternative this function will support is regex matching for pd.Series
    return string.str.contains(pat, regex = True)


def replace_compute(string, old_dubslash_new):
    '''string: str, or pandas.Series containing strings.
old_dubslash_new: str of the form "old//new", where old is to be replaced and new is
    the replacement. old and new are read as regular expressions supporting group
    callbacks.
Returns: obj of same type as string, where all instances of old replace with new.'''
    old, new = old_dubslash_new.split('//')
    if isinstance(string, str):
        return re.sub(old, new, string)
    return string.str.replace(old, new, regex = True)



op_regex = re.compile((r'((?:\(|\)' # parens
                       r'|\[|\]' # square brackets enclosing an expr, for array access
                       r'|\+|(?<!:)\-|//?|%|\*\*?' # arithmetic 
                                                   # note '-' can't be preceded by ':'
                       r'|[<>=]=|<|>|!=|=~' # comparisons
                       r'|\&|\||\^' # logical
                       r'|[a-zA-Z]+' # varnames, ufunctions, and some binops
                       # r'|sum|len|int|float|str|tuple|values|not|set|max|min|sorted'
                       # r'|in|sub|map' # reserved words
                       r'|`(?:[^`]|(?<=\\)`)*`' # backtick-enclosed strings
                       # note that the backtick-string regex allows "`" inside strings
                       # by escaping them.
                       ')\s*)'))
                      
safe_op_regex = re.compile((r'((?:\(|\)' # parens
                            r'|\+|(?<!:)\-|//?|%|\*\*?' # arithmetic
                            r'|[<>=]=|<|>|!=' # comparisons
                            r'|\&|\||\^' # logical
                            r'|[a-zA-Z]+' # varnames, ufunctions, and some binops
                            # r'|not|int|float' # the only ufunctions w/o iterables
                        ')\s*)'))

class ComputeError(Exception):
    def __init__(self, message = '', tokens = tuple(), token_number = 0):
        self.message = message
        self.tokens = tokens
        self.token_number = token_number
        self.lexpos = sum(len(x) for x in tokens[:token_number])
    def __repr__(self):
        out = ''
        if self.tokens:
            out = "Error at {tknum}^th token ('{tok}'): {msg}\n{eqn}\n".format(tknum=self.token_number, tok=self.tokens[self.token_number], msg=self.message, eqn=''.join(self.tokens))
            out += ' '*self.lexpos + '^'
        return out
        # ComputeError('...', 'a + bluten_ru', 2) should look something like this: 
        # ComputeError: Error at 2^th token ('bluten_ru'): ...
        # a + bluten_ru
        #     ^
    __str__ = __repr__


class IntRange:
    '''A class like a builtin range() object that is treated as *equaling* all
    integers in its range as well as *containing* them.
Like the builtin range, it is iterable. If the stop is +/-infinity, 
    iteration will stop at self.start - 3,141,592 or self.start + 3,141,592.
IntRanges have a slice(arr) method that returns a slice of arr with indices 
    from the IntRange.

NOTE: IntRange.fromstring("::x"), where x is a negative integer, will NOT 
have a slice attribute that is equivalent to the slice produced by the "::x" 
syntax in normal Python.

The best way to build an IntRange that slices an array in reverse order 
starting from the last index is to use IntRange.fromstring("-1::x") where x 
is a negative integer.
    '''
    def __init__(self, *args):
        if len(args) == 1:
            self.start = 0
            self.stop = args[0]
            self.step = 1
            self.slice = slice(args[0])
        if len(args) == 2:
            self.start = int(args[0])
            self.stop = args[1] # can't coerce it to an int, because math.inf is float
            self.step = 1
            if abs(args[1]) == inf:
                self.slice = slice(self.start, None)
            else:
                self.slice = slice(self.start, self.stop)
        if len(args) == 3:
            assert args[2] != 0, 'IntRange() arg 3 must be nonzero'
            self.start = int(args[0])
            self.stop = args[1]
            self.step = int(args[2])
            if abs(args[1]) == inf:
                self.slice = slice(self.start, None, self.step)
            else:
                self.slice = slice(self.start, self.stop, self.step)

    def __eq__(self, x):
        if isinstance(x, (int, float)):
            if self.start < self.stop:
                return x >= self.start and x < self.stop and (x-self.start)%self.step==0
            else:
                return x > self.stop and x <= self.start and (x-self.start)%self.step==0
        elif isinstance(x, IntRange):
            return hash(self) == hash(x)
        return False
    __contains__ = __eq__
    
    def __str__(self):
        return "IntRange({}, {}, {})".format(self.start, self.stop, self.step)
    __repr__ = __str__
    def __hash__(self):
        return hash(repr(self))
    
    def __iter__(self):
        ii = self.start
        if self.stop == inf:
            stop = self.start + 3_141_592 # to avoid infinite iteration. Also, pi.
        elif self.stop == -inf:
            stop = self.start - 3_141_592
        else:
            stop = self.stop
            
        if stop > self.start and self.step > 0:
            while ii < stop:
                yield ii
                ii += self.step
        elif stop < self.start and self.step < 0:
            while ii > stop:
                yield ii
                ii += self.step
                
    def __len__(self):
        if self.stop == inf:
            stop = self.start + 3_141_592
        elif self.stop == -inf:
            stop = self.start - 3_141_592
        else:
            stop = self.stop
        return max(0, int((stop - self.start)/self.step))
            
    @classmethod
    def fromstring(self, string):
        '''assumes string is a set of 1 to 3 integers delimited by ':'.
You can also use 'inf' or '-inf' in place of an integer, and it will be read as
    inf or -inf.
If there's one argument, it's read as the 'stop' arg, and 'inf' or '' sets it to inf.
If there are two or more args, the first arg defaults to 0 if empty and the second arg
    defaults to inf if empty.
The third arg is always the step, default 1.'''
        nums = string.split(':')
        step = 1
        if len(nums) == 1:
            start = 0
            if nums[0] in ('', 'inf'):
                stop = inf
            elif nums[0] == '-inf':
                stop = -inf
                step = -1
            else:
                stop = int(nums[0])
        else:
            # note that we are NOT allowing start to be inf or -inf, because while
            # you certainly can start counting from a finite number towards infinity,
            # you can't start counting at infinity and get to a finite number.
            if nums[0] == '':
                start = 0 
            else:
                start = int(nums[0])
        if len(nums) > 1:
            if nums[1] in ('', 'inf'):
                stop = inf
            elif nums[1] == '-inf':
                stop = -inf
                if len(nums) < 3 or nums[2] == '':
                    step = -1
            else:
                stop = int(nums[1])
        if len(nums) == 3:
            if nums[2] == '':
                step = 1
            else:
                step = int(nums[2])
                if step < 0 and nums[1] == '':
                    stop = -inf
        return IntRange(start, stop, step)
    
    def indices_from(self, arr):
        start, stop, step = self.slice.indices(len(arr))
        for ii in range(start, stop, step):
            yield ii 

# def map_compute(fun, itbl):
    # '''fun: a string with the name of a ufunction defined in compute(), or a function
    # of a single variable.
# itbl: any iterable.
# Returns: a list, [fun(elt) for elt in itbl]'''
    # if fun in ufunctions:
        # return (ufunctions[fun](elt)  for elt in itbl)
    # return (fun(elt)  for elt in itbl)



safe_ufunctions = {
    'int'       : int,
    'float'     : float,
    'not'       : operator.not_,
}

ufunctions = {k: v for (k, v) in safe_ufunctions.items()}
ufunctions.update({
    'str'        : str,
    'len'        : len,
    'sum'        : sum,
    'tuple'      : tuple,
    'set'        : set,
    'values'     : dict.values,
    'max'        : max,
    'min'        : min,
    'sorted'     : sorted,
    'intar'      : astype_int,
    'floatar'    : astype_float,
    'strar'      : astype_str,
    'iterable'   : literal_eval, # convert backtickstring into an iterable
})

safe_binops = {
    '&'  : operator.and_,
    '|'  : operator.or_,
    '^'  : operator.xor,
    '=~' : has_pattern,
    '==' : operator.eq,
    '!=' : operator.ne,
    '<'  : operator.lt,
    '>'  : operator.gt,
    '>=' : operator.ge,
    '<=' : operator.le,
    '+'  : operator.add,
    '-'  : operator.sub,
    '//' : operator.floordiv,
    '%'  : operator.mod,
    '*'  : operator.mul,
    '/'  : operator.truediv,
    '**' : operator.pow,
}

binops = {k: v for (k, v) in safe_binops.items()}
binops.update({
    'in' : contained_by,
    'map': map,
    'sub': replace_compute,
})

precedence_map = {
    replace_compute   : -3,
    contained_by      : -2,
    map               : -1,
    operator.and_     : 0,
    operator.or_      : 0,
    operator.xor      : 0,
    has_pattern       : 1,
    operator.eq       : 1,
    operator.ne       : 1,
    operator.lt       : 1,
    operator.gt       : 1,
    operator.ge       : 1,
    operator.le       : 1,
    operator.add      : 2,
    operator.sub      : 2,
    operator.floordiv : 3,
    operator.mod      : 3,
    operator.mul      : 3,
    operator.truediv  : 3,
    # operator.neg      : 4, # uminus precedence
    operator.pow      : 5,
    negpow            : 5,
    getitem           : 6,
    neg_getitem       : 6,
}

constants = {
    'e': e,
    'False': False,
    'inf': inf,
    'None': None,
    'True': True,
    'pi': pi,
}


def add_binop(name, function, precedence):
    '''name: a string not already in ufunctions or binops.
    The name also shouldn't have any such names as substrings, or it might not work.
function: a function that takes exactly two required arguments.
precedence: Where the function should be on the precedence_map.
Returns: None. Maps name to function, and function to precedence.
NOTES:    
    - Choose precedence carefully! If you're not sure, you should probably make it
        as high as possible, so that it resolves before any other operations do.
    '''
    # raise NotImplementedError
    # new_op_regex = r'(\(|\)|\[|\]|`(?:[^`]|(?<=\\)`)+`|' + \
                   # '|'.join(re.escape(x) for x in ufunctions) + \
                   # '|'.join(re.escape(x) for x in binops)
    binops[name] = function
    precedence_map[function] = precedence
    
def add_ufunction(name, function):
    '''name: a string not already in ufunctions or binops.
    The name also shouldn't have any such names as substrings, or it might not work.
function: a function that takes exactly one required argument.
Returns: None. Equivalent to ufunctions[name] = function.
    '''
    ufunctions[name] = function


def funcname(func):
    '''Mostly useful for running functions on arbitrary inputs with the eval(string) function.'''
    module = func.__module__
    name = re.findall("<.*(?:function|class) \'?([a-zA-Z_\d\.]+)\'?.*>", repr(func))[0]
    if isinstance(func, type) or module in ['builtins', '__main__']:
        return name
    return module + '.' + name


def parse_token(tok):
    if re.match('\d*\.\d+$', tok):
        return float(tok)
    elif re.match('\d+$', tok):
        return int(tok)
    elif re.match('-?\d*(?::-?\d*)?:-?\d*$', tok):
        return IntRange.fromstring(tok)
    elif tok in binops:
        return binops[tok]
    elif tok in ufunctions:
        return ufunctions[tok]
    elif tok in constants:
        return constants[tok]
    elif re.match('[a-zA-Z]+$', tok):
        return tok
    elif tok[0]=='`' and tok[-1]=='`':
        return tok[1:-1].replace('\\`', '`')
    raise ComputeError
    

def parse_safe_token(tok):
    if re.match('\d*\.\d+$', tok):
        return float(tok)
    elif re.match('\d+$', tok):
        return int(tok)
    elif re.match('-?\d*(?::-?\d*)?:-?\d*$', tok):
        return IntRange.fromstring(tok)
    elif tok in safe_binops:
        return safe_binops[tok]
    elif tok in safe_ufunctions:
        return safe_ufunctions[tok]
    elif tok in constants:
        return constants[tok]
    elif re.match('[a-zA-Z]+$', tok):
        return tok
    raise ComputeError


def eqn_eval(eqn):
    '''Uses builtin eval() to evaluate a mathematical expression with <=1 variable name.
Returns a number if there is no variable name, otherwise returns a lambda expression.
It's not *guaranteed* to be safe, because you can use letters in the expression, but
you probably can't do anything unsafe with only numbers and one word without
underscores.'''
    varnames = ','.join(set(re.findall('[a-zA-Z]+', eqn)))
    assert len(varnames) <= 1, \
        'Cannot evaluate an expression with more than one variable.'
    if not varnames:
        return eval(eqn)
    else:
        return eval("lambda {var}: {eqn}".format(var=varnames, eqn=eqn))


def apply_uminus(expr, varnames):
    if expr in varnames:
        ind = varnames.index(expr)
        return lambda args: -args[ind]
    elif isinstance(expr, function):
        return lambda args: -expr(args)
    elif isinstance(expr, IntRange):
        # because of the way my tokenizer works, if the start parameter of an IntRange
        # is a negative number, the '-' sign is treated as a separate token rather than
        # part of the start parameter of the IntRange's string notation
        return IntRange(-expr.start, expr.stop, expr.step)
    else:
        return -expr


def apply_ufunction(ufunction, expr, varnames):
    '''ufunction: a function that accepts one argument.
expr: a mathematical expression that can be evaluated by compute().
varnames: the variable names in an equation, sorted in ASCII order.
Returns: the result of applying ufunction to the expression.
    '''
    if expr in varnames:
        ind = varnames.index(expr)
        return lambda args: ufunction(args[ind])
    elif isinstance(expr, function):
        return lambda args: ufunction(expr(args))
    elif expr is None:
        return ufunction()
    else:
        return ufunction(expr)


def get_precedence(evald_tok):
    try:
        return precedence_map.get(evald_tok)
    except TypeError as ex:
        if 'unhashable' in repr(ex):
            return None
        else:
            raise TypeError(ex)


# class ResoBin:
    # def __init__(self, new_elt, binop, old_elt, varnames):
        # self.new_elt = new_elt
        # self.binop = binop
        # self.old_elt = old_elt
        # self.varnames = varnames
        
    
    # def __call__(self, args):
        # return self.func(args)
    
    # def __str__(self):
        # return f"ResoBin({repr(self.new_elt)}, {funcname(self.binop)}, {repr(self.old_elt)})"
    # __repr__ = __str__


def resolve_binop(new_elt, binop, old_elt, varnames):
    '''func: a binary operator that accepts two numbers.
new_elt, old_elt: each is either a number, or a string representing a variable name,
    or a function taking a single numeric input.
    A string representing a variable name is essentially equivalent to lambda x: x.
Returns:
    If old_elt or new_elt is a function or string, returns a function of a single 
        numeric input.
    If both are numbers, returns a number.
Examples:
>>> fun1 = resolve_binop(2, operator.add, 'x') # returns lambda x: 2 + x 
>>> fun1(2)
4
>>> fun2 = resolve_binop('x', operator.mul, 2)
>>> fun2(0.5)
1.0
>>> resolve_binop(2.0, operator.pow, 3)
8.0
>>> fun3 = resolve_binop(lambda x: x + 3, operator.mul, 5)
>>> fun3(2)
25
>>> fun4 = resolve_binop(lambda x: x + 3, operator.add, 'x')
>>> fun4(1)
5
>>> fun5 = resolve_binop('x', operator.pow, lambda x: x*2)
>>> fun5(2.0)
16.0
    '''
    if binop == map:
        # TODO: make it so that this same logic applies automatically to any binop
        # that takes a function as an argument but returns a scalar.
        if new_elt in ufunctions:
            if old_elt in varnames:
                ind_old = varnames.index(old_elt)
                return lambda args: map(ufunctions[new_elt], args[ind_old])
            elif isinstance(old_elt, function):
                return lambda args: map(ufunctions[new_elt], old_elt(args))
            else:
                return map(ufunctions[new_elt], old_elt)
        elif new_elt in varnames:
            ind_new = varnames.index(new_elt)
            if old_elt in varnames:
                ind_old = varnames.index(old_elt)
                return lambda args: binop(args[ind_new], args[ind_old])
            elif isinstance(old_elt, function): 
                return lambda args: binop(args[ind_new], old_elt(args))
            else:
                return lambda args: binop(args[ind_new], old_elt)
        elif isinstance(new_elt, function):
            if old_elt in varnames:
                ind_old = varnames.index(old_elt)
                return lambda args: binop(new_elt(args), args[ind_old])
            elif isinstance(old_elt, function):
                return lambda args: binop(new_elt(args), old_elt(args))
            else:
                return lambda args: binop(new_elt(args), old_elt)
        else: # new_elt is a string representing a function to be computed
            fun = compute(new_elt)
            if old_elt in varnames:
                ind_old = varnames.index(old_elt)
                return lambda args: binop(fun, args[ind_old])
            elif isinstance(old_elt, function):
                return lambda args: binop(fun, old_elt(args))
            else:
                return binop(fun, old_elt)
    if new_elt in varnames:
        ind_new = varnames.index(new_elt)
        if old_elt in varnames:
            ind_old = varnames.index(old_elt)
            return lambda args: binop(args[ind_new], args[ind_old])
        elif isinstance(old_elt, function): 
            return lambda args: binop(args[ind_new], old_elt(args))
        else:
            return lambda args: binop(args[ind_new], old_elt)
    elif isinstance(new_elt, function):
        if old_elt in varnames:
            ind_old = varnames.index(old_elt)
            return lambda args: binop(new_elt(args), args[ind_old])
        elif isinstance(old_elt, function):
            return lambda args: binop(new_elt(args), old_elt(args))
        else:
            return lambda args: binop(new_elt(args), old_elt)
    else:
        if old_elt in varnames:
            ind_old = varnames.index(old_elt)
            return lambda args: binop(new_elt, args[ind_old])
        elif isinstance(old_elt, function):
            return lambda args: binop(new_elt, old_elt(args))
        else:
            return binop(new_elt, old_elt)


def tokenize(eqn):
    tokens = op_regex.split(eqn.lstrip())
    tokens = [tok for tok in tokens if tok.strip()!='']
    
    first_open_sqbk, first_open_paren = None, None
    open_paren_count, open_sqbk_count = 0, 0
    for ii, tok in enumerate(tokens):
        if tok.strip() == '(':
            open_paren_count += 1
            if first_open_paren is None:
                first_open_paren = ii
        if tok.strip() == ')':
            open_paren_count -= 1
            if open_paren_count < 0:
                raise ComputeError("Unmatched ')'", tokens, ii)
            if open_paren_count == 0:
                first_open_paren = None
        if tok.strip() == '[':
            open_sqbk_count += 1
            if first_open_sqbk is None:
                first_open_sqbk = ii
        if tok.strip() == ']':
            open_sqbk_count -= 1
            if open_sqbk_count < 0:
                raise ComputeError("Unmatched ']'", tokens, ii)
            if open_sqbk_count == 0:
                first_open_sqbk = None
    
    if open_paren_count > 0:
        raise ComputeError("Unmatched '('", tokens, first_open_paren)
    if open_sqbk_count > 0:
        raise ComputeError("Unmatched '['", tokens, first_open_sqbk)    
    
    
    if len(tokens) == 1:
        assert tokens[0] not in binops, \
            "Cannot resolve binary operator {} without inputs".format(tokens[0])
    
    ComputeLogger.debug("tokens = {}".format(tokens))
    return tokens


def evaluate_tokens(tokens, varnames, safe = False):
    if safe:
        parse_token = parse_safe_token
        binops = safe_binops
        ufunctions = safe_ufunctions
    else:
        parse_token = globals()['parse_token']
        binops = globals()['binops']
        ufunctions = globals()['ufunctions']
    evald_tokens = []
    last_tok = None
    uminus = False
    parens_opened = 0
    paren_expressions = []
    last_num_ind = None
    last_func_ind = None
    ufunction, ufuncname = None, None
    ii = 0
    while ii < len(tokens):
        tok = tokens[ii].strip()
        if tok == '[' and not safe: # square brackets for slicing and indexing
            new_expr = []
            parens_opened += 1
            for jj in range(ii+1, len(tokens)):
                if tokens[jj].strip() == ']':
                    parens_opened -= 1
                    if parens_opened == 0:
                        last_num_ind = len(evald_tokens)
                        if jj-ii > 2:
                            paren_evald_toks = evaluate_tokens(new_expr, varnames)
                            paren_expr = resolve_big_stack(paren_evald_toks, varnames)
                        elif jj-ii == 2:
                            # square brackets containing only one token, e.g.
                            # "x[1]"
                            paren_expr = parse_token(tokens[ii+1])
                        else: # parentheses enclosing nothing
                            paren_expr = None
                        
                        if uminus: # eqn is something like "-x[0]"
                            evald_tokens.append(neg_getitem)
                            uminus = False
                        else:
                            evald_tokens.append(getitem)
                        evald_tokens.append(paren_expr)
                        ii = jj+1
                        break
                    else:
                        new_expr.append(tokens[jj])
                elif tokens[jj].strip() == '[':
                    parens_opened += 1
                    new_expr.append(tokens[jj])
                else:
                    new_expr.append(tokens[jj])
            last_tok = evald_tokens[-1]
            continue
        if tok == '(':
            tried_calling_uncallable = False
            try:
                if (last_tok is not None) and (get_precedence(last_tok) is None) \
                and (last_tok not in set(ufunctions.values())):
                    tried_calling_uncallable = True
            except: # because last_tok is an unhashable thing like a list or set;
                    # those are also uncallable generally speaking
                tried_calling_uncallable = True
            if tried_calling_uncallable:
                raise ComputeError("'{}' is not callable within a compute() expression.".format(last_tok), tokens, ii)
            new_expr = []
            parens_opened += 1
            for jj in range(ii+1, len(tokens)):
                if tokens[jj].strip() == ')':
                    parens_opened -= 1
                    if parens_opened == 0:
                        last_num_ind = len(evald_tokens)
                        if jj-ii > 2:
                            paren_evald_toks = evaluate_tokens(new_expr, varnames, safe)
                            paren_expr = resolve_big_stack(paren_evald_toks, varnames)
                        elif jj-ii == 2: 
                            # the paren expression only contains one token, 
                            # so it's as if the parens weren't there at all
                            paren_expr = parse_token(tokens[ii+1])
                        else: # parentheses enclosing nothing
                            paren_expr = None
                        if ufunction:
                            evald_tokens.append(apply_ufunction(ufunction, 
                                                                paren_expr, 
                                                                varnames))
                        else:
                            evald_tokens.append(paren_expr)
                        ufunction = None
                        ufuncname = None
                        ii = jj+1
                        break
                    else:
                        new_expr.append(tokens[jj])
                elif tokens[jj].strip() == '(':
                    parens_opened += 1
                    new_expr.append(tokens[jj])
                else:
                    new_expr.append(tokens[jj])
            if evald_tokens:
                last_tok = evald_tokens[-1]
            continue
        
        if ufuncname:
            raise ComputeError("Missing '(' for argument to function {}".format(ufuncname), tokens, ii)
        try:
            evald_tok = parse_token(tok)
        except ComputeError:
            message = ''
            if safe:
                message += "Tokens must be strings representing numbers,\nstrings representing binary operators "
                binops_to_display = list(safe_binops)
                ufuncs_to_display = list(safe_ufunctions)
            else:
                message += 'Tokens must be strings representing numbers, "`"-enclosed string literals,\nstrings representing binary operators '
                binops_to_display = list(binops)
                ufuncs_to_display = list(ufunctions)
            raise ComputeError(message + '''({binops}),
one of the reserved functions {ufuncs},
parentheses, square brackets, or variable names containing only ASCII letters.'''.format(binops=binops_to_display, ufuncs=ufuncs_to_display), tokens, ii)
        if tok in binops: # current token is a function
            last_func_ind = len(evald_tokens)
            if (last_tok is None) or (get_precedence(last_tok) is not None):
                if tok != '-':
                    raise ComputeError("The only operator allowed directly after another operator or as the first token is the unary '-'.", tokens, ii)
                uminus = not uminus
                ComputeLogger.debug("uminus = {}".format(uminus))
                ii += 1
                continue
            elif uminus:
                if tok == '**':
                    evald_tok = negpow
                else:
                    # ComputeLogger.debug(f"Applying uminus to {evald_tok}")
                    evald_tokens[last_num_ind] = apply_uminus(evald_tokens[last_num_ind], varnames)
                uminus = False
            evald_tokens.append(evald_tok)
        elif tok in ufunctions:
            ufunction = evald_tok
            ufuncname = tok
        elif isinstance(evald_tok, str):
            last_num_ind = len(evald_tokens)
            evald_tokens.append(evald_tok)
        else: # current token is a number
            last_num_ind = len(evald_tokens)
            evald_tokens.append(evald_tok)
        ComputeLogger.debug("{}^th (tok, evald_tok): ({}, {})".format(ii, repr(tok), repr(evald_tok)))
        ii += 1
        if evald_tokens:
            last_tok = evald_tokens[-1]
    
    if uminus:
        evald_tokens[last_num_ind] = apply_uminus(evald_tokens[last_num_ind], varnames)
    return evald_tokens


def resolve_substack(stack, varnames):
    '''special-case stack reduction for when all binops have same precedence'''
    if len(stack) == 1:
        if stack[0] in varnames: # 'x' is a complete substack
            ind = varnames.index(stack[0])
            return lambda args: args[ind]
        else:
            return stack[0] # a scalar is also a complete substack
    else:
        if stack[1] in {operator.pow, negpow}:
            # chained exponentiation is evaluated right->left
            funcstack = [stack[-1]]
            for ii in range(-3, -len(stack)-1, -2):
                funcstack.append(resolve_binop(stack[ii], stack[ii+1], funcstack[-1], varnames))
            return funcstack[-1]
        else:
            # all other chained equal-precedence binops are evaluated left->right
            funcstack = [stack[0]]
            for ii in range(2, len(stack), 2):
                funcstack.append(resolve_binop(funcstack[-1], stack[ii-1], stack[ii], varnames))
            return funcstack[-1]


def simplify_big_stack(stack, varnames):
    if len(stack) == 1:
        return stack
    big_stack, substack = [], []
    uminus = False
    for ii, elt in enumerate(stack):
        ComputeLogger.debug("in simplify_big_stack, elt = {}, substack = {}".format(repr(elt), substack))
        precedence = get_precedence(elt)
        if precedence is None: 
            substack.append(elt)
        elif ii < 3: # elt is first operator
            substack.append(elt)
        else: # elt is an operator, but not the first
            last_precedence = get_precedence(stack[ii-2])
            if len(substack) > 1:
                if precedence > last_precedence:
                    new_func = resolve_substack(substack[:-2], varnames)
                    big_stack.extend([new_func, substack[-2]])
                    substack = [substack[-1], elt]
                    ComputeLogger.debug("in simplify_big_stack, big_stack = {}".format(big_stack))
                elif precedence < last_precedence:
                    new_func = resolve_substack(substack, varnames)
                    big_stack.extend([new_func, elt])
                    substack = []
                    ComputeLogger.debug("in simplify_big_stack, big_stack = {}".format(big_stack))
                else: # elt has same precedence as last operator
                    substack.append(elt)
            else:
                if precedence <= last_precedence:
                    big_stack.extend([substack[0], elt])
                    substack = []
                else:
                    substack.append(elt)
    big_stack.append(resolve_substack(substack, varnames))
    ComputeLogger.debug("in simplify_big_stack, big_stack = {}".format(big_stack))
    return big_stack
                

def resolve_big_stack(stack, varnames):
    stacks = [stack]
    while len(stacks[-1]) > 1:
        precedences = set(get_precedence(x) for x in stacks[-1])
        if len(precedences) < 3: # there is only one kind of operator in the last stack
            stacks.append([resolve_substack(stacks[-1], varnames)])
        else:
            stacks.append(simplify_big_stack(stacks[-1], varnames))
    return resolve_substack(stacks[-1], varnames)


def get_varnames(tokens, safe):
    '''tokens: a list of compute() expression tokens returned by tokenize.
Returns: a list of syntactically valid variable names in the equation.'''
    out = set()
    if safe:
        reserved_words = {k: v for k, v in safe_binops.items()}
        reserved_words.update(safe_ufunctions)
    else:
        reserved_words = {k: v for k, v in binops.items()}
        reserved_words.update(ufunctions)
    reserved_words.update(constants)
    for tok in tokens:
        if tok.strip() not in reserved_words and re.fullmatch("[a-zA-Z]+\s*", tok):
            out.add(tok.strip())
    return sorted(out)


def compute(eqn, safe = False):
    '''Evaluate a string encoding a mathematical expression of any number of variables
    (including no variables).
safe: bool. If True, eqn can only contain numbers, arithmetic, comparisons, and the
    unary functions 'float', 'int', and 'not'. All iterables are forbidden in safe mode.
    Also, a function produced by compute() with safe = True will raise a
    ValueError if supplied any non-numeric inputs.
Notes:
    - 'e', 'pi', 'inf', 'True', and 'False' are constants with the values 
        you'd expect.
        - You can add more constants using the "constants" dict.
    - Variable names may contain only ASCII letters.
    - Do not declare variable names; they is determined at runtime.
    - Square brackets for array and dict access can be used as in normal Python.
    - Returns a function (if variable names were included) or a scalar otherwise.
    - All arithmetic and comparison operators are allowed, as are nested parentheses,
        as are the logical '^' (xor), '&' (and), and '|' operators.
    - IntRange() objects (which act like builtin range() objects, but are treated as
        *equal* to all integers in the range as well as *containing* all of them)
        can be declared in a compute() expression by the same start:stop:step syntax
        that is used to declare a slice in normal Python.
    - IntRanges can be used inside array-slicing square brackets in the same way as
        a normal slice.
    - IntRanges support the '==' operation and no other arithmetic operations.
    - You can declare a string literal inside a compute expression by surrounding the
        string in '``' backticks. '``' characters can be included inside the string by
        escaping them with '\\'.
        - If you want arbitrarily nested string literals (e.g., something like
            before a backtick for each level of nesting of that backtick.
            So in the compute expression "x+`3+int(\\`7\\`+\\`float(\\\\`4\\\\`)\\`)`",
            "3+int(`7`+`float(\\`4\\`)`)" is a string on level 1,
            "7" and "float(`4`)" are strings on level 2, and '4' is a string on level 3.
    - Chained comparisons are evaluated left-to-right, unlike in base Python.  
    - The logical '^', '|', and '&' operators are evaluated AFTER the comparison 
        operators, unlike in base Python where the logical operators are evaluated 
        first.
    - The following function names are reserved functions of one argument in compute():
        - int, float, str, len, sum, tuple, values, not, min, max, sorted.
        - These all do the same things as in normal Python ('values' means dict.values).
        - Unlike in base Python, the "not" function requires parens; so "not(expr)".
        - Note that since you can't define arrays of numbers in a compute() expression,
            you can't actually use "sum" on anything other than arrays passed in as
            variables.
        - You can easily add new functions that take one variable as an argument
            by adding new name-function pairs to the "ufunctions" dict that is defined
            above.
        - An unfortunate corrolary of the above observation is that if you added enough
            ufunctions, you could undoubtedly find a way to do something dangerous
            with compute().
        - You cannot specify a key or the "reversed" parameter for "sorted(x)".
    - "map" is also a reserved function of two arguments.
        - "`fun` map itbl" works very much like map(func, itbl) in base Python; it also
            returns a generator expression applying a function to everything in itbl.
        - Note that the proper syntax is "x map y", not map(x,y), because my parser
            does not support the latter method for calling binary operators.
        - Also, eqn must be a compute expression of one variable or a function name in
            ufunctions. Because eqn is a string literal within the context of the
            compute() expression, eqn must be backtick-enclosed.
    - "=~" is a reserved function of two arguments, both strings.
        - "`string` =~ `pat`" is equivalent to (re.search(pat, string) is not None).
    - "sub" is a reserved function that accepts two arguments.
        - The proper syntax is "<string/varname> sub "<regex>//<replacement>"
        - The above is equivalent to re.sub(<regex>, <replacement>, <string/varname>)
    - The arithmetic and logic binops work fine for pandas Series and numpy arrays,
        but the float, str, and int functions only work on scalars.
        - To change the type of a numpy array or pandas Series, use the "intar",
            "floatar", and "strar" functions to change to the type before the "ar".
    '''
    tokens = tokenize(eqn)
    varnames = get_varnames(tokens, safe)
    evald_tokens = evaluate_tokens(tokens, varnames, safe)
    ComputeLogger.debug(f"evald_tokens = {evald_tokens}")
    stackfunc = resolve_big_stack(evald_tokens, varnames)
    if isinstance(stackfunc, function):
        if safe:
            def outfunc(*args):
                for arg in args:
                    if type(arg) not in {int, float, bool, Fraction, Decimal, complex}:
                        raise ValueError("Functions produced by compute() with safe = True do not accept non-numeric arguments.")
                return stackfunc(args)
            outfunc.__doc__ = eqn + "\nArgs are positional-only in the order {}\nThis function only accepts numeric arguments.".format(varnames)
        else:
            def outfunc(*args):
                return stackfunc(args)
            outfunc.__doc__ = eqn + "\nArgs are positional-only in the order {}.".format(varnames)
        return outfunc
    else:
        return stackfunc


def safe_compute(eqn):
    '''wrapper for compute(eqn, safe = True)'''
    return compute(eqn, safe = True)