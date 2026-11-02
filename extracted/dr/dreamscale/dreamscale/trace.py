"""Opt-in bounded, camera-free Rerun recording. Install dreamscale[trace]."""

from __future__ import annotations

import json
import queue
import threading
import time
from dataclasses import asdict, fields
from math import degrees
from pathlib import Path

import numpy as np
from dreamscale_transport import catalog

from dreamscale.policy.runtime.contract import runtime_contract_for_model
from dreamscale.policy.types import RunHooks

_COLORS = {
    "raw": (168, 85, 247),
    "old": (148, 163, 184),
    "merged": (245, 158, 11),
    "requested": (245, 158, 11),
    "accepted": (34, 197, 94),
    "measured": (56, 189, 248),
}
_ROLES = ("top", "left", "right")


def observation_frame(observation, role):
    """The frame an observation carries for a camera role, or None: a typed observation's
    ``<role>_frame`` (SO-101, YAM, Franka), else the frame a robot observation keys
    ``observation.images.<role>`` (Universal Robots, deployments)."""
    frame = getattr(observation, f"{role}_frame", None)
    if frame is None:
        cameras = getattr(observation, "cameras", None)
        if isinstance(cameras, tuple):
            frame = dict(cameras).get(f"observation.images.{role}")
    return frame if isinstance(frame, np.ndarray) else None


