"""
Functions for printing

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from argparse import Namespace
from typing import Any, Dict, Set

DEFAULT_WIDTH = 10


def print_set(s: Set[str], header: str = None, width: int = DEFAULT_WIDTH) -> None:
    """Print set s with section header.

    :param s: set to print
    :param header: header of the table
    :param width: width of the left column
    """
    if s:
        if header:
            print('{}:'.format(header))
        for element in sorted(s):
            print('  {:>{}} {}'.format('', width, element))


def print_dict(d: Dict[str, Any], header: str = None, width: int = DEFAULT_WIDTH) -> None:
    """Print dictionary d with section header.

    :param d: dictionary to print
    :param header: header of the table
    :param width: width of the left column
    """
    if d:
        if header:
            print('{}:'.format(header))
        for key in sorted(d):
            left = str(d[key])
            print('  {:>{}} {}'.format(left, width, key))


def print_namespace(ns: Namespace, header: str = None) -> None:
    """Print namespace with header.

    :param ns: namespace to print
    :param header: header of the table
    """
    if ns:
        if header:
            print('{}:'.format(header))
        keys = sorted(vars(ns))
        if keys:
            for var in keys:
                value = getattr(ns, var)
                print('  {} ({}): {!r}'.format(var, type(value).__name__, value))
        else:
            print('  (empty)')
