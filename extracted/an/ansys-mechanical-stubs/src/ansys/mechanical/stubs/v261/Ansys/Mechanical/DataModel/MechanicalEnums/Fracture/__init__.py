"""Fracture module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CrackSurfaceType(Enum):
    """
    This enum defines the crack surface types available for a Pre-Meshed Crack.
    """

    NonPlanar = 2
    Planar = 1
    Unspecified = 0

