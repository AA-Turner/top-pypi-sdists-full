# -*- coding: utf-8 -*-

"""
Bring in sentinel ``NOTHING`` into your Python function arguments.
"""


from ._version import __version__

__short_description__ = "Bring in sentinel ``NOTHING`` into your Python function arguments."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .args import NOTHING, resolve_kwargs
except ImportError: # pragma: no cover
    pass
