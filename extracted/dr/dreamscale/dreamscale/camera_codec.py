"""The camera codec of an internally rolled-out robot (opt-in per robot, no user-facing option).

A robot whose camera frames are coded by a device beside it (the YAM's a7 and its Jetson Orin)
opts in with one section in ``$DREAMSCALE_HOME/config.toml``:

    [camera_codec]
    device = "10.10.0.2:7461"      # the codec device

π0.5-YAM sessions then offer the T16 codec when the device, the worker and the rig's camera
sizes (640x360) agree, and send today's JPEG otherwise, with the reason on the status line.
Any change mid-session, each request sent as JPEG instead of T16, and the run's tally are
printed as ``! `` lines, so a codec run that fell back can't pass for one that didn't.
``DREAMSCALE_CAMERA_CODEC=off`` disables it for one run; ``=wire`` sends today's JPEG made by
the device (an A/B's reference arm, paying the same hop). Per-request records go to
``DREAMSCALE_CODEC_LOG`` (JSONL; default ``$DREAMSCALE_HOME/codec-logs/<UTC time>-<pid>.jsonl``),
and every sent frame beside it, as sent but with the session token redacted (``.frames``;
``read_sent_frames``).

The settings object lives for the process: a session whose codec was turned off stays on JPEG
when it reconnects, and the next session tries again.
"""

from __future__ import annotations

import atexit
import json
import logging
import os
import queue
import threading
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from dreamscale_transport import catalog
from dreamscale_transport.codec_client import CodecSettings

from dreamscale.config import dreamscale_home, load_config
from dreamscale.constants import (
    CAMERA_KEY_BIMANUAL_YAM_LEFT,
    CAMERA_KEY_BIMANUAL_YAM_RIGHT,
    CAMERA_KEY_BIMANUAL_YAM_TOP,
)

log = logging.getLogger(__name__)

CODEC_ENV = "DREAMSCALE_CAMERA_CODEC"
LOG_ENV = "DREAMSCALE_CODEC_LOG"
YAM_CAMERAS = (CAMERA_KEY_BIMANUAL_YAM_TOP, CAMERA_KEY_BIMANUAL_YAM_LEFT,
               CAMERA_KEY_BIMANUAL_YAM_RIGHT)

_SETTINGS: dict[tuple[object, ...], CodecSettings] = {}
# The running rig's frame size per camera (width, height after rotation), noted by the robot
# runner before it connects, so a rig the codec can't code says JPEG at connect.
_RIG_FRAME_SIZES: dict[str, tuple[int, int]] | None = None


def note_rig_frame_sizes(sizes: Mapping[str, tuple[int, int]] | None) -> None:
    """Record the rig's camera frame sizes for this process's codec sessions."""
    global _RIG_FRAME_SIZES
    _RIG_FRAME_SIZES = None if sizes is None else {k: tuple(v) for k, v in sizes.items()}
    for settings in _SETTINGS.values():
        settings.source_sizes = _RIG_FRAME_SIZES


def codec_settings(
    model: str,
    *,
    section: Mapping[str, object] | None = None,
    environ: Mapping[str, str] | None = None,
) -> CodecSettings | None:
    """This process's camera-codec settings for a session of ``model``, or None (JPEG)."""
    env = os.environ if environ is None else environ
    override = env.get(CODEC_ENV, "").strip().lower()
    if override not in ("", "off", "wire"):
        raise ValueError(f"{CODEC_ENV} must be off or wire, not {override!r}")
    if override == "off":
        return None
    if section is None:
        section = load_config().camera_codec
    device = str(section.get("device") or "").strip()
    if not device:
        return None
    served = catalog.camera_codec_models()
    if model not in served:
        log.info("The camera codec serves %s only; %s sends JPEG.", ", ".join(sorted(served)),
                 model)
        return None
    if device == "local":
        log.warning("[camera_codec] device = \"local\" is not supported yet; sending JPEG.")
        return None
    host, _, port = device.rpartition(":")
    if not host or not port.isdigit() or not 0 < int(port) < 65536:
        raise ValueError("[camera_codec] device must be host:port")
    mode = "wire" if override == "wire" else "t16"
    log_path = env.get(LOG_ENV, "").strip()
    key = (mode, device, log_path)
    settings = _SETTINGS.get(key)
    if settings is None:
        from dreamscale.policy.runtime.contract import runtime_contract_for_model

        wire_image = runtime_contract_for_model(model).wire_image
        assert wire_image is not None
        path = Path(log_path).expanduser() if log_path else _default_log_path()
        settings = CodecSettings(
            mode=mode, host=host.strip("[]"), port=int(port), cameras=YAM_CAMERAS,
            wire_image=wire_image, on_record=JsonlRecords(path),
            on_frame=SentFrames(path.with_suffix(".frames")),
        )
        _SETTINGS[key] = settings
        log.info("Camera codec %s through %s; records in %s (+ .frames)", mode, device, path)
    settings.source_sizes = _RIG_FRAME_SIZES
    return settings


