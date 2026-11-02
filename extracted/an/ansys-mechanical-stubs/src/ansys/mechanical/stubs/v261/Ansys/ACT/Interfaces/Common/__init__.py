"""Common module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class AngleUnitType(Enum):
    """
    Specifies the AngleUnitType.
    """

    Radian = 1
    Degree = 0

class AngularVelocityUnitType(Enum):
    """
    Specifies the AngularVelocityUnitType.
    """

    RadianPerMilliSecond = 2
    RadianPerSecond = 1
    RPM = 0

class MechanicalUnitSystemEnum(Enum):
    """
    Specifies the WBUnitSystemType.
    """

    ConsistentBFT = 7
    ConsistentBIN = 8
    ConsistentCGS = 5
    ConsistentMKS = 11
    ConsistentNMM = 6
    ConsistentUMKS = 10
    NoUnitSystem = 19
    StandardBFT = 3
    StandardBIN = 4
    StandardCGS = 1
    StandardCUST = 12
    StandardMKS = 0
    StandardNMM = 2
    StandardNMMdat = 14
    StandardNMMton = 13
    StandardUMKS = 9
    StandardKNMS = 15
    StandardGMMS = 17

class MetricTemperatureUnitType(Enum):
    """
    Specifies the MetricTemperatureUnitType.
    """

    Celsius = 1
    Kelvin = 0

class SelectionTypeEnum(Enum):
    """
    
            Specifies the selection type.
            
    """

    GeometryEntities = 0
    MeshNodes = 1
    MeshElements = 2
    PathSpecific = 3
    SurfaceSpecific = 4
    WorksheetSpecific = 5
    MeshElementFaces = 6

class State(Enum):
    """
    
            General state enumeration to be used across ACT Apps.
            
    """

    UpToDate = 0
    RefreshRequired = 1
    OutOfDate = 2
    UpdateRequired = 3
    Modified = 4
    Unfulfilled = 5
    Disabled = 6
    Error = 7
    EditRequired = 8
    Interrupted = 9
    UpstreamChangesPending = 10
    Unknown = 11

class StateMessageTypes(Enum):
    """
    
            Specifies the selection type.
            
    """

    Information = 0
    Warning = 1
    Error = 2

class IProcessUtilities(object):

    def Start(self, target: str, args: str) -> int:
        """
        Start method.
        """
        pass


class ISourceFile(object):
    """
    
            A file containing source code.
            
    """

    @property
    def FilePath(self) -> typing.Optional[str]:
        """
        
            Represents the absolute path of the source file.
            
        """
        return None

    @property
    def FileName(self) -> typing.Optional[str]:
        """
        
            The name of the source file.
            
        """
        return None

    @property
    def Content(self) -> typing.Optional[str]:
        """
        
            Reads or writes the content of the file.
            
        """
        return None

    @Content.setter
    def Content(self, value: typing.Optional[str]) -> None:
        """
        
            Reads or writes the content of the file.
            
        """
        pass

    def Save(self) -> None:
        """
        
            Saves the modified content.
            
        """
        pass

    def Equals(self, other: Ansys.ACT.Interfaces.Common.ISourceFile) -> bool:
        """
        Equals method.
        """
        pass


class IWorksheet(object):
    """
    
            Defines a worksheets information.
            
    """

    @property
    def RowCount(self) -> typing.Optional[int]:
        """
        
            Gets the number of rows contained in the worksheet.
            
        """
        return None

    def AddRow(self) -> int:
        """
        
            Adds a row to the worksheet.
            
        """
        pass

    def DeleteRow(self, index: int) -> None:
        """
        
            Deletes a row from the worksheet at index.
            
        """
        pass


class IParameter(object):
    """
    
            Defines a design parameter.
            
    """

    @property
    def Key(self) -> typing.Optional[str]:
        """
        
            Gets the identifier of the parameter.
            
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the name of the parameter.
            
        """
        return None

    @property
    def Value(self) -> typing.Optional[float]:
        """
        
            Gets the value of the parameter.
            
        """
        return None


class IAttributeCollection(object):
    """
    
            Defines a collection of attributes.
            
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
    def Keys(self) -> typing.Optional[System.Collections.Generic.ICollection[str]]:
        """
        
            Gets the list of attribute names.
            
        """
        return None

    def GetValue(self, name: str, defaultValue: typing.Any) -> typing.Any:
        """
        
            Returns the value of the attribute identified by its name.
            
        """
        pass

    def GetStringValue(self, name: str) -> str:
        """
        
            Returns the string value of the attribute identified by its name.
            
        """
        pass

    def SetValue(self, name: str, value: typing.Any) -> None:
        """
        
            Sets the value of an attribute identified by its name.
            
        """
        pass

    def Remove(self, name: str) -> bool:
        """
        
            Removes the attribute identified by its name.
            
        """
        pass

    def Contains(self, name: str) -> bool:
        """
        
            Checks if the collection contains the attribute identified by its name.
            
        """
        pass


