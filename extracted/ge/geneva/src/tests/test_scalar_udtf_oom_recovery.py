# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections import Counter, deque
from collections.abc import Callable
from typing import Any

import pytest

import geneva.runners.ray.pipeline as pipeline_module
from geneva.errors import FatalWorkerExitError, FatalWorkerOOMError
from geneva.runners.ray.actor_pool import (
    ActorLostError,
    ActorPoolTaskError,
    ActorStateSnapshot,
)
from geneva.runners.ray.kuberay import PodStatus
from geneva.runners.ray.oom_recovery_budget import (
    OOMRecoveryBudgetConfig,
    OOMRecoveryBudgetTracker,
)
from geneva.runners.ray.pipeline import (
    _iter_scalar_udtf_results,
    _ScalarUDTFWorkState,
)


class _FakePool:
    def __init__(
        self,
        run: Callable[[list[int], int], Any],
    ) -> None:
        self._run = run
        self._pending: deque[tuple[Callable, list[int]]] = deque()
        self.attempts: Counter[tuple[int, ...]] = Counter()
        self.submitted: list[list[int]] = []

    def submit(self, fn: Callable, row_ids: list[int]) -> None:
        self.submitted.append(row_ids)
        self._pending.append((fn, row_ids))

    def has_next(self) -> bool:
        return bool(self._pending)

    def get_next_unordered(self, timeout: float | None = None) -> Any:
        del timeout
        _fn, row_ids = self._pending.popleft()
        key = tuple(row_ids)
        self.attempts[key] += 1
        return self._run(row_ids, self.attempts[key])


class _BrokenJobTracker:
    class _Remote:
        @staticmethod
        def remote(*_args: object, **_kwargs: object) -> None:
            raise RuntimeError("tracker unavailable")

    set_total = _Remote()
    increment = _Remote()


def _tracker(*, max_same_range: int = 3) -> OOMRecoveryBudgetTracker:
    return OOMRecoveryBudgetTracker(
        config=OOMRecoveryBudgetConfig(
            enabled=True,
            max_total_oom_recoveries=10,
            max_same_range_oom_recoveries=max_same_range,
        )
    )


def test_scalar_udtf_oom_splits_only_failed_work_and_reuses_success_once() -> None:
    """A sibling result is yielded once while only the OOM item is bisected."""

    def run(row_ids: list[int], attempt: int) -> tuple[int, ...]:
        if row_ids == [0, 1, 2, 3] and attempt == 1:
            raise ActorPoolTaskError(
                task=row_ids,
                cause=FatalWorkerOOMError("worker OOMKilled"),
            )
        return tuple(row_ids)

    pool = _FakePool(run)
    state = _ScalarUDTFWorkState(total_work_items=2)

    results = list(
        _iter_scalar_udtf_results(
            pool,  # type: ignore[arg-type]
            lambda _actor, row_ids: row_ids,
            [[0, 1, 2, 3], [4, 5]],
            prefetch=2,
            oom_budget_tracker=_tracker(),
            job_tracker=_BrokenJobTracker(),  # type: ignore[arg-type]
            job_id="scalar-oom-test",
            state=state,
        )
    )

    flattened = [row_id for result in results for row_id in result]
    assert sorted(flattened) == list(range(6))
    assert len(flattened) == len(set(flattened))
    assert pool.attempts[(4, 5)] == 1
    assert pool.submitted == [[0, 1, 2, 3], [4, 5], [0, 1], [2, 3]]
    assert state.total_work_items == 3
    assert state.completed_work_items == 3
    assert state.oom_recoveries == 1


