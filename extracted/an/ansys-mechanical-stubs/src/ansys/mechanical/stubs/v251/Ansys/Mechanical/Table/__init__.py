"""Table module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ColumnarDataImportDefinition(object):
    """
    
            A simple class to hold the import definitions for how a column from a data source in
            columnar format should be processed.
            
    """

    @property
    def Index(self) -> typing.Optional[int]:
        """
        
            Gets or sets the specified data source column index from which this variable will be
            imported.
            
        """
        return None

    @Index.setter
    def Index(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the specified data source column index from which this variable will be
            imported.
            
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets an identifier for the data source column.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets an identifier for the data source column.
            
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            Gets or sets the unit of the column.
            
        """
        return None

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the unit of the column.
            
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType]:
        """
        
            Gets or sets the variable type of the column.
            
        """
        return None

    @VariableType.setter
    def VariableType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType]) -> None:
        """
        
            Gets or sets the variable type of the column.
            
        """
        pass

    @property
    def VariableClassification(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification]:
        """
        
            Gets or sets the variable classification of the column.
            
        """
        return None

    @VariableClassification.setter
    def VariableClassification(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification]) -> None:
        """
        
            Gets or sets the variable classification of the column.
            
        """
        pass

    def __init__(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType, variableClassification: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification, unit: str, name: str) -> None:
        """
        
            Construct a  instance.
            
        """
        pass

    @classmethod
    def GenerateFromComImportDefinition(cls, comImportDefinition: Ansys.Common.Interop.AnsStdObjects.DSTableImportSettingsColumnarDataImportDefinition) -> Ansys.Mechanical.Table.ColumnarDataImportDefinition:
        """
        GenerateFromComImportDefinition method.
        """
        pass

    @classmethod
    def SaveAsComImportDefinition(cls, importDefinition: Ansys.Mechanical.Table.ColumnarDataImportDefinition) -> Ansys.Common.Interop.AnsStdObjects.DSTableImportSettingsColumnarDataImportDefinition:
        """
        SaveAsComImportDefinition method.
        """
        pass


