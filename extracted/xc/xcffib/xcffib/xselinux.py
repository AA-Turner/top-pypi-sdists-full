import xcffib
import struct
import io

MAJOR_VERSION = 1
MINOR_VERSION = 0
key = xcffib.ExtensionKey("SELinux")
_events = {}
_errors = {}
from . import xproto


class QueryVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.server_major, self.server_minor = unpacker.unpack("=xx2x4xHH")
        self.bufsize = unpacker.offset - base


class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply


class GetDeviceCreateContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetDeviceCreateContextCookie(xcffib.Cookie):
    reply_type = GetDeviceCreateContextReply


class GetDeviceContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetDeviceContextCookie(xcffib.Cookie):
    reply_type = GetDeviceContextReply


class GetWindowCreateContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetWindowCreateContextCookie(xcffib.Cookie):
    reply_type = GetWindowCreateContextReply


class GetWindowContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetWindowContextCookie(xcffib.Cookie):
    reply_type = GetWindowContextReply


class ListItem(xcffib.Struct):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.name, self.object_context_len, self.data_context_len = unpacker.unpack(
            "=III"
        )
        self.object_context = xcffib.List(unpacker, "c", self.object_context_len)
        unpacker.pad("c")
        self.data_context = xcffib.List(unpacker, "c", self.data_context_len)
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(
            struct.pack(
                "=III", self.name, self.object_context_len, self.data_context_len
            )
        )
        buf.write(xcffib.pack_list(self.object_context, "c"))
        buf.write(
            struct.pack(
                "=4x",
            )
        )
        buf.write(xcffib.pack_list(self.data_context, "c"))
        buf.write(
            struct.pack(
                "=4x",
            )
        )
        return buf.getvalue()

    @classmethod
    def synthetic(
        cls, name, object_context_len, data_context_len, object_context, data_context
    ):
        self = cls.__new__(cls)
        self.name = name
        self.object_context_len = object_context_len
        self.data_context_len = data_context_len
        self.object_context = object_context
        self.data_context = data_context
        return self


class GetPropertyCreateContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetPropertyCreateContextCookie(xcffib.Cookie):
    reply_type = GetPropertyCreateContextReply


class GetPropertyUseContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetPropertyUseContextCookie(xcffib.Cookie):
    reply_type = GetPropertyUseContextReply


class GetPropertyContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetPropertyContextCookie(xcffib.Cookie):
    reply_type = GetPropertyContextReply


class GetPropertyDataContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetPropertyDataContextCookie(xcffib.Cookie):
    reply_type = GetPropertyDataContextReply


class ListPropertiesReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.properties_len,) = unpacker.unpack("=xx2x4xI20x")
        self.properties = xcffib.List(unpacker, ListItem, self.properties_len)
        self.bufsize = unpacker.offset - base


class ListPropertiesCookie(xcffib.Cookie):
    reply_type = ListPropertiesReply


class GetSelectionCreateContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetSelectionCreateContextCookie(xcffib.Cookie):
    reply_type = GetSelectionCreateContextReply


class GetSelectionUseContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetSelectionUseContextCookie(xcffib.Cookie):
    reply_type = GetSelectionUseContextReply


class GetSelectionContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetSelectionContextCookie(xcffib.Cookie):
    reply_type = GetSelectionContextReply


class GetSelectionDataContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetSelectionDataContextCookie(xcffib.Cookie):
    reply_type = GetSelectionDataContextReply


class ListSelectionsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.selections_len,) = unpacker.unpack("=xx2x4xI20x")
        self.selections = xcffib.List(unpacker, ListItem, self.selections_len)
        self.bufsize = unpacker.offset - base


class ListSelectionsCookie(xcffib.Cookie):
    reply_type = ListSelectionsReply


class GetClientContextReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.context_len,) = unpacker.unpack("=xx2x4xI20x")
        self.context = xcffib.List(unpacker, "c", self.context_len)
        self.bufsize = unpacker.offset - base


class GetClientContextCookie(xcffib.Cookie):
    reply_type = GetClientContextReply


