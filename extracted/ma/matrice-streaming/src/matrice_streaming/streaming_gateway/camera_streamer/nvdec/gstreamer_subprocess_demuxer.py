"""GStreamer Subprocess Demuxer — Isolates GStreamer from PyNvVideoCodec.

PyNvVideoCodec bundles FFmpeg 6.x, while GStreamer uses system FFmpeg 4.4.
Loading both in the same process causes SIGABRT when rtspsrc connects.

This module runs GStreamer demuxing in a separate subprocess (via subprocess.Popen)
that only imports GStreamer. H264/H265 NAL bytes + RTP timestamps are streamed
through a pipe to the parent process where NVDEC decodes them.

TODO: Replace stdout pipe with shared memory (/dev/shm ring buffer) to avoid
kernel copy overhead on every frame. The pipe currently copies each frame
twice (child write → kernel buffer → parent read). SHM would give zero-copy.

Interface is compatible with GstRTPDemuxer: provides open(), close(), demux(),
and properties (width, height, fps, session_id, first_rtp_timestamp).
"""

from __future__ import annotations

import json
import logging
import os
import struct
import subprocess
import sys
import tempfile
import time
import uuid
from typing import Iterator, Optional, Tuple

logger = logging.getLogger(__name__)

# Wire protocol over stdout pipe:
#   4 bytes: message length (big-endian uint32)
#   N bytes: JSON or raw NAL data
#
# Message types (first byte of JSON):
#   {"type":"meta", ...}  - metadata (width, height, fps, etc.)
#   {"type":"frame", "rtp_ts": int, "rtp_ns": int, "abs_ns": int, "size": int}
#     followed by: 4 bytes length + raw NAL bytes (H264 or H265)
#   {"type":"eof"}
#   {"type":"error", "msg": str}

# The child script that runs GStreamer — as a standalone string to avoid
# any import of the parent package tree.
_CHILD_SCRIPT = r'''
import importlib.util
import json
import os
import struct
import sys
import time

def write_msg(data: bytes):
    """Write length-prefixed message to stdout."""
    sys.stdout.buffer.write(struct.pack(">I", len(data)))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

def write_json(obj):
    write_msg(json.dumps(obj).encode())

def main():
    video_path = sys.argv[1]
    use_tcp = sys.argv[2] == "true"
    demuxer_path = sys.argv[3]
    codec = sys.argv[4] if len(sys.argv) > 4 else "h264"

    # Import GstRTPDemuxer by file path (avoids package __init__.py -> PyNvVideoCodec)
    # Create a synthetic package so relative imports (from ..codec_detect ...) resolve.
    # pkg.__path__ includes both nvdec/ dir and parent camera_streamer/ dir so that
    # codec_detect.py (which lives in camera_streamer/) is discoverable.
    import types
    pkg_dir = os.path.dirname(os.path.abspath(demuxer_path))
    pkg_name = "_camera_streamer"
    pkg = types.ModuleType(pkg_name)
    pkg.__path__ = [pkg_dir, os.path.dirname(pkg_dir)]
    pkg.__package__ = pkg_name
    sys.modules[pkg_name] = pkg

    mod_name = f"{pkg_name}.gstreamer_rtp_demuxer"
    spec = importlib.util.spec_from_file_location(mod_name, demuxer_path)
    mod = importlib.util.module_from_spec(spec)
    mod.__package__ = pkg_name
    sys.modules[mod_name] = mod
    sys.modules["gstreamer_rtp_demuxer"] = mod  # Required for dataclass decorator
    spec.loader.exec_module(mod)
    GstRTPDemuxer = mod.GstRTPDemuxer

    try:
        demuxer = GstRTPDemuxer(video_path, use_tcp=use_tcp, codec=codec)
        demuxer.open(quiet=True)

        # SIGTERM handler: route through demuxer.close() so the GStreamer
        # pipeline transitions to NULL and frees its dmabufs before exit.
        # Without this, parent's SIGTERM->SIGKILL escalation can kill the
        # process mid-pipeline and the buffer-backed inode references stay
        # held in the kernel until drop_caches=2 reclaims them.
        import signal as _signal_mod
        _term_done = [False]
        def _graceful_term(_signum=None, _frame=None):
            if _term_done[0]:
                return
            _term_done[0] = True
            try:
                demuxer.close()
            except Exception:
                pass
            sys.exit(0)
        try:
            _signal_mod.signal(_signal_mod.SIGTERM, _graceful_term)
            _signal_mod.signal(_signal_mod.SIGINT, _graceful_term)
        except (OSError, ValueError):
            pass

        write_json({
            "type": "meta",
            "width": demuxer.width,
            "height": demuxer.height,
            "fps": demuxer.fps,
            "session_id": demuxer.session_id,
            "first_rtp_timestamp": demuxer.first_rtp_timestamp,
        })

        for nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns in demuxer.demux():
            # Write frame header
            write_json({
                "type": "frame",
                "rtp_ts": rtp_ts,
                "rtp_ns": rtp_ts_ns,
                "abs_ns": absolute_ns,
                "size": len(nal_bytes),
            })
            # Write raw NAL data
            write_msg(nal_bytes)

        write_json({"type": "eof"})

    except Exception as e:
        try:
            write_json({"type": "error", "msg": str(e)})
        except Exception:
            pass
        sys.exit(1)

    finally:
        try:
            demuxer.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
'''


