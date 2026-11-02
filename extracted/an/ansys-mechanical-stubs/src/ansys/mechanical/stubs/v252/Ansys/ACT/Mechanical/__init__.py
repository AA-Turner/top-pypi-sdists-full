"""Mechanical module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v252.Ansys.ACT.Mechanical.AdditionalProperties as AdditionalProperties
import ansys.mechanical.stubs.v252.Ansys.ACT.Mechanical.Utilities as Utilities
import ansys.mechanical.stubs.v252.Ansys.ACT.Mechanical.Fields as Fields
import ansys.mechanical.stubs.v252.Ansys.ACT.Mechanical.Application as Application


class Transaction(object):
    """
    
            Speeds up bulk user interactions.
            
    """

    def __init__(self, suspendClicks: bool, suspendStateEngine: bool) -> None:
        """
        
            
             
        """
        pass

    def Dispose(self) -> None:
        pass

    def ForceClickOnUnsuspend(self) -> None:
        """
        ForceClickOnUnsuspend method.
        """
        pass


class UnitsHelper(object):
    """
    
            Defines set of methods that can be used to find mechanical unit information
            
    """

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    @classmethod
    def RegisterConvertionFunction(cls, fct: typing.Callable[str,str,str]) -> None:
        """
        RegisterConvertionFunction method.
        """
        pass

    @classmethod
    def ConvertMechanicalUnitToCoreUnit(cls, mechanicalUnit: str, unitCategory: str) -> str:
        """
        
            Takes input mechanical unit string and category string
            And returns framework unit string which can be used for conversion
            
        """
        pass

    @classmethod
    def GetCurrentCompactUnitString(cls, quantityName: str) -> str:
        """
        
            Return a compact unit string for the supplied field.
            for example, on an acceleration object acc (in MKS and NMM, respectively):
            -  acc.Magnitude.Output.Unit ==> 'm sec^-1 sec^-1' , 'm sec^-1 sec^-1'
            -  GetCurrentCompactUnitString(ExtAPI, acc.Magnitude.Output.QuantityName) ==> 'm/s²' , 'mm/s²'
            
        """
        pass

    @classmethod
    def GetValidQuantityNamesAndUnits(cls) -> dict[str,str]:
        """
        
            Retrieve a dictionary of quantity names to unit strings.
            These quantity names represent valid quantity names that can be used when defining quantities in 
            Mechanical ACT extensions.        
            
        """
        pass

    @classmethod
    def GetQuantityNameBasedOnUnitCategoryType(cls, unitCategory: Ansys.Mechanical.DataModel.Enums.UnitCategoryType) -> str:
        """
        GetQuantityNameBasedOnUnitCategoryType method.
        """
        pass


class MechanicalDataModel(object):

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        InternalObject property.
        """
        return None

    @property
    def Project(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Project]:
        """
        Project property.
        """
        return None

    @property
    def MeshDataNames(self) -> typing.Optional[typing.List[str]]:
        """
        MeshDataNames property.
        """
        return None

    @property
    def GeoData(self) -> typing.Optional[Ansys.ACT.Interfaces.Geometry.IGeoData]:
        """
        GeoData property.
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
    def EngineeringData(self) -> typing.Optional[typing.Any]:
        """
        EngineeringData property.
        """
        return None

    @property
    def Components(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Mechanical.IMechanicalSelectionInfo]]:
        """
        Components property.
        """
        return None

    @property
    def CoordinateSystems(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Interfaces.Analysis.ICoordinateSystem]]:
        """
        CoordinateSystems property.
        """
        return None

    @property
    def WorkingDir(self) -> typing.Optional[str]:
        """
        WorkingDir property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[Ansys.Mechanical.Application.ObjectTags]:
        """
        ObjectTags property.
        """
        return None

    @property
    def InternalDataObjects(self) -> typing.Optional[typing.List[typing.Any]]:
        """
        InternalDataObjects property.
        """
        return None

    @property
    def ObjectLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.UserObject.ObjectLocationEnum]:
        """
        ObjectLocation property.
        """
        return None

    @property
    def DataModelObject(self) -> typing.Optional[Ansys.ACT.Interfaces.DataModel.IDataModelObject]:
        """
        DataModelObject property.
        """
        return None

    @property
    def ObjectIdentifier(self) -> typing.Optional[Ansys.ACT.Core.Application.Model.ObjectIdentifier]:
        """
        ObjectIdentifier property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.ACT.Core.Application.Model.IApplicationObject]:
        """
        Parent property.
        """
        return None

    @property
    def Tree(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Tree]:
        """
        Tree property.
        """
        return None

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

    @typing.overload
    def GetObjectsByType(self, type: type) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    @typing.overload
    def GetObjectsByType(self, dataModelObjectCategory: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetObjectsByType(self, *args: typing.Any) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GetObjectsByType method.
        """
        pass

    def GetUserObjectById(self, id: int) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        """
        GetUserObjectById method.
        """
        pass

    def CreateObjectCommand(self, userObject: Ansys.ACT.Interfaces.UserObject.IUserObject) -> Ansys.Common.Interop.DSWBApplet.IDSAppCommand:
        """
        CreateObjectCommand method.
        """
        pass

    @typing.overload
    def CreateObject(self, objName: str) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        ...

    @typing.overload
    def CreateObject(self, objName: str, extNameOrGUID: str) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        ...

    @typing.overload
    def CreateObject(self, objName: str, ext: Ansys.ACT.Interfaces.Common.IExtension) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        ...

    def CreateObject(self, *args: typing.Any) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        """
        CreateObject method.
        """
        pass

    def CreateChild(self, objName: str, ext: Ansys.ACT.Interfaces.Common.IExtension, parentObj: typing.Any) -> Ansys.ACT.Interfaces.UserObject.IUserObject:
        """
        CreateChild method.
        """
        pass

    @typing.overload
    def GetUserObjects(self, ext: Ansys.ACT.Interfaces.Common.IExtension) -> typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]:
        ...

    @typing.overload
    def GetUserObjects(self, extNameOrGUID: str) -> typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]:
        ...

    def GetUserObjects(self, *args: typing.Any) -> typing.Iterable[Ansys.ACT.Interfaces.UserObject.IUserObject]:
        """
        GetUserObjects method.
        """
        pass

    def MeshDataByName(self, name: str) -> Ansys.ACT.Interfaces.Mesh.IMeshData:
        """
        MeshDataByName method.
        """
        pass

    def AnalysisByName(self, name: str) -> Ansys.ACT.Interfaces.Analysis.IAnalysis:
        """
        AnalysisByName method.
        """
        pass

    def AnalysisById(self, id: int) -> Ansys.ACT.Interfaces.Analysis.IAnalysis:
        """
        
            See  for general information about this method.
            
        """
        pass

    def CurrentUnitFromQuantityName(self, quantityName: str) -> str:
        """
        CurrentUnitFromQuantityName method.
        """
        pass

    def CurrentConsistentUnitFromQuantityName(self, quantityName: str) -> str:
        """
        CurrentConsistentUnitFromQuantityName method.
        """
        pass

    def ShouldSuspendStateEngineForDelete(self) -> bool:
        """
        ShouldSuspendStateEngineForDelete method.
        """
        pass

    def Suppress(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        Suppress method.
        """
        pass

    def Unsuppress(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        Unsuppress method.
        """
        pass

    @typing.overload
    def Remove(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        ...

    @typing.overload
    def Remove(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject], forceRemove: bool) -> None:
        ...

    @typing.overload
    def Remove(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        ...

    @typing.overload
    def Remove(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject, forceRemove: bool) -> None:
        ...

    def Remove(self, *args: typing.Any) -> None:
        """
        Remove method.
        """
        pass

    def Delete(self, objsToDelete: Ansys.Common.Interop.AnsCoreObjects.AnsVARIANTColl) -> bool:
        """
        Delete method.
        """
        pass

    def ComponentById(self, id: int) -> Ansys.ACT.Interfaces.Mechanical.IMechanicalSelectionInfo:
        """
        ComponentById method.
        """
        pass

    def CoordinateSystemById(self, id: int) -> Ansys.ACT.Interfaces.Analysis.ICoordinateSystem:
        """
        CoordinateSystemById method.
        """
        pass

    def GetSessionVariableValue(self, varName: str) -> str:
        """
        GetSessionVariableValue method.
        """
        pass

    def AddSessionVariable(self, varName: str, value: str) -> None:
        """
        AddSessionVariable method.
        """
        pass

    def DeleteSessionVariable(self, varName: str) -> None:
        """
        DeleteSessionVariable method.
        """
        pass

    def DummyNodeRemoveAndFillObjects(self, classId: Ansys.Common.Interop.DSObjectTypes.DSClsId) -> None:
        """
        DummyNodeRemoveAndFillObjects method.
        """
        pass

    def RecomputeState(self) -> None:
        """
        
            Recomputes the states of the data model objects. Best used with data model changes made during callbacks in Python Code or Extensions.
            
        """
        pass

    def AreEqual(self, other: Ansys.ACT.Core.Application.Model.IApplicationObject) -> bool:
        """
        AreEqual method.
        """
        pass

    def CleanUp(self) -> None:
        """
        CleanUp method.
        """
        pass

    def InitializeLifetimeService(self) -> typing.Any:
        """
        InitializeLifetimeService method.
        """
        pass

    def CreateObjRef(self, requestedType: type) -> System.Runtime.Remoting.ObjRef:
        """
        CreateObjRef method.
        """
        pass

    def GetLifetimeService(self) -> typing.Any:
        """
        GetLifetimeService method.
        """
        pass


