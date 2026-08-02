#!/usr/bin/env python3
"""GStreamer RTP Demuxer with ABSOLUTE RTP Timestamps.

This module provides RTSP and file demuxing using GStreamer, extracting H264 NAL units
with ABSOLUTE RTP timestamps that persist across reconnections.

Key features:
- Captures RAW 32-bit RTP timestamps via pad probe BEFORE depayloading
- RTCP Sender Reports for absolute NTP time mapping
- Outputs H264 NAL units for external decoder (PyNvVideoCodec)

Key difference from PyAV/FFmpeg:
- PyAV/FFmpeg normalizes PTS to start near 0 each session (relative timestamps)
- GStreamer provides the ACTUAL raw 32-bit RTP timestamp from the source
- Raw RTP timestamps are at 90kHz and persist across reconnections

Architecture (RTSP):
    RTSP -> rtspsrc -> [PAD PROBE captures raw timestamp] -> rtph264depay ->
         -> h264parse -> appsink (H264 NAL units)

Architecture (File):
    File -> filesrc -> qtdemux -> h264parse -> appsink (H264 NAL units)

Usage:
    from gstreamer_rtp_demuxer import GstRTPDemuxer

    demuxer = GstRTPDemuxer("rtsp://camera/stream")
    demuxer.open()
    for nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns in demuxer.demux():
        # nal_bytes: H264/H265 NAL unit bytes
        # rtp_ts: ABSOLUTE 32-bit RTP timestamp (NOT normalized!)
        # rtp_ts_ns: RTP timestamp converted to nanoseconds
        # absolute_ns: Absolute Unix time if RTCP SR available
        decoded_frame = nvc_decoder.Decode(nal_bytes)
    demuxer.close()
"""

from __future__ import annotations

import logging
import os
import re
import threading
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional, Tuple

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstRtp", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import GLib, Gst, GstRtp  # noqa: E402

Gst.init(None)

logger = logging.getLogger(__name__)

# RTP clock rate for video (H.264/H.265)
RTP_CLOCK_RATE = 90000


def _validate_gst_location(source: str) -> str:
    """Reject source URLs unsafe to interpolate into a Gst.parse_launch string.

    ``Gst.parse_launch`` parses the whole string as pipeline grammar, so a
    source containing whitespace or ``!`` (element separator) could inject or
    reconfigure pipeline elements (e.g. append a ``filesink``). ``self.source``
    comes from backend-supplied camera data, so validate it before use. The
    allowed set covers legitimate rtsp/file URLs; anything with whitespace,
    ``!``, or control chars is refused.
    """
    if not isinstance(source, str) or not source:
        raise ValueError("Empty or non-string GStreamer source")
    if any(c.isspace() for c in source) or "!" in source:
        raise ValueError(f"Refusing unsafe GStreamer source (whitespace/'!' present): {source!r}")
    if any(ord(c) < 0x20 for c in source):
        raise ValueError("Refusing GStreamer source with control characters")
    return source


# Exact PTS -> RTP correlation. Lives in its own gi-free module, in
# camera_streamer/ rather than beside this file, for two reasons: the logic is
# unit-testable on hosts (and in CI) without PyGObject, and `nvdec/` is excluded
# from the coverage denominator by pyproject `[tool.coverage.run] omit`
# ("*/camera_streamer/nvdec/*" — hardware/GPU decode paths). A pure dict is not a
# hardware path, and the correctness of published timestamps should be measured.
# See rtp_correlation.py for the anchor bug it replaces.
try:
    from ..rtp_correlation import DEFAULT_MAX_ENTRIES as _PTS_RTP_MAP_MAX
    from ..rtp_correlation import RtpPtsCorrelator
except ImportError:
    # The subprocess demuxer child (gstreamer_subprocess_demuxer._CHILD_SCRIPT)
    # loads this module by file path under a synthetic package whose parent does
    # not exist, so the relative import above fails there. Mirror the by-path
    # fallback already used for codec_detect below (same directory as that one:
    # camera_streamer/, one level up from nvdec/).
    import importlib.util as _ilu
    import os as _os

    _rc_path = _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
        "rtp_correlation.py",
    )
    _rc_spec = _ilu.spec_from_file_location("rtp_correlation", _rc_path)
    _rc_mod = _ilu.module_from_spec(_rc_spec)
    _rc_spec.loader.exec_module(_rc_mod)
    RtpPtsCorrelator = _rc_mod.RtpPtsCorrelator
    _PTS_RTP_MAP_MAX = _rc_mod.DEFAULT_MAX_ENTRIES

