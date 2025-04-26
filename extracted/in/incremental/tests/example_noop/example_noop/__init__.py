"""
An example setuptools project that doesn't use Incremental at all.

This is used to verify that Incremental correctly deactivates itself
when there is no opt-in, even though setuptools always invokes its
hook.
"""

__version__ = "100"

__all__ = ["__version__"]