class TraceRecorder:
    """One recording per managed run, with durable summary even if events drop.

    hooks() can compose existing hooks. on_request borrows the observation only
    during the callback; optional RGB inputs are copied then, never re-acquired.
    measured() accepts state already read by an adapter; it does no hardware I/O.
    Writer faults do not alter control. close() reports them in status.json.
    """

    def __init__(
        self, directory, *, images=False, strategy=None, model=None, contract=None,
        execution_mode=None, camera_roles=_ROLES, layout=None,
    ):
        try:
            import rerun as rr
        except ImportError as exc:
            raise RuntimeError(
                "Install recording support: pip install 'dreamscale[trace]'"
            ) from exc
        from dreamscale.trace_views import blueprint

        # With neither, YAM's default model's (the trace views are YAM diagnostics).
        self.contract = contract or runtime_contract_for_model(
            model or catalog.robot_models("yam")[0])
        # The joint layout views draw on: the model's own, or the robot's (layout) when
        # the model's rows declare none. Metadata keeps the model's contract.
        self.view = layout or self.contract
        if not self.view.joint_groups:
            raise ValueError("trace views require a declared joint layout")
        self._groups = self.view.joint_groups
        self._grippers = self.view.gripper_indices
        self._names = (
            ("left", "right")
            if len(self._groups) == 2
            else tuple(f"arm_{i + 1}" for i in range(len(self._groups)))
        )
        self._normalized_grippers = set(self._grippers).issubset(
            self.view.normalized_gripper_indices
        )
        self.directory = Path(directory).expanduser().resolve()
        self.directory.mkdir(parents=True, exist_ok=False)
        self.path = self.directory / "rollout.rrd"
        self.images = bool(images)
        self._roles = tuple(camera_roles)
        self._origin = time.monotonic_ns()
        self._rr = rr
        self._stream = rr.RecordingStream("dreamscale_async_inference")
        self._stream.save(self.path, default_blueprint=blueprint(self.view))
        self._queue = queue.Queue(maxsize=512)
        self._lock = threading.Lock()
        self._closing = threading.Event()
        self._closed = False
        self._image_bytes = 0
        self._dropped = 0
        self._written = 0
        self._error = None
        self._summary = None
        self._cleanup = None
        self._last_dispatch = None
        self._last_request = None
        self._last_chunk = None
        self._merge_details = {}
        self._series = set()
        self._metadata = {
            "schema_version": 1,
            "model": model,
            "images": self.images,
            "contract": asdict(self.contract),
            "strategy": asdict(strategy) if strategy is not None else None,
            "timeline": "elapsed monotonic seconds; horizon x is control index",
            "disagreement": "absolute raw-to-raw difference; missing overlap is NaN, not zero",
            "color_scale": (
                f"arms in {self.view.joint_unit}; grippers "
                + (
                    "[0,1]"
                    if self._normalized_grippers
                    else "raw checkpoint units, automatic range"
                )
                + "; display scales are not safety bands"
            ),
        }
        if execution_mode is not None:
            self._metadata["execution_mode"] = execution_mode
            self._metadata["smoothing_applied"] = execution_mode != "sync"
        self._thread = threading.Thread(target=self._write, name="dreamscale-trace", daemon=True)
        self._thread.start()
        self._put("metadata", self._metadata)

    def hooks(self, existing=None):
        callbacks = {
            "on_request": self._request,
            "on_queue_merge": lambda e: self._put("queue_merge", e, e.accepted_ns),
            "on_action": lambda e: self._put("action", e),
            "on_dispatch": lambda e: self._put("dispatch", e, e.started_ns),
            "on_timing": lambda e: self._put("timing", e),
            "on_buffer": lambda e: self._put("buffer", e),
            "on_merge": lambda e: self._put("merge", e),
            "on_summary": self._record_summary,
        }
        existing = existing or RunHooks()

        def compose(first, second):
            def emit(event):
                try:
                    first(event)
                except Exception as exc:
                    self._error = f"{type(exc).__name__}: {exc}"
                if second is not None:
                    second(event)

            return emit

        return RunHooks(
            **{
                field.name: compose(callbacks[field.name], getattr(existing, field.name))
                if field.name in callbacks
                else getattr(existing, field.name)
                for field in fields(RunHooks)
            }
        )

    def measured(self, positions, *, velocities=None, capture_unix_s=None):
        """Record existing state, with acquisition time distinct from receipt time."""
        self._put(
            "measured",
            {
                "positions": tuple(float(x) for x in positions),
                "velocities": None if velocities is None else tuple(float(x) for x in velocities),
                "capture_unix_s": capture_unix_s,
                "received_unix_s": time.time(),
            },
        )

    def _record_summary(self, result):
        self._summary = asdict(result)  # independent of bounded/lossy event queue
        self._put("summary", self._summary)

    def _request(self, event):
        observation = event.observation
        data = {
            "submitted_ns": event.submitted_ns,
            "submitted_unix_ns": time.time_ns(),
            "base_action_index": event.base_action_index,
            "actions_remaining": event.actions_remaining,
            "camera_capture_times_ns": getattr(observation, "camera_capture_times_ns", None),
            "hold_action": getattr(observation, "hold_action", None),
        }
        frames = [observation_frame(observation, role) for role in self._roles]
        image_size = sum(frame.nbytes for frame in frames if isinstance(frame, np.ndarray))
        # Reserve the memory budget before copying. Never block waiting for disk.
        with self._lock:
            copy_images = self.images and self._image_bytes + image_size <= 32 * 1024**2
            if copy_images:
                self._image_bytes += image_size
            elif self.images:
                self._dropped += 1
        try:
            if copy_images:
                data["frames"] = tuple(
                    frame.copy() if isinstance(frame, np.ndarray) else None for frame in frames
                )
            self._put("request", data, event.submitted_ns, image_size if copy_images else 0)
        except Exception:
            with self._lock:
                if copy_images:
                    self._image_bytes -= image_size
                self._dropped += 1

    def _put(self, kind, event, timestamp=None, image_bytes=0):
        with self._lock:
            if self._closing.is_set() or self._error is not None:
                self._dropped += 1
                self._image_bytes -= image_bytes
                return
            try:
                self._queue.put_nowait((kind, event, timestamp or time.monotonic_ns(), image_bytes))
            except queue.Full:
                self._dropped += 1
                self._image_bytes -= image_bytes

    def close(self, *, timeout_s=5.0, cleanup=None):
        if cleanup is not None:
            self._cleanup = cleanup
        if not self._closed:
            self._closing.set()
            self._thread.join(timeout=max(0.0, timeout_s))
            self._closed = not self._thread.is_alive()
        status = {
            **self._metadata,
            "events_written": self._written,
            "events_dropped": self._dropped,
            "writer_error": self._error,
            "writer_finished": not self._thread.is_alive(),
            "pending_events": self._queue.qsize(),
            "summary": self._summary,
            "cleanup": self._cleanup,
        }
        from dreamscale.camera_codec import status_summary

        codec = status_summary()
        if codec:  # a robot with a camera codec device: its stream in 1 s windows
            status["camera_codec"] = codec
        temporary = self.directory / "status.json.tmp"
        temporary.write_text(json.dumps(status, indent=2, allow_nan=False) + "\n")
        temporary.replace(self.directory / "status.json")
        return status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            self.close()
        except Exception:
            if exc is None:
                raise

    def _write(self):
        last_flush = time.monotonic()
        try:
            while not self._closing.is_set() or not self._queue.empty():
                try:
                    kind, event, timestamp, size = self._queue.get(timeout=0.1)
                except queue.Empty:
                    if time.monotonic() - last_flush >= 1:
                        self._stream.flush(timeout_sec=0.5)
                        last_flush = time.monotonic()
                    continue
                try:
                    self._stream.set_time(
                        "elapsed", duration=max(0, timestamp - self._origin) / 1e9
                    )
                    self._log(kind, event)
                    self._written += 1
                finally:
                    with self._lock:
                        self._image_bytes -= size
                if time.monotonic() - last_flush >= 1:
                    self._stream.flush(timeout_sec=0.5)
                    last_flush = time.monotonic()
        except Exception as exc:
            self._error = f"{type(exc).__name__}: {exc}"
        finally:
            try:
                self._stream.flush(timeout_sec=2.0)
                self._stream.disconnect()
            except Exception as exc:
                self._error = self._error or f"{type(exc).__name__}: {exc}"

    def _scalar(self, path, value, color=None):
        if value is None:
            return
        if color is not None and path not in self._series:
            self._stream.log(path, self._rr.SeriesLines(colors=color), static=True)
            self._series.add(path)
        self._stream.log(path, self._rr.Scalars(float(value)))

    def _vector(self, prefix, kind, values):
        if values is None or len(values) != self.contract.action_dim:
            return
        for group_index, (side, group) in enumerate(zip(self._names, self._groups, strict=True)):
            path = f"{prefix}/{side}/{kind}"
            if path not in self._series:
                self._stream.log(
                    path,
                    self._rr.SeriesLines(
                        colors=[_COLORS[kind]] * len(group),
                        names=[f"{kind} j{joint + 1}" for joint in range(len(group))],
                    ),
                    static=True,
                )
                self._series.add(path)
            self._stream.log(path, self._rr.Scalars([values[i] for i in group]))
            if prefix == "joints" and group_index < len(self._grippers):
                self._scalar(
                    f"grippers/{side}/{kind}", values[self._grippers[group_index]], _COLORS[kind]
                )

    def _log(self, kind, event):
        rr, stream = self._rr, self._stream
        if kind in {"metadata", "summary"}:
            stream.log("summary", rr.TextDocument(json.dumps(event, indent=2)))
        elif kind == "request":
            self._last_request = event["submitted_ns"]
            self._scalar("queue/in_flight", 1)
            self._scalar("queue/request_base", event["base_action_index"])
            self._vector("joints", "measured", event["hold_action"])
            for role, frame in zip(self._roles, event.get("frames", ()), strict=False):
                if frame is not None:
                    stream.log(f"cameras/{role}", rr.Image(frame))
            captures = event["camera_capture_times_ns"]
            if captures is not None:
                for role, captured in zip(self._roles, captures, strict=True):
                    self._scalar(
                        f"latency/camera_age/{role}",
                        (event["submitted_unix_ns"] - captured) / 1e6,
                    )
        elif kind == "action":
            self._vector("joints", "requested", event.action)
            self._scalar("queue/hold", int(event.stalled))
            self._scalar("queue/control_step", event.action_index)
        elif kind == "dispatch":
            self._vector("joints", "accepted", event.accepted_action)
            self._scalar("latency/dispatch_ms", (event.completed_ns - event.started_ns) / 1e6)
            if self._last_dispatch is not None:
                previous = self._last_dispatch
                dt = (event.started_ns - previous.started_ns) / 1e9
                if dt > 0:
                    self._vector(
                        "velocity",
                        "accepted",
                        [
                            (b - a) / dt
                            for a, b in zip(
                                previous.accepted_action, event.accepted_action, strict=True
                            )
                        ],
                    )
            self._last_dispatch = event
        elif kind == "measured":
            self._vector("joints", "measured", event["positions"])
            self._vector("velocity", "measured", event["velocities"])
            if event["capture_unix_s"] is not None:
                self._scalar(
                    "latency/state_age_ms",
                    (event["received_unix_s"] - event["capture_unix_s"]) * 1000,
                )
        elif kind == "buffer":
            for name in ("remaining", "capacity", "in_flight"):
                self._scalar(f"queue/{name}", getattr(event, name))
        elif kind == "timing":
            for name, value in asdict(event).items():
                if name.endswith("_ms"):
                    self._scalar(f"latency/{name}", value)
        elif kind == "merge":
            self._merge_details = asdict(event)
            stream.log("merge_details", rr.TextDocument(json.dumps(asdict(event), indent=2)))
            for name in (
                "transition_steps",
                "arm_speed_rad_s",
                "new_action_weight",
                "correction_gain",
                "correction_rate_ratio",
                "stale_steps",
                "overlap_steps",
            ):
                self._scalar(f"smoothing/{name}", getattr(event, name))
        elif kind == "queue_merge":
            self._log_queue(event)

    def _log_queue(self, event):
        rr, stream = self._rr, self._stream
        chunk = event.chunk
        indices = chunk.action_indices or tuple(range(len(chunk.actions)))
        raw = {
            chunk.base_action_index + i: action
            for i, action in zip(indices, chunk.actions, strict=True)
            if chunk.base_action_index + i >= chunk.accepted_action_index
        }
        old, old_raw, after = dict(event.before), dict(event.before_raw), dict(event.after)
        self._scalar(
            "latency/submission_to_merge_ms", (event.accepted_ns - event.submitted_ns) / 1e6
        )
        if self._last_chunk is not None:
            self._scalar("latency/chunk_interval_ms", (event.accepted_ns - self._last_chunk) / 1e6)
        self._last_chunk = event.accepted_ns
        steps = sorted(raw)
        trajectories = (("raw", raw), ("old", old), ("merged", after))
        # Preserve full values/indices separately from the scaled display geometry.
        for name, values in (*trajectories, ("old_raw", old_raw)):
            stream.log(f"targets/{name}", rr.TextDocument(json.dumps(values)))
        stream.log(
            "merge_details",
            rr.TextDocument(
                json.dumps(
                    {
                        **self._merge_details,
                        "incoming_control_indices": steps,
                        "request_submitted_ns": event.submitted_ns,
                        "accepted_ns": event.accepted_ns,
                    },
                    indent=2,
                )
            ),
        )
        if not steps:
            stream.log("disagreement", rr.Clear(recursive=True))
            stream.log("horizon", rr.Clear(recursive=True))
            return
        differences = np.full((len(steps), self.contract.action_dim), np.nan)
        for row, step in enumerate(steps):
            if step in old_raw:
                differences[row] = np.abs(np.asarray(raw[step]) - old_raw[step])
        stream.log(
            "disagreement/arms",
            rr.Tensor(
                differences[:, self.view.joint_indices],
                dim_names=["incoming row", "arm coordinate"],
                value_range=[0, degrees(0.1) if self.view.joint_unit == "deg" else 0.1],
            ),
        )
        stream.log(
            "disagreement/grippers",
            rr.Tensor(
                differences[:, self._grippers],
                dim_names=["incoming row", "gripper"],
                **({"value_range": [0, 1]} if self._normalized_grippers else {}),
            ),
        )
        for side, group in zip(self._names, self._groups, strict=True):
            for joint in range(len(group)):
                all_points = [
                    (step, action[group[joint]])
                    for _, values in trajectories
                    for step, action in values.items()
                ]
                xmin, xmax = min(x for x, _ in all_points), max(x for x, _ in all_points)
                low, high = min(y for _, y in all_points), max(y for _, y in all_points)
                padding = max(0.002, (high - low) * 0.1)
                low, high = low - padding, high + padding
                root = f"horizon/{side}/{joint}"
                width, height = 720.0, 200.0
                stream.log(
                    f"{root}/axes",
                    rr.LineStrips2D(
                        [[(0, 0), (0, height), (width, height)]],
                        colors=(120, 120, 120),
                    ),
                )
                stream.log(
                    f"{root}/labels",
                    rr.Points2D(
                        [(0, height + 18), (width, height + 18), (-45, 0), (-45, height)],
                        radii=0,
                        colors=(110, 110, 110),
                        show_labels=True,
                        labels=[
                            f"step {xmin}",
                            f"step {xmax}",
                            f"{high:.4f} {self.view.joint_unit}",
                            f"{low:.4f} {self.view.joint_unit}",
                        ],
                    ),
                )
                for name, values in trajectories:
                    # Split missing control indices; never draw a fictitious bridge.
                    strips, current, prior = [], [], None
                    for step in sorted(values):
                        if prior is not None and step != prior + 1:
                            strips.append(current)
                            current = []
                        current.append(
                            (
                                width * (step - xmin) / max(1, xmax - xmin),
                                height * (high - values[step][group[joint]]) / (high - low),
                            )
                        )
                        prior = step
                    if current:
                        strips.append(current)
                    stream.log(
                        f"{root}/{name}",
                        rr.LineStrips2D(
                            strips,
                            colors=_COLORS[name],
                            radii=1.2,
                        ),
                    )