def _find_demuxer_module_path() -> str:
    """Find gstreamer_rtp_demuxer.py — prefer same directory, then installed packages."""
    # Check same directory as this file
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gstreamer_rtp_demuxer.py")
    if os.path.isfile(local):
        return local

    try:
        import site

        for sp in site.getsitepackages():
            candidate = os.path.join(
                sp,
                "matrice_streaming",
                "streaming_gateway",
                "camera_streamer",
                "nvdec",
                "gstreamer_rtp_demuxer.py",
            )
            if os.path.isfile(candidate):
                return candidate
    except Exception:  # nosec B110
        pass
    return ""


class GStreamerSubprocessDemuxer:
    """GStreamer demuxer that runs in a subprocess to avoid FFmpeg conflicts.

    Drop-in replacement for GstRTPDemuxer with the same interface:
    - open() / close()
    - demux() generator yielding (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns)
    - Properties: width, height, fps, session_id, first_rtp_timestamp
    """

    def __init__(self, video_path: str, use_tcp: bool = True, codec: str = "h264"):
        from ..codec_detect import normalize_codec

        self.video_path = video_path
        self.use_tcp = use_tcp
        self.codec = normalize_codec(codec)
        self._proc: Optional[subprocess.Popen] = None
        self._script_path: Optional[str] = None

        # Metadata (populated after open)
        self.width: Optional[int] = None
        self.height: Optional[int] = None
        self.fps: float = 0.0
        self.session_id: str = uuid.uuid4().hex[:8]
        self.first_rtp_timestamp: Optional[int] = None

    def _read_exact(self, n: int) -> bytes:
        """Read exactly n bytes from subprocess stdout, retrying on short reads."""
        buf = b""
        while len(buf) < n:
            chunk = self._proc.stdout.read(n - len(buf))
            if not chunk:
                raise EOFError("Subprocess pipe closed")
            buf += chunk
        return buf

    def _read_msg(self) -> bytes:
        """Read a length-prefixed message from the subprocess stdout."""
        header = self._read_exact(4)
        length = struct.unpack(">I", header)[0]
        return self._read_exact(length)

    def _read_json(self) -> dict:
        """Read a JSON message from the subprocess."""
        data = self._read_msg()
        return json.loads(data)

    # Retry configuration for subprocess startup
    _OPEN_RETRY_DELAYS = [
        1,
        3,
    ]  # 2 retries — keep fast, background retry handles persistence

    def open(self, quiet: bool = True) -> None:
        """Start the GStreamer subprocess and wait for metadata.

        Retries up to 5 times with exponential backoff to handle transient
        RTSP source unavailability (e.g., video storage restart).
        """
        last_error = None
        for attempt in range(len(self._OPEN_RETRY_DELAYS) + 1):
            try:
                self._open_once(quiet=quiet)
                return  # Success
            except RuntimeError as e:
                last_error = e
                if attempt < len(self._OPEN_RETRY_DELAYS):
                    delay = self._OPEN_RETRY_DELAYS[attempt]
                    logger.warning(
                        f"GStreamer subprocess open failed (attempt {attempt + 1}): {e}, retrying in {delay}s"
                    )
                    time.sleep(delay)
        raise RuntimeError(
            f"GStreamer subprocess failed for {self.video_path} after "
            f"{len(self._OPEN_RETRY_DELAYS) + 1} attempts: {last_error}"
        )

    def _open_once(self, quiet: bool = True) -> None:
        """Single attempt to start the GStreamer subprocess."""
        demuxer_path = _find_demuxer_module_path()
        if not demuxer_path:
            raise RuntimeError("gstreamer_rtp_demuxer.py not found in installed packages")

        # Write child script to a unique temp file
        fd, script_path = tempfile.mkstemp(prefix="_gst_demux_", suffix=".py")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(_CHILD_SCRIPT)
        self._script_path = script_path

        self._proc = subprocess.Popen(  # nosec B603
            [
                sys.executable,
                script_path,
                self.video_path,
                "true" if self.use_tcp else "false",
                demuxer_path,
                self.codec,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )

        # Wait for metadata message
        try:
            meta = self._read_json()
        except Exception as e:
            stderr = ""
            if self._proc.stderr:
                try:
                    stderr = self._proc.stderr.read(2000).decode(errors="replace")
                except Exception:  # nosec B110
                    pass
            self.close()
            raise RuntimeError(f"GStreamer subprocess failed for {self.video_path}: {e}\nstderr: {stderr}") from e

        if meta.get("type") == "error":
            self.close()
            raise RuntimeError(f"GStreamer subprocess error: {meta.get('msg')}")

        if meta.get("type") != "meta":
            self.close()
            raise RuntimeError(f"Unexpected message from subprocess: {meta}")

        self.width = meta.get("width")
        self.height = meta.get("height")
        self.fps = meta.get("fps", 0.0)
        self.session_id = meta.get("session_id", self.session_id)
        self.first_rtp_timestamp = meta.get("first_rtp_timestamp")

        # Child has started and sent metadata, safe to delete temp script
        if self._script_path:
            try:
                os.unlink(self._script_path)
            except OSError:
                pass
            self._script_path = None

        if not quiet:
            logger.info(
                f"GStreamer subprocess started: {self.width}x{self.height}@{self.fps:.1f}fps, "
                f"session={self.session_id}, first_rtp={self.first_rtp_timestamp}"
            )

    def close(self) -> None:
        """Stop the subprocess and clean up all resources."""
        if self._proc:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=3)
            except Exception:
                try:
                    self._proc.kill()
                    self._proc.wait(timeout=2)
                except Exception:  # nosec B110
                    pass
            self._proc = None
        # Clean up temp script file if it still exists
        script_path = getattr(self, "_script_path", None)
        if script_path:
            try:
                os.unlink(script_path)
            except OSError:
                pass
            self._script_path = None

    def restart(self) -> None:
        """Restart the demuxer (reconnect to RTSP)."""
        self.close()
        self.open(quiet=True)

    def demux(self) -> Iterator[Tuple[bytes, int, int, Optional[int]]]:
        """Yield (nal_bytes, rtp_ts, rtp_ts_ns, absolute_ns) from subprocess."""
        if not self._proc:
            return

        while True:
            try:
                msg = self._read_json()
            except EOFError:
                return
            except Exception as e:
                logger.warning(f"GStreamer subprocess read error: {e}")
                return

            msg_type = msg.get("type")

            if msg_type == "eof":
                return
            elif msg_type == "error":
                logger.error(f"GStreamer subprocess error: {msg.get('msg')}")
                return
            elif msg_type == "meta":
                # Child reconnected after EOF (simulation video loop).
                # Update session metadata and continue yielding frames.
                self.session_id = msg.get("session_id", self.session_id)
                self.first_rtp_timestamp = msg.get("first_rtp_timestamp")
                logger.debug(f"GStreamer subprocess reconnected, new session={self.session_id}")
            elif msg_type == "frame":
                rtp_ts = msg.get("rtp_ts", 0)
                rtp_ns = msg.get("rtp_ns", 0)
                abs_ns = msg.get("abs_ns")
                # Read NAL data
                try:
                    nal_bytes = self._read_msg()
                except EOFError:
                    return
                yield (nal_bytes, rtp_ts, rtp_ns, abs_ns)

    def __del__(self):
        self.close()
