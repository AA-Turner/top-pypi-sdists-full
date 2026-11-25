# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
import logging
import random
import threading
import time
from collections.abc import Iterable
from concurrent.futures import Future, ThreadPoolExecutor
from types import SimpleNamespace
from typing import Any, cast

import pytest
import ray
from google.protobuf.json_format import MessageToDict
from ray.core.generated import common_pb2

from geneva.errors import FatalWorkerHardwareError
from geneva.runners.ray import actor_pool as actor_pool_mod
from geneva.runners.ray import jobtracker as jobtracker_mod
from geneva.runners.ray.actor_pool import (
    ActorLostError,
    ActorPool,
    ActorPoolTaskError,
    ActorStateSnapshot,
)
from geneva.runners.ray.jobtracker import _JobTracker


class _InlineExecutor:
    """Runs submitted work synchronously and returns an already-completed
    Future. Lets liveness-scan detection tests drive the background-scan flow
    deterministically (start on one poll, consume on the next) without threads.
    """

    def submit(self, fn, /, *args, **kwargs) -> Future:
        future: Future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except BaseException as exc:  # noqa: BLE001
            future.set_exception(exc)
        return future

    def shutdown(self, *args: object, **kwargs: object) -> None:
        return None


def _dead_actor_state(
    actor_id: str,
    *,
    death_reason: str = "WORKER_DIED",
    node_death_info: bool = False,
    node_death_reason: str = "AUTOSCALER_DRAIN_PREEMPTED",
) -> SimpleNamespace:
    death_cause = common_pb2.ActorDeathCause()
    actor_context = death_cause.actor_died_error_context
    actor_context.reason = getattr(common_pb2.ActorDiedErrorContext, death_reason)
    if node_death_info:
        actor_context.node_death_info.reason = getattr(
            common_pb2.NodeDeathInfo,
            node_death_reason,
        )
    return SimpleNamespace(
        actor_id=actor_id,
        state="DEAD",
        death_cause=MessageToDict(death_cause),
        node_id="node-1",
        num_restarts_due_to_node_preemption=1 if "PREEMPT" in death_reason else 0,
    )


def _dead_oom_actor_state(actor_id: str) -> SimpleNamespace:
    death_cause = common_pb2.ActorDeathCause()
    death_cause.oom_context.error_message = "Task failed due to OOM"
    death_cause.oom_context.fail_immediately = True
    return SimpleNamespace(
        actor_id=actor_id,
        state="DEAD",
        death_cause=MessageToDict(death_cause, preserving_proto_field_name=True),
        node_id="node-1",
        num_restarts_due_to_node_preemption=0,
    )


def _alive_actor_state(actor_id: str) -> SimpleNamespace:
    return SimpleNamespace(actor_id=actor_id, state="ALIVE")


def _record_worker_metric(pool: ActorPool) -> list[tuple[str, int]]:
    """Give a bare pool a job tracker that records worker-metric deltas."""
    updates: list[tuple[str, int]] = []
    pool.worker_metric = "workers"
    pool.job_tracker = SimpleNamespace(
        increment=SimpleNamespace(
            remote=lambda metric, delta: updates.append((metric, delta))
        )
    )
    return updates


@ray.remote
class TestActor:
    def echo(self, i: int) -> int:
        return i


@pytest.mark.parametrize(
    ("num_calls", "num_actors"),
    list(itertools.product([1000], [7])),
)
@pytest.mark.ray
def test_actor_pool(
    num_calls: int,
    num_actors: int,
) -> None:
    # do it twice should not affect the result
    pool = ActorPool(TestActor.remote, num_actors)
    unordered_res = pool.map_unordered(
        lambda actor, i: actor.echo.remote(i), range(num_calls)
    )
    unordered_res = list(unordered_res)
    assert list(range(num_calls)) == sorted(unordered_res)
    assert len(unordered_res) == num_calls
    assert list(range(num_calls)) != unordered_res
    pool.shutdown()


@pytest.mark.parametrize(
    ("running", "pending", "expected"),
    [
        (0, 0, 9),
        (8, 0, 1),
        (8, 1, 0),
        (3, 2, 4),
    ],
)
def test_submission_capacity_preserves_actor_plus_one_bound(
    running: int,
    pending: int,
    expected: int,
) -> None:
    pool = object.__new__(ActorPool)
    pool._num_actors = 8
    pool._future_to_actor = {object(): (index, object()) for index in range(running)}
    pool._pending_submits = [(object(), index) for index in range(pending)]

    assert pool.submission_capacity() == expected


def test_actor_pool_shutdown_clears_all_actor_states_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    idle_actor = object()
    busy_actor = object()
    starting_actor = object()
    shared_actor = object()
    parked_actor = object()
    busy_future = object()
    shared_future = object()
    starting_future = object()
    duplicate_starting_future = object()
    metric_updates: list[tuple[str, int]] = []
    killed: list[object] = []

    pool._idle_actors = [idle_actor, shared_actor]
    pool._future_to_actor = {
        busy_future: (0, busy_actor),
        shared_future: (1, shared_actor),
    }
    pool._ready_fut_to_actor = {
        starting_future: starting_actor,
        duplicate_starting_future: shared_actor,
    }
    pool._index_to_future = {0: busy_future, 1: shared_future}
    pool._parked_actors = [parked_actor]
    pool._pending_submits = [(object(), "pending-task")]
    pool._future_to_task = {
        busy_future: (object(), "busy-task"),
        shared_future: (object(), "shared-task"),
    }
    pool._future_to_actor_id = {
        busy_future: "busy-actor",
        shared_future: "shared-actor",
    }
    pool._drained_buffer = ["stranded-result"]
    pool._next_task_index = 2
    pool._last_actor_liveness_scan_at = time.monotonic()
    pool._liveness_scan_future = Future()
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()
    pool.worker_metric = "test-workers"
    pool.job_tracker = SimpleNamespace(
        increment=SimpleNamespace(
            remote=lambda metric, delta: metric_updates.append((metric, delta))
        )
    )
    monkeypatch.setattr(ray, "kill", lambda actor: killed.append(actor))

    pool.shutdown()
    pool.shutdown()

    assert killed == [
        idle_actor,
        shared_actor,
        busy_actor,
        starting_actor,
        parked_actor,
    ]
    assert metric_updates == [("test-workers", -5)]
    assert pool._idle_actors == []
    assert pool._parked_actors == []
    assert pool._ready_fut_to_actor == {}
    assert pool._future_to_actor == {}
    assert pool._index_to_future == {}
    assert pool._pending_submits == []
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._drained_buffer == []
    assert pool._liveness_scan_future is None
    assert pool._liveness_scan_cancelled.is_set()
    assert pool._next_task_index == 0
    assert pool._last_actor_liveness_scan_at is None


@pytest.mark.parametrize(
    ("actor_state", "death_reason", "is_oom_loss"),
    [
        pytest.param(
            _dead_actor_state("actor-dead"),
            "WORKER_DIED",
            False,
            id="worker-died",
        ),
        pytest.param(
            _dead_oom_actor_state("actor-dead"),
            None,
            True,
            id="oom-context",
        ),
    ],
)
@pytest.mark.slow
def test_actor_pool_detects_dead_busy_actor_before_future_ready(
    monkeypatch: pytest.MonkeyPatch,
    actor_state: SimpleNamespace,
    death_reason: str | None,
    is_oom_loss: bool,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace()
    task = "task-1"
    queued_replacements: list[bool] = []

    pool._ready_fut_to_actor = {}
    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._pending_submits = []
    pool._drained_buffer = []
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool.resubmit_on_actor_failure = False
    # Inline executor: one poll starts the scan, the next consumes it, all
    # within get_next_unordered's poll loop.
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    metric_updates = _record_worker_metric(pool)
    pool._get_next_by_fut = lambda _futs, _timeout=None: (_ for _ in ()).throw(
        actor_pool_mod.PollTimeoutError("not ready")
    )

    def list_alive_actors(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        assert ("state", "=", "ALIVE") in filters
        return []

    pool._actor_state_by_id = lambda actor_id: ActorStateSnapshot.from_ray_state(
        actor_id,
        actor_state,
    )

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_alive_actors,
    )
    # The lost future has no result available (actor died mid-task).
    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([], list(futures)))

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool.get_next_unordered(timeout=1.0)

    assert exc_info.value.task == task
    assert isinstance(exc_info.value.cause, ActorLostError)
    assert "actor-dead" in str(exc_info.value.cause)
    assert exc_info.value.cause.snapshot.death_reason == death_reason
    assert exc_info.value.cause.is_oom_loss is is_oom_loss
    assert isinstance(exc_info.value.cause.snapshot, ActorStateSnapshot)
    assert pool._future_to_actor == {}
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._index_to_future == {}
    assert queued_replacements == [True]
    # The lost actor leaves the worker count; its replacement adds itself back.
    assert metric_updates == [("workers", -1)]


