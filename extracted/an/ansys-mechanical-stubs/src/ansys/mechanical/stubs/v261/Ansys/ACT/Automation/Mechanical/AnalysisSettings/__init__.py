"""AnalysisSettings module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class TopoOptAnalysisSettings(object):
    """
    Defines a TopoOptAnalysisSettings.
    """

    @property
    def ExportDesignProperties(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationExportDesignProperties]:
        """
        Gets or sets the ExportDesignProperties.
        """
        return None

    @ExportDesignProperties.setter
    def ExportDesignProperties(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationExportDesignProperties]) -> None:
        """
        Gets or sets the ExportDesignProperties.
        """
        pass

    @property
    def ExportDesignPropertiesFileFormat(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationExportDesignPropertiesFileFormat]:
        """
        Gets or sets the ExportDesignPropertiesFileFormat.
        """
        return None

    @ExportDesignPropertiesFileFormat.setter
    def ExportDesignPropertiesFileFormat(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationExportDesignPropertiesFileFormat]) -> None:
        """
        Gets or sets the ExportDesignPropertiesFileFormat.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSAnalysisSettingsObjects.IDSAnalysisSettings]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ConvergenceAccuracy(self) -> typing.Optional[float]:
        """
        Gets or sets the ConvergenceAccuracy.
        """
        return None

    @ConvergenceAccuracy.setter
    def ConvergenceAccuracy(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ConvergenceAccuracy.
        """
        pass

    @property
    def TopoOptInitialDensity(self) -> typing.Optional[float]:
        """
        Gets or sets the TopoOptInitialDensity.
        """
        return None

    @TopoOptInitialDensity.setter
    def TopoOptInitialDensity(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TopoOptInitialDensity.
        """
        pass

    @property
    def MaxNumOfIntermediateFiles(self) -> typing.Optional[int]:
        """
        Gets or sets the MaxNumOfIntermediateFiles.
        """
        return None

    @MaxNumOfIntermediateFiles.setter
    def MaxNumOfIntermediateFiles(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaxNumOfIntermediateFiles.
        """
        pass

    @property
    def MaximumNumberOfIterations(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumNumberOfIterations.
        """
        return None

    @MaximumNumberOfIterations.setter
    def MaximumNumberOfIterations(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumNumberOfIterations.
        """
        pass

    @property
    def MinimumNormalizedDensity(self) -> typing.Optional[float]:
        """
        Gets or sets the MinimumNormalizedDensity.
        """
        return None

    @MinimumNormalizedDensity.setter
    def MinimumNormalizedDensity(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MinimumNormalizedDensity.
        """
        pass

    @property
    def StoreResultsAtValue(self) -> typing.Optional[int]:
        """
        Gets or sets the StoreResultsAtValue.
        """
        return None

    @StoreResultsAtValue.setter
    def StoreResultsAtValue(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the StoreResultsAtValue.
        """
        pass

    @property
    def PenaltyFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PenaltyFactor.
        """
        return None

    @PenaltyFactor.setter
    def PenaltyFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PenaltyFactor.
        """
        pass

    @property
    def Algorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AlgorithmType]:
        """
        Gets or sets the Algorithm.
        """
        return None

    @Algorithm.setter
    def Algorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AlgorithmType]) -> None:
        """
        Gets or sets the Algorithm.
        """
        pass

    @property
    def StoreResultsAt(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.IterationOptions]:
        """
        Gets or sets the StoreResultsAt.
        """
        return None

    @StoreResultsAt.setter
    def StoreResultsAt(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.IterationOptions]) -> None:
        """
        Gets or sets the StoreResultsAt.
        """
        pass

    @property
    def FutureAnalysis(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FutureIntentType]:
        """
        Gets or sets the FutureAnalysis.
        """
        return None

    @FutureAnalysis.setter
    def FutureAnalysis(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FutureIntentType]) -> None:
        """
        Gets or sets the FutureAnalysis.
        """
        pass

    @property
    def MultiOptimTypeStrategy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultiOptimTypeStrategyType]:
        """
        Gets or sets the MultiOptimTypeStrategy.
        """
        return None

    @MultiOptimTypeStrategy.setter
    def MultiOptimTypeStrategy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultiOptimTypeStrategyType]) -> None:
        """
        Gets or sets the MultiOptimTypeStrategy.
        """
        pass

    @property
    def OptimizationOutputLog(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationOutputLog]:
        """
        Gets or sets the OptimizationOutputLog.
        """
        return None

    @OptimizationOutputLog.setter
    def OptimizationOutputLog(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationOutputLog]) -> None:
        """
        Gets or sets the OptimizationOutputLog.
        """
        pass

    @property
    def RegionOfAMOverhangConstraint(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]:
        """
        Gets or sets the RegionOfAMOverhangConstraint.
        """
        return None

    @RegionOfAMOverhangConstraint.setter
    def RegionOfAMOverhangConstraint(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]) -> None:
        """
        Gets or sets the RegionOfAMOverhangConstraint.
        """
        pass

    @property
    def RegionOfManufacturingConstraint(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]:
        """
        Gets or sets the RegionOfManufacturingConstraint.
        """
        return None

    @RegionOfManufacturingConstraint.setter
    def RegionOfManufacturingConstraint(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]) -> None:
        """
        Gets or sets the RegionOfManufacturingConstraint.
        """
        pass

    @property
    def RegionOfMinMemberSize(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]:
        """
        Gets or sets the RegionOfMinMemberSize.
        """
        return None

    @RegionOfMinMemberSize.setter
    def RegionOfMinMemberSize(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExclusionParticipantType]) -> None:
        """
        Gets or sets the RegionOfMinMemberSize.
        """
        pass

    @property
    def SolverUnitSystem(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the SolverUnitSystem.
        """
        return None

    @SolverUnitSystem.setter
    def SolverUnitSystem(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the SolverUnitSystem.
        """
        pass

    @property
    def SolverType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.OptimizationSolverType]:
        """
        Gets or sets the SolverType.
        """
        return None

    @SolverType.setter
    def SolverType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.OptimizationSolverType]) -> None:
        """
        Gets or sets the SolverType.
        """
        pass

    @property
    def SolverUnits(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverUnitsControlType]:
        """
        Gets or sets the SolverUnits.
        """
        return None

    @SolverUnits.setter
    def SolverUnits(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverUnitsControlType]) -> None:
        """
        Gets or sets the SolverUnits.
        """
        pass

    @property
    def Filter(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationDensityFilter]:
        """
        Gets or sets the Filter.
        """
        return None

    @Filter.setter
    def Filter(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TopoOptimizationDensityFilter]) -> None:
        """
        Gets or sets the Filter.
        """
        pass

    @property
    def DeleteUnneededFiles(self) -> typing.Optional[bool]:
        """
        Gets or sets the DeleteUnneededFiles.
        """
        return None

    @DeleteUnneededFiles.setter
    def DeleteUnneededFiles(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DeleteUnneededFiles.
        """
        pass

    @property
    def ExportKnockdownFilePath(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExportKnockdownFilePath.
        """
        return None

    @ExportKnockdownFilePath.setter
    def ExportKnockdownFilePath(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExportKnockdownFilePath.
        """
        pass

    @property
    def SaveMAPDLDB(self) -> typing.Optional[bool]:
        """
        Gets or sets the SaveMAPDLDB.
        """
        return None

    @SaveMAPDLDB.setter
    def SaveMAPDLDB(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SaveMAPDLDB.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Graph(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnalysisSettingsGraph]:
        """
        Graph property.
        """
        return None

    @property
    def SurfaceStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the SurfaceStress.
        """
        return None

    @SurfaceStress.setter
    def SurfaceStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SurfaceStress.
        """
        pass

    @property
    def ScratchSolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the ScratchSolverFilesDirectory.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the SolverFilesDirectory.
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

    def DeleteAllRestartPoints(self) -> None:
        """
        DeleteAllRestartPoints method.
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


class AnalysisSettings(object):
    """
    Defines a AnalysisSettings.
    """

    @property
    def Graph(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnalysisSettingsGraph]:
        """
        Graph property.
        """
        return None

    @property
    def SurfaceStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the SurfaceStress.
        """
        return None

    @SurfaceStress.setter
    def SurfaceStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SurfaceStress.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSAnalysisSettingsObjects.IDSAnalysisSettings]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ScratchSolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the ScratchSolverFilesDirectory.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the SolverFilesDirectory.
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

    def DeleteAllRestartPoints(self) -> None:
        """
        DeleteAllRestartPoints method.
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


class ANSYSAnalysisSettings(object):
    """
    Defines a ANSYSAnalysisSettings.
    """

    @property
    def StepName(self) -> typing.Optional[str]:
        """
        Gets or sets the Step Name.
        """
        return None

    @StepName.setter
    def StepName(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Step Name.
        """
        pass

    @property
    def AMStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        Gets or sets the AM Process Step Type.
        """
        return None

    @property
    def AMSubstepsToApplyHeats(self) -> typing.Optional[int]:
        """
        Gets or sets the AM Substeps to Apply Heat.
        """
        return None

    @AMSubstepsToApplyHeats.setter
    def AMSubstepsToApplyHeats(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AM Substeps to Apply Heat.
        """
        pass

    @property
    def AMSubstepsBetweenHeating(self) -> typing.Optional[int]:
        """
        Gets or sets the AM Substeps Between Heating.
        """
        return None

    @AMSubstepsBetweenHeating.setter
    def AMSubstepsBetweenHeating(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AM Substeps Between Heating.
        """
        pass

    @property
    def AMCooldownNumberOfSubsteps(self) -> typing.Optional[int]:
        """
        Gets or sets the AM Cooldown Number of Substeps.
        """
        return None

    @AMCooldownNumberOfSubsteps.setter
    def AMCooldownNumberOfSubsteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AM Cooldown Number of Substeps.
        """
        pass

    @property
    def CooldownTimeType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMCooldownTimeType]:
        """
        Gets or sets the AM Cooldown Time Type.
        """
        return None

    @CooldownTimeType.setter
    def CooldownTimeType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMCooldownTimeType]) -> None:
        """
        Gets or sets the AM Cooldown Time Type.
        """
        pass

    @property
    def CooldownTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AM Cooldown Time.
        """
        return None

    @CooldownTime.setter
    def CooldownTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AM Cooldown Time.
        """
        pass

    @property
    def LayersToBuild(self) -> typing.Optional[int]:
        """
        Gets or sets the AM Layers to Build.
        """
        return None

    @LayersToBuild.setter
    def LayersToBuild(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AM Layers to Build.
        """
        pass

    @property
    def ReferenceTemperatureType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMReferenceTemperatureType]:
        """
        Gets or sets the AM Reference Temperature Type.
        """
        return None

    @ReferenceTemperatureType.setter
    def ReferenceTemperatureType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMReferenceTemperatureType]) -> None:
        """
        Gets or sets the AM Reference Temperature Type.
        """
        pass

    @property
    def ReferenceTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AM Reference Temperature.
        """
        return None

    @ReferenceTemperature.setter
    def ReferenceTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AM Reference Temperature.
        """
        pass

    @property
    def RelaxationTemperatureType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMRelaxationTemperatureType]:
        """
        Gets or sets the AM Relaxation Temperature Type.
        """
        return None

    @RelaxationTemperatureType.setter
    def RelaxationTemperatureType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMRelaxationTemperatureType]) -> None:
        """
        Gets or sets the AM Relaxation Temperature Type.
        """
        pass

    @property
    def NumberOfRestartPoints(self) -> typing.Optional[int]:
        """
        Gets Number of Restart Points.
        """
        return None

    @property
    def CurrentRestartPoint(self) -> typing.Optional[int]:
        """
        Gets or sets the Current Restart Point.
        """
        return None

    @CurrentRestartPoint.setter
    def CurrentRestartPoint(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the Current Restart Point.
        """
        pass

    @property
    def AggressiveRemeshing(self) -> typing.Optional[bool]:
        """
        Gets or sets the AggressiveRemeshing.
        """
        return None

    @AggressiveRemeshing.setter
    def AggressiveRemeshing(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the AggressiveRemeshing.
        """
        pass

    @property
    def SpinSoftening(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpinSofteningType]:
        """
        Gets or sets the SpinSoftening.
        """
        return None

    @SpinSoftening.setter
    def SpinSoftening(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpinSofteningType]) -> None:
        """
        Gets or sets the SpinSoftening.
        """
        pass

    @property
    def UserDefinedFrequencySteps(self) -> typing.Optional[typing.List[Ansys.Core.Units.Quantity]]:
        """
        Gets or sets the UserDefinedFrequencySteps.
        """
        return None

    @UserDefinedFrequencySteps.setter
    def UserDefinedFrequencySteps(self, value: typing.Optional[typing.List[Ansys.Core.Units.Quantity]]) -> None:
        """
        Gets or sets the UserDefinedFrequencySteps.
        """
        pass

    @property
    def VariationalTechnology(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicVariationalTechnology]:
        """
        Gets or sets the VariationalTechnology.
        """
        return None

    @VariationalTechnology.setter
    def VariationalTechnology(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicVariationalTechnology]) -> None:
        """
        Gets or sets the VariationalTechnology.
        """
        pass

    @property
    def SkipExpansion(self) -> typing.Optional[bool]:
        """
        Gets or sets the SkipExpansion.
        """
        return None

    @SkipExpansion.setter
    def SkipExpansion(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SkipExpansion.
        """
        pass

    @property
    def OnDemandExpansion(self) -> typing.Optional[bool]:
        """
        Gets or sets the OnDemandExpansion.
        """
        return None

    @OnDemandExpansion.setter
    def OnDemandExpansion(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the OnDemandExpansion.
        """
        pass

    @property
    def CombineDistributedResultFiles(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CombineDistributedResultFilesType]:
        """
        Gets or sets the CombineDistributedResultFiles.
        """
        return None

    @CombineDistributedResultFiles.setter
    def CombineDistributedResultFiles(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CombineDistributedResultFilesType]) -> None:
        """
        Gets or sets the CombineDistributedResultFiles.
        """
        pass

    @property
    def MultipleRPMs(self) -> typing.Optional[bool]:
        """
        Gets or sets the MultipleRPMs.
        """
        return None

    @MultipleRPMs.setter
    def MultipleRPMs(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MultipleRPMs.
        """
        pass

    @property
    def CurrentRPMNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the CurrentRPMNumber.
        """
        return None

    @CurrentRPMNumber.setter
    def CurrentRPMNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CurrentRPMNumber.
        """
        pass

    @property
    def CoriolisEffect(self) -> typing.Optional[bool]:
        """
        Gets or sets the CoriolisEffect in Stationary Reference Frame.
        """
        return None

    @CoriolisEffect.setter
    def CoriolisEffect(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CoriolisEffect in Stationary Reference Frame.
        """
        pass

    @property
    def OutputSelection(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.OutputSelection]:
        """
        
            Gets or sets the Output Selection property in the Output Controls group of Analysis Settings.
            
        """
        return None

    @OutputSelection.setter
    def OutputSelection(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.OutputSelection]) -> None:
        """
        
            Gets or sets the Output Selection property in the Output Controls group of Analysis Settings.
            
        """
        pass

    @property
    def NamedSelection(self) -> typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]]:
        """
        
            Gets or sets the objects of type NamedSelection to -- Named Selection property in the Output Controls group of Analysis Settings.
            If the OutputSelection != OutputSelection.NamedSelection or NamedSelectionOnModeFile,
            1. NamedSelection cannot be set. An exception will be thrown saying “Cannot modify ANSYSAnalysisSettings.NamedSelection if ANSYSAnalysisSettings.OutputSelection is not set to "OutputSelection.NamedSelection”.”
            2. Getting the NamedSelection value will return an empty list.
            
        """
        return None

    @NamedSelection.setter
    def NamedSelection(self, value: typing.Optional[typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]]) -> None:
        """
        
            Gets or sets the objects of type NamedSelection to -- Named Selection property in the Output Controls group of Analysis Settings.
            If the OutputSelection != OutputSelection.NamedSelection or NamedSelectionOnModeFile,
            1. NamedSelection cannot be set. An exception will be thrown saying “Cannot modify ANSYSAnalysisSettings.NamedSelection if ANSYSAnalysisSettings.OutputSelection is not set to "OutputSelection.NamedSelection”.”
            2. Getting the NamedSelection value will return an empty list.
            
        """
        pass

    @property
    def GlobalSizeRatioExpansion(self) -> typing.Optional[float]:
        """
        Gets or sets the Expansion (GSR) to control remeshing via element coarsening. Default: 0. Valid range is greater than or equal to 0.
        """
        return None

    @GlobalSizeRatioExpansion.setter
    def GlobalSizeRatioExpansion(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Expansion (GSR) to control remeshing via element coarsening. Default: 0. Valid range is greater than or equal to 0.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSAnalysisSettingsObjects.IDSAnalysisSettings]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MassCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the MassCoefficient.
        """
        return None

    @MassCoefficient.setter
    def MassCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MassCoefficient.
        """
        pass

    @property
    def StiffnessCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the StiffnessCoefficient.
        """
        return None

    @StiffnessCoefficient.setter
    def StiffnessCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StiffnessCoefficient.
        """
        pass

    @property
    def DampingRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the DampingRatio.
        """
        return None

    @DampingRatio.setter
    def DampingRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DampingRatio.
        """
        pass

    @property
    def ConstantDampingRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the ConstantDampingRatio.
        """
        return None

    @ConstantDampingRatio.setter
    def ConstantDampingRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ConstantDampingRatio.
        """
        pass

    @property
    def StructuralDampingCoefficient(self) -> typing.Optional[float]:
        """
        Gets or sets the StructuralDampingCoefficient.
        """
        return None

    @StructuralDampingCoefficient.setter
    def StructuralDampingCoefficient(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StructuralDampingCoefficient.
        """
        pass

    @property
    def ContactSplitMaxNum(self) -> typing.Optional[int]:
        """
        Gets or sets the ContactSplitMaxNum.
        """
        return None

    @ContactSplitMaxNum.setter
    def ContactSplitMaxNum(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ContactSplitMaxNum.
        """
        pass

    @property
    def ChargeConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the ChargeConvergenceTolerance.
        """
        return None

    @ChargeConvergenceTolerance.setter
    def ChargeConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ChargeConvergenceTolerance.
        """
        pass

    @property
    def CurrentConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the CurrentConvergenceTolerance.
        """
        return None

    @CurrentConvergenceTolerance.setter
    def CurrentConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CurrentConvergenceTolerance.
        """
        pass

    @property
    def EmagAMPSConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the EmagAMPSConvergenceTolerance.
        """
        return None

    @EmagAMPSConvergenceTolerance.setter
    def EmagAMPSConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the EmagAMPSConvergenceTolerance.
        """
        pass

    @property
    def EmagCSGConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the EmagCSGConvergenceTolerance.
        """
        return None

    @EmagCSGConvergenceTolerance.setter
    def EmagCSGConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the EmagCSGConvergenceTolerance.
        """
        pass

    @property
    def EnergyConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the EnergyConvergenceTolerance.
        """
        return None

    @EnergyConvergenceTolerance.setter
    def EnergyConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the EnergyConvergenceTolerance.
        """
        pass

    @property
    def HeatConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the HeatConvergenceTolerance.
        """
        return None

    @HeatConvergenceTolerance.setter
    def HeatConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the HeatConvergenceTolerance.
        """
        pass

    @property
    def TemperatureConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the TemperatureConvergenceTolerance.
        """
        return None

    @TemperatureConvergenceTolerance.setter
    def TemperatureConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TemperatureConvergenceTolerance.
        """
        pass

    @property
    def VoltageConvergenceTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the VoltageConvergenceTolerance.
        """
        return None

    @VoltageConvergenceTolerance.setter
    def VoltageConvergenceTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the VoltageConvergenceTolerance.
        """
        pass

    @property
    def CreepLimitRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the CreepLimitRatio.
        """
        return None

    @CreepLimitRatio.setter
    def CreepLimitRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the CreepLimitRatio.
        """
        pass

    @property
    def CurrentStepNumberHarmonic(self) -> typing.Optional[int]:
        """
        Gets or sets the CurrentStepNumberHarmonic.
        """
        return None

    @CurrentStepNumberHarmonic.setter
    def CurrentStepNumberHarmonic(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CurrentStepNumberHarmonic.
        """
        pass

    @property
    def CurrentStepNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the CurrentStepNumber.
        """
        return None

    @CurrentStepNumber.setter
    def CurrentStepNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the CurrentStepNumber.
        """
        pass

    @property
    def EngineOrderofExcitation(self) -> typing.Optional[int]:
        """
        Gets or sets the EngineOrderofExcitation.
        """
        return None

    @EngineOrderofExcitation.setter
    def EngineOrderofExcitation(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the EngineOrderofExcitation.
        """
        pass

    @property
    def MaximumHarmonicIndex(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumHarmonicIndex.
        """
        return None

    @MaximumHarmonicIndex.setter
    def MaximumHarmonicIndex(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumHarmonicIndex.
        """
        pass

    @property
    def MinimumHarmonicIndex(self) -> typing.Optional[int]:
        """
        Gets or sets the MinimumHarmonicIndex.
        """
        return None

    @MinimumHarmonicIndex.setter
    def MinimumHarmonicIndex(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MinimumHarmonicIndex.
        """
        pass

    @property
    def HarmonicIndexInterval(self) -> typing.Optional[int]:
        """
        Gets or sets the HarmonicIndexInterval.
        """
        return None

    @HarmonicIndexInterval.setter
    def HarmonicIndexInterval(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the HarmonicIndexInterval.
        """
        pass

    @property
    def ClusterNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the ClusterNumber.
        """
        return None

    @ClusterNumber.setter
    def ClusterNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ClusterNumber.
        """
        pass

    @property
    def SolutionIntervals(self) -> typing.Optional[int]:
        """
        Gets or sets the SolutionIntervals.
        """
        return None

    @SolutionIntervals.setter
    def SolutionIntervals(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SolutionIntervals.
        """
        pass

    @property
    def KrylovSubspaceDimension(self) -> typing.Optional[int]:
        """
        Gets or sets the KrylovSubspaceDimension.
        """
        return None

    @KrylovSubspaceDimension.setter
    def KrylovSubspaceDimension(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the KrylovSubspaceDimension.
        """
        pass

    @property
    def KrylovResidualTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the KrylovResidualTolerance.
        """
        return None

    @KrylovResidualTolerance.setter
    def KrylovResidualTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the KrylovResidualTolerance.
        """
        pass

    @property
    def HarmonicOrders(self) -> typing.Optional[str]:
        """
        Gets or sets the HarmonicOrders.
        """
        return None

    @HarmonicOrders.setter
    def HarmonicOrders(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the HarmonicOrders.
        """
        pass

    @property
    def HDFBufferSize(self) -> typing.Optional[int]:
        """
        Gets or sets the HDFBufferSize.
        """
        return None

    @HDFBufferSize.setter
    def HDFBufferSize(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the HDFBufferSize.
        """
        pass

    @property
    def HDFCompressionLevel(self) -> typing.Optional[int]:
        """
        Gets or sets the HDFCompressionLevel.
        """
        return None

    @HDFCompressionLevel.setter
    def HDFCompressionLevel(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the HDFCompressionLevel.
        """
        pass

    @property
    def HDFNumberOfThreads(self) -> typing.Optional[int]:
        """
        Gets or sets the HDFNumberOfThreads.
        """
        return None

    @HDFNumberOfThreads.setter
    def HDFNumberOfThreads(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the HDFNumberOfThreads.
        """
        pass

    @property
    def InitialSubsteps(self) -> typing.Optional[int]:
        """
        Gets or sets the InitialSubsteps.
        """
        return None

    @InitialSubsteps.setter
    def InitialSubsteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InitialSubsteps.
        """
        pass

    @property
    def InverseOptionEndStep(self) -> typing.Optional[int]:
        """
        Gets or sets the InverseOptionEndStep.
        """
        return None

    @InverseOptionEndStep.setter
    def InverseOptionEndStep(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the InverseOptionEndStep.
        """
        pass

    @property
    def MaximumSubsteps(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumSubsteps.
        """
        return None

    @MaximumSubsteps.setter
    def MaximumSubsteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumSubsteps.
        """
        pass

    @property
    def MeshLoadStepValue(self) -> typing.Optional[int]:
        """
        Gets or sets the MeshLoadStepValue.
        """
        return None

    @MeshLoadStepValue.setter
    def MeshLoadStepValue(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MeshLoadStepValue.
        """
        pass

    @property
    def MinimumSubsteps(self) -> typing.Optional[int]:
        """
        Gets or sets the MinimumSubsteps.
        """
        return None

    @MinimumSubsteps.setter
    def MinimumSubsteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MinimumSubsteps.
        """
        pass

    @property
    def ModalNumberOfPoints(self) -> typing.Optional[int]:
        """
        Gets or sets the ModalNumberOfPoints.
        """
        return None

    @ModalNumberOfPoints.setter
    def ModalNumberOfPoints(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ModalNumberOfPoints.
        """
        pass

    @property
    def ModeSignificanceLevel(self) -> typing.Optional[float]:
        """
        Gets or sets the ModeSignificanceLevel.
        """
        return None

    @ModeSignificanceLevel.setter
    def ModeSignificanceLevel(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ModeSignificanceLevel.
        """
        pass

    @property
    def GlobalSizeRatioQualityImprovement(self) -> typing.Optional[float]:
        """
        Gets or sets the GlobalSizeRatioQualityImprovement.
        """
        return None

    @GlobalSizeRatioQualityImprovement.setter
    def GlobalSizeRatioQualityImprovement(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GlobalSizeRatioQualityImprovement.
        """
        pass

    @property
    def GlobalSizeRatioQualityRefinement(self) -> typing.Optional[float]:
        """
        Gets or sets the GlobalSizeRatioQualityRefinement.
        """
        return None

    @GlobalSizeRatioQualityRefinement.setter
    def GlobalSizeRatioQualityRefinement(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GlobalSizeRatioQualityRefinement.
        """
        pass

    @property
    def NumberOfSculptedLayersQualityImprovement(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfSculptedLayersQualityImprovement.
        """
        return None

    @NumberOfSculptedLayersQualityImprovement.setter
    def NumberOfSculptedLayersQualityImprovement(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfSculptedLayersQualityImprovement.
        """
        pass

    @property
    def NumberOfSculptedLayersRefinement(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfSculptedLayersRefinement.
        """
        return None

    @NumberOfSculptedLayersRefinement.setter
    def NumberOfSculptedLayersRefinement(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfSculptedLayersRefinement.
        """
        pass

    @property
    def RemeshingToleranceQualityImprovement(self) -> typing.Optional[float]:
        """
        Gets or sets the RemeshingToleranceQualityImprovement.
        """
        return None

    @RemeshingToleranceQualityImprovement.setter
    def RemeshingToleranceQualityImprovement(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the RemeshingToleranceQualityImprovement.
        """
        pass

    @property
    def RemeshingToleranceRefinement(self) -> typing.Optional[float]:
        """
        Gets or sets the RemeshingToleranceRefinement.
        """
        return None

    @RemeshingToleranceRefinement.setter
    def RemeshingToleranceRefinement(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the RemeshingToleranceRefinement.
        """
        pass

    @property
    def StoreResulsAtValue(self) -> typing.Optional[int]:
        """
        Gets or sets the StoreResulsAtValue.
        """
        return None

    @StoreResulsAtValue.setter
    def StoreResulsAtValue(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the StoreResulsAtValue.
        """
        pass

    @property
    def NumberOfModesToUse(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfModesToUse.
        """
        return None

    @NumberOfModesToUse.setter
    def NumberOfModesToUse(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfModesToUse.
        """
        pass

    @property
    def NumberOfRPMs(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfRPMs.
        """
        return None

    @NumberOfRPMs.setter
    def NumberOfRPMs(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfRPMs.
        """
        pass

    @property
    def NumberOfSteps(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfSteps.
        """
        return None

    @NumberOfSteps.setter
    def NumberOfSteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfSteps.
        """
        pass

    @property
    def NumberOfSubSteps(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfSubSteps.
        """
        return None

    @NumberOfSubSteps.setter
    def NumberOfSubSteps(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfSubSteps.
        """
        pass

    @property
    def NumericalDampingValue(self) -> typing.Optional[float]:
        """
        Gets or sets the NumericalDampingValue.
        """
        return None

    @NumericalDampingValue.setter
    def NumericalDampingValue(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the NumericalDampingValue.
        """
        pass

    @property
    def NumLoadVectors(self) -> typing.Optional[int]:
        """
        Gets or sets the NumLoadVectors.
        """
        return None

    @NumLoadVectors.setter
    def NumLoadVectors(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumLoadVectors.
        """
        pass

    @property
    def MaximumModesToFind(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumModesToFind.
        """
        return None

    @MaximumModesToFind.setter
    def MaximumModesToFind(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumModesToFind.
        """
        pass

    @property
    def NumberOfZones(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfZones.
        """
        return None

    @NumberOfZones.setter
    def NumberOfZones(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfZones.
        """
        pass

    @property
    def AxisymmetryDivisions(self) -> typing.Optional[int]:
        """
        Gets or sets the AxisymmetryDivisions.
        """
        return None

    @AxisymmetryDivisions.setter
    def AxisymmetryDivisions(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the AxisymmetryDivisions.
        """
        pass

    @property
    def HemicubeResolution(self) -> typing.Optional[int]:
        """
        Gets or sets the HemicubeResolution.
        """
        return None

    @HemicubeResolution.setter
    def HemicubeResolution(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the HemicubeResolution.
        """
        pass

    @property
    def FluxConvergence(self) -> typing.Optional[float]:
        """
        Gets or sets the FluxConvergence.
        """
        return None

    @FluxConvergence.setter
    def FluxConvergence(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the FluxConvergence.
        """
        pass

    @property
    def MaximumIteration(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumIteration.
        """
        return None

    @MaximumIteration.setter
    def MaximumIteration(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumIteration.
        """
        pass

    @property
    def OverRelaxation(self) -> typing.Optional[float]:
        """
        Gets or sets the OverRelaxation.
        """
        return None

    @OverRelaxation.setter
    def OverRelaxation(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the OverRelaxation.
        """
        pass

    @property
    def ReformulationTolerance(self) -> typing.Optional[float]:
        """
        Gets or sets the ReformulationTolerance.
        """
        return None

    @ReformulationTolerance.setter
    def ReformulationTolerance(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ReformulationTolerance.
        """
        pass

    @property
    def RestartAtLoadStep(self) -> typing.Optional[int]:
        """
        Gets the RestartAtLoadStep.
        """
        return None

    @property
    def RestartAtSubstep(self) -> typing.Optional[int]:
        """
        Gets the RestartAtSubstep.
        """
        return None

    @property
    def RestartAtTime(self) -> typing.Optional[float]:
        """
        Gets the RestartAtTime.
        """
        return None

    @property
    def RpmClusterNumber(self) -> typing.Optional[int]:
        """
        Gets or sets the RpmClusterNumber.
        """
        return None

    @RpmClusterNumber.setter
    def RpmClusterNumber(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the RpmClusterNumber.
        """
        pass

    @property
    def RpmSolutionIntervals(self) -> typing.Optional[int]:
        """
        Gets or sets the RpmSolutionIntervals.
        """
        return None

    @RpmSolutionIntervals.setter
    def RpmSolutionIntervals(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the RpmSolutionIntervals.
        """
        pass

    @property
    def MaximumPointsToSavePerStep(self) -> typing.Optional[int]:
        """
        Gets or sets the MaximumPointsToSavePerStep.
        """
        return None

    @MaximumPointsToSavePerStep.setter
    def MaximumPointsToSavePerStep(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the MaximumPointsToSavePerStep.
        """
        pass

    @property
    def MaximumTotalFilesToSave(self) -> typing.Optional[int]:
        """
        Gets or sets the maximum total number of restart files that can be saved.
            Applicable for manual restart points and all load steps settings. Valid range: 0 to 999. Default: 0 (sets to All).
        """
        return None

    @MaximumTotalFilesToSave.setter
    def MaximumTotalFilesToSave(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the maximum total number of restart files that can be saved.
            Applicable for manual restart points and all load steps settings. Valid range: 0 to 999. Default: 0 (sets to All).
        """
        pass

    @property
    def SaveSpecifiedLoadStep(self) -> typing.Optional[int]:
        """
        Gets or sets the SaveSpecifiedLoadStep.
        """
        return None

    @SaveSpecifiedLoadStep.setter
    def SaveSpecifiedLoadStep(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the SaveSpecifiedLoadStep.
        """
        pass

    @property
    def LoadStepValue(self) -> typing.Optional[int]:
        """
        Gets or sets the LoadStepValue.
        """
        return None

    @LoadStepValue.setter
    def LoadStepValue(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the LoadStepValue.
        """
        pass

    @property
    def SignificanceThreshold(self) -> typing.Optional[float]:
        """
        Gets or sets the SignificanceThreshold.
        """
        return None

    @SignificanceThreshold.setter
    def SignificanceThreshold(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the SignificanceThreshold.
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
    def StabilizationEnergyDissipationRatio(self) -> typing.Optional[float]:
        """
        Gets or sets the StabilizationEnergyDissipationRatio.
        """
        return None

    @StabilizationEnergyDissipationRatio.setter
    def StabilizationEnergyDissipationRatio(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StabilizationEnergyDissipationRatio.
        """
        pass

    @property
    def StabilizationForceLimit(self) -> typing.Optional[float]:
        """
        Gets or sets the StabilizationForceLimit.
        """
        return None

    @StabilizationForceLimit.setter
    def StabilizationForceLimit(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StabilizationForceLimit.
        """
        pass

    @property
    def TransientApplicationUserDefined(self) -> typing.Optional[float]:
        """
        Gets or sets the TransientApplicationUserDefined.
        """
        return None

    @TransientApplicationUserDefined.setter
    def TransientApplicationUserDefined(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the TransientApplicationUserDefined.
        """
        pass

    @property
    def SpringStiffnessFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the SpringStiffnessFactor.
        """
        return None

    @SpringStiffnessFactor.setter
    def SpringStiffnessFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the SpringStiffnessFactor.
        """
        pass

    @property
    def RelaxationTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RelaxationTemperature.
        """
        return None

    @RelaxationTemperature.setter
    def RelaxationTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RelaxationTemperature.
        """
        pass

    @property
    def Frequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Frequency.
        """
        return None

    @Frequency.setter
    def Frequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Frequency.
        """
        pass

    @property
    def CentralFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CentralFrequency.
        """
        return None

    @CentralFrequency.setter
    def CentralFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CentralFrequency.
        """
        pass

    @property
    def ChargeConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ChargeConvergenceMinimumReference.
        """
        return None

    @ChargeConvergenceMinimumReference.setter
    def ChargeConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ChargeConvergenceMinimumReference.
        """
        pass

    @property
    def ChargeConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ChargeConvergenceValue.
        """
        return None

    @ChargeConvergenceValue.setter
    def ChargeConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ChargeConvergenceValue.
        """
        pass

    @property
    def CurrentConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CurrentConvergenceMinimumReference.
        """
        return None

    @CurrentConvergenceMinimumReference.setter
    def CurrentConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CurrentConvergenceMinimumReference.
        """
        pass

    @property
    def CurrentConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CurrentConvergenceValue.
        """
        return None

    @CurrentConvergenceValue.setter
    def CurrentConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CurrentConvergenceValue.
        """
        pass

    @property
    def DisplacementConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DisplacementConvergenceMinimumReference.
        """
        return None

    @DisplacementConvergenceMinimumReference.setter
    def DisplacementConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DisplacementConvergenceMinimumReference.
        """
        pass

    @property
    def DisplacementConvergenceTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DisplacementConvergenceTolerance.
        """
        return None

    @DisplacementConvergenceTolerance.setter
    def DisplacementConvergenceTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DisplacementConvergenceTolerance.
        """
        pass

    @property
    def DisplacementConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DisplacementConvergenceValue.
        """
        return None

    @DisplacementConvergenceValue.setter
    def DisplacementConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DisplacementConvergenceValue.
        """
        pass

    @property
    def EmagAMPSConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EmagAMPSConvergenceMinimumReference.
        """
        return None

    @EmagAMPSConvergenceMinimumReference.setter
    def EmagAMPSConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EmagAMPSConvergenceMinimumReference.
        """
        pass

    @property
    def EmagAMPSConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EmagAMPSConvergenceValue.
        """
        return None

    @EmagAMPSConvergenceValue.setter
    def EmagAMPSConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EmagAMPSConvergenceValue.
        """
        pass

    @property
    def EmagCSGConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EmagCSGConvergenceMinimumReference.
        """
        return None

    @EmagCSGConvergenceMinimumReference.setter
    def EmagCSGConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EmagCSGConvergenceMinimumReference.
        """
        pass

    @property
    def EmagCSGConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EmagCSGConvergenceValue.
        """
        return None

    @EmagCSGConvergenceValue.setter
    def EmagCSGConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EmagCSGConvergenceValue.
        """
        pass

    @property
    def EnergyConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EnergyConvergenceMinimumReference.
        """
        return None

    @EnergyConvergenceMinimumReference.setter
    def EnergyConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EnergyConvergenceMinimumReference.
        """
        pass

    @property
    def EnergyConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EnergyConvergenceValue.
        """
        return None

    @EnergyConvergenceValue.setter
    def EnergyConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EnergyConvergenceValue.
        """
        pass

    @property
    def ForceConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ForceConvergenceMinimumReference.
        """
        return None

    @ForceConvergenceMinimumReference.setter
    def ForceConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ForceConvergenceMinimumReference.
        """
        pass

    @property
    def ForceConvergenceTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ForceConvergenceTolerance.
        """
        return None

    @ForceConvergenceTolerance.setter
    def ForceConvergenceTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ForceConvergenceTolerance.
        """
        pass

    @property
    def ForceConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ForceConvergenceValue.
        """
        return None

    @ForceConvergenceValue.setter
    def ForceConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ForceConvergenceValue.
        """
        pass

    @property
    def HeatConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the HeatConvergenceMinimumReference.
        """
        return None

    @HeatConvergenceMinimumReference.setter
    def HeatConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the HeatConvergenceMinimumReference.
        """
        pass

    @property
    def HeatConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the HeatConvergenceValue.
        """
        return None

    @HeatConvergenceValue.setter
    def HeatConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the HeatConvergenceValue.
        """
        pass

    @property
    def MomentConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MomentConvergenceMinimumReference.
        """
        return None

    @MomentConvergenceMinimumReference.setter
    def MomentConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MomentConvergenceMinimumReference.
        """
        pass

    @property
    def MomentConvergenceTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MomentConvergenceTolerance.
        """
        return None

    @MomentConvergenceTolerance.setter
    def MomentConvergenceTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MomentConvergenceTolerance.
        """
        pass

    @property
    def MomentConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MomentConvergenceValue.
        """
        return None

    @MomentConvergenceValue.setter
    def MomentConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MomentConvergenceValue.
        """
        pass

    @property
    def RotationConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RotationConvergenceMinimumReference.
        """
        return None

    @RotationConvergenceMinimumReference.setter
    def RotationConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RotationConvergenceMinimumReference.
        """
        pass

    @property
    def RotationConvergenceTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RotationConvergenceTolerance.
        """
        return None

    @RotationConvergenceTolerance.setter
    def RotationConvergenceTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RotationConvergenceTolerance.
        """
        pass

    @property
    def TemperatureConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TemperatureConvergenceMinimumReference.
        """
        return None

    @TemperatureConvergenceMinimumReference.setter
    def TemperatureConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TemperatureConvergenceMinimumReference.
        """
        pass

    @property
    def TemperatureConvergenceInputValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TemperatureConvergenceInputValue.
        """
        return None

    @TemperatureConvergenceInputValue.setter
    def TemperatureConvergenceInputValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TemperatureConvergenceInputValue.
        """
        pass

    @property
    def VoltageConvergenceMinimumReference(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the VoltageConvergenceMinimumReference.
        """
        return None

    @VoltageConvergenceMinimumReference.setter
    def VoltageConvergenceMinimumReference(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the VoltageConvergenceMinimumReference.
        """
        pass

    @property
    def VoltageConvergenceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the VoltageConvergenceValue.
        """
        return None

    @VoltageConvergenceValue.setter
    def VoltageConvergenceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the VoltageConvergenceValue.
        """
        pass

    @property
    def RemovalDirection(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RemovalDirection.
        """
        return None

    @RemovalDirection.setter
    def RemovalDirection(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RemovalDirection.
        """
        pass

    @property
    def RemovalStepSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RemovalStepSize.
        """
        return None

    @RemovalStepSize.setter
    def RemovalStepSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RemovalStepSize.
        """
        pass

    @property
    def StepEndTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the StepEndTime.
        """
        return None

    @StepEndTime.setter
    def StepEndTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the StepEndTime.
        """
        pass

    @property
    def MinimumElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Minimum Element Size property for Geometry Based Adaptivity.
        """
        return None

    @MinimumElementSize.setter
    def MinimumElementSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Minimum Element Size property for Geometry Based Adaptivity.
        """
        pass

    @property
    def RangeMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Range Maximum property in Options group of Analysis Settings in Harmonic Analysis.
        """
        return None

    @RangeMaximum.setter
    def RangeMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Range Maximum property in Options group of Analysis Settings in Harmonic Analysis.
        """
        pass

    @property
    def RangeMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Range Minimum property in Options group of Analysis Settings in Harmonic Analysis.
        """
        return None

    @RangeMinimum.setter
    def RangeMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Range Minimum property in Options group of Analysis Settings in Harmonic Analysis.
        """
        pass

    @property
    def KrylovSubspaceFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the KrylovSubspaceFrequency.
        """
        return None

    @KrylovSubspaceFrequency.setter
    def KrylovSubspaceFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the KrylovSubspaceFrequency.
        """
        pass

    @property
    def ModalRangeMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ModalRangeMaximum.
        """
        return None

    @ModalRangeMaximum.setter
    def ModalRangeMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ModalRangeMaximum.
        """
        pass

    @property
    def ModalRangeMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ModalRangeMinimum.
        """
        return None

    @ModalRangeMinimum.setter
    def ModalRangeMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ModalRangeMinimum.
        """
        pass

    @property
    def InitialTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the InitialTimeStep.
        """
        return None

    @InitialTimeStep.setter
    def InitialTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the InitialTimeStep.
        """
        pass

    @property
    def SearchRangeMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Range Maximum property in Options group of Analysis Settings in Modal Analysis.
        """
        return None

    @SearchRangeMaximum.setter
    def SearchRangeMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Range Maximum property in Options group of Analysis Settings in Modal Analysis.
        """
        pass

    @property
    def MaximumTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MaximumTimeStep.
        """
        return None

    @MaximumTimeStep.setter
    def MaximumTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MaximumTimeStep.
        """
        pass

    @property
    def SearchRangeMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Range Minimum property in Options group of Analysis Settings in Modal Analysis.
        """
        return None

    @SearchRangeMinimum.setter
    def SearchRangeMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Range Minimum property in Options group of Analysis Settings in Modal Analysis.
        """
        pass

    @property
    def MinimumTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the MinimumTimeStep.
        """
        return None

    @MinimumTimeStep.setter
    def MinimumTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the MinimumTimeStep.
        """
        pass

    @property
    def BoundaryAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BoundaryAngle.
        """
        return None

    @BoundaryAngle.setter
    def BoundaryAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BoundaryAngle.
        """
        pass

    @property
    def EdgeSplittingAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the EdgeSplittingAngle.
        """
        return None

    @EdgeSplittingAngle.setter
    def EdgeSplittingAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the EdgeSplittingAngle.
        """
        pass

    @property
    def SolverTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SolverTolerance.
        """
        return None

    @SolverTolerance.setter
    def SolverTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SolverTolerance.
        """
        pass

    @property
    def RpmValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RpmValue.
        """
        return None

    @RpmValue.setter
    def RpmValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RpmValue.
        """
        pass

    @property
    def RpmCentralFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RpmCentralFrequency.
        """
        return None

    @RpmCentralFrequency.setter
    def RpmCentralFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RpmCentralFrequency.
        """
        pass

    @property
    def RpmRangeMaximum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RpmRangeMaximum.
        """
        return None

    @RpmRangeMaximum.setter
    def RpmRangeMaximum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RpmRangeMaximum.
        """
        pass

    @property
    def RpmRangeMinimum(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RpmRangeMinimum.
        """
        return None

    @RpmRangeMinimum.setter
    def RpmRangeMinimum(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RpmRangeMinimum.
        """
        pass

    @property
    def TimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the TimeStep.
        """
        return None

    @TimeStep.setter
    def TimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the TimeStep.
        """
        pass

    @property
    def SpringStiffnessValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SpringStiffnessValue.
        """
        return None

    @SpringStiffnessValue.setter
    def SpringStiffnessValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SpringStiffnessValue.
        """
        pass

    @property
    def BaseRemovalType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMBaseRemovalType]:
        """
        Gets or sets the BaseRemovalType.
        """
        return None

    @BaseRemovalType.setter
    def BaseRemovalType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMBaseRemovalType]) -> None:
        """
        Gets or sets the BaseRemovalType.
        """
        pass

    @property
    def StiffnessCoefficientDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DampingType]:
        """
        Gets or sets the StiffnessCoefficientDefineBy.
        """
        return None

    @StiffnessCoefficientDefineBy.setter
    def StiffnessCoefficientDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DampingType]) -> None:
        """
        Gets or sets the StiffnessCoefficientDefineBy.
        """
        pass

    @property
    def CacheResultsInMemory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CacheResultsInMemory]:
        """
        Gets or sets the CacheResultsInMemory.
        """
        return None

    @CacheResultsInMemory.setter
    def CacheResultsInMemory(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CacheResultsInMemory]) -> None:
        """
        Gets or sets the CacheResultsInMemory.
        """
        pass

    @property
    def ParticipationFactor(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CalculateParticipationFactorResult]:
        """
        Gets or sets the ParticipationFactor.
        """
        return None

    @ParticipationFactor.setter
    def ParticipationFactor(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CalculateParticipationFactorResult]) -> None:
        """
        Gets or sets the ParticipationFactor.
        """
        pass

    @property
    def StoreResultsAt(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimePointsOptions]:
        """
        Gets or sets the StoreResultsAt.
        """
        return None

    @StoreResultsAt.setter
    def StoreResultsAt(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimePointsOptions]) -> None:
        """
        Gets or sets the StoreResultsAt.
        """
        pass

    @property
    def ConstantDamping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConstantDampingType]:
        """
        Gets or sets the ConstantDamping.
        """
        return None

    @ConstantDamping.setter
    def ConstantDamping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConstantDampingType]) -> None:
        """
        Gets or sets the ConstantDamping.
        """
        pass

    @property
    def ContactSplit(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSplitType]:
        """
        Gets or sets the ContactSplit.
        """
        return None

    @ContactSplit.setter
    def ContactSplit(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSplitType]) -> None:
        """
        Gets or sets the ContactSplit.
        """
        pass

    @property
    def ContactSummary(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSummaryType]:
        """
        Gets or sets the ContactSummary.
        """
        return None

    @ContactSummary.setter
    def ContactSummary(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ContactSummaryType]) -> None:
        """
        Gets or sets the ContactSummary.
        """
        pass

    @property
    def ChargeConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the ChargeConvergence.
        """
        return None

    @ChargeConvergence.setter
    def ChargeConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the ChargeConvergence.
        """
        pass

    @property
    def CurrentConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the CurrentConvergence.
        """
        return None

    @CurrentConvergence.setter
    def CurrentConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the CurrentConvergence.
        """
        pass

    @property
    def DisplacementConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the DisplacementConvergence.
        """
        return None

    @DisplacementConvergence.setter
    def DisplacementConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the DisplacementConvergence.
        """
        pass

    @property
    def AMPSConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the AMPSConvergence.
        """
        return None

    @AMPSConvergence.setter
    def AMPSConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the AMPSConvergence.
        """
        pass

    @property
    def CSGConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the CSGConvergence.
        """
        return None

    @CSGConvergence.setter
    def CSGConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the CSGConvergence.
        """
        pass

    @property
    def EnergyConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the EnergyConvergence.
        """
        return None

    @EnergyConvergence.setter
    def EnergyConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the EnergyConvergence.
        """
        pass

    @property
    def ForceConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the ForceConvergence.
        """
        return None

    @ForceConvergence.setter
    def ForceConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the ForceConvergence.
        """
        pass

    @property
    def HeatConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the HeatConvergence.
        """
        return None

    @HeatConvergence.setter
    def HeatConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the HeatConvergence.
        """
        pass

    @property
    def MomentConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the MomentConvergence.
        """
        return None

    @MomentConvergence.setter
    def MomentConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the MomentConvergence.
        """
        pass

    @property
    def RotationConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the RotationConvergence.
        """
        return None

    @RotationConvergence.setter
    def RotationConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the RotationConvergence.
        """
        pass

    @property
    def TemperatureConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the TemperatureConvergence.
        """
        return None

    @TemperatureConvergence.setter
    def TemperatureConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the TemperatureConvergence.
        """
        pass

    @property
    def TemperatureConvergenceValue(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NonLinearValueType]:
        """
        Gets or sets the TemperatureConvergenceValue.
        """
        return None

    @TemperatureConvergenceValue.setter
    def TemperatureConvergenceValue(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NonLinearValueType]) -> None:
        """
        Gets or sets the TemperatureConvergenceValue.
        """
        pass

    @property
    def VoltageConvergence(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]:
        """
        Gets or sets the VoltageConvergence.
        """
        return None

    @VoltageConvergence.setter
    def VoltageConvergence(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType]) -> None:
        """
        Gets or sets the VoltageConvergence.
        """
        pass

    @property
    def CoriolisEffectApplied(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CoriolisEffectType]:
        """
        Gets or sets the CoriolisEffectApplied.
        """
        return None

    @CoriolisEffectApplied.setter
    def CoriolisEffectApplied(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CoriolisEffectType]) -> None:
        """
        Gets or sets the CoriolisEffectApplied.
        """
        pass

    @property
    def CreepEffects(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Creep]:
        """
        Gets or sets the CreepEffects.
        """
        return None

    @CreepEffects.setter
    def CreepEffects(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Creep]) -> None:
        """
        Gets or sets the CreepEffects.
        """
        pass

    @property
    def HarmonicIndexRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CyclicHarmonicIndex]:
        """
        Gets or sets the HarmonicIndexRange.
        """
        return None

    @HarmonicIndexRange.setter
    def HarmonicIndexRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CyclicHarmonicIndex]) -> None:
        """
        Gets or sets the HarmonicIndexRange.
        """
        pass

    @property
    def DampingDefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DampingDefineBy]:
        """
        Gets or sets the DampingDefineBy.
        """
        return None

    @DampingDefineBy.setter
    def DampingDefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DampingDefineBy]) -> None:
        """
        Gets or sets the DampingDefineBy.
        """
        pass

    @property
    def FarFieldRadiationSurface(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FarFieldRadiationSurfaceType]:
        """
        Gets or sets the FarFieldRadiationSurface.
        """
        return None

    @FarFieldRadiationSurface.setter
    def FarFieldRadiationSurface(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FarFieldRadiationSurfaceType]) -> None:
        """
        Gets or sets the FarFieldRadiationSurface.
        """
        pass

    @property
    def ExpandResultsFrom(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExpandResultFrom]:
        """
        Gets or sets the ExpandResultsFrom.
        """
        return None

    @ExpandResultsFrom.setter
    def ExpandResultsFrom(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ExpandResultFrom]) -> None:
        """
        Gets or sets the ExpandResultsFrom.
        """
        pass

    @property
    def FrequencySpacing(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FrequencySpacingType]:
        """
        Gets or sets the FrequencySpacing.
        """
        return None

    @FrequencySpacing.setter
    def FrequencySpacing(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FrequencySpacingType]) -> None:
        """
        Gets or sets the FrequencySpacing.
        """
        pass

    @property
    def FutureAnalysis(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FutureIntentType]:
        """
        Gets or sets the FutureAnalysis.
        """
        return None

    @FutureAnalysis.setter
    def FutureAnalysis(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FutureIntentType]) -> None:
        """
        Gets or sets the FutureAnalysis.
        """
        pass

    @property
    def GeneralMiscellaneousOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GeneralMiscellaneousOptionType]:
        """
        Gets or sets the GeneralMiscellaneousOption.
        """
        return None

    @GeneralMiscellaneousOption.setter
    def GeneralMiscellaneousOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GeneralMiscellaneousOptionType]) -> None:
        """
        Gets or sets the GeneralMiscellaneousOption.
        """
        pass

    @property
    def MultistepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMultiStepType]:
        """
        Gets or sets the MultistepType.
        """
        return None

    @MultistepType.setter
    def MultistepType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMultiStepType]) -> None:
        """
        Gets or sets the MultistepType.
        """
        pass

    @property
    def ModalFrequencyRange(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModalFrequencyRangeType]:
        """
        Gets or sets the ModalFrequencyRange.
        """
        return None

    @ModalFrequencyRange.setter
    def ModalFrequencyRange(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModalFrequencyRangeType]) -> None:
        """
        Gets or sets the ModalFrequencyRange.
        """
        pass

    @property
    def StoreResultsAtAllFrequencies(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMSUPStorage]:
        """
        Gets or sets the StoreResultsAtAllFrequencies.
        """
        return None

    @StoreResultsAtAllFrequencies.setter
    def StoreResultsAtAllFrequencies(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMSUPStorage]) -> None:
        """
        Gets or sets the StoreResultsAtAllFrequencies.
        """
        pass

    @property
    def SolutionMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMethod]:
        """
        Gets or sets the SolutionMethod.
        """
        return None

    @SolutionMethod.setter
    def SolutionMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.HarmonicMethod]) -> None:
        """
        Gets or sets the SolutionMethod.
        """
        pass

    @property
    def HDFCompression(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.HDFCompressionType]:
        """
        Gets or sets the HDFCompression.
        """
        return None

    @HDFCompression.setter
    def HDFCompression(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.HDFCompressionType]) -> None:
        """
        Gets or sets the HDFCompression.
        """
        pass

    @property
    def IncludeNegativeLoadMultiplier(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverControlsIncludeNegativeLoadMultiplier]:
        """
        Gets or sets the IncludeNegativeLoadMultiplier.
        """
        return None

    @IncludeNegativeLoadMultiplier.setter
    def IncludeNegativeLoadMultiplier(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverControlsIncludeNegativeLoadMultiplier]) -> None:
        """
        Gets or sets the IncludeNegativeLoadMultiplier.
        """
        pass

    @property
    def LineSearch(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LineSearchType]:
        """
        Gets or sets the LineSearch.
        """
        return None

    @LineSearch.setter
    def LineSearch(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LineSearchType]) -> None:
        """
        Gets or sets the LineSearch.
        """
        pass

    @property
    def GenerateMeshRestartPoints(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartControlsType]:
        """
        Gets or sets the GenerateMeshRestartPoints.
        """
        return None

    @GenerateMeshRestartPoints.setter
    def GenerateMeshRestartPoints(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartControlsType]) -> None:
        """
        Gets or sets the GenerateMeshRestartPoints.
        """
        pass

    @property
    def MeshRetainFilesAfterFullSolve(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartRetainFilesType]:
        """
        Gets or sets the MeshRetainFilesAfterFullSolve.
        """
        return None

    @MeshRetainFilesAfterFullSolve.setter
    def MeshRetainFilesAfterFullSolve(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartRetainFilesType]) -> None:
        """
        Gets or sets the MeshRetainFilesAfterFullSolve.
        """
        pass

    @property
    def MeshSaveAtLoadStep(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartSaveAtLoadStep]:
        """
        Gets or sets the MeshSaveAtLoadStep.
        """
        return None

    @MeshSaveAtLoadStep.setter
    def MeshSaveAtLoadStep(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartSaveAtLoadStep]) -> None:
        """
        Gets or sets the MeshSaveAtLoadStep.
        """
        pass

    @property
    def MeshSaveAtSubstep(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartSaveAtSubstep]:
        """
        Gets or sets the MeshSaveAtSubstep.
        """
        return None

    @MeshSaveAtSubstep.setter
    def MeshSaveAtSubstep(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MeshRestartSaveAtSubstep]) -> None:
        """
        Gets or sets the MeshSaveAtSubstep.
        """
        pass

    @property
    def ModeReuse(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverControlsModeReuse]:
        """
        Gets or sets the ModeReuse.
        """
        return None

    @ModeReuse.setter
    def ModeReuse(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverControlsModeReuse]) -> None:
        """
        Gets or sets the ModeReuse.
        """
        pass

    @property
    def ModesCombinationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModesCombinationType]:
        """
        Gets or sets the ModesCombinationType.
        """
        return None

    @ModesCombinationType.setter
    def ModesCombinationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModesCombinationType]) -> None:
        """
        Gets or sets the ModesCombinationType.
        """
        pass

    @property
    def ModeSelectionMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModeSelectionMethod]:
        """
        Gets or sets the ModeSelectionMethod.
        """
        return None

    @ModeSelectionMethod.setter
    def ModeSelectionMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModeSelectionMethod]) -> None:
        """
        Gets or sets the ModeSelectionMethod.
        """
        pass

    @property
    def OnDemandExpansionOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.OnDemandExpansionType]:
        """
        Gets or sets the OnDemandExpansionOption.
        """
        return None

    @OnDemandExpansionOption.setter
    def OnDemandExpansionOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.OnDemandExpansionType]) -> None:
        """
        Gets or sets the OnDemandExpansionOption.
        """
        pass

    @property
    def NewtonRaphsonOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NewtonRaphsonType]:
        """
        Gets or sets the NewtonRaphsonOption.
        """
        return None

    @NewtonRaphsonOption.setter
    def NewtonRaphsonOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NewtonRaphsonType]) -> None:
        """
        Gets or sets the NewtonRaphsonOption.
        """
        pass

    @property
    def NodalForces(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.OutputControlsNodalForcesType]:
        """
        Gets or sets the NodalForces.
        """
        return None

    @NodalForces.setter
    def NodalForces(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.OutputControlsNodalForcesType]) -> None:
        """
        Gets or sets the NodalForces.
        """
        pass

    @property
    def ProjectToGeometry(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NLADControlProjectToGeometry]:
        """
        Gets or sets the ProjectToGeometry.
        """
        return None

    @ProjectToGeometry.setter
    def ProjectToGeometry(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NLADControlProjectToGeometry]) -> None:
        """
        Gets or sets the ProjectToGeometry.
        """
        pass

    @property
    def RefinementAlgorithm(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NonlinearAdaptivityControlsRefinementAlgorithmType]:
        """
        Gets or sets the RefinementAlgorithm.
        """
        return None

    @RefinementAlgorithm.setter
    def RefinementAlgorithm(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NonlinearAdaptivityControlsRefinementAlgorithmType]) -> None:
        """
        Gets or sets the RefinementAlgorithm.
        """
        pass

    @property
    def RemeshingGradient(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NonlinearAdaptivityControlsRemeshingGradientType]:
        """
        Gets or sets the RemeshingGradient.
        """
        return None

    @RemeshingGradient.setter
    def RemeshingGradient(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NonlinearAdaptivityControlsRemeshingGradientType]) -> None:
        """
        Gets or sets the RemeshingGradient.
        """
        pass

    @property
    def NonLinearFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NonLinearFormulationType]:
        """
        Gets or sets the NonLinearFormulation.
        """
        return None

    @NonLinearFormulation.setter
    def NonLinearFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NonLinearFormulationType]) -> None:
        """
        Gets or sets the NonLinearFormulation.
        """
        pass

    @property
    def NumericalDamping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TransientDampingType]:
        """
        Gets or sets the NumericalDamping.
        """
        return None

    @NumericalDamping.setter
    def NumericalDamping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TransientDampingType]) -> None:
        """
        Gets or sets the NumericalDamping.
        """
        pass

    @property
    def Expansion(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ExpandResultsSubType]:
        """
        Gets the Expansion.
        """
        return None

    @property
    def ViewFactorMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RadiosityViewFactorType]:
        """
        Gets or sets the ViewFactorMethod.
        """
        return None

    @ViewFactorMethod.setter
    def ViewFactorMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RadiosityViewFactorType]) -> None:
        """
        Gets or sets the ViewFactorMethod.
        """
        pass

    @property
    def RadiositySolver(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RadiositySolverType]:
        """
        Gets or sets the RadiositySolver.
        """
        return None

    @RadiositySolver.setter
    def RadiositySolver(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RadiositySolverType]) -> None:
        """
        Gets or sets the RadiositySolver.
        """
        pass

    @property
    def CombineRestartFiles(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.CombineRestartFilesType]:
        """
        Gets or sets the CombineRestartFiles.
        """
        return None

    @CombineRestartFiles.setter
    def CombineRestartFiles(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.CombineRestartFilesType]) -> None:
        """
        Gets or sets the CombineRestartFiles.
        """
        pass

    @property
    def GenerateRestartPoints(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartControlsType]:
        """
        Gets or sets the GenerateRestartPoints.
        """
        return None

    @GenerateRestartPoints.setter
    def GenerateRestartPoints(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartControlsType]) -> None:
        """
        Gets or sets the GenerateRestartPoints.
        """
        pass

    @property
    def RetainFilesAfterFullSolve(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartRetainFilesType]:
        """
        Gets or sets the RetainFilesAfterFullSolve.
        """
        return None

    @RetainFilesAfterFullSolve.setter
    def RetainFilesAfterFullSolve(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartRetainFilesType]) -> None:
        """
        Gets or sets the RetainFilesAfterFullSolve.
        """
        pass

    @property
    def RestartType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartType]:
        """
        Gets or sets the RestartType.
        """
        return None

    @RestartType.setter
    def RestartType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartType]) -> None:
        """
        Gets or sets the RestartType.
        """
        pass

    @property
    def ResultFileCompression(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileCompressionType]:
        """
        Gets or sets the ResultFileCompression.
        """
        return None

    @ResultFileCompression.setter
    def ResultFileCompression(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileCompressionType]) -> None:
        """
        Gets or sets the ResultFileCompression.
        """
        pass

    @property
    def ResultFileFormat(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileFormatType]:
        """
        Gets or sets the ResultFileFormat.
        """
        return None

    @ResultFileFormat.setter
    def ResultFileFormat(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultFileFormatType]) -> None:
        """
        Gets or sets the ResultFileFormat.
        """
        pass

    @property
    def RpmFrequencySpacing(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.FrequencySpacingType]:
        """
        Gets or sets the RpmFrequencySpacing.
        """
        return None

    @RpmFrequencySpacing.setter
    def RpmFrequencySpacing(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.FrequencySpacingType]) -> None:
        """
        Gets or sets the RpmFrequencySpacing.
        """
        pass

    @property
    def SaveAtLoadStep(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartSaveAtLoadStep]:
        """
        Gets or sets the SaveAtLoadStep.
        """
        return None

    @SaveAtLoadStep.setter
    def SaveAtLoadStep(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartSaveAtLoadStep]) -> None:
        """
        Gets or sets the SaveAtLoadStep.
        """
        pass

    @property
    def SaveAtSubstep(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartSaveAtSubstep]:
        """
        Gets or sets the SaveAtSubstep.
        """
        return None

    @SaveAtSubstep.setter
    def SaveAtSubstep(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RestartSaveAtSubstep]) -> None:
        """
        Gets or sets the SaveAtSubstep.
        """
        pass

    @property
    def ScatteredFieldFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ScatteredFieldFormulation]:
        """
        Gets or sets the ScatteredFieldFormulation.
        """
        return None

    @ScatteredFieldFormulation.setter
    def ScatteredFieldFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ScatteredFieldFormulation]) -> None:
        """
        Gets or sets the ScatteredFieldFormulation.
        """
        pass

    @property
    def ScatteringOutputType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ScatteringOutputType]:
        """
        Gets or sets the ScatteringOutputType.
        """
        return None

    @ScatteringOutputType.setter
    def ScatteringOutputType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ScatteringOutputType]) -> None:
        """
        Gets or sets the ScatteringOutputType.
        """
        pass

    @property
    def SolverUnitSystem(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the SolverUnitSystem.
        """
        return None

    @SolverUnitSystem.setter
    def SolverUnitSystem(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the SolverUnitSystem.
        """
        pass

    @property
    def SolverPivotChecking(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverPivotChecking]:
        """
        Gets or sets the SolverPivotChecking.
        """
        return None

    @SolverPivotChecking.setter
    def SolverPivotChecking(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverPivotChecking]) -> None:
        """
        Gets or sets the SolverPivotChecking.
        """
        pass

    @property
    def SolverType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverType]:
        """
        Gets or sets the SolverType.
        """
        return None

    @SolverType.setter
    def SolverType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverType]) -> None:
        """
        Gets or sets the SolverType.
        """
        pass

    @property
    def SolverUnits(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverUnitsControlType]:
        """
        Gets or sets the SolverUnits.
        """
        return None

    @SolverUnits.setter
    def SolverUnits(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SolverUnitsControlType]) -> None:
        """
        Gets or sets the SolverUnits.
        """
        pass

    @property
    def SpectrumType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpectrumType]:
        """
        Gets or sets the SpectrumType.
        """
        return None

    @SpectrumType.setter
    def SpectrumType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpectrumType]) -> None:
        """
        Gets or sets the SpectrumType.
        """
        pass

    @property
    def Stabilization(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationType]:
        """
        Gets or sets the Stabilization.
        """
        return None

    @Stabilization.setter
    def Stabilization(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationType]) -> None:
        """
        Gets or sets the Stabilization.
        """
        pass

    @property
    def StabilizationActivationForFirstSubstep(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationFirstSubstepOption]:
        """
        Gets or sets the StabilizationActivationForFirstSubstep.
        """
        return None

    @StabilizationActivationForFirstSubstep.setter
    def StabilizationActivationForFirstSubstep(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationFirstSubstepOption]) -> None:
        """
        Gets or sets the StabilizationActivationForFirstSubstep.
        """
        pass

    @property
    def StabilizationMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationMethod]:
        """
        Gets or sets the StabilizationMethod.
        """
        return None

    @StabilizationMethod.setter
    def StabilizationMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StabilizationMethod]) -> None:
        """
        Gets or sets the StabilizationMethod.
        """
        pass

    @property
    def StoreModalResults(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.StoreModalResult]:
        """
        Gets or sets the StoreModalResults.
        """
        return None

    @StoreModalResults.setter
    def StoreModalResults(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.StoreModalResult]) -> None:
        """
        Gets or sets the StoreModalResults.
        """
        pass

    @property
    def DefineBy(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeStepDefineByType]:
        """
        Gets or sets the DefineBy.
        """
        return None

    @DefineBy.setter
    def DefineBy(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TimeStepDefineByType]) -> None:
        """
        Gets or sets the DefineBy.
        """
        pass

    @property
    def TransientApplication(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.TransientApplicationType]:
        """
        Gets or sets the TransientApplication.
        """
        return None

    @TransientApplication.setter
    def TransientApplication(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.TransientApplicationType]) -> None:
        """
        Gets or sets the TransientApplication.
        """
        pass

    @property
    def UpdateViewFactor(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.UpdateViewFactor]:
        """
        Gets or sets the specification for updating the view factor.
        """
        return None

    @UpdateViewFactor.setter
    def UpdateViewFactor(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.UpdateViewFactor]) -> None:
        """
        Gets or sets the specification for updating the view factor.
        """
        pass

    @property
    def AutomaticTimeStepping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping]:
        """
        Gets or sets the AutomaticTimeStepping.
        """
        return None

    @AutomaticTimeStepping.setter
    def AutomaticTimeStepping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping]) -> None:
        """
        Gets or sets the AutomaticTimeStepping.
        """
        pass

    @property
    def RetainModesymFileAfterSolve(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.UseExistingModesymFile]:
        """
        Gets or sets the RetainModesymFileAfterSolve.
        """
        return None

    @RetainModesymFileAfterSolve.setter
    def RetainModesymFileAfterSolve(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.UseExistingModesymFile]) -> None:
        """
        Gets or sets the RetainModesymFileAfterSolve.
        """
        pass

    @property
    def WeakSprings(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WeakSpringsType]:
        """
        Gets or sets the WeakSprings.
        """
        return None

    @WeakSprings.setter
    def WeakSprings(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WeakSpringsType]) -> None:
        """
        Gets or sets the WeakSprings.
        """
        pass

    @property
    def SpringStiffness(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringsStiffnessType]:
        """
        Gets or sets the SpringStiffness.
        """
        return None

    @SpringStiffness.setter
    def SpringStiffness(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SpringsStiffnessType]) -> None:
        """
        Gets or sets the SpringStiffness.
        """
        pass

    @property
    def IgnoreAcousticDamping(self) -> typing.Optional[bool]:
        """
        Gets or sets the IgnoreAcousticDamping.
        """
        return None

    @IgnoreAcousticDamping.setter
    def IgnoreAcousticDamping(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the IgnoreAcousticDamping.
        """
        pass

    @property
    def CalculateAcceleration(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateAcceleration.
        """
        return None

    @CalculateAcceleration.setter
    def CalculateAcceleration(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateAcceleration.
        """
        pass

    @property
    def BackStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the BackStress.
        """
        return None

    @BackStress.setter
    def BackStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the BackStress.
        """
        pass

    @property
    def ContactMiscellaneous(self) -> typing.Optional[bool]:
        """
        Gets or sets the ContactMiscellaneous.
        """
        return None

    @ContactMiscellaneous.setter
    def ContactMiscellaneous(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ContactMiscellaneous.
        """
        pass

    @property
    def CStarIntegral(self) -> typing.Optional[bool]:
        """
        Gets or sets the CStarIntegral.
        """
        return None

    @CStarIntegral.setter
    def CStarIntegral(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CStarIntegral.
        """
        pass

    @property
    def ElementCurrentDensity(self) -> typing.Optional[bool]:
        """
        Gets or sets the ElementCurrentDensity.
        """
        return None

    @ElementCurrentDensity.setter
    def ElementCurrentDensity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ElementCurrentDensity.
        """
        pass

    @property
    def FieldIntensityandFluxDensity(self) -> typing.Optional[bool]:
        """
        Gets or sets the FieldIntensityandFluxDensity.
        """
        return None

    @FieldIntensityandFluxDensity.setter
    def FieldIntensityandFluxDensity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FieldIntensityandFluxDensity.
        """
        pass

    @property
    def ElectromagneticNodalForces(self) -> typing.Optional[bool]:
        """
        Gets or sets the ElectromagneticNodalForces.
        """
        return None

    @ElectromagneticNodalForces.setter
    def ElectromagneticNodalForces(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ElectromagneticNodalForces.
        """
        pass

    @property
    def ContactData(self) -> typing.Optional[bool]:
        """
        Gets or sets the ContactData.
        """
        return None

    @ContactData.setter
    def ContactData(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ContactData.
        """
        pass

    @property
    def CalculateVolumeEnergy(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateVolumeEnergy.
        """
        return None

    @CalculateVolumeEnergy.setter
    def CalculateVolumeEnergy(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateVolumeEnergy.
        """
        pass

    @property
    def NonlinearData(self) -> typing.Optional[bool]:
        """
        Gets or sets the NonlinearData.
        """
        return None

    @NonlinearData.setter
    def NonlinearData(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the NonlinearData.
        """
        pass

    @property
    def CalculateEnergy(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateEnergy.
        """
        return None

    @CalculateEnergy.setter
    def CalculateEnergy(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateEnergy.
        """
        pass

    @property
    def CalculateEulerAngles(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateEulerAngles.
        """
        return None

    @CalculateEulerAngles.setter
    def CalculateEulerAngles(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateEulerAngles.
        """
        pass

    @property
    def HeatGenerationRate(self) -> typing.Optional[bool]:
        """
        Gets or sets the HeatGenerationRate.
        """
        return None

    @HeatGenerationRate.setter
    def HeatGenerationRate(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the HeatGenerationRate.
        """
        pass

    @property
    def JIntegral(self) -> typing.Optional[bool]:
        """
        Gets or sets the JIntegral.
        """
        return None

    @JIntegral.setter
    def JIntegral(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the JIntegral.
        """
        pass

    @property
    def MaterialForce(self) -> typing.Optional[bool]:
        """
        Gets or sets the MaterialForce.
        """
        return None

    @MaterialForce.setter
    def MaterialForce(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the MaterialForce.
        """
        pass

    @property
    def CalculateReactions(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateReactions.
        """
        return None

    @CalculateReactions.setter
    def CalculateReactions(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateReactions.
        """
        pass

    @property
    def SIFS(self) -> typing.Optional[bool]:
        """
        Gets or sets the SIFS.
        """
        return None

    @SIFS.setter
    def SIFS(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SIFS.
        """
        pass

    @property
    def Strain(self) -> typing.Optional[bool]:
        """
        Gets or sets the Strain.
        """
        return None

    @Strain.setter
    def Strain(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Strain.
        """
        pass

    @property
    def Stress(self) -> typing.Optional[bool]:
        """
        Gets or sets the Stress.
        """
        return None

    @Stress.setter
    def Stress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Stress.
        """
        pass

    @property
    def CalculateThermalFlux(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateThermalFlux.
        """
        return None

    @CalculateThermalFlux.setter
    def CalculateThermalFlux(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateThermalFlux.
        """
        pass

    @property
    def TStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the TStress.
        """
        return None

    @TStress.setter
    def TStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the TStress.
        """
        pass

    @property
    def CalculateVelocity(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateVelocity.
        """
        return None

    @CalculateVelocity.setter
    def CalculateVelocity(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateVelocity.
        """
        pass

    @property
    def CalculateVelocityAndAcceleration(self) -> typing.Optional[bool]:
        """
        Gets or sets the CalculateVelocityAndAcceleration.
        """
        return None

    @CalculateVelocityAndAcceleration.setter
    def CalculateVelocityAndAcceleration(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CalculateVelocityAndAcceleration.
        """
        pass

    @property
    def CampbellDiagram(self) -> typing.Optional[bool]:
        """
        Gets or sets the CampbellDiagram.
        """
        return None

    @CampbellDiagram.setter
    def CampbellDiagram(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CampbellDiagram.
        """
        pass

    @property
    def CarryOverTimeStep(self) -> typing.Optional[bool]:
        """
        Gets or sets the CarryOverTimeStep.
        """
        return None

    @CarryOverTimeStep.setter
    def CarryOverTimeStep(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CarryOverTimeStep.
        """
        pass

    @property
    def DeleteUnneededFiles(self) -> typing.Optional[bool]:
        """
        Gets or sets the DeleteUnneededFiles.
        """
        return None

    @DeleteUnneededFiles.setter
    def DeleteUnneededFiles(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DeleteUnneededFiles.
        """
        pass

    @property
    def CyclicModeSuperposition(self) -> typing.Optional[bool]:
        """
        Gets or sets the CyclicModeSuperposition.
        """
        return None

    @CyclicModeSuperposition.setter
    def CyclicModeSuperposition(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the CyclicModeSuperposition.
        """
        pass

    @property
    def Damped(self) -> typing.Optional[bool]:
        """
        Gets or sets the Damped.
        """
        return None

    @Damped.setter
    def Damped(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Damped.
        """
        pass

    @property
    def EqvDampingRatioFromModal(self) -> typing.Optional[bool]:
        """
        Gets or sets the EqvDampingRatioFromModal.
        """
        return None

    @EqvDampingRatioFromModal.setter
    def EqvDampingRatioFromModal(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the EqvDampingRatioFromModal.
        """
        pass

    @property
    def ExcludeInsignificantModes(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExcludeInsignificantModes.
        """
        return None

    @ExcludeInsignificantModes.setter
    def ExcludeInsignificantModes(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExcludeInsignificantModes.
        """
        pass

    @property
    def ExportHighStrains(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExportHighStrains.
        """
        return None

    @ExportHighStrains.setter
    def ExportHighStrains(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExportHighStrains.
        """
        pass

    @property
    def ExportLayerEndTemperature(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExportLayerEndTemperature.
        """
        return None

    @ExportLayerEndTemperature.setter
    def ExportLayerEndTemperature(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExportLayerEndTemperature.
        """
        pass

    @property
    def ExportRecoaterInterference(self) -> typing.Optional[bool]:
        """
        Gets or sets the ExportRecoaterInterference.
        """
        return None

    @ExportRecoaterInterference.setter
    def ExportRecoaterInterference(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ExportRecoaterInterference.
        """
        pass

    @property
    def ExportShrinkline(self) -> typing.Optional[bool]:
        """
        Gets or sets the specification for exporting the AM Shrinkline Result.
        """
        return None

    @ExportShrinkline.setter
    def ExportShrinkline(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the specification for exporting the AM Shrinkline Result.
        """
        pass

    @property
    def FractureSolverControls(self) -> typing.Optional[bool]:
        """
        Gets or sets the FractureSolverControls.
        """
        return None

    @FractureSolverControls.setter
    def FractureSolverControls(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FractureSolverControls.
        """
        pass

    @property
    def GeneralMiscellaneous(self) -> typing.Optional[bool]:
        """
        Gets or sets the GeneralMiscellaneous.
        """
        return None

    @GeneralMiscellaneous.setter
    def GeneralMiscellaneous(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GeneralMiscellaneous.
        """
        pass

    @property
    def ClusterResults(self) -> typing.Optional[bool]:
        """
        Gets or sets the ClusterResults.
        """
        return None

    @ClusterResults.setter
    def ClusterResults(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ClusterResults.
        """
        pass

    @property
    def UserDefinedFrequencies(self) -> typing.Optional[bool]:
        """
        Gets or sets the UserDefinedFrequencies.
        """
        return None

    @UserDefinedFrequencies.setter
    def UserDefinedFrequencies(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UserDefinedFrequencies.
        """
        pass

    @property
    def Multistep(self) -> typing.Optional[bool]:
        """
        Gets or sets the Multistep.
        """
        return None

    @Multistep.setter
    def Multistep(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Multistep.
        """
        pass

    @property
    def IncludeResidualVector(self) -> typing.Optional[bool]:
        """
        Gets or sets the IncludeResidualVector.
        """
        return None

    @IncludeResidualVector.setter
    def IncludeResidualVector(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the IncludeResidualVector.
        """
        pass

    @property
    def InverseOption(self) -> typing.Optional[bool]:
        """
        Gets or sets the InverseOption.
        """
        return None

    @InverseOption.setter
    def InverseOption(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the InverseOption.
        """
        pass

    @property
    def KeepModalResults(self) -> typing.Optional[bool]:
        """
        Gets or sets the KeepModalResults.
        """
        return None

    @KeepModalResults.setter
    def KeepModalResults(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the KeepModalResults.
        """
        pass

    @property
    def KeepPreStressLoadPattern(self) -> typing.Optional[bool]:
        """
        Gets or sets the KeepPreStressLoadPattern.
        """
        return None

    @KeepPreStressLoadPattern.setter
    def KeepPreStressLoadPattern(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the KeepPreStressLoadPattern.
        """
        pass

    @property
    def NonLinearSolution(self) -> typing.Optional[bool]:
        """
        Gets the NonLinearSolution.
        """
        return None

    @property
    def QuasiStaticSolution(self) -> typing.Optional[bool]:
        """
        Gets or sets the QuasiStaticSolution.
        """
        return None

    @QuasiStaticSolution.setter
    def QuasiStaticSolution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the QuasiStaticSolution.
        """
        pass

    @property
    def LimitSearchToRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the LimitSearchToRange.
        """
        return None

    @LimitSearchToRange.setter
    def LimitSearchToRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the LimitSearchToRange.
        """
        pass

    @property
    def SaveMAPDLDB(self) -> typing.Optional[bool]:
        """
        Gets or sets the SaveMAPDLDB.
        """
        return None

    @SaveMAPDLDB.setter
    def SaveMAPDLDB(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SaveMAPDLDB.
        """
        pass

    @property
    def StoreComplexSolution(self) -> typing.Optional[bool]:
        """
        Gets or sets the StoreComplexSolution.
        """
        return None

    @StoreComplexSolution.setter
    def StoreComplexSolution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the StoreComplexSolution.
        """
        pass

    @property
    def InertiaRelief(self) -> typing.Optional[bool]:
        """
        Gets or sets the InertiaRelief.
        """
        return None

    @InertiaRelief.setter
    def InertiaRelief(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the InertiaRelief.
        """
        pass

    @property
    def LargeDeflection(self) -> typing.Optional[bool]:
        """
        Gets or sets the LargeDeflection.
        """
        return None

    @LargeDeflection.setter
    def LargeDeflection(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the LargeDeflection.
        """
        pass

    @property
    def TimeIntegration(self) -> typing.Optional[bool]:
        """
        Gets or sets the TimeIntegration.
        """
        return None

    @TimeIntegration.setter
    def TimeIntegration(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the TimeIntegration.
        """
        pass

    @property
    def ElectricOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ElectricOnly.
        """
        return None

    @ElectricOnly.setter
    def ElectricOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ElectricOnly.
        """
        pass

    @property
    def StructuralOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the StructuralOnly.
        """
        return None

    @StructuralOnly.setter
    def StructuralOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the StructuralOnly.
        """
        pass

    @property
    def ThermalOnly(self) -> typing.Optional[bool]:
        """
        Gets or sets the ThermalOnly.
        """
        return None

    @ThermalOnly.setter
    def ThermalOnly(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ThermalOnly.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def Graph(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnalysisSettingsGraph]:
        """
        Graph property.
        """
        return None

    @property
    def SurfaceStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the SurfaceStress.
        """
        return None

    @SurfaceStress.setter
    def SurfaceStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SurfaceStress.
        """
        pass

    @property
    def ScratchSolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the ScratchSolverFilesDirectory.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the SolverFilesDirectory.
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

    def GetAPIName(self, dispId: int) -> str:
        """
        GetAPIName method.
        """
        pass

    def GetStepEndTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Step End Time at a given solution step.
            
        """
        pass

    def SetStepEndTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Step End Time for a given solution step.
            
        """
        pass

    def GetAutomaticTimeStepping(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping:
        """
        
            Gets the Automatic Time Stepping at a given solution step.
            
        """
        pass

    def GetAffectedSteps(self) -> typing.List[int]:
        """
        GetAffectedSteps method.
        """
        pass

    def SetAutomaticTimeStepping(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping) -> None:
        """
        
            Sets the Automatic Time Stepping for a given solution step.
            
        """
        pass

    def GetForceConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Force Convergence Tolerance Type at a given solution step.
            
        """
        pass

    def SetForceConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Force Convergence Tolerance Type for a given solution step.
            
        """
        pass

    def GetForceConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Force Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def SetForceConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Force Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def GetForceConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Force Convergence Value at a given solution step.
            
        """
        pass

    def SetForceConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Force Convergence Value for a given solution step.
            
        """
        pass

    def GetForceConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Force Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def SetForceConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Force Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def GetMomentConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Moment Convergence Tolerance type at a given solution step.
            
        """
        pass

    def SetMomentConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Moment Convergence Tolerance type for a given solution step.
            
        """
        pass

    def GetMomentConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Moment Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def SetMomentConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Moment Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def GetMomentConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Moment Convergence Value at a given solution step.
            
        """
        pass

    def SetMomentConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Moment Convergence Value for a given solution step.
            
        """
        pass

    def GetMomentConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Moment Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def SetMomentConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Moment Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def GetDisplacementConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Displacement Convergence Tolerance type at a given solution step.
            
        """
        pass

    def SetDisplacementConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Displacement Convergence Tolerance type for a given solution step.
            
        """
        pass

    def GetDisplacementConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Displacement Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def SetDisplacementConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Displacement Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def GetDisplacementConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Displacement Convergence Value at a given solution step.
            
        """
        pass

    def SetDisplacementConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Displacement Convergence Value for a given solution step.
            
        """
        pass

    def GetDisplacementConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Displacement Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def SetDisplacementConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Displacement Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def GetRotationConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Rotation Convergence Tolerance type at a given solution step.
            
        """
        pass

    def SetRotationConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Rotation Convergence Tolerance type for a given solution step.
            
        """
        pass

    def GetRotationConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Rotation Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def SetRotationConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Rotation Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def GetRotationConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Rotation Convergence Value at a given solution step.
            
        """
        pass

    def SetRotationConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Rotation Convergence Value for a given solution step.
            
        """
        pass

    def GetRotationConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Rotation Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def SetRotationConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Rotation Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetTemperatureConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Temperature Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetTemperatureConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Temperature Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetTemperatureConvergenceValue(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.NonLinearValueType) -> None:
        """
        
            Sets the Temperature Convergence Value for a given solution step.
            
        """
        pass

    def SetTemperatureConvergenceInputValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Temperature Convergence Input Value for a given solution step.
            
        """
        pass

    def SetTemperatureConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Temperature Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetHeatConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Heat Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetHeatConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Heat Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetHeatConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Heat Convergence Value for a given solution step.
            
        """
        pass

    def SetHeatConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Heat Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetVoltageConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Voltage Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetVoltageConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Voltage Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetVoltageConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Voltage Convergence Value for a given solution step.
            
        """
        pass

    def SetVoltageConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Voltage Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetChargeConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Charge Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetChargeConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Charge Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetChargeConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Charge Convergence Value for a given solution step.
            
        """
        pass

    def SetChargeConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Charge Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetEnergyConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Energy Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetEnergyConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Energy Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetEnergyConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Energy Convergence Value for a given solution step.
            
        """
        pass

    def SetEnergyConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Energy Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetCurrentConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the Current Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetCurrentConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Current Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetCurrentConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Current Convergence Value for a given solution step.
            
        """
        pass

    def SetCurrentConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Current Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetEmagAMPSConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the EmagAMPS Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetEmagAMPSConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the EmagAMPS Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetEmagAMPSConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the EmagAMPS Convergence Value for a given solution step.
            
        """
        pass

    def SetEmagAMPSConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the EmagAMPS Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def SetEmagCSGConvergenceType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType) -> None:
        """
        
            Sets the EmagCSG Convergence Tolerance type for a given solution step.
            
        """
        pass

    def SetEmagCSGConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the EmagCSG Convergence Tolerance as a percentage for a given solution step.
            For example if the user input is 5% then the "value" argument should be set to 5.
            
        """
        pass

    def SetEmagCSGConvergenceValue(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the EmagCSG Convergence Value for a given solution step.
            
        """
        pass

    def SetEmagCSGConvergenceMinimumReference(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the EmagCSG Convergence Minimum Reference for a given solution step.
            
        """
        pass

    def GetTemperatureConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Temperature Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetTemperatureConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Temperature Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetTemperatureConvergenceValue(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.NonLinearValueType:
        """
        
            Gets the Temperature Convergence Value at a given solution step.
            
        """
        pass

    def GetTemperatureConvergenceInputValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Temperature Convergence Input Value at a given solution step.
            
        """
        pass

    def GetTemperatureConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Temperature Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetHeatConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Heat Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetHeatConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Heat Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetHeatConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Heat Convergence Value at a given solution step.
            
        """
        pass

    def GetHeatConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Heat Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetVoltageConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Voltage Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetVoltageConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Voltage Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetVoltageConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Voltage Convergence Value at a given solution step.
            
        """
        pass

    def GetVoltageConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Voltage Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetCurrentConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Current Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetCurrentConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Current Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetCurrentConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Current Convergence Value at a given solution step.
            
        """
        pass

    def GetCurrentConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Current Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetEmagAMPSConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the EmagAMPS Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetEmagAMPSConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the EmagAMPS Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetEmagAMPSConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the EmagAMPS Convergence Value at a given solution step.
            
        """
        pass

    def GetEmagAMPSConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the EmagAMPS Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetEmagCSGConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the EmagCSG Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetEmagCSGConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the EmagCSG Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetEmagCSGConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the EmagCSG Convergence Value at a given solution step.
            
        """
        pass

    def GetEmagCSGConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the EmagCSG Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetEnergyConvergenceType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.ConvergenceToleranceType:
        """
        
            Gets the Energy Convergence Tolerance type at a given solution step.
            
        """
        pass

    def GetEnergyConvergenceTolerance(self, stepNumber: int) -> float:
        """
        
            Gets the Energy Convergence Tolerance as a percentage at a given solution step.
            
        """
        pass

    def GetEnergyConvergenceValue(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Energy Convergence Value at a given solution step.
            
        """
        pass

    def GetEnergyConvergenceMinimumReference(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Energy Convergence Minimum Reference at a given solution step.
            
        """
        pass

    def GetLineSearch(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.LineSearchType:
        """
        
            Gets the Line Search at a given solution step.
            
        """
        pass

    def SetLineSearch(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.LineSearchType) -> None:
        """
        
            Sets the Line Search for a given solution step.
            
        """
        pass

    def GetStabilization(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.StabilizationType:
        """
        
            Gets the Stabilization at a given solution step.
            
        """
        pass

    def SetStabilization(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.StabilizationType) -> None:
        """
        
            Sets the Stabilization for a given solution step.
            
        """
        pass

    def GetStabilizationMethod(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.StabilizationMethod:
        """
        
            Gets the Stabilization Method at a given solution step.
            
        """
        pass

    def SetStabilizationMethod(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.StabilizationMethod) -> None:
        """
        
            Sets the Stabilization Method for a given solution step.
            
        """
        pass

    def GetStabilizationEnergyDissipationRatio(self, stepNumber: int) -> float:
        """
        
            Gets the Stabilization Energy Dissipation Ratio at a given solution step.
            
        """
        pass

    def SetStabilizationEnergyDissipationRatio(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Stabilization Energy Dissipation Ratio for a given solution step.
            
        """
        pass

    def GetStabilizationDampingFactor(self, stepNumber: int) -> float:
        """
        
            Gets the Stabilization Damping Factor at a given solution step.
            
        """
        pass

    def SetStabilizationDampingFactor(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Stabilization Damping Factor for a given solution step.
            
        """
        pass

    def GetStabilizationFirstSubstepOption(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.StabilizationFirstSubstepOption:
        """
        
            Gets the Stabilization First Substep Option at a given solution step.
            
        """
        pass

    def SetStabilizationFirstSubstepOption(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.StabilizationFirstSubstepOption) -> None:
        """
        
            Sets the Stabilization First Substep Option for a given solution step.
            
        """
        pass

    def GetStabilizationForceLimit(self, stepNumber: int) -> float:
        """
        
            Gets the Stabilization Force Limit at a given solution step.
            
        """
        pass

    def SetStabilizationForceLimit(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Stabilization Force Limit for a given solution step.
            
        """
        pass

    def GetStoreResultsAt(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.TimePointsOptions:
        """
        
            Gets the Store Results At at a given solution step.
            
        """
        pass

    def SetStoreResultsAt(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.TimePointsOptions) -> None:
        """
        
            Sets the Store Results At for a given solution step.
            
        """
        pass

    def GetStoreResulsAtValue(self, stepNumber: int) -> int:
        """
        
            Gets the Store Results At Value at a given solution step.
            
        """
        pass

    def SetStoreResulsAtValue(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Store Results At Value for a given solution step.
            
        """
        pass

    def GetDefineBy(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.TimeStepDefineByType:
        """
        
            Gets the Define By at a given solution step.
            
        """
        pass

    def SetDefineBy(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.TimeStepDefineByType) -> None:
        """
        
            Sets the Define By for a given solution step.
            
        """
        pass

    def GetCarryOverTimeStep(self, stepNumber: int) -> bool:
        """
        
            Gets the Carry Over Time Step at a given solution step.
            
        """
        pass

    def SetCarryOverTimeStep(self, stepNumber: int, value: bool) -> None:
        """
        
            Sets the Carry Over Time Step for a given solution step.
            
        """
        pass

    def GetInitialTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Initial Time Step at a given solution step.
            
        """
        pass

    def SetInitialTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Initial Time Step for a given solution step.
            
        """
        pass

    def GetMinimumTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Minimum Time Step at a given solution step.
            
        """
        pass

    def SetMinimumTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Minimum Time Step for a given solution step.
            
        """
        pass

    def GetMaximumTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Maximum Time Step at a given solution step.
            
        """
        pass

    def SetMaximumTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Maximum Time Step for a given solution step.
            
        """
        pass

    def GetInitialSubsteps(self, stepNumber: int) -> int:
        """
        
            Gets the Initial Substeps at a given solution step.
            
        """
        pass

    def SetInitialSubsteps(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Initial Substeps for a given solution step.
            
        """
        pass

    def GetMinimumSubsteps(self, stepNumber: int) -> int:
        """
        
            Gets the Minimum Substeps at a given solution step.
            
        """
        pass

    def SetMinimumSubsteps(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Minimum Substeps for a given solution step.
            
        """
        pass

    def GetMaximumSubsteps(self, stepNumber: int) -> int:
        """
        
            Gets the Maximum Substeps at a given solution step.
            
        """
        pass

    def SetMaximumSubsteps(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Maximum Substeps for a given solution step.
            
        """
        pass

    def GetMaximumIterationsPerSubstep(self, stepNumber: int) -> int:
        """
        
            Gets the Maximum Iterations Per Substep at a given solution step. Special values are: '-1' to specify that one iteration is forced per substep and '0' to specify Program Controlled.
            
        """
        pass

    def SetMaximumIterationsPerSubstep(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Maximum Iterations Per Substep for a given solution step. Default: 0 (Program Controlled). Valid range is greater than or equal to -1, where -1 forces one iteration per substep. An exception will be thrown for invalid values.
            
        """
        pass

    def SetNumberOfSubSteps(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Number of Substeps for a given solution step.
            
        """
        pass

    def GetNumberOfSubSteps(self, stepNumber: int) -> int:
        """
        
            Gets the Number of Substeps for a given solution step.
            
        """
        pass

    def SetTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Time Step for a given solution step.
            
        """
        pass

    def GetTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Sets the Time Step for a given solution step.
            
        """
        pass

    def SetTimeIntegration(self, stepNumber: int, value: bool) -> None:
        """
        
            Sets the TimeIntegration for a given solution step.
            
        """
        pass

    def SetStructuralOnly(self, stepNumber: int, value: bool) -> None:
        """
        
            Sets the TimeIntegration Structural for a given solution step.
            
        """
        pass

    def SetThermalOnly(self, stepNumber: int, value: bool) -> None:
        """
        
            Sets the TimeIntegration Thermal for a given solution step.
            
        """
        pass

    def GetTimeIntegration(self, stepNumber: int) -> bool:
        """
        
            Gets the TimeIntegration for a given solution step.
            
        """
        pass

    def GetStructuralOnly(self, stepNumber: int) -> bool:
        """
        
            Gets the TimeIntegration Structural for a given solution step.
            
        """
        pass

    def GetThermalOnly(self, stepNumber: int) -> bool:
        """
        
            Sets the TimeIntegration Thermal for a given solution step.
            
        """
        pass

    def GetStepName(self, stepNumber: int) -> str:
        """
        Gets the Step name at a given step.
        """
        pass

    def SetStepName(self, stepNumber: int, value: str) -> None:
        """
        Sets the Step name at a given step.
        """
        pass

    def GetAMStepType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.AMProcessStepType:
        """
        Gets the AM Process Step Type at a given step.
        """
        pass

    def CopyTo(self, other: Ansys.ACT.Automation.Mechanical.DataModelObject) -> None:
        """
        CopyTo method.
        """
        pass

    def SetCreepEffects(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.Creep) -> None:
        """
        
            Sets the Creep Effects for a given solution step.
            
        """
        pass

    def GetCreepEffects(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.Creep:
        """
        
            Gets the Creep Effects for a given solution step.
            
        """
        pass

    def SetCreepLimitRatio(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Creep Limit Ratio for a given solution step.
            
        """
        pass

    def GetCreepLimitRatio(self, stepNumber: int) -> float:
        """
        
            Gets the Creep Limit Ratio for a given solution step.
            
        """
        pass

    def PerformSplitFrequencyRange(self) -> None:
        """
        
            Split the user-defined frequencies into multiple step harmonic analysis
            
        """
        pass

    def DeleteAllRestartPoints(self) -> None:
        """
        DeleteAllRestartPoints method.
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


class EXDAnalysisSettings(object):
    """
    
            Defines Analysis Settings for Explicit Dynamics System.
            Note: Cycles in the UI are referred to as TimeSteps in API
            
    """

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        
            Gets the Internal Object. For advanced usage only.
            
        """
        return None

    @property
    def PreferenceType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDPreferenceType]:
        """
        
            Gets or sets the PreferenceType
            
        """
        return None

    @PreferenceType.setter
    def PreferenceType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDPreferenceType]) -> None:
        """
        
            Gets or sets the PreferenceType
            
        """
        pass

    @property
    def NumberOfSteps(self) -> typing.Optional[int]:
        """
        
            Gets or sets the NumberOfSteps.
            
        """
        return None

    @NumberOfSteps.setter
    def NumberOfSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the NumberOfSteps.
            
        """
        pass

    @property
    def CurrentStepNumber(self) -> typing.Optional[int]:
        """
        
            Gets or sets the CurrentStepNumber.
            
        """
        return None

    @CurrentStepNumber.setter
    def CurrentStepNumber(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the CurrentStepNumber.
            
        """
        pass

    @property
    def ResumeFromTimeStep(self) -> typing.Optional[int]:
        """
        
            Gets or sets the ResumeFromCycle.
             
        """
        return None

    @ResumeFromTimeStep.setter
    def ResumeFromTimeStep(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the ResumeFromCycle.
             
        """
        pass

    @property
    def MaximumTimeSteps(self) -> typing.Optional[int]:
        """
        
            Gets or sets the MaximumNumberofCycles.
             
        """
        return None

    @MaximumTimeSteps.setter
    def MaximumTimeSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the MaximumNumberofCycles.
             
        """
        pass

    @property
    def MaximumEnergyError(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  MaximumEnergyError.
             
        """
        return None

    @MaximumEnergyError.setter
    def MaximumEnergyError(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  MaximumEnergyError.
             
        """
        pass

    @property
    def ReferenceEnergyTimeStep(self) -> typing.Optional[int]:
        """
        
            Gets or sets the ReferenceEnergyCycle.
             
        """
        return None

    @ReferenceEnergyTimeStep.setter
    def ReferenceEnergyTimeStep(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the ReferenceEnergyCycle.
             
        """
        pass

    @property
    def InitialTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the InitialTimeStep.
             
        """
        return None

    @InitialTimeStep.setter
    def InitialTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the InitialTimeStep.
             
        """
        pass

    @property
    def MinimumTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the MinimumTimeStep.
             
        """
        return None

    @MinimumTimeStep.setter
    def MinimumTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the MinimumTimeStep.
             
        """
        pass

    @property
    def MaximumTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the MaximumTimeStep.
             
        """
        return None

    @MaximumTimeStep.setter
    def MaximumTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the MaximumTimeStep.
             
        """
        pass

    @property
    def TimeStepSafetyFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  TimeStepSafetyFactor.
             
        """
        return None

    @TimeStepSafetyFactor.setter
    def TimeStepSafetyFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  TimeStepSafetyFactor.
             
        """
        pass

    @property
    def CharZoneDimensionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDCharZoneDimensionType]:
        """
        
            Gets or sets the  CharZoneDimensionType.
             
        """
        return None

    @CharZoneDimensionType.setter
    def CharZoneDimensionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDCharZoneDimensionType]) -> None:
        """
        
            Gets or sets the  CharZoneDimensionType.
             
        """
        pass

    @property
    def StepawareMassScalingType(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets the Step aware Mass Scaling Controls.
             
        """
        return None

    @StepawareMassScalingType.setter
    def StepawareMassScalingType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets the Step aware Mass Scaling Controls.
             
        """
        pass

    @property
    def AutomaticMassScalingType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the  AutomaticMassScaling.
             
        """
        return None

    @AutomaticMassScalingType.setter
    def AutomaticMassScalingType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the  AutomaticMassScaling.
             
        """
        pass

    @property
    def MassScalingMinTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  MassScalingMinTimeStep.
             
        """
        return None

    @MassScalingMinTimeStep.setter
    def MassScalingMinTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  MassScalingMinTimeStep.
             
        """
        pass

    @property
    def MassScalingMaxElem(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  MassScalingMaxElem.
             
        """
        return None

    @MassScalingMaxElem.setter
    def MassScalingMaxElem(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  MassScalingMaxElem.
             
        """
        pass

    @property
    def MassScalingMaxPart(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  MassScalingMaxPart.
             
        """
        return None

    @MassScalingMaxPart.setter
    def MassScalingMaxPart(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  MassScalingMaxPart.
             
        """
        pass

    @property
    def MassScalingUpdateFreq(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  MassScalingUpdateFreq.
             
        """
        return None

    @MassScalingUpdateFreq.setter
    def MassScalingUpdateFreq(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  MassScalingUpdateFreq.
             
        """
        pass

    @property
    def SolverPrecisionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSolverPrecisionType]:
        """
        
            Gets or sets the  SolverPrecisionType.
             
        """
        return None

    @SolverPrecisionType.setter
    def SolverPrecisionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSolverPrecisionType]) -> None:
        """
        
            Gets or sets the  SolverPrecisionType.
             
        """
        pass

    @property
    def SolveUnits(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSolveUnitsType]:
        """
        
            Gets or sets the  SolveUnits.
             
        """
        return None

    @SolveUnits.setter
    def SolveUnits(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSolveUnitsType]) -> None:
        """
        
            Gets or sets the  SolveUnits.
             
        """
        pass

    @property
    def BeamSolutionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDBeamSolutionType]:
        """
        
            Gets or sets the  BeamSolutionType.
             
        """
        return None

    @BeamSolutionType.setter
    def BeamSolutionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDBeamSolutionType]) -> None:
        """
        
            Gets or sets the  BeamSolutionType.
             
        """
        pass

    @property
    def BeamTimeStepSafetyFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  BeamTimeStepSafetyFactor.
             
        """
        return None

    @BeamTimeStepSafetyFactor.setter
    def BeamTimeStepSafetyFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  BeamTimeStepSafetyFactor.
             
        """
        pass

    @property
    def HexIntegrationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDHexIntegrationType]:
        """
        
            Gets or sets the  HexIntegrationType.
             
        """
        return None

    @HexIntegrationType.setter
    def HexIntegrationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDHexIntegrationType]) -> None:
        """
        
            Gets or sets the  HexIntegrationType.
             
        """
        pass

    @property
    def ShellSublayers(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  ShellSublayers.
             
        """
        return None

    @ShellSublayers.setter
    def ShellSublayers(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  ShellSublayers.
             
        """
        pass

    @property
    def ShellShearCorrectionFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  ShellShearCorrectionFactor.
             
        """
        return None

    @ShellShearCorrectionFactor.setter
    def ShellShearCorrectionFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  ShellShearCorrectionFactor.
             
        """
        pass

    @property
    def ShellWarpCorrection(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the  ShellWarpCorrection.
             
        """
        return None

    @ShellWarpCorrection.setter
    def ShellWarpCorrection(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the  ShellWarpCorrection.
             
        """
        pass

    @property
    def ShellThicknessUpdateType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDShellThicknessUpdateType]:
        """
        
            Gets or sets the  ShellThicknessUpdateType.
             
        """
        return None

    @ShellThicknessUpdateType.setter
    def ShellThicknessUpdateType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDShellThicknessUpdateType]) -> None:
        """
        
            Gets or sets the  ShellThicknessUpdateType.
             
        """
        pass

    @property
    def PusoCoefficient(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  PusoCoefficient.
             
        """
        return None

    @PusoCoefficient.setter
    def PusoCoefficient(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  PusoCoefficient.
             
        """
        pass

    @property
    def TetPressureIntegrationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDTetPressureIntegrationType]:
        """
        
            Gets or sets the  TetIntegrationType.
             
        """
        return None

    @TetPressureIntegrationType.setter
    def TetPressureIntegrationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDTetPressureIntegrationType]) -> None:
        """
        
            Gets or sets the  TetIntegrationType.
             
        """
        pass

    @property
    def ShellInertiaUpdateType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDShellInertiaUpdateType]:
        """
        
            Gets or sets the  ShellInertiaUpdateType.
             
        """
        return None

    @ShellInertiaUpdateType.setter
    def ShellInertiaUpdateType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDShellInertiaUpdateType]) -> None:
        """
        
            Gets or sets the  ShellInertiaUpdateType.
             
        """
        pass

    @property
    def DensityUpdateType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDDensityUpdateType]:
        """
        
            Gets or sets the  DensityUpdateType.
             
        """
        return None

    @DensityUpdateType.setter
    def DensityUpdateType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDDensityUpdateType]) -> None:
        """
        
            Gets or sets the  DensityUpdateType.
             
        """
        pass

    @property
    def SphMinTimeStep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  Minimum Timestep for SPH.
             
        """
        return None

    @SphMinTimeStep.setter
    def SphMinTimeStep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  Minimum Timestep for SPH.
             
        """
        pass

    @property
    def SPHMinDensityFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  Minimum Density Factor for SPH.
             
        """
        return None

    @SPHMinDensityFactor.setter
    def SPHMinDensityFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  Minimum Density Factor for SPH.
             
        """
        pass

    @property
    def SPHMaxDensityFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  Maximum Density Factor for SPH.
             
        """
        return None

    @SPHMaxDensityFactor.setter
    def SPHMaxDensityFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  Maximum Density Factor for SPH.
             
        """
        pass

    @property
    def SPHNodeDensityCutoffOption(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSPHNodeDensityCutoffOption]:
        """
        
            Gets or sets the  SPHNodeDensityCutoffOption.
             
        """
        return None

    @SPHNodeDensityCutoffOption.setter
    def SPHNodeDensityCutoffOption(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSPHNodeDensityCutoffOption]) -> None:
        """
        
            Gets or sets the  SPHNodeDensityCutoffOption.
             
        """
        pass

    @property
    def DetonationBurnType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDDetonationBurnType]:
        """
        
            Gets or sets the  DetonationBurnType.
             
        """
        return None

    @DetonationBurnType.setter
    def DetonationBurnType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDDetonationBurnType]) -> None:
        """
        
            Gets or sets the  DetonationBurnType.
             
        """
        pass

    @property
    def MinimumVelocity(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  MinimumVelocity.
             
        """
        return None

    @MinimumVelocity.setter
    def MinimumVelocity(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  MinimumVelocity.
             
        """
        pass

    @property
    def MaximumVelocity(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  MaximumVelocity.
             
        """
        return None

    @MaximumVelocity.setter
    def MaximumVelocity(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  MaximumVelocity.
             
        """
        pass

    @property
    def RadiusCutoff(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  RadiusCutoff.
             
        """
        return None

    @RadiusCutoff.setter
    def RadiusCutoff(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  RadiusCutoff.
             
        """
        pass

    @property
    def MinimumStrainCutOff(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  MinimumStrainCutOff.
             
        """
        return None

    @MinimumStrainCutOff.setter
    def MinimumStrainCutOff(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  MinimumStrainCutOff.
             
        """
        pass

    @property
    def EulerSizeDefType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerSizeDefType]:
        """
        
            Gets or sets the  EulerSizeDefType.
             
        """
        return None

    @EulerSizeDefType.setter
    def EulerSizeDefType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerSizeDefType]) -> None:
        """
        
            Gets or sets the  EulerSizeDefType.
             
        """
        pass

    @property
    def EulerDomainType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerDomainType]:
        """
        
            Gets or sets the  EulerDomainType.
             
        """
        return None

    @EulerDomainType.setter
    def EulerDomainType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerDomainType]) -> None:
        """
        
            Gets or sets the  EulerDomainType.
             
        """
        pass

    @property
    def EulerDisplayBox(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the  EulerDisplayBox.
             
        """
        return None

    @EulerDisplayBox.setter
    def EulerDisplayBox(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the  EulerDisplayBox.
             
        """
        pass

    @property
    def EulerDomScopeDefType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerDomScopeDefType]:
        """
        
            Gets or sets the  EulerDomScopeDefType.
             
        """
        return None

    @EulerDomScopeDefType.setter
    def EulerDomScopeDefType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerDomScopeDefType]) -> None:
        """
        
            Gets or sets the  EulerDomScopeDefType.
             
        """
        pass

    @property
    def EulerXScaleFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  EulerXScaleFactor.
             
        """
        return None

    @EulerXScaleFactor.setter
    def EulerXScaleFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  EulerXScaleFactor.
             
        """
        pass

    @property
    def EulerYScaleFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  EulerYScaleFactor.
             
        """
        return None

    @EulerYScaleFactor.setter
    def EulerYScaleFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  EulerYScaleFactor.
             
        """
        pass

    @property
    def EulerZScaleFactor(self) -> typing.Optional[float]:
        """
        
            Gets or sets the  EulerZScaleFactor.
             
        """
        return None

    @EulerZScaleFactor.setter
    def EulerZScaleFactor(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the  EulerZScaleFactor.
             
        """
        pass

    @property
    def EulerXOrigin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerXOrigin.
             
        """
        return None

    @EulerXOrigin.setter
    def EulerXOrigin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerXOrigin.
             
        """
        pass

    @property
    def EulerYOrigin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerYOrigin.
             
        """
        return None

    @EulerYOrigin.setter
    def EulerYOrigin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerYOrigin.
             
        """
        pass

    @property
    def EulerZOrigin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerZOrigin.
             
        """
        return None

    @EulerZOrigin.setter
    def EulerZOrigin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerZOrigin.
             
        """
        pass

    @property
    def EulerXDim(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerXDim.
             
        """
        return None

    @EulerXDim.setter
    def EulerXDim(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerXDim.
             
        """
        pass

    @property
    def EulerYDim(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerYDim.
             
        """
        return None

    @EulerYDim.setter
    def EulerYDim(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerYDim.
             
        """
        pass

    @property
    def EulerZDim(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerZDim.
             
        """
        return None

    @EulerZDim.setter
    def EulerZDim(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerZDim.
             
        """
        pass

    @property
    def EulerResolutionDefType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerResolutionDefType]:
        """
        
            Gets or sets the  EulerResolutionDefType.
             
        """
        return None

    @EulerResolutionDefType.setter
    def EulerResolutionDefType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerResolutionDefType]) -> None:
        """
        
            Gets or sets the  EulerResolutionDefType.
             
        """
        pass

    @property
    def EulerGradedDefinition(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerGradedDefinition]:
        """
        
            Gets or sets the  EulerGradedDefinition.
             
        """
        return None

    @EulerGradedDefinition.setter
    def EulerGradedDefinition(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerGradedDefinition]) -> None:
        """
        
            Gets or sets the  EulerGradedDefinition.
             
        """
        pass

    @property
    def EulerGradeIncrement(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerGradeIncrement.
             
        """
        return None

    @EulerGradeIncrement.setter
    def EulerGradeIncrement(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerGradeIncrement.
             
        """
        pass

    @property
    def EulerGradeNumberOfTimes(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerGradeNumberOfTimes.
             
        """
        return None

    @EulerGradeNumberOfTimes.setter
    def EulerGradeNumberOfTimes(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerGradeNumberOfTimes.
             
        """
        pass

    @property
    def EulerCellSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerCellSize.
             
        """
        return None

    @EulerCellSize.setter
    def EulerCellSize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerCellSize.
             
        """
        pass

    @property
    def EulerTotalCells(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerTotalCells.
             
        """
        return None

    @EulerTotalCells.setter
    def EulerTotalCells(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerTotalCells.
             
        """
        pass

    @property
    def EulerXZones(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerXZones.
             
        """
        return None

    @EulerXZones.setter
    def EulerXZones(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerXZones.
             
        """
        pass

    @property
    def EulerYZones(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerYZones.
             
        """
        return None

    @EulerYZones.setter
    def EulerYZones(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerYZones.
             
        """
        pass

    @property
    def EulerZZones(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerZZones.
             
        """
        return None

    @EulerZZones.setter
    def EulerZZones(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerZZones.
             
        """
        pass

    @property
    def EulerBoundLowerX(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundLowerX.
             
        """
        return None

    @EulerBoundLowerX.setter
    def EulerBoundLowerX(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundLowerX.
             
        """
        pass

    @property
    def EulerBoundLowerY(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundLowerY.
             
        """
        return None

    @EulerBoundLowerY.setter
    def EulerBoundLowerY(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundLowerY.
             
        """
        pass

    @property
    def EulerBoundLowerZ(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundLowerZ.
             
        """
        return None

    @EulerBoundLowerZ.setter
    def EulerBoundLowerZ(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundLowerZ.
             
        """
        pass

    @property
    def EulerBoundUpperX(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundUpperX.
             
        """
        return None

    @EulerBoundUpperX.setter
    def EulerBoundUpperX(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundUpperX.
             
        """
        pass

    @property
    def EulerBoundUpperY(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundUpperY.
             
        """
        return None

    @EulerBoundUpperY.setter
    def EulerBoundUpperY(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundUpperY.
             
        """
        pass

    @property
    def EulerBoundUpperZ(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]:
        """
        
            Gets or sets the  EulerBoundUpperZ.
             
        """
        return None

    @EulerBoundUpperZ.setter
    def EulerBoundUpperZ(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerBoundaryDefType]) -> None:
        """
        
            Gets or sets the  EulerBoundUpperZ.
             
        """
        pass

    @property
    def EulerTrackType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDEulerTrackType]:
        """
        
            Gets the  EulerTrackType.
             
        """
        return None

    @property
    def EulerPropertyXmin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyXmin.
             
        """
        return None

    @EulerPropertyXmin.setter
    def EulerPropertyXmin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyXmin.
             
        """
        pass

    @property
    def EulerPropertyYmin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyYmin.
             
        """
        return None

    @EulerPropertyYmin.setter
    def EulerPropertyYmin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyYmin.
             
        """
        pass

    @property
    def EulerPropertyZmin(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyZmin.
             
        """
        return None

    @EulerPropertyZmin.setter
    def EulerPropertyZmin(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyZmin.
             
        """
        pass

    @property
    def EulerPropertyXsize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyXsize.
             
        """
        return None

    @EulerPropertyXsize.setter
    def EulerPropertyXsize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyXsize.
             
        """
        pass

    @property
    def EulerPropertyYsize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyYsize.
             
        """
        return None

    @EulerPropertyYsize.setter
    def EulerPropertyYsize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyYsize.
             
        """
        pass

    @property
    def EulerPropertyZsize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the  EulerPropertyZsize.
             
        """
        return None

    @EulerPropertyZsize.setter
    def EulerPropertyZsize(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the  EulerPropertyZsize.
             
        """
        pass

    @property
    def EulerPropertyXres(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerPropertyXres.
             
        """
        return None

    @EulerPropertyXres.setter
    def EulerPropertyXres(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerPropertyXres.
             
        """
        pass

    @property
    def EulerPropertyYres(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerPropertyYres.
             
        """
        return None

    @EulerPropertyYres.setter
    def EulerPropertyYres(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerPropertyYres.
             
        """
        pass

    @property
    def EulerPropertyZres(self) -> typing.Optional[int]:
        """
        
            Gets or sets the  EulerPropertyZres.
             
        """
        return None

    @EulerPropertyZres.setter
    def EulerPropertyZres(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the  EulerPropertyZres.
             
        """
        pass

    @property
    def EulerPropertyDisplayBox(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the  EulerPropertyDisplayBox.
             
        """
        return None

    @EulerPropertyDisplayBox.setter
    def EulerPropertyDisplayBox(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the  EulerPropertyDisplayBox.
             
        """
        pass

    @property
    def LinearArtificialViscosity(self) -> typing.Optional[float]:
        """
        
            Gets or sets the LinearArtificialViscosity.
            
        """
        return None

    @LinearArtificialViscosity.setter
    def LinearArtificialViscosity(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the LinearArtificialViscosity.
            
        """
        pass

    @property
    def QuadraticArtificialViscosity(self) -> typing.Optional[float]:
        """
        
            Gets or sets the QuadraticArtificialViscosity.
            
        """
        return None

    @QuadraticArtificialViscosity.setter
    def QuadraticArtificialViscosity(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the QuadraticArtificialViscosity.
            
        """
        pass

    @property
    def LinearViscosityExpansionType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the LinearViscosityExpansionType.
            
        """
        return None

    @LinearViscosityExpansionType.setter
    def LinearViscosityExpansionType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the LinearViscosityExpansionType.
            
        """
        pass

    @property
    def ArtificialViscosityForShellsType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the ArtificialViscosityForShellsType.
            
        """
        return None

    @ArtificialViscosityForShellsType.setter
    def ArtificialViscosityForShellsType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the ArtificialViscosityForShellsType.
            
        """
        pass

    @property
    def LinearViscositySPH(self) -> typing.Optional[float]:
        """
        
            Gets or sets the Linear Artificial Viscosity for SPH.
            
        """
        return None

    @LinearViscositySPH.setter
    def LinearViscositySPH(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the Linear Artificial Viscosity for SPH.
            
        """
        pass

    @property
    def QuadratricViscositySPH(self) -> typing.Optional[float]:
        """
        
            Gets or sets the Quadratic Artificial Viscosity for SPH.
            
        """
        return None

    @QuadratricViscositySPH.setter
    def QuadratricViscositySPH(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the Quadratic Artificial Viscosity for SPH.
            
        """
        pass

    @property
    def HourglassDampingType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDHourglassDampingType]:
        """
        
            Gets or sets the HourglassDampingType.
            
        """
        return None

    @HourglassDampingType.setter
    def HourglassDampingType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDHourglassDampingType]) -> None:
        """
        
            Gets or sets the HourglassDampingType.
            
        """
        pass

    @property
    def StiffnessCoefficient(self) -> typing.Optional[float]:
        """
        
            Gets or sets the StiffnessCoefficient.
            
        """
        return None

    @StiffnessCoefficient.setter
    def StiffnessCoefficient(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the StiffnessCoefficient.
            
        """
        pass

    @property
    def ViscousCoefficient(self) -> typing.Optional[float]:
        """
        
            Gets or sets the ViscousCoefficient.
            
        """
        return None

    @ViscousCoefficient.setter
    def ViscousCoefficient(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the ViscousCoefficient.
            
        """
        pass

    @property
    def ViscousCoefficientFB(self) -> typing.Optional[float]:
        """
        
            Gets or sets the ViscousCoefficientFB.
            
        """
        return None

    @ViscousCoefficientFB.setter
    def ViscousCoefficientFB(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the ViscousCoefficientFB.
            
        """
        pass

    @property
    def ErosionOnGeomStrainType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the ErosionOnGeomStrainType.
            
        """
        return None

    @ErosionOnGeomStrainType.setter
    def ErosionOnGeomStrainType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the ErosionOnGeomStrainType.
            
        """
        pass

    @property
    def ErosionGeomStrainLimit(self) -> typing.Optional[float]:
        """
        
            Gets or sets the ErosionGeomStrainLimit
            
        """
        return None

    @ErosionGeomStrainLimit.setter
    def ErosionGeomStrainLimit(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the ErosionGeomStrainLimit
            
        """
        pass

    @property
    def ErosionOnMaterialFailureType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the ErosionOnMaterialFailureType
            
        """
        return None

    @ErosionOnMaterialFailureType.setter
    def ErosionOnMaterialFailureType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the ErosionOnMaterialFailureType
            
        """
        pass

    @property
    def ErosionOnMinElemTimestepType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the ErosionOnMinElemTimestepType
            
        """
        return None

    @ErosionOnMinElemTimestepType.setter
    def ErosionOnMinElemTimestepType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the ErosionOnMinElemTimestepType
            
        """
        pass

    @property
    def ErosionMinElemTimestep(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the ErosionMinElemTimestep
            
        """
        return None

    @ErosionMinElemTimestep.setter
    def ErosionMinElemTimestep(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the ErosionMinElemTimestep
            
        """
        pass

    @property
    def ErosionRetainIntertiaType(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the ErosionRetainIntertiaType
            
        """
        return None

    @ErosionRetainIntertiaType.setter
    def ErosionRetainIntertiaType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the ErosionRetainIntertiaType
            
        """
        pass

    @property
    def StepawareOutputControlsType(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets the Step aware Output Controls.
             
        """
        return None

    @StepawareOutputControlsType.setter
    def StepawareOutputControlsType(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets the Step aware Output Controls.
             
        """
        pass

    @property
    def OutputContactForcesOnType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDOutputContactForcesOnType]:
        """
        
            Gets or Sets OutputContactForces Increment Type.
             
        """
        return None

    @OutputContactForcesOnType.setter
    def OutputContactForcesOnType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDOutputContactForcesOnType]) -> None:
        """
        
            Gets or Sets OutputContactForces Increment Type.
             
        """
        pass

    @property
    def OutputContactForcesOnTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or Sets the Time increment for OutputContactForcesOnTime.
             
        """
        return None

    @OutputContactForcesOnTime.setter
    def OutputContactForcesOnTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or Sets the Time increment for OutputContactForcesOnTime.
             
        """
        pass

    @property
    def OutputContactForcesOnTimeSteps(self) -> typing.Optional[int]:
        """
        
            Gets or Sets the Cycle increment for OutputContactForcesOnTimeSteps.
             
        """
        return None

    @OutputContactForcesOnTimeSteps.setter
    def OutputContactForcesOnTimeSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets the Cycle increment for OutputContactForcesOnTimeSteps.
             
        """
        pass

    @property
    def OutputContactForcesOnPoints(self) -> typing.Optional[int]:
        """
        
            Gets or Sets the Points increment for OutputContactForcesOnPoints.
             
        """
        return None

    @OutputContactForcesOnPoints.setter
    def OutputContactForcesOnPoints(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets the Points increment for OutputContactForcesOnPoints.
             
        """
        pass

    @property
    def SavePrintSummaryOnType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSavePrintSummaryOnType]:
        """
        
            Gets or Sets SavePrintSummaryOnType.
             
        """
        return None

    @SavePrintSummaryOnType.setter
    def SavePrintSummaryOnType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSavePrintSummaryOnType]) -> None:
        """
        
            Gets or Sets SavePrintSummaryOnType.
             
        """
        pass

    @property
    def SavePrintSummaryOnTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or Sets the Time increment for SavePrintSummaryOnTime.
             
        """
        return None

    @SavePrintSummaryOnTime.setter
    def SavePrintSummaryOnTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or Sets the Time increment for SavePrintSummaryOnTime.
             
        """
        pass

    @property
    def SavePrintSummaryOnTimeSteps(self) -> typing.Optional[int]:
        """
        
            Gets or Sets Cycle increment for SavePrintSummaryOnTimeSteps.
             
        """
        return None

    @SavePrintSummaryOnTimeSteps.setter
    def SavePrintSummaryOnTimeSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets Cycle increment for SavePrintSummaryOnTimeSteps.
             
        """
        pass

    @property
    def OutputRemapFile(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDOutputRemapFileOnType]:
        """
        
            Gets or Sets the Output Remap File Type.
             
        """
        return None

    @OutputRemapFile.setter
    def OutputRemapFile(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDOutputRemapFileOnType]) -> None:
        """
        
            Gets or Sets the Output Remap File Type.
             
        """
        pass

    @property
    def SaveUserEditOnType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSaveUserEditOnType]:
        """
        
            Gets or Sets SaveUserEditOnType.
             
        """
        return None

    @SaveUserEditOnType.setter
    def SaveUserEditOnType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EXDSaveUserEditOnType]) -> None:
        """
        
            Gets or Sets SaveUserEditOnType.
             
        """
        pass

    @property
    def SaveUserEditOnTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or Sets Time increment for SaveUserEditOnTime.
             
        """
        return None

    @SaveUserEditOnTime.setter
    def SaveUserEditOnTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or Sets Time increment for SaveUserEditOnTime.
             
        """
        pass

    @property
    def SaveUserEditOnTimeSteps(self) -> typing.Optional[int]:
        """
        
            Gets or Sets Cycle increment for SaveUserEditOnTimeSteps.
             
        """
        return None

    @SaveUserEditOnTimeSteps.setter
    def SaveUserEditOnTimeSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets Cycle increment for SaveUserEditOnTimeSteps.
             
        """
        pass

    @property
    def Graph(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnalysisSettingsGraph]:
        """
        Graph property.
        """
        return None

    @property
    def SurfaceStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the SurfaceStress.
        """
        return None

    @SurfaceStress.setter
    def SurfaceStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SurfaceStress.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSAnalysisSettingsObjects.IDSAnalysisSettings]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ScratchSolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the ScratchSolverFilesDirectory.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the SolverFilesDirectory.
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

    def GetStepEndTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Step End Time at a given solution step.
            
        """
        pass

    def SetStepEndTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Step End Time for a given solution step.
            
        """
        pass

    def GetLoadStepType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.EXDLoadStepType:
        """
        
            Gets the  LoadStepType for a step.
             
        """
        pass

    def SetLoadStepType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDLoadStepType) -> None:
        """
        
            Sets the LoadStepType for a step.
             
        """
        pass

    def getADRConvergenceMethod(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.EXDADRConvergenceMethod:
        """
        
            Gets the Covergence Method for ADR loadstep.
             
        """
        pass

    def setADRConvergenceMethod(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDADRConvergenceMethod) -> None:
        """
        
            Sets the Covergence Method for ADR loadstep.
             
        """
        pass

    def getADRConvergenceTolerance(self, stepNumber: int) -> typing.Any:
        """
        
            Gets the Covergence Tolerance for ADR loadstep.
             
        """
        pass

    def setADRConvergenceTolerance(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the Covergence Tolerance for ADR loadstep.
             
        """
        pass

    def getADRMaximumIterations(self, stepNumber: int) -> typing.Any:
        """
        
            Gets the Maximum Iterations for ADR loadstep.
             
        """
        pass

    def setADRMaximumIterations(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Maximum Iterations for ADR loadstep.
             
        """
        pass

    def GetAutomaticMassScalingType(self, stepNumber: int) -> bool:
        """
        
            Gets the  AutomaticMassScalingType for a load step.
             
        """
        pass

    def SetAutomaticMassScalingType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDAutomaticMassScalingType) -> None:
        """
        
            Sets the  AutomaticMassScalingType for a load step.
             
        """
        pass

    def GetMassScalingMinTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the  MassScalingMinTimeStep for a load step.
             
        """
        pass

    def SetMassScalingMinTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the  MassScalingMinTimeStep for a load step.
             
        """
        pass

    def GetStaticDamping(self, stepNumber: int) -> typing.Any:
        """
        
            Gets the StaticDamping.
            
        """
        pass

    def SetStaticDamping(self, stepNumber: int, value: float) -> None:
        """
        
            Sets the StaticDamping.
            
        """
        pass

    def GetSaveResultsOnType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.EXDSaveResultsOnType:
        """
        
            Gets the  Save Results Type for a load step.
             
        """
        pass

    def SetSaveResultsOnType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDSaveResultsOnType) -> None:
        """
        
            Sets the  Save Results Type for a load step.
             
        """
        pass

    def GetSaveResultsOnTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Time increment for Save Results On for a load step.
             
        """
        pass

    def SetSaveResultsOnTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Set the Time increment for Save Results On for a load step.
             
        """
        pass

    def GetSaveResultsOnTimeSteps(self, stepNumber: int) -> int:
        """
        
            Gets the Cycle increment for Save Results On for a load step.
             
        """
        pass

    def SetSaveResultsOnTimeSteps(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the Cycle increment for Save Results On for a load step.
             
        """
        pass

    def GetSaveResultsOnPoints(self, stepNumber: int) -> int:
        """
        
            Gets the Points increment for Save Results On for a load step.
             
        """
        pass

    def SetSaveResultsOnPoints(self, stepNumber: int, value: int) -> None:
        """
        
            Set the Points increment for Save Results On for a load step.
             
        """
        pass

    def GetSaveRestartsOnType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.EXDSaveRestartsOnType:
        """
        
            Gets the  Save Restarts Type for a load step.
             
        """
        pass

    def SetSaveRestartsOnType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDSaveRestartsOnType) -> None:
        """
        
            Sets the  Save Restarts Type for a load step.
             
        """
        pass

    def GetSaveRestartsOnTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Time increment for Save Restarts On for a load step.
             
        """
        pass

    def SetSaveRestartsOnTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Set the Time increment for Save Restarts On for a load step.
             
        """
        pass

    def GetSaveRestartsOnTimeSteps(self, stepNumber: int) -> int:
        """
        
            Gets the Cycle increment for Save Restarts On for a load step.
             
        """
        pass

    def SetSaveRestartsOnTimeSteps(self, stepNumber: int, value: int) -> None:
        """
        
            Set the Cycle increment for Save Restarts On for a load step.
             
        """
        pass

    def GetSaveRestartsOnPoints(self, stepNumber: int) -> int:
        """
        
            Gets the Points increment for Save Restarts On Points for a load step.
             
        """
        pass

    def SetSaveRestartsOnPoints(self, stepNumber: int, value: int) -> None:
        """
        
            Set the Points increment for Save Restarts On for a load step.
             
        """
        pass

    def GetSaveProbeDataOnType(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.EXDSaveProbeDataOnType:
        """
        
            Gets the  Save ProbeData Type for a load step.
             
        """
        pass

    def SetSaveProbeDataOnType(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.EXDSaveProbeDataOnType) -> None:
        """
        
            Sets the  Save ProbeData Type for a load step.
             
        """
        pass

    def GetSaveProbeDataOnTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Time increment for Save ProbeData On for a load step.
             
        """
        pass

    def SetSaveProbeDataOnTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Set the Time increment for Save ProbeData On for a load step.
             
        """
        pass

    def GetSaveProbeDataOnTimeSteps(self, stepNumber: int) -> int:
        """
        
            Gets the Cycle increment for Save ProbeData On for a load step.
             
        """
        pass

    def SetSaveProbeDataOnTimeSteps(self, stepNumber: int, value: int) -> None:
        """
        
            Set the Cycle increment for Save ProbeData On for a load step.
             
        """
        pass

    def DeleteAllRestartPoints(self) -> None:
        """
        DeleteAllRestartPoints method.
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


class RBDAnalysisSettings(object):

    @property
    def InternalObject(self) -> typing.Optional[typing.Any]:
        """
        InternalObject property.
        """
        return None

    @property
    def NumberOfSteps(self) -> typing.Optional[int]:
        """
        
            Gets or sets the NumberOfSteps.
            
        """
        return None

    @NumberOfSteps.setter
    def NumberOfSteps(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the NumberOfSteps.
            
        """
        pass

    @property
    def CurrentStepNumber(self) -> typing.Optional[int]:
        """
        
            Gets or sets the CurrentStepNumber.
            
        """
        return None

    @CurrentStepNumber.setter
    def CurrentStepNumber(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the CurrentStepNumber.
            
        """
        pass

    @property
    def TimeIntegrationType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDTimeIntegrationType]:
        """
        
            Gets or sets the Integration Method.
            
        """
        return None

    @TimeIntegrationType.setter
    def TimeIntegrationType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDTimeIntegrationType]) -> None:
        """
        
            Gets or sets the Integration Method.
            
        """
        pass

    @property
    def PositionCorrection(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the PositionCorrection.
            
        """
        return None

    @PositionCorrection.setter
    def PositionCorrection(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the PositionCorrection.
            
        """
        pass

    @property
    def VelocityCorrection(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the VelocityCorrection.
            
        """
        return None

    @VelocityCorrection.setter
    def VelocityCorrection(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the VelocityCorrection.
            
        """
        pass

    @property
    def CorrectionType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDCorrectionType]:
        """
        
            Gets or sets the CorrectionType.
            
        """
        return None

    @CorrectionType.setter
    def CorrectionType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDCorrectionType]) -> None:
        """
        
            Gets or sets the CorrectionType.
            
        """
        pass

    @property
    def AssemblyType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDCorrectionType]:
        """
        
            Gets or sets the AssemblyType.
            
        """
        return None

    @AssemblyType.setter
    def AssemblyType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDCorrectionType]) -> None:
        """
        
            Gets or sets the AssemblyType.
            
        """
        pass

    @property
    def DropoffTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the DropoffTolerance.
            
        """
        return None

    @DropoffTolerance.setter
    def DropoffTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the DropoffTolerance.
            
        """
        pass

    @property
    def RelativeAssemblyTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the RelativeAssemblyTolerance activity.
            
        """
        return None

    @RelativeAssemblyTolerance.setter
    def RelativeAssemblyTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the RelativeAssemblyTolerance activity.
            
        """
        pass

    @property
    def RelativeAssemblyToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the RelativeAssemblyToleranceValue.
            
        """
        return None

    @RelativeAssemblyToleranceValue.setter
    def RelativeAssemblyToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the RelativeAssemblyToleranceValue.
            
        """
        pass

    @property
    def EnergyAccuracyTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the EnergyAccuracyTolerance activity.
            
        """
        return None

    @EnergyAccuracyTolerance.setter
    def EnergyAccuracyTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the EnergyAccuracyTolerance activity.
            
        """
        pass

    @property
    def EnergyAccuracyToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the EnergyAccuracyToleranceValue.
            
        """
        return None

    @EnergyAccuracyToleranceValue.setter
    def EnergyAccuracyToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the EnergyAccuracyToleranceValue.
            
        """
        pass

    @property
    def NumericalDampingTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the NumericalDamping activity.
            
        """
        return None

    @NumericalDampingTolerance.setter
    def NumericalDampingTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the NumericalDamping activity.
            
        """
        pass

    @property
    def NumericalDampingValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the NumericalDampingValue.
            
        """
        return None

    @NumericalDampingValue.setter
    def NumericalDampingValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the NumericalDampingValue.
            
        """
        pass

    @property
    def ForceResidualTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the ForceResidualTolerance activity.
            
        """
        return None

    @ForceResidualTolerance.setter
    def ForceResidualTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the ForceResidualTolerance activity.
            
        """
        pass

    @property
    def ForceResidualToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the ForceResidualToleranceValue.
            
        """
        return None

    @ForceResidualToleranceValue.setter
    def ForceResidualToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the ForceResidualToleranceValue.
            
        """
        pass

    @property
    def ConstraintEquationResidualTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the ConstraintEquationResidualTolerance activity.
            
        """
        return None

    @ConstraintEquationResidualTolerance.setter
    def ConstraintEquationResidualTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the ConstraintEquationResidualTolerance activity.
            
        """
        pass

    @property
    def ConstraintEquationResidualToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the ConstraintEquationResidualToleranceValue.
            
        """
        return None

    @ConstraintEquationResidualToleranceValue.setter
    def ConstraintEquationResidualToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the ConstraintEquationResidualToleranceValue.
            
        """
        pass

    @property
    def VelocityConstraintEquationResidualTolerance(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]:
        """
        
            Gets or sets the VelocityConstraintEquationResidualTolerance activity.
            
        """
        return None

    @VelocityConstraintEquationResidualTolerance.setter
    def VelocityConstraintEquationResidualTolerance(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDProgramControlType]) -> None:
        """
        
            Gets or sets the VelocityConstraintEquationResidualTolerance activity.
            
        """
        pass

    @property
    def VelocityConstraintEquationResidualToleranceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the ConstraintEquationResidualToleranceValue.
            
        """
        return None

    @VelocityConstraintEquationResidualToleranceValue.setter
    def VelocityConstraintEquationResidualToleranceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the ConstraintEquationResidualToleranceValue.
            
        """
        pass

    @property
    def PerformStaticAnalysis(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDDoStaticAnalysisType]:
        """
        
            Gets or sets the .
            
        """
        return None

    @PerformStaticAnalysis.setter
    def PerformStaticAnalysis(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.RBDDoStaticAnalysisType]) -> None:
        """
        
            Gets or sets the .
            
        """
        pass

    @property
    def Graph(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnalysisSettingsGraph]:
        """
        Graph property.
        """
        return None

    @property
    def SurfaceStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the SurfaceStress.
        """
        return None

    @SurfaceStress.setter
    def SurfaceStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the SurfaceStress.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSAnalysisSettingsObjects.IDSAnalysisSettings]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ScratchSolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the ScratchSolverFilesDirectory.
        """
        return None

    @property
    def SolverFilesDirectory(self) -> typing.Optional[str]:
        """
        Gets the SolverFilesDirectory.
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

    def GetStepEndTime(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Step End Time at a given solution step.
            
        """
        pass

    def SetStepEndTime(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Step End Time for a given solution step.
            
        """
        pass

    def GetAutomaticTimeStepping(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping:
        """
        
            Gets the Automatic Time Stepping at a given solution step.
            
        """
        pass

    def SetAutomaticTimeStepping(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.AutomaticTimeStepping) -> None:
        """
        
            Sets the Automatic Time Stepping for a given solution step.
            
        """
        pass

    def GetCarryOverTimeStep(self, stepNumber: int) -> bool:
        """
        
            Gets the Carry Over Time Step at a given solution step.
            
        """
        pass

    def SetCarryOverTimeStep(self, stepNumber: int, value: bool) -> None:
        """
        
            Sets the Carry Over Time Step for a given solution step.
            
        """
        pass

    def GetInitialTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Initial Time Step at a given solution step.
            
        """
        pass

    def SetInitialTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Initial Time Step for a given solution step.
            
        """
        pass

    def GetMinimumTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Minimum Time Step at a given solution step.
            
        """
        pass

    def SetMinimumTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Minimum Time Step for a given solution step.
            
        """
        pass

    def GetMaximumTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the Maximum Time Step at a given solution step.
            
        """
        pass

    def SetMaximumTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the Maximum Time Step for a given solution step.
            
        """
        pass

    def GetTimeStep(self, stepNumber: int) -> Ansys.Core.Units.Quantity:
        """
        
            Gets the (fixed) Time Step at a given solution step.
            
        """
        pass

    def SetTimeStep(self, stepNumber: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        
            Sets the (fixed) Time Step for a given solution step.
            
        """
        pass

    def GetStoreResultAt(self, stepNumber: int) -> Ansys.Mechanical.DataModel.Enums.TimePointsOptions:
        """
        
            Gets the StoreResultAt setting at a given solution step.
            
        """
        pass

    def SetStoreResultAt(self, stepNumber: int, value: Ansys.Mechanical.DataModel.Enums.TimePointsOptions) -> None:
        """
        
            Sets the StoreResultAt setting for a given solution step.
            
        """
        pass

    def GetStoreResultAtValue(self, stepNumber: int) -> int:
        """
        
            Gets the StoreResultAtValue setting at a given solution step.
            
        """
        pass

    def SetStoreResultAtValue(self, stepNumber: int, value: int) -> None:
        """
        
            Sets the StoreResultAtValue setting for a given solution step.
            
        """
        pass

    def DeleteAllRestartPoints(self) -> None:
        """
        DeleteAllRestartPoints method.
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


