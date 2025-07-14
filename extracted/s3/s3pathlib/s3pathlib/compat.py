# -*- coding: utf-8 -*-

"""
Provide compatibility with older versions of Python and dependent libraries.
"""

import sys

try:
    import smart_open

    parts = smart_open.__version__.split(".")
    smart_open_version_major = int(parts[0])
    smart_open_version_minor = int(parts[1])
except ImportError:  # pragma: no cover
    smart_open = None
    smart_open_version_major = None
    smart_open_version_minor = None
except:  # pragma: no cover
    raise


class Compat:  # pragma: no cover
    @property
    def smart_open_version_major(self) -> int:
        if smart_open_version_major is None:
            raise ImportError("You don't have smart_open installed")
        return smart_open_version_major

    @property
    def smart_open_version_minor(self) -> int:
        if smart_open_version_minor is None:
            raise ImportError("You don't have smart_open installed")
        return smart_open_version_minor


compat = Compat()
