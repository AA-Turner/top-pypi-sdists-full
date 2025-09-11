import math
from .type_utils import det_bool_T,is_number
from functools import reduce

"""
math_utils.py

This module offers a set of mathematical utility functions tailored to perform specific calculations. Some of its functionalities include:
- Computing the quotient and remainder of dividing two numbers.
- Rounding up numbers to the nearest integer.
- Checking if a number falls outside a given range or boundary.

Usage:
    import abstract_utilities.math_utils as math_utils This module is part of the `abstract_utilities` package.

As part of the `abstract_utilities` package, the module serves to abstract and simplify certain mathematical operations that may be frequently used in various applications.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""

def get_multiply_remainder(x: int, y: int) -> tuple:
    """
    Computes the quotient and remainder of dividing x by y.

    Args:
        x (int): The dividend.
        y (int): The divisor.

    Returns:
        tuple: A tuple containing the quotient and remainder.
    """
    if x <= y:
        return 0, x
    mul = int(float(x) / float(y))
    return mul, int(x) - int(mul * y)
def rounded_up_integer(number: (float or int)) -> int:
    """
    Rounds up a given number to the nearest integer and returns the result.

    Parameters:
    number (float or int): The number to be rounded up.

    Returns:
    int: The rounded up integer value of the input number.
    """
    if isinstance(number, int):
        number = float(number)
    
    if isinstance(number, float):
        number = math.ceil(number)
    
    return number
def out_of_bounds(upper: (int or float) = 100, lower: (int or float) = 0, obj: (int or float) = -1):
    """
    Checks if the given object is out of the specified upper and lower bounds.

    Args:
        upper (int or float): The upper bound.
        lower (int or float): The lower bound.
        obj (int or float): The object to check.

        bool: True if the object is out of bounds, False otherwise.
    """
    return det_bool_T(obj > 100 or obj < 0)
def convert_to_percentage(number):
    """
    Converts a number to its percentage if greater than one; otherwise, returns the original number.
    
    Args:
        number (float): The number to be converted.
        
    Returns:
        float: The percentage value of the number if greater than one, otherwise the original number.
    """
    if number > 1:
        return number / 100
    else:
        return number

def find_common_denominator(indent_lists):
    """
    Finds the greatest common divisor (GCD) of all non-zero indentation levels in a list of lists.
    
    Args:
        indent_lists (list of lists): A list of lists, where each sublist contains indentation levels.
        
    Returns:
        int: The GCD of the non-zero indentation levels, or 1 if no non-zero indentations exist.
    """
    # Flatten the list of lists and remove zeros
    all_indents = [indent for sublist in indent_lists for indent in sublist if indent != 0]

    # Find GCD of all indentation levels
    if all_indents:
        return reduce(math.gcd, all_indents)
    else:
        return 1  # Return 1 if there are no indentations other than 0


def exponential(value, exp=9, num=-1):
    """
    Calculates the result of value multiplied by 10 raised to the power of (exp * num).
    
    Args:
        value (float): The base value.
        exp (int, optional): The exponent base (default is 9).
        num (int, optional): The multiplier for the exponent (default is -1).
        
    Returns:
        float: The result of the calculation.
    """
    return multiply_it(value, exp_it(10, exp, num))


def return_0(*args):
    """
    Checks if any of the provided arguments are None, not a number, or represent zero.
    
    Args:
        *args: Variable number of arguments to be checked.
        
    Returns:
        float: Returns 0.0 if any argument is None, not a number, or represents zero.
    """
    for arg in args:
        if arg is None or not is_number(arg) or arg in [0, '0', '', 'null', ' ']:
            return float(0)


def exp_it(number, integer, mul):
    """
    Raises a number to the power of (integer * mul), provided none of the inputs are zero.
    
    Args:
        number (float): The base number to be exponentiated.
        integer (float): The exponent.
        mul (int): The multiplier for the exponent.
        
    Returns:
        float: The result of number raised to the power of (integer * mul), or 0.0 if any argument is zero.
    """
    if return_0(number, integer, mul) == float(0):
        return float(0)
    return float(number) ** float(float(integer) * int(mul))


def divide_it(number_1, number_2):
    """
    Divides number_1 by number_2 if neither is zero or invalid.
    
    Args:
        number_1 (float): The numerator.
        number_2 (float): The denominator.
        
    Returns:
        float: The result of the division, or 0.0 if any argument is zero or invalid.
    """
    if return_0(number_1, number_2) == float(0):
        return float(0)
    return float(number_1) / float(number_2)


def multiply_it(number_1, number_2):
    """
    Multiplies two numbers if neither is zero or invalid.
    
    Args:
        number_1 (float): The first number.
        number_2 (float): The second number.
        
    Returns:
        float: The result of the multiplication, or 0.0 if any argument is zero or invalid.
    """
    if return_0(number_1, number_2) == float(0):
        return float(0)
    return float(number_1) * float(number_2)


def add_it(number_1, number_2):
    """
    Adds two numbers if neither is zero or invalid.
    
    Args:
        number_1 (float): The first number.
        number_2 (float): The second number.
        
    Returns:
        float: The result of the addition, or 0.0 if any argument is zero or invalid.
    """
    if return_0(number_1, number_2) == float(0):
        return float(0)
    return float(number_1) + float(number_2)


def get_percentage(owner_balance, address_balance):
    """
    Calculates the percentage of owner_balance relative to address_balance.
    
    Args:
        owner_balance (float): The balance owned by the owner.
        address_balance (float): The total balance of the address.
        
    Returns:
        float: The percentage of owner_balance relative to address_balance, rounded to two decimal places.
    """
    retained_div = divide_it(owner_balance, address_balance)
    retained_mul = multiply_it(retained_div, 100)
    return round(retained_mul, 2)
