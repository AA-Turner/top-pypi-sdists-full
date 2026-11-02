"""FrequencyResponseResults module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class EquivalentRadiatedPowerWaterfallDiagram(object):
    """
    Defines a EquivalentRadiatedPowerWaterfallDiagram.
    """

    @property
    def ErpFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]:
        """
        Gets or sets the ErpFormulation.
        """
        return None

    @ErpFormulation.setter
    def ErpFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]) -> None:
        """
        Gets or sets the ErpFormulation.
        """
        pass

    @property
    def RpmSelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the RpmSelectionUnit.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def RpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RpmSelection.
        """
        return None

    @RpmSelection.setter
    def RpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RpmSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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


class EquivalentRadiatedPower(object):
    """
    Defines a EquivalentRadiatedPower.
    """

    @property
    def ErpFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]:
        """
        Gets or sets the ErpFormulation.
        """
        return None

    @ErpFormulation.setter
    def ErpFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]) -> None:
        """
        Gets or sets the ErpFormulation.
        """
        pass

    @property
    def FrequencySelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the FrequencySelectionUnit.
        """
        return None

    @property
    def Charts(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Mechanical.IReadOnlyChart]]:
        """
        Charts property.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

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
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def FrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the FrequencyRange.
        """
        return None

    @FrequencyRange.setter
    def FrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FrequencyRange.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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

    def GetNumberOfCharts(self) -> int:
        """
        GetNumberOfCharts method.
        """
        pass

    def GetGraphInteractionEvent(self, ppEventArgs: typing.Any, chartIndex: int) -> None:
        """
        GetGraphInteractionEvent method.
        """
        pass

    def SetGraphInteractionEvent(self, pEventArgs: typing.Any, chartIndex: int) -> None:
        """
        SetGraphInteractionEvent method.
        """
        pass

    def GetChartAxisDisplayUnit(self, chart_idx: int, axis_id: int) -> str:
        """
        GetChartAxisDisplayUnit method.
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


