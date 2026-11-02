"""Mechanical module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class MechanicalPanelEnum(Enum):
    """
    
            Specifies the panel type.
            
    """

    DataView = 0
    Worksheet = 1
    TabularData = 2
    Graph = 3
    Outline = 4
    Graphics = 5
    Wizard = 6

class IMechanicalGraphics(object):
    """
    
            Interface for MechanicalGraphics.
            
    """

    @property
    def ModelViewManager(self) -> typing.Optional[Ansys.ACT.Interfaces.Graphics.IModelViewManager]:
        """
        
            An instance of the ModelViewManager.
            
        """
        return None

    @property
    def KeyframeAnimationUtility(self) -> typing.Optional[Ansys.ACT.Common.Graphics.KeyframeAnimationUtility]:
        """
        KeyframeAnimationUtility property.
        """
        return None

    @property
    def SectionPlanes(self) -> typing.Optional[Ansys.Mechanical.Graphics.SectionPlanes]:
        """
        
            An instance of the SectionPlanes.
            
        """
        return None


class IMechanicalSelectionInfo(object):
    """
    
            Defines the mechanical selection information.
            
    """

    @property
    def Entities(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Geometry.IGeoEntity]]:
        """
        
            Gets the list of selected geometry entities.
            
        """
        return None

    @property
    def ElementFaceIndices(self) -> typing.Optional[typing.List[int]]:
        """
        
            Gets the list indices needed to define the face of an element.
            
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        Id property.
        """
        return None

    @property
    def Ids(self) -> typing.Optional[typing.List[int]]:
        """
        Ids property.
        """
        return None

    @Ids.setter
    def Ids(self, value: typing.Optional[typing.List[int]]) -> None:
        """
        Ids property.
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Name property.
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        Name property.
        """
        pass

    @property
    def SelectionType(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.SelectionTypeEnum]:
        """
        SelectionType property.
        """
        return None

    @SelectionType.setter
    def SelectionType(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.SelectionTypeEnum]) -> None:
        """
        SelectionType property.
        """
        pass


class IMechanicalDataModel(object):
    """
    
            Defines the data model of the Mechanical application.
            
    """

    @property
    def Project(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Project]:
        """
        
            Gets the project object. Main object of the tree of Mechanical.
            
        """
        return None

    @property
    def Tree(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Tree]:
        """
        
            Gets the tree of Mechanical.
            
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[Ansys.Mechanical.Application.ObjectTags]:
        """
        
            Gets the ObjectTags object for the Data Model, which represents the current list of tags visable in the User Interface. 
            
        """
        return None

    @property
    def AnalysisNames(self) -> typing.Optional[typing.List[str]]:
        """
        AnalysisNames property.
        """
        return None

    @property
    def AnalysisList(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Analysis.IAnalysis]]:
        """
        AnalysisList property.
        """
        return None

    @property
    def ObjectType(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectTypeEnum]:
        """
        ObjectType property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def SupportedLocations(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        SupportedLocations property.
        """
        return None

    @property
    def GeoData(self) -> typing.Optional[Ansys.ACT.Interfaces.Geometry.IGeoData]:
        """
        GeoData property.
        """
        return None

    @property
    def MeshDataNames(self) -> typing.Optional[typing.List[str]]:
        """
        MeshDataNames property.
        """
        return None

    def CurrentUnitFromQuantityName(self, quantityName: str) -> str:
        """
        
            Returns the current unit from a quantity name.
            
        """
        pass

    def GetUserObjectById(self, id: int) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        """
         Gets the user object based on the application id.
        """
        pass

    def AnalysisByName(self, name: str) -> Ansys.ACT.Interfaces.Analysis.IAnalysis:
        """
        AnalysisByName method.
        """
        pass

    def AnalysisById(self, id: int) -> Ansys.ACT.Interfaces.Analysis.IAnalysis:
        """
        AnalysisById method.
        """
        pass

    def CurrentConsistentUnitFromQuantityName(self, quantityName: str) -> str:
        """
        CurrentConsistentUnitFromQuantityName method.
        """
        pass

    def MeshDataByName(self, name: str) -> Ansys.ACT.Interfaces.Mesh.IMeshData:
        """
        MeshDataByName method.
        """
        pass

    def GetObjectById(self, id: int) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        GetObjectById method.
        """
        pass

    def GetObjectsByName(self, name: str) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GetObjectsByName method.
        """
        pass

    def GetObjectsByType(self, type: type) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GetObjectsByType method.
        """
        pass

    def GetUserObjects(self, extNameOrGUID: str) -> typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]:
        """
        GetUserObjects method.
        """
        pass


class IMechanicalExtAPI(object):
    """
    
            Exposes the main entry point of all ATC APIs.
            
    """

    @property
    def UsesStandaloneResultReaderImplementation(self) -> typing.Optional[bool]:
        """
        
            Gets or sets a value indicating which implementation to use when post processing results.
            
        """
        return None

    @UsesStandaloneResultReaderImplementation.setter
    def UsesStandaloneResultReaderImplementation(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets a value indicating which implementation to use when post processing results.
            
        """
        pass

    @property
    def UsesStandaloneActResultReaderImplementation(self) -> typing.Optional[bool]:
        """
        
            Gets or sets a value indicating which implementation to use when post processing results.
            
        """
        return None

    @UsesStandaloneActResultReaderImplementation.setter
    def UsesStandaloneActResultReaderImplementation(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets a value indicating which implementation to use when post processing results.
            
        """
        pass

    @property
    def ActResultReaderUsingMeshDataFromRst(self) -> typing.Optional[bool]:
        """
        
            Gets or sets a value indicating whether the mesh data are read inside the .rst file or not.
            
        """
        return None

    @ActResultReaderUsingMeshDataFromRst.setter
    def ActResultReaderUsingMeshDataFromRst(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets a value indicating whether the mesh data are read inside the .rst file or not.
            
        """
        pass

    @property
    def ResultReaderConnectionType(self) -> typing.Optional[str]:
        """
        
            Gets or sets the type of connection to use for the ACT Result Reader : "PIPE" or "TCP"
            
        """
        return None

    @ResultReaderConnectionType.setter
    def ResultReaderConnectionType(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the type of connection to use for the ACT Result Reader : "PIPE" or "TCP"
            
        """
        pass

    @property
    def ResultReaderPort(self) -> typing.Optional[int]:
        """
        
            Gets or sets the port used for the connection to the result reader
            
        """
        return None

    @ResultReaderPort.setter
    def ResultReaderPort(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the port used for the connection to the result reader
            
        """
        pass

    @property
    def ResultReaderAllowsMultiServers(self) -> typing.Optional[bool]:
        """
        
            If true then allow to create many readers by result file else create only one reader by result file.
            
        """
        return None

    @ResultReaderAllowsMultiServers.setter
    def ResultReaderAllowsMultiServers(self, value: typing.Optional[bool]) -> None:
        """
        
            If true then allow to create many readers by result file else create only one reader by result file.
            
        """
        pass

    @property
    def GraphicsAddin(self) -> typing.Optional[Ansys.Mechanical.Graphics.MechanicalGraphicsAddin]:
        """
        
            Gets the Mechanical Graphics Addin instance for providing custom graphics
            
        """
        return None

    @property
    def Application(self) -> typing.Optional[Ansys.ACT.Interfaces.Mechanical.IMechanicalApplication]:
        """
        Application property.
        """
        return None

    @property
    def Tools(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ITools]:
        """
        Tools property.
        """
        return None

    @property
    def SelectionManager(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionManager]:
        """
        SelectionManager property.
        """
        return None

    @property
    def Log(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ILog]:
        """
        Log property.
        """
        return None

    @property
    def ExtensionManager(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtensionManager]:
        """
        ExtensionManager property.
        """
        return None

    @property
    def ExtensionMgr(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtensionManager]:
        """
        ExtensionMgr property.
        """
        return None

    @property
    def UserInterface(self) -> typing.Optional[Ansys.ACT.Interfaces.UserInterface.IUserInterface]:
        """
        UserInterface property.
        """
        return None

    @property
    def Context(self) -> typing.Optional[str]:
        """
        Context property.
        """
        return None

    @property
    def DataModel(self) -> typing.Optional[Ansys.ACT.Mechanical.MechanicalDataModel]:
        """
        DataModel property.
        """
        return None

    @property
    def Graphics(self) -> typing.Optional[Ansys.ACT.Common.Graphics.MechanicalGraphicsWrapper]:
        """
        Graphics property.
        """
        return None

    def UnlockPrePostLicense(self) -> None:
        """
        R
            Unlocks the license used by the PRE/POST application. This is required if you want to manually launch the Ansys solver.
            You must relock the license after its use. If you don't relock the license, the PRE/POST application will be in read-only mode.
            
        """
        pass

    def LockPrePostLicense(self) -> None:
        """
        
            Locks the license used by the PRE/POST application.
            
        """
        pass

    def CloseResultReader(self, filename: str) -> None:
        """
        
            Close the result readers for a given result file
            
        """
        pass

    def ExecuteCommand(self, cmd: str, args: System.Collections.Generic.Dictionary[str,typing.Any], vars: str) -> System.Collections.Generic.Dictionary[str,typing.Any]:
        """
        ExecuteCommand method.
        """
        pass


class IMechanicalUserLoad(object):
    """
    
            Defines a Mechanical user load.
            
    """

    @property
    def ObjectType(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectTypeEnum]:
        """
        ObjectType property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def SupportedLocations(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        SupportedLocations property.
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        Id property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Name property.
        """
        return None

    @property
    def Version(self) -> typing.Optional[int]:
        """
        Version property.
        """
        return None

    @property
    def State(self) -> typing.Optional[str]:
        """
        State property.
        """
        return None

    @property
    def Caption(self) -> typing.Optional[str]:
        """
        Caption property.
        """
        return None

    @property
    def InternalCaption(self) -> typing.Optional[str]:
        """
        InternalCaption property.
        """
        return None

    @property
    def Icon(self) -> typing.Optional[str]:
        """
        Icon property.
        """
        return None

    @property
    def Extension(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtension]:
        """
        Extension property.
        """
        return None

    @property
    def Controller(self) -> typing.Optional[typing.Any]:
        """
        Controller property.
        """
        return None

    @property
    def Attributes(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IAttributeCollection]:
        """
        Attributes property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.IPropertyCollection]:
        """
        Properties property.
        """
        return None

    @property
    def AllProperties(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.ISimProperty]]:
        """
        AllProperties property.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]]:
        """
        Children property.
        """
        return None

    @property
    def Analysis(self) -> typing.Optional[Ansys.ACT.Interfaces.Analysis.IAnalysis]:
        """
        
            Gets the associated analysis.
            
        """
        return None

    @property
    def Color(self) -> typing.Optional[int]:
        """
        Color property.
        """
        return None

    @Color.setter
    def Color(self, value: typing.Optional[int]) -> None:
        """
        Color property.
        """
        pass

    @property
    def IsLoad(self) -> typing.Optional[bool]:
        """
        IsLoad property.
        """
        return None

    @property
    def AffectsSolution(self) -> typing.Optional[bool]:
        """
        AffectsSolution property.
        """
        return None

    @property
    def IsSupport(self) -> typing.Optional[bool]:
        """
        IsSupport property.
        """
        return None

    @property
    def Suppressed(self) -> typing.Optional[bool]:
        """
        Suppressed property.
        """
        return None

    @Suppressed.setter
    def Suppressed(self, value: typing.Optional[bool]) -> None:
        """
        Suppressed property.
        """
        pass

    def SetCoordinateSystem(self, system: Ansys.ACT.Interfaces.Analysis.ICoordinateSystem) -> None:
        """
        SetCoordinateSystem method.
        """
        pass

    def Import(self) -> None:
        """
        Import method.
        """
        pass

    def NotifyChange(self) -> None:
        """
        NotifyChange method.
        """
        pass

    def SetDefaultSelection(self, selection: Ansys.ACT.Interfaces.Common.ISelectionInfo, notifyChange: bool) -> None:
        """
        
            Sets the default selection of the entity.
            
        """
        pass

    def CreateChild(self, name: str) -> Ansys.ACT.Interfaces.UserObject.IUserLoad:
        """
        CreateChild method.
        """
        pass


