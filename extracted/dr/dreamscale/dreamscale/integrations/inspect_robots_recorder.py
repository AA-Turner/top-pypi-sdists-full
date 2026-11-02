"""Record attended `dreamscale run <robot>` tasks as an Inspect Robots eval log.

One session is one eval log (`<log_dir>/<task>_<id>.json`), the format
`inspect-robots run` writes and `inspect-robots view` renders. Each instruction is a
scene and each executed task one trial (epoch), with its executed actions in
`actions/<run_id>/<scene>-e<epoch>.jsonl`. The operator grades a task while the arms
hold its final pose; the grade is the trial's `operator` score. Dreamscale's control
loop runs unchanged: recording appends to memory from its hooks, and files are
written between tasks.
"""

from __future__ import annotations

import asyncio
import json
import os
import statistics
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from importlib import metadata as package_metadata
from pathlib import Path
from typing import Any

from dreamscale.policy.types import RunHooks

GRADE_PROMPT = "Grade: y success · n failure · 0–1 partial (+ optional note) · Enter skips:"
POLICY = "dreamscale"
SCORER = "operator"
# How a run stopped, in Inspect Robots' termination vocabulary.
_TERMINATION = {"action_limit": "max_steps", "interrupted": "operator_end", "act_callback": "done"}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


@dataclass
class _Trial:
    scene_id: str
    instruction: str
    epoch: int
    score: float | None  # None: errored, never scored
    judgement: str | None
    note: str | None
    termination: str | None
    error: str | None
    metadata: dict[str, Any] = field(default_factory=dict)
    steps: int = 0
    latencies_s: list[float] = field(default_factory=list)


class InspectRobotsJob:
    """One session's eval log; `start()` opens a trial, `close()` finalizes the log."""

    def __init__(self, *, model, embodiment, log_dir="logs", task=None, scenes=(),
                 max_steps=None, print_fn=print):
        self.model = model
        self.embodiment = f"dreamscale_{embodiment.name}"
        self.labels = list(embodiment.joints)
        self.task = task or "adhoc"
        self.max_steps = max_steps
        self.log_dir = Path(log_dir)
        suffix = uuid.uuid4().hex[:8]
        self.run_id = f"{datetime.now(UTC):%Y%m%d_%H%M%S}_{suffix}"
        self.path = self.log_dir / f"{self.task.replace('/', '_')}_{suffix}.json"
        self.print_fn = print_fn
        # Queued (scene id, instruction) pairs a registered task runs, in order.
        self._queue = list(scenes)
        self._total = len(self._queue)
        # Every scene seen, in order: scene id -> instruction.
        self._scenes: dict[str, str] = {}
        self._adhoc: dict[str, str] = {}
        self._trials: list[_Trial] = []
        self._metadata: dict[str, Any] = {}
        self._created = _now()
        self._started = time.monotonic()
        self._closed = False

    def announce(self) -> None:
        """Before a registered task: the scene order the operator sets up, trial by trial."""
        if self._queue:
            order = ", ".join(scene for scene, _ in self._queue)
            self.print_fn(f"Inspect Robots task {self.task}: {self._total} trials, scenes in "
                          f"order: {order}.")

    async def start(self, instruction, *, frames=None, joints=None, fps=None, metadata=None):
        if self._queue and self._queue[0][1] == instruction:
            scene_id = self._queue.pop(0)[0]
            self.print_fn(
                f"Recording {scene_id} · trial {self._total - len(self._queue)} of {self._total}."
            )
        else:
            if instruction not in self._adhoc:
                self._adhoc[instruction] = f"scene-{len(self._adhoc)}"
            scene_id = self._adhoc[instruction]
        self._scenes.setdefault(scene_id, instruction)
        epoch = sum(1 for t in self._trials if t.scene_id == scene_id)
        self._metadata = dict(metadata or {})
        return InspectRobotsEpisode(self, scene_id, instruction, epoch, fps)

    def _add(self, trial: _Trial) -> None:
        self._trials.append(trial)
        self._write("started")

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if not self._trials:
            return
        self._write("success")
        self.print_fn(f"Inspect Robots log: {self.path} · view: inspect-robots view {self.log_dir}")

    def _write(self, status: str) -> None:
        from inspect_robots.log import (
            SCHEMA_VERSION,
            EvalLog,
            EvalResults,
            EvalSpec,
            EvalStats,
            SceneResult,
        )

        meta = self._metadata
        scenes = []
        for scene_id, instruction in self._scenes.items():
            trials = [t for t in self._trials if t.scene_id == scene_id]
            if not trials:
                continue
            scored = [t.score for t in trials if t.score is not None]
            scenes.append(SceneResult(
                scene_id=scene_id,
                status="error" if any(t.error for t in trials) else "success",
                reduced={SCORER: statistics.fmean(scored)} if scored else {},
                epochs=tuple({} if t.score is None else {SCORER: t.score} for t in trials),
                error=next((t.error for t in trials if t.error), None),
                instruction=instruction,
                operator_judgements=tuple(t.judgement for t in trials),
                judgement_sources=tuple("prompt" if t.judgement else None for t in trials),
                operator_notes=tuple(t.note for t in trials),
                operator_messages=tuple(() for _ in trials),
                trial_metadata=tuple(t.metadata for t in trials),
                termination_reasons=tuple(t.termination for t in trials),
                policy_transcripts=tuple(None for _ in trials),
            ))
        latencies = [s for t in self._trials for s in t.latencies_s]
        means = [s.reduced[SCORER] for s in scenes if SCORER in s.reduced]
        log = EvalLog(
            version=SCHEMA_VERSION,
            status=status,
            eval=EvalSpec(
                task=self.task,
                policy=POLICY,
                embodiment=self.embodiment,
                created=self._created,
                inspect_robots_version=package_metadata.version("inspect-robots"),
                policy_config={
                    key: meta.get(key) for key in (
                        "model", "mode", "rtc", "context", "checkpoint", "region",
                        "provider", "speed", "keep_warm", "action_smoothing",
                        "dreamscale_version",
                    )
                },
                embodiment_info={
                    "control_hz": meta.get("action_hz"),
                    "capabilities": ["self_paced"],
                    "is_simulated": False,
                    "rig": meta.get("rig"),
                },
                max_steps=self.max_steps,
                policy_checkpoint=meta.get("checkpoint") or self.model,
                grader=SCORER,
            ),
            results=EvalResults(
                total_scenes=len(scenes),
                total_trials=len(self._trials),
                metrics={SCORER: statistics.fmean(means)} if means else {},
                errored_trials=sum(1 for t in self._trials if t.score is None),
            ),
            stats=EvalStats(
                started_at=self._created,
                completed_at=_now(),
                duration_s=time.monotonic() - self._started,
                total_steps=sum(t.steps for t in self._trials),
                mean_inference_latency_s=statistics.fmean(latencies) if latencies else None,
            ),
            samples=tuple(scenes),
        )
        _write_atomic(self.path, json.dumps(log.to_dict(), allow_nan=False, indent=2) + "\n")


