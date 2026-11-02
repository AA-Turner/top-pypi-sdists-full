"""ImportedLoads module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ImportedBodyForceDensity(object):
    """
    Defines a ImportedBodyForceDensity.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedBodyTemperature(object):
    """
    Defines a ImportedBodyTemperature.
    """

    @property
    def ApplyToInitialMesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the ApplyToInitialMesh.
        """
        return None

    @ApplyToInitialMesh.setter
    def ApplyToInitialMesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ApplyToInitialMesh.
        """
        pass

    @property
    def MappedData(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappedData]:
        """
        Gets or sets the MappedData.
        """
        return None

    @MappedData.setter
    def MappedData(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappedData]) -> None:
        """
        Gets or sets the MappedData.
        """
        pass

    @property
    def DisplayMappedData(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMappedData.
        """
        return None

    @DisplayMappedData.setter
    def DisplayMappedData(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMappedData.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LoadVectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the LoadVectorNumber.
        """
        return None

    @LoadVectorNumber.setter
    def LoadVectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LoadVectorNumber.
        """
        pass

    @property
    def LoadVectorAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadVectorAssignment]:
        """
        Gets or sets the LoadVectorAssignment.
        """
        return None

    @LoadVectorAssignment.setter
    def LoadVectorAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadVectorAssignment]) -> None:
        """
        Gets or sets the LoadVectorAssignment.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedConvection(object):
    """
    Defines a ImportedConvection.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DisplayConnectionLines(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayConnectionLines.
        """
        return None

    @DisplayConnectionLines.setter
    def DisplayConnectionLines(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayConnectionLines.
        """
        pass

    @property
    def FluidFlow(self) -> typing.Optional[bool]:
        """
        Gets or sets the FluidFlow.
        """
        return None

    @FluidFlow.setter
    def FluidFlow(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FluidFlow.
        """
        pass

    @property
    def FluidFlowLocation(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the FluidFlowLocation.
        """
        return None

    @FluidFlowLocation.setter
    def FluidFlowLocation(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the FluidFlowLocation.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedCutBoundaryRemoteConstraint(object):
    """
    Defines a ImportedCutBoundaryRemoteConstraint.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedCutBoundaryRemoteForce(object):
    """
    Defines a ImportedCutBoundaryRemoteForce.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedDisplacement(object):
    """
    Defines a ImportedDisplacement.
    """

    @property
    def ApplyToInitialMesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the ApplyToInitialMesh.
        """
        return None

    @ApplyToInitialMesh.setter
    def ApplyToInitialMesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ApplyToInitialMesh.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def DisplacementType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadDisplacementType]:
        """
        Gets or sets the DisplacementType.
        """
        return None

    @DisplacementType.setter
    def DisplacementType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadDisplacementType]) -> None:
        """
        Gets or sets the DisplacementType.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedSurfaceForceDensity(object):
    """
    Defines a ImportedSurfaceForceDensity.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedTemperature(object):
    """
    Defines a ImportedTemperature.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedVelocity(object):
    """
    Defines a ImportedVelocity.
    """

    @property
    def MappedData(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappedData]:
        """
        Gets or sets the MappedData.
        """
        return None

    @MappedData.setter
    def MappedData(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappedData]) -> None:
        """
        Gets or sets the MappedData.
        """
        pass

    @property
    def DisplayMappedData(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMappedData.
        """
        return None

    @DisplayMappedData.setter
    def DisplayMappedData(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMappedData.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def CutoffFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutoffFrequency.
        """
        return None

    @CutoffFrequency.setter
    def CutoffFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutoffFrequency.
        """
        pass

    @property
    def MaximumTimeRange(self) -> typing.Optional[float]:
        """
        Gets or sets the MaximumTimeRange.
        """
        return None

    @MaximumTimeRange.setter
    def MaximumTimeRange(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaximumTimeRange.
        """
        pass

    @property
    def MinimumTimeRange(self) -> typing.Optional[float]:
        """
        Gets or sets the MinimumTimeRange.
        """
        return None

    @MinimumTimeRange.setter
    def MinimumTimeRange(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MinimumTimeRange.
        """
        pass

    @property
    def SourceTimeDefinitionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceTimeDefinitionType]:
        """
        Gets or sets the SourceTimeDefinitionType.
        """
        return None

    @SourceTimeDefinitionType.setter
    def SourceTimeDefinitionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceTimeDefinitionType]) -> None:
        """
        Gets or sets the SourceTimeDefinitionType.
        """
        pass

    @property
    def WindowType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]:
        """
        Gets or sets the WindowType.
        """
        return None

    @WindowType.setter
    def WindowType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]) -> None:
        """
        Gets or sets the WindowType.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedLoadGroup(object):
    """
    Defines a ImportedLoadGroup.
    """

    @property
    def ResultFile(self) -> typing.Optional[str]:
        """
        Gets or sets the ResultFile.
        """
        return None

    @ResultFile.setter
    def ResultFile(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ResultFile.
        """
        pass

    @property
    def ResultFileUnitSystem(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the ResultFileUnitSystem.
        """
        return None

    @ResultFileUnitSystem.setter
    def ResultFileUnitSystem(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the ResultFileUnitSystem.
        """
        pass

    @property
    def FilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the FilesDirectory.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def TransferStep(self) -> typing.Optional[int]:
        """
        Controls which additive simulation step is used for the data transfer.
        """
        return None

    @TransferStep.setter
    def TransferStep(self, value: typing.Optional[int]) -> None:
        """
        Controls which additive simulation step is used for the data transfer.
        """
        pass

    @property
    def Source(self) -> typing.Optional[str]:
        """
        Gets the Source.
        """
        return None

    @property
    def ResultFileTimestamp(self) -> typing.Optional[str]:
        """
        Gets the ResultFileTimestamp.
        """
        return None

    @property
    def SourceDimension(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]:
        """
        Gets or sets the SourceDimension.
        """
        return None

    @SourceDimension.setter
    def SourceDimension(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SourceDimension]) -> None:
        """
        Gets or sets the SourceDimension.
        """
        pass

    @property
    def DeleteMappedDataFilesAfterImport(self) -> typing.Optional[bool]:
        """
        Gets or sets the DeleteMappedDataFilesAfterImport.
        """
        return None

    @DeleteMappedDataFilesAfterImport.setter
    def DeleteMappedDataFilesAfterImport(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DeleteMappedDataFilesAfterImport.
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
    def TransferTemperaturesDuringSolve(self) -> typing.Optional[bool]:
        """
        Gets or sets the TransferTemperaturesDuringSolve.
        """
        return None

    @TransferTemperaturesDuringSolve.setter
    def TransferTemperaturesDuringSolve(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the TransferTemperaturesDuringSolve.
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

    def CreateExternalLoadVelocitiesAndSyncAnalysisSettings(self) -> None:
        """
        Run the CreateExternalLoadVelocitiesAndSyncAnalysisSettings action.
        """
        pass

    def SetResultFile(self, resultFile: str, unitSystem: Ansys.Mechanical.DataModel.Enums.WBUnitSystemType) -> None:
        """
        Sets the ResultFile with unitSystem supplied. For MAPDL Results File without a unit system.
        """
        pass

    def ImportExternalDataFiles(self, externalDataFiles: Ansys.Mechanical.ExternalData.ExternalDataFileCollection) -> None:
        """
        
            
            Imports external data files for current Imported Load Group.
            
            
            This includes saving the external data files to project if specified, generating the XML representation 
            of the external data settings, and updating the file association for mapping.
            
            
            An ExternalDataFileCollection object can be created by calling the GetSettingsForFormat 
            method from the factory class . 
            
            
        """
        pass

    def GetExternalDataFiles(self) -> Ansys.Mechanical.ExternalData.ExternalDataFileCollection:
        """
        
            
            Gets a copy of the most recently imported ExternalDataFileCollection. 
            >
            
            Returns an empty Collection if an ImportExternalData operation has never been done.
            >
            
        """
        pass

    def ReloadExternalDataFiles(self) -> None:
        """
        Reloads the external data files for current Imported Load Group.
        """
        pass

    def Delete(self) -> None:
        """
        Run the Delete action.
        """
        pass

    def AddImportedBodyTemperature(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedBodyTemperature:
        """
        Creates a new ImportedBodyTemperature
        """
        pass

    def AddImportedTemperature(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedTemperature:
        """
        Creates a new ImportedTemperature
        """
        pass

    def CreateBodyForceDensitiesAndSyncAnalysisSettings(self) -> None:
        """
        Create body force densities for all RPMs.
        """
        pass

    def CreateSurfaceForceDensitiesAndSyncAnalysisSettings(self) -> None:
        """
        Create surface force densities for all RPMs.
        """
        pass

    def CreateVelocitiesAndSyncAnalysisSettings(self) -> None:
        """
        Create velocities for all RPMs.
        """
        pass

    def AddImportedBodyForceDensity(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedBodyForceDensity:
        """
        Creates a new ImportedBodyForceDensity
        """
        pass

    def AddImportedConvection(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedConvection:
        """
        Creates a new ImportedConvection
        """
        pass

    def AddImportedCutBoundaryRemoteConstraint(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedCutBoundaryRemoteConstraint:
        """
        Creates a new ImportedCutBoundaryRemoteConstraint
        """
        pass

    def AddImportedCutBoundaryRemoteForce(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedCutBoundaryRemoteForce:
        """
        Creates a new ImportedCutBoundaryRemoteForce
        """
        pass

    def AddImportedDisplacement(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedDisplacement:
        """
        Creates a new ImportedDisplacement
        """
        pass

    def AddImportedCutBoundaryConstraint(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedDisplacement:
        """
        Creates a new ImportedDisplacement
        """
        pass

    def AddImportedElementOrientation(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedElementOrientation:
        """
        Creates a new ImportedElementOrientation
        """
        pass

    def AddImportedFiberRatio(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedFiberRatio:
        """
        Creates a new ImportedFiberRatio
        """
        pass

    def AddImportedForce(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedForce:
        """
        Creates a new ImportedForce
        """
        pass

    def AddImportedHeatFlux(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedHeatFlux:
        """
        Creates a new ImportedHeatFlux
        """
        pass

    def AddImportedHeatGeneration(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedHeatGeneration:
        """
        Creates a new ImportedHeatGeneration
        """
        pass

    def AddImportedInitialStrain(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedInitialStrain:
        """
        Creates a new ImportedInitialStrain
        """
        pass

    def AddImportedInitialStress(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedInitialStress:
        """
        Creates a new ImportedInitialStress
        """
        pass

    def AddImportedMaterialField(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedMaterialField:
        """
        Creates a new ImportedMaterialField
        """
        pass

    def AddImportedPressure(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedPressure:
        """
        Creates a new ImportedPressure
        """
        pass

    def AddImportedSurfaceForceDensity(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedSurfaceForceDensity:
        """
        Creates a new ImportedSurfaceForceDensity
        """
        pass

    def AddImportedThickness(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedThickness:
        """
        Creates a new ImportedThickness
        """
        pass

    def AddImportedTrace(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedTrace:
        """
        Creates a new ImportedTrace
        """
        pass

    def AddImportedVelocity(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedVelocity:
        """
        Creates a new ImportedVelocity
        """
        pass

    def AddImportedWarpWeftRatio(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedWarpWeftRatio:
        """
        Creates a new ImportedWarpWeftRatio
        """
        pass

    def AddImportedYarnAngle(self) -> Ansys.ACT.Automation.Mechanical.ImportedLoads.ImportedYarnAngle:
        """
        Creates a new ImportedYarnAngle
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
        """
        pass

    def ImportLoad(self) -> None:
        """
        Run the ImportLoad action.
        """
        pass

    def RefreshImportedLoad(self) -> None:
        """
        Run the RefreshImportedLoad action.
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


class ImportedLoad(object):
    """
    Defines a ImportedLoad.
    """

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedTrace(object):
    """
    Defines a ImportedTrace.
    """

    @property
    def Vias(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]]:
        """
        Vias property.
        """
        return None

    @property
    def Layers(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]]:
        """
        Layers property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedElementOrientation(object):
    """
    Defines a ImportedElementOrientation.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedFiberRatio(object):
    """
    Defines a ImportedFiberRatio.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedForce(object):
    """
    Defines a ImportedForce.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedHeatFlux(object):
    """
    Defines a ImportedHeatFlux.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedHeatGeneration(object):
    """
    Defines a ImportedHeatGeneration.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedInitialStrain(object):
    """
    Defines a ImportedInitialStrain.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedInitialStress(object):
    """
    Defines a ImportedInitialStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedMaterialField(object):
    """
    Defines a ImportedMaterialField.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedPressure(object):
    """
    Defines a ImportedPressure.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LoadVectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the LoadVectorNumber.
        """
        return None

    @LoadVectorNumber.setter
    def LoadVectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LoadVectorNumber.
        """
        pass

    @property
    def LoadVectorNumberImaginary(self) -> typing.Optional[int]:
        """
        Gets or sets the LoadVectorNumberImaginary.
        """
        return None

    @LoadVectorNumberImaginary.setter
    def LoadVectorNumberImaginary(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LoadVectorNumberImaginary.
        """
        pass

    @property
    def AppliedBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadAppliedBy]:
        """
        Gets or sets the AppliedBy.
        """
        return None

    @AppliedBy.setter
    def AppliedBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadAppliedBy]) -> None:
        """
        Gets or sets the AppliedBy.
        """
        pass

    @property
    def LoadVectorAssignment(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadVectorAssignment]:
        """
        Gets or sets the LoadVectorAssignment.
        """
        return None

    @LoadVectorAssignment.setter
    def LoadVectorAssignment(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LoadVectorAssignment]) -> None:
        """
        Gets or sets the LoadVectorAssignment.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedThickness(object):
    """
    Defines a ImportedThickness.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedWarpWeftRatio(object):
    """
    Defines a ImportedWarpWeftRatio.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


class ImportedYarnAngle(object):
    """
    Defines a ImportedYarnAngle.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSExternalLoadAuto]:
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
    def Weighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]:
        """
        Weighting property.
        """
        return None

    @Weighting.setter
    def Weighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeightingType]) -> None:
        """
        Weighting property.
        """
        pass

    @property
    def MappingControl(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]:
        """
        MappingControl property.
        """
        return None

    @MappingControl.setter
    def MappingControl(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingControlType]) -> None:
        """
        MappingControl property.
        """
        pass

    @property
    def DisplaySourcePoints(self) -> typing.Optional[bool]:
        """
        DisplaySourcePoints property.
        """
        return None

    @DisplaySourcePoints.setter
    def DisplaySourcePoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePoints property.
        """
        pass

    @property
    def DisplaySourcePointIds(self) -> typing.Optional[bool]:
        """
        DisplaySourcePointIds property.
        """
        return None

    @DisplaySourcePointIds.setter
    def DisplaySourcePointIds(self, value: typing.Optional[bool]) -> None:
        """
        DisplaySourcePointIds property.
        """
        pass

    @property
    def DisplayInteriorPoints(self) -> typing.Optional[bool]:
        """
        DisplayInteriorPoints property.
        """
        return None

    @DisplayInteriorPoints.setter
    def DisplayInteriorPoints(self, value: typing.Optional[bool]) -> None:
        """
        DisplayInteriorPoints property.
        """
        pass

    @property
    def DisplayProjectionPlane(self) -> typing.Optional[bool]:
        """
        DisplayProjectionPlane property.
        """
        return None

    @DisplayProjectionPlane.setter
    def DisplayProjectionPlane(self, value: typing.Optional[bool]) -> None:
        """
        DisplayProjectionPlane property.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]:
        """
        Algorithm property.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingAlgorithm]) -> None:
        """
        Algorithm property.
        """
        pass

    @property
    def BoundingBoxTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        BoundingBoxTolerance property.
        """
        return None

    @BoundingBoxTolerance.setter
    def BoundingBoxTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        BoundingBoxTolerance property.
        """
        pass

    @property
    def CreateNameSelectionForMappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForMappedNodes property.
        """
        return None

    @CreateNameSelectionForMappedNodes.setter
    def CreateNameSelectionForMappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForMappedNodes property.
        """
        pass

    @property
    def CreateNameSelectionForOutsideNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        return None

    @CreateNameSelectionForOutsideNodes.setter
    def CreateNameSelectionForOutsideNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForOutsideNodes property.
        """
        pass

    @property
    def CreateNameSelectionForUnmappedNodes(self) -> typing.Optional[bool]:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        return None

    @CreateNameSelectionForUnmappedNodes.setter
    def CreateNameSelectionForUnmappedNodes(self, value: typing.Optional[bool]) -> None:
        """
        CreateNameSelectionForUnmappedNodes property.
        """
        pass

    @property
    def Mapping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]:
        """
        Mapping property.
        """
        return None

    @Mapping.setter
    def Mapping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingInterpolationType]) -> None:
        """
        Mapping property.
        """
        pass

    @property
    def LegendMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMaximum property.
        """
        return None

    @LegendMaximum.setter
    def LegendMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMaximum property.
        """
        pass

    @property
    def LegendMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        LegendMinimum property.
        """
        return None

    @LegendMinimum.setter
    def LegendMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        LegendMinimum property.
        """
        pass

    @property
    def LegendRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]:
        """
        LegendRange property.
        """
        return None

    @LegendRange.setter
    def LegendRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendRangeType]) -> None:
        """
        LegendRange property.
        """
        pass

    @property
    def MaxOutsideDistance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        MaxOutsideDistance property.
        """
        return None

    @MaxOutsideDistance.setter
    def MaxOutsideDistance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        MaxOutsideDistance property.
        """
        pass

    @property
    def Method(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingMethod]:
        """
        Method property.
        """
        return None

    @property
    def OutsideDistanceCheck(self) -> typing.Optional[bool]:
        """
        OutsideDistanceCheck property.
        """
        return None

    @OutsideDistanceCheck.setter
    def OutsideDistanceCheck(self, value: typing.Optional[bool]) -> None:
        """
        OutsideDistanceCheck property.
        """
        pass

    @property
    def OutsideOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]:
        """
        OutsideOption property.
        """
        return None

    @OutsideOption.setter
    def OutsideOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingOutsideOption]) -> None:
        """
        OutsideOption property.
        """
        pass

    @property
    def Projection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Projection property.
        """
        return None

    @Projection.setter
    def Projection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Projection property.
        """
        pass

    @property
    def RigidBodyTransformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]:
        """
        RigidBodyTransformationType property.
        """
        return None

    @RigidBodyTransformationType.setter
    def RigidBodyTransformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RigidBodyTransformationType]) -> None:
        """
        RigidBodyTransformationType property.
        """
        pass

    @property
    def RigidTransformSourceCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        return None

    @RigidTransformSourceCoordinateSystem.setter
    def RigidTransformSourceCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformSourceCoordinateSystem property.
        """
        pass

    @property
    def RigidTransformTargetCoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        return None

    @RigidTransformTargetCoordinateSystem.setter
    def RigidTransformTargetCoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        RigidTransformTargetCoordinateSystem property.
        """
        pass

    @property
    def ShellThicknessFactor(self) -> typing.Optional[float]:
        """
        ShellThicknessFactor property.
        """
        return None

    @ShellThicknessFactor.setter
    def ShellThicknessFactor(self, value: typing.Optional[float]) -> None:
        """
        ShellThicknessFactor property.
        """
        pass

    @property
    def SourceMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMaximum property.
        """
        return None

    @SourceMaximum.setter
    def SourceMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMaximum property.
        """
        pass

    @property
    def SourceMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        SourceMinimum property.
        """
        return None

    @SourceMinimum.setter
    def SourceMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        SourceMinimum property.
        """
        pass

    @property
    def VariableType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MappingVariableType]:
        """
        VariableType property.
        """
        return None

    @property
    def Interpolation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]:
        """
        Interpolation property.
        """
        return None

    @Interpolation.setter
    def Interpolation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.InterpolationType]) -> None:
        """
        Interpolation property.
        """
        pass

    @property
    def UnmappedNodesName(self) -> typing.Optional[str]:
        """
        UnmappedNodesName property.
        """
        return None

    @UnmappedNodesName.setter
    def UnmappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        UnmappedNodesName property.
        """
        pass

    @property
    def MappedNodesName(self) -> typing.Optional[str]:
        """
        MappedNodesName property.
        """
        return None

    @MappedNodesName.setter
    def MappedNodesName(self, value: typing.Optional[str]) -> None:
        """
        MappedNodesName property.
        """
        pass

    @property
    def OutsideNodesName(self) -> typing.Optional[str]:
        """
        OutsideNodesName property.
        """
        return None

    @OutsideNodesName.setter
    def OutsideNodesName(self, value: typing.Optional[str]) -> None:
        """
        OutsideNodesName property.
        """
        pass

    @property
    def Pinball(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Pinball property.
        """
        return None

    @Pinball.setter
    def Pinball(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Pinball property.
        """
        pass

    @property
    def NumberOfPoints(self) -> typing.Optional[int]:
        """
        NumberOfPoints property.
        """
        return None

    @NumberOfPoints.setter
    def NumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        NumberOfPoints property.
        """
        pass

    @property
    def OrientationRealignment(self) -> typing.Optional[bool]:
        """
        OrientationRealignment property.
        """
        return None

    @OrientationRealignment.setter
    def OrientationRealignment(self, value: typing.Optional[bool]) -> None:
        """
        OrientationRealignment property.
        """
        pass

    @property
    def Limit(self) -> typing.Optional[int]:
        """
        Limit property.
        """
        return None

    @Limit.setter
    def Limit(self, value: typing.Optional[int]) -> None:
        """
        Limit property.
        """
        pass

    @property
    def KrigingCorrelationFunction(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]:
        """
        KrigingCorrelationFunction property.
        """
        return None

    @KrigingCorrelationFunction.setter
    def KrigingCorrelationFunction(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingCorrFuncType]) -> None:
        """
        KrigingCorrelationFunction property.
        """
        pass

    @property
    def KrigingPolynom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]:
        """
        KrigingPolynom property.
        """
        return None

    @KrigingPolynom.setter
    def KrigingPolynom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.KrigingPolynomType]) -> None:
        """
        KrigingPolynom property.
        """
        pass

    @property
    def ExtrapolationTolerancePercent(self) -> typing.Optional[float]:
        """
        ExtrapolationTolerancePercent property.
        """
        return None

    @ExtrapolationTolerancePercent.setter
    def ExtrapolationTolerancePercent(self, value: typing.Optional[float]) -> None:
        """
        ExtrapolationTolerancePercent property.
        """
        pass

    @property
    def ApplyAs(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
        """
        return None

    @ApplyAs.setter
    def ApplyAs(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExternalLoadApplicationType]) -> None:
        """
        This controls how the imported load is applied, either as a boundary condition or an initial condition.
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
    def SharedRefBody(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Body]:
        """
        Gets or sets the SharedRefBody.
        """
        return None

    @SharedRefBody.setter
    def SharedRefBody(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Body]) -> None:
        """
        Gets or sets the SharedRefBody.
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

    def GetTableByName(self, name: str) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.WorksheetRow]:
        """
        GetTableByName method.
        """
        pass

    def CreateTabbedFile(self) -> str:
        """
        Gets mapped values.
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

    def Import(self) -> None:
        """
        Import.
        """
        pass

    def ImportLoad(self) -> None:
        """
        
            Run the ImportLoad action.
            
        """
        pass

    def ReloadConfiguration(self) -> None:
        """
        Reload the Imported Load's setup from its associated configuration file (if available).
        """
        pass

    def GetActivateAtLoadStep(self, stepNumber: int) -> bool:
        """
        GetActivateAtLoadStep method.
        """
        pass

    def SetActivateAtLoadStep(self, stepNumber: int, bActive: bool) -> None:
        """
        SetActivateAtLoadStep method.
        """
        pass

    def AddMappingValidation(self) -> Ansys.ACT.Automation.Mechanical.MappingValidation:
        """
        Creates a new MappingValidation
        """
        pass

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
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