class IExtension(object):
    """
    
            Defines an extension.
            
    """

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets the name of the extension.
            
        """
        return None

    @property
    def Version(self) -> typing.Optional[int]:
        """
        
            Gets the version of the extension.
            
        """
        return None

    @property
    def MinorVersion(self) -> typing.Optional[int]:
        """
        
            Gets the minor version of the extension.
            
        """
        return None

    @property
    def ScriptEngine(self) -> typing.Optional[Microsoft.Scripting.Hosting.ScriptEngine]:
        """
        
            Gets the IronPython script engine.
            
        """
        return None

    @property
    def ScriptScope(self) -> typing.Optional[Microsoft.Scripting.Hosting.ScriptScope]:
        """
        
            Gets the IronPython scope.
            
        """
        return None

    @property
    def UniqueId(self) -> typing.Optional[str]:
        """
        
            Gets the unique identifier of the extension.
            
        """
        return None

    @property
    def InstallDir(self) -> typing.Optional[str]:
        """
        
            Gets the folder where the extension is installed.
            
        """
        return None

    @property
    def Attributes(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IAttributeCollection]:
        """
        
            Gets the attributes of the extension.
            
        """
        return None


class IExtensionManager(object):
    """
    
            Defines an extension manager.
            
    """

    @property
    def CurrentExtension(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtension]:
        """
        
            Gets the current extension.
            
        """
        return None

    @property
    def Extensions(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Common.IExtension]]:
        """
        
            Gets the list of loaded extensions.
            
        """
        return None


class ILog(object):
    """
    
            Defines log engine.
            
    """

    def WriteMessage(self, message: str) -> None:
        """
        
            Adds a new message entry into the log. 
            
        """
        pass

    def WriteWarning(self, message: str) -> None:
        """
        
            Adds a new warning message entry into the log. 
            
        """
        pass

    def WriteError(self, message: str) -> None:
        """
        
            Adds a new error message entry into the log.
            
        """
        pass


class IParameterManager(object):
    """
    
            Defines a parameter manager.
            
    """

    @property
    def Parameters(self) -> typing.Optional[System.Collections.ObjectModel.ReadOnlyCollection[Ansys.ACT.Interfaces.Common.IParameter]]:
        """
        
            Gets a collection of design parameters.
            
        """
        return None


class ISelectionInfo(object):
    """
    
            Defines a selection information.
            
    """

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets the selection identifier.
            
        """
        return None

    @property
    def Ids(self) -> typing.Optional[typing.List[int]]:
        """
        
            Gets or sets selected IDs.
            
        """
        return None

    @Ids.setter
    def Ids(self, value: typing.Optional[typing.List[int]]) -> None:
        """
        
            Gets or sets selected IDs.
            
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the selection name.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the selection name.
            
        """
        pass

    @property
    def SelectionType(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.SelectionTypeEnum]:
        """
        
            Gets or sets the selection type.
            
        """
        return None

    @SelectionType.setter
    def SelectionType(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.SelectionTypeEnum]) -> None:
        """
        
            Gets or sets the selection type.
            
        """
        pass


