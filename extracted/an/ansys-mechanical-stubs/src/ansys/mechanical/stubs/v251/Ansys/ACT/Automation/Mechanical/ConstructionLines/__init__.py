"""ConstructionLines module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ConstructionLine(object):
    """
    
                
                    Enables the construction and generation of straight line edges directly within
                    Mechanical.
                
            
    """

    @property
    def Edges(self) -> typing.Optional[typing.List[typing.Any]]:
        """
        
                Creates for the user an IEdge representation of each edge in this Construction Line.
            
        """
        return None

    @property
    def Points(self) -> typing.Optional[typing.List[typing.Any]]:
        """
        
                Returns all points in this Construction Line, both those that have been created
                as well as virtual representations.
            
        """
        return None

    @property
    def Planes(self) -> typing.Optional[typing.List[typing.Any]]:
        """
        
                Creates for the user an Plane representation of each plane in this Construction Line.
            
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSLines.IDSLinesPythonInteraction]:
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

    def CreatePoints(self, pointDefinitionCollection: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
        """
        CreatePoints method.
        """
        pass

    def CreatePlanarPoints(self, plane: Ansys.Mechanical.DataModel.ConstructionLines.Plane, pointDefinitionCollection: typing.Iterable[typing.Any]) -> typing.List[typing.Any]:
        """
        CreatePlanarPoints method.
        """
        pass

    def CreatePlane(self, sketchPlaneDefinition: typing.Any) -> Ansys.Mechanical.DataModel.ConstructionLines.Plane:
        """
        
                Create a plane.
            
        """
        pass

    @typing.overload
    def CreateStraightLines(self, pointCollection: typing.Iterable[Ansys.Mechanical.DataModel.ConstructionLines.Point]) -> typing.List[typing.Any]:
        ...

    @typing.overload
    def CreateStraightLines(self, pointCollection: typing.Iterable[Ansys.Mechanical.DataModel.ConstructionLines.Point], connectionCollection: typing.Iterable[typing.Iterable[typing.Any]]) -> typing.List[typing.Any]:
        ...

    def CreateStraightLines(self, *args: typing.Any) -> typing.List[typing.Any]:
        """
        CreateStraightLines method.
        """
        pass

    def FlipEdges(self, edgesToFlip: typing.Iterable[Ansys.Mechanical.DataModel.ConstructionLines.Edges.IEdge]) -> None:
        """
        FlipEdges method.
        """
        pass

    def DeleteEdges(self, edgeCollection: typing.Iterable[Ansys.Mechanical.DataModel.ConstructionLines.Edges.IEdge]) -> None:
        """
        DeleteEdges method.
        """
        pass

    def DeletePlane(self, plane: Ansys.Mechanical.DataModel.ConstructionLines.Plane, forceDelete: bool) -> None:
        """
        
                Delete a plane associated with this construction line.
            
        """
        pass

    def AddToGeometry(self) -> Ansys.ACT.Interfaces.Geometry.IGeoPart:
        """
        
                Add a part to Geometry with line bodies as contained in this ConstructionLine instance.
            
        """
        pass

    def UpdateGeometry(self) -> None:
        """
        
                Update the corresponding part with any changes made in this ConstructionLine instance.
            
        """
        pass

    def RemoveFromGeometry(self) -> None:
        """
        
                Remove the corresponding part from the geometry.
            
        """
        pass

    def GetPartFromGeometry(self) -> Ansys.ACT.Interfaces.Geometry.IGeoPart:
        """
        
                Get the corresponding part for a ConstructionLine instance.
            
        """
        pass

    def Undo(self) -> None:
        """
        
                Undo the last operation in this Construction Line instance.
            
        """
        pass

    def Redo(self) -> None:
        """
        
                Redo and undone operation in this Construction Line instance.
            
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


