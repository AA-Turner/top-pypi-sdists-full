"""Common module."""
from __future__ import annotations
import typing
if typing.TYPE_CHECKING:
    import Ansys
import ansys.mechanical.stubs.v261.Ansys.ACT.Common.Graphics as Graphics


class BrowserQt(object):

    @property
    def Html(self) -> typing.Optional[str]:
        """
        Html property.
        """
        return None

    @Html.setter
    def Html(self, value: typing.Optional[str]) -> None:
        """
        Html property.
        """
        pass

    @property
    def UseAnsEventTracker(self) -> typing.Optional[bool]:
        """
        UseAnsEventTracker property.
        """
        return None

    @UseAnsEventTracker.setter
    def UseAnsEventTracker(self, value: typing.Optional[bool]) -> None:
        """
        UseAnsEventTracker property.
        """
        pass

    @property
    def CanGoBack(self) -> typing.Optional[bool]:
        """
        CanGoBack property.
        """
        return None

    @property
    def CanGoForward(self) -> typing.Optional[bool]:
        """
        CanGoForward property.
        """
        return None

    @property
    def PreventNavigation(self) -> typing.Optional[bool]:
        """
        PreventNavigation property.
        """
        return None

    @PreventNavigation.setter
    def PreventNavigation(self, value: typing.Optional[bool]) -> None:
        """
        PreventNavigation property.
        """
        pass

    @property
    def ZoomFactor(self) -> typing.Optional[System.Single]:
        """
        ZoomFactor property.
        """
        return None

    @ZoomFactor.setter
    def ZoomFactor(self, value: typing.Optional[System.Single]) -> None:
        """
        ZoomFactor property.
        """
        pass

    @property
    def Url(self) -> typing.Optional[System.Uri]:
        """
        Url property.
        """
        return None

    @Url.setter
    def Url(self, value: typing.Optional[System.Uri]) -> None:
        """
        Url property.
        """
        pass

    @property
    def WebPage(self) -> typing.Optional[Ansys.UI.Toolkit.WebBrowser.WebPage]:
        """
        WebPage property.
        """
        return None

    @property
    def DataObjects(self) -> typing.Optional[Ansys.UI.Toolkit.WebBrowser.WebBrowser.DataObjectCollection]:
        """
        DataObjects property.
        """
        return None

    @property
    def WebSockets(self) -> typing.Optional[Ansys.UI.Toolkit.WebBrowser.WebBrowser.WebSocketCollection]:
        """
        WebSockets property.
        """
        return None

    @property
    def Tag(self) -> typing.Optional[typing.Any]:
        """
        Tag property.
        """
        return None

    @Tag.setter
    def Tag(self, value: typing.Optional[typing.Any]) -> None:
        """
        Tag property.
        """
        pass

    @property
    def Handle(self) -> typing.Optional[System.IntPtr]:
        """
        Handle property.
        """
        return None

    @property
    def InvokeRequired(self) -> typing.Optional[bool]:
        """
        InvokeRequired property.
        """
        return None

    @property
    def Parent(self) -> typing.Optional[Ansys.UI.Toolkit.Control]:
        """
        Parent property.
        """
        return None

    @Parent.setter
    def Parent(self, value: typing.Optional[Ansys.UI.Toolkit.Control]) -> None:
        """
        Parent property.
        """
        pass

    @property
    def OwnerDrawn(self) -> typing.Optional[bool]:
        """
        OwnerDrawn property.
        """
        return None

    @OwnerDrawn.setter
    def OwnerDrawn(self, value: typing.Optional[bool]) -> None:
        """
        OwnerDrawn property.
        """
        pass

    @property
    def Enabled(self) -> typing.Optional[bool]:
        """
        Enabled property.
        """
        return None

    @Enabled.setter
    def Enabled(self, value: typing.Optional[bool]) -> None:
        """
        Enabled property.
        """
        pass

    @property
    def Visible(self) -> typing.Optional[bool]:
        """
        Visible property.
        """
        return None

    @Visible.setter
    def Visible(self, value: typing.Optional[bool]) -> None:
        """
        Visible property.
        """
        pass

    @property
    def Cursor(self) -> typing.Optional[Ansys.UI.Toolkit.Cursor]:
        """
        Cursor property.
        """
        return None

    @Cursor.setter
    def Cursor(self, value: typing.Optional[Ansys.UI.Toolkit.Cursor]) -> None:
        """
        Cursor property.
        """
        pass

    @property
    def Controls(self) -> typing.Optional[Ansys.UI.Toolkit.ControlCollection]:
        """
        Controls property.
        """
        return None

    @property
    def Font(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Font]:
        """
        Font property.
        """
        return None

    @Font.setter
    def Font(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Font]) -> None:
        """
        Font property.
        """
        pass

    @property
    def BackColor(self) -> typing.Optional[Ansys.Utilities.Color]:
        """
        BackColor property.
        """
        return None

    @BackColor.setter
    def BackColor(self, value: typing.Optional[Ansys.Utilities.Color]) -> None:
        """
        BackColor property.
        """
        pass

    @property
    def ForeColor(self) -> typing.Optional[Ansys.Utilities.Color]:
        """
        ForeColor property.
        """
        return None

    @ForeColor.setter
    def ForeColor(self, value: typing.Optional[Ansys.Utilities.Color]) -> None:
        """
        ForeColor property.
        """
        pass

    @property
    def Focused(self) -> typing.Optional[bool]:
        """
        Focused property.
        """
        return None

    @property
    def AllowDrop(self) -> typing.Optional[bool]:
        """
        AllowDrop property.
        """
        return None

    @AllowDrop.setter
    def AllowDrop(self, value: typing.Optional[bool]) -> None:
        """
        AllowDrop property.
        """
        pass

    @property
    def IsMouseCaptured(self) -> typing.Optional[bool]:
        """
        IsMouseCaptured property.
        """
        return None

    @IsMouseCaptured.setter
    def IsMouseCaptured(self, value: typing.Optional[bool]) -> None:
        """
        IsMouseCaptured property.
        """
        pass

    @property
    def Width(self) -> typing.Optional[int]:
        """
        Width property.
        """
        return None

    @Width.setter
    def Width(self, value: typing.Optional[int]) -> None:
        """
        Width property.
        """
        pass

    @property
    def Height(self) -> typing.Optional[int]:
        """
        Height property.
        """
        return None

    @Height.setter
    def Height(self, value: typing.Optional[int]) -> None:
        """
        Height property.
        """
        pass

    @property
    def Size(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Size]:
        """
        Size property.
        """
        return None

    @Size.setter
    def Size(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Size]) -> None:
        """
        Size property.
        """
        pass

    @property
    def Left(self) -> typing.Optional[int]:
        """
        Left property.
        """
        return None

    @Left.setter
    def Left(self, value: typing.Optional[int]) -> None:
        """
        Left property.
        """
        pass

    @property
    def Top(self) -> typing.Optional[int]:
        """
        Top property.
        """
        return None

    @Top.setter
    def Top(self, value: typing.Optional[int]) -> None:
        """
        Top property.
        """
        pass

    @property
    def Location(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Point]:
        """
        Location property.
        """
        return None

    @Location.setter
    def Location(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Point]) -> None:
        """
        Location property.
        """
        pass

    @property
    def Bounds(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Rectangle]:
        """
        Bounds property.
        """
        return None

    @Bounds.setter
    def Bounds(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Rectangle]) -> None:
        """
        Bounds property.
        """
        pass

    @property
    def Margins(self) -> typing.Optional[Ansys.UI.Toolkit.Padding]:
        """
        Margins property.
        """
        return None

    @Margins.setter
    def Margins(self, value: typing.Optional[Ansys.UI.Toolkit.Padding]) -> None:
        """
        Margins property.
        """
        pass

    @property
    def PreferredSize(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Size]:
        """
        PreferredSize property.
        """
        return None

    @property
    def MinimumSize(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Size]:
        """
        MinimumSize property.
        """
        return None

    @MinimumSize.setter
    def MinimumSize(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Size]) -> None:
        """
        MinimumSize property.
        """
        pass

    @property
    def MaximumSize(self) -> typing.Optional[Ansys.UI.Toolkit.Drawing.Size]:
        """
        MaximumSize property.
        """
        return None

    @MaximumSize.setter
    def MaximumSize(self, value: typing.Optional[Ansys.UI.Toolkit.Drawing.Size]) -> None:
        """
        MaximumSize property.
        """
        pass

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
    def ToolTipText(self) -> typing.Optional[str]:
        """
        ToolTipText property.
        """
        return None

    @ToolTipText.setter
    def ToolTipText(self, value: typing.Optional[str]) -> None:
        """
        ToolTipText property.
        """
        pass

    @property
    def WhatsThisText(self) -> typing.Optional[str]:
        """
        WhatsThisText property.
        """
        return None

    @WhatsThisText.setter
    def WhatsThisText(self, value: typing.Optional[str]) -> None:
        """
        WhatsThisText property.
        """
        pass

    @property
    def IsDisposed(self) -> typing.Optional[bool]:
        """
        IsDisposed property.
        """
        return None

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass

    def NavigateToPage(self, page: str, args: str) -> None:
        """
        NavigateToPage method.
        """
        pass

    def add_Navigated(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserNavigatedEventDelagate) -> None:
        """
        add_Navigated method.
        """
        pass

    def remove_Navigated(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserNavigatedEventDelagate) -> None:
        """
        remove_Navigated method.
        """
        pass

    def add_ProgressChanged(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserProgressChangedEventDelegate) -> None:
        """
        add_ProgressChanged method.
        """
        pass

    def remove_ProgressChanged(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserProgressChangedEventDelegate) -> None:
        """
        remove_ProgressChanged method.
        """
        pass

    def add_LoadFinished(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_LoadFinished method.
        """
        pass

    def remove_LoadFinished(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_LoadFinished method.
        """
        pass

    def add_LoadStarted(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_LoadStarted method.
        """
        pass

    def remove_LoadStarted(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_LoadStarted method.
        """
        pass

    def add_LinkClicked(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserLinkClickedEventDelegate) -> None:
        """
        add_LinkClicked method.
        """
        pass

    def remove_LinkClicked(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserLinkClickedEventDelegate) -> None:
        """
        remove_LinkClicked method.
        """
        pass

    def add_CreateWindow(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserCreateWindowEventDelegate) -> None:
        """
        add_CreateWindow method.
        """
        pass

    def remove_CreateWindow(self, value: Ansys.UI.Toolkit.WebBrowser.WebBrowserCreateWindowEventDelegate) -> None:
        """
        remove_CreateWindow method.
        """
        pass

    def add_ContextMenu(self, value: Ansys.UI.Toolkit.WebBrowser.ContextMenuEventDelegate) -> None:
        """
        add_ContextMenu method.
        """
        pass

    def remove_ContextMenu(self, value: Ansys.UI.Toolkit.WebBrowser.ContextMenuEventDelegate) -> None:
        """
        remove_ContextMenu method.
        """
        pass

    def add_DownloadCompleted(self, value: Ansys.UI.Toolkit.WebBrowser.FileDownloadCompletedDelegate) -> None:
        """
        add_DownloadCompleted method.
        """
        pass

    def remove_DownloadCompleted(self, value: Ansys.UI.Toolkit.WebBrowser.FileDownloadCompletedDelegate) -> None:
        """
        remove_DownloadCompleted method.
        """
        pass

    def Dispose(self) -> None:
        """
        Dispose method.
        """
        pass

    def GoBack(self) -> None:
        """
        GoBack method.
        """
        pass

    def GoForward(self) -> None:
        """
        GoForward method.
        """
        pass

    def GoHome(self) -> None:
        """
        GoHome method.
        """
        pass

    def ClearHistory(self) -> None:
        """
        ClearHistory method.
        """
        pass

    @typing.overload
    def Navigate(self, url: str) -> None:
        ...

    @typing.overload
    def Navigate(self, url: System.Uri) -> None:
        ...

    def Navigate(self, *args: typing.Any) -> None:
        """
        Navigate method.
        """
        pass

    def Print(self) -> None:
        """
        Print method.
        """
        pass

    def Reload(self) -> None:
        """
        Reload method.
        """
        pass

    def Stop(self) -> None:
        """
        Stop method.
        """
        pass

    def FindText(self, subString: str, options: Ansys.UI.Toolkit.WebBrowser.WebPageFindFlags) -> bool:
        """
        FindText method.
        """
        pass

    def SetHtml(self, html: str, baseUrl: str) -> None:
        """
        SetHtml method.
        """
        pass

    def GetLocalURI(self, relativePath: str) -> str:
        """
        GetLocalURI method.
        """
        pass

    def GenerateMenuItem(self, action: Ansys.UI.Toolkit.WebBrowser.WebAction) -> Ansys.UI.Toolkit.MenuItem:
        """
        GenerateMenuItem method.
        """
        pass

    def TriggerPageAction(self, action: Ansys.UI.Toolkit.WebBrowser.WebAction) -> None:
        """
        TriggerPageAction method.
        """
        pass

    def add_GotFocus(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_GotFocus method.
        """
        pass

    def remove_GotFocus(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_GotFocus method.
        """
        pass

    def add_LostFocus(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_LostFocus method.
        """
        pass

    def remove_LostFocus(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_LostFocus method.
        """
        pass

    def add_VisibilityChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_VisibilityChanged method.
        """
        pass

    def remove_VisibilityChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_VisibilityChanged method.
        """
        pass

    def add_MouseDown(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        add_MouseDown method.
        """
        pass

    def remove_MouseDown(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        remove_MouseDown method.
        """
        pass

    def add_MouseUp(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        add_MouseUp method.
        """
        pass

    def remove_MouseUp(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        remove_MouseUp method.
        """
        pass

    def add_MouseMove(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        add_MouseMove method.
        """
        pass

    def remove_MouseMove(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        remove_MouseMove method.
        """
        pass

    def add_MouseWheel(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        add_MouseWheel method.
        """
        pass

    def remove_MouseWheel(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        remove_MouseWheel method.
        """
        pass

    def add_MouseDoubleClick(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        add_MouseDoubleClick method.
        """
        pass

    def remove_MouseDoubleClick(self, value: Ansys.UI.Toolkit.MouseEventDelegate) -> None:
        """
        remove_MouseDoubleClick method.
        """
        pass

    def add_MouseEnter(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_MouseEnter method.
        """
        pass

    def remove_MouseEnter(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_MouseEnter method.
        """
        pass

    def add_MouseLeave(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_MouseLeave method.
        """
        pass

    def remove_MouseLeave(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_MouseLeave method.
        """
        pass

    def add_KeyDown(self, value: Ansys.UI.Toolkit.KeyEventDelegate) -> None:
        """
        add_KeyDown method.
        """
        pass

    def remove_KeyDown(self, value: Ansys.UI.Toolkit.KeyEventDelegate) -> None:
        """
        remove_KeyDown method.
        """
        pass

    def add_KeyPress(self, value: Ansys.UI.Toolkit.KeyPressEventDelegate) -> None:
        """
        add_KeyPress method.
        """
        pass

    def remove_KeyPress(self, value: Ansys.UI.Toolkit.KeyPressEventDelegate) -> None:
        """
        remove_KeyPress method.
        """
        pass

    def add_KeyUp(self, value: Ansys.UI.Toolkit.KeyEventDelegate) -> None:
        """
        add_KeyUp method.
        """
        pass

    def remove_KeyUp(self, value: Ansys.UI.Toolkit.KeyEventDelegate) -> None:
        """
        remove_KeyUp method.
        """
        pass

    def add_SizeChanged(self, value: Ansys.UI.Toolkit.SizeChangedEventDelegate) -> None:
        """
        add_SizeChanged method.
        """
        pass

    def remove_SizeChanged(self, value: Ansys.UI.Toolkit.SizeChangedEventDelegate) -> None:
        """
        remove_SizeChanged method.
        """
        pass

    def add_LocationChanged(self, value: Ansys.UI.Toolkit.LocationChangedEventDelegate) -> None:
        """
        add_LocationChanged method.
        """
        pass

    def remove_LocationChanged(self, value: Ansys.UI.Toolkit.LocationChangedEventDelegate) -> None:
        """
        remove_LocationChanged method.
        """
        pass

    def add_FontChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_FontChanged method.
        """
        pass

    def remove_FontChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_FontChanged method.
        """
        pass

    def add_ParentChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_ParentChanged method.
        """
        pass

    def remove_ParentChanged(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_ParentChanged method.
        """
        pass

    def add_ControlAdded(self, value: Ansys.UI.Toolkit.ControlEventDelegate) -> None:
        """
        add_ControlAdded method.
        """
        pass

    def remove_ControlAdded(self, value: Ansys.UI.Toolkit.ControlEventDelegate) -> None:
        """
        remove_ControlAdded method.
        """
        pass

    def add_ControlRemoved(self, value: Ansys.UI.Toolkit.ControlEventDelegate) -> None:
        """
        add_ControlRemoved method.
        """
        pass

    def remove_ControlRemoved(self, value: Ansys.UI.Toolkit.ControlEventDelegate) -> None:
        """
        remove_ControlRemoved method.
        """
        pass

    def add_DragEnter(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        add_DragEnter method.
        """
        pass

    def remove_DragEnter(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        remove_DragEnter method.
        """
        pass

    def add_DragMove(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        add_DragMove method.
        """
        pass

    def remove_DragMove(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        remove_DragMove method.
        """
        pass

    def add_DragLeave(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        add_DragLeave method.
        """
        pass

    def remove_DragLeave(self, value: Ansys.UI.Toolkit.EventDelegate) -> None:
        """
        remove_DragLeave method.
        """
        pass

    def add_DragDrop(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        add_DragDrop method.
        """
        pass

    def remove_DragDrop(self, value: Ansys.UI.Toolkit.DragEventDelegate) -> None:
        """
        remove_DragDrop method.
        """
        pass

    def add_DoDragDropCompleted(self, value: Ansys.UI.Toolkit.DragDropCompletedEventDelegate) -> None:
        """
        add_DoDragDropCompleted method.
        """
        pass

    def remove_DoDragDropCompleted(self, value: Ansys.UI.Toolkit.DragDropCompletedEventDelegate) -> None:
        """
        remove_DoDragDropCompleted method.
        """
        pass

    def add_BeforeToolTip(self, value: Ansys.UI.Toolkit.ToolTipEventEventDelegate) -> None:
        """
        add_BeforeToolTip method.
        """
        pass

    def remove_BeforeToolTip(self, value: Ansys.UI.Toolkit.ToolTipEventEventDelegate) -> None:
        """
        remove_BeforeToolTip method.
        """
        pass

    def add_WhatsThis(self, value: Ansys.UI.Toolkit.WhatsThisEventEventDelegate) -> None:
        """
        add_WhatsThis method.
        """
        pass

    def remove_WhatsThis(self, value: Ansys.UI.Toolkit.WhatsThisEventEventDelegate) -> None:
        """
        remove_WhatsThis method.
        """
        pass

    def add_WhatsThisLinkClicked(self, value: Ansys.UI.Toolkit.WhatsThisLinkClickedEventDelegate) -> None:
        """
        add_WhatsThisLinkClicked method.
        """
        pass

    def remove_WhatsThisLinkClicked(self, value: Ansys.UI.Toolkit.WhatsThisLinkClickedEventDelegate) -> None:
        """
        remove_WhatsThisLinkClicked method.
        """
        pass

    def add_Paint(self, value: Ansys.UI.Toolkit.Drawing.PaintEventDelegate) -> None:
        """
        add_Paint method.
        """
        pass

    def remove_Paint(self, value: Ansys.UI.Toolkit.Drawing.PaintEventDelegate) -> None:
        """
        remove_Paint method.
        """
        pass

    def FindParentWindow(self) -> Ansys.UI.Toolkit.Window:
        """
        FindParentWindow method.
        """
        pass

    def FindParentDialog(self) -> Ansys.UI.Toolkit.Dialog:
        """
        FindParentDialog method.
        """
        pass

    def FindTopMostParentControl(self) -> Ansys.UI.Toolkit.Control:
        """
        FindTopMostParentControl method.
        """
        pass

    def PointToClient(self, point: Ansys.UI.Toolkit.Drawing.Point) -> Ansys.UI.Toolkit.Drawing.Point:
        """
        PointToClient method.
        """
        pass

    def PointToGlobal(self, point: Ansys.UI.Toolkit.Drawing.Point) -> Ansys.UI.Toolkit.Drawing.Point:
        """
        PointToGlobal method.
        """
        pass

    def Focus(self) -> None:
        """
        Focus method.
        """
        pass

    def FocusNextControl(self, forward: bool) -> bool:
        """
        FocusNextControl method.
        """
        pass

    def SendToBack(self) -> None:
        """
        SendToBack method.
        """
        pass

    def BringToFront(self) -> None:
        """
        BringToFront method.
        """
        pass

    def Show(self) -> None:
        """
        Show method.
        """
        pass

    def Hide(self) -> None:
        """
        Hide method.
        """
        pass

    def GetPreferredSize(self) -> Ansys.UI.Toolkit.Drawing.Size:
        """
        GetPreferredSize method.
        """
        pass

    def GetPreferredHeightForWidth(self, width: int) -> int:
        """
        GetPreferredHeightForWidth method.
        """
        pass

    @typing.overload
    def Invalidate(self) -> None:
        ...

    @typing.overload
    def Invalidate(self, rectangle: Ansys.UI.Toolkit.Drawing.Rectangle) -> None:
        ...

    def Invalidate(self, *args: typing.Any) -> None:
        """
        Invalidate method.
        """
        pass

    def Update(self) -> None:
        """
        Update method.
        """
        pass

    @typing.overload
    def Refresh(self) -> None:
        ...

    @typing.overload
    def Refresh(self, rectangle: Ansys.UI.Toolkit.Drawing.Rectangle) -> None:
        ...

    def Refresh(self, *args: typing.Any) -> None:
        """
        Refresh method.
        """
        pass

    def DoDragDrop(self, data: Ansys.UI.Toolkit.DataObject, allowedEffects: Ansys.UI.Toolkit.DragDropEffects) -> Ansys.UI.Toolkit.DragDropEffects:
        """
        DoDragDrop method.
        """
        pass

    def Invoke(self, method: typing.Callable, args: typing.Any) -> typing.Any:
        """
        Invoke method.
        """
        pass

    def BeginInvoke(self, method: typing.Callable, args: typing.Any) -> "System.IAsyncResult":
        """
        BeginInvoke method.
        """
        pass

    def EndInvoke(self, asyncResult: "System.IAsyncResult") -> typing.Any:
        """
        EndInvoke method.
        """
        pass

    def OnThemeChanged(self, newTheme: Ansys.UI.Toolkit.Themes.ITheme) -> None:
        """
        OnThemeChanged method.
        """
        pass


class CoordinateSystem(object):
    """
    
            CoordinateSystem class
            
    """

    @property
    def CoordinateSystemType(self) -> typing.Optional[Ansys.ACT.Interfaces.Analysis.CoordinateSystemTypeEnum]:
        """
        
            Gets or sets the coordinate system type.
            
        """
        return None

    @CoordinateSystemType.setter
    def CoordinateSystemType(self, value: typing.Optional[Ansys.ACT.Interfaces.Analysis.CoordinateSystemTypeEnum]) -> None:
        """
        
            Gets or sets the coordinate system type.
            
        """
        pass

    @property
    def Name(self) -> typing.Optional[str]:
        """
        
            Gets or sets the name of the coordinate system.
            
        """
        return None

    @Name.setter
    def Name(self, value: typing.Optional[str]) -> None:
        """
        
            Gets or sets the name of the coordinate system.
            
        """
        pass

    @property
    def Id(self) -> typing.Optional[int]:
        """
        
            Gets or sets the ID of the coordinate system.
            
        """
        return None

    @Id.setter
    def Id(self, value: typing.Optional[int]) -> None:
        """
        
            Gets or sets the ID of the coordinate system.
            
        """
        pass

    @property
    def Origin(self) -> typing.Optional[typing.Iterable[float]]:
        """
        
            Gets or sets the origin of the coordinate system.
            
        """
        return None

    @Origin.setter
    def Origin(self, value: typing.Optional[typing.Iterable[float]]) -> None:
        """
        
            Gets or sets the origin of the coordinate system.
            
        """
        pass

    @property
    def Matrix(self) -> typing.Optional[typing.Iterable[float]]:
        """
        
            Gets or sets the matrix definition of the coordinate system.
            
        """
        return None

    @Matrix.setter
    def Matrix(self, value: typing.Optional[typing.Iterable[float]]) -> None:
        """
        
            Gets or sets the matrix definition of the coordinate system.
            
        """
        pass

    @property
    def XAxis(self) -> typing.Optional[typing.Iterable[float]]:
        """
        
            Gets or sets the X axis of the coordinate system.
            
        """
        return None

    @XAxis.setter
    def XAxis(self, value: typing.Optional[typing.Iterable[float]]) -> None:
        """
        
            Gets or sets the X axis of the coordinate system.
            
        """
        pass

    @property
    def YAxis(self) -> typing.Optional[typing.Iterable[float]]:
        """
        
            Gets or sets the Y axis of the coordinate system.
            
        """
        return None

    @YAxis.setter
    def YAxis(self, value: typing.Optional[typing.Iterable[float]]) -> None:
        """
        
            Gets or sets the Y axis of the coordinate system.
            
        """
        pass

    @property
    def ZAxis(self) -> typing.Optional[typing.Iterable[float]]:
        """
        
            Gets or sets the Z axis of the coordinate system.
            
        """
        return None

    @ZAxis.setter
    def ZAxis(self, value: typing.Optional[typing.Iterable[float]]) -> None:
        """
        
            Gets or sets the Z axis of the coordinate system.
            
        """
        pass

    def __init__(self, type: Ansys.ACT.Interfaces.Analysis.CoordinateSystemTypeEnum) -> None:
        """
        
            Constructor.
            
        """
        pass


class SimpleTransform(object):
    """
    
            Exposes simple getters and setters for rigid body transformations.
            
    """

    @property
    def TransformationMatrix(self) -> typing.Optional[Ansys.Mechanical.DataModel.Utilities.RigidBodyTransformationMatrix]:
        """
        TransformationMatrix property.
        """
        return None

    @TransformationMatrix.setter
    def TransformationMatrix(self, value: typing.Optional[Ansys.Mechanical.DataModel.Utilities.RigidBodyTransformationMatrix]) -> None:
        """
        TransformationMatrix property.
        """
        pass

    @property
    def IsOrthonormal(self) -> typing.Optional[bool]:
        """
        
            Returns `true` if the provided axis vectors are all normalized and orthogonal.
            
        """
        return None

    @property
    def Translation(self) -> typing.Optional[Ansys.ACT.Core.Math.Point3D]:
        """
        
            The translation of the transformation with respect to the global/world coordinate
            system.
            
        """
        return None

    @Translation.setter
    def Translation(self, value: typing.Optional[Ansys.ACT.Core.Math.Point3D]) -> None:
        """
        
            The translation of the transformation with respect to the global/world coordinate
            system.
            
        """
        pass

    @property
    def XAxis(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
            The X-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        return None

    @XAxis.setter
    def XAxis(self, value: typing.Optional[Ansys.ACT.Core.Math.Vector3D]) -> None:
        """
        
            The X-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        pass

    @property
    def YAxis(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
            The Y-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        return None

    @YAxis.setter
    def YAxis(self, value: typing.Optional[Ansys.ACT.Core.Math.Vector3D]) -> None:
        """
        
            The Y-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        pass

    @property
    def ZAxis(self) -> typing.Optional[Ansys.ACT.Core.Math.Vector3D]:
        """
        
            The X-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        return None

    @ZAxis.setter
    def ZAxis(self, value: typing.Optional[Ansys.ACT.Core.Math.Vector3D]) -> None:
        """
        
            The X-axis orientation of the transformation with respect to the global/world
            coordinate system.
            
        """
        pass

    def __init__(self) -> None:
        """
        __init__ method.
        """
        pass