class InspectRobotsEpisode:
    """One executed task: its dispatched actions, timing, summary and grade."""

    grade_prompt = GRADE_PROMPT

    def __init__(self, job, scene_id, instruction, epoch, fps):
        self.job, self.scene_id, self.instruction, self.epoch = job, scene_id, instruction, epoch
        self.fps = fps
        self._actions: list[tuple[int, tuple[float, ...]]] = []
        self._latencies_s: list[float] = []
        self._summary = None
        self._failure: BaseException | None = None
        self._actions_path: str | None = None

    def hooks(self) -> RunHooks:
        return RunHooks(
            on_dispatch=self._on_dispatch, on_timing=self._on_timing, on_summary=self._on_summary,
        )

    def _on_dispatch(self, event) -> None:
        self._actions.append((event.action_index, tuple(event.accepted_action)))

    def _on_timing(self, event) -> None:
        self._latencies_s.append(event.obs_to_action_ms / 1000.0)

    def _on_summary(self, result) -> None:
        self._summary = result

    def measured(self, position) -> None:
        """Measured joints are not part of an Inspect Robots trial record."""

    def stop_recording(self, failure=None) -> None:
        self._failure = failure
        relative = Path("actions") / self.job.run_id / f"{self.scene_id}-e{self.epoch}.jsonl"
        header = {
            "kind": "header", "run_id": self.job.run_id, "scene_id": self.scene_id,
            "epoch": self.epoch, "action_dim": len(self.job.labels), "labels": self.job.labels,
        }
        lines = [json.dumps(header, allow_nan=False)] + [
            json.dumps({"t": t, "action": list(action)}, allow_nan=False)
            for t, action in self._actions
        ]
        try:
            _write_atomic(self.job.log_dir / relative, "\n".join(lines) + "\n")
            self._actions_path = relative.as_posix()
        except (OSError, ValueError) as exc:
            self.job.print_fn(f"Inspect Robots action log not saved: {type(exc).__name__}.")

    async def finish(self, grade=None) -> None:
        failure = self._failure
        cancelled = isinstance(failure, (asyncio.CancelledError, KeyboardInterrupt))
        errored = failure is not None and not cancelled
        summary = self._summary
        if cancelled:
            termination = "operator_end"
        elif errored:
            termination = None
        else:
            termination = _TERMINATION.get(getattr(summary, "stop_reason", None))
        if errored:
            score, judgement = None, None
        elif grade is None:
            score, judgement = 0.0, None
        else:
            score = float(grade.reward)
            judgement = (
                "success" if score >= 1.0 else "failure" if score <= 0.0 else "partial"
            )
        dreamscale = {
            "model": self.job.model,
            "session_id": self.job._metadata.get("session_id"),
            "actions": len(self._actions),
        }
        if summary is not None:
            dreamscale.update(
                policy_calls=summary.policy_calls, underruns=summary.underruns,
                elapsed_s=summary.elapsed_s,
            )
        self.job._add(_Trial(
            scene_id=self.scene_id,
            instruction=self.instruction,
            epoch=self.epoch,
            score=score,
            judgement=judgement,
            note=None if grade is None else grade.note,
            termination=termination,
            error=f"{type(failure).__name__}: {failure}" if errored else None,
            metadata={
                **({"actions": self._actions_path} if self._actions_path else {}),
                "dreamscale": dreamscale,
            },
            steps=len(self._actions),
            latencies_s=self._latencies_s,
        ))
