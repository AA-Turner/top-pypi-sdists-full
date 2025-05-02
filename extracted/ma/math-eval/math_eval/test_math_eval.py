from math_eval import *
import random
import string
import itertools
import traceback
import sys
import math
try:
    import pandas as pd
except:
    pass # should enable people w/o pandas to use my ComputeTester object for testing

values = lambda dict_: dict_.values()   

def five_to_the_x(x): return 5**x
def five_to_the_float_x(x): return 5**float(x)
problem_eqn = "-3----3//-(Q)*(2/-2.8659-2.4492)"
my_eqn = "5.3*2**x // x - 5.4*43 + x ** -3/0.7"
xs = [x/2 for x in range(-11, 12, 2)]
ufunctions_binops_example = "len(int(2*(-(2+3**2))/x)*tuple(`int` map y))"
nested_map_example = ("int(2*(-(2+3**2))/x)"
                      "*sum(tuple("
                                  "`float(x)**(3/"
                                  "tuple(\\`int\\` map \\`733\\`)[2])`"
                            "map y))")


def approx_equal(x,y, epsilon = 10*sys.float_info.epsilon, na_equal = False):
    '''If x and y are both numbers, returns True if abs(x-y) is very close to the
minimum precision of float numbers.
If x or y is not a number, returns (x==y).
If na_equal is True, it will return True if x and y are both float('nan').'''    
    try:
        good = abs(x-y) <= epsilon
        if na_equal and not good:
            return good | (math.isnan(x) & math.isnan(y))
        return good
    except:
        return x == y


def test_resolve_binop(elts = [five_to_the_x, 0, -1, 2, -0.5, 'w', 'x'],
                       binops = [operator.add, operator.mul],
                       xs = [-1, 0, 1]):
    for e1, func, e2, x in itertools.product(elts, binops, elts, xs):
        outfunc = resolve_binop(e1, func, e2, ['w', 'x'])
        if isinstance(outfunc, (function, ResoBin)):
            print(e1, func, e2, x, outfunc(x))
        else:
            print(e1, func, e2, x, outfunc)


class ImmutableDict:
    '''What it says on the tin. Behaves like a normal dict, but has no 
    methods for adding or removing elements. Also doesn't have the overloaded '|'.
Useful chiefly because an ImmutableDict can be an item in a set or a key in a dict
    because it's hashable, whereas a normal dict is not hashable.'''
    def __init__(self, items):
        self.__dict = dict(items)
    def __getitem__(self, x):
        return self.__dict[x]
    def get(self, x, default = None):
        return self.__dict.get(x, default)
    def keys(self):
        return self.__dict.keys()
    def values(self):
        return self.__dict.values()
    def items(self):
        return self.__dict.items()
    def copy(self):
        return ImmutableDict(self.__dict.copy())
    def __str__(self):
        return "ImmutableDict({})".format(self.__dict)
    __repr__ = __str__
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return isinstance(other, ImmutableDict) and str(self)==str(other)
    def __len__(self):
        return len(self.__dict)
    def __iter__(self):
        return iter(self.__dict)
    @classmethod
    def fromkeys(self, itbl, value = None):
        return ImmutableDict({k: value for k in itbl})


