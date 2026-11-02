"""Tools module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class CurrentLegendSettings(object):
    """
    
             Represents a CurrentLegendSettings object. This object holds properties of the CurrentLegendSettings.
             
    """

    @property
    def NumberOfBands(self) -> typing.Optional[int]:
        """
        Number of bands on the legend (min:3, max:30). Bands are added/removed from the top of the legend.
        """
        return None

    @NumberOfBands.setter
    def NumberOfBands(self, value: typing.Optional[int]) -> None:
        """
        Number of bands on the legend (min:3, max:30). Bands are added/removed from the top of the legend.
        """
        pass

    @property
    def AllScientificNotation(self) -> typing.Optional[bool]:
        """
        Whether the result values are displayed in scientific notation.
        """
        return None

    @AllScientificNotation.setter
    def AllScientificNotation(self, value: typing.Optional[bool]) -> None:
        """
        Whether the result values are displayed in scientific notation.
        """
        pass

    @property
    def Digits(self) -> typing.Optional[int]:
        """
        Number of significant digits(min:2, max:8).
        """
        return None

    @Digits.setter
    def Digits(self, value: typing.Optional[int]) -> None:
        """
        Number of significant digits(min:2, max:8).
        """
        pass

    @property
    def ColorScheme(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendColorSchemeType]:
        """
        Color Scheme for the legend.
        """
        return None

    @ColorScheme.setter
    def ColorScheme(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendColorSchemeType]) -> None:
        """
        Color Scheme for the legend.
        """
        pass

    @property
    def SemiTransparency(self) -> typing.Optional[bool]:
        """
        Whether the legend is semi-transparent.
        """
        return None

    @SemiTransparency.setter
    def SemiTransparency(self, value: typing.Optional[bool]) -> None:
        """
        Whether the legend is semi-transparent.
        """
        pass

    @property
    def LogarithmicScale(self) -> typing.Optional[bool]:
        """
        Whether the result values are distributed in a Logarithmic scale.
        """
        return None

    @LogarithmicScale.setter
    def LogarithmicScale(self, value: typing.Optional[bool]) -> None:
        """
        Whether the result values are distributed in a Logarithmic scale.
        """
        pass

    @property
    def HighFidelity(self) -> typing.Optional[bool]:
        """
        Whether to replot and improve the synchronization of the result values.
        """
        return None

    @HighFidelity.setter
    def HighFidelity(self, value: typing.Optional[bool]) -> None:
        """
        Whether to replot and improve the synchronization of the result values.
        """
        pass

    @property
    def Title(self) -> typing.Optional[str]:
        """
        Title property.
        """
        return None

    @property
    def Title2(self) -> typing.Optional[str]:
        """
        Title2 property.
        """
        return None

    @property
    def Subtitles(self) -> typing.Optional[typing.List[str]]:
        """
        Subtitles property.
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def GetBandColor(self, index: int) -> int:
        """
        Gets the color of the specified band.
        """
        pass

    def SetBandColor(self, index: int, ColorValue: int) -> None:
        """
        Sets the color of the specified band.
        """
        pass

    def GetLowerBound(self, index: int) -> Ansys.Core.Units.Quantity:
        """
        Gets lower bound value of the specified band.
        """
        pass

    def SetLowerBound(self, index: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        Sets lower bound value of the specified band.
        """
        pass

    def GetUpperBound(self, index: int) -> Ansys.Core.Units.Quantity:
        """
        Gets upper bound value of the specified band.
        """
        pass

    def SetUpperBound(self, index: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        Sets upper bound value of the specified band.
        """
        pass

    def GetBandColorAuto(self, index: int) -> bool:
        """
        Gets whether the specified band is set to Automatic or not.
        """
        pass

    def SetBandColorAuto(self, index: int, val: bool) -> None:
        """
        Sets the specified band to Automatic.
        """
        pass

    def GetUpperBandValueAuto(self, index: int) -> bool:
        """
        Gets whether the specified upper band value is set to Automatic or not.
        """
        pass

    def SetUpperBandValueAuto(self, index: int, val: bool) -> None:
        """
        SetUpperBandValueAuto method.
        """
        pass

    def GetLowerBandValueAuto(self, index: int) -> bool:
        """
        Gets whether the specified lower band value is set to Automatic or not.
        """
        pass

    def SetLowerBandValueAuto(self, index: int, val: bool) -> None:
        """
        SetLowerBandValueAuto method.
        """
        pass

    def ResetColors(self) -> None:
        """
        Resets all colors to default values.
        """
        pass

    def Reset(self) -> None:
        """
        Resets all legend customizations into default values.
        """
        pass

    def MakeCopy(self) -> Ansys.Mechanical.Graphics.Tools.LegendSettings:
        """
        Makes a copy of the CurrentLegendSettings object.
        """
        pass

    def ExportLegend(self, filePath: str) -> None:
        """
        ExportLegend method.
        """
        pass


class LegendSettings(object):
    """
    
            Represents a LegendSettings object. This object holds properties of the Standalone LegendSettings.
            
    """

    @property
    def NumberOfBands(self) -> typing.Optional[int]:
        """
        Number of bands on the legend (min:3, max:30). Bands are added/removed from the top of the legend.
        """
        return None

    @NumberOfBands.setter
    def NumberOfBands(self, value: typing.Optional[int]) -> None:
        """
        Number of bands on the legend (min:3, max:30). Bands are added/removed from the top of the legend.
        """
        pass

    @property
    def Min(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Min property.
        """
        return None

    @property
    def Max(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Max property.
        """
        return None

    @property
    def AllScientificNotation(self) -> typing.Optional[bool]:
        """
        Whether the result values are displayed in scientific notation.
        """
        return None

    @AllScientificNotation.setter
    def AllScientificNotation(self, value: typing.Optional[bool]) -> None:
        """
        Whether the result values are displayed in scientific notation.
        """
        pass

    @property
    def Digits(self) -> typing.Optional[int]:
        """
        Number of significant digits (min:2 , max:8).
        """
        return None

    @Digits.setter
    def Digits(self, value: typing.Optional[int]) -> None:
        """
        Number of significant digits (min:2 , max:8).
        """
        pass

    @property
    def ColorScheme(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendColorSchemeType]:
        """
        Color Scheme for the legend.
        """
        return None

    @ColorScheme.setter
    def ColorScheme(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendColorSchemeType]) -> None:
        """
        Color Scheme for the legend.
        """
        pass

    @property
    def SemiTransparency(self) -> typing.Optional[bool]:
        """
        Whether the legend is semi-transparent.
        """
        return None

    @SemiTransparency.setter
    def SemiTransparency(self, value: typing.Optional[bool]) -> None:
        """
        Whether the legend is semi-transparent.
        """
        pass

    @property
    def LogarithmicScale(self) -> typing.Optional[bool]:
        """
        Whether the result values are distributed in a Logarithmic scale.
        """
        return None

    @LogarithmicScale.setter
    def LogarithmicScale(self, value: typing.Optional[bool]) -> None:
        """
        Whether the result values are distributed in a Logarithmic scale.
        """
        pass

    @property
    def HighFidelity(self) -> typing.Optional[bool]:
        """
        Whether to replot and improve the synchronization of the result values.
        """
        return None

    @HighFidelity.setter
    def HighFidelity(self, value: typing.Optional[bool]) -> None:
        """
        Whether to replot and improve the synchronization of the result values.
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        The unit for the legend.
        """
        return None

    def __init__(self, unit: str) -> None:
        """
        __init__ method.
        """
        pass

    def SetMinMax(self, min: Ansys.Core.Units.Quantity, max: Ansys.Core.Units.Quantity) -> None:
        """
        SetMinMax method.
        """
        pass

    def GetLowerBound(self, index: int) -> Ansys.Core.Units.Quantity:
        """
        Gets lower bound value of the specified band.
        """
        pass

    def SetLowerBound(self, index: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        Sets lower bound value of the specified band.
        """
        pass

    def GetUpperBound(self, index: int) -> Ansys.Core.Units.Quantity:
        """
        Gets upper bound value of the specified band.
        """
        pass

    def SetUpperBound(self, index: int, value: Ansys.Core.Units.Quantity) -> None:
        """
        Sets upper bound value of the specified band.
        """
        pass

    def GetBandColor(self, index: int) -> int:
        """
        Gets the color of the specified band.
        """
        pass

    def SetBandColor(self, index: int, colorValue: int) -> None:
        """
        Sets the color of the specified band.
        """
        pass

    def GetBandColorAuto(self, index: int) -> bool:
        """
        Gets whether the specified band is set to Automatic or not.
        """
        pass

    def SetBandColorAuto(self, index: int, val: bool) -> None:
        """
        Sets the specified band to Automatic.
        """
        pass

    def SetUpperBandValueAuto(self, index: int, val: bool) -> None:
        """
        SetUpperBandValueAuto method.
        """
        pass

    def GetUpperBandValueAuto(self, index: int) -> bool:
        """
        Gets whether the specified upper band value is set to Automatic or not.
        """
        pass

    def SetLowerBandValueAuto(self, index: int, val: bool) -> None:
        """
        SetLowerBandValueAuto method.
        """
        pass

    def GetLowerBandValueAuto(self, index: int) -> bool:
        """
        Gets whether the lower specified band value is set to Automatic or not.
        """
        pass

    def ResetColors(self) -> None:
        """
        Resets all colors to default values.
        """
        pass

    def Reset(self) -> None:
        """
        Resets all legend customizations into default values.
        """
        pass

    def CopyTo(self, activeLegend: Ansys.Mechanical.Graphics.Tools.CurrentLegendSettings) -> None:
        """
        CopyTo method.
        """
        pass

    def ExportLegend(self, filePath: str) -> None:
        """
        ExportLegend method.
        """
        pass


