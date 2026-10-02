import xcffib
import struct
import io

MAJOR_VERSION = 1
MINOR_VERSION = 2
key = xcffib.ExtensionKey("DPMS")
_events = {}
_errors = {}
from . import xproto


class GetVersionReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.server_major_version, self.server_minor_version = unpacker.unpack(
            "=xx2x4xHH"
        )
        self.bufsize = unpacker.offset - base


class GetVersionCookie(xcffib.Cookie):
    reply_type = GetVersionReply


class CapableReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        (self.capable,) = unpacker.unpack("=xx2x4xB23x")
        self.bufsize = unpacker.offset - base


class CapableCookie(xcffib.Cookie):
    reply_type = CapableReply


class GetTimeoutsReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.standby_timeout, self.suspend_timeout, self.off_timeout = unpacker.unpack(
            "=xx2x4xHHH18x"
        )
        self.bufsize = unpacker.offset - base


class GetTimeoutsCookie(xcffib.Cookie):
    reply_type = GetTimeoutsReply


class DPMSMode:
    On = 0
    Standby = 1
    Suspend = 2
    Off = 3


class InfoReply(xcffib.Reply):
    xge = False

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.power_level, self.state = unpacker.unpack("=xx2x4xHB21x")
        self.bufsize = unpacker.offset - base


class InfoCookie(xcffib.Cookie):
    reply_type = InfoReply


class EventMask:
    InfoNotify = 1 << 0


class InfoNotifyEvent(xcffib.Event):
    xge = True

    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Event.__init__(self, unpacker)
        base = unpacker.offset
        self.timestamp, self.power_level, self.state = unpacker.unpack("=xx2x2xIHB21x")
        self.bufsize = unpacker.offset - base

    def pack(self):
        buf = io.BytesIO()
        buf.write(struct.pack("=B", 0))
        buf.write(
            struct.pack("=x2x2xIHB21x", self.timestamp, self.power_level, self.state)
        )
        buf_len = len(buf.getvalue())
        if buf_len < 32:
            buf.write(struct.pack(("%dx" % (32 - buf_len))))
        return buf.getvalue()

    @classmethod
    def synthetic(cls, timestamp, power_level, state):
        self = cls.__new__(cls)
        self.timestamp = timestamp
        self.power_level = power_level
        self.state = state
        return self


_events[0] = InfoNotifyEvent


class dpmsExtension(xcffib.Extension):
    def GetVersion(self, client_major_version, client_minor_version, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xHH", client_major_version, client_minor_version))
        return self.send_request(0, buf, GetVersionCookie, is_checked=is_checked)

    def GetVersionChecked(self, client_major_version, client_minor_version):
        return self.GetVersion(
            client_major_version, client_minor_version, is_checked=True
        )

    def GetVersionUnchecked(self, client_major_version, client_minor_version):
        return self.GetVersion(
            client_major_version, client_minor_version, is_checked=False
        )

    def Capable(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(1, buf, CapableCookie, is_checked=is_checked)

    def CapableChecked(self):
        return self.Capable(is_checked=True)

    def CapableUnchecked(self):
        return self.Capable(is_checked=False)

    def GetTimeouts(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(2, buf, GetTimeoutsCookie, is_checked=is_checked)

    def GetTimeoutsChecked(self):
        return self.GetTimeouts(is_checked=True)

    def GetTimeoutsUnchecked(self):
        return self.GetTimeouts(is_checked=False)

    def SetTimeouts(
        self, standby_timeout, suspend_timeout, off_timeout, is_checked=False
    ):
        buf = io.BytesIO()
        buf.write(
            struct.pack("=xx2xHHH", standby_timeout, suspend_timeout, off_timeout)
        )
        return self.send_request(3, buf, is_checked=is_checked)

    def SetTimeoutsChecked(self, standby_timeout, suspend_timeout, off_timeout):
        return self.SetTimeouts(
            standby_timeout, suspend_timeout, off_timeout, is_checked=True
        )

    def SetTimeoutsUnchecked(self, standby_timeout, suspend_timeout, off_timeout):
        return self.SetTimeouts(
            standby_timeout, suspend_timeout, off_timeout, is_checked=False
        )

    def Enable(self, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(4, buf, is_checked=is_checked)

    def EnableChecked(self):
        return self.Enable(is_checked=True)

    def EnableUnchecked(self):
        return self.Enable(is_checked=False)

    def Disable(self, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(5, buf, is_checked=is_checked)

    def DisableChecked(self):
        return self.Disable(is_checked=True)

    def DisableUnchecked(self):
        return self.Disable(is_checked=False)

    def ForceLevel(self, power_level, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xH", power_level))
        return self.send_request(6, buf, is_checked=is_checked)

    def ForceLevelChecked(self, power_level):
        return self.ForceLevel(power_level, is_checked=True)

    def ForceLevelUnchecked(self, power_level):
        return self.ForceLevel(power_level, is_checked=False)

    def Info(self, is_checked=True):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(7, buf, InfoCookie, is_checked=is_checked)

    def InfoChecked(self):
        return self.Info(is_checked=True)

    def InfoUnchecked(self):
        return self.Info(is_checked=False)

    def SelectInput(self, event_mask, is_checked=False):
        buf = io.BytesIO()
        buf.write(struct.pack("=xx2xI", event_mask))
        return self.send_request(8, buf, is_checked=is_checked)

    def SelectInputChecked(self, event_mask):
        return self.SelectInput(event_mask, is_checked=True)

    def SelectInputUnchecked(self, event_mask):
        return self.SelectInput(event_mask, is_checked=False)


xcffib._add_ext(key, dpmsExtension, _events, _errors)