class ComputeTester: #TODO: figure out how to capture error eqns
    def __init__(self):
        self.bad_eqns = {}
        self.good_eqns = {}
        self.error_eqns = {}
        self.comp_errors = {}
        self.true_errors = {}
        self.dframe = None
    def _build_dframe(self):
        try:
            self.dframe = pd.DataFrame()
        except:
            return
        eqns = []
        inputs = []
        true_outputs = []
        comp_outputs = []
        comp_errors, true_errors = [], []
        statuses = ['good' for x in self.good_eqns] + ['bad' for x in self.bad_eqns] + ['error' for x in self.error_eqns]
        for eqn in self.good_eqns:
            if isinstance(eqn, tuple):
                eqns.append(eqn[0])
                inputs.append(eqn[1])
            else:
                eqns.append(eqn)
                inputs.append(None)
            true_outputs.append(self.good_eqns[eqn]['true'])
            comp_outputs.append(self.good_eqns[eqn]['comp'])
            true_errors.append(self.true_errors[eqn])
            comp_errors.append(self.comp_errors[eqn])
        for eqn in self.bad_eqns:
            if isinstance(eqn, tuple):
                eqns.append(eqn[0])
                inputs.append(eqn[1])
            else:
                eqns.append(eqn)
                inputs.append(None)
            true_outputs.append(self.bad_eqns[eqn]['true'])
            comp_outputs.append(self.bad_eqns[eqn]['comp'])
            true_errors.append(self.true_errors[eqn])
            comp_errors.append(self.comp_errors[eqn])
        for eqn in self.error_eqns:
            if isinstance(eqn, tuple):
                eqns.append(eqn[0])
                inputs.append(eqn[1])
            else:
                eqns.append(eqn)
                inputs.append(None)
            true_outputs.append(self.error_eqns[eqn]['true'])
            comp_outputs.append(self.error_eqns[eqn]['comp'])
            true_errors.append(self.true_errors[eqn])
            comp_errors.append(self.comp_errors[eqn])
        self.dframe['eqns'] = eqns
        self.dframe['inputs'] = inputs
        self.dframe['true_outputs'] = true_outputs
        self.dframe['comp_outputs'] = comp_outputs
        self.dframe['statuses'] = statuses
        self.dframe['operators'] = [tuple(op_regex.findall(eqn)) for eqn in eqns]
        self.dframe['true_errors'] = true_errors
        self.dframe['comp_errors'] = comp_errors
        del statuses, eqns, inputs, true_outputs, comp_outputs, true_errors, comp_errors
        # self.statuses = self.dframe['statuses']
        # self.eqns = self.dframe['eqns']
        # self.inputs = self.dframe['inputs']
        # self.true_outputs = self.dframe['true_outputs']
        # self.comp_outputs = self.dframe['comp_outputs']
        # self.statuses = self.dframe['statuses']
        # self.operators = self.dframe['operators']


backtickstring_acceptable_errors = "(?:un|not )supported.+?\'(?:str|int|bool)\' and \'(?:str|int|bool)\'"
# errors of the type "TypeError: unsupported operand type(s) for -: 'str' and 'float'"
numeric_acceptable_errors = "ZeroDivision|Overflow|complex"
# the "complex" covers errors like 
# "TypeError: '>' not supported between instances of 'complex' and 'int'"

