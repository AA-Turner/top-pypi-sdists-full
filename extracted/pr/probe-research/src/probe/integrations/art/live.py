"""ART's live samples (rl-next W37): `track(model)` never sees a rollout start (ART awaits the user's own coroutines,
spike A1), so the recipe decorates the rollout: `@tracker.record_rollout(task_key=...)`. Each call is a live sample
`art:<uuid4>` from its start to its return; the returned `Trajectory` carries the key as
`metadata["probe_attempt_key"]`, which its final sample names as `attempt_key`. No command: `COMMAND_REFUSAL`.
Line refs are `OpenPipe/ART@414acc5`. Why: DESIGN.md "Live samples"."""

from __future__ import annotations

import contextlib
import contextvars
import functools
import inspect
import uuid
from collections import OrderedDict
from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, Any

from probe.sdk.run.samples.rollout import RolloutCapture

from .._live import LiveAttempts

if TYPE_CHECKING:
    from .art import ArtTracker

#: The refusal the server answers a cancel, retry or watch of an ART sample with (the W30 spike, A2).
COMMAND_REFUSAL = ("a cancelled rollout raises in your gather, and ART's default `max_exceptions=0` stops the "
                   "step")
#: Where a trajectory carries its live sample's key (a string `MetadataValue`, `trajectories.py:46`).
ATTEMPT_KEY = "probe_attempt_key"
KEY_PREFIX = "art:"
#: Rollouts whose files wait for their trajectory's sample (`apply_files`); past it the oldest are forgotten (a
#: trajectory never logged nor trained).
MAX_WAITING_ROLLOUTS = 4096

#: The live sample the current rollout task is (for `ArtTracker.send_progress`).
_CURRENT: contextvars.ContextVar[str | None] = contextvars.ContextVar("probe_art_rollout", default=None)

#: A task key, or how to read one from the rollout's own arguments.
TaskKeySpec = str | Callable[..., Any]


class ArtLive:
    """One ART model's live samples, written as its producer (`art`); made when its run opens."""

    def __init__(self, tracker: ArtTracker) -> None:
        self._tracker = tracker
        self.attempts: LiveAttempts | None = None
        #: Each finished rollout's export (files + span), by its key, until its trajectory's part is mapped.
        self._exports: OrderedDict[str, dict] = OrderedDict()

    def open(self, samples: Any, reward_max: float | None) -> None:
        self.attempts = LiveAttempts(samples, reward_max=reward_max)

    def wrap_rollout(self, function: Callable[..., Any], task_key: TaskKeySpec) -> Callable[..., Any]:
        """``function``, a rollout (async, or returning an awaitable), with each call a live sample. Its result and its
        error are the caller's."""
        tracker = self._tracker

        @functools.wraps(function)
        async def call_rollout(*args: Any, **kwargs: Any) -> Any:
            if tracker.is_finished:
                return await _call(function, args, kwargs)
            await tracker.guard.call_async("a live sample", tracker.ensure_run)
            key = tracker.guard.call("a live sample", self._start, task_key, args, kwargs)
            capture = tracker.guard.call("a rollout's files", RolloutCapture, tracker.run, key) if key else None
            token = _CURRENT.set(key)
            try:
                with capture if capture is not None else contextlib.nullcontext():
                    result = await _call(function, args, kwargs)
            except BaseException as exc:
                if key is not None:
                    tracker.guard.call("a live sample", self._end_error, key, exc)
                if capture is not None:  # the span closes; the files stay the run's, linked to no sample
                    await tracker.guard.call_async("a rollout's files", capture.export_async)
                raise
            finally:
                _CURRENT.reset(token)
            if key is not None:
                tracker.guard.call("a live sample", self._end, key, result)
            if capture is not None:
                exported = await tracker.guard.call_async("a rollout's files", capture.export_async)
                tracker.guard.call("a rollout's files", self._keep_export, key, exported)
            return result

        return call_rollout

    def apply_files(self, part: dict) -> dict:
        """``part`` (a trajectory's generator part) with the files and span its decorated rollout's own code
        attached (`probe.samples.attach_file` inside `record_rollout`), found by its `attempt_key`."""
        exported = self._exports.pop(part.get("attempt_key") or "", None)
        return RolloutCapture.update_part(part, exported)

    def send_progress(self, snapshot: Mapping[str, Any]) -> None:
        """The current rollout's progress (`phase`, `turns`, `tokens`, `activity`), when it runs decorated."""
        key = _CURRENT.get()
        if key is not None and self.attempts is not None:
            self.attempts.send_progress([key], **snapshot)

    # -- inside --------------------------------------------------------------------------------------------
    def _start(self, task_key: TaskKeySpec, args: tuple, kwargs: dict) -> str | None:
        attempts = self.attempts
        if attempts is None:
            return None
        task = task_key(*args, **kwargs) if callable(task_key) else task_key
        key = f"{KEY_PREFIX}{uuid.uuid4()}"
        start: dict[str, Any] = {"key": key, "task_key": str(task), **self._tracker.get_where()}
        step = self._tracker.get_cached_step()
        if isinstance(step, int):
            start["weight_version"] = step  # ART serves its latest step (`local/backend.py:885`)
        return key if attempts.start([start]) else None

    def _end(self, key: str, result: Any) -> None:
        """The rollout returned: its trajectories carry the key; it ends graded by its reward when one was set, else
        `ungraded` (an ART `Trajectory.reward` defaults to 0.0, so an unset one is no grade)."""
        trajectories = [item for item in (result if isinstance(result, (list, tuple)) else [result])
                        if isinstance(getattr(item, "metadata", None), dict)]
        rewards = []
        for trajectory in trajectories:
            trajectory.metadata.setdefault(ATTEMPT_KEY, key)
            if "reward" in (getattr(trajectory, "model_fields_set", None) or ()):
                rewards.append(trajectory.reward)
        attempts = self.attempts
        reward = max(rewards) if rewards else None
        attempts.end([{"key": key, "outcome": attempts.get_outcome(reward)}])

    def _keep_export(self, key: str, exported: Mapping[str, Any] | None) -> None:
        if not exported:
            return
        self._exports[key] = dict(exported)
        while len(self._exports) > MAX_WAITING_ROLLOUTS:
            self._exports.popitem(last=False)

    def _end_error(self, key: str, error: BaseException) -> None:
        self.attempts.end_error([key], error)


async def _call(function: Callable[..., Any], args: tuple, kwargs: dict) -> Any:
    """A rollout's result: awaited when it returns an awaitable (a coroutine function, a partial of one)."""
    result = function(*args, **kwargs)
    return await result if inspect.isawaitable(result) else result


def read_attempt_key(trajectory: Any) -> str | None:
    """The live sample a trajectory came from (`metadata["probe_attempt_key"]`), if a decorated rollout made it."""
    value = (getattr(trajectory, "metadata", None) or {}).get(ATTEMPT_KEY)
    return value if isinstance(value, str) and value else None
