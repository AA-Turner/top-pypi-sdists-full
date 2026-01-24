"""Importing this package will upgrade the `backslashreplace` error handling
scheme in the global `codecs` registry to support handling decoding errors as
well as encoding errors.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from . import backcompat

backcompat.upgrade_backslashreplace()