def _compare_eqn_evaluations(tester, 
                             eqn, 
                             tb_true, 
                             tb_comp, 
                             input_, 
                             c_out, 
                             t_out, 
                             acceptable_error_types,
                             na_equal):
    if (tb_true is None) and (tb_comp is None): # neither function had an error
        if approx_equal(c_out, t_out, na_equal = na_equal): # all good
            if input_ is None:
                tester.good_eqns[eqn] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[eqn] = 'None'
                tester.true_errors[eqn] = 'None'
            else:
                tester.good_eqns[(eqn, input_)] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[(eqn, input_)] = 'None'
                tester.true_errors[(eqn, input_)] = 'None'
        else: # the two outputs are not equal
            if input_ is None:
                tester.bad_eqns[eqn] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[eqn] = 'None'
                tester.true_errors[eqn] = 'None'
            else:
                tester.bad_eqns[(eqn, input_)] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[(eqn, input_)] = 'None'
                tester.true_errors[(eqn, input_)] = 'None'
        return
    true_error_OK = None
    comp_error_OK = None
    tb_string_comp, tb_string_true = 'None', 'None'
    fatal = False
    message = "eqn = {}, input_ = {}\n".format(repr(eqn), input_)
    if tb_true is not None: # true function had an error
        tb_string_true = list(tb_true.format_exception_only())[0]
        true_error_OK = re.findall(acceptable_error_types, tb_string_true)
        message += "~~~~~~~~~~~~~\nTrue output:\n" + ''.join(tb_true.format())
        if not true_error_OK:
            fatal = True
    else:
        message += "~~~~~~~~~~~~~\nTrue output:\n" + str(t_out)
    
    if tb_comp is not None: # compute had an error
        tb_string_comp = list(tb_comp.format_exception_only())[0]
        comp_error_OK = re.findall(acceptable_error_types, tb_string_comp)
        message += "\n~~~~~~~~~~~~~\nCompute output:\n" + ''.join(tb_comp.format())
        if not comp_error_OK:
            fatal = True
    else:
        message += "\n~~~~~~~~~~~~~\nCompute output:\n" + str(c_out)
    
    if fatal:
        # Either my function or the "true" function errored out for an unacceptable
        # reason, and testing should be halted and the user notified.
        return message
    elif isinstance(comp_error_OK, list) and isinstance(true_error_OK, list):
        if comp_error_OK[-1] != true_error_OK[-1]:
            # they both errored out for "acceptable" reasons, but not the same reason.
            # My function is faulted for this, but the discrepancy should not cause 
            # testing to stop.
            if input_ is None:
                tester.bad_eqns[eqn] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[eqn] = tb_string_comp
                tester.true_errors[eqn] = tb_string_true
            else:
                tester.bad_eqns[(eqn, input_)] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[(eqn, input_)] = tb_string_comp
                tester.true_errors[(eqn, input_)] = tb_string_true
        else:
            # They both errored out for the same "acceptable" reason.
            # My function is not faulted for this, and testing should not stop.
            if input_ is None:
                tester.error_eqns[eqn] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[eqn] = tb_string_comp
                tester.true_errors[eqn] = tb_string_true
            else:
                tester.error_eqns[(eqn, input_)] = {'comp': c_out, 'true': t_out}
                tester.comp_errors[(eqn, input_)] = tb_string_comp
                tester.true_errors[(eqn, input_)] = tb_string_true
    else:
        # One of them errored out for an "acceptable" reason and the other did not
        # have an error at all.
        # My function is faulted for this discrepancy, but testing should not stop.
        if input_ is None:
            tester.bad_eqns[eqn] = {'comp': c_out, 'true': t_out}
            tester.comp_errors[eqn] = tb_string_comp
            tester.true_errors[eqn] = tb_string_true
        else:
            tester.bad_eqns[(eqn, input_)] = {'comp': c_out, 'true': t_out}
            tester.comp_errors[(eqn, input_)] = tb_string_comp
            tester.true_errors[(eqn, input_)] = tb_string_true
            
   
