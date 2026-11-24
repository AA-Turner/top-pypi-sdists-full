"""Loop-exhaustion contract for exported v4 while-loops.

The exception class lives in the shared ``testmu_appium._errors`` so every mode
raises the same class; this module keeps the helpers import path.
"""
from testmu_appium._errors import LoopExhausted

__all__ = ["LoopExhausted"]
