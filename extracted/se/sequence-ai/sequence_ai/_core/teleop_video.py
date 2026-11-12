"""The WebRTC video path for direct-connect teleop (operator <-> robot, aiortc): encode low-latency H264 with a bitrate
cap you can lift, on the receive side keep only the freshest frame, and release each frame on its RTP marker instead of a
frame late.

Software libx264 only, on purpose. The operator's and the robot's machines are not any one kind -- "not always mac but
might be other computer", and not always a box with an NVIDIA card -- so there is no hardware-specific encoder path here;
one cross-platform encoder behaves the same everywhere. {the user 11-10: "we sholldnt optimize for the hardware because
amc is not always mac but might be other computer"}


Why this file exists -- aiortc 1.16 ships one H264 path and it is limiting for teleop (verified in source):
  * codecs/h264.py clamps the bitrate to 0.5-3 Mbps (MIN_BITRATE/MAX_BITRATE), so anything above 3 Mbps is unreachable,
    and re-creates the codec on any >10% bitrate change (h264.py:246), each rebuild a keyframe spike;
  * rtcrtpreceiver.py feeds decoded frames through an unbounded `asyncio.Queue()`, so a slow consumer lags further and
    further behind;
  * the jitterbuffer releases a frame only when the NEXT frame's first packet arrives (jitterbuffer.py:77, a timestamp
    change) and never reads the RTP marker the sender sets (rtcrtpsender.py:385) -- ~one frame interval (~33 ms at
    30 fps) of pure latency on every frame.
This module addresses all three without forking aiortc: a drop-in libx264 encoder with a configurable [min, max] bitrate
and rebuild hysteresis, a receive-side track that drains to the newest frame, and a marker-release patch for the
jitterbuffer. Low-latency libx264 params match aiortc's: zerolatency, Baseline (no B-frames), keyframe on demand.

Robots differ only by parameters here (bitrate, resolution come from config) -- there is no per-robot code.

New dependencies (aiortc, av) live in the `teleop` extra, imported lazily; without them these calls raise MissingPackage.
Interface owned here; wired into the connection by sequence_ai/_core/teleop.py and teleop_robot.py (worker 3).
"""
from __future__ import annotations

import logging
import time
from typing import Callable, Optional

from ..errors import MissingPackage

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


_REBUILD_BITRATE_THRESHOLD = 0.3
_REBUILD_MIN_INTERVAL_S = 2.0


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


def make_video_encoder(*, min_bitrate: int = _DEFAULT_MIN_BITRATE, max_bitrate: Optional[int] = None):
    """Build the aiortc Encoder for the direct-connect video track. Separate from the class definition so the aiortc
    import stays lazy. `max_bitrate`: the most for its track, or None - by its frames' size and rate (bitrate_cap)."""
    base = _h264_base()
    av = _av()
    from aiortc.mediastreams import VIDEO_TIME_BASE, convert_timebase

    class _VideoEncoder(base):
        """A drop-in for aiortc's H264Encoder: same libx264 and the same RTP packetisation, but the bitrate may run up to
        its track's cap (aiortc stops at 3 Mbps), x264 is told its frames' own rate, and the codec is not re-created on
        every small bitrate change."""

        def __init__(self) -> None:
            super().__init__()
            self._min_bitrate = int(min_bitrate)
            self._max_bitrate = None if max_bitrate is None else int(max_bitrate)

            self._cap = self._max_bitrate if self._max_bitrate is not None else _MOST_BITRATE
            self._bitrate = min(max(1_000_000, self._min_bitrate), self._cap)
            self._rate: Optional[int] = None
            self._cc = None
            self._last_latency_ms: Optional[float] = None
            self._rebuilds = 0
            self._last_rebuild_t = 0.0

        @property
        def encoder_name(self) -> str:
            return ENCODER

        @property
        def last_latency_ms(self) -> Optional[float]:
            """Encode wall time of the most recent frame, for worker 1's stats."""
            return self._last_latency_ms


        @property
        def target_bitrate(self) -> int:
            return self._bitrate

        @target_bitrate.setter
        def target_bitrate(self, bitrate: int) -> None:
            self._bitrate = max(self._min_bitrate, min(int(bitrate), self._cap))

        def _ensure_cc(self, frame) -> None:
            import fractions

            rate = _rate_of(frame)
            resized = self._cc is not None and (frame.width != self._cc.width or frame.height != self._cc.height
                                                or rate != self._rate)
            bitrate_moved = self._cc is not None and (
                abs(self._bitrate - self._cc.bit_rate) / max(self._cc.bit_rate, 1) > _REBUILD_BITRATE_THRESHOLD
                and (time.perf_counter() - self._last_rebuild_t) >= _REBUILD_MIN_INTERVAL_S
            )
            if resized or bitrate_moved:
                self._cc = None
            if self._cc is None:
                self._rebuilds += 1
                self._last_rebuild_t = time.perf_counter()
                self._rate = rate
                if self._max_bitrate is None:
                    self._cap = bitrate_cap(frame.width, frame.height, rate)
                    self._bitrate = max(self._min_bitrate, min(self._bitrate, self._cap))
                cc = av.CodecContext.create(ENCODER, "w")
                cc.width, cc.height = frame.width, frame.height
                cc.pix_fmt = "yuv420p"
                cc.bit_rate = self._bitrate


                cc.framerate = fractions.Fraction(rate, 1)
                cc.time_base = fractions.Fraction(1, rate)
                try:
                    cc.max_b_frames = 0
                except Exception:
                    pass
                cc.options = _LIBX264_OPTS
                try:
                    cc.profile = _LIBX264_PROFILE
                except Exception:
                    pass
                self._cc = cc

        def encode(self, frame, force_keyframe: bool = False):
            assert isinstance(frame, av.VideoFrame)
            self._ensure_cc(frame)
            frame.pict_type = (
                av.video.frame.PictureType.I if force_keyframe else av.video.frame.PictureType.NONE
            )
            t0 = time.perf_counter()
            packets = list(self._cc.encode(frame))
            self._last_latency_ms = (time.perf_counter() - t0) * 1000.0
            if not packets:
                return [], convert_timebase(frame.pts, frame.time_base, VIDEO_TIME_BASE)
            data = b"".join(bytes(p) for p in packets)
            tb = packets[0].time_base or frame.time_base
            timestamp = convert_timebase(packets[0].pts, tb, VIDEO_TIME_BASE)
            return self._packetize(self._split_bitstream(data)), timestamp

    return _VideoEncoder()


