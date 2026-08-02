"""
pipebio

A PipeBio client package.
"""

import sys

if sys.version_info >= (3, 14):
    raise RuntimeError("Python 3.14 is not supported. Please use Python 3.13 or lower.")

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # for Python <3.8 fallback

__version__ = version("pipebio")
__author__ = 'PipeBio'
