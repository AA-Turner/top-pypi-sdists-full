'''
We want to safely evaluate mathematical expressions, without ever
    getting anywhere near the dreaded eval().
The established solutions include:
    - ast.literal_eval
    - numexpr
    - checking a string with regular expressions to see if it's safe
        then using eval()
    - building a calculator with ply (Python Lex/Yacc)
Unfortunately, all established solutions are:
    a: limited in scope OR
    b: slow-running (even eval() itself takes several microseconds 
        to do simple math).
and ast.literal_eval is really picky about inputs.

Not only that, most safe evaluation functions exclude variable names by design.
This module is designed for use cases where the user passes in a query string that 
    encodes a mathematical test for numbers (like only select values that are greater
    than 2), and they're going to be reusing that same test over and over again.
    It has been tested (using test_math_eval) on Python 3.6-3.9.
The compute-intensive work of parsing strings as equations is done
    up-front, and the resultant function uses pure math operations
    to work in a few hundred ns per variable rather than 5-50 microseconds per variable.
That said, the initial evaluation of an expression is perhaps 10-25x slower than the
    evaluation of the corresponding expression with eval() or numexpr.
Functions:
    math_eval(string): evaluates mathematical expressions (including comparisons) 
        with exactly one ASCII word allowed.
    compute(string): parses an expression including arithmetic, comparisons, logical
        operators, string literals, array slicers, a few reserved functions of one
        argument, regex replacement and membership checking,
        and a "map" function, and returns:
            a scalar, or a function that operates on any number of variables.
    safe_compute(string): as compute, but only allows math operations and only
        accepts numeric inputs.
    IntRange: like a builtin range() object, but  it is treated as *equaling* all
        elements in it as well as *containing* them.
    TODO: Add support for fun(arg1, arg2,..., argn)-type syntax in compute().
    TODO: Add syntax for defining a new function or variable within compute expressions.
'''
from math_eval.math_eval import *
from .Equation import Equation
__version__ = '0.2.4'