"""PhaseResponseResults module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class AccelerationPhaseResponse(object):
    """
    Defines a AccelerationPhaseResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def ChartDimensions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]:
        """
        Gets or sets the Chart Dimensions
        """
        return None

    @ChartDimensions.setter
    def ChartDimensions(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]) -> None:
        """
        Gets or sets the Chart Dimensions
        """
        pass

    @property
    def BoundaryCondition(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @BoundaryCondition.setter
    def BoundaryCondition(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]) -> None:
        """
        Gets or sets the BoundaryCondition.
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
    def CutFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutFrequency.
        """
        return None

    @CutFrequency.setter
    def CutFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutFrequency.
        """
        pass

    @property
    def SectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the SectorNumber.
        """
        return None

    @SectorNumber.setter
    def SectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SectorNumber.
        """
        pass

    @property
    def GeometrySelectionString(self) -> typing.Optional[str]:
        """
        Gets or sets the GeometrySelectionString.
        """
        return None

    @GeometrySelectionString.setter
    def GeometrySelectionString(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GeometrySelectionString.
        """
        pass

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
    def ReportedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ReportedFrequency.
        """
        return None

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Duration.
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Duration.
        """
        pass

    @property
    def FilterMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMaximum.
        """
        return None

    @property
    def FilterMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMinimum.
        """
        return None

    @property
    def FrequencyAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FrequencyAtMaximumAmplitude.
        """
        return None

    @property
    def ImaginaryAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ImaginaryAtMaximumAmplitude.
        """
        return None

    @property
    def MaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumAmplitude.
        """
        return None

    @property
    def MaximumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumFrequency.
        """
        return None

    @MaximumFrequency.setter
    def MaximumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumFrequency.
        """
        pass

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MinimumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumFrequency.
        """
        return None

    @MinimumFrequency.setter
    def MinimumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumFrequency.
        """
        pass

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def PhaseAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PhaseAngle.
        """
        return None

    @property
    def RealAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the RealAtMaximumAmplitude.
        """
        return None

    @property
    def RequestedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RequestedFrequency.
        """
        return None

    @RequestedFrequency.setter
    def RequestedFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RequestedFrequency.
        """
        pass

    @property
    def AccelerationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the AccelerationType.
        """
        return None

    @AccelerationType.setter
    def AccelerationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the AccelerationType.
        """
        pass

    @property
    def ChartViewingStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]:
        """
        Gets or sets the ChartViewingStyle.
        """
        return None

    @ChartViewingStyle.setter
    def ChartViewingStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]) -> None:
        """
        Gets or sets the ChartViewingStyle.
        """
        pass

    @property
    def DeformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the DeformationType.
        """
        return None

    @DeformationType.setter
    def DeformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the DeformationType.
        """
        pass

    @property
    def FilterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]:
        """
        Gets or sets the FilterType.
        """
        return None

    @FilterType.setter
    def FilterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]) -> None:
        """
        Gets or sets the FilterType.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets the SpatialResolution.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets the SpatialResolution.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the NormalOrientation.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the NormalOrientation.
        """
        pass

    @property
    def CurvesAppearanceDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        return None

    @CurvesAppearanceDisplay.setter
    def CurvesAppearanceDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]) -> None:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        pass

    @property
    def ResultChartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartResultType]:
        """
        Gets the ResultChartType.
        """
        return None

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
    def XAxisValues(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]:
        """
        Gets or sets the XAxisValues.
        """
        return None

    @XAxisValues.setter
    def XAxisValues(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]) -> None:
        """
        Gets or sets the XAxisValues.
        """
        pass

    @property
    def ShearOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]:
        """
        Gets or sets the ShearOrientation.
        """
        return None

    @ShearOrientation.setter
    def ShearOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]) -> None:
        """
        Gets or sets the ShearOrientation.
        """
        pass

    @property
    def StressStrainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]:
        """
        Gets or sets the StressStrainType.
        """
        return None

    @StressStrainType.setter
    def StressStrainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]) -> None:
        """
        Gets or sets the StressStrainType.
        """
        pass

    @property
    def TimeHistoryDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        return None

    @TimeHistoryDisplay.setter
    def TimeHistoryDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]) -> None:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        pass

    @property
    def VelocityType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the VelocityType.
        """
        return None

    @VelocityType.setter
    def VelocityType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the VelocityType.
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
    def EnhancedTracking(self) -> typing.Optional[bool]:
        """
        Gets the EnhancedTracking.
        """
        return None

    @property
    def UseParentFrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseParentFrequencyRange.
        """
        return None

    @UseParentFrequencyRange.setter
    def UseParentFrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseParentFrequencyRange.
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
    def Spring(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]:
        """
        Gets or sets the Spring.
        """
        return None

    @Spring.setter
    def Spring(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]) -> None:
        """
        Gets or sets the Spring.
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

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
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

    def GetQuantityNameFromType(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityNameFromType method.
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


class DeformationPhaseResponse(object):
    """
    Defines a DeformationPhaseResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
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
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def ChartDimensions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]:
        """
        Gets or sets the Chart Dimensions
        """
        return None

    @ChartDimensions.setter
    def ChartDimensions(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]) -> None:
        """
        Gets or sets the Chart Dimensions
        """
        pass

    @property
    def BoundaryCondition(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @BoundaryCondition.setter
    def BoundaryCondition(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]) -> None:
        """
        Gets or sets the BoundaryCondition.
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
    def CutFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutFrequency.
        """
        return None

    @CutFrequency.setter
    def CutFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutFrequency.
        """
        pass

    @property
    def SectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the SectorNumber.
        """
        return None

    @SectorNumber.setter
    def SectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SectorNumber.
        """
        pass

    @property
    def GeometrySelectionString(self) -> typing.Optional[str]:
        """
        Gets or sets the GeometrySelectionString.
        """
        return None

    @GeometrySelectionString.setter
    def GeometrySelectionString(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GeometrySelectionString.
        """
        pass

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
    def ReportedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ReportedFrequency.
        """
        return None

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Duration.
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Duration.
        """
        pass

    @property
    def FilterMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMaximum.
        """
        return None

    @property
    def FilterMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMinimum.
        """
        return None

    @property
    def FrequencyAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FrequencyAtMaximumAmplitude.
        """
        return None

    @property
    def ImaginaryAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ImaginaryAtMaximumAmplitude.
        """
        return None

    @property
    def MaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumAmplitude.
        """
        return None

    @property
    def MaximumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumFrequency.
        """
        return None

    @MaximumFrequency.setter
    def MaximumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumFrequency.
        """
        pass

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MinimumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumFrequency.
        """
        return None

    @MinimumFrequency.setter
    def MinimumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumFrequency.
        """
        pass

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def PhaseAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PhaseAngle.
        """
        return None

    @property
    def RealAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the RealAtMaximumAmplitude.
        """
        return None

    @property
    def RequestedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RequestedFrequency.
        """
        return None

    @RequestedFrequency.setter
    def RequestedFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RequestedFrequency.
        """
        pass

    @property
    def AccelerationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the AccelerationType.
        """
        return None

    @AccelerationType.setter
    def AccelerationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the AccelerationType.
        """
        pass

    @property
    def ChartViewingStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]:
        """
        Gets or sets the ChartViewingStyle.
        """
        return None

    @ChartViewingStyle.setter
    def ChartViewingStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]) -> None:
        """
        Gets or sets the ChartViewingStyle.
        """
        pass

    @property
    def DeformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the DeformationType.
        """
        return None

    @DeformationType.setter
    def DeformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the DeformationType.
        """
        pass

    @property
    def FilterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]:
        """
        Gets or sets the FilterType.
        """
        return None

    @FilterType.setter
    def FilterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]) -> None:
        """
        Gets or sets the FilterType.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets the SpatialResolution.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets the SpatialResolution.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the NormalOrientation.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the NormalOrientation.
        """
        pass

    @property
    def CurvesAppearanceDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        return None

    @CurvesAppearanceDisplay.setter
    def CurvesAppearanceDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]) -> None:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        pass

    @property
    def ResultChartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartResultType]:
        """
        Gets the ResultChartType.
        """
        return None

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
    def XAxisValues(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]:
        """
        Gets or sets the XAxisValues.
        """
        return None

    @XAxisValues.setter
    def XAxisValues(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]) -> None:
        """
        Gets or sets the XAxisValues.
        """
        pass

    @property
    def ShearOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]:
        """
        Gets or sets the ShearOrientation.
        """
        return None

    @ShearOrientation.setter
    def ShearOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]) -> None:
        """
        Gets or sets the ShearOrientation.
        """
        pass

    @property
    def StressStrainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]:
        """
        Gets or sets the StressStrainType.
        """
        return None

    @StressStrainType.setter
    def StressStrainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]) -> None:
        """
        Gets or sets the StressStrainType.
        """
        pass

    @property
    def TimeHistoryDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        return None

    @TimeHistoryDisplay.setter
    def TimeHistoryDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]) -> None:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        pass

    @property
    def VelocityType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the VelocityType.
        """
        return None

    @VelocityType.setter
    def VelocityType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the VelocityType.
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
    def EnhancedTracking(self) -> typing.Optional[bool]:
        """
        Gets the EnhancedTracking.
        """
        return None

    @property
    def UseParentFrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseParentFrequencyRange.
        """
        return None

    @UseParentFrequencyRange.setter
    def UseParentFrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseParentFrequencyRange.
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
    def Spring(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]:
        """
        Gets or sets the Spring.
        """
        return None

    @Spring.setter
    def Spring(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]) -> None:
        """
        Gets or sets the Spring.
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

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
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

    def GetQuantityNameFromType(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityNameFromType method.
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


class ElasticStrainPhaseResponse(object):
    """
    Defines a ElasticStrainPhaseResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def ChartDimensions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]:
        """
        Gets or sets the Chart Dimensions
        """
        return None

    @ChartDimensions.setter
    def ChartDimensions(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]) -> None:
        """
        Gets or sets the Chart Dimensions
        """
        pass

    @property
    def BoundaryCondition(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @BoundaryCondition.setter
    def BoundaryCondition(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]) -> None:
        """
        Gets or sets the BoundaryCondition.
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
    def CutFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutFrequency.
        """
        return None

    @CutFrequency.setter
    def CutFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutFrequency.
        """
        pass

    @property
    def SectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the SectorNumber.
        """
        return None

    @SectorNumber.setter
    def SectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SectorNumber.
        """
        pass

    @property
    def GeometrySelectionString(self) -> typing.Optional[str]:
        """
        Gets or sets the GeometrySelectionString.
        """
        return None

    @GeometrySelectionString.setter
    def GeometrySelectionString(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GeometrySelectionString.
        """
        pass

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
    def ReportedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ReportedFrequency.
        """
        return None

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Duration.
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Duration.
        """
        pass

    @property
    def FilterMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMaximum.
        """
        return None

    @property
    def FilterMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMinimum.
        """
        return None

    @property
    def FrequencyAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FrequencyAtMaximumAmplitude.
        """
        return None

    @property
    def ImaginaryAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ImaginaryAtMaximumAmplitude.
        """
        return None

    @property
    def MaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumAmplitude.
        """
        return None

    @property
    def MaximumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumFrequency.
        """
        return None

    @MaximumFrequency.setter
    def MaximumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumFrequency.
        """
        pass

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MinimumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumFrequency.
        """
        return None

    @MinimumFrequency.setter
    def MinimumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumFrequency.
        """
        pass

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def PhaseAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PhaseAngle.
        """
        return None

    @property
    def RealAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the RealAtMaximumAmplitude.
        """
        return None

    @property
    def RequestedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RequestedFrequency.
        """
        return None

    @RequestedFrequency.setter
    def RequestedFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RequestedFrequency.
        """
        pass

    @property
    def AccelerationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the AccelerationType.
        """
        return None

    @AccelerationType.setter
    def AccelerationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the AccelerationType.
        """
        pass

    @property
    def ChartViewingStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]:
        """
        Gets or sets the ChartViewingStyle.
        """
        return None

    @ChartViewingStyle.setter
    def ChartViewingStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]) -> None:
        """
        Gets or sets the ChartViewingStyle.
        """
        pass

    @property
    def DeformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the DeformationType.
        """
        return None

    @DeformationType.setter
    def DeformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the DeformationType.
        """
        pass

    @property
    def FilterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]:
        """
        Gets or sets the FilterType.
        """
        return None

    @FilterType.setter
    def FilterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]) -> None:
        """
        Gets or sets the FilterType.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets the SpatialResolution.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets the SpatialResolution.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the NormalOrientation.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the NormalOrientation.
        """
        pass

    @property
    def CurvesAppearanceDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        return None

    @CurvesAppearanceDisplay.setter
    def CurvesAppearanceDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]) -> None:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        pass

    @property
    def ResultChartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartResultType]:
        """
        Gets the ResultChartType.
        """
        return None

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
    def XAxisValues(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]:
        """
        Gets or sets the XAxisValues.
        """
        return None

    @XAxisValues.setter
    def XAxisValues(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]) -> None:
        """
        Gets or sets the XAxisValues.
        """
        pass

    @property
    def ShearOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]:
        """
        Gets or sets the ShearOrientation.
        """
        return None

    @ShearOrientation.setter
    def ShearOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]) -> None:
        """
        Gets or sets the ShearOrientation.
        """
        pass

    @property
    def StressStrainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]:
        """
        Gets or sets the StressStrainType.
        """
        return None

    @StressStrainType.setter
    def StressStrainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]) -> None:
        """
        Gets or sets the StressStrainType.
        """
        pass

    @property
    def TimeHistoryDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        return None

    @TimeHistoryDisplay.setter
    def TimeHistoryDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]) -> None:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        pass

    @property
    def VelocityType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the VelocityType.
        """
        return None

    @VelocityType.setter
    def VelocityType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the VelocityType.
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
    def EnhancedTracking(self) -> typing.Optional[bool]:
        """
        Gets the EnhancedTracking.
        """
        return None

    @property
    def UseParentFrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseParentFrequencyRange.
        """
        return None

    @UseParentFrequencyRange.setter
    def UseParentFrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseParentFrequencyRange.
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
    def Spring(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]:
        """
        Gets or sets the Spring.
        """
        return None

    @Spring.setter
    def Spring(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]) -> None:
        """
        Gets or sets the Spring.
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

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
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

    def GetQuantityNameFromType(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityNameFromType method.
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


class StressPhaseResponse(object):
    """
    Defines a StressPhaseResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
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
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def ChartDimensions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]:
        """
        Gets or sets the Chart Dimensions
        """
        return None

    @ChartDimensions.setter
    def ChartDimensions(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]) -> None:
        """
        Gets or sets the Chart Dimensions
        """
        pass

    @property
    def BoundaryCondition(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @BoundaryCondition.setter
    def BoundaryCondition(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]) -> None:
        """
        Gets or sets the BoundaryCondition.
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
    def CutFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutFrequency.
        """
        return None

    @CutFrequency.setter
    def CutFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutFrequency.
        """
        pass

    @property
    def SectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the SectorNumber.
        """
        return None

    @SectorNumber.setter
    def SectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SectorNumber.
        """
        pass

    @property
    def GeometrySelectionString(self) -> typing.Optional[str]:
        """
        Gets or sets the GeometrySelectionString.
        """
        return None

    @GeometrySelectionString.setter
    def GeometrySelectionString(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GeometrySelectionString.
        """
        pass

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
    def ReportedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ReportedFrequency.
        """
        return None

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Duration.
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Duration.
        """
        pass

    @property
    def FilterMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMaximum.
        """
        return None

    @property
    def FilterMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMinimum.
        """
        return None

    @property
    def FrequencyAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FrequencyAtMaximumAmplitude.
        """
        return None

    @property
    def ImaginaryAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ImaginaryAtMaximumAmplitude.
        """
        return None

    @property
    def MaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumAmplitude.
        """
        return None

    @property
    def MaximumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumFrequency.
        """
        return None

    @MaximumFrequency.setter
    def MaximumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumFrequency.
        """
        pass

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MinimumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumFrequency.
        """
        return None

    @MinimumFrequency.setter
    def MinimumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumFrequency.
        """
        pass

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def PhaseAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PhaseAngle.
        """
        return None

    @property
    def RealAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the RealAtMaximumAmplitude.
        """
        return None

    @property
    def RequestedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RequestedFrequency.
        """
        return None

    @RequestedFrequency.setter
    def RequestedFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RequestedFrequency.
        """
        pass

    @property
    def AccelerationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the AccelerationType.
        """
        return None

    @AccelerationType.setter
    def AccelerationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the AccelerationType.
        """
        pass

    @property
    def ChartViewingStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]:
        """
        Gets or sets the ChartViewingStyle.
        """
        return None

    @ChartViewingStyle.setter
    def ChartViewingStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]) -> None:
        """
        Gets or sets the ChartViewingStyle.
        """
        pass

    @property
    def DeformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the DeformationType.
        """
        return None

    @DeformationType.setter
    def DeformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the DeformationType.
        """
        pass

    @property
    def FilterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]:
        """
        Gets or sets the FilterType.
        """
        return None

    @FilterType.setter
    def FilterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]) -> None:
        """
        Gets or sets the FilterType.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets the SpatialResolution.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets the SpatialResolution.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the NormalOrientation.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the NormalOrientation.
        """
        pass

    @property
    def CurvesAppearanceDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        return None

    @CurvesAppearanceDisplay.setter
    def CurvesAppearanceDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]) -> None:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        pass

    @property
    def ResultChartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartResultType]:
        """
        Gets the ResultChartType.
        """
        return None

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
    def XAxisValues(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]:
        """
        Gets or sets the XAxisValues.
        """
        return None

    @XAxisValues.setter
    def XAxisValues(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]) -> None:
        """
        Gets or sets the XAxisValues.
        """
        pass

    @property
    def ShearOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]:
        """
        Gets or sets the ShearOrientation.
        """
        return None

    @ShearOrientation.setter
    def ShearOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]) -> None:
        """
        Gets or sets the ShearOrientation.
        """
        pass

    @property
    def StressStrainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]:
        """
        Gets or sets the StressStrainType.
        """
        return None

    @StressStrainType.setter
    def StressStrainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]) -> None:
        """
        Gets or sets the StressStrainType.
        """
        pass

    @property
    def TimeHistoryDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        return None

    @TimeHistoryDisplay.setter
    def TimeHistoryDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]) -> None:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        pass

    @property
    def VelocityType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the VelocityType.
        """
        return None

    @VelocityType.setter
    def VelocityType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the VelocityType.
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
    def EnhancedTracking(self) -> typing.Optional[bool]:
        """
        Gets the EnhancedTracking.
        """
        return None

    @property
    def UseParentFrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseParentFrequencyRange.
        """
        return None

    @UseParentFrequencyRange.setter
    def UseParentFrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseParentFrequencyRange.
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
    def Spring(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]:
        """
        Gets or sets the Spring.
        """
        return None

    @Spring.setter
    def Spring(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]) -> None:
        """
        Gets or sets the Spring.
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

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
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

    def GetQuantityNameFromType(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityNameFromType method.
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


class VelocityPhaseResponse(object):
    """
    Defines a VelocityPhaseResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def IsSolved(self) -> typing.Optional[bool]:
        """
        Gets the IsSolved.
        """
        return None

    @property
    def ChartDimensions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]:
        """
        Gets or sets the Chart Dimensions
        """
        return None

    @ChartDimensions.setter
    def ChartDimensions(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartDimensions]) -> None:
        """
        Gets or sets the Chart Dimensions
        """
        pass

    @property
    def BoundaryCondition(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]:
        """
        Gets or sets the BoundaryCondition.
        """
        return None

    @BoundaryCondition.setter
    def BoundaryCondition(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.BoundaryConditions.GenericBoundaryCondition]) -> None:
        """
        Gets or sets the BoundaryCondition.
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
    def CutFrequency(self) -> typing.Optional[float]:
        """
        Gets or sets the CutFrequency.
        """
        return None

    @CutFrequency.setter
    def CutFrequency(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CutFrequency.
        """
        pass

    @property
    def SectorNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the SectorNumber.
        """
        return None

    @SectorNumber.setter
    def SectorNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SectorNumber.
        """
        pass

    @property
    def GeometrySelectionString(self) -> typing.Optional[str]:
        """
        Gets or sets the GeometrySelectionString.
        """
        return None

    @GeometrySelectionString.setter
    def GeometrySelectionString(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the GeometrySelectionString.
        """
        pass

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
    def ReportedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ReportedFrequency.
        """
        return None

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Duration.
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Duration.
        """
        pass

    @property
    def FilterMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMaximum.
        """
        return None

    @property
    def FilterMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FilterMinimum.
        """
        return None

    @property
    def FrequencyAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the FrequencyAtMaximumAmplitude.
        """
        return None

    @property
    def ImaginaryAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ImaginaryAtMaximumAmplitude.
        """
        return None

    @property
    def MaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MaximumAmplitude.
        """
        return None

    @property
    def MaximumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumFrequency.
        """
        return None

    @MaximumFrequency.setter
    def MaximumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumFrequency.
        """
        pass

    @property
    def Maximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Maximum.
        """
        return None

    @property
    def MinimumFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumFrequency.
        """
        return None

    @MinimumFrequency.setter
    def MinimumFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumFrequency.
        """
        pass

    @property
    def Minimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Minimum.
        """
        return None

    @property
    def PhaseAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PhaseAngle.
        """
        return None

    @property
    def RealAtMaximumAmplitude(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the RealAtMaximumAmplitude.
        """
        return None

    @property
    def RequestedFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RequestedFrequency.
        """
        return None

    @RequestedFrequency.setter
    def RequestedFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RequestedFrequency.
        """
        pass

    @property
    def AccelerationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the AccelerationType.
        """
        return None

    @AccelerationType.setter
    def AccelerationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the AccelerationType.
        """
        pass

    @property
    def ChartViewingStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]:
        """
        Gets or sets the ChartViewingStyle.
        """
        return None

    @ChartViewingStyle.setter
    def ChartViewingStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartAxisScaleType]) -> None:
        """
        Gets or sets the ChartViewingStyle.
        """
        pass

    @property
    def DeformationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the DeformationType.
        """
        return None

    @DeformationType.setter
    def DeformationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the DeformationType.
        """
        pass

    @property
    def FilterType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]:
        """
        Gets or sets the FilterType.
        """
        return None

    @FilterType.setter
    def FilterType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FilterType]) -> None:
        """
        Gets or sets the FilterType.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets the SpatialResolution.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets the SpatialResolution.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the NormalOrientation.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the NormalOrientation.
        """
        pass

    @property
    def CurvesAppearanceDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        return None

    @CurvesAppearanceDisplay.setter
    def CurvesAppearanceDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartPlotStyle]) -> None:
        """
        Gets or sets the CurvesAppearanceDisplay.
        """
        pass

    @property
    def ResultChartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ChartResultType]:
        """
        Gets the ResultChartType.
        """
        return None

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
    def XAxisValues(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]:
        """
        Gets or sets the XAxisValues.
        """
        return None

    @XAxisValues.setter
    def XAxisValues(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.XAxisValues]) -> None:
        """
        Gets or sets the XAxisValues.
        """
        pass

    @property
    def ShearOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]:
        """
        Gets or sets the ShearOrientation.
        """
        return None

    @ShearOrientation.setter
    def ShearOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShearOrientationType]) -> None:
        """
        Gets or sets the ShearOrientation.
        """
        pass

    @property
    def StressStrainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]:
        """
        Gets or sets the StressStrainType.
        """
        return None

    @StressStrainType.setter
    def StressStrainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StressStrainType]) -> None:
        """
        Gets or sets the StressStrainType.
        """
        pass

    @property
    def TimeHistoryDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        return None

    @TimeHistoryDisplay.setter
    def TimeHistoryDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeHistoryDisplayType]) -> None:
        """
        Gets or sets the TimeHistoryDisplay.
        """
        pass

    @property
    def VelocityType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]:
        """
        Gets or sets the VelocityType.
        """
        return None

    @VelocityType.setter
    def VelocityType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TotalOrDirectional]) -> None:
        """
        Gets or sets the VelocityType.
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
    def EnhancedTracking(self) -> typing.Optional[bool]:
        """
        Gets the EnhancedTracking.
        """
        return None

    @property
    def UseParentFrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseParentFrequencyRange.
        """
        return None

    @UseParentFrequencyRange.setter
    def UseParentFrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseParentFrequencyRange.
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
    def Spring(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]:
        """
        Gets or sets the Spring.
        """
        return None

    @Spring.setter
    def Spring(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Spring]) -> None:
        """
        Gets or sets the Spring.
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

    def GetQuantityName(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityName method.
        """
        pass

    def ExportAnimation(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsAnimationExportFormat, settings: Ansys.Mechanical.Graphics.AnimationExportSettings) -> None:
        """
        Run the ExportAnimation action.
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

    def GetQuantityNameFromType(self, obj: Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto) -> str:
        """
        GetQuantityNameFromType method.
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


