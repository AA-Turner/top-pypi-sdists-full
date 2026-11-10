"""Harbor inside SkyRL (RL plan §6.3, W22): SkyRL's `HarborGenerator` runs each trajectory as Harbor `Trial`s, retrying
a failed one (`examples/train_integrations/harbor/harbor_generator.py:360-469`). The join adds Probe's Harbor trial
hook to each of those trials, so a trial and SkyRL's rows for it merge into one sample: both key it by the trial's
`TrialResult.id`. Pure: duck-typed on SkyRL's and Harbor's objects. Why: DESIGN.md "Harbor inside SkyRL"."""

from __future__ import annotations

import contextvars
import functools
import sys
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .. import _rl_owner

#: SkyRL's Harbor generator (`harbor_generator.py:223`) and the method that runs one trajectory's trials (`:360`).
GENERATOR_CLASS = "HarborGenerator"
AGENT_LOOP = "_harbor_agent_loop"
#: The name `_harbor_agent_loop` creates each trial through (`harbor_generator.py:17, 401`).
TRIAL_NAME = "Trial"


@dataclass(frozen=True)
class HarborTrajectory:
    """What SkyRL's rows for one trajectory take from its Harbor trials: the final trial's key and task."""

    key: str
    task_key: str
    scenario: Mapping[str, Any]
    #: The trial broke (an exception): Harbor's part names why, so SkyRL's rows leave their own guess out.
    has_error: bool


@dataclass
class _Trajectory:
    """One `_harbor_agent_loop` call: the trials it created, in order."""

    hooks: list[Any] = field(default_factory=list)


_CURRENT: contextvars.ContextVar[_Trajectory | None] = contextvars.ContextVar("probe_harbor_trajectory", default=None)


def is_harbor_generator(generator: Any) -> bool:
    return any(cls.__name__ == GENERATOR_CLASS for cls in type(generator).__mro__) and callable(
        getattr(generator, AGENT_LOOP, None))


class HarborJoin:
    """Wires one `HarborGenerator`. Trials' parts go through ``sink`` (`SkyrlRecorder.record_parts`, so they are
    stamped with the step whose seal is next); `take` hands SkyRL's mapper each trajectory's trial."""

    def __init__(self, sink: Any, guard: _rl_owner.HookGuard, live: Any = None) -> None:
        self._sink = sink
        self._guard = guard
        #: Each try as a live sample keyed by its `TrialResult.id` (`live.SkyrlLive.watch_try`), when recorded.
        self._live = live
        #: id(TrajectoryID) -> (the TrajectoryID, its trials' outcome): the same object rides from the input batch
        #: into `_harbor_agent_loop` and into the output (`harbor_generator.py:340-350, 113, 170`).
        self._found: dict[int, tuple[Any, HarborTrajectory]] = {}

    def install(self, generator: Any) -> bool:
        """Wrap this instance's `_harbor_agent_loop`, and have its module's `Trial.create` hook each trial made
        inside one (a no-op anywhere else). False, with one warning, where Probe's Harbor connector is not installed
        (it ships in `probe-research[cli]`): SkyRL's rows are then recorded alone."""
        if _load_trial_hook() is None:
            from probe.foundation.safe_warn import safe_warn

            safe_warn.warn("probe.integrations.skyrl: SkyRL's Harbor trials are recorded as SkyRL rows only; install "
                           "probe-research[cli,harbor] beside SkyRL to merge each Harbor trial into its sample.")
            return False
        original = getattr(generator, AGENT_LOOP)

        @functools.wraps(original)
        async def call_agent_loop(*args: Any, **kwargs: Any) -> Any:
            trajectory_id = kwargs.get("trajectory_id", args[1] if len(args) > 1 else None)
            binding = _Trajectory()
            token = _CURRENT.set(binding)
            try:
                return await original(*args, **kwargs)
            finally:
                _CURRENT.reset(token)
                self._guard.call("a Harbor trajectory", self._keep, trajectory_id, binding)

        object.__setattr__(generator, AGENT_LOOP, call_agent_loop)
        _wrap_trial_class(sys.modules.get(type(generator).__module__), self)
        return True

    def take(self, trajectory_ids: Any) -> dict[int, HarborTrajectory]:
        """The trials behind ``trajectory_ids`` (an output's), keyed by `id(TrajectoryID)`, and forgotten."""
        found = {}
        for trajectory in trajectory_ids or ():
            entry = self._found.pop(id(trajectory), None)
            if entry is not None and entry[0] is trajectory:
                found[id(trajectory)] = entry[1]
        return found

    def attach(self, trial: Any) -> None:
        """A trial `_harbor_agent_loop` just created: Probe's hooks on it, as `harbor` parts (SkyRL writes the
        content); a retry names the try before it, which reads superseded."""
        binding = _CURRENT.get()
        if binding is None:
            return
        before = binding.hooks[-1].key if binding.hooks else None
        hook = _load_trial_hook()(trial, None, role="harbor", samples=self._sink, supersedes_key=before)
        binding.hooks.append(hook)
        if self._live is not None:
            self._guard.call("a live Harbor try", self._live.watch_try, trial, hook)

    def _keep(self, trajectory_id: Any, binding: _Trajectory) -> None:
        last = next((hook for hook in reversed(binding.hooks) if hook.attempt is not None), None)
        if trajectory_id is None or last is None:
            return
        head = last.attempt.parts[0]
        errors = [last.attempt.result.get("exception_info")] + [
            step.get("exception_info") for step in last.attempt.result.get("step_results") or ()
            if isinstance(step, Mapping)]
        self._found[id(trajectory_id)] = (trajectory_id, HarborTrajectory(
            key=last.attempt.key, task_key=str(head.get("task_key")), scenario=dict(head.get("scenario") or {}),
            has_error=any(isinstance(error, Mapping) and error.get("exception_type") for error in errors)))


def _load_trial_hook() -> Any:
    """Probe's Harbor trial hook (`connectors/harbor/runner.py` `record_trial_sample`), private to `probe-research-cli`:
    None where only the SDK is installed."""
    try:
        from probe.connectors.harbor.runner import record_trial_sample
    except ImportError:
        return None
    return record_trial_sample


def _wrap_trial_class(module: Any, join: HarborJoin) -> None:
    """The generator module's `Trial`, subclassed once so `create` also attaches the current join's hooks."""
    real = getattr(module, TRIAL_NAME, None) if module is not None else None
    if real is None or getattr(real, "_probe_join", None) is not None:
        if real is not None:
            real._probe_join = join  # a new generator in this process: the newest join hooks
        return

    class ProbeTrial(real):  # type: ignore[misc, valid-type]
        """Harbor's `Trial` (`trial/trial.py:469-523`), whose trials made inside a joined `_harbor_agent_loop`
        carry Probe's hooks."""

        _probe_join = join

        @classmethod
        async def create(cls, *args: Any, **kwargs: Any) -> Any:
            trial = await real.create(*args, **kwargs)
            cls._probe_join._guard.call("a Harbor trial", cls._probe_join.attach, trial)
            return trial

    ProbeTrial.__name__ = ProbeTrial.__qualname__ = real.__name__
    setattr(module, TRIAL_NAME, ProbeTrial)
