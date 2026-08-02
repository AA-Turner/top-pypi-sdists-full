# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Ray Authors
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# forked actor pool from ray.util.actor_pool
# we added support for FT and autoscaling to this implementation
# ordered map supoort is dropped atm, but can be added back if needed

import contextlib
import logging
import time
from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

import attrs
import ray
import ray.actor
import ray.exceptions
from ray import ObjectRef
from ray.actor import ActorHandle
from ray.util.state import list_actors

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


@attrs.define(frozen=True)
class ActorPoolTaskError(RuntimeError):
    """Raised when a submitted actor task fails due to actor loss."""

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
    def is_transient_infra_loss(self) -> bool:
        return self.preempted or _death_cause_has_node_death_info(self.death_cause)


@attrs.define(frozen=True)
class ActorLostError(RuntimeError):
    """Raised when Ray state shows a busy actor died before its future resolved."""

    snapshot: ActorStateSnapshot
    task: Any

    @property
    def is_transient_infra_loss(self) -> bool:
        return self.snapshot.is_transient_infra_loss

    def __str__(self) -> str:
        return (
            "actor lost while task was inflight "
            f"(actor_id={self.snapshot.actor_id}; state={self.snapshot.state}; "
            f"death_reason={self.snapshot.death_reason or 'unknown'}; "
            f"node_id={self.snapshot.node_id or 'unknown'}; "
            f"preempted={self.snapshot.preempted}; "
            f"death_cause={'present' if self.snapshot.death_cause else 'absent'}; "
            f"task={self.task!r})"
        )


_ACTOR_LOSS_ERRORS = (
    ray.exceptions.RayActorError,
    ray.exceptions.NodeDiedError,
)
_ACTOR_LIVENESS_SCAN_INTERVAL_S = 30.0


def _actor_id_hex(actor: Any) -> str | None:
    actor_id = getattr(actor, "_actor_id", None)
    if actor_id is None:
        return None
    hex_fn = getattr(actor_id, "hex", None)
    if callable(hex_fn):
        return str(hex_fn())
    return str(actor_id)


