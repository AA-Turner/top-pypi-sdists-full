"""Graphics module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v242.Ansys.Mechanical.Graphics.Tools as Tools


class GraphicsViewportsExportSettings(object):
    """
    
            Settings object to control Graphics.ExportViewports behavior.
            
    """

    @property
    def BorderStyle(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsViewportsExportBorderStyle]:
        """
        
            Specifies which borders to add, if any, to the exported viewports image.
            Border style enum values can be combined via bitwise-or ( | ).
            Defaults to None.
            
        """
        return None

    @BorderStyle.setter
    def BorderStyle(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsViewportsExportBorderStyle]) -> None:
        """
        
            Specifies which borders to add, if any, to the exported viewports image.
            Border style enum values can be combined via bitwise-or ( | ).
            Defaults to None.
            
        """
        pass

    @property
    def CurrentGraphicsDisplay(self) -> typing.Optional[bool]:
        """
        
            Specifies whether to use the current graphics display settings. Defaults to true.
            
        """
        return None

    @CurrentGraphicsDisplay.setter
    def CurrentGraphicsDisplay(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether to use the current graphics display settings. Defaults to true.
            
        """
        pass

    @property
    def AppendGraph(self) -> typing.Optional[bool]:
        """
        
            Specifies whether to append the viewport graph(s) to the exported image. Defaults to false.
            
        """
        return None

    @AppendGraph.setter
    def AppendGraph(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether to append the viewport graph(s) to the exported image. Defaults to false.
            
        """
        pass

    @property
    def Resolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType]:
        """
        
            Specifies the resolution type. Defaults to NormalResolution.
            
        """
        return None

    @Resolution.setter
    def Resolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType]) -> None:
        """
        
            Specifies the resolution type. Defaults to NormalResolution.
            
        """
        pass

    @property
    def Capture(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsCaptureType]:
        """
        
            Specifies what to include in the capture. Defaults to ImageAndLegend.
            
        """
        return None

    @Capture.setter
    def Capture(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsCaptureType]) -> None:
        """
        
            Specifies what to include in the capture. Defaults to ImageAndLegend.
            
        """
        pass

    @property
    def Background(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]:
        """
        
            Specifies the background color. Defaults to GraphicsAppearanceSetting.
            
        """
        return None

    @Background.setter
    def Background(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]) -> None:
        """
        
            Specifies the background color. Defaults to GraphicsAppearanceSetting.
            
        """
        pass

    @property
    def FontMagnification(self) -> typing.Optional[float]:
        """
        
            Specifies the font magnification factor. Defaults to 1.0.
            
        """
        return None

    @FontMagnification.setter
    def FontMagnification(self, value: typing.Optional[float]) -> None:
        """
        
            Specifies the font magnification factor. Defaults to 1.0.
            
        """
        pass

    @property
    def Width(self) -> typing.Optional[int]:
        """
        
            Specifies the image width. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        return None

    @Width.setter
    def Width(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the image width. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        pass

    @property
    def Height(self) -> typing.Optional[int]:
        """
        
            Specifies the image height. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        return None

    @Height.setter
    def Height(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the image height. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        pass

    def __init__(self) -> None:
        """
        
            Creates a new GraphicsViewportsExportSettings instance.
            
        """
        pass


class AnnotationPreferences(object):

    @property
    def ShowAllAnnotations(self) -> typing.Optional[bool]:
        """
        Sets the visibility of all annotations.
        """
        return None

    @ShowAllAnnotations.setter
    def ShowAllAnnotations(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of all annotations.
        """
        pass

    @property
    def ShowCustomAnnotations(self) -> typing.Optional[bool]:
        """
        Sets the visibility of user defined annotations.
        """
        return None

    @ShowCustomAnnotations.setter
    def ShowCustomAnnotations(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of user defined annotations.
        """
        pass

    @property
    def ShowLabels(self) -> typing.Optional[bool]:
        """
        Sets the visibility of annotation labels.
        """
        return None

    @ShowLabels.setter
    def ShowLabels(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of annotation labels.
        """
        pass

    @property
    def ShowPointMasses(self) -> typing.Optional[bool]:
        """
        Sets the visibility of point mass annotations.
        """
        return None

    @ShowPointMasses.setter
    def ShowPointMasses(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of point mass annotations.
        """
        pass

    @property
    def ShowBeams(self) -> typing.Optional[bool]:
        """
        Sets the visibility of beam annotations.
        """
        return None

    @ShowBeams.setter
    def ShowBeams(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of beam annotations.
        """
        pass

    @property
    def ShowSprings(self) -> typing.Optional[bool]:
        """
        Sets the visibility of spring annotations.
        """
        return None

    @ShowSprings.setter
    def ShowSprings(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of spring annotations.
        """
        pass

    @property
    def ShowBearings(self) -> typing.Optional[bool]:
        """
        Sets the visibility of bearing annotations.
        """
        return None

    @ShowBearings.setter
    def ShowBearings(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of bearing annotations.
        """
        pass

    @property
    def ShowCracks(self) -> typing.Optional[bool]:
        """
        Sets the visibility of crack annotations.
        """
        return None

    @ShowCracks.setter
    def ShowCracks(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of crack annotations.
        """
        pass

    @property
    def ShowForceArrows(self) -> typing.Optional[bool]:
        """
        Sets the visibility of force arrows on surface reaction.
        """
        return None

    @ShowForceArrows.setter
    def ShowForceArrows(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of force arrows on surface reaction.
        """
        pass

    @property
    def ShowBodyScopings(self) -> typing.Optional[bool]:
        """
        Sets the visibility of body scoping annotations.
        """
        return None

    @ShowBodyScopings.setter
    def ShowBodyScopings(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of body scoping annotations.
        """
        pass

    @property
    def ShowMeshAnnotations(self) -> typing.Optional[bool]:
        """
        Sets the visibility of mesh node and mesh element annotations in named selection displays.
        """
        return None

    @ShowMeshAnnotations.setter
    def ShowMeshAnnotations(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of mesh node and mesh element annotations in named selection displays.
        """
        pass

    @property
    def ShowNodeNumbers(self) -> typing.Optional[bool]:
        """
        Sets the visibility of mesh node numbers in named selection, mesh, and result displays.
        """
        return None

    @ShowNodeNumbers.setter
    def ShowNodeNumbers(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of mesh node numbers in named selection, mesh, and result displays.
        """
        pass

    @property
    def ShowElementNumbers(self) -> typing.Optional[bool]:
        """
        Sets the visibility of mesh element numbers in named Selection, mesh, and result displays.
        """
        return None

    @ShowElementNumbers.setter
    def ShowElementNumbers(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of mesh element numbers in named Selection, mesh, and result displays.
        """
        pass

    @property
    def ShowNamedSelectionElements(self) -> typing.Optional[bool]:
        """
        Sets the visibility of elements for all items in the named selection group.
        """
        return None

    @ShowNamedSelectionElements.setter
    def ShowNamedSelectionElements(self, value: typing.Optional[bool]) -> None:
        """
        Sets the visibility of elements for all items in the named selection group.
        """
        pass

    @property
    def PointMassSize(self) -> typing.Optional[int]:
        """
        Sets the size for point mass annotation. (Small-Large ; 1-100) 
        """
        return None

    @PointMassSize.setter
    def PointMassSize(self, value: typing.Optional[int]) -> None:
        """
        Sets the size for point mass annotation. (Small-Large ; 1-100) 
        """
        pass

    @property
    def SpringSize(self) -> typing.Optional[int]:
        """
        Sets the size for spring annotation. (Small-Large ; 1-100)
        """
        return None

    @SpringSize.setter
    def SpringSize(self, value: typing.Optional[int]) -> None:
        """
        Sets the size for spring annotation. (Small-Large ; 1-100)
        """
        pass

    def SetNodeNumbering(self, begin: int, end: int, inc: int) -> None:
        """
        Sets the begin, end and increment values to display node numbering.
        """
        pass

    def SetElementNumbering(self, begin: int, end: int, inc: int) -> None:
        """
        Sets the begin, end and increment values to display element numbering.
        """
        pass


class ResultPreference(object):

    @property
    def GeometryView(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.GeometryView]:
        """
        Sets the result geometry view.
        """
        return None

    @GeometryView.setter
    def GeometryView(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.GeometryView]) -> None:
        """
        Sets the result geometry view.
        """
        pass

    @property
    def ContourView(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ContourView]:
        """
        Sets the result contour view.
        """
        return None

    @ContourView.setter
    def ContourView(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ContourView]) -> None:
        """
        Sets the result contour view.
        """
        pass

    @property
    def ExtraModelDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ExtraModelDisplay]:
        """
        Sets the result edge display option.
        """
        return None

    @ExtraModelDisplay.setter
    def ExtraModelDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ExtraModelDisplay]) -> None:
        """
        Sets the result edge display option.
        """
        pass

    @property
    def DeformationScaling(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.DeformationScaling]:
        """
        Sets the deformation scale multiplier to either AutoScale or TrueScale.
        """
        return None

    @DeformationScaling.setter
    def DeformationScaling(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.DeformationScaling]) -> None:
        """
        Sets the deformation scale multiplier to either AutoScale or TrueScale.
        """
        pass

    @property
    def DeformationScaleMultiplier(self) -> typing.Optional[float]:
        """
        Sets the deformation scale multiplier.
        """
        return None

    @DeformationScaleMultiplier.setter
    def DeformationScaleMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Sets the deformation scale multiplier.
        """
        pass

    @property
    def IsoSurfaceValue(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Sets the capping value for capped iso surface view .
        """
        return None

    @IsoSurfaceValue.setter
    def IsoSurfaceValue(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Sets the capping value for capped iso surface view .
        """
        pass

    @property
    def CappingType(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.CappingType]:
        """
        Sets the result capping type.
        """
        return None

    @CappingType.setter
    def CappingType(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.CappingType]) -> None:
        """
        Sets the result capping type.
        """
        pass

    @property
    def ScopingDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ScopingDisplay]:
        """
        Sets the result scoping display.
        """
        return None

    @ScopingDisplay.setter
    def ScopingDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.MechanicalEnums.Graphics.ScopingDisplay]) -> None:
        """
        Sets the result scoping display.
        """
        pass

    @property
    def ShowMinimum(self) -> typing.Optional[bool]:
        """
        Displays the result minimum value annotation label.
        """
        return None

    @ShowMinimum.setter
    def ShowMinimum(self, value: typing.Optional[bool]) -> None:
        """
        Displays the result minimum value annotation label.
        """
        pass

    @property
    def ShowMaximum(self) -> typing.Optional[bool]:
        """
        Displays the result maximum value annotation label.
        """
        return None

    @ShowMaximum.setter
    def ShowMaximum(self, value: typing.Optional[bool]) -> None:
        """
        Displays the result maximum value annotation label.
        """
        pass


class VectorDisplay(object):

    @property
    def LengthType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.VectorLengthType]:
        """
        Sets the result vector length type.
        """
        return None

    @LengthType.setter
    def LengthType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.VectorLengthType]) -> None:
        """
        Sets the result vector length type.
        """
        pass

    @property
    def DisplayType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.VectorDisplayType]:
        """
        Sets the vector display type.
        """
        return None

    @DisplayType.setter
    def DisplayType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.VectorDisplayType]) -> None:
        """
        Sets the vector display type.
        """
        pass

    @property
    def ControlDisplayDensity(self) -> typing.Optional[bool]:
        """
        Allows control of the vector display density.
        """
        return None

    @ControlDisplayDensity.setter
    def ControlDisplayDensity(self, value: typing.Optional[bool]) -> None:
        """
        Allows control of the vector display density.
        """
        pass

    @property
    def DisplayDensity(self) -> typing.Optional[float]:
        """
        Sets the vector display density in percentage.
        """
        return None

    @DisplayDensity.setter
    def DisplayDensity(self, value: typing.Optional[float]) -> None:
        """
        Sets the vector display density in percentage.
        """
        pass

    @property
    def LengthMultiplier(self) -> typing.Optional[float]:
        """
        Sets the vector length multiplier.
        """
        return None

    @LengthMultiplier.setter
    def LengthMultiplier(self, value: typing.Optional[float]) -> None:
        """
        Sets the vector length multiplier.
        """
        pass

    @property
    def ShowTriadXAxis(self) -> typing.Optional[bool]:
        """
        Displays the X axis vector of the triad/tensor.
        """
        return None

    @ShowTriadXAxis.setter
    def ShowTriadXAxis(self, value: typing.Optional[bool]) -> None:
        """
        Displays the X axis vector of the triad/tensor.
        """
        pass

    @property
    def ShowTriadYAxis(self) -> typing.Optional[bool]:
        """
        Displays the Y axis vector of the triad/tensor.
        """
        return None

    @ShowTriadYAxis.setter
    def ShowTriadYAxis(self, value: typing.Optional[bool]) -> None:
        """
        Displays the Y axis vector of the triad/tensor.
        """
        pass

    @property
    def ShowTriadZAxis(self) -> typing.Optional[bool]:
        """
        Displays the Z axis vector of the triad/tensor.
        """
        return None

    @ShowTriadZAxis.setter
    def ShowTriadZAxis(self, value: typing.Optional[bool]) -> None:
        """
        Displays the Z axis vector of the triad/tensor.
        """
        pass


class AnalysisSettingsGraph(object):

    @property
    def BoundaryConditionVisibility(self) -> typing.Optional[Ansys.Mechanical.Graphics.BoundaryConditionVisibilityDictionary]:
        """
        BoundaryConditionVisibility property.
        """
        return None

    def __init__(self, analysisSettings: Ansys.Common.Interop.DSObjectsAuto.IDSAnalysisSettings) -> None:
        """
        __init__ method.
        """
        pass


class GlobalLegendSettings(object):
    """
    Defines global legend settings.
    """

    @property
    def LegendOrientation(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendOrientationType]:
        """
        Whether the orientation of the legend.
        """
        return None

    @LegendOrientation.setter
    def LegendOrientation(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.LegendOrientationType]) -> None:
        """
        Whether the orientation of the legend.
        """
        pass

    @property
    def ShowDateAndTime(self) -> typing.Optional[bool]:
        """
        Whether the  date and time of the legend is shown.
        """
        return None

    @ShowDateAndTime.setter
    def ShowDateAndTime(self, value: typing.Optional[bool]) -> None:
        """
        Whether the  date and time of the legend is shown.
        """
        pass

    @property
    def ShowMinMax(self) -> typing.Optional[bool]:
        """
        Whether the Min and Max value are shown.
        """
        return None

    @ShowMinMax.setter
    def ShowMinMax(self, value: typing.Optional[bool]) -> None:
        """
        Whether the Min and Max value are shown.
        """
        pass

    @property
    def ShowDeformingScaling(self) -> typing.Optional[bool]:
        """
        Whether the Deformation Scaling is shown.
        """
        return None

    @ShowDeformingScaling.setter
    def ShowDeformingScaling(self, value: typing.Optional[bool]) -> None:
        """
        Whether the Deformation Scaling is shown.
        """
        pass

    def GetDefaultBandColor(self, index: int) -> int:
        """
        GetDefaultBandColor method.
        """
        pass

    def SetDefaultBandColor(self, index: int, ColorValue: int) -> None:
        """
        SetDefaultBandColor method.
        """
        pass

    def Reset(self) -> None:
        """
        Reset method.
        """
        pass


class AnimationExportSettings(object):

    @property
    def Width(self) -> typing.Optional[int]:
        """
        
            Specifies the video width.
            
        """
        return None

    @Width.setter
    def Width(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the video width.
            
        """
        pass

    @property
    def Height(self) -> typing.Optional[int]:
        """
        
            Specifies the video height.
            
        """
        return None

    @Height.setter
    def Height(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the video height.
            
        """
        pass

    @property
    def TemporaryFramesPath(self) -> typing.Optional[str]:
        """
        
            When not null, this parameter tells the animation tool to leave behind at the specified directory PNG images of each frame used to generate the animation.
            
        """
        return None

    @TemporaryFramesPath.setter
    def TemporaryFramesPath(self, value: typing.Optional[str]) -> None:
        """
        
            When not null, this parameter tells the animation tool to leave behind at the specified directory PNG images of each frame used to generate the animation.
            
        """
        pass

    def __init__(self, width: int, height: int) -> None:
        """
        
            Specifies the Animation Export File Properties.
            
        """
        pass


class ResultAnimationOptions(object):

    @property
    def NumberOfFrames(self) -> typing.Optional[int]:
        """
        
            Gets or Sets the Number Of Frames for Distributed Result Animation.
            
        """
        return None

    @NumberOfFrames.setter
    def NumberOfFrames(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets the Number Of Frames for Distributed Result Animation.
            
        """
        pass

    @property
    def Duration(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Gets or Sets the Duration for Result Animation.
            
        """
        return None

    @Duration.setter
    def Duration(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Gets or Sets the Duration for Result Animation.
            
        """
        pass

    @property
    def RangeType(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultAnimationRangeType]:
        """
        
            Gets or Sets the Range Type for Result Animation.
            
        """
        return None

    @RangeType.setter
    def RangeType(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ResultAnimationRangeType]) -> None:
        """
        
            Gets or Sets the Range Type for Result Animation.
            
        """
        pass

    @property
    def UpdateContourRangeAtEachFrame(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets if the Legend Contours will Update at Each Frame.
            
        """
        return None

    @UpdateContourRangeAtEachFrame.setter
    def UpdateContourRangeAtEachFrame(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets if the Legend Contours will Update at Each Frame.
            
        """
        pass

    @property
    def FitDeformationScalingToAnimation(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets if the Animation Displacement Fits for full range of Time Steps in the Screen.
            
        """
        return None

    @FitDeformationScalingToAnimation.setter
    def FitDeformationScalingToAnimation(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets if the Animation Displacement Fits for full range of Time Steps in the Screen.
            
        """
        pass

    @property
    def TimeDecayCycles(self) -> typing.Optional[int]:
        """
        
            Gets or Sets the Number of Cycles for Time Decay.
            
        """
        return None

    @TimeDecayCycles.setter
    def TimeDecayCycles(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or Sets the Number of Cycles for Time Decay.
            
        """
        pass

    @property
    def TimeDecay(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets the Time Decay.
            
        """
        return None

    @TimeDecay.setter
    def TimeDecay(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets the Time Decay.
            
        """
        pass

    @property
    def CanEngageMultiViewportAnimation(self) -> typing.Optional[bool]:
        """
        CanEngageMultiViewportAnimation property.
        """
        return None

    @property
    def MultiViewportAnimation(self) -> typing.Optional[bool]:
        """
        MultiViewportAnimation property.
        """
        return None

    @MultiViewportAnimation.setter
    def MultiViewportAnimation(self, value: typing.Optional[bool]) -> None:
        """
        MultiViewportAnimation property.
        """
        pass

    @property
    def AcceleratedAnimationWillBeUsed(self) -> typing.Optional[bool]:
        """
        
            Whether the accelerated animation will be used given the current result and display options.
            
        """
        return None

    @property
    def DisplacementTraces(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets if the Displacement Traces are Enabled/Disabled
            
        """
        return None

    @DisplacementTraces.setter
    def DisplacementTraces(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets if the Displacement Traces are Enabled/Disabled
            
        """
        pass

    def __init__(self, graphics: Ansys.Common.Interop.Gfx.IDSGraphics) -> None:
        """
        __init__ method.
        """
        pass


class SectionPlane(object):
    """
    
            Represents a SectionPlane object. This object holds properties of the Plane.
            
    """

    @property
    def Active(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets the Active State of the Section Plane
            
        """
        return None

    @Active.setter
    def Active(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets the Active State of the Section Plane
            
        """
        pass

    @property
    def Center(self) -> typing.Optional[Ansys.Mechanical.Graphics.Point]:
        """
        
            Gets or Sets the Center point of the Section Plane
            
        """
        return None

    @Center.setter
    def Center(self, value: typing.Optional[Ansys.Mechanical.Graphics.Point]) -> None:
        """
        
            Gets or Sets the Center point of the Section Plane
            
        """
        pass

    @property
    def Direction(self) -> typing.Optional[Ansys.ACT.Math.Vector3D]:
        """
        
            Gets or Sets the Direction(Normal) of the Section Plane
            
        """
        return None

    @Direction.setter
    def Direction(self, value: typing.Optional[Ansys.ACT.Math.Vector3D]) -> None:
        """
        
            Gets or Sets the Direction(Normal) of the Section Plane
            
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or Sets the Name of the Section Plane
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or Sets the Name of the Section Plane
            
        """
        pass

    @property
    def Type(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SectionPlaneType]:
        """
        
            Gets or Sets the SectionPlane Type of the Section Plane
            
        """
        return None

    @Type.setter
    def Type(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SectionPlaneType]) -> None:
        """
        
            Gets or Sets the SectionPlane Type of the Section Plane
            
        """
        pass

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, center: Ansys.Mechanical.Graphics.Point, direction: Ansys.ACT.Math.Vector3D, name: str, type: Ansys.Mechanical.DataModel.Enums.SectionPlaneType, active: bool) -> None:
        ...

    def __init__(self, *args: typing.Any) -> None:
        """
        
             Creates a SectionPlane Object
            
        """
        pass

    def Equals(self, sectionPlane: Ansys.Mechanical.Graphics.SectionPlane) -> bool:
        """
        
             Indicates whether the current SectionPlane properties are equal to the properties of another SectionPlane object.
            
        """
        pass


class SectionPlanes(object):
    """
    
            Represents the collection of section planes used by graphics
            
    """

    @property
    def ShowWholeElement(self) -> typing.Optional[bool]:
        """
        
            Gets or Sets the Element Visibility of the Section Plane
            
        """
        return None

    @ShowWholeElement.setter
    def ShowWholeElement(self, value: typing.Optional[bool]) -> None:
        """
        
            Gets or Sets the Element Visibility of the Section Plane
            
        """
        pass

    @property
    def Capping(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.SectionPlaneCappingType]:
        """
        
            Gets or Sets the Capping style of the Section Plane
            
        """
        return None

    @Capping.setter
    def Capping(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.SectionPlaneCappingType]) -> None:
        """
        
            Gets or Sets the Capping style of the Section Plane
            
        """
        pass

    @property
    def Item(self) -> typing.Optional[Ansys.Mechanical.Graphics.SectionPlane]:
        """
        Item property.
        """
        return None

    @Item.setter
    def Item(self, value: typing.Optional[Ansys.Mechanical.Graphics.SectionPlane]) -> None:
        """
        Item property.
        """
        pass

    @property
    def Count(self) -> typing.Optional[int]:
        """
        
            The number of section planes in the collection.
            
        """
        return None

    @property
    def IsReadOnly(self) -> typing.Optional[bool]:
        """
        IsReadOnly property.
        """
        return None

    def __init__(self, graphics: Ansys.Common.Interop.Gfx.IDSGraphics) -> None:
        """
        __init__ method.
        """
        pass

    def Add(self, sectionPlane: Ansys.Mechanical.Graphics.SectionPlane) -> None:
        """
        
            Adds the given SectionPlane object to the collection to modify the view. Currently only 6 SectionPlane objects in the collection can be activated at once.
            
        """
        pass

    def Clear(self) -> None:
        """
        
            Clears the collection of all SectionPlane objects.
            
        """
        pass

    def Contains(self, item: Ansys.Mechanical.Graphics.SectionPlane) -> bool:
        """
        
            Returns true if the SectionPlane belongs to the collection.
            
        """
        pass

    def CopyTo(self, array: Ansys.Mechanical.Graphics.SectionPlane, arrayIndex: int) -> None:
        """
        CopyTo method.
        """
        pass

    def IndexOf(self, sectionPlane: Ansys.Mechanical.Graphics.SectionPlane) -> int:
        """
        
            Returns the index of the SectionObject if in the collection.  Returns -1 if not found.
            
        """
        pass

    def Remove(self, sectionPlane: Ansys.Mechanical.Graphics.SectionPlane) -> bool:
        """
        
            Removes the requested SectionPlane from the collection.
            
        """
        pass

    def RemoveAt(self, index: int) -> None:
        """
        
            Removes the SectionPlane at the given index.
            
        """
        pass

    def GetEnumerator(self) -> Ansys.Mechanical.Graphics.SectionPlaneList:
        """
        GetEnumerator method.
        """
        pass


class Graphics3DExportSettings(object):

    @property
    def Background(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]:
        """
        
            Specifies the background color.
            
        """
        return None

    @Background.setter
    def Background(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]) -> None:
        """
        
            Specifies the background color.
            
        """
        pass

    def __init__(self) -> None:
        """
        
            Specifies the settings when exporting 3D Graphics.
            
        """
        pass


class GraphicsImageExportSettings(object):

    @property
    def CurrentGraphicsDisplay(self) -> typing.Optional[bool]:
        """
        
            Specifies whether to use the current graphics display settings. Defaults to true.
            
        """
        return None

    @CurrentGraphicsDisplay.setter
    def CurrentGraphicsDisplay(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether to use the current graphics display settings. Defaults to true.
            
        """
        pass

    @property
    def AppendGraph(self) -> typing.Optional[bool]:
        """
        
            Specifies whether to append the viewport graph(s) to the exported image. Defaults to false.
            
        """
        return None

    @AppendGraph.setter
    def AppendGraph(self, value: typing.Optional[bool]) -> None:
        """
        
            Specifies whether to append the viewport graph(s) to the exported image. Defaults to false.
            
        """
        pass

    @property
    def Resolution(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType]:
        """
        
            Specifies the resolution type. Defaults to NormalResolution.
            
        """
        return None

    @Resolution.setter
    def Resolution(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsResolutionType]) -> None:
        """
        
            Specifies the resolution type. Defaults to NormalResolution.
            
        """
        pass

    @property
    def Capture(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsCaptureType]:
        """
        
            Specifies what to include in the capture. Defaults to ImageAndLegend.
            
        """
        return None

    @Capture.setter
    def Capture(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsCaptureType]) -> None:
        """
        
            Specifies what to include in the capture. Defaults to ImageAndLegend.
            
        """
        pass

    @property
    def Background(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]:
        """
        
            Specifies the background color. Defaults to GraphicsAppearanceSetting.
            
        """
        return None

    @Background.setter
    def Background(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.GraphicsBackgroundType]) -> None:
        """
        
            Specifies the background color. Defaults to GraphicsAppearanceSetting.
            
        """
        pass

    @property
    def FontMagnification(self) -> typing.Optional[float]:
        """
        
            Specifies the font magnification factor. Defaults to 1.0.
            
        """
        return None

    @FontMagnification.setter
    def FontMagnification(self, value: typing.Optional[float]) -> None:
        """
        
            Specifies the font magnification factor. Defaults to 1.0.
            
        """
        pass

    @property
    def Width(self) -> typing.Optional[int]:
        """
        
            Specifies the image width. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        return None

    @Width.setter
    def Width(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the image width. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        pass

    @property
    def Height(self) -> typing.Optional[int]:
        """
        
            Specifies the image height. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        return None

    @Height.setter
    def Height(self, value: typing.Optional[int]) -> None:
        """
        
            Specifies the image height. Defaults to 0. If width AND height are zero, this uses the current dimensions. If only one of the two are nonzero, the current dimension’s ratio is used along with the nonzero of the two properties to determine the computed value of the zero property.
            
        """
        pass

    def __init__(self) -> None:
        """
        
            Creates a new GraphicsImageExportSettings instance.
            
        """
        pass


class Point(object):

    @property
    def Location(self) -> typing.Optional[typing.List[float]]:
        """
        
             The location of the Point.
            
        """
        return None

    @Location.setter
    def Location(self, value: typing.Optional[typing.List[float]]) -> None:
        """
        
             The location of the Point.
            
        """
        pass

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            The length unit of the Point.
            
        """
        return None

    @Unit.setter
    def Unit(self, value: typing.Optional[str]) -> None:
        """
        
            The length unit of the Point.
            
        """
        pass

    def __init__(self, location: typing.List[typing.Any], lengthUnit: str) -> None:
        """
        __init__ method.
        """
        pass

    def ToString(self) -> str:
        """
        ToString method.
        """
        pass

    @typing.overload
    def Equals(self, point: Ansys.Mechanical.Graphics.Point) -> bool:
        ...

    @typing.overload
    def Equals(self, o: typing.Any) -> bool:
        ...

    def Equals(self, *args: typing.Any) -> bool:
        """
        Equals method.
        """
        pass

    @classmethod
    def ConvertUnit(cls, inPoint: Ansys.Mechanical.Graphics.Point, outputUnit: str) -> Ansys.Mechanical.Graphics.Point:
        """
        
            Returns a new Point given new unit.
            
        """
        pass

    @classmethod
    def __eq__(cls, a: Ansys.Mechanical.Graphics.Point, b: Ansys.Mechanical.Graphics.Point) -> bool:
        """
        Equal operator
        """
        pass

    @classmethod
    def __ne__(cls, a: Ansys.Mechanical.Graphics.Point, b: Ansys.Mechanical.Graphics.Point) -> bool:
        """
        Not-Equal operator
        """
        pass

    def GetHashCode(self) -> int:
        """
        Object.GetHashCode() override
        """
        pass


class ViewOptions(object):

    @property
    def VectorDisplay(self) -> typing.Optional[Ansys.Mechanical.Graphics.VectorDisplay]:
        """
        VectorDisplay property.
        """
        return None

    @property
    def ResultPreference(self) -> typing.Optional[Ansys.Mechanical.Graphics.ResultPreference]:
        """
        ResultPreference property.
        """
        return None

    @property
    def AnnotationPreferences(self) -> typing.Optional[Ansys.Mechanical.Graphics.AnnotationPreferences]:
        """
        AnnotationPreferences property.
        """
        return None

    @property
    def ShowShellThickness(self) -> typing.Optional[bool]:
        """
        Displays the thickness of shells.
        """
        return None

    @ShowShellThickness.setter
    def ShowShellThickness(self, value: typing.Optional[bool]) -> None:
        """
        Displays the thickness of shells.
        """
        pass

    @property
    def ShowBeamThickness(self) -> typing.Optional[bool]:
        """
        Displays the thickness of beams.
        """
        return None

    @ShowBeamThickness.setter
    def ShowBeamThickness(self, value: typing.Optional[bool]) -> None:
        """
        Displays the thickness of beams.
        """
        pass

    @property
    def ShowSPHExpansion(self) -> typing.Optional[bool]:
        """
        Displays the expansion for SPH elements.
        """
        return None

    @ShowSPHExpansion.setter
    def ShowSPHExpansion(self, value: typing.Optional[bool]) -> None:
        """
        Displays the expansion for SPH elements.
        """
        pass

    @property
    def ShowMesh(self) -> typing.Optional[bool]:
        """
        Display the model's mesh.
        """
        return None

    @ShowMesh.setter
    def ShowMesh(self, value: typing.Optional[bool]) -> None:
        """
        Display the model's mesh.
        """
        pass

    @property
    def ShowRandomColors(self) -> typing.Optional[bool]:
        """
        Sets random colors for each object of the application.
        """
        return None

    @ShowRandomColors.setter
    def ShowRandomColors(self, value: typing.Optional[bool]) -> None:
        """
        Sets random colors for each object of the application.
        """
        pass

    @property
    def ShowVertices(self) -> typing.Optional[bool]:
        """
        Display all the vertices of the model.
        """
        return None

    @ShowVertices.setter
    def ShowVertices(self, value: typing.Optional[bool]) -> None:
        """
        Display all the vertices of the model.
        """
        pass

    @property
    def ShowClusteredVertices(self) -> typing.Optional[bool]:
        """
        Displays all closely clustered vertices of the model.
        """
        return None

    @ShowClusteredVertices.setter
    def ShowClusteredVertices(self, value: typing.Optional[bool]) -> None:
        """
        Displays all closely clustered vertices of the model.
        """
        pass

    @property
    def ShowEdgeDirection(self) -> typing.Optional[bool]:
        """
        Displays the edge direction arrow.
        """
        return None

    @ShowEdgeDirection.setter
    def ShowEdgeDirection(self, value: typing.Optional[bool]) -> None:
        """
        Displays the edge direction arrow.
        """
        pass

    @property
    def ShowMeshConnection(self) -> typing.Optional[bool]:
        """
        Displays edge connection using a color scheme based on the mesh connection information.
        """
        return None

    @ShowMeshConnection.setter
    def ShowMeshConnection(self, value: typing.Optional[bool]) -> None:
        """
        Displays edge connection using a color scheme based on the mesh connection information.
        """
        pass

    @property
    def ShowThickEdgeScoping(self) -> typing.Optional[bool]:
        """
        Thicken the display of edge scoping.
        """
        return None

    @ShowThickEdgeScoping.setter
    def ShowThickEdgeScoping(self, value: typing.Optional[bool]) -> None:
        """
        Thicken the display of edge scoping.
        """
        pass

    @property
    def ModelDisplay(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelDisplay]:
        """
        Sets the model display option.
        """
        return None

    @ModelDisplay.setter
    def ModelDisplay(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelDisplay]) -> None:
        """
        Sets the model display option.
        """
        pass

    @property
    def ModelColoring(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelColoring]:
        """
        Sets the Model display Coloring.
        """
        return None

    @ModelColoring.setter
    def ModelColoring(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.ModelColoring]) -> None:
        """
        Sets the Model display Coloring.
        """
        pass

    @property
    def ShowCoordinateSystems(self) -> typing.Optional[bool]:
        """
        Displays all coordinate system defined.
        """
        return None

    @ShowCoordinateSystems.setter
    def ShowCoordinateSystems(self, value: typing.Optional[bool]) -> None:
        """
        Displays all coordinate system defined.
        """
        pass

    @property
    def ClusteredVertexTolerance(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        Sets the clustered vertices custom tolerance value.
        """
        return None

    @ClusteredVertexTolerance.setter
    def ClusteredVertexTolerance(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        Sets the clustered vertices custom tolerance value.
        """
        pass

    @property
    def ShowLegend(self) -> typing.Optional[bool]:
        """
        Displays the legend.
        """
        return None

    @ShowLegend.setter
    def ShowLegend(self, value: typing.Optional[bool]) -> None:
        """
        Displays the legend.
        """
        pass

    @property
    def ShowLogo(self) -> typing.Optional[bool]:
        """
        Displays the logo. The logo is always shown when using an academic license.
        """
        return None

    @ShowLogo.setter
    def ShowLogo(self, value: typing.Optional[bool]) -> None:
        """
        Displays the logo. The logo is always shown when using an academic license.
        """
        pass

    @property
    def ShowTriad(self) -> typing.Optional[bool]:
        """
        Displays the triad.
        """
        return None

    @ShowTriad.setter
    def ShowTriad(self, value: typing.Optional[bool]) -> None:
        """
        Displays the triad.
        """
        pass

    @property
    def ShowRuler(self) -> typing.Optional[bool]:
        """
        Displays the ruler.
        """
        return None

    @ShowRuler.setter
    def ShowRuler(self, value: typing.Optional[bool]) -> None:
        """
        Displays the ruler.
        """
        pass

    @property
    def ShowResultVectors(self) -> typing.Optional[bool]:
        """
        Displays the result vectors.
        """
        return None

    @ShowResultVectors.setter
    def ShowResultVectors(self, value: typing.Optional[bool]) -> None:
        """
        Displays the result vectors.
        """
        pass

    @property
    def ShowRemotePointConnections(self) -> typing.Optional[bool]:
        """
        Displays the Remote Point Connections.
        """
        return None

    @ShowRemotePointConnections.setter
    def ShowRemotePointConnections(self, value: typing.Optional[bool]) -> None:
        """
        Displays the Remote Point Connections.
        """
        pass

    @property
    def ShowBoundingMeshEdges(self) -> typing.Optional[bool]:
        """
        ShowBoundingMeshEdges property.
        """
        return None

    @ShowBoundingMeshEdges.setter
    def ShowBoundingMeshEdges(self, value: typing.Optional[bool]) -> None:
        """
        ShowBoundingMeshEdges property.
        """
        pass

    @property
    def SeamWeldReview(self) -> typing.Optional[bool]:
        """
        Activate Seam Weld review mode.
        """
        return None

    @SeamWeldReview.setter
    def SeamWeldReview(self, value: typing.Optional[bool]) -> None:
        """
        Activate Seam Weld review mode.
        """
        pass

    @property
    def DisplayGraphOverlay(self) -> typing.Optional[bool]:
        """
        Display Graph overlay in the current viewport.
        """
        return None

    @DisplayGraphOverlay.setter
    def DisplayGraphOverlay(self, value: typing.Optional[bool]) -> None:
        """
        Display Graph overlay in the current viewport.
        """
        pass

    def RescaleAnnotations(self) -> None:
        """
        Rescale size of annotation following a zoom in or zoom out of the model.
        """
        pass

    def ZoomToWeld(self) -> None:
        """
        Zoom to the bodies that are affected by the Weld object.
        """
        pass

    def Reset(self) -> None:
        """
        Reset method.
        """
        pass


