"""Top-level package for nanto."""

__author__ = """Matthew Andres Moreno"""
__email__ = 'm.more500@gmail.com'
__version__ = '0.1.1'

from .nanto import isanan
from .nanto import nanto
from .nantonone import nantonone
from .nantozero import nantozero

# adapted from https://stackoverflow.com/a/31079085
__all__ = [
    'isanan',
    'nanto',
    'nantonone',
    'nantozero',
]
