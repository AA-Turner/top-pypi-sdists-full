"""ConstructionLines module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.Mechanical.DataModel.ConstructionLines.Edges as Edges


class PlaneType(Enum):
    """
    
                Enumeration for the possible edge vertex types that can be represented.
            
    """

    CoordinateSystem = 0
    GeometryFace = 1
    OrthogonalPlane = 2

class PointType(Enum):
    """
    
                Enumeration for the possible edge vertex types that can be represented.
            
    """

    Global = 0
    GeometryVertex = 1
    Planar = 2

class ConstructionLineHelper(object):
    """
    
                Helper to perform queries and modifications against a ConstructionLine instance.
            
    """

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def GetEdgeVerticesById(cls, constructionLine: Ansys.ACT.Automation.Mechanical.ConstructionLines.ConstructionLine, edgeVertexIdCollection: typing.Iterable[int]) -> typing.List[typing.Any]:
        """
        GetEdgeVerticesById method.
        """
        pass

    @classmethod
    def GetEdgesById(cls, constructionLine: Ansys.ACT.Automation.Mechanical.ConstructionLines.ConstructionLine, edgeIdCollection: typing.Iterable[int]) -> typing.List[typing.Any]:
        """
        GetEdgesById method.
        """
        pass

    @classmethod
    def GetPlanesById(cls, constructionLine: Ansys.ACT.Automation.Mechanical.ConstructionLines.ConstructionLine, planeIdCollection: typing.Iterable[int]) -> typing.List[typing.Any]:
        """
        GetPlanesById method.
        """
        pass

    @classmethod
    def GetEdgesUsingPoint(cls, point: Ansys.Mechanical.DataModel.ConstructionLines.Point) -> typing.List[typing.Any]:
        """
        
                Get a list of IEdge that use the given Point.
            
        """
        pass

    @classmethod
    def GetContainedEdges(cls, plane: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> typing.List[typing.Any]:
        """
        
                Get all the edges that have both start and end edge vertices in the given plane.
            
        """
        pass

    @classmethod
    def GetRelatedEdges(cls, plane: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> typing.List[typing.Any]:
        """
        
                Get all the edges that have only edge vertex in the given plane.
            
        """
        pass

    @classmethod
    def ExportToXML(cls, constructionLine: Ansys.ACT.Automation.Mechanical.ConstructionLines.ConstructionLine, xmlFilePath: str) -> None:
        """
        
                 Collect all the edges and edge vertices, then export them as global points to an XML file.
             
        """
        pass

    @classmethod
    def ClearExistingDataAndImportFromXML(cls, constructionLine: Ansys.ACT.Automation.Mechanical.ConstructionLines.ConstructionLine, xmlFilePath: str) -> typing.List[typing.Any]:
        """
        
                 Import global points and connecting edges from an XML file.
             
        """
        pass


class Plane(object):
    """
    
                A 2D sketching planes in a ConstructionLine instance.
            
    """

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.PlaneType]:
        """
        Type property.
        """
        return None

    @property
    def Definition(self) -> typing.Optional[typing.Any]:
        """
        Definition property.
        """
        return None

    @Definition.setter
    def Definition(self, value: typing.Optional[typing.Any]) -> None:
        """
        Definition property.
        """
        pass

    @property
    def Origin(self) -> typing.Optional[Ansys.ACT.Core.Math.Point3D]:
        """
        
                The global location of this plane's origin.
            
        """
        return None

    @property
    def PrimaryAxisDirection(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
                The orientation of the plane's primary (X) axis orientation.
            
        """
        return None

    @property
    def SecondaryAxisDirection(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
                The orientation of the plane's secondary (Y) axis orientation.
            
        """
        return None

    @property
    def Normal(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
                The plane's normal vector (Z axis orientation) orientation.
            
        """
        return None

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

    def Equivalent(self, other: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> bool:
        """
        
                Checks to see if another plane is equivalent to this one.
            
        """
        pass

    @typing.overload
    def Equals(self, other: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> bool:
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
    def __eq__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Plane, right: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> bool:
        """
        op_Equality method.
        """
        pass

    @classmethod
    def __ne__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Plane, right: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> bool:
        """
        op_Inequality method.
        """
        pass


class Point(object):
    """
    
                A point in a ConstructionLine instance, may have an associated edge vertex.
            
    """

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.ConstructionLines.PointType]:
        """
        Type property.
        """
        return None

    @property
    def Definition(self) -> typing.Optional[typing.Any]:
        """
        Definition property.
        """
        return None

    @Definition.setter
    def Definition(self, value: typing.Optional[typing.Any]) -> None:
        """
        Definition property.
        """
        pass

    @property
    def Location(self) -> typing.Optional[Ansys.ACT.Core.Math.Point3D]:
        """
        
                Get the global location of this point.
            
        """
        return None

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

    def Equivalent(self, other: Ansys.Mechanical.DataModel.ConstructionLines.Point) -> bool:
        """
        
                Checks to see if another point is equivalent to this one.
            
        """
        pass

    @typing.overload
    def Equals(self, other: Ansys.Mechanical.DataModel.ConstructionLines.Point) -> bool:
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
    def __eq__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Point, right: Ansys.Mechanical.DataModel.ConstructionLines.Point) -> bool:
        """
        op_Equality method.
        """
        pass

    @classmethod
    def __ne__(cls, left: Ansys.Mechanical.DataModel.ConstructionLines.Point, right: Ansys.Mechanical.DataModel.ConstructionLines.Point) -> bool:
        """
        op_Inequality method.
        """
        pass


class Point2DPlanar(object):
    """
    
                Basic data that describe a 2D point on a plane.
            
    """

    @typing.overload
    def __init__(self, location: Ansys.ACT.Core.Math.Point2D, plane: Ansys.Mechanical.DataModel.ConstructionLines.Plane) -> None:
        ...

    @typing.overload
    def __init__(self, point2DPlanar: Ansys.Mechanical.DataModel.ConstructionLines.Point2DPlanar) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        
                Construct an instance using the provided plane and location.
            
        """
        pass

    @classmethod
    def GetGlobalLocation(cls, pointPlane: Ansys.Mechanical.DataModel.ConstructionLines.Point2DPlanar) -> Ansys.ACT.Core.Math.Point3D:
        """
        
                Get the global location of a Point2DPlanar.
            
        """
        pass

    def Equals(self, obj: typing.Any) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


