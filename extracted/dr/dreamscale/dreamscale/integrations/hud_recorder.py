"""Record attended robot tasks on HUD: one job per session, one graded trace per task.

Each executed task streams measured and commanded joints, the model's action
chunks and one H.264 video per camera to a HUD trace. The operator's grade,
entered while the arms hold their final pose, becomes the trace reward. HUD
never drives the robot: Dreamscale's control loop runs unchanged and recording
happens on a worker thread, so a slow upload drops recorded frames, never
control ticks.
"""

from __future__ import annotations

import asyncio
import math
import os
import queue
import re
import threading
import uuid
from dataclasses import asdict, dataclass, is_dataclass

from dreamscale.model_names import public_model
from dreamscale.policy.types import RunHooks

# H.264 Main@3.0, which HUD's trace viewer pins, tops out near 720x576.
_MAX_VIDEO_PIXELS = 720 * 576
# About three seconds of 30 Hz frames before recording drops instead of buffering.
_QUEUE_TICKS = 90
_GRADE_WORDS = {
    "y": 1.0, "yes": 1.0, "s": 1.0, "success": 1.0, "pass": 1.0,
    "n": 0.0, "no": 0.0, "f": 0.0, "fail": 0.0, "failure": 0.0,
}
GRADE_PROMPT = "HUD grade: y success · n failure · 0–1 partial (+ optional note) · Enter skips:"


class HudUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class Grade:
    reward: float
    note: str | None = None

    @property
    def success(self):
        return self.reward >= 1.0


def parse_grade(text):
    """'y', 'n' or a 0–1 score, optionally followed by a note; None for an unclear answer."""
    word, _, note = text.strip().partition(" ")
    reward = _GRADE_WORDS.get(word.lower())
    if reward is None:
        try:
            reward = float(word)
        except ValueError:
            return None
        if not math.isfinite(reward) or not 0.0 <= reward <= 1.0:
            return None
    return Grade(reward, note.strip() or None)


def prompt_grade(read, print_fn=print):
    """Ask until the answer is a grade; Enter, EOF or Ctrl+C (``read`` -> None) skips."""
    while True:
        answer = read(GRADE_PROMPT)
        if not answer:
            return None
        grade = parse_grade(answer)
        if grade is not None:
            return grade
        print_fn("Enter y, n, or a score from 0 to 1.")


def task_slug(instruction):
    """Repeated instructions share a slug, so HUD groups their success rate."""
    slug = re.sub(r"[^a-z0-9]+", "-", instruction.lower()).strip("-")
    return slug[:80].rstrip("-") or "task"


def video_frame(rgb):
    """Downsample by striding until the frame fits the viewer's H.264 level."""
    height, width = rgb.shape[:2]
    stride = max(1, math.ceil(math.sqrt(height * width / _MAX_VIDEO_PIXELS)))
    return rgb[::stride, ::stride] if stride > 1 else rgb


class _Platform:
    """The few hud SDK calls used here, imported only when --hud is requested."""

    def __init__(self):
        from dreamscale.integrations import hud as integration

        key = integration.api_key()
        if not key:
            raise HudUnavailable(f"HUD is not set up. Run: {integration.SETUP_COMMAND}")
        # hud reads its key from the environment when its settings first load.
        os.environ[integration.API_KEY_ENV] = key
        try:
            from hud.settings import settings
            from hud.telemetry import exporter
            from hud.telemetry.robot import TraceRecorder
            from hud.utils.platform import PlatformClient
        except ImportError as exc:
            raise HudUnavailable(
                f"HUD support is not installed. Run: {integration.SETUP_COMMAND}"
            ) from exc
        settings.api_key = key
        if not settings.telemetry_enabled:
            raise HudUnavailable("HUD telemetry is disabled; unset HUD_TELEMETRY_ENABLED.")
        self.web_url = settings.hud_web_url.rstrip("/")
        self._client = PlatformClient.from_settings()
        self._recorder = TraceRecorder
        self._exporter = exporter

    async def post(self, path, body):
        await self._client.apost(path, json={k: v for k, v in body.items() if v is not None})

    def recorder(self, *, trace_id, fps, prompt, joints):
        joints = list(joints)
        return self._recorder(
            trace_id=trace_id,
            fps=fps,
            prompt=prompt,
            action_names=joints,
            state_names={"joint_positions": joints, "commanded_joint_positions": joints},
            # Blocks only this module's worker thread, never the control loop.
            lossless_video=True,
        )

    def flush(self, timeout):
        return self._exporter.flush(timeout=timeout)


