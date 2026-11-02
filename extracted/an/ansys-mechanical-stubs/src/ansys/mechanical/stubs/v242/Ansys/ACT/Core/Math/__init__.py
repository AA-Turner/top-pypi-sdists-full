"""Math module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Point2D(object):

    @property
    def X(self) -> typing.Optional[float]:
        """
        X property.
        """
        return None

    @X.setter
    def X(self, value: typing.Optional[float]) -> None:
        """
        X property.
        """
        pass

    @property
    def Y(self) -> typing.Optional[float]:
        """
        Y property.
        """
        return None

    @Y.setter
    def Y(self, value: typing.Optional[float]) -> None:
        """
        Y property.
        """
        pass

    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        ...

    @typing.overload
    def __init__(self, point: Ansys.ACT.Core.Math.Point2D) -> None:
        ...

    @typing.overload
    def __init__(self, xyz: float) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
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


class Vector3D(object):

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

    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None:
        ...

    @typing.overload
    def __init__(self, vector: Ansys.ACT.Core.Math.Vector3D) -> None:
        ...

    @typing.overload
    def __init__(self, xyz: float) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def SphericalToCartesian(self) -> Ansys.ACT.Core.Math.Vector3D:
        """
        SphericalToCartesian method.
        """
        pass

    def CylindricalToCartesian(self) -> Ansys.ACT.Core.Math.Vector3D:
        """
        CylindricalToCartesian method.
        """
        pass

    @classmethod
    def __sub__(cls, a: Ansys.ACT.Core.Math.Vector3D, b: Ansys.ACT.Core.Math.Vector3D) -> Ansys.ACT.Core.Math.Vector3D:
        """
        op_Subtraction method.
        """
        pass

    @classmethod
    def __add__(cls, a: Ansys.ACT.Core.Math.Vector3D, b: Ansys.ACT.Core.Math.Vector3D) -> Ansys.ACT.Core.Math.Vector3D:
        """
        op_Addition method.
        """
        pass

    def ToArray(self) -> float:
        """
        ToArray method.
        """
        pass

    def Normalize(self) -> None:
        """
        Normalize method.
        """
        pass

    def Substract(self, other: Ansys.ACT.Core.Math.Vector3D) -> None:
        """
        Substract method.
        """
        pass

    def Length(self) -> float:
        """
        Length method.
        """
        pass

    def SquareLength(self) -> float:
        """
        SquareLength method.
        """
        pass

    def CrossProduct(self, other: Ansys.ACT.Interfaces.Graphics.IVector3D) -> Ansys.ACT.Core.Math.Vector3D:
        """
        CrossProduct method.
        """
        pass

    def GetNormal(self) -> Ansys.ACT.Interfaces.Graphics.IVector3D:
        """
        GetNormal method.
        """
        pass

    @typing.overload
    def IsColinearTo(self, other: Ansys.ACT.Interfaces.Graphics.IVector3D) -> bool:
        ...

    @typing.overload
    def IsColinearTo(self, other: Ansys.ACT.Interfaces.Graphics.IVector3D, precision: float) -> bool:
        ...

    def IsColinearTo(self, *args: typing.Any) -> bool:
        """
        IsColinearTo method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass

    @typing.overload
    def Equals(self, other: Ansys.ACT.Core.Math.Vector3D) -> bool:
        ...

    @typing.overload
    def Equals(self, other: typing.Any) -> bool:
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
    def __eq__(cls, v1: Ansys.ACT.Core.Math.Vector3D, v2: Ansys.ACT.Core.Math.Vector3D) -> bool:
        """
        op_Equality method.
        """
        pass

    @classmethod
    def __ne__(cls, v1: Ansys.ACT.Core.Math.Vector3D, v2: Ansys.ACT.Core.Math.Vector3D) -> bool:
        """
        op_Inequality method.
        """
        pass


class Point3D(object):

    @property
    def X(self) -> typing.Optional[float]:
        """
        X property.
        """
        return None

    @X.setter
    def X(self, value: typing.Optional[float]) -> None:
        """
        X property.
        """
        pass

    @property
    def Y(self) -> typing.Optional[float]:
        """
        Y property.
        """
        return None

    @Y.setter
    def Y(self, value: typing.Optional[float]) -> None:
        """
        Y property.
        """
        pass

    @property
    def Z(self) -> typing.Optional[float]:
        """
        Z property.
        """
        return None

    @Z.setter
    def Z(self, value: typing.Optional[float]) -> None:
        """
        Z property.
        """
        pass

    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None:
        ...

    @typing.overload
    def __init__(self, point: Ansys.ACT.Core.Math.Point3D) -> None:
        ...

    @typing.overload
    def __init__(self, xyz: float) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
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


