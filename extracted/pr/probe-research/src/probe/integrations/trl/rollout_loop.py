"""AsyncGRPO's live samples (S1 C1): each rollout is a live sample, recorded in the spawned rollout process where TRL
generates it, as producer `trl-rollout`. `ProbeRolloutLoop` stands where the worker's `loop_cls` was and wraps the loop
it builds. Key `{version}:{group}:r{j}` (j = dispatch order in the group), never a sample key; the scored sample
carries `j` and the version to the main process in its own `metrics`. Line refs are `huggingface/trl@4ae4d34a86f3`
`trl/experimental/async_grpo/async_rollout_worker.py`. Why: DESIGN.md "Live samples"."""

from __future__ import annotations

import asyncio
import concurrent.futures
import contextvars
import functools
import logging
import os
import socket
import threading
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Any

from probe.generated.samples import AttemptOutcome, AttemptPhase

from .. import _rl_owner
from .._live import LiveAttempts, refuse_commands
from .live import COMMAND_REFUSAL
from .rows import RowReader

logger = logging.getLogger(__name__)

#: The rollout process's producer: it writes live samples only, never seals, so the plan never declares it.
ROLLOUT_PRODUCER = "trl-rollout"
#: What a scored sample carries to the main process in its `metrics`: floats, because TRL's collator averages every
#: value there (`async_grpo_trainer.py:588-592`). The main process takes them out before TRL's reader reads them.
CARRY_ROLLOUT = "_probe_rollout"
CARRY_VERSION = "_probe_rollout_version"
#: How long the first rollout waits for this process to join the run (off the event loop) before rollouts go
#: unrecorded until the join is done; the join starts as the loop is built, well before the first rollout.
START_WAIT_SECONDS = 5.0
#: How long the producer's release may wait for its outbox when the loops stop: TRL waits 15 s for the process
#: to exit, then terminates it (`AsyncRolloutWorker.stop`).
RELEASE_FLUSH_SECONDS = 8.0
UNSCORED = "reward_fn: no reward function scored this rollout"

_KEY: contextvars.ContextVar[str | None] = contextvars.ContextVar("probe_trl_rollout_key", default=None)


def make_rollout_key(version: int, group_id: int, ordinal: int) -> str:
    """One rollout's key. The `r` keeps it apart from every sample key (`{version}:{group}:{n}`, n = drain order)."""
    return f"{version}:{group_id}:r{ordinal}"


def take_rollout_key(sample: Any) -> str | None:
    """The live sample a drained `RolloutSample` came from, both carried numbers taken out of its `metrics` (always:
    TRL then never reads them). None when it carries none."""
    metrics = getattr(sample, "metrics", None)
    if not isinstance(metrics, MutableMapping):
        return None
    ordinal, version = metrics.pop(CARRY_ROLLOUT, None), metrics.pop(CARRY_VERSION, None)
    if not isinstance(ordinal, (int, float)) or not isinstance(version, (int, float)):
        return None
    return make_rollout_key(int(version), int(getattr(sample, "group_id", 0)), int(ordinal))


class ProbeRolloutLoop:
    """Stands where `AsyncRolloutWorker._loop_cls` was (`:1543`): `_child_main` calls it in the spawned process with
    the loop's arguments (`:382`). It builds the real loop, never a subclass of it, and wraps that instance. Pickled
    by reference into the child, so it holds only the class, the run id and plain values."""

    def __init__(self, loop_cls: Any, *, run_id: str, rows: RowReader | None = None,
                 reward_max: float | None = None) -> None:
        self.loop_cls = loop_cls
        self.run_id = run_id
        self.rows = rows or RowReader()
        self.reward_max = reward_max

    def __call__(self, **kwargs: Any) -> Any:
        loop = self.loop_cls(**kwargs)
        try:
            RolloutRecorder(loop, self).install()
        except Exception as exc:  # noqa: BLE001 -- fail open: the loop runs unrecorded
            logger.warning("Probe could not record this TRL rollout process's rollouts; TRL continues: %s", exc)
        return loop


@dataclass
class _Group:
    """A group as its first rollout saw it: the version it was made at (`:838-851`) and its task."""

    version: int
    start: dict
    dispatched: int = 0


@dataclass
class _Rollout:
    key: str
    version: int
    ordinal: int


