"""Top-level package for interval_search."""

__author__ = """Matthew Andres Moreno"""
__email__ = 'm.more500@gmail.com'
__version__ = '0.5.2'

from .binary_search import binary_search
from .binary_search_iterative import binary_search_iterative
from .binary_search_recursive import binary_search_recursive
from .curried_binary_search import curried_binary_search
from .curried_binary_search_iterative import curried_binary_search_iterative
from .curried_binary_search_recursive import curried_binary_search_recursive
from .curried_doubling_search import curried_doubling_search
from .doubling_search import doubling_search
from .interval_search import interval_search

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    'binary_search',
    'binary_search_iterative',
    'binary_search_recursive',
    'curried_binary_search',
    'curried_binary_search_iterative',
    'curried_binary_search_recursive',
    'curried_doubling_search',
    'doubling_search',
    'interval_search',
]