class ColumnarDataSourceBase(object):
    """
    
             is a class that provides foundational behavior for
            import settings that consume data from columnar data sources (such as delimited or
            fixed-width files).
            
    """

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of column definitions.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]) -> None:
        """
        Item property.
        """
        pass

    @property
    def SkipFooter(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        return None

    @SkipFooter.setter
    def SkipFooter(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        pass

    @property
    def SkipRows(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        return None

    @SkipRows.setter
    def SkipRows(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    @property
    def PathType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        return None

    @PathType.setter
    def PathType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]) -> None:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        pass

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType, variableClassification: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification, unit: str, name: str) -> Ansys.Mechanical.Table.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the data imported to .
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class FixedWidthImportSettings(object):
    """
    
             defines how to import data from a delimited source
            for tabular data.
            
    """

    @property
    def ColumnWidths(self) -> typing.Optional[typing.Any]:
        """
        
            Gets or sets the specified column widths.
            When setting, The value provided to  may be either:
            
              
                A `string` using Fortran-esque fixed-format specifications. This is similar to the
                “User-Defined” format specifier for External Data as described in the product
                documentation. Note, however, that regardless of the format specifier all imported
                columns WILL be interpreted using the .NET command `double.TryParse()` to support
                the requirements of the underlying variable data for Table.
              
              
                An  containing the widths of each column. Negative
                values may be specified to define a negated width, meaning ‘-2’ would be equivalent
                to the fixed-width string specification ’2X’.
              
            
            
        """
        return None

    @ColumnWidths.setter
    def ColumnWidths(self, value: typing.Optional[typing.Any]) -> None:
        """
        
            Gets or sets the specified column widths.
            When setting, The value provided to  may be either:
            
              
                A `string` using Fortran-esque fixed-format specifications. This is similar to the
                “User-Defined” format specifier for External Data as described in the product
                documentation. Note, however, that regardless of the format specifier all imported
                columns WILL be interpreted using the .NET command `double.TryParse()` to support
                the requirements of the underlying variable data for Table.
              
              
                An  containing the widths of each column. Negative
                values may be specified to define a negated width, meaning ‘-2’ would be equivalent
                to the fixed-width string specification ’2X’.
              
            
            
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of column definitions.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]) -> None:
        """
        Item property.
        """
        pass

    @property
    def SkipFooter(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        return None

    @SkipFooter.setter
    def SkipFooter(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        pass

    @property
    def SkipRows(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        return None

    @SkipRows.setter
    def SkipRows(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    @property
    def PathType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        return None

    @PathType.setter
    def PathType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]) -> None:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        pass

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def GenerateFromComImportSettings(cls, importSettings: Ansys.Common.Interop.DSObjects.IDSTableImportSettingsFixedWidth) -> Ansys.Mechanical.Table.ImportSettingsBase:
        """
        GenerateFromComImportSettings method.
        """
        pass

    @classmethod
    def SaveToComImportSettings(cls, importSettings: Ansys.Mechanical.Table.FixedWidthImportSettings) -> Ansys.Common.Interop.DSObjects.IDSTableImportSettingsBase:
        """
        SaveToComImportSettings method.
        """
        pass

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType, variableClassification: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification, unit: str, name: str) -> Ansys.Mechanical.Table.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the data imported to .
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class DelimitedImportSettings(object):
    """
    
             defines how to import data from a delimited source
            for tabular data.
            
    """

    @property
    def Delimiter(self) -> typing.Optional[str]:
        """
        
            The delimiter used to separate columns.
            
        """
        return None

    @Delimiter.setter
    def Delimiter(self, value: typing.Optional[str]) -> None:
        """
        
            The delimiter used to separate columns.
            
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of column definitions.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.Table.ColumnarDataImportDefinition]) -> None:
        """
        Item property.
        """
        pass

    @property
    def SkipFooter(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        return None

    @SkipFooter.setter
    def SkipFooter(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to ignore at the end of the file during import.
            
        """
        pass

    @property
    def SkipRows(self) -> typing.Optional[int]:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        return None

    @SkipRows.setter
    def SkipRows(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the number of rows to skip over at the start of the file during import.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    @property
    def PathType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        return None

    @PathType.setter
    def PathType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]) -> None:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        pass

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def GenerateFromComImportSettings(cls, comImportSettings: Ansys.Common.Interop.DSObjects.IDSTableImportSettingsDelimited) -> Ansys.Mechanical.Table.ImportSettingsBase:
        """
        GenerateFromComImportSettings method.
        """
        pass

    @classmethod
    def SaveToComImportSettings(cls, importSettings: Ansys.Mechanical.Table.DelimitedImportSettings) -> Ansys.Common.Interop.DSObjects.IDSTableImportSettingsBase:
        """
        SaveToComImportSettings method.
        """
        pass

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.Table.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableType, variableClassification: Ansys.Mechanical.DataModel.MechanicalEnums.Table.VariableClassification, unit: str, name: str) -> Ansys.Mechanical.Table.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the data imported to .
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class ImportHelpers(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def TryParseColumnWidths(cls, columnsWidthsAsString: str, columnWidthCollection: Ansys.Mechanical.Table.ImportHelpers.ColumnWidthSpecification) -> Ansys.Mechanical.Table.ImportHelpers.ColumnWidthsParseResult:
        """
        TryParseColumnWidths method.
        """
        pass


class ImportSettingsBase(object):
    """
    
            A base class for Table import settings.
            
    """

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Table.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    @property
    def PathType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        return None

    @PathType.setter
    def PathType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Common.PathType]) -> None:
        """
        
            Gets or sets the type of URI provided for Table import.
            Default: 
            
        """
        pass


class ImportSettingsFactory(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def GetSettingsForFormat(cls, format: Ansys.Mechanical.DataModel.MechanicalEnums.Table.ImportFormat) -> Ansys.Mechanical.Table.ImportSettingsBase:
        """
        
             constructs and returns the correct settings class
            instance based on the specified format.
            
        """
        pass


