"""verl's live samples (rl-next W37): each agent loop is a live sample, recorded in the AgentLoopWorker process (a Ray
actor) as producer `verl-rollout`. `AgentLoopWorker._run_agent_loop` is wrapped on the class as its module loads (a
`sys.meta_path` hook from Probe's Ray setup hook), before Ray builds the actor class from it; each model call is
progress; the loop's return or raise is the end. Keys: `{split}:{step}:{uid}:s{session}` (V1, one per `rollout.n`
session) or `:p{position}` (the legacy batch's row), never a sample key; train samples name them, validation samples
read theirs from what `_compute_score` stamps on the loop's output (`stamp_output`), with the engine's stop reason. No
command: `COMMAND_REFUSAL`. Line refs are `verl-project/verl@b17218ba58a6`. Why: DESIGN.md "Live samples"."""

from __future__ import annotations

import asyncio
import concurrent.futures
import contextlib
import contextvars
import functools
import hashlib
import itertools
import json
import logging
import os
import socket
import threading
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from typing import Any

from probe.generated.samples import AttemptPhase

from .._live import LiveAttempts, refuse_commands
from .rows import LIVE_KEY_FIELD, STOP_REASON_FIELD, TASK_KEY_FIELD, Split, get_scenario
from .tool_loop import ROLLOUT_EVAL_FIELD, ROLLOUT_FIELD, open_recording, watch_tool_loop_imports
from .wrapping import guard, guard_async, is_wrapped, make_install, set_wrapped

logger = logging.getLogger(__name__)

#: The refusal the server answers a cancel, retry or watch of a verl sample with (the W30 spike, V1).
COMMAND_REFUSAL = "verl/TRL gives Probe no handle on one rollout"
#: The agent loop workers' producer: they write live samples only, never seals, so the plan never declares it.
ROLLOUT_PRODUCER = "verl-rollout"
#: Where `AgentLoopWorker` lives (`experimental/agent_loop/agent_loop.py:534`); V1's `AgentLoopWorkerTQ` inherits its
#: `_run_agent_loop` (`trainer/ppo/v1/agent_loop_tq.py:53`).
AGENT_LOOP_MODULE = "verl.experimental.agent_loop.agent_loop"
WORKER_CLASS = "AgentLoopWorker"
RUN_LOOP = "_run_agent_loop"
#: Scores a finished loop's outputs (`agent_loop.py:1055`); both postprocesses call it, legacy `:910`, V1
#: `v1/agent_loop_tq.py:165`.
COMPUTE_SCORE = "_compute_score"
#: How long an agent loop waits for its process to join the run (once per process, off the event loop) before it runs
#: unrecorded; the worker's construction starts the join, so it is normally done long before the first loop.
START_WAIT_SECONDS = 5.0



@dataclass
class _Loop:
    """One agent loop as its wraps see it: its live key (None when unrecorded), whether it validates, and the stop
    reason of its newest model call (`TokenOutput.stop_reason`, `workers/rollout/replica.py:41`). One object per loop,
    so a task the loop starts (a copied context) writes to it too. A recorded loop also holds its capture
    (`tool_loop.LoopRecording`) and, once scored, the stamp it carries (`""` for none)."""

    key: str | None
    is_validate: bool
    stop_reason: str | None = None
    recording: Any = None
    rollout: str = ""


_LOOP: contextvars.ContextVar[_Loop | None] = contextvars.ContextVar("probe_verl_loop", default=None)
#: This process's join: its `VerlLive`, or None (Probe off here, or the join failed). Made once per process.
_START: concurrent.futures.Future | None = None
_LOCK = threading.Lock()


def make_live_key(split: str, step: Any, uid: Any, *, session: Any = None, position: Any = None) -> str | None:
    """One agent loop's key, or None when it cannot be named: by its V1 session, else its legacy batch position. The
    `s` / `p` mark keeps it apart from every sample key (`rows.make_sample_key`), whose index is bare."""
    if uid is None or step is None:
        return None
    if session is not None:
        return f"{split}:{step}:{uid}:s{session}"
    if position is not None:
        return f"{split}:{step}:{uid}:p{position}"
    return None