class ISelectionManager(object):
    """
    
            Defines a selection manager.
            
    """

    @property
    def CurrentSelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        
            Gets the current selection.
            
        """
        return None

    def AddSelection(self, info: Ansys.ACT.Interfaces.Common.ISelectionInfo) -> None:
        """
        
            Adds a new selection to the current selection.
            
        """
        pass

    def NewSelection(self, info: Ansys.ACT.Interfaces.Common.ISelectionInfo) -> None:
        """
        
            Creates a new selection.
            
        """
        pass

    def ClearSelection(self) -> None:
        """
        
            Clears the current selection.
            
        """
        pass

    def CreateSelectionInfo(self, selectionType: Ansys.ACT.Interfaces.Common.SelectionTypeEnum) -> Ansys.ACT.Interfaces.Common.ISelectionInfo:
        """
        
            Creates a new selection information based on its type.
            
        """
        pass


class ITools(object):
    """
    
            Defines common tools.
            
    """

    def GetResultsDataFromFile(self, filename: str) -> Ansys.ACT.Interfaces.Post.IResultReader:
        """
        
            Returns the result reader object associated to the file name specified.
            
        """
        pass

    def GetMeshDataFromFile(self, filename: str, bodyGrouping: str) -> Ansys.ACT.Interfaces.Mesh.IMeshData:
        """
        
            Returns the mesh data model associated to the file name specified.
            
        """
        pass

    def GetGeoDataFromFile(self, filename: str) -> Ansys.ACT.Interfaces.Geometry.IGeoData:
        """
        
            Returns the geo data model object for the CAD file name specified.
            
        """
        pass


class MechanicalUnitSystem(object):
    """
    
            Contains all possible mechanical unit systems (standard and consistent).
            The standard unit systems are used in the mechanical UI. (From the toolbar menu "Unit"). Be aware that the standard unit systems are NOT consistent.
            The consistent unit systems are mostly used in the solver.
            
    """

    @property
    def IsConsistent(self) -> typing.Optional[bool]:
        """
        IsConsistent property.
        """
        return None

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass

    def GetConsistentUnitSystem(self) -> Ansys.ACT.Interfaces.Common.MechanicalUnitSystem:
        """
        
            Gets the consistent unit system (i.e. solver unit system.)
            
        """
        pass

    def Equals(self, mechanicalUnitSystemType: Ansys.ACT.Interfaces.Common.MechanicalUnitSystemEnum) -> bool:
        """
        
            Specifies whether this instance of MechanicalUnitSystem is equal to the given MechanicalUnitSystemEnum value.
            
        """
        pass

    def GetMechanicalUnitSystemType(self) -> Ansys.ACT.Interfaces.Common.MechanicalUnitSystemEnum:
        """
        
            Get the MechanicalUnitSystemEnum for this MechanicalUnitSystem
            
        """
        pass


class UserErrorMessageException(object):
    """
    
            Defines a user exception used to send error message to the end user.
            
    """

    @property
    def Message(self) -> typing.Optional[str]:
        """
        Message property.
        """
        return None

    @property
    def Data(self) -> typing.Optional[System.Collections.IDictionary]:
        """
        Data property.
        """
        return None

    @property
    def InnerException(self) -> typing.Optional[System.Exception]:
        """
        InnerException property.
        """
        return None

    @property
    def TargetSite(self) -> typing.Optional[System.Reflection.MethodBase]:
        """
        TargetSite property.
        """
        return None

    @property
    def StackTrace(self) -> typing.Optional[str]:
        """
        StackTrace property.
        """
        return None

    @property
    def HelpLink(self) -> typing.Optional[str]:
        """
        HelpLink property.
        """
        return None

    @HelpLink.setter
    def HelpLink(self, value: typing.Optional[str]) -> None:
        """
        HelpLink property.
        """
        pass

    @property
    def Source(self) -> typing.Optional[str]:
        """
        Source property.
        """
        return None

    @Source.setter
    def Source(self, value: typing.Optional[str]) -> None:
        """
        Source property.
        """
        pass

    @property
    def HResult(self) -> typing.Optional[int]:
        """
        HResult property.
        """
        return None

    def __init__(self, msg: str) -> None:
        """
        __init__ method.
        """
        pass

    def GetBaseException(self) -> System.Exception:
        """
        GetBaseException method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetType(self) -> type:
        """
        GetType method.
        """
        pass


class IBreakpoint(object):
    """
    
            A stop point in the source file of a code.
            
    """

    @property
    def Line(self) -> typing.Optional[int]:
        """
        
            The line number on which the breakpoint is.
            
        """
        return None

    @property
    def SourceFile(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISourceFile]:
        """
        
            The file to which the breakpoint is attached.
            
        """
        return None

    @property
    def IsEnabled(self) -> typing.Optional[bool]:
        """
        
            Specifies whether the breakpoint is enabled or not.
            
        """
        return None

    @IsEnabled.setter
    def IsEnabled(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether the breakpoint is enabled or not.
            
        """
        pass

    def add_EnabledChanged(self, value: System.EventHandler) -> None:
        """
        add_EnabledChanged method.
        """
        pass

    def remove_EnabledChanged(self, value: System.EventHandler) -> None:
        """
        remove_EnabledChanged method.
        """
        pass


