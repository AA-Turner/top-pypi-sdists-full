"""The WebRTC video path for direct-connect teleop (operator <-> robot, aiortc): encode low-latency H264 with a bitrate
cap you can lift, on the receive side keep only the freshest frame, and release each frame on its RTP marker instead of a
frame late.

libx264 on every machine, and each hardware encoder PyAV's wheels carry where this machine has it, measured against it
once a process at the robot's frame size and rate: the fastest sends (chosen, HARDWARE). The machines are not any one
kind - not always a Mac, not always a box with an NVIDIA card - so the choice is measured, never assumed. On an Apple
chip libx264 wins: VideoToolbox through PyAV answers a frame only at a later call, 34 to 70 ms against libx264's 0.9 to
2.0.


Why this file exists -- aiortc 1.16 ships one H264 path and it is limiting for teleop (verified in source):
  * codecs/h264.py clamps the bitrate to 0.5-3 Mbps (MIN_BITRATE/MAX_BITRATE), so anything above 3 Mbps is unreachable,
    and re-creates the codec on any >10% bitrate change (h264.py:246), each rebuild a keyframe spike;
  * rtcrtpreceiver.py feeds decoded frames through an unbounded `asyncio.Queue()`, so a slow consumer lags further and
    further behind;
  * the jitterbuffer releases a frame only when the NEXT frame's first packet arrives (jitterbuffer.py:77, a timestamp
    change) and never reads the RTP marker the sender sets (rtcrtpsender.py:385) -- ~one frame interval (~33 ms at
    30 fps) of pure latency on every frame.
This module addresses all three without forking aiortc: a drop-in libx264 encoder with a configurable [min, max] bitrate,
a receive-side track that drains to the newest frame, and a marker-release patch for the jitterbuffer. Low-latency
libx264 params match aiortc's: zerolatency, Baseline (no B-frames), keyframe on demand.

Two more on the robot's side, so the operator's Chrome shows each frame sooner and the picture does not stop every few
seconds:
  * the encoder sends a keyframe only when the console asks (a PLI: a new console, a loss) or its frames' size or rate
    changes - never every 250 frames on its own, x264's default - and its VBV, on from the start, holds each frame to
    about one frame's share of the bitrate, which it changes in place, with no new codec and no keyframe for it;
  * its video carries RTP's playout-delay extension at 0 and 0, so Chrome shows each frame as soon as it is decoded,
    not after the wait its jitter estimate adds (install_playout_delay).

Robots differ only by parameters here (bitrate, resolution come from config) -- there is no per-robot code.

New dependencies (aiortc, av) live in the `teleop` extra, imported lazily; without them these calls raise MissingPackage.
Interface owned here; wired into the connection by sequence_ai/_core/teleop.py and teleop_robot.py.
"""
from __future__ import annotations

import logging
import os
import statistics
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from sequence_ai.errors import MissingPackage

_log = logging.getLogger("sequence_ai.teleop_video")

ENCODER = "libx264"






_LIBX264_OPTS = {"level": "31", "tune": "zerolatency", "preset": "ultrafast"}
_LIBX264_PROFILE = "Baseline"

_DEFAULT_MIN_BITRATE = 500_000









_CAP_AT_VGA30 = 2_500_000
_CAP_PIXEL_POWER = 0.75
_MOST_BITRATE = 8_000_000

_RATE_UNSAID = 30
_MOST_RATE = 240







_GOP_FRAMES = 1 << 30




_VBV_FRAMES = 1


def _av():
    try:
        import av
        return av
    except ImportError as exc:
        raise MissingPackage("av", extra="teleop") from exc


def _h264_base():
    try:
        from aiortc.codecs.h264 import H264Encoder
        return H264Encoder
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc





def bitrate_cap(width: int, height: int, fps: float) -> int:
    """A track's most bits a second, by its frames' size and rate (_CAP_AT_VGA30, _CAP_PIXEL_POWER), within
    [_DEFAULT_MIN_BITRATE, _MOST_BITRATE]."""
    vga = width * height / (640 * 480)
    return max(_DEFAULT_MIN_BITRATE, min(_MOST_BITRATE, int(_CAP_AT_VGA30 * vga ** _CAP_PIXEL_POWER * fps / 30)))


def _rate_of(frame) -> int:
    """The frames a second a frame's time base says (FrameTrack's: 1/hz), else _RATE_UNSAID."""
    tb = frame.time_base
    if tb is not None and tb.numerator == 1 and 1 <= tb.denominator <= _MOST_RATE:
        return int(tb.denominator)
    return _RATE_UNSAID


