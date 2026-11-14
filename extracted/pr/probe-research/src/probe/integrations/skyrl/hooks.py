"""The SkyRL hooks (RL plan §6.3): the generator's `generate` wrapped to record every call, the trainer's batch
conversion wrapped to record what a step trains on, and a callback for commits, checkpoints and seals. Instance
methods only; every hook fails open. Pure: duck-typed on SkyRL's objects (`NovaSky-AI/SkyRL@d87004689e3a`)."""

from __future__ import annotations

import functools
import math
import threading
from collections.abc import Mapping
from typing import Any

from probe.sdk.run.samples.points import TrainingGuard

from .. import _rl_owner
from .harbor import HarborJoin, is_harbor_generator
from .live import SkyrlLive
from .outputs import CallVersions
from .phases import PhaseClock
from .recorder import SkyrlRecorder
from .training import EvalPoints, setup_trainer_wraps, stamp_training_keys

#: A partial batch collected when the epoch ran out is thrown away untrained (`fully_async_trainer.py:560-575`).
EPOCH_END_DROP = "filter:epoch_exhausted"


class SkyrlHooks:
    """Wires one SkyRL training process to its recorder and Probe run handle."""

    def __init__(self, run: Any, recorder: SkyrlRecorder, guard: _rl_owner.HookGuard,
                 live: SkyrlLive | None = None) -> None:  # fmt: skip
        self.run = run
        self.recorder = recorder
        self.guard = guard
        #: Each rollout as a live sample (`live.py`), when the process records them.
        self.live = live
        self._client: Any = None
        #: The fully async trainer, whose step a generate call is scheduled at (`_get_scheduled_step`).
        self._async_trainer: Any = None
        #: SkyRL's Harbor generator: its trials join the samples (`harbor.HarborJoin`), else None.
        self.harbor: HarborJoin | None = None
        #: This process's timed blocks, sent as phases with the metrics row that reports them (`phases.py`).
        self.phases = PhaseClock()
        #: Each eval pass's per-trajectory rewards as per-sample metrics (`training/driver.py`).
        self.eval_points = EvalPoints(recorder.samples)
        #: Fails open for the per-sample metrics calls, saying what a failure costs them (`training/`).
        self.training_guard = TrainingGuard("SkyRL")

    # -- the generator -----------------------------------------------------------------------------------
    def wrap_generator(self, generator: Any, inference_client: Any) -> Any:
        """``generator.generate`` on this instance records each call. Its signature is kept: the fully async
        trainer reads it for `disable_tqdm` (`fully_async_trainer.py:990`)."""
        self._client = inference_client
        if is_harbor_generator(generator):
            join = HarborJoin(self.recorder, self.guard, live=self.live)
            if self.guard.call("the Harbor trials", join.install, generator):
                self.harbor = join
        elif self.live is not None:
            self.guard.call("the agent loops", self.live.wrap_loop, generator)
        original = generator.generate

        @functools.wraps(original)
        async def call_generate(input_batch: Any, *args: Any, **kwargs: Any) -> Any:
            first = self._get_weight_version()
            scheduled = self._get_scheduled_step()  # before the first await: the step the worker just read
            call_id = self.recorder.take_call()
            keys = self.guard.call("a live sample", self._start_live, input_batch, call_id, first, scheduled) or []
            token = self.live.enter_call(call_id) if self.live is not None else None
            try:
                output = await original(input_batch, *args, **kwargs)
            except BaseException as exc:
                if self.harbor is not None:  # a failed call's trials are never taken: forget them
                    self.guard.call("a Harbor trajectory", self.harbor.take, input_batch.get("trajectory_ids"))
                if keys:
                    self.guard.call("a live sample", self.live.end_error, keys, exc)
                raise
            finally:
                if token is not None:
                    self.live.exit_call(token)
            parts = self.guard.call("a generate call", self._record_generation, input_batch, output, first, scheduled,
                                    call_id)
            if parts:
                self.training_guard.call("per-sample eval metrics", self.eval_points.log, input_batch, output, parts)
            if keys:
                self.guard.call("a live sample", self.live.end_rows, parts or [], keys)
            return output

        object.__setattr__(generator, "generate", call_generate)
        return generator

    # -- the trainer -------------------------------------------------------------------------------------
    def wrap_trainer(self, trainer: Any, *, is_fully_async: bool) -> Any:
        """The batch conversion (what a step trains on, recorded before it trains, each row's key stamped for the
        workers) and the callback. The fully async trainer converts its groups through the same
        `convert_to_training_input` (`fully_async_trainer.py:1224`): the groups wrap only hands it the groups it
        dropped and reads an exhausted epoch's partial batch."""
        dropped_now = threading.local()  # the fully async conversion runs in a worker thread (`asyncio.to_thread`)
        if is_fully_async:
            self._async_trainer = trainer
            convert_groups = trainer.convert_generation_group_mini_batch_to_training_input
            collect = trainer._collect_generation_mini_batch

            @functools.wraps(convert_groups)
            def call_convert_groups(kept: Any, dropped: Any = None) -> Any:
                dropped_now.groups = list(dropped or [])
                try:
                    return convert_groups(kept, dropped)
                finally:
                    dropped_now.groups = None

            @functools.wraps(collect)
            async def call_collect(*args: Any, **kwargs: Any) -> Any:
                result = await collect(*args, **kwargs)
                self.guard.call("a discarded batch", self._record_exhausted, trainer, result)
                return result

            object.__setattr__(trainer, "convert_generation_group_mini_batch_to_training_input", call_convert_groups)
            object.__setattr__(trainer, "_collect_generation_mini_batch", call_collect)
        convert = trainer.convert_to_training_input

        @functools.wraps(convert)
        def call_convert(generator_output: Any, uids: Any) -> Any:
            row_keys = None
            if not is_fully_async:
                row_keys = self.guard.call("a training batch", self._record_sync_batch, trainer, generator_output)
            elif (dropped := getattr(dropped_now, "groups", None)) is not None:  # a fully async mini-batch
                row_keys = self.guard.call("a training batch", self._record_groups, trainer, generator_output,
                                           dropped)  # fmt: skip
            batch = convert(generator_output, uids)
            if row_keys is not None:  # each row's key rides to the policy workers (per-sample metrics, T3)
                self.training_guard.call("per-sample training metrics", stamp_training_keys, trainer, batch,
                                         row_keys)  # fmt: skip
            return batch

        object.__setattr__(trainer, "convert_to_training_input", call_convert)
        self.training_guard.call("per-sample training metrics", setup_trainer_wraps, trainer, self.training_guard)
        trainer.add_callback(ProbeCallback(self))
        return trainer

    def log_metrics(self, data: Mapping[str, Any], step: int) -> None:
        """A SkyRL tracker row as metrics at ``step``: finite numbers only (tables and text stay SkyRL's); the timed
        blocks it reports as `timing/<name>` as phases at that step."""
        row = {}
        for key, value in data.items():
            number = _to_number(value)
            if number is not None:
                row[str(key)] = number
        if row:
            self.run.log(row, step=step)
        phases = self.phases.take_reported(data)
        if phases:
            self.recorder.record_phases(step, phases)

    # -- inside ------------------------------------------------------------------------------------------
    def _get_weight_version(self) -> int | None:
        version = getattr(self._client, "weight_version", None)
        return version if isinstance(version, int) else None

    def _get_scheduled_step(self) -> int | None:
        """The fully async trainer's step as a generate call starts. Its worker sets the group's
        `global_step_when_scheduled` from the same counter just before the call, after waiting for a slot
        (`fully_async_trainer.py:983-997`, `:1006`); `batch_metadata.global_step` was stamped before that wait
        (`:969`), up to the staleness bound earlier. The sync trainer generates at its step: its metadata is right."""
        step = getattr(self._async_trainer, "global_step", None) if self._async_trainer is not None else None
        return step if isinstance(step, int) and not isinstance(step, bool) else None

    def _start_live(self, input_batch: Mapping[str, Any], call_id: int, first: int | None,
                    scheduled: int | None) -> list[str]:  # fmt: skip
        """The call's trajectories as live samples; a Harbor generator's are its tries instead (`live.watch_try`)."""
        if self.live is None or self.harbor is not None:
            return []
        version = self.recorder.get_version(first, fallback=_get_fallback_version(input_batch))
        return self.live.start_call(input_batch, call_id, version, scheduled)

    def _record_generation(self, input_batch: Mapping[str, Any], output: Mapping[str, Any], first: int | None,
                           scheduled: int | None = None, call_id: int | None = None) -> list[dict]:
        last = self._get_weight_version()
        fallback = _get_fallback_version(input_batch)
        versions = CallVersions(
            first=self.recorder.get_version(first, fallback=fallback),
            last=self.recorder.get_version(last, fallback=fallback),
        )
        trials = None
        if self.harbor is not None:
            trials = self.harbor.take(output.get("trajectory_ids") or input_batch.get("trajectory_ids"))
        return self.recorder.record_generation(input_batch, output, versions, harbor=trials, scheduled_step=scheduled,
                                               call_id=call_id)

    def _record_sync_batch(self, trainer: Any, generator_output: Mapping[str, Any]) -> list[list[str]]:
        return self.recorder.record_batch(int(trainer.global_step), generator_output, should_drop_leftovers=True)

    def _record_groups(self, trainer: Any, output: Mapping[str, Any], dropped: Any) -> list[list[str]]:
        """The fully async trainer's mini-batch, as it converts it: the kept groups' rows (concatenated and post-
        processed, `fully_async_trainer.py:1043-1224`) train at this step, each dropped (zero-variance) group's rows
        are stored drops. Returns each training row's sample keys, in order."""
        dropped_outputs = [group.generator_output for group in dropped]
        return self.recorder.record_batch(int(trainer.global_step), output, dropped=dropped_outputs)

    def _record_exhausted(self, trainer: Any, result: Any) -> None:
        """An epoch that ran out mid mini-batch: its partial batch and the zero-variance groups dropped while
        collecting it never reach the batch conversion (`fully_async_trainer.py:560-575`)."""
        kept, dropped, is_exhausted = result
        if not is_exhausted:
            return
        step = int(trainer.global_step)
        self.recorder.record_discarded(step, [group.generator_output for group in kept], EPOCH_END_DROP)
        self.recorder.record_discarded(step, [group.generator_output for group in dropped], "zero_variance")


