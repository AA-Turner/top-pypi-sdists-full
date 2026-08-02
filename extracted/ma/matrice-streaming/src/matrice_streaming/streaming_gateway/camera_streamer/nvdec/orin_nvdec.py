#!/usr/bin/env python3
"""Orin NVDEC Decoder Pool - GStreamer subprocess decode for Jetson Orin.

On Jetson Orin, the desktop CUVID API (cuvidGetDecoderCaps, cuvidCreateDecoder, etc.)
does NOT exist. PyNvVideoCodec fails with "Could not load function cuvidGetDecoderCaps".

Additionally, GStreamer Python bindings have plugin loading issues in
multiprocessing.spawn() worker processes (avdec_h264 and other libav plugins
fail to load in the spawned worker's GStreamer registry).

This module provides OrinNVDECDecoderPool as a drop-in replacement for
NVDECDecoderPool. Each camera gets its own Python GStreamer subprocess that
decodes to NV12 and extracts RTP timestamps via pad probes on rtph264depay.

Activated by: MATRICE_PLATFORM=orin environment variable.

Pipeline per camera (subprocess):
    rtspsrc -> [pad probe] -> rtph264depay -> h264parse -> avdec_h264
    -> videoconvert -> videoscale -> video/x-raw,NV12,640x640 -> appsink

NV12 frames + RTP timestamps are sent to the parent via a length-prefixed
wire protocol over stdout.

On Orin unified memory, CPU decode is efficient since CPU and GPU share DRAM.
"""

from __future__ import annotations

import json
import logging
import math
import os
import select
import signal
import struct
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

try:
    import cupy as cp

    CUPY_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore[assignment]
    CUPY_AVAILABLE = False

TARGET_WIDTH = 640
TARGET_HEIGHT = 640
NV12_HEIGHT = 960  # 640 * 1.5 for NV12
FRAME_SIZE = TARGET_WIDTH * NV12_HEIGHT  # 614,400 bytes

# RTP clock rate (90 kHz standard for H.264)
RTP_CLOCK_RATE = 90000

DEFAULT_SOURCE_FPS = 30.0


def _normalize_reported_fps(fps: float) -> float:
    """Clamp reported FPS so timestamp and FPS-limit math never divide by zero."""
    try:
        x = float(fps)
    except (TypeError, ValueError):
        return DEFAULT_SOURCE_FPS
    if x <= 0 or math.isnan(x):  # NaN
        return DEFAULT_SOURCE_FPS
    return x


