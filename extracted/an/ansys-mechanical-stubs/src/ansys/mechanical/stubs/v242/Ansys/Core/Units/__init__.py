"""Units module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Quantity(object):
    """
    Quantity class.
    """

    @property
    def Value(self) -> typing.Optional[float]:
        """
        Value property.
        """
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        Unit property.
        """
        return None

    @property
    def HasUnit(self) -> typing.Optional[bool]:
        """
        HasUnit property.
        """
        return None

    @typing.overload
    def __init__(self, value: float, unit: str) -> None:
        ...

    @typing.overload
    def __init__(self, value: str) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Abs(self) -> Ansys.Core.Units.Quantity:
        """
        Abs method.
        """
        pass

    @typing.overload
    def CompareTo(self, quantityB: Ansys.Core.Units.Quantity) -> int:
        ...

    @typing.overload
    def CompareTo(self, obj: typing.Any) -> int:
        ...

    def CompareTo(self, *args: typing.Any) -> int:
        """
        CompareTo method.
        """
        pass

    def ConvertToUnitSystem(self, unitSystem: str, quantityName: str) -> Ansys.Core.Units.Quantity:
        """
        ConvertToUnitSystem method.
        """
        pass

    @typing.overload
    def ConvertUnit(self, newUnit: str) -> Ansys.Core.Units.Quantity:
        ...

    @typing.overload
    def ConvertUnit(self, newUnit: str, quantityName: str) -> Ansys.Core.Units.Quantity:
        ...

    def ConvertUnit(self, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        ConvertUnit method.
        """
        pass

    def ConvertToUserUnit(self, quantityName: str) -> Ansys.Core.Units.Quantity:
        """
        ConvertToUserUnit method.
        """
        pass

    @typing.overload
    def ConvertToComputationalUnit(self, useBasicUnits: bool) -> Ansys.Core.Units.Quantity:
        ...

    @typing.overload
    def ConvertToComputationalUnit(self, quantityName: str, useBasicUnits: bool) -> Ansys.Core.Units.Quantity:
        ...

    def ConvertToComputationalUnit(self, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        ConvertToComputationalUnit method.
        """
        pass

    def ConvertToComputationalUnitForUnitSystem(self, quantityName: str, unitSystem: str, useBasicUnits: bool) -> Ansys.Core.Units.Quantity:
        """
        ConvertToComputationalUnitForUnitSystem method.
        """
        pass

    @typing.overload
    def Equals(self, value: Ansys.Core.Units.Quantity) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: typing.Any) -> bool:
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

    def GetConvertedValue(self, unit: str) -> float:
        """
        GetConvertedValue method.
        """
        pass

    @classmethod
    def Parse(cls, valueUnitString: str) -> Ansys.Core.Units.Quantity:
        """
        Parse method.
        """
        pass

    def Pow(self, exponent: float) -> Ansys.Core.Units.Quantity:
        """
        Pow method.
        """
        pass

    def Sqrt(self) -> Ansys.Core.Units.Quantity:
        """
        Sqrt method.
        """
        pass

    @typing.overload
    def ToString(self) -> str:
        ...

    @typing.overload
    def ToString(self, formatString: str) -> str:
        ...

    @typing.overload
    def ToString(self, provider: typing.Any) -> str:
        ...

    @typing.overload
    def ToString(self, format: str, provider: typing.Any) -> str:
        ...

    def ToString(self, *args: typing.Any) -> str:
        """
        ToString method.
        """
        pass

    @classmethod
    def TryParse(cls, valueStringQuantity: str, result: Ansys.Core.Units.Quantity) -> bool:
        """
        TryParse method.
        """
        pass

    def Round(self, fractionalDigits: int, rounding: typing.Optional[float]) -> Ansys.Core.Units.Quantity:
        """
        Round method.
        """
        pass

    @classmethod
    def __pos__(cls, quantityA: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        """
        op_UnaryPlus method.
        """
        pass

    @classmethod
    def __neg__(cls, quantityA: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        """
        op_UnaryNegation method.
        """
        pass

    @classmethod
    @typing.overload
    def __add__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __add__(cls, left: Ansys.Core.Units.Quantity, right: float) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __add__(cls, left: float, right: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    def __add__(cls, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        op_Addition method.
        """
        pass

    @classmethod
    @typing.overload
    def __sub__(cls, left: float, right: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __sub__(cls, left: Ansys.Core.Units.Quantity, right: float) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __sub__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    def __sub__(cls, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        op_Subtraction method.
        """
        pass

    @classmethod
    @typing.overload
    def __mul__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __mul__(cls, quantity: Ansys.Core.Units.Quantity, factor: float) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __mul__(cls, factor: float, quantity: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    def __mul__(cls, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        op_Multiply method.
        """
        pass

    @classmethod
    @typing.overload
    def __gt__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __gt__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __gt__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __gt__(cls, *args: typing.Any) -> bool:
        """
        op_GreaterThan method.
        """
        pass

    @classmethod
    @typing.overload
    def __lt__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __lt__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __lt__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __lt__(cls, *args: typing.Any) -> bool:
        """
        op_LessThan method.
        """
        pass

    @classmethod
    @typing.overload
    def __ge__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __ge__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __ge__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __ge__(cls, *args: typing.Any) -> bool:
        """
        op_GreaterThanOrEqual method.
        """
        pass

    @classmethod
    @typing.overload
    def __le__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __le__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __le__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __le__(cls, *args: typing.Any) -> bool:
        """
        op_LessThanOrEqual method.
        """
        pass

    @classmethod
    @typing.overload
    def __eq__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __eq__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __eq__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __eq__(cls, *args: typing.Any) -> bool:
        """
        op_Equality method.
        """
        pass

    @classmethod
    @typing.overload
    def __ne__(cls, other: float, quantity: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    @typing.overload
    def __ne__(cls, quantity: Ansys.Core.Units.Quantity, other: float) -> bool:
        ...

    @classmethod
    @typing.overload
    def __ne__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> bool:
        ...

    @classmethod
    def __ne__(cls, *args: typing.Any) -> bool:
        """
        op_Inequality method.
        """
        pass

    @classmethod
    @typing.overload
    def __mod__(cls, quantityLeft: Ansys.Core.Units.Quantity, quantityRight: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __mod__(cls, quantityLeft: Ansys.Core.Units.Quantity, numberRight: float) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __mod__(cls, doubleLeft: float, quantityRight: Ansys.Core.Units.Quantity) -> float:
        ...

    @classmethod
    def __mod__(cls, *args: typing.Any) -> Ansys.Core.Units.Quantity | float:
        """
        op_Modulus method.
        """
        pass

    @classmethod
    @typing.overload
    def __truediv__(cls, quantityA: Ansys.Core.Units.Quantity, quantityB: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __truediv__(cls, quantity: Ansys.Core.Units.Quantity, factor: float) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __truediv__(cls, factor: float, quantity: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    @typing.overload
    def __truediv__(cls, a: Ansys.Core.Units.Quantity, b: typing.Any) -> Ansys.Core.Units.Quantity:
        ...

    @classmethod
    def __truediv__(cls, *args: typing.Any) -> Ansys.Core.Units.Quantity:
        """
        op_Division method.
        """
        pass

    @classmethod
    def __rtruediv__(cls, a: typing.Any, b: Ansys.Core.Units.Quantity) -> Ansys.Core.Units.Quantity:
        """
        __rtruediv__ method.
        """
        pass

    def __pow__(self, exponent: typing.Any) -> typing.Any:
        """
        __pow__ method.
        """
        pass

    def __repr__(self) -> typing.Any:
        """
        __repr__ method.
        """
        pass


