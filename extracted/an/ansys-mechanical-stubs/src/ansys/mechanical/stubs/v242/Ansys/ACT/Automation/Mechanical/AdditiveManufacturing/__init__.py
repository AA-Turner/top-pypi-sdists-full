"""AdditiveManufacturing module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class AMBuildSettings(object):
    """
    Defines a AMBuildSettings.
    """

    @property
    def LayerHeightType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMLayerHeightType]:
        """
        
            LayerHeightType - Get/Sets the layer height type.
            
        """
        return None

    @LayerHeightType.setter
    def LayerHeightType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMLayerHeightType]) -> None:
        """
        
            LayerHeightType - Get/Sets the layer height type.
            
        """
        pass

    @property
    def ThermalStrainMaterialModel(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMaterialModel]:
        """
        Gets or sets the MachineLearningModel using the deprecated ThermalStrainMaterialModel methods.
        """
        return None

    @ThermalStrainMaterialModel.setter
    def ThermalStrainMaterialModel(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMaterialModel]) -> None:
        """
        Gets or sets the MachineLearningModel using the deprecated ThermalStrainMaterialModel methods.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSettingsAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Absorptivity(self) -> typing.Optional[float]:
        """
        Gets or sets the Absorptivity.
        """
        return None

    @Absorptivity.setter
    def Absorptivity(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the Absorptivity.
        """
        pass

    @property
    def ASCParallel(self) -> typing.Optional[float]:
        """
        Gets or sets the ASCParallel.
        """
        return None

    @ASCParallel.setter
    def ASCParallel(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ASCParallel.
        """
        pass

    @property
    def ASCPerpendicular(self) -> typing.Optional[float]:
        """
        Gets or sets the ASCPerpendicular.
        """
        return None

    @ASCPerpendicular.setter
    def ASCPerpendicular(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ASCPerpendicular.
        """
        pass

    @property
    def ASCVertical(self) -> typing.Optional[float]:
        """
        Gets or sets the ASCVertical.
        """
        return None

    @ASCVertical.setter
    def ASCVertical(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ASCVertical.
        """
        pass

    @property
    def BeamDiameter(self) -> typing.Optional[float]:
        """
        Gets or sets the BeamDiameter.
        """
        return None

    @BeamDiameter.setter
    def BeamDiameter(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the BeamDiameter.
        """
        pass

    @property
    def BeamPower(self) -> typing.Optional[float]:
        """
        Gets or sets the BeamPower.
        """
        return None

    @BeamPower.setter
    def BeamPower(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the BeamPower.
        """
        pass

    @property
    def PowderPropertyFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the PowderPropertyFactor.
        """
        return None

    @PowderPropertyFactor.setter
    def PowderPropertyFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the PowderPropertyFactor.
        """
        pass

    @property
    def DwellTimeMultiple(self) -> typing.Optional[float]:
        """
        Gets or sets the DwellTimeMultiple.
        """
        return None

    @DwellTimeMultiple.setter
    def DwellTimeMultiple(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DwellTimeMultiple.
        """
        pass

    @property
    def GeneratedLayerRotationAngle(self) -> typing.Optional[float]:
        """
        Gets or sets the GeneratedLayerRotationAngle.
        """
        return None

    @GeneratedLayerRotationAngle.setter
    def GeneratedLayerRotationAngle(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GeneratedLayerRotationAngle.
        """
        pass

    @property
    def GeneratedStartLayerAngle(self) -> typing.Optional[float]:
        """
        Gets or sets the GeneratedStartLayerAngle.
        """
        return None

    @GeneratedStartLayerAngle.setter
    def GeneratedStartLayerAngle(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the GeneratedStartLayerAngle.
        """
        pass

    @property
    def NumberOfHeatSources(self) -> typing.Optional[int]:
        """
        Gets or sets the NumberOfHeatSources.
        """
        return None

    @NumberOfHeatSources.setter
    def NumberOfHeatSources(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the NumberOfHeatSources.
        """
        pass

    @property
    def ScanPatternBuildFilePath(self) -> typing.Optional[str]:
        """
        Gets or sets the ScanPatternBuildFilePath.
        """
        return None

    @ScanPatternBuildFilePath.setter
    def ScanPatternBuildFilePath(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ScanPatternBuildFilePath.
        """
        pass

    @property
    def ScanStripeWidth(self) -> typing.Optional[float]:
        """
        Gets or sets the ScanStripeWidth.
        """
        return None

    @ScanStripeWidth.setter
    def ScanStripeWidth(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ScanStripeWidth.
        """
        pass

    @property
    def StrainScalingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the StrainScalingFactor.
        """
        return None

    @StrainScalingFactor.setter
    def StrainScalingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StrainScalingFactor.
        """
        pass

    @property
    def StrainScalingFactorX(self) -> typing.Optional[float]:
        """
        Gets or sets the StrainScalingFactorX.
        """
        return None

    @StrainScalingFactorX.setter
    def StrainScalingFactorX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StrainScalingFactorX.
        """
        pass

    @property
    def StrainScalingFactorY(self) -> typing.Optional[float]:
        """
        Gets or sets the StrainScalingFactorY.
        """
        return None

    @StrainScalingFactorY.setter
    def StrainScalingFactorY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StrainScalingFactorY.
        """
        pass

    @property
    def StrainScalingFactorZ(self) -> typing.Optional[float]:
        """
        Gets or sets the StrainScalingFactorZ.
        """
        return None

    @StrainScalingFactorZ.setter
    def StrainScalingFactorZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the StrainScalingFactorZ.
        """
        pass

    @property
    def ThermalStrainScalingFactor(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalStrainScalingFactor.
        """
        return None

    @ThermalStrainScalingFactor.setter
    def ThermalStrainScalingFactor(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalStrainScalingFactor.
        """
        pass

    @property
    def BuildGasConvectionCoefficient(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BuildGasConvectionCoefficient.
        """
        return None

    @BuildGasConvectionCoefficient.setter
    def BuildGasConvectionCoefficient(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BuildGasConvectionCoefficient.
        """
        pass

    @property
    def BuildGasTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BuildGasTemperature.
        """
        return None

    @BuildGasTemperature.setter
    def BuildGasTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BuildGasTemperature.
        """
        pass

    @property
    def BuildPowderConvectionCoefficient(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BuildPowderConvectionCoefficient.
        """
        return None

    @BuildPowderConvectionCoefficient.setter
    def BuildPowderConvectionCoefficient(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BuildPowderConvectionCoefficient.
        """
        pass

    @property
    def BuildPowderTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the BuildPowderTemperature.
        """
        return None

    @BuildPowderTemperature.setter
    def BuildPowderTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the BuildPowderTemperature.
        """
        pass

    @property
    def CooldownGasConvectionCoefficient(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CooldownGasConvectionCoefficient.
        """
        return None

    @CooldownGasConvectionCoefficient.setter
    def CooldownGasConvectionCoefficient(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CooldownGasConvectionCoefficient.
        """
        pass

    @property
    def CooldownGasTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CooldownGasTemperature.
        """
        return None

    @CooldownGasTemperature.setter
    def CooldownGasTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CooldownGasTemperature.
        """
        pass

    @property
    def CooldownPowderConvectionCoefficient(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CooldownPowderConvectionCoefficient.
        """
        return None

    @CooldownPowderConvectionCoefficient.setter
    def CooldownPowderConvectionCoefficient(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CooldownPowderConvectionCoefficient.
        """
        pass

    @property
    def CooldownPowderTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the CooldownPowderTemperature.
        """
        return None

    @CooldownPowderTemperature.setter
    def CooldownPowderTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the CooldownPowderTemperature.
        """
        pass

    @property
    def DepositionThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DepositionThickness.
        """
        return None

    @DepositionThickness.setter
    def DepositionThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DepositionThickness.
        """
        pass

    @property
    def DwellTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DwellTime.
        """
        return None

    @DwellTime.setter
    def DwellTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DwellTime.
        """
        pass

    @property
    def HatchSpacing(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the HatchSpacing.
        """
        return None

    @HatchSpacing.setter
    def HatchSpacing(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the HatchSpacing.
        """
        pass

    @property
    def LayerHeightValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the LayerHeightValue.
        """
        return None

    @LayerHeightValue.setter
    def LayerHeightValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the LayerHeightValue.
        """
        pass

    @property
    def PreheatTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the PreheatTemperature.
        """
        return None

    @PreheatTemperature.setter
    def PreheatTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the PreheatTemperature.
        """
        pass

    @property
    def RoomTemperature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the RoomTemperature.
        """
        return None

    @RoomTemperature.setter
    def RoomTemperature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the RoomTemperature.
        """
        pass

    @property
    def ScanSpeed(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the ScanSpeed.
        """
        return None

    @ScanSpeed.setter
    def ScanSpeed(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the ScanSpeed.
        """
        pass

    @property
    def BuildGasOrPowderTemperatureType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessSettingsType]:
        """
        Gets or sets the BuildGasOrPowderTemperatureType.
        """
        return None

    @BuildGasOrPowderTemperatureType.setter
    def BuildGasOrPowderTemperatureType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessSettingsType]) -> None:
        """
        Gets or sets the BuildGasOrPowderTemperatureType.
        """
        pass

    @property
    def BuildMachineType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMBuildMachineType]:
        """
        Gets or sets the BuildMachineType.
        """
        return None

    @BuildMachineType.setter
    def BuildMachineType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMBuildMachineType]) -> None:
        """
        Gets or sets the BuildMachineType.
        """
        pass

    @property
    def CooldownGasOrPowderTemperatureType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessSettingsType]:
        """
        Gets or sets the CooldownGasOrPowderTemperatureType.
        """
        return None

    @CooldownGasOrPowderTemperatureType.setter
    def CooldownGasOrPowderTemperatureType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessSettingsType]) -> None:
        """
        Gets or sets the CooldownGasOrPowderTemperatureType.
        """
        pass

    @property
    def HeatingDuration(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMHeatingDurationType]:
        """
        Gets or sets the HeatingDuration.
        """
        return None

    @HeatingDuration.setter
    def HeatingDuration(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMHeatingDurationType]) -> None:
        """
        Gets or sets the HeatingDuration.
        """
        pass

    @property
    def HeatingMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMHeatingMethod]:
        """
        Gets or sets the HeatingMethod.
        """
        return None

    @HeatingMethod.setter
    def HeatingMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMHeatingMethod]) -> None:
        """
        Gets or sets the HeatingMethod.
        """
        pass

    @property
    def InherentStrainDefinition(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMInherentStrainDefinition]:
        """
        Gets or sets the InherentStrainDefinition.
        """
        return None

    @InherentStrainDefinition.setter
    def InherentStrainDefinition(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMInherentStrainDefinition]) -> None:
        """
        Gets or sets the InherentStrainDefinition.
        """
        pass

    @property
    def MachineLearningModel(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMachineLearningModel]:
        """
        Gets or sets the MachineLearningModel.
        """
        return None

    @MachineLearningModel.setter
    def MachineLearningModel(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMachineLearningModel]) -> None:
        """
        Gets or sets the MachineLearningModel.
        """
        pass

    @property
    def AdditiveProcess(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessType]:
        """
        Gets or sets the AdditiveProcess.
        """
        return None

    @AdditiveProcess.setter
    def AdditiveProcess(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessType]) -> None:
        """
        Gets or sets the AdditiveProcess.
        """
        pass

    @property
    def ScanPatternDefinition(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMScanPatternDefinition]:
        """
        Gets or sets the ScanPatternDefinition.
        """
        return None

    @ScanPatternDefinition.setter
    def ScanPatternDefinition(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMScanPatternDefinition]) -> None:
        """
        Gets or sets the ScanPatternDefinition.
        """
        pass

    @property
    def ThermalStrainMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMethod]:
        """
        Gets or sets the ThermalStrainMethod.
        """
        return None

    @ThermalStrainMethod.setter
    def ThermalStrainMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMethod]) -> None:
        """
        Gets or sets the ThermalStrainMethod.
        """
        pass

    @property
    def InherentStrain(self) -> typing.Optional[bool]:
        """
        Gets or sets the InherentStrain.
        """
        return None

    @InherentStrain.setter
    def InherentStrain(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the InherentStrain.
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

    def SaveBuildSettings(self, fName: str) -> None:
        """
        Run the SaveBuildSettings action.
        """
        pass

    def LoadBuildSettings(self, fName: str) -> None:
        """
        Run the LoadBuildSettings action.
        """
        pass

    def ResetToDefault(self) -> None:
        """
        ResetToDefault - Restores default values of all properties.
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


class IAMProcessStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass


class SupportRemoval(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def Support(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.AMSupport]:
        """
        Support property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    def __init__(self, obj: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.AMSupport) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class BaseRemoval(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class BaseUnboltStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class UserStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class BuildStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class HeatTreatmentStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class CooldownStep(object):

    @property
    def ProcessStepType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMProcessStepType]:
        """
        ProcessStepType property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep]:
        """
        InternalObject property.
        """
        return None

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, internalObject: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequenceStep) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def Equals(self, other: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        Equals method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass


class AMSupportRemovalSequence(object):

    @property
    def Item(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        IsReadOnly property.
        """
        return None

    def __init__(self, sequenceObj: Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSequence) -> None:
        """
        __init__ method.
        """
        pass

    def GetEnumerator(self) -> typing.Iterator[Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep]:
        """
        GetEnumerator method.
        """
        pass

    def Add(self, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> None:
        """
        
            Adds a support or base removal step.
            Throws a notSupportedException if the same step was already added.
            Usage:
             removalSequence.Add(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval())
             removalSequence.Add(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj))
            
        """
        pass

    @typing.overload
    def Remove(self, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        ...

    @typing.overload
    def Remove(self, index: int) -> bool:
        ...

    def Remove(self, *args: typing.Any) -> bool:
        """
        
            Remove a support or base removal step.
            Returns true if the step was removed
            Returns false if the step could not be removed because it did not exist
            Usage:
            C#:
                removalSequence.Remove(new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval());
                removalSequence.Remove(new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
                removalSequence.Remove(removalSequence[2]));
            Python:
                removalSequence.Remove(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval());
                removalSequence.Remove(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
                removalSequence.Remove(removalSequence[2]))
            
        """
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Remove AM step at index.
            Throws IndexOutOfRangeException if index is out of range
            Usage:
             removalSequence.RemoveAt(0)
            
        """
        pass

    @typing.overload
    def Swap(self, item1: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep, item2: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        ...

    @typing.overload
    def Swap(self, index1: int, index2: int) -> bool:
        ...

    def Swap(self, *args: typing.Any) -> bool:
        """
        
            Swaps two steps in the Removal sequence.
            Returns true if successful and false if unsuccessful
            Usage:
            C#
             removalSequence.Swap(
                new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval(),
                new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
            Python
             removalSequence.Swap(
                Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval(),
                Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj))
            
        """
        pass

    def Find(self, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> int:
        """
        Find method.
        """
        pass

    def IndexOf(self, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> int:
        """
        
            Returns index of removal object
            Returns -1 if removal object not found
            Usage:
            C#
                index1 = removalSequence.IndexOf(new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval());
                index2 = removalSequence.IndexOf(new Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
            Python
                index1 = removalSequence.IndexOf(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval());
                index2 = removalSequence.IndexOf(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
            
        """
        pass

    def Insert(self, index: int, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> None:
        """
        
            Inserts a given step at particular index(zero based)
            Throws an IndexOutOfRangeException if the step is being inserted out of range.
            Throws a NotSupportedException if the insertion is invalid
            Usage:
             Sequence.Insert(0,Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.UserStep())
            
        """
        pass

    def Clear(self) -> None:
        """
        Clear method.
        """
        pass

    def Contains(self, item: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep) -> bool:
        """
        
            Returns true if the step exists in the sequencer. If not, returns false
            Usage:
                index1 = removalSequence.Contains(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.BaseRemoval());
                index2 = removalSequence.Contains(Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.SupportRemoval(supportObj));
            
        """
        pass

    def CopyTo(self, array: Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.IAMProcessStep, index: int) -> None:
        """
        CopyTo method.
        """
        pass


class AMProcess(object):
    """
    Defines a AMProcess.
    """

    @property
    def BuildGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the PartGeometry using the deprecated BuildGeometry method.
        """
        return None

    @BuildGeometry.setter
    def BuildGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the PartGeometry using the deprecated BuildGeometry method.
        """
        pass

    @property
    def ThermalStrainMaterialModel(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMaterialModel]:
        """
        ThermalStrainMaterialModel property.
        """
        return None

    @ThermalStrainMaterialModel.setter
    def ThermalStrainMaterialModel(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMThermalStrainMaterialModel]) -> None:
        """
        ThermalStrainMaterialModel property.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMProcessSimulationAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def ZLocationAtTopOfBase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ZLocationAtTopOfBase.
        """
        return None

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
    def LengthUnits(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the LengthUnits.
        """
        return None

    @LengthUnits.setter
    def LengthUnits(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the LengthUnits.
        """
        pass

    @property
    def NonlinearEffects(self) -> typing.Optional[bool]:
        """
        Gets or sets the NonlinearEffects.
        """
        return None

    @NonlinearEffects.setter
    def NonlinearEffects(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the NonlinearEffects.
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
    def BaseGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the BaseGeometry.
        """
        return None

    @BaseGeometry.setter
    def BaseGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the BaseGeometry.
        """
        pass

    @property
    def PartGeometry(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the PartGeometry.
        """
        return None

    @PartGeometry.setter
    def PartGeometry(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the PartGeometry.
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

    def GetSequence(self, analysis: Ansys.ACT.Automation.Mechanical.Analysis) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.AMSupportRemovalSequence:
        """
        
            Gets the support removal sequence for a given environment.
            
        """
        pass

    def ResetAllSequences(self) -> None:
        """
        
            Resets the sequence for all analyses
            
        """
        pass

    @classmethod
    def IsStaticAnalysisDownstreamOfThermalAnalysis(cls, staticAnalysis: Ansys.ACT.Automation.Mechanical.Analysis, thermalAnalysis: Ansys.ACT.Automation.Mechanical.Analysis) -> bool:
        """
        IsStaticAnalysisDownstreamOfThermalAnalysis method.
        """
        pass

    def AddCartesianMesh(self) -> Ansys.ACT.Automation.Mechanical.MeshControls.AutomaticMethod:
        """
        AddCartesianMesh method.
        """
        pass

    def CreateBuildToBaseContact(self) -> Ansys.ACT.Automation.Mechanical.Connections.ContactRegion:
        """
        Run the CreateBuildToBaseContact action.
        """
        pass

    def CreateAMBondConnections(self) -> None:
        """
        Run the CreateAMBondConnections action.
        """
        pass

    def GenerateAMStrains(self) -> None:
        """
        Run the GenerateAMStrains action.
        """
        pass

    def CleanAMStrains(self) -> None:
        """
        Run the CleanAMStrains action.
        """
        pass

    def HasAMStrains(self) -> bool:
        """
        Get the HasAMStrains property.
        """
        pass

    def AddSupportGroup(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.AMSupportGroup:
        """
        Creates a new AMSupportGroup
        """
        pass

    def AddGeneratedAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.GeneratedAMSupport:
        """
        Creates a new GeneratedAMSupport
        """
        pass

    def AddPredefinedAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.PredefinedAMSupport:
        """
        Creates a new PredefinedAMSupport
        """
        pass

    def AddSTLAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.STLAMSupport:
        """
        Creates a new STLAMSupport
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


class AMSupportGroup(object):
    """
    Defines a AMSupportGroup.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMSupportGroupAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def HangAngle(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the HangAngle.
        """
        return None

    @HangAngle.setter
    def HangAngle(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the HangAngle.
        """
        pass

    @property
    def DetectAboveZLocation(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the DetectAboveZLocation.
        """
        return None

    @DetectAboveZLocation.setter
    def DetectAboveZLocation(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the DetectAboveZLocation.
        """
        pass

    @property
    def OutputType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportGroupOutputType]:
        """
        Gets or sets the OutputType.
        """
        return None

    @OutputType.setter
    def OutputType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportGroupOutputType]) -> None:
        """
        Gets or sets the OutputType.
        """
        pass

    @property
    def GenerateOnRemesh(self) -> typing.Optional[bool]:
        """
        Gets or sets the GenerateOnRemesh.
        """
        return None

    @GenerateOnRemesh.setter
    def GenerateOnRemesh(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the GenerateOnRemesh.
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

    def DetectSupportFaces(self) -> typing.Iterable[Ansys.Mechanical.DataModel.Interfaces.IDataModelObject]:
        """
        Runs the Detect Support Faces action.
        """
        pass

    def AddGeneratedAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.GeneratedAMSupport:
        """
        Creates a new GeneratedAMSupport
        """
        pass

    def AddPredefinedAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.PredefinedAMSupport:
        """
        Creates a new PredefinedAMSupport
        """
        pass

    def AddSTLAMSupport(self) -> Ansys.ACT.Automation.Mechanical.AdditiveManufacturing.STLAMSupport:
        """
        Creates a new GeneratedAMSupport
        """
        pass

    def PromoteToNamedSelection(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def Clean(self) -> None:
        """
        Clean method.
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


class GeneratedAMSupport(object):
    """
    Defines a GeneratedAMSupport.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMSupportAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Mode(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]:
        """
        Gets or sets the Mode.
        """
        return None

    @Mode.setter
    def Mode(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AutomaticOrManual]) -> None:
        """
        Gets or sets the Mode.
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
    def ThermalConductivityMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        return None

    @ThermalConductivityMultipleInX.setter
    def ThermalConductivityMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        pass

    @property
    def ThermalConductivityMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        return None

    @ThermalConductivityMultipleInY.setter
    def ThermalConductivityMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        pass

    @property
    def ThermalConductivityMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        return None

    @ThermalConductivityMultipleInZ.setter
    def ThermalConductivityMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        pass

    @property
    def DensityMultiple(self) -> typing.Optional[float]:
        """
        Gets or sets the DensityMultiple.
        """
        return None

    @DensityMultiple.setter
    def DensityMultiple(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DensityMultiple.
        """
        pass

    @property
    def MaterialMultiplier(self) -> typing.Optional[float]:
        """
        Gets or sets the MaterialMultiplier.
        """
        return None

    @MaterialMultiplier.setter
    def MaterialMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaterialMultiplier.
        """
        pass

    @property
    def ElasticModulusMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        return None

    @ElasticModulusMultipleInX.setter
    def ElasticModulusMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        pass

    @property
    def ElasticModulusMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        return None

    @ElasticModulusMultipleInY.setter
    def ElasticModulusMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        pass

    @property
    def ElasticModulusMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        return None

    @ElasticModulusMultipleInZ.setter
    def ElasticModulusMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        pass

    @property
    def ShearModulusMultipleInXY(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        return None

    @ShearModulusMultipleInXY.setter
    def ShearModulusMultipleInXY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        pass

    @property
    def ShearModulusMultipleInXZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        return None

    @ShearModulusMultipleInXZ.setter
    def ShearModulusMultipleInXZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        pass

    @property
    def ShearModulusMultipleInYZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        return None

    @ShearModulusMultipleInYZ.setter
    def ShearModulusMultipleInYZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        pass

    @property
    def WallSpacing(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WallSpacing.
        """
        return None

    @WallSpacing.setter
    def WallSpacing(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WallSpacing.
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
    def Volume(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Volume.
        """
        return None

    @Volume.setter
    def Volume(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Volume.
        """
        pass

    @property
    def MultiplierEntry(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]:
        """
        Gets or sets the MultiplierEntry.
        """
        return None

    @MultiplierEntry.setter
    def MultiplierEntry(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]) -> None:
        """
        Gets or sets the MultiplierEntry.
        """
        pass

    @property
    def SupportType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]:
        """
        Gets or sets the SupportType.
        """
        return None

    @SupportType.setter
    def SupportType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]) -> None:
        """
        Gets or sets the SupportType.
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

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
        """
        pass

    def GenerateSupportBodies(self, progress: Ansys.Mechanical.Application.Progress) -> None:
        """
        Generate Support Bodies.
        """
        pass

    def CreateNamedSelectionOfGeneratedElements(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Run the PromoteToNamedSelection action.
        """
        pass

    def GetGeneratedBody(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        Returns the generated body object
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class STLAMSupport(object):
    """
    Defines a STLAMSupport.
    """

    @property
    def VoxelSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the VoxelSize.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMSupportAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def Filename(self) -> typing.Optional[str]:
        """
        Gets or sets the Filename.
        """
        return None

    @Filename.setter
    def Filename(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the Filename.
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
    def ElementSize(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the ElementSize.
        """
        return None

    @property
    def StlWallThickness(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the StlWallThickness.
        """
        return None

    @StlWallThickness.setter
    def StlWallThickness(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the StlWallThickness.
        """
        pass

    @property
    def LengthUnits(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]:
        """
        Gets or sets the LengthUnits.
        """
        return None

    @LengthUnits.setter
    def LengthUnits(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WBUnitSystemType]) -> None:
        """
        Gets or sets the LengthUnits.
        """
        pass

    @property
    def STLSupportView(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.STLSupportViewType]:
        """
        Gets or sets the STLSupportView.
        """
        return None

    @STLSupportView.setter
    def STLSupportView(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.STLSupportViewType]) -> None:
        """
        Gets or sets the STLSupportView.
        """
        pass

    @property
    def Source(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMStlSource]:
        """
        Gets or sets the Source.
        """
        return None

    @Source.setter
    def Source(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMStlSource]) -> None:
        """
        Gets or sets the Source.
        """
        pass

    @property
    def STLSupportType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportSTLType]:
        """
        Gets or sets the STLSupportType.
        """
        return None

    @STLSupportType.setter
    def STLSupportType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportSTLType]) -> None:
        """
        Gets or sets the STLSupportType.
        """
        pass

    @property
    def STL(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.STL]:
        """
        Gets or sets the STL.
        """
        return None

    @STL.setter
    def STL(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.STL]) -> None:
        """
        Gets or sets the STL.
        """
        pass

    @property
    def GeometrySelection(self) -> typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]:
        """
        Gets or sets the GeometrySelection.
        """
        return None

    @GeometrySelection.setter
    def GeometrySelection(self, value: typing.Optional[Ansys.ACT.Interfaces.Common.ISelectionInfo]) -> None:
        """
        Gets or sets the GeometrySelection.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def ThermalConductivityMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        return None

    @ThermalConductivityMultipleInX.setter
    def ThermalConductivityMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        pass

    @property
    def ThermalConductivityMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        return None

    @ThermalConductivityMultipleInY.setter
    def ThermalConductivityMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        pass

    @property
    def ThermalConductivityMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        return None

    @ThermalConductivityMultipleInZ.setter
    def ThermalConductivityMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        pass

    @property
    def DensityMultiple(self) -> typing.Optional[float]:
        """
        Gets or sets the DensityMultiple.
        """
        return None

    @DensityMultiple.setter
    def DensityMultiple(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DensityMultiple.
        """
        pass

    @property
    def MaterialMultiplier(self) -> typing.Optional[float]:
        """
        Gets or sets the MaterialMultiplier.
        """
        return None

    @MaterialMultiplier.setter
    def MaterialMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaterialMultiplier.
        """
        pass

    @property
    def ElasticModulusMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        return None

    @ElasticModulusMultipleInX.setter
    def ElasticModulusMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        pass

    @property
    def ElasticModulusMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        return None

    @ElasticModulusMultipleInY.setter
    def ElasticModulusMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        pass

    @property
    def ElasticModulusMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        return None

    @ElasticModulusMultipleInZ.setter
    def ElasticModulusMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        pass

    @property
    def ShearModulusMultipleInXY(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        return None

    @ShearModulusMultipleInXY.setter
    def ShearModulusMultipleInXY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        pass

    @property
    def ShearModulusMultipleInXZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        return None

    @ShearModulusMultipleInXZ.setter
    def ShearModulusMultipleInXZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        pass

    @property
    def ShearModulusMultipleInYZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        return None

    @ShearModulusMultipleInYZ.setter
    def ShearModulusMultipleInYZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        pass

    @property
    def WallSpacing(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WallSpacing.
        """
        return None

    @WallSpacing.setter
    def WallSpacing(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WallSpacing.
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
    def Volume(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Volume.
        """
        return None

    @Volume.setter
    def Volume(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Volume.
        """
        pass

    @property
    def MultiplierEntry(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]:
        """
        Gets or sets the MultiplierEntry.
        """
        return None

    @MultiplierEntry.setter
    def MultiplierEntry(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]) -> None:
        """
        Gets or sets the MultiplierEntry.
        """
        pass

    @property
    def SupportType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]:
        """
        Gets or sets the SupportType.
        """
        return None

    @SupportType.setter
    def SupportType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]) -> None:
        """
        Gets or sets the SupportType.
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

    def ClearGeneratedData(self) -> None:
        """
        Run the ClearGeneratedData action.
        """
        pass

    def GenerateSupportBodies(self, progress: Ansys.Mechanical.Application.Progress) -> None:
        """
        Generate Support Bodies.
        """
        pass

    def CreateNamedSelectionOfGeneratedElements(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Create a named selection of the generated elements.
        """
        pass

    def CreateNamedSelectionOfExternalElementFaces(self) -> typing.Iterable[Ansys.ACT.Automation.Mechanical.NamedSelection]:
        """
        Create a named selection of the generated exterior element faces.
        """
        pass

    def ExportStl(self, filename: str, progress: Ansys.Mechanical.Application.Progress) -> None:
        """
        Export STL data.
        """
        pass

    def GetGeneratedBody(self) -> Ansys.Mechanical.DataModel.Interfaces.IDataModelObject:
        """
        Returns the generated body object
        """
        pass

    def ImportSTL(self) -> None:
        """
        Run the ImportSTL action.
        """
        pass

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class AMSupport(object):
    """
    Defines a AMSupport.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMSupportAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def ThermalConductivityMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        return None

    @ThermalConductivityMultipleInX.setter
    def ThermalConductivityMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        pass

    @property
    def ThermalConductivityMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        return None

    @ThermalConductivityMultipleInY.setter
    def ThermalConductivityMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        pass

    @property
    def ThermalConductivityMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        return None

    @ThermalConductivityMultipleInZ.setter
    def ThermalConductivityMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        pass

    @property
    def DensityMultiple(self) -> typing.Optional[float]:
        """
        Gets or sets the DensityMultiple.
        """
        return None

    @DensityMultiple.setter
    def DensityMultiple(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DensityMultiple.
        """
        pass

    @property
    def MaterialMultiplier(self) -> typing.Optional[float]:
        """
        Gets or sets the MaterialMultiplier.
        """
        return None

    @MaterialMultiplier.setter
    def MaterialMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaterialMultiplier.
        """
        pass

    @property
    def ElasticModulusMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        return None

    @ElasticModulusMultipleInX.setter
    def ElasticModulusMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        pass

    @property
    def ElasticModulusMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        return None

    @ElasticModulusMultipleInY.setter
    def ElasticModulusMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        pass

    @property
    def ElasticModulusMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        return None

    @ElasticModulusMultipleInZ.setter
    def ElasticModulusMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        pass

    @property
    def ShearModulusMultipleInXY(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        return None

    @ShearModulusMultipleInXY.setter
    def ShearModulusMultipleInXY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        pass

    @property
    def ShearModulusMultipleInXZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        return None

    @ShearModulusMultipleInXZ.setter
    def ShearModulusMultipleInXZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        pass

    @property
    def ShearModulusMultipleInYZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        return None

    @ShearModulusMultipleInYZ.setter
    def ShearModulusMultipleInYZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        pass

    @property
    def WallSpacing(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WallSpacing.
        """
        return None

    @WallSpacing.setter
    def WallSpacing(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WallSpacing.
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
    def Volume(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Volume.
        """
        return None

    @Volume.setter
    def Volume(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Volume.
        """
        pass

    @property
    def MultiplierEntry(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]:
        """
        Gets or sets the MultiplierEntry.
        """
        return None

    @MultiplierEntry.setter
    def MultiplierEntry(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]) -> None:
        """
        Gets or sets the MultiplierEntry.
        """
        pass

    @property
    def SupportType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]:
        """
        Gets or sets the SupportType.
        """
        return None

    @SupportType.setter
    def SupportType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]) -> None:
        """
        Gets or sets the SupportType.
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

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


class PredefinedAMSupport(object):
    """
    Defines a PredefinedAMSupport.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSAMSupportAuto]:
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
    def ThermalConductivityMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        return None

    @ThermalConductivityMultipleInX.setter
    def ThermalConductivityMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInX.
        """
        pass

    @property
    def ThermalConductivityMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        return None

    @ThermalConductivityMultipleInY.setter
    def ThermalConductivityMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInY.
        """
        pass

    @property
    def ThermalConductivityMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        return None

    @ThermalConductivityMultipleInZ.setter
    def ThermalConductivityMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ThermalConductivityMultipleInZ.
        """
        pass

    @property
    def DensityMultiple(self) -> typing.Optional[float]:
        """
        Gets or sets the DensityMultiple.
        """
        return None

    @DensityMultiple.setter
    def DensityMultiple(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the DensityMultiple.
        """
        pass

    @property
    def MaterialMultiplier(self) -> typing.Optional[float]:
        """
        Gets or sets the MaterialMultiplier.
        """
        return None

    @MaterialMultiplier.setter
    def MaterialMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MaterialMultiplier.
        """
        pass

    @property
    def ElasticModulusMultipleInX(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        return None

    @ElasticModulusMultipleInX.setter
    def ElasticModulusMultipleInX(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInX.
        """
        pass

    @property
    def ElasticModulusMultipleInY(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        return None

    @ElasticModulusMultipleInY.setter
    def ElasticModulusMultipleInY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInY.
        """
        pass

    @property
    def ElasticModulusMultipleInZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        return None

    @ElasticModulusMultipleInZ.setter
    def ElasticModulusMultipleInZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ElasticModulusMultipleInZ.
        """
        pass

    @property
    def ShearModulusMultipleInXY(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        return None

    @ShearModulusMultipleInXY.setter
    def ShearModulusMultipleInXY(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXY.
        """
        pass

    @property
    def ShearModulusMultipleInXZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        return None

    @ShearModulusMultipleInXZ.setter
    def ShearModulusMultipleInXZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInXZ.
        """
        pass

    @property
    def ShearModulusMultipleInYZ(self) -> typing.Optional[float]:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        return None

    @ShearModulusMultipleInYZ.setter
    def ShearModulusMultipleInYZ(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the ShearModulusMultipleInYZ.
        """
        pass

    @property
    def WallSpacing(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the WallSpacing.
        """
        return None

    @WallSpacing.setter
    def WallSpacing(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the WallSpacing.
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
    def Volume(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the Volume.
        """
        return None

    @Volume.setter
    def Volume(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the Volume.
        """
        pass

    @property
    def MultiplierEntry(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]:
        """
        Gets or sets the MultiplierEntry.
        """
        return None

    @MultiplierEntry.setter
    def MultiplierEntry(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMMultiplierEntryType]) -> None:
        """
        Gets or sets the MultiplierEntry.
        """
        pass

    @property
    def SupportType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]:
        """
        Gets or sets the SupportType.
        """
        return None

    @SupportType.setter
    def SupportType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AMSupportType]) -> None:
        """
        Gets or sets the SupportType.
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

    def AddCommandSnippet(self) -> Ansys.ACT.Automation.Mechanical.CommandSnippet:
        """
        Creates a new CommandSnippet
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