class RolloutRecorder:
    """One rollout loop's live samples: `generate_one` starts and ends each (`:854`), `generate_one_turn` is its
    progress, `_score_group` grades it (`:962`), `close` ends what the loop left (`:678`)."""

    def __init__(self, loop: Any, spec: ProbeRolloutLoop) -> None:
        self.loop = loop
        self.spec = spec
        self.guard = _rl_owner.HookGuard("TRL rollout process")
        self.attempts: LiveAttempts | None = None
        self._where = {"host": socket.gethostname(), "worker": f"pid:{os.getpid()}"}
        self._groups: dict[int, _Group] = {}
        #: id(rollout.completion) -> the rollout: `_score_group` builds each sample with that same list (`:1470`).
        self._generated: dict[int, _Rollout] = {}
        self._turns: dict[str, int] = {}
        self._run: Any = None
        self._deadline: float | None = None
        self._joined: concurrent.futures.Future = concurrent.futures.Future()

    def install(self) -> None:
        threading.Thread(target=self._join, name="probe-trl-rollout", daemon=True).start()
        loop = self.loop
        generate_one, turn = loop.generate_one, loop.generate_one_turn
        score, close = loop._score_group, loop.close

        @functools.wraps(generate_one)
        def call_generate_one(prompt: Any, tools: Any, *args: Any, **kwargs: Any) -> Any:
            group_id = kwargs.get("group_id", args[0] if args else 0)
            coroutine = generate_one(prompt, tools, *args, **kwargs)
            rollout = self.guard.call("a rollout", self._make_rollout, prompt, group_id)
            return coroutine if rollout is None else self._run_rollout(coroutine, *rollout)

        @functools.wraps(turn)
        async def call_generate_one_turn(*args: Any, **kwargs: Any) -> Any:
            key = _KEY.get()
            number = self._turns.get(key, 0) + 1 if key is not None else 0
            if key is not None:
                self.guard.call("a model call", self._send_progress, key, AttemptPhase.GENERATING,
                                activity=f"model call {number}", turns=number - 1)
            result = await turn(*args, **kwargs)
            if key is not None:
                self._turns[key] = number
            return result

        @functools.wraps(score)
        async def call_score_group(group: Any, *args: Any, **kwargs: Any) -> Any:
            try:
                samples = await score(group, *args, **kwargs)
            except BaseException as exc:
                self.guard.call("a scored group", self._end_group_error, group, exc)
                raise
            self.guard.call("a scored group", self._end_group, group, samples)
            return samples

        @functools.wraps(close)
        async def call_close(*args: Any, **kwargs: Any) -> Any:
            try:
                return await close(*args, **kwargs)
            finally:
                self.guard.call("the rollout process's close", self._close)

        for name, value in (("generate_one", call_generate_one), ("generate_one_turn", call_generate_one_turn),
                            ("_score_group", call_score_group), ("close", call_close)):
            object.__setattr__(loop, name, value)

    # -- one rollout -------------------------------------------------------------------------------------------
    def _make_rollout(self, prompt: Any, group_id: int) -> tuple[_Rollout, dict]:
        """At the dispatch (`:854`), in the same synchronous stretch that made the group: its version and task are
        read at its first rollout (a later `model_version` may already be newer), and the row the loop is on
        (`_row_index`, `:1136`) is the group's."""
        group = self._groups.get(group_id)
        if group is None:
            version = int(self.loop.model_version)
            group = _Group(version, self._make_start(prompt, version, group_id))
            self._groups[group_id] = group
        ordinal, group.dispatched = group.dispatched, group.dispatched + 1
        rollout = _Rollout(make_rollout_key(group.version, group_id, ordinal), group.version, ordinal)
        return rollout, {**group.start, "key": rollout.key}

    def _make_start(self, prompt: Any, version: int, group_id: int) -> dict:
        row = None
        try:
            row = self.loop.dataset[int(self.loop._row_index)]
        except Exception:  # noqa: BLE001 -- a dataset that cannot be indexed keys the task by prompt
            pass
        task = self.spec.rows.read_task(row, prompt)
        return {"task_key": task["task_key"], "scenario": task.get("scenario") or {},
                "group_key": f"{version}:{group_id}", "weight_version": version, **self._where}

    async def _run_rollout(self, coroutine: Any, rollout: _Rollout, start: dict) -> Any:
        try:
            attempts = await self._get_attempts()
        except BaseException:
            coroutine.close()
            raise
        if attempts is None or not attempts.start([start]):
            return await coroutine
        token = _KEY.set(rollout.key)
        try:
            result = await coroutine
        except asyncio.CancelledError:  # the loops stopping (`:936-939`)
            self._turns.pop(rollout.key, None)
            self.guard.call("a rollout", self._end, [{"key": rollout.key, "outcome": AttemptOutcome.ABORTED}])
            raise
        except BaseException as exc:
            self._turns.pop(rollout.key, None)
            self.guard.call("a rollout", attempts.end_error, [rollout.key], exc)
            raise
        finally:
            _KEY.reset(token)
        self.guard.call("a rollout", self._mark_generated, rollout, result)
        return result

    def _mark_generated(self, rollout: _Rollout, result: Any) -> None:
        """Generated: it waits for its group's reward functions."""
        self._generated[id(result.completion)] = rollout
        self._send_progress(rollout.key, AttemptPhase.SCORING, activity="reward functions",
                            turns=self._turns.pop(rollout.key, None))

    def _send_progress(self, key: str, phase: AttemptPhase, *, activity: str, turns: int | None) -> None:
        if self.attempts is not None:
            self.attempts.send_progress([key], phase=phase, activity=activity, turns=turns)

    # -- a group -----------------------------------------------------------------------------------------------
    def _end_group(self, group: Any, samples: list) -> None:
        """Each rollout ends with its reward, `group.rewards[i]` beside `group.completions[i]` (`:1385`); a group
        TRL dropped whole (all rewards equal: `[]`) ends `dropped`. Each sample names its rollout."""
        rollouts = self._take_group(group)
        rewards = getattr(group, "rewards", None)
        ends = []
        for index, rollout in enumerate(rollouts):
            if rollout is None:
                continue
            if not samples:
                ends.append({"key": rollout.key, "outcome": AttemptOutcome.DROPPED})
                continue
            reward = _get_reward(rewards, index)
            if reward is None:
                ends.append({"key": rollout.key, "outcome": AttemptOutcome.ERROR, "error_reason": "reward_fn",
                             "error_message": UNSCORED})
            else:
                ends.append({"key": rollout.key, "outcome": self.attempts.get_outcome(reward)})
        self._end(ends)
        by_completion = {id(completion): rollout
                         for completion, rollout in zip(group.completions, rollouts) if rollout is not None}
        for sample in samples or ():
            rollout = by_completion.get(id(sample.completion))
            if rollout is not None and isinstance(sample.metrics, MutableMapping):
                sample.metrics[CARRY_ROLLOUT] = float(rollout.ordinal)
                sample.metrics[CARRY_VERSION] = float(rollout.version)

    def _end_group_error(self, group: Any, error: BaseException) -> None:
        keys = [rollout.key for rollout in self._take_group(group) if rollout is not None]
        if self.attempts is not None and keys:
            self.attempts.end_error(keys, error)

    def _take_group(self, group: Any) -> list[_Rollout | None]:
        self._groups.pop(getattr(group, "group_id", None), None)
        return [self._generated.pop(id(completion), None) for completion in getattr(group, "completions", ())]

    def _end(self, ends: list[dict]) -> None:
        if self.attempts is not None and ends:
            self.attempts.end(ends)

    # -- the process -------------------------------------------------------------------------------------------
    def _close(self) -> None:
        """The loops stopped: every rollout generated whose group was never scored ends `dropped`, then this
        process's producer is released, its outbox delivered, before TRL's join times out."""
        self._end([{"key": rollout.key, "outcome": AttemptOutcome.DROPPED} for rollout in self._generated.values()])
        self._generated.clear()
        run, self._run = self._run, None
        if run is not None:
            run.finish("completed", flush_timeout=RELEASE_FLUSH_SECONDS)

    def _join(self) -> None:
        """Join the run the trainer opened (its id came with this loop: `track()` opens it, not a launcher) as
        `trl-rollout`, with this process's Probe settings (a spawned child inherits the environment)."""
        try:
            from probe.sdk.run.samples import attach_producer

            run = attach_producer(ROLLOUT_PRODUCER, run_id=self.spec.run_id, should_sample_hardware=False,
                                  should_capture_logs=False)
            samples = run.samples.as_producer(ROLLOUT_PRODUCER)
            refuse_commands(samples, COMMAND_REFUSAL)
            self._run = run
            self.attempts = LiveAttempts(samples, reward_max=self.spec.reward_max)
            self._joined.set_result(self.attempts)
        except Exception as exc:  # noqa: BLE001 -- fail open: the rollouts run unrecorded
            logger.warning("Probe could not record this TRL rollout process's rollouts; TRL continues: %s", exc)
            self._joined.set_result(None)

    async def _get_attempts(self) -> LiveAttempts | None:
        """This process's live samples: rollouts wait for the join until `START_WAIT_SECONDS` after the first one
        asked (never blocking the event loop); after that, a rollout that finds it not done goes unrecorded."""
        if self._joined.done():
            return self._joined.result()
        now = asyncio.get_running_loop().time()
        if self._deadline is None:
            self._deadline = now + START_WAIT_SECONDS
        if now >= self._deadline:
            return None
        try:
            return await asyncio.wait_for(asyncio.shield(asyncio.wrap_future(self._joined)), self._deadline - now)
        except asyncio.TimeoutError:
            return None


def _get_reward(rewards: Any, index: int) -> float | None:
    try:
        reward = float(rewards[index])
    except (TypeError, ValueError, IndexError):
        return None
    return reward if reward == reward else None
