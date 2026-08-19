# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
import random
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from types import SimpleNamespace

import pytest
import ray
from google.protobuf.json_format import MessageToDict
from ray.core.generated import common_pb2

from geneva.runners.ray import actor_pool as actor_pool_mod
from geneva.runners.ray.actor_pool import (
    ActorLostError,
    ActorPool,
    ActorPoolTaskError,
    ActorStateSnapshot,
)


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

    assert killed == [idle_actor, shared_actor, busy_actor, starting_actor]
    assert metric_updates == [("test-workers", -4)]
    assert pool._idle_actors == []
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
    # Second poll consumes the finished scan and resubmits the lost task.
    assert pool._pop_dead_actor_task() is pool.NoResult
    assert pool._future_to_actor == {}
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._index_to_future == {}
    assert queued_replacements == [True]
    assert resubmitted == [task]


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

    def raise_actor_died(_future: object) -> None:
        raise actor_died

    monkeypatch.setattr(ray, "wait", lambda futures, **_kwargs: ([future], []))
    monkeypatch.setattr(ray, "get", raise_actor_died)
    monkeypatch.setattr(ray, "kill", lambda _actor: None)
    monkeypatch.setattr(ActorPool, "_actor_state_by_id", lambda _self, _id: None)

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool._get_next_by_fut([future])

    assert exc_info.value.cause is actor_died


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
