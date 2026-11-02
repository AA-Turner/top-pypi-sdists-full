"""Charts module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ChartDisplayOptions(object):
    """
    
            A class that exposes methods/properties to customize the display settings of a chart.
            
    """

    @property
    def _displayOption(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDSChartDisplayOptions]:
        """
        _displayOption property.
        """
        return None

    @property
    def ShowLegend(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the visibility of the legend.
            
        """
        return None

    @ShowLegend.setter
    def ShowLegend(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the visibility of the legend.
            
        """
        pass

    @property
    def LegendPosition(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.LegendPosition]:
        """
        
            Gets or sets the position of the legend. The default option is "ProgramControlled".
            
        """
        return None

    @LegendPosition.setter
    def LegendPosition(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.LegendPosition]) -> None:
        """
        
            Gets or sets the position of the legend. The default option is "ProgramControlled".
            
        """
        pass

    @property
    def Title(self) -> typing.Optional[str]:
        """
        
            Gets or sets the chart title.
            
        """
        return None

    @Title.setter
    def Title(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the chart title.
            
        """
        pass

    @property
    def TitleFontSize(self) -> typing.Optional[int]:
        """
        
            Gets or sets the font size of the chart title.
            An ArgumentException is thrown for values less than 1.
            
        """
        return None

    @TitleFontSize.setter
    def TitleFontSize(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the font size of the chart title.
            An ArgumentException is thrown for values less than 1.
            
        """
        pass

    def __init__(self, variable: Ansys.Common.Interop.DSUtils.IDSChartDisplayOptions) -> None:
        """
        __init__ method.
        """
        pass

    def CopySettingsFrom(self, display_options_original: Ansys.Mechanical.DataModel.Utilities.Charts.ChartDisplayOptions) -> None:
        """
        
            Copies the settings used in the input ChartDisplayOptions reference to the ChartDisplayOptions calling this method.
            
        """
        pass


class LabelCollection(object):
    """
    
            A class to manage labels on the chart.
            
    """

    @property
    def Labels(self) -> typing.Optional[typing.Iterable[Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo]]:
        """
        
            Gets an IEnumerable of ILabelInfo objects, which contain information about the underlying label 
            
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDSChartLabelCollection]:
        """
        InternalObject property.
        """
        return None

    def CreateAndAddLabel(self, x_anchor: Ansys.Core.Units.Quantity, y_anchor: Ansys.Core.Units.Quantity, label_text: str) -> Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo:
        """
        
            Creates a new label and adds it to the chart at a specified position, where the label_text parameter is optional. 
            The default label text is: “x: <x_value>, y: <y_value>” (example: “x: 0.3497, y: 1.9821”).  
            An InvalidOperationException will be thrown when creating a Label at a location already assigned to another Label.
            
        """
        pass

    def DeleteLabel(self, label: Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo) -> None:
        """
        
            Deletes a label from a specific position in the chart. 
            An InvalidOperationException will be thrown when deleting a Label that does not exist.
            
        """
        pass

    def CreateLabelOnSegment(self, data_point_index: int, fractional_distance: float) -> Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo:
        """
        
            Create a label on the segment of the dataset starting from the data point at a specified distance along the segment. 
            Distance values are fractional going from 0 to 1 (first datapoint at 0) along the length of the segment
            An ArgumentException will be thrown when creating a Label at a location already assigned to another Label.
            
        """
        pass

    def CreateLabelsAtXCoordinate(self, x_anchor: Ansys.Core.Units.Quantity) -> typing.List[Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo]:
        """
        
            Creates label(s) on the dataset at a specified X coordinate. 
            This API may return multiple `LabelInfo` references in case the corresponding dataset has more than one Y-value for the given X-value (for eg. Spiral graphs). 
            Each `LabelInfo` reference corresponds to the multiple anchor positions thus obtained. 
            An ArgumentException will be thrown when creating a Label at a location already assigned to another Label.
            
        """
        pass

    def CreateLabelsAtYCoordinate(self, y_anchor: Ansys.Core.Units.Quantity) -> typing.List[Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection.LabelInfo]:
        """
        
            Creates label(s) on the dataset at a specified Y coordinate. 
            This API may return multiple `LabelInfo` references in case the corresponding dataset has more than one X-value for a given Y-value. 
            Each `LabelInfo` reference corresponds to the multiple anchor positions thus obtained. 
            An ArgumentException will be thrown when creating a Label at a location already assigned to another Label.
            
        """
        pass


class ReadOnlyChart(object):
    """
    
            ReadOnlyChart is used by objects to display data as a chart.
            The data itself is treated as read only and cannot be modified.
            Additional options are provided to customize the presentation of the data itself.
            
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDSCharts]:
        """
        InternalObject property.
        """
        return None

    @InternalObject.setter
    def InternalObject(self, value: typing.Optional[Ansys.Common.Interop.DSUtils.IDSCharts]) -> None:
        """
        InternalObject property.
        """
        pass

    @property
    def Datasets(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D]]:
        """
        
            Retrieves all datasets of a chart.
            
        """
        return None

    @property
    def XAxisDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.AxisDisplayOptions]:
        """
        
            Returns a reference to the x-axis display options of a chart.
            
        """
        return None

    @property
    def YAxisDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.AxisDisplayOptions]:
        """
        
            Returns a reference to the y-axis display options of a chart.
            
        """
        return None

    @property
    def NormalizeYAxis(self) -> typing.Optional[bool]:
        """
        
            Allows a normalized display of y-axis values, usually for cases where the axis has mixed quantities.
            An InvalidOperationException will be thrown if attempting to set to False,
            when the Y axis datasets have incompatible Quantity types and the UseAutomaticLimits property is also set to False.
            
        """
        return None

    @NormalizeYAxis.setter
    def NormalizeYAxis(self, value: typing.Optional[bool]) -> None:
        """
        
            Allows a normalized display of y-axis values, usually for cases where the axis has mixed quantities.
            An InvalidOperationException will be thrown if attempting to set to False,
            when the Y axis datasets have incompatible Quantity types and the UseAutomaticLimits property is also set to False.
            
        """
        pass

    @property
    def ChartDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.ChartDisplayOptions]:
        """
        
            Returns a reference to the display options of a chart.
            
        """
        return None

    def GetDisplayOptionsForDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D) -> Ansys.Mechanical.DataModel.Utilities.Charts.Dataset2DDisplayOptions:
        """
        
            Returns a reference to the dataset display options for a specific dataset.
            
        """
        pass

    def GetLabelCollectionForDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D) -> Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection:
        """
        
            Returns a reference to the label collection for a specific dataset.
            
        """
        pass


class Chart(object):
    """
    
            Chart is an object utilized by the Line Chart object to display charts and
            customize them with the flexibility to allow modification to the data of the chart
            to a certain extent. 
            
    """

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDSCharts]:
        """
        InternalObject property.
        """
        return None

    @InternalObject.setter
    def InternalObject(self, value: typing.Optional[Ansys.Common.Interop.DSUtils.IDSCharts]) -> None:
        """
        InternalObject property.
        """
        pass

    @property
    def Datasets(self) -> typing.Optional[typing.List[Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D]]:
        """
        
            Retrieves all datasets of a chart.
            
        """
        return None

    @property
    def XAxisDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.AxisDisplayOptions]:
        """
        
            Returns a reference to the x-axis display options of a chart.
            
        """
        return None

    @property
    def YAxisDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.AxisDisplayOptions]:
        """
        
            Returns a reference to the y-axis display options of a chart.
            
        """
        return None

    @property
    def NormalizeYAxis(self) -> typing.Optional[bool]:
        """
        
            Allows a normalized display of y-axis values, usually for cases where the axis has mixed quantities.
            An InvalidOperationException will be thrown if attempting to set to False,
            when the Y axis datasets have incompatible Quantity types and the UseAutomaticLimits property is also set to False.
            
        """
        return None

    @NormalizeYAxis.setter
    def NormalizeYAxis(self, value: typing.Optional[bool]) -> None:
        """
        
            Allows a normalized display of y-axis values, usually for cases where the axis has mixed quantities.
            An InvalidOperationException will be thrown if attempting to set to False,
            when the Y axis datasets have incompatible Quantity types and the UseAutomaticLimits property is also set to False.
            
        """
        pass

    @property
    def ChartDisplayOptions(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.Charts.ChartDisplayOptions]:
        """
        
            Returns a reference to the display options of a chart.
            
        """
        return None

    def AddDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D, name: str) -> None:
        """
        
            Adds a dataset to a chart, provided the data is valid.
            Adding a name for the dataset is optional, the default name for the nth dataset added is “Series n”.
            An InvalidOperationException is thrown if the dataset is either invalid, already added to the chart,
            or contains non-positive values when the chart has IsLogarithmic enabled.
            
        """
        pass

    def RemoveDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D) -> None:
        """
        
            Removes a dataset from the chart.
            
        """
        pass

    def GetDisplayOptionsForDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D) -> Ansys.Mechanical.DataModel.Utilities.Charts.Dataset2DDisplayOptions:
        """
        
            Returns a reference to the dataset display options for a specific dataset.
            
        """
        pass

    def GetLabelCollectionForDataset(self, dataset: Ansys.Mechanical.DataModel.Utilities.Dataset.Dataset2D) -> Ansys.Mechanical.DataModel.Utilities.Charts.LabelCollection:
        """
        
            Returns a reference to the label collection for a specific dataset.
            
        """
        pass


class AxisDisplayOptions(object):
    """
    
            A class that exposes methods/properties to customize the display of a chart axis. 
            
    """

    @property
    def _axisDisplayOption(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDSAxisDisplayOptions]:
        """
        _axisDisplayOption property.
        """
        return None

    @property
    def AxisLabel(self) -> typing.Optional[str]:
        """
        
            Gets or sets the axis label.
            
        """
        return None

    @AxisLabel.setter
    def AxisLabel(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the axis label.
            
        """
        pass

    @property
    def ShowGridLines(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the visibility of the axis gridlines.
            
        """
        return None

    @ShowGridLines.setter
    def ShowGridLines(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the visibility of the axis gridlines.
            
        """
        pass

    @property
    def IsLogarithmic(self) -> typing.Optional[bool]:
        """
        
            Gets or sets whether the axis is logarithmic.
            A NotSupportedException is thrown if a dataset contains a non-positive value on the chosen axis.
            
        """
        return None

    @IsLogarithmic.setter
    def IsLogarithmic(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets whether the axis is logarithmic.
            A NotSupportedException is thrown if a dataset contains a non-positive value on the chosen axis.
            
        """
        pass

    @property
    def ShowScrollBarOnZoom(self) -> typing.Optional[bool]:
        """
        ShowScrollBarOnZoom property.
        """
        return None

    @ShowScrollBarOnZoom.setter
    def ShowScrollBarOnZoom(self, value: typing.Optional[bool]) -> None:
        """
        ShowScrollBarOnZoom property.
        """
        pass

    @property
    def UseAutomaticLimits(self) -> typing.Optional[bool]:
        """
        
            Gets or sets whether axis limits are automatic or user-defined.
            When True, the MinimumLimit and MaximumLimit will be set to the LowerLimit and UpperLimit respectively.
            
        """
        return None

    @UseAutomaticLimits.setter
    def UseAutomaticLimits(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets whether axis limits are automatic or user-defined.
            When True, the MinimumLimit and MaximumLimit will be set to the LowerLimit and UpperLimit respectively.
            
        """
        pass

    @property
    def MinimumLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the Minimum limit used for the chart display.
            If UseAutomaticLimits is True, a NotSupportedException is thrown on the setter.
            
        """
        return None

    @MinimumLimit.setter
    def MinimumLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the Minimum limit used for the chart display.
            If UseAutomaticLimits is True, a NotSupportedException is thrown on the setter.
            
        """
        pass

    @property
    def MaximumLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or sets the Maximum limit used for the chart display.
            If UseAutomaticLimits is True, a NotSupportedException is thrown on the setter.
            
        """
        return None

    @MaximumLimit.setter
    def MaximumLimit(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or sets the Maximum limit used for the chart display.
            If UseAutomaticLimits is True, a NotSupportedException is thrown on the setter.
            
        """
        pass

    @property
    def LowerLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets the default lower limit of the axis range.
            
        """
        return None

    @property
    def UpperLimit(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets the default higher limit of the axis range.
            
        """
        return None

    def CopySettingsFrom(self, display_options_original: Ansys.Mechanical.DataModel.Utilities.Charts.AxisDisplayOptions) -> None:
        """
        
            Copies the settings used in the input AxisDisplayOptions reference to the AxisDisplayOptions calling this method.
            
        """
        pass


class Dataset2DDisplayOptions(object):
    """
    
            A class that exposes methods/properties to customize the display of a dataset on the chart.
            
    """

    @property
    def _displayOption(self) -> typing.Optional[Ansys.Common.Interop.DSUtils.IDS2DDatasetDisplayOptions]:
        """
        _displayOption property.
        """
        return None

    @property
    def LineType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.LineType]:
        """
        
            Gets or sets the Dataset2D Line display type 
            
        """
        return None

    @LineType.setter
    def LineType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.LineType]) -> None:
        """
        
            Gets or sets the Dataset2D Line display type 
            
        """
        pass

    @property
    def DatasetType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.Chart2DDatasetType]:
        """
        DatasetType property.
        """
        return None

    @DatasetType.setter
    def DatasetType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.Chart2DDatasetType]) -> None:
        """
        DatasetType property.
        """
        pass

    @property
    def Color(self) -> typing.Optional[int]:
        """
        
            Gets or sets the Dataset2D Color 
            
        """
        return None

    @Color.setter
    def Color(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the Dataset2D Color 
            
        """
        pass

    @property
    def LineThickness(self) -> typing.Optional[float]:
        """
        
            Gets or sets the Dataset2D line thickness (in pixels) 
            
            An ArgumentException is thrown for values less than 1.
            
        """
        return None

    @LineThickness.setter
    def LineThickness(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the Dataset2D line thickness (in pixels) 
            
            An ArgumentException is thrown for values less than 1.
            
        """
        pass

    @property
    def MarkerShape(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.MarkerShape]:
        """
        
            Gets or sets the Dataset2D marker shape 
            
        """
        return None

    @MarkerShape.setter
    def MarkerShape(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Charts.Dataset2D.MarkerShape]) -> None:
        """
        
            Gets or sets the Dataset2D marker shape 
            
        """
        pass

    @property
    def MarkerSize(self) -> typing.Optional[float]:
        """
        
            Gets or sets the Dataset2D marker size (in pixels)
            
        """
        return None

    @MarkerSize.setter
    def MarkerSize(self, value: typing.Optional[float]) -> None:
        """
        
            Gets or sets the Dataset2D marker size (in pixels)
            
        """
        pass

    @property
    def IsVisible(self) -> typing.Optional[bool]:
        """
        
            Gets or sets the visibility of the Dataset2D
            
        """
        return None

    @IsVisible.setter
    def IsVisible(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or sets the visibility of the Dataset2D
            
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the Dataset2D name 
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the Dataset2D name 
            
        """
        pass

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, variable: Ansys.Common.Interop.DSUtils.IDS2DDatasetDisplayOptions) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass

    def CopySettingsFrom(self, input_display_options: Ansys.Mechanical.DataModel.Utilities.Charts.Dataset2DDisplayOptions) -> None:
        """
        
            Copies the settings of a Dataset2DDisplayOptions reference to this Dataset2DDisplayOptions . 
            
        """
        pass


class ChartVariable(object):
    """
    
            Chart Variable enables user to create a list of values that can be used to construct a dataset object.
            
    """

    @property
    def Item(self) -> typing.Optional[float]:
        """
        Item property.
        """
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        Unit property.
        """
        return None

    @property
    def QuantityName(self) -> typing.Optional[str]:
        """
        QuantityName property.
        """
        return None

    @property
    def Count(self) -> typing.Optional[int]:
        """
        Count property.
        """
        return None

    @typing.overload
    def __init__(self, vals: typing.Iterable[typing.Any], quantity_name: str, unit: str) -> None:
        ...

    @typing.overload
    def __init__(self, vals: Ansys.Mechanical.Interfaces.IDataSeries) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        __init__ method.
        """
        pass


class LabelInfo(object):

    @property
    def X(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        X property.
        """
        return None

    @property
    def Y(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Y property.
        """
        return None

    @property
    def XDisplay(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        XDisplay property.
        """
        return None

    @property
    def YDisplay(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        YDisplay property.
        """
        return None

    @property
    def Text(self) -> typing.Optional[str]:
        """
        Text property.
        """
        return None

    @Text.setter
    def Text(self, value: typing.Optional[str]) -> None:
        """
        Text property.
        """
        pass

    @property
    def FormattedLabelText(self) -> typing.Optional[str]:
        """
        FormattedLabelText property.
        """
        return None

    @classmethod
    @property
    def DefaultText(cls) -> typing.Optional[str]:
        """
        DefaultText property.
        """
        return 'x: {xvalue} [{xunit}] y: {yvalue} [{yunit}]'

    @property
    def IsVisible(self) -> typing.Optional[bool]:
        """
        IsVisible property.
        """
        return None

    @IsVisible.setter
    def IsVisible(self, value: typing.Optional[bool]) -> None:
        """
        IsVisible property.
        """
        pass

    def Move(self, x_display: Ansys.Core.Units.Quantity, y_display: Ansys.Core.Units.Quantity) -> None:
        """
        
            Moves the label to the position on the X axis and the Y axis. An InvalidOperationException will be thrown when moving a Label that does not exist.
            
        """
        pass


