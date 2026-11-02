"""Results module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ResultDataTable(object):
    """
    Specifies the Result Table.
    """

    @property
    def Item(self) -> typing.Optional[typing.Iterable]:
        """
        Item property.
        """
        return None

    @property
    def Independents(self) -> typing.Optional[dict[str,typing.Iterable]]:
        """
        Independents property.
        """
        return None

    @property
    def Dependents(self) -> typing.Optional[dict[str,typing.Iterable]]:
        """
        Dependents property.
        """
        return None

    @property
    def Keys(self) -> typing.Optional[typing.Iterable[str]]:
        """
        Keys property.
        """
        return None

    @property
    def Values(self) -> typing.Optional[typing.Iterable[typing.Iterable]]:
        """
        Values property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    @property
    def ShowHiddenColumns(self) -> typing.Optional[bool]:
        """
        ShowHiddenColumns property.
        """
        return None

    @ShowHiddenColumns.setter
    def ShowHiddenColumns(self, value: typing.Optional[bool]) -> None:
        """
        ShowHiddenColumns property.
        """
        pass

    @property
    def HiddenColumns(self) -> typing.Optional[tuple[str]]:
        """
        HiddenColumns property.
        """
        return None

    def __init__(self, independents: typing.Iterable[dict[str,typing.Iterable]], dependents: typing.Iterable[dict[str,typing.Iterable]], hiddenColumns: tuple[str]) -> None:
        """
        __init__ method.
        """
        pass

    def ContainsKey(self, key: str) -> bool:
        """
        ContainsKey method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[dict[str,typing.Iterable]]:
        """
        GetEnumerator method.
        """
        pass

    def TryGetValue(self, key: str, value: typing.Iterable) -> bool:
        """
        TryGetValue method.
        """
        pass

    @typing.overload
    def ToString(self) -> str:
        ...

    @typing.overload
    def ToString(self, showHiddenColumns: bool) -> str:
        ...

    def ToString(self, *args: typing.Any) -> str:
        """
        ToString method.
        """
        pass

    def __repr__(self) -> str:
        """
        __repr__ method.
        """
        pass


class ResultVariable(object):
    """
    Specifies column data for the Result Table.
    """

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        Unit property.
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        QuantityName property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass

    def __repr__(self) -> str:
        """
        __repr__ method.
        """
        pass


