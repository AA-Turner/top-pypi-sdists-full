"""
Base module of castepinput
"""
from .inputs import ParamInput, CellInput
from .common import Block

__version__ = "0.1.11"
__all__ = ["Block", "ParamInput", "CellInput"]
