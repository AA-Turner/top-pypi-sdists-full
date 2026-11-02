"""Selection module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class GeometryRayCastHit(object):
    """
    
            GeometryRayCastHit, contains geoEntity and vector normal
            
    """

    @property
    def HitVector(self) -> typing.Optional[Ansys.Mechanical.Math.BoundVector]:
        """
        
            BoundVector with location and normal direction on geometry entity to ray cast
            
        """
        return None

    @HitVector.setter
    def HitVector(self, value: typing.Optional[Ansys.Mechanical.Math.BoundVector]) -> None:
        """
        
            BoundVector with location and normal direction on geometry entity to ray cast
            
        """
        pass

    @property
    def Entity(self) -> typing.Optional[Ansys.ACT.Interfaces.Geometry.IGeoEntity]:
        """
        
            Geometry entity hit by ray cast
            
        """
        return None

    @Entity.setter
    def Entity(self, value: typing.Optional[Ansys.ACT.Interfaces.Geometry.IGeoEntity]) -> None:
        """
        
            Geometry entity hit by ray cast
            
        """
        pass


class GeometryRayCastSettings(object):

    @property
    def HitFaces(self) -> typing.Optional[bool]:
        """
        
            Specifies whether ray casting should hit faces. 
            Defaults to true.
            
        """
        return None

    @HitFaces.setter
    def HitFaces(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether ray casting should hit faces. 
            Defaults to true.
            
        """
        pass

    @property
    def HitEdges(self) -> typing.Optional[bool]:
        """
        
            Specifies whether ray casting should hit edges. 
            Defaults to false.
            
        """
        return None

    @HitEdges.setter
    def HitEdges(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether ray casting should hit edges. 
            Defaults to false.
            
        """
        pass

    @property
    def HitVertices(self) -> typing.Optional[bool]:
        """
        
            Specifies whether ray casting should hit vertices. 
            Defaults to false.
            
        """
        return None

    @HitVertices.setter
    def HitVertices(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether ray casting should hit vertices. 
            Defaults to false.
            
        """
        pass

    @property
    def HitBodies(self) -> typing.Optional[bool]:
        """
        
            Specifies whether ray casting should hit bodies. 
            Defaults to false.
            
        """
        return None

    @HitBodies.setter
    def HitBodies(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether ray casting should hit bodies. 
            Defaults to false.
            
        """
        pass

    @property
    def MaxHits(self) -> typing.Optional[int]:
        """
        
            Specifies maximum number of ray casting hits. 
            Defaults to 1000.
            
        """
        return None

    @MaxHits.setter
    def MaxHits(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies maximum number of ray casting hits. 
            Defaults to 1000.
            
        """
        pass

    @property
    def CastRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Optional; specifies maximum radial distance from BoundVector.
            
        """
        return None

    @CastRadius.setter
    def CastRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Optional; specifies maximum radial distance from BoundVector.
            
        """
        pass

    @property
    def CastLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Optional; specifies maximum axial distance from BoundVector origin.
            Defaults to maximum needed length.
            
        """
        return None

    @CastLength.setter
    def CastLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Optional; specifies maximum axial distance from BoundVector origin.
            Defaults to maximum needed length.
            
        """
        pass

    def __init__(self) -> None:
        """
        
            Creates a new GeometryRayCastSettings instance.
            
        """
        pass


class SelectionHelper(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def CreateVector3D(cls, selection: Ansys.ACT.Interfaces.Common.ISelectionInfo, reversed: bool) -> Ansys.ACT.Math.Vector3D:
        """
        Creates a Vector3D object based on the given selection and reverse flag.  
            The direction is computed as the outward normal of a planar face, the direction between 
            two nodes or vertices from the first to the second, or the axis of an edge.  
            The reversed flag will return the opposite of the computed direction.
            
        """
        pass

    @classmethod
    def CastRayOnGeometry(cls, castVector: Ansys.Mechanical.Math.BoundVector, settings: Ansys.Mechanical.Selection.GeometryRayCastSettings) -> typing.Iterable[Ansys.Mechanical.Selection.GeometryRayCastHit]:
        """
        
            Finds geometry entities intersecting input BoundVector and returns them in list of GeometryRayCastHit.
            These are returned in the order they are hit, each item containing the entity and BoundVector normal to point hit.
            
        """
        pass