def evaluate_eqn_on_inputs(computer, 
                           eqn,
                           inputs, 
                           tester, 
                           acceptable_error_types,
                           na_equal,
                           lambda_eqn = None): 
    varnames = get_varnames(tokenize(eqn), safe = False)
    if varnames:
        tb_comp = None
        tb_true = None
        full_inputs = []
        for ii in range(5):
            full_inputs.append(tuple(random.choice(inputs) for var in range(len(varnames))))
        try:
            comp_fun = computer(eqn)
        except Exception as ex:
            tb_comp = traceback.TracebackException.from_exception(ex)
        try:
            if lambda_eqn:
                # for cases where compute syntax differs from normal Python syntax
                true_fun = eval("lambda {}: {}".format(','.join(varnames), lambda_eqn))
            else:
                true_fun = eval("lambda {}: {}".format(','.join(varnames), eqn))
        except Exception as ex:
            tb_true = traceback.TracebackException.from_exception(ex)
        for input_ in full_inputs:
            comp_out = float('nan')
            true_out = float('nan')
            if tb_comp is not None: # there was an error building the compute function
                tb_comp_in = tb_comp
            else: # let's try the compute function on this input
                try:
                    comp_out = comp_fun(*input_)
                    tb_comp_in = None
                except Exception as ex: # oops! bad input!
                    tb_comp_in = traceback.TracebackException.from_exception(ex)
            if tb_true is not None: # there was an error building the true function
                tb_true_in = tb_true
            else: # let's try the true function on this input
                try:
                    true_out = true_fun(*input_)
                    tb_true_in = None
                except Exception as ex: # oops! bad input!
                    tb_true_in = traceback.TracebackException.from_exception(ex)
            compare_result = _compare_eqn_evaluations(tester, 
                                                      eqn, 
                                                      tb_true_in, 
                                                      tb_comp_in, 
                                                      input_, 
                                                      comp_out, 
                                                      true_out, 
                                                      acceptable_error_types,
                                                      na_equal)
            if isinstance(compare_result, str): # fatal error, kill testing now
                return compare_result
            
    else: # both inputs are scalars
        comp_out = float('nan')
        true_out = float('nan')
        tb_comp = None
        tb_true = None
        try:
            comp_out = computer(eqn)
        except Exception as ex:
            tb_comp = traceback.TracebackException.from_exception(ex)
        try:
            if lambda_eqn:
                true_out = eval(lambda_eqn)
            else:
                true_out = eval(eqn)
        except Exception as ex:
            tb_true = traceback.TracebackException.from_exception(ex)
        compare_result = _compare_eqn_evaluations(tester, 
                                                  eqn, 
                                                  tb_true, 
                                                  tb_comp, 
                                                  None, 
                                                  comp_out, 
                                                  true_out, 
                                                  acceptable_error_types,
                                                  na_equal)
        if isinstance(compare_result, str): # fatal error, kill testing now
            return compare_result


