"""A verl process's Probe session (RL plan §6.5): the run handle (the launcher's run joined as producer `verl`, or a
run of its own without the launcher), the recorder, and the trainer wraps it installs. One per process: the training
process's starts with its first `Tracking` with the `probe` backend; the fully async rollouter's (producer
`verl-rollouter`, its validation only) when it builds its validation logger. Why: DESIGN.md."""

from __future__ import annotations

import math
import threading
from collections.abc import Mapping
from typing import Any

from probe.foundation.safe_warn import safe_warn as _diagnostics

from .. import _rl_owner
from .._live import refuse_commands
from .live import COMMAND_REFUSAL
from .phases import PhaseClock, install_phase_timer
from .recorder import VerlRecorder
from .runs import (
    get_resume_folder, get_external_id, get_names, get_rewind_step, get_run_config, get_run_name, read_resume_step,
)
from .trainers import FAMILIES, RollouterFamily, TrainerFamily, TrainerWraps, build_mapper

#: The producer the verl training process writes samples as.
PRODUCER = "verl"
#: The fully async rollouter's own producer: its validation samples, written from its process. Never declared on the
#: plan (it seals only the steps it validated at, so capture never waits on it for a training step).
ROLLOUTER_PRODUCER = "verl-rollouter"
#: verl's actor update metrics (`rename_dict(..., "actor/")`, `ray_trainer.py:1371`, `v1/trainer_base.py:1878`): a
#: logged row with one means this process just updated the actor.
ACTOR_METRIC_PREFIX = "actor/"

_ACTIVE: VerlSession | None = None
_START_LOCK = threading.Lock()
#: `register(**init_kwargs)`: how this process opens or joins its run (a client, a project).
_INIT_KWARGS: dict[str, Any] = {}


class VerlSession:
    """One process's recording: ``run`` is its handle; ``is_owner`` when it opened the run itself. A training
    session keeps verl's timed blocks as phases (``phases``); the rollouter's (``is_rollouter``) records validation
    only."""

    def __init__(self, run: Any, *, is_owner: bool, floor: int = 0, is_rollouter: bool = False) -> None:
        self.run = run
        self.is_owner = is_owner
        self.guard = _rl_owner.HookGuard("verl")
        self.samples = run.samples.as_producer(ROLLOUTER_PRODUCER if is_rollouter else PRODUCER)
        self.recorder = VerlRecorder(self.samples, floor=floor, is_eval_only=is_rollouter)
        self.phases = None if is_rollouter else PhaseClock()
        self.wraps = TrainerWraps(get_active_session)
        self._trainers: set[int] = set()
        self._is_finished = False
        self._is_hooks_checked = False

    def setup_trainer(self, trainer: Any, family: TrainerFamily) -> None:
        """Once per trainer: its tokenizer decodes, its step count goes in the plan."""
        if id(trainer) in self._trainers:
            return
        self._trainers.add(id(trainer))
        self.recorder.set_mapper(build_mapper(trainer))
        self.recorder.plan_steps(family.get_total_steps(trainer))

    def log_metrics(self, data: Mapping[str, Any], step: Any) -> None:
        """A verl metrics row as metrics at ``step``: finite numbers only (tables and text stay verl's)."""
        if not isinstance(step, int) or isinstance(step, bool):
            return
        row = {str(key): number for key, value in data.items() if (number := _to_number(value)) is not None}
        if row:
            self.run.log(row, step=step)
        phases = self.phases.take_reported(data) if self.phases is not None else []
        if phases:
            self.samples.record_phases(step, phases)

    def check_hooks(self, data: Mapping[str, Any]) -> None:
        """Once this process logs an actor update, its recorder must have taken a training batch: a wrap that ran is
        not enough (`TrainerWraps._get_recording` can step aside without a word). None taken: warn once, and flag
        this producer on the plan so capture says why it answers "no"."""
        if self._is_hooks_checked or not any(str(key).startswith(ACTOR_METRIC_PREFIX) for key in data):
            return
        self._is_hooks_checked = True
        if self.recorder.accepted_batches:
            return
        _diagnostics.warn(
            "probe.integrations.verl: verl updated the actor in this process, but Probe recorded no training batch "
            "(its trainer hooks never ran, or every record failed), so this run's samples are not captured; its plan "
            "is flagged adapter_hooks_missing. Metrics are still recorded. Please report it with your verl version.")
        self.samples.plan(adapter_hooks_missing=True)

    def record_checkpoint(self, trainer: Any, step: int) -> None:
        """`{default_local_dir}/global_step_{N}` (`v1/trainer_base.py:952-954`) holds the whole trainer state:
        recorded where it is, never uploaded or read."""
        import os

        from probe.sdk.artifact.hashing import local_file_uri

        folder = os.path.join(str(trainer.config.trainer.default_local_dir), f"global_step_{step}")
        _rl_owner.stamp_checkpoint(self.run, folder)  # first: a telemetry failure below never skips it
        self.run.log_artifact(
            f"global_step_{step}", path=folder, kind="checkpoint", reference=True, allow_missing=True,
            step_index=step, meta={"framework": "verl"}, strict=False,
        )
        uri = folder if "://" in folder else local_file_uri(os.path.abspath(folder))
        self.recorder.record_checkpoint(step, {"uri": uri, "step": step})

    def finish(self, status: str) -> None:
        """This producer's end: what it holds journaled; its lease released (the launcher closes the run), or the
        run closed behind the close barrier when this process opened it."""
        global _ACTIVE
        if self._is_finished:
            return
        self._is_finished = True
        if _ACTIVE is self:
            _ACTIVE = None  # the wraps stop recording; a later `probe` Tracking starts a new session
        final_step = self.recorder.close()
        if self.is_owner:
            _rl_owner.close_run(self.run, self.samples, final_step=final_step, should_finish=True, status=status)
        else:
            self.run.finish(status)