# =============================================================================
# Child subprocess script - runs GStreamer with pad probes for RTP timestamps
# =============================================================================
_ORIN_CHILD_SCRIPT = r'''
"""Orin GStreamer child process: decode + RTP timestamp extraction.

Builds a GStreamer pipeline with appsink and pad probes on rtph264depay
to capture raw 32-bit RTP timestamps. Sends NV12 frames + RTP metadata
to parent via length-prefixed wire protocol on stdout.

Usage: python3 <script> <video_path> <width> <height> [--file]
"""
import json
import os
import re
import struct
import sys
import threading
import time
from collections import OrderedDict

# --- Wire protocol helpers (same as gstreamer_subprocess_demuxer.py) ---

def write_msg(data: bytes):
    sys.stdout.buffer.write(struct.pack(">I", len(data)))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

def write_json(obj):
    write_msg(json.dumps(obj).encode())

# --- GStreamer setup ---

def main():
    video_path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    is_file = "--file" in sys.argv
    # Parse codec from --codec=h265 argument (default h264)
    codec = "h264"
    for arg in sys.argv:
        if arg.startswith("--codec="):
            codec = arg.split("=", 1)[1].lower()

    # Redirect GStreamer debug output to stderr (keep stdout clean for wire protocol)
    os.environ.setdefault("GST_DEBUG", "1")

    import gi
    gi.require_version('Gst', '1.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gst, GLib

    Gst.init(None)

    # Try to import GstRtp for RTP timestamp extraction
    HAS_GST_RTP = False
    GstRtp = None
    try:
        gi.require_version('GstRtp', '1.0')
        from gi.repository import GstRtp as _GstRtp
        GstRtp = _GstRtp
        HAS_GST_RTP = True
    except (ValueError, ImportError):
        print("[orin-child] GstRtp not available, RTP timestamps disabled", file=sys.stderr, flush=True)

    # --- Shared state between probe callback and main loop ---
    current_frame_rtp_ts = [None]  # mutable container for closure
    first_rtp_ts = [None]
    pipeline_error = [None]
    pipeline_eof = [False]

    # Exact PTS -> RTP correlation. Mirrors camera_streamer/rtp_correlation.py
    # (RtpPtsCorrelator); inlined because this child runs as a bare temp script
    # with no package on sys.path. Keep the two in step.
    #
    # This REPLACES a session-anchor + extrapolation scheme that paired one
    # frame's PTS with a different frame's RTP timestamp (peeking rtp_deque[0],
    # the oldest completed frame, while the PTS belonged to frame k). Every
    # published value was then true_rtp - k*frame_ticks. Downstream
    # extract-by-RTP keys on rtp_timestamp exactly, so a constant offset returns
    # the wrong stored frame.
    #
    # Keyed on PTS, not FIFO-popped: appsink runs drop=true, and a dropped
    # sample would shift a FIFO queue permanently.
    PTS_RTP_MAP_MAX = 256
    pts_to_rtp = OrderedDict()
    pts_to_rtp_lock = threading.Lock()
    current_frame_pts = [None]
    rtp_hits = [0]
    rtp_misses = [0]

    # RTCP Sender Report tracking for absolute time
    NTP_UNIX_EPOCH_DIFF = 2208988800
    latest_sr_rtp = [None]     # RTP timestamp from most recent SR
    latest_sr_unix = [None]    # Unix time (float seconds) from most recent SR
    sr_lock = threading.Lock()

    def on_rtp_buffer(pad, info):
        """Pad probe on depay sink - record each frame's TRUE RTP timestamp.

        The value is taken verbatim from the RTP header. The frame's timestamp and
        correlation key both come from its FIRST packet: all packets of a frame
        share the RTP timestamp, and the depayloader propagates that packet's PTS
        to the access unit it emits (h26Xparse preserves it), so the appsink
        sample carries the identical PTS.
        """
        buf = info.get_buffer()
        try:
            success, rtp_buf = GstRtp.RTPBuffer.map(buf, Gst.MapFlags.READ)
            if success:
                rtp_ts = rtp_buf.get_timestamp()
                marker = rtp_buf.get_marker()
                rtp_buf.unmap()

                if first_rtp_ts[0] is None:
                    first_rtp_ts[0] = rtp_ts

                if current_frame_rtp_ts[0] is None:
                    current_frame_rtp_ts[0] = rtp_ts
                    pts = buf.pts
                    current_frame_pts[0] = None if pts == Gst.CLOCK_TIME_NONE else pts

                if marker:
                    if current_frame_pts[0] is not None:
                        with pts_to_rtp_lock:
                            pts_to_rtp[current_frame_pts[0]] = current_frame_rtp_ts[0]
                            pts_to_rtp.move_to_end(current_frame_pts[0])
                            while len(pts_to_rtp) > PTS_RTP_MAP_MAX:
                                pts_to_rtp.popitem(last=False)
                    current_frame_rtp_ts[0] = None
                    current_frame_pts[0] = None
        except Exception:
            pass
        return Gst.PadProbeReturn.OK

    def rtp_for_pts(buffer_pts):
        """Return this frame's TRUE RTP timestamp, or 0 if unknown.

        Never approximates: 0 is the established "no timestamp" signal that the
        parent already handles, so a miss costs one frame's timestamp instead of
        publishing a wrong one.
        """
        rtp_ts = None
        if buffer_pts != Gst.CLOCK_TIME_NONE:
            with pts_to_rtp_lock:
                rtp_ts = pts_to_rtp.pop(buffer_pts, None)
        if rtp_ts is None:
            rtp_misses[0] += 1
            if rtp_misses[0] in (1, 10, 100) or rtp_misses[0] % 1000 == 0:
                print(f"[orin-child] RTP correlation miss for PTS={buffer_pts} "
                      f"({rtp_misses[0]} misses / {rtp_hits[0]} hits); publishing "
                      f"rtp_ts=0 rather than a synthesized value",
                      file=sys.stderr, flush=True)
            return 0
        rtp_hits[0] += 1
        return rtp_ts

    # --- RTCP Sender Report tracking ---

    def parse_rtcp_sr(stats_str, ssrc):
        """Parse RTCP Sender Report from GStreamer session stats."""
        ntp_match = re.search(r'sr-ntptime=\([^)]+\)(\d+)', stats_str)
        rtp_match = re.search(r'sr-rtptime=\([^)]+\)(\d+)', stats_str)
        have_sr_match = re.search(r'have-sr=\([^)]+\)(true|false)', stats_str)

        if (have_sr_match and have_sr_match.group(1) == 'true'
                and ntp_match and rtp_match):
            ntp_val = int(ntp_match.group(1))
            rtp_val = int(rtp_match.group(1))
            if ntp_val > 0:
                ntp_seconds = ntp_val >> 32
                ntp_fractions = ntp_val & 0xFFFFFFFF
                unix_time = ((ntp_seconds - NTP_UNIX_EPOCH_DIFF)
                             + ntp_fractions / (2**32))
                with sr_lock:
                    latest_sr_rtp[0] = rtp_val
                    latest_sr_unix[0] = unix_time
                print(f"[orin-child] RTCP SR: RTP {rtp_val} -> Unix {unix_time:.3f}",
                      file=sys.stderr, flush=True)
                return True
        return False

    def rtp_to_unix_ns(rtp_timestamp):
        """Convert RTP timestamp to absolute Unix nanoseconds using latest SR."""
        with sr_lock:
            if latest_sr_rtp[0] is None:
                return None
            sr_rtp = latest_sr_rtp[0]
            sr_unix = latest_sr_unix[0]

        diff = (rtp_timestamp - sr_rtp) & 0xFFFFFFFF
        if diff > 0x7FFFFFFF:
            diff = diff - 0x100000000
        unix_time = sr_unix + diff / 90000
        return int(unix_time * 1_000_000_000)

    def on_new_manager(rtspsrc_elem, manager):
        """Connect to rtpbin manager for RTCP SR notifications."""
        try:
            manager.connect("on-sender-ssrc-active", on_sender_ssrc_active)
            print("[orin-child] Connected RTCP SR handler", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"[orin-child] Failed to connect RTCP handler: {e}",
                  file=sys.stderr, flush=True)

    def on_sender_ssrc_active(manager, session, ssrc):
        """Called when RTCP SR is received from the sender."""
        try:
            internal_session = manager.emit("get-internal-session", session)
            if internal_session:
                stats = internal_session.get_property("stats")
                if stats:
                    source_stats = stats.get_value("source-stats")
                    if source_stats:
                        for i in range(len(source_stats)):
                            parse_rtcp_sr(str(source_stats[i]), ssrc)
        except Exception as e:
            print(f"[orin-child] RTCP handler error: {e}",
                  file=sys.stderr, flush=True)

    # --- Build pipeline ---
    # Gst.parse_launch parses the whole string as pipeline grammar, so reject a
    # backend-supplied video_path containing whitespace or '!' (element
    # separator) before interpolating it — otherwise it could inject/reconfigure
    # pipeline elements. Mirrors gstreamer_rtp_demuxer._validate_gst_location.
    if (
        not isinstance(video_path, str)
        or not video_path
        or any(c.isspace() for c in video_path)
        or "!" in video_path
        or any(ord(c) < 0x20 for c in video_path)
    ):
        write_json({"type": "error", "msg": "Unsafe pipeline source rejected"})
        sys.exit(1)
    # Use videoscale add-borders=true to preserve aspect ratio and pad to target
    # size. Padding color is set to gray (114) to match ultralytics LetterBox.
    # border-value encodes ARGB as a uint: 0xFF727272 = (255, 114, 114, 114)
    letterbox_scale = (
        f"videoconvert ! videoscale add-borders=true border-value=4285558642 ! "
        f"video/x-raw,format=NV12,width={width},height={height},pixel-aspect-ratio=1/1"
    )
    if is_file:
        # decodebin auto-detects codec for files
        pipeline_str = (
            f"filesrc location={video_path} ! decodebin ! "
            f"{letterbox_scale} ! "
            f"appsink name=sink emit-signals=false sync=false max-buffers=4 drop=false"
        )
    else:
        # Codec-specific RTSP pipeline elements
        if codec == "h265":
            depay_parse_decode = "rtph265depay name=depay ! h265parse config-interval=-1 ! avdec_h265"
        else:
            depay_parse_decode = "rtph264depay name=depay ! h264parse config-interval=-1 ! avdec_h264"
        pipeline_str = (
            f"rtspsrc location={video_path} latency=0 buffer-mode=0 "
            f"protocols=tcp do-rtcp=true name=source ! "
            f"{depay_parse_decode} ! "
            f"{letterbox_scale} ! "
            f"appsink name=sink emit-signals=false sync=false max-buffers=4 drop=true"
        )

    pipeline = Gst.parse_launch(pipeline_str)
    if not pipeline:
        write_json({"type": "error", "msg": "Failed to create pipeline"})
        sys.exit(1)

    appsink = pipeline.get_by_name("sink")
    if not appsink:
        write_json({"type": "error", "msg": "appsink not found in pipeline"})
        sys.exit(1)

    # Add RTP pad probes and RTCP tracking if available and RTSP source
    if HAS_GST_RTP and not is_file:
        depay = pipeline.get_by_name("depay")
        if depay:
            # Probe on depay SINK: capture raw RTP timestamps. There is
            # deliberately NO depay-SOURCE probe — it existed only to build the
            # mis-paired session anchor described above.
            depay_sink = depay.get_static_pad("sink")
            if depay_sink:
                depay_sink.add_probe(Gst.PadProbeType.BUFFER, on_rtp_buffer)

        # Connect RTCP SR tracking on rtspsrc
        source = pipeline.get_by_name("source")
        if source:
            source.connect("new-manager", on_new_manager)

    # --- Bus message handling ---
    def on_bus_message(bus, message):
        if message.type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            pipeline_error[0] = err.message
            print(f"[orin-child] Pipeline error: {err.message}", file=sys.stderr, flush=True)
            if mainloop[0]:
                mainloop[0].quit()
        elif message.type == Gst.MessageType.EOS:
            pipeline_eof[0] = True
            if mainloop[0]:
                mainloop[0].quit()
        return True

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_bus_message)

    # --- SIGTERM handler: drive the pipeline to NULL before exit so the GPU
    # driver releases NVDEC dmabufs proactively. Without this, parent's
    # SIGTERM->SIGKILL escalation kills the process mid-mainloop and the
    # buffer-backed inode references stay reclaimable-but-held in the kernel
    # until drop_caches=2 runs (the Jetson-Thor leak class).
    import signal as _signal_mod
    _shutdown_done = [False]
    def _graceful_shutdown(_signum=None, _frame=None):
        if _shutdown_done[0]:
            return
        _shutdown_done[0] = True
        try:
            pipeline.set_state(Gst.State.NULL)
        except Exception:
            pass
        try:
            if mainloop[0] is not None:
                mainloop[0].quit()
        except Exception:
            pass
        sys.exit(0)
    try:
        _signal_mod.signal(_signal_mod.SIGTERM, _graceful_shutdown)
        _signal_mod.signal(_signal_mod.SIGINT, _graceful_shutdown)
    except (OSError, ValueError):
        pass

    # --- Start pipeline ---
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        write_json({"type": "error", "msg": "Failed to set pipeline to PLAYING"})
        sys.exit(1)

    mainloop = [None]
    def run_mainloop():
        mainloop[0] = GLib.MainLoop()
        try:
            mainloop[0].run()
        except Exception:
            pass

    ml_thread = threading.Thread(target=run_mainloop, daemon=True)
    ml_thread.start()

    # --- Wait for first sample to get stream info ---
    fps = 30.0
    actual_width = width
    actual_height = height
    first_sample = appsink.emit("try-pull-sample", int(5 * Gst.SECOND))

    if first_sample is None:
        err_msg = pipeline_error[0] or "Timeout waiting for first frame"
        write_json({"type": "error", "msg": err_msg})
        pipeline.set_state(Gst.State.NULL)
        sys.exit(1)

    caps = first_sample.get_caps()
    if caps:
        s = caps.get_structure(0)
        _, actual_width = s.get_int("width")
        _, actual_height = s.get_int("height")
        fps_ok, fps_num, fps_den = s.get_fraction("framerate")
        if fps_ok and fps_den > 0:
            fps = fps_num / fps_den

    # --- Send meta ---
    write_json({
        "type": "meta",
        "width": actual_width,
        "height": actual_height,
        "fps": fps,
    })

    # --- Process first sample ---
    def process_sample(sample):
        buf = sample.get_buffer()
        buffer_pts = buf.pts  # Capture PTS before unmap
        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return
        nv12_bytes = bytes(map_info.data)
        buf.unmap(map_info)

        # This frame's OWN RTP timestamp, verbatim from its RTP header, or 0.
        # Nothing is synthesized, offset, or extrapolated.
        rtp_ts = rtp_for_pts(buffer_pts)

        # Compute derived timestamps
        rtp_ns = rtp_ts * 1_000_000_000 // 90000 if rtp_ts else 0
        abs_ns = rtp_to_unix_ns(rtp_ts) if rtp_ts else None

        write_json({
            "type": "frame",
            "rtp_ts": rtp_ts,
            "rtp_ns": rtp_ns,
            "abs_ns": abs_ns,
            "size": len(nv12_bytes),
        })
        write_msg(nv12_bytes)

    process_sample(first_sample)

    # --- Main loop: pull samples and send ---
    while not pipeline_eof[0] and pipeline_error[0] is None:
        sample = appsink.emit("try-pull-sample", int(0.1 * Gst.SECOND))
        if sample is None:
            if pipeline_eof[0] or pipeline_error[0]:
                break
            continue
        process_sample(sample)

    # --- Cleanup ---
    if pipeline_error[0]:
        write_json({"type": "error", "msg": pipeline_error[0]})
    else:
        write_json({"type": "eof"})

    pipeline.set_state(Gst.State.NULL)
    if mainloop[0]:
        mainloop[0].quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        try:
            import json as _json, struct as _struct
            data = _json.dumps({"type": "error", "msg": str(e)}).encode()
            sys.stdout.buffer.write(_struct.pack(">I", len(data)))
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except Exception:
            pass
        sys.exit(1)
'''


