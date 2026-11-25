# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Ray Authors
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# forked actor pool from ray.util.actor_pool
# we added support for FT and autoscaling to this implementation
# ordered map supoort is dropped atm, but can be added back if needed

import contextlib
import logging
import os
import threading
import time
from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import Future, ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, TypeVar

import attrs
import ray
import ray.actor
import ray.exceptions
from ray import ObjectRef
from ray.actor import ActorHandle
from ray.util.state import get_actor, list_actors

if TYPE_CHECKING:
    from ray.util.state.common import PredicateType, SupportedFilterType

from geneva.errors import FatalWorkerError, FatalWorkerHardwareError
from geneva.runners.ray.jobtracker import (
    job_tracker_options,
    job_tracker_throttle_kwargs,
)

V = TypeVar("V")
T = TypeVar("T")


def ray_tqdm(iterable: Iterable[T], job_tracker: Any, metric: str) -> Iterator[T]:
    """Wrap an iterable to track progress via a JobTracker."""
    for item in iterable:
        job_tracker.increment.remote(metric, 1)
        yield item
    job_tracker.mark_done.remote(metric)


_LOG = logging.getLogger(__name__)

# Stall watchdog for ``map``/``map_unordered``. Without it these loops call
# ``get_next_unordered`` with no timeout, so a task that never completes -- or an
# actor that can never be scheduled (its submits stay pending, nothing is inflight)
# -- blocks forever with no error. ``backfill``'s applier loop already has this
# guard; mirror it here so the MV-refresh / UDTF / chunker / sparse paths (which
# go through ``_map``) fail loud on no-progress instead of hanging. Same env var as
# the backfill watchdog so both share one knob.
_MAP_POLL_INTERVAL_S = 5.0
_MAP_STALL_TIMEOUT_S = float(os.environ.get("GENEVA_PIPELINE_STALL_TIMEOUT_S", "1800"))


@attrs.define(frozen=True)
class ActorPoolTaskError(RuntimeError):
    """Raised when a submitted actor task needs caller-managed recovery."""

    task: Any
    cause: Exception

    def __str__(self) -> str:
        return f"Actor pool task failed for {self.task!r}: {self.cause}"


