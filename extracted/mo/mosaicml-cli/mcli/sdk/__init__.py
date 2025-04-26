"""
When the mcli sdk was first created, this was the main entry point for the SDK

We will soon be deprecating this, and pushing users to import directly from mcli
"""

import warnings

from mcli import *

warnings.warn("mcli.sdk will soon be deprecated, please import directly from mcli instead", DeprecationWarning)
