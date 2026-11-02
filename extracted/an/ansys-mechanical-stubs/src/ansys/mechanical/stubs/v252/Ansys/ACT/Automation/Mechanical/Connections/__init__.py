"""Connections module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class AMBondConnection(object):
    """
    Defines a AMBondConnection.
    """

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
    def ContactType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]:
        """
        Gets or sets the ContactType.
        """
        return None

    @ContactType.setter
    def ContactType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]) -> None:
        """
        Gets or sets the ContactType.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMBondConnectionAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ContactBodies(self) -> typing.Optional[str]:
        """
        Gets the ContactBodies.
        """
        return None

    @property
    def TargetBodies(self) -> typing.Optional[str]:
        """
        Gets the TargetBodies.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def SearchConnectionsForDuplicatePairs(self) -> None:
        """
        Run the SearchConnectionsForDuplicatePairs action.
        """
        pass

    def FlipContactTarget(self) -> None:
        """
        Run the FlipContactTarget action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class SpotWeldConnection(object):
    """
    Defines a SpotWeldConnection.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSSpotWeldConnectionAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Material(self) -> typing.Optional[str]:
        """
        Gets or sets the Material.
        """
        return None

    @Material.setter
    def Material(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Material.
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
    def NumWeldPoints(self) -> typing.Optional[int]:
        """
        Gets the NumWeldPoints.
        """
        return None

    @property
    def AngleTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AngleTolerance.
        """
        return None

    @AngleTolerance.setter
    def AngleTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AngleTolerance.
        """
        pass

    @property
    def PenetrationTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PenetrationTolerance.
        """
        return None

    @PenetrationTolerance.setter
    def PenetrationTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PenetrationTolerance.
        """
        pass

    @property
    def Radius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Radius.
        """
        return None

    @Radius.setter
    def Radius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Radius.
        """
        pass

    @property
    def SnapToEdgeTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SnapToEdgeTolerance.
        """
        return None

    @SnapToEdgeTolerance.setter
    def SnapToEdgeTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SnapToEdgeTolerance.
        """
        pass

    @property
    def SearchDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SearchDistance.
        """
        return None

    @SearchDistance.setter
    def SearchDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SearchDistance.
        """
        pass

    @property
    def ConnectionBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]:
        """
        Gets or sets the ConnectionBehavior.
        """
        return None

    @ConnectionBehavior.setter
    def ConnectionBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]) -> None:
        """
        Gets or sets the ConnectionBehavior.
        """
        pass

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpotWeldTypes]:
        """
        Gets or sets the Type.
        """
        return None

    @Type.setter
    def Type(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpotWeldTypes]) -> None:
        """
        Gets or sets the Type.
        """
        pass

    @property
    def StiffnessBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]:
        """
        Gets or sets the StiffnessBehavior.
        """
        return None

    @StiffnessBehavior.setter
    def StiffnessBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]) -> None:
        """
        Gets or sets the StiffnessBehavior.
        """
        pass

    @property
    def ShellThicknessEffect(self) -> typing.Optional[bool]:
        """
        Gets or sets the ShellThicknessEffect.
        """
        return None

    @ShellThicknessEffect.setter
    def ShellThicknessEffect(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ShellThicknessEffect.
        """
        pass

    @property
    def SourceGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SourceGeometry.
        """
        return None

    @SourceGeometry.setter
    def SourceGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SourceGeometry.
        """
        pass

    @property
    def TargetGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the TargetGeometry.
        """
        return None

    @TargetGeometry.setter
    def TargetGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the TargetGeometry.
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
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def add_OnHitPointAdded(self, value: System.EventHandler[Ansys.ACT.Automation.Mechanical.Connections.SpotWeldConnectionChangedArgs]) -> None:
        """
        add_OnHitPointAdded method.
        """
        pass

    def remove_OnHitPointAdded(self, value: System.EventHandler[Ansys.ACT.Automation.Mechanical.Connections.SpotWeldConnectionChangedArgs]) -> None:
        """
        remove_OnHitPointAdded method.
        """
        pass

    def add_OnPointPicked(self, value: System.EventHandler) -> None:
        """
        add_OnPointPicked method.
        """
        pass

    def remove_OnPointPicked(self, value: System.EventHandler) -> None:
        """
        remove_OnPointPicked method.
        """
        pass

    def AttachToEvents(self) -> None:
        """
        AttachToEvents method.
        """
        pass

    def DetachEvents(self) -> None:
        """
        DetachEvents method.
        """
        pass

    def GetSpotWeldIds(self) -> tuple[int]:
        """
        GetSpotWeldIds method.
        """
        pass

    def GetSpotWeldLocations(self) -> tuple[float]:
        """
        GetSpotWeldLocations method.
        """
        pass

    def UnitSys(self) -> str:
        """
        UnitSys method.
        """
        pass

    def SetXCoordinate(self, spotWeldId: int, val: Ansys.Core.Units.Quantity) -> None:
        """
        Set the X coordinate given the Spot Weld ID.
        """
        pass

    def SetYCoordinate(self, spotWeldId: int, val: Ansys.Core.Units.Quantity) -> None:
        """
        Set the Y coordinate given the Spot Weld ID.
        """
        pass

    def SetZCoordinate(self, spotWeldId: int, val: Ansys.Core.Units.Quantity) -> None:
        """
        Set the Z coordinate given the Spot Weld ID.
        """
        pass

    def setXYZ(self, spotWeldId: int, point: Ansys.Mechanical.Graphics.Point) -> None:
        """
        setXYZ method.
        """
        pass

    def AddNewSpotWeld(self, customId: int) -> None:
        """
        Add a new spot weld with/without a customID.
        """
        pass

    def RemoveSpotWeld(self, spotWeldId: int) -> None:
        """
        Remove an existing spot weld.
        """
        pass

    def SetCurrentItemsInWorksheet(self, spotWeldIds: typing.List[int]) -> None:
        """
        SetCurrentItemsInWorksheet method.
        """
        pass

    def GetCurrentItemsInWorksheet(self) -> tuple[int]:
        """
        GetCurrentItemsInWorksheet method.
        """
        pass

    def ExportToCSVFile(self, fileName: str) -> None:
        """
        Export the contents to a CSV file.
        """
        pass

    def NotifyOnHitPointAdded(self, x: float, y: float, z: float) -> None:
        """
        NotifyOnHitPointAdded method.
        """
        pass

    def CreateSpotWeldFromHitPoint(self) -> None:
        """
        Add a new spot weld by using a Hit Point.
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


