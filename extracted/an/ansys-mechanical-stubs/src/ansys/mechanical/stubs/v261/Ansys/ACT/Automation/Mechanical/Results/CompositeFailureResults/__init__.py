"""CompositeFailureResults module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CompositeFailureCriteria(object):
    """
    Defines a CompositeFailureCriteria.
    """

    @property
    def MaximumStrain(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.MaximumStrainSettings]:
        """
        Gets the configuration of the maximum strain criterion for reinforced materials.
        """
        return None

    @property
    def MaximumStress(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.MaximumStressSettings]:
        """
        Gets the configuration of the maximum stress criterion for reinforced materials.
        """
        return None

    @property
    def TsaiWu(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.TsaiWuSettings]:
        """
        Gets the configuration of the Tsai-Wu failure criterion for reinforced materials.
        """
        return None

    @property
    def TsaiHill(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.TsaiHillSettings]:
        """
        Gets the configuration of the Tsai-Hill failure criterion for reinforced materials.
        """
        return None

    @property
    def Hoffman(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.HoffmanSettings]:
        """
        Gets the configuration of the Hoffman failure criterion for reinforced materials.
        """
        return None

    @property
    def Hashin(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.HashinSettings]:
        """
        Gets the configuration of the Hashin failure criterion for reinforced materials.
        """
        return None

    @property
    def Puck(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.PuckSettings]:
        """
        Gets the configuration of the Puck failure criterion for reinforced materials.
        """
        return None

    @property
    def LaRC(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.LaRCSettings]:
        """
        Gets the configuration of the LaRC (Langley Research Center) failure criterion for reinforced materials.
        """
        return None

    @property
    def Cuntze(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CuntzeSettings]:
        """
        Gets the configuration of the Cuntze failure criterion for reinforced materials.
        """
        return None

    @property
    def FaceSheetWrinkling(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.FaceSheetWrinklingSettings]:
        """
        Gets the configuration of the Face Sheet Wrinkling sandwich failure criterion.
        """
        return None

    @property
    def CoreFailure(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CoreFailureSettings]:
        """
        Gets the configuration of the Core Failure sandwich failure criterion
        """
        return None

    @property
    def ShearCrimping(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.ShearCrimpingSettings]:
        """
        Gets the configuration of the Shear Crimping sandwich failure criterion
        """
        return None

    @property
    def VonMises(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.VonMisesSettings]:
        """
        Gets the configuration of the Von Mises failure criterion for isotropic materials.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets the list of children.
        """
        return None

    @property
    def Comments(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Comment]]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Figure]]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        ObjectId property.
        """
        return None

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
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        ObjectTags property.
        """
        return None

    @property
    def IconName(self) -> typing.Optional[str]:
        """
        IconName property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ClsId(self) -> typing.Optional[int]:
        """
        ClsId property.
        """
        return None

    @property
    def AttachedRefs(self) -> typing.Optional[typing.List[int]]:
        """
        AttachedRefs property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    @property
    def State(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Legacy.State]:
        """
        State property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @typing.overload
    def __init__(self, internalObject: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    @typing.overload
    def GetChildren(self, recurses: bool, children: typing.List[ChildrenType]) -> typing.List[ChildrenType]:
        ...

    @typing.overload
    def GetChildren(self, category: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory, recurses: bool, children: typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetChildren(self, *args: typing.Any) -> typing.List[ChildrenType] | typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the list of children, filtered by type.
        """
        pass

    def AddComment(self) -> Ansys.ACT.Automation.Mechanical.Comment:
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> Ansys.ACT.Automation.Mechanical.Figure:
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: str) -> Ansys.ACT.Automation.Mechanical.Image:
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetPath(self) -> str:
        """
        GetPath method.
        """
        pass

    def GetIconFile(self) -> System.Byte:
        """
        GetIconFile method.
        """
        pass

    def Activate(self) -> None:
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def GetDetailsView(self) -> Ansys.ACT.Automation.Mechanical.DetailsViewData:
        """
        GetDetailsView method.
        """
        pass

    def Duplicate(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> None:
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def GetPropertyName(self, dispId: int) -> str:
        """
        GetPropertyName method.
        """
        pass

    def GetPropertyValue(self, name: str) -> typing.Any:
        """
        GetPropertyValue method.
        """
        pass

    @typing.overload
    def IsPropertyVisible(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyVisible(self, propName: str) -> bool:
        ...

    def IsPropertyVisible(self, *args: typing.Any) -> bool:
        """
        IsPropertyVisible method.
        """
        pass

    @typing.overload
    def IsPropertyEditable(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyEditable(self, propName: str) -> bool:
        ...

    def IsPropertyEditable(self, *args: typing.Any) -> bool:
        """
        IsPropertyEditable method.
        """
        pass

    def GetVisiblePropertyNames(self) -> typing.List[str]:
        """
        GetVisiblePropertyNames method.
        """
        pass

    def GetVisibleProperties(self) -> typing.List[System.Reflection.PropertyInfo]:
        """
        GetVisibleProperties method.
        """
        pass

    def GetAllProperties(self) -> typing.List[Ansys.ACT.Automation.Mechanical.AutomationPropertyWrapper]:
        """
        GetAllProperties method.
        """
        pass

    def PropertyByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def PropertyById(self, dispId: int) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        PropertyById method.
        """
        pass

    def CreateParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Creates a new parameter for a Property.
            
        """
        pass

    def GetParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: str) -> None:
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass

    def GetAPIName(self, dispId: int) -> str:
        """
        
            Property name bound to dispId.
            
        """
        pass

    def GetEnumName(self, enumType: type, value: int, dispId: int) -> str:
        """
        
            Enum name bound to value
            
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


class CompositeFailureCriterionSettings(object):
    """
    Base class for settings objects which contain the configuration of a single failure criterion.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class CompositeFailureTool(object):
    """
    Defines a CompositeFailureTool.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureToolAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets the list of children.
        """
        return None

    @property
    def Comments(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Comment]]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Figure]]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        ObjectId property.
        """
        return None

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
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        ObjectTags property.
        """
        return None

    @property
    def IconName(self) -> typing.Optional[str]:
        """
        IconName property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ClsId(self) -> typing.Optional[int]:
        """
        ClsId property.
        """
        return None

    @property
    def AttachedRefs(self) -> typing.Optional[typing.List[int]]:
        """
        AttachedRefs property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    @property
    def State(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Legacy.State]:
        """
        State property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @typing.overload
    def __init__(self, internalObject: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def AddInverseReserveFactor(self) -> Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CompositeFailureResult:
        """
        Creates a new InverseReserveFactor
        """
        pass

    def AddSafetyFactor(self) -> Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CompositeFailureResult:
        """
        Creates a new SafetyFactor
        """
        pass

    def AddSafetyMargin(self) -> Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CompositeFailureResult:
        """
        Creates a new SafetyMargin
        """
        pass

    def EvaluateAllResults(self) -> None:
        """
        Run the EvaluateAllResults action.
        """
        pass

    def AddGroupedScopedACPResults(self, resultType: Ansys.Mechanical.DataModel.Enums.ResultType, selectedPlies: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        AddGroupedScopedACPResults method.
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    @typing.overload
    def GetChildren(self, recurses: bool, children: typing.List[ChildrenType]) -> typing.List[ChildrenType]:
        ...

    @typing.overload
    def GetChildren(self, category: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory, recurses: bool, children: typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetChildren(self, *args: typing.Any) -> typing.List[ChildrenType] | typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the list of children, filtered by type.
        """
        pass

    def AddComment(self) -> Ansys.ACT.Automation.Mechanical.Comment:
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> Ansys.ACT.Automation.Mechanical.Figure:
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: str) -> Ansys.ACT.Automation.Mechanical.Image:
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetPath(self) -> str:
        """
        GetPath method.
        """
        pass

    def GetIconFile(self) -> System.Byte:
        """
        GetIconFile method.
        """
        pass

    def Activate(self) -> None:
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def GetDetailsView(self) -> Ansys.ACT.Automation.Mechanical.DetailsViewData:
        """
        GetDetailsView method.
        """
        pass

    def Duplicate(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> None:
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def GetPropertyName(self, dispId: int) -> str:
        """
        GetPropertyName method.
        """
        pass

    def GetPropertyValue(self, name: str) -> typing.Any:
        """
        GetPropertyValue method.
        """
        pass

    @typing.overload
    def IsPropertyVisible(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyVisible(self, propName: str) -> bool:
        ...

    def IsPropertyVisible(self, *args: typing.Any) -> bool:
        """
        IsPropertyVisible method.
        """
        pass

    @typing.overload
    def IsPropertyEditable(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyEditable(self, propName: str) -> bool:
        ...

    def IsPropertyEditable(self, *args: typing.Any) -> bool:
        """
        IsPropertyEditable method.
        """
        pass

    def GetVisiblePropertyNames(self) -> typing.List[str]:
        """
        GetVisiblePropertyNames method.
        """
        pass

    def GetVisibleProperties(self) -> typing.List[System.Reflection.PropertyInfo]:
        """
        GetVisibleProperties method.
        """
        pass

    def GetAllProperties(self) -> typing.List[Ansys.ACT.Automation.Mechanical.AutomationPropertyWrapper]:
        """
        GetAllProperties method.
        """
        pass

    def PropertyByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def PropertyById(self, dispId: int) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        PropertyById method.
        """
        pass

    def CreateParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Creates a new parameter for a Property.
            
        """
        pass

    def GetParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: str) -> None:
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass

    def GetAPIName(self, dispId: int) -> str:
        """
        
            Property name bound to dispId.
            
        """
        pass

    def GetEnumName(self, enumType: type, value: int, dispId: int) -> str:
        """
        
            Enum name bound to value
            
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


class CoreFailureSettings(object):
    """
    Defines the configuration for the Core failure criterion for sandwich structures.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the core failure criterion. The corresponding failure label
            is 'cf'.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the core failure criterion. The corresponding failure label
            is 'cf'.
        """
        pass

    @property
    def ConsiderInterlaminarNormalStresses(self) -> typing.Optional[bool]:
        """
        Gets or sets whether interlaminar normal stresses are included in the core failure evaluation.
        """
        return None

    @ConsiderInterlaminarNormalStresses.setter
    def ConsiderInterlaminarNormalStresses(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether interlaminar normal stresses are included in the core failure evaluation.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class CuntzeSettings(object):
    """
    Defines the configuration for the Cuntze failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def FailureDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @FailureDimension.setter
    def FailureDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def EvaluateFiberTensionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber tension failure is evaluated. The corresponding failure label is 'cft'
        """
        return None

    @EvaluateFiberTensionFailure.setter
    def EvaluateFiberTensionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber tension failure is evaluated. The corresponding failure label is 'cft'
        """
        pass

    @property
    def FiberTensionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber tension failure (cft) evaluation.
        """
        return None

    @FiberTensionFailureWeightingFactor.setter
    def FiberTensionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber tension failure (cft) evaluation.
        """
        pass

    @property
    def EvaluateFiberCompressionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber compression failure is evaluated. The corresponding failure label is 'cfc'
        """
        return None

    @EvaluateFiberCompressionFailure.setter
    def EvaluateFiberCompressionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber compression failure is evaluated. The corresponding failure label is 'cfc'
        """
        pass

    @property
    def FiberCompressionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber compression failure (cfc) evaluation.
        """
        return None

    @FiberCompressionFailureWeightingFactor.setter
    def FiberCompressionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber compression failure (cfc) evaluation.
        """
        pass

    @property
    def EvaluateMatrixTensionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'cmA'
        """
        return None

    @EvaluateMatrixTensionFailure.setter
    def EvaluateMatrixTensionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'cmA'
        """
        pass

    @property
    def MatrixTensionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix tension failure (cmA) evaluation.
        """
        return None

    @MatrixTensionFailureWeightingFactor.setter
    def MatrixTensionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix tension failure (cmA) evaluation.
        """
        pass

    @property
    def EvaluateMatrixCompressionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'cmB'
        """
        return None

    @EvaluateMatrixCompressionFailure.setter
    def EvaluateMatrixCompressionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'cmB'
        """
        pass

    @property
    def MatrixCompressionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix compression failure (cmB) evaluation.
        """
        return None

    @MatrixCompressionFailureWeightingFactor.setter
    def MatrixCompressionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix compression failure (cmB) evaluation.
        """
        pass

    @property
    def EvaluateMatrixWedgeShapeFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix wedge shape failure is evaluated. The corresponding failure label is 'cmC'
        """
        return None

    @EvaluateMatrixWedgeShapeFailure.setter
    def EvaluateMatrixWedgeShapeFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix wedge shape failure is evaluated. The corresponding failure label is 'cmC'
        """
        pass

    @property
    def MatrixWedgeShapeFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix wedge shape failure (cmC) evaluation.
        """
        return None

    @MatrixWedgeShapeFailureWeightingFactor.setter
    def MatrixWedgeShapeFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix wedge shape failure (cmC) evaluation.
        """
        pass

    @property
    def ModeInteractionCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the mode interaction coefficient.
        """
        return None

    @ModeInteractionCoefficient.setter
    def ModeInteractionCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the mode interaction coefficient.
        """
        pass

    @property
    def InPlaneShearFrictionCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the in-plane shear friction coefficient b21.
            The value must be greater than or equal to 0.
        """
        return None

    @InPlaneShearFrictionCoefficient.setter
    def InPlaneShearFrictionCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the in-plane shear friction coefficient b21.
            The value must be greater than or equal to 0.
        """
        pass

    @property
    def OutOfPlaneShearFrictionCoefficient(self) -> typing.Optional[float]:
        """
        Gets the out-of-plane shear friction coefficient b32.
            Computed from the fracture plane angle theta.
        """
        return None

    @property
    def FracturePlaneAngle(self) -> typing.Optional[float]:
        """
        Gets or sets the fracture plane angle theta.
            The value must be in the range [45, 90).
        """
        return None

    @FracturePlaneAngle.setter
    def FracturePlaneAngle(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the fracture plane angle theta.
            The value must be in the range [45, 90).
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class FaceSheetWrinklingSettings(object):
    """
    Defines the configuration for the Face Sheet Wrinkling failure criterion for sandwich structures.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the face sheet wrinkling criterion. The corresponding failure
            label is 'wt' for wrinkling at the top face, 'wb' at the bottom face.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the face sheet wrinkling criterion. The corresponding failure
            label is 'wt' for wrinkling at the top face, 'wb' at the bottom face.
        """
        pass

    @property
    def HomogeneousCoreCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the wrinkling coefficient of homogeneous core materials.
        """
        return None

    @HomogeneousCoreCoefficient.setter
    def HomogeneousCoreCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the wrinkling coefficient of homogeneous core materials.
        """
        pass

    @property
    def HoneycombCoreCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the wrinkling coefficient of honeycomb core materials.
        """
        return None

    @HoneycombCoreCoefficient.setter
    def HoneycombCoreCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the wrinkling coefficient of honeycomb core materials.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class HashinSettings(object):
    """
    Defines the configuration for the Hashin failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def FailureDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @FailureDimension.setter
    def FailureDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def EvaluateFiberFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber failure is evaluated. The corresponding failure label is 'hf'
        """
        return None

    @EvaluateFiberFailure.setter
    def EvaluateFiberFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber failure is evaluated. The corresponding failure label is 'hf'
        """
        pass

    @property
    def FiberFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber failure evaluation.
        """
        return None

    @FiberFailureWeightingFactor.setter
    def FiberFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber failure evaluation.
        """
        pass

    @property
    def EvaluateMatrixFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix failure is evaluated. The corresponding failure label is 'hm'
        """
        return None

    @EvaluateMatrixFailure.setter
    def EvaluateMatrixFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix failure is evaluated. The corresponding failure label is 'hm'
        """
        pass

    @property
    def MatrixFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix failure evaluation.
        """
        return None

    @MatrixFailureWeightingFactor.setter
    def MatrixFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix failure evaluation.
        """
        pass

    @property
    def EvaluateDelamination(self) -> typing.Optional[bool]:
        """
        Gets or sets whether delamination is evaluated. Only applies when three-dimensional
            evaluation is selected. The corresponding failure label is 'hd'
        """
        return None

    @EvaluateDelamination.setter
    def EvaluateDelamination(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether delamination is evaluated. Only applies when three-dimensional
            evaluation is selected. The corresponding failure label is 'hd'
        """
        pass

    @property
    def DelaminationWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the delamination evaluation.
        """
        return None

    @DelaminationWeightingFactor.setter
    def DelaminationWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the delamination evaluation.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class HoffmanSettings(object):
    """
    Defines the configuration for the Hoffman failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def FailureDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @FailureDimension.setter
    def FailureDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'ho'.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'ho'.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class LaRCSettings(object):
    """
    Defines the configuration for the LaRC failure criterion for reinforced materials
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def Formulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.LaRCFormulation]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @Formulation.setter
    def Formulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.LaRCFormulation]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def EvaluateFiberTensionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber tension failure is evaluated. The corresponding failure label is 'ltf3'.
        """
        return None

    @EvaluateFiberTensionFailure.setter
    def EvaluateFiberTensionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber tension failure is evaluated. The corresponding failure label is 'ltf3'.
        """
        pass

    @property
    def FiberTensionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber tension failure (ltf3) evaluation.
        """
        return None

    @FiberTensionFailureWeightingFactor.setter
    def FiberTensionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber tension failure (ltf3) evaluation.
        """
        pass

    @property
    def EvaluateFiberCompressionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber compression failure is evaluated. The corresponding failure label is 'lfc4/6'.
        """
        return None

    @EvaluateFiberCompressionFailure.setter
    def EvaluateFiberCompressionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber compression failure is evaluated. The corresponding failure label is 'lfc4/6'.
        """
        pass

    @property
    def FiberCompressionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber compression failure (lfc4/6) evaluation.
        """
        return None

    @FiberCompressionFailureWeightingFactor.setter
    def FiberCompressionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber compression failure (lfc4/6) evaluation.
        """
        pass

    @property
    def EvaluateMatrixTensionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'lmt1'.
        """
        return None

    @EvaluateMatrixTensionFailure.setter
    def EvaluateMatrixTensionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'lmt1'.
        """
        pass

    @property
    def MatrixTensionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix tension failure (lmt1) evaluation.
        """
        return None

    @MatrixTensionFailureWeightingFactor.setter
    def MatrixTensionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix tension failure (lmt1) evaluation.
        """
        pass

    @property
    def EvaluateMatrixCompressionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'lmc2/5'.
        """
        return None

    @EvaluateMatrixCompressionFailure.setter
    def EvaluateMatrixCompressionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'lmc2/5'.
        """
        pass

    @property
    def MatrixCompressionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix compression failure (lmc2/5) evaluation.
        """
        return None

    @MatrixCompressionFailureWeightingFactor.setter
    def MatrixCompressionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix compression failure (lmc2/5) evaluation.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class MaximumStrainSettings(object):
    """
    Defines the configuration for the Maximum Strain failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def EvaluateMaterialOneDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the material 1
            direction. The corresponding failure label is 'e1'.
        """
        return None

    @EvaluateMaterialOneDirectionFailure.setter
    def EvaluateMaterialOneDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the material 1
            direction. The corresponding failure label is 'e1'.
        """
        pass

    @property
    def MaterialOneDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the material 1 direction. 
        """
        return None

    @MaterialOneDirectionFailureWeightingFactor.setter
    def MaterialOneDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the material 1 direction. 
        """
        pass

    @property
    def EvaluateMaterialTwoDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the material 2
            direction. The corresponding failure label is 'e2'.
        """
        return None

    @EvaluateMaterialTwoDirectionFailure.setter
    def EvaluateMaterialTwoDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the material 2
            direction. The corresponding failure label is 'e2'.
        """
        pass

    @property
    def MaterialTwoDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the material 2 direction. 
        """
        return None

    @MaterialTwoDirectionFailureWeightingFactor.setter
    def MaterialTwoDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the material 2 direction. 
        """
        pass

    @property
    def EvaluateMaterialThreeDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the out-of-plane
            direction. The corresponding failure label is 'e3'.
        """
        return None

    @EvaluateMaterialThreeDirectionFailure.setter
    def EvaluateMaterialThreeDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the out-of-plane
            direction. The corresponding failure label is 'e3'.
        """
        pass

    @property
    def MaterialThreeDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the out-of-plane direction. 
        """
        return None

    @MaterialThreeDirectionFailureWeightingFactor.setter
    def MaterialThreeDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the out-of-plane direction. 
        """
        pass

    @property
    def EvaluateShearOneTwoFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the in-plane shear e12. The corresponding failure
            label is 'e12'.
        """
        return None

    @EvaluateShearOneTwoFailure.setter
    def EvaluateShearOneTwoFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the in-plane shear e12. The corresponding failure
            label is 'e12'.
        """
        pass

    @property
    def ShearOneTwoFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to in-plane shear e12.
        """
        return None

    @ShearOneTwoFailureWeightingFactor.setter
    def ShearOneTwoFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to in-plane shear e12.
        """
        pass

    @property
    def EvaluateShearOneThreeFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear e13. The corresponding failure
            label is 'e13'.
        """
        return None

    @EvaluateShearOneThreeFailure.setter
    def EvaluateShearOneThreeFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear e13. The corresponding failure
            label is 'e13'.
        """
        pass

    @property
    def ShearOneThreeFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear e13.
        """
        return None

    @ShearOneThreeFailureWeightingFactor.setter
    def ShearOneThreeFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear e13.
        """
        pass

    @property
    def EvaluateShearTwoThreeFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear e23. The corresponding failure
            label is 'e23'.
        """
        return None

    @EvaluateShearTwoThreeFailure.setter
    def EvaluateShearTwoThreeFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear e23. The corresponding failure
            label is 'e23'.
        """
        pass

    @property
    def ShearTwoThreeFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear e23.
        """
        return None

    @ShearTwoThreeFailureWeightingFactor.setter
    def ShearTwoThreeFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear e23.
        """
        pass

    @property
    def OverrideMaterial(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the global strain limits are used, overriding material-specific limits.
        """
        return None

    @OverrideMaterial.setter
    def OverrideMaterial(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the global strain limits are used, overriding material-specific limits.
        """
        pass

    @property
    def TensileLimitMaterialOneDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global tensile strain limit in the material 1 direction (eXt).
            Only used if OverrideMaterial is true.
        """
        return None

    @TensileLimitMaterialOneDirection.setter
    def TensileLimitMaterialOneDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global tensile strain limit in the material 1 direction (eXt).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def CompressiveLimitMaterialOneDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global compressive strain limit in the material 1 direction (eXc).
            Only used if OverrideMaterial is true.
        """
        return None

    @CompressiveLimitMaterialOneDirection.setter
    def CompressiveLimitMaterialOneDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global compressive strain limit in the material 1 direction (eXc).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def TensileLimitMaterialTwoDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global tensile strain limit in the material 2 direction (eYt).
            Only used if OverrideMaterial is true.
        """
        return None

    @TensileLimitMaterialTwoDirection.setter
    def TensileLimitMaterialTwoDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global tensile strain limit in the material 2 direction (eYt).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def CompressiveLimitMaterialTwoDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global compressive strain limit in the material 2 direction (eYc).
            Only used if OverrideMaterial is true.
        """
        return None

    @CompressiveLimitMaterialTwoDirection.setter
    def CompressiveLimitMaterialTwoDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global compressive strain limit in the material 2 direction (eYc).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def TensileLimitMaterialThreeDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global tensile strain limit in the out-of-plane direction (eZt).
            Only used if OverrideMaterial is true.
        """
        return None

    @TensileLimitMaterialThreeDirection.setter
    def TensileLimitMaterialThreeDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global tensile strain limit in the out-of-plane direction (eZt).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def CompressiveLimitMaterialThreeDirection(self) -> typing.Optional[float]:
        """
        Gets or sets the global compressive strain limit in the out-of-plane direction (eZc).
            Only used if OverrideMaterial is true.
        """
        return None

    @CompressiveLimitMaterialThreeDirection.setter
    def CompressiveLimitMaterialThreeDirection(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global compressive strain limit in the out-of-plane direction (eZc).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def ShearLimitOneTwo(self) -> typing.Optional[float]:
        """
        Gets or sets the global in-plane shear strain limit (eSxy).
            Only used if OverrideMaterial is true.
        """
        return None

    @ShearLimitOneTwo.setter
    def ShearLimitOneTwo(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global in-plane shear strain limit (eSxy).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def ShearLimitOneThree(self) -> typing.Optional[float]:
        """
        Gets or sets the global out-of-plane shear strain limit (eSxz).
            Only used if OverrideMaterial is true.
        """
        return None

    @ShearLimitOneThree.setter
    def ShearLimitOneThree(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global out-of-plane shear strain limit (eSxz).
            Only used if OverrideMaterial is true.
        """
        pass

    @property
    def ShearLimitTwoThree(self) -> typing.Optional[float]:
        """
        Gets or sets the global out-of-plane shear strain limit (eSyz).
            Only used if OverrideMaterial is true.
        """
        return None

    @ShearLimitTwoThree.setter
    def ShearLimitTwoThree(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the global out-of-plane shear strain limit (eSyz).
            Only used if OverrideMaterial is true.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class MaximumStressSettings(object):
    """
    Defines the configuration for the Maximum Stress failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def EvaluateMaterialOneDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the material 1 direction.
            The corresponding failure label is 's1'.
        """
        return None

    @EvaluateMaterialOneDirectionFailure.setter
    def EvaluateMaterialOneDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the material 1 direction.
            The corresponding failure label is 's1'.
        """
        pass

    @property
    def MaterialOneDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the material 1 direction.
        """
        return None

    @MaterialOneDirectionFailureWeightingFactor.setter
    def MaterialOneDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the material 1 direction.
        """
        pass

    @property
    def EvaluateMaterialTwoDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the material 2 direction.
            The corresponding failure label is 's2'.
        """
        return None

    @EvaluateMaterialTwoDirectionFailure.setter
    def EvaluateMaterialTwoDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the material 2 direction.
            The corresponding failure label is 's2'.
        """
        pass

    @property
    def MaterialTwoDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the material 2 direction.
        """
        return None

    @MaterialTwoDirectionFailureWeightingFactor.setter
    def MaterialTwoDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the material 2 direction.
        """
        pass

    @property
    def EvaluateMaterialThreeDirectionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the failure criterion is evaluated in the out-of-plane direction.
            The corresponding failure label is 's3'.
        """
        return None

    @EvaluateMaterialThreeDirectionFailure.setter
    def EvaluateMaterialThreeDirectionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated in the out-of-plane direction.
            The corresponding failure label is 's3'.
        """
        pass

    @property
    def MaterialThreeDirectionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion in the out-of-plane direction.
        """
        return None

    @MaterialThreeDirectionFailureWeightingFactor.setter
    def MaterialThreeDirectionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion in the out-of-plane direction.
        """
        pass

    @property
    def EvaluateShearOneTwoFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the in-plane shear s12.
            The corresponding failure label is 's12'.
        """
        return None

    @EvaluateShearOneTwoFailure.setter
    def EvaluateShearOneTwoFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the in-plane shear s12.
            The corresponding failure label is 's12'.
        """
        pass

    @property
    def ShearOneTwoFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to in-plane shear s12.
        """
        return None

    @ShearOneTwoFailureWeightingFactor.setter
    def ShearOneTwoFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to in-plane shear s12.
        """
        pass

    @property
    def EvaluateShearOneThreeFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear s13.
            The corresponding failure label is 's13'.
        """
        return None

    @EvaluateShearOneThreeFailure.setter
    def EvaluateShearOneThreeFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear s13.
            The corresponding failure label is 's13'.
        """
        pass

    @property
    def ShearOneThreeFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear s13.
        """
        return None

    @ShearOneThreeFailureWeightingFactor.setter
    def ShearOneThreeFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear s13.
        """
        pass

    @property
    def EvaluateShearTwoThreeFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear s23.
            The corresponding failure label is 's23'.
        """
        return None

    @EvaluateShearTwoThreeFailure.setter
    def EvaluateShearTwoThreeFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether failure is evaluated for the out-of-plane shear s23.
            The corresponding failure label is 's23'.
        """
        pass

    @property
    def ShearTwoThreeFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear s23.
        """
        return None

    @ShearTwoThreeFailureWeightingFactor.setter
    def ShearTwoThreeFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for failure due to out-of-plane shear s23.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class PuckSettings(object):
    """
    Defines the configuration for the Puck failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def Formulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.PuckFormulation]:
        """
        Gets or sets whether the simplified, 2D, or 3D Puck formulation is used.
        """
        return None

    @Formulation.setter
    def Formulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.PuckFormulation]) -> None:
        """
        Gets or sets whether the simplified, 2D, or 3D Puck formulation is used.
        """
        pass

    @property
    def ConsiderInterFiberParallelStresses(self) -> typing.Optional[bool]:
        """
        Gets or sets whether inter-fiber failure will include the influence of the fiber parallel stresses.
        """
        return None

    @ConsiderInterFiberParallelStresses.setter
    def ConsiderInterFiberParallelStresses(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether inter-fiber failure will include the influence of the fiber parallel stresses.
        """
        pass

    @property
    def EvaluateFiberFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether fiber failure (pf) is evaluated. The corresponding failure label is 'pf'.
        """
        return None

    @EvaluateFiberFailure.setter
    def EvaluateFiberFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether fiber failure (pf) is evaluated. The corresponding failure label is 'pf'.
        """
        pass

    @property
    def FiberFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the fiber failure evaluation.
        """
        return None

    @FiberFailureWeightingFactor.setter
    def FiberFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the fiber failure evaluation.
        """
        pass

    @property
    def EvaluateMatrixTensionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'pmA'.
        """
        return None

    @EvaluateMatrixTensionFailure.setter
    def EvaluateMatrixTensionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix tension failure is evaluated. The corresponding failure label is 'pmA'.
        """
        pass

    @property
    def MatrixTensionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix tension (pmA) failure evaluation.
        """
        return None

    @MatrixTensionFailureWeightingFactor.setter
    def MatrixTensionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix tension (pmA) failure evaluation.
        """
        pass

    @property
    def EvaluateMatrixCompressionFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'pmB'.
        """
        return None

    @EvaluateMatrixCompressionFailure.setter
    def EvaluateMatrixCompressionFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix compression failure is evaluated. The corresponding failure label is 'pmB'.
        """
        pass

    @property
    def MatrixCompressionFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix compression (pmB) failure evaluation.
        """
        return None

    @MatrixCompressionFailureWeightingFactor.setter
    def MatrixCompressionFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix compression (pmB) failure evaluation.
        """
        pass

    @property
    def EvaluateMatrixShearFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether matrix shear failure is evaluated. The corresponding failure label is 'pmC'.
        """
        return None

    @EvaluateMatrixShearFailure.setter
    def EvaluateMatrixShearFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether matrix shear failure is evaluated. The corresponding failure label is 'pmC'.
        """
        pass

    @property
    def MatrixShearFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the matrix shear (pmC) failure evaluation.
        """
        return None

    @MatrixShearFailureWeightingFactor.setter
    def MatrixShearFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the matrix shear (pmC) failure evaluation.
        """
        pass

    @property
    def EvaluateDelamination(self) -> typing.Optional[bool]:
        """
        Gets or sets whether delamination is evaluated. Only applies when three-dimensional
            evaluation is selected. The corresponding failure label is 'pd'.
        """
        return None

    @EvaluateDelamination.setter
    def EvaluateDelamination(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether delamination is evaluated. Only applies when three-dimensional
            evaluation is selected. The corresponding failure label is 'pd'.
        """
        pass

    @property
    def DelaminationWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the delamination (pd) evaluation.
        """
        return None

    @DelaminationWeightingFactor.setter
    def DelaminationWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the delamination (pd) evaluation.
        """
        pass

    @property
    def OverrideMaterial(self) -> typing.Optional[bool]:
        """
        Gets or sets whether the global Puck constants are used overriding material-specific constants.
        """
        return None

    @OverrideMaterial.setter
    def OverrideMaterial(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether the global Puck constants are used overriding material-specific constants.
        """
        pass

    @property
    def InclinationFactorTwoOnePositive(self) -> typing.Optional[float]:
        """
        Gets or sets the p21(+) Puck constant.
        """
        return None

    @InclinationFactorTwoOnePositive.setter
    def InclinationFactorTwoOnePositive(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the p21(+) Puck constant.
        """
        pass

    @property
    def InclinationFactorTwoOneNegative(self) -> typing.Optional[float]:
        """
        Gets or sets the p21(-) Puck constant.
        """
        return None

    @InclinationFactorTwoOneNegative.setter
    def InclinationFactorTwoOneNegative(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the p21(-) Puck constant.
        """
        pass

    @property
    def InclinationFactorTwoTwoPositive(self) -> typing.Optional[float]:
        """
        Gets or sets the p22(+) Puck constant.
        """
        return None

    @InclinationFactorTwoTwoPositive.setter
    def InclinationFactorTwoTwoPositive(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the p22(+) Puck constant.
        """
        pass

    @property
    def InclinationFactorTwoTwoNegative(self) -> typing.Optional[float]:
        """
        Gets or sets the p22(-) Puck constant.
        """
        return None

    @InclinationFactorTwoTwoNegative.setter
    def InclinationFactorTwoTwoNegative(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the p22(-) Puck constant.
        """
        pass

    @property
    def DegradationInitiationFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the degradation initiation factor s (0 < s < 1).
        """
        return None

    @DegradationInitiationFactor.setter
    def DegradationInitiationFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the degradation initiation factor s (0 < s < 1).
        """
        pass

    @property
    def DegradationResidualStrengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the degradation residual strength factor M (0 < M < 1).
        """
        return None

    @DegradationResidualStrengthFactor.setter
    def DegradationResidualStrengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the degradation residual strength factor M (0 < M < 1).
        """
        pass

    @property
    def InterfaceWeakeningFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the interface weakening factor.
        """
        return None

    @InterfaceWeakeningFactor.setter
    def InterfaceWeakeningFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the interface weakening factor.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class ShearCrimpingSettings(object):
    """
    Defines the configuration for the Face Sheet Crimping failure criterion for sandwich structures.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for shear crimping failure.
            The corresponding failure label is 'sc'.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for shear crimping failure.
            The corresponding failure label is 'sc'.
        """
        pass

    @property
    def CoreWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor of core material of crimping allowable.
        """
        return None

    @CoreWeightingFactor.setter
    def CoreWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor of core material of crimping allowable.
        """
        pass

    @property
    def FaceSheetWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor of face sheets of crimping allowable.
        """
        return None

    @FaceSheetWeightingFactor.setter
    def FaceSheetWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor of face sheets of crimping allowable.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class TsaiHillSettings(object):
    """
    Defines the configuration for the Tsai-Hill failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def FailureDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @FailureDimension.setter
    def FailureDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'th'.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'th'.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class TsaiWuSettings(object):
    """
    Defines the configuration for the Tsai-Wu failure criterion for reinforced materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def FailureDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        return None

    @FailureDimension.setter
    def FailureDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.CompositeFailure.FailureDimension]) -> None:
        """
        Gets or sets whether the failure criterion is evaluated only in-plane (2D),
            or also in the out-of-plane direction (3D).
        """
        pass

    @property
    def WeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'tw'.
        """
        return None

    @WeightingFactor.setter
    def WeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the failure criterion.
            The corresponding failure label is 'tw'.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class VonMisesSettings(object):
    """
    Defines the configuration for the Von Mises failure criterion for isotropic materials.
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Active property.
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        Active property.
        """
        pass

    @property
    def EvaluateStrainFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether strain failure is evaluated. The corresponding failure label is 'vMe'.
        """
        return None

    @EvaluateStrainFailure.setter
    def EvaluateStrainFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether strain failure is evaluated. The corresponding failure label is 'vMe'.
        """
        pass

    @property
    def StrainFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the strain failure (vMe) evaluation.
        """
        return None

    @StrainFailureWeightingFactor.setter
    def StrainFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the strain failure (vMe) evaluation.
        """
        pass

    @property
    def EvaluateStressFailure(self) -> typing.Optional[bool]:
        """
        Gets or sets whether stress failure is evaluated. The corresponding failure label is 'vMs'
        """
        return None

    @EvaluateStressFailure.setter
    def EvaluateStressFailure(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether stress failure is evaluated. The corresponding failure label is 'vMs'
        """
        pass

    @property
    def StressFailureWeightingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the weighting factor for the stress failure (vMs) evaluation.
        """
        return None

    @StressFailureWeightingFactor.setter
    def StressFailureWeightingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the weighting factor for the stress failure (vMs) evaluation.
        """
        pass

    @property
    def ConsiderInterlaminarNormalStresses(self) -> typing.Optional[bool]:
        """
        Gets or sets whether interlaminar normal stresses are evaluated.
        """
        return None

    @ConsiderInterlaminarNormalStresses.setter
    def ConsiderInterlaminarNormalStresses(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets whether interlaminar normal stresses are evaluated.
        """
        pass

    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureCriteriaAuto) -> None:
        """
        __init__ method.
        """
        pass

    def Reset(self) -> None:
        """
        Resets the settings to their default values.
        """
        pass


class CompositeFailureResult(object):

    @property
    def Ply(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.AnalysisPly]]:
        """
        Gets or sets the Ply selection.
        """
        return None

    @Ply.setter
    def Ply(self, value: typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.AnalysisPly]]) -> None:
        """
        Gets or sets the Ply selection.
        """
        pass

    @property
    def ShowOnReferenceSurface(self) -> typing.Optional[bool]:
        """
        Gets or sets the Show On Reference Surface property.
        """
        return None

    @ShowOnReferenceSurface.setter
    def ShowOnReferenceSurface(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Show On Reference Surface property.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def ShowCriticalFailureMode(self) -> typing.Optional[bool]:
        """
        Controls whether to show the critical failure mode text plot in graphics. Default: true
        """
        return None

    @ShowCriticalFailureMode.setter
    def ShowCriticalFailureMode(self, value: typing.Optional[bool]) -> None:
        """
        Controls whether to show the critical failure mode text plot in graphics. Default: true
        """
        pass

    @property
    def ShowCriticalLayer(self) -> typing.Optional[bool]:
        """
        Controls whether to show the critical layer text plot in graphics. Default: false
        """
        return None

    @ShowCriticalLayer.setter
    def ShowCriticalLayer(self, value: typing.Optional[bool]) -> None:
        """
        Controls whether to show the critical layer text plot in graphics. Default: false
        """
        pass

    @property
    def ShowCriticalLoadCase(self) -> typing.Optional[bool]:
        """
        Controls whether to show the critical load case text plot in graphics. Only supported for Envelope Solution Combinations. Default: false
        """
        return None

    @ShowCriticalLoadCase.setter
    def ShowCriticalLoadCase(self, value: typing.Optional[bool]) -> None:
        """
        Controls whether to show the critical load case text plot in graphics. Only supported for Envelope Solution Combinations. Default: false
        """
        pass

    @property
    def CriticalTextVisualizationMode(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]:
        """
        Controls whether the Critical Text Visualization Threshold is defined automatically by the product or manually by the user. Default: 
        """
        return None

    @CriticalTextVisualizationMode.setter
    def CriticalTextVisualizationMode(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]) -> None:
        """
        Controls whether the Critical Text Visualization Threshold is defined automatically by the product or manually by the user. Default: 
        """
        pass

    @property
    def CriticalTextVisualizationThreshold(self) -> typing.Optional[float]:
        """
        Gets or sets the text plot threshold value when CriticalTextVisualizationMode is set to Manual. Text will not be displayed for elements with result values below the threshold for Inverse Reserve Factor results or result values exceeding the threshold for Safety factor and Safety Margin results.
        """
        return None

    @CriticalTextVisualizationThreshold.setter
    def CriticalTextVisualizationThreshold(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the text plot threshold value when CriticalTextVisualizationMode is set to Manual. Text will not be displayed for elements with result values below the threshold for Inverse Reserve Factor results or result values exceeding the threshold for Safety factor and Safety Margin results.
        """
        pass

    @property
    def PlotData(self) -> typing.Optional[Ansys.Mechanical.DataModel.Results.ResultDataTable]:
        """
        Gets the result table.
        """
        return None

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def Location(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Location.
        """
        return None

    @Location.setter
    def Location(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Location.
        """
        pass

    @property
    def TimeForMinimumOfMinimumValues(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Get the Time for the minimum of minimum values.
        """
        return None

    @property
    def TimeForMinimumOfMaximumValues(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Get the Time for the minimum of maximum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMinimumValues(self) -> typing.Optional[int]:
        """
        Get the Load Step for the minimum of minimum values.
        """
        return None

    @property
    def LoadStepForMinimumOfMaximumValues(self) -> typing.Optional[int]:
        """
        Get the Load Step for the minimum of maximum values.
        """
        return None

    @property
    def TimeForMaximumOfMinimumValues(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Get the Time for the maximum of minimum values.
        """
        return None

    @property
    def TimeForMaximumOfMaximumValues(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Get the Time for the maximum of maximum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMinimumValues(self) -> typing.Optional[int]:
        """
        Get the Load Step for the maximum of minimum values.
        """
        return None

    @property
    def LoadStepForMaximumOfMaximumValues(self) -> typing.Optional[int]:
        """
        Get the Load Step for the maximum of maximum values.
        """
        return None

    @property
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        
            Gets or sets the Coordinate System. 
            Accepts/Returns None for Solution Coordinate System in the general case (if applicable). 
            Accepts/Returns None for Fiber Coordinate System for a result that is sub scoped by ply.
            
        """
        pass

    @property
    def ResultType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultType]:
        """
        Gets or sets the ResultType.
        """
        return None

    @ResultType.setter
    def ResultType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultType]) -> None:
        """
        Gets or sets the ResultType.
        """
        pass

    @property
    def ScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the ScopingMethod.
        """
        return None

    @ScopingMethod.setter
    def ScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the ScopingMethod.
        """
        pass

    @property
    def SetNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the Set Number.
        """
        return None

    @SetNumber.setter
    def SetNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Set Number.
        """
        pass

    @property
    def CombinationNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        return None

    @CombinationNumber.setter
    def CombinationNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Combination Number for a Solution Combination result.
        """
        pass

    @property
    def SolutionCombinationDriver(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle]:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        return None

    @SolutionCombinationDriver.setter
    def SolutionCombinationDriver(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolutionCombinationDriverStyle]) -> None:
        """
        Gets or sets the SolutionCombinationDriver.
        """
        pass

    @property
    def SeparateDataByEntity(self) -> typing.Optional[bool]:
        """
        Gets or sets the SeparateDataByEntity.
        """
        return None

    @SeparateDataByEntity.setter
    def SeparateDataByEntity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SeparateDataByEntity.
        """
        pass

    @property
    def Path(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Path]:
        """
        Path property.
        """
        return None

    @Path.setter
    def Path(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Path]) -> None:
        """
        Path property.
        """
        pass

    @property
    def Surface(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Surface]:
        """
        Surface property.
        """
        return None

    @Surface.setter
    def Surface(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Surface]) -> None:
        """
        Surface property.
        """
        pass

    @property
    def SurfaceCoating(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.SurfaceCoating]:
        """
        SurfaceCoating property.
        """
        return None

    @SurfaceCoating.setter
    def SurfaceCoating(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.SurfaceCoating]) -> None:
        """
        SurfaceCoating property.
        """
        pass

    @property
    def NamedSelections(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets or sets the NamedSelections.
        """
        return None

    @NamedSelections.setter
    def NamedSelections(self, value: typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]) -> None:
        """
        Gets or sets the NamedSelections.
        """
        pass

    @property
    def RpmSetNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the RpmSetNumber.
        """
        return None

    @RpmSetNumber.setter
    def RpmSetNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the RpmSetNumber.
        """
        pass

    @property
    def RPMSelection(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RPM Selection value at which the results are evaluated.
        """
        return None

    @RPMSelection.setter
    def RPMSelection(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RPM Selection value at which the results are evaluated.
        """
        pass

    @property
    def WaterfallDisplayFilterBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WaterfallDisplayFilterBy]:
        """
        Gets or sets the Filer in Waterfall.
        """
        return None

    @WaterfallDisplayFilterBy.setter
    def WaterfallDisplayFilterBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WaterfallDisplayFilterBy]) -> None:
        """
        Gets or sets the Filer in Waterfall.
        """
        pass

    @property
    def WaterfallDisplayRpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RPM Selection.
        """
        return None

    @WaterfallDisplayRpmSelection.setter
    def WaterfallDisplayRpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RPM Selection.
        """
        pass

    @property
    def WaterfallDisplayOrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the Order Selection.
        """
        return None

    @WaterfallDisplayOrderSelection.setter
    def WaterfallDisplayOrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Order Selection.
        """
        pass

    @property
    def WaterfallDisplayFrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the Frequency Selection.
        """
        return None

    @WaterfallDisplayFrequencySelection.setter
    def WaterfallDisplayFrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Frequency Selection.
        """
        pass

    @property
    def WaterfallDisplayModeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the Mode Selection.
        """
        return None

    @WaterfallDisplayModeSelection.setter
    def WaterfallDisplayModeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Mode Selection.
        """
        pass

    @property
    def WaterfallDisplayTimeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the Time Selection.
        """
        return None

    @WaterfallDisplayTimeSelection.setter
    def WaterfallDisplayTimeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Time Selection.
        """
        pass

    @property
    def WaterfallDisplayMinRPM(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Display Min RPM.
        """
        return None

    @WaterfallDisplayMinRPM.setter
    def WaterfallDisplayMinRPM(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Display Min RPM.
        """
        pass

    @property
    def WaterfallDisplayMaxRPM(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Display Max RPM.
        """
        return None

    @WaterfallDisplayMaxRPM.setter
    def WaterfallDisplayMaxRPM(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Display Max RPM.
        """
        pass

    @property
    def WaterfallDisplayInterpolateData(self) -> typing.Optional[bool]:
        """
        Gets or sets the Interpolate Data Property.
        """
        return None

    @WaterfallDisplayInterpolateData.setter
    def WaterfallDisplayInterpolateData(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Interpolate Data Property.
        """
        pass

    @property
    def WaterfallDisplayScopeToOrderLines(self) -> typing.Optional[bool]:
        """
        Gets or sets the Scope to Order Lines Property.
        """
        return None

    @WaterfallDisplayScopeToOrderLines.setter
    def WaterfallDisplayScopeToOrderLines(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Scope to Order Lines Property.
        """
        pass

    @property
    def WaterfallDisplayLowerBand(self) -> typing.Optional[float]:
        """
        Gets or sets the Lower Band Value.
        """
        return None

    @WaterfallDisplayLowerBand.setter
    def WaterfallDisplayLowerBand(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Lower Band Value.
        """
        pass

    @property
    def WaterfallDisplayUpperBand(self) -> typing.Optional[float]:
        """
        Gets or sets the Upper Band Value.
        """
        return None

    @WaterfallDisplayUpperBand.setter
    def WaterfallDisplayUpperBand(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Upper Band Value.
        """
        pass

    @property
    def WaterfallDisplayXAxisMinimum(self) -> typing.Optional[float]:
        """
        Gets or sets the Minimum X-Axis Value.
        """
        return None

    @WaterfallDisplayXAxisMinimum.setter
    def WaterfallDisplayXAxisMinimum(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Minimum X-Axis Value.
        """
        pass

    @property
    def WaterfallDisplayXAxisMaximum(self) -> typing.Optional[float]:
        """
        Gets or sets the Maximum X-Axis Value.
        """
        return None

    @WaterfallDisplayXAxisMaximum.setter
    def WaterfallDisplayXAxisMaximum(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Maximum X-Axis Value.
        """
        pass

    @property
    def WaterfallDisplayYAxisMinimum(self) -> typing.Optional[float]:
        """
        Gets or sets the Minimum Y-Axis Value.
        """
        return None

    @WaterfallDisplayYAxisMinimum.setter
    def WaterfallDisplayYAxisMinimum(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Minimum Y-Axis Value.
        """
        pass

    @property
    def WaterfallDisplayYAxisMaximum(self) -> typing.Optional[float]:
        """
        Gets or sets the Maximum Y-Axis Value.
        """
        return None

    @WaterfallDisplayYAxisMaximum.setter
    def WaterfallDisplayYAxisMaximum(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Maximum Y-Axis Value.
        """
        pass

    @property
    def WaterfallShowTextOnMosaic(self) -> typing.Optional[bool]:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        return None

    @WaterfallShowTextOnMosaic.setter
    def WaterfallShowTextOnMosaic(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Waterfall Mosaic Text Property.
        """
        pass

    @property
    def Average(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Average.
        """
        return None

    @property
    def Total(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Total.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def CrackFrontNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the CrackFrontNumber.
        """
        return None

    @CrackFrontNumber.setter
    def CrackFrontNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CrackFrontNumber.
        """
        pass

    @property
    def GlobalIDs(self) -> typing.Optional[str]:
        """
        Gets or sets the GlobalIDs.
        """
        return None

    @GlobalIDs.setter
    def GlobalIDs(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GlobalIDs.
        """
        pass

    @property
    def Identifier(self) -> typing.Optional[str]:
        """
        Gets or sets the Identifier.
        """
        return None

    @Identifier.setter
    def Identifier(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Identifier.
        """
        pass

    @property
    def IterationNumber(self) -> typing.Optional[int]:
        """
        Gets the IterationNumber.
        """
        return None

    @property
    def LoadStep(self) -> typing.Optional[int]:
        """
        Gets the LoadStep.
        """
        return None

    @property
    def MaximumOccursOn(self) -> typing.Optional[str]:
        """
        Gets the MaximumOccursOn.
        """
        return None

    @property
    def MinimumOccursOn(self) -> typing.Optional[str]:
        """
        Gets the MinimumOccursOn.
        """
        return None

    @property
    def LoadStepNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the LoadStepNumber.
        """
        return None

    @LoadStepNumber.setter
    def LoadStepNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LoadStepNumber.
        """
        pass

    @property
    def SolverComponentIDs(self) -> typing.Optional[str]:
        """
        Gets or sets the SolverComponentIDs.
        """
        return None

    @SolverComponentIDs.setter
    def SolverComponentIDs(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the SolverComponentIDs.
        """
        pass

    @property
    def Substep(self) -> typing.Optional[int]:
        """
        Gets the Substep.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MaximumOfMaximumOverTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumOfMaximumOverTime.
        """
        return None

    @property
    def MaximumOfMinimumOverTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumOfMinimumOverTime.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def MinimumOfMaximumOverTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MinimumOfMaximumOverTime.
        """
        return None

    @property
    def MinimumOfMinimumOverTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MinimumOfMinimumOverTime.
        """
        return None

    @property
    def Time(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Time.
        """
        return None

    @property
    def DisplayTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DisplayTime.
        """
        return None

    @DisplayTime.setter
    def DisplayTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DisplayTime.
        """
        pass

    @property
    def GraphControlsXAxis(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis]:
        """
        Gets or sets the GraphControlsXAxis.
        """
        return None

    @GraphControlsXAxis.setter
    def GraphControlsXAxis(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphControlsXAxis]) -> None:
        """
        Gets or sets the GraphControlsXAxis.
        """
        pass

    @property
    def DisplayOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultAveragingType]:
        """
        Gets or sets the DisplayOption.
        """
        return None

    @DisplayOption.setter
    def DisplayOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultAveragingType]) -> None:
        """
        Gets or sets the DisplayOption.
        """
        pass

    @property
    def DpfEvaluation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DpfEvaluationType]:
        """
        Gets or sets the DpfEvaluation.
        """
        return None

    @DpfEvaluation.setter
    def DpfEvaluation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DpfEvaluationType]) -> None:
        """
        Gets or sets the DpfEvaluation.
        """
        pass

    @property
    def By(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SetDriverStyle]:
        """
        Gets or sets the By.
        """
        return None

    @By.setter
    def By(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SetDriverStyle]) -> None:
        """
        Gets or sets the By.
        """
        pass

    @property
    def ItemType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileItemType]:
        """
        Gets or sets the ItemType.
        """
        return None

    @ItemType.setter
    def ItemType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileItemType]) -> None:
        """
        Gets or sets the ItemType.
        """
        pass

    @property
    def CalculateTimeHistory(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateTimeHistory.
        """
        return None

    @CalculateTimeHistory.setter
    def CalculateTimeHistory(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateTimeHistory.
        """
        pass

    @property
    def Suppressed(self) -> typing.Optional[bool]:
        """
        Gets or sets the Suppressed.
        """
        return None

    @Suppressed.setter
    def Suppressed(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Suppressed.
        """
        pass

    @property
    def Children(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets the list of children.
        """
        return None

    @property
    def Comments(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Comment]]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Figure]]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        ObjectId property.
        """
        return None

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
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        ObjectTags property.
        """
        return None

    @property
    def IconName(self) -> typing.Optional[str]:
        """
        IconName property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ClsId(self) -> typing.Optional[int]:
        """
        ClsId property.
        """
        return None

    @property
    def AttachedRefs(self) -> typing.Optional[typing.List[int]]:
        """
        AttachedRefs property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    @property
    def State(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Legacy.State]:
        """
        State property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @typing.overload
    def __init__(self, internalObject: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
        """
        pass

    def EvaluateAllResults(self) -> None:
        """
        Run the EvaluateAllResults action.
        """
        pass

    def FetchRemoteResult(self) -> None:
        """
        Run the FetchRemoteResult action.
        """
        pass

    def FetchRemoteResults(self) -> None:
        """
        Run the FetchRemoteResult action.
        """
        pass

    @typing.overload
    def ExportToTextFile(self, bIgnoreExcelPreference: bool, filePath: str) -> None:
        ...

    @typing.overload
    def ExportToTextFile(self, filePath: str) -> None:
        ...

    def ExportToTextFile(self, *args: typing.Any) -> None:
        """
        ExportToTextFile method.
        """
        pass

    def ExportToSTLFile(self, filePath: str) -> None:
        """
        ExportToSTLFile method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
        """
        pass

    def GetNodalValues(self, bodyRefId: int) -> System.Collections.Generic.Dictionary[int,float]:
        """
        GetNodalValues method.
        """
        pass

    def DuplicateWithoutResults(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        Run the DuplicateWithoutResults action.
        """
        pass

    def CreateResultsAtAllSets(self) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Creates results at all sets for results under a solution.
        """
        pass

    def RetrieveRemoteDPFResults(self) -> None:
        """
        RetrieveRemoteDPFResults method.
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def GetAPIName(self, dispId: int) -> str:
        """
        GetAPIName method.
        """
        pass

    def CreateParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        CreateParameter method.
        """
        pass

    def RetrieveResult(self) -> None:
        """
        
            Evaluates the individual result without evaluating all the results in the same solution.
            
        """
        pass

    def BodyWhereMaximumOccurs(self) -> Ansys.ACT.Automation.Mechanical.Body:
        """
        
            Gets the body that has the maximum result value.
            Throws an exception if body not found.
            
        """
        pass

    def AddAlert(self) -> Ansys.ACT.Automation.Mechanical.Results.Alert:
        """
        Creates a new Alert
        """
        pass

    def AddConvergence(self) -> Ansys.ACT.Automation.Mechanical.Results.Convergence:
        """
        Creates a new Convergence
        """
        pass

    def RenameBasedOnDefinition(self) -> None:
        """
        Run the RenameBasedOnDefinition action.
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    @typing.overload
    def GetChildren(self, recurses: bool, children: typing.List[ChildrenType]) -> typing.List[ChildrenType]:
        ...

    @typing.overload
    def GetChildren(self, category: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory, recurses: bool, children: typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetChildren(self, *args: typing.Any) -> typing.List[ChildrenType] | typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the list of children, filtered by type.
        """
        pass

    def AddComment(self) -> Ansys.ACT.Automation.Mechanical.Comment:
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> Ansys.ACT.Automation.Mechanical.Figure:
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: str) -> Ansys.ACT.Automation.Mechanical.Image:
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetPath(self) -> str:
        """
        GetPath method.
        """
        pass

    def GetIconFile(self) -> System.Byte:
        """
        GetIconFile method.
        """
        pass

    def Activate(self) -> None:
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def GetDetailsView(self) -> Ansys.ACT.Automation.Mechanical.DetailsViewData:
        """
        GetDetailsView method.
        """
        pass

    def Duplicate(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> None:
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def GetPropertyName(self, dispId: int) -> str:
        """
        GetPropertyName method.
        """
        pass

    def GetPropertyValue(self, name: str) -> typing.Any:
        """
        GetPropertyValue method.
        """
        pass

    @typing.overload
    def IsPropertyVisible(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyVisible(self, propName: str) -> bool:
        ...

    def IsPropertyVisible(self, *args: typing.Any) -> bool:
        """
        IsPropertyVisible method.
        """
        pass

    @typing.overload
    def IsPropertyEditable(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyEditable(self, propName: str) -> bool:
        ...

    def IsPropertyEditable(self, *args: typing.Any) -> bool:
        """
        IsPropertyEditable method.
        """
        pass

    def GetVisiblePropertyNames(self) -> typing.List[str]:
        """
        GetVisiblePropertyNames method.
        """
        pass

    def GetVisibleProperties(self) -> typing.List[System.Reflection.PropertyInfo]:
        """
        GetVisibleProperties method.
        """
        pass

    def GetAllProperties(self) -> typing.List[Ansys.ACT.Automation.Mechanical.AutomationPropertyWrapper]:
        """
        GetAllProperties method.
        """
        pass

    def PropertyByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def PropertyById(self, dispId: int) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        PropertyById method.
        """
        pass

    def GetParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: str) -> None:
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass

    def GetEnumName(self, enumType: type, value: int, dispId: int) -> str:
        """
        
            Enum name bound to value
            
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


class CompositeSamplingPoint(object):
    """
    Defines a CompositeSamplingPoint.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSCompositeSamplingPointResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Location(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Location.
        """
        return None

    @Location.setter
    def Location(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Location.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets the list of children.
        """
        return None

    @property
    def Comments(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Comment]]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Figure]]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        ObjectId property.
        """
        return None

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
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        ObjectTags property.
        """
        return None

    @property
    def IconName(self) -> typing.Optional[str]:
        """
        IconName property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ClsId(self) -> typing.Optional[int]:
        """
        ClsId property.
        """
        return None

    @property
    def AttachedRefs(self) -> typing.Optional[typing.List[int]]:
        """
        AttachedRefs property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    @property
    def State(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Legacy.State]:
        """
        State property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @typing.overload
    def __init__(self, internalObject: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    @typing.overload
    def GetChildren(self, recurses: bool, children: typing.List[ChildrenType]) -> typing.List[ChildrenType]:
        ...

    @typing.overload
    def GetChildren(self, category: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory, recurses: bool, children: typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetChildren(self, *args: typing.Any) -> typing.List[ChildrenType] | typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the list of children, filtered by type.
        """
        pass

    def AddComment(self) -> Ansys.ACT.Automation.Mechanical.Comment:
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> Ansys.ACT.Automation.Mechanical.Figure:
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: str) -> Ansys.ACT.Automation.Mechanical.Image:
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetPath(self) -> str:
        """
        GetPath method.
        """
        pass

    def GetIconFile(self) -> System.Byte:
        """
        GetIconFile method.
        """
        pass

    def Activate(self) -> None:
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def GetDetailsView(self) -> Ansys.ACT.Automation.Mechanical.DetailsViewData:
        """
        GetDetailsView method.
        """
        pass

    def Duplicate(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> None:
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def GetPropertyName(self, dispId: int) -> str:
        """
        GetPropertyName method.
        """
        pass

    def GetPropertyValue(self, name: str) -> typing.Any:
        """
        GetPropertyValue method.
        """
        pass

    @typing.overload
    def IsPropertyVisible(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyVisible(self, propName: str) -> bool:
        ...

    def IsPropertyVisible(self, *args: typing.Any) -> bool:
        """
        IsPropertyVisible method.
        """
        pass

    @typing.overload
    def IsPropertyEditable(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyEditable(self, propName: str) -> bool:
        ...

    def IsPropertyEditable(self, *args: typing.Any) -> bool:
        """
        IsPropertyEditable method.
        """
        pass

    def GetVisiblePropertyNames(self) -> typing.List[str]:
        """
        GetVisiblePropertyNames method.
        """
        pass

    def GetVisibleProperties(self) -> typing.List[System.Reflection.PropertyInfo]:
        """
        GetVisibleProperties method.
        """
        pass

    def GetAllProperties(self) -> typing.List[Ansys.ACT.Automation.Mechanical.AutomationPropertyWrapper]:
        """
        GetAllProperties method.
        """
        pass

    def PropertyByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def PropertyById(self, dispId: int) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        PropertyById method.
        """
        pass

    def CreateParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Creates a new parameter for a Property.
            
        """
        pass

    def GetParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: str) -> None:
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass

    def GetAPIName(self, dispId: int) -> str:
        """
        
            Property name bound to dispId.
            
        """
        pass

    def GetEnumName(self, enumType: type, value: int, dispId: int) -> str:
        """
        
            Enum name bound to value
            
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


class CompositeSamplingPointTool(object):
    """
    Defines a CompositeSamplingPointTool.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSCompositeFailureToolAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Children(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]]:
        """
        Gets the list of children.
        """
        return None

    @property
    def Comments(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Comment]]:
        """
        Gets the list of associated comments.
        """
        return None

    @property
    def Figures(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Figure]]:
        """
        Gets the list of associated figures.
        """
        return None

    @property
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ObjectId(self) -> typing.Optional[int]:
        """
        ObjectId property.
        """
        return None

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
    def Parent(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Parent property.
        """
        return None

    @property
    def GroupingFolder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        GroupingFolder property.
        """
        return None

    @property
    def ObjectTags(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IObjectTag]]:
        """
        ObjectTags property.
        """
        return None

    @property
    def IconName(self) -> typing.Optional[str]:
        """
        IconName property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ClsId(self) -> typing.Optional[int]:
        """
        ClsId property.
        """
        return None

    @property
    def AttachedRefs(self) -> typing.Optional[typing.List[int]]:
        """
        AttachedRefs property.
        """
        return None

    @property
    def Properties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties for this object.
            
        """
        return None

    @property
    def VisibleProperties(self) -> typing.Optional[tuple[Ansys.ACT.Automation.Mechanical.Property]]:
        """
        
            Gets the list of properties that are visible for this object.
            
        """
        return None

    @property
    def State(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Legacy.State]:
        """
        State property.
        """
        return None

    @property
    def ObjectState(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ObjectState]:
        """
        ObjectState property.
        """
        return None

    @typing.overload
    def __init__(self, internalObject: typing.Any) -> None:
        ...

    @typing.overload
    def __init__(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def AddCompositeSamplingPoint(self) -> Ansys.ACT.Automation.Mechanical.Results.CompositeFailureResults.CompositeSamplingPoint:
        """
        Creates a new CompositeSamplingPoint
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    @typing.overload
    def GetChildren(self, recurses: bool, children: typing.List[ChildrenType]) -> typing.List[ChildrenType]:
        ...

    @typing.overload
    def GetChildren(self, category: Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory, recurses: bool, children: typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        ...

    def GetChildren(self, *args: typing.Any) -> typing.List[ChildrenType] | typing.List[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Gets the list of children, filtered by type.
        """
        pass

    def AddComment(self) -> Ansys.ACT.Automation.Mechanical.Comment:
        """
        Creates a new child Comment.
        """
        pass

    def AddFigure(self) -> Ansys.ACT.Automation.Mechanical.Figure:
        """
        Creates a new child Figure.
        """
        pass

    def AddImage(self, filePath: str) -> Ansys.ACT.Automation.Mechanical.Image:
        """
        
            Creates a new child Image.
            If a filePath is provided, the image will be loaded from that file,
            if not, the image will be a screen capture of the Geometry window.
            
        """
        pass

    def Equals(self, other: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> bool:
        """
        Equals method.
        """
        pass

    def GetHashCode(self) -> int:
        """
        GetHashCode method.
        """
        pass

    def GetObjectData(self, info: System.Runtime.Serialization.SerializationInfo, context: System.Runtime.Serialization.StreamingContext) -> None:
        """
        GetObjectData method.
        """
        pass

    def GetPath(self) -> str:
        """
        GetPath method.
        """
        pass

    def GetIconFile(self) -> System.Byte:
        """
        GetIconFile method.
        """
        pass

    def Activate(self) -> None:
        """
        Activate the current object.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        
            Copies all visible properties from this object to another.
            
        """
        pass

    def GetDetailsView(self) -> Ansys.ACT.Automation.Mechanical.DetailsViewData:
        """
        GetDetailsView method.
        """
        pass

    def Duplicate(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        
            Creates a copy of the current DataModelObject.
            
        """
        pass

    def GroupAllSimilarChildren(self) -> None:
        """
        Run the GroupAllSimilarChildren action.
        """
        pass

    def GroupSimilarObjects(self) -> Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
        """
        Run the GroupSimilarObjects action.
        """
        pass

    def GetPropertyName(self, dispId: int) -> str:
        """
        GetPropertyName method.
        """
        pass

    def GetPropertyValue(self, name: str) -> typing.Any:
        """
        GetPropertyValue method.
        """
        pass

    @typing.overload
    def IsPropertyVisible(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyVisible(self, propName: str) -> bool:
        ...

    def IsPropertyVisible(self, *args: typing.Any) -> bool:
        """
        IsPropertyVisible method.
        """
        pass

    @typing.overload
    def IsPropertyEditable(self, dispId: int) -> bool:
        ...

    @typing.overload
    def IsPropertyEditable(self, propName: str) -> bool:
        ...

    def IsPropertyEditable(self, *args: typing.Any) -> bool:
        """
        IsPropertyEditable method.
        """
        pass

    def GetVisiblePropertyNames(self) -> typing.List[str]:
        """
        GetVisiblePropertyNames method.
        """
        pass

    def GetVisibleProperties(self) -> typing.List[System.Reflection.PropertyInfo]:
        """
        GetVisibleProperties method.
        """
        pass

    def GetAllProperties(self) -> typing.List[Ansys.ACT.Automation.Mechanical.AutomationPropertyWrapper]:
        """
        GetAllProperties method.
        """
        pass

    def PropertyByName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its unique name.
            
        """
        pass

    def PropertyByAPIName(self, name: str) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        
            Get a property by its API name.
            If multiple properties have the same API Name, only the first property with that name will be returned.
            
        """
        pass

    def PropertyById(self, dispId: int) -> Ansys.ACT.Automation.Mechanical.Property:
        """
        PropertyById method.
        """
        pass

    def CreateParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Creates a new parameter for a Property.
            
        """
        pass

    def GetParameter(self, propName: str) -> Ansys.ACT.Interfaces.Mechanical.IParameter:
        """
        
            Gets the parameter corresponding to the given property.
            
        """
        pass

    def RemoveParameter(self, propName: str) -> None:
        """
        
            Removes the parameter from the parameter set corresponding to the given property.
            
        """
        pass

    def GetAPIName(self, dispId: int) -> str:
        """
        
            Property name bound to dispId.
            
        """
        pass

    def GetEnumName(self, enumType: type, value: int, dispId: int) -> str:
        """
        
            Enum name bound to value
            
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


