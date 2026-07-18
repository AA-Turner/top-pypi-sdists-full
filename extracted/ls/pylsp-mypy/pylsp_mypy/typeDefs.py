# -*- coding: utf-8 -*-
"""
File to house the   class.

Created on Wed Jul 15 22:16:07 2026

@author: Richard Kellnberger
"""

from typing import TypedDict


class WindowsFlag(TypedDict, total=False):
    """
    Windows started opening opening a cmd-like window for every subprocess call.
    This flag prevents that.
    This flag is new in python 3.7
    """

    creationflags: int
