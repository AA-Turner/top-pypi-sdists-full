"""Dataset2D module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class LineType(Enum):
    """
    
            An enum that allows user to control the display of dataset with respect to showing lines and markers on the chart. 
            
    """

    MarkersOnly = 0
    LinesOnly = 1
    LinesAndMarkers = 2

class MarkerShape(Enum):
    """
    
            An enum that allows user to control the shape of dataset markers on the chart. 
            
    """

    Circle = 0
    Square = 1
    Triangle = 2
    EmptySquare = 3
    VerticalLine = 5
    PointStyleRhomb = 6
    PointStyleX = 7

