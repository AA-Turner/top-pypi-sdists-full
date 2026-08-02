# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""In-process synchronous shim for the subset of Ray geneva's MV-refresh uses, for
fast cluster-free sweeps. Replaces ``ray.remote`` / ``get`` / ``wait`` / ``put`` /
``kill`` and ``ray.util.queue.Queue`` (keeping the real ``ray`` module otherwise),
so every ``@ray.remote`` actor/task runs in-process with no cluster -- ~0.15s per
refresh vs ~3s on a local cluster. Lazy futures + a would-block deferral preserve
the pipeline's producer/consumer ordering. See ``mv_differential_sweep.py``.

Two caveats:
- ``install()`` MUST run before geneva imports (``@ray.remote`` decorates at
  import), so this is a standalone-script tool, not an in-session pytest fixture.
- It is a candidate generator, not a perfect oracle: it raises where real Ray
  restarts the writer and gap-fills NULLs, so confirm any finding on real Ray.
"""

import asyncio
import collections
import contextlib
import inspect
from collections.abc import Callable, Collection, Iterator
from typing import Any

import ray
import ray.actor
import ray.exceptions
import ray.util.queue

_loop: asyncio.AbstractEventLoop | None = None


def _run_coro(coro: Any) -> Any:
    global _loop
    if _loop is None:
        _loop = asyncio.new_event_loop()
    return _loop.run_until_complete(coro)


class _WouldBlockError(Exception):
    """Raised by a shimmed queue.get() on an empty queue: the consuming task
    isn't ready to complete yet -- re-run it on a later wait."""


class FakeRef:
    """A deferred, lazily-evaluated stand-in for a Ray ObjectRef."""

    __slots__ = ("_thunk", "_done", "_v", "_e")

    def __init__(self, thunk: Any) -> None:
        self._thunk = thunk
        self._done = False
        self._v: Any = None
        self._e: BaseException | None = None

    def result(self) -> Any:
        if self._done:
            if self._e is not None:
                raise self._e
            return self._v
        try:
            r = self._thunk()
            if inspect.iscoroutine(r):
                r = _run_coro(r)
        except _WouldBlockError:
            raise  # leave un-run; a later wait will retry
        except Exception as e:  # mirror ray: surfaces at ray.get time
            self._done = True
            self._e = e
            raise
        self._done = True
        self._v = r
        return r


def _resolve(r: Any) -> Any:
    return r.result() if isinstance(r, FakeRef) else r


def _try_ready(r: Any) -> bool:
    """Return True if r is done, False if it would block.

    A thunk that RAISED is "done" in Ray's model: ``ray.wait`` reports it ready and
    the error surfaces only at ``ray.get``. ``FakeRef.result`` has already stored the
    exception on the ref, so swallow it here and let a later ``ray.get`` re-raise it.
    Propagating it from ``ray.wait`` instead would surface remote failures one step too
    early -- e.g. a writer-actor death would crash the poll loop rather than reach the
    driver's ``ray.get`` handler (the graceful-degradation path)."""
    try:
        _resolve(r)
        return True
    except _WouldBlockError:
        return False
    except Exception:  # noqa: BLE001 -- the ref stored it; ray.get will re-raise
        return True


def shim_get(refs: Any, *a: Any, **k: Any) -> Any:
    if isinstance(refs, (list, tuple)):
        return [_resolve(r) for r in refs]
    return _resolve(refs)


def shim_wait(
    refs: Any, *, num_returns: int = 1, timeout: Any = None, fetch_local: bool = True
) -> tuple[list, list]:
    # Run each thunk; ones that would block stay "not ready" (re-runnable).
    ready: list = []
    rest: list = []
    for r in refs:
        if len(ready) < num_returns and (not isinstance(r, FakeRef) or _try_ready(r)):
            ready.append(r)
        else:
            rest.append(r)
    return ready, rest


def shim_put(v: Any, *a: Any, **k: Any) -> "FakeRef":
    return FakeRef(lambda: v)


