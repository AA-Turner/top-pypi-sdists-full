"""Files a verl reward function attaches (D11). At the pinned commit a loop's reward runs in a `RewardLoopWorker` Ray
actor (`agent_loop.py:1112-1116`), another process, so the rollout's context cannot follow: the loop stamps a handle
(`stamps.HANDLE_FIELD`), `compute_score` is wrapped to open a capture from it (this process joins the run as producer
`verl-reward`, never declared on the plan), and the call's attached files go back in its `reward_extra_info`
(`stamps.FILES_FIELD`), which the loop's `_compute_score` wrap takes off before verl reads it. A sync reward function
runs in the loop's default executor (`naive.py:75`), which copies no context: the worker's loop gets one that does."""

from __future__ import annotations

import asyncio
import concurrent.futures
import contextvars
import functools
import json
import logging
import threading
import weakref
from collections.abc import Mapping, MutableMapping
from typing import Any

from ..wrapping import guard, is_wrapped, make_install, set_wrapped
from .executor import run_in_executor
from .stamps import FILES_FIELD, HANDLE_FIELD, read_stamp

logger = logging.getLogger(__name__)

REWARD_LOOP_MODULE = "verl.experimental.reward_loop.reward_loop"
REWARD_WORKER_CLASS = "RewardLoopWorker"
COMPUTE_SCORE = "compute_score"
#: The reward workers' producer: it writes files only, never samples or seals, so the plan never declares it.
REWARD_PRODUCER = "verl-reward"
#: How long one scoring waits for this process to join the run (started when the worker is made), then runs as is.
JOIN_WAIT_SECONDS = 5.0

_JOIN: concurrent.futures.Future | None = None
_LOCK = threading.Lock()
_LOOPS_WITH_CONTEXT: weakref.WeakSet = weakref.WeakSet()


class ContextExecutor(concurrent.futures.ThreadPoolExecutor):
    """A default executor that runs each call in a copy of the submitting task's context (what `asyncio.to_thread`
    does), so a sync reward function sees the rollout the scoring opened."""

    def submit(self, function: Any, /, *args: Any, **kwargs: Any) -> concurrent.futures.Future:
        return super().submit(contextvars.copy_context().run, function, *args, **kwargs)


def wrap_reward_worker(cls: type) -> bool:
    """``cls.compute_score`` attaches into the rollout its handle names, and ``cls.__init__`` starts the join. Once,
    on the class that defines them, before Ray builds the actor class from it."""
    original = cls.__dict__.get(COMPUTE_SCORE)
    if not callable(original) or is_wrapped(original):
        return False
    init = cls.__dict__.get("__init__")
    if callable(init):

        @functools.wraps(init)
        def __init__(self: Any, *args: Any, **kwargs: Any) -> None:
            init(self, *args, **kwargs)
            guard(start_join)

        setattr(cls, "__init__", __init__)

    @functools.wraps(original)
    async def compute_score(self: Any, data: Any, *args: Any, **kwargs: Any) -> Any:
        handle = guard(take_handle, data)
        run = await get_reward_run() if handle else None
        if run is None or str(getattr(run, "id", "")) != str(handle.get("run_id")):
            return await original(self, data, *args, **kwargs)
        from probe.sdk.run.samples.rollout import RolloutCapture

        remote = guard(RolloutCapture.from_handle, run, handle)  # None for a malformed handle or another run's
        if remote is None:
            return await original(self, data, *args, **kwargs)
        guard(use_context_executor, self)
        with remote:
            result = await original(self, data, *args, **kwargs)
        try:
            files = await run_in_executor(remote.collect_files)
            if (files or remote.failed_count) and isinstance(result, MutableMapping):
                info = result.setdefault("reward_extra_info", {})
                if isinstance(info, MutableMapping):
                    info[FILES_FIELD] = json.dumps({"files": files, "failed": remote.failed_count}, default=str)
        except Exception as exc:  # noqa: BLE001 -- fail open: the score goes back without the files
            logger.debug("probe: a verl reward's files were not handed back (%s: %s)", type(exc).__name__, exc)
        return result

    set_wrapped(cls, COMPUTE_SCORE, compute_score)
    return True


def take_handle(data: Any) -> Mapping[str, Any] | None:
    """The handle on the scored rows' `tool_extra_fields` (the loop's outputs' `extra_fields`, `agent_loop.py:1098`),
    from the last row (the one verl scores, `naive.py:35`), taken off every row: verl merges the row into the reward
    function's `extra_info` (`naive.py:45-47`), which then reads as verl built it. The rows are this worker's copy."""
    columns = getattr(data, "non_tensor_batch", None) or {}
    rows = columns.get("tool_extra_fields") if isinstance(columns, Mapping) else None
    if rows is None or not len(rows):
        return None
    last = rows[-1]
    handle = read_stamp(last.get(HANDLE_FIELD)) if isinstance(last, Mapping) else None
    for row in rows:
        if isinstance(row, MutableMapping):
            row.pop(HANDLE_FIELD, None)
    return handle if handle and handle.get("run_id") and handle.get("attempt_key") else None


def use_context_executor(worker: Any) -> None:
    """The running loop and the reward manager's (`naive.py:75` runs a sync reward function on its loop's default
    executor) copy the caller's context into their executor threads. Once per loop; replacing an executor verl
    already made leaves its idle threads."""
    loops = {asyncio.get_running_loop(), getattr(getattr(worker, "reward_manager", None), "loop", None)}
    for loop in loops:
        if isinstance(loop, asyncio.AbstractEventLoop) and loop not in _LOOPS_WITH_CONTEXT:
            loop.set_default_executor(ContextExecutor(thread_name_prefix="probe-verl-reward"))
            _LOOPS_WITH_CONTEXT.add(loop)


def start_join() -> concurrent.futures.Future:
    """Join the launcher's run (`PROBE_RUN_ID`) as `verl-reward`, once per process, on a thread of its own. Its
    result is the run, or None (Probe off here, or the join failed; never retried)."""
    global _JOIN
    with _LOCK:
        if _JOIN is not None:
            return _JOIN
        _JOIN = concurrent.futures.Future()
        from probe.sdk.settings.settings import Mode, env_run_id, resolve_mode

        if not env_run_id() or resolve_mode(None) is Mode.DISABLED:
            _JOIN.set_result(None)
        else:
            threading.Thread(target=_join_run, args=(_JOIN,), name="probe-verl-reward", daemon=True).start()
        return _JOIN


async def get_reward_run() -> Any:
    """This process's run for a scoring: waits at most `JOIN_WAIT_SECONDS`, never blocking the event loop."""
    started = guard(start_join)
    if started is None:
        return None
    if started.done():
        return started.result()
    try:
        return await asyncio.wait_for(asyncio.shield(asyncio.wrap_future(started)), JOIN_WAIT_SECONDS)
    except asyncio.TimeoutError:
        return None


def _join_run(started: concurrent.futures.Future) -> None:
    try:
        from probe.sdk.run.samples import attach_producer

        started.set_result(attach_producer(REWARD_PRODUCER, should_sample_hardware=False, should_capture_logs=False))
    except Exception as exc:  # noqa: BLE001 -- fail open: rewards score with nothing attached
        logger.warning("Probe could not join this verl reward worker to the run; its rewards attach no files: %s", exc)
        started.set_result(None)


install = make_install(REWARD_WORKER_CLASS, wrap_reward_worker)
