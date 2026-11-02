"""ExternalData module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CGNSImportSettings(object):
    """
    
             defines how to import external data from a CGNS file.
            
    """

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


class H5ImportSettings(object):
    """
    
             defines how to import external data from a H5 file.
            
    """

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


class AXDTImportSettings(object):
    """
    
             defines how to import external data from an AXDT file.
            
    """

    @property
    def Dimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]:
        """
        
            The dimension of the AXDT file.
            
        """
        return None

    @Dimension.setter
    def Dimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]) -> None:
        """
        
            The dimension of the AXDT file.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


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
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType]:
        """
        
            Gets or sets the variable type of the column.
            
        """
        return None

    @VariableType.setter
    def VariableType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType]) -> None:
        """
        
            Gets or sets the variable type of the column.
            
        """
        pass

    @property
    def UserFieldVariable(self) -> typing.Optional[str]:
        """
        
            
            Gets or sets the user field variable type as a string for the column. 
            
            
            This property is only used when VariableType is UserField.
            
            
        """
        return None

    @UserFieldVariable.setter
    def UserFieldVariable(self, value: typing.Optional[str]) -> None:
        """
        
            
            Gets or sets the user field variable type as a string for the column. 
            
            
            This property is only used when VariableType is UserField.
            
            
        """
        pass

    def __init__(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType, unit: str, name: str, userFieldVariable: str) -> None:
        """
        
            Construct a  instance.
            
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
    def Item(self) -> typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]) -> None:
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
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType, unit: str, name: str) -> Ansys.Mechanical.ExternalData.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the table/>.
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class DelimitedImportSettings(object):
    """
    
             defines how to import external data from a delimited source file.
            
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
    def AverageCornerNodesToMidsideNodes(self) -> typing.Optional[bool]:
        """
        
            
            If set to Yes, the data at Midside nodes is calculated as average of data specified at corner nodes. 
            
            
            Defaults to False.
            
            
            This property is used only when there is another external data file defined with MAPDL import format. 
            
            
        """
        return None

    @AverageCornerNodesToMidsideNodes.setter
    def AverageCornerNodesToMidsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        
            
            If set to Yes, the data at Midside nodes is calculated as average of data specified at corner nodes. 
            
            
            Defaults to False.
            
            
            This property is used only when there is another external data file defined with MAPDL import format. 
            
            
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of column definitions.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]) -> None:
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
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType, unit: str, name: str) -> Ansys.Mechanical.ExternalData.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the table/>.
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class ECADImportSettings(object):
    """
    
             defines how to import external data from an ECAD file.
            
    """

    @property
    def UseDummyNetData(self) -> typing.Optional[bool]:
        """
        
            The UseDummyNetData falg of the ECAD file. For External Data files that include trace mapping, 
            selecting this option enables you to import trace data belonging to the dummy net of the file.
            
        """
        return None

    @UseDummyNetData.setter
    def UseDummyNetData(self, value: typing.Optional[bool]) -> None:
        """
        
            The UseDummyNetData falg of the ECAD file. For External Data files that include trace mapping, 
            selecting this option enables you to import trace data belonging to the dummy net of the file.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


class ExternalDataFile(object):
    """
    
            A basic definition of the external data file. 
            
    """

    @property
    def FilePath(self) -> typing.Optional[str]:
        """
        
            Gets or sets the file path of the external data file.
            
        """
        return None

    @FilePath.setter
    def FilePath(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the file path of the external data file.
            
        """
        pass

    @property
    def Identifier(self) -> typing.Optional[str]:
        """
        
            Gets or sets the identifier of the external data file.
            
        """
        return None

    @Identifier.setter
    def Identifier(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the identifier of the external data file.
            
        """
        pass

    @property
    def Description(self) -> typing.Optional[str]:
        """
        
            Gets or sets the optional description of the external data file.
            
        """
        return None

    @Description.setter
    def Description(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the optional description of the external data file.
            
        """
        pass

    @property
    def IsMainFile(self) -> typing.Optional[bool]:
        """
        
            
            Gets or sets the main file flag of the external data file.
            
            
            The nodal coordinate data for the selected main file is processed by the mapping 
            utility. The nodal coordinate data will be skipped in all other files. 
            
            
            Only one file can be set as the main file, otherwise, an exception will be thrown 
            during the import. 
            
            
            If the import format is MAPDL, the value of this property will be ignored as the 
            MAPDL CDB file will always be treated as main file during the import.
            
            
        """
        return None

    @IsMainFile.setter
    def IsMainFile(self, value: typing.Optional[bool]) -> None:
        """
        
            
            Gets or sets the main file flag of the external data file.
            
            
            The nodal coordinate data for the selected main file is processed by the mapping 
            utility. The nodal coordinate data will be skipped in all other files. 
            
            
            Only one file can be set as the main file, otherwise, an exception will be thrown 
            during the import. 
            
            
            If the import format is MAPDL, the value of this property will be ignored as the 
            MAPDL CDB file will always be treated as main file during the import.
            
            
        """
        pass

    @property
    def ImportSettings(self) -> typing.Optional[Ansys.Mechanical.ExternalData.ImportSettingsBase]:
        """
        
            
            Gets or sets the import settings for current external data file.
            
            
            An import settings can be created by calling the GetSettingsForFormat 
            method from the factory class .
            
            
        """
        return None

    @ImportSettings.setter
    def ImportSettings(self, value: typing.Optional[Ansys.Mechanical.ExternalData.ImportSettingsBase]) -> None:
        """
        
            
            Gets or sets the import settings for current external data file.
            
            
            An import settings can be created by calling the GetSettingsForFormat 
            method from the factory class .
            
            
        """
        pass

    @property
    def IsRootRelativePath(self) -> typing.Optional[bool]:
        """
        IsRootRelativePath property.
        """
        return None

    @IsRootRelativePath.setter
    def IsRootRelativePath(self, value: typing.Optional[bool]) -> None:
        """
        IsRootRelativePath property.
        """
        pass

    def __init__(self, importSettings: Ansys.Mechanical.ExternalData.ImportSettingsBase, filePath: str, identifier: str, description: str, isMainFile: bool, isRootRelativePath: bool) -> None:
        """
        
            
            Construct a  instance.
            
            
            If `identifier` is provided, it should be unique, otherwise, an exception will be thrown during the import. 
            
            
            An import settings can be created by calling the GetSettingsForFormat 
            method from the factory class .
            
            
        """
        pass


class ExternalDataFileCollection(object):
    """
    
             is a class that provides foundational behavior for
            holding external data files.
            
    """

    @property
    def SaveFilesWithProject(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the flag controlling if the external data files will be copied to the project directory. 
            If this flag is set to False, the external data files will directly reference the file path. 
            The default is False. 
            
        """
        return None

    @SaveFilesWithProject.setter
    def SaveFilesWithProject(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the flag controlling if the external data files will be copied to the project directory. 
            If this flag is set to False, the external data files will directly reference the file path. 
            The default is False. 
            
        """
        pass

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.ExternalData.ExternalDataFile]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.ExternalData.ExternalDataFile]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of external data files.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        return None

    def __init__(self, saveFilesWithProject: bool) -> None:
        """
        
            
            Construct a  instance.
            
            
        """
        pass

    def Add(self, item: Ansys.Mechanical.ExternalData.ExternalDataFile) -> None:
        pass

    def Clear(self) -> None:
        pass

    def Contains(self, item: Ansys.Mechanical.ExternalData.ExternalDataFile) -> bool:
        pass

    def CopyTo(self, array: Ansys.Mechanical.ExternalData.ExternalDataFile, arrayIndex: int) -> None:
        """
        CopyTo method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.ExternalData.ExternalDataFile]:
        pass

    def IndexOf(self, item: Ansys.Mechanical.ExternalData.ExternalDataFile) -> int:
        pass

    def Insert(self, index: int, item: Ansys.Mechanical.ExternalData.ExternalDataFile) -> None:
        pass

    def Remove(self, item: Ansys.Mechanical.ExternalData.ExternalDataFile) -> bool:
        pass

    def RemoveAt(self, index: int) -> None:
        pass


class FixedWidthImportSettings(object):
    """
    
             defines how to import external data from a fixed-width source file.
            
    """

    @property
    def ColumnWidths(self) -> typing.Optional[str]:
        """
        
            
            Gets or sets the specified column widths as a `string` using Fortran-esque fixed-format specifications. 
            
            
            This is equivalent to the “User-Defined” format specifier for External Data as described in the product 
            documentation. 
            
            
            Note, however, that regardless of the format specifier all imported columns WILL be interpreted using the 
            .NET command `double.TryParse()` to support the requirements of the underlying variable data for Table. 
            
            
            In the example below, the line has one integer followed by four exponential data types. 
            385 8.333333333E-003 9.375000000E-003 3.375000000E-001 0.000000000E+000 
            The corresponding format is `1i3,4e17.9` 
            Where: 
            The first entry is the number of occurrences
            The second entry is the format specifier
            The third entry is the number of characters of data in the definition(including numeric values (0-9), 
            the letter 'e' (for instances of scientific notation), and any white space and + or - signs) 
            The fourth entry is the number of digits after the decimal point.
            
            
        """
        return None

    @ColumnWidths.setter
    def ColumnWidths(self, value: typing.Optional[str]) -> None:
        """
        
            
            Gets or sets the specified column widths as a `string` using Fortran-esque fixed-format specifications. 
            
            
            This is equivalent to the “User-Defined” format specifier for External Data as described in the product 
            documentation. 
            
            
            Note, however, that regardless of the format specifier all imported columns WILL be interpreted using the 
            .NET command `double.TryParse()` to support the requirements of the underlying variable data for Table. 
            
            
            In the example below, the line has one integer followed by four exponential data types. 
            385 8.333333333E-003 9.375000000E-003 3.375000000E-001 0.000000000E+000 
            The corresponding format is `1i3,4e17.9` 
            Where: 
            The first entry is the number of occurrences
            The second entry is the format specifier
            The third entry is the number of characters of data in the definition(including numeric values (0-9), 
            the letter 'e' (for instances of scientific notation), and any white space and + or - signs) 
            The fourth entry is the number of digits after the decimal point.
            
            
        """
        pass

    @property
    def AverageCornerNodesToMidsideNodes(self) -> typing.Optional[bool]:
        """
        
            
            If set to Yes, the data at Midside nodes is calculated as average of data specified at corner nodes. 
            
            
            Defaults to False.
            
            
            This property is used only when there is another external data file defined with MAPDL import format. 
            
            
        """
        return None

    @AverageCornerNodesToMidsideNodes.setter
    def AverageCornerNodesToMidsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        
            
            If set to Yes, the data at Midside nodes is calculated as average of data specified at corner nodes. 
            
            
            Defaults to False.
            
            
            This property is used only when there is another external data file defined with MAPDL import format. 
            
            
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            Gets the number of column definitions.
            
        """
        return None

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]) -> None:
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
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def Clear(self) -> None:
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.Mechanical.ExternalData.ColumnarDataImportDefinition]:
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the import definition at the specified index.
            
        """
        pass

    def UseColumn(self, index: int, variableType: Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.VariableType, unit: str, name: str) -> Ansys.Mechanical.ExternalData.ColumnarDataSourceBase:
        """
        
            
            Add a column to be imported from the specified data source column index and configured
            as the specified variable type. The order in which columns are added determines their
            order in the table/>.
            
            
            If unit is `null`, the default unit (in the active unit system) for the specified
            variable type will be assumed during import.
            
            
            If name is `null` or empty, a unique name will be generated from the specified
            variableType during import.
            
            
            A reference to the instance is returned so that invocations can be chained together.
            
            
        """
        pass


class ICEPAKImportSettings(object):
    """
    
             defines how to import external data from an ICEPAK BOOL or ICEPAK COND file. 
            
    """

    @property
    def SupportingFilePath(self) -> typing.Optional[str]:
        """
        
            The supporting file path of the ICEPAK INFO file.
            
        """
        return None

    @SupportingFilePath.setter
    def SupportingFilePath(self, value: typing.Optional[str]) -> None:
        """
        
            The supporting file path of the ICEPAK INFO file.
            
        """
        pass

    @property
    def SupportingFileIdentifier(self) -> typing.Optional[str]:
        """
        
            The supporting file identifier. The identifier should be unique, otherwise, an exception will be 
            thrown during the import. 
            
        """
        return None

    @SupportingFileIdentifier.setter
    def SupportingFileIdentifier(self, value: typing.Optional[str]) -> None:
        """
        
            The supporting file identifier. The identifier should be unique, otherwise, an exception will be 
            thrown during the import. 
            
        """
        pass

    @property
    def SupportingFileDescription(self) -> typing.Optional[str]:
        """
        
            The supporting file description. This is optional.
            
        """
        return None

    @SupportingFileDescription.setter
    def SupportingFileDescription(self, value: typing.Optional[str]) -> None:
        """
        
            The supporting file description. This is optional.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


class ImportSettingsBase(object):
    """
    
            A base class for Table import settings.
            
    """

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None


class ImportSettingsFactory(object):

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def GetSettingsForFormat(cls, format: Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat) -> Ansys.Mechanical.ExternalData.ImportSettingsBase:
        """
        
             constructs and returns the correct settings class
            instance based on the specified format.
            
        """
        pass


class MAPDLImportSettings(object):
    """
    
             defines how to import external data from a MAPDL CDB file.
            
    """

    @property
    def Dimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]:
        """
        
            The dimension of the MAPDL CDB file.
            
        """
        return None

    @Dimension.setter
    def Dimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]) -> None:
        """
        
            The dimension of the MAPDL CDB file.
            
        """
        pass

    @property
    def LengthUnit(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.LengthUnit]:
        """
        
            The length unit of the MAPDL CDB file.
            
        """
        return None

    @LengthUnit.setter
    def LengthUnit(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.LengthUnit]) -> None:
        """
        
            The length unit of the MAPDL CDB file.
            
        """
        pass

    @property
    def Format(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.ExternalData.ImportFormat]:
        """
        
            Gets the existing corresponding format.
            
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


