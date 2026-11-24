"""Off-hot-path local LeRobot v3.0 episode spooler.

Captures tick-synchronized joint states, executed actions, Dreamscale intervention
columns (``action_source``, ``intervention``, ``checkpoint_id``), and per-camera
H.264/MP4 clips to crash-safe local episode folders without blocking the control
loop or touching the live QUIC/WSS inference link.

Each finalized episode directory contains:
- ``episode.parquet`` — LeRobot v3.0 per-frame table compatible with cloud compaction
- ``<camera_role>.mp4`` — H.264 (or mpeg4 fallback) video per recorded camera
- ``episode.json`` — atomic manifest & upload state (``recording`` -> ``ready`` -> ``uploaded``)
"""

from __future__ import annotations

import json
import math
import os
import queue
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

RECORD_EXTRA_HINT = "Install episode recording support: pip install 'dreamscale[record]'"
DEFAULT_QUEUE_MAXSIZE = 256
ZERO_MOTION_EPS = 1e-4


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex[:8]}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _clean_camera_name(role: str) -> str:
    text = role.strip()
    if text.startswith("observation.images."):
        text = text[len("observation.images.") :]
    safe = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in text).strip("_")
    return safe or "camera"


def _to_rgb_uint8(frame: np.ndarray) -> np.ndarray:
    arr = np.asarray(frame)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    if arr.ndim != 3:
        raise ValueError(f"Expected HxWxC camera frame, got shape {arr.shape}")
    if arr.shape[2] == 4:
        arr = arr[:, :, :3]
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    return np.ascontiguousarray(arr)


class _CameraVideoWriter:
    """Dedicated PyAV encoder for one camera stream, always called from the writer thread."""

    def __init__(self, path: Path, *, width: int, height: int, fps: float) -> None:
        try:
            import av
        except ImportError as exc:
            raise RuntimeError(RECORD_EXTRA_HINT) from exc

        self._av = av
        self.path = path
        self.tmp_path = path.with_name(f".{path.name}.tmp.mp4")
        rate = max(1, int(round(fps)))
        # Ensure even dimensions for yuv420p H.264 compatibility.
        self._width = width if width % 2 == 0 else width + 1
        self._height = height if height % 2 == 0 else height + 1
        self._container = av.open(str(self.tmp_path), mode="w", format="mp4")
        stream = None
        for codec, options in (
            ("libx264", {"preset": "ultrafast", "tune": "zerolatency", "crf": "23"}),
            ("h264", {}),
            ("mpeg4", {}),
        ):
            try:
                stream = self._container.add_stream(codec, rate=rate)
                stream.width = self._width
                stream.height = self._height
                stream.pix_fmt = "yuv420p"
                if options:
                    stream.options = options
                break
            except Exception:  # noqa: BLE001 - fall back across installed codecs
                stream = None
        if stream is None:
            self._container.close()
            raise RuntimeError(
                "PyAV could not open an MP4 video stream (libx264/mpeg4 unavailable)"
            )
        self._stream = stream
        self._closed = False

    def write(self, rgb: np.ndarray) -> None:
        if self._closed:
            return
        h, w = rgb.shape[:2]
        if h != self._height or w != self._width:
            padded = np.zeros((self._height, self._width, 3), dtype=np.uint8)
            ch, cw = min(h, self._height), min(w, self._width)
            padded[:ch, :cw] = rgb[:ch, :cw]
            rgb = padded
        vf = self._av.VideoFrame.from_ndarray(rgb, format="rgb24")
        for packet in self._stream.encode(vf):
            self._container.mux(packet)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            for packet in self._stream.encode():
                self._container.mux(packet)
        finally:
            self._container.close()
        if self.tmp_path.exists():
            os.replace(self.tmp_path, self.path)


@dataclass(frozen=True)
class EpisodeSummary:
    """Finalized local spool summary returned by ``SpoolEpisode.finish()``."""

    client_episode_id: str
    directory: Path
    manifest_path: Path
    status: str
    files: tuple[str, ...]
    bytes: int
    frame_count: int
    fps: float
    duration_seconds: float
    state_dim: int | None
    action_dim: int | None
    cameras: tuple[str, ...]
    source_kind: str
    takeover_count: int
    takeover_frames: int
    dropped_frames: int
    dropped_frame_ratio: float
    has_nonfinite: bool
    zero_motion: bool
    writer_error: str | None