def _noop(*a: Any, **k: Any) -> None:
    pass


class _BoundRemote:
    """Shim for a @ray.remote *function* (task)."""

    def __init__(self, fn: Any) -> None:
        self.fn = fn

    def remote(self, *a: Any, **k: Any) -> "FakeRef":
        return FakeRef(lambda: self.fn(*a, **k))

    def options(self, *a: Any, **k: Any) -> "_BoundRemote":
        return self

    def __call__(self, *a: Any, **k: Any) -> Any:
        return self.fn(*a, **k)


# --- actor-death injection: faithful in-process worker death ----------------
# Arm a RayActorError at a chosen call of a target actor method so its in-flight task
# surfaces to the consumer and geneva's real ActorPool death path runs (_get_next_by_fut
# -> ActorPoolTaskError -> _handle_fatal_task_failure, since geneva sets
# resubmit_on_actor_failure=False). The fabricated commit/fragment faults never reach
# that path. A faithful death needs the consumer-side error and geneva's recovery, which
# only exist in-process; under real Ray you kill the worker for real.


class _ActorDeathPolicy:
    """Arms a death error at selected 1-based calls to ``class_name.method``.

    The error is raised lazily at ``ray.get`` time (like real Ray surfacing a killed
    worker's in-flight task), not at submission, so geneva's consumer-side handler is
    the one that sees it. ``fired`` records which occurrences died, for assertions.
    """

    def __init__(
        self,
        class_name: str,
        method: str,
        occurrences: "frozenset[int] | set[int] | tuple[int, ...]",
        error_factory: Callable[[], BaseException],
    ) -> None:
        self.class_name = class_name
        self.method = method
        self.occurrences = frozenset(occurrences)
        self.error_factory = error_factory
        self.calls = 0  # 1-based count of submissions to the target method
        self.fired: list[int] = []

    def arm(self, class_name: str, method: str) -> bool:
        """Count a submission of ``class_name.method`` and report whether it dies.

        Decided at submission so a method that internally would-block (and re-runs under
        the shim's deferral) is not double-counted -- the verdict is fixed once."""
        if class_name != self.class_name or method != self.method:
            return False
        self.calls += 1
        if self.calls in self.occurrences:
            self.fired.append(self.calls)
            return True
        return False


_ACTOR_DEATH: _ActorDeathPolicy | None = None


def set_actor_death(policy: _ActorDeathPolicy | None) -> None:
    global _ACTOR_DEATH
    _ACTOR_DEATH = policy


def make_actor_death_policy(
    class_name: str,
    method: str = "run",
    occurrences: "tuple[int, ...]" = (1,),
    error_factory: Callable[[], BaseException] | None = None,
) -> _ActorDeathPolicy:
    """Build (but do not install) an actor-death policy; default error is RayActorError.

    For callers that need the policy object up front -- e.g. to pair the context manager
    with a ``policy.fired`` predicate (the sweep's fault installer)."""
    ef = error_factory or ray.exceptions.RayActorError
    return _ActorDeathPolicy(class_name, method, occurrences, ef)


@contextlib.contextmanager
def using_actor_death_policy(
    policy: _ActorDeathPolicy,
) -> Iterator[_ActorDeathPolicy]:
    """Install a pre-built actor-death policy for the block, restoring the prior one."""
    prev = _ACTOR_DEATH
    set_actor_death(policy)
    try:
        yield policy
    finally:
        set_actor_death(prev)


@contextlib.contextmanager
def using_actor_death(
    class_name: str,
    method: str = "run",
    occurrences: "tuple[int, ...]" = (1,),
    error_factory: Callable[[], BaseException] | None = None,
) -> Iterator[_ActorDeathPolicy]:
    """Install an actor-death policy for the block (default: kill the 1st call to
    ``class_name.run`` with a ``RayActorError``), restoring the prior one after."""
    with using_actor_death_policy(
        make_actor_death_policy(class_name, method, occurrences, error_factory)
    ) as policy:
        yield policy


