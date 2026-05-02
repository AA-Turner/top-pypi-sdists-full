"""
spotilyzer cli utilities
"""

# system imports
import argparse


def options(name, shortname=None):
    """
    Return options for argparse.
    :param name: long name
    :param shortname: short name to override first character of long name
    :return: tuple with short and long options
    """
    return f'-{shortname is None and name[0] or shortname}', \
           f'--{name}'


def posint(string):
    """
    Positive definite integer for argparse type.
    :param string: string value
    :return: integer value
    """
    try:
        value = int(string)
    except ValueError as err:
        raise argparse.ArgumentTypeError(err)
    if value < 1:
        raise argparse.ArgumentTypeError(f"invalid value {string}: value must "
                                         "be greater than 0")
    return value


def posfloat(string):
    """
    Positive semi-definite float type for argparse type.
    :param string: string value
    :return: float value
    """
    try:
        value = float(string)
    except ValueError as err:
        raise argparse.ArgumentTypeError(err)
    if value < 0.0:
        raise argparse.ArgumentTypeError(f"invalid value {string}: value must "
                                         "be greater than or equal to 0.0")
    return value


def csv(string):
    """
    Split CSV to a list.
    :param string: comma-separated list
    :return: list of values
    """
    return string.split(',')
