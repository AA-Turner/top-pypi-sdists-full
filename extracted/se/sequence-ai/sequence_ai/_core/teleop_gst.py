"""
Teleop's second WebRTC stack: GStreamer's webrtcbin on the robot's side, the transport "gstreamer" (teleop_transport) -
the wire aiortc's speaks (teleop_direct): its five channels and their pieces, its answer said the same way, each camera
an H.264 track whose frames are named on seq-ctl, so a console - aiortc's or a browser - meets it unchanged.

In one sentence: a console's offer → a pipeline of its own: webrtcbin and, for each video track the offer asks for, an
appsrc → the H.264 encoder this machine chose (ENCODERS: a board's own where GStreamer has it, x264 else) → RTP → its
answer, its candidates gathered, said back through the pairing server → the console opens the channels, each wired as it
comes → each step, frame and reply handed to one sending thread, each message in pieces and paced as aiortc's are.
WHY: a robot's board encodes H.264 in hardware - a Jetson (nvv4l2h264enc), a Raspberry Pi 4 (v4l2h264enc), a Rockchip
(mpph264enc), Intel or AMD graphics (vah264enc), a Mac (vtenc_h264_hw) - and GStreamer reaches each where PyAV's wheels
carry none of the boards' encoders; every core the encoder spares is the robot's control loop's.




Where it differs from aiortc's:
  * its bitrate: aiortc's follows the console's estimate (REMB, which needs the sender's abs-send-time, an extension
    GStreamer has no element for); this follows the loss the console's receiver reports (_LossRate), within each
    track's cap (teleop_video.bitrate_cap)

  * its playout-delay (min 0, max 0: a browser shows each frame at once, teleop_video.install_playout_delay's) is
    written into each packet by a probe on a copy of it, GStreamer having no element for that extension - where the
    console offered it (a browser does; aiortc's console does not)

  * the same: a console's NACKs, and a PLI answered with a keyframe (rtpsession's force-key-unit to the encoder)
"""
from __future__ import annotations

import asyncio
import itertools
import logging
import os
import statistics
import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Optional
from urllib.parse import quote

from sequence_ai.errors import MissingPackage
from sequence_ai._core import msgpack_io as _msgpack
from sequence_ai._core import teleop_direct as _td

_log = logging.getLogger("sequence_ai.teleop")


STUN: Optional[tuple] = _td.STUN

_GST = (1, 20)




_INSTALL = ("GStreamer 1.20 or later with webrtcbin, libnice's elements and PyGObject - on Debian or Ubuntu: apt install "
            "python3-gi gir1.2-gst-plugins-bad-1.0 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-nice; "
            "on a Mac: brew install gstreamer libnice-gstreamer pygobject3, and in a virtualenv PyGObject and "
            "DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib")

_NEEDED = ("webrtcbin", "nicesrc", "nicesink", "dtlssrtpenc", "sctpenc", "appsrc", "videoconvert", "h264parse",
           "rtph264pay", "appsink")


_GATHER_S = 5.0

_PROMISE_S = 10.0

_RATE_EVERY_S = 1.0

_GI: dict = {}
_MAIN: Optional[Any] = None
_MAIN_LOCK = threading.Lock()


def require() -> None:
    """GStreamer here, with what a connection is made of: MissingPackage saying what to install, else nothing. The
    bindings imported once, GStreamer initialised and its main loop started."""
    global _MAIN
    with _MAIN_LOCK:
        if _GI:
            return
        try:
            import gi

            gi.require_version("Gst", "1.0")
            gi.require_version("GstWebRTC", "1.0")
            gi.require_version("GstSdp", "1.0")
            gi.require_version("GstRtp", "1.0")
            from gi.repository import GLib, Gst, GstRtp, GstSdp, GstWebRTC
        except (ImportError, ValueError) as exc:
            raise MissingPackage(f"the teleop transport \"gstreamer\" needs GStreamer and its Python bindings ({exc})",
                                 hint=_INSTALL) from exc
        Gst.init(None)
        if Gst.version()[:2] < _GST:
            raise MissingPackage(f"the teleop transport \"gstreamer\" needs GStreamer {_GST[0]}.{_GST[1]} or later, and "
                                 f"this is {Gst.version_string()}", hint=_INSTALL)
        missing = [name for name in _NEEDED if Gst.ElementFactory.find(name) is None]
        if missing:
            raise MissingPackage(f"the teleop transport \"gstreamer\" needs GStreamer's {', '.join(missing)}",
                                 hint=_INSTALL)
        _GI.update(Gst=Gst, GstWebRTC=GstWebRTC, GstSdp=GstSdp, GstRtp=GstRtp, GLib=GLib)

        _MAIN = GLib.MainLoop()
        threading.Thread(target=_MAIN.run, daemon=True, name="seq-teleop-gst-main").start()




@dataclass(frozen=True)
class Encoder:
    """An H.264 encoder as this transport runs it: its GStreamer element; the elements between the robot's RGB frames and
    it (`before`, gst-launch's words); its properties for low latency - no B-frames, a keyframe when a console asks (a
    PLI) and not on a timer; its bitrate as properties (`rate`, from bits a second and the frames a second); the caps its
    stream is held to (`after`); whether it is a chip's (`hardware`), preferred where it is about as fast; and whether it
    is a last resort (`fallback`), measured only where no other answers."""
    element: str
    before: str
    props: tuple
    rate: Callable[[int, int], tuple]
    after: str = ""
    hardware: bool = True
    fallback: bool = False