def install_encoder(*, min_bitrate: int = _DEFAULT_MIN_BITRATE,
                    max_bitrate: Optional[int] = None) -> tuple[str, Callable[[], None]]:
    """Make aiortc hand out our libx264 encoder for H264 on every new sender. Returns (encoder_name, restore). aiortc's
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

    def restore() -> None:
        _codecs.get_encoder = orig_codecs
        _sender.get_encoder = orig_sender
        _sender.uint32_add = orig_uint32_add

    return ENCODER, restore





def FrameTrack(key: str, *, hz: float, send_meta: Optional[Callable[[dict], None]] = None):
    """The robot's camera as an aiortc video track for the direct connection. The robot's observe() thread calls
    `put(frame, n=, capture_us=)` with the raw HxWx3 uint8 RGB array (before marked encoding), non-blocking and
    latest-only -- an older frame not yet pulled is dropped. recv() hands aiortc the freshest frame, so the send rate
    follows the slower of the camera and the link. Each frame gets a monotonic `seq`, and `send_meta` (worker 3's seq-ctl
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
    batch via `on_drop` -- hand that to worker 1's stats). `recv()` returns `(frame_rgb: np.ndarray, n, capture_us)`: the
    `n` and `capture_us` are the ones the sideband meta (worker 3's console on_meta via `feed_meta`) gave for this frame's
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
            """worker 3 calls this from its console-side on_meta handler (seq-ctl): remember each frame's n and capture
            time by its `rtp`, so recv() pairs the frame it returns to its own meta, not the newest to arrive."""
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
    pyproject pins the minor tested; one without it fails here. Returns a restore(). {loopback check 11-11, before this: 0 of
    61 frames named by the step their picture is of}"""
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
    Returns how many packets it dropped. {dev 11-11, the robot on the mini and the console on Wi-Fi, 4 runs: 3 to 4 s with no
    frame in 3 of them, both cameras, the PLI sent within 0.5 s and the robot's keyframe at once - its arrival 2.7 to 3.7 s
    later, as the buffer overflowed; the arrays meanwhile on time}"""
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





def bench_encoder(width: int, height: int, *, n: int = 120, fps: float = 30.0, bitrate: int = 2_000_000) -> dict:
    """Encode `n` synthetic frames paced at `fps` and measure each frame's wall time from submission to its encoded
    packet. Returns {encoder, size, p50_ms, p95_ms, n, out_kbps}. Dev/measurement only; needs numpy."""
    import fractions
    import statistics

    av = _av()
    try:
        import numpy as np
    except ImportError as exc:
        raise MissingPackage("numpy", extra="teleop") from exc

    def make_frame(i: int):
        arr = np.empty((height, width, 3), dtype=np.uint8)
        arr[:, :, 0] = ((np.arange(width, dtype=np.int32)[None, :] + i * 3) % 256).astype(np.uint8)
        arr[:, :, 1] = ((np.arange(height, dtype=np.int32)[:, None] + i * 5) % 256).astype(np.uint8)
        arr[:, :, 2] = np.uint8((i * 7) % 256)
        f = av.VideoFrame.from_ndarray(arr, format="rgb24").reformat(format="yuv420p")
        f.pts = i
        f.time_base = fractions.Fraction(1, int(round(fps)))
        return f

    cc = av.CodecContext.create(ENCODER, "w")
    cc.width, cc.height, cc.pix_fmt = width, height, "yuv420p"
    cc.framerate = fractions.Fraction(int(round(fps)), 1)
    cc.time_base = fractions.Fraction(1, int(round(fps)))
    cc.bit_rate = bitrate
    try:
        cc.max_b_frames = 0
    except Exception:
        pass
    cc.options = _LIBX264_OPTS
    try:
        cc.profile = _LIBX264_PROFILE
    except Exception:
        pass

    submit_wall: dict[int, float] = {}
    latencies: list[float] = []
    out_bytes = 0
    period = 1.0 / fps
    start = time.perf_counter()
    for i in range(n):
        target = start + i * period
        delay = target - time.perf_counter()
        if delay > 0:
            time.sleep(delay)
        f = make_frame(i)
        if i == 0:
            f.pict_type = av.video.frame.PictureType.I
        submit_wall[i] = time.perf_counter()
        for p in cc.encode(f):
            now = time.perf_counter()
            out_bytes += p.size
            if p.pts in submit_wall:
                latencies.append((now - submit_wall[p.pts]) * 1000.0)
    flush_at = time.perf_counter()
    for p in cc.encode(None):
        out_bytes += p.size
        if p.pts in submit_wall:
            latencies.append((flush_at - submit_wall[p.pts]) * 1000.0)
    latencies.sort()
    p50 = statistics.median(latencies) if latencies else float("nan")
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else float("nan")
    return {
        "encoder": ENCODER,
        "size": f"{width}x{height}",
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
        "n": len(latencies),
        "out_kbps": round(out_bytes * 8 / (n / fps) / 1000),
    }