class ActorPool:
    """Utility class to operate on a fixed pool of actors.

    Parameters
    ----------
        actor_factory
            Factory used to create actors. This should be a callable
            that returns a new actor handle when called. The factory will be called
            num_actors times to create the initial pool of actors.
        num_actors
            Number of actors to create in the pool.
        worker_tracker
            Optional ObjectRef for tracking worker progress.

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
    ) -> None:
        # factory to create actors
        self._actor_factory = actors_factory

        # number of actors # added
        self._num_actors = num_actors

        # readyness future to actor # added
        self._ready_fut_to_actor = {}

        # actors to be used
        self._idle_actors = []

        # get actor from future
        self._future_to_actor = {}

        # get future from index
        self._index_to_future = {}

        # next task to do
        self._next_task_index = 0

        # next work depending when actors free
        self._pending_submits = []

        # the task that was submitted # added
        self._future_to_task = {}

        # actor id for each submitted future, used to detect actors that Ray has
        # marked DEAD before their task future resolves.
        self._future_to_actor_id = {}
        self._last_actor_liveness_scan_at: float | None = None

        self.worker_metric = worker_metric
        self.resubmit_on_actor_failure = resubmit_on_actor_failure

        spawn_job_tracker = job_tracker_options().remote
        self.job_tracker = job_tracker or spawn_job_tracker(  # type: ignore[call-arg]
            "fake job id", None, **job_tracker_throttle_kwargs()
        )
        self.job_tracker.set_total.remote(worker_metric, num_actors)  # type: ignore[attr-defined]
        self.job_tracker.set.remote(worker_metric, 0)  # type: ignore[attr-defined]
        ray_tqdm([], self.job_tracker, worker_metric)

        for _ in range(num_actors):
            self._queue_actor_startup()

    def _queue_actor_startup(self) -> None:
        new_actor = self._actor_factory()
        ready_fut = new_actor.__ray_ready__.remote()
        self.job_tracker.increment.remote(self.worker_metric, 1)  # type: ignore[attr-defined]
        self._ready_fut_to_actor[ready_fut] = new_actor

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

        next_fn = self.get_next_unordered

        while self.has_next():
            yield next_fn()
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
            actor = self._idle_actors.pop()
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
        return bool(self._future_to_actor) or bool(self._pending_submits)

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

        states: dict[str, ActorStateSnapshot] = {}
        for actor_id in sorted(actor_ids):
            try:
                actors = list_actors(
                    filters=[("actor_id", "=", actor_id)],
                    limit=1,
                    detail=True,
                    raise_on_missing_output=False,
                )
            except Exception:
                _LOG.debug(
                    "Failed to list Ray actor %s while checking actor liveness",
                    actor_id,
                    exc_info=True,
                )
                return None

            for actor in actors:
                returned_actor_id = getattr(actor, "actor_id", None)
                if returned_actor_id is None or str(returned_actor_id) != actor_id:
                    continue
                states[actor_id] = ActorStateSnapshot.from_ray_state(actor_id, actor)
                break
        return states

    def _cleanup_lost_actor_future(
        self, future: Any, snapshot: ActorStateSnapshot
    ) -> tuple[Any, Any, ActorLostError]:
        actor, fn, task = self._pop_future_state(future)
        lost_error = ActorLostError(snapshot=snapshot, task=task)
        _LOG.error(
            "Actor %s became %s while running task %r; death_reason=%s; "
            "preempted=%s; cleaning it up",
            snapshot.actor_id,
            snapshot.state,
            task,
            snapshot.death_reason,
            snapshot.preempted,
        )
        with contextlib.suppress(Exception):
            ray.kill(actor)
        self._queue_actor_startup()
        return fn, task, lost_error

    def _pop_dead_actor_task(self) -> Any | NoResult:
        actor_ids = set(self._future_to_actor_id.values())
        if not actor_ids:
            return self.NoResult

        now = time.monotonic()
        last_scan_at = getattr(self, "_last_actor_liveness_scan_at", None)
        if (
            last_scan_at is not None
            and now - last_scan_at < self._actor_liveness_scan_interval_s
        ):
            return self.NoResult

        states = self._actor_states_by_id(actor_ids)
        if states is None:
            return self.NoResult
        dead_futures = []
        for future, actor_id in list(self._future_to_actor_id.items()):
            actor_state = states.get(actor_id)
            if actor_state is None or actor_state.state != "DEAD":
                continue
            dead_futures.append((future, actor_state))

        if not dead_futures:
            self._last_actor_liveness_scan_at = now
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

        self._last_actor_liveness_scan_at = now
        lost_tasks = []
        for future, actor_state in dead_futures:
            lost_tasks.append(self._cleanup_lost_actor_future(future, actor_state))

        for fn, task, _cause in lost_tasks:
            self.submit(fn, task)
        return self.NoResult

    def _get_next_by_fut(self, futures, timeout=None) -> Any | NoResult:
        timeout_msg = "Timed out waiting for result"

        # get_next will just pass a single future
        # get_next_unordered will pass a list of futures
        res, _ = ray.wait(futures, num_returns=1, timeout=timeout, fetch_local=True)
        if res:
            [future] = res
        else:
            raise TimeoutError(timeout_msg)

        a, fn, task = self._pop_future_state(future)

        try:
            # this is fast because ray.wait already fetched the result
            res = ray.get(future)
            # don't return the future till we get the result
            # because the actor could be dead
            self._return_actor(a)
        except ray.exceptions.OutOfMemoryError as e:
            # Ray's memory monitor kills the worker and raises
            # OutOfMemoryError (a RayError, not a RayActorError), so it
            # bypasses the actor-loss handling below. Never silently
            # resubmit an OOM at the same size: surface it as a typed task
            # failure so the caller's OOM recovery (budget + shrink) runs.
            _LOG.exception("Task killed by Ray memory monitor")
            with contextlib.suppress(Exception):
                ray.kill(a)
            self._queue_actor_startup()
            raise ActorPoolTaskError(task=task, cause=e) from e
        except _ACTOR_LOSS_ERRORS as e:
            _LOG.exception("Actor died or unavailable, cleaning it up")
            with contextlib.suppress(Exception):
                ray.kill(a)
            # queue a new actor
            self._queue_actor_startup()
            if self.resubmit_on_actor_failure:
                # resubmit the task
                self.submit(fn, task)
                return self.NoResult
            raise ActorPoolTaskError(task=task, cause=e) from e

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
            TimeoutError
                if the timeout is reached.

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

            futs = list(self._future_to_actor)
            if not futs:
                # No inflight yet; spin until at least one submission exists
                self._collect_ready_actors()
                futs = list(self._future_to_actor)
                if not futs:
                    continue

            current_timeout = poll_timeout
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Timed out waiting for result")
                current_timeout = min(current_timeout, remaining)

            try:
                item = self._get_next_by_fut(futs, current_timeout)
            except TimeoutError:
                item = self._pop_dead_actor_task()
                if item is not self.NoResult:
                    return item
                if deadline is not None and deadline - time.monotonic() <= 0:
                    raise
                # No task finished within the poll interval; loop to collect more actors
                continue

            if item is not self.NoResult:
                return item

    def _return_actor(self, actor) -> None:
        self._idle_actors.append(actor)
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
            return self._idle_actors.pop()
        return None

    def shutdown(self) -> None:
        while (actor := self.pop_idle()) is not None:
            _LOG.debug("Shutting down actor %s", actor)
            ray.kill(actor)
            self.job_tracker.increment.remote("workers", -1)  # type: ignore[attr-defined]

    def broadcast(self, method: str, *, timeout: float = 10.0) -> None:
        """Best-effort, no-arg call of ``method`` on every idle actor.

        Ignores errors and actors that don't define the method. Intended for
        lifecycle hooks (e.g. a final telemetry flush) right before
        :meth:`shutdown`, when all tasks have drained and every actor is idle.
        """
        refs = []
        for actor in self._idle_actors:
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
