# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
Replicas of a model, each in its own process, each running one call at a time; a replica that dies is replaced.

    from sequence_ai.engine.replicas import ReplicaPool

    pool = ReplicaPool(load, replicas=2, devices=[0, 1])     # load() builds the model in the replica's own process
    output = await pool.run(observation)                      # in a request's handler: off the event loop
    pool.close()

`load` is a function a new process can import (defined at a module's top level) that builds the model and returns
the callable each call runs: `model(payload) -> output`. What is sent to a replica and what comes back is pickled.

In one sentence: the pool starts a fixed set of replicas, each in its own process on the GPU that `devices` assigns to
it (it sees that GPU alone: CUDA_VISIBLE_DEVICES), and every call runs in one of them, off the server's event loop; a
replica that dies is retired and replaced. So a forward pass never blocks the server's I/O, replicas never contend for
one interpreter, and one dead process never takes the server down.

WHY a queue of idle replicas rather than a lock around a list: the queue gives fair first-come hand-off for free, and
waiting on it is the natural place for a call to wait when every replica is busy. Waiting for a *replica* is the point:
it is what makes a request queue for a GPU instead of for the interpreter.
WHY a model's error and a replica's death are distinguished (ReplicaError, ReplicaDied): the two demand opposite
handling. A model that raised is still loaded and takes the next call; a process that has exited (killed mid-call, out
of memory, past its deadline) holds nothing, and is replaced.
WHY the pool stops replacing after a few deaths in a row (PoolHalted once none is left): a model that dies on every call
would otherwise be loaded again and again, each load costing minutes of GPU time.
WHY a new process is spawned, never forked: a forked child inherits its parent's CUDA state, which CUDA does not
support.

Standard library only. Written for this package after the pool General Sequences serves with, which is bound to its
own child protocol; the rules above are that one's.
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import functools
import multiprocessing
import os
import pickle
import queue
import threading
import time
import traceback
from typing import Any, Callable, Optional, Sequence


class ReplicaDied(RuntimeError):
    """A replica's process has exited: it exited or was killed mid-call, or it exceeded its deadline and was terminated.
    `reason`: "exited", "deadline"."""

    def __init__(self, message: str, *, reason: str = "exited") -> None:
        super().__init__(message)
        self.reason = reason


class ReplicaStartFailed(RuntimeError):
    """A replica never became ready: its load raised, it died while loading, or it did not load in time. `traceback`:
    the load's own, when it raised."""

    def __init__(self, message: str, *, traceback: Optional[str] = None) -> None:  # noqa: A002 (its public name)
        super().__init__(message)
        self.traceback = traceback


class ReplicaError(RuntimeError):
    """The model raised in its replica, which stays alive. `traceback`: the replica's own."""

    def __init__(self, message: str, *, traceback: Optional[str] = None) -> None:  # noqa: A002
        super().__init__(message)
        self.traceback = traceback


class PoolHalted(RuntimeError):
    """No replica is left: several died in a row and the pool stopped replacing them, or it was closed."""


def _child(load: Callable[[], Callable[[Any], Any]], conn, device, env: Optional[dict]) -> None:
    """A replica's process: its GPU set before anything loads, the model built once, then one call at a time."""
    if device is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
    os.environ.update(env or {})
    try:
        model = load()
    except BaseException as exc:  # noqa: BLE001 (a load's error is reported to the parent, then the process ends)
        conn.send(("failed", f"{type(exc).__name__}: {exc}", traceback.format_exc()))
        return
    conn.send(("ready", os.getpid(), None))
    while True:
        try:
            message = conn.recv()
        except (EOFError, OSError):
            return                                   # the parent has exited
        if message[0] == "stop":
            return
        try:
            reply = ("ok", model(message[1]), None)
        except Exception as exc:  # noqa: BLE001 (the model's own error goes to its caller, and the replica stays alive)
            reply = ("error", f"{type(exc).__name__}: {exc}", traceback.format_exc())
        try:
            conn.send(reply)
        except Exception as exc:  # noqa: BLE001 (a result that cannot be pickled)
            conn.send(("error", f"the result could not be sent back: {type(exc).__name__}: {exc}", None))


class Replica:
    """One replica in its own process, running one call at a time (the pool assigns it to one caller)."""

    def __init__(self, load: Callable[[], Callable[[Any], Any]], *, device=None, env: Optional[dict] = None,
                 start_timeout: float = 900.0) -> None:
        ctx = multiprocessing.get_context("spawn")
        self._conn, theirs = ctx.Pipe()
        self.device = device
        self.process = ctx.Process(target=_child, args=(load, theirs, device, env), daemon=True)
        try:
            self.process.start()
        except (AttributeError, TypeError, pickle.PicklingError) as unsendable:
            # a new process imports `load` by name: a lambda or a nested function has no importable name
            raise TypeError(
                "load must be a function a new process can import: defined at a module's top level, not a lambda "
                f"and not a function inside another. Each replica starts in its own process ({unsendable})"
            ) from unsendable
        theirs.close()
        self.pid: int = self._await_ready(start_timeout)

    def _await_ready(self, start_timeout: float) -> int:
        deadline = time.monotonic() + start_timeout
        while True:
            try:
                if self._conn.poll(0.05):
                    kind, value, trace = self._conn.recv()
                    if kind == "ready":
                        return value
                    self.kill()
                    raise ReplicaStartFailed(f"the model's load raised: {value}", traceback=trace)
            except (EOFError, OSError):
                pass                                 # its end of the pipe closed: it has exited, reported below
            if not self.process.is_alive():
                raise ReplicaStartFailed(f"the replica died while loading (exit code {self.process.exitcode})")
            if time.monotonic() > deadline:
                self.kill()
                raise ReplicaStartFailed(f"the model did not load within {start_timeout:g} s")

    def alive(self) -> bool:
        """Whether this replica's process is still running."""
        return self.process.is_alive()

    def call(self, payload: Any, timeout: Optional[float] = None) -> Any:
        """`payload` run by the model in this replica: its result; ReplicaError when the model raised; ReplicaDied when
        the process has exited, or exceeded `timeout` seconds and was terminated."""
        deadline = None if timeout is None else time.monotonic() + timeout
        try:
            self._conn.send(("call", payload))
        except (BrokenPipeError, OSError):
            raise ReplicaDied(f"the replica had exited before its call (exit code {self.process.exitcode})") from None
        while True:
            try:
                if self._conn.poll(0.05):
                    kind, value, trace = self._conn.recv()
                    if kind == "ok":
                        return value
                    raise ReplicaError(value, traceback=trace)
            except (EOFError, OSError):
                self.process.join(1.0)
                raise ReplicaDied(f"the replica died mid-call (exit code {self.process.exitcode})") from None
            if not self.process.is_alive() and not self._conn.poll(0):
                raise ReplicaDied(f"the replica died mid-call (exit code {self.process.exitcode})")
            if deadline is not None and time.monotonic() > deadline:
                self.kill()                          # its state is unknown: it is terminated, not waited for
                raise ReplicaDied(f"the call exceeded its {timeout:g} s deadline: the replica was terminated",
                                  reason="deadline")

    def kill(self) -> None:
        """Terminate this replica's process and wait for it to exit."""
        if self.process.is_alive():
            self.process.kill()
        self.process.join(5.0)
        self._conn.close()

    def close(self) -> None:
        """Ask it to stop, then terminate it if it does not."""
        try:
            self._conn.send(("stop",))
        except (BrokenPipeError, OSError):
            pass
        self.process.join(2.0)
        self.kill()


_GONE = object()        # in the queue of idle replicas once none is left: a waiting call is told, not left waiting


class ReplicaPool:
    """A fixed set of replicas, each running one call at a time, a dead one replaced (the module's docstring).

    run(payload)    from an event loop: the call runs in a replica, on one of the pool's threads
    call(payload)   the same, for a caller on its own thread
    size            the replicas alive now
    pids            their process ids"""

    def __init__(self, load: Callable[[], Callable[[Any], Any]], *, replicas: int = 1,
                 devices: Optional[Sequence] = None, env: Optional[dict] = None, start_timeout: float = 900.0,
                 deaths_in_a_row: int = 3) -> None:
        devices = [None] * replicas if devices is None else list(devices)
        if replicas < 1 or len(devices) != replicas:
            raise ValueError(f"{replicas} replicas and {len(devices)} devices: one device per replica, "
                             "at least one replica")
        self._load, self._env, self._start_timeout, self._limit = load, env, start_timeout, max(1, deaths_in_a_row)
        self._idle: "queue.Queue[Any]" = queue.Queue()
        self._lock = threading.Lock()
        self._all: set[Replica] = set()
        self._replacing = 0
        self._deaths = 0
        self._halted: Optional[str] = None
        # all replicas load concurrently: a model's load takes minutes, and they do not wait on each other
        with concurrent.futures.ThreadPoolExecutor(max_workers=replicas) as starters:
            started = [starters.submit(self._start, device) for device in devices]
            failed = None
            for future in started:
                try:
                    self._all.add(future.result())
                except ReplicaStartFailed as exc:
                    failed = failed or exc
        if failed is not None:
            for replica in self._all:
                replica.close()
            raise failed
        for replica in self._all:
            self._idle.put(replica)
        self._threads = concurrent.futures.ThreadPoolExecutor(max_workers=replicas,
                                                              thread_name_prefix="sequence-ai-replica")

    def _start(self, device) -> Replica:
        return Replica(self._load, device=device, env=self._env, start_timeout=self._start_timeout)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._all)

    @property
    def pids(self) -> list[int]:
        with self._lock:
            return sorted(replica.pid for replica in self._all)

    def call(self, payload: Any, *, timeout: Optional[float] = None) -> Any:
        """`payload` run in one replica, after waiting while every replica is busy: its result; ReplicaError when the
        model raised; ReplicaDied when its replica died during the call (and is being replaced); PoolHalted when no
        replica is left."""
        replica = self._idle.get()
        if replica is _GONE:
            self._idle.put(_GONE)                    # for the next waiting call
            raise PoolHalted(self._halted or "the pool is closed")
        try:
            output = replica.call(payload, timeout)
        except ReplicaError:
            self._idle.put(replica)                  # the model's own error: the replica stays alive
            raise
        except BaseException:                        # the replica died, or its caller was interrupted mid-call: its
            self._retire(replica)                    # state is unknown, so it is terminated and replaced
            raise
        with self._lock:
            self._deaths = 0
        self._idle.put(replica)
        return output

    async def run(self, payload: Any, *, timeout: Optional[float] = None) -> Any:
        """call(), from an event loop: on one of the pool's threads, so the loop keeps running while the model runs."""
        return await asyncio.get_running_loop().run_in_executor(
            self._threads, functools.partial(self.call, payload, timeout=timeout))

    def _retire(self, replica: Replica) -> None:
        """Remove a dead replica from the set, and start one in its place unless too many died in a row."""
        replica.kill()
        with self._lock:
            self._all.discard(replica)
            self._deaths += 1
            replace = self._halted is None and self._deaths < self._limit
            if replace:
                self._replacing += 1
            elif self._halted is None:
                self._halted = f"{self._deaths} replicas died in a row: the pool stopped replacing them"
        if replace:
            threading.Thread(target=self._replace, args=(replica.device,), daemon=True,
                             name="sequence-ai-replace").start()
        else:
            self._tell_if_none_left()

    def _replace(self, device) -> None:
        try:
            replica = self._start(device)
        except ReplicaStartFailed as exc:
            with self._lock:
                self._replacing -= 1
                self._deaths += 1
                if self._halted is None and self._deaths >= self._limit:
                    self._halted = f"{self._deaths} replicas died in a row, the last while loading ({exc})"
            self._tell_if_none_left()
            return
        with self._lock:
            self._replacing -= 1
            closed = self._halted == "the pool is closed"
            if not closed:
                self._all.add(replica)
        if closed:
            replica.close()
        else:
            self._idle.put(replica)

    def _tell_if_none_left(self) -> None:
        with self._lock:
            none_left = not self._all and not self._replacing
            if none_left and self._halted is None:
                self._halted = "no replica is left: the last one's replacement did not load"
        if none_left:
            self._idle.put(_GONE)

    def close(self) -> None:
        """Ask every replica to stop, then terminate it; a waiting call gets PoolHalted (the pool is closed)."""
        with self._lock:
            self._halted = "the pool is closed"
            replicas, self._all = list(self._all), set()
        while True:                                  # no idle replica is assigned from now on
            try:
                self._idle.get_nowait()
            except queue.Empty:
                break
        self._idle.put(_GONE)
        for replica in replicas:
            replica.close()
        self._threads.shutdown(wait=False)
