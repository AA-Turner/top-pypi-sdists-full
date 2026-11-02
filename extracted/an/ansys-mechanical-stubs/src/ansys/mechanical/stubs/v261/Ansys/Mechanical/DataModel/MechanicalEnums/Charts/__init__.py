"""Charts module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D as Dataset2D


class LegendPosition(Enum):
    """
    
            An enum that allows users to control the position of legend being shown on the chart.
            
    """

    Unspecified = 0
    ProgramControlled = 1
    Top = 2
    Right = 3

