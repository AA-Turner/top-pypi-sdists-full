"""Top-level package for opytional."""

__author__ = """Matthew Andres Moreno"""
__email__ = 'm.more500@gmail.com'
__version__ = '0.1.0'

from .apply_if_or_else import apply_if_or_else
from .apply_if_or_value import apply_if_or_value
from .apply_if import apply_if
from .or_else import or_else
from .or_value import or_value

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    'apply_if_or_else',
    'apply_if_or_value',
    'apply_if',
    'or_else',
    'or_value',
]