# How often to warn about correlation misses, in nanoseconds.
_RTP_MISS_WARN_INTERVAL_NS = 10_000_000_000  # 10s


class DemuxerType(Enum):
    """Demuxer backend selection."""

    NVC = "nvc"  # PyNvVideoCodec demuxer (files, fastest)
    GSTREAMER = "gstreamer"  # GStreamer demuxer (RTSP with ABSOLUTE RTP timestamps)


@dataclass
class RTCPSenderReport:
    """Parsed RTCP Sender Report for RTP-to-NTP time mapping.

    Attributes:
        ssrc: Synchronization source identifier
        ntp_timestamp: 64-bit NTP timestamp from RTCP SR
        rtp_timestamp: 32-bit RTP timestamp at SR time
        unix_time: NTP timestamp converted to Unix time
        received_at_ns: Local time when SR was received (nanoseconds)
    """

    ssrc: int
    ntp_timestamp: int  # 64-bit NTP timestamp
    rtp_timestamp: int  # 32-bit RTP timestamp at SR time
    unix_time: float  # Converted to Unix timestamp
    received_at_ns: int  # Local time when SR was received


class RTCPTracker:
    """Tracks RTCP Sender Reports for RTP-to-absolute-time mapping.

    RTCP Sender Reports provide the mapping between RTP timestamps (at 90kHz)
    and absolute wall-clock time (NTP). This allows converting any RTP timestamp
    to Unix time for cross-camera synchronization.
    """

    NTP_UNIX_EPOCH_DIFF = 2208988800  # Seconds between 1900 and 1970

    def __init__(self, clock_rate: int = RTP_CLOCK_RATE):
        self.clock_rate = clock_rate
        self._latest_sr: Optional[RTCPSenderReport] = None
        self._lock = threading.Lock()
        self._have_sr = threading.Event()

    def update_from_session_stats(self, stats_str: str, ssrc: int) -> Optional[RTCPSenderReport]:
        """Parse RTCP SR from GStreamer session stats.

        Args:
            stats_str: GStreamer stats structure as string
            ssrc: Source SSRC identifier

        Returns:
            RTCPSenderReport if valid SR found, None otherwise
        """
        try:
            ntp_match = re.search(r"sr-ntptime=\([^)]+\)(\d+)", stats_str)
            rtp_match = re.search(r"sr-rtptime=\([^)]+\)(\d+)", stats_str)
            have_sr_match = re.search(r"have-sr=\([^)]+\)(true|false)", stats_str)

            if have_sr_match and have_sr_match.group(1) == "true" and ntp_match and rtp_match:
                ntp_val = int(ntp_match.group(1))
                rtp_val = int(rtp_match.group(1))

                if ntp_val > 0:
                    # Convert 64-bit NTP to Unix time
                    ntp_seconds = ntp_val >> 32
                    ntp_fractions = ntp_val & 0xFFFFFFFF
                    unix_time = (ntp_seconds - self.NTP_UNIX_EPOCH_DIFF) + (ntp_fractions / (2**32))

                    sr = RTCPSenderReport(
                        ssrc=ssrc,
                        ntp_timestamp=ntp_val,
                        rtp_timestamp=rtp_val,
                        unix_time=unix_time,
                        received_at_ns=time.time_ns(),
                    )

                    with self._lock:
                        self._latest_sr = sr
                        self._have_sr.set()

                    return sr
        except Exception as e:
            logger.debug(f"Failed to parse RTCP SR: {e}")
        return None

    def rtp_to_unix_ns(self, rtp_timestamp: int) -> Optional[int]:
        """Convert RTP timestamp to absolute Unix time in nanoseconds.

        Uses the most recent RTCP Sender Report to map RTP timestamps to
        absolute wall-clock time. Handles 32-bit RTP timestamp rollover.

        Args:
            rtp_timestamp: 32-bit RTP timestamp to convert

        Returns:
            Unix time in nanoseconds, or None if no SR available
        """
        with self._lock:
            if self._latest_sr is None:
                return None
            sr = self._latest_sr

        # Handle 32-bit rollover with signed arithmetic
        diff = (rtp_timestamp - sr.rtp_timestamp) & 0xFFFFFFFF
        if diff > 0x7FFFFFFF:
            diff = diff - 0x100000000

        time_diff = diff / self.clock_rate
        unix_time = sr.unix_time + time_diff
        return int(unix_time * 1_000_000_000)

    def has_sender_report(self) -> bool:
        """Check if at least one RTCP Sender Report has been received."""
        return self._have_sr.is_set()

    @property
    def latest_sr(self) -> Optional[RTCPSenderReport]:
        """Get the most recent RTCP Sender Report."""
        with self._lock:
            return self._latest_sr


