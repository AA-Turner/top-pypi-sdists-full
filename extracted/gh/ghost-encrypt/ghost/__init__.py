# __init__.py
# encoding: utf-8

"""
Ghost

Tool for encryption and decryption.
Contains various functions and possibilities
for creating an encrypted network stream and for
en-/decrypting files.

© Copyright 2021 Marius Kraus
"""

from .config import Config
from .key import Key
from .encryption import *
from .stream import *

__version__ = "1.0.6"