class xselinuxExtension(xcffib.Extension):
    def QueryVersion(self, client_major, client_minor, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xBB", client_major, client_minor))
        return self.send_request(0, buf, QueryVersionCookie, is_checked=is_checked)

    def QueryVersionChecked(self, client_major, client_minor):
        return self.QueryVersion(client_major, client_minor, is_checked=True)

    def QueryVersionUnchecked(self, client_major, client_minor):
        return self.QueryVersion(client_major, client_minor, is_checked=False)

    def SetDeviceCreateContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(1, buf, is_checked=is_checked)

    def SetDeviceCreateContextChecked(self, context_len, context):
        return self.SetDeviceCreateContext(context_len, context, is_checked=True)

    def SetDeviceCreateContextUnchecked(self, context_len, context):
        return self.SetDeviceCreateContext(context_len, context, is_checked=False)

    def GetDeviceCreateContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            2, buf, GetDeviceCreateContextCookie, is_checked=is_checked
        )

    def GetDeviceCreateContextChecked(self):
        return self.GetDeviceCreateContext(is_checked=True)

    def GetDeviceCreateContextUnchecked(self):
        return self.GetDeviceCreateContext(is_checked=False)

    def SetDeviceContext(self, device, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", device, context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(3, buf, is_checked=is_checked)

    def SetDeviceContextChecked(self, device, context_len, context):
        return self.SetDeviceContext(device, context_len, context, is_checked=True)

    def SetDeviceContextUnchecked(self, device, context_len, context):
        return self.SetDeviceContext(device, context_len, context, is_checked=False)

    def GetDeviceContext(self, device, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", device))
        return self.send_request(4, buf, GetDeviceContextCookie, is_checked=is_checked)

    def GetDeviceContextChecked(self, device):
        return self.GetDeviceContext(device, is_checked=True)

    def GetDeviceContextUnchecked(self, device):
        return self.GetDeviceContext(device, is_checked=False)

    def SetWindowCreateContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(5, buf, is_checked=is_checked)

    def SetWindowCreateContextChecked(self, context_len, context):
        return self.SetWindowCreateContext(context_len, context, is_checked=True)

    def SetWindowCreateContextUnchecked(self, context_len, context):
        return self.SetWindowCreateContext(context_len, context, is_checked=False)

    def GetWindowCreateContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            6, buf, GetWindowCreateContextCookie, is_checked=is_checked
        )

    def GetWindowCreateContextChecked(self):
        return self.GetWindowCreateContext(is_checked=True)

    def GetWindowCreateContextUnchecked(self):
        return self.GetWindowCreateContext(is_checked=False)

    def GetWindowContext(self, window, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", window))
        return self.send_request(7, buf, GetWindowContextCookie, is_checked=is_checked)

    def GetWindowContextChecked(self, window):
        return self.GetWindowContext(window, is_checked=True)

    def GetWindowContextUnchecked(self, window):
        return self.GetWindowContext(window, is_checked=False)

    def SetPropertyCreateContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(8, buf, is_checked=is_checked)

    def SetPropertyCreateContextChecked(self, context_len, context):
        return self.SetPropertyCreateContext(context_len, context, is_checked=True)

    def SetPropertyCreateContextUnchecked(self, context_len, context):
        return self.SetPropertyCreateContext(context_len, context, is_checked=False)

    def GetPropertyCreateContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            9, buf, GetPropertyCreateContextCookie, is_checked=is_checked
        )

    def GetPropertyCreateContextChecked(self):
        return self.GetPropertyCreateContext(is_checked=True)

    def GetPropertyCreateContextUnchecked(self):
        return self.GetPropertyCreateContext(is_checked=False)

    def SetPropertyUseContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(10, buf, is_checked=is_checked)

    def SetPropertyUseContextChecked(self, context_len, context):
        return self.SetPropertyUseContext(context_len, context, is_checked=True)

    def SetPropertyUseContextUnchecked(self, context_len, context):
        return self.SetPropertyUseContext(context_len, context, is_checked=False)

    def GetPropertyUseContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            11, buf, GetPropertyUseContextCookie, is_checked=is_checked
        )

    def GetPropertyUseContextChecked(self):
        return self.GetPropertyUseContext(is_checked=True)

    def GetPropertyUseContextUnchecked(self):
        return self.GetPropertyUseContext(is_checked=False)

    def GetPropertyContext(self, window, property, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", window, property))
        return self.send_request(
            12, buf, GetPropertyContextCookie, is_checked=is_checked
        )

    def GetPropertyContextChecked(self, window, property):
        return self.GetPropertyContext(window, property, is_checked=True)

    def GetPropertyContextUnchecked(self, window, property):
        return self.GetPropertyContext(window, property, is_checked=False)

    def GetPropertyDataContext(self, window, property, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xII", window, property))
        return self.send_request(
            13, buf, GetPropertyDataContextCookie, is_checked=is_checked
        )

    def GetPropertyDataContextChecked(self, window, property):
        return self.GetPropertyDataContext(window, property, is_checked=True)

    def GetPropertyDataContextUnchecked(self, window, property):
        return self.GetPropertyDataContext(window, property, is_checked=False)

    def ListProperties(self, window, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", window))
        return self.send_request(14, buf, ListPropertiesCookie, is_checked=is_checked)

    def ListPropertiesChecked(self, window):
        return self.ListProperties(window, is_checked=True)

    def ListPropertiesUnchecked(self, window):
        return self.ListProperties(window, is_checked=False)

    def SetSelectionCreateContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(15, buf, is_checked=is_checked)

    def SetSelectionCreateContextChecked(self, context_len, context):
        return self.SetSelectionCreateContext(context_len, context, is_checked=True)

    def SetSelectionCreateContextUnchecked(self, context_len, context):
        return self.SetSelectionCreateContext(context_len, context, is_checked=False)

    def GetSelectionCreateContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            16, buf, GetSelectionCreateContextCookie, is_checked=is_checked
        )

    def GetSelectionCreateContextChecked(self):
        return self.GetSelectionCreateContext(is_checked=True)

    def GetSelectionCreateContextUnchecked(self):
        return self.GetSelectionCreateContext(is_checked=False)

    def SetSelectionUseContext(self, context_len, context, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", context_len))
        buf.write(xcffib.pack_list(context, "c"))
        return self.send_request(17, buf, is_checked=is_checked)

    def SetSelectionUseContextChecked(self, context_len, context):
        return self.SetSelectionUseContext(context_len, context, is_checked=True)

    def SetSelectionUseContextUnchecked(self, context_len, context):
        return self.SetSelectionUseContext(context_len, context, is_checked=False)

    def GetSelectionUseContext(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(
            18, buf, GetSelectionUseContextCookie, is_checked=is_checked
        )

    def GetSelectionUseContextChecked(self):
        return self.GetSelectionUseContext(is_checked=True)

    def GetSelectionUseContextUnchecked(self):
        return self.GetSelectionUseContext(is_checked=False)

    def GetSelectionContext(self, selection, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", selection))
        return self.send_request(
            19, buf, GetSelectionContextCookie, is_checked=is_checked
        )

    def GetSelectionContextChecked(self, selection):
        return self.GetSelectionContext(selection, is_checked=True)

    def GetSelectionContextUnchecked(self, selection):
        return self.GetSelectionContext(selection, is_checked=False)

    def GetSelectionDataContext(self, selection, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", selection))
        return self.send_request(
            20, buf, GetSelectionDataContextCookie, is_checked=is_checked
        )

    def GetSelectionDataContextChecked(self, selection):
        return self.GetSelectionDataContext(selection, is_checked=True)

    def GetSelectionDataContextUnchecked(self, selection):
        return self.GetSelectionDataContext(selection, is_checked=False)

    def ListSelections(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(21, buf, ListSelectionsCookie, is_checked=is_checked)

    def ListSelectionsChecked(self):
        return self.ListSelections(is_checked=True)

    def ListSelectionsUnchecked(self):
        return self.ListSelections(is_checked=False)

    def GetClientContext(self, resource, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", resource))
        return self.send_request(22, buf, GetClientContextCookie, is_checked=is_checked)

    def GetClientContextChecked(self, resource):
        return self.GetClientContext(resource, is_checked=True)

    def GetClientContextUnchecked(self, resource):
        return self.GetClientContext(resource, is_checked=False)


xcffib._add_ext(key, xselinuxExtension, _events, _errors)
