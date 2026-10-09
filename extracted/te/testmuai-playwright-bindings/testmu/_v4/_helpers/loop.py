"""Loop-exhaustion contract for exported v4 while-loops.

The exception class lives in the shared ``testmu._errors`` so both the v3 and
v4 implementations raise the same class; this module keeps the old import path.
"""
from testmu._errors import LoopExhausted

__all__ = ["LoopExhausted"]