def _dead_thunk(error_factory: Callable[[], BaseException]) -> Callable[[], Any]:
    def thunk() -> Any:
        raise error_factory()

    return thunk


class _ActorMethod:
    def __init__(self, inst: Any, name: str) -> None:
        self.inst = inst
        self.name = name

    def remote(self, *a: Any, **k: Any) -> "FakeRef":
        policy = _ACTOR_DEATH
        if policy is not None and policy.arm(type(self.inst).__name__, self.name):
            # Model the actor dying on this task: raise at get-time, not now.
            return FakeRef(_dead_thunk(policy.error_factory))
        return FakeRef(lambda: getattr(self.inst, self.name)(*a, **k))

    def options(self, *a: Any, **k: Any) -> "_ActorMethod":
        return self


class _ReadyMethod:
    """Ray-internal actor methods (e.g. __ray_ready__ readiness probe)."""

    def remote(self, *a: Any, **k: Any) -> "FakeRef":
        return FakeRef(lambda: None)

    def options(self, *a: Any, **k: Any) -> "_ReadyMethod":
        return self


class _ActorHandle:
    def __init__(self, inst: Any) -> None:
        object.__setattr__(self, "_inst", inst)

    def __getattr__(self, name: str) -> Any:
        inst = object.__getattribute__(self, "_inst")
        try:
            attr = getattr(inst, name)
        except AttributeError:
            if name.startswith("__ray"):  # __ray_ready__, __ray_call__, ...
                return _ReadyMethod()
            raise
        if callable(attr) and not isinstance(attr, type):
            return _ActorMethod(inst, name)
        return attr


class _ActorClassShim:
    """Shim for a @ray.remote *class* (actor)."""

    def __init__(self, cls: Any) -> None:
        self.cls = cls

    def remote(self, *a: Any, **k: Any) -> "_ActorHandle":
        return _ActorHandle(self.cls(*a, **k))

    def options(self, *a: Any, **k: Any) -> "_ActorClassShim":
        return self


def shim_remote(*dargs: Any, **dkwargs: Any) -> Any:
    def wrap(obj: Any) -> Any:
        if inspect.isclass(obj):
            return _ActorClassShim(obj)
        return _BoundRemote(obj)

    if (
        len(dargs) == 1
        and not dkwargs
        and (inspect.isclass(dargs[0]) or inspect.isfunction(dargs[0]))
    ):
        return wrap(dargs[0])
    return wrap


class _QueueFaultPolicy:
    """Faults enqueue operations on shim queues (1-based count, process-wide).

    ``drop_at`` skips the append -- a lost fire-and-forget ``put_nowait`` (the real
    enqueue path submits to the queue actor without awaiting the reply). ``dup_at``
    appends the item twice -- a retried enqueue delivered twice. Seal sentinels
    (first element < 0) are never counted or faulted: dropping the seal only hangs
    the consumer, which is not the silent class this models.
    """

    def __init__(
        self,
        *,
        drop_at: Collection[int] = (),
        dup_at: Collection[int] = (),
    ) -> None:
        self.drop_at = frozenset(drop_at)
        self.dup_at = frozenset(dup_at)
        self.calls = 0
        self.dropped: list[int] = []
        self.dupped: list[int] = []

    def decide(self, item: Any) -> str | None:
        is_seal = (
            isinstance(item, tuple)
            and bool(item)
            and isinstance(item[0], int)
            and item[0] < 0
        )
        if is_seal:
            return None
        self.calls += 1
        n = self.calls
        if n in self.drop_at:
            self.dropped.append(n)
            return "drop"
        if n in self.dup_at:
            self.dupped.append(n)
            return "dup"
        return None


_QUEUE_FAULTS: _QueueFaultPolicy | None = None


def make_queue_fault_policy(
    *, drop_at: Collection[int] = (), dup_at: Collection[int] = ()
) -> _QueueFaultPolicy:
    return _QueueFaultPolicy(drop_at=drop_at, dup_at=dup_at)


