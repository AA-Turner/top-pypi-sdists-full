"""Math module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Matrix4D(object):
    """
    
             Transformation matrix 
              *single linear*      *standard zero-based row-column index*
             |  0  4  8  12  |   |  Rot00*Sx  Rot01     Rot02     TransX  |
             |  1  5  9  13  |   |  Rot10     Rot11*Sy  Rot12     TransY  |
             |  2  6  10 14  | = |  Rot20     Rot21     Rot22*Sz  TransZ  |
             |  3  7  11 15  |   |  0 (30)    0 (31)    0 (32)    1 (33)  |
            
             
    """

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[float]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[float]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Determinant(self) -> typing.Optional[float]:
        """
        
            Matrix determinant accessor.
            
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, entries: float) -> None:
        ...

    @typing.overload
    def __init__(self, m44: Ansys.ACT.Math.Matrix4D) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        
            Default constructor - creates identity 4x4 matrix
            
        """
        pass

    @classmethod
    def CreateRotate(cls, rotationAxis: Ansys.ACT.Math.Vector3D, rotationRadians: float) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Create transformation matrix that rotates about a given vector by a given angle
            
        """
        pass

    @classmethod
    def CreateScale(cls, x: float, y: float, z: float) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Create scaling transformation matrix
            
        """
        pass

    @classmethod
    def CreateTranslate(cls, x: float, y: float, z: float) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Create translating transformation matrix
            
        """
        pass

    @classmethod
    def CreateMirror(cls, normal: Ansys.ACT.Math.Vector3D, d: float) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Create transformation matrix mirroring about a plane
            
        """
        pass

    @classmethod
    def CreateSystem(cls, xAxis: Ansys.ACT.Math.Vector3D, yAxis: Ansys.ACT.Math.Vector3D, zAxis: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Create transformation matrix converting to new coordinate system.
            
        """
        pass

    @classmethod
    def op_Explicit(cls, m44: Ansys.ACT.Math.Matrix4D) -> float:
        """
        op_Explicit method.
        """
        pass

    def Add(self, m44: Ansys.ACT.Math.Matrix4D) -> None:
        """
        
            Add matrix to itself.
            
        """
        pass

    def Subtract(self, m44: Ansys.ACT.Math.Matrix4D) -> None:
        """
        
            Subtract matrix from itself.
            
        """
        pass

    def Multiply(self, m44: Ansys.ACT.Math.Matrix4D) -> None:
        """
        
            Multiply this matrix by the given matrix
            
        """
        pass

    def Scale(self, x: float, y: float, z: float) -> None:
        """
        
            Convenient method to combine x, y, z scale into itself.
            
        """
        pass

    def Translate(self, x: float, y: float, z: float) -> None:
        """
        
            Convenient method to combine (x, y, z) translatation into itself.
            
        """
        pass

    def Transpose(self) -> None:
        """
        
            Transpose itself.
            
        """
        pass

    def Invert(self) -> int:
        """
        
            Invert itself if determinant is non-zero. Return 0 if inverted; 1 - otherwise.
            
        """
        pass

    def Transform(self, vector3D: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Apply this transformation matrix to a given point/vector.
            Note: assumes (0,0,0,1) in last row.
            
        """
        pass

    @classmethod
    def __mul__(cls, a: Ansys.ACT.Math.Matrix4D, b: Ansys.ACT.Math.Matrix4D) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Matrix multiplication operator - assumes (0,0,0,1) in last row.
            
        """
        pass

    @classmethod
    def __add__(cls, a: Ansys.ACT.Math.Matrix4D, b: Ansys.ACT.Math.Matrix4D) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Matrix addition operator.
            
        """
        pass

    @classmethod
    def __sub__(cls, a: Ansys.ACT.Math.Matrix4D, b: Ansys.ACT.Math.Matrix4D) -> Ansys.ACT.Math.Matrix4D:
        """
        
            Matrix subtraction operator.
            
        """
        pass

    def ToString(self) -> str:
        """
        
            String representation.
            
        """
        pass


class Vector3D(object):
    """
    
            Vector in 3D-space
            
    """

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[float]) -> None:
        """
        Item property.
        """
        pass

    @property
    def MagnitudeSquared(self) -> typing.Optional[float]:
        """
        
            Vector magnitude squared accessor
            
        """
        return None

    @property
    def Magnitude(self) -> typing.Optional[float]:
        """
        
            Vector magnitude accessor
            
        """
        return None

    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None:
        ...

    @typing.overload
    def __init__(self, coordinates: float) -> None:
        ...

    @typing.overload
    def __init__(self, vec3: Ansys.ACT.Math.Vector3D) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        
            Create a vector with ( x, y, z ) coordinates
            
        """
        pass

    def Normalize(self) -> None:
        """
        
            Convert to an unit vector
            
        """
        pass

    def CloneNormalized(self) -> Ansys.ACT.Math.Vector3D:
        """
        
            Create a normalized copy of a vector
            
        """
        pass

    @classmethod
    def op_Explicit(cls, vec3: Ansys.ACT.Math.Vector3D) -> float:
        """
        op_Explicit method.
        """
        pass

    @classmethod
    def GetDistanceSquared(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> float:
        """
        
            Squared distance between vectors/points
            
        """
        pass

    @classmethod
    def GetDistance(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> float:
        """
        
            Squared distance between vectors/points
            
        """
        pass

    def Add(self, vec3: Ansys.ACT.Math.Vector3D) -> None:
        """
        
            Add vector to itself.
            
        """
        pass

    def Subtract(self, vec3: Ansys.ACT.Math.Vector3D) -> None:
        """
        
            Subtract vector from itself.
            
        """
        pass

    def DotProduct(self, vec3: Ansys.ACT.Math.Vector3D) -> float:
        """
        
            Dot product.
            
        """
        pass

    @classmethod
    def Dot(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> float:
        """
        
            Dot product.
            
        """
        pass

    def CrossProduct(self, vec3: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Cross product.
            
        """
        pass

    @classmethod
    def Cross(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Cross product - same as multiply operator
            
        """
        pass

    @classmethod
    def __eq__(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> bool:
        """
        
            Equal operator
            
        """
        pass

    @classmethod
    def __ne__(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> bool:
        """
        
            Not-Equal operator
            
        """
        pass

    @classmethod
    def __add__(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Plus operator
            
        """
        pass

    @classmethod
    def __sub__(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Minus operator
            
        """
        pass

    @classmethod
    def __neg__(cls, vec3: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        """
        
            Unary minus operator
            
        """
        pass

    @classmethod
    @typing.overload
    def __mul__(cls, factor: float, vec3: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        ...

    @classmethod
    @typing.overload
    def __mul__(cls, vec3: Ansys.ACT.Math.Vector3D, factor: float) -> Ansys.ACT.Math.Vector3D:
        ...

    @classmethod
    @typing.overload
    def __mul__(cls, a: Ansys.ACT.Math.Vector3D, b: Ansys.ACT.Math.Vector3D) -> Ansys.ACT.Math.Vector3D:
        ...

    @classmethod
    def __mul__(cls, *args: typing.Any) -> Ansys.ACT.Math.Vector3D:
        """
        
            Multiply a factor by a vector operator.
            
        """
        pass

    @classmethod
    def __truediv__(cls, vec3: Ansys.ACT.Math.Vector3D, divFactor: float) -> Ansys.ACT.Math.Vector3D:
        """
        
            Divide a vector by a factor operator.
            
        """
        pass

    def Equals(self, o: typing.Any) -> bool:
        """
        
            Object.Equals(object o) override
            
        """
        pass

    def GetHashCode(self) -> int:
        """
        
            Object.GetHashCode() override
            
        """
        pass

    def ToString(self) -> str:
        """
        
            String representation.
            
        """
        pass