def test_actor_pool_resubmits_transient_dead_busy_actor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"
    queued_replacements: list[bool] = []
    resubmitted: list[str] = []

    def submit(_fn: object, task: str) -> None:
        resubmitted.append(task)

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._pending_submits = []
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()
    pool.resubmit_on_actor_failure = True
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = submit
    metric_updates = _record_worker_metric(pool)

    def list_alive_actors(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        assert ("state", "=", "ALIVE") in filters
        return []

    dead_actor_state = _dead_actor_state(
        "actor-dead",
        death_reason="NODE_DIED",
        node_death_info=True,
    )
    pool._actor_state_by_id = lambda actor_id: ActorStateSnapshot.from_ray_state(
        actor_id,
        dead_actor_state,
    )

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_alive_actors,
    )
    # The lost future has no result available (actor died mid-task).
    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([], list(futures)))

    # First poll starts the background scan; nothing is cleaned up yet.
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert resubmitted == []
    assert metric_updates == []
    # Second poll consumes the finished scan and resubmits the lost task.
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert pool._future_to_actor == {}
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._index_to_future == {}
    assert queued_replacements == [True]
    assert resubmitted == [task]
    assert metric_updates == [("workers", -1)]


def test_node_died_reason_is_transient_without_optional_node_death_info() -> None:
    actor_state = _dead_actor_state(
        "actor-dead",
        death_reason="NODE_DIED",
        node_death_info=False,
    )

    snapshot = ActorStateSnapshot.from_ray_state("actor-dead", actor_state)

    assert snapshot.death_reason == "NODE_DIED"
    assert snapshot.is_transient_infra_loss is True


@pytest.mark.parametrize(
    ("actor_state", "expected_transient"),
    [
        pytest.param(
            _dead_actor_state(
                "actor-dead",
                death_reason="NODE_DIED",
                node_death_info=True,
                node_death_reason="EXPECTED_TERMINATION",
            ),
            True,
            id="node-died",
        ),
        pytest.param(
            _dead_actor_state("actor-dead", death_reason="WORKER_DIED"),
            False,
            id="worker-died",
        ),
    ],
)
def test_actor_pool_rehydrates_ready_actor_death_from_state(
    monkeypatch: pytest.MonkeyPatch,
    actor_state: SimpleNamespace,
    expected_transient: bool,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"
    queried_actor_ids: list[str] = []
    queued_replacements: list[bool] = []

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool.resubmit_on_actor_failure = False
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    metric_updates = _record_worker_metric(pool)

    actor_died = ray.exceptions.ActorDiedError(None)

    def raise_actor_died(_future: object) -> None:
        raise actor_died

    def actor_state_by_id(_self: ActorPool, actor_id: str) -> ActorStateSnapshot:
        queried_actor_ids.append(actor_id)
        return ActorStateSnapshot.from_ray_state(actor_id, actor_state)

    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([future], []))
    monkeypatch.setattr(ray, "get", raise_actor_died)
    monkeypatch.setattr(ray, "kill", lambda _actor: None)
    monkeypatch.setattr(
        ActorPool,
        "_actor_state_by_id",
        actor_state_by_id,
        raising=False,
    )

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert queried_actor_ids == ["actor-dead"]
    assert exc_info.value.task == task
    assert isinstance(exc_info.value.cause, ActorLostError)
    assert exc_info.value.cause.snapshot.death_reason == (
        "NODE_DIED" if expected_transient else "WORKER_DIED"
    )
    assert exc_info.value.cause.is_transient_infra_loss is expected_transient
    assert queued_replacements == [True]
    assert metric_updates == [("workers", -1)]


def test_actor_pool_keeps_raw_ready_actor_error_when_state_lookup_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"
    actor_died = ray.exceptions.ActorDiedError(None)

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool.resubmit_on_actor_failure = False
    pool._queue_actor_startup = lambda: None
    metric_updates = _record_worker_metric(pool)

    def raise_actor_died(_future: object) -> None:
        raise actor_died

    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([future], []))
    monkeypatch.setattr(ray, "get", raise_actor_died)
    monkeypatch.setattr(ray, "kill", lambda _actor: None)
    monkeypatch.setattr(ActorPool, "_actor_state_by_id", lambda _self, _id: None)

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert exc_info.value.cause is actor_died
    assert metric_updates == [("workers", -1)]


def test_actor_liveness_scan_batches_alive_state_query_and_checks_missing_actor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    actor_ids = {f"actor-{idx:04d}" for idx in range(2621)}
    dead_actor_id = "actor-1337"
    bulk_calls: list[dict[str, object]] = []
    exact_calls: list[str] = []

    def list_alive_actors(**kwargs: object) -> list[SimpleNamespace]:
        bulk_calls.append(kwargs)
        return [
            _alive_actor_state(actor_id)
            for actor_id in actor_ids
            if actor_id != dead_actor_id
        ]

    def exact_actor_state(actor_id: str) -> ActorStateSnapshot:
        exact_calls.append(actor_id)
        return ActorStateSnapshot.from_ray_state(
            actor_id,
            _dead_actor_state(actor_id, death_reason="NODE_DIED"),
        )

    pool._actor_state_by_id = exact_actor_state

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_alive_actors,
    )
    # The lost future has no result available (actor died mid-task).
    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([], list(futures)))

    states = pool._actor_states_by_id(actor_ids)

    assert states is not None
    assert set(states) == {dead_actor_id}
    assert exact_calls == [dead_actor_id]
    assert len(bulk_calls) == 1
    filters = bulk_calls[0]["filters"]
    assert isinstance(filters, list)
    assert ("job_id", "=", "job-1") in filters
    assert ("state", "=", "ALIVE") in filters
    assert bulk_calls[0]["address"] == "gcs-1"
    assert bulk_calls[0]["detail"] is False
    assert bulk_calls[0]["raise_on_missing_output"] is False


def test_actor_liveness_scan_skips_exact_queries_when_all_busy_actors_are_alive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    actor_ids = {f"actor-{idx:04d}" for idx in range(2621)}

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        lambda **_kwargs: [_alive_actor_state(actor_id) for actor_id in actor_ids],
    )
    pool._actor_state_by_id = lambda _actor_id: pytest.fail(
        "all busy actors were present in the ALIVE bulk result"
    )

    assert pool._actor_states_by_id(actor_ids) == {}


def test_actor_liveness_scan_treats_truncated_alive_results_as_unknown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    actor_ids = {"actor-alive-returned", "actor-alive-missing", "actor-dead"}
    exact_calls: list[str] = []

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        lambda **_kwargs: [_alive_actor_state("actor-alive-returned")],
    )

    def exact_actor_state(actor_id: str) -> ActorStateSnapshot:
        exact_calls.append(actor_id)
        state = (
            _dead_actor_state(actor_id, death_reason="NODE_DIED")
            if actor_id == "actor-dead"
            else _alive_actor_state(actor_id)
        )
        return ActorStateSnapshot.from_ray_state(actor_id, state)

    pool._actor_state_by_id = exact_actor_state

    states = pool._actor_states_by_id(actor_ids)

    assert states is not None
    assert set(exact_calls) == {"actor-alive-missing", "actor-dead"}
    assert states["actor-alive-missing"].state == "ALIVE"
    assert states["actor-dead"].state == "DEAD"


def test_actor_liveness_scan_does_not_fan_out_when_bulk_query_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    pool._actor_state_by_id = lambda _actor_id: pytest.fail(
        "bulk State API failures must not trigger exact-query fanout"
    )

    def fail_bulk_query(**_kwargs: object) -> list[SimpleNamespace]:
        raise RuntimeError("State API unavailable")

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        fail_bulk_query,
    )

    assert pool._actor_states_by_id({"actor-1", "actor-2"}) is None


def test_actor_states_by_id_aborts_before_bulk_query_when_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A scan cancelled by shutdown skips even the bulk State API query."""
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_cancelled.set()

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        lambda **_kwargs: pytest.fail("cancelled scan must not query the State API"),
    )
    assert pool._actor_states_by_id({"actor-1", "actor-2"}) is None


def test_actor_states_by_id_skips_fanout_when_cancelled_mid_scan(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If the pool is torn down during the bulk query, the exact-query fanout for
    the just-killed (now-missing) actors is skipped."""
    pool = object.__new__(ActorPool)
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    pool._actor_state_by_id = lambda _actor_id: pytest.fail(
        "cancelled scan must not fan out exact queries"
    )

    def list_and_cancel(**_kwargs: object) -> list[SimpleNamespace]:
        pool._liveness_scan_cancelled.set()  # shutdown lands during the bulk query
        return []  # every busy actor now looks missing

    monkeypatch.setattr("geneva.runners.ray.actor_pool.list_actors", list_and_cancel)
    assert pool._actor_states_by_id({"actor-1", "actor-2"}) is None