def test_compute_one_op(computer = compute, 
                        include_comparisons = True,
                        include_logic = True,
                        include_strings = True,
                        acceptable_error_types = numeric_acceptable_errors,
                        na_equal = True):
    tester = ComputeTester()
    tokens = ['x', '3', '5.7432', '0', '-4', '-2.3', 'w', "`ab`"]
    inputs = [3, 0.5, -4, -5.2, 0, frozenset({'1',2,(1,2)}), '123']
    funcs = ['+', '-', '*', '/', '//', '%', '**']
    comparison_funcs = ['>', '<', '<=', '>=', '==', '!=']
    ufunctions = list(globals()['safe_ufunctions']) + ['']
    if include_logic:
        funcs = ['+', '-', '*', '//', '%', '**', '^', '|', '&']
    if include_comparisons:
        funcs += comparison_funcs
    if include_strings:
        ufunctions = ['sum', 'len','int','float','str','tuple', 'not', 'set', '']
        funcs += ['in']
    for (ufunc1, in1, func, ufunc2, in2) in itertools.product(ufunctions, 
                                                              tokens, 
                                                              funcs, 
                                                              ufunctions, 
                                                              tokens):
        eqn = ' {u1}({i1}) {f} ({u2}({i2}))'.format(u1=ufunc1, i1=in1, f=func, u2=ufunc2, i2=in2)
        lambda_eqn = None
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester,
                                             acceptable_error_types,
                                             na_equal,
                                             lambda_eqn)
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def test_map(computer = compute,
             acceptable_error_types = numeric_acceptable_errors + '|' + backtickstring_acceptable_errors,
             na_equal = True):
    tester = ComputeTester()
    ufunctions = ['str', 'tuple','set', '']
    inputs = [five_to_the_x, '123', frozenset({2, 5, 9})]
    tokens = ['w', "`int`", "`str(x)+\\`3\\``", "`a\\`bun\\`bar`", 'x']
    oldlen = 0
    for tok1, ufunc, tok2, input_ in itertools.product(tokens, 
                                                       ufunctions, 
                                                       tokens, 
                                                       inputs):
        eqn = 'tuple( {t1} map {uf}({t2}))'.format(t1=tok1, uf=ufunc, t2=tok2)
        if tok1 == "`str(x)+\\`3\\``":
            tok1_adj = "lambda x: str(x) + '3'"
        elif tok1 == '`int`':
            tok1_adj = 'int'
        else:
            tok1_adj = tok1
        lambda_eqn = 'tuple(map({t1a}, {uf}({t2})))'.format(t1a=tok1_adj, uf=ufunc, t2=tok2)
        lambda_eqn = re.sub("(?<!\\\\)`", "'", lambda_eqn).replace("\\`", "`")
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester,
                                             acceptable_error_types,
                                             na_equal,
                                             lambda_eqn)
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def test_compute_two_ops(computer = compute, 
                         include_comparisons = True,
                         include_logic = False,
                         acceptable_error_types = numeric_acceptable_errors,
                         na_equal = True):
    tester = ComputeTester()
    inputs = [1, 0.5, -4, -5.2, 0]
    funcs = ['+', '-', '*', '/', '//', '%', '**']
    tokens = ['x', '3', '5.7432', '0', '-4', '-2.3', 'w', "`ab`"]
    if include_logic:
        funcs = ['+', '-', '*', '//', '%', '**', '^', '|', '&']
        tokens = ['a', '1', '-2', '0', 'b', 'c']
        inputs = [2, 0, -3]
    if include_comparisons:
        funcs += ['>', '<', '<=', '>=', '==', '!=']
    for (optional_uminus, in1, func1, in2, func2, in3) in itertools.product(['', '-'], tokens, funcs, tokens, funcs, tokens):
        eqn = optional_uminus + in1 + func1 + in2 + func2 + in3
        if include_logic and ('**' in eqn):
            eqn = re.sub("\*\*-", '**', eqn)
            inputs = [2, 0]
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester, 
                                             acceptable_error_types,
                                             na_equal)
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def test_getitem(computer = compute,
             acceptable_error_types = numeric_acceptable_errors + '|' + backtickstring_acceptable_errors,
             na_equal = True):
    tester = ComputeTester()
    inputs = [ImmutableDict({'a': 1, 1: 2}), 
              ImmutableDict({'b': 3}), 
              '123', 
              (7, 8, 9, 10, 11)]
    iterables = ['w', "tuple(`str` map y)", "str(z)", "`a\\`bun\\`bar`",
                 '-x']
    slicers = ['`a`', '1', '1:', ':', '-3::-1', ':4:2', ':3', 'int(x[0])']
    oldlen = 0
    for itbl, inp, slicer in itertools.product(iterables, inputs, slicers):
        eqn = '{it}[{sli}]'.format(it=itbl, sli=slicer)
        if itbl == "tuple(`str` map y)":
            itbl_adj = "tuple(map(str, y))"
        else:
            itbl_adj = itbl
        lambda_eqn = '{ita}[{sli}]'.format(ita=itbl_adj, sli = slicer)
        lambda_eqn = re.sub("(?<!\\\\)`", "'", lambda_eqn).replace("\\`", "`")
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester,
                                             acceptable_error_types,
                                             na_equal,
                                             lambda_eqn)
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def examine_bad_two_ops(tester2):
    bad_ops = {}
    for eqn in tester2.bad_eqns:
        if isinstance(eqn, tuple):
            eqn, input_ = eqn
        else:
            input_ = None
        split_eqn = op_regex.split(eqn)
        bad_ops.setdefault((split_eqn[1],split_eqn[3]), set())
        bad_ops[(split_eqn[1], split_eqn[3])].add(input_)
    return bad_ops


