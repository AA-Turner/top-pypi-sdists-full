"""
Token-Oriented Object Notation (TOON) for Python.

A compact, human-readable format designed for passing structured data
to Large Language Models with significantly reduced token usage.
"""

from toon_format.decoder import decode
from toon_format.encoder import encode
from toon_format.types import DecodeOptions, EncodeOptions

__version__ = "0.1.0"
__all__ = ["encode", "decode", "EncodeOptions", "DecodeOptions"]
