"""
An example project that uses setup.py

@added: example_setuppy NEXT
"""

from incremental import Version
from ._version import __version__

__all__ = ["__version__"]

if Version("example_setuppy", "NEXT", 0, 0) > __version__:
    print("Unreleased!")