@contextlib.contextmanager
def using_queue_faults(policy: _QueueFaultPolicy) -> Iterator[_QueueFaultPolicy]:
    """Install a queue-enqueue fault policy for the block, restoring the prior one."""
    global _QUEUE_FAULTS
    prev = _QUEUE_FAULTS
    _QUEUE_FAULTS = policy
    try:
        yield policy
    finally:
        _QUEUE_FAULTS = prev


def _fault_append(d: "collections.deque", item: Any) -> None:
    pol = _QUEUE_FAULTS
    if pol is not None:
        decision = pol.decide(item)
        if decision == "drop":
            return
        if decision == "dup":
            d.append(item)
            d.append(item)
            return
    d.append(item)


class _QueueBackend:
    """Backs FakeQueue.actor so ``queue.actor.put_nowait.remote(x)`` works."""

    def __init__(self, d: "collections.deque") -> None:
        self._d = d

    def put_nowait(self, x: Any) -> None:
        _fault_append(self._d, x)

    def put_nowait_batch(self, items: Any) -> None:
        for x in items:
            _fault_append(self._d, x)

    def get(self, *a: Any, **k: Any) -> Any:
        if not self._d:
            raise _WouldBlockError
        return self._d.popleft()

    def get_nowait(self) -> Any:
        if not self._d:
            raise _WouldBlockError
        return self._d.popleft()

    def qsize(self) -> int:
        return len(self._d)

    def empty(self) -> bool:
        return not self._d


class FakeQueue:
    """In-memory replacement for ray.util.queue.Queue (single-process FIFO).

    ``get()`` on an empty queue raises ``_WouldBlockError`` instead of blocking,
    so a consumer task primed before the producer fills the queue is deferred and
    retried by the shim's wait loop rather than crashing or hanging.
    """

    def __init__(self, *a: Any, **k: Any) -> None:
        self._d: collections.deque = collections.deque()
        self.actor = _ActorHandle(_QueueBackend(self._d))

    def put(self, x: Any, *a: Any, **k: Any) -> None:
        _fault_append(self._d, x)

    def put_nowait(self, x: Any) -> None:
        _fault_append(self._d, x)

    def get(self, *a: Any, **k: Any) -> Any:
        if not self._d:
            raise _WouldBlockError
        return self._d.popleft()

    def get_nowait(self) -> Any:
        if not self._d:
            raise _WouldBlockError
        return self._d.popleft()

    def empty(self) -> bool:
        return not self._d

    def qsize(self) -> int:
        return len(self._d)

    def shutdown(self, *a: Any, **k: Any) -> None:
        pass

    def __len__(self) -> int:
        return len(self._d)


def install() -> None:
    """Monkeypatch the behavioral ray primitives. Call before importing geneva."""
    ray.remote = shim_remote
    ray.get = shim_get
    ray.wait = shim_wait
    ray.put = shim_put
    ray.kill = _noop
    ray.cancel = _noop
    ray.init = _noop
    ray.shutdown = _noop
    ray.is_initialized = lambda: True
    ray.util.queue.Queue = FakeQueue
    if hasattr(ray.actor, "exit_actor"):
        ray.actor.exit_actor = _noop


def stub_geneva_cluster_polling() -> None:
    """Optional speedup (~1.5x per refresh): no-op geneva's Ray cluster-status
    polling, which is meaningless under this shim (no cluster) and only sets
    progress metrics -- it never touches view data, so it is safe for the
    differential sweeps. Call after geneva is importable.
    """
    import geneva.runners.ray.pipeline as p

    def _noop_status(self: Any) -> None:
        return None

    p.ColumnAddPipelineJob._refresh_cluster_status = _noop_status  # type: ignore[method-assign]
    p.ColumnAddPipelineJob._try_refresh_cluster_status = _noop_status  # type: ignore[method-assign]