def make_random_eqn(num_ops = 5,
                    num_vars = 1,
                    intrange = range(-20, 21),
                    floatrange = range(-20, 21),
                    include_comparisons = True,
                    include_logic = False,
                    include_ufunctions = False):
    out = ''
    varnames = []
    for varnum in range(num_vars):
        var_ = ''.join(random.sample(string.ascii_letters, random.randint(1,2)))
        while var_ in varnames:
            var_ = ''.join(random.sample(string.ascii_letters, random.randint(1,2)))
        try: # check if this varname is syntactically valid in Python
            fun = eval("lambda {}: 1".format(var_))
        except: # we randomly generated a reserved word as a varname
            var_ = 'x'*(varnum+3)
        if include_ufunctions and random.random() < 0.5:
            var_ += random.choice(['ii','ff'])
        varnames.append(var_)
    
    comparators = ['>', '<', '>=', '<=', '==', '!=']
    logic_funcs = ['^', '|', '&']
    ufunctions = ['int', 'float', 'not']
    if include_logic:
        # bitwise logic functions raise TypeErrors when used with floats
        vartypes = [int] + [str]*num_vars 
        funcs = ['-', '+', '*', '//', '%', '**']
        intrange = range(0, intrange.stop)
    else:
        vartypes = [int, float]+[str]*num_vars
        funcs = ['-', '+', '*', '/', '//', '%', '**']
    
    ufunc = False
    parens_opened = []
    for opnum in range(num_ops):
        if random.random() < 0.3:
            if include_logic:
                if out[-2:] != '**':
                    # if the last token was exponentiation, the unary minus would lead
                    # exponentiation to a negative power, and the integers are not
                    # closed under that operation
                    out += '-'
                else:
                    pass
            else:
                out += '-'
        vartype = random.choice(vartypes)
        if not parens_opened:
            if random.random() < 0.25:
                if random.random() < 0.5 and include_ufunctions:
                    out += '(' + random.choice(ufunctions)
                    parens_opened.append(opnum)
                    ufunc = True
                out += '('
                parens_opened.append(opnum)
        if vartype == int:
            out += str(random.choice(intrange))
        elif vartype == float:
            out += str(round(random.choice(floatrange) + random.random(), 4))
        else:
            out += random.choice(varnames)
        if random.random() < min(1, 0.33333*len(parens_opened)):
            if ufunc:
                out += ')'
                parens_opened.pop(0)
                ufunc = False
            out += ')'
            parens_opened.pop(0)
        rand = random.random()
        if include_comparisons and include_logic:
            if rand < 0.18:
                out += random.choice(comparators)
            elif rand > 0.82:
                out += random.choice(logic_funcs)
            else:
                out += random.choice(funcs)
        elif include_logic:
            if rand < 0.25:
                out += random.choice(logic_funcs)
            else:
                out += random.choice(funcs)
        elif include_comparisons:
            if rand < 0.25:
                out += random.choice(comparators)
            else:
                out += random.choice(funcs)
        else:
            out += random.choice(funcs)
    vartype = random.choice(vartypes)
    if vartype == int:
        out += str(random.choice(intrange))
    elif vartype == float:
        out += str(round(random.choice(intrange) + random.random(), 4))
    else:
        out += random.choice(varnames)
    for ii in range(len(parens_opened)):
        out += ')'
    return out


