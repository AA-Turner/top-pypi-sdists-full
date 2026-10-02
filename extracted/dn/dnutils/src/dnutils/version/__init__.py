"""
_version
Version information for dnutils.
"""
import sys


__all__ = [
    'VERSION_MAJOR',
    'VERSION_MINOR',
    'VERSION_PATCH',
    'VERSION_STRING_FULL',
    'VERSION_STRING_SHORT',
    '__version__',
]


VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH = (0, 3, 14)

VERSION_STRING_FULL = '%s.%s.%s' % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
VERSION_STRING_SHORT = '%s.%s' % (VERSION_MAJOR, VERSION_MINOR)

__version__ = VERSION_STRING_FULL

if sys.version_info[0] == 3:
    __basedir__ = 'src'
else:
    raise Exception('Unsupported Python version: %s' % sys.version_info[0])