def test_actor_state_by_id_short_circuits_when_cancelled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Per-actor lookups short-circuit once cancelled, so an in-flight fanout
    drains fast instead of issuing thousands of get_actor calls post-shutdown."""
    pool = object.__new__(ActorPool)
    pool._gcs_address = "gcs-1"
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_cancelled.set()

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.get_actor",
        lambda *_args, **_kwargs: pytest.fail("cancelled scan must not call get_actor"),
    )
    assert pool._actor_state_by_id("actor-1") is None


def test_get_next_unordered_consumes_completed_scan_even_when_results_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A busy pool that never times out must still consume a finished scan and
    surface the dead actor it found, rather than stranding it forever."""
    pool = object.__new__(ActorPool)
    dead_future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"

    pool._ready_fut_to_actor = {}
    pool._future_to_actor = {dead_future: (0, actor)}
    pool._index_to_future = {0: dead_future}
    pool._pending_submits = []
    pool._drained_buffer = []
    pool._future_to_task = {dead_future: (lambda _a, _t: None, task)}
    pool._future_to_actor_id = {dead_future: "actor-dead"}
    pool._last_actor_liveness_scan_at = None
    pool.resubmit_on_actor_failure = False
    pool._collect_ready_actors = lambda: None
    pool._queue_actor_startup = lambda: None
    metric_updates = _record_worker_metric(pool)

    scan_future: Future = Future()
    scan_future.set_result(
        {
            "actor-dead": ActorStateSnapshot.from_ray_state(
                "actor-dead",
                _dead_actor_state("actor-dead", death_reason="WORKER_DIED"),
            )
        }
    )
    pool._liveness_scan_future = scan_future
    # A result is ready (busy pool), but the completed scan must be consumed
    # first -- so _get_next_by_fut is never reached.
    pool._get_next_by_fut = lambda _futs, _timeout=None: pytest.fail(
        "completed dead-actor scan must be consumed before fetching a result"
    )
    # The dead actor's task future is not ready (it truly died mid-task).
    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([], list(futures)))
    monkeypatch.setattr("geneva.runners.ray.actor_pool.ray.kill", lambda _a: None)

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool.get_next_unordered(timeout=1.0)

    assert exc_info.value.task == task
    assert pool._liveness_scan_future is None
    assert pool._future_to_actor_id == {}
    assert metric_updates == [("workers", -1)]


def test_handle_dead_actor_states_skips_future_with_ready_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A future whose result is already available (task finished, then the actor
    died) must not be classified as lost -- no raise, no resubmit."""
    pool = object.__new__(ActorPool)
    ready_future = object()
    pool._future_to_actor_id = {ready_future: "actor-dead"}
    pool.resubmit_on_actor_failure = False
    pool._cleanup_lost_actor_future = lambda *_a: pytest.fail(
        "a future whose result is ready is not lost"
    )
    # ray.wait reports the future's result as already available.
    wait_kwargs: dict[str, object] = {}

    def _wait(futures: object, **kwargs: object) -> tuple[list, list]:
        wait_kwargs.update(kwargs)
        return (list(futures), [])  # type: ignore[arg-type]

    monkeypatch.setattr(ray, "wait", _wait)

    states = {
        "actor-dead": ActorStateSnapshot.from_ray_state(
            "actor-dead",
            _dead_actor_state("actor-dead", death_reason="WORKER_DIED"),
        )
    }
    assert pool._handle_dead_actor_states(states) is pool.NoResult
    # A completion check, not a fetch: a remote-but-undownloaded result counts
    # as done and must not be misreported as lost.
    assert wait_kwargs.get("fetch_local") is False


@pytest.mark.parametrize(
    "scan_result",
    [None, {}],
    ids=["failed-scan", "successful-empty-scan"],
)
def test_actor_liveness_scan_rate_limits_from_scan_completion(
    monkeypatch: pytest.MonkeyPatch,
    scan_result: dict[str, ActorStateSnapshot] | None,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    calls = 0
    monotonic_times = iter([0.0, 31.0, 31.0, 31.0])

    pool._future_to_actor_id = {future: "actor-1"}
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()

    def scan(_actor_ids: set[str]) -> dict[str, ActorStateSnapshot] | None:
        nonlocal calls
        calls += 1
        return scan_result

    pool._actor_states_by_id = scan
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.time.monotonic",
        lambda: next(monotonic_times),
    )

    # First poll runs a scan (completes inline); the second, within the
    # interval of that completion, must not start another.
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert calls == 1


def test_actor_pool_does_not_resubmit_non_transient_dead_busy_actor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"
    queued_replacements: list[bool] = []
    resubmitted: list[str] = []

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._pending_submits = []
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool._job_id = "job-1"
    pool._gcs_address = "gcs-1"
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()
    pool.resubmit_on_actor_failure = True
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = lambda _fn, submitted_task: resubmitted.append(submitted_task)
    metric_updates = _record_worker_metric(pool)

    def list_alive_actors(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        assert ("state", "=", "ALIVE") in filters
        return []

    dead_actor_state = _dead_actor_state(
        "actor-dead",
        death_reason="WORKER_DIED",
    )
    pool._actor_state_by_id = lambda actor_id: ActorStateSnapshot.from_ray_state(
        actor_id,
        dead_actor_state,
    )

    monkeypatch.setattr("geneva.runners.ray.actor_pool.ray.kill", lambda _actor: None)
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_alive_actors,
    )
    # The lost future has no result available (actor died mid-task).
    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([], list(futures)))

    # First poll starts the scan; the second consumes it and raises for the
    # non-transiently-dead actor instead of resubmitting.
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert resubmitted == []
    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._pop_dead_actor_task()

    assert exc_info.value.task == task
    assert isinstance(exc_info.value.cause, ActorLostError)
    assert exc_info.value.cause.snapshot.death_reason == "WORKER_DIED"
    assert pool._future_to_actor == {}
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._index_to_future == {}
    assert queued_replacements == [True]
    assert resubmitted == []
    assert metric_updates == [("workers", -1)]


def test_liveness_scan_runs_off_main_thread_without_blocking() -> None:
    """The poll that starts a scan returns immediately; the (slow) scan runs on
    the background executor and is consumed by a later poll."""
    pool = object.__new__(ActorPool)
    pool._future_to_actor_id = {object(): "actor-1"}
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="test-liveness"
    )

    started = threading.Event()
    release = threading.Event()

    def blocking_scan(_actor_ids: set[str]) -> dict[str, ActorStateSnapshot]:
        started.set()
        assert release.wait(timeout=5.0)
        return {}

    pool._actor_states_by_id = blocking_scan
    try:
        # Starting the scan must not block on its execution.
        start = time.monotonic()
        assert pool._pop_dead_actor_task() is pool.NoResult
        assert time.monotonic() - start < 1.0
        assert started.wait(timeout=5.0)  # scan is running in the background

        # While it is in flight, further polls are non-blocking no-ops.
        assert pool._pop_dead_actor_task() is pool.NoResult

        # Once it finishes, the next poll consumes it (no dead actors found).
        release.set()
        pool._liveness_scan_future.result(timeout=5.0)
        assert pool._pop_dead_actor_task() is pool.NoResult
        assert pool._liveness_scan_future is None
    finally:
        release.set()
        pool._liveness_scan_executor.shutdown(wait=False, cancel_futures=True)


def test_liveness_scan_is_single_flight() -> None:
    """Repeated polls while a scan is in flight never start a second scan."""
    pool = object.__new__(ActorPool)
    pool._future_to_actor_id = {object(): "actor-1"}
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="test-liveness"
    )

    started = threading.Event()
    release = threading.Event()
    scan_runs = 0

    def blocking_scan(_actor_ids: set[str]) -> dict[str, ActorStateSnapshot]:
        nonlocal scan_runs
        scan_runs += 1
        started.set()
        assert release.wait(timeout=5.0)
        return {}

    pool._actor_states_by_id = blocking_scan
    try:
        futures_seen = set()
        for _ in range(5):
            assert pool._pop_dead_actor_task() is pool.NoResult
            futures_seen.add(id(pool._liveness_scan_future))
        assert started.wait(timeout=5.0)
        assert len(futures_seen) == 1  # the same single in-flight scan throughout
        assert scan_runs == 1
    finally:
        release.set()
        pool._liveness_scan_executor.shutdown(wait=False, cancel_futures=True)


@pytest.mark.parametrize(
    ("num_calls", "num_actors"),
    list(itertools.product([1000], [7])),
)
@pytest.mark.ray
def test_actor_pool_fault_tolerance(
    num_calls: int, num_actors: int, monkeypatch
) -> None:
    # do it twice should not affect the result
    original_return_actor = ActorPool._return_actor

    def faulty_return_actor(self, actor) -> None:
        if random.random() < 0.01:
            ray.kill(actor)

        original_return_actor(self, actor)

    monkeypatch.setattr(ActorPool, "_return_actor", faulty_return_actor)

    pool = ActorPool(TestActor.remote, num_actors)
    for _ in range(2):
        unordered_res = pool.map_unordered(
            lambda actor, i: actor.echo.remote(i), range(num_calls)
        )
        unordered_res = list(unordered_res)
        assert list(range(num_calls)) == sorted(unordered_res)
        assert len(unordered_res) == num_calls
        assert list(range(num_calls)) != unordered_res
    pool.shutdown()


def test_actor_pool_wraps_memory_monitor_oom_as_task_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Monitor-raised ``OutOfMemoryError`` is a ``RayError``, not a
    ``RayActorError``, so the actor-loss handling does not see it. It must
    surface as ``ActorPoolTaskError`` so the caller's OOM recovery runs, and
    must never be silently resubmitted at the same size."""
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-1")
    task = "task-1"
    queued_replacements: list[bool] = []
    killed: list[object] = []
    resubmitted: list[str] = []

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-oom"}
    # Even with silent resubmission enabled, an OOM must raise.
    pool.resubmit_on_actor_failure = True
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = lambda _fn, task: resubmitted.append(task)
    metric_updates = _record_worker_metric(pool)

    oom = ray.exceptions.OutOfMemoryError(
        "Task was killed due to the node running low on memory"
    )

    def _raise_oom(_future: object) -> None:
        raise oom

    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([future], []))
    monkeypatch.setattr(ray, "get", _raise_oom)
    monkeypatch.setattr(ray, "kill", lambda a: killed.append(a))

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert exc_info.value.cause is oom
    assert exc_info.value.task == task
    assert killed == [actor]
    assert queued_replacements == [True]
    assert resubmitted == []
    assert metric_updates == [("workers", -1)]


