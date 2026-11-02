"""LinearizedStressResults module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class LinearizedStressResult(object):
    """
    Defines a LinearizedStressResult.
    """

    @property
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

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


class LinearizedEquivalentStress(object):
    """
    Defines a LinearizedEquivalentStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedMaximumPrincipalStress(object):
    """
    Defines a LinearizedMaximumPrincipalStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedMaximumShearStress(object):
    """
    Defines a LinearizedMaximumShearStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedMiddlePrincipalStress(object):
    """
    Defines a LinearizedMiddlePrincipalStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedMinimumPrincipalStress(object):
    """
    Defines a LinearizedMinimumPrincipalStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedNormalStress(object):
    """
    Defines a LinearizedNormalStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedShearStress(object):
    """
    Defines a LinearizedShearStress.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

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
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


class LinearizedStressIntensity(object):
    """
    Defines a LinearizedStressIntensity.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
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
    def ZeroThroughThicknessBendingStress(self) -> typing.Optional[bool]:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        return None

    @ZeroThroughThicknessBendingStress.setter
    def ZeroThroughThicknessBendingStress(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the ZeroThroughThicknessBendingStress.
        """
        pass

    @property
    def LoadMultiplier(self) -> typing.Optional[float]:
        """
        Gets the LoadMultiplier.
        """
        return None

    @property
    def AverageRadiusOfCurvature(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        return None

    @AverageRadiusOfCurvature.setter
    def AverageRadiusOfCurvature(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the AverageRadiusOfCurvature.
        """
        pass

    @property
    def BendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingInside.
        """
        return None

    @property
    def BendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the BendingOutside.
        """
        return None

    @property
    def MembraneBendingCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingCenter.
        """
        return None

    @property
    def MembraneBendingInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingInside.
        """
        return None

    @property
    def MembraneBendingOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the MembraneBendingOutside.
        """
        return None

    @property
    def Membrane(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Membrane.
        """
        return None

    @property
    def PeakCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakCenter.
        """
        return None

    @property
    def PeakInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakInside.
        """
        return None

    @property
    def PeakOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the PeakOutside.
        """
        return None

    @property
    def SweepingPhase(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the SweepingPhase.
        """
        return None

    @SweepingPhase.setter
    def SweepingPhase(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the SweepingPhase.
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
    def TotalCenter(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalCenter.
        """
        return None

    @property
    def TotalInside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalInside.
        """
        return None

    @property
    def TotalOutside(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the TotalOutside.
        """
        return None

    @property
    def Linearized2DBehavior(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]:
        """
        Gets or sets the Linearized2DBehavior.
        """
        return None

    @Linearized2DBehavior.setter
    def Linearized2DBehavior(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.Linearized2DBehavior]) -> None:
        """
        Gets or sets the Linearized2DBehavior.
        """
        pass

    @property
    def Subtype(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]:
        """
        Gets or sets the Subtype.
        """
        return None

    @Subtype.setter
    def Subtype(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LinearizedSubtype]) -> None:
        """
        Gets or sets the Subtype.
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
    def Position(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]:
        """
        Gets or sets the Position.
        """
        return None

    @Position.setter
    def Position(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShellFaceType]) -> None:
        """
        Gets or sets the Position.
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
    def ThroughThicknessBendingStress(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        return None

    @ThroughThicknessBendingStress.setter
    def ThroughThicknessBendingStress(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ThroughThicknessBendingStress]) -> None:
        """
        Gets or sets the ThroughThicknessBendingStress.
        """
        pass

    @property
    def Amplitude(self) -> typing.Optional[bool]:
        """
        Gets or sets the Amplitude.
        """
        return None

    @Amplitude.setter
    def Amplitude(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Amplitude.
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


