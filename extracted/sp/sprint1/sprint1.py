"""Calculator package!"""

__version__ = "0.2"

from cmath import nan
import math
from math import isnan, isinf
import py.test
import itertools
from hypothesis import given, assume, strategies as st 


class Calculator:
    '''This is a calculator class
    Create an instance newCalc = Calculator()
    and call function like: newCalc.add(2)'''
    memory = 0.0

    def add(self,input):
        Calculator.memory +=  input
        return Calculator.memory

    def sub(self, input):
        Calculator.memory -=  input
        return Calculator.memory

    def mul(self, input):
        Calculator.memory *=  input
        return Calculator.memory

    def div(self, input):
        if input == 0:
            return nan
        else:
            Calculator.memory /=  input 
            return Calculator.memory
    

    def root(self,  input):
        if input <= 0:
            return nan
        else:
            Calculator.memory = Calculator.memory ** (1.0 / input)
            return Calculator.memory
        
    def reset(self):
        Calculator.memory = 0.0
        return Calculator.memory 



'''Test of addition function'''
@given(
    st.floats()
)
def test_add(x): 
    assume(not isnan(x))
    newCalc = Calculator()
    newCalc.reset()
    assert newCalc.add(x) == x
    assert newCalc.add(x) == x+x
    assert newCalc.add(x) == x+x+x

'''Test of substraction function'''
@given(
    st.floats()
)
def test_sub(x): 
    assume(not isnan(x))
    assume(x !=0 )
    newCalc = Calculator()
    newCalc.reset()
    assert math.isclose(newCalc.sub(x) , -x, abs_tol = 0.0001 )
    assert math.isclose(newCalc.sub(x) , -x-x, abs_tol = 0.0001)
    assert math.isclose(newCalc.sub(x) , -x-x-x, abs_tol = 0.0001)

'''Test of multiplication function'''
@given(
    st.floats()
)
def test_mul(x): 
    assume(not isnan(x))
    assume(not isinf(x))
    newCalc = Calculator()
    newCalc.reset()
    assert math.isclose(newCalc.mul(x) , newCalc.memory * x, abs_tol = 0.0001 )
    assert math.isclose(newCalc.mul(x) , newCalc.memory * x*x, abs_tol = 0.0001)
    assert math.isclose(newCalc.mul(x) , newCalc.memory * x*x*x, abs_tol = 0.0001)

'''Test of division function'''
@given(
    st.floats()
)
def test_div(x): 
    assume(not isnan(x))
    assume(not isinf(x))
    assume(x !=0 )
    newCalc = Calculator()
    newCalc.reset()
    assert math.isclose(newCalc.div(x) , newCalc.memory /x, abs_tol = 0.0001 )
    assert math.isclose(newCalc.div(x) , newCalc.memory /x/x, abs_tol = 0.0001)
    assert math.isclose(newCalc.div(x) , newCalc.memory /x/x/x, abs_tol = 0.0001)
    assert math.isnan(newCalc.div(0))

'''Test of root function'''
@given(
    st.floats()
)
def test_root(x): 
    assume(not isnan(x))
    assume(not isinf(x))
    assume(x > 0 )
    assume (abs(x)> 0.001)
    newCalc = Calculator()
    newCalc.reset()
    assert math.isclose(newCalc.root(x) , newCalc.memory ** (1.0 / x), abs_tol = 0.0001 )
    assert math.isclose(newCalc.root(x) , newCalc.memory ** (1.0 / x) ** (1.0 / x), abs_tol = 0.0001)
    assert math.isclose(newCalc.root(x) , newCalc.memory ** (1.0 / x) ** (1.0 / x) ** (1.0 / x), abs_tol = 0.0001)
    assert math.isnan(newCalc.root(0))
