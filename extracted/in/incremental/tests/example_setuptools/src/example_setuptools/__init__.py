"""
An example project that uses setuptools in pyproject.toml

@added: example_setuptools NEXT
"""

from incremental import Version

from ._version import __version__

__all__ = ["__version__"]

if Version("example_setuptools", "NEXT", 0, 0) > __version__:
    print("Unreleased!")