class IMechanicalUserObject(object):
    """
    
            Defines a Mechanical user object.
            
    """

    @property
    def Analysis(self) -> typing.Optional[Ansys.ACT.Interfaces.Analysis.IAnalysis]:
        """
        
            Gets the associated analysis.
            
        """
        return None

    @property
    def ObjectType(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectTypeEnum]:
        """
        ObjectType property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def SupportedLocations(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        SupportedLocations property.
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        Id property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Name property.
        """
        return None

    @property
    def Version(self) -> typing.Optional[int]:
        """
        Version property.
        """
        return None

    @property
    def State(self) -> typing.Optional[str]:
        """
        State property.
        """
        return None

    @property
    def Caption(self) -> typing.Optional[str]:
        """
        Caption property.
        """
        return None

    @property
    def InternalCaption(self) -> typing.Optional[str]:
        """
        InternalCaption property.
        """
        return None

    @property
    def Icon(self) -> typing.Optional[str]:
        """
        Icon property.
        """
        return None

    @property
    def Extension(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtension]:
        """
        Extension property.
        """
        return None

    @property
    def Controller(self) -> typing.Optional[typing.Any]:
        """
        Controller property.
        """
        return None

    @property
    def Attributes(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IAttributeCollection]:
        """
        Attributes property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.IPropertyCollection]:
        """
        Properties property.
        """
        return None

    @property
    def AllProperties(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.ISimProperty]]:
        """
        AllProperties property.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]]:
        """
        Children property.
        """
        return None

    def SetDefaultSelection(self, selection: Ansys.ACT.Interfaces.Common.ISelectionInfo, notifyChange: bool) -> None:
        """
        
            Sets the default selection of the entity.
            
        """
        pass

    def NotifyChange(self) -> None:
        """
        NotifyChange method.
        """
        pass