def get_session_key(config: Any, init_kwargs: Mapping[str, Any]) -> str | None:
    """The key a session opens its run with: the job's project and experiment, or the name its init kwargs chose
    (`runs.get_external_id`); None when it has neither project nor experiment."""
    project, experiment = get_names(config)
    return get_external_id(config, init_kwargs.get("name")) if (project or experiment) else None


def start_session(project_name: Any, experiment_name: Any, config: Any) -> VerlSession:
    """This process's session, started once: under the launcher (`PROBE_RUN_ID`) it joins the run as producer
    `verl`; without it, it opens a run named for the experiment (reopened with a rewind on a resume)."""
    global _ACTIVE
    with _START_LOCK:
        if _ACTIVE is not None:
            return _ACTIVE
        from probe.sdk.settings.settings import env_run_id

        resume = read_resume_step(config)
        floor = get_rewind_step(resume) if resume > 0 else 0
        init_kwargs = dict(_INIT_KWARGS)
        should_sample_hardware = init_kwargs.pop("should_sample_hardware", None)
        if env_run_id():
            from probe.sdk.run.samples import attach_producer

            run = attach_producer(PRODUCER, client=init_kwargs.get("client"),
                                  should_sample_hardware=should_sample_hardware)
            _rl_owner.send_missing_config(run, get_run_config(config))
            is_owner = False
        else:
            project, experiment = get_names(config)
            run, is_owner = _rl_owner.open_run(
                name=get_run_name(experiment_name or experiment),
                external_id=get_session_key(config, init_kwargs),
                rewind_step=floor or None, config=get_run_config(config), init_kwargs=init_kwargs,
                resume_from=get_resume_folder(config, resume), should_stamp_checkpoints=True,
            )
        session = VerlSession(run, is_owner=is_owner, floor=floor)
        session.samples.plan(producers=[PRODUCER])
        refuse_commands(session.samples, COMMAND_REFUSAL)
        session.wraps.install()
        install_phase_timer(get_phase_clock)
        if not any(family.get_class() is not None for family in FAMILIES):
            _diagnostics.warn("probe.integrations.verl: no verl trainer class is imported in this process, so only "
                              "metrics are recorded here (samples come from the process that trains).")
        _ACTIVE = session
        return session


def start_rollouter_session(owner: Any) -> VerlSession | None:
    """The fully async rollouter's session, when ``owner`` is the rollouter and this process joins a launcher's run
    (`PROBE_RUN_ID`): its validation passes are recorded here, the trainer never sees their samples. None for any
    other owner, or when this process already records."""
    global _ACTIVE
    with _START_LOCK:
        if _ACTIVE is not None or owner is None or not RollouterFamily().is_base_of(type(owner)):
            return None
        from probe.sdk.settings.settings import Mode, env_run_id, resolve_mode

        if not env_run_id() or resolve_mode(None) is Mode.DISABLED:
            return None
        from probe.sdk.run.samples import attach_producer

        init_kwargs = dict(_INIT_KWARGS)
        run = attach_producer(ROLLOUTER_PRODUCER, client=init_kwargs.get("client"), should_sample_hardware=False)
        session = VerlSession(run, is_owner=False, is_rollouter=True)
        session.wraps.install()
        _ACTIVE = session
        return session


def get_active_session() -> VerlSession | None:
    return _ACTIVE


def get_phase_clock() -> PhaseClock | None:
    """The clock verl's timers report to in this process: the active training session's."""
    session = _ACTIVE
    return session.phases if session is not None else None


def set_init_kwargs(init_kwargs: dict[str, Any]) -> None:
    """What `probe.init` (or the producer join) gets in this process: a client, a project, `should_sample_hardware`."""
    _INIT_KWARGS.clear()
    _INIT_KWARGS.update(init_kwargs)


def _to_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return float(value)
    item = getattr(value, "item", None)  # numpy and torch scalars
    if callable(item) and not isinstance(value, (int, float)):
        try:
            value = item()
        except Exception:  # noqa: BLE001 -- not a scalar: not a metric
            return None
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    return None