def check_device(
    section: Mapping[str, object], environ: Mapping[str, str] | None = None
) -> tuple[str, str, str | None]:
    """``dreamscale doctor``'s view of this robot's codec device: (status, detail, fix).

    Asks the device's health report, which never disturbs a running session.
    """
    import asyncio

    from dreamscale_transport.codec_service import CodecServiceError, device_health

    env = os.environ if environ is None else environ
    device = str(section.get("device") or "").strip()
    if env.get(CODEC_ENV, "").strip().lower() == "off":
        return "skip", f"off for this run ({CODEC_ENV}=off)", None
    if device == "local":
        return "warn", 'device = "local" is not supported yet; sessions send JPEG', None
    host, _, port = device.rpartition(":")
    if not host or not port.isdigit() or not 0 < int(port) < 65536:
        return "fail", f"device {device!r} is not host:port", (
            'set [camera_codec] device = "<address>:<port>" in config.toml'
        )
    try:
        health = asyncio.run(device_health(host.strip("[]"), int(port), timeout_s=2.0))
    except CodecServiceError as exc:
        return "fail", f"{device} did not answer ({exc.reason})", (
            "check the codec device is on and wired to this computer and its service is "
            "running; sessions send JPEG until it answers"
        )
    if health.get("failure") or health.get("self_check") in (False, "fail", "failed"):
        detail = (health.get("failure") or health.get("self_check_detail")
                  or "self-check failed")
        return "fail", f"{device}: {detail}", (
            "restart the codec service on the device; sessions send JPEG until it passes"
        )
    if health.get("warm") is not True:
        return "warn", f"{device} is warming up; sessions send JPEG until it is warm", None
    codec = health.get("codec") if isinstance(health.get("codec"), Mapping) else {}
    sha = str(codec.get("bundle_sha256") or "")
    cap = health.get("cap_mbps")
    return "pass", (
        f"T16 via {host}: warm, bundle {sha[:8]}…" + (f", cap {cap:g} Mb/s" if cap else "")
    ), None


def status_summary() -> list[dict[str, Any]]:
    """Every camera-codec connection of this process in 1 s windows (for status.json)."""
    return [summary for settings in _SETTINGS.values() for summary in settings.summaries()]


def _default_log_path() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    return dreamscale_home() / "codec-logs" / f"{stamp}-{os.getpid()}.jsonl"


class SentFrames:
    """Append every frame the codec connection sends to ``path`` (``<log>.frames``), as sent
    except for the session token, which the transport redacts before handing it over.

    Each sent frame is already length-prefixed (4-byte big-endian, then the frame), so the file
    is those frames back to back; ``read_sent_frames`` iterates them. Written from a background
    thread, so a slow disk never holds a send; flushed per frame, drained at exit (5 s bound)."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._queue: queue.SimpleQueue[bytes | None] = queue.SimpleQueue()
        self._thread = threading.Thread(target=self._run, name="camera-codec-frames", daemon=True)
        self._thread.start()
        atexit.register(self.close)

    def __call__(self, frame: bytes) -> None:
        self._queue.put(bytes(frame))

    def _run(self) -> None:
        handle = None
        while (frame := self._queue.get()) is not None:
            try:
                if handle is None:
                    self.path.parent.mkdir(parents=True, exist_ok=True)
                    handle = self.path.open("ab")
                handle.write(frame)
                handle.flush()
            except OSError:
                log.warning("camera codec: could not write %s", self.path, exc_info=True)
        if handle is not None:
            handle.close()

    def close(self, timeout_s: float = 5.0) -> None:
        if self._thread.is_alive():
            self._queue.put(None)
            self._thread.join(timeout_s)


def read_sent_frames(path: Path):
    """The ``(metadata, payloads)`` of each frame in a ``SentFrames`` file, in send order."""
    from dreamscale_transport.framing import decode_websocket_stream_frame

    data = Path(path).read_bytes()
    offset = 0
    while offset + 4 <= len(data):
        size = int.from_bytes(data[offset:offset + 4], "big")
        end = offset + 4 + size
        if end > len(data):
            break  # a frame cut short by a crash mid-write
        yield decode_websocket_stream_frame(data[offset:end])
        offset = end


class JsonlRecords:
    """Append each record as one JSON line (flushed per line, so a crash keeps what it saw)."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def __call__(self, record: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps({"logged_ns": time.time_ns(), **record}, sort_keys=True, default=str)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
