"""MeshControls module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class Deviation(object):
    """
    Defines a Deviation.
    """

    @property
    def Tolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Tolerance property.
        """
        return None

    @Tolerance.setter
    def Tolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Tolerance property.
        """
        pass

    @property
    def MeshSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MeshSize property.
        """
        return None

    @MeshSize.setter
    def MeshSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MeshSize property.
        """
        pass

    @property
    def NumberOfDivisions(self) -> typing.Optional[int]:
        """
        NumberOfDivisions property.
        """
        return None

    @NumberOfDivisions.setter
    def NumberOfDivisions(self, value: typing.Optional[int]) -> None:
        """
        NumberOfDivisions property.
        """
        pass

    @property
    def ControlType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DeviationControlType]:
        """
        Gets or sets the SagControlType.
        """
        return None

    @ControlType.setter
    def ControlType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DeviationControlType]) -> None:
        """
        Gets or sets the SagControlType.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class RepairTopology(object):
    """
    Defines a RepairTopology.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FeatureAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FeatureAngle.
        """
        return None

    @FeatureAngle.setter
    def FeatureAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FeatureAngle.
        """
        pass

    @property
    def PinchTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PinchTolerance.
        """
        return None

    @PinchTolerance.setter
    def PinchTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PinchTolerance.
        """
        pass

    @property
    def SharpAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SharpAngle.
        """
        return None

    @SharpAngle.setter
    def SharpAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SharpAngle.
        """
        pass

    @property
    def ShortEdgeLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ShortEdgeLength.
        """
        return None

    @ShortEdgeLength.setter
    def ShortEdgeLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ShortEdgeLength.
        """
        pass

    @property
    def ThinFaceWidth(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ThinFaceWidth.
        """
        return None

    @ThinFaceWidth.setter
    def ThinFaceWidth(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ThinFaceWidth.
        """
        pass

    @property
    def CollapseShortEdges(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the CollapseShortEdges.
        """
        return None

    @CollapseShortEdges.setter
    def CollapseShortEdges(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the CollapseShortEdges.
        """
        pass

    @property
    def FillHole(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the FillHole.
        """
        return None

    @FillHole.setter
    def FillHole(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the FillHole.
        """
        pass

    @property
    def FillHoleGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the FillHoleGeometryDefineBy.
        """
        return None

    @FillHoleGeometryDefineBy.setter
    def FillHoleGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the FillHoleGeometryDefineBy.
        """
        pass

    @property
    def MergeFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the MergeFaces.
        """
        return None

    @MergeFaces.setter
    def MergeFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the MergeFaces.
        """
        pass

    @property
    def MergeFacesGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the MergeFacesGeometryDefineBy.
        """
        return None

    @MergeFacesGeometryDefineBy.setter
    def MergeFacesGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the MergeFacesGeometryDefineBy.
        """
        pass

    @property
    def PinchFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the PinchFaces.
        """
        return None

    @PinchFaces.setter
    def PinchFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the PinchFaces.
        """
        pass

    @property
    def PinchFacesGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the PinchFacesGeometryDefineBy.
        """
        return None

    @PinchFacesGeometryDefineBy.setter
    def PinchFacesGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the PinchFacesGeometryDefineBy.
        """
        pass

    @property
    def PinchFacesUseLocalScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the PinchFacesUseLocalScoping.
        """
        return None

    @PinchFacesUseLocalScoping.setter
    def PinchFacesUseLocalScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the PinchFacesUseLocalScoping.
        """
        pass

    @property
    def RemoveSharpAngleFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the RemoveSharpAngleFaces.
        """
        return None

    @RemoveSharpAngleFaces.setter
    def RemoveSharpAngleFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the RemoveSharpAngleFaces.
        """
        pass

    @property
    def RemoveThinFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the RemoveThinFaces.
        """
        return None

    @RemoveThinFaces.setter
    def RemoveThinFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the RemoveThinFaces.
        """
        pass

    @property
    def RepairPartialDefeature(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the use of partial defeature, which partially removes thin faces and sharp angles within provided tolerances, such that only topology impacting mesh quality is removed.
        """
        return None

    @RepairPartialDefeature.setter
    def RepairPartialDefeature(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the use of partial defeature, which partially removes thin faces and sharp angles within provided tolerances, such that only topology impacting mesh quality is removed.
        """
        pass

    @property
    def RepairPartialDefeatureGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the type of scoping selection to be used with Partial Defeature.
        """
        return None

    @RepairPartialDefeatureGeometryDefineBy.setter
    def RepairPartialDefeatureGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the type of scoping selection to be used with Partial Defeature.
        """
        pass

    @property
    def SharpAngleGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the SharpAngleGeometryDefineBy.
        """
        return None

    @SharpAngleGeometryDefineBy.setter
    def SharpAngleGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the SharpAngleGeometryDefineBy.
        """
        pass

    @property
    def SharpAngleUseLocalScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the SharpAngleUseLocalScoping.
        """
        return None

    @SharpAngleUseLocalScoping.setter
    def SharpAngleUseLocalScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the SharpAngleUseLocalScoping.
        """
        pass

    @property
    def ShortEdgeGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the ShortEdgeGeometryDefineBy.
        """
        return None

    @ShortEdgeGeometryDefineBy.setter
    def ShortEdgeGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the ShortEdgeGeometryDefineBy.
        """
        pass

    @property
    def ShortEdgeUseLocalScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the ShortEdgeUseLocalScoping.
        """
        return None

    @ShortEdgeUseLocalScoping.setter
    def ShortEdgeUseLocalScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the ShortEdgeUseLocalScoping.
        """
        pass

    @property
    def SuppressEdgesGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the SuppressEdgesGeometryDefineBy.
        """
        return None

    @SuppressEdgesGeometryDefineBy.setter
    def SuppressEdgesGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the SuppressEdgesGeometryDefineBy.
        """
        pass

    @property
    def SuppressEdges(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the SuppressEdges.
        """
        return None

    @SuppressEdges.setter
    def SuppressEdges(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the SuppressEdges.
        """
        pass

    @property
    def ThinFaceGeometryDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the ThinFaceGeometryDefineBy.
        """
        return None

    @ThinFaceGeometryDefineBy.setter
    def ThinFaceGeometryDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the ThinFaceGeometryDefineBy.
        """
        pass

    @property
    def ThinFacesUseLocalScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the ThinFacesUseLocalScoping.
        """
        return None

    @ThinFacesUseLocalScoping.setter
    def ThinFacesUseLocalScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the ThinFacesUseLocalScoping.
        """
        pass

    @property
    def FillHoleNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the FillHoleNamedSelection.
        """
        return None

    @FillHoleNamedSelection.setter
    def FillHoleNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the FillHoleNamedSelection.
        """
        pass

    @property
    def MergeFacesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the MergeFacesNamedSelection.
        """
        return None

    @MergeFacesNamedSelection.setter
    def MergeFacesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the MergeFacesNamedSelection.
        """
        pass

    @property
    def PartialDefeatureNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the partial defeature scoping using named selections.
        """
        return None

    @PartialDefeatureNamedSelection.setter
    def PartialDefeatureNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the partial defeature scoping using named selections.
        """
        pass

    @property
    def PinchFacesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the PinchFacesNamedSelection.
        """
        return None

    @PinchFacesNamedSelection.setter
    def PinchFacesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the PinchFacesNamedSelection.
        """
        pass

    @property
    def SharpAngleNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the SharpAngleNamedSelection.
        """
        return None

    @SharpAngleNamedSelection.setter
    def SharpAngleNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the SharpAngleNamedSelection.
        """
        pass

    @property
    def ShortEdgeNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the ShortEdgeNamedSelection.
        """
        return None

    @ShortEdgeNamedSelection.setter
    def ShortEdgeNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the ShortEdgeNamedSelection.
        """
        pass

    @property
    def SuppressEdgesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the SuppressEdgesNamedSelection.
        """
        return None

    @SuppressEdgesNamedSelection.setter
    def SuppressEdgesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the SuppressEdgesNamedSelection.
        """
        pass

    @property
    def ThinFaceNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the ThinFaceNamedSelection.
        """
        return None

    @ThinFaceNamedSelection.setter
    def ThinFaceNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the ThinFaceNamedSelection.
        """
        pass

    @property
    def FillHoleGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the FillHoleGeometrySelection.
        """
        return None

    @FillHoleGeometrySelection.setter
    def FillHoleGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the FillHoleGeometrySelection.
        """
        pass

    @property
    def MergeFacesGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MergeFacesGeometrySelection.
        """
        return None

    @MergeFacesGeometrySelection.setter
    def MergeFacesGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MergeFacesGeometrySelection.
        """
        pass

    @property
    def PartialDefeatureGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the partial defeature scoping using geometry selections.
        """
        return None

    @PartialDefeatureGeometrySelection.setter
    def PartialDefeatureGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the partial defeature scoping using geometry selections.
        """
        pass

    @property
    def PinchFacesGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the PinchFacesGeometrySelection.
        """
        return None

    @PinchFacesGeometrySelection.setter
    def PinchFacesGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the PinchFacesGeometrySelection.
        """
        pass

    @property
    def SharpAngleGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SharpAngleGeometrySelection.
        """
        return None

    @SharpAngleGeometrySelection.setter
    def SharpAngleGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SharpAngleGeometrySelection.
        """
        pass

    @property
    def ShortEdgeGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ShortEdgeGeometrySelection.
        """
        return None

    @ShortEdgeGeometrySelection.setter
    def ShortEdgeGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ShortEdgeGeometrySelection.
        """
        pass

    @property
    def SuppressEdgesGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SuppressEdgesGeometrySelection.
        """
        return None

    @SuppressEdgesGeometrySelection.setter
    def SuppressEdgesGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SuppressEdgesGeometrySelection.
        """
        pass

    @property
    def ThinFaceGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ThinFaceGeometrySelection.
        """
        return None

    @ThinFaceGeometrySelection.setter
    def ThinFaceGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ThinFaceGeometrySelection.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Washer(object):
    """
    Defines a Washer.
    """

    @property
    def NumberOfWasherLayers(self) -> typing.Optional[int]:
        """
        NumberOfWasherLayers property.
        """
        return None

    @NumberOfWasherLayers.setter
    def NumberOfWasherLayers(self, value: typing.Optional[int]) -> None:
        """
        NumberOfWasherLayers property.
        """
        pass

    @property
    def NumberOfLayers(self) -> typing.Optional[int]:
        """
        NumberOfLayers property.
        """
        return None

    @NumberOfLayers.setter
    def NumberOfLayers(self, value: typing.Optional[int]) -> None:
        """
        NumberOfLayers property.
        """
        pass

    @property
    def WasherMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherMethod]:
        """
        WasherMethod property.
        """
        return None

    @WasherMethod.setter
    def WasherMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherMethod]) -> None:
        """
        WasherMethod property.
        """
        pass

    @property
    def WasherType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherType]:
        """
        WasherType property.
        """
        return None

    @WasherType.setter
    def WasherType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherType]) -> None:
        """
        WasherType property.
        """
        pass

    @property
    def WasherHeightType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherType]:
        """
        WasherHeightType property.
        """
        return None

    @WasherHeightType.setter
    def WasherHeightType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WasherType]) -> None:
        """
        WasherHeightType property.
        """
        pass

    @property
    def LayerTransitionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LayerTransitionType]:
        """
        LayerTransitionType property.
        """
        return None

    @LayerTransitionType.setter
    def LayerTransitionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LayerTransitionType]) -> None:
        """
        LayerTransitionType property.
        """
        pass

    @property
    def NumberOfWasherDivisions(self) -> typing.Optional[int]:
        """
        NumberOfWasherDivisions property.
        """
        return None

    @NumberOfWasherDivisions.setter
    def NumberOfWasherDivisions(self, value: typing.Optional[int]) -> None:
        """
        NumberOfWasherDivisions property.
        """
        pass

    @property
    def NumberOfDivisions(self) -> typing.Optional[int]:
        """
        NumberOfDivisions property.
        """
        return None

    @NumberOfDivisions.setter
    def NumberOfDivisions(self, value: typing.Optional[int]) -> None:
        """
        NumberOfDivisions property.
        """
        pass

    @property
    def MinimumNumberOfWasherDivisions(self) -> typing.Optional[int]:
        """
        MinimumNumberOfWasherDivisions property.
        """
        return None

    @MinimumNumberOfWasherDivisions.setter
    def MinimumNumberOfWasherDivisions(self, value: typing.Optional[int]) -> None:
        """
        MinimumNumberOfWasherDivisions property.
        """
        pass

    @property
    def MinimumNumberOfDivisions(self) -> typing.Optional[int]:
        """
        MinimumNumberOfDivisions property.
        """
        return None

    @MinimumNumberOfDivisions.setter
    def MinimumNumberOfDivisions(self, value: typing.Optional[int]) -> None:
        """
        MinimumNumberOfDivisions property.
        """
        pass

    @property
    def FactorOfDiameter(self) -> typing.Optional[float]:
        """
        FactorOfDiameter property.
        """
        return None

    @FactorOfDiameter.setter
    def FactorOfDiameter(self, value: typing.Optional[float]) -> None:
        """
        FactorOfDiameter property.
        """
        pass

    @property
    def ScaleOfDiameter(self) -> typing.Optional[float]:
        """
        ScaleOfDiameter property.
        """
        return None

    @ScaleOfDiameter.setter
    def ScaleOfDiameter(self, value: typing.Optional[float]) -> None:
        """
        ScaleOfDiameter property.
        """
        pass

    @property
    def ElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Quad Layer Element Size.
        """
        return None

    @ElementSize.setter
    def ElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Quad Layer Element Size.
        """
        pass

    @property
    def QuadLayerDirection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerDirection]:
        """
        Gets or sets the Quad Layer Direction.
        """
        return None

    @QuadLayerDirection.setter
    def QuadLayerDirection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerDirection]) -> None:
        """
        Gets or sets the Quad Layer Direction.
        """
        pass

    @property
    def FaceScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the face scoping method for Quad Layer Direction.
        """
        return None

    @FaceScopingMethod.setter
    def FaceScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the face scoping method for Quad Layer Direction.
        """
        pass

    @property
    def FaceSelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Quad Layer Direction Face Geoemetry Selection.
        """
        return None

    @FaceSelection.setter
    def FaceSelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Quad Layer Direction Face Geoemetry Selection.
        """
        pass

    @property
    def FaceNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the Named Selection for Quad Layer Direction Face Scoping.
        """
        return None

    @FaceNamedSelection.setter
    def FaceNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the Named Selection for Quad Layer Direction Face Scoping.
        """
        pass

    @property
    def Relaxation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerRelaxation]:
        """
        Gets or sets the relaxation of Quad Layer.
        """
        return None

    @Relaxation.setter
    def Relaxation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerRelaxation]) -> None:
        """
        Gets or sets the relaxation of Quad Layer.
        """
        pass

    @property
    def QuadLayerType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerType]:
        """
        Gets or sets the Quad Layer Type.
        """
        return None

    @QuadLayerType.setter
    def QuadLayerType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.QuadLayerType]) -> None:
        """
        Gets or sets the Quad Layer Type.
        """
        pass

    @property
    def LayerHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LayerHeight property.
        """
        return None

    @LayerHeight.setter
    def LayerHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LayerHeight property.
        """
        pass

    @property
    def WasherLayerHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        WasherLayerHeight property.
        """
        return None

    @WasherLayerHeight.setter
    def WasherLayerHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        WasherLayerHeight property.
        """
        pass

    @property
    def FirstLayerHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        FirstLayerHeight property.
        """
        return None

    @FirstLayerHeight.setter
    def FirstLayerHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        FirstLayerHeight property.
        """
        pass

    @property
    def GrowthRate(self) -> typing.Optional[float]:
        """
        GrowthRate property.
        """
        return None

    @GrowthRate.setter
    def GrowthRate(self, value: typing.Optional[float]) -> None:
        """
        GrowthRate property.
        """
        pass

    @property
    def WasherDefeatureProximityTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        WasherDefeatureProximityTolerance property.
        """
        return None

    @WasherDefeatureProximityTolerance.setter
    def WasherDefeatureProximityTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        WasherDefeatureProximityTolerance property.
        """
        pass

    @property
    def QuadLayerDefeatureProximityTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        QuadLayerDefeatureProximityTolerance property.
        """
        return None

    @QuadLayerDefeatureProximityTolerance.setter
    def QuadLayerDefeatureProximityTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        QuadLayerDefeatureProximityTolerance property.
        """
        pass

    @property
    def WasherAutoDefeature(self) -> typing.Optional[bool]:
        """
        WasherAutoDefeature property.
        """
        return None

    @WasherAutoDefeature.setter
    def WasherAutoDefeature(self, value: typing.Optional[bool]) -> None:
        """
        WasherAutoDefeature property.
        """
        pass

    @property
    def AllowNodeMovement(self) -> typing.Optional[bool]:
        """
        Gets or sets the AllowNodeMovement.
        """
        return None

    @AllowNodeMovement.setter
    def AllowNodeMovement(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AllowNodeMovement.
        """
        pass

    @property
    def NodeMovementTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        NodeMovementTolerance property.
        """
        return None

    @NodeMovementTolerance.setter
    def NodeMovementTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        NodeMovementTolerance property.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Weld(object):
    """
    Defines a Weld.
    """

    @property
    def BottomEntities(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Bottom Entities (Bodies / Faces ) or Extension.
        """
        return None

    @BottomEntities.setter
    def BottomEntities(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Bottom Entities (Bodies / Faces ) or Extension.
        """
        pass

    @property
    def TopEntities(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Top Entities (Bodies / Faces ) or Extension.
        """
        return None

    @TopEntities.setter
    def TopEntities(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Top Entities (Bodies / Faces ) or Extension.
        """
        pass

    @property
    def WeldCurves(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Weld Curves.
        """
        return None

    @WeldCurves.setter
    def WeldCurves(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Weld Curves.
        """
        pass

    @property
    def WeldCurvesBody(self) -> typing.Optional[int]:
        """
        WeldCurvesBody property.
        """
        return None

    @WeldCurvesBody.setter
    def WeldCurvesBody(self, value: typing.Optional[int]) -> None:
        """
        WeldCurvesBody property.
        """
        pass

    @property
    def EdgeSelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the Edges.
        """
        return None

    @EdgeSelection.setter
    def EdgeSelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the Edges.
        """
        pass

    @property
    def ControlType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldType]:
        """
        Gets or sets the WeldControlType.
        """
        return None

    @ControlType.setter
    def ControlType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldType]) -> None:
        """
        Gets or sets the WeldControlType.
        """
        pass

    @property
    def Source(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldSource]:
        """
        Gets or sets the WeldControlSource.
        """
        return None

    @Source.setter
    def Source(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldSource]) -> None:
        """
        Gets or sets the WeldControlSource.
        """
        pass

    @property
    def ModeledAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldModeledAs]:
        """
        Gets or sets the WeldControlModeledAs.
        """
        return None

    @ModeledAs.setter
    def ModeledAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldModeledAs]) -> None:
        """
        Gets or sets the WeldControlModeledAs.
        """
        pass

    @property
    def WeldElementRows(self) -> typing.Optional[int]:
        """
        Gets or sets the WeldControlElementRows.
        """
        return None

    @WeldElementRows.setter
    def WeldElementRows(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the WeldControlElementRows.
        """
        pass

    @property
    def Relaxation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldRelaxation]:
        """
        Gets or sets the WeldControlRelaxation.
        """
        return None

    @Relaxation.setter
    def Relaxation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldRelaxation]) -> None:
        """
        Gets or sets the WeldControlRelaxation.
        """
        pass

    @property
    def WeldTargetShellFace(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldTargetShellFaceType]:
        """
        Gets or sets the WeldTargetShellFace.
        """
        return None

    @WeldTargetShellFace.setter
    def WeldTargetShellFace(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldTargetShellFaceType]) -> None:
        """
        Gets or sets the WeldTargetShellFace.
        """
        pass

    @property
    def WeldFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFormulation]:
        """
        Gets or sets the WeldFormulation.
        """
        return None

    @WeldFormulation.setter
    def WeldFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFormulation]) -> None:
        """
        Gets or sets the WeldFormulation.
        """
        pass

    @property
    def WeldPinballRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldPinballRadius
            
        """
        return None

    @WeldPinballRadius.setter
    def WeldPinballRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldPinballRadius
            
        """
        pass

    @property
    def TentDirection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldTentDirection]:
        """
        Gets or sets the WeldControlTentDirection.
        """
        return None

    @TentDirection.setter
    def TentDirection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldTentDirection]) -> None:
        """
        Gets or sets the WeldControlTentDirection.
        """
        pass

    @property
    def AngledDirection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldAngledDirection]:
        """
        Gets or sets the WeldControlAngledDirection.
        """
        return None

    @AngledDirection.setter
    def AngledDirection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldAngledDirection]) -> None:
        """
        Gets or sets the WeldControlAngledDirection.
        """
        pass

    @property
    def CreateUsing(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCreateUsing]:
        """
        Gets or sets the WeldControlCreateUsing.
        """
        return None

    @CreateUsing.setter
    def CreateUsing(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCreateUsing]) -> None:
        """
        Gets or sets the WeldControlCreateUsing.
        """
        pass

    @property
    def UseWorksheet(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlUseWorksheet.
        """
        return None

    @UseWorksheet.setter
    def UseWorksheet(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlUseWorksheet.
        """
        pass

    @property
    def CurveScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCurveScoping]:
        """
        Gets or sets the WeldControlCurveScoping.
        """
        return None

    @CurveScoping.setter
    def CurveScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCurveScoping]) -> None:
        """
        Gets or sets the WeldControlCurveScoping.
        """
        pass

    @property
    def CreationCriteria(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCreationCriteria]:
        """
        Gets or sets the WeldControlCreationCriteria.
        """
        return None

    @CreationCriteria.setter
    def CreationCriteria(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldCreationCriteria]) -> None:
        """
        Gets or sets the WeldControlCreationCriteria.
        """
        pass

    @property
    def ThicknessAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldThickness]:
        """
        Gets or sets the WeldControlThicknessAssignment.
        """
        return None

    @ThicknessAssignment.setter
    def ThicknessAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldThickness]) -> None:
        """
        Gets or sets the WeldControlThicknessAssignment.
        """
        pass

    @property
    def WeldWidthAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldWidthAssignment]:
        """
        Gets or sets the WeldControlWeldWidthAssignment.
        """
        return None

    @WeldWidthAssignment.setter
    def WeldWidthAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldWidthAssignment]) -> None:
        """
        Gets or sets the WeldControlWeldWidthAssignment.
        """
        pass

    @property
    def EdgeMeshSizeAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldEdgeMeshSizeAssignment]:
        """
        Gets or sets the WeldControlEdgeMeshSizeAssignment.
        """
        return None

    @EdgeMeshSizeAssignment.setter
    def EdgeMeshSizeAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldEdgeMeshSizeAssignment]) -> None:
        """
        Gets or sets the WeldControlEdgeMeshSizeAssignment.
        """
        pass

    @property
    def WeldHeightAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHeightAssignment]:
        """
        Gets or sets the WeldControlWeldHeightAssignment.
        """
        return None

    @WeldHeightAssignment.setter
    def WeldHeightAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHeightAssignment]) -> None:
        """
        Gets or sets the WeldControlWeldHeightAssignment.
        """
        pass

    @property
    def HAZDistanceAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHAZDistanceAssignment]:
        """
        Gets or sets the WeldControlHAZDistanceAssignment.
        """
        return None

    @HAZDistanceAssignment.setter
    def HAZDistanceAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHAZDistanceAssignment]) -> None:
        """
        Gets or sets the WeldControlHAZDistanceAssignment.
        """
        pass

    @property
    def HAZDistanceOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHAZDistanceOption]:
        """
        Gets or sets the WeldControlHAZDistanceOption.
        """
        return None

    @HAZDistanceOption.setter
    def HAZDistanceOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldHAZDistanceOption]) -> None:
        """
        Gets or sets the WeldControlHAZDistanceOption.
        """
        pass

    @property
    def WeldThicknessExpression(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlThicknessExpression Value.
        """
        return None

    @WeldThicknessExpression.setter
    def WeldThicknessExpression(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlThicknessExpression Value.
        """
        pass

    @property
    def EdgeMeshSizeExpression(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlEdgeMeshSizeExpression Value.
        """
        return None

    @EdgeMeshSizeExpression.setter
    def EdgeMeshSizeExpression(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlEdgeMeshSizeExpression Value.
        """
        pass

    @property
    def WeldWidthExpression(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlWeldWidthExpression Value.
        """
        return None

    @WeldWidthExpression.setter
    def WeldWidthExpression(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlWeldWidthExpression Value.
        """
        pass

    @property
    def WeldHeightExpression(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlWeldHeightExpression Value.
        """
        return None

    @WeldHeightExpression.setter
    def WeldHeightExpression(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlWeldHeightExpression Value.
        """
        pass

    @property
    def HAZDistanceExpressionTopPlate(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlHAZDistanceExpression Value.
        """
        return None

    @HAZDistanceExpressionTopPlate.setter
    def HAZDistanceExpressionTopPlate(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlHAZDistanceExpression Value.
        """
        pass

    @property
    def LayerTransitionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LayerTransitionType]:
        """
        Gets or sets the WeldControlHAZLayerTransitionType.
        """
        return None

    @LayerTransitionType.setter
    def LayerTransitionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LayerTransitionType]) -> None:
        """
        Gets or sets the WeldControlHAZLayerTransitionType.
        """
        pass

    @property
    def HAZDistanceExpression(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlHAZDistanceExpression Value.
        """
        return None

    @HAZDistanceExpression.setter
    def HAZDistanceExpression(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlHAZDistanceExpression Value.
        """
        pass

    @property
    def HAZDistanceExpressionBottomPlate(self) -> typing.Optional[str]:
        """
        Gets or sets HAZDistanceExpressionBottomPlate Value.
        """
        return None

    @HAZDistanceExpressionBottomPlate.setter
    def HAZDistanceExpressionBottomPlate(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets HAZDistanceExpressionBottomPlate Value.
        """
        pass

    @property
    def MaxThicknessFactor(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlMaxThicknessFactor
            
        """
        return None

    @MaxThicknessFactor.setter
    def MaxThicknessFactor(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlMaxThicknessFactor
            
        """
        pass

    @property
    def MinThicknessFactor(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlMinThicknessFactor
            
        """
        return None

    @MinThicknessFactor.setter
    def MinThicknessFactor(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlMinThicknessFactor
            
        """
        pass

    @property
    def Thickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlThickness
            
        """
        return None

    @Thickness.setter
    def Thickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlThickness
            
        """
        pass

    @property
    def AdjustWeldHeight(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlAdjustWeldHeight.
        """
        return None

    @AdjustWeldHeight.setter
    def AdjustWeldHeight(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlAdjustWeldHeight.
        """
        pass

    @property
    def CreateOffsetLayer(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlCreateOffsetLayer.
        """
        return None

    @CreateOffsetLayer.setter
    def CreateOffsetLayer(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlCreateOffsetLayer.
        """
        pass

    @property
    def CreateHAZLayer(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlCreateHAZLayer.
        """
        return None

    @CreateHAZLayer.setter
    def CreateHAZLayer(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlCreateHAZLayer.
        """
        pass

    @property
    def WeldHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        return None

    @WeldHeight.setter
    def WeldHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        pass

    @property
    def WeldAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WeldAngle.
        """
        return None

    @WeldAngle.setter
    def WeldAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WeldAngle.
        """
        pass

    @property
    def SharpAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WeldSharpAngle.
        """
        return None

    @SharpAngle.setter
    def SharpAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WeldSharpAngle.
        """
        pass

    @property
    def ButtWeldOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the ButtWeldOption.
        """
        return None

    @ButtWeldOption.setter
    def ButtWeldOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the ButtWeldOption.
        """
        pass

    @property
    def LapWeldAngleTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the LapWeldAngleTolerance.
        """
        return None

    @LapWeldAngleTolerance.setter
    def LapWeldAngleTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the LapWeldAngleTolerance.
        """
        pass

    @property
    def EdgeMeshSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlEdgeMeshSize
            
        """
        return None

    @EdgeMeshSize.setter
    def EdgeMeshSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlEdgeMeshSize
            
        """
        pass

    @property
    def WeldControlWeldWidth(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlWeldWidth
            
        """
        return None

    @WeldControlWeldWidth.setter
    def WeldControlWeldWidth(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlWeldWidth
            
        """
        pass

    @property
    def HAZDistanceTopPlate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets HAZDistanceTopPlate
            
        """
        return None

    @HAZDistanceTopPlate.setter
    def HAZDistanceTopPlate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets HAZDistanceTopPlate
            
        """
        pass

    @property
    def HAZDistanceBottomPlate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets HAZDistanceBottomPlate
            
        """
        return None

    @HAZDistanceBottomPlate.setter
    def HAZDistanceBottomPlate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets HAZDistanceBottomPlate
            
        """
        pass

    @property
    def HAZDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlHAZDistance
            
        """
        return None

    @HAZDistance.setter
    def HAZDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlHAZDistance
            
        """
        pass

    @property
    def WeldLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        return None

    @WeldLength.setter
    def WeldLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        pass

    @property
    def WeldPitch(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        return None

    @WeldPitch.setter
    def WeldPitch(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        pass

    @property
    def NumberOfWelds(self) -> typing.Optional[int]:
        """
        
            Gets or sets WeldControlNumberOfLayers
            
        """
        return None

    @NumberOfWelds.setter
    def NumberOfWelds(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets WeldControlNumberOfLayers
            
        """
        pass

    @property
    def Offset1(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        return None

    @Offset1.setter
    def Offset1(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        pass

    @property
    def Offset2(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        return None

    @Offset2.setter
    def Offset2(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerHeight
            
        """
        pass

    @property
    def OffsetLayerGrowthRate(self) -> typing.Optional[float]:
        """
        
             Gets or sets the WeldControlOffsetLayerGrowthRate
            
        """
        return None

    @OffsetLayerGrowthRate.setter
    def OffsetLayerGrowthRate(self, value: typing.Optional[float]) -> None:
        """
        
             Gets or sets the WeldControlOffsetLayerGrowthRate
            
        """
        pass

    @property
    def HAZGrowthRate(self) -> typing.Optional[float]:
        """
        
             Gets or sets the WeldControlHAZGrowthRate
            
        """
        return None

    @HAZGrowthRate.setter
    def HAZGrowthRate(self, value: typing.Optional[float]) -> None:
        """
        
             Gets or sets the WeldControlHAZGrowthRate
            
        """
        pass

    @property
    def ConnectionTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
             Gets or sets the WeldControlConnectionTolerance
            
        """
        return None

    @ConnectionTolerance.setter
    def ConnectionTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
             Gets or sets the WeldControlConnectionTolerance
            
        """
        pass

    @property
    def NumberOfLayers(self) -> typing.Optional[int]:
        """
        
            Gets or sets WeldControlNumberOfLayers
            
        """
        return None

    @NumberOfLayers.setter
    def NumberOfLayers(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets WeldControlNumberOfLayers
            
        """
        pass

    @property
    def GenerateNamedSelection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldGeneratedNamedSelection]:
        """
        Gets or sets the WeldControlGenerateNamedSelection.
        """
        return None

    @GenerateNamedSelection.setter
    def GenerateNamedSelection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeldGeneratedNamedSelection]) -> None:
        """
        Gets or sets the WeldControlGenerateNamedSelection.
        """
        pass

    @property
    def GenerateEndCaps(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlSmoothing.
        """
        return None

    @GenerateEndCaps.setter
    def GenerateEndCaps(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlSmoothing.
        """
        pass

    @property
    def WriteDefinitionFile(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlSmoothing.
        """
        return None

    @WriteDefinitionFile.setter
    def WriteDefinitionFile(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlSmoothing.
        """
        pass

    @property
    def WeldDefinitionFileLocation(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldDefinitionFile Location.
        """
        return None

    @WeldDefinitionFileLocation.setter
    def WeldDefinitionFileLocation(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldDefinitionFile Location.
        """
        pass

    @property
    def WeldIntersectionTag(self) -> typing.Optional[str]:
        """
        Gets or sets the WeldControlIntersectionTag Value.
        """
        return None

    @WeldIntersectionTag.setter
    def WeldIntersectionTag(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the WeldControlIntersectionTag Value.
        """
        pass

    @property
    def WeldIntersectionTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the WeldControlIntersectionTolerance Value.
        """
        return None

    @WeldIntersectionTolerance.setter
    def WeldIntersectionTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the WeldControlIntersectionTolerance Value.
        """
        pass

    @property
    def Smoothing(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the WeldControlSmoothing.
        """
        return None

    @Smoothing.setter
    def Smoothing(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the WeldControlSmoothing.
        """
        pass

    @property
    def CrossSectionId(self) -> typing.Optional[int]:
        """
        Gets or sets the WeldControlCrossSectionId.
        """
        return None

    @CrossSectionId.setter
    def CrossSectionId(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the WeldControlCrossSectionId.
        """
        pass

    @property
    def MaterialId(self) -> typing.Optional[int]:
        """
        Gets or sets the WeldControlMaterialId.
        """
        return None

    @MaterialId.setter
    def MaterialId(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the WeldControlMaterialId.
        """
        pass

    @property
    def NameFilter(self) -> typing.Optional[str]:
        """
        Gets or sets the NameFilter.
        """
        return None

    @NameFilter.setter
    def NameFilter(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the NameFilter.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def WeldEdgesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the WeldEdgesNamedSelection.
        """
        return None

    @WeldEdgesNamedSelection.setter
    def WeldEdgesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the WeldEdgesNamedSelection.
        """
        pass

    @property
    def BottomEntitiesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the BottomEntitiesNamedSelection.
        """
        return None

    @BottomEntitiesNamedSelection.setter
    def BottomEntitiesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the BottomEntitiesNamedSelection.
        """
        pass

    @property
    def TopEntitiesNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the TopEntitiesNamedSelection.
        """
        return None

    @TopEntitiesNamedSelection.setter
    def TopEntitiesNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the TopEntitiesNamedSelection.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def ClearWeldControlIntersectionTag(self) -> None:
        """
        
             clear the WeldControlIntersectionTag
            
        """
        pass

    def AppendWeldControlIntersectionTag(self, val: str) -> None:
        """
        
             append the WeldControlIntersectionTag
            
        """
        pass

    def GenerateWeldIntersectionTag(self) -> None:
        """
        
             Auto detect Intersection Tags within specified tolerance
            
        """
        pass

    def ClearAutoWeldIntersectionTag(self, includeInactive: bool) -> None:
        """
        
             Clear Auto Intersection Tags
            
        """
        pass

    def WeldWorksheetStatus(self, rowIndex: int) -> Ansys.Mechanical.DataModel.Enums.WeldStatus:
        """
        
             Get state of a given row
            
        """
        pass

    def GetWeldWorksheetNumWarning(self) -> int:
        """
        
             Get Number of rows with warnings
            
        """
        pass

    def GetWeldWorksheetNumError(self) -> int:
        """
        
             Get Number of Errored rows
            
        """
        pass

    def GetWeldWorksheetWarningIndices(self) -> typing.List[int]:
        """
        
             Get Indices for Warnings
            
        """
        pass

    def GetWeldWorksheetErrorIndices(self) -> typing.List[int]:
        """
        
             Get Indices for Errors
            
        """
        pass

    def ActivateAllWorksheetEntries(self) -> None:
        """
        
             set the ActivateAllWorksheetEntries
            
        """
        pass

    def DeactivateAllWorksheetEntries(self) -> None:
        """
        
             set the DeactivateAllWorksheetEntries
            
        """
        pass

    def SetWeldWorksheetActive(self, rowIndices: typing.Iterable[int], val: bool) -> None:
        """
        SetWeldWorksheetActive method.
        """
        pass

    def GetWeldWorksheetActive(self, rowIndex: int) -> bool:
        """
        
             get the WeldWorksheetActive
            
        """
        pass

    def SetWeldWorksheetEdgeMeshSize(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetEdgeMeshSize method.
        """
        pass

    def GetWeldWorksheetEdgeMeshSize(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetEdgeMeshSize
            
        """
        pass

    def SetWeldWorksheetWeldAngle(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetWeldAngle method.
        """
        pass

    def GetWeldWorksheetWeldAngle(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetWeldAngle
            
        """
        pass

    def GetWeldWorksheetHAZDistanceBottomPlate(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetHAZDistance
            
        """
        pass

    def GetWeldWorksheetHAZDistance(self, rowIndex: int) -> float:
        """
        GetWeldWorksheetHAZDistance method.
        """
        pass

    def SetWeldWorksheetHAZDistanceTopPlate(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetHAZDistanceTopPlate method.
        """
        pass

    def SetWeldWorksheetHAZDistance(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetHAZDistance method.
        """
        pass

    def SetWeldWorksheetHAZDistanceBottomPlate(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetHAZDistanceBottomPlate method.
        """
        pass

    def GetWeldWorksheetSharpAngle(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetSharpAngle
            
        """
        pass

    def SetWeldWorksheetSharpAngle(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetSharpAngle method.
        """
        pass

    def GetWeldWorksheetHeight(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetHeight
            
        """
        pass

    def SetWeldWorksheetHeight(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetHeight method.
        """
        pass

    def GetWeldWorksheetLength(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetLength
            
        """
        pass

    def SetWeldWorksheetLength(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetLength method.
        """
        pass

    def GetWeldWorksheetWidth(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetWidth
            
        """
        pass

    def SetWeldWorksheetWidth(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetWidth method.
        """
        pass

    def WeldWorksheetNumEntries(self) -> int:
        """
        
             Get total number of entries in worksheet
            
        """
        pass

    def GetWeldWorksheetPitch(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetPitch
            
        """
        pass

    def SetWeldWorksheetPitch(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetPitch method.
        """
        pass

    def GetWeldWorksheetThickness(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetThickness
            
        """
        pass

    def SetWeldWorksheetThickness(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetThickness method.
        """
        pass

    def GetWeldWorksheetAbsTol(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetAbsTol
            
        """
        pass

    def SetWeldWorksheetAbsTol(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetAbsTol method.
        """
        pass

    def GetWeldWorksheetNumWelds(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetNumWelds
            
        """
        pass

    def SetWeldWorksheetNumWelds(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetNumWelds method.
        """
        pass

    def GetWeldWorksheetOffset1(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetOffset1
            
        """
        pass

    def SetWeldWorksheetOffset1(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetOffset1 method.
        """
        pass

    def GetWeldWorksheetOffset2(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetOffset2
            
        """
        pass

    def SetWeldWorksheetOffset2(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetOffset2 method.
        """
        pass

    def GetWeldWorksheetSmoothing(self, rowIndex: int) -> bool:
        """
        
             get the WeldControlWorksheetSmoothing option
            
        """
        pass

    def SetWeldWorksheetSmoothing(self, rowIndices: typing.Iterable[int], val: bool) -> None:
        """
        SetWeldWorksheetSmoothing method.
        """
        pass

    def GetWeldWorksheetLapAngleTol(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetLapAngleTol
            
        """
        pass

    def SetWeldWorksheetLapAngleTol(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetLapAngleTol method.
        """
        pass

    def GetWeldWorksheetGenerateEndCaps(self, rowIndex: int) -> bool:
        """
        
             get the WeldControlWorksheetGenerateEndCaps
            
        """
        pass

    def SetWeldWorksheetGenerateEndCaps(self, rowIndices: typing.Iterable[int], val: bool) -> None:
        """
        SetWeldWorksheetGenerateEndCaps method.
        """
        pass

    def GetWeldWorksheetOffsetLayerGrowthRate(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetOffsetLayerGrowthRate
            
        """
        pass

    def GetWeldWorksheetHAZGrowthRate(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetHAZGrowthRate
            
        """
        pass

    def SetWeldWorksheetNumLayers(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetNumLayers method.
        """
        pass

    def GetWeldWorksheetNumLayers(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetNumLayers
            
        """
        pass

    def SetWeldWorksheetOffsetLayerGrowthRate(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetOffsetLayerGrowthRate method.
        """
        pass

    def SetWeldWorksheetHAZGrowthRate(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetHAZGrowthRate method.
        """
        pass

    def GetWeldWorksheetMaxThicknessFactor(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetMaxThicknessFactor
            
        """
        pass

    def SetWeldWorksheetMaxThicknessFactor(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetMaxThicknessFactor method.
        """
        pass

    def GetWeldWorksheetMinThicknessFactor(self, rowIndex: int) -> float:
        """
        
             get the WeldControlWorksheetMinThicknessFactor
            
        """
        pass

    def SetWeldWorksheetMinThicknessFactor(self, rowIndices: typing.Iterable[int], val: float) -> None:
        """
        SetWeldWorksheetMinThicknessFactor method.
        """
        pass

    def GetWeldWorksheetThicknessExpression(self, rowIndex: int) -> str:
        """
        
             get the WeldControlWorksheetThicknessExpression
            
        """
        pass

    def SetWeldWorksheetThicknessExpression(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetThicknessExpression method.
        """
        pass

    def GetWeldWorksheetEdgeMeshSizeExpression(self, rowIndex: int) -> str:
        """
        
             get the WeldControlWorksheetEdgeMeshSizeExpression
            
        """
        pass

    def SetWeldWorksheetEdgeMeshSizeExpression(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetEdgeMeshSizeExpression method.
        """
        pass

    def GetWeldWorksheetWeldWidthExpression(self, rowIndex: int) -> str:
        """
        
             get the WeldControlWorksheetWeldWidth
            
        """
        pass

    def SetWeldWorksheetWeldWidthExpression(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetWeldWidthExpression method.
        """
        pass

    def GetWeldWorksheetWeldHeightExpression(self, rowIndex: int) -> str:
        """
        
             get the WeldControlWorksheetWeldHeight
            
        """
        pass

    def SetWeldWorksheetWeldHeightExpression(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetWeldHeightExpression method.
        """
        pass

    def GetWeldWorksheetHAZDistanceExpressionTopPlate(self, rowIndex: int) -> str:
        """
        
             get WorksheetHAZDistanceExpressionTopPlate
            
        """
        pass

    def GetWeldWorksheetHAZDistanceExpressionBottomPlate(self, rowIndex: int) -> str:
        """
        
             get WorksheetHAZDistanceExpressionBottomPlate
            
        """
        pass

    def GetWeldWorksheetHAZDistanceExpression(self, rowIndex: int) -> str:
        """
        GetWeldWorksheetHAZDistanceExpression method.
        """
        pass

    def SetWeldWorksheetHAZDistanceExpression(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetHAZDistanceExpression method.
        """
        pass

    def SetWeldWorksheetHAZDistanceExpressionTopPlate(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetHAZDistanceExpressionTopPlate method.
        """
        pass

    def SetWeldWorksheetHAZDistanceExpressionBottomPlate(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetHAZDistanceExpressionBottomPlate method.
        """
        pass

    def GetWeldWorksheetWeldCurve(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetWeldCurve
            
        """
        pass

    def SetWeldWorksheetWeldCurve(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetWeldCurve method.
        """
        pass

    def SetWeldWorksheetWeldBody(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetWeldBody method.
        """
        pass

    def DeactivateProblematicWorksheetEntries(self) -> None:
        """
        
             Deactivate Problematic Worksheet Entries
            
        """
        pass

    def GetWeldWorksheetEdges(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetEdges
            
        """
        pass

    def SetWeldWorksheetEdges(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetEdges method.
        """
        pass

    def GetWeldWorksheetMaterialId(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetMaterialId
            
        """
        pass

    def SetWeldWorksheetMaterialId(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetMaterialId method.
        """
        pass

    def GetWeldWorksheetCrossSectionId(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetCrossSectionId
            
        """
        pass

    def SetWeldWorksheetCrossSectionId(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetCrossSectionId method.
        """
        pass

    def GetWeldWorksheetBottomEntities(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetBottomEntities
            
        """
        pass

    def SetWeldWorksheetBottomEntities(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetBottomEntities method.
        """
        pass

    def GetWeldWorksheetIntersectionTag(self, rowIndex: int) -> str:
        """
        
             get the WeldControlWorksheetIntersectionTag
            
        """
        pass

    def SetWeldWorksheetIntersectionTag(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        SetWeldWorksheetIntersectionTag method.
        """
        pass

    def ClearWeldWorksheetIntersectionTag(self, rowIndices: typing.Iterable[int]) -> None:
        """
        ClearWeldWorksheetIntersectionTag method.
        """
        pass

    def AppendWeldWorksheetIntersectionTag(self, rowIndices: typing.Iterable[int], val: str) -> None:
        """
        AppendWeldWorksheetIntersectionTag method.
        """
        pass

    def GetWeldWorksheetTopEntities(self, rowIndex: int) -> int:
        """
        
             get the WeldControlWorksheetTopEntities
            
        """
        pass

    def SetWeldWorksheetTopEntities(self, rowIndices: typing.Iterable[int], val: int) -> None:
        """
        SetWeldWorksheetTopEntities method.
        """
        pass

    def GetCrossSectionIds(self, rowIndex: int) -> Ansys.Common.Interop.AnsCoreObjects.IAnsUINTColl:
        """
        
             get CrossSection Ids
            
        """
        pass

    def GetMaterialIds(self, rowIndex: int) -> Ansys.Common.Interop.AnsCoreObjects.IAnsUINTColl:
        """
        
             get Material Ids
            
        """
        pass

    def WeldWorksheetAddEntry(self) -> None:
        """
        
             add an entry to WeldWorksheet
            
        """
        pass

    def WeldWorksheetDeleteEntry(self, indices: typing.Iterable[int]) -> None:
        """
        WeldWorksheetDeleteEntry method.
        """
        pass

    def WeldWorksheetImport(self, fileName: str) -> None:
        """
        
             import WeldWorksheet
            
        """
        pass

    def WeldWorksheetExport(self, fileName: str) -> None:
        """
        
             export WeldWorksheet
            
        """
        pass

    def WeldWorksheetCreateControlForCurveBodies(self) -> None:
        """
        
             Create worksheet entries for all curve bodies
            
        """
        pass

    def WeldWorksheetCreateControlForSolidBodies(self) -> None:
        """
        
             Create worksheet entries for solid bodies
            
        """
        pass

    def AddWeldWorksheetScopeToSelection(self, index: int, subset: int) -> bool:
        """
        
             Create worksheet entry scope to selection
            
        """
        pass

    def PromoteToWeldControl(self, indices: typing.Iterable[int]) -> int:
        """
        PromoteToWeldControl method.
        """
        pass

    def PreviewMeshOnWeldWorksheet(self, rowIndices: typing.Iterable[int]) -> None:
        """
        PreviewMeshOnWeldWorksheet method.
        """
        pass

    def PreviewGeometryOnWeldWorksheet(self, rowIndices: typing.Iterable[int]) -> None:
        """
        PreviewGeometryOnWeldWorksheet method.
        """
        pass

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Sizing(object):
    """
    Defines a Sizing.
    """

    @property
    def BodyOfInfluence(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets the BodyOfInfluence.
        """
        return None

    @BodyOfInfluence.setter
    def BodyOfInfluence(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets the BodyOfInfluence.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def BiasGrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the BiasGrowthRate.
        """
        return None

    @BiasGrowthRate.setter
    def BiasGrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the BiasGrowthRate.
        """
        pass

    @property
    def NumberOfDivisions(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfDivisions.
        """
        return None

    @NumberOfDivisions.setter
    def NumberOfDivisions(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfDivisions.
        """
        pass

    @property
    def GrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the GrowthRate.
        """
        return None

    @GrowthRate.setter
    def GrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GrowthRate.
        """
        pass

    @property
    def BiasFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the BiasFactor.
        """
        return None

    @BiasFactor.setter
    def BiasFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the BiasFactor.
        """
        pass

    @property
    def ElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElementSize.
        """
        return None

    @ElementSize.setter
    def ElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElementSize.
        """
        pass

    @property
    def SphereRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SphereRadius.
        """
        return None

    @SphereRadius.setter
    def SphereRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SphereRadius.
        """
        pass

    @property
    def DefeatureSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DefeatureSize.
        """
        return None

    @DefeatureSize.setter
    def DefeatureSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DefeatureSize.
        """
        pass

    @property
    def LocalMinimumSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the LocalMinimumSize.
        """
        return None

    @LocalMinimumSize.setter
    def LocalMinimumSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the LocalMinimumSize.
        """
        pass

    @property
    def ProximityGapFactor(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ProximityGapFactor.
        """
        return None

    @ProximityGapFactor.setter
    def ProximityGapFactor(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ProximityGapFactor.
        """
        pass

    @property
    def ProximityMinimumSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ProximityMinimumSize.
        """
        return None

    @ProximityMinimumSize.setter
    def ProximityMinimumSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ProximityMinimumSize.
        """
        pass

    @property
    def CurvatureNormalAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        return None

    @CurvatureNormalAngle.setter
    def CurvatureNormalAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        pass

    @property
    def OriginX(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the OriginX.
        """
        return None

    @property
    def OriginY(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the OriginY.
        """
        return None

    @property
    def OriginZ(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the OriginZ.
        """
        return None

    @property
    def BiasOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasOptionType]:
        """
        Gets or sets the BiasOption.
        """
        return None

    @BiasOption.setter
    def BiasOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasOptionType]) -> None:
        """
        Gets or sets the BiasOption.
        """
        pass

    @property
    def ProximitySizeSources(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ProximitySFSourcesType]:
        """
        Gets or sets the ProximitySizeSources.
        """
        return None

    @ProximitySizeSources.setter
    def ProximitySizeSources(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ProximitySFSourcesType]) -> None:
        """
        Gets or sets the ProximitySizeSources.
        """
        pass

    @property
    def Behavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SizingBehavior]:
        """
        Gets or sets the Behavior.
        """
        return None

    @Behavior.setter
    def Behavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SizingBehavior]) -> None:
        """
        Gets or sets the Behavior.
        """
        pass

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SizingType]:
        """
        Gets or sets the Type.
        """
        return None

    @Type.setter
    def Type(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SizingType]) -> None:
        """
        Gets or sets the Type.
        """
        pass

    @property
    def BiasType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasType]:
        """
        Gets or sets the BiasType.
        """
        return None

    @BiasType.setter
    def BiasType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasType]) -> None:
        """
        Gets or sets the BiasType.
        """
        pass

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Gets the Active.
        """
        return None

    @property
    def CaptureCurvature(self) -> typing.Optional[bool]:
        """
        Gets or sets the CaptureCurvature.
        """
        return None

    @CaptureCurvature.setter
    def CaptureCurvature(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CaptureCurvature.
        """
        pass

    @property
    def CaptureProximity(self) -> typing.Optional[bool]:
        """
        Gets or sets the CaptureProximity.
        """
        return None

    @CaptureProximity.setter
    def CaptureProximity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CaptureProximity.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

    @property
    def SphereCenter(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the SphereCenter.
        """
        return None

    @SphereCenter.setter
    def SphereCenter(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the SphereCenter.
        """
        pass

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
    def ReverseBias(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReverseBias.
        """
        return None

    @ReverseBias.setter
    def ReverseBias(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReverseBias.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class AutomaticMethod(object):
    """
    Defines a AutomaticMethod.
    """

    @property
    def AggressiveInflateOption(self) -> typing.Optional[bool]:
        """
        Gets or sets the AggressiveInflateOption.
        """
        return None

    @AggressiveInflateOption.setter
    def AggressiveInflateOption(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AggressiveInflateOption.
        """
        pass

    @property
    def AggressiveTetImprovement(self) -> typing.Optional[bool]:
        """
        Gets or sets the AggressiveTetImprovement.
        """
        return None

    @AggressiveTetImprovement.setter
    def AggressiveTetImprovement(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AggressiveTetImprovement.
        """
        pass

    @property
    def ControlMessages(self) -> typing.Optional[bool]:
        """
        Gets the ControlMessages.
        """
        return None

    @property
    def CornerAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CornerAngle.
        """
        return None

    @CornerAngle.setter
    def CornerAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CornerAngle.
        """
        pass

    @property
    def DefeatureLayerVolume(self) -> typing.Optional[float]:
        """
        Gets or sets the DefeatureLayerVolume.
        """
        return None

    @DefeatureLayerVolume.setter
    def DefeatureLayerVolume(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DefeatureLayerVolume.
        """
        pass

    @property
    def ElementMidsideNodes(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementMidsideNodesType]:
        """
        Gets or sets the ElementMidsideNodes.
        """
        return None

    @ElementMidsideNodes.setter
    def ElementMidsideNodes(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementMidsideNodesType]) -> None:
        """
        Gets or sets the ElementMidsideNodes.
        """
        pass

    @property
    def ElementOrder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementOrder]:
        """
        Gets or sets the ElementOrder.
        """
        return None

    @ElementOrder.setter
    def ElementOrder(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementOrder]) -> None:
        """
        Gets or sets the ElementOrder.
        """
        pass

    @property
    def GenerateLayersUsingFacets(self) -> typing.Optional[bool]:
        """
        Gets or sets the GenerateLayersUsingFacets.
        """
        return None

    @GenerateLayersUsingFacets.setter
    def GenerateLayersUsingFacets(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GenerateLayersUsingFacets.
        """
        pass

    @property
    def InflateRelativeTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the InflateRelativeTolerance.
        """
        return None

    @InflateRelativeTolerance.setter
    def InflateRelativeTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the InflateRelativeTolerance.
        """
        pass

    @property
    def LayerHeight(self) -> typing.Optional[float]:
        """
        Gets or sets the LayerHeight.
        """
        return None

    @LayerHeight.setter
    def LayerHeight(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the LayerHeight.
        """
        pass

    @property
    def LayerStart(self) -> typing.Optional[float]:
        """
        Gets or sets the LayerStart.
        """
        return None

    @LayerStart.setter
    def LayerStart(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the LayerStart.
        """
        pass

    @property
    def MeshInCenter(self) -> typing.Optional[int]:
        """
        Gets or sets the MeshInCenter.
        """
        return None

    @MeshInCenter.setter
    def MeshInCenter(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MeshInCenter.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MethodType]:
        """
        Gets or sets the Method.
        """
        return None

    @Method.setter
    def Method(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MethodType]) -> None:
        """
        Gets or sets the Method.
        """
        pass

    @property
    def OverlappingAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the OverlappingAngle.
        """
        return None

    @OverlappingAngle.setter
    def OverlappingAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the OverlappingAngle.
        """
        pass

    @property
    def ProjectCornersToTop(self) -> typing.Optional[bool]:
        """
        Gets or sets the ProjectCornersToTop.
        """
        return None

    @ProjectCornersToTop.setter
    def ProjectCornersToTop(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ProjectCornersToTop.
        """
        pass

    @property
    def RelativeTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the PrimeRelativeTolerance.
        """
        return None

    @RelativeTolerance.setter
    def RelativeTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PrimeRelativeTolerance.
        """
        pass

    @property
    def RepairFacets(self) -> typing.Optional[bool]:
        """
        Gets or sets the RepairFacets.
        """
        return None

    @RepairFacets.setter
    def RepairFacets(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the RepairFacets.
        """
        pass

    @property
    def SlicerFeatureAngle(self) -> typing.Optional[float]:
        """
        Gets or sets the SlicerFeatureAngle.
        """
        return None

    @SlicerFeatureAngle.setter
    def SlicerFeatureAngle(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the SlicerFeatureAngle.
        """
        pass

    @property
    def SliverTriangleHeight(self) -> typing.Optional[float]:
        """
        Gets or sets the SliverTriangleHeight.
        """
        return None

    @SliverTriangleHeight.setter
    def SliverTriangleHeight(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the SliverTriangleHeight.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ProjectionFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ProjectionFactor.
        """
        return None

    @ProjectionFactor.setter
    def ProjectionFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ProjectionFactor.
        """
        pass

    @property
    def StretchFactorX(self) -> typing.Optional[float]:
        """
        Gets or sets the StretchFactorX.
        """
        return None

    @StretchFactorX.setter
    def StretchFactorX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StretchFactorX.
        """
        pass

    @property
    def StretchFactorY(self) -> typing.Optional[float]:
        """
        Gets or sets the StretchFactorY.
        """
        return None

    @StretchFactorY.setter
    def StretchFactorY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StretchFactorY.
        """
        pass

    @property
    def StretchFactorZ(self) -> typing.Optional[float]:
        """
        Gets or sets the StretchFactorZ.
        """
        return None

    @StretchFactorZ.setter
    def StretchFactorZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StretchFactorZ.
        """
        pass

    @property
    def SpacingOption(self) -> typing.Optional[int]:
        """
        Gets or sets the SpacingOption.
        """
        return None

    @SpacingOption.setter
    def SpacingOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SpacingOption.
        """
        pass

    @property
    def SubsampleRate(self) -> typing.Optional[int]:
        """
        Gets or sets the SubsampleRate.
        """
        return None

    @SubsampleRate.setter
    def SubsampleRate(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SubsampleRate.
        """
        pass

    @property
    def BFCartSubType(self) -> typing.Optional[int]:
        """
        Gets the BFCartSubType.
        """
        return None

    @property
    def Refinement(self) -> typing.Optional[int]:
        """
        Gets or sets the Refinement.
        """
        return None

    @Refinement.setter
    def Refinement(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Refinement.
        """
        pass

    @property
    def FillingFraction(self) -> typing.Optional[float]:
        """
        Gets or sets the FillingFraction.
        """
        return None

    @FillingFraction.setter
    def FillingFraction(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FillingFraction.
        """
        pass

    @property
    def ApproximativeNumberOfElementsPerPart(self) -> typing.Optional[int]:
        """
        Gets or sets the ApproximativeNumberOfElementsPerPart.
        """
        return None

    @ApproximativeNumberOfElementsPerPart.setter
    def ApproximativeNumberOfElementsPerPart(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ApproximativeNumberOfElementsPerPart.
        """
        pass

    @property
    def CartSweepSpacingOption(self) -> typing.Optional[int]:
        """
        Gets or sets the  CartSweep SpacingOption in Multizone ( 0 = Uniform, 1 = Key-Points).
        """
        return None

    @CartSweepSpacingOption.setter
    def CartSweepSpacingOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the  CartSweep SpacingOption in Multizone ( 0 = Uniform, 1 = Key-Points).
        """
        pass

    @property
    def SurfaceMeshMethod(self) -> typing.Optional[int]:
        """
        Gets or sets the SurfaceMeshMethod.
        """
        return None

    @SurfaceMeshMethod.setter
    def SurfaceMeshMethod(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SurfaceMeshMethod.
        """
        pass

    @property
    def MZSweepNumberDivisions(self) -> typing.Optional[int]:
        return None

    @MZSweepNumberDivisions.setter
    def MZSweepNumberDivisions(self, value: typing.Optional[int]) -> None:
        pass

    @property
    def SweepNumberDivisions(self) -> typing.Optional[int]:
        """
        Gets or sets the SweepNumberDivisions.
        """
        return None

    @SweepNumberDivisions.setter
    def SweepNumberDivisions(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SweepNumberDivisions.
        """
        pass

    @property
    def NumberOfCellsAcrossGap(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfCellsAcrossGap.
        """
        return None

    @NumberOfCellsAcrossGap.setter
    def NumberOfCellsAcrossGap(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfCellsAcrossGap.
        """
        pass

    @property
    def FaceProximityGapFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the FaceProximityGapFactor for PCTet.
        """
        return None

    @FaceProximityGapFactor.setter
    def FaceProximityGapFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FaceProximityGapFactor for PCTet.
        """
        pass

    @property
    def FilletCollapse(self) -> typing.Optional[int]:
        """
        Gets or sets the FilletCollapse for AutoNodeMove under PCTet ( 0 = No, 1 = ProgramControlled ).
        """
        return None

    @FilletCollapse.setter
    def FilletCollapse(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the FilletCollapse for AutoNodeMove under PCTet ( 0 = No, 1 = ProgramControlled ).
        """
        pass

    @property
    def ImprovementIterations(self) -> typing.Optional[int]:
        """
        Gets or sets the ImprovementIterations for AutoNodeMove under PCTet.
        """
        return None

    @ImprovementIterations.setter
    def ImprovementIterations(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ImprovementIterations for AutoNodeMove under PCTet.
        """
        pass

    @property
    def NumberOfElementLayers(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfElementLayers for PCTet.
        """
        return None

    @NumberOfElementLayers.setter
    def NumberOfElementLayers(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfElementLayers for PCTet.
        """
        pass

    @property
    def TetraGrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the TetraGrowthRate.
        """
        return None

    @TetraGrowthRate.setter
    def TetraGrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TetraGrowthRate.
        """
        pass

    @property
    def PreserveBoundaries(self) -> typing.Optional[int]:
        """
        Gets or sets the PreserveBoundaries.
        """
        return None

    @PreserveBoundaries.setter
    def PreserveBoundaries(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PreserveBoundaries.
        """
        pass

    @property
    def SourceTargetSelection(self) -> typing.Optional[int]:
        """
        Gets or sets the SourceTargetSelection.
        """
        return None

    @SourceTargetSelection.setter
    def SourceTargetSelection(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SourceTargetSelection.
        """
        pass

    @property
    def LateralDefeatureSize(self) -> typing.Optional[float]:
        """
        Gets or sets the LateralDefeatureSize.
        """
        return None

    @LateralDefeatureSize.setter
    def LateralDefeatureSize(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the LateralDefeatureSize.
        """
        pass

    @property
    def StackingDefeatureSize(self) -> typing.Optional[float]:
        """
        Gets or sets the StackingDefeatureSize.
        """
        return None

    @StackingDefeatureSize.setter
    def StackingDefeatureSize(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StackingDefeatureSize.
        """
        pass

    @property
    def FreeMeshType(self) -> typing.Optional[int]:
        """
        Gets or sets the FreeMeshType.
        """
        return None

    @FreeMeshType.setter
    def FreeMeshType(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the FreeMeshType.
        """
        pass

    @property
    def MappedSweptType(self) -> typing.Optional[int]:
        """
        Gets or sets the MappedSweptType.
        """
        return None

    @MappedSweptType.setter
    def MappedSweptType(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MappedSweptType.
        """
        pass

    @property
    def SweepBiasValue(self) -> typing.Optional[float]:
        """
        Gets or sets the SweepBiasValue.
        """
        return None

    @SweepBiasValue.setter
    def SweepBiasValue(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the SweepBiasValue.
        """
        pass

    @property
    def SweepESizeType(self) -> typing.Optional[int]:
        """
        Gets or sets the SweepESizeType.
        """
        return None

    @SweepESizeType.setter
    def SweepESizeType(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SweepESizeType.
        """
        pass

    @property
    def RadialGrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the RadialGrowthRate.
        """
        return None

    @RadialGrowthRate.setter
    def RadialGrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the RadialGrowthRate.
        """
        pass

    @property
    def FreeFaceMeshType(self) -> typing.Optional[int]:
        """
        Gets or sets the FreeFaceMeshType.
        """
        return None

    @FreeFaceMeshType.setter
    def FreeFaceMeshType(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the FreeFaceMeshType.
        """
        pass

    @property
    def SweepSizeBehavior(self) -> typing.Optional[int]:
        """
        Gets or sets the SweepSizeBehavior.
        """
        return None

    @SweepSizeBehavior.setter
    def SweepSizeBehavior(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SweepSizeBehavior.
        """
        pass

    @property
    def AutoPinchTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AutoPinchTolerance.
        """
        return None

    @AutoPinchTolerance.setter
    def AutoPinchTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AutoPinchTolerance.
        """
        pass

    @property
    def AutoRepairFeatureAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AutoRepairFeatureAngle.
        """
        return None

    @AutoRepairFeatureAngle.setter
    def AutoRepairFeatureAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AutoRepairFeatureAngle.
        """
        pass

    @property
    def AutoSharpAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AutoSharpAngle.
        """
        return None

    @AutoSharpAngle.setter
    def AutoSharpAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AutoSharpAngle.
        """
        pass

    @property
    def AutoShortEdgeLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AutoShortEdgeLength.
        """
        return None

    @AutoShortEdgeLength.setter
    def AutoShortEdgeLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AutoShortEdgeLength.
        """
        pass

    @property
    def AutoThinFaceWidth(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AutoThinFaceWidth.
        """
        return None

    @AutoThinFaceWidth.setter
    def AutoThinFaceWidth(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AutoThinFaceWidth.
        """
        pass

    @property
    def WallThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WallThickness.
        """
        return None

    @WallThickness.setter
    def WallThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WallThickness.
        """
        pass

    @property
    def BFCartTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BFCartTolerance.
        """
        return None

    @property
    def CartesianSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CartesianSize in Multizone.
        """
        return None

    @CartesianSize.setter
    def CartesianSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CartesianSize in Multizone.
        """
        pass

    @property
    def CurvatureNormalAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        return None

    @CurvatureNormalAngle.setter
    def CurvatureNormalAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        pass

    @property
    def Clearence(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Clearence.
        """
        return None

    @Clearence.setter
    def Clearence(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Clearence.
        """
        pass

    @property
    def SweepElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepElementSize.
        """
        return None

    @SweepElementSize.setter
    def SweepElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepElementSize.
        """
        pass

    @property
    def MaximumElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumElementSize.
        """
        return None

    @MaximumElementSize.setter
    def MaximumElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumElementSize.
        """
        pass

    @property
    def MinimumSizeLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumSizeLimit.
        """
        return None

    @MinimumSizeLimit.setter
    def MinimumSizeLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumSizeLimit.
        """
        pass

    @property
    def KeyPointsTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the KeyPoints Tolerance in Multizone.
        """
        return None

    @KeyPointsTolerance.setter
    def KeyPointsTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the KeyPoints Tolerance in Multizone.
        """
        pass

    @property
    def MinimumEdgeLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MinimumEdgeLength.
        """
        return None

    @property
    def DefeaturingTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DefeaturingTolerance.
        """
        return None

    @DefeaturingTolerance.setter
    def DefeaturingTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DefeaturingTolerance.
        """
        pass

    @property
    def ParticleDiameter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ParticleDiameter.
        """
        return None

    @ParticleDiameter.setter
    def ParticleDiameter(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ParticleDiameter.
        """
        pass

    @property
    def FeatureProtectionAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DihedralAngle for AutoNodeMove under PCTet.
        """
        return None

    @FeatureProtectionAngle.setter
    def FeatureProtectionAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DihedralAngle for AutoNodeMove under PCTet.
        """
        pass

    @property
    def MinimumThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumThickness for PCTet.
        """
        return None

    @MinimumThickness.setter
    def MinimumThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumThickness for PCTet.
        """
        pass

    @property
    def FeatureAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FeatureAngle.
        """
        return None

    @FeatureAngle.setter
    def FeatureAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FeatureAngle.
        """
        pass

    @property
    def PrimeRepairTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets repair tolerance length for Prime meshing. This can be used to reduce variability of output topology, prevent the collapse and defeature of thin or short topologies, and allow the creation of a coarse mesh while keeping topology as-is.
        """
        return None

    @PrimeRepairTolerance.setter
    def PrimeRepairTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets repair tolerance length for Prime meshing. This can be used to reduce variability of output topology, prevent the collapse and defeature of thin or short topologies, and allow the creation of a coarse mesh while keeping topology as-is.
        """
        pass

    @property
    def SplitAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SplitAngle in Multizone.
        """
        return None

    @SplitAngle.setter
    def SplitAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SplitAngle in Multizone.
        """
        pass

    @property
    def SweepThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepThickness in Multizone.
        """
        return None

    @SweepThickness.setter
    def SweepThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepThickness in Multizone.
        """
        pass

    @property
    def AutoCollapseShortEdges(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the AutoCollapseShortEdges.
        """
        return None

    @AutoCollapseShortEdges.setter
    def AutoCollapseShortEdges(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the AutoCollapseShortEdges.
        """
        pass

    @property
    def AutoPinchFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the AutoPinchFaces.
        """
        return None

    @AutoPinchFaces.setter
    def AutoPinchFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the AutoPinchFaces.
        """
        pass

    @property
    def RemoveSharpAngleFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the RemoveSharpAngleFaces.
        """
        return None

    @RemoveSharpAngleFaces.setter
    def RemoveSharpAngleFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the RemoveSharpAngleFaces.
        """
        pass

    @property
    def AutoRemoveThinFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the AutoRemoveThinFaces.
        """
        return None

    @AutoRemoveThinFaces.setter
    def AutoRemoveThinFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the AutoRemoveThinFaces.
        """
        pass

    @property
    def AutoRepairPartialDefeature(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the use of partial defeature, which partially removes thin faces and sharp angles within provided tolerances, such that only topology impacting mesh quality is removed.
        """
        return None

    @AutoRepairPartialDefeature.setter
    def AutoRepairPartialDefeature(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the use of partial defeature, which partially removes thin faces and sharp angles within provided tolerances, such that only topology impacting mesh quality is removed.
        """
        pass

    @property
    def KeyPointsSelection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]:
        """
        Gets or sets the KeyPointsSelection.
        """
        return None

    @KeyPointsSelection.setter
    def KeyPointsSelection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]) -> None:
        """
        Gets or sets the KeyPointsSelection.
        """
        pass

    @property
    def BodyStackingType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BodyStackingType]:
        """
        Gets or sets the BodyStackingType.
        """
        return None

    @BodyStackingType.setter
    def BodyStackingType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BodyStackingType]) -> None:
        """
        Gets or sets the BodyStackingType.
        """
        pass

    @property
    def FillingDirection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CoordinateSystemAxisType]:
        """
        Gets or sets the FillingDirection.
        """
        return None

    @FillingDirection.setter
    def FillingDirection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CoordinateSystemAxisType]) -> None:
        """
        Gets or sets the FillingDirection.
        """
        pass

    @property
    def DefinedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.PatchIndependentDefineType]:
        """
        Gets or sets the DefinedBy.
        """
        return None

    @DefinedBy.setter
    def DefinedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.PatchIndependentDefineType]) -> None:
        """
        Gets or sets the DefinedBy.
        """
        pass

    @property
    def ElementOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SweepElementOptionType]:
        """
        Gets or sets the ElementOption.
        """
        return None

    @ElementOption.setter
    def ElementOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SweepElementOptionType]) -> None:
        """
        Gets or sets the ElementOption.
        """
        pass

    @property
    def DecompositionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DecompositionType]:
        """
        Gets or sets the DecompositionType in Multizone.
        """
        return None

    @DecompositionType.setter
    def DecompositionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DecompositionType]) -> None:
        """
        Gets or sets the DecompositionType in Multizone.
        """
        pass

    @property
    def AutomaticNodeMovement(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticNodeMovementMethod]:
        """
        Gets or sets the AutomaticNodeMovement method under PCTet.
        """
        return None

    @AutomaticNodeMovement.setter
    def AutomaticNodeMovement(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticNodeMovementMethod]) -> None:
        """
        Gets or sets the AutomaticNodeMovement method under PCTet.
        """
        pass

    @property
    def PrimeMethodAutoRepair(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the PrimeMethodAutoRepair.
        """
        return None

    @PrimeMethodAutoRepair.setter
    def PrimeMethodAutoRepair(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the PrimeMethodAutoRepair.
        """
        pass

    @property
    def MeshFlowControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshFlowControlMethod]:
        """
        Gets or sets the MeshFlowControl.
        """
        return None

    @MeshFlowControl.setter
    def MeshFlowControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshFlowControlMethod]) -> None:
        """
        Gets or sets the MeshFlowControl.
        """
        pass

    @property
    def MeshType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MethodMeshType]:
        """
        Gets or sets the MeshType.
        """
        return None

    @MeshType.setter
    def MeshType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MethodMeshType]) -> None:
        """
        Gets or sets the MeshType.
        """
        pass

    @property
    def TriangleReduction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]:
        """
        Gets or sets the TriangleReduction.
        """
        return None

    @TriangleReduction.setter
    def TriangleReduction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]) -> None:
        """
        Gets or sets the TriangleReduction.
        """
        pass

    @property
    def SolidShellElementForStacker(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]:
        """
        Gets or sets the SolidShellElementForStacker.
        """
        return None

    @SolidShellElementForStacker.setter
    def SolidShellElementForStacker(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoType]) -> None:
        """
        Gets or sets the SolidShellElementForStacker.
        """
        pass

    @property
    def SolidShellElementForStackerScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the SolidShellElementForStackerScopingMethod.
        """
        return None

    @SolidShellElementForStackerScopingMethod.setter
    def SolidShellElementForStackerScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the SolidShellElementForStackerScopingMethod.
        """
        pass

    @property
    def SrcTrgScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Sets Scoping method for Source/Target selection for MultiZone control.
        """
        return None

    @SrcTrgScopingMethod.setter
    def SrcTrgScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Sets Scoping method for Source/Target selection for MultiZone control.
        """
        pass

    @property
    def StackingAxis(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CoordinateSystemAxisType]:
        """
        Gets or sets the StackingAxis.
        """
        return None

    @StackingAxis.setter
    def StackingAxis(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CoordinateSystemAxisType]) -> None:
        """
        Gets or sets the StackingAxis.
        """
        pass

    @property
    def StackerFreeFaceMeshType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StackerMethodMeshType]:
        """
        Gets or sets the StackerFreeFaceMeshType.
        """
        return None

    @StackerFreeFaceMeshType.setter
    def StackerFreeFaceMeshType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StackerMethodMeshType]) -> None:
        """
        Gets or sets the StackerFreeFaceMeshType.
        """
        pass

    @property
    def StackerTriangleReduction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]:
        """
        Gets or sets the StackerTriangleReduction.
        """
        return None

    @StackerTriangleReduction.setter
    def StackerTriangleReduction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]) -> None:
        """
        Gets or sets the StackerTriangleReduction.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshMethodAlgorithm]:
        """
        Gets or sets the Algorithm.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshMethodAlgorithm]) -> None:
        """
        Gets or sets the Algorithm.
        """
        pass

    @property
    def SweepBiasType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasType]:
        """
        Gets or sets the SweepBiasType.
        """
        return None

    @SweepBiasType.setter
    def SweepBiasType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BiasType]) -> None:
        """
        Gets or sets the SweepBiasType.
        """
        pass

    @property
    def FallBackMeshType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SweepAxisymmetricFallBackMeshType]:
        """
        Gets or sets the FallBackMeshType.
        """
        return None

    @FallBackMeshType.setter
    def FallBackMeshType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SweepAxisymmetricFallBackMeshType]) -> None:
        """
        Gets or sets the FallBackMeshType.
        """
        pass

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Gets the Active.
        """
        return None

    @property
    def ProjectInConstantZPlane(self) -> typing.Optional[bool]:
        """
        Gets or sets the ProjectInConstantZPlane.
        """
        return None

    @ProjectInConstantZPlane.setter
    def ProjectInConstantZPlane(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ProjectInConstantZPlane.
        """
        pass

    @property
    def MeshUsingVoxelization(self) -> typing.Optional[bool]:
        """
        Gets or sets the MeshUsingVoxelization.
        """
        return None

    @MeshUsingVoxelization.setter
    def MeshUsingVoxelization(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MeshUsingVoxelization.
        """
        pass

    @property
    def ConstrainBoundary(self) -> typing.Optional[bool]:
        """
        Gets or sets the ConstrainBoundary.
        """
        return None

    @ConstrainBoundary.setter
    def ConstrainBoundary(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ConstrainBoundary.
        """
        pass

    @property
    def MeshBasedDefeaturing(self) -> typing.Optional[bool]:
        """
        Gets or sets the MeshBasedDefeaturing.
        """
        return None

    @MeshBasedDefeaturing.setter
    def MeshBasedDefeaturing(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MeshBasedDefeaturing.
        """
        pass

    @property
    def PartialFill(self) -> typing.Optional[bool]:
        """
        Gets or sets the PartialFill.
        """
        return None

    @PartialFill.setter
    def PartialFill(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PartialFill.
        """
        pass

    @property
    def MatchMeshWherePossible(self) -> typing.Optional[bool]:
        """
        Gets or sets the MatchMeshWherePossible.
        """
        return None

    @MatchMeshWherePossible.setter
    def MatchMeshWherePossible(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MatchMeshWherePossible.
        """
        pass

    @property
    def SmoothMeshSpacing(self) -> typing.Optional[bool]:
        """
        Gets or sets the SmoothMeshSpacing in Multizone.
        """
        return None

    @SmoothMeshSpacing.setter
    def SmoothMeshSpacing(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SmoothMeshSpacing in Multizone.
        """
        pass

    @property
    def RefineAtThinSection(self) -> typing.Optional[bool]:
        """
        Gets or sets the RefineAtThinSection for PCTet.
        """
        return None

    @RefineAtThinSection.setter
    def RefineAtThinSection(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the RefineAtThinSection for PCTet.
        """
        pass

    @property
    def RefineSurfaceMesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the RefineSurfaceMesh for PCTet.
        """
        return None

    @RefineSurfaceMesh.setter
    def RefineSurfaceMesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the RefineSurfaceMesh for PCTet.
        """
        pass

    @property
    def RestrictNodeMovementsToSurface(self) -> typing.Optional[bool]:
        """
        Gets or sets the RestrictNodeMovementsToSurface for AutoNodeMove under PCTet.
        """
        return None

    @RestrictNodeMovementsToSurface.setter
    def RestrictNodeMovementsToSurface(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the RestrictNodeMovementsToSurface for AutoNodeMove under PCTet.
        """
        pass

    @property
    def ShowAdvancedImproveOptions(self) -> typing.Optional[bool]:
        """
        Gets or sets the ShowAdvancedImproveOptions for AutoNodeMove under PCTet.
        """
        return None

    @ShowAdvancedImproveOptions.setter
    def ShowAdvancedImproveOptions(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ShowAdvancedImproveOptions for AutoNodeMove under PCTet.
        """
        pass

    @property
    def SmoothTransition(self) -> typing.Optional[bool]:
        """
        Gets or sets the SmoothTransition.
        """
        return None

    @SmoothTransition.setter
    def SmoothTransition(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SmoothTransition.
        """
        pass

    @property
    def ReuseBlocking(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReuseBlocking.
        """
        return None

    @ReuseBlocking.setter
    def ReuseBlocking(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReuseBlocking.
        """
        pass

    @property
    def UseSplitAngle(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseSplitAngle in Multizone.
        """
        return None

    @UseSplitAngle.setter
    def UseSplitAngle(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseSplitAngle in Multizone.
        """
        pass

    @property
    def WriteICEMCFDFiles(self) -> typing.Optional[bool]:
        """
        Gets or sets the WriteICEMCFDFiles.
        """
        return None

    @WriteICEMCFDFiles.setter
    def WriteICEMCFDFiles(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the WriteICEMCFDFiles.
        """
        pass

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

    @property
    def ParticleCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ParticleCoordinateSystem.
        """
        return None

    @ParticleCoordinateSystem.setter
    def ParticleCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ParticleCoordinateSystem.
        """
        pass

    @property
    def SolidShellElementForStackerNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the SolidShellElementForStackerNamedSelection.
        """
        return None

    @SolidShellElementForStackerNamedSelection.setter
    def SolidShellElementForStackerNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the SolidShellElementForStackerNamedSelection.
        """
        pass

    @property
    def SrcTrgNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Sets Named selection as Source/Target for MultiZone control.
        """
        return None

    @SrcTrgNamedSelection.setter
    def SrcTrgNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Sets Named selection as Source/Target for MultiZone control.
        """
        pass

    @property
    def StackerCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the StackerCoordinateSystem.
        """
        return None

    @StackerCoordinateSystem.setter
    def StackerCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the StackerCoordinateSystem.
        """
        pass

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
    def SolidShellElementForStackerGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SolidShellElementForStackerGeometrySelection.
        """
        return None

    @SolidShellElementForStackerGeometrySelection.setter
    def SolidShellElementForStackerGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SolidShellElementForStackerGeometrySelection.
        """
        pass

    @property
    def SourceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SourceLocation.
        """
        return None

    @SourceLocation.setter
    def SourceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SourceLocation.
        """
        pass

    @property
    def SweepEdges(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SweepEdges.
        """
        return None

    @SweepEdges.setter
    def SweepEdges(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SweepEdges.
        """
        pass

    @property
    def TargetLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the TargetLocation.
        """
        return None

    @TargetLocation.setter
    def TargetLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the TargetLocation.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Inflation(object):
    """
    Defines a Inflation.
    """

    @property
    def BoundaryLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the BoundaryLocation.
        """
        return None

    @BoundaryLocation.setter
    def BoundaryLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the BoundaryLocation.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def GrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the GrowthRate.
        """
        return None

    @GrowthRate.setter
    def GrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GrowthRate.
        """
        pass

    @property
    def InflationAlgorithm(self) -> typing.Optional[int]:
        """
        Gets or sets the InflationAlgorithm.
        """
        return None

    @InflationAlgorithm.setter
    def InflationAlgorithm(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InflationAlgorithm.
        """
        pass

    @property
    def InflationOption(self) -> typing.Optional[int]:
        """
        Gets or sets the InflationOption.
        """
        return None

    @InflationOption.setter
    def InflationOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InflationOption.
        """
        pass

    @property
    def AspectRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the AspectRatio.
        """
        return None

    @AspectRatio.setter
    def AspectRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the AspectRatio.
        """
        pass

    @property
    def MaximumLayers(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumLayers.
        """
        return None

    @MaximumLayers.setter
    def MaximumLayers(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumLayers.
        """
        pass

    @property
    def NumberOfLayers(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfLayers.
        """
        return None

    @NumberOfLayers.setter
    def NumberOfLayers(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfLayers.
        """
        pass

    @property
    def TransitionRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the TransitionRatio.
        """
        return None

    @TransitionRatio.setter
    def TransitionRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TransitionRatio.
        """
        pass

    @property
    def FirstLayerHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FirstLayerHeight.
        """
        return None

    @FirstLayerHeight.setter
    def FirstLayerHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FirstLayerHeight.
        """
        pass

    @property
    def MaximumThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumThickness.
        """
        return None

    @MaximumThickness.setter
    def MaximumThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumThickness.
        """
        pass

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Gets the Active.
        """
        return None

    @property
    def BoundaryNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the BoundaryNamedSelection.
        """
        return None

    @BoundaryNamedSelection.setter
    def BoundaryNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the BoundaryNamedSelection.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Mesh(object):
    """
    Defines a Mesh.
    """

    @property
    def IsMeshing(self) -> typing.Optional[bool]:
        """
        IsMeshing property.
        """
        return None

    @property
    def Worksheet(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IWorksheet]:
        """
        Get the MeshControlWorksheet action.
        """
        return None

    @property
    def MaximumFaceSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaximumFaceSize property.
        """
        return None

    @MaximumFaceSize.setter
    def MaximumFaceSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaximumFaceSize property.
        """
        pass

    @property
    def ElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElementSize.
        """
        return None

    @ElementSize.setter
    def ElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElementSize.
        """
        pass

    @property
    def RigidBodyFaceMeshType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshControlGroupRigidBodyFaceMeshType]:
        """
        Gets or sets the RigidBodyFaceMeshType.
        """
        return None

    @RigidBodyFaceMeshType.setter
    def RigidBodyFaceMeshType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshControlGroupRigidBodyFaceMeshType]) -> None:
        """
        Gets or sets the RigidBodyFaceMeshType.
        """
        pass

    @property
    def RigidBodyBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshControlGroupRigidBodyBehaviorType]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @RigidBodyBehavior.setter
    def RigidBodyBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshControlGroupRigidBodyBehaviorType]) -> None:
        """
        Gets or sets the BoundaryCondition.
        """
        pass

    @property
    def CurrentConfiguration(self) -> typing.Optional[int]:
        """
        Gets the Assembly Mesh's current configuration Id.
        """
        return None

    @property
    def MinimizeNumTriangles(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]:
        """
        Gets or sets the TriangleReduction option for Batch Connections.
        """
        return None

    @MinimizeNumTriangles.setter
    def MinimizeNumTriangles(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TriangleReduction]) -> None:
        """
        Gets or sets the TriangleReduction option for Batch Connections.
        """
        pass

    @property
    def NumberOfShellMeshQualityMetrics(self) -> typing.Optional[int]:
        """
        
            Gets the number of Mesh Quality Metrics
            
        """
        return None

    @property
    def NumberOfSolidMeshQualityMetrics(self) -> typing.Optional[int]:
        """
        NumberOfSolidMeshQualityMetrics property.
        """
        return None

    @property
    def NumberOfSolidSurfaceMeshQualityMetrics(self) -> typing.Optional[int]:
        """
        NumberOfSolidSurfaceMeshQualityMetrics property.
        """
        return None

    @property
    def GetPhysicsPreference(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshPhysicsPreferenceType]:
        """
        GetPhysicsPreference property.
        """
        return None

    @property
    def GlobalUseCustomTargetLimit(self) -> typing.Optional[int]:
        """
        Gets or sets the GlobalUseCustomTargetLimit.
        """
        return None

    @GlobalUseCustomTargetLimit.setter
    def GlobalUseCustomTargetLimit(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the GlobalUseCustomTargetLimit.
        """
        pass

    @property
    def ConnectionToleranceType(self) -> typing.Optional[int]:
        """
        ConnectionToleranceType property.
        """
        return None

    @ConnectionToleranceType.setter
    def ConnectionToleranceType(self, value: typing.Optional[int]) -> None:
        """
        ConnectionToleranceType property.
        """
        pass

    @property
    def LocalConnectionOption(self) -> typing.Optional[int]:
        """
        Gets or sets the LocalConnectionOption.
        """
        return None

    @LocalConnectionOption.setter
    def LocalConnectionOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LocalConnectionOption.
        """
        pass

    @property
    def LocalConnectionTolerance(self) -> typing.Optional[str]:
        """
        Gets or sets the LocalConnectionTolerance.
        """
        return None

    @LocalConnectionTolerance.setter
    def LocalConnectionTolerance(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the LocalConnectionTolerance.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ConnectionTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the ConnectionTolerance.
        """
        return None

    @ConnectionTolerance.setter
    def ConnectionTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ConnectionTolerance.
        """
        pass

    @property
    def ConnectionToleranceList(self) -> typing.Optional[str]:
        """
        Gets or sets the ConnectionToleranceList.
        """
        return None

    @ConnectionToleranceList.setter
    def ConnectionToleranceList(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ConnectionToleranceList.
        """
        pass

    @property
    def UseAdvancedSizeFunction(self) -> typing.Optional[int]:
        """
        Gets or sets the UseAdvancedSizeFunction.
        """
        return None

    @UseAdvancedSizeFunction.setter
    def UseAdvancedSizeFunction(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the UseAdvancedSizeFunction.
        """
        pass

    @property
    def Method(self) -> typing.Optional[int]:
        """
        Gets or sets the Method.
        """
        return None

    @Method.setter
    def Method(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Method.
        """
        pass

    @property
    def UseAutomaticInflation(self) -> typing.Optional[int]:
        """
        Gets or sets the UseAutomaticInflation.
        """
        return None

    @UseAutomaticInflation.setter
    def UseAutomaticInflation(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the UseAutomaticInflation.
        """
        pass

    @property
    def AutomaticMeshBasedDefeaturing(self) -> typing.Optional[int]:
        """
        Gets or sets the AutomaticMeshBasedDefeaturing.
        """
        return None

    @AutomaticMeshBasedDefeaturing.setter
    def AutomaticMeshBasedDefeaturing(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AutomaticMeshBasedDefeaturing.
        """
        pass

    @property
    def Beam3(self) -> typing.Optional[int]:
        """
        Gets the Beam3.
        """
        return None

    @property
    def Beam4(self) -> typing.Optional[int]:
        """
        Gets the Beam4.
        """
        return None

    @property
    def BeamElements(self) -> typing.Optional[int]:
        """
        Gets the BeamElements.
        """
        return None

    @property
    def CheckMeshQuality(self) -> typing.Optional[int]:
        """
        Gets or sets the CheckMeshQuality.
        """
        return None

    @CheckMeshQuality.setter
    def CheckMeshQuality(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CheckMeshQuality.
        """
        pass

    @property
    def CollisionAvoidance(self) -> typing.Optional[int]:
        """
        Gets or sets the CollisionAvoidance.
        """
        return None

    @CollisionAvoidance.setter
    def CollisionAvoidance(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CollisionAvoidance.
        """
        pass

    @property
    def ConnectionSize(self) -> typing.Optional[float]:
        """
        Gets or sets the ConnectionSize.
        """
        return None

    @ConnectionSize.setter
    def ConnectionSize(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ConnectionSize.
        """
        pass

    @property
    def CornerNodes(self) -> typing.Optional[int]:
        """
        Gets the CornerNodes.
        """
        return None

    @property
    def Elements(self) -> typing.Optional[int]:
        """
        Gets the Elements.
        """
        return None

    @property
    def GrowthRate(self) -> typing.Optional[float]:
        """
        Gets or sets the GrowthRate.
        """
        return None

    @GrowthRate.setter
    def GrowthRate(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GrowthRate.
        """
        pass

    @property
    def GrowthRateType(self) -> typing.Optional[int]:
        """
        Gets or sets the GrowthRateType.
        """
        return None

    @GrowthRateType.setter
    def GrowthRateType(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the GrowthRateType.
        """
        pass

    @property
    def GasketElements(self) -> typing.Optional[int]:
        """
        Gets the GasketElements.
        """
        return None

    @property
    def Hex20(self) -> typing.Optional[int]:
        """
        Gets the Hex20.
        """
        return None

    @property
    def Hex8(self) -> typing.Optional[int]:
        """
        Gets the Hex8.
        """
        return None

    @property
    def HoleRemovalTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the HoleRemovalTolerance.
        """
        return None

    @HoleRemovalTolerance.setter
    def HoleRemovalTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the HoleRemovalTolerance.
        """
        pass

    @property
    def InflationAlgorithm(self) -> typing.Optional[int]:
        """
        Gets or sets the InflationAlgorithm.
        """
        return None

    @InflationAlgorithm.setter
    def InflationAlgorithm(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InflationAlgorithm.
        """
        pass

    @property
    def MaximumHeightOverBase(self) -> typing.Optional[float]:
        """
        Gets or sets the MaximumHeightOverBase.
        """
        return None

    @MaximumHeightOverBase.setter
    def MaximumHeightOverBase(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaximumHeightOverBase.
        """
        pass

    @property
    def FilletRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the FilletRatio.
        """
        return None

    @FilletRatio.setter
    def FilletRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FilletRatio.
        """
        pass

    @property
    def GapFactor(self) -> typing.Optional[float]:
        """
        Gets or Sets the Gap factor for Global Inflation
        """
        return None

    @GapFactor.setter
    def GapFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or Sets the Gap factor for Global Inflation
        """
        pass

    @property
    def InflationOption(self) -> typing.Optional[int]:
        """
        Gets or sets the InflationOption.
        """
        return None

    @InflationOption.setter
    def InflationOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InflationOption.
        """
        pass

    @property
    def InitialSizeSeed(self) -> typing.Optional[int]:
        """
        Gets or sets the InitialSizeSeed.
        """
        return None

    @InitialSizeSeed.setter
    def InitialSizeSeed(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InitialSizeSeed.
        """
        pass

    @property
    def AspectRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the AspectRatio.
        """
        return None

    @AspectRatio.setter
    def AspectRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the AspectRatio.
        """
        pass

    @property
    def Line2(self) -> typing.Optional[int]:
        """
        Gets the Line2.
        """
        return None

    @property
    def Line3(self) -> typing.Optional[int]:
        """
        Gets the Line3.
        """
        return None

    @property
    def MaximumLayers(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumLayers.
        """
        return None

    @MaximumLayers.setter
    def MaximumLayers(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumLayers.
        """
        pass

    @property
    def MidNodes(self) -> typing.Optional[int]:
        """
        Gets the MidNodes.
        """
        return None

    @property
    def Nodes(self) -> typing.Optional[int]:
        """
        Gets the Nodes.
        """
        return None

    @property
    def NumberOfRetries(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfRetries.
        """
        return None

    @NumberOfRetries.setter
    def NumberOfRetries(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfRetries.
        """
        pass

    @property
    def ProximityGapFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ProximityGapFactor.
        """
        return None

    @ProximityGapFactor.setter
    def ProximityGapFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ProximityGapFactor.
        """
        pass

    @property
    def NumberOfCPUsForParallelPartMeshing(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfCPUsForParallelPartMeshing.
        """
        return None

    @NumberOfCPUsForParallelPartMeshing.setter
    def NumberOfCPUsForParallelPartMeshing(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfCPUsForParallelPartMeshing.
        """
        pass

    @property
    def NumLayers(self) -> typing.Optional[int]:
        """
        Gets or Sets the Number of Layers of Global Inflation
        """
        return None

    @NumLayers.setter
    def NumLayers(self, value: typing.Optional[int]) -> None:
        """
        Gets or Sets the Number of Layers of Global Inflation
        """
        pass

    @property
    def OrientationNodes(self) -> typing.Optional[int]:
        """
        Gets the OrientationNodes.
        """
        return None

    @property
    def GeneratePinchOnRefresh(self) -> typing.Optional[int]:
        """
        Gets or sets the GeneratePinchOnRefresh.
        """
        return None

    @GeneratePinchOnRefresh.setter
    def GeneratePinchOnRefresh(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the GeneratePinchOnRefresh.
        """
        pass

    @property
    def Pyramid13(self) -> typing.Optional[int]:
        """
        Gets the Pyramid13.
        """
        return None

    @property
    def Pyramid5(self) -> typing.Optional[int]:
        """
        Gets the Pyramid5.
        """
        return None

    @property
    def Quad4(self) -> typing.Optional[int]:
        """
        Gets the Quad4.
        """
        return None

    @property
    def Quad8(self) -> typing.Optional[int]:
        """
        Gets the Quad8.
        """
        return None

    @property
    def Relevance(self) -> typing.Optional[int]:
        """
        Gets or sets the Relevance.
        """
        return None

    @Relevance.setter
    def Relevance(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Relevance.
        """
        pass

    @property
    def RelevanceCenter(self) -> typing.Optional[int]:
        """
        Gets or sets the RelevanceCenter.
        """
        return None

    @RelevanceCenter.setter
    def RelevanceCenter(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the RelevanceCenter.
        """
        pass

    @property
    def Resolution(self) -> typing.Optional[int]:
        """
        Gets or sets the Resolution.
        """
        return None

    @Resolution.setter
    def Resolution(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Resolution.
        """
        pass

    @property
    def ShapeChecking(self) -> typing.Optional[int]:
        """
        Gets or sets the ShapeChecking.
        """
        return None

    @ShapeChecking.setter
    def ShapeChecking(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ShapeChecking.
        """
        pass

    @property
    def SharedNodes(self) -> typing.Optional[int]:
        """
        Gets the SharedNodes.
        """
        return None

    @property
    def ShellElements(self) -> typing.Optional[int]:
        """
        Gets the ShellElements.
        """
        return None

    @property
    def SmoothingIterations(self) -> typing.Optional[int]:
        """
        Gets or sets the SmoothingIterations.
        """
        return None

    @SmoothingIterations.setter
    def SmoothingIterations(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SmoothingIterations.
        """
        pass

    @property
    def Smoothing(self) -> typing.Optional[int]:
        """
        Gets or sets the Smoothing.
        """
        return None

    @Smoothing.setter
    def Smoothing(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Smoothing.
        """
        pass

    @property
    def SolidElements(self) -> typing.Optional[int]:
        """
        Gets the SolidElements.
        """
        return None

    @property
    def SolidShellElements(self) -> typing.Optional[int]:
        """
        Gets the SolidShellElements.
        """
        return None

    @property
    def SpanAngleCenter(self) -> typing.Optional[int]:
        """
        Gets or sets the SpanAngleCenter.
        """
        return None

    @SpanAngleCenter.setter
    def SpanAngleCenter(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SpanAngleCenter.
        """
        pass

    @property
    def TargetExplicitAspectRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the TargetExplicitAspectRatio.
        """
        return None

    @TargetExplicitAspectRatio.setter
    def TargetExplicitAspectRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TargetExplicitAspectRatio.
        """
        pass

    @property
    def TargetQuality(self) -> typing.Optional[float]:
        """
        Gets or sets the TargetQuality.
        """
        return None

    @TargetQuality.setter
    def TargetQuality(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TargetQuality.
        """
        pass

    @property
    def Tet10(self) -> typing.Optional[int]:
        """
        Gets the Tet10.
        """
        return None

    @property
    def Tet4(self) -> typing.Optional[int]:
        """
        Gets the Tet4.
        """
        return None

    @property
    def TransitionOption(self) -> typing.Optional[int]:
        """
        Gets or sets the TransitionOption.
        """
        return None

    @TransitionOption.setter
    def TransitionOption(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the TransitionOption.
        """
        pass

    @property
    def TransitionRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the TransitionRatio.
        """
        return None

    @TransitionRatio.setter
    def TransitionRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TransitionRatio.
        """
        pass

    @property
    def GrowthRateSF(self) -> typing.Optional[float]:
        """
        Gets or sets the GrowthRateSF.
        """
        return None

    @GrowthRateSF.setter
    def GrowthRateSF(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GrowthRateSF.
        """
        pass

    @property
    def Tri3(self) -> typing.Optional[int]:
        """
        Gets the Tri3.
        """
        return None

    @property
    def Tri6(self) -> typing.Optional[int]:
        """
        Gets the Tri6.
        """
        return None

    @property
    def TriangleSurfaceMesher(self) -> typing.Optional[int]:
        """
        Gets or sets the TriangleSurfaceMesher.
        """
        return None

    @TriangleSurfaceMesher.setter
    def TriangleSurfaceMesher(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the TriangleSurfaceMesher.
        """
        pass

    @property
    def UsePostSmoothing(self) -> typing.Optional[int]:
        """
        Gets or sets the UsePostSmoothing.
        """
        return None

    @UsePostSmoothing.setter
    def UsePostSmoothing(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the UsePostSmoothing.
        """
        pass

    @property
    def Wedge15(self) -> typing.Optional[int]:
        """
        Gets the Wedge15.
        """
        return None

    @property
    def Wedge6(self) -> typing.Optional[int]:
        """
        Gets the Wedge6.
        """
        return None

    @property
    def CoplanarAngleTol(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CoplanarAngleTol.
        """
        return None

    @CoplanarAngleTol.setter
    def CoplanarAngleTol(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CoplanarAngleTol.
        """
        pass

    @property
    def FirstLayerHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FirstLayerHeight.
        """
        return None

    @FirstLayerHeight.setter
    def FirstLayerHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FirstLayerHeight.
        """
        pass

    @property
    def MaximumAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumAngle.
        """
        return None

    @MaximumAngle.setter
    def MaximumAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumAngle.
        """
        pass

    @property
    def MaximumThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumThickness.
        """
        return None

    @MaximumThickness.setter
    def MaximumThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumThickness.
        """
        pass

    @property
    def MaximumSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumSize.
        """
        return None

    @MaximumSize.setter
    def MaximumSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumSize.
        """
        pass

    @property
    def DefeatureTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DefeatureTolerance.
        """
        return None

    @DefeatureTolerance.setter
    def DefeatureTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DefeatureTolerance.
        """
        pass

    @property
    def Average(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Average.
        """
        return None

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def StandardDeviation(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the StandardDeviation.
        """
        return None

    @property
    def MinimumEdgeLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MinimumEdgeLength.
        """
        return None

    @property
    def MinimumSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumSize.
        """
        return None

    @MinimumSize.setter
    def MinimumSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumSize.
        """
        pass

    @property
    def PinchTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PinchTolerance.
        """
        return None

    @PinchTolerance.setter
    def PinchTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PinchTolerance.
        """
        pass

    @property
    def ProximityMinimumSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ProximityMinimumSize.
        """
        return None

    @ProximityMinimumSize.setter
    def ProximityMinimumSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ProximityMinimumSize.
        """
        pass

    @property
    def CurvatureNormalAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        return None

    @CurvatureNormalAngle.setter
    def CurvatureNormalAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CurvatureNormalAngle.
        """
        pass

    @property
    def TargetCharacteristicLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TargetCharacteristicLength.
        """
        return None

    @TargetCharacteristicLength.setter
    def TargetCharacteristicLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TargetCharacteristicLength.
        """
        pass

    @property
    def TargetSkewness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TargetSkewness.
        """
        return None

    @TargetSkewness.setter
    def TargetSkewness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TargetSkewness.
        """
        pass

    @property
    def DefaultShellMesher(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DefaultShellMesherType]:
        """
        Gets or sets the default meshing engine used to mesh sheet bodies. The default value is Quad Dominant.
        """
        return None

    @DefaultShellMesher.setter
    def DefaultShellMesher(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DefaultShellMesherType]) -> None:
        """
        Gets or sets the default meshing engine used to mesh sheet bodies. The default value is Quad Dominant.
        """
        pass

    @property
    def DisplayStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshDisplayStyle]:
        """
        Gets or sets the DisplayStyle.
        """
        return None

    @DisplayStyle.setter
    def DisplayStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshDisplayStyle]) -> None:
        """
        Gets or sets the DisplayStyle.
        """
        pass

    @property
    def ElementOrder(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementOrder]:
        """
        Gets or sets the ElementOrder.
        """
        return None

    @ElementOrder.setter
    def ElementOrder(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementOrder]) -> None:
        """
        Gets or sets the ElementOrder.
        """
        pass

    @property
    def ExportFormat(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FluentExportMeshType]:
        """
        Gets or sets the ExportFormat.
        """
        return None

    @ExportFormat.setter
    def ExportFormat(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FluentExportMeshType]) -> None:
        """
        Gets or sets the ExportFormat.
        """
        pass

    @property
    def InflationElementType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshInflationElementType]:
        """
        Gets or Sets the InflationElementType
        """
        return None

    @InflationElementType.setter
    def InflationElementType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshInflationElementType]) -> None:
        """
        Gets or Sets the InflationElementType
        """
        pass

    @property
    def MeshMetric(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshMetricType]:
        """
        Gets or sets the MeshMetric.
        """
        return None

    @MeshMetric.setter
    def MeshMetric(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshMetricType]) -> None:
        """
        Gets or sets the MeshMetric.
        """
        pass

    @property
    def PhysicsPreference(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshPhysicsPreferenceType]:
        """
        Gets or sets the PhysicsPreference.
        """
        return None

    @PhysicsPreference.setter
    def PhysicsPreference(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshPhysicsPreferenceType]) -> None:
        """
        Gets or sets the PhysicsPreference.
        """
        pass

    @property
    def ExportUnit(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.PolyflowExportUnit]:
        """
        Gets or sets the ExportUnit.
        """
        return None

    @ExportUnit.setter
    def ExportUnit(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.PolyflowExportUnit]) -> None:
        """
        Gets or sets the ExportUnit.
        """
        pass

    @property
    def ProximitySizeSources(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ProximitySFSourcesType]:
        """
        Gets or sets the ProximitySizeSources.
        """
        return None

    @ProximitySizeSources.setter
    def ProximitySizeSources(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ProximitySFSourcesType]) -> None:
        """
        Gets or sets the ProximitySizeSources.
        """
        pass

    @property
    def SolverPreference(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshSolverPreferenceType]:
        """
        Gets or sets the SolverPreference.
        """
        return None

    @SolverPreference.setter
    def SolverPreference(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshSolverPreferenceType]) -> None:
        """
        Gets or sets the SolverPreference.
        """
        pass

    @property
    def ViewAdvancedOptions(self) -> typing.Optional[bool]:
        """
        Gets or sets the ViewAdvancedOptions.
        """
        return None

    @ViewAdvancedOptions.setter
    def ViewAdvancedOptions(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ViewAdvancedOptions.
        """
        pass

    @property
    def CaptureCurvature(self) -> typing.Optional[bool]:
        """
        Gets or sets the CaptureCurvature.
        """
        return None

    @CaptureCurvature.setter
    def CaptureCurvature(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CaptureCurvature.
        """
        pass

    @property
    def CaptureProximity(self) -> typing.Optional[bool]:
        """
        Gets or sets the CaptureProximity.
        """
        return None

    @CaptureProximity.setter
    def CaptureProximity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CaptureProximity.
        """
        pass

    @property
    def ExtraRetriesForAssembly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExtraRetriesForAssembly.
        """
        return None

    @ExtraRetriesForAssembly.setter
    def ExtraRetriesForAssembly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExtraRetriesForAssembly.
        """
        pass

    @property
    def MeshMorphing(self) -> typing.Optional[bool]:
        """
        Gets or sets the MeshMorphing.
        """
        return None

    @MeshMorphing.setter
    def MeshMorphing(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MeshMorphing.
        """
        pass

    @property
    def MultiConnectionSteps(self) -> typing.Optional[bool]:
        """
        Gets or sets the MultiConnectionSteps.
        """
        return None

    @MultiConnectionSteps.setter
    def MultiConnectionSteps(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MultiConnectionSteps.
        """
        pass

    @property
    def UseSheetThicknessForPinch(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseSheetThicknessForPinch.
        """
        return None

    @UseSheetThicknessForPinch.setter
    def UseSheetThicknessForPinch(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseSheetThicknessForPinch.
        """
        pass

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets the ReadOnly.
        """
        return None

    @property
    def SheetLoopRemoval(self) -> typing.Optional[bool]:
        """
        Gets or sets the SheetLoopRemoval.
        """
        return None

    @SheetLoopRemoval.setter
    def SheetLoopRemoval(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SheetLoopRemoval.
        """
        pass

    @property
    def ShowDetailedStatistics(self) -> typing.Optional[bool]:
        """
        Gets or sets the ShowDetailedStatistics.
        """
        return None

    @ShowDetailedStatistics.setter
    def ShowDetailedStatistics(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ShowDetailedStatistics.
        """
        pass

    @property
    def StraightSidedElements(self) -> typing.Optional[bool]:
        """
        Gets or sets the StraightSidedElements.
        """
        return None

    @StraightSidedElements.setter
    def StraightSidedElements(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the StraightSidedElements.
        """
        pass

    @property
    def TopologyChecking(self) -> typing.Optional[bool]:
        """
        Gets or sets the TopologyChecking.
        """
        return None

    @TopologyChecking.setter
    def TopologyChecking(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the TopologyChecking.
        """
        pass

    @property
    def UseAdaptiveSizing(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseAdaptiveSizing.
        """
        return None

    @UseAdaptiveSizing.setter
    def UseAdaptiveSizing(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseAdaptiveSizing.
        """
        pass

    @property
    def UseFixedSizeFunctionForSheets(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseFixedSizeFunctionForSheets.
        """
        return None

    @UseFixedSizeFunctionForSheets.setter
    def UseFixedSizeFunctionForSheets(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseFixedSizeFunctionForSheets.
        """
        pass

    @property
    def QuadMesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the QuadMesh.
        """
        return None

    @QuadMesh.setter
    def QuadMesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the QuadMesh.
        """
        pass

    @property
    def MeshBasedConnection(self) -> typing.Optional[bool]:
        """
        Gets or sets the MeshBasedConnection.
        """
        return None

    @MeshBasedConnection.setter
    def MeshBasedConnection(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MeshBasedConnection.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
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

    def GetMeshMetricQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlGroupAuto) -> str:
        """
        GetMeshMetricQuantityName method.
        """
        pass

    def PreviewWelds(self) -> None:
        """
        Preview Welds.
        """
        pass

    def PreviewGeometryOnWelds(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        PreviewGeometryOnWelds method.
        """
        pass

    def PreviewMeshOnWelds(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        """
        PreviewMeshOnWelds method.
        """
        pass

    def PreviewGeometryOnWeld(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        """
        
            Preview geometry on one weld control provided.
            
        """
        pass

    def PreviewMeshOnWeld(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        """
        
            Preview model mesh on one weld control provided.
            
        """
        pass

    def PreviewMeshOnAllWelds(self) -> None:
        """
        
            Preview model mesh on all weld controls of the Mesh.
            
        """
        pass

    def ShowOverlappingFaces(self) -> None:
        """
        Run the ShowOverlappingFaces action.
        """
        pass

    def ShowUnconnectedFacesNearEdges(self) -> None:
        """
        Run the  ShowUnconnectedFreeEdges action.
        """
        pass

    def PreviewMeshOnWeldWorksheet(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject, indices: typing.Iterable[int]) -> None:
        """
        PreviewMeshOnWeldWorksheet method.
        """
        pass

    def PreviewGeometryOnWeldWorksheet(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject, indices: typing.Iterable[int]) -> None:
        """
        PreviewGeometryOnWeldWorksheet method.
        """
        pass

    def PreviewMeshOnWeldCurve(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        """
        
            Preview model mesh on a given single weld curve.
            
        """
        pass

    def RunStackerDiagnostics(self, direction: int) -> None:
        """
        
            Find stackable bodies in a given direction
            
        """
        pass

    def RunStackerDiagnosticsOnAllFindX(self) -> None:
        """
        
            Find stackable bodies in the Global X direction
            
        """
        pass

    def RunStackerDiagnosticsOnAllFindY(self) -> None:
        """
        
            /// Find stackable bodies in the Global Y direction
            
        """
        pass

    def RunStackerDiagnosticsOnAllFindZ(self) -> None:
        """
        
            /// Find stackable bodies in the Global Z direction
            
        """
        pass

    @typing.overload
    def PreviewQuadLayers(self, dataModelObjects: typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]) -> None:
        ...

    @typing.overload
    def PreviewQuadLayers(self, dataModelObjects: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        ...

    def PreviewQuadLayers(self, *args: typing.Any) -> None:
        """
        PreviewQuadLayers method.
        """
        pass

    def PreviewAllQuadLayers(self) -> None:
        """
        
            Preview quad layers on all Quad Layer controls of the Mesh.
            
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
        """
        pass

    @typing.overload
    def CleanPartOrBody(self, dataModelObjects: typing.Iterable) -> None:
        ...

    @typing.overload
    def CleanPartOrBody(self, dataModelObject: Ansys.Mechanical.DataModel.Interfaces.IDataModelObject) -> None:
        ...

    def CleanPartOrBody(self, *args: typing.Any) -> None:
        """
        
            Clear generated data for parts and/or bodies provided.
            
        """
        pass

    def AddNodeMergeGroup(self) -> Ansys.ACT.Automation.Mechanical.NodeMergeGroup:
        """
        Add a new NodeMergeGroup.
        """
        pass

    def AddNodeMerge(self) -> None:
        """
        Add a new NodeMerge.
        """
        pass

    def AddAutomaticMethod(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.AutomaticMethod:
        """
        Creates a new AutomaticMethod
        """
        pass

    def AddMeshConnectionGroup(self) -> Ansys.ACT.Automation.Mechanical.MeshConnectionGroup:
        """
        
            Add a new MeshConnectionGroup.
            
        """
        pass

    def AddContactMatchGroup(self) -> Ansys.ACT.Automation.Mechanical.ContactMatchGroup:
        """
        
            Add a new AddContactMatchGroup.
            
        """
        pass

    def AddManualMeshConnection(self) -> None:
        """
        
            Add a new ManualMeshConnection
            
        """
        pass

    def AddPullExtrude(self) -> Ansys.ACT.Automation.Mechanical.MeshExtrude:
        """
        
            Add a new Pull (Extrude).
            
        """
        pass

    def AddPullRevolve(self) -> Ansys.ACT.Automation.Mechanical.MeshExtrude:
        """
        
            Add a new Pull (Revolve).
            
        """
        pass

    def AddPullSurfaceCoating(self) -> Ansys.ACT.Automation.Mechanical.MeshExtrude:
        """
        
            Add a new Pull (Surface Coating)).
            
        """
        pass

    def AddDirectMorph(self) -> Ansys.ACT.Automation.Mechanical.DirectMorph:
        """
        
            Add a new DirectMorph.
            
        """
        pass

    def AddDeviation(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Deviation:
        """
        Creates a new SagControl
        """
        pass

    def AddWasher(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Washer:
        """
        Creates a new SagControl
        """
        pass

    def AddWeld(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Weld:
        """
        Creates a new WeldControl
        """
        pass

    def AddRepairTopology(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.RepairTopology:
        """
        Creates a new RepairTopology
        """
        pass

    def AddConnect(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Connect:
        """
        Creates a new Connect Control
        """
        pass

    def AddFeatureSuppress(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.FeatureSuppress:
        """
        Creates a new FeatureSuppress
        """
        pass

    def AddGeometryFidelity(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.GeometryFidelity:
        """
        Creates a new GeometryFidelity
        """
        pass

    def AddMeshCopy(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.MeshCopy:
        """
        Creates a new MeshCopy
        """
        pass

    def AddTopologySuppressControl(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.TopologySuppressControl:
        """
        Creates a new TopologySuppressControl
        """
        pass

    def SaveMeshToFileHelper(self, filePath: str, type: int) -> None:
        """
        SaveMeshToFileHelper
        """
        pass

    def ExportWeldDefinitionFile(self, filePath: str) -> None:
        """
        
            Export the weld definition file to the specified location.
            If the folder does not exist or file cannot be written to the location, an exception will be thrown.
            Pre-existing files will be overwritten.
            
        """
        pass

    def SaveMeshReportHelper(self, filePath: str, filter: int) -> None:
        """
        SaveMeshReportHelper
        """
        pass

    def SaveMeshReportForPartHelper(self, filePath: str, filter: int) -> None:
        """
        SaveMeshReportForPartHelper
        """
        pass

    def SaveBodiesToXMLHelper(self, filePath: str) -> None:
        """
        SaveMeshReportHelper
        """
        pass

    def PrimeMeshFileHelper(self, filePath: str, mode: int) -> None:
        """
        PrimeMeshFileHelper
        """
        pass

    def PinchControlGeomtry(self, geomType: Ansys.Mechanical.DataModel.Enums.MeshControlPinchGeomtryType) -> None:
        """
        Set the geometry type for the Pinch Control.
        """
        pass

    def IsMeshMetricVisible(self, index: int) -> bool:
        """
        IsMeshMetricVisible method.
        """
        pass

    def ColorByMeshingEngine(self) -> None:
        """
        ColorByMeshingEngine method.
        """
        pass

    def GetIndexFromSurfaceMeshMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get Index of shell mesh metric vector based on mesh metric
            
        """
        pass

    def GetIsShellTargetMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get Shell Target Metric
            
        """
        pass

    def GetSheetQuantityTypeString(self, metric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
            Get quantity type of sheet metric from mesh metric type
            
        """
        pass

    def GetSurfaceMeshQualityDisplayMetric(self, index: int) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        
             Get Surface Mesh Quality Metric 
             
        """
        pass

    def GetActiveSurfaceMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Active User Mesh Quality
             
        """
        pass

    def GetSurfaceMeshQualityName(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Name
             
        """
        pass

    def GetSurfaceMeshQualityWarningLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Mesh Quality Warning Limit is default
             
        """
        pass

    def GetSurfaceMeshQualityErrorLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Mesh Quality Error Limit is default
             
        """
        pass

    def GetSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get User Mesh Quality Warning Limit
             
        """
        pass

    def GetSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get User Mesh Quality Error Limit
             
        """
        pass

    def GetSurfaceMeshQualityPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Percentage Failed 
             
        """
        pass

    def GetSurfaceMeshQualityCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Count Failed
             
        """
        pass

    def GetSurfaceMeshQualityWarningPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Warning Percentage Failed 
             
        """
        pass

    def GetSurfaceMeshQualityWarningCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Warning Count Failed
             
        """
        pass

    def GetSurfaceMeshQualityWorstMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Worst Metric Value
             
        """
        pass

    def GetSurfaceMeshQualityAverageMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Average Metric Value
             
        """
        pass

    def GetSurfaceMeshQualityWorstMetricBackgroundColor(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric BackgroundColor
             
        """
        pass

    def GetSurfaceMeshQualityWorstMetricTooltip(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric Tooltip
             
        """
        pass

    def SetActiveSurfaceMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, activeMetric: float) -> None:
        """
        
             Set Active Mesh Quality 
             
        """
        pass

    @typing.overload
    def SetSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: float) -> None:
        ...

    @typing.overload
    def SetSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetSurfaceMeshQualityWarningLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Warning Limit
             
        """
        pass

    @typing.overload
    def SetSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: float) -> None:
        ...

    @typing.overload
    def SetSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetSurfaceMeshQualityErrorLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Error Level
             
        """
        pass

    def CreateMQSurfaceElementsNamedSelection(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, failCode: int) -> None:
        """
        
              Create Mesh Quality Surface Element Named Selection
             
        """
        pass

    def GetSurfaceMeshQualityState(self) -> int:
        """
        
            Get the state of surface mesh quality worksheet tab
            
        """
        pass

    def GetSolidMeshQualityState(self) -> int:
        """
        
            Get the state of solid mesh quality worksheet tab
            
        """
        pass

    def GetSolidSurfaceMeshQualityState(self) -> int:
        """
        
            Get the state of solid surface mesh quality worksheet tab
            
        """
        pass

    def GetVolumeQuantityTypeString(self, metric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
            Get Quantity type from solid mesh metric type
            
        """
        pass

    def GetIndexFromVolumeMeshMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get index from solid mesh quality worksheet from given mesh metric type.
            
        """
        pass

    def GetIsSolidTargetMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get Solid Target Metric
            
        """
        pass

    def GetVolumeMeshQualityDisplayMetric(self, index: int) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        
             Get Volume Mesh Quality Metric 
             
        """
        pass

    def GetVolumeMeshQualityName(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Name
             
        """
        pass

    def GetActiveVolumeMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Active Mesh Quality 
             
        """
        pass

    def GetVolumeMeshQualityWarningLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Volume Mesh Quality Worksheet Warning Limit is Default 
             
        """
        pass

    def GetVolumeMeshQualityErrorLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Volume Mesh Quality Worksheet Error Limit is Default 
             
        """
        pass

    def GetVolumeMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Warning Limit
             
        """
        pass

    def GetVolumeMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Error Limit
             
        """
        pass

    def GetVolumeMeshQualityPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Percentage Failed 
             
        """
        pass

    def GetVolumeMeshQualityCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Count Failed
             
        """
        pass

    def GetVolumeMeshQualityWarningPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Warning Percentage Failed 
             
        """
        pass

    def GetVolumeMeshQualityWarningCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Warning Count Failed
             
        """
        pass

    def GetVolumeMeshQualityWorstMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Worst Metric Value
             
        """
        pass

    def GetVolumeMeshQualityAverageMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Average Metric Value
             
        """
        pass

    def GetVolumeMeshQualityWorstMetricBackgroundColor(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric BackgroundColor
             
        """
        pass

    def GetVolumeMeshQualityWorstMetricTooltip(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric Tooltip
             
        """
        pass

    def SetActiveVolumeMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, activeMetric: float) -> None:
        """
        
             Set Active Mesh Quality 
             
        """
        pass

    @typing.overload
    def SetVolumeMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: float) -> None:
        ...

    @typing.overload
    def SetVolumeMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetVolumeMeshQualityWarningLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Warning Limit
             
        """
        pass

    @typing.overload
    def SetVolumeMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: float) -> None:
        ...

    @typing.overload
    def SetVolumeMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetVolumeMeshQualityErrorLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Error Limit
             
        """
        pass

    def CreateMQVolumeElementsNamedSelection(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, failCode: int) -> None:
        """
        
              Create Mesh Quality Volume Element Name Selection
             
        """
        pass

    def GetSolidSurfaceQuantityTypeString(self, metric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
            Get Quantity type from SolidSurface mesh metric type
            
        """
        pass

    def GetIndexFromSolidSurfaceMeshMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get index from SolidSurface mesh quality worksheet from given mesh metric type.
            
        """
        pass

    def GetIsSolidSurfaceTargetMetric(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
            Get SolidSurface Target Metric
            
        """
        pass

    def GetSolidSurfaceMeshQualityDisplayMetric(self, index: int) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        
             Get SolidSurface Mesh Quality Metric 
             
        """
        pass

    def GetSolidSurfaceMeshQualityName(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Name
             
        """
        pass

    def GetActiveSolidSurfaceMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get Active Mesh Quality 
             
        """
        pass

    def GetSolidSurfaceMeshQualityWarningLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get SolidSurface Mesh Quality Worksheet Warning Limit is Default 
             
        """
        pass

    def GetSolidSurfaceMeshQualityErrorLimitIsDefault(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> bool:
        """
        
             Get SolidSurface Mesh Quality Worksheet Error Limit is Default 
             
        """
        pass

    def GetSolidSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Warning Limit
             
        """
        pass

    def GetSolidSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Error Limit
             
        """
        pass

    def GetSolidSurfaceMeshQualityPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Percentage Failed 
             
        """
        pass

    def GetSolidSurfaceMeshQualityCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Count Failed
             
        """
        pass

    def GetSolidSurfaceMeshQualityWarningPercentageFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> float:
        """
        
             Get Mesh Quality Warning Percentage Failed 
             
        """
        pass

    def GetSolidSurfaceMeshQualityWarningCountFailed(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> int:
        """
        
             Get Mesh Quality Warning Count Failed
             
        """
        pass

    def GetSolidSurfaceMeshQualityWorstMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Worst Metric Value
             
        """
        pass

    def GetSolidSurfaceMeshQualityAverageMetricValue(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Core.Units.Quantity:
        """
        
             Get Mesh Quality Average Metric Value
             
        """
        pass

    def GetSolidSurfaceMeshQualityWorstMetricBackgroundColor(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric BackgroundColor
             
        """
        pass

    def GetSolidSurfaceMeshQualityWorstMetricTooltip(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> str:
        """
        
             Get Mesh Quality Worst Metric Tooltip
             
        """
        pass

    def SetActiveSolidSurfaceMeshQuality(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, activeMetric: float) -> None:
        """
        
             Set Active Mesh Quality 
             
        """
        pass

    @typing.overload
    def SetSolidSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: float) -> None:
        ...

    @typing.overload
    def SetSolidSurfaceMeshQualityWarningLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetSolidSurfaceMeshQualityWarningLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Warning Limit
             
        """
        pass

    @typing.overload
    def SetSolidSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: float) -> None:
        ...

    @typing.overload
    def SetSolidSurfaceMeshQualityErrorLimit(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, errorLevel: Ansys.Core.Units.Quantity) -> None:
        ...

    def SetSolidSurfaceMeshQualityErrorLimit(self, *args: typing.Any) -> None:
        """
        
              Set Mesh Quality Error Limit
             
        """
        pass

    def CreateMQSolidSurfaceElementsNamedSelection(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, failCode: int) -> None:
        """
        
              Create Mesh Quality SolidSurface Element Name Selection
             
        """
        pass

    def ComputeMeshQualityMetrics(self) -> None:
        """
        ComputeMeshQualityMetrics method.
        """
        pass

    def ValidateMeshQualityMetrics(self) -> None:
        """
        ValidateMeshQualityMetrics method.
        """
        pass

    def ResetMeshQualityMetrics(self) -> None:
        """
        ResetMeshQualityMetrics method.
        """
        pass

    def RefreshMeshQualityGridInfo(self) -> None:
        """
        RefreshMeshQualityGridInfo method.
        """
        pass

    def GetMeshQualityAdvancedView(self) -> int:
        """
        GetMeshQualityAdvancedView method.
        """
        pass

    def SetMeshQualityAdvancedView(self, advancedView: int) -> None:
        """
        SetMeshQualityAdvancedView method.
        """
        pass

    def LoadMQWorksheetFile(self, filePath: str) -> None:
        """
        LoadMQWorksheetFile method.
        """
        pass

    def SaveMQWorksheetFile(self, filePath: str) -> None:
        """
        SaveMQWorksheetFile method.
        """
        pass

    def GetSurfaceMeshMetrics(self) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        GetSurfaceMeshMetrics method.
        """
        pass

    def GetVolumeMeshMetrics(self) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        GetVolumeMeshMetrics method.
        """
        pass

    def GetSolidSurfaceMeshMetrics(self) -> Ansys.Mechanical.DataModel.Enums.MeshMetricType:
        """
        GetSolidSurfaceMeshMetrics method.
        """
        pass

    def SetSurfaceMeshMetricLimits(self, metricType: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLimit: Ansys.Core.Units.Quantity, ErrorLimit: Ansys.Core.Units.Quantity) -> None:
        """
        SetSurfaceMeshMetricLimits method.
        """
        pass

    def SetSolidMeshMetricLimits(self, metricType: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLimit: Ansys.Core.Units.Quantity, ErrorLimit: Ansys.Core.Units.Quantity) -> None:
        """
        SetSolidMeshMetricLimits method.
        """
        pass

    def SetSolidSurfaceMeshMetricLimits(self, metricType: Ansys.Mechanical.DataModel.Enums.MeshMetricType, warningLimit: Ansys.Core.Units.Quantity, ErrorLimit: Ansys.Core.Units.Quantity) -> None:
        """
        SetSolidSurfaceMeshMetricLimits method.
        """
        pass

    def ActivateAllSurfaceWorksheetRows(self) -> None:
        """
        ActivateAllSurfaceWorksheetRows method.
        """
        pass

    def ActivateAllVolumeWorksheetRows(self) -> None:
        """
        ActivateAllVolumeWorksheetRows method.
        """
        pass

    def ActivateAllSolidSurfaceWorksheetRows(self) -> None:
        """
        ActivateAllSolidSurfaceWorksheetRows method.
        """
        pass

    def DeactivateAllSurfaceWorksheetRows(self) -> None:
        """
        DeactivateAllSurfaceWorksheetRows method.
        """
        pass

    def DeactivateAllVolumeWorksheetRows(self) -> None:
        """
        DeactivateAllVolumeWorksheetRows method.
        """
        pass

    def DeactivateAllSolidSurfaceWorksheetRows(self) -> None:
        """
        DeactivateAllSolidSurfaceWorksheetRows method.
        """
        pass

    def SetMeshMetricOptions(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType, prefValue: Ansys.Mechanical.DataModel.Enums.MetricPreference) -> None:
        """
        SetMeshMetricOptions method.
        """
        pass

    def GetMeshMetricOptions(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> Ansys.Mechanical.DataModel.Enums.MetricPreference:
        """
        GetMeshMetricOptions method.
        """
        pass

    def SetMeshQualityTabIndex(self, tabIndex: int) -> None:
        """
        SetMeshQualityTabIndex method.
        """
        pass

    def GetMeshQualityTabIndex(self) -> int:
        """
        GetMeshQualityTabIndex method.
        """
        pass

    def GetDisplayStyle(self) -> Ansys.Common.Interop.DSObjectTypes.DSMeshDisplayStyle:
        """
        GetDisplayStyle method.
        """
        pass

    def CreateHistogram(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> None:
        """
        CreateHistogram method.
        """
        pass

    def ShowProblematicBodies(self, meshMetric: Ansys.Mechanical.DataModel.Enums.MeshMetricType) -> None:
        """
        ShowProblematicBodies method.
        """
        pass

    def OpenTroubleShootDoc(self) -> None:
        """
        OpenTroubleShootDoc method.
        """
        pass

    def AddMeshLayers(self) -> None:
        """
        Adds Mesh Layers when contour enabled in Mesh Quality Workhseet mode.
        """
        pass

    def RemoveMeshLayers(self) -> None:
        """
        Removes Mesh Layers when contour enabled in Mesh Quality Workhseet mode.
        """
        pass

    def GetActiveUnits(self) -> Ansys.ACT.Interfaces.Common.MechanicalUnitSystemEnum:
        """
        GetActiveUnits method.
        """
        pass

    def IsDegree(self) -> bool:
        """
        IsDegree method.
        """
        pass

    def HasSolids(self) -> bool:
        """
        HasSolids method.
        """
        pass

    def HasSheets(self) -> bool:
        """
        HasSheets method.
        """
        pass

    def GetLegendStyle(self) -> Ansys.Common.Interop.DSObjectTypes.DSMeshLegendStyle:
        """
        GetLegendStyle method.
        """
        pass

    def ToggleLegend(self, legendStyle: Ansys.Common.Interop.DSObjectTypes.DSMeshLegendStyle) -> None:
        """
        ToggleLegend method.
        """
        pass

    def AddSmallestEdgesToSelection(self) -> None:
        """
        AddSmallestEdgesToSelection method.
        """
        pass

    def GetCalculatedMaxFaceSize(self) -> Ansys.Core.Units.Quantity:
        """
        GetCalculatedMaxFaceSize method.
        """
        pass

    def ShowAxisymmetricBodies(self) -> None:
        """
        ShowAxisymmetricBodies method.
        """
        pass

    def ShowSuppressibleTopology(self, type: int) -> None:
        """
        
            Select all edges/vertices that are topologically suppressible.
            Dimension of the topology (0 for Vertices, 1 for Edges)
            
        """
        pass

    def SetMeshWorksheetActive(self, active: bool) -> None:
        """
        SetMeshWorksheetActive method.
        """
        pass

    def AddContactSizing(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.ContactSizing:
        """
        Creates a new ContactSizing
        """
        pass

    def AddFaceMeshing(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.FaceMeshing:
        """
        Creates a new FaceMeshing
        """
        pass

    def AddInflation(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Inflation:
        """
        Creates a new Inflation
        """
        pass

    def AddMatchControl(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.MatchControl:
        """
        Creates a new MatchControl
        """
        pass

    def AddPinch(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Pinch:
        """
        Creates a new Pinch
        """
        pass

    def AddRefinement(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Refinement:
        """
        Creates a new Refinement
        """
        pass

    def AddSizing(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.Sizing:
        """
        Creates a new Sizing
        """
        pass

    def CreatePinchControls(self) -> None:
        """
        Run the CreatePinchControls action.
        """
        pass

    def GenerateMesh(self) -> None:
        """
        Run the GenerateMesh action.
        """
        pass

    def PreviewInflation(self) -> None:
        """
        Run the PreviewInflation action.
        """
        pass

    def PreviewSurfaceMesh(self) -> None:
        """
        Run the PreviewSurfaceMesh action.
        """
        pass

    def ShowFeatureSuppressibleFaces(self) -> None:
        """
        Run the ShowFeatureSuppressibleFaces action.
        """
        pass

    def ShowMappableBodies(self) -> None:
        """
        Run the ShowMappableBodies action.
        """
        pass

    def ShowSweepableBodies(self) -> None:
        """
        Run the ShowSweepableBodies action.
        """
        pass

    def Update(self) -> None:
        """
        Run the Update action.
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


class MeshControl(object):
    """
    Defines a MeshControl.
    """

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
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Connect(object):
    """
    Defines a Connect.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ConnectionToleranceList(self) -> typing.Optional[str]:
        """
        Gets or sets the ConnectionToleranceList.
        """
        return None

    @ConnectionToleranceList.setter
    def ConnectionToleranceList(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ConnectionToleranceList.
        """
        pass

    @property
    def ConnectionTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ConnectionTolerance.
        """
        return None

    @ConnectionTolerance.setter
    def ConnectionTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ConnectionTolerance.
        """
        pass

    @property
    def ConnectionSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ConnectionSize.
        """
        return None

    @ConnectionSize.setter
    def ConnectionSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ConnectionSize.
        """
        pass

    @property
    def CoplanarAngleTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CoplanarAngleTolerance.
        """
        return None

    @CoplanarAngleTolerance.setter
    def CoplanarAngleTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CoplanarAngleTolerance.
        """
        pass

    @property
    def ConnectionOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionOptions]:
        """
        Gets or sets the ConnectionOption.
        """
        return None

    @ConnectionOption.setter
    def ConnectionOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionOptions]) -> None:
        """
        Gets or sets the ConnectionOption.
        """
        pass

    @property
    def MultipleConnectionStep(self) -> typing.Optional[bool]:
        """
        Gets or sets the MultipleConnectionStep.
        """
        return None

    @MultipleConnectionStep.setter
    def MultipleConnectionStep(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MultipleConnectionStep.
        """
        pass

    @property
    def PerformIntersections(self) -> typing.Optional[bool]:
        """
        Gets or sets the PerformIntersections.
        """
        return None

    @PerformIntersections.setter
    def PerformIntersections(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PerformIntersections.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class ContactSizing(object):
    """
    Defines a ContactSizing.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Relevance(self) -> typing.Optional[float]:
        """
        Gets or sets the Relevance.
        """
        return None

    @Relevance.setter
    def Relevance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Relevance.
        """
        pass

    @property
    def Type(self) -> typing.Optional[int]:
        """
        Gets or sets the Type.
        """
        return None

    @Type.setter
    def Type(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Type.
        """
        pass

    @property
    def ElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElementSize.
        """
        return None

    @ElementSize.setter
    def ElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElementSize.
        """
        pass

    @property
    def ContactRegion(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion]:
        """
        Gets or sets the ContactRegion.
        """
        return None

    @ContactRegion.setter
    def ContactRegion(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.ContactRegion]) -> None:
        """
        Gets or sets the ContactRegion.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class FaceMeshing(object):
    """
    Defines a FaceMeshing.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ConstrainBoundary(self) -> typing.Optional[int]:
        """
        Gets or sets the ConstrainBoundary.
        """
        return None

    @ConstrainBoundary.setter
    def ConstrainBoundary(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ConstrainBoundary.
        """
        pass

    @property
    def InternalNumberOfDivisions(self) -> typing.Optional[int]:
        """
        Gets or sets the InternalNumberOfDivisions.
        """
        return None

    @InternalNumberOfDivisions.setter
    def InternalNumberOfDivisions(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InternalNumberOfDivisions.
        """
        pass

    @property
    def TransitionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TransitionType]:
        """
        Gets or sets the TransitionType of MZ Face Meshing (Mapping)
        """
        return None

    @TransitionType.setter
    def TransitionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TransitionType]) -> None:
        """
        Gets or sets the TransitionType of MZ Face Meshing (Mapping)
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FaceMeshingMethod]:
        """
        Gets or sets the Method.
        """
        return None

    @Method.setter
    def Method(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FaceMeshingMethod]) -> None:
        """
        Gets or sets the Method.
        """
        pass

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        Gets the Active.
        """
        return None

    @property
    def MappedMesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the MappedMesh.
        """
        return None

    @MappedMesh.setter
    def MappedMesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MappedMesh.
        """
        pass

    @property
    def MultiZoneSemiStructured(self) -> typing.Optional[bool]:
        """
        Gets or sets the Semi-Structured in MZ Face Meshing (Mapping).
        """
        return None

    @MultiZoneSemiStructured.setter
    def MultiZoneSemiStructured(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Semi-Structured in MZ Face Meshing (Mapping).
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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
    def SpecifiedCorners(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SpecifiedCorners.
        """
        return None

    @SpecifiedCorners.setter
    def SpecifiedCorners(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SpecifiedCorners.
        """
        pass

    @property
    def SpecifiedEnds(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SpecifiedEnds.
        """
        return None

    @SpecifiedEnds.setter
    def SpecifiedEnds(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SpecifiedEnds.
        """
        pass

    @property
    def SpecifiedSides(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SpecifiedSides.
        """
        return None

    @SpecifiedSides.setter
    def SpecifiedSides(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SpecifiedSides.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class FeatureSuppress(object):
    """
    Defines a FeatureSuppress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FeatureHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        To specify the Feature Height.
        """
        return None

    @FeatureHeight.setter
    def FeatureHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        To specify the Feature Height.
        """
        pass

    @property
    def SourceSelection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FeatureSuppressMethod]:
        """
        To select the FeatureSuppress method.
        """
        return None

    @SourceSelection.setter
    def SourceSelection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FeatureSuppressMethod]) -> None:
        """
        To select the FeatureSuppress method.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

    @property
    def SourceNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the SourceNamedSelection.
        """
        return None

    @SourceNamedSelection.setter
    def SourceNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the SourceNamedSelection.
        """
        pass

    @property
    def SourceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        To specify the face selections for the method: Defeature Faces or Parent Faces.
        """
        return None

    @SourceLocation.setter
    def SourceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        To specify the face selections for the method: Defeature Faces or Parent Faces.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class GeometryFidelity(object):
    """
    Defines a GeometryFidelity.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class MatchControl(object):
    """
    Defines a MatchControl.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Transformation(self) -> typing.Optional[int]:
        """
        Gets or sets the Transformation.
        """
        return None

    @Transformation.setter
    def Transformation(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Transformation.
        """
        pass

    @property
    def ControlMessages(self) -> typing.Optional[bool]:
        """
        Gets the ControlMessages.
        """
        return None

    @property
    def HighNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the HighNamedSelection.
        """
        return None

    @HighNamedSelection.setter
    def HighNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the HighNamedSelection.
        """
        pass

    @property
    def LowNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the LowNamedSelection.
        """
        return None

    @LowNamedSelection.setter
    def LowNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the LowNamedSelection.
        """
        pass

    @property
    def RotationAxis(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the RotationAxis.
        """
        return None

    @RotationAxis.setter
    def RotationAxis(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the RotationAxis.
        """
        pass

    @property
    def HighCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the HighCoordinateSystem.
        """
        return None

    @HighCoordinateSystem.setter
    def HighCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the HighCoordinateSystem.
        """
        pass

    @property
    def LowCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the LowCoordinateSystem.
        """
        return None

    @LowCoordinateSystem.setter
    def LowCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the LowCoordinateSystem.
        """
        pass

    @property
    def HighGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the HighGeometrySelection.
        """
        return None

    @HighGeometrySelection.setter
    def HighGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the HighGeometrySelection.
        """
        pass

    @property
    def LowGeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the LowGeometrySelection.
        """
        return None

    @LowGeometrySelection.setter
    def LowGeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the LowGeometrySelection.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class MeshCopy(object):
    """
    Defines a MeshCopy.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def NodeMergeTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the NodeMergeTolerance.
        """
        return None

    @NodeMergeTolerance.setter
    def NodeMergeTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NodeMergeTolerance.
        """
        pass

    @property
    def PercentageOfElementSize(self) -> typing.Optional[float]:
        """
        Gets or sets the PercentageOfElementSize.
        """
        return None

    @PercentageOfElementSize.setter
    def PercentageOfElementSize(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PercentageOfElementSize.
        """
        pass

    @property
    def NodeMergeToleranceOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NodeMergeToleranceMethod]:
        """
        Gets or sets the NodeMergeToleranceOption.
        """
        return None

    @NodeMergeToleranceOption.setter
    def NodeMergeToleranceOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NodeMergeToleranceMethod]) -> None:
        """
        Gets or sets the NodeMergeToleranceOption.
        """
        pass

    @property
    def TargetScoping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the TargetScoping.
        """
        return None

    @TargetScoping.setter
    def TargetScoping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the TargetScoping.
        """
        pass

    @property
    def SourceAnchorsNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the SourceAnchorsNamedSelection.
        """
        return None

    @SourceAnchorsNamedSelection.setter
    def SourceAnchorsNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the SourceAnchorsNamedSelection.
        """
        pass

    @property
    def TargetAnchorsNamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the TargetAnchorsNamedSelection.
        """
        return None

    @TargetAnchorsNamedSelection.setter
    def TargetAnchorsNamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the TargetAnchorsNamedSelection.
        """
        pass

    @property
    def SourceAnchors(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SourceAnchors.
        """
        return None

    @SourceAnchors.setter
    def SourceAnchors(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SourceAnchors.
        """
        pass

    @property
    def TargetAnchors(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the TargetAnchors.
        """
        return None

    @TargetAnchors.setter
    def TargetAnchors(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the TargetAnchors.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Pinch(object):
    """
    Defines a Pinch.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def AutoManualMode(self) -> typing.Optional[int]:
        """
        Gets the AutoManualMode.
        """
        return None

    @property
    def Tolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Tolerance.
        """
        return None

    @Tolerance.setter
    def Tolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Tolerance.
        """
        pass

    @property
    def MasterGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MasterGeometry.
        """
        return None

    @MasterGeometry.setter
    def MasterGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MasterGeometry.
        """
        pass

    @property
    def SlaveGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SlaveGeometry.
        """
        return None

    @SlaveGeometry.setter
    def SlaveGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SlaveGeometry.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Refinement(object):
    """
    Defines a Refinement.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def NumberOfRefinements(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfRefinements.
        """
        return None

    @NumberOfRefinements.setter
    def NumberOfRefinements(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfRefinements.
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class Relevance(object):
    """
    Defines a Relevance.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def PartRelavance(self) -> typing.Optional[int]:
        """
        Gets the PartRelavance.
        """
        return None

    @property
    def NamedSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Gets or sets the NamedSelection.
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.NamedSelection]) -> None:
        """
        Gets or sets the NamedSelection.
        """
        pass

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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


class TopologySuppressControl(object):
    """
    Defines a TopologySuppressControl.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSMeshControlAuto]:
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

    def GenerateMesh(self) -> None:
        """
        Generate the Mesh.
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