class VerlLive:
    """One AgentLoopWorker process's live samples."""

    def __init__(self, run: Any) -> None:
        self.run = run
        samples = run.samples.as_producer(ROLLOUT_PRODUCER)
        refuse_commands(samples, COMMAND_REFUSAL)
        self.attempts = LiveAttempts(samples)
        self._where = {"host": socket.gethostname(), "worker": f"pid:{os.getpid()}"}
        self._unnamed = itertools.count()
        self._clients: set[int] = set()
        #: Model calls each open loop made so far.
        self._turns: dict[str, int] = {}
        #: The newest weight version this worker's servers answered with (`extra_fields["global_steps"]`).
        self._version: int | None = None

    def start_loop(self, worker: Any, trajectory: Mapping[str, Any], kwargs: Mapping[str, Any]) -> str | None:
        """An agent loop begins (`agent_loop.py:749`): its live sample, keyed from its trajectory info and row."""
        self._watch_client(getattr(worker, "llm_client", None))
        split = Split.EVAL if trajectory.get("validate") else Split.TRAIN
        step, version = self._get_step(_as_step(kwargs.get("global_steps"), trajectory.get("step")))
        key = make_live_key(split, step, kwargs.get("uid"), session=kwargs.get("session_id"),
                            position=kwargs.get("priority"))  # fmt: skip
        named = f"{split}:{step}" if step is not None else str(split)
        if key is None:  # no row to name it by: live, but its sample never names it
            key = f"{named}:{kwargs.get('uid')}:w{os.getpid()}.{next(self._unnamed)}"
        extra = kwargs.get("extra_info") if isinstance(kwargs.get("extra_info"), Mapping) else {}
        start: dict[str, Any] = {"key": key, "task_key": _get_task_key(extra, kwargs.get("raw_prompt")),
                                 "scenario": get_scenario(extra), "group_key": f"{named}:{kwargs.get('uid')}",
                                 **self._where}  # fmt: skip
        if step is not None:
            start["scheduled_step"] = step
        if version is not None:
            start["weight_version"] = version
        return key if self.attempts.start([start]) else None

    def _get_step(self, step: int | None) -> tuple[int | None, int | None]:
        """The loop's step, and the weight version when the step came from it. The fully async rollouter sends no
        `global_steps` (`agent_loop.py:723-725` reads -1): there it is the trainer's step on the weights the servers
        serve, `current_param_version + 1` (the trainer pushes its version with the weights,
        `fully_async_trainer.py:733-735`, and the servers answer with it, `llm_server.py:343-367`); unknown until this
        worker's first answer. A step verl names keeps no version: a sync step's loops all start before any answer,
        so the newest answered version is the step before's."""
        if step is not None and step >= 0:
            return step, None
        return (self._version + 1, self._version) if self._version is not None else (None, None)

    def _record_version(self, output: Any) -> None:
        extra = getattr(output, "extra_fields", None)
        version = extra.get("global_steps") if isinstance(extra, Mapping) else None
        if isinstance(version, int) and not isinstance(version, bool) and version >= 0:
            self._version = version if self._version is None else max(self._version, version)

    def end_loop(self, key: str, output: Any) -> None:
        """The loop returned: graded when it scored itself (`reward_score`, a reward loop worker's), else `ungraded` (V1
        writes its output to the TransferQueue and returns nothing)."""
        self._turns.pop(key, None)
        reward = getattr(output, "reward_score", None)
        self.attempts.end([{"key": key, "outcome": self.attempts.get_outcome(reward)}])

    def end_error(self, key: str, error: BaseException) -> None:
        self._turns.pop(key, None)
        self.attempts.end_error([key], error)

    def _watch_client(self, client: Any) -> None:
        """The worker's `LLMServerClient.generate` (`workers/rollout/llm_server.py:99`), once: each call inside a live
        agent loop is progress."""
        if client is None or id(client) in self._clients:
            return
        self._clients.add(id(client))
        generate = client.generate
        attempts, turns = self.attempts, self._turns

        @functools.wraps(generate)
        async def call_generate(*args: Any, **kwargs: Any) -> Any:
            loop = _LOOP.get()
            key = loop.key if loop is not None else None
            if key is None or not attempts.is_open(key):
                output = await generate(*args, **kwargs)
                guard(_keep_stop_reason, loop, output)
                return output
            number = turns.get(key, 0) + 1
            attempts.send_progress([key], phase=AttemptPhase.GENERATING, turns=number - 1, activity=f"model call {number}")
            output = await generate(*args, **kwargs)
            guard(_keep_stop_reason, loop, output)
            turns[key] = number
            guard(self._record_version, output)
            attempts.send_progress([key], phase=AttemptPhase.ENVIRONMENT, turns=number,
                                   activity=f"model replied ({getattr(output, 'stop_reason', None) or 'done'})")
            return output

        object.__setattr__(client, "generate", call_generate)


