"""Determine Unicode text segmentations."""

from importlib.metadata import PackageNotFoundError, version

__all__ = [
    '__version__',
    'unidata_version',
]


try:
    __version__ = version(__name__)
    """Version string of the module."""
except PackageNotFoundError:
    # package is not installed
    pass

unidata_version = '16.0.0'
"""Version of the Unicode used in the package."""