def test_scalar_udtf_pod_oom_evidence_splits_generic_worker_loss() -> None:
    """Kubelet-only OOM evidence routes an untagged worker death to shrinking."""

    def lose_worker_once(row_ids: list[int], attempt: int) -> tuple[int, ...]:
        if row_ids == [0, 1, 2, 3] and attempt == 1:
            raise ActorPoolTaskError(
                task=row_ids,
                cause=ActorLostError(
                    snapshot=ActorStateSnapshot(
                        actor_id="actor-cgroup-oom",
                        state="DEAD",
                        death_reason="WORKER_DIED",
                        node_id="node-live",
                    ),
                    task=row_ids,
                ),
            )
        return tuple(row_ids)

    pod_status_fetches = 0

    def fetch_pod_statuses() -> list[PodStatus]:
        nonlocal pod_status_fetches
        pod_status_fetches += 1
        return [
            {
                "name": "ray-worker",
                "phase": "Failed",
                "ready": False,
                "node_type": "worker",
                "node_name": "node-live",
                "waiting_reasons": Counter(),
                "init_waiting_reasons": Counter(),
                "pulling_count": 0,
                "gpu_requested": False,
                "node_is_gpu": False,
                "oom_evidence": Counter({"last_state.reason=OOMKilled": 1}),
            }
        ]

    pool = _FakePool(lose_worker_once)
    state = _ScalarUDTFWorkState(total_work_items=1)

    results = list(
        _iter_scalar_udtf_results(
            pool,  # type: ignore[arg-type]
            lambda _actor, row_ids: row_ids,
            [[0, 1, 2, 3]],
            prefetch=1,
            oom_budget_tracker=_tracker(),
            job_tracker=None,
            job_id="scalar-cgroup-oom-test",
            state=state,
            pod_status_fetcher=fetch_pod_statuses,
        )
    )

    assert results == [(0, 1), (2, 3)]
    assert pool.submitted == [[0, 1, 2, 3], [0, 1], [2, 3]]
    assert pod_status_fetches == 1
    assert state.total_work_items == 2
    assert state.completed_work_items == 2
    assert state.oom_recoveries == 1


def test_scalar_udtf_irreducible_oom_exhausts_same_range_budget() -> None:
    """A one-row OOM reruns on replacements only until the hard budget fires."""

    def always_oom(row_ids: list[int], _attempt: int) -> None:
        raise ActorPoolTaskError(
            task=row_ids,
            cause=FatalWorkerOOMError("worker OOMKilled"),
        )

    pool = _FakePool(always_oom)
    tracker = _tracker(max_same_range=1)
    state = _ScalarUDTFWorkState(total_work_items=1)

    with pytest.raises(FatalWorkerOOMError, match="OOM recovery budget exceeded"):
        list(
            _iter_scalar_udtf_results(
                pool,  # type: ignore[arg-type]
                lambda _actor, row_ids: row_ids,
                [[7]],
                prefetch=1,
                oom_budget_tracker=tracker,
                job_tracker=None,
                job_id="scalar-irreducible-test",
                state=state,
            )
        )

    assert pool.submitted == [[7], [7]]
    assert tracker.total_oom_recoveries == 2
    assert state.total_work_items == 1
    assert state.completed_work_items == 0
    assert state.oom_recoveries == 1


def test_scalar_udtf_non_oom_transient_actor_loss_retries_same_work() -> None:
    """A node loss keeps the pre-existing exact-work-item retry semantics."""

    def lose_node_once(row_ids: list[int], attempt: int) -> tuple[int, ...]:
        if attempt == 1:
            raise ActorPoolTaskError(
                task=row_ids,
                cause=ActorLostError(
                    snapshot=ActorStateSnapshot(
                        actor_id="actor-transient",
                        state="DEAD",
                        death_reason="NODE_DIED",
                        node_id="node-gone",
                    ),
                    task=row_ids,
                ),
            )
        return tuple(row_ids)

    pool = _FakePool(lose_node_once)
    state = _ScalarUDTFWorkState(total_work_items=1)

    results = list(
        _iter_scalar_udtf_results(
            pool,  # type: ignore[arg-type]
            lambda _actor, row_ids: row_ids,
            [[8, 9]],
            prefetch=1,
            oom_budget_tracker=_tracker(),
            job_tracker=None,
            job_id="scalar-transient-test",
            state=state,
        )
    )

    assert results == [(8, 9)]
    assert pool.submitted == [[8, 9], [8, 9]]
    assert state.total_work_items == 1
    assert state.completed_work_items == 1
    assert state.oom_recoveries == 0