class SpoolEpisode:
    """One crash-safe local LeRobot v3.0 episode recording.

    ``record_step`` only copies minimal values into a bounded queue via ``put_nowait``
    so it never blocks the robot control loop. All Parquet/MP4 encoding happens on a
    background daemon thread.
    """

    def __init__(
        self,
        spool_root: Path,
        *,
        client_episode_id: str | None = None,
        dataset_ref: str | None = None,
        policy_id: str | None = None,
        policy_version: int | None = None,
        deployment_id: str | None = None,
        session_id: str | None = None,
        robot_id: str | None = None,
        task: str = "",
        fps: float = 30.0,
        default_source_kind: str = "autonomous",
        keep_local: bool = False,
        queue_maxsize: int = DEFAULT_QUEUE_MAXSIZE,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.client_episode_id = client_episode_id or f"ep-{uuid.uuid4().hex[:16]}"
        self.directory = Path(spool_root).expanduser().resolve() / self.client_episode_id
        self.directory.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.directory / "episode.json"

        self.dataset_ref = dataset_ref
        self.policy_id = policy_id
        self.policy_version = policy_version
        self.deployment_id = deployment_id
        self.session_id = session_id
        self.robot_id = robot_id
        self.task = task.strip()
        self.fps = float(fps) if fps and fps > 0 else 30.0
        self.default_source_kind = default_source_kind
        self.keep_local = bool(keep_local)
        self.extra_metadata = dict(metadata or {})
        self.recorded_at = datetime.now(UTC).isoformat()

        self._origin_s = time.monotonic()
        self._queue: queue.Queue[dict[str, Any] | None] = queue.Queue(maxsize=max(8, queue_maxsize))
        self._dropped_frames = 0
        self._submitted_frames = 0
        self._finished = False
        self._summary: EpisodeSummary | None = None
        self._writer_error: str | None = None

        # Owned solely by the background writer thread until join().
        self._states: list[list[float]] = []
        self._actions: list[list[float]] = []
        self._timestamps: list[float] = []
        self._action_sources: list[str] = []
        self._interventions: list[bool] = []
        self._checkpoint_ids: list[str] = []
        self._videos: dict[str, _CameraVideoWriter] = {}
        self._camera_order: list[str] = []
        self._has_nonfinite = False
        self._takeover_count = 0
        self._takeover_frames = 0
        self._in_takeover = False

        _atomic_write_json(
            self.manifest_path,
            {
                "schema_version": 1,
                "status": "recording",
                "client_episode_id": self.client_episode_id,
                "dataset_ref": self.dataset_ref,
                "policy_id": self.policy_id,
                "policy_version": self.policy_version,
                "deployment_id": self.deployment_id,
                "session_id": self.session_id,
                "robot_id": self.robot_id,
                "task": self.task,
                "fps": self.fps,
                "recorded_at": self.recorded_at,
                "keep_local": self.keep_local,
            },
        )

        self._thread = threading.Thread(
            target=self._writer_loop,
            name=f"dreamscale-spool-{self.client_episode_id[:8]}",
            daemon=True,
        )
        self._thread.start()

    def record_step(
        self,
        state: Any,
        action: Any,
        *,
        frames: dict[str, np.ndarray] | None = None,
        timestamp_s: float | None = None,
        action_source: str = "policy",
        intervention: bool = False,
        checkpoint_id: str | None = None,
    ) -> bool:
        """Enqueue one tick-synchronized step without blocking.

        Returns True when queued, False if the episode is already finished or the
        bounded queue is full (never raises into the robot control loop).
        """
        if self._finished:
            return False
        self._submitted_frames += 1
        ts = float(time.monotonic() - self._origin_s) if timestamp_s is None else float(timestamp_s)
        copied_frames: dict[str, np.ndarray] | None = None
        if frames:
            copied_frames = {
                role: np.array(frame, copy=True)
                for role, frame in frames.items()
                if isinstance(frame, np.ndarray)
            }
        item = {
            "state": [float(v) for v in state],
            "action": [float(v) for v in action],
            "timestamp": ts,
            "frames": copied_frames,
            "action_source": str(action_source or "policy"),
            "intervention": bool(intervention),
            "checkpoint_id": str(
                checkpoint_id if checkpoint_id is not None else (self.deployment_id or "")
            ),
        }
        try:
            self._queue.put_nowait(item)
            return True
        except queue.Full:
            self._dropped_frames += 1
            return False

    def _writer_loop(self) -> None:
        while True:
            item = self._queue.get()
            if item is None:
                break
            try:
                self._consume(item)
            except Exception as exc:  # noqa: BLE001 - writer errors never crash control
                if self._writer_error is None:
                    self._writer_error = f"{type(exc).__name__}: {exc}"

    def _consume(self, item: dict[str, Any]) -> None:
        state = item["state"]
        action = item["action"]
        if not self._has_nonfinite and (
            any(not math.isfinite(v) for v in state)
            or any(not math.isfinite(v) for v in action)
        ):
            self._has_nonfinite = True
        self._states.append(state)
        self._actions.append(action)
        self._timestamps.append(item["timestamp"])
        src = item["action_source"]
        intervening = bool(item["intervention"])
        self._action_sources.append(src)
        self._interventions.append(intervening)
        self._checkpoint_ids.append(item["checkpoint_id"])

        if intervening:
            self._takeover_frames += 1
            if not self._in_takeover:
                self._takeover_count += 1
                self._in_takeover = True
        else:
            self._in_takeover = False

        frames: dict[str, np.ndarray] | None = item.get("frames")
        if frames:
            for role, raw in frames.items():
                cam = _clean_camera_name(role)
                rgb = _to_rgb_uint8(raw)
                writer = self._videos.get(cam)
                if writer is None:
                    h, w = rgb.shape[:2]
                    writer = _CameraVideoWriter(
                        self.directory / f"{cam}.mp4",
                        width=w,
                        height=h,
                        fps=self.fps,
                    )
                    self._videos[cam] = writer
                    self._camera_order.append(cam)
                writer.write(rgb)

    def _write_parquet(self) -> Path:
        try:
            import pyarrow as pa
            import pyarrow.parquet as pq
        except ImportError as exc:
            raise RuntimeError(RECORD_EXTRA_HINT) from exc

        n = len(self._states)
        table = pa.table(
            {
                "observation.state": pa.array(self._states, type=pa.list_(pa.float32())),
                "action": pa.array(self._actions, type=pa.list_(pa.float32())),
                "timestamp": pa.array(self._timestamps, type=pa.float32()),
                "frame_index": pa.array(list(range(n)), type=pa.int64()),
                "action_source": pa.array(self._action_sources, type=pa.string()),
                "intervention": pa.array(self._interventions, type=pa.bool_()),
                "checkpoint_id": pa.array(self._checkpoint_ids, type=pa.string()),
            }
        )
        out_path = self.directory / "episode.parquet"
        tmp_path = out_path.with_name(f".{out_path.name}.{uuid.uuid4().hex[:8]}.tmp")
        pq.write_table(table, tmp_path)
        os.replace(tmp_path, out_path)
        return out_path

    def _compute_zero_motion(self) -> bool:
        if len(self._states) < 2:
            return len(self._states) == 0
        arr = np.asarray(self._states, dtype=np.float64)
        if not np.all(np.isfinite(arr)):
            return False
        return float(np.max(np.ptp(arr, axis=0))) < ZERO_MOTION_EPS

    def _effective_source_kind(self) -> str:
        if self._takeover_count > 0:
            return "takeover"
        if self._action_sources and all(src == "human" for src in self._action_sources):
            return "teleop"
        return self.default_source_kind

    def finish(
        self,
        *,
        outcome: str | None = None,
        dataset_ref: str | None = None,
        timeout_s: float = 15.0,
    ) -> EpisodeSummary:
        """Flush queued frames, close video & Parquet atomically, and mark episode ready."""
        if self._summary is not None:
            return self._summary
        self._finished = True
        if dataset_ref:
            self.dataset_ref = dataset_ref

        # Deliver sentinel to drain the queue cleanly.
        deadline = time.monotonic() + max(1.0, timeout_s)
        while True:
            try:
                self._queue.put(None, timeout=0.25)
                break
            except queue.Full:
                if time.monotonic() >= deadline:
                    break
                try:
                    self._queue.get_nowait()
                    self._dropped_frames += 1
                except queue.Empty:
                    pass
        self._thread.join(timeout=max(0.5, deadline - time.monotonic()))

        for writer in self._videos.values():
            try:
                writer.close()
            except Exception as exc:  # noqa: BLE001
                if self._writer_error is None:
                    self._writer_error = f"{type(exc).__name__}: {exc}"

        files: list[str] = []
        n = len(self._states)
        if n > 0:
            try:
                pq_path = self._write_parquet()
                files.append(pq_path.name)
            except Exception as exc:  # noqa: BLE001
                if self._writer_error is None:
                    self._writer_error = f"{type(exc).__name__}: {exc}"
        for cam in self._camera_order:
            mp4 = self.directory / f"{cam}.mp4"
            if mp4.exists() and mp4.stat().st_size > 0:
                files.append(mp4.name)

        total_bytes = sum((self.directory / name).stat().st_size for name in files)
        duration_s = (
            float(self._timestamps[-1] - self._timestamps[0])
            if n >= 2
            else (n / self.fps if n else 0.0)
        )
        if n > 0 and duration_s <= 0.0:
            duration_s = n / self.fps
        state_dim = len(self._states[0]) if n > 0 else None
        action_dim = len(self._actions[0]) if n > 0 else None
        dropped_ratio = (
            self._dropped_frames / self._submitted_frames if self._submitted_frames > 0 else 0.0
        )
        zero_motion = self._compute_zero_motion()
        source_kind = self._effective_source_kind()
        cameras = tuple(f"observation.images.{cam}" for cam in self._camera_order)

        if n == 0 or "episode.parquet" not in files:
            status = "empty"
        elif self.dataset_ref:
            status = "ready"
        else:
            status = "local_only"

        manifest: dict[str, Any] = {
            "schema_version": 1,
            "status": status,
            "client_episode_id": self.client_episode_id,
            "dataset_ref": self.dataset_ref,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "deployment_id": self.deployment_id,
            "session_id": self.session_id,
            "robot_id": self.robot_id,
            "task": self.task,
            "source_kind": source_kind,
            "fps": self.fps,
            "frame_count": n,
            "duration_seconds": round(duration_s, 4),
            "bytes": total_bytes,
            "state_dim": state_dim,
            "action_dim": action_dim,
            "cameras": list(cameras),
            "takeover_count": self._takeover_count,
            "takeover_frames": self._takeover_frames,
            "dropped_frames": self._dropped_frames,
            "dropped_frame_ratio": round(dropped_ratio, 6),
            "has_nonfinite": self._has_nonfinite,
            "zero_motion": zero_motion,
            "outcome": outcome,
            "recorded_at": self.recorded_at,
            "finished_at": datetime.now(UTC).isoformat(),
            "files": files,
            "keep_local": self.keep_local,
            "writer_error": self._writer_error,
            "metadata": self.extra_metadata,
        }
        _atomic_write_json(self.manifest_path, manifest)

        self._summary = EpisodeSummary(
            client_episode_id=self.client_episode_id,
            directory=self.directory,
            manifest_path=self.manifest_path,
            status=status,
            files=tuple(files),
            bytes=total_bytes,
            frame_count=n,
            fps=self.fps,
            duration_seconds=round(duration_s, 4),
            state_dim=state_dim,
            action_dim=action_dim,
            cameras=cameras,
            source_kind=source_kind,
            takeover_count=self._takeover_count,
            takeover_frames=self._takeover_frames,
            dropped_frames=self._dropped_frames,
            dropped_frame_ratio=round(dropped_ratio, 6),
            has_nonfinite=self._has_nonfinite,
            zero_motion=zero_motion,
            writer_error=self._writer_error,
        )
        return self._summary