class IMechanicalUserResult(object):
    """
    
            Defines a Mechanical user result.
            
    """

    @property
    def ObjectType(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectTypeEnum]:
        """
        ObjectType property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def SupportedLocations(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        SupportedLocations property.
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        Id property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Name property.
        """
        return None

    @property
    def Version(self) -> typing.Optional[int]:
        """
        Version property.
        """
        return None

    @property
    def State(self) -> typing.Optional[str]:
        """
        State property.
        """
        return None

    @property
    def Caption(self) -> typing.Optional[str]:
        """
        Caption property.
        """
        return None

    @property
    def InternalCaption(self) -> typing.Optional[str]:
        """
        InternalCaption property.
        """
        return None

    @property
    def Icon(self) -> typing.Optional[str]:
        """
        Icon property.
        """
        return None

    @property
    def Extension(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtension]:
        """
        Extension property.
        """
        return None

    @property
    def Controller(self) -> typing.Optional[typing.Any]:
        """
        Controller property.
        """
        return None

    @property
    def Attributes(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IAttributeCollection]:
        """
        Attributes property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.IPropertyCollection]:
        """
        Properties property.
        """
        return None

    @property
    def AllProperties(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.ISimProperty]]:
        """
        AllProperties property.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]]:
        """
        Children property.
        """
        return None

    @property
    def Analysis(self) -> typing.Optional[Ansys.ACT.Interfaces.Analysis.IAnalysis]:
        """
        
            Gets the associated analysis.
            
        """
        return None

    @property
    def ResultLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Post.ResultLocationEnum]:
        """
        ResultLocation property.
        """
        return None

    @ResultLocation.setter
    def ResultLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Post.ResultLocationEnum]) -> None:
        """
        ResultLocation property.
        """
        pass

    @property
    def ResultType(self) -> typing.Optional[Ansys.ACT.Interfaces.Post.ResultTypeEnum]:
        """
        ResultType property.
        """
        return None

    @ResultType.setter
    def ResultType(self, value: typing.Optional[Ansys.ACT.Interfaces.Post.ResultTypeEnum]) -> None:
        """
        ResultType property.
        """
        pass

    @property
    def ResultAveraging(self) -> typing.Optional[Ansys.ACT.Interfaces.Post.ResultAveragingEnum]:
        """
        ResultAveraging property.
        """
        return None

    @ResultAveraging.setter
    def ResultAveraging(self, value: typing.Optional[Ansys.ACT.Interfaces.Post.ResultAveragingEnum]) -> None:
        """
        ResultAveraging property.
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        Unit property.
        """
        return None

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        """
        Unit property.
        """
        pass

    @property
    def HasImaginary(self) -> typing.Optional[bool]:
        """
        HasImaginary property.
        """
        return None

    @HasImaginary.setter
    def HasImaginary(self, value: typing.Optional[bool]) -> None:
        """
        HasImaginary property.
        """
        pass

    @property
    def CalculateTimeHistory(self) -> typing.Optional[bool]:
        """
        CalculateTimeHistory property.
        """
        return None

    @CalculateTimeHistory.setter
    def CalculateTimeHistory(self, value: typing.Optional[bool]) -> None:
        """
        CalculateTimeHistory property.
        """
        pass

    @property
    def Suppressed(self) -> typing.Optional[bool]:
        """
        Suppressed property.
        """
        return None

    @Suppressed.setter
    def Suppressed(self, value: typing.Optional[bool]) -> None:
        """
        Suppressed property.
        """
        pass

    def NotifyChange(self) -> None:
        """
        NotifyChange method.
        """
        pass

    def SetDefaultSelection(self, selection: Ansys.ACT.Interfaces.Common.ISelectionInfo, notifyChange: bool) -> None:
        """
        
            Sets the default selection of the entity.
            
        """
        pass


