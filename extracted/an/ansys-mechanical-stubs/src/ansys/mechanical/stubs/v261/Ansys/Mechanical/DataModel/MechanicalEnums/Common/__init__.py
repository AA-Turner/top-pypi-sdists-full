"""Common module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class PlaneOrientation(Enum):
    """
    Specifies the PlaneOrientation
    """

    PlaneOrientation_XZ = 1
    PlaneOrientation_XY = 2
    PlaneOrientation_YZ = 3
    Undefined = 0

class CartesianDirection(Enum):
    """
    Used to specify cardinal directions with respect to a Cartesian-based system.
    """

    Unspecified = 0
    X = 1
    Y = 2
    Z = 3

class PathType(Enum):
    """
    This enum specifies how a path should be interpreted.
    """

    Absolute = 1
    RelativeToProject = 2
    Undefined = 0

