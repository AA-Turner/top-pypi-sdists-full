# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import itertools
import random
from types import SimpleNamespace

import pytest
import ray
from google.protobuf.json_format import MessageToDict
from ray.core.generated import common_pb2

from geneva.runners.ray.actor_pool import (
    ActorLostError,
    ActorPool,
    ActorPoolTaskError,
)


def _dead_actor_state(
    actor_id: str,
    *,
    death_reason: str = "WORKER_DIED",
    node_death_info: bool = False,
) -> SimpleNamespace:
    death_cause = common_pb2.ActorDeathCause()
    actor_context = death_cause.actor_died_error_context
    actor_context.reason = getattr(common_pb2.ActorDiedErrorContext, death_reason)
    if node_death_info:
        actor_context.node_death_info.reason = (
            common_pb2.NodeDeathInfo.AUTOSCALER_DRAIN_PREEMPTED
        )
    return SimpleNamespace(
        actor_id=actor_id,
        state="DEAD",
        death_cause=MessageToDict(death_cause),
        node_id="node-1",
        num_restarts_due_to_node_preemption=1 if "PREEMPT" in death_reason else 0,
    )


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


@pytest.mark.slow
def test_actor_pool_detects_dead_busy_actor_before_future_ready(
    monkeypatch: pytest.MonkeyPatch,
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
    pool._future_to_task = {future: (lambda _actor, _task: None, task)}
    pool._future_to_actor_id = {future: "actor-dead"}
    pool.resubmit_on_actor_failure = False
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool._get_next_by_fut = lambda _futs, _timeout=None: (_ for _ in ()).throw(
        TimeoutError("not ready")
    )

    def list_dead_actor(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        assert filters[0][2] == "actor-dead"
        return [_dead_actor_state("actor-dead")]

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_dead_actor,
    )

    with pytest.raises(ActorPoolTaskError) as exc_info:
        pool.get_next_unordered(timeout=0.01)

    assert exc_info.value.task == task
    assert isinstance(exc_info.value.cause, ActorLostError)
    assert "actor-dead" in str(exc_info.value.cause)
    assert exc_info.value.cause.snapshot.death_reason == "WORKER_DIED"
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
    pool._last_actor_liveness_scan_at = None
    pool.resubmit_on_actor_failure = True
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = submit

    def list_dead_actor(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        actor_id = filters[0][2]
        return [
            _dead_actor_state(
                actor_id,
                death_reason="NODE_DIED",
                node_death_info=True,
            )
        ]

    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_dead_actor,
    )

    assert pool._pop_dead_actor_task() is pool.NoResult
    assert pool._future_to_actor == {}
    assert pool._future_to_task == {}
    assert pool._future_to_actor_id == {}
    assert pool._index_to_future == {}
    assert queued_replacements == [True]
    assert resubmitted == [task]


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
    pool._last_actor_liveness_scan_at = None
    pool.resubmit_on_actor_failure = True
    pool._queue_actor_startup = lambda: queued_replacements.append(True)
    pool.submit = lambda _fn, submitted_task: resubmitted.append(submitted_task)

    def list_dead_actor(**kwargs: object) -> list[SimpleNamespace]:
        filters = kwargs["filters"]
        assert isinstance(filters, list)
        actor_id = filters[0][2]
        return [_dead_actor_state(actor_id, death_reason="WORKER_DIED")]

    monkeypatch.setattr("geneva.runners.ray.actor_pool.ray.kill", lambda _actor: None)
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.list_actors",
        list_dead_actor,
    )

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