class IMechanicalUserSolver(object):
    """
    
            Defines a Mechanical user solver.
            
    """

    @property
    def ObjectType(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectTypeEnum]:
        """
        ObjectType property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def SupportedLocations(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        SupportedLocations property.
        """
        return None

    @property
    def Id(self) -> typing.Optional[int]:
        """
        Id property.
        """
        return None

    @property
    def Name(self) -> typing.Optional[str]:
        """
        Name property.
        """
        return None

    @property
    def Version(self) -> typing.Optional[int]:
        """
        Version property.
        """
        return None

    @property
    def State(self) -> typing.Optional[str]:
        """
        State property.
        """
        return None

    @property
    def Caption(self) -> typing.Optional[str]:
        """
        Caption property.
        """
        return None

    @property
    def InternalCaption(self) -> typing.Optional[str]:
        """
        InternalCaption property.
        """
        return None

    @property
    def Icon(self) -> typing.Optional[str]:
        """
        Icon property.
        """
        return None

    @property
    def Extension(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IExtension]:
        """
        Extension property.
        """
        return None

    @property
    def Controller(self) -> typing.Optional[typing.Any]:
        """
        Controller property.
        """
        return None

    @property
    def Attributes(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IAttributeCollection]:
        """
        Attributes property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.IPropertyCollection]:
        """
        Properties property.
        """
        return None

    @property
    def AllProperties(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.ISimProperty]]:
        """
        AllProperties property.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]]:
        """
        Children property.
        """
        return None

    @property
    def Analysis(self) -> typing.Optional[Ansys.ACT.Interfaces.Analysis.IAnalysis]:
        """
        
            Gets the associated analysis.
            
        """
        return None

    @property
    def AnalysisType(self) -> typing.Optional[str]:
        """
        AnalysisType property.
        """
        return None

    @property
    def PhysicsType(self) -> typing.Optional[str]:
        """
        PhysicsType property.
        """
        return None

    def NotifyChange(self) -> None:
        """
        NotifyChange method.
        """
        pass

    def SetDefaultSelection(self, selection: Ansys.ACT.Interfaces.Common.ISelectionInfo, notifyChange: bool) -> None:
        """
        
            Sets the default selection of the entity.
            
        """
        pass