class ProbeCallback:
    """A SkyRL `TrainingCallback` (duck-typed: the handler calls each event by name, `callbacks.py:145-147`)."""

    def __init__(self, hooks: SkyrlHooks) -> None:
        self._hooks = hooks

    def on_train_start(self, trainer: Any, callback_input: Any, control: Any) -> None:
        hooks = self._hooks
        client = getattr(trainer, "inference_engine_client", None)
        version = getattr(client, "weight_version", None)
        hooks.guard.call("train start", hooks.recorder.start, int(callback_input.global_step),
                         version if isinstance(version, int) else None)

    def on_step_end(self, trainer: Any, callback_input: Any, control: Any) -> None:
        self._hooks.guard.call("a commit", self._hooks.recorder.commit, int(callback_input.global_step))

    def on_save(self, trainer: Any, callback_input: Any, control: Any) -> None:
        self._hooks.guard.call("a checkpoint", self._record_checkpoint, callback_input)

    def on_log(self, trainer: Any, callback_input: Any, control: Any) -> None:
        self._hooks.guard.call("a seal", self._hooks.recorder.send_seals, int(callback_input.global_step))

    def on_train_end(self, trainer: Any, callback_input: Any, control: Any) -> None:
        return None

    on_epoch_start = on_epoch_end = on_step_start = on_eval_start = on_eval_end = on_train_end

    def _record_checkpoint(self, callback_input: Any) -> None:
        """`global_step_N/` holds the whole trainer state (GBs): recorded where it is, never uploaded or read."""
        path = callback_input.ckpt_path
        step = int(callback_input.global_step)
        if not path:
            return
        _rl_owner.stamp_checkpoint(self._hooks.run, path)  # first: a telemetry failure below never skips it
        self._hooks.run.log_artifact(
            f"global_step_{step}", path=str(path), kind="checkpoint", reference=True, allow_missing=True,
            step_index=step, meta={"framework": "skyrl"}, strict=False,
        )
        from probe.sdk.artifact.hashing import local_file_uri

        uri = str(path) if "://" in str(path) else local_file_uri(_get_absolute(str(path)))
        self._hooks.recorder.record_checkpoint(step, {"uri": uri, "step": step})


def _get_fallback_version(input_batch: Mapping[str, Any]) -> int | None:
    """No engine counter: a train call at step N runs on the weights of N-1 updates, an eval at N on N's."""
    metadata = input_batch.get("batch_metadata")
    step = getattr(metadata, "global_step", None)
    phase = getattr(metadata, "training_phase", None)
    return None if not isinstance(step, int) else (step if phase == "eval" else max(step - 1, 0))


def _get_absolute(path: str) -> str:
    import os

    return os.path.abspath(path)


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
