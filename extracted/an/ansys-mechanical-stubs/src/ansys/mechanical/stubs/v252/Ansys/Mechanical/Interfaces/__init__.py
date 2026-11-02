"""Interfaces module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class IDataSeries(object):

    @property
    def DataType(self) -> typing.Optional[type]:
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the name of the data series.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the name of the data series.
            
        """
        pass

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        
            Gets or sets the quantity name of the data series, e.g., “Length”, “Pressure”, or “Heat Flux”.
            
        """
        return None

    @QuantityName.setter
    def QuantityName(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the quantity name of the data series, e.g., “Length”, “Pressure”, or “Heat Flux”.
            
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            Gets or sets a string representation of the data series units, e.g., “m”,
            “kg m^-1 s^-2”, or “kg m^2 s^-3”.
            
        """
        return None

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets a string representation of the data series units, e.g., “m”,
            “kg m^-1 s^-2”, or “kg m^2 s^-3”.
            
        """
        pass

    @property
    def Values(self) -> typing.Optional[typing.Collection]:
        """
        
            Explicitly gets or sets the values of the data series.
            
        """
        return None

    @Values.setter
    def Values(self, value: typing.Optional[typing.Collection]) -> None:
        """
        
            Explicitly gets or sets the values of the data series.
            
        """
        pass

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
        """
        IsReadOnly property.
        """
        return None

    @property
    def IsFixedSize(self) -> typing.Optional[bool]:
        """
        IsFixedSize property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    @property
    def SyncRoot(self) -> typing.Optional[typing.Any]:
        """
        SyncRoot property.
        """
        return None

    @property
    def IsSynchronized(self) -> typing.Optional[bool]:
        """
        IsSynchronized property.
        """
        return None

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

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass

    def Add(self, value: typing.Any) -> int:
        """
        Add method.
        """
        pass

    def Contains(self, value: typing.Any) -> bool:
        """
        Contains method.
        """
        pass

    def Clear(self) -> None:
        """
        Clear method.
        """
        pass

    def IndexOf(self, value: typing.Any) -> int:
        """
        IndexOf method.
        """
        pass

    def Insert(self, index: int, value: typing.Any) -> None:
        """
        Insert method.
        """
        pass

    def Remove(self, value: typing.Any) -> None:
        """
        Remove method.
        """
        pass

    def RemoveAt(self, index: int) -> None:
        """
        RemoveAt method.
        """
        pass

    def CopyTo(self, array: typing.List, index: int) -> None:
        """
        CopyTo method.
        """
        pass


class IDataTable(object):

    @property
    def ColumnNames(self) -> typing.Optional[tuple[str]]:
        return None

    @property
    def Columns(self) -> typing.Optional[typing.List[Ansys.Mechanical.Interfaces.IDataSeries]]:
        """
        
            Explicitly get the columns of the data table.
            
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of columns in the table.
            
        """
        return None

    @property
    def IsFixedColumnCount(self) -> typing.Optional[bool]:
        """
        
            Get whether additional columns can be added or removed from the contained .
            
        """
        return None

    @property
    def IsFixedRowCount(self) -> typing.Optional[bool]:
        """
        
            Get whether additional rows can be added or removed from the contained
            .
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        
            Gets whether the data table is read-only.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Interfaces.IDataSeries]:
        """
        Item property.
        """
        return None

    @property
    def Metadata(self) -> typing.Optional[dict[str,typing.Any]]:
        """
        
            Gets or set a dictionary with additional information that may be useful to understanding
            the context of data in the table.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Get or set the name of the table.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Get or set the name of the table.
            
        """
        pass

    @property
    def RowCount(self) -> typing.Optional[int]:
        return None

    def Add(self, dataSeries: Ansys.Mechanical.Interfaces.IDataSeries) -> None:
        """
        
            Add a new column to the data table.
            
        """
        pass

    def Clear(self) -> None:
        """
        
            Drops all columns from the data table.
            
        """
        pass

    def Contains(self, name: str) -> bool:
        """
        
            Returns whether the data table contains a column with the specified name.
            
        """
        pass

    def GetRow(self, rowIndex: int) -> typing.Iterable:
        pass

    def Insert(self, columnIndex: int, dataSeries: Ansys.Mechanical.Interfaces.IDataSeries) -> None:
        """
        
            Insert a column at the specified index.
            
        """
        pass

    def Remove(self, key: typing.Any) -> None:
        """
        
            Removes the specified column. If key is an , it will
            be interpreted as an index. If key is a , it will
            be interpreted as a column name.
            
        """
        pass

    def TryInsertRow(self, rowIndex: int, values: typing.Iterable) -> bool:
        """
        
            Try to insert the values at the specified row index.
            
        """
        pass

    def TryRemoveRow(self, rowIndex: int) -> bool:
        """
        
            Try to remove the specified row.
            
        """
        pass

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass


class IReadOnlyDataSeries(object):

    @property
    def Item(self) -> typing.Optional[typing.Any]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of data points.
            
        """
        return None

    @property
    def DataType(self) -> typing.Optional[type]:
        """
        
            Gets the type stored by the data series.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the name of the data series.
            
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        
            Gets the quantity name of the data series, e.g., “Length”, “Pressure”, or “Heat Flux”.
            
        """
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            Gets the string representation of the data series units, e.g., “m”, “kg m^-1 s^-2”,
            or “kg m^2 s^-3”.
            
        """
        return None

    @property
    def Values(self) -> typing.Optional[typing.Collection]:
        """
        
            Explicitly get the values of the data series.
            
        """
        return None

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass


class IReadOnlyDataTable(object):

    @property
    def ColumnNames(self) -> typing.Optional[tuple[str]]:
        """
        
            Gets a list of the column names.
            
        """
        return None

    @property
    def Columns(self) -> typing.Optional[tuple[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]]:
        """
        
            Explicitly get the columns of the table.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Interfaces.IReadOnlyDataSeries]:
        """
        Item property.
        """
        return None

    @property
    def Metadata(self) -> typing.Optional[dict[str,typing.Any]]:
        """
        
            Gets a dictionary with additional information that may be useful to understanding the
            context of data in the table.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Get the name of the table.
            
        """
        return None

    @property
    def RowCount(self) -> typing.Optional[int]:
        """
        
            Gets the maximum number of data points (rows) among all columns in the table
            
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    def GetRow(self, rowIndex: int) -> typing.Iterable:
        """
        
            Returns an enumerable to iterate over the values in a row.
            
        """
        pass

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass


class ITable(object):
    """
    
            Exposes a table, which is a two-dimensional tabular data structure with labeled columns.
            The columns are usually instances of IVariable but can be any sort of array
            
    """

    @property
    def Independents(self) -> typing.Optional[dict[str,typing.Iterable]]:
        """
        The portion of the table corresponding to independent variables.
        """
        return None

    @property
    def Dependents(self) -> typing.Optional[dict[str,typing.Iterable]]:
        """
        The portion of the table corresponding to dependent variables.
        """
        return None

    @property
    def Item(self) -> typing.Optional[typing.Iterable]:
        """
        Item property.
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

    def ContainsKey(self, key: str) -> bool:
        """
        ContainsKey method.
        """
        pass

    def TryGetValue(self, key: str, value: typing.Iterable) -> bool:
        """
        TryGetValue method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass


class IVariable(object):
    """
    Exposes a variable, which is a one dimensional array of real numbers with a unit.
    """

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        The unit of the variable.  For example, this could be "mm".
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        The quantity name of the variable.  For example, this could be "Length".
        """
        return None

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    def GetEnumerator(self) -> typing.Iterator:
        """
        GetEnumerator method.
        """
        pass


