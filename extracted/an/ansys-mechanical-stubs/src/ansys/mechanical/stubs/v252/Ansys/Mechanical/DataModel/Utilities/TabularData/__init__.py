"""TabularData module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class DataSeriesAdapter(object):
    """
    
            Expresses any Data Series as a  instance with optional read-only
            enforcement.
            
    """

    @property
    def Item(self) -> typing.Optional[typing.Any]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[typing.Any]) -> None:
        """
        Item property.
        """
        pass

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        return None

    @property
    def IsFixedSize(self) -> typing.Optional[bool]:
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        return None

    @property
    def SyncRoot(self) -> typing.Optional[typing.Any]:
        return None

    @property
    def IsSynchronized(self) -> typing.Optional[bool]:
        return None

    @property
    def DataType(self) -> typing.Optional[type]:
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        pass

    @property
    def QuantityName(self) -> typing.Optional[str]:
        return None

    @QuantityName.setter
    def QuantityName(self, value: typing.Optional[str]) -> None:
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        return None

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        pass

    @property
    def Values(self) -> typing.Optional[typing.Collection]:
        return None

    @Values.setter
    def Values(self, value: typing.Optional[typing.Collection]) -> None:
        pass

    def __init__(self, potentialDataSeries: typing.Any, enforceReadOnly: bool) -> None:
        """
        
            Construct by wrapping around a potential Data Series instance.
            
        """
        pass

    def GetEnumerator(self) -> typing.Iterator:
        pass

    def Add(self, value: typing.Any) -> int:
        pass

    def Contains(self, value: typing.Any) -> bool:
        pass

    def Clear(self) -> None:
        pass

    def IndexOf(self, value: typing.Any) -> int:
        pass

    def Insert(self, index: int, value: typing.Any) -> None:
        pass

    def Remove(self, value: typing.Any) -> None:
        pass

    def RemoveAt(self, index: int) -> None:
        pass

    def CopyTo(self, array: typing.List, destinationStartIndex: int) -> None:
        pass

    def add_PropertyChanged(self, value: System.ComponentModel.PropertyChangedEventHandler) -> None:
        """
        add_PropertyChanged method.
        """
        pass

    def remove_PropertyChanged(self, value: System.ComponentModel.PropertyChangedEventHandler) -> None:
        """
        remove_PropertyChanged method.
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


class ReadOnlyDataSeriesAdapter(object):
    """
    
            Exposes any Data Series instance through the  interface.
            
    """

    @property
    def Item(self) -> typing.Optional[typing.Any]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        return None

    @property
    def DataType(self) -> typing.Optional[type]:
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        return None

    @property
    def Values(self) -> typing.Optional[typing.Collection]:
        return None

    def __init__(self, potentialDataSeries: typing.Any) -> None:
        """
        
            Construct by wrapping around a potential Data Series instance.
            
        """
        pass

    def GetEnumerator(self) -> typing.Iterator:
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


class ReadOnlyDataTableAdapter(object):
    """
    
            Exposes and  instance through the 
            interface.
            
    """

    @property
    def Count(self) -> typing.Optional[int]:
        return None

    @property
    def ColumnNames(self) -> typing.Optional[tuple[str]]:
        return None

    @property
    def Columns(self) -> typing.Optional[tuple[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]]:
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]:
        """
        Item property.
        """
        return None

    @property
    def Metadata(self) -> typing.Optional[dict[str,typing.Any]]:
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        return None

    @property
    def RowCount(self) -> typing.Optional[int]:
        return None

    def __init__(self, dataTable: Ansys.Mechanical.Interfaces.IDataTable) -> None:
        """
        
            Construct by wrapping around an IDataTable instance.
            
        """
        pass

    def GetRow(self, rowIndex: int) -> typing.Iterable:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]:
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


