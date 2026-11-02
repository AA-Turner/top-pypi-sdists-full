"""Graphics module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys


class DMCameraWrapper(object):
    """
    
            Wrapper for Camera in Design Modeler.
            
    """

    @property
    def ZoomFactor(self) -> typing.Optional[float]:
        """
        ZoomFactor property.
        """
        return None

    @ZoomFactor.setter
    def ZoomFactor(self, value: typing.Optional[float]) -> None:
        """
        ZoomFactor property.
        """
        pass

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.GraphicsDataModel.IDSCameraItf]:
        """
        InternalObject property.
        """
        return None

    def __init__(self, graphics: Ansys.ACT.Common.Graphics.GraphicsWrapper, camera: Ansys.Common.Interop.GraphicsDataModel.IDSCameraItf) -> None:
        """
        __init__ method.
        """
        pass

    def GetLocation(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        GetLocation method.
        """
        pass

    def GetTarget(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        GetTarget method.
        """
        pass


class MechanicalCameraWrapper(object):
    """
    
            Wrapper for Camera in Mechanical.
            
    """

    @property
    def ZoomFactor(self) -> typing.Optional[float]:
        """
        ZoomFactor property.
        """
        return None

    @ZoomFactor.setter
    def ZoomFactor(self, value: typing.Optional[float]) -> None:
        """
        ZoomFactor property.
        """
        pass

    @property
    def FocalPoint(self) -> typing.Optional[Ansys.Mechanical.Graphics.Point]:
        """
        
            The focal point of the camera (coordinates are in the global coordinate system).
            
        """
        return None

    @FocalPoint.setter
    def FocalPoint(self, value: typing.Optional[Ansys.Mechanical.Graphics.Point]) -> None:
        """
        
            The focal point of the camera (coordinates are in the global coordinate system).
            
        """
        pass

    @property
    def UpVector(self) -> typing.Optional[Ansys.ACT.Math.Vector3D]:
        """
        
            The vector pointing up from the focal point.
            
        """
        return None

    @UpVector.setter
    def UpVector(self, value: typing.Optional[Ansys.ACT.Math.Vector3D]) -> None:
        """
        
            The vector pointing up from the focal point.
            
        """
        pass

    @property
    def ViewVector(self) -> typing.Optional[Ansys.ACT.Math.Vector3D]:
        """
        
            The vector pointing from the focal point to the camera.
            
        """
        return None

    @ViewVector.setter
    def ViewVector(self, value: typing.Optional[Ansys.ACT.Math.Vector3D]) -> None:
        """
        
            The vector pointing from the focal point to the camera.
            
        """
        pass

    @property
    def SceneHeight(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Specifies the scene height (in length units) that will be projected and fit to the viewport.
            
        """
        return None

    @SceneHeight.setter
    def SceneHeight(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Specifies the scene height (in length units) that will be projected and fit to the viewport.
            
        """
        pass

    @property
    def SceneWidth(self) -> typing.Optional[Ansys.Core.Units.Quantity]:
        """
        
            Specifies the scene width (in length units) that will be projected and fit to the viewport.
            
        """
        return None

    @SceneWidth.setter
    def SceneWidth(self, value: typing.Optional[Ansys.Core.Units.Quantity]) -> None:
        """
        
            Specifies the scene width (in length units) that will be projected and fit to the viewport.
            
        """
        pass

    @property
    def ViewportHeight(self) -> typing.Optional[int]:
        """
        ViewportHeight property.
        """
        return None

    @property
    def ViewportWidth(self) -> typing.Optional[int]:
        """
        ViewportWidth property.
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.GraphicsDataModel.IDSCameraItf]:
        """
        InternalObject property.
        """
        return None

    def __init__(self, graphics: Ansys.ACT.Common.Graphics.GraphicsWrapper, camera: Ansys.Common.Interop.GraphicsDataModel.IDSCameraItf) -> None:
        """
        __init__ method.
        """
        pass

    def RotateView(self, angle: float) -> None:
        """
        RotateView method.
        """
        pass

    @typing.overload
    def GetLocation(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        ...

    @typing.overload
    def GetLocation(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        ...

    def GetLocation(self, *args: typing.Any) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        GetLocation method.
        """
        pass

    @typing.overload
    def GetTarget(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        ...

    @typing.overload
    def GetTarget(self) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        ...

    def GetTarget(self, *args: typing.Any) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        GetTarget method.
        """
        pass

    def Rotate(self, angle: float, axis: Ansys.Mechanical.DataModel.Enums.CameraAxisType) -> None:
        """
        
            Rotates the camera about an axis.
            
        """
        pass

    def SetSpecificViewOrientation(self, type: Ansys.Mechanical.DataModel.Enums.ViewOrientationType) -> None:
        """
        
            Sets a specific view orientation.
            
        """
        pass

    def SetFit(self, sel: Ansys.ACT.Interfaces.Common.ISelectionInfo) -> None:
        """
        
            Fits the view to the specified selection. If null is supplied, fits the view to the entire model.
            
        """
        pass

    def GetAsString(self, appType: Ansys.Mechanical.DataModel.Enums.ApplicationType) -> str:
        """
        
            Retrieves the view commands as related to the application type as a string.
            
        """
        pass

    def Zoom(self, zoomVal: float) -> None:
        """
        
            Zooms in or out on the model. 
            
        """
        pass

    def Pan(self, x: Ansys.Core.Units.Quantity, y: Ansys.Core.Units.Quantity) -> None:
        """
        
            Shifts the camera position horizontally or vertically based on x and y quantities. 
            
        """
        pass

    def SaveUndoRedoView(self, forcesave: int) -> None:
        """
        SaveUndoRedoView method.
        """
        pass

    def ZoomRectPixels(self, min_x: int, min_y: int, max_x: int, max_y: int) -> None:
        """
        ZoomRectPixels method.
        """
        pass

    def ZoomRectSubpixels(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        """
        ZoomRectSubpixels method.
        """
        pass


class MechanicalGraphicsWrapper(object):
    """
    
            Wrapper for Graphics in Mechanical.
            
    """

    @property
    def AdvancedRenderingIsSupported(self) -> typing.Optional[bool]:
        """
        AdvancedRenderingIsSupported property.
        """
        return None

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        
            Gets the current graphics unit.
            
        """
        return None

    @property
    def InternalObject(self) -> typing.Optional[Ansys.Common.Interop.Gfx.IDSGraphics]:
        """
        InternalObject property.
        """
        return None

    @property
    def LabelManager(self) -> typing.Optional[Ansys.Mechanical.Graphics.Labels.LabelManager]:
        """
        
            Manages labels and the creation and deletion of them.
            
        """
        return None

    @property
    def OverlayManager(self) -> typing.Optional[Ansys.Mechanical.Graphics.OverlayManager]:
        """
        
            Manages overlays and the creation and deletion of them.
            
        """
        return None

    @property
    def ModelViewManager(self) -> typing.Optional[Ansys.ACT.Interfaces.Graphics.IModelViewManager]:
        """
        
            An instance of the ModelViewManager.
            
        """
        return None

    @property
    def KeyframeAnimationUtility(self) -> typing.Optional[Ansys.ACT.Common.Graphics.KeyframeAnimationUtility]:
        """
        
            A utility for creating animations based on keyframes.
            
        """
        return None

    @property
    def ImageCompare(self) -> typing.Optional[Ansys.ACT.Common.Graphics.ImageCompare]:
        """
        ImageCompare property.
        """
        return None

    @property
    def ResultAnimationOptions(self) -> typing.Optional[Ansys.Mechanical.Graphics.ResultAnimationOptions]:
        """
        
            Gets the Global Result Animation options.
            
        """
        return None

    @property
    def SectionPlanes(self) -> typing.Optional[Ansys.Mechanical.Graphics.SectionPlanes]:
        """
        
            Returns the collection of section planes used by graphics
            
        """
        return None

    @property
    def ViewOptions(self) -> typing.Optional[Ansys.Mechanical.Graphics.ViewOptions]:
        """
        
            Gets the Graphics View Options.
            
        """
        return None

    @property
    def GlobalLegendSettings(self) -> typing.Optional[Ansys.Mechanical.Graphics.GlobalLegendSettings]:
        """
        
            Gets the Global Graphics Legend Settings.
            
        """
        return None

    @property
    def Camera(self) -> typing.Optional[Ansys.ACT.Common.Graphics.MechanicalCameraWrapper]:
        """
        
            Gets the camera.
            
        """
        return None

    @property
    def RotateAngle(self) -> typing.Optional[float]:
        """
        RotateAngle property.
        """
        return None

    @property
    def CanPlotDisplacementTraces(self) -> typing.Optional[bool]:
        """
        CanPlotDisplacementTraces property.
        """
        return None

    @property
    def AcceleratedGraphics(self) -> typing.Optional[Ansys.Mechanical.DataModel.Enums.AccGraphicsPreference]:
        """
        Gets or sets the Accelerated Graphics Preference
        """
        return None

    @AcceleratedGraphics.setter
    def AcceleratedGraphics(self, value: typing.Optional[Ansys.Mechanical.DataModel.Enums.AccGraphicsPreference]) -> None:
        """
        Gets or sets the Accelerated Graphics Preference
        """
        pass

    @property
    def ImageExportRescaleGraphOverlayPreference(self) -> typing.Optional[bool]:
        """
        Gets or sets the Image Export Rescale Graph Overlay Preference
        """
        return None

    @ImageExportRescaleGraphOverlayPreference.setter
    def ImageExportRescaleGraphOverlayPreference(self, value: typing.Optional[bool]) -> None:
        """
        Gets or sets the Image Export Rescale Graph Overlay Preference
        """
        pass

    @property
    def DrawContexts(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Graphics.IDrawContext]]:
        """
        DrawContexts property.
        """
        return None

    @property
    def Scene(self) -> typing.Optional[Ansys.ACT.Interfaces.Graphics.IGraphicsCollection]:
        """
        
            Gets the scene.
            
        """
        return None

    @property
    def LineWeight(self) -> typing.Optional[int]:
        """
        LineWeight property.
        """
        return None

    @LineWeight.setter
    def LineWeight(self, value: typing.Optional[int]) -> None:
        """
        LineWeight property.
        """
        pass

    @property
    def Translucency(self) -> typing.Optional[float]:
        """
        Translucency property.
        """
        return None

    @Translucency.setter
    def Translucency(self, value: typing.Optional[float]) -> None:
        """
        Translucency property.
        """
        pass

    @property
    def Color(self) -> typing.Optional[int]:
        """
        Color property.
        """
        return None

    @Color.setter
    def Color(self, value: typing.Optional[int]) -> None:
        """
        Color property.
        """
        pass

    @property
    def DepthTest(self) -> typing.Optional[bool]:
        """
        DepthTest property.
        """
        return None

    @DepthTest.setter
    def DepthTest(self, value: typing.Optional[bool]) -> None:
        """
        DepthTest property.
        """
        pass

    def __init__(self, mechanicalApi: Ansys.ACT.Mechanical.MechanicalAPI, graphics: Ansys.Common.Interop.Gfx.IDSGraphics) -> None:
        """
        __init__ method.
        """
        pass

    def FullRedraw(self) -> None:
        """
        FullRedraw method.
        """
        pass

    def ExportScreenToImage(self, filePath: str) -> None:
        """
        ExportScreenToImage method.
        """
        pass

    def ExportImage(self, filePath: str, formatImage: Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat, settings: Ansys.Mechanical.Graphics.GraphicsImageExportSettings) -> None:
        """
        
            Exports the current graphics display to a 2D image file.
            
        """
        pass

    def ExportViewportImage(self, viewportIndex: int, filePath: str, formatImage: Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat, settings: Ansys.Mechanical.Graphics.GraphicsImageExportSettings) -> None:
        """
        
            Exports the current graphics display to a 2D image file.
            
        """
        pass

    def ExportViewportChart(self, viewportIndex: int, filePath: str, width: int, height: int, formatImage: Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat) -> None:
        """
        
            Exports the specified viewport's chart to file.
            
        """
        pass

    def ExportViewports(self, filePath: str, format: Ansys.Mechanical.DataModel.Enums.GraphicsImageExportFormat, settings: Ansys.Mechanical.Graphics.GraphicsViewportsExportSettings) -> None:
        """
        
            Creates a composite of images exported from each open viewport.
            
        """
        pass

    def Export3D(self, filePath: str, format3d: Ansys.Mechanical.DataModel.Enums.Graphics3DExportFormat, settings: Ansys.Mechanical.Graphics.Graphics3DExportSettings) -> None:
        """
        
            Exports the current Graphics display in a 3d format to a file.
            
        """
        pass

    def ImportLegend(self, filePath: str, unit: str) -> Ansys.Mechanical.Graphics.Tools.LegendSettings:
        """
        ImportLegend method.
        """
        pass

    def VerifyLocaleStringsAreAllRenderable(self) -> tuple[str,bool]:
        """
        
            Performs a test to see if all characters present in all locale dsstringtable.xml files can be found via DSGStream's TextEngine
            
        """
        pass

    def add_ExtendObjectsToDisplay(self, value: System.EventHandler[Ansys.ACT.Common.Graphics.ExtendObjectsToDisplayArgs]) -> None:
        """
        add_ExtendObjectsToDisplay method.
        """
        pass

    def remove_ExtendObjectsToDisplay(self, value: System.EventHandler[Ansys.ACT.Common.Graphics.ExtendObjectsToDisplayArgs]) -> None:
        """
        remove_ExtendObjectsToDisplay method.
        """
        pass

    def RemoveContext(self, context: Ansys.ACT.Interfaces.Graphics.IDrawContext) -> None:
        """
        RemoveContext method.
        """
        pass

    def Redraw(self) -> None:
        """
        
            Forces the scene to redraw its content.
            
        """
        pass

    def Suspend(self) -> Ansys.ACT.Interfaces.Graphics.ISuspendController:
        """
        
            Prevents the scene to redraw until the Resume controller method was called.
            
        """
        pass

    def ForceResume(self) -> None:
        """
        
            Forces the scene to resume. Useful in interactive context (console) if a reference on an
            operation has been lost.
            
        """
        pass

    def CreatePixelPoint(self, x: int, y: int) -> Ansys.ACT.Interfaces.Graphics.IPixelPoint:
        """
        
            Creates a point from pixel coordinates (ie. window coordinates).
            
        """
        pass

    def CreateWorldPoint(self, x: float, y: float, z: float) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        
            Create a point from world coordinates.
            
        """
        pass

    def CreateVector3D(self, x: float, y: float, z: float) -> Ansys.ACT.Interfaces.Graphics.IVector3D:
        """
        
            Create a 3D vector from world coordinates.
            
        """
        pass

    def CreateAndOpenDraw3DContext(self) -> Ansys.ACT.Interfaces.Graphics.IDraw3DContext:
        """
        CreateAndOpenDraw3DContext method.
        """
        pass

    def DrawText2D(self, x: int, y: int, text: str) -> None:
        """
        DrawText2D method.
        """
        pass

    def MoveTo2D(self, x: int, y: int) -> None:
        """
        MoveTo2D method.
        """
        pass

    def LineTo2D(self, x: int, y: int) -> None:
        """
        LineTo2D method.
        """
        pass

    @typing.overload
    def WorldToPixel(self, pt: typing.Iterable[float]) -> int:
        ...

    @typing.overload
    def WorldToPixel(self, x: float, y: float, z: float) -> int:
        ...

    def WorldToPixel(self, *args: typing.Any) -> int:
        """
        WorldToPixel method.
        """
        pass

    @typing.overload
    def PixelToWorld(self, xy: typing.Iterable[int]) -> float:
        ...

    @typing.overload
    def PixelToWorld(self, x: int, y: int) -> float:
        ...

    def PixelToWorld(self, *args: typing.Any) -> float:
        """
        PixelToWorld method.
        """
        pass


class DMGraphicsWrapper(object):
    """
    
            Wrapper for Graphics in Design Modeler.
            
    """

    @property
    def Unit(self) -> typing.Optional[str]:
        """
        Unit property.
        """
        return None

    @property
    def Camera(self) -> typing.Optional[Ansys.ACT.Interfaces.Graphics.ICamera]:
        """
        Camera property.
        """
        return None

    @property
    def DrawContexts(self) -> typing.Optional[typing.List[Ansys.ACT.Interfaces.Graphics.IDrawContext]]:
        """
        DrawContexts property.
        """
        return None

    @property
    def Scene(self) -> typing.Optional[Ansys.ACT.Interfaces.Graphics.IGraphicsCollection]:
        """
        
            Gets the scene.
            
        """
        return None

    @property
    def LineWeight(self) -> typing.Optional[int]:
        """
        LineWeight property.
        """
        return None

    @LineWeight.setter
    def LineWeight(self, value: typing.Optional[int]) -> None:
        """
        LineWeight property.
        """
        pass

    @property
    def Translucency(self) -> typing.Optional[float]:
        """
        Translucency property.
        """
        return None

    @Translucency.setter
    def Translucency(self, value: typing.Optional[float]) -> None:
        """
        Translucency property.
        """
        pass

    @property
    def Color(self) -> typing.Optional[int]:
        """
        Color property.
        """
        return None

    @Color.setter
    def Color(self, value: typing.Optional[int]) -> None:
        """
        Color property.
        """
        pass

    @property
    def DepthTest(self) -> typing.Optional[bool]:
        """
        DepthTest property.
        """
        return None

    @DepthTest.setter
    def DepthTest(self, value: typing.Optional[bool]) -> None:
        """
        DepthTest property.
        """
        pass

    def __init__(self, dmGraphics: Ansys.Common.Interop.AGGfx.IAGGfxService) -> None:
        """
        __init__ method.
        """
        pass

    def RemoveContext(self, context: Ansys.ACT.Interfaces.Graphics.IDrawContext) -> None:
        """
        RemoveContext method.
        """
        pass

    def Redraw(self) -> None:
        """
        
            Forces the scene to redraw its content.
            
        """
        pass

    def Suspend(self) -> Ansys.ACT.Interfaces.Graphics.ISuspendController:
        """
        
            Prevents the scene to redraw until the Resume controller method was called.
            
        """
        pass

    def ForceResume(self) -> None:
        """
        
            Forces the scene to resume. Useful in interactive context (console) if a reference on an
            operation has been lost.
            
        """
        pass

    def CreatePixelPoint(self, x: int, y: int) -> Ansys.ACT.Interfaces.Graphics.IPixelPoint:
        """
        
            Creates a point from pixel coordinates (ie. window coordinates).
            
        """
        pass

    def CreateWorldPoint(self, x: float, y: float, z: float) -> Ansys.ACT.Interfaces.Graphics.IWorldPoint:
        """
        
            Create a point from world coordinates.
            
        """
        pass

    def CreateVector3D(self, x: float, y: float, z: float) -> Ansys.ACT.Interfaces.Graphics.IVector3D:
        """
        
            Create a 3D vector from world coordinates.
            
        """
        pass

    def CreateAndOpenDraw3DContext(self) -> Ansys.ACT.Interfaces.Graphics.IDraw3DContext:
        """
        CreateAndOpenDraw3DContext method.
        """
        pass

    def DrawText2D(self, x: int, y: int, text: str) -> None:
        """
        DrawText2D method.
        """
        pass

    def MoveTo2D(self, x: int, y: int) -> None:
        """
        MoveTo2D method.
        """
        pass

    def LineTo2D(self, x: int, y: int) -> None:
        """
        LineTo2D method.
        """
        pass

    @typing.overload
    def WorldToPixel(self, pt: typing.Iterable[float]) -> int:
        ...

    @typing.overload
    def WorldToPixel(self, x: float, y: float, z: float) -> int:
        ...

    def WorldToPixel(self, *args: typing.Any) -> int:
        """
        WorldToPixel method.
        """
        pass

    @typing.overload
    def PixelToWorld(self, xy: typing.Iterable[int]) -> float:
        ...

    @typing.overload
    def PixelToWorld(self, x: int, y: int) -> float:
        ...

    def PixelToWorld(self, *args: typing.Any) -> float:
        """
        PixelToWorld method.
        """
        pass

    def ExportScreenToImage(self, filePath: str) -> None:
        """
        
            Exports the current Graphics screen to a file.
            
        """
        pass


class ModelViewManager(object):

    @property
    def NumberOfViews(self) -> typing.Optional[int]:
        """
        
            The number of views currently defined.
            
        """
        return None

    @property
    def ActiveViewPort(self) -> typing.Optional[Ansys.ACT.Common.Graphics.MechanicalViewPort]:
        """
        ActiveViewPort property.
        """
        return None

    def __init__(self, wrapper: Ansys.ACT.Common.Graphics.MechanicalGraphicsWrapper, graphics: Ansys.Common.Interop.Gfx.IDSGraphics) -> None:
        """
        __init__ method.
        """
        pass

    @typing.overload
    def CreateView(self) -> None:
        ...

    @typing.overload
    def CreateView(self, viewName: str) -> None:
        ...

    def CreateView(self, *args: typing.Any) -> None:
        """
        
            Create a view from current graphics with default naming.
            
        """
        pass

    @typing.overload
    def RenameView(self, viewIndex: int, newLabel: str) -> None:
        ...

    @typing.overload
    def RenameView(self, viewLabel: str, newLabel: str) -> None:
        ...

    def RenameView(self, *args: typing.Any) -> None:
        """
        
            Rename the model view specified by viewIndex to newLabel.
            
        """
        pass

    @typing.overload
    def DeleteView(self, viewLabel: str) -> None:
        ...

    @typing.overload
    def DeleteView(self, viewIndex: int) -> None:
        ...

    def DeleteView(self, *args: typing.Any) -> None:
        """
        
            Delete the specified view by name.
            
        """
        pass

    @typing.overload
    def ApplyModelView(self, viewIndex: int) -> None:
        ...

    @typing.overload
    def ApplyModelView(self, viewLabel: str) -> None:
        ...

    def ApplyModelView(self, *args: typing.Any) -> None:
        """
        
            Apply the view specified by index.
            
        """
        pass

    def ImportModelViews(self, viewfilepath: str) -> None:
        """
        
            Import model views from the specified file.
            
        """
        pass

    def ExportModelViews(self, viewfilepath: str) -> None:
        """
        
            Export model views to the specified file.
            
        """
        pass

    @typing.overload
    def CaptureModelView(self, index: int, mode: str) -> None:
        ...

    @typing.overload
    def CaptureModelView(self, viewLabel: str, mode: str) -> None:
        ...

    @typing.overload
    def CaptureModelView(self, viewLabel: str, mode: str, folder: str) -> None:
        ...

    @typing.overload
    def CaptureModelView(self, index: int, mode: str, folder: str) -> None:
        ...

    def CaptureModelView(self, *args: typing.Any) -> None:
        """
        
            Save the view specified by index as an image to the project userfiles.
            
        """
        pass

    def Capture3DImage(self, avzfilepath: str) -> None:
        """
        
            Exports the active object to a 3d AVZ file.
            
        """
        pass

    def CaptureObjectImage(self, obj: Ansys.ACT.Automation.Mechanical.DataModelObject, mode: str, folder: str) -> None:
        """
        
            Save the object specified as an image. The image have the same name as the object.
            
        """
        pass

    def SetISOView(self) -> None:
        """
        
            Change to ISO view.
            
        """
        pass

    def SetFitView(self) -> None:
        """
        
            Change to Fit view.
            
        """
        pass

    def SetFrontView(self) -> None:
        """
        
            Change to Front view.
            
        """
        pass

    def SetBackView(self) -> None:
        """
        
            Change to Back view.
            
        """
        pass

    def SetRightView(self) -> None:
        """
        
            Change to Right view.
            
        """
        pass

    def SetLeftView(self) -> None:
        """
        
            Change to Left view.
            
        """
        pass

    def SetTopView(self) -> None:
        """
        
            Change to Top view.
            
        """
        pass

    def SetBottomView(self) -> None:
        """
        
            Change to Bottom view.
            
        """
        pass

    def RotateView(self, angle: float) -> None:
        """
        
            Rotate the current ModelView.
            
        """
        pass

    @typing.overload
    def SetViewPorts(self, numViewPorts: int, horizontal: bool) -> None:
        ...

    @typing.overload
    def SetViewPorts(self, layout: Ansys.Mechanical.DataModel.Enums.ViewportLayoutStyle) -> None:
        ...

    def SetViewPorts(self, *args: typing.Any) -> None:
        """
        
            Set the number of viewports displayed.
            
        """
        pass

    def GetViewPorts(self) -> Ansys.Mechanical.DataModel.Enums.ViewportLayoutStyle:
        """
        
            Get the viewport display style.
            
        """
        pass

    def GetViewPortSize(self, viewportIndex: int) -> tuple[int,int]:
        """
        
            Returns the width and height of the specified viewport.
            
        """
        pass

    @typing.overload
    def SetActiveViewPort(self, winRowIndex: int, winColIndex: int) -> None:
        ...

    @typing.overload
    def SetActiveViewPort(self, windowsId: int) -> None:
        ...

    def SetActiveViewPort(self, *args: typing.Any) -> None:
        """
        
            Set the active of viewport.
            
        """
        pass