def test_scalar_udtf_transient_loss_does_not_extend_stall_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Repeated transient losses remain bounded by the no-progress deadline."""

    def lose_node(row_ids: list[int], _attempt: int) -> None:
        raise ActorPoolTaskError(
            task=row_ids,
            cause=ActorLostError(
                snapshot=ActorStateSnapshot(
                    actor_id="actor-transient",
                    state="DEAD",
                    death_reason="NODE_DIED",
                    node_id="node-gone",
                ),
                task=row_ids,
            ),
        )

    times = iter([100.0, 101.0])
    monkeypatch.setattr(pipeline_module, "PIPELINE_STALL_TIMEOUT_S", 0.5)
    monkeypatch.setattr(pipeline_module.time, "monotonic", lambda: next(times))

    pool = _FakePool(lose_node)
    state = _ScalarUDTFWorkState(total_work_items=1)

    with pytest.raises(TimeoutError, match="Scalar UDTF ActorPool stalled"):
        list(
            _iter_scalar_udtf_results(
                pool,  # type: ignore[arg-type]
                lambda _actor, row_ids: row_ids,
                [[8, 9]],
                prefetch=1,
                oom_budget_tracker=_tracker(),
                job_tracker=None,
                job_id="scalar-transient-stall-test",
                state=state,
            )
        )

    assert pool.submitted == [[8, 9]]
    assert state.completed_work_items == 0
    assert state.oom_recoveries == 0


def test_scalar_udtf_non_oom_task_error_is_not_split() -> None:
    """The scalar recovery loop is strictly OOM-only."""
    original = ActorPoolTaskError(
        task=[1, 2],
        cause=FatalWorkerExitError("worker exited"),
    )

    def fail_non_oom(_row_ids: list[int], _attempt: int) -> None:
        raise original

    pool = _FakePool(fail_non_oom)
    state = _ScalarUDTFWorkState(total_work_items=1)

    with pytest.raises(ActorPoolTaskError) as exc_info:
        list(
            _iter_scalar_udtf_results(
                pool,  # type: ignore[arg-type]
                lambda _actor, row_ids: row_ids,
                [[1, 2]],
                prefetch=1,
                oom_budget_tracker=_tracker(),
                job_tracker=None,
                job_id="scalar-non-oom-test",
                state=state,
            )
        )

    assert exc_info.value is original
    assert pool.submitted == [[1, 2]]
    assert state.oom_recoveries == 0


def test_scalar_udtf_worker_loss_without_pod_oom_is_not_split() -> None:
    """An untagged worker death stays fail-fast without fresh pod OOM evidence."""
    original = ActorPoolTaskError(
        task=[1, 2],
        cause=ActorLostError(
            snapshot=ActorStateSnapshot(
                actor_id="actor-exit",
                state="DEAD",
                death_reason="WORKER_DIED",
                node_id="node-live",
            ),
            task=[1, 2],
        ),
    )

    def fail_worker(_row_ids: list[int], _attempt: int) -> None:
        raise original

    pool = _FakePool(fail_worker)
    state = _ScalarUDTFWorkState(total_work_items=1)

    with pytest.raises(ActorPoolTaskError) as exc_info:
        list(
            _iter_scalar_udtf_results(
                pool,  # type: ignore[arg-type]
                lambda _actor, row_ids: row_ids,
                [[1, 2]],
                prefetch=1,
                oom_budget_tracker=_tracker(),
                job_tracker=None,
                job_id="scalar-worker-exit-test",
                state=state,
                pod_status_fetcher=list,
            )
        )

    assert exc_info.value is original
    assert pool.submitted == [[1, 2]]
    assert state.oom_recoveries == 0