class GstRTPDemuxer:
    """GStreamer H264 demuxer with ABSOLUTE RTP timestamp capture.

    For RTSP streams:
    - Captures RAW 32-bit RTP timestamps via pad probe BEFORE depayloading
    - These are the ACTUAL timestamps from the RTP packet header
    - NOT normalized like PyAV (which starts near 0 each session)
    - Timestamps persist across reconnections (monotonically increasing from source)
    - Automatically converts localhost to 127.0.0.1 to avoid IPv6 issues
    - Uses TCP by default to avoid UDP IPv6 socket issues

    For files:
    - Uses container PTS (presentation timestamp)
    - No RTP timestamps available

    Outputs H264 NAL units for external decoder (e.g., PyNvVideoCodec).

    Args:
        source: RTSP URL or file path
        use_tcp: Use TCP for RTSP transport (default: True, more reliable)
        loop: Loop file playback (default: False)
    """

    # Class-level retry configuration
    MAX_RETRIES = 5
    RETRY_DELAYS = [1, 1, 2, 3, 5, 5]  # exponential backoff per attempt (~17s total)

    @staticmethod
    def _normalize_rtsp_url(url: str) -> str:
        """Convert localhost to 127.0.0.1 to avoid IPv6 issues.

        GStreamer's rtspsrc has issues with IPv6 UDP sockets on some systems.
        Using explicit IPv4 address avoids 'Invalid address family (got 10)' errors.
        """
        if url.lower().startswith(("rtsp://", "rtsps://")):
            # Replace localhost with 127.0.0.1 (case-insensitive)
            url = re.sub(
                r"(rtsp://|rtsps://)localhost([:/])",
                r"\g<1>127.0.0.1\2",
                url,
                flags=re.IGNORECASE,
            )
            url = re.sub(
                r"(rtsp://|rtsps://)localhost$",
                r"\g<1>127.0.0.1",
                url,
                flags=re.IGNORECASE,
            )
        return url

    def __init__(self, source: str, use_tcp: bool = True, loop: bool = False, codec: str = "h264"):
        # Normalize RTSP URL to avoid IPv6 issues
        self.source = self._normalize_rtsp_url(source)
        self.use_tcp = use_tcp
        self.loop = loop
        try:
            from ..codec_detect import normalize_codec
        except ImportError:
            import importlib.util as _ilu
            import os as _os

            _cd_path = _os.path.join(
                _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                "codec_detect.py",
            )
            _cd_spec = _ilu.spec_from_file_location("codec_detect", _cd_path)
            _cd_mod = _ilu.module_from_spec(_cd_spec)
            _cd_spec.loader.exec_module(_cd_mod)
            normalize_codec = _cd_mod.normalize_codec
        self.codec = normalize_codec(codec)  # "h264" or "h265"
        self._original_source = source  # Keep original for logging

        # Detect source type
        self._is_rtsp = self.source.lower().startswith(("rtsp://", "rtsps://"))

        # GStreamer state
        self._pipeline: Optional[Gst.Pipeline] = None
        self._appsink: Optional[Gst.Element] = None
        self._depay: Optional[Gst.Element] = None
        self._rtspsrc: Optional[Gst.Element] = None
        self._mainloop: Optional[GLib.MainLoop] = None
        self._mainloop_thread: Optional[threading.Thread] = None

        # RTCP tracking (for absolute time mapping)
        self._rtcp_tracker = RTCPTracker()

        # Exact PTS -> RTP correlation, keyed by the buffer PTS that GStreamer
        # stamps on the frame's FIRST RTP packet. The depayloader propagates that
        # PTS to the access unit it emits, and h264parse/h265parse preserve it, so
        # the appsink sample carries the same PTS and that frame's TRUE RTP
        # timestamp can be recovered with no arithmetic.
        self._rtp_correlator = RtpPtsCorrelator()

        # Frame accumulator for RTP packets: the RTP timestamp and PTS of the
        # first packet of the frame currently being received.
        self._current_frame_rtp_ts: Optional[int] = None
        self._current_frame_pts: Optional[int] = None

        # Throttle for the correlation-miss warning.
        self._last_rtp_miss_warn_ns = 0

        # Stream info (populated after open)
        self._width: int = 0
        self._height: int = 0
        self._fps: float = 30.0

        # State
        self._is_open = False
        self._eof = False
        self._reconnect_pending = False
        self._error: Optional[str] = None
        self._frames_demuxed = 0
        self._session_id: str = ""
        self._session_start_ns: int = 0
        self._first_rtp_ts: Optional[int] = None

    def _create_pipeline(self) -> bool:
        """Create GStreamer pipeline for H264 extraction."""
        try:
            if self._is_rtsp:
                return self._create_rtsp_pipeline()
            return self._create_file_pipeline()
        except Exception as e:
            logger.exception(f"Error creating pipeline: {e}")
            return False

    def _create_rtsp_pipeline(self) -> bool:
        """Create RTSP pipeline with RTP timestamp capture.

        Pipeline outputs H264/H265 NAL units (not decoded frames):
        rtspsrc -> [PAD PROBE] -> rtpXXXdepay -> XXXparse -> appsink
        """
        protocol = "tcp" if self.use_tcp else "udp"
        if self.codec == "h265":
            depay = "rtph265depay"
            parse = "h265parse config-interval=-1"
            caps = "video/x-h265,stream-format=byte-stream,alignment=au"
        else:
            depay = "rtph264depay"
            parse = "h264parse config-interval=-1"
            caps = "video/x-h264,stream-format=byte-stream,alignment=au"
        # appsink max-buffers must be high enough to absorb scheduler jitter in
        # the parent reader; otherwise drop=true throws away reference frames and
        # downstream NVDEC throws "Decode Error occurred for picture N" until the
        # next IDR. Was 4; env-tunable via MATRICE_SG_APPSINK_MAX_BUFFERS.
        _max_buf = int(os.environ.get("MATRICE_SG_APPSINK_MAX_BUFFERS", "64"))
        _validate_gst_location(self.source)
        pipeline_str = f"""
            rtspsrc location={self.source} latency=0 buffer-mode=0
                protocols={protocol} do-rtcp=true name=source !
            {depay} name=depay !
            {parse} !
            {caps} !
            appsink name=sink emit-signals=false sync=false max-buffers={_max_buf} drop=true
        """

        self._pipeline = Gst.parse_launch(pipeline_str)
        if not self._pipeline:
            return False

        # Get element references
        self._rtspsrc = self._pipeline.get_by_name("source")
        self._depay = self._pipeline.get_by_name("depay")
        self._appsink = self._pipeline.get_by_name("sink")

        if not all([self._rtspsrc, self._depay, self._appsink]):
            return False

        # Setup RTP timestamp probe BEFORE depayloading (captures raw RTP header)
        self._setup_rtp_probe()

        # Setup RTCP tracking
        self._rtspsrc.connect("new-manager", self._on_new_manager)

        return True

    def _create_file_pipeline(self) -> bool:
        """Create file pipeline for local video NAL extraction.

        Pipeline outputs H264/H265 NAL units:
        filesrc -> demuxer -> XXXparse -> appsink
        """
        source_lower = self.source.lower()
        if source_lower.endswith((".mp4", ".mov")):
            demux = "qtdemux"
        elif source_lower.endswith(".mkv"):
            demux = "matroskademux"
        elif source_lower.endswith(".avi"):
            demux = "avidemux"
        elif source_lower.endswith(".ts"):
            demux = "tsdemux"
        else:
            demux = "qtdemux"

        if self.codec == "h265":
            parse = "h265parse config-interval=-1"
            caps = "video/x-h265,stream-format=byte-stream,alignment=au"
        else:
            parse = "h264parse config-interval=-1"
            caps = "video/x-h264,stream-format=byte-stream,alignment=au"

        _max_buf = int(os.environ.get("MATRICE_SG_APPSINK_MAX_BUFFERS", "64"))
        _validate_gst_location(self.source)
        pipeline_str = f"""
            filesrc location={self.source} name=source !
            {demux} name=demux !
            {parse} !
            {caps} !
            appsink name=sink emit-signals=false sync=false max-buffers={_max_buf} drop=false
        """

        self._pipeline = Gst.parse_launch(pipeline_str)
        if not self._pipeline:
            return False

        self._appsink = self._pipeline.get_by_name("sink")

        if self.loop:
            bus = self._pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect("message::eos", self._on_file_eos)

        return True

    def _on_file_eos(self, bus, message):
        """Handle EOS for file looping."""
        if self.loop and self._pipeline:
            self._pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, 0)
            return True
        return False

    def _setup_rtp_probe(self):
        """Add the probe that captures each frame's TRUE RTP timestamp.

        One probe, on the depay SINK, where raw RTP packets still carry their
        headers. It records ``buffer PTS -> RTP timestamp`` for the first packet
        of every frame; :meth:`demux` then looks up the appsink sample's PTS to
        recover that exact frame's RTP timestamp.

        There is deliberately NO probe on the depay SOURCE any more. The old
        second probe tried to establish a single session-wide
        ``first_pts -> first_rtp`` anchor and extrapolate every later timestamp
        from it, but it paired the CURRENT output buffer's PTS with
        ``_timestamp_queue[0]`` — the OLDEST completed frame. The sink probe runs
        upstream, so by the time the first output buffer was probed the queue
        already held k>=1 completed frames, and the anchor bound the wrong pair.
        Every published timestamp was then ``true_rtp - k * frame_ticks`` (the
        observed ``-2 * 6000`` at 15 fps), which broke extract-by-RTP against the
        recorder because it keys on ``rtp_timestamp`` exactly.
        """
        if self._depay:
            # Probe on depay SINK to capture raw RTP timestamps
            depay_sink = self._depay.get_static_pad("sink")
            if depay_sink:
                depay_sink.add_probe(Gst.PadProbeType.BUFFER, self._on_rtp_buffer)

    def _on_rtp_buffer(self, pad, info):
        """Record the TRUE 32-bit RTP timestamp of each frame, keyed by its PTS.

        The value is taken verbatim from the RTP header — never modified,
        normalized, offset, or extrapolated. The frame's timestamp is the one on
        its FIRST packet (all packets of a frame share it); the marker bit ends
        the frame.

        The PTS recorded alongside it is the one GStreamer stamped on that same
        first packet. The depayloader propagates it to the access unit it emits
        and h264parse/h265parse preserve it, so the appsink sample carries the
        identical value and the lookup in :meth:`demux` is exact.
        """
        buffer = info.get_buffer()

        try:
            success, rtp_buffer = GstRtp.RTPBuffer.map(buffer, Gst.MapFlags.READ)
            if success:
                # Get RAW 32-bit RTP timestamp from packet header
                rtp_ts = rtp_buffer.get_timestamp()
                marker = rtp_buffer.get_marker()
                rtp_buffer.unmap()

                # Track first RTP timestamp
                if self._first_rtp_ts is None:
                    self._first_rtp_ts = rtp_ts
                    logger.debug(f"First ABSOLUTE RTP timestamp: {rtp_ts:,}")

                # First packet of a frame owns both the RTP timestamp and the PTS
                # that the depayloader will carry to the access unit.
                if self._current_frame_rtp_ts is None:
                    self._current_frame_rtp_ts = rtp_ts
                    pts = buffer.pts
                    self._current_frame_pts = None if pts == Gst.CLOCK_TIME_NONE else pts

                # When marker bit is set, frame is complete
                if marker:
                    self._rtp_correlator.record(self._current_frame_pts, self._current_frame_rtp_ts)
                    self._current_frame_rtp_ts = None
                    self._current_frame_pts = None
        except Exception as e:
            logger.debug(f"RTP probe error: {e}")

        return Gst.PadProbeReturn.OK

    def _rtp_for_pts(self, buffer_pts: int) -> int:
        """Return the TRUE RTP timestamp for ``buffer_pts``, or 0 if unknown.

        Returns 0 rather than guessing. ``_compute_gst_timestamp_ns`` in nvdec.py
        already treats a non-positive RTP timestamp as "no timestamp from the
        camera" (rate-limited warning, ``capture_timestamp_ns=0``), so a
        correlation miss costs one frame's timestamp and never publishes a wrong
        one. Misses are warned about periodically because a systematic mismatch is
        a real defect that would otherwise be silent.
        """
        rtp_ts = self._rtp_correlator.lookup(buffer_pts)
        if rtp_ts:
            return rtp_ts

        now = time.monotonic_ns()
        if now - self._last_rtp_miss_warn_ns > _RTP_MISS_WARN_INTERVAL_NS:
            self._last_rtp_miss_warn_ns = now
            hits, misses = self._rtp_correlator.stats
            logger.warning(
                "RTP correlation miss for PTS=%s (%d/%d frames, %.1f%%): publishing "
                "rtp_timestamp=0 for this frame rather than a synthesized value. A "
                "sustained rate here means appsink PTS does not match the depay-sink "
                "PTS on this GStreamer build.",
                buffer_pts,
                misses,
                hits + misses,
                100.0 * self._rtp_correlator.miss_ratio,
            )
        return 0

    @property
    def rtp_correlation_stats(self) -> Tuple[int, int]:
        """``(hits, misses)`` for PTS -> RTP correlation. Diagnostics only."""
        return self._rtp_correlator.stats

    def _on_new_manager(self, rtspsrc, manager):
        """Setup RTCP tracking when rtpbin manager is created."""
        try:
            manager.connect("on-sender-ssrc-active", self._on_sender_ssrc_active)
        except Exception as e:
            logger.debug(f"Failed to connect RTCP handler: {e}")

    def _on_sender_ssrc_active(self, manager, session, ssrc):
        """Called when RTCP SR is received."""
        try:
            internal_session = manager.emit("get-internal-session", session)
            if internal_session:
                stats = internal_session.get_property("stats")
                if stats:
                    source_stats = stats.get_value("source-stats")
                    if source_stats:
                        for i in range(len(source_stats)):
                            sr = self._rtcp_tracker.update_from_session_stats(str(source_stats[i]), ssrc)
                            if sr:
                                logger.debug(f"RTCP SR: RTP {sr.rtp_timestamp} -> Unix {sr.unix_time:.3f}")
        except Exception as e:
            logger.debug(f"RTCP handler error: {e}")

    def _on_bus_message(self, bus, message):
        """Handle GStreamer bus messages."""
        if message.type == Gst.MessageType.ERROR:
            err, _ = message.parse_error()
            self._error = err.message
            logger.error(f"Pipeline error: {err.message}")
            if self._mainloop:
                self._mainloop.quit()
        elif message.type == Gst.MessageType.EOS:
            if self._is_rtsp:
                # RTSP EOS = simulation video looped. Reconnect pipeline
                # in-place instead of exiting demux(). This avoids
                # subprocess churn at scale (1000 cameras).
                logger.debug("RTSP EOS — reconnecting pipeline")
                self._reconnect_pending = True
            else:
                self._eof = True
                logger.debug("Pipeline EOS")
                if self._mainloop:
                    self._mainloop.quit()
        return True

    def _run_mainloop(self):
        """Run GLib mainloop in separate thread."""
        self._mainloop = GLib.MainLoop()
        try:
            self._mainloop.run()
        except Exception as e:
            logger.debug(f"Mainloop error: {e}")

    def _cleanup_pipeline(self):
        """Clean up pipeline resources for retry."""
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
        if self._mainloop:
            self._mainloop.quit()
        self._pipeline = None
        self._appsink = None
        self._depay = None
        self._rtspsrc = None
        self._mainloop = None
        self._mainloop_thread = None
        self._error = None
        self._width = 0
        self._height = 0

    def _try_open(self) -> bool:
        """Attempt to open the pipeline. Returns True on success."""
        self._eof = False
        self._error = None

        if not self._create_pipeline():
            return False

        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._on_bus_message)

        ret = self._pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            return False

        self._mainloop_thread = threading.Thread(target=self._run_mainloop, daemon=True)
        self._mainloop_thread.start()

        # Wait for first sample to get stream info
        timeout = 5.0
        start = time.perf_counter()
        while self._width == 0 and time.perf_counter() - start < timeout:
            if self._error:
                return False

            sample = self._appsink.emit("try-pull-sample", int(0.1 * Gst.SECOND))
            if sample:
                caps = sample.get_caps()
                if caps:
                    struct = caps.get_structure(0)
                    _, self._width = struct.get_int("width")
                    _, self._height = struct.get_int("height")
                    fps_ok, fps_num, fps_den = struct.get_fraction("framerate")
                    if fps_ok and fps_den > 0:
                        self._fps = fps_num / fps_den
                break

        return self._width > 0

    def open(self, quiet: bool = False) -> "GstRTPDemuxer":
        """Open source and initialize demuxer pipeline with retry logic.

        For RTSP streams, automatically retries with TCP if UDP fails,
        and converts localhost to 127.0.0.1 to avoid IPv6 issues.

        Args:
            quiet: Suppress info logging

        Returns:
            self (for chaining)

        Raises:
            RuntimeError: If pipeline creation fails after all retries
        """
        self._session_start_ns = time.time_ns()
        self._session_id = str(uuid.uuid4())[:8]
        last_error = None

        # Try with current settings first
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                if self._try_open():
                    break  # Success!

                # Failed - prepare for retry
                last_error = self._error or "Failed to get video dimensions (0x0 resolution)"
                self._cleanup_pipeline()

                if attempt < self.MAX_RETRIES:
                    # On first retry, try switching to TCP if using UDP
                    if attempt == 0 and not self.use_tcp and self._is_rtsp:
                        logger.warning(f"Retry {attempt + 1}: Switching to TCP transport...")
                        self.use_tcp = True
                    else:
                        logger.warning(f"Retry {attempt + 1}: Retrying connection...")

                    delay = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS) - 1)]
                    time.sleep(delay)

            except Exception as e:
                last_error = str(e)
                self._cleanup_pipeline()
                if attempt < self.MAX_RETRIES:
                    delay = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS) - 1)]
                    time.sleep(delay)

        if self._width == 0:
            raise RuntimeError(f"Failed to open source after {self.MAX_RETRIES + 1} attempts: {last_error}")

        self._is_open = True

        if not quiet:
            src_type = "RTSP" if self._is_rtsp else "File"
            logger.info(f"GstRTPDemuxer ({src_type}): {self._width}x{self._height} @ {self._fps:.1f} FPS")
            if self._is_rtsp and self._first_rtp_ts:
                logger.info(f"First ABSOLUTE RTP timestamp: {self._first_rtp_ts:,}")

        return self

    def _reconnect_rtsp(self) -> bool:
        """Reconnect RTSP pipeline in-place after EOS.

        Tears down the current pipeline and creates a fresh one without
        destroying the process. Returns True on success.
        """
        try:
            self._cleanup_pipeline()
            time.sleep(0.3)  # Brief pause for RTSP server

            # Reset RTP tracking state for new session. The correlation map MUST
            # be cleared: the new session restarts GStreamer's PTS clock, so a
            # stale PTS key could collide with a fresh one and hand a frame the
            # previous session's RTP timestamp.
            self._first_rtp_ts = None
            self._current_frame_rtp_ts = None
            self._current_frame_pts = None
            self._rtp_correlator.clear()
            self._rtcp_tracker = RTCPTracker()
            self._eof = False
            self._reconnect_pending = False
            self._error = None

            # New session
            self._session_id = str(uuid.uuid4())[:8]
            self._session_start_ns = time.time_ns()

            if self._try_open():
                self._is_open = True
                logger.debug(f"RTSP reconnected: {self._width}x{self._height}, session={self._session_id}")
                return True
            logger.warning("RTSP reconnect failed")
            self._eof = True
            return False
        except Exception as e:
            logger.warning(f"RTSP reconnect error: {e}")
            self._eof = True
            return False

    def demux(self) -> Iterator[Tuple[bytes, int, int, Optional[int]]]:
        """Demux H264/H265 NAL units with timestamps.

        Yields:
            (nal_bytes, timestamp, timestamp_ns, absolute_time_ns)

            For RTSP:
            - nal_bytes: H264/H265 NAL unit as bytes
            - timestamp: RAW 32-bit RTP timestamp (ABSOLUTE, NOT normalized)
            - timestamp_ns: RTP timestamp converted to nanoseconds (at 90kHz)
            - absolute_time_ns: Unix time if RTCP SR available, None otherwise

            For files:
            - nal_bytes: H264/H265 NAL unit as bytes
            - timestamp: Container PTS
            - timestamp_ns: PTS in nanoseconds
            - absolute_time_ns: None
        """
        if not self._is_open:
            self.open()

        frame_counter = 0

        while not self._eof:
            if self._error:
                logger.warning(f"Demux stopping due to error: {self._error}")
                break

            # Handle RTSP reconnect (set by EOS handler)
            if self._reconnect_pending:
                if not self._reconnect_rtsp():
                    break
                continue  # Re-enter loop with fresh pipeline

            sample = self._appsink.emit("try-pull-sample", int(0.1 * Gst.SECOND))
            if sample is None:
                continue

            buffer = sample.get_buffer()
            caps = sample.get_caps()

            # Update dimensions if needed
            if self._width == 0 and caps:
                struct = caps.get_structure(0)
                _, self._width = struct.get_int("width")
                _, self._height = struct.get_int("height")

            # Get timestamp based on source type
            if self._is_rtsp:
                # This frame's OWN RTP timestamp, taken verbatim from its RTP
                # header via the exact PTS correlation, or 0 when unknown.
                # Nothing is synthesized, offset, or extrapolated — downstream
                # extract-by-RTP keys on this value exactly, so a value that is
                # merely close is worse than none.
                #
                # Keyed on PTS rather than FIFO-popped deliberately: the appsink
                # is configured `drop=true`, so a dropped sample would shift a
                # FIFO queue permanently and turn a bounded error into unbounded
                # drift. A PTS lookup is immune to drops.
                rtp_ts = self._rtp_for_pts(buffer.pts)

                timestamp = rtp_ts
                timestamp_ns = rtp_ts * 1_000_000_000 // RTP_CLOCK_RATE
                absolute_time_ns = self._rtcp_tracker.rtp_to_unix_ns(rtp_ts)
            else:
                # File: use buffer PTS
                pts = buffer.pts if buffer.pts != Gst.CLOCK_TIME_NONE else frame_counter * 1_000_000_000 // 30
                timestamp = pts
                timestamp_ns = pts
                absolute_time_ns = None

            # Map buffer and extract NAL bytes
            success, map_info = buffer.map(Gst.MapFlags.READ)
            if not success:
                continue

            try:
                # Extract NAL unit as bytes
                nal_bytes = bytes(map_info.data)

                self._frames_demuxed += 1
                frame_counter += 1
                yield (nal_bytes, timestamp, timestamp_ns, absolute_time_ns)

            finally:
                buffer.unmap(map_info)

    def close(self):
        """Close demuxer and release resources."""
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
        if self._mainloop:
            self._mainloop.quit()
        self._pipeline = None
        self._is_open = False
        logger.debug(f"GstRTPDemuxer closed, demuxed {self._frames_demuxed} frames")

    # Properties
    @property
    def width(self) -> int:
        """Video frame width."""
        return self._width

    @property
    def height(self) -> int:
        """Video frame height."""
        return self._height

    @property
    def fps(self) -> float:
        """Video frame rate."""
        return self._fps

    @property
    def session_id(self) -> str:
        """Unique session identifier."""
        return self._session_id

    @property
    def session_start_ns(self) -> int:
        """Session start time in nanoseconds."""
        return self._session_start_ns

    @property
    def first_rtp_timestamp(self) -> Optional[int]:
        """First ABSOLUTE RTP timestamp captured (RTSP only)."""
        return self._first_rtp_ts

    @property
    def has_rtcp_sr(self) -> bool:
        """Whether RTCP Sender Report is available for absolute time mapping."""
        return self._rtcp_tracker.has_sender_report()

    @property
    def latest_rtcp_sr(self) -> Optional[RTCPSenderReport]:
        """Most recent RTCP Sender Report."""
        return self._rtcp_tracker.latest_sr

    @property
    def frames_demuxed(self) -> int:
        """Number of frames demuxed in this session."""
        return self._frames_demuxed

    @property
    def is_rtsp(self) -> bool:
        """Whether source is RTSP stream."""
        return self._is_rtsp

    @property
    def is_eof(self) -> bool:
        """Whether end-of-stream has been reached."""
        return self._eof