def make_random_backtickstring_eqn(num_ops = 5,
                                    num_vars = 1,
                                    intrange = range(-1, 50),
                                    include_comparisons = True,
                                    include_logic = False,
                                    include_ufunctions = True):
    out = ''
    vartypes = [int, str] + ['var']*num_vars
    comparison_since_last_logic = False
    logic_since_last_comparison = True
    comparisons = 0
    
    funcs = ['+', '*']
    comparators = ['>', '<', '==', '!=', '<=', '>=', '=~']
    logic_funcs = ['^', '|', '&']
    ufunctions = ['int', 'float', 'not', 'str', 'tuple', 'len', 'set']
    
    varnames = []
    for varnum in range(num_vars):
        var_ = ''.join(random.sample(string.ascii_letters, random.randint(1,2)))
        while var_ in varnames:
            var_ = ''.join(random.sample(string.ascii_letters, random.randint(1,2)))
        try: # check if this varname is syntactically valid in Python
            fun = eval("lambda {}: 1".format(var_))
        except: # we randomly generated a reserved word as a varname
            var_ = 'x'*(varnum+3)
        varnames.append(var_)
    
    parens_opened = []
    for opnum in range(num_ops):
        if not parens_opened:
            if random.random() < 0.25:
                if random.random() < 0.5 and include_ufunctions:
                    out += random.choice(ufunctions)
                out += '('
                parens_opened.append(opnum)
        
        vartype = random.choice(vartypes)
        if vartype == int:
            out += str(random.choice(intrange))
        elif vartype == str:
            out += '`' + ''.join(random.choices(string.ascii_letters+'1234567890', k=3)) + '`'
        else:
            out += random.choice(varnames)
        
        if random.random() < min(1, 0.33333*len(parens_opened)):
            out += ')'
            parens_opened.pop(0)
        rand = random.random()
        if include_comparisons and include_logic:
            if (rand < 0.18 or not comparison_since_last_logic) and logic_since_last_comparison and (comparisons < 2):
                comparison_since_last_logic = True
                logic_since_last_comparison = False
                comparisons += 1
                out += random.choice(comparators)
            elif (rand > 0.82 and comparison_since_last_logic) or not logic_since_last_comparison:
                out += random.choice(logic_funcs)
                comparison_since_last_logic = False
                logic_since_last_comparison = True
            else:
                out += random.choice(funcs)
        elif include_comparisons:
            if rand < 0.25:
                out += random.choice(comparators)
            else:
                out += random.choice(funcs)
        else:
            out += random.choice(funcs)
    vartype = random.choice(vartypes)
    if vartype == int:
        out += str(random.choice(intrange))
    elif vartype == str:
        out += '`' + re.sub('`', '\\`', 
                            ''.join(random.choices(string.printable, k=3))) + '`'
    else:
        out += random.choice(varnames)
    for ii in range(len(parens_opened)):
        out += ')'
    return out


def test_random_eqns(computer = compute,
                     n = 2000,
                     num_inputs = 4,
                     sizerange = range(6, 9), 
                     numvar_range = range(0,5),
                     intrange = range(-20, 21),
                     floatrange = range(-20, 21),
                     include_comparisons = False,
                     include_logic = False,
                     include_ufunctions = False,
                     acceptable_error_types = numeric_acceptable_errors,
                     na_equal = True):
    tester = ComputeTester()
    inputs = []
    for ii in range(-2,num_inputs-2):
        if int(ii/2)==ii:
            inputs.append(int(ii/2))
        elif not include_logic:
            inputs.append(ii/2)
    for ii in range(n):
        eqn = make_random_eqn(random.choice(sizerange),
                              random.choice(numvar_range),
                              intrange,
                              floatrange,
                              include_comparisons,
                              include_logic,
                              include_ufunctions)
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester, 
                                             acceptable_error_types,
                                             na_equal)
        # return inputs, eqn, eval_result
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def test_random_backtickstring_eqns(computer = compute,
                     n = 2000,
                     num_inputs = 5,
                     sizerange = range(6, 9), 
                     numvar_range = range(0,5),
                     intrange = range(-3, 50),
                     include_comparisons = True,
                     include_logic = True,
                     include_ufunctions = False,
                     acceptable_error_types = backtickstring_acceptable_errors,
                     na_equal = True):
    tester = ComputeTester()
    inputs = list(range(-1, -1+num_inputs))
    for ii in range(n):
        eqn = make_random_backtickstring_eqn(random.choice(sizerange),
                                             random.choice(numvar_range),
                                             intrange,
                                             include_comparisons,
                                             include_logic,
                                             include_ufunctions)
        lambda_eqn = re.sub(r'\\?`','"', eqn)
        eval_result = evaluate_eqn_on_inputs(computer, 
                                             eqn,
                                             inputs, 
                                             tester, 
                                             acceptable_error_types,
                                             na_equal,
                                             lambda_eqn)
        # return inputs, eqn, eval_result
        if eval_result is not None:
            print(eval_result)
            return
    tester._build_dframe()
    return tester