def start_live() -> concurrent.futures.Future:
    """Join the launcher's run (`PROBE_RUN_ID`) as producer `verl-rollout`, once per process, on a thread of its own: the
    join talks to the Probe service, and an agent loop runs on verl's event loop. Its result is None when Probe is off
    here or the join failed (never retried)."""
    global _START
    with _LOCK:
        if _START is not None:
            return _START
        _START = concurrent.futures.Future()
        from probe.sdk.settings.settings import Mode, env_run_id, resolve_mode

        if not env_run_id() or resolve_mode(None) is Mode.DISABLED:
            _START.set_result(None)
        else:
            threading.Thread(target=_join_run, args=(_START,), name="probe-verl-live", daemon=True).start()
        return _START


async def get_live() -> VerlLive | None:
    """This process's live samples for an agent loop: waits at most `START_WAIT_SECONDS` for the join (never blocking
    the event loop); None when it is not done by then, Probe is off here, or the join failed."""
    started = start_live()
    if started.done():
        return started.result()
    try:
        return await asyncio.wait_for(asyncio.shield(asyncio.wrap_future(started)), START_WAIT_SECONDS)
    except asyncio.TimeoutError:
        return None


def _join_run(started: concurrent.futures.Future) -> None:
    try:
        from probe.sdk.run.samples import attach_producer

        run = attach_producer(ROLLOUT_PRODUCER, should_sample_hardware=False, should_capture_logs=False)
        started.set_result(VerlLive(run))
    except Exception as exc:  # noqa: BLE001 -- fail open: the loops run unrecorded
        logger.warning("Probe could not record this verl agent loop worker's live samples; verl continues: %s", exc)
        started.set_result(None)


def wrap_agent_loop_worker(cls: type) -> bool:
    """``cls._run_agent_loop`` (`agent_loop.py:749`) records each loop as a live sample, and ``cls.__init__`` (`:544`)
    starts the process's join. Once per class; on the class that defines them, before Ray builds an actor class from it
    (Ray's copies then call the wraps)."""
    original = cls.__dict__.get(RUN_LOOP)
    if not callable(original) or is_wrapped(original):
        return False
    init = cls.__dict__.get("__init__")
    if callable(init):

        @functools.wraps(init)
        def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
            init(self, *args, **kwargs)
            guard(start_live)  # a worker is made long before its first loop: the join is done by then

        setattr(cls, "__init__", __init__)

    @functools.wraps(original)
    async def _run_agent_loop(self: Any, *args: Any, **kwargs: Any) -> Any:
        live = await guard_async(get_live)
        trajectory = kwargs.get("trajectory", args[1] if len(args) > 1 else None)
        is_live = live is not None and isinstance(trajectory, Mapping)
        key = guard(live.start_loop, self, trajectory, kwargs) if is_live else None
        is_validate = bool(trajectory.get("validate")) if isinstance(trajectory, Mapping) else False
        recording = guard(open_recording, live.run, key) if key is not None else None
        token = _LOOP.set(_Loop(key, is_validate, recording=recording))
        try:
            with recording.enter() if recording is not None else contextlib.nullcontext():
                output = await original(self, *args, **kwargs)
        except BaseException as exc:
            if key is not None:
                guard(live.end_error, key, exc)
            raise
        finally:
            _LOOP.reset(token)
        if key is not None:
            guard(live.end_loop, key, output)
        return output

    set_wrapped(cls, RUN_LOOP, _run_agent_loop)
    score = cls.__dict__.get(COMPUTE_SCORE)
    if callable(score) and not is_wrapped(score):

        @functools.wraps(score)
        async def _compute_score(self: Any, outputs: Any, *args: Any, **kwargs: Any) -> Any:
            loop = _LOOP.get()
            recording = loop.recording if loop is not None else None
            if recording is not None:
                guard(recording.stamp_handle, self, outputs)
            result = await score(self, outputs, *args, **kwargs)
            if recording is not None:
                loop.rollout = await guard_async(recording.finish, outputs) or ""
            guard(stamp_output, outputs, loop)
            return result

        set_wrapped(cls, COMPUTE_SCORE, _compute_score)
    return True