if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="GStreamer RTP Demuxer with ABSOLUTE Timestamps")
    parser.add_argument("source", nargs="?", help="RTSP URL or file path")
    parser.add_argument("--duration", type=float, default=5.0, help="Test duration in seconds")
    parser.add_argument("--max-frames", type=int, default=100, help="Max frames to demux (file only)")
    args = parser.parse_args()

    if not args.source:
        print("Usage: python gstreamer_rtp_demuxer.py <rtsp://url | /path/to/video.mp4>")
        print("\nExample (RTSP with ABSOLUTE RTP timestamps):")
        print("  python gstreamer_rtp_demuxer.py rtsp://camera/stream --duration 10")
        print("\nExample (file):")
        print("  python gstreamer_rtp_demuxer.py /path/to/video.mp4 --max-frames 50")
        sys.exit(1)

    demuxer = GstRTPDemuxer(args.source)
    demuxer.open()

    is_rtsp = demuxer.is_rtsp
    print(f"\n{'RTSP' if is_rtsp else 'File'}: {args.source}")
    print(f"Resolution: {demuxer.width}x{demuxer.height} @ {demuxer.fps:.1f} FPS")
    if is_rtsp and demuxer.first_rtp_timestamp:
        print(f"First ABSOLUTE RTP timestamp: {demuxer.first_rtp_timestamp:,}")
    print()

    if is_rtsp:
        print(f"{'#':>4} {'ABSOLUTE RTP':>18} {'RTP (ms)':>12} {'H264 size':>12}")
    else:
        print(f"{'#':>4} {'PTS':>15} {'PTS (ms)':>12} {'H264 size':>12}")
    print("-" * 60)

    frames = 0
    start = time.perf_counter()

    for nal_bytes, ts, ts_ns, absolute_ns in demuxer.demux():
        frames += 1

        if frames <= 10:
            ts_ms = ts_ns / 1_000_000
            size_kb = len(nal_bytes) / 1024
            if is_rtsp:
                print(f"{frames:4} {ts:18,} {ts_ms:12.1f} {size_kb:10.1f} KB")
            else:
                print(f"{frames:4} {ts:15} {ts_ms:12.1f} {size_kb:10.1f} KB")

        # Check stop condition
        if is_rtsp:
            if time.perf_counter() - start >= args.duration:
                break
        else:
            if frames >= args.max_frames:
                break

    elapsed = time.perf_counter() - start
    fps = frames / elapsed if elapsed > 0 else 0

    print("-" * 60)
    print(f"Demuxed {frames} frames in {elapsed:.2f}s = {fps:.1f} FPS")
    if is_rtsp:
        print(f"RTCP Sender Report available: {demuxer.has_rtcp_sr}")

    demuxer.close()