def _dict_context(value: Any, *keys: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    for key in keys:
        context = value.get(key)
        if isinstance(context, dict):
            return context
    return {}


def _actor_died_context(death_cause: Any) -> dict[str, Any]:
    return _dict_context(
        death_cause,
        "actorDiedErrorContext",
        "actor_died_error_context",
    )


def _node_death_info(actor_context: dict[str, Any]) -> dict[str, Any]:
    return _dict_context(actor_context, "nodeDeathInfo", "node_death_info")


def _dict_get(value: Any, *keys: str) -> Any:
    if not isinstance(value, dict):
        return None
    for key in keys:
        if key in value:
            return value[key]
    return None


def _death_cause_reason(death_cause: Any) -> str | None:
    actor_context = _actor_died_context(death_cause)
    reason = actor_context.get("reason")
    if reason is None:
        reason = _dict_get(death_cause, "reason")
    if reason is not None:
        return str(reason)
    return None


def _death_cause_has_node_death_info(death_cause: Any) -> bool:
    return bool(_node_death_info(_actor_died_context(death_cause)))


def _death_cause_has_oom_context(death_cause: Any) -> bool:
    """Return whether Ray actor state identifies an OOM death.

    ``death_cause`` is a protobuf-derived dictionary. The protobuf field name is
    ``oom_context``, while protobuf JSON serialization exposes it as
    ``oomContext`` unless configured to preserve proto field names.
    """
    if not isinstance(death_cause, dict):
        return False
    return any(
        isinstance(death_cause.get(key), dict) for key in ("oom_context", "oomContext")
    )


def _has_preemption_text(value: Any) -> bool:
    return value is not None and "PREEMPT" in str(value).upper()


def _extract_preempted(actor_state: Any, death_cause: Any) -> bool:
    if getattr(actor_state, "num_restarts_due_to_node_preemption", 0) > 0:
        return True
    actor_context = _actor_died_context(death_cause)
    node_info = _node_death_info(actor_context)
    return any(
        _has_preemption_text(candidate)
        for candidate in (
            actor_context.get("reason"),
            _dict_get(actor_context, "errorMessage", "error_message"),
            node_info.get("reason"),
            _dict_get(death_cause, "reason"),
        )
    )


@attrs.define(frozen=True)
class ActorStateSnapshot:
    """Structured Ray state for a busy actor observed by liveness polling."""

    actor_id: str
    state: str
    death_cause: Any | None = None
    death_reason: str | None = None
    node_id: str | None = None
    preempted: bool = False

    @classmethod
    def from_ray_state(cls, actor_id: str, actor_state: Any) -> "ActorStateSnapshot":
        death_cause = getattr(actor_state, "death_cause", None)
        node_id = getattr(actor_state, "node_id", None)
        return cls(
            actor_id=actor_id,
            state=str(getattr(actor_state, "state", "UNKNOWN")),
            death_cause=death_cause,
            death_reason=_death_cause_reason(death_cause),
            node_id=str(node_id) if node_id is not None else None,
            preempted=_extract_preempted(actor_state, death_cause),
        )

    @property
    def is_oom_loss(self) -> bool:
        """Whether Ray reported this actor death through OomContext."""
        return _death_cause_has_oom_context(self.death_cause)

    @property
    def is_transient_infra_loss(self) -> bool:
        """Whether Ray attributes the actor loss to recoverable infrastructure.

        Node-level loss (NODE_DIED, nodeDeathInfo, or preemption) removes every
        actor on the node and usually reflects recoverable cluster churn such as
        a node crash, network partition, or autoscaling. WORKER_DIED while its
        node remains alive is process-scoped and likely points to a crashing
        workload or UDF, so it is not transient.
        """
        return (
            self.preempted
            or (self.death_reason or "").upper() == "NODE_DIED"
            or _death_cause_has_node_death_info(self.death_cause)
        )


@attrs.define(frozen=True)
class ActorLostError(RuntimeError):
    """Raised when Ray state shows a busy actor died before its future resolved."""

    snapshot: ActorStateSnapshot
    task: Any

    @property
    def is_oom_loss(self) -> bool:
        """Whether the lost actor was killed for exceeding memory limits."""
        return self.snapshot.is_oom_loss

    @property
    def is_transient_infra_loss(self) -> bool:
        return self.snapshot.is_transient_infra_loss

    def __str__(self) -> str:
        return (
            "actor lost while task was inflight "
            f"(actor_id={self.snapshot.actor_id}; state={self.snapshot.state}; "
            f"death_reason={self.snapshot.death_reason or 'unknown'}; "
            f"node_id={self.snapshot.node_id or 'unknown'}; "
            f"oom_loss={self.snapshot.is_oom_loss}; "
            f"preempted={self.snapshot.preempted}; "
            f"death_cause={'present' if self.snapshot.death_cause else 'absent'}; "
            f"task={self.task!r})"
        )


_ACTOR_LOSS_ERRORS = (
    ray.exceptions.RayActorError,
    ray.exceptions.NodeDiedError,
)
_ACTOR_LIVENESS_SCAN_INTERVAL_S = 30.0
_ACTOR_STATE_QUERY_TIMEOUT_S = 5
_ACTOR_STATE_SCAN_LIMIT = 10_000
_ACTOR_STATE_EXACT_QUERY_CONCURRENCY = 32


class PollTimeoutError(TimeoutError):
    """The pool's own wait expired before any result arrived.

    Deliberately distinct from a ``TimeoutError`` raised *by a task*: Ray
    surfaces task exceptions as ``RayTaskError`` subclassing the task's own
    exception type, so a task that times out against a dependent API is a
    ``TimeoutError`` instance too. Poll loops must catch THIS type, not bare
    ``TimeoutError``, or they silently swallow that task failure as
    "no result yet".
    """


def _actor_id_hex(actor: Any) -> str | None:
    actor_id = getattr(actor, "_actor_id", None)
    if actor_id is None:
        return None
    hex_fn = getattr(actor_id, "hex", None)
    if callable(hex_fn):
        return str(hex_fn())
    return str(actor_id)


def _current_job_id_hex() -> str | None:
    try:
        job_id = ray.get_runtime_context().get_job_id()
    except Exception:
        _LOG.debug("Failed to read the current Ray job id", exc_info=True)
        return None
    hex_fn = getattr(job_id, "hex", None)
    if callable(hex_fn):
        return str(hex_fn())
    return str(job_id)


def _current_gcs_address() -> str | None:
    try:
        return str(ray.get_runtime_context().gcs_address)
    except Exception:
        _LOG.debug("Failed to read the current Ray GCS address", exc_info=True)
        return None


class ActorPool:
    """Utility class to operate on a pool of up to ``num_actors`` actors.

    Parameters
    ----------
        actor_factory
            Factory used to create actors. This should be a callable
            that returns a new actor handle when called. The factory will be called
            num_actors times to create the initial pool of actors.
        num_actors
            Number of actors to create in the pool. Actors freed by
            :meth:`release_idle_actors` are restarted for later work, never
            past this size.
        worker_tracker
            Optional ObjectRef for tracking worker progress.
        clock
            Monotonic clock that times how long actors stay idle for
            :meth:`release_idle_actors`. Defaults to ``time.monotonic``.

    Examples
    --------
        .. testcode::

            import ray
            from ray.util.actor_pool import ActorPool

            @ray.remote
            class Actor:
                def double(self, v):
                    return 2 * v

            a1, a2 = Actor.remote(), Actor.remote()
            pool = ActorPool([a1, a2])
            print(list(pool.map(lambda a, v: a.double.remote(v),
                                [1, 2, 3, 4])))

        .. testoutput::

            [2, 4, 6, 8]
    """

    _actor_liveness_scan_interval_s = _ACTOR_LIVENESS_SCAN_INTERVAL_S

    def __init__(
        self,
        actors_factory: Callable[[], Any],
        num_actors: int,
        *,
        job_tracker: ObjectRef | ActorHandle | Any | None = None,
        worker_metric: str = "workers",
        resubmit_on_actor_failure: bool = True,
        actor_num_gpus: float | None = None,
        clock: Callable[[], float] | None = None,
    ) -> None:
        # factory to create actors
        self._actor_factory = actors_factory
        self._clock = clock or time.monotonic

        self._actor_num_gpus = actor_num_gpus
        self._parked_actors: list[Any] = []
        self.last_hardware_fault: Exception | None = None

        # number of actors # added
        self._num_actors = num_actors

        # readyness future to actor # added
        self._ready_fut_to_actor = {}

        # actors to be used
        self._idle_actors = []

        # When each idle actor (by _actor_key) last became idle.
        self._idle_since: dict[tuple[str, Any], float] = {}

        # get actor from future
        self._future_to_actor = {}

        # get future from index
        self._index_to_future = {}

        # next task to do
        self._next_task_index = 0

        # next work depending when actors free
        self._pending_submits = []

        # Actor slots freed by release_idle_actors and not yet refilled. Live
        # actors (idle, busy, starting) plus these always equal num_actors, so
        # restarting into them can never grow the pool past its original size.
        self._released_slots = 0

        # results drained by drain_ready before a mid-batch task error, held so
        # the next drain_ready call returns them instead of dropping them
        self._drained_buffer: list[Any] = []

        # the task that was submitted # added
        self._future_to_task = {}

        # actor id for each submitted future, used to detect actors that Ray has
        # marked DEAD before their task future resolves.
        self._future_to_actor_id = {}
        self._job_id = _current_job_id_hex()
        self._gcs_address = _current_gcs_address()
        self._last_actor_liveness_scan_at: float | None = None
        # Actor liveness scans (Ray State API) run on a dedicated background
        # thread so a slow scan (~46s at 10k actors) never stalls the driver's
        # result loop. Single-flight: at most one scan in flight at a time.
        self._liveness_scan_executor = ThreadPoolExecutor(
            max_workers=1, thread_name_prefix="geneva-liveness-scan"
        )
        self._liveness_scan_future: Future | None = None
        # Set on shutdown so an in-flight scan bails out instead of fanning out
        # thousands of exact State API queries for actors it just killed.
        self._liveness_scan_cancelled = threading.Event()

        self.worker_metric = worker_metric
        self.resubmit_on_actor_failure = resubmit_on_actor_failure

        spawn_job_tracker = job_tracker_options().remote
        self.job_tracker = job_tracker or spawn_job_tracker(  # type: ignore[call-arg]
            "fake job id", None, **job_tracker_throttle_kwargs()
        )
        self.job_tracker.set_total.remote(worker_metric, num_actors)  # type: ignore[attr-defined]
        # No reset call: the tracker drops a worker count restored from a
        # previous run on the first increment (see RESTART_STALE_METRICS).
        ray_tqdm([], self.job_tracker, worker_metric)

        for _ in range(num_actors):
            self._queue_actor_startup()

    def _holds_whole_gpu(self) -> bool:
        """Whether parking an actor keeps its GPU out of Ray's scheduling pool."""
        return self._actor_num_gpus is not None and self._actor_num_gpus >= 1

    def _now(self) -> float:
        """Current time on the pool's idle clock."""
        return getattr(self, "_clock", time.monotonic)()

    def _idle_since_by_key(self) -> dict[tuple[str, Any], float]:
        """When each idle actor became idle, keyed by :meth:`_actor_key`."""
        idle_since = getattr(self, "_idle_since", None)
        if idle_since is None:
            idle_since = self._idle_since = {}
        return idle_since

    def _pop_idle_actor(self) -> Any:
        """Take the most recently idled actor, so the longest idle go first."""
        actor = self._idle_actors.pop()
        self._idle_since_by_key().pop(self._actor_key(actor), None)
        return actor

    def _queue_actor_startup(self) -> None:
        new_actor = self._actor_factory()
        ready_fut = new_actor.__ray_ready__.remote()
        self.job_tracker.increment.remote(self.worker_metric, 1)  # type: ignore[attr-defined]
        self._ready_fut_to_actor[ready_fut] = new_actor

    def _record_actor_gone(self) -> None:
        """Subtract a failed actor that left the pool for good from the count.

        Call once per actor, after it is removed from every pool state, so
        ``shutdown`` (which subtracts the actors it still owns) never counts it
        again.
        """
        self.job_tracker.increment.remote(self.worker_metric, -1)  # type: ignore[attr-defined]

    def _collect_ready_actors(self) -> None:
        # Non‑blocking drain of all currently ready actors. This avoids throttling
        # ramp‑up without waiting for not‑yet‑ready actors.
        while True:
            futs = list(self._ready_fut_to_actor.keys())
            if not futs:
                return
            ready, _ = ray.wait(futs, num_returns=1, timeout=0.0)
            if not ready:
                # No more ready actors at this moment
                return

            for fut in ready:
                _LOG.debug("Adding ready actors to pool: %s", fut)
                actor = self._ready_fut_to_actor.pop(fut)
                try:
                    ray.get(fut)
                    self._return_actor(actor)
                except _ACTOR_LOSS_ERRORS:
                    _LOG.exception("Actor died or unavailable, cleaning it up")
                    with contextlib.suppress(Exception):
                        ray.kill(actor)
                    self._record_actor_gone()
                    self._queue_actor_startup()

    def _map(
        self,
        fn: Callable[["ray.actor.ActorHandle", V], Any],
        values: Iterable[V],
        *,
        ordered: bool,
    ) -> Iterator[Any]:
        # Ignore/Cancel all the previous submissions
        # by calling `has_next` and `gen_next` repeteadly.
        while self.has_next():
            with contextlib.suppress(TimeoutError):
                self.get_next_unordered(timeout=0)

        it = iter(values)

        def _maybe_submit() -> bool:
            try:
                v = next(it)
            except StopIteration:
                return False
            self.submit(fn, v)
            return True

        # prime the workers
        # always have one pending task so when we call get_next or get_next_unordered
        # we can submit task immediately without waiting for the puller to yield back
        submits = self._num_actors + 1
        while submits and _maybe_submit():
            submits -= 1

        # Poll with a bounded timeout and a stall deadline that resets on every
        # yielded result, so a hung task or an unschedulable actor fails loud
        # instead of blocking forever (mirrors backfill's applier loop). Catch
        # only PollTimeoutError: a task-raised TimeoutError (e.g. a dependent
        # API timing out inside the UDF) is a task failure and must propagate.
        stall_deadline = time.monotonic() + _MAP_STALL_TIMEOUT_S
        while self.has_next():
            try:
                result = self.get_next_unordered(timeout=_MAP_POLL_INTERVAL_S)
            except PollTimeoutError:
                if time.monotonic() >= stall_deadline:
                    raise TimeoutError(
                        "ActorPool stalled: no result produced in "
                        f"{_MAP_STALL_TIMEOUT_S}s (a task is hung, or no actor "
                        "could be scheduled)"
                    ) from None
                continue
            stall_deadline = time.monotonic() + _MAP_STALL_TIMEOUT_S
            yield result
            _maybe_submit()

    def map_unordered(
        self, fn: Callable[["ray.actor.ActorHandle", V], Any], values: Iterable[V]
    ) -> Iterator[Any]:
        """Similar to map(), but returning an unordered iterator.

        This returns an unordered iterator that will return results of the map
        as they finish. This can be more efficient that map() if some results
        take longer to compute than others.

        Parameters
        ----------
            fn
                Function that takes (actor, value) as argument and
                returns an ObjectRef computing the result over the value. The
                actor will be considered busy until the ObjectRef completes.
            values
                Iterable of values that fn(actor, value) should be
                applied to.

        Returns
        -------
            Iterator over results from applying fn to the actors and values.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1, a2 = Actor.remote(), Actor.remote()
                pool = ActorPool([a1, a2])
                print(list(pool.map_unordered(lambda a, v: a.double.remote(v),
                                              [1, 2, 3, 4])))

            .. testoutput::
                :options: +MOCK

                [6, 8, 4, 2]
        """
        yield from self._map(fn, values, ordered=False)

    def submit(self, fn, value) -> None:
        """Schedule a single task to run in the pool.

        This has the same argument semantics as map(), but takes on a single
        value instead of a list of values. The result can be retrieved using
        get_next() / get_next_unordered().

        Parameters
        ----------
            fn
                Function that takes (actor, value) as argument and
                returns an ObjectRef computing the result over the value. The
                actor will be considered busy until the ObjectRef completes.
            value
                Value to compute a result for.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1, a2 = Actor.remote(), Actor.remote()
                pool = ActorPool([a1, a2])
                pool.submit(lambda a, v: a.double.remote(v), 1)
                pool.submit(lambda a, v: a.double.remote(v), 2)
                print(pool.get_next(), pool.get_next())

            .. testoutput::

                2 4
        """
        if self._idle_actors:
            actor = self._pop_idle_actor()
            future = fn(actor, value)
            future_key = tuple(future) if isinstance(future, list) else future
            self._future_to_actor[future_key] = (self._next_task_index, actor)
            self._index_to_future[self._next_task_index] = future
            self._next_task_index += 1
            self._future_to_task[future_key] = (fn, value)
            actor_id = _actor_id_hex(actor)
            if actor_id is not None:
                self._future_to_actor_id[future_key] = actor_id
        else:
            self._pending_submits.append((fn, value))
            self._restart_released_actors()

    def _restart_released_actors(self) -> None:
        """Start actors for queued work in slots freed by release_idle_actors.

        Queued submits beyond the actors already starting each get a new
        actor, until the released slots run out. A no-op unless actors were
        released, so a pool that never releases keeps its exact behavior.
        """
        while getattr(self, "_released_slots", 0) > 0:
            if len(self._pending_submits) <= len(self._ready_fut_to_actor):
                return
            self._queue_actor_startup()
            self._released_slots -= 1
            _LOG.info(
                "Restarted an actor for late work (%d queued task(s), %d "
                "released slot(s) left)",
                len(self._pending_submits),
                self._released_slots,
            )

    def has_next(self) -> bool:
        """Returns whether there are any pending results to return.

        Returns
        -------
            True if there are any pending results not yet returned.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1, a2 = Actor.remote(), Actor.remote()
                pool = ActorPool([a1, a2])
                pool.submit(lambda a, v: a.double.remote(v), 1)
                print(pool.has_next())
                print(pool.get_next())
                print(pool.has_next())

            .. testoutput::

                True
                2
                False
        """
        # _drained_buffer holds results drain_ready stranded when a task failed
        # mid-batch; they are still pending delivery, so the driver loop must not
        # treat the pool as exhausted while they remain.
        return (
            bool(self._future_to_actor)
            or bool(self._pending_submits)
            or bool(self._drained_buffer)
        )

    def has_buffered_results(self) -> bool:
        """Whether a failed drain has completed results awaiting delivery."""
        return bool(self._drained_buffer)

    def submission_capacity(self, *, extra_pending: int = 1) -> int:
        """Return how many tasks can be submitted without overfilling the pool.

        Keep one queued task by default so an actor can immediately take new
        work when it finishes. Dynamic fanout can use this capacity to refill
        all idle actor slots at once while preserving the existing
        ``num_actors + 1`` bound on in-flight plus pool-pending submissions.
        """
        target = self._num_actors + max(0, extra_pending)
        outstanding = len(self._future_to_actor) + len(self._pending_submits)
        return max(0, target - outstanding)

    class NoResult: ...

    def _pop_future_state(self, future) -> tuple[Any, Any, Any]:
        i, actor = self._future_to_actor.pop(future)
        fn, task = self._future_to_task.pop(future)
        self._future_to_actor_id.pop(future, None)
        del self._index_to_future[i]
        return actor, fn, task

    def _actor_states_by_id(
        self, actor_ids: set[str]
    ) -> dict[str, ActorStateSnapshot] | None:
        if not actor_ids:
            return {}
        if self._liveness_scan_cancelled.is_set():
            return None

        # Start with one bulk ALIVE query because per-actor State API calls can
        # block result processing for minutes on pools with thousands of actors.
        # Treat ALIVE as positive evidence and exact-query only busy actors missing
        # from the bulk result. A bulk DEAD query is unsafe because a long-running
        # Ray job can accumulate more than the State API's 10k historical-record
        # cap and the endpoint has no pagination.
        filters: list[tuple[str, PredicateType, SupportedFilterType]] = [
            ("state", "=", "ALIVE")
        ]
        job_id = getattr(self, "_job_id", None)
        if job_id is not None:
            filters.append(("job_id", "=", job_id))
        try:
            actors = list_actors(
                address=getattr(self, "_gcs_address", None),
                filters=filters,
                limit=_ACTOR_STATE_SCAN_LIMIT,
                timeout=_ACTOR_STATE_QUERY_TIMEOUT_S,
                detail=False,
                # Truncation is safe here: an omitted actor is not assumed dead;
                # it is verified by an exact-ID query below.
                raise_on_missing_output=False,
            )
        except Exception:
            _LOG.warning(
                "Failed to batch-list ALIVE Ray actors while checking liveness",
                exc_info=True,
            )
            return None

        alive_actor_ids: set[str] = set()
        for actor in actors:
            returned_actor_id = getattr(actor, "actor_id", None)
            if returned_actor_id is None:
                continue
            actor_id = str(returned_actor_id)
            if actor_id not in actor_ids or str(getattr(actor, "state", "")) != "ALIVE":
                continue
            alive_actor_ids.add(actor_id)

        missing_actor_ids = sorted(actor_ids - alive_actor_ids)
        if not missing_actor_ids:
            return {}
        # Skip the exact-query fanout if the pool was torn down mid-scan: those
        # actors are missing because shutdown just killed them, not because they
        # died in flight.
        if self._liveness_scan_cancelled.is_set():
            return None

        states: dict[str, ActorStateSnapshot] = {}
        max_workers = min(
            _ACTOR_STATE_EXACT_QUERY_CONCURRENCY,
            len(missing_actor_ids),
        )
        with ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="geneva-ray-actor-state",
        ) as executor:
            snapshots = executor.map(self._actor_state_by_id, missing_actor_ids)
            for actor_id, snapshot in zip(
                missing_actor_ids,
                snapshots,
                strict=True,
            ):
                if snapshot is None or snapshot.actor_id != actor_id:
                    continue
                states[actor_id] = snapshot
        return states

    def _actor_state_by_id(self, actor_id: str) -> ActorStateSnapshot | None:
        """Best-effort exact Actor State lookup for a busy actor."""
        # Short-circuit remaining fanout queries once the scan is cancelled so a
        # post-shutdown scan drains fast instead of hammering the State API.
        if self._liveness_scan_cancelled.is_set():
            return None
        try:
            actor = get_actor(
                actor_id,
                address=getattr(self, "_gcs_address", None),
                timeout=_ACTOR_STATE_QUERY_TIMEOUT_S,
            )
            if actor is None:
                return None
            returned_actor_id = getattr(actor, "actor_id", None)
            if returned_actor_id is None or str(returned_actor_id) != actor_id:
                return None
            return ActorStateSnapshot.from_ray_state(actor_id, actor)
        except Exception:
            _LOG.warning(
                "Failed to get Ray actor %s while checking actor liveness",
                actor_id,
                exc_info=True,
            )
            return None

    def _cleanup_lost_actor_future(
        self, future: Any, snapshot: ActorStateSnapshot
    ) -> tuple[Any, Any, ActorLostError]:
        actor, fn, task = self._pop_future_state(future)
        lost_error = ActorLostError(snapshot=snapshot, task=task)
        _LOG.error(
            "Actor %s became %s while running task %r; death_reason=%s; "
            "oom_loss=%s; preempted=%s; cleaning it up",
            snapshot.actor_id,
            snapshot.state,
            task,
            snapshot.death_reason,
            snapshot.is_oom_loss,
            snapshot.preempted,
        )
        with contextlib.suppress(Exception):
            ray.kill(actor)
        self._record_actor_gone()
        self._queue_actor_startup()
        return fn, task, lost_error

    def _pop_dead_actor_task(self) -> Any | NoResult:
        # Consume a finished background scan (may raise ActorPoolTaskError), then
        # start a new one if due. Neither step blocks on the ~46s scan itself.
        result = self._consume_liveness_scan()
        if result is not self.NoResult:
            return result
        self._maybe_start_liveness_scan()
        return self.NoResult

    def _maybe_start_liveness_scan(self) -> None:
        """Submit a background liveness scan if one is due and none is running."""
        if self._liveness_scan_cancelled.is_set():
            return  # pool shut down: the executor is gone, don't submit
        if self._liveness_scan_future is not None:
            return  # single-flight: a scan is already in progress
        now = time.monotonic()
        last_scan_at = self._last_actor_liveness_scan_at
        if (
            last_scan_at is not None
            and now - last_scan_at < self._actor_liveness_scan_interval_s
        ):
            return  # rate-limited (measured from the last scan's completion)
        # Snapshot the busy actors only once we're actually going to scan, so the
        # per-poll hot path stays O(1) (this branch runs at most once per interval).
        actor_ids = set(self._future_to_actor_id.values())
        if not actor_ids:
            return
        self._liveness_scan_future = self._liveness_scan_executor.submit(
            self._actor_states_by_id, actor_ids
        )

    def _consume_liveness_scan(self) -> Any | NoResult:
        """Process a completed background scan, if any. Never blocks.

        Returns NoResult while no scan has finished; otherwise handles the dead
        actors it found (raising ActorPoolTaskError or resubmitting).
        """
        future = self._liveness_scan_future
        if future is None or not future.done():
            return self.NoResult
        self._liveness_scan_future = None
        # Rate-limit from completion: a transient dashboard/GCS failure must not
        # make every 50ms result poll spawn another scan.
        self._last_actor_liveness_scan_at = time.monotonic()
        try:
            states = future.result()
        except Exception:
            _LOG.warning("Background actor liveness scan failed", exc_info=True)
            return self.NoResult
        if states is None:
            return self.NoResult
        return self._handle_dead_actor_states(states)

    def _handle_dead_actor_states(
        self, states: dict[str, ActorStateSnapshot]
    ) -> Any | NoResult:
        """Clean up busy actors the scan found DEAD. Runs on the main thread."""
        dead_futures = []
        for future, actor_id in list(self._future_to_actor_id.items()):
            actor_state = states.get(actor_id)
            if actor_state is None or actor_state.state != "DEAD":
                continue
            dead_futures.append((future, actor_state))

        if not dead_futures:
            return self.NoResult

        # A scan snapshot lags reality: an actor can finish its task (result
        # already in the object store) and only then die. A future whose result
        # is already available is not lost -- drop it here and let the normal
        # drain path return the result, instead of raising a false failure or
        # resubmitting a task that already ran.
        # fetch_local=False: this is a completion check, not a fetch. A result
        # that finished on a remote node but is not yet downloaded to the driver
        # is still "done" (the task succeeded) and must not be treated as lost.
        ready, _ = ray.wait(
            [future for future, _ in dead_futures],
            num_returns=len(dead_futures),
            timeout=0,
            fetch_local=False,
        )
        if ready:
            ready_futures = set(ready)
            dead_futures = [
                (future, state)
                for future, state in dead_futures
                if future not in ready_futures
            ]
            if not dead_futures:
                return self.NoResult

        if not self.resubmit_on_actor_failure:
            future, actor_state = dead_futures[0]
            _fn, task, lost_error = self._cleanup_lost_actor_future(future, actor_state)
            raise ActorPoolTaskError(
                task=task,
                cause=lost_error,
            )

        for future, actor_state in dead_futures:
            if actor_state.is_transient_infra_loss:
                continue
            _fn, task, lost_error = self._cleanup_lost_actor_future(future, actor_state)
            raise ActorPoolTaskError(task=task, cause=lost_error)

        lost_tasks = []
        for future, actor_state in dead_futures:
            lost_tasks.append(self._cleanup_lost_actor_future(future, actor_state))

        for fn, task, _cause in lost_tasks:
            self.submit(fn, task)
        return self.NoResult

    def _get_next_by_fut(self, futures, timeout=None) -> Any | NoResult:
        # get_next will just pass a single future
        # get_next_unordered will pass a list of futures
        res, _ = ray.wait(futures, num_returns=1, timeout=timeout, fetch_local=True)
        if not res:
            raise PollTimeoutError("Timed out waiting for result")
        [future] = res
        return self._resolve_future(future)

    def _resolve_future(self, future) -> Any | NoResult:
        """Resolve a single already-ready future.

        Fetches the result, returns the actor to the pool, and handles OOM /
        actor-loss (resubmit or raise) identically to the single-result path.
        Shared by ``get_next_unordered`` and the batched ``drain_ready``.
        """
        actor_id = self._future_to_actor_id.get(future)
        a, fn, task = self._pop_future_state(future)

        try:
            # this is fast because ray.wait already fetched the result
            res = ray.get(future)
            # don't return the future till we get the result
            # because the actor could be dead
            self._return_actor(a)
        except (ray.exceptions.OutOfMemoryError, FatalWorkerError) as e:
            # Both memory-monitor OOM and typed child-worker failures require
            # caller-managed recovery with the original task context.
            _LOG.exception("Worker task requires caller-managed recovery")
            hardware_fault = isinstance(e, FatalWorkerHardwareError)
            if hardware_fault:
                self.last_hardware_fault = e
            if hardware_fault and self._holds_whole_gpu():
                _LOG.warning(
                    "Parking actor %s after a GPU hardware fault; its GPU stays "
                    "allocated and out of rotation for this job",
                    a,
                )
                # Still alive, so it stays counted until shutdown kills it.
                self._parked_actors.append(a)
            else:
                with contextlib.suppress(Exception):
                    ray.kill(a)
                self._record_actor_gone()
            self._queue_actor_startup()
            raise ActorPoolTaskError(task=task, cause=e) from e
        except _ACTOR_LOSS_ERRORS as e:
            _LOG.exception("Actor died or unavailable, cleaning it up")
            cause: Exception = e
            if (
                not self.resubmit_on_actor_failure
                and isinstance(e, ray.exceptions.ActorDiedError)
                and actor_id is not None
            ):
                # Ray's Python ActorDiedError drops ActorDiedErrorContext and
                # retains only the rendered message plus `preempted`. Re-query
                # the exact actor so NODE_DIED can be distinguished from a
                # WORKER_DIED process crash without brittle message matching.
                snapshot = self._actor_state_by_id(actor_id)
                if snapshot is not None and snapshot.state == "DEAD":
                    cause = ActorLostError(snapshot=snapshot, task=task)
            with contextlib.suppress(Exception):
                ray.kill(a)
            self._record_actor_gone()
            # queue a new actor
            self._queue_actor_startup()
            if self.resubmit_on_actor_failure:
                # resubmit the task
                self.submit(fn, task)
                return self.NoResult
            raise ActorPoolTaskError(task=task, cause=cause) from e

        return res

    def get_next_unordered(self, timeout=None) -> Any:
        """Returns any of the next pending results.

        This returns some result produced by submit(), blocking for up to
        the specified timeout until it is available. Unlike get_next(), the
        results are not always returned in same order as submitted, which can
        improve performance.

        Returns
        -------
            The next result.

        Raises
        ------
            PollTimeoutError
                if the timeout is reached with no result available. (A
                ``TimeoutError`` raised by a task itself propagates as the
                task's own error, not as ``PollTimeoutError``.)

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1, a2 = Actor.remote(), Actor.remote()
                pool = ActorPool([a1, a2])
                pool.submit(lambda a, v: a.double.remote(v), 1)
                pool.submit(lambda a, v: a.double.remote(v), 2)
                print(pool.get_next_unordered())
                print(pool.get_next_unordered())

            .. testoutput::
                :options: +MOCK

                4
                2
        """
        if not self.has_next():
            raise StopIteration("No more results to get")

        # Serve results drain_ready buffered on a mid-batch error so both drain
        # APIs stay consistent with has_next(); one at a time, matching this
        # method's single-result contract.
        if self._drained_buffer:
            return self._drained_buffer.pop(0)

        # Use a short default timeout to interleave collecting newly-ready actors
        poll_timeout = 0.05  # 50ms default poll interval
        deadline = None
        if timeout is not None:
            # Respect explicit timeout while still polling frequently
            timeout = max(timeout, 0.0)
            deadline = time.monotonic() + timeout
            # If the requested timeout is shorter than our poll interval, use it
            poll_timeout = min(poll_timeout, timeout)

        while True:
            # Always collect any actors that became ready since last iteration
            self._collect_ready_actors()

            # Run the liveness watchdog on every poll, not only on timeout:
            # consume a finished scan (surfacing any dead actor it found) and
            # start a new one if due. Both are O(1) unless there is real work, so
            # a busy pool that never times out still detects silent actor death.
            # Raises ActorPoolTaskError for a dead actor in non-resubmit mode.
            self._pop_dead_actor_task()

            futs = list(self._future_to_actor)
            if not futs:
                # No inflight yet; spin until at least one submission exists
                self._collect_ready_actors()
                futs = list(self._future_to_actor)
                if not futs:
                    # Honor an explicit (positive) timeout even while nothing is
                    # inflight -- e.g. actors that never become schedulable, so
                    # submits stay pending forever. Without this the branch spins
                    # ignoring ``deadline``. ``timeout == 0`` keeps its original
                    # non-blocking-probe behavior (used by _map's drain).
                    past_deadline = (
                        deadline is not None
                        and timeout
                        and time.monotonic() >= deadline
                    )
                    if past_deadline:
                        raise PollTimeoutError("Timed out waiting for result")
                    # Nothing is inflight, so the only state change to wait
                    # for is an actor finishing startup: block on those
                    # futures (bounded by the poll interval / deadline)
                    # instead of spinning non-blocking.
                    wait_s = poll_timeout
                    if deadline is not None:
                        wait_s = min(wait_s, max(deadline - time.monotonic(), 0.0))
                    ready_futs = list(self._ready_fut_to_actor)
                    if ready_futs:
                        ray.wait(ready_futs, num_returns=1, timeout=wait_s)
                    elif wait_s > 0:
                        time.sleep(wait_s)
                    continue

            current_timeout = poll_timeout
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise PollTimeoutError("Timed out waiting for result")
                current_timeout = min(current_timeout, remaining)

            try:
                item = self._get_next_by_fut(futs, current_timeout)
            except PollTimeoutError:
                # The liveness watchdog already ran at the top of the loop.
                if deadline is not None and deadline - time.monotonic() <= 0:
                    raise
                # No task finished within the poll interval; loop to collect more actors
                continue

            if item is not self.NoResult:
                return item

    def drain_ready(self, timeout=None) -> list[Any]:
        """Drain every result that is ready right now, in a single pass.

        Blocks up to ``timeout`` for the first result -- reusing
        ``get_next_unordered``'s tested blocking, nothing-inflight, and
        dead-actor handling -- then non-blocking-collects all other
        already-ready results via one batched ``ray.wait``. This amortizes the
        O(N) wait over the whole batch instead of paying it per result.

        Returns
        -------
            A non-empty list of results.

        Raises
        ------
            PollTimeoutError
                if no result becomes ready within ``timeout``.
            ActorPoolTaskError
                if a drained task failed (non-resubmit mode). Results already
                drained earlier in the same pass are buffered on the pool and
                returned by the next call, so they are never dropped.
        """
        # Flush results stranded by a prior pass that raised mid-batch.
        if self._drained_buffer:
            out = self._drained_buffer
            self._drained_buffer = []
            return out
        results = [self.get_next_unordered(timeout=timeout)]
        self._drain_ready_now(results)
        return results

    def _drain_ready_now(self, results: list[Any]) -> None:
        """Resolve every future ready at this instant, appending to ``results``.

        Single snapshot, single non-blocking ``ray.wait``: futures submitted
        while resolving this batch are left for the next pass. On a task error,
        results drained so far this pass are buffered and the error re-raised so
        the caller can handle the failure without losing completed work.
        """
        futs = list(self._future_to_actor)
        if not futs:
            return
        ready, _ = ray.wait(futs, num_returns=len(futs), timeout=0, fetch_local=True)
        for future in ready:
            try:
                item = self._resolve_future(future)
            except Exception:
                # Any failure mid-batch -- ActorPoolTaskError, or an ordinary
                # task exception re-raised by ray.get -- must not drop results
                # already drained this pass. Buffer them for the next call and
                # re-raise so the caller handles the failure.
                self._drained_buffer.extend(results)
                results.clear()
                raise
            if item is not self.NoResult:
                results.append(item)

    def _return_actor(self, actor) -> None:
        self._idle_actors.append(actor)
        self._idle_since_by_key()[self._actor_key(actor)] = self._now()
        # while self._idle_actors and self._pending_submits:
        if self._pending_submits:
            self.submit(*self._pending_submits.pop(0))

    def has_free(self) -> bool:
        """Returns whether there are any idle actors available.

        Returns
        -------
            True if there are any idle actors and no pending submits.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1 = Actor.remote()
                pool = ActorPool([a1])
                pool.submit(lambda a, v: a.double.remote(v), 1)
                print(pool.has_free())
                print(pool.get_next())
                print(pool.has_free())

            .. testoutput::

                False
                2
                True
        """
        return len(self._idle_actors) > 0 and len(self._pending_submits) == 0

    def pop_idle(self) -> ray.actor.ActorHandle | None:
        """Removes an idle actor from the pool.

        Returns
        -------
            An idle actor if one is available.
            None if no actor was free to be removed.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1 = Actor.remote()
                pool = ActorPool([a1])
                pool.submit(lambda a, v: a.double.remote(v), 1)
                assert pool.pop_idle() is None
                assert pool.get_next() == 2
                assert pool.pop_idle() == a1

        """
        if self.has_free():
            return self._pop_idle_actor()
        return None

    @staticmethod
    def _actor_key(actor: Any) -> tuple[str, Any]:
        """Identify an actor by Ray actor ID, or by object for test doubles."""
        actor_id = _actor_id_hex(actor)
        return ("actor", actor_id) if actor_id is not None else ("object", id(actor))

    @classmethod
    def _unique_actors(cls, actors: Iterable[Any]) -> list[Any]:
        """Deduplicate actors by :meth:`_actor_key`, keeping first-seen order.

        An actor should only occupy one pool state, but transitions could
        overlap.
        """
        actors_by_key: dict[tuple[str, Any], Any] = {}
        for actor in actors:
            actors_by_key.setdefault(cls._actor_key(actor), actor)
        return list(actors_by_key.values())

    def release_idle_actors(
        self,
        *,
        idle_grace_s: float = 0.0,
        cleanup_method: str | None = None,
        cleanup_timeout: float = 10.0,
    ) -> int:
        """Kill actors that have no work left, so their resources free early.

        Call only when the caller has nothing more to submit for now. Releases
        actors idle for at least ``idle_grace_s`` seconds, and actors still
        starting up. Actors idle for less stay, so work submitted within the
        grace runs on them. Busy actors keep running, and parked actors keep
        their faulty GPU out of rotation. Each released idle actor first runs
        ``cleanup_method``, because ``ray.kill`` skips the actor's exit hooks.
        If work is submitted later, :meth:`submit` starts new actors, up to the
        pool's original size.

        Returns
        -------
            The number of actors released.
        """
        if self._pending_submits:
            return 0
        now = self._now()
        idle_since = self._idle_since_by_key()
        expired: list[Any] = []
        within_grace: list[Any] = []
        for actor in self._idle_actors:
            # An actor added without a timestamp starts its grace now.
            since = idle_since.setdefault(self._actor_key(actor), now)
            (expired if now - since >= idle_grace_s else within_grace).append(actor)
        kept = {self._actor_key(actor) for actor in within_grace}
        starting = [
            actor
            for actor in self._ready_fut_to_actor.values()
            if self._actor_key(actor) not in kept
        ]
        if not expired and not starting:
            return 0
        if cleanup_method is not None and expired:
            self._call_each(expired, cleanup_method, timeout=cleanup_timeout)
        # Drop the actors from every pool state before killing them, so a
        # startup future that fails because of the kill is never collected and
        # replaced, and liveness scans (which only track busy actors) never
        # see them.
        self._idle_actors[:] = within_grace
        for actor in expired:
            idle_since.pop(self._actor_key(actor), None)
        self._ready_fut_to_actor.clear()
        released = self._unique_actors([*expired, *starting])
        for actor in released:
            with contextlib.suppress(Exception):
                ray.kill(actor)
        self._released_slots = getattr(self, "_released_slots", 0) + len(released)
        self.job_tracker.increment.remote(  # type: ignore[attr-defined]
            self.worker_metric, -len(released)
        )
        _LOG.info(
            "Released %d actor(s) with no work left (%d idle for %.0fs or more, "
            "%d starting); %d idle within the grace, %d still busy",
            len(released),
            len(expired),
            idle_grace_s,
            len(starting),
            len(within_grace),
            len(self._future_to_actor),
        )
        return len(released)

    def shutdown(self) -> None:
        """Kill the pool's actors and stop the liveness scanner. Single-use:
        the pool must not be reused after shutdown."""
        # Cancel first, before killing actors: otherwise an in-flight scan can
        # observe the just-killed actors as missing during the kill loop and
        # start the exact-query fanout this flag is meant to prevent.
        self._liveness_scan_cancelled.set()
        owned_actors = self._unique_actors(
            [
                *self._idle_actors,
                *(actor for _, actor in self._future_to_actor.values()),
                *self._ready_fut_to_actor.values(),
                *self._parked_actors,
            ]
        )

        for actor in owned_actors:
            _LOG.debug("Shutting down actor %s", actor)
            with contextlib.suppress(Exception):
                ray.kill(actor)

        if owned_actors:
            self.job_tracker.increment.remote(  # type: ignore[attr-defined]
                self.worker_metric, -len(owned_actors)
            )

        self._idle_actors.clear()
        self._idle_since_by_key().clear()
        self._parked_actors.clear()
        self._ready_fut_to_actor.clear()
        self._future_to_actor.clear()
        self._index_to_future.clear()
        self._pending_submits.clear()
        self._future_to_task.clear()
        self._future_to_actor_id.clear()
        self._drained_buffer.clear()
        self._next_task_index = 0
        self._last_actor_liveness_scan_at = None
        # Abandon any in-flight scan without blocking teardown on its ~46s query
        # (cancelled above so it stops issuing State API calls). Single-use pool.
        self._liveness_scan_future = None
        self._liveness_scan_executor.shutdown(wait=False, cancel_futures=True)

    def broadcast(self, method: str, *, timeout: float = 10.0) -> None:
        """Best-effort, no-arg call of ``method`` on every idle actor.

        Ignores errors and actors that don't define the method. Intended for
        lifecycle hooks (e.g. a final telemetry flush) right before
        :meth:`shutdown` kills the idle actors. Busy actors are not called.
        """
        self._call_each(self._idle_actors, method, timeout=timeout)

    @staticmethod
    def _call_each(actors: Iterable[Any], method: str, *, timeout: float) -> None:
        """Best-effort, no-arg call of ``method`` on ``actors``; waits for all."""
        refs = []
        for actor in actors:
            with contextlib.suppress(Exception):
                refs.append(getattr(actor, method).remote())
        if refs:
            with contextlib.suppress(Exception):
                ray.get(refs, timeout=timeout)

    def push(self, actor) -> None:
        """Pushes a new actor into the current list of idle actors.

        Examples
        --------
            .. testcode::

                import ray
                from ray.util.actor_pool import ActorPool

                @ray.remote
                class Actor:
                    def double(self, v):
                        return 2 * v

                a1, a2 = Actor.remote(), Actor.remote()
                pool = ActorPool([a1])
                pool.push(a2)
        """
        busy_actors = []
        if self._future_to_actor.values():
            _, busy_actors = zip(*self._future_to_actor.values(), strict=False)
        if actor in self._idle_actors or actor in busy_actors:
            raise ValueError("Actor already belongs to current ActorPool")
        else:
            self._return_actor(actor)
