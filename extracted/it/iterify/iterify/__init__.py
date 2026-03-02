"""Top-level package for iterify."""

__author__ = """Matthew Andres Moreno"""
__email__ = 'm.more500@gmail.com'
__version__ = '0.1.0'

from .cyclify import cyclify
from .iterify import iterify
from .samplify import samplify
from .shufflify import shufflify

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    'cyclify',
    'iterify',
    'samplify',
    'shufflify',
]
