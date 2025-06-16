# -*- coding: utf-8 -*-
###########################################################
#  Copyright (C) Joel B. Mohler <joel@kiwistrawberry.us>
#
#  Distributed under the terms of The MIT License
###########################################################
"""
fuzzyparsers library initialization
"""

from .strings import default_match, fuzzy_match
from .dates import *

__version_info__ = ['0', '9', '5']
__version__ = '.'.join(__version_info__)
