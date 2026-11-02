"""Math module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class BoundVector(object):
    """
    
            A vector with fixed intial point and terminal point.
            Or a vector with fixed initial point(origin) and a direction(vector).
            
    """

    @property
    def Origin(self) -> typing.Optional[Ansys.Mechanical.Graphics.Point]:
        """
        
            The location at the start of the BoundVector.
            
        """
        return None

    @Origin.setter
    def Origin(self, value: typing.Optional[Ansys.Mechanical.Graphics.Point]) -> None:
        """
        
            The location at the start of the BoundVector.
            
        """
        pass

    @property
    def Vector(self) -> typing.Optional[Ansys.ACT.Math.Vector3D]:
        """
        
            The direction of the BoundVector.
            
        """
        return None

    @Vector.setter
    def Vector(self, value: typing.Optional[Ansys.ACT.Math.Vector3D]) -> None:
        """
        
            The direction of the BoundVector.
            
        """
        pass

    def __init__(self, point: Ansys.Mechanical.Graphics.Point, vector: Ansys.ACT.Math.Vector3D) -> None:
        """
        
            Creates a BoundVector from a point and a vector.
            
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