@dataclass
class OrinStreamState:
    """State for a Python GStreamer subprocess camera stream."""

    stream_id: int
    camera_id: str
    video_path: str
    width: int = TARGET_WIDTH
    height: int = TARGET_HEIGHT
    stream_type: str = "rtsp"
    codec: str = "h264"  # "h264" or "h265"
    process: Any = None  # subprocess.Popen
    source_fps: float = 30.0
    frames_decoded: int = 0
    session_id: str = ""
    session_start_ns: int = 0
    errors: int = 0
    transient_errors: int = 0  # short reads, unexpected msg types (reset on success)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    first_rtp_ts: Optional[int] = None
    last_rtp_ts: Optional[int] = None
    _last_rtp_warn: float = 0.0  # throttle for missing-RTP warnings
    _rtcp_logged: bool = False


class OrinNVDECDecoderPool:
    """Orin-compatible NVDEC decoder pool using Python GStreamer subprocesses.

    Drop-in replacement for NVDECDecoderPool on Jetson Orin where CUVID API
    is not available. Uses a Python subprocess per camera with GStreamer
    pipeline + pad probes for RTP timestamp extraction.

    API matches NVDECDecoderPool exactly:
        - assign_stream(stream_id, camera_id, video_path, ...)
        - decode_round(decoder_idx, frames_per_stream) -> (total, [(cam, tensor, ts, ...)])
        - get_camera_ids_for_decoder(decoder_idx)
        - get_source_fps_for_decoder(decoder_idx)
        - release()
    """

    def __init__(
        self,
        pool_size: int,
        gpu_id: int = 0,
        demuxer_type: str = "gstreamer",
        codec: str = "h264",
    ):
        from ..codec_detect import normalize_codec

        self.pool_size = pool_size
        self.gpu_id = gpu_id
        self.codec = normalize_codec(codec)
        self.demuxer_type = demuxer_type
        self.decoders = [None] * pool_size  # Placeholder for API compat
        self.actual_pool_size = pool_size
        self.streams_per_decoder: List[List[OrinStreamState]] = [[] for _ in range(pool_size)]
        self._all_streams: Dict[str, OrinStreamState] = {}
        self._frame_size = FRAME_SIZE
        self._script_written = False
        self._child_script_path: Optional[str] = None

        if CUPY_AVAILABLE and cp is not None:
            cp.cuda.Device(gpu_id).use()

        logger.info(
            f"[Orin] Created subprocess NVDEC pool: {pool_size} slots on GPU {gpu_id}, "
            f"frame_size={self._frame_size} bytes"
        )

    def _ensure_child_script(self) -> str:
        """Write child script into a private, owner-only temp directory.

        Uses ``tempfile.mkdtemp`` (mode 0700, unpredictable name) instead of a
        fixed world-writable ``/tmp`` path so a hostile local user cannot
        pre-create / symlink the file and hijack the code the pool subprocess
        executes.
        """
        if not self._script_written or not self._child_script_path:
            script_dir = tempfile.mkdtemp(prefix="orin_gst_")
            script_path = os.path.join(script_dir, "_orin_gst_child.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(_ORIN_CHILD_SCRIPT)
            self._child_script_path = script_path
            self._script_written = True
        return self._child_script_path

    # --- Wire protocol readers ---

    @staticmethod
    def _read_exact(proc, n: int, timeout: float = 5.0) -> bytes:
        """Read exactly n bytes from subprocess stdout, with select() timeout.

        Raises:
            EOFError: pipe closed
            TimeoutError: no data within timeout
        """
        buf = b""
        while len(buf) < n:
            ready, _, _ = select.select([proc.stdout], [], [], timeout)
            if not ready:
                raise TimeoutError(f"No data from subprocess within {timeout}s (read {len(buf)}/{n} bytes)")
            chunk = proc.stdout.read(n - len(buf))
            if not chunk:
                raise EOFError("Subprocess pipe closed")
            buf += chunk
        return buf

    @staticmethod
    def _read_msg(proc) -> bytes:
        """Read a length-prefixed message from subprocess stdout."""
        header = OrinNVDECDecoderPool._read_exact(proc, 4)
        length = struct.unpack(">I", header)[0]
        return OrinNVDECDecoderPool._read_exact(proc, length)

    @staticmethod
    def _read_json(proc) -> dict:
        """Read a JSON message from subprocess."""
        data = OrinNVDECDecoderPool._read_msg(proc)
        return json.loads(data)

    # Retry configuration for subprocess startup
    _PIPELINE_RETRY_DELAYS = [1, 2, 3, 5, 5]  # ~16s total window

    def _start_pipeline(self, stream: OrinStreamState) -> bool:
        """Start Python GStreamer subprocess for a stream.

        Retries up to 5 times with exponential backoff to handle transient
        RTSP source unavailability (e.g., video storage restart).
        """
        for attempt in range(len(self._PIPELINE_RETRY_DELAYS) + 1):
            result = self._start_pipeline_once(stream)
            if result:
                return True
            if attempt < len(self._PIPELINE_RETRY_DELAYS):
                delay = self._PIPELINE_RETRY_DELAYS[attempt]
                logger.warning(
                    f"[Orin] {stream.camera_id}: Pipeline start failed (attempt {attempt + 1}), retrying in {delay}s"
                )
                time.sleep(delay)
        logger.error(
            f"[Orin] {stream.camera_id}: Pipeline start failed after {len(self._PIPELINE_RETRY_DELAYS) + 1} attempts"
        )
        return False

    def _start_pipeline_once(self, stream: OrinStreamState) -> bool:
        """Single attempt to start the GStreamer subprocess."""
        try:
            script_path = self._ensure_child_script()

            cmd_args = [
                sys.executable,
                script_path,
                stream.video_path,
                str(stream.width),
                str(stream.height),
            ]
            if stream.stream_type != "rtsp":
                cmd_args.append("--file")
            if stream.codec and stream.codec != "h264":
                cmd_args.append(f"--codec={stream.codec}")

            logger.info(f"[Orin] {stream.camera_id}: Starting GStreamer subprocess")

            proc = subprocess.Popen(  # nosec B603
                cmd_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
                preexec_fn=os.setsid,  # Own process group for cleanup
            )

            stream.process = proc
            stream.session_start_ns = time.time_ns()
            stream.session_id = str(uuid.uuid4())[:8]
            stream.frames_decoded = 0
            stream.errors = 0
            stream.transient_errors = 0
            stream.first_rtp_ts = None
            stream.last_rtp_ts = None

            # Wait for meta message from child
            try:
                meta = self._read_json(proc)
            except Exception as e:
                stderr = ""
                try:
                    stderr = proc.stderr.read(1000).decode(errors="replace")
                except Exception:  # nosec B110
                    pass
                logger.exception(f"[Orin] {stream.camera_id}: Failed to read meta: {e}\n{stderr}")
                self._stop_pipeline(stream)
                return False

            if meta.get("type") == "error":
                logger.error(f"[Orin] {stream.camera_id}: Child error: {meta.get('msg')}")
                self._stop_pipeline(stream)
                return False

            if meta.get("type") != "meta":
                logger.error(f"[Orin] {stream.camera_id}: Unexpected msg from child: {meta}")
                self._stop_pipeline(stream)
                return False

            stream.source_fps = _normalize_reported_fps(meta.get("fps", 30.0))

            logger.info(
                f"[Orin] {stream.camera_id}: Subprocess pipeline started "
                f"(pid={proc.pid}, session={stream.session_id}, "
                f"fps={stream.source_fps:.1f})"
            )
            return True

        except Exception as e:
            logger.exception(f"[Orin] {stream.camera_id}: Pipeline start failed: {e}")
            return False

    def _stop_pipeline(self, stream: OrinStreamState):
        """Stop subprocess pipeline for a stream."""
        try:
            if stream.process and stream.process.poll() is None:
                try:
                    os.killpg(os.getpgid(stream.process.pid), signal.SIGTERM)
                except (ProcessLookupError, PermissionError):
                    pass
                try:
                    stream.process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(os.getpgid(stream.process.pid), signal.SIGKILL)
                    except (ProcessLookupError, PermissionError):
                        pass
            stream.process = None
        except Exception as e:
            logger.warning(f"[Orin] {stream.camera_id}: Pipeline stop error: {e}")

    def _restart_pipeline(self, stream: OrinStreamState) -> bool:
        """Restart subprocess pipeline on error."""
        self._stop_pipeline(stream)
        time.sleep(0.5)
        return self._start_pipeline(stream)

    def assign_stream(
        self,
        stream_id: int,
        camera_id: str,
        video_path: str,
        width: int = TARGET_WIDTH,
        height: int = TARGET_HEIGHT,
        stream_type: str = "file",
        demuxer_type: str = None,
        codec: str = None,
    ) -> bool:
        """Assign a camera stream and start its subprocess."""
        if self.actual_pool_size == 0:
            return False

        decoder_idx = stream_id % self.actual_pool_size

        stream = OrinStreamState(
            stream_id=stream_id,
            camera_id=camera_id,
            video_path=video_path,
            width=width,
            height=height,
            stream_type=stream_type,
            codec=codec or self.codec,
        )

        success = self._start_pipeline(stream)
        self.streams_per_decoder[decoder_idx].append(stream)
        self._all_streams[camera_id] = stream

        if success:
            logger.info(f"[Orin] {camera_id}: Assigned to decoder slot {decoder_idx} ({stream_type})")
        else:
            logger.warning(f"[Orin] {camera_id}: Pipeline not started, will retry")

        return success

    def _compute_orin_timestamp(
        self,
        stream: "OrinStreamState",
        abs_ns: Optional[int],
        rtp_ns: Optional[int],
        rtp_ts_val: Optional[int],
    ) -> int:
        """Compute timestamp_ns using priority cascade.

        Returns RTP-derived nanoseconds only (rtp_ts * 1e9 / 90kHz), or 0.
        This keeps capture_timestamp_ns purely RTP-based on both platforms
        so the frontend can use it consistently for overlay sync.
        """
        # RTP-derived timestamp only — consistent across nvdec and orin
        if rtp_ns and rtp_ns > 0:
            return rtp_ns
        now = time.time()
        if now - stream._last_rtp_warn > 5.0:
            logger.warning(
                f"[Orin] {stream.camera_id}: capture_timestamp_ns=0 "
                f"(no RTP timestamp from camera, frame {stream.frames_decoded})"
            )
            stream._last_rtp_warn = now
        return 0
        # --- Alternative timestamp sources (disabled, kept for reference) ---
        # # RTCP Sender Report: absolute Unix epoch nanoseconds
        # if abs_ns and abs_ns > 0:
        #     if not stream._rtcp_logged:
        #         logger.info(
        #             f"[Orin] {stream.camera_id}: RTCP SR active, using absolute time"
        #         )
        #         stream._rtcp_logged = True
        #     return abs_ns
        # # Wall-clock fallback for live RTSP (epoch, ~100ms offset from capture)
        # if stream.stream_type == "rtsp":
        #     return time.time_ns()
        # # T0 + RTP delta (approximate epoch, drifts over time)
        # if rtp_ts_val is not None and stream.first_rtp_ts is not None:
        #     rtp_delta = (rtp_ts_val - stream.first_rtp_ts) & 0xFFFFFFFF
        #     if rtp_delta > 0x7FFFFFFF:
        #         rtp_delta -= 0x100000000
        #     return stream.session_start_ns + int(
        #         rtp_delta * 1_000_000_000 / RTP_CLOCK_RATE
        #     )
        # # Frame-count estimate (file sources)
        # return int(stream.frames_decoded * 1_000_000_000 / stream.source_fps)

    def _pull_frame(self, stream: OrinStreamState) -> Optional[Tuple[Any, int, Optional[int]]]:
        """Pull one NV12 frame from Python GStreamer subprocess via wire protocol.

        Returns:
            (nv12_tensor, timestamp_ns, rtp_ts) or None if no frame available.
            rtp_ts is the raw 32-bit RTP timestamp, or None for file sources.
        """
        if stream.process is None:
            return None

        # Check if process is still alive
        if stream.process.poll() is not None:
            stream.errors += 1
            if stream.errors <= 3:
                stderr = ""
                try:
                    stderr = stream.process.stderr.read().decode("utf-8", errors="replace")[:300]
                except Exception:  # nosec B110
                    pass
                logger.warning(
                    f"[Orin] {stream.camera_id}: Subprocess exited (rc={stream.process.returncode}): {stderr}"
                )
            if stream.errors >= 3:
                logger.info(f"[Orin] {stream.camera_id}: Restarting pipeline")
                self._restart_pipeline(stream)
            return None

        try:
            # Read frame header (JSON)
            msg = self._read_json(stream.process)
            msg_type = msg.get("type")

            if msg_type == "eof":
                logger.info(f"[Orin] {stream.camera_id}: Stream EOF")
                self._restart_pipeline(stream)
                return None

            if msg_type == "error":
                logger.warning(f"[Orin] {stream.camera_id}: Child error: {msg.get('msg')}")
                self._restart_pipeline(stream)
                return None

            if msg_type != "frame":
                stream.transient_errors += 1
                logger.warning(f"[Orin] {stream.camera_id}: Unexpected msg type: {msg_type}")
                return None

            rtp_ts_raw = msg.get("rtp_ts", 0)
            rtp_ns = msg.get("rtp_ns", 0)
            abs_ns = msg.get("abs_ns")  # None if no RTCP SR yet
            expected_size = msg.get("size", self._frame_size)

            # Read raw NV12 frame data
            data = self._read_msg(stream.process)

            if len(data) < expected_size:
                stream.transient_errors += 1
                logger.warning(f"[Orin] {stream.camera_id}: Short frame read: {len(data)}/{expected_size}")
                return None

            # Reshape to NV12 layout: (960, 640, 1)
            nv12_np = np.frombuffer(data, dtype=np.uint8).reshape(int(stream.height * 1.5), stream.width, 1)

            # Upload to GPU via CuPy (shared DRAM on Orin)
            tensor = cp.asarray(nv12_np)

            # Determine RTP timestamp
            rtp_ts_val = rtp_ts_raw if rtp_ts_raw and rtp_ts_raw > 0 else None

            # Calculate timestamp_ns
            stream.frames_decoded += 1

            if rtp_ts_val is not None:
                # Track first RTP timestamp
                if stream.first_rtp_ts is None:
                    stream.first_rtp_ts = rtp_ts_val
                    logger.info(f"[Orin] {stream.camera_id}: First RTP ts: {rtp_ts_val}")
                stream.last_rtp_ts = rtp_ts_val

            timestamp_ns = self._compute_orin_timestamp(stream, abs_ns, rtp_ns, rtp_ts_val)

            stream.errors = 0
            stream.transient_errors = 0

            # Log first frame and periodic status
            if stream.frames_decoded == 1:
                logger.info(
                    f"[Orin] {stream.camera_id}: First frame decoded! shape={tensor.shape}, rtp_ts={rtp_ts_val}"
                )
            elif stream.frames_decoded % 500 == 0:
                elapsed = (time.time_ns() - stream.session_start_ns) / 1e9
                fps = stream.frames_decoded / elapsed if elapsed > 0 else 0
                logger.info(
                    f"[Orin] {stream.camera_id}: {stream.frames_decoded} frames, "
                    f"{fps:.1f} fps, rtp_ts={rtp_ts_val}, "
                    f"transient_errs={stream.transient_errors}"
                )

            return tensor, timestamp_ns, rtp_ts_val

        except EOFError:
            stream.errors += 1
            if stream.errors >= 3:
                logger.warning(f"[Orin] {stream.camera_id}: Pipe EOF, restarting")
                self._restart_pipeline(stream)
            return None

        except TimeoutError as te:
            stream.errors += 1
            if stream.errors <= 3:
                logger.warning(f"[Orin] {stream.camera_id}: Read timeout: {te}")
            if stream.errors >= 3:
                logger.warning(f"[Orin] {stream.camera_id}: Repeated timeouts, restarting")
                self._restart_pipeline(stream)
            return None

        except Exception as e:
            stream.errors += 1
            if stream.errors <= 3:
                logger.warning(f"[Orin] {stream.camera_id}: Pull frame error: {e}")
            if stream.errors >= 10:
                logger.warning(f"[Orin] {stream.camera_id}: Too many errors, restarting")
                self._restart_pipeline(stream)
            return None

    def decode_round(
        self,
        decoder_idx: int,
        frames_per_stream: int = 4,
        target_h: int = TARGET_HEIGHT,
        target_w: int = TARGET_WIDTH,
        benchmark_metrics: Any = None,
    ) -> Tuple[int, List[Tuple[str, Any, int, str, str, int, Optional[int]]]]:
        """Decode frames from all streams assigned to this decoder slot.

        Returns same format as NVDECDecoderPool.decode_round:
            (total_frames, [(camera_id, nv12_tensor, timestamp_ns,
                             stream_type, session_id, session_start_ns, rtp_timestamp), ...])
        """
        if decoder_idx >= self.actual_pool_size:
            return 0, []

        streams = self.streams_per_decoder[decoder_idx]
        if not streams:
            return 0, []

        total_frames = 0
        decoded_frames: List[Tuple[str, Any, int, str, str, int, Optional[int]]] = []

        for stream in streams:
            if stream.process is None or (stream.process and stream.process.poll() is not None):
                self._start_pipeline(stream)
                continue

            for _ in range(frames_per_stream):
                result = self._pull_frame(stream)
                if result is None:
                    break

                tensor, timestamp_ns, rtp_ts = result
                decoded_frames.append(
                    (
                        stream.camera_id,
                        tensor,
                        timestamp_ns,
                        stream.stream_type,
                        stream.session_id,
                        stream.session_start_ns,
                        rtp_ts,
                    )
                )
                total_frames += 1

        return total_frames, decoded_frames

    def get_camera_ids_for_decoder(self, decoder_idx: int) -> List[str]:
        """Get camera IDs assigned to a decoder slot."""
        if decoder_idx >= self.actual_pool_size:
            return []
        return [s.camera_id for s in self.streams_per_decoder[decoder_idx]]

    def get_source_fps_for_decoder(self, decoder_idx: int) -> float:
        """Get average source FPS for streams on this decoder."""
        if decoder_idx >= self.actual_pool_size:
            return DEFAULT_SOURCE_FPS
        streams = self.streams_per_decoder[decoder_idx]
        if not streams:
            return DEFAULT_SOURCE_FPS
        return _normalize_reported_fps(sum(s.source_fps for s in streams) / len(streams))

    def close(self):
        """Close all decoders (API compat with NVDECDecoderPool)."""
        self.release()

    def release(self):
        """Stop all subprocess pipelines."""
        for camera_id, stream in self._all_streams.items():
            self._stop_pipeline(stream)
            logger.info(f"[Orin] {camera_id}: Pipeline stopped")
        self._all_streams.clear()

    def __del__(self):
        try:
            self.release()
        except Exception:  # nosec B110
            pass