def _pool_with_one_busy_actor(
    monkeypatch: pytest.MonkeyPatch, error: Exception, *, num_gpus: float | None
) -> tuple[ActorPool, object, object, list[object], list[bool], list[tuple[str, int]]]:
    pool = object.__new__(ActorPool)
    future = object()
    actor = SimpleNamespace(name="actor-gpu")
    queued_replacements: list[bool] = []
    killed: list[object] = []

    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._future_to_task = {future: (lambda _actor, _task: None, "task-gpu")}
    pool._future_to_actor_id = {future: "actor-gpu"}
    pool.resubmit_on_actor_failure = False
    pool._actor_num_gpus = num_gpus
    pool._parked_actors = []
    pool.last_hardware_fault = None
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = lambda _fn, _task: pytest.fail("must not resubmit")
    metric_updates = _record_worker_metric(pool)

    def _raise(_future: object) -> None:
        raise error

    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([future], []))
    monkeypatch.setattr(ray, "get", _raise)
    monkeypatch.setattr(ray, "kill", lambda a: killed.append(a))
    return pool, future, actor, killed, queued_replacements, metric_updates


def test_actor_pool_parks_whole_gpu_actor_after_hardware_fault(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A parked actor stays alive so its GPU allocation is never handed to
    the replacement; the task still surfaces for driver-managed recovery."""
    fault = FatalWorkerHardwareError("GPU 0 requires reset")
    pool, future, actor, killed, queued, metric_updates = _pool_with_one_busy_actor(
        monkeypatch, fault, num_gpus=1.0
    )

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert exc_info.value.cause is fault
    assert exc_info.value.task == "task-gpu"
    assert killed == []
    assert pool._parked_actors == [actor]
    assert pool.last_hardware_fault is fault
    assert queued == [True]
    # Still alive and holding its GPU: it stays counted until shutdown.
    assert metric_updates == []


def test_actor_pool_kills_shared_gpu_actor_after_hardware_fault(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without a whole-GPU allocation there is nothing to withhold, so the
    actor is retired the ordinary way."""
    fault = FatalWorkerHardwareError("GPU 0 requires reset")
    pool, future, actor, killed, queued, metric_updates = _pool_with_one_busy_actor(
        monkeypatch, fault, num_gpus=0.5
    )

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert exc_info.value.cause is fault
    assert killed == [actor]
    assert pool._parked_actors == []
    assert pool.last_hardware_fault is fault
    assert queued == [True]
    assert metric_updates == [("workers", -1)]


def _bare_pool_with_fake_actors(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[ActorPool, list[tuple[str, int]], set[object], dict[object, Exception]]:
    """A pool whose real startup, collect, resolve and shutdown run on fakes.

    Returns the pool, its recorded worker-metric deltas, the ready futures
    whose startup fails, and task futures mapped to the error they raise.
    """
    pool = object.__new__(ActorPool)
    metric_updates = _record_worker_metric(pool)
    failing_startups: set[object] = set()
    task_errors: dict[object, Exception] = {}

    def factory() -> SimpleNamespace:
        ready = object()
        return SimpleNamespace(__ray_ready__=SimpleNamespace(remote=lambda: ready))

    def fake_get(future: object) -> str:
        if future in failing_startups:
            raise ray.exceptions.ActorDiedError(None)
        if future in task_errors:
            raise task_errors[future]
        return "ok"

    pool._actor_factory = factory
    pool._actor_num_gpus = 1.0
    pool.last_hardware_fault = None
    pool.resubmit_on_actor_failure = False
    pool._ready_fut_to_actor = {}
    pool._idle_actors = []
    pool._parked_actors = []
    pool._future_to_actor = {}
    pool._index_to_future = {}
    pool._future_to_task = {}
    pool._future_to_actor_id = {}
    pool._pending_submits = []
    pool._drained_buffer = []
    pool._next_task_index = 0
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._liveness_scan_executor = _InlineExecutor()
    monkeypatch.setattr(
        ray, "wait", lambda futures, **_kwargs: (list(futures)[:1], list(futures)[1:])
    )
    monkeypatch.setattr(ray, "get", fake_get)
    monkeypatch.setattr(ray, "kill", lambda _actor: None)
    return pool, metric_updates, failing_startups, task_errors


def _submit_tracked(pool: ActorPool, count: int) -> list[object]:
    """Submit ``count`` tasks to idle actors and return their futures."""
    futures: list[object] = []

    def run(_actor: object, _value: int) -> object:
        future = object()
        futures.append(future)
        return future

    for value in range(count):
        pool.submit(run, value)
    return futures


def test_actor_pool_failed_startup_leaves_worker_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An actor whose startup fails was counted when queued, so it is
    subtracted when dropped; its replacement counts itself."""
    pool, metric_updates, failing_startups, _ = _bare_pool_with_fake_actors(monkeypatch)
    for _ in range(2):
        pool._queue_actor_startup()
    failing_startups.add(next(iter(pool._ready_fut_to_actor)))

    pool._collect_ready_actors()

    assert len(pool._idle_actors) == 2
    assert pool._ready_fut_to_actor == {}
    assert metric_updates == [
        ("workers", 1),
        ("workers", 1),
        ("workers", -1),
        ("workers", 1),
    ]


def test_actor_pool_worker_count_unchanged_when_no_actor_dies(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool, metric_updates, _, _ = _bare_pool_with_fake_actors(monkeypatch)
    for _ in range(2):
        pool._queue_actor_startup()
    pool._collect_ready_actors()
    for future in _submit_tracked(pool, 2):
        assert pool._resolve_future(future) == "ok"

    assert metric_updates == [("workers", 1), ("workers", 1)]
    pool.shutdown()
    assert metric_updates == [("workers", 1), ("workers", 1), ("workers", -2)]


def test_actor_pool_worker_count_ends_at_zero_after_actor_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Started minus gone: each death subtracts once, replacements add back,
    and shutdown subtracts only actors it still owns, parked ones included."""
    pool, metric_updates, failing_startups, task_errors = _bare_pool_with_fake_actors(
        monkeypatch
    )
    for _ in range(3):
        pool._queue_actor_startup()
    failing_startups.add(next(iter(pool._ready_fut_to_actor)))
    pool._collect_ready_actors()

    crashed, oom, gpu_fault = _submit_tracked(pool, 3)
    task_errors[crashed] = ray.exceptions.ActorDiedError(None)
    task_errors[oom] = ray.exceptions.OutOfMemoryError("node low on memory")
    task_errors[gpu_fault] = FatalWorkerHardwareError("GPU 0 requires reset")
    for future in (crashed, oom, gpu_fault):
        with pytest.raises(ActorPoolTaskError):
            pool._resolve_future(future)
    assert len(pool._parked_actors) == 1

    # Replacements come up; one busy actor is then lost to a liveness scan.
    pool._collect_ready_actors()
    [lost] = _submit_tracked(pool, 1)
    pool._cleanup_lost_actor_future(
        lost,
        ActorStateSnapshot.from_ray_state(
            "actor-lost", _dead_actor_state("actor-lost")
        ),
    )
    pool._collect_ready_actors()

    owned = len(pool._idle_actors) + len(pool._parked_actors)
    assert owned == 4
    assert sum(delta for _, delta in metric_updates) == owned
    pool.shutdown()
    assert metric_updates[-1] == ("workers", -owned)
    assert sum(delta for _, delta in metric_updates) == 0


# ---------------------------------------------------------------------------
# Stall watchdog: the map loop must fail loud, not hang, when no
# result is ever produced -- whether because a dispatched task never returns
# or because no actor can be scheduled to run it.
# ---------------------------------------------------------------------------


@ray.remote
class HangActor:
    def hang(self, i: int) -> int:
        time.sleep(120)  # outlives the test's stall window; self-cleans after
        return i


def test_map_unordered_raises_when_pool_stalls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A never-arriving result trips the stall deadline instead of blocking."""
    monkeypatch.setattr(actor_pool_mod, "_MAP_STALL_TIMEOUT_S", 0.5)
    monkeypatch.setattr(actor_pool_mod, "_MAP_POLL_INTERVAL_S", 0.05)

    pool = object.__new__(ActorPool)
    pool._num_actors = 1
    pool.submit = lambda _fn, _v: None

    # ``_map`` first drains any leftover results (one ``has_next`` probe), then
    # enters the watchdog loop. Report "nothing to drain" once so the drain is
    # skipped, then "work pending" forever so the watchdog -- not the drain --
    # is what we exercise.
    drained = {"done": False}

    def _has_next() -> bool:
        if not drained["done"]:
            drained["done"] = True
            return False
        return True

    pool.has_next = _has_next

    def _never_ready(timeout: float | None = None) -> object:
        # Emulate a hung task / unschedulable actor: nothing ever completes.
        # PollTimeoutError is the pool's "no result yet" signal; a bare
        # TimeoutError would be a task failure and must NOT reset-and-continue.
        time.sleep(timeout or 0)
        raise actor_pool_mod.PollTimeoutError("not ready")

    pool.get_next_unordered = _never_ready

    start = time.monotonic()
    with pytest.raises(TimeoutError, match="ActorPool stalled"):
        list(pool.map_unordered(lambda _a, _v: None, [1]))
    # Fail loud promptly -- a few stall windows, nowhere near forever.
    assert time.monotonic() - start < 5.0


def test_get_next_unordered_times_out_when_nothing_schedulable() -> None:
    """A positive timeout is honored even when no future is ever inflight.

    This is the ``_map`` poll's contract for the never-ready-actor case: with
    submits pending but no actor schedulable, ``_future_to_actor`` stays empty,
    and the call must still raise within the timeout rather than spin forever.
    """
    pool = object.__new__(ActorPool)
    pool.has_next = lambda: True
    pool._collect_ready_actors = lambda: None
    pool._drained_buffer = []
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._last_actor_liveness_scan_at = None
    pool._future_to_actor = {}  # nothing inflight, ever
    pool._future_to_actor_id = {}
    pool._ready_fut_to_actor = {}  # no actor ever finishes startup

    start = time.monotonic()
    with pytest.raises(TimeoutError, match="Timed out waiting for result"):
        pool.get_next_unordered(timeout=0.2)
    assert time.monotonic() - start < 5.0


# ---------------------------------------------------------------------------
# Batch drain: drain_ready collects every ready result in a single pass so the
# driver refills the whole fleet per iteration instead of one actor at a time.
# ---------------------------------------------------------------------------


@pytest.mark.ray
def test_drain_ready_returns_all_ready_results_in_one_pass() -> None:
    """With N tasks finished, one drain_ready call returns all N results."""
    n = 8
    pool = ActorPool(TestActor.remote, n)
    ray.get(list(pool._ready_fut_to_actor), timeout=30.0)
    pool._collect_ready_actors()
    assert len(pool._idle_actors) == n

    for i in range(n):
        pool.submit(lambda actor, v: actor.echo.remote(v), i)
    # Block until every result is materialized before the single drain.
    ray.wait(list(pool._future_to_actor), num_returns=n, timeout=30.0)

    batch = pool.drain_ready(timeout=5.0)
    assert sorted(batch) == list(range(n))
    assert not pool.has_next()
    pool.shutdown()


def test_drain_ready_flushes_buffer_before_blocking_for_new_work() -> None:
    """A non-empty buffer is returned as-is, without blocking for more work."""
    pool = object.__new__(ActorPool)
    pool._drained_buffer = ["buffered-1", "buffered-2"]
    blocked: list[bool] = []
    pool.get_next_unordered = lambda timeout=None: blocked.append(True)

    out = pool.drain_ready(timeout=0.1)

    assert out == ["buffered-1", "buffered-2"]
    assert pool._drained_buffer == []
    assert blocked == []


def test_drain_ready_buffers_good_results_when_task_fails_mid_batch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A task failure mid-batch must not drop results drained before it.

    The good results are buffered and returned by the next call, after the
    caller has handled the ActorPoolTaskError; futures not yet resolved stay
    tracked for the next pass."""
    pool = object.__new__(ActorPool)
    pool._drained_buffer = []
    good_a, bad_b, good_c = object(), object(), object()
    pool._future_to_actor = {good_a: (0, "a"), bad_b: (1, "b"), good_c: (2, "c")}
    pool.get_next_unordered = lambda timeout=None: "first"
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.ray.wait",
        lambda futures, **_kwargs: (list(futures), []),
    )

    err = ActorPoolTaskError(task="task-b", cause=RuntimeError("boom"))

    def _resolve(future: object) -> object:
        if future is bad_b:
            raise err
        return {good_a: "res-a", good_c: "res-c"}[future]

    pool._resolve_future = _resolve

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool.drain_ready(timeout=0.1)
    assert exc_info.value is err
    assert pool._drained_buffer == ["first", "res-a"]

    # Next call returns the buffered results before draining anything new.
    assert pool.drain_ready(timeout=0.1) == ["first", "res-a"]
    assert pool._drained_buffer == []


def test_drain_ready_buffers_good_results_on_ordinary_task_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An ordinary task exception (not ActorPoolTaskError) raised by ray.get
    mid-batch must also preserve results already drained this pass; they were
    removed from pool state and would otherwise be lost."""
    pool = object.__new__(ActorPool)
    pool._drained_buffer = []
    good_a, bad_b = object(), object()
    pool._future_to_actor = {good_a: (0, "a"), bad_b: (1, "b")}
    pool.get_next_unordered = lambda timeout=None: "first"
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.ray.wait",
        lambda futures, **_kwargs: (list(futures), []),
    )

    def _resolve(future: object) -> object:
        if future is bad_b:
            raise TimeoutError("embedding API timed out")
        return "res-a"

    pool._resolve_future = _resolve

    with pytest.raises(TimeoutError, match="embedding API timed out"):
        pool.drain_ready(timeout=0.1)
    assert pool._drained_buffer == ["first", "res-a"]


def test_get_next_unordered_serves_buffered_results() -> None:
    """get_next_unordered drains drain_ready's buffer one result at a time, so
    the two drain APIs stay consistent with has_next()."""
    pool = object.__new__(ActorPool)
    pool._future_to_actor = {}
    pool._pending_submits = []
    pool._drained_buffer = ["r1", "r2"]

    assert pool.get_next_unordered(timeout=0.1) == "r1"
    assert pool._drained_buffer == ["r2"]
    assert pool.get_next_unordered(timeout=0.1) == "r2"
    assert pool._drained_buffer == []


def test_has_next_true_while_results_buffered() -> None:
    """Buffered results keep has_next True even with nothing else inflight, so
    the driver loop drains them instead of exiting and dropping the results."""
    pool = object.__new__(ActorPool)
    pool._future_to_actor = {}
    pool._pending_submits = []
    pool._drained_buffer = ["stranded-result"]
    assert pool.has_next() is True

    pool._drained_buffer = []
    assert pool.has_next() is False


def test_drain_ready_times_out_when_nothing_schedulable() -> None:
    """drain_ready inherits get_next_unordered's positive-timeout contract."""
    pool = object.__new__(ActorPool)
    pool._drained_buffer = []
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    pool._last_actor_liveness_scan_at = None
    pool.has_next = lambda: True
    pool._collect_ready_actors = lambda: None
    pool._future_to_actor = {}
    pool._future_to_actor_id = {}
    pool._ready_fut_to_actor = {}

    start = time.monotonic()
    with pytest.raises(TimeoutError, match="Timed out waiting for result"):
        pool.drain_ready(timeout=0.2)
    assert time.monotonic() - start < 5.0


@pytest.mark.ray
def test_map_unordered_fails_loud_on_hung_task(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end: a schedulable actor whose task never returns surfaces a
    TimeoutError within the stall window instead of hanging the driver."""
    monkeypatch.setattr(actor_pool_mod, "_MAP_STALL_TIMEOUT_S", 2.0)
    monkeypatch.setattr(actor_pool_mod, "_MAP_POLL_INTERVAL_S", 0.2)

    pool = ActorPool(HangActor.remote, 1)
    ray.get(list(pool._ready_fut_to_actor), timeout=30.0)
    pool._collect_ready_actors()
    assert len(pool._idle_actors) == 1

    start = time.monotonic()
    with pytest.raises(TimeoutError, match="ActorPool stalled"):
        list(pool.map_unordered(lambda actor, i: actor.hang.remote(i), [1]))
    assert time.monotonic() - start < 30.0

    # The stalled task remains inflight after the map watchdog fires. Shutdown
    # must terminate its busy actor, not leave the native Ray worker alive until
    # interpreter teardown.
    assert len(pool._future_to_actor) == 1
    outstanding_future = next(iter(pool._future_to_actor))
    pool.shutdown()
    with pytest.raises(ray.exceptions.RayActorError):
        ray.get(outstanding_future, timeout=30.0)

    assert pool._idle_actors == []
    assert pool._ready_fut_to_actor == {}
    assert pool._future_to_actor == {}
    assert pool._index_to_future == {}
    assert pool._pending_submits == []
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}


@ray.remote
class ApiTimeoutActor:
    def call(self, i: int) -> int:
        # Emulates a UDF whose dependency (e.g. an embedding API) times out.
        raise TimeoutError("embedding API timed out")


@pytest.mark.ray
def test_map_unordered_surfaces_task_raised_timeout_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A TimeoutError raised INSIDE a task is a task failure, not a stall.

    Ray re-raises task exceptions as ``RayTaskError`` subclassing the task's
    own type, so a task-raised TimeoutError is a ``TimeoutError`` instance.
    It must propagate immediately with the task's message -- not be swallowed
    as a poll timeout and later mislabeled by the stall watchdog."""
    # Stall window far larger than the test budget: if the error were
    # misclassified as a stall, this test would time out, not pass.
    monkeypatch.setattr(actor_pool_mod, "_MAP_STALL_TIMEOUT_S", 300.0)

    pool = ActorPool(ApiTimeoutActor.remote, 1)
    with pytest.raises(TimeoutError, match="embedding API timed out"):
        list(pool.map_unordered(lambda actor, i: actor.call.remote(i), [1]))
    pool.shutdown()


# ---------------------------------------------------------------------------
# Telemetry flush ordering: the final flush broadcast reaches only actors still
# in the idle list. shutdown() drains that list before it ray.kills the actors,
# so a broadcast issued AFTER shutdown reaches nobody and the workers' buffered
# spans are lost (atexit does not run under ray.kill). This is why the UDTF
# refresh teardown must broadcast the flush BEFORE calling shutdown().
# ---------------------------------------------------------------------------


def test_broadcast_flushes_only_actors_still_idle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """broadcast() flushes every idle actor, but reaches nothing once the idle
    list is drained -- exactly what shutdown() does before ray.kill. Hence the
    UDTF teardown must broadcast before it shuts the pool down; the reverse
    silently drops the workers' buffered spans."""
    monkeypatch.setattr("geneva.runners.ray.actor_pool.ray.get", lambda *a, **k: None)

    class _FakeActor:
        def __init__(self) -> None:
            self.flushes = 0

        @property
        def flush_telemetry(self) -> SimpleNamespace:
            # Mirror a Ray ActorHandle's ``.method.remote()`` call shape.
            return SimpleNamespace(remote=self._flush)

        def _flush(self) -> None:
            self.flushes += 1

    actors = [_FakeActor(), _FakeActor()]
    pool = object.__new__(ActorPool)
    pool._idle_actors = list(actors)

    # Actors still idle (pre-shutdown): the broadcast reaches every one.
    pool.broadcast("flush_telemetry")
    assert [a.flushes for a in actors] == [1, 1]

    # shutdown() drains _idle_actors before killing the actors; a broadcast
    # issued afterward iterates an empty list and reaches nobody.
    pool._idle_actors = []
    pool.broadcast("flush_telemetry")
    assert [a.flushes for a in actors] == [1, 1]  # unchanged -> flush was lost


def test_udtf_processor_actor_exposes_flush_telemetry() -> None:
    """The UDTF pool broadcasts ``flush_telemetry`` before shutdown; the actor
    must define that method or the flush is a silent no-op (broadcast suppresses
    the AttributeError). Guards buffered-span loss on short UDTF refreshes."""
    from geneva.table import _make_udtf_processor_actor

    actor_cls = _make_udtf_processor_actor()
    assert "flush_telemetry" in actor_cls.__ray_metadata__.method_meta.methods


# ---------------------------------------------------------------------------
# Releasing actors with no work left (GEN-1018). A long-tail backfill releases
# idle appliers so their resources free before the job ends; late replacement
# work restarts actors, never past the pool's original size.
# ---------------------------------------------------------------------------


class _ReleasableActor:
    """Ray-handle double that records ``flush_telemetry`` calls in ``events``."""

    def __init__(self, name: str, events: list[tuple[str, str]]) -> None:
        self.name = name
        self._events = events
        self.__ray_ready__ = SimpleNamespace(remote=lambda: f"ready-{name}")

    @property
    def flush_telemetry(self) -> SimpleNamespace:
        return SimpleNamespace(remote=lambda: self._events.append(("flush", self.name)))


class _FakeClock:
    """Monotonic clock double; tests advance ``now`` by hand."""

    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def _releasable_pool(
    monkeypatch: pytest.MonkeyPatch,
    *,
    num_actors: int = 4,
    clock: _FakeClock | None = None,
) -> tuple[ActorPool, list[tuple[str, str]], list[tuple[str, int]]]:
    """An empty pool double whose cleanup calls and kills land in ``events``.

    Actors started by the pool (late work into released slots) are named
    ``new-<n>``, so a test can tell a restart from a reused actor.
    """
    events: list[tuple[str, str]] = []
    metric_updates: list[tuple[str, int]] = []
    started: list[_ReleasableActor] = []

    def _factory() -> _ReleasableActor:
        actor = _ReleasableActor(f"new-{len(started)}", events)
        started.append(actor)
        return actor

    pool = object.__new__(ActorPool)
    pool._actor_factory = _factory
    pool._num_actors = num_actors
    pool._clock = clock or _FakeClock()
    pool._idle_actors = []
    pool._idle_since = {}
    pool._ready_fut_to_actor = {}
    pool._future_to_actor = {}
    pool._index_to_future = {}
    pool._future_to_task = {}
    pool._future_to_actor_id = {}
    pool._pending_submits = []
    pool._parked_actors = []
    pool._drained_buffer = []
    pool._next_task_index = 0
    pool._released_slots = 0
    pool.worker_metric = "workers"
    pool.job_tracker = SimpleNamespace(
        increment=SimpleNamespace(
            remote=lambda metric, delta: metric_updates.append((metric, delta))
        )
    )
    monkeypatch.setattr(ray, "kill", lambda actor: events.append(("kill", actor.name)))
    monkeypatch.setattr(ray, "get", lambda *_args, **_kwargs: None)
    return pool, events, metric_updates


def test_release_idle_actors_cleans_up_then_kills_actors_without_work(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Idle and starting actors go; busy and parked actors stay. Cleanup runs on
    every idle actor before any kill, because ray.kill skips exit hooks."""
    pool, events, metrics = _releasable_pool(monkeypatch)
    busy = _ReleasableActor("busy", events)
    parked = _ReleasableActor("parked", events)
    busy_future = object()
    pool._idle_actors = [
        _ReleasableActor("idle-0", events),
        _ReleasableActor("idle-1", events),
    ]
    pool._ready_fut_to_actor = {object(): _ReleasableActor("starting", events)}
    pool._future_to_actor = {busy_future: (0, busy)}
    pool._future_to_actor_id = {busy_future: "busy-id"}
    pool._parked_actors = [parked]

    assert pool.release_idle_actors(cleanup_method="flush_telemetry") == 3

    assert events == [
        ("flush", "idle-0"),
        ("flush", "idle-1"),
        ("kill", "idle-0"),
        ("kill", "idle-1"),
        ("kill", "starting"),
    ]
    assert pool._idle_actors == []
    assert pool._ready_fut_to_actor == {}
    assert pool._future_to_actor == {busy_future: (0, busy)}
    assert pool._parked_actors == [parked]
    assert pool._released_slots == 3
    assert metrics == [("workers", -3)]


_TrackerCall = tuple[str, tuple[object, ...]]


class _RecordingTracker:
    """Job-tracker handle double that records every ``.remote`` call in order.

    The pool sends these without waiting. The real tracker usually applies
    one caller's calls in the order recorded here, but Ray does not guarantee
    that for async actors.
    """

    def __init__(self) -> None:
        self.calls: list[_TrackerCall] = []

    def __getattr__(self, method: str) -> SimpleNamespace:
        def remote(*args: object) -> _TrackerCall:
            call = (method, args)
            self.calls.append(call)
            return call

        return SimpleNamespace(remote=remote)


def _start_pools_without_ray(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(actor_pool_mod, "_current_job_id_hex", lambda: None)
    monkeypatch.setattr(actor_pool_mod, "_current_gcs_address", lambda: None)
    monkeypatch.setattr(ray, "kill", lambda _actor: None)


async def _replay_workers(
    ledger: _JobTracker, calls: Iterable[_TrackerCall]
) -> list[int]:
    """Apply tracker calls to an in-process ledger; the workers count after each."""
    counts = []
    for method, args in calls:
        await getattr(ledger, method)(*args)
        counts.append(ledger.metrics.get("workers", {}).get("n", 0))
    return counts


class _RestoredTracker(_JobTracker):
    """In-process tracker whose hydration restores a saved workers count of 5
    and 40 checkpointed rows, as a tracker for a recovered job does. Saves are
    no-ops."""

    async def _load_persisted_state(self) -> tuple[dict[str, dict], None]:
        workers = {"n": 5, "total": 3, "done": True, "desc": "Workers started"}
        rows = {"n": 40, "total": 100, "done": False, "desc": "Rows checkpointed"}
        return {"workers": workers, "rows_checkpointed": rows}, None

    async def _save_with_throttle(self, force: bool = False) -> None:
        return None


def _fresh_ledger(*, restored: bool) -> _JobTracker:
    if restored:
        return _RestoredTracker(job_id="job", table_ref=cast("Any", object()))
    return _JobTracker(job_id="job", table_ref=None, enable_saves=False)


async def test_worker_count_is_exact_in_any_tracker_execution_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Each actor the pool starts (at init or for late work) and each one it
    kills (release or shutdown) moves the workers count by one, so on a fresh
    tracker the count ends at zero whatever order the calls are applied in."""
    _start_pools_without_ray(monkeypatch)
    events: list[tuple[str, str]] = []
    ids = itertools.count()
    tracker = _RecordingTracker()

    pool = ActorPool(
        lambda: _ReleasableActor(f"actor-{next(ids)}", events),
        3,
        job_tracker=tracker,
    )
    assert pool.release_idle_actors() == 3
    pool.submit(lambda _a, _v: None, "late-task")
    pool.shutdown()
    assert next(ids) == 4  # 3 initial actors + 1 restarted for the late task

    for order in set(itertools.permutations(tracker.calls)):
        ledger = _fresh_ledger(restored=False)
        counts = await _replay_workers(ledger, order)
        assert counts[-1] == 0, order


@pytest.mark.parametrize(
    ("restored", "startup"), [(False, [0, 1, 2, 3]), (True, [5, 1, 2, 3])]
)
async def test_pool_counts_workers_from_zero_after_a_restore(
    monkeypatch: pytest.MonkeyPatch, restored: bool, startup: list[int]
) -> None:
    """A recovered job's tracker restores the workers count of the run that
    crashed (5). The pool's first increment drops it, so a pool of 3 reads
    1, 2, 3 and ends at 0, as a job that never crashed does. The pool only
    calls tracker methods that Geneva 0.18.0 workers have."""
    _start_pools_without_ray(monkeypatch)
    ids = itertools.count()
    tracker = _RecordingTracker()

    pool = ActorPool(
        lambda: _ReleasableActor(f"actor-{next(ids)}", []),
        3,
        job_tracker=tracker,
    )
    assert pool.release_idle_actors() == 3
    pool.submit(lambda _a, _v: None, "late-task")
    pool.shutdown()
    assert {method for method, _ in tracker.calls} == {"set_total", "increment"}

    counts = await _replay_workers(_fresh_ledger(restored=restored), tracker.calls)
    assert counts[:4] == startup
    assert counts[-1] == 0
    assert min(counts) >= 0


@pytest.mark.parametrize("restored", [False, True], ids=["fresh", "restored"])
async def test_two_pools_on_one_tracker_keep_the_count_exact(
    monkeypatch: pytest.MonkeyPatch, restored: bool
) -> None:
    """Two pools share a tracker, with their updates landing in any
    interleaving. Whichever pool adds first marks the count live, so the
    other pool's adds reset nothing and the count ends at exactly 0."""
    _start_pools_without_ray(monkeypatch)
    tracker = _RecordingTracker()
    ids = itertools.count()

    def _factory() -> _ReleasableActor:
        return _ReleasableActor(f"actor-{next(ids)}", [])

    ActorPool(_factory, 2, job_tracker=tracker).shutdown()
    first = list(tracker.calls)
    ActorPool(_factory, 1, job_tracker=tracker).shutdown()
    second = tracker.calls[len(first) :]

    total = len(first) + len(second)
    for slots in itertools.combinations(range(total), len(first)):
        first_iter, second_iter = iter(first), iter(second)
        order = [
            next(first_iter) if i in slots else next(second_iter) for i in range(total)
        ]
        counts = await _replay_workers(_fresh_ledger(restored=restored), order)
        assert counts[-1] == 0, order
        assert min(counts) >= 0, order
        first_add = order.index(("increment", ("workers", 1)))
        assert max(counts[first_add:]) <= 3, order


@pytest.mark.parametrize("path", ["increment", "batch_increment"])
async def test_tracker_drops_only_a_restored_worker_count(
    path: str, caplog: pytest.LogCaptureFixture
) -> None:
    """The first add to a restored workers count drops it, once, with an info
    log; a restored progress count keeps its value."""
    ledger = _fresh_ledger(restored=True)

    async def add(name: str, delta: int) -> None:
        if path == "increment":
            await ledger.increment(name, delta)
        else:
            await ledger.batch_increment({name: delta})

    with caplog.at_level(logging.INFO, logger=jobtracker_mod.__name__):
        await add("workers", 1)
        await add("workers", 1)
        await add("rows_checkpointed", 10)

    assert ledger.metrics["workers"]["n"] == 2
    assert ledger.metrics["workers"]["done"] is False
    assert ledger.metrics["rows_checkpointed"]["n"] == 50
    drops = [r for r in caplog.records if "stale restored count" in r.message]
    assert [r.getMessage() for r in drops] == [
        "Discarding stale restored count of workers: 5"
    ]


@pytest.mark.parametrize(
    ("first_call", "expected"),
    [
        # A 0.18.0 client starts each pool with set(workers, 0).
        (("set", ("workers", 0)), [0, 1, 2]),
        # The tracker restarted under a live pool, whose next update is a
        # release; the restored count is real, so it is kept.
        (("increment", ("workers", -1)), [4, 5, 6]),
    ],
    ids=["old-client-set-zero", "live-pool-decrement"],
)
async def test_tracker_keeps_a_restored_worker_count_after_other_updates(
    first_call: _TrackerCall, expected: list[int]
) -> None:
    calls = [first_call, ("increment", ("workers", 1)), ("increment", ("workers", 1))]
    assert await _replay_workers(_fresh_ledger(restored=True), calls) == expected


def test_pool_start_does_not_wait_on_the_tracker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A slow or failing tracker never blocks the pool from starting: the
    pool sends its updates and never waits on them."""
    _start_pools_without_ray(monkeypatch)
    waits: list[tuple[object, ...]] = []

    def _timeout(*args: object, **_kwargs: object) -> None:
        waits.append(args)
        raise ray.exceptions.GetTimeoutError("tracker busy")

    monkeypatch.setattr(ray, "get", _timeout)
    ids = itertools.count()
    tracker = _RecordingTracker()
    pool = ActorPool(
        lambda: _ReleasableActor(f"actor-{next(ids)}", []), 2, job_tracker=tracker
    )

    assert waits == []
    assert len(pool._ready_fut_to_actor) == 2
    pool.shutdown()


def test_release_idle_actors_keeps_actors_while_work_is_queued(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool, events, metrics = _releasable_pool(monkeypatch)
    pool._ready_fut_to_actor = {object(): _ReleasableActor("starting", events)}
    pool._pending_submits = [(object(), "queued-task")]

    assert pool.release_idle_actors(cleanup_method="flush_telemetry") == 0
    assert len(pool._ready_fut_to_actor) == 1

    pool._pending_submits = []
    pool._ready_fut_to_actor = {}
    assert pool.release_idle_actors(cleanup_method="flush_telemetry") == 0
    assert events == []
    assert metrics == []
    assert pool._released_slots == 0


def test_submit_restarts_released_actors_up_to_original_size(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Late work starts one actor per queued task, until the released slots are
    refilled: busy plus starting actors never exceed the original pool size."""
    pool, events, metrics = _releasable_pool(monkeypatch, num_actors=4)
    pool._future_to_actor = {object(): (0, _ReleasableActor("busy", events))}
    pool._idle_actors = [_ReleasableActor(f"idle-{i}", events) for i in range(3)]
    assert pool.release_idle_actors() == 3
    metrics.clear()

    for i in range(6):
        pool.submit(lambda _a, _v: pytest.fail("no idle actor to run on"), i)

    assert len(pool._pending_submits) == 6
    assert len(pool._ready_fut_to_actor) == 3
    assert pool._released_slots == 0
    assert metrics == [("workers", 1)] * 3


def test_submit_counts_starting_actors_before_restarting(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed task's replacement actor is already starting; only queued work
    beyond the starting actors restarts released slots."""
    pool, events, _metrics = _releasable_pool(monkeypatch)
    pool._released_slots = 3
    pool._ready_fut_to_actor = {object(): _ReleasableActor("replacement", events)}

    pool.submit(lambda _a, _v: None, "first")
    assert len(pool._ready_fut_to_actor) == 1
    assert pool._released_slots == 3

    pool.submit(lambda _a, _v: None, "second")
    assert len(pool._ready_fut_to_actor) == 2
    assert pool._released_slots == 2


def test_submit_never_starts_actors_when_none_were_released(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With release off the pool keeps its fixed size: queued work just waits."""
    pool, events, metrics = _releasable_pool(monkeypatch)
    pool._future_to_actor = {object(): (0, _ReleasableActor("busy", events))}

    pool.submit(lambda _a, _v: None, "queued")

    assert pool._pending_submits != []
    assert pool._ready_fut_to_actor == {}
    assert metrics == []


# Idle grace: an idle actor is released only once it has been idle for
# ``idle_grace_s``, so late work that arrives sooner runs on a warm actor.


def _idle_at(
    pool: ActorPool, clock: _FakeClock, at: float, *actors: _ReleasableActor
) -> None:
    """Hand ``actors`` back to the pool as idle at time ``at``."""
    clock.now = at
    for actor in actors:
        pool._return_actor(actor)


def test_release_keeps_actors_idle_for_less_than_the_grace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    idle = _ReleasableActor("idle", events)
    _idle_at(pool, clock, 0.0, idle)

    clock.now = 59.9
    released = pool.release_idle_actors(
        idle_grace_s=60, cleanup_method="flush_telemetry"
    )

    assert released == 0
    assert pool._idle_actors == [idle]
    assert events == []
    assert metrics == []
    assert pool._released_slots == 0


def test_release_frees_actors_once_idle_for_the_grace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Actors idle for the whole grace are flushed, then killed. One that went
    idle later stays until its own grace ends."""
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    early = [_ReleasableActor(f"early-{i}", events) for i in range(2)]
    late = _ReleasableActor("late", events)
    _idle_at(pool, clock, 0.0, *early)
    _idle_at(pool, clock, 40.0, late)

    clock.now = 60.0
    released = pool.release_idle_actors(
        idle_grace_s=60, cleanup_method="flush_telemetry"
    )

    assert released == 2
    assert events == [
        ("flush", "early-0"),
        ("flush", "early-1"),
        ("kill", "early-0"),
        ("kill", "early-1"),
    ]
    assert pool._idle_actors == [late]
    assert metrics == [("workers", -2)]
    assert pool._released_slots == 2

    clock.now = 100.0
    assert pool.release_idle_actors(idle_grace_s=60) == 1
    assert pool._idle_actors == []
    assert pool._idle_since == {}
    assert metrics == [("workers", -2), ("workers", -1)]


def test_work_within_the_grace_reuses_an_idle_actor_without_a_restart(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Late work (a retry, an OOM split) arriving within the grace runs on the
    idle actor: nothing is released or restarted. The actor's idle time
    starts over when it finishes that work."""
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    warm = _ReleasableActor("warm", events)
    _idle_at(pool, clock, 0.0, warm)
    clock.now = 10.0
    assert pool.release_idle_actors(idle_grace_s=60) == 0

    ran_on: list[_ReleasableActor] = []

    def _run(actor: _ReleasableActor, _task: str) -> object:
        ran_on.append(actor)
        return object()

    clock.now = 50.0
    pool.submit(_run, "retry")

    assert ran_on == [warm]
    assert pool._pending_submits == []
    assert pool._ready_fut_to_actor == {}
    assert pool._released_slots == 0
    assert pool._idle_since == {}
    assert events == []
    assert metrics == []

    (future,) = pool._future_to_actor
    pool._pop_future_state(future)
    _idle_at(pool, clock, 70.0, warm)
    clock.now = 129.0
    assert pool.release_idle_actors(idle_grace_s=60) == 0
    clock.now = 130.0
    assert pool.release_idle_actors(idle_grace_s=60) == 1
    assert events == [("kill", "warm")]


def test_release_frees_starting_actors_without_waiting_for_the_grace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An actor still starting holds no warm state: once no work is left it goes
    at once, while an idle actor within the grace stays."""
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    idle = _ReleasableActor("idle", events)
    _idle_at(pool, clock, 0.0, idle)
    pool._ready_fut_to_actor = {object(): _ReleasableActor("starting", events)}

    released = pool.release_idle_actors(
        idle_grace_s=60, cleanup_method="flush_telemetry"
    )

    assert released == 1
    assert events == [("kill", "starting")]
    assert pool._idle_actors == [idle]
    assert pool._ready_fut_to_actor == {}
    assert pool._released_slots == 1
    assert metrics == [("workers", -1)]


def test_zero_grace_releases_an_actor_as_soon_as_it_goes_idle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    _idle_at(pool, clock, 5.0, _ReleasableActor("idle", events))

    released = pool.release_idle_actors(
        idle_grace_s=0, cleanup_method="flush_telemetry"
    )

    assert released == 1
    assert events == [("flush", "idle"), ("kill", "idle")]
    assert metrics == [("workers", -1)]


@pytest.mark.parametrize("idle_grace_s", [0.0, 60.0])
def test_release_keeps_every_actor_while_work_is_queued(
    monkeypatch: pytest.MonkeyPatch, idle_grace_s: float
) -> None:
    clock = _FakeClock()
    pool, events, metrics = _releasable_pool(monkeypatch, clock=clock)
    _idle_at(pool, clock, 0.0, _ReleasableActor("idle", events))
    pool._ready_fut_to_actor = {object(): _ReleasableActor("starting", events)}
    pool._pending_submits = [(object(), "queued-task")]
    clock.now = 600.0

    assert pool.release_idle_actors(idle_grace_s=idle_grace_s) == 0
    assert len(pool._idle_actors) == 1
    assert len(pool._ready_fut_to_actor) == 1
    assert events == []
    assert metrics == []


def test_pool_times_idle_actors_on_the_injected_clock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _start_pools_without_ray(monkeypatch)
    tracker = _RecordingTracker()
    clock = _FakeClock()
    clock.now = 42.0
    pool = ActorPool(
        lambda: _ReleasableActor("new", []), 1, job_tracker=tracker, clock=clock
    )
    idle = _ReleasableActor("idle", [])

    pool._return_actor(idle)

    assert pool._idle_since == {ActorPool._actor_key(idle): 42.0}
    pool.shutdown()


def test_liveness_scan_ignores_actor_released_after_scan_started(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A scan snapshotted while an actor was busy can report it DEAD after it
    finished its task and was released. A released actor is not lost: no
    task error, no resubmit."""
    pool, events, _metrics = _releasable_pool(monkeypatch)
    actor = _ReleasableActor("finished", events)
    future = object()
    pool._future_to_actor = {future: (0, actor)}
    pool._index_to_future = {0: future}
    pool._future_to_task = {future: (lambda _a, _t: None, "task")}
    pool._future_to_actor_id = {future: "actor-finished"}
    pool.resubmit_on_actor_failure = False
    pool._last_actor_liveness_scan_at = None
    pool._liveness_scan_future = None
    pool._liveness_scan_cancelled = threading.Event()
    scanned: list[set[str]] = []
    scan_future: Future = Future()

    class _DeferredExecutor:
        def submit(self, _fn: object, actor_ids: set[str]) -> Future:
            scanned.append(set(actor_ids))
            return scan_future

    pool._liveness_scan_executor = _DeferredExecutor()
    pool._maybe_start_liveness_scan()
    assert scanned == [{"actor-finished"}]

    monkeypatch.setattr(ray, "get", lambda *_args, **_kwargs: "result")
    assert pool._resolve_future(future) == "result"
    assert pool.release_idle_actors(cleanup_method="flush_telemetry") == 1

    scan_future.set_result(
        {
            "actor-finished": ActorStateSnapshot.from_ray_state(
                "actor-finished", _dead_actor_state("actor-finished")
            )
        }
    )
    pool._cleanup_lost_actor_future = lambda *_a: pytest.fail(
        "a released actor is not a lost actor"
    )
    assert pool._consume_liveness_scan() is pool.NoResult
    assert pool._pending_submits == []


def test_applier_actor_exposes_flush_telemetry() -> None:
    """Releasing an idle applier calls ``flush_telemetry`` before ``ray.kill``;
    the actor must define it or the flush is a silent no-op."""
    from geneva.runners.ray.pipeline import ApplierActor

    assert "flush_telemetry" in ApplierActor.__ray_metadata__.method_meta.methods