def test_IntRange():
    ranges = [range(1,2), 
              range(17), 
              range(5, 72, 4), 
              range(115, 40, -5),
              range(1, 1),
              range(1, -1)]
    IntRanges = [IntRange(1, 2), 
              IntRange(17), 
              IntRange(5, 72, 4), 
              IntRange(115, 40, -5),
              IntRange(1, 1),
              IntRange(1, -1)]
    results = []
    for rng, irng in zip(ranges, IntRanges):
        results.append(set(rng).symmetric_difference(set(irng)))
    return results, ranges, IntRanges


if __name__ == '__main__':
    pass
    for rst, rng, irng in zip(*test_IntRange()):
        if len(rst) != 0:
            print("Expected {} to have same contents as {}, but it didn't!".format(irng, rng))
    tester1 = test_compute_one_op(computer = compute, include_logic = True, include_strings = True, acceptable_error_types = '')
    if tester1.dframe is not None:
        df1 = tester1.dframe
        del df1['operators']
        bad1 = df1.loc[df1.statuses == 'bad', df1.columns!='statuses']
    
    testermap = test_map(acceptable_error_types = '')
    if testermap.dframe is not None:
        dfmap = testermap.dframe
        del dfmap['operators']
        badmap = dfmap.loc[dfmap.statuses == 'bad', dfmap.columns!='statuses']
        
    testerg = test_getitem(acceptable_error_types='')
    if testerg.dframe is not None:
        dfg = testerg.dframe
        badg = dfg[dfg.statuses=='bad']
        dfg_errors = dfg[['comp_errors', 'true_errors']].value_counts()
    
    tester2 = test_compute_two_ops(computer = compute, include_logic = True)
    if tester2.dframe is not None:
        bad2 = tester2.dframe[tester2.dframe.statuses == 'bad']
        bad2 = pd.concat((bad2, bad2.operators.astype(str).str.split(', ',expand=True).rename({ii: 'op'+str(ii+1) for ii in range(6)},axis = 1)), axis = 1)
        bad2_ops =  [bad2['op'+str(ii)].value_counts() for ii in range(1,7)]
        assert all(bad2.operators.astype(str).str.count("\||\^|&|[<=>!]=?")==2), \
            'There was at least one case in which an equation with two operators failed for some reason other than having two logical/comparison operators.'
        # we know that every time we have two comparison/logical operators without
        # appropriate grouping parentheses, my function will get a different answer
        # from the corresponding lambda functions, but only because we follow different
        # orders of operations.
        # Thus, we only care about different return values due to something other than
        # the order of operations.
    
    tester3 = test_random_eqns(n = 25_000, 
                               numvar_range = range(0,5),
                               sizerange = range(6, 9), 
                               intrange = range(-3, 4), 
                               floatrange = range(-3, 4),
                               acceptable_error_types = numeric_acceptable_errors,
                               include_ufunctions = True)
    if tester3.dframe is not None:
        df3 = tester3.dframe
        bad3 = df3.loc[df3.statuses=='bad', df3.columns!='statuses']
        bad3_errors = bad3[['comp_errors','true_errors']].value_counts()
        df3_errors = df3[['comp_errors', 'true_errors']].value_counts()
    
    # tester4 = test_random_backtickstring_eqns(10000, acceptable_error_types = '')
    # if tester4.dframe is not None:
        # df4 = tester4.dframe
        # bad4 = df4.loc[df4.statuses=='bad', df4.columns!='statuses']
    
# badeqn = '`z^H`>gJ^(`ecC`<gJ)+`|fu`<S+gJ+S'
# tester = ComputeTester()
