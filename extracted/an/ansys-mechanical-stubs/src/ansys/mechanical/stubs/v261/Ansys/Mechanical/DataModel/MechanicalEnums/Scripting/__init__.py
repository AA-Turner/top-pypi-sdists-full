"""Scripting module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class EngineType(Enum):
    """
    
            Enum used to specifiy what engine type to use for script execution.
            
    """

    Unspecified = 0
    IronPython = 1
    CPython = 2