_install = make_install(WORKER_CLASS, wrap_agent_loop_worker)


def stamp_output(outputs: Any, loop: _Loop | None) -> None:
    """After verl scored a loop (`agent_loop.py:1055-1117`): its last output carries the engine's stop reason and, in
    a validation loop, its live key, stop reason and capture (`ROLLOUT_EVAL_FIELD`) in `reward_extra_info` too; a
    training loop's capture rides `extra_fields` (`ROLLOUT_FIELD`). Every validation loop is stamped, `""` when there
    is none: the legacy postprocess reads each `reward_extra_info` key of the batch's first row from every row
    (`agent_loop.py:1196-1199`), so a key on one row and not another would raise there."""
    if loop is None or not outputs:
        return
    extra = getattr(outputs[-1], "extra_fields", None)
    if not isinstance(extra, MutableMapping):
        return
    extra[STOP_REASON_FIELD] = loop.stop_reason or ""
    if loop.rollout and not loop.is_validate:
        extra[ROLLOUT_FIELD] = loop.rollout
    if loop.is_validate:  # V1's `_validate` hands on only `reward_extra_info` (`v1/trainer_base.py:1131-1145`)
        info = extra.setdefault("reward_extra_info", {})
        if isinstance(info, MutableMapping):
            info[LIVE_KEY_FIELD] = loop.key or ""
            info[STOP_REASON_FIELD] = loop.stop_reason or ""
            info[ROLLOUT_EVAL_FIELD] = loop.rollout or ""


def _keep_stop_reason(loop: _Loop | None, output: Any) -> None:
    reason = getattr(output, "stop_reason", None)
    if loop is not None and reason is not None:
        loop.stop_reason = str(reason)


def watch_agent_loop_import() -> None:
    """Wrap `AgentLoopWorker` the moment its module loads in this process (now, when it already has), and the tool
    loop, its parser and the reward worker (`tool_loop`). Ray's setup hook calls it in every worker: each finder looks
    at one module name and costs nothing else."""
    from probe.sdk.run.samples.points import watch_import

    watch_import(AGENT_LOOP_MODULE, _install, framework="verl")
    watch_tool_loop_imports()


def _as_step(*values: Any) -> int | None:
    for value in values:
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        item = getattr(value, "item", None)  # a 0-d tensor or numpy scalar
        if callable(item):
            try:
                found = item()
            except Exception:  # noqa: BLE001 -- not a scalar
                continue
            if isinstance(found, int):
                return found
    return None


def _get_task_key(extra: Mapping[str, Any], raw_prompt: Any) -> str:
    """The dataset's `extra_info.task_id` (what its sample names too); else a hash of the prompt's messages, `chat:`,
    never the sample's own `prompt:` hash (that one hashes the decoded tokens, which the loop has not made yet)."""
    named = extra.get(TASK_KEY_FIELD)
    if isinstance(named, (str, int)) and str(named):
        return str(named)
    canonical = json.dumps(raw_prompt, sort_keys=True, default=str, ensure_ascii=False)
    return "chat:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
