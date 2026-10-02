import xcffib
import struct
import io

MAJOR_VERSION = 0
MINOR_VERSION = 4
key = xcffib.ExtensionKey("Composite")
_events = {}
_errors = {}
from . import xproto
from . import xfixes


class Redirect:
    Automatic = 0
    Manual = 1


class QueryVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.major_version, self.minor_version = unpacker.unpack("=xx2x4xII16x")
        self.bufsize = unpacker.offset - base


class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply


class GetOverlayWindowReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.overlay_win,) = unpacker.unpack("=xx2x4xI20x")
        self.bufsize = unpacker.offset - base


class GetOverlayWindowCookie(xcffib.Cookie):
    reply_type = GetOverlayWindowReply


class compositeExtension(xcffib.Extension):
    def QueryVersion(self, client_major_version, client_minor_version, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", client_major_version, client_minor_version))
        return self.send_request(0, buf, QueryVersionCookie, is_checked=is_checked)

    def QueryVersionChecked(self, client_major_version, client_minor_version):
        return self.QueryVersion(
            client_major_version, client_minor_version, is_checked=True
        )

    def QueryVersionUnchecked(self, client_major_version, client_minor_version):
        return self.QueryVersion(
            client_major_version, client_minor_version, is_checked=False
        )

    def RedirectWindow(self, window, update, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", window, update))
        return self.send_request(1, buf, is_checked=is_checked)

    def RedirectWindowChecked(self, window, update):
        return self.RedirectWindow(window, update, is_checked=True)

    def RedirectWindowUnchecked(self, window, update):
        return self.RedirectWindow(window, update, is_checked=False)

    def RedirectSubwindows(self, window, update, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", window, update))
        return self.send_request(2, buf, is_checked=is_checked)

    def RedirectSubwindowsChecked(self, window, update):
        return self.RedirectSubwindows(window, update, is_checked=True)

    def RedirectSubwindowsUnchecked(self, window, update):
        return self.RedirectSubwindows(window, update, is_checked=False)

    def UnredirectWindow(self, window, update, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", window, update))
        return self.send_request(3, buf, is_checked=is_checked)

    def UnredirectWindowChecked(self, window, update):
        return self.UnredirectWindow(window, update, is_checked=True)

    def UnredirectWindowUnchecked(self, window, update):
        return self.UnredirectWindow(window, update, is_checked=False)

    def UnredirectSubwindows(self, window, update, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", window, update))
        return self.send_request(4, buf, is_checked=is_checked)

    def UnredirectSubwindowsChecked(self, window, update):
        return self.UnredirectSubwindows(window, update, is_checked=True)

    def UnredirectSubwindowsUnchecked(self, window, update):
        return self.UnredirectSubwindows(window, update, is_checked=False)

    def CreateRegionFromBorderClip(self, region, window, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", region, window))
        return self.send_request(5, buf, is_checked=is_checked)

    def CreateRegionFromBorderClipChecked(self, region, window):
        return self.CreateRegionFromBorderClip(region, window, is_checked=True)

    def CreateRegionFromBorderClipUnchecked(self, region, window):
        return self.CreateRegionFromBorderClip(region, window, is_checked=False)

    def NameWindowPixmap(self, window, pixmap, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", window, pixmap))
        return self.send_request(6, buf, is_checked=is_checked)

    def NameWindowPixmapChecked(self, window, pixmap):
        return self.NameWindowPixmap(window, pixmap, is_checked=True)

    def NameWindowPixmapUnchecked(self, window, pixmap):
        return self.NameWindowPixmap(window, pixmap, is_checked=False)

    def GetOverlayWindow(self, window, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", window))
        return self.send_request(7, buf, GetOverlayWindowCookie, is_checked=is_checked)

    def GetOverlayWindowChecked(self, window):
        return self.GetOverlayWindow(window, is_checked=True)

    def GetOverlayWindowUnchecked(self, window):
        return self.GetOverlayWindow(window, is_checked=False)

    def ReleaseOverlayWindow(self, window, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", window))
        return self.send_request(8, buf, is_checked=is_checked)

    def ReleaseOverlayWindowChecked(self, window):
        return self.ReleaseOverlayWindow(window, is_checked=True)

    def ReleaseOverlayWindowUnchecked(self, window):
        return self.ReleaseOverlayWindow(window, is_checked=False)


xcffib._add_ext(key, compositeExtension, _events, _errors)