class HudJob:
    """One HUD job for a `dreamscale run <robot> --hud` session."""

    def __init__(
        self, *, model, robot, name=None, metadata=None, platform=None, print_fn=print
    ):
        self.platform = platform or _Platform()
        self.model = model
        self.name = name or f"{public_model(model)} on {robot}"
        self.metadata = dict(metadata or {})
        self.print_fn = print_fn
        self.id = uuid.uuid4().hex
        self.traces = 0
        self._opened = False

    @property
    def url(self):
        return f"{self.platform.web_url}/jobs/{uuid.UUID(self.id)}"

    async def start(self, instruction, *, frames, joints, fps, metadata=None):
        """Open a trace. ``frames()`` returns the latest {camera: RGB array} from any
        thread without blocking; ``joints`` names the measured and commanded values."""
        trace_id = uuid.uuid4().hex
        entered = False
        try:
            if not self._opened:
                await self.platform.post(
                    f"/trace/job/{self.id}/enter", {"name": self.name, "group": 1}
                )
                self._opened = True
                self.print_fn(f"HUD job: {self.url}")
            await self.platform.post(
                f"/trace/{trace_id}/enter",
                {"job_id": self.id, "task_slug": task_slug(instruction), "model": self.model},
            )
            entered = True
            recorder = self.platform.recorder(
                trace_id=trace_id, fps=fps, prompt=instruction, joints=joints
            )
        except Exception as exc:
            if entered:  # never leave a trace running on HUD
                await self.platform.post(
                    f"/trace/{trace_id}/exit",
                    {"status": "error", "error": f"{type(exc).__name__}: {exc}"},
                )
            # An untracked evaluation rollout is worse than none; nothing has moved yet.
            raise HudUnavailable(
                f"HUD could not record this task ({type(exc).__name__}: {exc}); arms not moved. "
                "Check the network, or run: dreamscale integrations hud setup"
            ) from exc
        self.traces += 1
        return HudEpisode(
            self.platform,
            trace_id,
            recorder,
            frames=frames,
            metadata={**self.metadata, **(metadata or {}), "instruction": instruction},
            print_fn=self.print_fn,
        )

    def close(self, timeout=60.0):
        if not self._opened:
            return
        if not self.platform.flush(timeout):
            self.print_fn(f"HUD upload unconfirmed after {timeout:g}s; some video may be missing.")
        self.print_fn(f"HUD job: {self.url} ({self.traces} traces)")


class HudEpisode:
    """One executed task. Hooks enqueue; a worker thread reads frames and records."""

    def __init__(self, platform, trace_id, recorder, *, frames, metadata, print_fn=print):
        self.platform = platform
        self.trace_id = trace_id
        self.recorder = recorder
        self.frames = frames
        self.metadata = metadata
        self.print_fn = print_fn
        self.result = None
        self.error = None
        self.dropped = 0
        self.recorded = 0
        self._measured = None
        self._recording_error = None
        self._queue = queue.Queue(_QUEUE_TICKS)
        self._finished = False
        self._worker = threading.Thread(target=self._record, name="dreamscale-hud", daemon=True)
        self._worker.start()

    def measured(self, positions):
        """The latest measured joint positions, in ``joints`` order; any thread."""
        self._measured = [float(v) for v in positions]

    def hooks(self, existing=None):
        existing = existing or RunHooks()

        def chain(own, other):
            def emit(event):
                try:
                    own(event)
                except Exception:  # recording must never stop the robot
                    pass
                if other is not None:
                    other(event)

            return emit

        return RunHooks(**{
            **{name: getattr(existing, name) for name in RunHooks.__dataclass_fields__},
            "on_dispatch": chain(self._dispatch, existing.on_dispatch),
            "on_chunk": chain(self._chunk, existing.on_chunk),
            "on_summary": chain(self._summary, existing.on_summary),
        })

    def _put(self, item):
        try:
            self._queue.put_nowait(item)
        except queue.Full:
            self.dropped += 1

    def _dispatch(self, event):
        self._put(("observation", event.action_index, self._measured, event.accepted_action))

    def _chunk(self, event):
        self._put(("chunk", event.base_action_index, event.actions))

    def _summary(self, result):
        self.result = result

    def finish_sync(self, grade=None):
        """``finish`` for synchronous callers (no running event loop)."""
        asyncio.run(self.finish(grade))

    def _record(self):
        while (item := self._queue.get()) is not None:
            try:
                if item[0] == "chunk":
                    self.recorder.record_inference(item[2], tick=item[1])
                    continue
                _, tick, measured, commanded = item
                data = {camera: video_frame(rgb) for camera, rgb in self.frames().items()}
                if measured is not None:
                    data["joint_positions"] = measured
                data["commanded_joint_positions"] = commanded
                self.recorder.record_observation(data, tick=tick)
                self.recorded += 1
            except Exception as exc:
                self._recording_error = f"{type(exc).__name__}: {exc}"

    def stop_recording(self, error=None):
        """Stop at the task boundary, before homing, and flush video tails."""
        if not self._worker.is_alive():
            return
        self.error = error
        self._queue.put(None)
        self._worker.join()
        try:
            self.recorder.close()
        except Exception as exc:
            self._recording_error = self._recording_error or f"{type(exc).__name__}: {exc}"

    async def finish(self, grade=None):
        """Report the outcome once; an ungraded trace has no reward."""
        if self._finished:
            return
        self._finished = True
        await asyncio.to_thread(self.stop_recording)
        run = asdict(self.result) if is_dataclass(self.result) else None
        metadata = {
            **self.metadata,
            "run": run,
            "recorded_ticks": self.recorded,
            "dropped_ticks": self.dropped,
            "recording_error": self._recording_error,
            "operator_grade": None if grade is None else asdict(grade) | {
                "success": grade.success,
            },
        }
        failed = self.error is not None and not isinstance(self.error, asyncio.CancelledError)
        body = {
            "status": "error" if failed and grade is None else "completed",
            "error": f"{type(self.error).__name__}: {self.error}" if failed else None,
            "reward": None if grade is None else grade.reward,
            "evaluation_result": None if grade is None else {
                "reward": grade.reward,
                "done": True,
                "content": grade.note,
                "info": {"grader": "operator", "success": grade.success},
            },
            "metadata": metadata,
        }
        try:
            await self.platform.post(f"/trace/{self.trace_id}/exit", body)
        except Exception as exc:
            self.print_fn(f"HUD trace report failed: {type(exc).__name__}: {exc}")
            return
        outcome = "ungraded" if grade is None else f"reward {grade.reward:g}"
        self.print_fn(f"HUD trace recorded ({outcome}).")