def _kbps(bps: int) -> str:
    return str(max(1, bps // 1000))





_CONVERT = "videoconvert n-threads=4"



ENCODERS = (




    Encoder("nvv4l2h264enc",
            f"{_CONVERT} ! video/x-raw,format=RGBA ! nvvidconv ! video/x-raw(memory:NVMM),format=NV12",
            (("maxperf-enable", "true"), ("preset-level", "1"), ("control-rate", "1"), ("profile", "0"),
             ("num-B-Frames", "0"), ("insert-sps-pps", "true"), ("iframeinterval", "2147483647"),
             ("idrinterval", "2147483647")),
            lambda bps, fps: (("bitrate", str(bps)),)),



    Encoder("v4l2h264enc", f"{_CONVERT} ! video/x-raw,format=I420", (),
            lambda bps, fps: (("extra-controls", f"encode,video_bitrate={bps},video_bitrate_mode=1,"
                                                 f"h264_i_frame_period=2147483647,repeat_sequence_header=1,"
                                                 f"h264_profile=1"),),
            after="video/x-h264,level=(string)4"),


    Encoder("mpph264enc", f"{_CONVERT} ! video/x-raw,format=NV12",
            (("rc-mode", "cbr"), ("gop", "-1"), ("header-mode", "each-idr"), ("profile", "66")),
            lambda bps, fps: (("bps", str(bps)),)),


    Encoder("vah264enc", f"{_CONVERT} ! video/x-raw,format=NV12",
            (("rate-control", "cbr"), ("target-usage", "7"), ("b-frames", "0"), ("key-int-max", "1024")),
            lambda bps, fps: (("bitrate", _kbps(bps)),)),





    Encoder("vtenc_h264_hw", f"{_CONVERT} ! video/x-raw,format=NV12",
            (("realtime", "true"), ("allow-frame-reordering", "false"), ("rate-control", "cbr"),
             ("max-keyframe-interval", "2147483647")),
            lambda bps, fps: (("bitrate", _kbps(bps)),)),



    Encoder("x264enc", f"{_CONVERT} ! video/x-raw,format=I420",
            (("tune", "zerolatency"), ("speed-preset", "ultrafast"), ("bframes", "0"), ("key-int-max", "2147483647")),
            lambda bps, fps: (("bitrate", _kbps(bps)), ("vbv-buf-capacity", str(max(1, round(1000 / max(1, fps)))))),
            after="video/x-h264,profile=constrained-baseline", hardware=False),




    Encoder("openh264enc", f"{_CONVERT} ! video/x-raw,format=I420",
            (("usage-type", "camera"), ("complexity", "low"), ("rate-control", "bitrate"), ("gop-size", "2147483647")),
            lambda bps, fps: (("bitrate", str(bps)),), hardware=False, fallback=True),
)
_BY_NAME = {e.element: e for e in ENCODERS}

_MEASURE_FRAMES = 8



_WARM_OUT = 2
_PREFER_HARDWARE_MS = 1.0
_MEASURE_S = 3.0
_CHOICE: dict = {}
_CHOICE_LOCK = threading.Lock()


def _await(webrtc: Any, signal: str, arg: Any, timeout_s: float = _PROMISE_S) -> Any:
    """webrtcbin's action `signal` with `arg` and a promise, the promise waited for `timeout_s`: its reply (None where it
    replied with none); RuntimeError where it did not answer in time or answered with an error."""
    Gst = _GI["Gst"]
    done = threading.Event()
    promise = Gst.Promise.new_with_change_func(lambda _p: done.set())
    webrtc.emit(signal, arg, promise)
    if not done.wait(timeout_s):
        promise.interrupt()
        raise RuntimeError(f"webrtcbin did not answer {signal} within {timeout_s:.0f} s")
    if promise.wait() != Gst.PromiseResult.REPLIED:
        raise RuntimeError(f"webrtcbin did not answer {signal}")
    reply = promise.get_reply()
    if reply is not None and reply.has_field("error"):
        raise RuntimeError(f"{signal}: {reply.get_value('error')}")
    return reply


def _set(element: Any, props: tuple) -> None:
    """Each of `props` that `element` has, from its words as gst-launch says them; one it lacks is said at debug."""
    Gst = _GI["Gst"]
    for name, value in props:
        if element.find_property(name) is None:
            _log.debug("teleop_gst: %s has no property %s", element.get_factory().get_name(), name)
            continue
        Gst.util_set_object_arg(element, name, value)


def _present() -> list:
    """The encoders this GStreamer has, in ENCODERS' order."""
    Gst = _GI["Gst"]
    return [e for e in ENCODERS if Gst.ElementFactory.find(e.element) is not None]


def _measure(encoder: Encoder, width: int, height: int, rate: int) -> Optional[float]:
    """Milliseconds from a frame handed to `encoder` to its H.264 out, the median of _MEASURE_FRAMES handed at `rate`,
    as a robot hands its camera's, once it answers at all: frames are handed until _WARM_OUT came out, untimed, then the
    timed ones; None where it does not answer within _MEASURE_S (an element present with no chip under it)."""
    Gst = _GI["Gst"]
    after = f" ! {encoder.after}" if encoder.after else ""
    try:
        pipe = Gst.parse_launch(
            f"appsrc name=src is-live=true format=time caps=video/x-raw,format=RGB,width={width},height={height},"
            f"framerate={rate}/1 ! {encoder.before} ! {encoder.element} name=enc{after} ! "
            f"appsink name=out sync=false emit-signals=true max-buffers=64")
    except Exception as exc:
        _log.debug("teleop_gst: %s does not open: %s", encoder.element, exc)
        return None
    _set(pipe.get_by_name("enc"), encoder.props + encoder.rate(1_000_000, rate))
    handed: dict = {}
    took: list = []
    seen = {"out": 0, "timed_from": None}
    done = threading.Event()

    def sample(sink: Any) -> Any:
        got = sink.emit("pull-sample")
        if got is None:
            return Gst.FlowReturn.OK
        seen["out"] += 1




        at = handed.pop(got.get_segment().to_running_time(Gst.Format.TIME, got.get_buffer().pts), None)
        if at is not None and seen["timed_from"] is not None and at[0] >= seen["timed_from"]:
            took.append((time.perf_counter() - at[1]) * 1000.0)
            if len(took) >= _MEASURE_FRAMES - 1:
                done.set()
        return Gst.FlowReturn.OK

    pipe.get_by_name("out").connect("new-sample", sample)
    src = pipe.get_by_name("src")
    frame = bytes(width * height * 3)

    def hand(i: int) -> None:
        buf = Gst.Buffer.new_wrapped(frame)
        buf.pts = buf.dts = i * Gst.SECOND // rate
        buf.duration = Gst.SECOND // rate
        handed[buf.pts] = (i, time.perf_counter())
        src.emit("push-buffer", buf)
        time.sleep(1.0 / rate)

    try:
        if pipe.set_state(Gst.State.PLAYING) == Gst.StateChangeReturn.FAILURE:
            return None
        start, i = time.perf_counter(), 0
        while seen["out"] < _WARM_OUT:
            if time.perf_counter() - start > _MEASURE_S:
                return None
            hand(i)
            i += 1
        seen["timed_from"] = i
        for _ in range(_MEASURE_FRAMES):
            hand(i)
            i += 1
        done.wait(_MEASURE_S)
    finally:
        pipe.set_state(Gst.State.NULL)

    return statistics.median(took) if len(took) >= _MEASURE_FRAMES // 2 else None


def chosen(width: int = 640, height: int = 480, rate: int = 30) -> Encoder:
    """The encoder this process sends with, decided once - at its first console, before that console's frames say their
    size, so at 640x480: SEQ_TELEOP_ENCODER's where it names one of ENCODERS that opens here; else each this GStreamer
    has, measured (_measure), the fastest kept, a chip's within _PREFER_HARDWARE_MS of it preferred (it spares the CPU),
    x264 where none answers - teleop_video.chosen's rule, over GStreamer's elements."""
    with _CHOICE_LOCK:
        if _CHOICE:
            return _CHOICE["encoder"]
        asked = os.environ.get("SEQ_TELEOP_ENCODER", "auto").strip() or "auto"
        tried: dict = {}
        if asked in _BY_NAME:
            took = _measure(_BY_NAME[asked], width, height, rate)
            if took is not None:
                _CHOICE.update(encoder=_BY_NAME[asked], tried_ms={asked: round(took, 2)}, asked=asked)
                _log.info("teleop_gst: %s, as SEQ_TELEOP_ENCODER says (%.1f ms a frame)", asked, took)
                return _BY_NAME[asked]
            _log.warning("teleop_gst: SEQ_TELEOP_ENCODER=%s does not open here; measuring the encoders this machine "
                         "has", asked)
        present = _present()
        for last in (False, True):
            if last and tried:
                break
            for encoder in present:
                if encoder.fallback != last or encoder.element == asked:
                    continue
                took = _measure(encoder, width, height, rate)
                if took is not None:
                    tried[encoder.element] = took
        best = _BY_NAME["x264enc"]
        if tried:
            fastest = min(tried.values())
            near = [e for e in ENCODERS if e.element in tried and e.hardware
                    and tried[e.element] <= fastest + _PREFER_HARDWARE_MS]
            best = near[0] if near else _BY_NAME[min(tried, key=tried.get)]
        _CHOICE.update(encoder=best, tried_ms={k: round(v, 2) for k, v in tried.items()}, asked=asked)
        _log.info("teleop_gst: sending with %s (%s)", best.element,
                  ", ".join(f"{k} {v:.1f} ms" for k, v in tried.items()) or "none answered")
        return best


def encoder_report() -> dict:
    """The encoder this process chose, for teleop_metrics(): {"name", "tried_ms", "asked"} - teleop_video's shape;
    {} before a console's first connection chose one."""
    if not _CHOICE:
        return {}
    return {"name": _CHOICE["encoder"].element, "tried_ms": dict(_CHOICE["tried_ms"]), "asked": _CHOICE["asked"]}




def h264_types(sdp: str) -> list:
    """The H.264 payload type each video m-line of an offer is answered with: packetization-mode 1 and a Baseline
    profile first (what every encoder here sends), then packetization-mode 1, then any H.264; None for a line with no
    H.264 (aiortc's console offers 42001f and 42e01f, a browser a dozen)."""
    types: list = []
    rtpmap: dict = {}
    fmtp: dict = {}
    video = False
    for line in sdp.splitlines() + ["m=end"]:
        if line.startswith("m="):
            if video:
                types.append(_pick(rtpmap, fmtp))
            video, rtpmap, fmtp = line.startswith("m=video "), {}, {}
        elif video and line.startswith("a=rtpmap:"):
            pt, _, codec = line[len("a=rtpmap:"):].partition(" ")
            rtpmap[pt] = codec.split("/")[0].upper()
        elif video and line.startswith("a=fmtp:"):
            pt, _, params = line[len("a=fmtp:"):].partition(" ")
            fmtp[pt] = dict(p.strip().partition("=")[::2] for p in params.split(";") if "=" in p)
    return types


def _pick(rtpmap: dict, fmtp: dict) -> Optional[int]:
    """One m-line's H.264 payload type, by h264_types' order."""
    h264 = [pt for pt, codec in rtpmap.items() if codec == "H264"]

    def mode1(pt: str) -> bool:
        return fmtp.get(pt, {}).get("packetization-mode") == "1"

    def baseline(pt: str) -> bool:
        return fmtp.get(pt, {}).get("profile-level-id", "")[:2].lower() == "42"

    for keep in (lambda pt: mode1(pt) and baseline(pt), mode1, lambda pt: True):
        for pt in h264:
            if keep(pt):
                return int(pt)
    return None


def playout_delay_ids(sdp: str) -> list:
    """The id each video m-line of an offer gives the playout-delay extension (teleop_video.PLAYOUT_DELAY_URI), None for
    a line that offers none."""
    from sequence_ai._core import teleop_video as _video

    ids: list = []
    for section in sdp.replace("\r\n", "\n").split("\nm=")[1:]:
        if not section.startswith("video "):
            continue
        found = None
        for line in section.split("\n"):
            if line.startswith("a=extmap:") and line.split()[-1] == _video.PLAYOUT_DELAY_URI:
                found = int(line[len("a=extmap:"):].split()[0].split("/")[0])
        ids.append(found)
    return ids


def with_playout_delay(sdp: str, ids: list) -> str:
    """An answer with the playout-delay extension accepted on each video m-line its offer gave it an id on (`ids`, by
    playout_delay_ids): its a=extmap line after the line's a=mid, as webrtcbin's own would stand."""
    from sequence_ai._core import teleop_video as _video

    out: list = []
    video, current = -1, False
    lines = sdp.replace("\r\n", "\n").rstrip("\n").split("\n")
    for line in lines:
        out.append(line)
        if line.startswith("m="):
            video = video + 1 if line.startswith("m=video ") else video
            current = line.startswith("m=video ")
        elif line.startswith("a=mid:") and current and video < len(ids) and ids[video] is not None:
            out.append(f"a=extmap:{ids[video]} {_video.PLAYOUT_DELAY_URI}")
    return "\r\n".join(out) + "\r\n"


def _show_at_once(ext_id: int) -> Callable:
    """A probe for a payloader's source pad that writes the playout-delay extension (min 0, max 0) as `ext_id` into
    each RTP packet: on a copy - the probe's own is shared, and a write to it is refused - handed to the next element
    in its place, a list's packets alike (rtph264pay sends a frame's fragments as one).
"""
    from sequence_ai._core import teleop_video as _video

    Gst, GstRtp = _GI["Gst"], _GI["GstRtp"]
    flags = Gst.MapFlags.READ | Gst.MapFlags.WRITE

    def marked(buf: Any) -> Any:
        new = buf.copy_deep()
        ok, rtp = GstRtp.RTPBuffer.map(new, flags)
        if ok:
            rtp.add_extension_onebyte_header(ext_id, _video._SHOW_AT_ONCE)
            rtp.unmap()
        return new

    def probe(pad: Any, info: Any) -> Any:
        peer = pad.get_peer()
        if peer is None:
            return Gst.PadProbeReturn.OK
        if info.type & Gst.PadProbeType.BUFFER:
            peer.chain(marked(info.get_buffer()))
        else:
            got = info.get_buffer_list()
            out = Gst.BufferList.new_sized(got.length())
            for i in range(got.length()):
                out.insert(-1, marked(got.get(i)))
            peer.chain_list(out)
        return Gst.PadProbeReturn.DROP

    return probe


def turn_urls(ice_servers: Any) -> list:
    """The TURN servers its pairing server handed with an offer ({"urls", "username", "credential"}, as aiortc's take
    them) as webrtcbin's add-turn-server takes them: turn(s)://user:password@host:port[?transport=], user and password
    escaped - a time-limited user's "timestamp:name" has a colon.
"""
    out = []
    for server in ice_servers or ():
        if not isinstance(server, dict) or not server.get("urls"):
            continue
        urls = server["urls"] if isinstance(server["urls"], (list, tuple)) else [server["urls"]]
        user = quote(str(server.get("username") or ""), safe="")
        password = quote(str(server.get("credential") or ""), safe="")
        for url in urls:
            scheme, _, rest = str(url).partition(":")
            if scheme not in ("turn", "turns") or not rest:
                continue
            out.append(f"{scheme}://{user}:{password}@{rest.lstrip('/')}")
    return out


def with_candidates(sdp: str, candidates: list) -> str:
    """`sdp` with each of `candidates` (its "candidate:..." lines, as on-ice-candidate gave them) it lacks, after the
    first media section's own: all of a bundle's are that section's. webrtcbin's description holds those gathered by the
    time it was read; one gathered later is added here."""
    lines = sdp.replace("\r\n", "\n").rstrip("\n").split("\n")
    have = {line[2:] for line in lines if line.startswith("a=candidate:")}

    new = [f"a={c}" for c in candidates if c and c.startswith("candidate:") and c not in have]
    if not new:
        return "\r\n".join(lines) + "\r\n"
    first = next((i for i, line in enumerate(lines) if line.startswith("m=")), None)
    if first is None:
        return "\r\n".join(lines + new) + "\r\n"
    end = next((i for i in range(first + 1, len(lines)) if lines[i].startswith("m=")), len(lines))
    return "\r\n".join(lines[:end] + new + lines[end:]) + "\r\n"


def rtp_of(seq: int, rate: int) -> int:
    """Frame `seq`'s RTP timestamp at `rate` frames a second: aiortc's FrameTrack's (convert_timebase of pts `seq` in
    1/rate to 1/90000, floored), so either robot's frames read alike."""
    return (seq * 90000 // rate) & 0xFFFFFFFF


def pts_of(seq: int, rate: int) -> int:
    """The buffer time (ns) that rtph264pay turns into rtp_of(seq, rate) exactly: its timestamp-offset 0, it floors
    running time x 90000 / 1e9, and the ceiling here keeps that floor on the tick.
 
"""
    ticks = seq * 90000 // rate
    return -(-ticks * 1_000_000_000 // 90000)


def _ssrcs(count: int) -> list:
    """`count` SSRCs, random, different and none 0: one a track."""
    out: list = []
    while len(out) < count:
        ssrc = int.from_bytes(os.urandom(4), "big")
        if ssrc and ssrc not in out:
            out.append(ssrc)
    return out




class _LossRate:
    """A console's tracks' bitrate, as a share of each track's cap (teleop_video.bitrate_cap), moved by the loss its
    receiver reports each _RATE_EVERY_S: past 10% cut by half the loss, under 2% up 5%, between held - the loss-based half
    of Google's congestion control; it starts where aiortc's encoder does, 1 Mbps at a 640x480@30 track's 2.5.
    """

    START = 0.4
    LEAST = 0.05

    def __init__(self) -> None:
        self.share = self.START

    def heard(self, lost: Optional[float]) -> float:
        """The fraction lost since the last report (None: no report yet): the share after it."""
        if lost is None:
            return self.share
        if lost > 0.10:
            self.share = max(self.LEAST, self.share * (1 - 0.5 * lost))
        elif lost < 0.02:
            self.share = min(1.0, self.share * 1.05)
        return self.share




class _Sender:
    """One thread every send goes through - steps, frames, replies, a channel drained - so a channel's queue has one
    owner and the robot's observe() thread never waits on a connection (teleop_direct.soon's loop, for GStreamer)."""

    def __init__(self) -> None:
        self._jobs: deque = deque()
        self._have = threading.Condition()
        threading.Thread(target=self._run, daemon=True, name="seq-teleop-gst-send").start()

    def soon(self, fn: Callable, *args: Any) -> None:
        with self._have:
            self._jobs.append((fn, args))
            self._have.notify()

    def stop(self) -> None:
        """Its thread ended once what is queued before this is done: its links closed."""
        self.soon(None)

    def _run(self) -> None:
        while True:
            with self._have:
                while not self._jobs:
                    self._have.wait()
                fn, args = self._jobs.popleft()
            if fn is None:
                return
            try:
                fn(*args)
            except Exception:
                _log.debug("teleop_gst: a send failed", exc_info=True)




class _Channel:
    """One data channel's sending side, paced as teleop_direct._Channel's: messages queued whole, handed on a piece at a
    time while the connection holds less than HIGH_BYTES unsent and again as it drains below LOW_BYTES; the oldest not
    yet begun dropped past _QUEUED. Touched on the sending thread alone."""

    def __init__(self, channel: Any, sender: _Sender) -> None:
        self.channel = channel
        self.label = channel.get_property("label")
        self.most = _td._QUEUED.get(self.label, 8)
        self.queue: deque = deque()
        self.numbers = itertools.count()
        self.dropped = 0
        channel.set_property("buffered-amount-low-threshold", _td.LOW_BYTES)
        channel.connect("on-buffered-amount-low", lambda _c: sender.soon(self.pump))

    def is_open(self) -> bool:
        return self.channel.get_property("ready-state") == _GI["GstWebRTC"].WebRTCDataChannelState.OPEN

    def put(self, data: bytes) -> None:
        self.queue.append([_td.pieces(next(self.numbers), data), 0])
        begun = 1 if self.queue[0][1] > 0 else 0
        while len(self.queue) - begun > self.most:
            del self.queue[begun]
            self.dropped += 1
        self.pump()

    def pump(self) -> None:
        if not self.is_open():
            return
        GLib = _GI["GLib"]
        while self.queue and self.channel.get_property("buffered-amount") < _td.HIGH_BYTES:
            head = self.queue[0]
            try:
                self.channel.send_data_full(GLib.Bytes.new(head[0][head[1]]))
            except GLib.Error:
                return
            head[1] += 1
            if head[1] == len(head[0]):
                self.queue.popleft()


class _Track:
    """One video track to a console: its appsrc, its encoder, the camera it carries and its frames' count."""

    def __init__(self, src: Any, encoder_element: Any, kind: Encoder) -> None:
        self.src, self.element, self.kind = src, encoder_element, kind
        self.key: Optional[str] = None
        self.seq = 0
        self.size: Optional[tuple] = None
        self.cap = 0


class _Side:
    """One console's connection: its pipeline - webrtcbin and a track per camera it asked for -, its channels as the
    console opens them, their pieces put back together (each whole message to `on_message(label, data, at_us)`), and
    `on_open` / `on_gone` told once each."""

    def __init__(self, links: "RobotLinks", peer: str, tracks: list, hz: float, ice_servers: Any = None,
                 delay_ids: Optional[list] = None) -> None:
        Gst = _GI["Gst"]

        self.links, self.peer, self.relay = links, peer, bool(ice_servers)
        self.rate = max(1, int(round(hz)))
        self.kind = chosen(rate=self.rate) if tracks else None
        branches = []




        ssrcs = _ssrcs(len(tracks))
        for i, (pt, ssrc) in enumerate(zip(tracks, ssrcs)):
            kind = self.kind
            after = f" ! {kind.after}" if kind.after else ""

            branches.append(
                f"appsrc name=cam{i} is-live=true format=time do-timestamp=false max-buffers=1 leaky-type=downstream "
                f"block=false ! {kind.before} ! {kind.element} name=enc{i}{after} ! h264parse config-interval=-1 ! "
                f"rtph264pay name=pay{i} pt={pt} ssrc={ssrc} config-interval=-1 aggregate-mode=zero-latency "
                f"timestamp-offset=0 ! "
                f"application/x-rtp,media=video,encoding-name=H264,payload={pt},clock-rate=90000,ssrc=(uint){ssrc} ! w.")
        stun = f" stun-server=stun://{STUN[0]}:{STUN[1]}" if STUN else ""
        made = Gst.parse_launch(f"webrtcbin name=w bundle-policy=max-bundle{stun} " + " ".join(branches))
        if not isinstance(made, Gst.Pipeline):

            self.pipe = Gst.Pipeline.new(None)
            self.pipe.add(made)
        else:
            self.pipe = made
        self.webrtc = self.pipe.get_by_name("w")

        self.delay_ids = list(delay_ids or [])[:len(tracks)]
        for i, ext_id in enumerate(self.delay_ids):
            if ext_id is not None:
                self.pipe.get_by_name(f"pay{i}").get_static_pad("src").add_probe(
                    Gst.PadProbeType.BUFFER | Gst.PadProbeType.BUFFER_LIST, _show_at_once(ext_id))
        self.tracks = []
        for i in range(len(tracks)):
            element = self.pipe.get_by_name(f"enc{i}")
            _set(element, self.kind.props + self.kind.rate(1_000_000, self.rate))
            self.tracks.append(_Track(self.pipe.get_by_name(f"cam{i}"), element, self.kind))
        for url in turn_urls(ice_servers):
            self.webrtc.emit("add-turn-server", url)
        self.track_of: dict = {}
        self.left_out: set = set()
        self.episode: Optional[str] = None
        self.out: dict = {}
        self.assembly = {label: _td.Assembly() for label in _td.CHANNELS}
        self.opened = threading.Event()
        self.ended = threading.Event()
        self.candidates: list = []
        self.srflx_at: Optional[float] = None
        self.gathered = threading.Event()
        self.loss = _LossRate()
        self.webrtc.connect("on-data-channel", self._channel)
        self.webrtc.connect("on-ice-candidate", self._candidate)
        self.webrtc.connect("notify::ice-gathering-state", self._gathering)
        self.webrtc.connect("notify::connection-state", self._state)



    def _candidate(self, _w: Any, _mline: int, candidate: str) -> None:
        if not candidate:
            return
        self.candidates.append(candidate)
        if " typ srflx" in candidate and self.srflx_at is None:
            self.srflx_at = time.monotonic()

    def _gathering(self, *_: Any) -> None:
        if self.webrtc.get_property("ice-gathering-state") == _GI["GstWebRTC"].WebRTCICEGatheringState.COMPLETE:
            self.gathered.set()

    def _state(self, *_: Any) -> None:
        State = _GI["GstWebRTC"].WebRTCPeerConnectionState
        if self.webrtc.get_property("connection-state") in (State.FAILED, State.CLOSED):
            self.links.gone(self)

    def _channel(self, _w: Any, channel: Any) -> None:
        """One of CHANNELS, as the console opened it: its sending side and its pieces in."""
        label = channel.get_property("label")
        if label not in _td.CHANNELS:
            return
        sender = self.links.sender
        assembly = self.assembly[label]

        def message(_c: Any, data: Any) -> None:
            whole = assembly.add(bytes(data.get_data())) if data is not None else None
            if whole is not None:

                self.links.heard(self.peer, label, whole, time.time_ns() // 1000)

        channel.connect("on-message-data", message)
        channel.connect("on-open", lambda _c: sender.soon(self._opened))
        channel.connect("on-close", lambda _c: self.links.gone(self))
        sender.soon(self._wire, label, channel)



    def _wire(self, label: str, channel: Any) -> None:
        self.out[label] = _Channel(channel, self.links.sender)
        self._opened()

    def _opened(self) -> None:
        if len(self.out) == len(_td.CHANNELS) and all(c.is_open() for c in self.out.values()):
            for c in self.out.values():
                c.pump()
            if not self.opened.is_set() and not self.ended.is_set():
                self.opened.set()
                self.links.opened(self)

    def send(self, label: str, data: bytes) -> bool:
        channel = self.out.get(label)
        if channel is None or not channel.is_open():
            return False
        channel.put(data)
        return True

    def frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        """A step's camera frames to its tracks: each camera a track, in the order they first came, its frame named on
        seq-ctl before it is handed to the encoder (aiortc's order); those past its tracks go to no one, said once each."""
        self.episode = episode
        new_left = []
        for key, frame in raw.items():
            track = self.track_of.get(key)
            if track is None:
                if len(self.track_of) >= len(self.tracks):
                    if key not in self.left_out:
                        new_left.append(key)
                    continue
                track = self.track_of[key] = self.tracks[len(self.track_of)]
                track.key = key
            self._push(track, frame, n, t_us)
        if new_left:
            self.left_out.update(new_left)
            _log.warning("a console takes %d cameras of this robot's: %s not sent to it", len(self.tracks),
                         ", ".join(sorted(self.left_out)))

    def _push(self, track: _Track, frame: Any, n: int, t_us: int) -> None:
        import numpy as np

        Gst = _GI["Gst"]
        arr = np.ascontiguousarray(frame, dtype=np.uint8)
        if arr.ndim != 3 or arr.shape[2] != 3:
            return
        height, width = arr.shape[:2]
        if (width * 3) % 4:

            arr = np.pad(arr.reshape(height, width * 3), ((0, 0), (0, 4 - (width * 3) % 4)))
        if track.size != (width, height):

            track.size = (width, height)
            track.src.set_property("caps", Gst.Caps.from_string(
                f"video/x-raw,format=RGB,width={width},height={height},framerate={self.rate}/1"))
            from sequence_ai._core import teleop_video as _video

            track.cap = _video.bitrate_cap(width, height, self.rate)
            self._bitrate(track)
        track.seq += 1
        self.send("seq-ctl", _msgpack.pack({"t": "vm", "i": self.tracks.index(track), "key": track.key,
                                            "e": self.episode, "seq": track.seq, "n": int(n),
                                            "capture_us": int(t_us), "rtp": rtp_of(track.seq, self.rate)}))
        buf = Gst.Buffer.new_wrapped(arr.tobytes())
        buf.pts = buf.dts = pts_of(track.seq, self.rate)
        buf.duration = Gst.SECOND // self.rate
        track.src.emit("push-buffer", buf)

    def _bitrate(self, track: _Track) -> None:
        """A track's bitrate: its share (_LossRate) of its cap, no less than teleop_video's least."""
        if not track.cap:
            return
        from sequence_ai._core import teleop_video as _video

        bps = max(_video._DEFAULT_MIN_BITRATE, int(track.cap * self.loss.share))
        _set(track.element, track.kind.rate(bps, self.rate))

    def stats(self) -> dict:
        """webrtcbin's stats now, by their id: {id: GstStructure} - {} where it did not answer."""
        try:
            reply = _await(self.webrtc, "get-stats", None, timeout_s=2.0)
        except RuntimeError:
            return {}
        if reply is None:
            return {}
        out = {}
        for i in range(reply.n_fields()):
            name = reply.nth_field_name(i)
            value = reply.get_value(name)
            if hasattr(value, "get_value"):
                out[name] = value
        return out

    def lost(self) -> Optional[float]:
        """The most of its tracks' fraction lost the console's receiver last reported (RTCP's receiver reports); None
        before any report."""
        StatsType = _GI["GstWebRTC"].WebRTCStatsType
        worst = None
        for s in self.stats().values():
            if s.get_value("type") != StatsType.REMOTE_INBOUND_RTP:
                continue
            ok, lost = s.get_double("fraction-lost")
            if ok:
                worst = lost if worst is None else max(worst, lost)
        return worst

    def path(self) -> str:
        """"relay" where the pair its ICE chose has a TURN server's candidate on either end, else "direct" - from its
        stats' candidate pair, where it may relay at all."""
        if not self.relay:
            return "direct"
        StatsType = _GI["GstWebRTC"].WebRTCStatsType
        stats = self.stats()
        for s in stats.values():
            if s.get_value("type") != StatsType.CANDIDATE_PAIR:
                continue
            for end in ("local-candidate-id", "remote-candidate-id"):
                candidate = stats.get(s.get_string(end) or "")
                if candidate is not None and str(candidate.get_value("candidate-type")).lower().endswith("relay"):
                    return "relay"
        return "direct"

    def close(self) -> None:
        self.ended.set()
        self.pipe.set_state(_GI["Gst"].State.NULL)




class RobotLinks:
    """A robot's connections through GStreamer, one per console that asked (teleop_transport.RobotTransport): answer()
    each offer - its answer said back through `say(peer, message)` -, step() each step to every console open, frames()
    its cameras to those that take video, reply() to one; what a console sends goes to `on_message(peer, label, data,
    at_us)` on webrtcbin's thread, and `on_peer(peer, "open" | "gone")` as one connects or leaves."""

    def __init__(self, on_message: Callable, say: Callable, on_peer: Optional[Callable] = None) -> None:
        require()
        self._on_message, self._say, self._on_peer = on_message, say, on_peer
        self._sides: dict = {}
        self._lock = threading.Lock()
        self.sender = _Sender()
        self._closed = threading.Event()
        threading.Thread(target=self._rates, daemon=True, name="seq-teleop-gst-rate").start()

    @property
    def peers(self) -> int:
        with self._lock:
            return sum(1 for s in self._sides.values() if s.opened.is_set() and not s.ended.is_set())

    @property
    def tracks(self) -> int:
        with self._lock:
            return sum(1 for s in self._sides.values() if s.tracks and s.opened.is_set() and not s.ended.is_set())

    def answer(self, peer: str, sdp: str, hz: float = 30.0, ice_servers: Any = None) -> None:
        """A console's offer, answered on a thread of its own - {"t": "rtc", "sdp", "nat"} said back, or {"t": "rtc",
        "error"} - never waited for here."""
        if not isinstance(peer, str) or not isinstance(sdp, str):
            return
        threading.Thread(target=self._answer, args=(peer, sdp, hz, ice_servers), daemon=True,
                         name="seq-teleop-gst-answer").start()

    def _answer(self, peer: str, sdp: str, hz: float, ice_servers: Any) -> None:
        Gst, GstSdp, GstWebRTC = _GI["Gst"], _GI["GstSdp"], _GI["GstWebRTC"]
        side = None
        try:
            with self._lock:
                old = self._sides.pop(peer, None)
                if len(self._sides) >= _td.MOST_PEERS:
                    raise RuntimeError(_td.no_place())
            if old is not None:
                old.close()

            probing = asyncio.run_coroutine_threadsafe(_td.nat_probe(), _td.loop())
            relay = bool(ice_servers)
            offer = _td.kept_candidates(sdp, relay=relay)
            types = h264_types(offer)[:_td.MOST_TRACKS]
            if any(pt is None for pt in types):
                raise RuntimeError("the console's offer has a video track with no H.264, the one codec sent here")
            side = _Side(self, peer, types, hz, ice_servers if relay else None, playout_delay_ids(offer))
            with self._lock:
                self._sides[peer] = side
            if side.pipe.set_state(Gst.State.PLAYING) == Gst.StateChangeReturn.FAILURE:
                raise RuntimeError("its GStreamer pipeline did not start")
            ok, message = GstSdp.SDPMessage.new_from_text(offer)
            if ok != GstSdp.SDPResult.OK:
                raise RuntimeError("the console's offer does not read as SDP")
            _await(side.webrtc, "set-remote-description",
                   GstWebRTC.WebRTCSessionDescription.new(GstWebRTC.WebRTCSDPType.OFFER, message))
            reply = _await(side.webrtc, "create-answer", None)
            answer = reply.get_value("answer") if reply is not None else None
            if answer is None:
                raise RuntimeError("webrtcbin made no answer to the console's offer")
            _await(side.webrtc, "set-local-description", answer)
            self._gather(side)
            local = side.webrtc.get_property("local-description").sdp.as_text()
            local = with_playout_delay(with_candidates(local, side.candidates), side.delay_ids)
            local = _td.kept_candidates(local, relay=relay)
            try:
                nat = probing.result(timeout=5.0)
            except Exception:
                nat = {"kind": "unknown", "public": None}
            self._say(peer, {"t": "rtc", "sdp": local, "nat": nat})

            timer = threading.Timer(_td.OPEN_S, self._unopened, args=(side,))
            timer.daemon = True
            timer.start()
        except Exception as exc:
            _log.warning("a console's direct connection was not answered: %s", exc)
            with self._lock:
                if side is not None and self._sides.get(peer) is side:
                    del self._sides[peer]
            if side is not None:
                side.close()
            self._say(peer, {"t": "rtc", "error": f"{type(exc).__name__}: {exc}"[:300]})

    def _unopened(self, side: _Side) -> None:
        """A side not open OPEN_S after its answer given up (gone): a console behind a firewall closes a connection this
        robot never hears close, and its place would be held as long as the ICE checks go on."""
        if not side.opened.is_set():
            self.gone(side)

    @staticmethod
    def _gather(side: _Side) -> None:
        """Its candidates gathered: every interface's, or - once a server-reflexive one came - those that came within
        teleop_direct.GATHER_GRACE_S of it (an interface whose STUN never answers is not waited for), or _GATHER_S's."""
        end = time.monotonic() + _GATHER_S
        while not side.gathered.wait(0.02):
            now = time.monotonic()
            if now >= end or (side.srflx_at is not None and now - side.srflx_at >= _td.GATHER_GRACE_S):
                return



    def heard(self, peer: str, label: str, data: bytes, at_us: int) -> None:
        self._on_message(peer, label, data, at_us)

    def opened(self, side: _Side) -> None:
        with self._lock:
            current = self._sides.get(side.peer) is side
        if current and self._on_peer is not None:
            self._on_peer(side.peer, "open")

    def gone(self, side: _Side) -> None:
        """A console's connection failed or closed - its channels, or its ICE: its place given up, its pipeline stopped
        on the sending thread (not webrtcbin's own, which stopping it would wait on), the robot told once."""
        with self._lock:
            current = self._sides.get(side.peer) is side
            if current:
                del self._sides[side.peer]
        if side.ended.is_set():
            return
        side.ended.set()
        self.sender.soon(side.close)
        if current and side.opened.is_set() and self._on_peer is not None:
            self._on_peer(side.peer, "gone")



    def path(self, peer: str) -> str:
        with self._lock:
            side = self._sides.get(peer)
        return side.path() if side is not None else "direct"

    def _open_sides(self, *, video: bool = False) -> list:
        with self._lock:
            return [s for s in self._sides.values() if s.opened.is_set() and not s.ended.is_set()
                    and (s.tracks or not video)]

    def step(self, data: dict) -> None:
        """One step to every console open: its arrays on seq-state, the rest on seq-video (teleop_direct's)."""
        self.sender.soon(self._fan, data)

    def _fan(self, data: dict) -> None:
        for side in self._open_sides():
            if data.get("state") is not None:
                side.send("seq-state", data["state"])
            if data.get("rest") is not None:
                side.send("seq-video", data["rest"])

    def frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        self.sender.soon(self._fan_frames, episode, raw, n, t_us)

    def _fan_frames(self, episode: str, raw: dict, n: int, t_us: int) -> None:
        for side in self._open_sides(video=True):
            side.frames(episode, raw, n, t_us)

    def reply(self, peer: str, message: dict, *, label: str = "seq-ctl") -> bool:
        with self._lock:
            side = self._sides.get(peer)
        if side is None or not side.opened.is_set() or side.ended.is_set():
            return False
        self.sender.soon(side.send, label, _msgpack.pack(message))
        return True

    def tell_all(self, message: dict) -> None:
        for side in self._open_sides():
            self.reply(side.peer, message, label="seq-who")

    def connected(self) -> list:
        return [s.peer for s in self._open_sides()]

    def encoder_report(self) -> dict:
        """The encoder its video is sent with (encoder_report): teleop_metrics()'s "encoder"."""
        return encoder_report()

    def _rates(self) -> None:
        """Each _RATE_EVERY_S: each console's loss read and its tracks' bitrate moved by it (_LossRate)."""
        while not self._closed.wait(_RATE_EVERY_S):
            for side in self._open_sides(video=True):
                try:
                    side.loss.heard(side.lost())
                except Exception:
                    continue
                for track in side.tracks:
                    self.sender.soon(side._bitrate, track)

    def close(self) -> None:
        self._closed.set()
        with self._lock:
            sides, self._sides = list(self._sides.values()), {}
        for side in sides:
            try:
                side.close()
            except Exception:
                pass
        self.sender.stop()