class SpotWeldGroup(object):
    """
    Defines a SpotWeldGroup.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSSpotWeldGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Material(self) -> typing.Optional[str]:
        """
        Gets or sets the Material.
        """
        return None

    @Material.setter
    def Material(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Material.
        """
        pass

    @property
    def NumConnections(self) -> typing.Optional[int]:
        """
        Gets the NumConnections.
        """
        return None

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
    def NumWeldPoints(self) -> typing.Optional[int]:
        """
        Gets the NumWeldPoints.
        """
        return None

    @property
    def SpotWeldFileName(self) -> typing.Optional[str]:
        """
        Gets or sets the SpotWeldFileName.
        """
        return None

    @SpotWeldFileName.setter
    def SpotWeldFileName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the SpotWeldFileName.
        """
        pass

    @property
    def AngleTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AngleTolerance.
        """
        return None

    @AngleTolerance.setter
    def AngleTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AngleTolerance.
        """
        pass

    @property
    def PenetrationTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PenetrationTolerance.
        """
        return None

    @PenetrationTolerance.setter
    def PenetrationTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PenetrationTolerance.
        """
        pass

    @property
    def SnapToEdgeTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SnapToEdgeTolerance.
        """
        return None

    @SnapToEdgeTolerance.setter
    def SnapToEdgeTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SnapToEdgeTolerance.
        """
        pass

    @property
    def WeldRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WeldRadius.
        """
        return None

    @WeldRadius.setter
    def WeldRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WeldRadius.
        """
        pass

    @property
    def WeldSearchDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WeldSearchDistance.
        """
        return None

    @WeldSearchDistance.setter
    def WeldSearchDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WeldSearchDistance.
        """
        pass

    @property
    def ChildrenCreationMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionCreationMethod]:
        """
        Gets or sets the ChildrenCreationMethod.
        """
        return None

    @ChildrenCreationMethod.setter
    def ChildrenCreationMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionCreationMethod]) -> None:
        """
        Gets or sets the ChildrenCreationMethod.
        """
        pass

    @property
    def ConnectionBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]:
        """
        Gets or sets the ConnectionBehavior.
        """
        return None

    @ConnectionBehavior.setter
    def ConnectionBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]) -> None:
        """
        Gets or sets the ConnectionBehavior.
        """
        pass

    @property
    def Units(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the Units.
        """
        return None

    @Units.setter
    def Units(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the Units.
        """
        pass

    @property
    def WeldType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpotWeldTypes]:
        """
        Gets or sets the WeldType.
        """
        return None

    @WeldType.setter
    def WeldType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpotWeldTypes]) -> None:
        """
        Gets or sets the WeldType.
        """
        pass

    @property
    def StiffnessBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]:
        """
        Gets or sets the StiffnessBehavior.
        """
        return None

    @StiffnessBehavior.setter
    def StiffnessBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StiffnessBehavior]) -> None:
        """
        Gets or sets the StiffnessBehavior.
        """
        pass

    @property
    def ShellThicknessEffect(self) -> typing.Optional[bool]:
        """
        Gets or sets the ShellThicknessEffect.
        """
        return None

    @ShellThicknessEffect.setter
    def ShellThicknessEffect(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ShellThicknessEffect.
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
    def Images(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.Image]]:
        """
        Gets the list of associated images.
        """
        return None

    @property
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def GetLargestSpotWeldID(self) -> int:
        """
        GetLargestSpotWeldID method.
        """
        pass

    def SetLargestSpotWeldID(self, largestId: int) -> None:
        """
        SetLargestSpotWeldID method.
        """
        pass

    def GetAllSpotWeldIds(self) -> typing.List[int]:
        """
        GetAllSpotWeldIds method.
        """
        pass

    def AddSpotWeldConnection(self) -> Ansys.ACT.Automation.Mechanical.Connections.SpotWeldConnection:
        """
        Creates a new child SpotWeldConnection.
        """
        pass

    def ExportToFile(self, filePath: str) -> None:
        """
        Exports all spot welds to user selected path.
        """
        pass

    def GenerateSpotWeldConnections(self) -> None:
        """
        Generate spot welds provided in the Weld input file.
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


class Beam(object):
    """
    Defines a Beam.
    """

    @property
    def ReferenceNodeId(self) -> typing.Optional[int]:
        """
        Returns Reference Node Id.
        """
        return None

    @property
    def MobileNodeId(self) -> typing.Optional[int]:
        """
        Returns Mobile Node Id.
        """
        return None

    @property
    def GloballyAvailable(self) -> typing.Optional[bool]:
        """
        Gets or sets the GloballyAvailable.
        """
        return None

    @GloballyAvailable.setter
    def GloballyAvailable(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GloballyAvailable.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSBeamConnectionAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def BeamElementAPDLName(self) -> typing.Optional[str]:
        """
        Gets or sets the BeamElementAPDLName.
        """
        return None

    @BeamElementAPDLName.setter
    def BeamElementAPDLName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the BeamElementAPDLName.
        """
        pass

    @property
    def Material(self) -> typing.Optional[str]:
        """
        Gets or sets the Material.
        """
        return None

    @Material.setter
    def Material(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Material.
        """
        pass

    @property
    def MobileBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @MobileBeamCoincidentLengthFactor.setter
    def MobileBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def MobileBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the MobileBeamMaterial.
        """
        return None

    @MobileBeamMaterial.setter
    def MobileBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the MobileBeamMaterial.
        """
        pass

    @property
    def MobileBody(self) -> typing.Optional[str]:
        """
        Gets the MobileBody.
        """
        return None

    @property
    def ReferenceBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @ReferenceBeamCoincidentLengthFactor.setter
    def ReferenceBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def ReferenceBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        return None

    @ReferenceBeamMaterial.setter
    def ReferenceBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        pass

    @property
    def ReferenceBody(self) -> typing.Optional[str]:
        """
        Gets the ReferenceBody.
        """
        return None

    @property
    def MobileBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileBeamRadius.
        """
        return None

    @MobileBeamRadius.setter
    def MobileBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileBeamRadius.
        """
        pass

    @property
    def MobileXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileXCoordinate.
        """
        return None

    @MobileXCoordinate.setter
    def MobileXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileXCoordinate.
        """
        pass

    @property
    def MobileYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileYCoordinate.
        """
        return None

    @MobileYCoordinate.setter
    def MobileYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileYCoordinate.
        """
        pass

    @property
    def MobileZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileZCoordinate.
        """
        return None

    @MobileZCoordinate.setter
    def MobileZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileZCoordinate.
        """
        pass

    @property
    def MobilePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobilePinballRegion.
        """
        return None

    @MobilePinballRegion.setter
    def MobilePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobilePinballRegion.
        """
        pass

    @property
    def Radius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Radius.
        """
        return None

    @Radius.setter
    def Radius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Radius.
        """
        pass

    @property
    def ReferenceBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        return None

    @ReferenceBeamRadius.setter
    def ReferenceBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        pass

    @property
    def ReferenceXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        return None

    @ReferenceXCoordinate.setter
    def ReferenceXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        pass

    @property
    def ReferenceYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        return None

    @ReferenceYCoordinate.setter
    def ReferenceYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        pass

    @property
    def ReferenceZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        return None

    @ReferenceZCoordinate.setter
    def ReferenceZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        pass

    @property
    def ReferencePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferencePinballRegion.
        """
        return None

    @ReferencePinballRegion.setter
    def ReferencePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferencePinballRegion.
        """
        pass

    @property
    def CrossSection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CrossSectionType]:
        """
        Gets the CrossSection.
        """
        return None

    @property
    def MobileAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the MobileAppliedBy.
        """
        return None

    @MobileAppliedBy.setter
    def MobileAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the MobileAppliedBy.
        """
        pass

    @property
    def MobileBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the MobileBehavior.
        """
        return None

    @MobileBehavior.setter
    def MobileBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the MobileBehavior.
        """
        pass

    @property
    def ReferenceAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        return None

    @ReferenceAppliedBy.setter
    def ReferenceAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        pass

    @property
    def ReferenceBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the ReferenceBehavior.
        """
        return None

    @ReferenceBehavior.setter
    def ReferenceBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the ReferenceBehavior.
        """
        pass

    @property
    def Scope(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringScopingType]:
        """
        Gets or sets the Scope.
        """
        return None

    @Scope.setter
    def Scope(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringScopingType]) -> None:
        """
        Gets or sets the Scope.
        """
        pass

    @property
    def Visible(self) -> typing.Optional[bool]:
        """
        Gets or sets the Visible.
        """
        return None

    @Visible.setter
    def Visible(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Visible.
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
    def MobileCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        return None

    @MobileCoordinateSystem.setter
    def MobileCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        pass

    @property
    def ReferenceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        return None

    @ReferenceCoordinateSystem.setter
    def ReferenceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        pass

    @property
    def MobileLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MobileLocation.
        """
        return None

    @MobileLocation.setter
    def MobileLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MobileLocation.
        """
        pass

    @property
    def ReferenceLocationPoint(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceLocationPoint.
        """
        return None

    @ReferenceLocationPoint.setter
    def ReferenceLocationPoint(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceLocationPoint.
        """
        pass

    @property
    def ReferenceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceLocation.
        """
        return None

    @ReferenceLocation.setter
    def ReferenceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceLocation.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def PromoteToRemotePoint(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Run the PromoteToRemotePoint action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class Bearing(object):
    """
    Defines a Bearing.
    """

    @property
    def ReferenceSet(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets the ReferenceSet.
        """
        return None

    @ReferenceSet.setter
    def ReferenceSet(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets the ReferenceSet.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSBearingAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def AnsBCType(self) -> typing.Optional[int]:
        """
        Gets the AnsBCType.
        """
        return None

    @property
    def MobileBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @MobileBeamCoincidentLengthFactor.setter
    def MobileBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def MobileBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the MobileBeamMaterial.
        """
        return None

    @MobileBeamMaterial.setter
    def MobileBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the MobileBeamMaterial.
        """
        pass

    @property
    def MobileBody(self) -> typing.Optional[str]:
        """
        Gets the MobileBody.
        """
        return None

    @property
    def ReferenceBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @ReferenceBeamCoincidentLengthFactor.setter
    def ReferenceBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def ReferenceBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        return None

    @ReferenceBeamMaterial.setter
    def ReferenceBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        pass

    @property
    def ReferenceBodyName(self) -> typing.Optional[str]:
        """
        Gets the ReferenceBodyName.
        """
        return None

    @property
    def DampingC11(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the DampingC11.
        """
        return None

    @property
    def DampingC12(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the DampingC12.
        """
        return None

    @property
    def DampingC21(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the DampingC21.
        """
        return None

    @property
    def DampingC22(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the DampingC22.
        """
        return None

    @property
    def StiffnessK11(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the StiffnessK11.
        """
        return None

    @property
    def StiffnessK12(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the StiffnessK12.
        """
        return None

    @property
    def StiffnessK21(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the StiffnessK21.
        """
        return None

    @property
    def StiffnessK22(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the StiffnessK22.
        """
        return None

    @property
    def MobileBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileBeamRadius.
        """
        return None

    @MobileBeamRadius.setter
    def MobileBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileBeamRadius.
        """
        pass

    @property
    def MobileXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileXCoordinate.
        """
        return None

    @MobileXCoordinate.setter
    def MobileXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileXCoordinate.
        """
        pass

    @property
    def MobileYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileYCoordinate.
        """
        return None

    @MobileYCoordinate.setter
    def MobileYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileYCoordinate.
        """
        pass

    @property
    def MobileZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileZCoordinate.
        """
        return None

    @MobileZCoordinate.setter
    def MobileZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileZCoordinate.
        """
        pass

    @property
    def MobilePinballSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobilePinballSize.
        """
        return None

    @MobilePinballSize.setter
    def MobilePinballSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobilePinballSize.
        """
        pass

    @property
    def ReferenceBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        return None

    @ReferenceBeamRadius.setter
    def ReferenceBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        pass

    @property
    def ReferenceXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        return None

    @ReferenceXCoordinate.setter
    def ReferenceXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        pass

    @property
    def ReferenceYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        return None

    @ReferenceYCoordinate.setter
    def ReferenceYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        pass

    @property
    def ReferenceZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        return None

    @ReferenceZCoordinate.setter
    def ReferenceZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        pass

    @property
    def ReferencePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferencePinballRegion.
        """
        return None

    @ReferencePinballRegion.setter
    def ReferencePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferencePinballRegion.
        """
        pass

    @property
    def MobileBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the MobileBehavior.
        """
        return None

    @MobileBehavior.setter
    def MobileBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the MobileBehavior.
        """
        pass

    @property
    def ReferenceBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the ReferenceBehavior.
        """
        return None

    @ReferenceBehavior.setter
    def ReferenceBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the ReferenceBehavior.
        """
        pass

    @property
    def ReferenceRotationPlane(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RotationPlane]:
        """
        Gets or sets the ReferenceRotationPlane.
        """
        return None

    @ReferenceRotationPlane.setter
    def ReferenceRotationPlane(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RotationPlane]) -> None:
        """
        Gets or sets the ReferenceRotationPlane.
        """
        pass

    @property
    def ConnectionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionScopingType]:
        """
        Gets or sets the ConnectionType.
        """
        return None

    @ConnectionType.setter
    def ConnectionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConnectionScopingType]) -> None:
        """
        Gets or sets the ConnectionType.
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
    def MobileCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        return None

    @MobileCoordinateSystem.setter
    def MobileCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        pass

    @property
    def ReferenceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        return None

    @ReferenceCoordinateSystem.setter
    def ReferenceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        pass

    @property
    def MobileLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MobileLocation.
        """
        return None

    @MobileLocation.setter
    def MobileLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MobileLocation.
        """
        pass

    @property
    def ReferenceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceLocation.
        """
        return None

    @ReferenceLocation.setter
    def ReferenceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceLocation.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def PromoteToRemotePoint(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Run the PromoteToRemotePoint action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class BodyInteraction(object):
    """
    Defines a BodyInteraction.
    """

    @property
    def ContactType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]:
        """
        Gets or sets the ContactType.
        """
        return None

    @ContactType.setter
    def ContactType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]) -> None:
        """
        Gets or sets the ContactType.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSBodyInteractionAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DecayConstant(self) -> typing.Optional[float]:
        """
        Gets or sets the DecayConstant.
        """
        return None

    @DecayConstant.setter
    def DecayConstant(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DecayConstant.
        """
        pass

    @property
    def DynamicCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the DynamicCoefficient.
        """
        return None

    @DynamicCoefficient.setter
    def DynamicCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DynamicCoefficient.
        """
        pass

    @property
    def NormalForceExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the NormalForceExponent.
        """
        return None

    @NormalForceExponent.setter
    def NormalForceExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NormalForceExponent.
        """
        pass

    @property
    def NormalStressExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the NormalStressExponent.
        """
        return None

    @NormalStressExponent.setter
    def NormalStressExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NormalStressExponent.
        """
        pass

    @property
    def ShearForceExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearForceExponent.
        """
        return None

    @ShearForceExponent.setter
    def ShearForceExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearForceExponent.
        """
        pass

    @property
    def ShearStressExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearStressExponent.
        """
        return None

    @ShearStressExponent.setter
    def ShearStressExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearStressExponent.
        """
        pass

    @property
    def FrictionCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the FrictionCoefficient.
        """
        return None

    @FrictionCoefficient.setter
    def FrictionCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FrictionCoefficient.
        """
        pass

    @property
    def MaximumOffset(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumOffset.
        """
        return None

    @MaximumOffset.setter
    def MaximumOffset(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumOffset.
        """
        pass

    @property
    def NormalForceLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the NormalForceLimit.
        """
        return None

    @NormalForceLimit.setter
    def NormalForceLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the NormalForceLimit.
        """
        pass

    @property
    def NormalStressLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the NormalStressLimit.
        """
        return None

    @NormalStressLimit.setter
    def NormalStressLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the NormalStressLimit.
        """
        pass

    @property
    def ShearForceLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ShearForceLimit.
        """
        return None

    @ShearForceLimit.setter
    def ShearForceLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ShearForceLimit.
        """
        pass

    @property
    def ShearStressLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ShearStressLimit.
        """
        return None

    @ShearStressLimit.setter
    def ShearStressLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ShearStressLimit.
        """
        pass

    @property
    def Breakable(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BondedBreakableType]:
        """
        Gets or sets the Breakable.
        """
        return None

    @Breakable.setter
    def Breakable(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BondedBreakableType]) -> None:
        """
        Gets or sets the Breakable.
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


class ContactRegion(object):
    """
    Defines a ContactRegion.
    """

    @property
    def ContactAPDLName(self) -> typing.Optional[str]:
        """
        Gets or sets the ContactAPDLName.
        """
        return None

    @ContactAPDLName.setter
    def ContactAPDLName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ContactAPDLName.
        """
        pass

    @property
    def TargetAPDLName(self) -> typing.Optional[str]:
        """
        Gets or sets the TargetAPDLName.
        """
        return None

    @TargetAPDLName.setter
    def TargetAPDLName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the TargetAPDLName.
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
    def AutomaticNormalStiffness(self) -> typing.Optional[bool]:
        """
        Gets or sets the AutomaticNormalStiffness.
        """
        return None

    @AutomaticNormalStiffness.setter
    def AutomaticNormalStiffness(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AutomaticNormalStiffness.
        """
        pass

    @property
    def BeamMaterialName(self) -> typing.Optional[str]:
        """
        Gets or sets the BeamMaterialName.
        """
        return None

    @BeamMaterialName.setter
    def BeamMaterialName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the BeamMaterialName.
        """
        pass

    @property
    def BeamBeamDetection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BeamBeamContactDetectionType]:
        """
        Gets or sets the BeamBeamDetection.
        """
        return None

    @BeamBeamDetection.setter
    def BeamBeamDetection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BeamBeamContactDetectionType]) -> None:
        """
        Gets or sets the BeamBeamDetection.
        """
        pass

    @property
    def GloballyAvailable(self) -> typing.Optional[bool]:
        """
        Gets or sets the GloballyAvailable.
        """
        return None

    @GloballyAvailable.setter
    def GloballyAvailable(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GloballyAvailable.
        """
        pass

    @property
    def ContactType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]:
        """
        ContactType property.
        """
        return None

    @ContactType.setter
    def ContactType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactType]) -> None:
        """
        ContactType property.
        """
        pass

    @property
    def ConstraintType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactConstraintType]:
        """
        Gets or sets the ConstraintType.
        """
        return None

    @ConstraintType.setter
    def ConstraintType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactConstraintType]) -> None:
        """
        Gets or sets the ConstraintType.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSContactRegionAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Material(self) -> typing.Optional[str]:
        """
        Gets or sets the Material.
        """
        return None

    @Material.setter
    def Material(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Material.
        """
        pass

    @property
    def StabilizationDampingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the StabilizationDampingFactor.
        """
        return None

    @StabilizationDampingFactor.setter
    def StabilizationDampingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StabilizationDampingFactor.
        """
        pass

    @property
    def DecayConstant(self) -> typing.Optional[float]:
        """
        Gets or sets the DecayConstant.
        """
        return None

    @DecayConstant.setter
    def DecayConstant(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DecayConstant.
        """
        pass

    @property
    def DynamicCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the DynamicCoefficient.
        """
        return None

    @DynamicCoefficient.setter
    def DynamicCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DynamicCoefficient.
        """
        pass

    @property
    def ElasticSlipToleranceFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticSlipToleranceFactor.
        """
        return None

    @ElasticSlipToleranceFactor.setter
    def ElasticSlipToleranceFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticSlipToleranceFactor.
        """
        pass

    @property
    def FrictionCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the FrictionCoefficient.
        """
        return None

    @FrictionCoefficient.setter
    def FrictionCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FrictionCoefficient.
        """
        pass

    @property
    def InitialClearanceFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the InitialClearanceFactor.
        """
        return None

    @InitialClearanceFactor.setter
    def InitialClearanceFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the InitialClearanceFactor.
        """
        pass

    @property
    def NormalForceExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the NormalForceExponent.
        """
        return None

    @NormalForceExponent.setter
    def NormalForceExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NormalForceExponent.
        """
        pass

    @property
    def NormalStiffnessFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the NormalStiffnessFactor.
        """
        return None

    @NormalStiffnessFactor.setter
    def NormalStiffnessFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NormalStiffnessFactor.
        """
        pass

    @property
    def NormalStressExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the NormalStressExponent.
        """
        return None

    @NormalStressExponent.setter
    def NormalStressExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NormalStressExponent.
        """
        pass

    @property
    def PenetrationToleranceFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PenetrationToleranceFactor.
        """
        return None

    @PenetrationToleranceFactor.setter
    def PenetrationToleranceFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PenetrationToleranceFactor.
        """
        pass

    @property
    def PinballFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PinballFactor.
        """
        return None

    @PinballFactor.setter
    def PinballFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PinballFactor.
        """
        pass

    @property
    def PressureAtZeroPenetrationFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PressureAtZeroPenetrationFactor.
        """
        return None

    @PressureAtZeroPenetrationFactor.setter
    def PressureAtZeroPenetrationFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PressureAtZeroPenetrationFactor.
        """
        pass

    @property
    def RestitutionFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the RestitutionFactor.
        """
        return None

    @RestitutionFactor.setter
    def RestitutionFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the RestitutionFactor.
        """
        pass

    @property
    def ShearForceExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearForceExponent.
        """
        return None

    @ShearForceExponent.setter
    def ShearForceExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearForceExponent.
        """
        pass

    @property
    def ShearStressExponent(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearStressExponent.
        """
        return None

    @ShearStressExponent.setter
    def ShearStressExponent(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearStressExponent.
        """
        pass

    @property
    def ContactBodies(self) -> typing.Optional[str]:
        """
        Gets the ContactBodies.
        """
        return None

    @property
    def TargetBodies(self) -> typing.Optional[str]:
        """
        Gets the TargetBodies.
        """
        return None

    @property
    def AutomaticDetectionValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the AutomaticDetectionValue.
        """
        return None

    @property
    def BeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BeamRadius.
        """
        return None

    @BeamRadius.setter
    def BeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BeamRadius.
        """
        pass

    @property
    def ThreadAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ThreadAngle.
        """
        return None

    @ThreadAngle.setter
    def ThreadAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ThreadAngle.
        """
        pass

    @property
    def MeanPitchDiameter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MeanPitchDiameter.
        """
        return None

    @MeanPitchDiameter.setter
    def MeanPitchDiameter(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MeanPitchDiameter.
        """
        pass

    @property
    def PitchDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PitchDistance.
        """
        return None

    @PitchDistance.setter
    def PitchDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PitchDistance.
        """
        pass

    @property
    def BondedMaximumOffset(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BondedMaximumOffset.
        """
        return None

    @BondedMaximumOffset.setter
    def BondedMaximumOffset(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BondedMaximumOffset.
        """
        pass

    @property
    def ElasticSlipToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElasticSlipToleranceValue.
        """
        return None

    @ElasticSlipToleranceValue.setter
    def ElasticSlipToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElasticSlipToleranceValue.
        """
        pass

    @property
    def ElectricCapacitanceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElectricCapacitanceValue.
        """
        return None

    @ElectricCapacitanceValue.setter
    def ElectricCapacitanceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElectricCapacitanceValue.
        """
        pass

    @property
    def ElectricConductanceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ElectricConductanceValue.
        """
        return None

    @ElectricConductanceValue.setter
    def ElectricConductanceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ElectricConductanceValue.
        """
        pass

    @property
    def InitialClearanceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the InitialClearanceValue.
        """
        return None

    @InitialClearanceValue.setter
    def InitialClearanceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the InitialClearanceValue.
        """
        pass

    @property
    def NormalForceLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the NormalForceLimit.
        """
        return None

    @NormalForceLimit.setter
    def NormalForceLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the NormalForceLimit.
        """
        pass

    @property
    def NormalStiffnessValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the NormalStiffnessValue.
        """
        return None

    @NormalStiffnessValue.setter
    def NormalStiffnessValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the NormalStiffnessValue.
        """
        pass

    @property
    def NormalStressLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the NormalStressLimit.
        """
        return None

    @NormalStressLimit.setter
    def NormalStressLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the NormalStressLimit.
        """
        pass

    @property
    def PenetrationToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PenetrationToleranceValue.
        """
        return None

    @PenetrationToleranceValue.setter
    def PenetrationToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PenetrationToleranceValue.
        """
        pass

    @property
    def PinballRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PinballRadius.
        """
        return None

    @PinballRadius.setter
    def PinballRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PinballRadius.
        """
        pass

    @property
    def PressureAtZeroPenetrationValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PressureAtZeroPenetrationValue.
        """
        return None

    @PressureAtZeroPenetrationValue.setter
    def PressureAtZeroPenetrationValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PressureAtZeroPenetrationValue.
        """
        pass

    @property
    def ShearForceLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ShearForceLimit.
        """
        return None

    @ShearForceLimit.setter
    def ShearForceLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ShearForceLimit.
        """
        pass

    @property
    def ShearStressLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ShearStressLimit.
        """
        return None

    @ShearStressLimit.setter
    def ShearStressLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ShearStressLimit.
        """
        pass

    @property
    def ThermalConductanceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ThermalConductanceValue.
        """
        return None

    @ThermalConductanceValue.setter
    def ThermalConductanceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ThermalConductanceValue.
        """
        pass

    @property
    def TrimTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TrimTolerance.
        """
        return None

    @TrimTolerance.setter
    def TrimTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TrimTolerance.
        """
        pass

    @property
    def UserOffset(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the UserOffset.
        """
        return None

    @UserOffset.setter
    def UserOffset(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the UserOffset.
        """
        pass

    @property
    def LineLineDetection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LineLineContactDetectionType]:
        """
        Gets or sets the LineLineDetection.
        """
        return None

    @LineLineDetection.setter
    def LineLineDetection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LineLineContactDetectionType]) -> None:
        """
        Gets or sets the LineLineDetection.
        """
        pass

    @property
    def BeamBeamModel(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BeamBeamModel]:
        """
        Gets or sets the BeamBeamModel.
        """
        return None

    @BeamBeamModel.setter
    def BeamBeamModel(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BeamBeamModel]) -> None:
        """
        Gets or sets the BeamBeamModel.
        """
        pass

    @property
    def Handedness(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBoltThreadHand]:
        """
        Gets or sets the Handedness.
        """
        return None

    @Handedness.setter
    def Handedness(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBoltThreadHand]) -> None:
        """
        Gets or sets the Handedness.
        """
        pass

    @property
    def ThreadType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBoltThreadType]:
        """
        Gets or sets the ThreadType.
        """
        return None

    @ThreadType.setter
    def ThreadType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBoltThreadType]) -> None:
        """
        Gets or sets the ThreadType.
        """
        pass

    @property
    def Breakable(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BondedBreakableType]:
        """
        Gets or sets the Breakable.
        """
        return None

    @Breakable.setter
    def Breakable(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BondedBreakableType]) -> None:
        """
        Gets or sets the Breakable.
        """
        pass

    @property
    def ContactGeometryCorrection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactCorrection]:
        """
        Gets or sets the ContactGeometryCorrection.
        """
        return None

    @ContactGeometryCorrection.setter
    def ContactGeometryCorrection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactCorrection]) -> None:
        """
        Gets or sets the ContactGeometryCorrection.
        """
        pass

    @property
    def ContactFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFormulation]:
        """
        Gets or sets the ContactFormulation.
        """
        return None

    @ContactFormulation.setter
    def ContactFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFormulation]) -> None:
        """
        Gets or sets the ContactFormulation.
        """
        pass

    @property
    def ContactOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactOrientation]:
        """
        Gets or sets the ContactOrientation.
        """
        return None

    @ContactOrientation.setter
    def ContactOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactOrientation]) -> None:
        """
        Gets or sets the ContactOrientation.
        """
        pass

    @property
    def ContactShellFace(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the ContactShellFace.
        """
        return None

    @ContactShellFace.setter
    def ContactShellFace(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the ContactShellFace.
        """
        pass

    @property
    def ContinuousDistanceComputation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]:
        """
        Gets or sets the ContinuousDistanceComputation.
        """
        return None

    @ContinuousDistanceComputation.setter
    def ContinuousDistanceComputation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]) -> None:
        """
        Gets or sets the ContinuousDistanceComputation.
        """
        pass

    @property
    def DetectionMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactDetectionPoint]:
        """
        Gets or sets the DetectionMethod.
        """
        return None

    @DetectionMethod.setter
    def DetectionMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactDetectionPoint]) -> None:
        """
        Gets or sets the DetectionMethod.
        """
        pass

    @property
    def EdgeContactType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EdgeContactType]:
        """
        Gets or sets the EdgeContactType.
        """
        return None

    @EdgeContactType.setter
    def EdgeContactType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EdgeContactType]) -> None:
        """
        Gets or sets the EdgeContactType.
        """
        pass

    @property
    def InitialClearance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InitialClearanceType]:
        """
        Gets or sets the InitialClearance.
        """
        return None

    @InitialClearance.setter
    def InitialClearance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InitialClearanceType]) -> None:
        """
        Gets or sets the InitialClearance.
        """
        pass

    @property
    def InterfaceTreatment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactInitialEffect]:
        """
        Gets or sets the InterfaceTreatment.
        """
        return None

    @InterfaceTreatment.setter
    def InterfaceTreatment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactInitialEffect]) -> None:
        """
        Gets or sets the InterfaceTreatment.
        """
        pass

    @property
    def ScopeMode(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]:
        """
        Gets the ScopeMode.
        """
        return None

    @property
    def ModelingOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelingOption]:
        """
        Gets or sets the ModelingOption.
        """
        return None

    @ModelingOption.setter
    def ModelingOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelingOption]) -> None:
        """
        Gets or sets the ModelingOption.
        """
        pass

    @property
    def NormalStiffnessValueType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementControlsNormalStiffnessType]:
        """
        Gets or sets the NormalStiffnessValueType.
        """
        return None

    @NormalStiffnessValueType.setter
    def NormalStiffnessValueType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ElementControlsNormalStiffnessType]) -> None:
        """
        Gets or sets the NormalStiffnessValueType.
        """
        pass

    @property
    def PinballRegion(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactPinballType]:
        """
        Gets or sets the PinballRegion.
        """
        return None

    @PinballRegion.setter
    def PinballRegion(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactPinballType]) -> None:
        """
        Gets or sets the PinballRegion.
        """
        pass

    @property
    def PressureAtZeroPenetration(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.PressureAtZeroPenetrationType]:
        """
        Gets or sets the PressureAtZeroPenetration.
        """
        return None

    @PressureAtZeroPenetration.setter
    def PressureAtZeroPenetration(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.PressureAtZeroPenetrationType]) -> None:
        """
        Gets or sets the PressureAtZeroPenetration.
        """
        pass

    @property
    def RBDContactDetection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DSRBDContactDetection]:
        """
        Gets or sets the RBDContactDetection.
        """
        return None

    @RBDContactDetection.setter
    def RBDContactDetection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DSRBDContactDetection]) -> None:
        """
        Gets or sets the RBDContactDetection.
        """
        pass

    @property
    def SmallSliding(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSmallSlidingType]:
        """
        Gets or sets the SmallSliding.
        """
        return None

    @SmallSliding.setter
    def SmallSliding(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSmallSlidingType]) -> None:
        """
        Gets or sets the SmallSliding.
        """
        pass

    @property
    def Behavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBehavior]:
        """
        Gets or sets the Behavior.
        """
        return None

    @Behavior.setter
    def Behavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactBehavior]) -> None:
        """
        Gets or sets the Behavior.
        """
        pass

    @property
    def TargetGeometryCorrection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TargetCorrection]:
        """
        Gets or sets the TargetGeometryCorrection.
        """
        return None

    @TargetGeometryCorrection.setter
    def TargetGeometryCorrection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TargetCorrection]) -> None:
        """
        Gets or sets the TargetGeometryCorrection.
        """
        pass

    @property
    def TargetOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TargetOrientation]:
        """
        Gets or sets the TargetOrientation.
        """
        return None

    @TargetOrientation.setter
    def TargetOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TargetOrientation]) -> None:
        """
        Gets or sets the TargetOrientation.
        """
        pass

    @property
    def TargetShellFace(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the TargetShellFace.
        """
        return None

    @TargetShellFace.setter
    def TargetShellFace(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the TargetShellFace.
        """
        pass

    @property
    def TimeStepControls(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactTimeStepControls]:
        """
        Gets or sets the TimeStepControls.
        """
        return None

    @TimeStepControls.setter
    def TimeStepControls(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactTimeStepControls]) -> None:
        """
        Gets or sets the TimeStepControls.
        """
        pass

    @property
    def TrimContact(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactTrimType]:
        """
        Gets or sets the TrimContact.
        """
        return None

    @TrimContact.setter
    def TrimContact(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactTrimType]) -> None:
        """
        Gets or sets the TrimContact.
        """
        pass

    @property
    def UpdateStiffness(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.UpdateContactStiffness]:
        """
        Gets or sets the UpdateStiffness.
        """
        return None

    @UpdateStiffness.setter
    def UpdateStiffness(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.UpdateContactStiffness]) -> None:
        """
        Gets or sets the UpdateStiffness.
        """
        pass

    @property
    def ElasticSlipTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactElasticSlipToleranceType]:
        """
        Gets or sets the ElasticSlipTolerance.
        """
        return None

    @ElasticSlipTolerance.setter
    def ElasticSlipTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactElasticSlipToleranceType]) -> None:
        """
        Gets or sets the ElasticSlipTolerance.
        """
        pass

    @property
    def PenetrationTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactPenetrationToleranceType]:
        """
        Gets or sets the PenetrationTolerance.
        """
        return None

    @PenetrationTolerance.setter
    def PenetrationTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactPenetrationToleranceType]) -> None:
        """
        Gets or sets the PenetrationTolerance.
        """
        pass

    @property
    def DisplayElementNormal(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayElementNormal.
        """
        return None

    @DisplayElementNormal.setter
    def DisplayElementNormal(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayElementNormal.
        """
        pass

    @property
    def FlipContact(self) -> typing.Optional[bool]:
        """
        Gets or sets the FlipContact.
        """
        return None

    @FlipContact.setter
    def FlipContact(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FlipContact.
        """
        pass

    @property
    def FlipTarget(self) -> typing.Optional[bool]:
        """
        Gets or sets the FlipTarget.
        """
        return None

    @FlipTarget.setter
    def FlipTarget(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FlipTarget.
        """
        pass

    @property
    def Protected(self) -> typing.Optional[bool]:
        """
        Gets or sets the Protected.
        """
        return None

    @Protected.setter
    def Protected(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Protected.
        """
        pass

    @property
    def ShellThicknessEffect(self) -> typing.Optional[bool]:
        """
        Gets or sets the ShellThicknessEffect.
        """
        return None

    @ShellThicknessEffect.setter
    def ShellThicknessEffect(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ShellThicknessEffect.
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
    def AutomaticElectricCapacitance(self) -> typing.Optional[bool]:
        """
        Gets or sets the AutomaticElectricCapacitance.
        """
        return None

    @AutomaticElectricCapacitance.setter
    def AutomaticElectricCapacitance(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AutomaticElectricCapacitance.
        """
        pass

    @property
    def AutomaticElectricConductance(self) -> typing.Optional[bool]:
        """
        Gets or sets the AutomaticElectricConductance.
        """
        return None

    @AutomaticElectricConductance.setter
    def AutomaticElectricConductance(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AutomaticElectricConductance.
        """
        pass

    @property
    def AutomaticThermalConductance(self) -> typing.Optional[bool]:
        """
        Gets or sets the AutomaticThermalConductance.
        """
        return None

    @AutomaticThermalConductance.setter
    def AutomaticThermalConductance(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AutomaticThermalConductance.
        """
        pass

    @property
    def ContactCenterPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ContactCenterPoint.
        """
        return None

    @ContactCenterPoint.setter
    def ContactCenterPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ContactCenterPoint.
        """
        pass

    @property
    def ContactEndingPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ContactEndingPoint.
        """
        return None

    @ContactEndingPoint.setter
    def ContactEndingPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ContactEndingPoint.
        """
        pass

    @property
    def ContactStartingPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ContactStartingPoint.
        """
        return None

    @ContactStartingPoint.setter
    def ContactStartingPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ContactStartingPoint.
        """
        pass

    @property
    def SharedSourceBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedSourceBody.
        """
        return None

    @SharedSourceBody.setter
    def SharedSourceBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedSourceBody.
        """
        pass

    @property
    def SharedTargetBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedTargetBody.
        """
        return None

    @SharedTargetBody.setter
    def SharedTargetBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedTargetBody.
        """
        pass

    @property
    def TargetCenterPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the TargetCenterPoint.
        """
        return None

    @TargetCenterPoint.setter
    def TargetCenterPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the TargetCenterPoint.
        """
        pass

    @property
    def TargetEndingPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the TargetEndingPoint.
        """
        return None

    @TargetEndingPoint.setter
    def TargetEndingPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the TargetEndingPoint.
        """
        pass

    @property
    def TargetStartingPoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the TargetStartingPoint.
        """
        return None

    @TargetStartingPoint.setter
    def TargetStartingPoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the TargetStartingPoint.
        """
        pass

    @property
    def SharedSourceReverseNormalLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SharedSourceReverseNormalLocation.
        """
        return None

    @SharedSourceReverseNormalLocation.setter
    def SharedSourceReverseNormalLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SharedSourceReverseNormalLocation.
        """
        pass

    @property
    def SharedTargetReverseNormalLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the SharedTargetReverseNormalLocation.
        """
        return None

    @SharedTargetReverseNormalLocation.setter
    def SharedTargetReverseNormalLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the SharedTargetReverseNormalLocation.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def SearchConnectionsForDuplicatePairs(self) -> None:
        """
        Run the SearchConnectionsForDuplicatePairs action.
        """
        pass

    def FlipContactTarget(self) -> None:
        """
        Run the FlipContactTarget action.
        """
        pass

    def SetDefaultAPDLNames(self) -> None:
        """
        Run the SetDefaultAPDLNames action.
        """
        pass

    def SaveContactRegionSettings(self, fName: str) -> None:
        """
        Run the SaveContactRegionSettings action.
        """
        pass

    def LoadContactRegionSettings(self, fName: str) -> None:
        """
        Run the LoadContactRegionSettings action.
        """
        pass

    @typing.overload
    def ResetToDefault(self) -> None:
        ...

    @typing.overload
    def ResetToDefault(self, b_Verify: bool) -> None:
        ...

    def ResetToDefault(self, *args: typing.Any) -> None:
        """
        Run the ResetToDefault action.
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def PromoteToRemotePoint(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Run the PromoteToRemotePoint action.
        """
        pass

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def NoSeparationSlidingWarning(self) -> None:
        """
        NoSeparationSlidingWarning method.
        """
        pass

    def ProjectedUncoupleUtoROTWaring(self) -> None:
        """
        ProjectedUncoupleUtoROTWaring method.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
        """
        pass

    def AddPythonCodeEventBased(self) -> Ansys.ACT.Automation.Mechanical.PythonCodeEventBased:
        """
        Creates a new PythonCodeEventBased
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


class ContactTool(object):
    """
    Defines a ContactTool.
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
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSContactToolAuto]:
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

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    def GetWorksheet(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactToolWorksheet:
        """
        GetWorksheet method.
        """
        pass

    def GenerateInitialContactResults(self) -> None:
        """
        Generate Initial Contact Results and Mesh Parts
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


class Spring(object):
    """
    Defines a Spring.
    """

    @property
    def NonLinearLongitudinalStiffness(self) -> typing.Optional[Ansys.ACT.Mechanical.Fields.Field]:
        """
        Gets the non linear longitudinal stiffness defined in the tabular data.
        """
        return None

    @property
    def LongitudinalStiffness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the constant longitudinal stiffness (expressed in N/m).
        """
        return None

    @LongitudinalStiffness.setter
    def LongitudinalStiffness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the constant longitudinal stiffness (expressed in N/m).
        """
        pass

    @property
    def ReferenceNodeId(self) -> typing.Optional[int]:
        """
        Returns Reference Node Id.
        """
        return None

    @property
    def MobileNodeId(self) -> typing.Optional[int]:
        """
        Returns Mobile Node Id.
        """
        return None

    @property
    def GloballyAvailable(self) -> typing.Optional[bool]:
        """
        Gets or sets the GloballyAvailable.
        """
        return None

    @GloballyAvailable.setter
    def GloballyAvailable(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GloballyAvailable.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSSpringAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Material(self) -> typing.Optional[str]:
        """
        Gets or sets the Material.
        """
        return None

    @Material.setter
    def Material(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Material.
        """
        pass

    @property
    def MobileBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @MobileBeamCoincidentLengthFactor.setter
    def MobileBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def MobileBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the MobileBeamMaterial.
        """
        return None

    @MobileBeamMaterial.setter
    def MobileBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the MobileBeamMaterial.
        """
        pass

    @property
    def MobileBody(self) -> typing.Optional[str]:
        """
        Gets the MobileBody.
        """
        return None

    @property
    def ReferenceBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @ReferenceBeamCoincidentLengthFactor.setter
    def ReferenceBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def ReferenceBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        return None

    @ReferenceBeamMaterial.setter
    def ReferenceBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        pass

    @property
    def ReferenceBody(self) -> typing.Optional[str]:
        """
        Gets the ReferenceBody.
        """
        return None

    @property
    def SpringElementAPDLName(self) -> typing.Optional[str]:
        """
        Gets or sets the SpringElementAPDLName.
        """
        return None

    @SpringElementAPDLName.setter
    def SpringElementAPDLName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the SpringElementAPDLName.
        """
        pass

    @property
    def MobileBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileBeamRadius.
        """
        return None

    @MobileBeamRadius.setter
    def MobileBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileBeamRadius.
        """
        pass

    @property
    def MobileXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileXCoordinate.
        """
        return None

    @MobileXCoordinate.setter
    def MobileXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileXCoordinate.
        """
        pass

    @property
    def MobileYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileYCoordinate.
        """
        return None

    @MobileYCoordinate.setter
    def MobileYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileYCoordinate.
        """
        pass

    @property
    def MobileZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileZCoordinate.
        """
        return None

    @MobileZCoordinate.setter
    def MobileZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileZCoordinate.
        """
        pass

    @property
    def ReferenceBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        return None

    @ReferenceBeamRadius.setter
    def ReferenceBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        pass

    @property
    def ReferenceXCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        return None

    @ReferenceXCoordinate.setter
    def ReferenceXCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceXCoordinate.
        """
        pass

    @property
    def ReferenceYCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        return None

    @ReferenceYCoordinate.setter
    def ReferenceYCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceYCoordinate.
        """
        pass

    @property
    def ReferenceZCoordinate(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        return None

    @ReferenceZCoordinate.setter
    def ReferenceZCoordinate(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceZCoordinate.
        """
        pass

    @property
    def SpringLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the SpringLength.
        """
        return None

    @property
    def LongitudinalDamping(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the LongitudinalDamping.
        """
        return None

    @LongitudinalDamping.setter
    def LongitudinalDamping(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the LongitudinalDamping.
        """
        pass

    @property
    def MobilePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobilePinballRegion.
        """
        return None

    @MobilePinballRegion.setter
    def MobilePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobilePinballRegion.
        """
        pass

    @property
    def FreeLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FreeLength.
        """
        return None

    @FreeLength.setter
    def FreeLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FreeLength.
        """
        pass

    @property
    def Load(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Load.
        """
        return None

    @Load.setter
    def Load(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Load.
        """
        pass

    @property
    def Rotation(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Rotation.
        """
        return None

    @Rotation.setter
    def Rotation(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Rotation.
        """
        pass

    @property
    def Torque(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Torque.
        """
        return None

    @Torque.setter
    def Torque(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Torque.
        """
        pass

    @property
    def ReferencePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferencePinballRegion.
        """
        return None

    @ReferencePinballRegion.setter
    def ReferencePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferencePinballRegion.
        """
        pass

    @property
    def TorsionalDamping(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TorsionalDamping.
        """
        return None

    @TorsionalDamping.setter
    def TorsionalDamping(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TorsionalDamping.
        """
        pass

    @property
    def TorsionalStiffness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TorsionalStiffness.
        """
        return None

    @TorsionalStiffness.setter
    def TorsionalStiffness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TorsionalStiffness.
        """
        pass

    @property
    def MobileAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the MobileAppliedBy.
        """
        return None

    @MobileAppliedBy.setter
    def MobileAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the MobileAppliedBy.
        """
        pass

    @property
    def MobileScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the MobileScopingMethod.
        """
        return None

    @MobileScopingMethod.setter
    def MobileScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the MobileScopingMethod.
        """
        pass

    @property
    def ReferenceAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        return None

    @ReferenceAppliedBy.setter
    def ReferenceAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        pass

    @property
    def ReferenceScopingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]:
        """
        Gets or sets the ReferenceScopingMethod.
        """
        return None

    @ReferenceScopingMethod.setter
    def ReferenceScopingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeometryDefineByType]) -> None:
        """
        Gets or sets the ReferenceScopingMethod.
        """
        pass

    @property
    def SpringBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringBehavior]:
        """
        Gets or sets the SpringBehavior.
        """
        return None

    @SpringBehavior.setter
    def SpringBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringBehavior]) -> None:
        """
        Gets or sets the SpringBehavior.
        """
        pass

    @property
    def MobileBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the MobileBehavior.
        """
        return None

    @MobileBehavior.setter
    def MobileBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the MobileBehavior.
        """
        pass

    @property
    def PreloadType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringPreloadType]:
        """
        Gets or sets the PreloadType.
        """
        return None

    @PreloadType.setter
    def PreloadType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringPreloadType]) -> None:
        """
        Gets or sets the PreloadType.
        """
        pass

    @property
    def ReferenceBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the ReferenceBehavior.
        """
        return None

    @ReferenceBehavior.setter
    def ReferenceBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the ReferenceBehavior.
        """
        pass

    @property
    def Scope(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringScopingType]:
        """
        Gets or sets the Scope.
        """
        return None

    @Scope.setter
    def Scope(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringScopingType]) -> None:
        """
        Gets or sets the Scope.
        """
        pass

    @property
    def SpringType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringType]:
        """
        Gets or sets the SpringType.
        """
        return None

    @SpringType.setter
    def SpringType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringType]) -> None:
        """
        Gets or sets the SpringType.
        """
        pass

    @property
    def Visible(self) -> typing.Optional[bool]:
        """
        Gets or sets the Visible.
        """
        return None

    @Visible.setter
    def Visible(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Visible.
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
    def MobileCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        return None

    @MobileCoordinateSystem.setter
    def MobileCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        pass

    @property
    def ReferenceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        return None

    @ReferenceCoordinateSystem.setter
    def ReferenceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        pass

    @property
    def MobileLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MobileLocation.
        """
        return None

    @MobileLocation.setter
    def MobileLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MobileLocation.
        """
        pass

    @property
    def MobileScopeLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MobileScopeLocation.
        """
        return None

    @MobileScopeLocation.setter
    def MobileScopeLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MobileScopeLocation.
        """
        pass

    @property
    def ReferenceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceLocation.
        """
        return None

    @ReferenceLocation.setter
    def ReferenceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceLocation.
        """
        pass

    @property
    def ReferenceScopeLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceScopeLocation.
        """
        return None

    @ReferenceScopeLocation.setter
    def ReferenceScopeLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceScopeLocation.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def PromoteToRemotePoint(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Run the PromoteToRemotePoint action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class Joint(object):
    """
    Defines a Joint.
    """

    @property
    def BushingWorksheet(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.IWorksheet]:
        """
        
            Returns the Bushing Coeffients worksheet associated with Bushing Joint.
            
        """
        return None

    @property
    def ReferenceNodeId(self) -> typing.Optional[int]:
        """
        Returns Reference Node Id.
        """
        return None

    @property
    def MobileNodeId(self) -> typing.Optional[int]:
        """
        Returns Mobile Node Id.
        """
        return None

    @property
    def GloballyAvailable(self) -> typing.Optional[bool]:
        """
        Gets or sets the GloballyAvailable.
        """
        return None

    @GloballyAvailable.setter
    def GloballyAvailable(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GloballyAvailable.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSJointAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FrictionCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the FrictionCoefficient.
        """
        return None

    @FrictionCoefficient.setter
    def FrictionCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FrictionCoefficient.
        """
        pass

    @property
    def JointElementAPDLName(self) -> typing.Optional[str]:
        """
        Gets or sets the JointElementAPDLName.
        """
        return None

    @JointElementAPDLName.setter
    def JointElementAPDLName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the JointElementAPDLName.
        """
        pass

    @property
    def RestitutionFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the RestitutionFactor.
        """
        return None

    @RestitutionFactor.setter
    def RestitutionFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the RestitutionFactor.
        """
        pass

    @property
    def MobileBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @MobileBeamCoincidentLengthFactor.setter
    def MobileBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on mobile side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def MobileBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the MobileBeamMaterial.
        """
        return None

    @MobileBeamMaterial.setter
    def MobileBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the MobileBeamMaterial.
        """
        pass

    @property
    def MobileBody(self) -> typing.Optional[str]:
        """
        Gets the MobileBody.
        """
        return None

    @property
    def ReferenceBeamCoincidentLengthFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        return None

    @ReferenceBeamCoincidentLengthFactor.setter
    def ReferenceBeamCoincidentLengthFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Coincident Length Factor on reference side that scales the stiffness of the connection between the beam elements and the remote point. This property is applicable when the Behavior property is set to “Beam”. Default: 1.
        """
        pass

    @property
    def ReferenceBeamMaterial(self) -> typing.Optional[str]:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        return None

    @ReferenceBeamMaterial.setter
    def ReferenceBeamMaterial(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ReferenceBeamMaterial.
        """
        pass

    @property
    def ReferenceBody(self) -> typing.Optional[str]:
        """
        Gets the ReferenceBody.
        """
        return None

    @property
    def EffectiveLength(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EffectiveLength.
        """
        return None

    @EffectiveLength.setter
    def EffectiveLength(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EffectiveLength.
        """
        pass

    @property
    def InnerRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the InnerRadius.
        """
        return None

    @InnerRadius.setter
    def InnerRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the InnerRadius.
        """
        pass

    @property
    def OuterRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the OuterRadius.
        """
        return None

    @OuterRadius.setter
    def OuterRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the OuterRadius.
        """
        pass

    @property
    def Radius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Radius.
        """
        return None

    @Radius.setter
    def Radius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Radius.
        """
        pass

    @property
    def MobilePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobilePinballRegion.
        """
        return None

    @MobilePinballRegion.setter
    def MobilePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobilePinballRegion.
        """
        pass

    @property
    def ReferencePinballRegion(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferencePinballRegion.
        """
        return None

    @ReferencePinballRegion.setter
    def ReferencePinballRegion(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferencePinballRegion.
        """
        pass

    @property
    def RadialGapHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RadialGapHeight.
        """
        return None

    @RadialGapHeight.setter
    def RadialGapHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RadialGapHeight.
        """
        pass

    @property
    def RadialGapInnerDiameter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RadialGapInnerDiameter.
        """
        return None

    @RadialGapInnerDiameter.setter
    def RadialGapInnerDiameter(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RadialGapInnerDiameter.
        """
        pass

    @property
    def RadialOuterDiameter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RadialOuterDiameter.
        """
        return None

    @RadialOuterDiameter.setter
    def RadialOuterDiameter(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RadialOuterDiameter.
        """
        pass

    @property
    def ScrewPitch(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ScrewPitch.
        """
        return None

    @ScrewPitch.setter
    def ScrewPitch(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ScrewPitch.
        """
        pass

    @property
    def RXMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RXMaximum.
        """
        return None

    @RXMaximum.setter
    def RXMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RXMaximum.
        """
        pass

    @property
    def RXMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RXMinimum.
        """
        return None

    @RXMinimum.setter
    def RXMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RXMinimum.
        """
        pass

    @property
    def RYMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RYMaximum.
        """
        return None

    @RYMaximum.setter
    def RYMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RYMaximum.
        """
        pass

    @property
    def RYMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RYMinimum.
        """
        return None

    @RYMinimum.setter
    def RYMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RYMinimum.
        """
        pass

    @property
    def RZMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RZMaximum.
        """
        return None

    @RZMaximum.setter
    def RZMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RZMaximum.
        """
        pass

    @property
    def RZMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RZMinimum.
        """
        return None

    @RZMinimum.setter
    def RZMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RZMinimum.
        """
        pass

    @property
    def XMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the XMaximum.
        """
        return None

    @XMaximum.setter
    def XMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the XMaximum.
        """
        pass

    @property
    def XMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the XMinimum.
        """
        return None

    @XMinimum.setter
    def XMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the XMinimum.
        """
        pass

    @property
    def YMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the YMaximum.
        """
        return None

    @YMaximum.setter
    def YMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the YMaximum.
        """
        pass

    @property
    def YMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the YMinimum.
        """
        return None

    @YMinimum.setter
    def YMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the YMinimum.
        """
        pass

    @property
    def ZMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ZMaximum.
        """
        return None

    @ZMaximum.setter
    def ZMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ZMaximum.
        """
        pass

    @property
    def ZMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ZMinimum.
        """
        return None

    @ZMinimum.setter
    def ZMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ZMinimum.
        """
        pass

    @property
    def TorsionalDamping(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TorsionalDamping.
        """
        return None

    @TorsionalDamping.setter
    def TorsionalDamping(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TorsionalDamping.
        """
        pass

    @property
    def TorsionalStiffness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TorsionalStiffness.
        """
        return None

    @TorsionalStiffness.setter
    def TorsionalStiffness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TorsionalStiffness.
        """
        pass

    @property
    def MobileBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MobileBeamRadius.
        """
        return None

    @MobileBeamRadius.setter
    def MobileBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MobileBeamRadius.
        """
        pass

    @property
    def ReferenceBeamRadius(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        return None

    @ReferenceBeamRadius.setter
    def ReferenceBeamRadius(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ReferenceBeamRadius.
        """
        pass

    @property
    def GeneralPrimitiveType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointGeneralPrimitiveType]:
        """
        Gets or sets the GeneralPrimitiveType.
        """
        return None

    @GeneralPrimitiveType.setter
    def GeneralPrimitiveType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointGeneralPrimitiveType]) -> None:
        """
        Gets or sets the GeneralPrimitiveType.
        """
        pass

    @property
    def InitialPosition(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointInitialPosition]:
        """
        Gets or sets the InitialPosition.
        """
        return None

    @InitialPosition.setter
    def InitialPosition(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointInitialPosition]) -> None:
        """
        Gets or sets the InitialPosition.
        """
        pass

    @property
    def MobileBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the MobileBehavior.
        """
        return None

    @MobileBehavior.setter
    def MobileBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the MobileBehavior.
        """
        pass

    @property
    def ReferenceBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]:
        """
        Gets or sets the ReferenceBehavior.
        """
        return None

    @ReferenceBehavior.setter
    def ReferenceBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadBehavior]) -> None:
        """
        Gets or sets the ReferenceBehavior.
        """
        pass

    @property
    def Formulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointFormulation]:
        """
        Gets or sets the Formulation.
        """
        return None

    @Formulation.setter
    def Formulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointFormulation]) -> None:
        """
        Gets or sets the Formulation.
        """
        pass

    @property
    def JointFrictionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointFrictionType]:
        """
        Gets or sets the JointFrictionType.
        """
        return None

    @JointFrictionType.setter
    def JointFrictionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointFrictionType]) -> None:
        """
        Gets or sets the JointFrictionType.
        """
        pass

    @property
    def MobileFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemotePointFormulation]:
        """
        Gets or sets the MobileFormulation.
        """
        return None

    @MobileFormulation.setter
    def MobileFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemotePointFormulation]) -> None:
        """
        Gets or sets the MobileFormulation.
        """
        pass

    @property
    def RadialGapType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RadialGapType.
        """
        return None

    @RadialGapType.setter
    def RadialGapType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RadialGapType.
        """
        pass

    @property
    def ReferenceFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemotePointFormulation]:
        """
        Gets or sets the ReferenceFormulation.
        """
        return None

    @ReferenceFormulation.setter
    def ReferenceFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemotePointFormulation]) -> None:
        """
        Gets or sets the ReferenceFormulation.
        """
        pass

    @property
    def ConnectionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointScopingType]:
        """
        Gets or sets the ConnectionType.
        """
        return None

    @ConnectionType.setter
    def ConnectionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointScopingType]) -> None:
        """
        Gets or sets the ConnectionType.
        """
        pass

    @property
    def RXMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RXMaximumType.
        """
        return None

    @RXMaximumType.setter
    def RXMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RXMaximumType.
        """
        pass

    @property
    def RXMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RXMinimumType.
        """
        return None

    @RXMinimumType.setter
    def RXMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RXMinimumType.
        """
        pass

    @property
    def RYMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RYMaximumType.
        """
        return None

    @RYMaximumType.setter
    def RYMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RYMaximumType.
        """
        pass

    @property
    def RYMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RYMinimumType.
        """
        return None

    @RYMinimumType.setter
    def RYMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RYMinimumType.
        """
        pass

    @property
    def RZMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RZMaximumType.
        """
        return None

    @RZMaximumType.setter
    def RZMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RZMaximumType.
        """
        pass

    @property
    def RZMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the RZMinimumType.
        """
        return None

    @RZMinimumType.setter
    def RZMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the RZMinimumType.
        """
        pass

    @property
    def XMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the XMaximumType.
        """
        return None

    @XMaximumType.setter
    def XMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the XMaximumType.
        """
        pass

    @property
    def XMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the XMinimumType.
        """
        return None

    @XMinimumType.setter
    def XMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the XMinimumType.
        """
        pass

    @property
    def YMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the YMaximumType.
        """
        return None

    @YMaximumType.setter
    def YMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the YMaximumType.
        """
        pass

    @property
    def YMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the YMinimumType.
        """
        return None

    @YMinimumType.setter
    def YMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the YMinimumType.
        """
        pass

    @property
    def ZMaximumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the ZMaximumType.
        """
        return None

    @ZMaximumType.setter
    def ZMaximumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the ZMaximumType.
        """
        pass

    @property
    def ZMinimumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]:
        """
        Gets or sets the ZMinimumType.
        """
        return None

    @ZMinimumType.setter
    def ZMinimumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointStopType]) -> None:
        """
        Gets or sets the ZMinimumType.
        """
        pass

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointType]:
        """
        Gets or sets the Type.
        """
        return None

    @Type.setter
    def Type(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointType]) -> None:
        """
        Gets or sets the Type.
        """
        pass

    @property
    def MobileAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the MobileAppliedBy.
        """
        return None

    @MobileAppliedBy.setter
    def MobileAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the MobileAppliedBy.
        """
        pass

    @property
    def ReferenceAppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        return None

    @ReferenceAppliedBy.setter
    def ReferenceAppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RemoteApplicationType]) -> None:
        """
        Gets or sets the ReferenceAppliedBy.
        """
        pass

    @property
    def Rotations(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointRotationDOFType]:
        """
        Gets or sets the Rotations.
        """
        return None

    @Rotations.setter
    def Rotations(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointRotationDOFType]) -> None:
        """
        Gets or sets the Rotations.
        """
        pass

    @property
    def SolverElementType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.JointSolverElementType]:
        """
        Gets or sets the SolverElementType.
        """
        return None

    @SolverElementType.setter
    def SolverElementType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.JointSolverElementType]) -> None:
        """
        Gets or sets the SolverElementType.
        """
        pass

    @property
    def TranslationX(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]:
        """
        Gets or sets the TranslationX.
        """
        return None

    @TranslationX.setter
    def TranslationX(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]) -> None:
        """
        Gets or sets the TranslationX.
        """
        pass

    @property
    def TranslationY(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]:
        """
        Gets or sets the TranslationY.
        """
        return None

    @TranslationY.setter
    def TranslationY(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]) -> None:
        """
        Gets or sets the TranslationY.
        """
        pass

    @property
    def TranslationZ(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]:
        """
        Gets or sets the TranslationZ.
        """
        return None

    @TranslationZ.setter
    def TranslationZ(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FixedOrFree]) -> None:
        """
        Gets or sets the TranslationZ.
        """
        pass

    @property
    def MobileRelaxationMethod(self) -> typing.Optional[bool]:
        """
        Gets or sets the MobileRelaxationMethod.
        """
        return None

    @MobileRelaxationMethod.setter
    def MobileRelaxationMethod(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MobileRelaxationMethod.
        """
        pass

    @property
    def ReferenceRelaxationMethod(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReferenceRelaxationMethod.
        """
        return None

    @ReferenceRelaxationMethod.setter
    def ReferenceRelaxationMethod(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReferenceRelaxationMethod.
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
    def SuppressedForSolve(self) -> typing.Optional[bool]:
        """
        Gets the SuppressedForSolve.
        """
        return None

    @property
    def ElementCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ElementCoordinateSystem.
        """
        return None

    @ElementCoordinateSystem.setter
    def ElementCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ElementCoordinateSystem.
        """
        pass

    @property
    def MobileCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        return None

    @MobileCoordinateSystem.setter
    def MobileCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the MobileCoordinateSystem.
        """
        pass

    @property
    def ReferenceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        return None

    @ReferenceCoordinateSystem.setter
    def ReferenceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the ReferenceCoordinateSystem.
        """
        pass

    @property
    def MobileLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the MobileLocation.
        """
        return None

    @MobileLocation.setter
    def MobileLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the MobileLocation.
        """
        pass

    @property
    def CurveOrientationSurface(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the CurveOrientationSurface.
        """
        return None

    @CurveOrientationSurface.setter
    def CurveOrientationSurface(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the CurveOrientationSurface.
        """
        pass

    @property
    def ReferenceLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the ReferenceLocation.
        """
        return None

    @ReferenceLocation.setter
    def ReferenceLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the ReferenceLocation.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def PromoteToRemotePoint(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Run the PromoteToRemotePoint action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
        """
        pass

    def FlipReferenceMobile(self) -> None:
        """
        Run the FlipReferenceMobile action.
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


class Connections(object):
    """
    Defines a Connections.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSContactGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets or sets the SolverFilesDirectory.
        """
        return None

    @SolverFilesDirectory.setter
    def SolverFilesDirectory(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the SolverFilesDirectory.
        """
        pass

    @property
    def GenerateAutomaticConnectionOnRefresh(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]:
        """
        Gets or sets the GenerateAutomaticConnectionOnRefresh.
        """
        return None

    @GenerateAutomaticConnectionOnRefresh.setter
    def GenerateAutomaticConnectionOnRefresh(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]) -> None:
        """
        Gets or sets the GenerateAutomaticConnectionOnRefresh.
        """
        pass

    @property
    def FixedJoints(self) -> typing.Optional[bool]:
        """
        Gets or sets the FixedJoints.
        """
        return None

    @FixedJoints.setter
    def FixedJoints(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FixedJoints.
        """
        pass

    @property
    def TransparencyEnabled(self) -> typing.Optional[bool]:
        """
        Gets or sets the TransparencyEnabled.
        """
        return None

    @TransparencyEnabled.setter
    def TransparencyEnabled(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the TransparencyEnabled.
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

    def AddContactRegion(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child ContactRegion.
        """
        pass

    def AddContactTool(self) -> Ansys.ACT.Automation.Mechanical.PreContactTool:
        """
        Creates a new ContactTool
        """
        pass

    def AddSpotWeldGroup(self) -> Ansys.ACT.Automation.Mechanical.Connections.SpotWeldGroup:
        """
        Creates a new child SpotWeldGroup.
        """
        pass

    def AddSpotWeld(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child SpotWeld.
        """
        pass

    def AddInterStage(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child InterStage.
        """
        pass

    def AddJoint(self) -> Ansys.ACT.Automation.Mechanical.Connections.Joint:
        """
        Creates a new child Joint.
        """
        pass

    def AddBodyInteraction(self) -> Ansys.ACT.Automation.Mechanical.Connections.BodyInteraction:
        """
        Creates a new child BodyInteraction.
        """
        pass

    def SearchConnectionsForDuplicatePairs(self) -> None:
        """
        Run the SearchConnectionsForDuplicatePairs action.
        """
        pass

    def CreateAutomaticConnections(self) -> None:
        """
        Run the CreateAutomaticConnections action.
        """
        pass

    def ExportModelTopology(self, filename: str) -> None:
        """
        ExportModelTopology method.
        """
        pass

    def GetJSON(self) -> str:
        """
        GetJSON method.
        """
        pass

    def AddBeamInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.Beam:
        """
        AddBeamInternal method.
        """
        pass

    def AddJointInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.Joint:
        """
        AddJointInternal method.
        """
        pass

    def AddSpringInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.Spring:
        """
        AddSpringInternal method.
        """
        pass

    def AddContactRegionInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        AddContactRegionInternal method.
        """
        pass

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def AddAMBondConnection(self) -> Ansys.ACT.Automation.Mechanical.Connections.AMBondConnection:
        """
        Creates a new AMBondConnection
        """
        pass

    def AddBeam(self) -> Ansys.ACT.Automation.Mechanical.Connections.Beam:
        """
        Creates a new Beam
        """
        pass

    def AddBearing(self) -> Ansys.ACT.Automation.Mechanical.Connections.Bearing:
        """
        Creates a new Bearing
        """
        pass

    def AddConnectionGroup(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionGroup:
        """
        Creates a new ConnectionGroup
        """
        pass

    def AddContactSolutionInformation(self) -> Ansys.ACT.Automation.Mechanical.ContactSolutionInformation:
        """
        Creates a new ContactSolutionInformation
        """
        pass

    def AddEndRelease(self) -> Ansys.ACT.Automation.Mechanical.EndRelease:
        """
        Creates a new EndRelease
        """
        pass

    def AddSpring(self) -> Ansys.ACT.Automation.Mechanical.Connections.Spring:
        """
        Creates a new Spring
        """
        pass

    def GenerateInitialContactResults(self) -> None:
        """
        Generate Initial Contact Results and Mesh Parts
        """
        pass

    def RepairOverlappingContactRegions(self) -> None:
        """
        Check for Overlapping Contact Regions. However, please note that this action does not result in any actual repair being performed.
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


class ConnectionGroup(object):
    """
    Defines a ConnectionGroup.
    """

    @property
    def ConnectionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutoDetectionType]:
        """
        Gets or sets the ConnectionType.
        """
        return None

    @ConnectionType.setter
    def ConnectionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutoDetectionType]) -> None:
        """
        Gets or sets the ConnectionType.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSConnectionGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ActiveConnections(self) -> typing.Optional[int]:
        """
        Gets the ActiveConnections.
        """
        return None

    @property
    def Connections(self) -> typing.Optional[int]:
        """
        Gets the Connections.
        """
        return None

    @property
    def EdgeOverlapTolerance(self) -> typing.Optional[int]:
        """
        Gets or sets the EdgeOverlapTolerance.
        """
        return None

    @EdgeOverlapTolerance.setter
    def EdgeOverlapTolerance(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the EdgeOverlapTolerance.
        """
        pass

    @property
    def FaceOverlapTolerance(self) -> typing.Optional[int]:
        """
        Gets or sets the FaceOverlapTolerance.
        """
        return None

    @FaceOverlapTolerance.setter
    def FaceOverlapTolerance(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the FaceOverlapTolerance.
        """
        pass

    @property
    def MinimumDistancePercentage(self) -> typing.Optional[int]:
        """
        Gets or sets the MinimumDistancePercentage.
        """
        return None

    @MinimumDistancePercentage.setter
    def MinimumDistancePercentage(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MinimumDistancePercentage.
        """
        pass

    @property
    def ThicknessScaleFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ThicknessScaleFactor.
        """
        return None

    @ThicknessScaleFactor.setter
    def ThicknessScaleFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThicknessScaleFactor.
        """
        pass

    @property
    def ToleranceSlider(self) -> typing.Optional[int]:
        """
        Gets or sets the ToleranceSlider.
        """
        return None

    @ToleranceSlider.setter
    def ToleranceSlider(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ToleranceSlider.
        """
        pass

    @property
    def FaceFaceDetectionAngleTolerence(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FaceFaceDetectionAngleTolerence.
        """
        return None

    @FaceFaceDetectionAngleTolerence.setter
    def FaceFaceDetectionAngleTolerence(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FaceFaceDetectionAngleTolerence.
        """
        pass

    @property
    def FaceAngleTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the FaceAngleTolerance.
        """
        return None

    @FaceAngleTolerance.setter
    def FaceAngleTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the FaceAngleTolerance.
        """
        pass

    @property
    def MinimumDistanceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MinimumDistanceValue.
        """
        return None

    @property
    def ToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ToleranceValue.
        """
        return None

    @ToleranceValue.setter
    def ToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ToleranceValue.
        """
        pass

    @property
    def CylindricalFaces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CylindricalFacesOption]:
        """
        Gets or sets the CylindricalFaces.
        """
        return None

    @CylindricalFaces.setter
    def CylindricalFaces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CylindricalFacesOption]) -> None:
        """
        Gets or sets the CylindricalFaces.
        """
        pass

    @property
    def Priority(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFaceEdgePriority]:
        """
        Gets or sets the Priority.
        """
        return None

    @Priority.setter
    def Priority(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFaceEdgePriority]) -> None:
        """
        Gets or sets the Priority.
        """
        pass

    @property
    def GroupBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactGroupingType]:
        """
        Gets or sets the GroupBy.
        """
        return None

    @GroupBy.setter
    def GroupBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactGroupingType]) -> None:
        """
        Gets or sets the GroupBy.
        """
        pass

    @property
    def SearchAcross(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSearchingType]:
        """
        Gets or sets the SearchAcross.
        """
        return None

    @SearchAcross.setter
    def SearchAcross(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSearchingType]) -> None:
        """
        Gets or sets the SearchAcross.
        """
        pass

    @property
    def ToleranceType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactToleranceType]:
        """
        Gets or sets the ToleranceType.
        """
        return None

    @ToleranceType.setter
    def ToleranceType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactToleranceType]) -> None:
        """
        Gets or sets the ToleranceType.
        """
        pass

    @property
    def EdgeEdge(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactEdgeEdgeOption]:
        """
        Gets or sets the EdgeEdge.
        """
        return None

    @EdgeEdge.setter
    def EdgeEdge(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactEdgeEdgeOption]) -> None:
        """
        Gets or sets the EdgeEdge.
        """
        pass

    @property
    def FaceEdge(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFaceEdgeOption]:
        """
        Gets or sets the FaceEdge.
        """
        return None

    @FaceEdge.setter
    def FaceEdge(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactFaceEdgeOption]) -> None:
        """
        Gets or sets the FaceEdge.
        """
        pass

    @property
    def AutomaticFixedJoints(self) -> typing.Optional[bool]:
        """
        Gets or sets the AutomaticFixedJoints.
        """
        return None

    @AutomaticFixedJoints.setter
    def AutomaticFixedJoints(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AutomaticFixedJoints.
        """
        pass

    @property
    def RevoluteJoints(self) -> typing.Optional[bool]:
        """
        Gets or sets the RevoluteJoints.
        """
        return None

    @RevoluteJoints.setter
    def RevoluteJoints(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the RevoluteJoints.
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
    def FaceFace(self) -> typing.Optional[bool]:
        """
        Gets or sets the FaceFace.
        """
        return None

    @FaceFace.setter
    def FaceFace(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FaceFace.
        """
        pass

    @property
    def UseRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseRange.
        """
        return None

    @UseRange.setter
    def UseRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseRange.
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
    def ReadOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ReadOnly.
        """
        return None

    @ReadOnly.setter
    def ReadOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ReadOnly.
        """
        pass

    @property
    def TransferableObjectId(self) -> typing.Optional[str]:
        """
        TransferableObjectId property.
        """
        return None

    @TransferableObjectId.setter
    def TransferableObjectId(self, value: typing.Optional[str]) -> None:
        """
        TransferableObjectId property.
        """
        pass

    @property
    def ImportableObjectSourceId(self) -> typing.Optional[str]:
        """
        ImportableObjectSourceId property.
        """
        return None

    @ImportableObjectSourceId.setter
    def ImportableObjectSourceId(self, value: typing.Optional[str]) -> None:
        """
        ImportableObjectSourceId property.
        """
        pass

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

    def AddContactRegion(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child ContactRegion.
        """
        pass

    def AddContactRegionInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child ContactRegion that is not visible.
        """
        pass

    def AddJoint(self) -> Ansys.ACT.Automation.Mechanical.Connections.Joint:
        """
        Creates a new child Joint.
        """
        pass

    def AddJointInternal(self) -> Ansys.ACT.Automation.Mechanical.Connections.Joint:
        pass

    def SearchConnectionsForDuplicatePairs(self) -> None:
        """
        Run the SearchConnectionsForDuplicatePairs action.
        """
        pass

    def AddSpotWeld(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child SpotWeld.
        """
        pass

    def AddInterStage(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Creates a new child InterStage.
        """
        pass

    def CreateAutomaticConnections(self) -> None:
        """
        Run the CreateAutomaticConnections action.
        """
        pass

    def DeleteChildren(self, verificationDialog: bool) -> None:
        """
        Run the DeleteChildren action with optional verification dialog.
        """
        pass

    def RenameBasedOnChildren(self) -> bool:
        """
        Rename the Connection group based on the children.
        """
        pass

    def SetDefaultAPDLNames(self) -> None:
        """
        Loop over all the valid contact regions and set the default APDL names.
        """
        pass

    def GetTableGenerator(self) -> Ansys.ACT.Automation.Mechanical.Connections.ConnectionsTableGenerator:
        """
        GetTableGenerator method.
        """
        pass

    def RepairOverlappingContactRegions(self) -> None:
        """
        Check for Overlapping Contact Regions. However, please note that this action does not result in any actual repair being performed.
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


class BodyInteractions(object):
    """
    Defines a BodyInteractions.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSBodyInteractionGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def PinballFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PinballFactor.
        """
        return None

    @PinballFactor.setter
    def PinballFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PinballFactor.
        """
        pass

    @property
    def Tolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the Tolerance.
        """
        return None

    @Tolerance.setter
    def Tolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Tolerance.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ShellThicknessFactor.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShellThicknessFactor.
        """
        pass

    @property
    def TimestepSafetyFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the TimestepSafetyFactor.
        """
        return None

    @TimestepSafetyFactor.setter
    def TimestepSafetyFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TimestepSafetyFactor.
        """
        pass

    @property
    def LimitingTimestepVelocity(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the LimitingTimestepVelocity.
        """
        return None

    @LimitingTimestepVelocity.setter
    def LimitingTimestepVelocity(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the LimitingTimestepVelocity.
        """
        pass

    @property
    def ContactDetection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactDetection]:
        """
        Gets or sets the ContactDetection.
        """
        return None

    @ContactDetection.setter
    def ContactDetection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactDetection]) -> None:
        """
        Gets or sets the ContactDetection.
        """
        pass

    @property
    def Formulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.BodyInteractionFormulation]:
        """
        Gets or sets the Formulation.
        """
        return None

    @Formulation.setter
    def Formulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.BodyInteractionFormulation]) -> None:
        """
        Gets or sets the Formulation.
        """
        pass

    @property
    def ManualContactTreatment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ManualContactTreatmentType]:
        """
        Gets or sets the ManualContactTreatment.
        """
        return None

    @ManualContactTreatment.setter
    def ManualContactTreatment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ManualContactTreatmentType]) -> None:
        """
        Gets or sets the ManualContactTreatment.
        """
        pass

    @property
    def NodalShellThickness(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]:
        """
        Gets or sets the NodalShellThickness.
        """
        return None

    @NodalShellThickness.setter
    def NodalShellThickness(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]) -> None:
        """
        Gets or sets the NodalShellThickness.
        """
        pass

    @property
    def SlidingContact(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SlidingContactType]:
        """
        Gets or sets the SlidingContact.
        """
        return None

    @SlidingContact.setter
    def SlidingContact(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SlidingContactType]) -> None:
        """
        Gets or sets the SlidingContact.
        """
        pass

    @property
    def BodySelfContact(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]:
        """
        Gets or sets the BodySelfContact.
        """
        return None

    @BodySelfContact.setter
    def BodySelfContact(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]) -> None:
        """
        Gets or sets the BodySelfContact.
        """
        pass

    @property
    def ElementSelfContact(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]:
        """
        Gets or sets the ElementSelfContact.
        """
        return None

    @ElementSelfContact.setter
    def ElementSelfContact(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.YesNoProgrammedControlled]) -> None:
        """
        Gets or sets the ElementSelfContact.
        """
        pass

    @property
    def EdgeOnEdgeContact(self) -> typing.Optional[bool]:
        """
        Gets or sets the EdgeOnEdgeContact.
        """
        return None

    @EdgeOnEdgeContact.setter
    def EdgeOnEdgeContact(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the EdgeOnEdgeContact.
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

    def AddBodyInteraction(self) -> Ansys.ACT.Automation.Mechanical.Connections.BodyInteraction:
        """
        Creates a new child BodyInteraction.
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


