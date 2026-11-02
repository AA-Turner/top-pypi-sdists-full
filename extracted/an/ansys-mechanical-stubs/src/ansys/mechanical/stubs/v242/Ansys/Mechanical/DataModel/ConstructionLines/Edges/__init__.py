"""Edges module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class StraightLineEdge(object):
    """
    
                Representation of a straight line edge between to edge vertices.
            
    """

    @property
    def Length(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Length property.
        """
        return None

    @property
    def EndPoint(self) -> typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.Point]:
        """
        
                A Point representing the end vertex of the edge.
            
        """
        return None

    @EndPoint.setter
    def EndPoint(self, value: typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.Point]) -> None:
        """
        
                A Point representing the end vertex of the edge.
            
        """
        pass

    @property
    def StartPoint(self) -> typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.Point]:
        """
        
                A Point representing the start vertex of an edge.
            
        """
        return None

    @StartPoint.setter
    def StartPoint(self, value: typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.Point]) -> None:
        """
        
                A Point representing the start vertex of an edge.
            
        """
        pass

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        
                Get the ID of the represented entity.
            
        """
        return None

    @property
    def IsRepresentation(self) -> typing.Optional[bool]:
        """
        
                Check to see if there is a valid entity that this instance represents.
            
        """
        return None

    @property
    def ConstructionLineId(self) -> typing.Optional[int]:
        """
        
                The ID of the associated ConstructionLine.
            
        """
        return None

    @typing.overload
    def Equals(self, other: Ansys.Mechanical.DataModel.ConstructionLines.Edges.StraightLineEdge) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
        ...

    @typing.overload
    def Equals(self, other: Ansys.Mechanical.DataModel.ConstructionLines.ConstructionLineAssociation) -> bool:
        ...

    def Equals(self, *args: typing.Any) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    @classmethod
    def __eq__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Edges.StraightLineEdge, right: Ansys.Mechanical.DataModel.ConstructionLines.Edges.StraightLineEdge) -> bool:
        """
        op_Equality method.
        """
        pass

    @classmethod
    def __ne__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Edges.StraightLineEdge, right: Ansys.Mechanical.DataModel.ConstructionLines.Edges.StraightLineEdge) -> bool:
        """
        op_Inequality method.
        """
        pass


class IEdge(object):
    """
    
                Interface for edges created by ConstructionLine.
            
    """

    @property
    def Length(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
                Get the length of this edge.
            
        """
        return None