def _vbv(cc, bitrate: int, rate: int) -> bool:
    """`bitrate` for the codec `cc`, held to it a frame at a time: VBV's most rate the bitrate and its buffer one frame's
    share (bitrate / frames a second), so no frame, a keyframe either, is much more than its share. Set when the codec
    opens, VBV is on from the start, and a later bitrate goes to the running codec: FFmpeg's libx264 reconfigures x264
    whenever bit_rate, rc_max_rate or rc_buffer_size changed before a frame (libx264.c reconfig_encoder) - only where VBV
    was on when it opened ("VBV can't be turned on if it wasn't on to begin with", x264 encoder.c) - so a new bitrate
    needs no new codec and no keyframe.



    Returns whether the VBV went in as said: False on a PyAV before 19, which sets neither (18.1, the newest for Python
    3.11 - PyAV 19 needs 3.12), where only the bitrate is set and the codec opens with its VBV at its most (_open_codec).
    {PyPI av 19.0.0 requires_python ">=3.12"; av 18.1.0: "attribute 'max_bit_rate' ... is not writable", no
    rc_buffer_size}"""
    cc.bit_rate = bitrate
    try:
        cc.max_bit_rate = bitrate
        cc.rc_buffer_size = max(bitrate * _VBV_FRAMES // max(rate, 1), 1)
    except AttributeError:
        return False
    return True


@dataclass(frozen=True)
class EncoderKind:
    """One H.264 encoder as this module opens it: FFmpeg's name for it, the options that make it low latency, the pixel
    format it takes, its profile, and whether a new bitrate goes to it as it runs (FFmpeg reconfigures it between
    frames) - else a new codec is made for a move of a third (_REBUILD_BITRATE_THRESHOLD), and a keyframe with it."""
    name: str
    options: dict = field(default_factory=dict)
    pix_fmt: str = "yuv420p"
    profile: Optional[str] = "Baseline"
    live_bitrate: bool = False


LIBX264 = EncoderKind(ENCODER, _LIBX264_OPTS, live_bitrate=True)








HARDWARE = (
    EncoderKind("h264_videotoolbox", {"allow_sw": "0"}),
    EncoderKind("h264_nvenc", {"preset": "p1", "tune": "ull", "zerolatency": "1", "delay": "0", "rc": "cbr",
                               "forced-idr": "1"}),
    EncoderKind("h264_qsv", {"preset": "veryfast", "async_depth": "1", "look_ahead": "0", "forced_idr": "1"},
                pix_fmt="nv12"),
    EncoderKind("h264_amf", {"usage": "ultralowlatency", "quality": "speed", "rc": "cbr"}),
    EncoderKind("h264_mf", {"hw_encoding": "1", "rate_control": "cbr"}, pix_fmt="nv12"),
    EncoderKind("h264_v4l2m2m", {}, profile=None),
)


_REBUILD_BITRATE_THRESHOLD = 0.3
_REBUILD_MIN_INTERVAL_S = 2.0


def _open_codec(width: int, height: int, rate: int, bitrate: int, most: int, kind: Optional[EncoderKind] = None):
    """A codec of `kind` (libx264 where None) for frames of this size and rate at `bitrate`, which may be raised to `most`
    as it runs, all of its settings here and in _vbv: another encoder is another EncoderKind, the encoder class
    unchanged."""
    import fractions

    kind = kind or LIBX264
    av = _av()
    cc = av.CodecContext.create(kind.name, "w")
    cc.width, cc.height = width, height
    cc.pix_fmt = kind.pix_fmt


    options = dict(kind.options)
    if not _vbv(cc, bitrate, rate):


        options.update(maxrate=str(most), bufsize=str(max(most * _VBV_FRAMES // max(rate, 1), 1)))
    cc.gop_size = _GOP_FRAMES


    cc.framerate = fractions.Fraction(rate, 1)
    cc.time_base = fractions.Fraction(1, rate)
    try:
        cc.max_b_frames = 0
    except Exception:
        pass
    cc.options = options
    if kind.profile:
        try:
            cc.profile = kind.profile
        except Exception:
            pass
    return cc





_MEASURE_FRAMES = 8
_PREFER_HARDWARE_MS = 1.0
_CHOICE: dict = {}


def _available() -> set:
    """The encoders this PyAV has."""
    return set(_av().codecs_available)


def _measure(kind: EncoderKind, width: int, height: int, rate: int) -> Optional[float]:
    """The median milliseconds from a frame handed to a codec of `kind` to its packet coming out, frames handed at
    `rate` as a robot's camera hands them - so an encoder that answers a frame only at a later call
 shows the wait; None where it
    does not open, or answers no frame."""
    import fractions

    av = _av()
    try:
        import numpy as np
        cc = _open_codec(width, height, rate, 1_000_000, 1_000_000, kind)
        image = np.random.default_rng(0).integers(0, 256, (height, width, 3), dtype=np.uint8)
        handed: dict = {}
        took: list = []
        start = time.perf_counter()
        for i in range(_MEASURE_FRAMES):
            time.sleep(max(0.0, start + i / rate - time.perf_counter()))
            frame = av.VideoFrame.from_ndarray(np.roll(image, i * 4, axis=1), format="rgb24").reformat(format=kind.pix_fmt)
            frame.pts, frame.time_base = i, fractions.Fraction(1, rate)
            handed[i] = time.perf_counter()
            for packet in cc.encode(frame):
                if packet.pts in handed:
                    took.append((time.perf_counter() - handed[packet.pts]) * 1000.0)
    except Exception as exc:
        _log.info("teleop_video: %s does not open here (%s)", kind.name, exc)
        return None
    return statistics.median(took) if len(took) >= _MEASURE_FRAMES // 2 else None


def chosen(width: int = 640, height: int = 480, rate: int = 30) -> EncoderKind:
    """The encoder this process sends with, decided once: SEQ_TELEOP_ENCODER's where it names one that opens here,
    else libx264 and each hardware encoder this PyAV has measured (_measure) on frames of this size and rate, the
    fastest kept - a hardware one within _PREFER_HARDWARE_MS of it, which spares the CPU - and libx264 where none
    answers."""
    if "kind" in _CHOICE:
        return _CHOICE["kind"]
    asked = os.environ.get("SEQ_TELEOP_ENCODER", "auto").strip() or "auto"
    kinds = {k.name: k for k in (LIBX264, *HARDWARE)}
    tried: dict = {}
    if asked != "auto" and asked in kinds and (asked == ENCODER or asked in _available()):
        tried[asked] = _measure(kinds[asked], width, height, rate)
        if tried[asked] is not None:
            _CHOICE.update(kind=kinds[asked], tried_ms=tried, asked=asked)
            _log.info("teleop_video: %s, as SEQ_TELEOP_ENCODER says (%.1f ms a frame)", asked, tried[asked])
            return kinds[asked]
    if asked != "auto":
        _log.warning("teleop_video: SEQ_TELEOP_ENCODER=%s does not open here; measuring the encoders this machine has",
                     asked)
    have = _available()
    for kind in (LIBX264, *(k for k in HARDWARE if k.name in have)):
        if kind.name not in tried:
            tried[kind.name] = _measure(kind, width, height, rate)
    answered = {name: ms for name, ms in tried.items() if ms is not None}
    best = min(answered, key=answered.get) if answered else ENCODER
    for kind in HARDWARE:
        if kind.name in answered and answered[kind.name] <= answered.get(best, 0.0) + _PREFER_HARDWARE_MS:
            best = kind.name
            break
    _CHOICE.update(kind=kinds[best], tried_ms=tried, asked=asked)
    _log.info("teleop_video: sending with %s; measured (ms a frame) %s", best,
              {n: (None if ms is None else round(ms, 1)) for n, ms in tried.items()})
    return kinds[best]


def encoder_report() -> dict:
    """What teleop_metrics() says of the encoder: {"name", "tried_ms": {name: its median ms, None where it did not open},
    "asked": SEQ_TELEOP_ENCODER's}; {} before the first frame chose one."""
    if "kind" not in _CHOICE:
        return {}
    return {"name": _CHOICE["kind"].name, "tried_ms": dict(_CHOICE["tried_ms"]), "asked": _CHOICE["asked"]}


def make_video_encoder(*, min_bitrate: int = _DEFAULT_MIN_BITRATE, max_bitrate: Optional[int] = None):
    """Build the aiortc Encoder for the direct-connect video track. Separate from the class definition so the aiortc
    import stays lazy. `max_bitrate`: the most for its track, or None - by its frames' size and rate (bitrate_cap)."""
    base = _h264_base()
    av = _av()
    from aiortc.mediastreams import VIDEO_TIME_BASE, convert_timebase

    class _VideoEncoder(base):
        """A drop-in for aiortc's H264Encoder: same libx264 and the same RTP packetisation, but the bitrate may run up to
        its track's cap (aiortc stops at 3 Mbps), x264 is told its frames' own rate, a new bitrate goes to the running
        codec (aiortc makes a new one, and a keyframe, on any 10% move), and a keyframe comes only when asked for or with
        a new size or rate (_GOP_FRAMES, _vbv)."""

        def __init__(self) -> None:
            super().__init__()
            self._min_bitrate = int(min_bitrate)
            self._max_bitrate = None if max_bitrate is None else int(max_bitrate)

            self._cap = self._max_bitrate if self._max_bitrate is not None else _MOST_BITRATE
            self._bitrate = min(max(1_000_000, self._min_bitrate), self._cap)
            self._rate: Optional[int] = None
            self._cc = None
            self._kind: Optional[EncoderKind] = None
            self._rebuilds = 0
            self._retunes = 0
            self._last_rebuild_t = 0.0
            self._last_latency_ms: Optional[float] = None

        @property
        def encoder_name(self) -> str:
            return (self._kind or _CHOICE.get("kind") or LIBX264).name

        @property
        def last_latency_ms(self) -> Optional[float]:
            """Encode wall time of the most recent frame, for the connection's stats."""
            return self._last_latency_ms


        @property
        def target_bitrate(self) -> int:
            return self._bitrate

        @target_bitrate.setter
        def target_bitrate(self, bitrate: int) -> None:
            self._bitrate = max(self._min_bitrate, min(int(bitrate), self._cap))

        def _ensure_cc(self, frame) -> None:
            rate = _rate_of(frame)

            if self._cc is not None and (frame.width != self._cc.width or frame.height != self._cc.height
                                         or rate != self._rate):
                self._cc = None
            if self._cc is not None and self._cc.bit_rate != self._bitrate:
                if self._kind.live_bitrate:
                    _vbv(self._cc, self._bitrate, self._rate)
                    self._retunes += 1
                elif (abs(self._bitrate - self._cc.bit_rate) / max(self._cc.bit_rate, 1) > _REBUILD_BITRATE_THRESHOLD
                      and time.perf_counter() - self._last_rebuild_t >= _REBUILD_MIN_INTERVAL_S):
                    self._cc = None
            if self._cc is not None:
                return
            if self._kind is None:
                self._kind = chosen(frame.width, frame.height, rate)
            self._rebuilds += 1
            self._last_rebuild_t = time.perf_counter()
            self._rate = rate
            if self._max_bitrate is None:
                self._cap = bitrate_cap(frame.width, frame.height, rate)
                self._bitrate = max(self._min_bitrate, min(self._bitrate, self._cap))
            self._cc = _open_codec(frame.width, frame.height, rate, self._bitrate, self._cap, self._kind)

        def encode(self, frame, force_keyframe: bool = False):
            assert isinstance(frame, av.VideoFrame)
            self._ensure_cc(frame)
            if frame.format.name != self._kind.pix_fmt:
                pts, time_base = frame.pts, frame.time_base
                frame = frame.reformat(format=self._kind.pix_fmt)
                frame.pts, frame.time_base = pts, time_base
            frame.pict_type = (
                av.video.frame.PictureType.I if force_keyframe else av.video.frame.PictureType.NONE
            )
            started = time.perf_counter()
            packets = list(self._cc.encode(frame))
            self._last_latency_ms = (time.perf_counter() - started) * 1000.0
            if not packets:
                return [], convert_timebase(frame.pts, frame.time_base, VIDEO_TIME_BASE)
            data = b"".join(bytes(p) for p in packets)
            tb = packets[0].time_base or frame.time_base
            timestamp = convert_timebase(packets[0].pts, tb, VIDEO_TIME_BASE)
            return self._packetize(self._split_bitstream(data)), timestamp

    return _VideoEncoder()


def install_encoder(*, min_bitrate: int = _DEFAULT_MIN_BITRATE,
                    max_bitrate: Optional[int] = None) -> tuple[str, Callable[[], None]]:
    """Make aiortc hand out our encoder for H264 on every new sender - libx264, or a hardware encoder measured faster
    here at its first frame (chosen) - returning (the encoder chosen in this process so far, libx264 until one is;
    restore). aiortc's
    sender binds `get_encoder` by name at import, so we patch it where it is used (rtcrtpsender) and in the codecs module.
    Call once per process before building the RTCPeerConnection; call restore() (e.g. on Driven.close()) to undo it."""
    import aiortc.codecs as _codecs
    import aiortc.rtcrtpsender as _sender

    orig_codecs = _codecs.get_encoder
    orig_sender = _sender.get_encoder

    def _patched(codec):
        if getattr(codec, "name", "") == "H264":
            return make_video_encoder(min_bitrate=min_bitrate, max_bitrate=max_bitrate)
        return orig_codecs(codec)

    _codecs.get_encoder = _patched
    _sender.get_encoder = _patched








    orig_uint32_add = _sender.uint32_add
    _sender.uint32_add = lambda _origin, ts: ts & 0xFFFFFFFF
    _log.info("teleop_video: installed %s encoder into aiortc (bitrate from %d bps, at most %s), RTP origin pinned", ENCODER,
              min_bitrate, max_bitrate or "by each track's size and rate")


    restore_playout = install_playout_delay()

    def restore() -> None:
        _codecs.get_encoder = orig_codecs
        _sender.get_encoder = orig_sender
        _sender.uint32_add = orig_uint32_add
        restore_playout()

    return (_CHOICE.get("kind") or LIBX264).name, restore











PLAYOUT_DELAY_URI = "http://www.webrtc.org/experiments/rtp-hdrext/playout-delay"
_SHOW_AT_ONCE = b"\x00\x00\x00"


def install_playout_delay() -> Callable[[], None]:
    """Every video sender of this process says playout-delay 0 and 0 on each packet, where the other side has the
    extension: its URI among aiortc's video header extensions - an answer keeps the offer's id for it, an offer of ours
    names it with an id no other extension has (one id space under BUNDLE) - and each packet of a sender that agreed it
    carries it. Read when the remote description is set, so it goes in first. Returns restore()."""
    import aiortc.codecs as _codecs
    from aiortc import rtp as _rtp
    from aiortc.rtcrtpparameters import RTCRtpHeaderExtensionParameters

    extensions_map = _rtp.HeaderExtensionsMap
    if getattr(extensions_map.set, "_seq_playout_delay", False):
        return lambda: None
    video = _codecs.HEADER_EXTENSIONS["video"]
    added = None
    if all(e.uri != PLAYOUT_DELAY_URI for e in video):
        taken = {e.id for kind in _codecs.HEADER_EXTENSIONS.values() for e in kind}
        added = RTCRtpHeaderExtensionParameters(id=min(set(range(1, 15)) - taken), uri=PLAYOUT_DELAY_URI)
        video.append(added)
    orig_configure, orig_set = extensions_map.configure, extensions_map.set

    def configure(self, parameters) -> None:
        orig_configure(self, parameters)

        self._seq_playout_delay = next((e.id for e in parameters.headerExtensions if e.uri == PLAYOUT_DELAY_URI), None)

    def set_(self, values):
        profile, value = orig_set(self, values)
        ext_id = getattr(self, "_seq_playout_delay", None)
        if not ext_id:
            return profile, value
        return _rtp.pack_header_extensions(_rtp.unpack_header_extensions(profile, value) + [(ext_id, _SHOW_AT_ONCE)])

    set_._seq_playout_delay = True
    extensions_map.configure, extensions_map.set = configure, set_

    def restore() -> None:
        extensions_map.configure, extensions_map.set = orig_configure, orig_set
        if added is not None and added in video:
            video.remove(added)

    return restore





def FrameTrack(key: str, *, hz: float, send_meta: Optional[Callable[[dict], None]] = None):
    """The robot's camera as an aiortc video track for the direct connection. The robot's observe() thread calls
    `put(frame, n=, capture_us=)` with the raw HxWx3 uint8 RGB array (before marked encoding), non-blocking and
    latest-only -- an older frame not yet pulled is dropped. recv() hands aiortc the freshest frame, so the send rate
    follows the slower of the camera and the link. Each frame gets a monotonic `seq`, and `send_meta` (the seq-ctl
    sender) carries {seq, n, capture_us, rtp} out of band -- `rtp` the frame's on-wire RTP timestamp (install_encoder pins
    the origin to 0, so it is convert_timebase(pts) exactly), by which the console and the Python receiver pair the frame
    they show to its n and capture time. `put` runs on the observe() thread, so the wake-up is marshalled to the track's
    event loop -- create the track inside that loop. Call `.stop()` to end it."""
    import asyncio
    import fractions

    av = _av()
    try:
        from aiortc import MediaStreamTrack
        from aiortc.mediastreams import VIDEO_TIME_BASE, convert_timebase
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc

    class _FrameTrack(MediaStreamTrack):
        kind = "video"

        def __init__(self) -> None:
            super().__init__()
            self.key = key
            self._hz = float(hz)
            self._send_meta = send_meta
            self._latest = None
            self._have = asyncio.Event()
            self._seq = 0
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = None

        def put(self, frame, *, n: int, capture_us: int) -> None:
            self._latest = (frame, int(n), int(capture_us))
            if self._loop is not None and self._loop.is_running():
                self._loop.call_soon_threadsafe(self._have.set)
            else:
                self._have.set()

        async def recv(self):
            await self._have.wait()
            self._have.clear()
            latest = self._latest
            if latest is None:
                err = _media_stream_error()
                raise err("track ended") if err else RuntimeError("track ended")
            arr, n, capture_us = latest
            vframe = av.VideoFrame.from_ndarray(arr, format="rgb24").reformat(format="yuv420p")
            self._seq += 1
            vframe.pts = self._seq
            vframe.time_base = fractions.Fraction(1, max(1, int(round(self._hz))))
            if self._send_meta is not None:




                rtp = convert_timebase(vframe.pts, vframe.time_base, VIDEO_TIME_BASE) & 0xFFFFFFFF
                try:
                    self._send_meta({"seq": self._seq, "n": n, "capture_us": capture_us, "rtp": int(rtp)})
                except Exception:
                    pass
            return vframe

    return _FrameTrack()





def latest_frame_track(source, *, on_drop: Optional[Callable[[int], None]] = None):
    """Wrap an incoming aiortc video track so the consumer always gets the newest frame and a slow consumer never builds a
    backlog (aiortc's receiver queue is unbounded). A background task pulls from `source` as fast as it delivers and keeps
    only the latest; frames overwritten before the consumer took them are counted as dropped (read `.dropped`, or get each
    batch via `on_drop` -- hand that to the connection's stats). `recv()` returns `(frame_rgb: np.ndarray, n, capture_us)`: the
    `n` and `capture_us` are the ones the sideband meta (the console's on_meta via `feed_meta`) gave for this frame's
    own RTP timestamp, so they are the frame returned, not the newest to arrive; a frame whose meta was lost returns None
    for both. Call `.stop()` to end it."""
    import asyncio

    try:
        from aiortc import MediaStreamTrack
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc

    class _LatestFrameTrack(MediaStreamTrack):
        kind = "video"

        def __init__(self) -> None:
            super().__init__()
            self._source = source
            self._on_drop = on_drop
            self._latest = None
            self._have = asyncio.Event()
            self._consumed = True
            self.dropped = 0
            self._by_rtp = {}
            self._pump = asyncio.ensure_future(self._drain())

        def feed_meta(self, meta: dict) -> None:
            """Called from the console side's on_meta handler (seq-ctl): remember each frame's n and capture time by its
            `rtp`, so recv() pairs the frame it returns to its own meta, not the newest to arrive."""
            rtp = meta.get("rtp")
            if rtp is None:
                return
            self._by_rtp[int(rtp) & 0xFFFFFFFF] = (meta.get("n"), meta.get("capture_us"))
            if len(self._by_rtp) > 600:
                self._by_rtp.pop(next(iter(self._by_rtp)))

        async def _drain(self) -> None:
            while True:
                try:
                    frame = await self._source.recv()
                except Exception:
                    self._have.set()
                    return
                if not self._consumed and self._latest is not None:
                    self.dropped += 1
                    if self._on_drop is not None:
                        try:
                            self._on_drop(1)
                        except Exception:
                            pass
                self._latest = frame
                self._consumed = False
                self._have.set()

        async def recv(self):
            await self._have.wait()
            self._have.clear()
            self._consumed = True
            if self._latest is None:
                err = _media_stream_error()
                raise err("track ended") if err else RuntimeError("track ended")
            arr = self._latest.to_ndarray(format="rgb24")


            pts = getattr(self._latest, "pts", None)
            n, capture_us = self._by_rtp.get(int(pts) & 0xFFFFFFFF, (None, None)) if pts is not None else (None, None)
            return arr, n, capture_us

        def stop(self) -> None:
            if not self._pump.done():
                self._pump.cancel()


            self._latest = None
            self._have.set()
            super().stop()

    return _LatestFrameTrack()


def _media_stream_error():
    try:
        from aiortc.mediastreams import MediaStreamError
        return MediaStreamError
    except Exception:
        return None





def install_wire_timestamps() -> Callable[[], None]:
    """Make a received frame's pts the RTP timestamp it came with. aiortc's receiver counts from the first timestamp it sees
    (rtcrtpreceiver.TimestampMapper), so a frame's pts is short of the `rtp` its sideband message names by the first frame's:
    every frame was paired with the step before it. Nothing else reads the pts. This replaces an aiortc internal, so
    pyproject pins the minor tested; one without it fails here. Returns a restore().
"""
    try:
        from aiortc import rtcrtpreceiver as _receiver
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc

    mapper = _receiver.TimestampMapper
    original = mapper.map
    mapper.map = lambda self, timestamp: timestamp

    def restore() -> None:
        mapper.map = original

    return restore


def install_jitterbuffer_marker_release() -> Callable[[], None]:
    """Make aiortc's video jitterbuffer emit a frame the moment its last packet (the one the sender marks) is in, rather
    than wait for the first packet of the NEXT frame. aiortc releases only on a timestamp change (jitterbuffer.py:77) and
    never reads the RTP marker the sender sets (rtcrtpsender.py:385), so every frame waits ~one frame interval -- ~33 ms
    at 30 fps, straight onto the glass-to-glass latency. This patches `JitterBuffer._remove_frame` for video only and
    stays gap-safe: a frame whose packets are not yet contiguous from the buffer origin (a missing/late packet before the
    marker) is held until it fills; audio is untouched. Monkeypatch -- aiortc is BSD-3, and this is a small, well isolated
    method. This replaces an aiortc internal, so pyproject pins the minor tested; one without it fails here. Returns a
    restore()."""
    try:
        from aiortc.jitterbuffer import JitterBuffer, JitterFrame
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc

    original = JitterBuffer._remove_frame

    def _remove_frame(self, sequence_number: int):
        if not self._is_video:
            return original(self, sequence_number)
        packets = []
        timestamp = None
        for count in range(self._capacity):
            packet = self._packets[(self._origin + count) % self._capacity]
            if packet is None:
                break
            if timestamp is None:
                timestamp = packet.timestamp
            elif packet.timestamp != timestamp:

                frame = JitterFrame(data=b"".join(p._data for p in packets), timestamp=timestamp)
                self.remove(count)
                return frame
            packets.append(packet)
            if getattr(packet, "marker", 0):
                frame = JitterFrame(data=b"".join(p._data for p in packets), timestamp=timestamp)
                self.remove(count + 1)
                return frame
        return None

    JitterBuffer._remove_frame = _remove_frame
    _log.info("teleop_video: installed jitterbuffer marker-release (video frames emit ~1 frame sooner)")
    return lambda: setattr(JitterBuffer, "_remove_frame", original)





class _TimedNack:
    """Decides, from the receiver's current set of missing packets, which to NACK again and which to give up on. Pure
    policy -- no aiortc, time injected -- so it is unit-tested on its own. aiortc NACKs a gap once on detection and never
    again (rtcrtpreceiver.py:535); here a still-missing packet is re-NACKed every ~RTT (libwebrtc's kLowRttNackMs = 20),
    and one missing past a deadline is given up so its frame does not freeze the picture -- the caller asks for a
    keyframe (PLI)."""

    def __init__(self) -> None:
        self._first_ms: dict[int, float] = {}
        self._nacked_ms: dict[int, float] = {}

    def observe(self, missing, now_ms: float) -> None:
        """Sync with the receiver's current `missing` set: forget recovered seqs, start the clock on new ones (aiortc
        already NACKed each once, on detection)."""
        for seq in list(self._first_ms):
            if seq not in missing:
                self._first_ms.pop(seq, None)
                self._nacked_ms.pop(seq, None)
        for seq in missing:
            if seq not in self._first_ms:
                self._first_ms[seq] = now_ms
                self._nacked_ms[seq] = now_ms

    def due(self, now_ms: float, interval_ms: float) -> list:
        """Seqs whose last NACK is at least `interval_ms` old -- re-NACK them."""
        return sorted(s for s, t in self._nacked_ms.items() if now_ms - t >= interval_ms)

    def mark_nacked(self, seqs, now_ms: float) -> None:
        for s in seqs:
            if s in self._nacked_ms:
                self._nacked_ms[s] = now_ms

    def expired(self, now_ms: float, deadline_ms: float) -> list:
        """Seqs missing for at least `deadline_ms` -- give up on them (and the frame they belong to)."""
        return sorted(s for s, t in self._first_ms.items() if now_ms - t >= deadline_ms)

    def forget(self, seqs) -> None:
        for s in seqs:
            self._first_ms.pop(s, None)
            self._nacked_ms.pop(s, None)


def skip_lost(buffer, lost) -> int:
    """Move a video jitterbuffer on past packets given up for lost: what it holds from its origin through the last of them is
    dropped, with the rest of the frame the hole is in - a frame nothing can complete now - so the frames after the hole go
    out as they complete, and the keyframe the PLI sent with this asks for mends the picture. Without it the buffer held
    every later frame, that keyframe too, until 512 packets had come behind the hole (aiortc's video capacity): seconds.
    Returns how many packets it dropped.

"""
    from aiortc.utils import uint16_add

    origin, capacity = buffer._origin, buffer._capacity
    if origin is None:
        return 0
    ahead = [seq for seq in lost if uint16_add(seq, -origin) < capacity]
    if not ahead:
        return 0
    last = max(ahead, key=lambda seq: uint16_add(seq, -origin))
    count = uint16_add(last, -origin) + 1
    held = (buffer._packets[(origin + i) % capacity] for i in range(count))
    timestamp = next((packet.timestamp for packet in held if packet is not None), None)
    buffer.remove(count)
    dropped = count
    while True:
        packet = buffer._packets[buffer._origin % capacity]
        if packet is None or (timestamp is not None and packet.timestamp != timestamp):
            break
        buffer.remove(1)
        dropped += 1
        if timestamp is None and getattr(packet, "marker", 0):
            break
    return dropped


_JITTER_BUFFER = "_RTCRtpReceiver__jitter_buffer"


def _give_up(receiver, nack, expired) -> None:
    """Packets missing past the deadline: NACKed no more, and the receiver's jitterbuffer moved on past them (skip_lost)."""
    nack.missing.difference_update(expired)
    buffer = getattr(receiver, _JITTER_BUFFER, None)
    if buffer is not None:
        skip_lost(buffer, expired)


def install_nack_retransmit(*, rtt_nack_ms: float = 20.0, give_up_ms: float = 100.0) -> Callable[[], None]:
    """Keep NACKing a lost video packet until it arrives or a deadline passes, then ask for a keyframe. aiortc sends a
    NACK once when it first sees a gap and never resends it (rtcrtpreceiver.py:535); if that single NACK is also lost the
    picture stalls until the buffer fills (~5 s). This starts, per video receiver, a ~`rtt_nack_ms` loop that re-NACKs
    still-missing packets and, for one missing past `give_up_ms`, sends a PLI and moves the jitterbuffer on past it
    (skip_lost). The loop lives as long as the receiver's own RTCP task and reads aiortc's existing
    NackGenerator.missing -- it does not replace it. Monkeypatch on `_handle_rtp_packet` (video only, audio has no nack
    generator). This replaces and calls aiortc internals, so pyproject pins the minor tested; one without them fails
    here. Returns restore()."""
    import asyncio

    try:
        from aiortc.rtcrtpreceiver import RTCRtpReceiver
    except ImportError as exc:
        raise MissingPackage("aiortc", extra="teleop") from exc

    NG, SSRC, EXITED = ("_RTCRtpReceiver__nack_generator", "_RTCRtpReceiver__rtcp_ssrc", "_RTCRtpReceiver__rtcp_exited")
    original = RTCRtpReceiver._handle_rtp_packet
    send_nack, send_pli = RTCRtpReceiver._send_rtcp_nack, RTCRtpReceiver._send_rtcp_pli

    async def _retransmit_loop(self, media_ssrc: int) -> None:
        timed = _TimedNack()
        loop = asyncio.get_running_loop()
        while True:
            await asyncio.sleep(rtt_nack_ms / 1000.0)
            exited = getattr(self, EXITED, None)
            if exited is not None and exited.is_set():
                return
            nack = getattr(self, NG, None)
            if nack is None or not getattr(nack, "missing", None):
                continue
            now = loop.time() * 1000.0
            timed.observe(set(nack.missing), now)
            ssrc = getattr(self, SSRC, None)
            due = timed.due(now, rtt_nack_ms)
            if due and ssrc is not None:
                try:
                    await send_nack(self, media_ssrc, due)
                    timed.mark_nacked(due, now)
                except Exception:
                    pass
            expired = timed.expired(now, give_up_ms)
            if expired:
                if ssrc is not None:
                    try:
                        await send_pli(self, media_ssrc)
                    except Exception:
                        pass
                timed.forget(expired)
                _give_up(self, nack, expired)

    async def _patched(self, packet, arrival_time_ms):
        if getattr(self, NG, None) is not None and not getattr(self, "_teleop_nack_started", False):
            self._teleop_nack_started = True
            asyncio.ensure_future(_retransmit_loop(self, packet.ssrc))
        return await original(self, packet, arrival_time_ms)

    RTCRtpReceiver._handle_rtp_packet = _patched
    _log.info("teleop_video: installed NACK retransmit (every %.0f ms, give up at %.0f ms -> keyframe)",
              rtt_nack_ms, give_up_ms)
    return lambda: setattr(RTCRtpReceiver, "_handle_rtp_packet", original)