class AccelerationWaterfallDiagram(object):
    """
    Defines a AccelerationWaterfallDiagram.
    """

    @property
    def RpmSelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the RpmSelectionUnit.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def STFTNumberSlice(self) -> typing.Optional[int]:
        """
        Gets or sets the STFTNumberSlice.
        """
        return None

    @STFTNumberSlice.setter
    def STFTNumberSlice(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the STFTNumberSlice.
        """
        pass

    @property
    def STFTOverlap(self) -> typing.Optional[float]:
        """
        Gets or sets the STFTOverlap.
        """
        return None

    @STFTOverlap.setter
    def STFTOverlap(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the STFTOverlap.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def RpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RpmSelection.
        """
        return None

    @RpmSelection.setter
    def RpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RpmSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def STFTCutoffFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        return None

    @STFTCutoffFrequency.setter
    def STFTCutoffFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        pass

    @property
    def STFTEndTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTEndTime.
        """
        return None

    @STFTEndTime.setter
    def STFTEndTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTEndTime.
        """
        pass

    @property
    def STFTMinFreqResolution(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        return None

    @STFTMinFreqResolution.setter
    def STFTMinFreqResolution(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        pass

    @property
    def STFTStartTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTStartTime.
        """
        return None

    @STFTStartTime.setter
    def STFTStartTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTStartTime.
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
    def STFTWindowType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]:
        """
        Gets or sets the STFTWindowType.
        """
        return None

    @STFTWindowType.setter
    def STFTWindowType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]) -> None:
        """
        Gets or sets the STFTWindowType.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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


class VelocityWaterfallDiagram(object):
    """
    Defines a VelocityWaterfallDiagram.
    """

    @property
    def RpmSelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the RpmSelectionUnit.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def STFTNumberSlice(self) -> typing.Optional[int]:
        """
        Gets or sets the STFTNumberSlice.
        """
        return None

    @STFTNumberSlice.setter
    def STFTNumberSlice(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the STFTNumberSlice.
        """
        pass

    @property
    def STFTOverlap(self) -> typing.Optional[float]:
        """
        Gets or sets the STFTOverlap.
        """
        return None

    @STFTOverlap.setter
    def STFTOverlap(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the STFTOverlap.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def RpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RpmSelection.
        """
        return None

    @RpmSelection.setter
    def RpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RpmSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def STFTCutoffFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        return None

    @STFTCutoffFrequency.setter
    def STFTCutoffFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        pass

    @property
    def STFTEndTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTEndTime.
        """
        return None

    @STFTEndTime.setter
    def STFTEndTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTEndTime.
        """
        pass

    @property
    def STFTMinFreqResolution(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        return None

    @STFTMinFreqResolution.setter
    def STFTMinFreqResolution(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        pass

    @property
    def STFTStartTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTStartTime.
        """
        return None

    @STFTStartTime.setter
    def STFTStartTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTStartTime.
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
    def STFTWindowType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]:
        """
        Gets or sets the STFTWindowType.
        """
        return None

    @STFTWindowType.setter
    def STFTWindowType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]) -> None:
        """
        Gets or sets the STFTWindowType.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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


class MCFWaterfallDiagram(object):
    """
    Defines a MCFWaterfallDiagram.
    """

    @property
    def FrequencySelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the FrequencySelectionUnit.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def ModesToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the ModesToDisplay.
        """
        return None

    @ModesToDisplay.setter
    def ModesToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ModesToDisplay.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayMode(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMode.
        """
        return None

    @DisplayMode.setter
    def DisplayMode(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMode.
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


class FrequencyResponseResultChart(object):
    """
    Defines a FrequencyResponseResultChart.
    """

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
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


class AcousticSPLFrequencyResponse(object):
    """
    Defines a AcousticSPLFrequencyResponse.
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

    def ExportToXMLFile(self, filePath: str) -> None:
        """
        Run the ExportToXMLFile action.
        """
        pass

    def ExportToWAVFile(self, filePath: str) -> None:
        """
        Run the ExportToWAVFile action.
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


class EquivalentRadiatedPowerLevel(object):
    """
    Defines a EquivalentRadiatedPowerLevel.
    """

    @property
    def ErpFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]:
        """
        Gets or sets the ErpFormulation.
        """
        return None

    @ErpFormulation.setter
    def ErpFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]) -> None:
        """
        Gets or sets the ErpFormulation.
        """
        pass

    @property
    def DBWeighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DBWeightingType]:
        """
        Gets or sets the DBWeighting.
        """
        return None

    @DBWeighting.setter
    def DBWeighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DBWeightingType]) -> None:
        """
        Gets or sets the DBWeighting.
        """
        pass

    @property
    def FrequencySelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the FrequencySelectionUnit.
        """
        return None

    @property
    def Charts(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Mechanical.IReadOnlyChart]]:
        """
        Charts property.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

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
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def FrequencyRange(self) -> typing.Optional[bool]:
        """
        Gets or sets the FrequencyRange.
        """
        return None

    @FrequencyRange.setter
    def FrequencyRange(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the FrequencyRange.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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

    def ExportToXMLFile(self, filePath: str) -> None:
        """
        Run the ExportToXMLFile action.
        """
        pass

    def ExportToWAVFile(self, filePath: str) -> None:
        """
        Run the ExportToWAVFile action.
        """
        pass

    def GetNumberOfCharts(self) -> int:
        """
        GetNumberOfCharts method.
        """
        pass

    def GetGraphInteractionEvent(self, ppEventArgs: typing.Any, chartIndex: int) -> None:
        """
        GetGraphInteractionEvent method.
        """
        pass

    def SetGraphInteractionEvent(self, pEventArgs: typing.Any, chartIndex: int) -> None:
        """
        SetGraphInteractionEvent method.
        """
        pass

    def GetChartAxisDisplayUnit(self, chart_idx: int, axis_id: int) -> str:
        """
        GetChartAxisDisplayUnit method.
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


class EquivalentRadiatedPowerLevelWaterfallDiagram(object):
    """
    Defines a EquivalentRadiatedPowerLevelWaterfallDiagram.
    """

    @property
    def ErpFormulation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]:
        """
        Gets or sets the ErpFormulation.
        """
        return None

    @ErpFormulation.setter
    def ErpFormulation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ErpFormulationType]) -> None:
        """
        Gets or sets the ErpFormulation.
        """
        pass

    @property
    def DBWeighting(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DBWeightingType]:
        """
        Gets or sets the DBWeighting.
        """
        return None

    @DBWeighting.setter
    def DBWeighting(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.DBWeightingType]) -> None:
        """
        Gets or sets the DBWeighting.
        """
        pass

    @property
    def RpmSelectionUnit(self) -> typing.Optional[str]:
        """
        Gets the RpmSelectionUnit.
        """
        return None

    @property
    def PanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the PanelContribution.
        """
        return None

    @PanelContribution.setter
    def PanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the PanelContribution.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def RpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RpmSelection.
        """
        return None

    @RpmSelection.setter
    def RpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RpmSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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

    def ExportToXMLFile(self, filePath: str) -> None:
        """
        Run the ExportToXMLFile action.
        """
        pass

    def ExportToWAVFile(self, filePath: str) -> None:
        """
        Run the ExportToWAVFile action.
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


class KrylovResidualNorm(object):
    """
    Defines a KrylovResidualNorm.
    """

    @property
    def MaximumResidual(self) -> typing.Optional[float]:
        """
        Gets the Maximum Residual value across the frequency range.
        """
        return None

    @property
    def FrequencyAtMaximumResidual(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets the Frequency at which the Residual is maximum.
        """
        return None

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class AccelerationFrequencyResponse(object):
    """
    Defines a AccelerationFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def ModeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the ModeSelection.
        """
        return None

    @ModeSelection.setter
    def ModeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ModeSelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def ModesToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the ModesToDisplay.
        """
        return None

    @ModesToDisplay.setter
    def ModesToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ModesToDisplay.
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
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayMode(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMode.
        """
        return None

    @DisplayMode.setter
    def DisplayMode(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMode.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class AcousticAWeightedSPLFrequencyResponse(object):
    """
    Defines a AcousticAWeightedSPLFrequencyResponse.
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


class AcousticKineticEnergyFrequencyResponse(object):
    """
    Defines a AcousticKineticEnergyFrequencyResponse.
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


class AcousticPotentialEnergyFrequencyResponse(object):
    """
    Defines a AcousticPotentialEnergyFrequencyResponse.
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


class AcousticPressureFrequencyResponse(object):
    """
    Defines a AcousticPressureFrequencyResponse.
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


class AcousticVelocityFrequencyResponse(object):
    """
    Defines a AcousticVelocityFrequencyResponse.
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


class ChargeReactionFrequencyResponse(object):
    """
    Defines a ChargeReactionFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LocationMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]:
        """
        Gets or sets the LocationMethod.
        """
        return None

    @LocationMethod.setter
    def LocationMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]) -> None:
        """
        Gets or sets the LocationMethod.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class DeformationFrequencyResponse(object):
    """
    Defines a DeformationFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def ModeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the ModeSelection.
        """
        return None

    @ModeSelection.setter
    def ModeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ModeSelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def ModesToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the ModesToDisplay.
        """
        return None

    @ModesToDisplay.setter
    def ModesToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ModesToDisplay.
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
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayMode(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMode.
        """
        return None

    @DisplayMode.setter
    def DisplayMode(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMode.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class DisplacementWaterfallDiagram(object):
    """
    Defines a DisplacementWaterfallDiagram.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def STFTNumberSlice(self) -> typing.Optional[int]:
        """
        Gets or sets the STFTNumberSlice.
        """
        return None

    @STFTNumberSlice.setter
    def STFTNumberSlice(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the STFTNumberSlice.
        """
        pass

    @property
    def STFTOverlap(self) -> typing.Optional[float]:
        """
        Gets or sets the STFTOverlap.
        """
        return None

    @STFTOverlap.setter
    def STFTOverlap(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the STFTOverlap.
        """
        pass

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def RpmSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the RpmSelection.
        """
        return None

    @RpmSelection.setter
    def RpmSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the RpmSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def STFTCutoffFrequency(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        return None

    @STFTCutoffFrequency.setter
    def STFTCutoffFrequency(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTCutoffFrequency.
        """
        pass

    @property
    def STFTEndTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTEndTime.
        """
        return None

    @STFTEndTime.setter
    def STFTEndTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTEndTime.
        """
        pass

    @property
    def STFTMinFreqResolution(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        return None

    @STFTMinFreqResolution.setter
    def STFTMinFreqResolution(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTMinFreqResolution.
        """
        pass

    @property
    def STFTStartTime(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Gets or sets the STFTStartTime.
        """
        return None

    @STFTStartTime.setter
    def STFTStartTime(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Gets or sets the STFTStartTime.
        """
        pass

    @property
    def SpatialResolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]:
        """
        Gets or sets how solution data from multiple nodes for the given scoping are combined into a single representative result. The default is Use Average.
        """
        return None

    @SpatialResolution.setter
    def SpatialResolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.MultipleNodeType]) -> None:
        """
        Gets or sets how solution data from multiple nodes for the given scoping are combined into a single representative result. The default is Use Average.
        """
        pass

    @property
    def NormalOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]:
        """
        Gets or sets the directional component(s) of the displacement vector used for plotting.
        """
        return None

    @NormalOrientation.setter
    def NormalOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.NormalOrientationType]) -> None:
        """
        Gets or sets the directional component(s) of the displacement vector used for plotting.
        """
        pass

    @property
    def STFTWindowType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]:
        """
        Gets or sets the STFTWindowType.
        """
        return None

    @STFTWindowType.setter
    def STFTWindowType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.WindowType]) -> None:
        """
        Gets or sets the STFTWindowType.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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


class ElasticStrainFrequencyResponse(object):
    """
    Defines a ElasticStrainFrequencyResponse.
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
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class EnergyContribution(object):
    """
    Defines a EnergyContribution.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def ModeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the ModeSelection.
        """
        return None

    @ModeSelection.setter
    def ModeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ModeSelection.
        """
        pass

    @property
    def TopBodiesToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the TopBodiesToDisplay.
        """
        return None

    @TopBodiesToDisplay.setter
    def TopBodiesToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the TopBodiesToDisplay.
        """
        pass

    @property
    def EnergyType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.EnergyContributionEnergyType]:
        """
        Gets or sets the EnergyType.
        """
        return None

    @EnergyType.setter
    def EnergyType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.EnergyContributionEnergyType]) -> None:
        """
        Gets or sets the EnergyType.
        """
        pass

    @property
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
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


class ForceReactionFrequencyResponse(object):
    """
    Defines a ForceReactionFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LocationMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]:
        """
        Gets or sets the LocationMethod.
        """
        return None

    @LocationMethod.setter
    def LocationMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]) -> None:
        """
        Gets or sets the LocationMethod.
        """
        pass

    @property
    def Beam(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Beam]:
        """
        Gets or sets the Beam.
        """
        return None

    @Beam.setter
    def Beam(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.Connections.Beam]) -> None:
        """
        Gets or sets the Beam.
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
    def RemotePoint(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePoint.
        """
        return None

    @RemotePoint.setter
    def RemotePoint(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePoint.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class ImpedanceFrequencyResponse(object):
    """
    Defines a ImpedanceFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def LocationMethod(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]:
        """
        Gets or sets the LocationMethod.
        """
        return None

    @LocationMethod.setter
    def LocationMethod(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LocationDefinitionMethod]) -> None:
        """
        Gets or sets the LocationMethod.
        """
        pass

    @property
    def DataModelObjectCategory(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.DataModelObjectCategory]:
        """
        Gets the current DataModelObject's category.
        """
        return None

    @property
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class StressFrequencyResponse(object):
    """
    Defines a StressFrequencyResponse.
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
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class VelocityFrequencyResponse(object):
    """
    Defines a VelocityFrequencyResponse.
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSObjectsAuto.IDSResultChartAuto]:
        """
        Gets the internal object. For advanced usage only.
        """
        return None

    @property
    def FrequencySelection(self) -> typing.Optional[str]:
        """
        Gets or sets the FrequencySelection.
        """
        return None

    @FrequencySelection.setter
    def FrequencySelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the FrequencySelection.
        """
        pass

    @property
    def ModeSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the ModeSelection.
        """
        return None

    @ModeSelection.setter
    def ModeSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the ModeSelection.
        """
        pass

    @property
    def OrderSelection(self) -> typing.Optional[str]:
        """
        Gets or sets the OrderSelection.
        """
        return None

    @OrderSelection.setter
    def OrderSelection(self, value: typing.Optional[str]) -> None:
        """
        Gets or sets the OrderSelection.
        """
        pass

    @property
    def OrdersToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the OrdersToDisplay.
        """
        return None

    @OrdersToDisplay.setter
    def OrdersToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the OrdersToDisplay.
        """
        pass

    @property
    def PanelsToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the PanelsToDisplay.
        """
        return None

    @PanelsToDisplay.setter
    def PanelsToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the PanelsToDisplay.
        """
        pass

    @property
    def MosaicChartLegendMax(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        return None

    @MosaicChartLegendMax.setter
    def MosaicChartLegendMax(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMax.
        """
        pass

    @property
    def MosaicChartLegendMin(self) -> typing.Optional[float]:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        return None

    @MosaicChartLegendMin.setter
    def MosaicChartLegendMin(self, value: typing.Optional[float]) -> None:
        """
        Gets or sets the MosaicChartLegendMin.
        """
        pass

    @property
    def ModesToDisplay(self) -> typing.Optional[int]:
        """
        Gets or sets the ModesToDisplay.
        """
        return None

    @ModesToDisplay.setter
    def ModesToDisplay(self, value: typing.Optional[int]) -> None:
        """
        Gets or sets the ModesToDisplay.
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
    def ShowTextOnMosaic(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        return None

    @ShowTextOnMosaic.setter
    def ShowTextOnMosaic(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ShowTextOnMosaicMode]) -> None:
        """
        Gets or sets the ShowTextOnMosaic.
        """
        pass

    @property
    def DisplayMode(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayMode.
        """
        return None

    @DisplayMode.setter
    def DisplayMode(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayMode.
        """
        pass

    @property
    def DisplayOrder(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayOrder.
        """
        return None

    @DisplayOrder.setter
    def DisplayOrder(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayOrder.
        """
        pass

    @property
    def DisplayPanel(self) -> typing.Optional[bool]:
        """
        Gets or sets the DisplayPanel.
        """
        return None

    @DisplayPanel.setter
    def DisplayPanel(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the DisplayPanel.
        """
        pass

    @property
    def UseModeContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UseModeContribution.
        """
        return None

    @UseModeContribution.setter
    def UseModeContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UseModeContribution.
        """
        pass

    @property
    def UsePanelContribution(self) -> typing.Optional[bool]:
        """
        Gets or sets the UsePanelContribution.
        """
        return None

    @UsePanelContribution.setter
    def UsePanelContribution(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the UsePanelContribution.
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
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


class VoltageFrequencyResponse(object):
    """
    Defines a VoltageFrequencyResponse.
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
    def CoordinateSystem(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        return None

    @CoordinateSystem.setter
    def CoordinateSystem(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.CoordinateSystem]) -> None:
        """
        Gets or sets the CoordinateSystem. Accepts/Returns None if it is the Solution Coordinate System.
        """
        pass

    @property
    def TabularData(self) -> typing.Optional[Ansys.Mechanical.Interfaces.ITable]:
        """
        Gets the tabular data of the result.  Use a to get index to each column of the tabular data.
        """
        return None

    @property
    def RemotePointSelection(self) -> typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]:
        """
        Gets or sets the RemotePointSelection.
        """
        return None

    @RemotePointSelection.setter
    def RemotePointSelection(self, value: typing.Optional[Ansys.ACT.Automation.Mechanical.RemotePoint]) -> None:
        """
        Gets or sets the RemotePointSelection.
        """
        pass

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


