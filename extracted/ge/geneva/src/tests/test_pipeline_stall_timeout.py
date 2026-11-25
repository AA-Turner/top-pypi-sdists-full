# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""The shared inactivity budget applies even when workers keep failing."""

from collections import Counter, deque
from types import SimpleNamespace
from unittest.mock import MagicMock

import attrs
import pyarrow as pa
import pytest

import geneva.runners.ray.pipeline as pipeline
from geneva import FatalWorkerError, FatalWorkerExitError, Retry, udf
from geneva.apply.task import BackfillUDFTask, ScanTask
from geneva.checkpoint import CheckpointStore, stamp_checkpoint_num_rows
from geneva.config.loader import from_env, loader
from geneva.jobs.config import JobConfig
from geneva.runners.ray.actor_pool import (
    ActorPool,
    ActorPoolTaskError,
    PollTimeoutError,
)
from geneva.runners.ray.pipeline import ColumnAddPipelineJob, ScheduledReadTask
from geneva.table import TableReference


@udf(data_type=pa.int64(), on_error=[Retry(FatalWorkerError, max_attempts=100)])
def _retrying_udf(a: int) -> int:
    return a + 1


def _scripted_job(
    monkeypatch: pytest.MonkeyPatch,
    events: list[tuple[float, str]],
    *,
    oom: bool = False,
    num_tasks: int = 1,
) -> tuple[ColumnAddPipelineJob, SimpleNamespace, MagicMock, MagicMock]:
    """Run the real feeder and failure handler with scripted worker results."""
    clock = SimpleNamespace(now=0.0)
    ref = TableReference(["tbl"], None, table_uri="memory://tbl")
    task = ScanTask(
        uri="memory://tbl", table_ref=ref, columns=["a"], frag_id=0, offset=0, limit=8
    )
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": _retrying_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=ref,
        input_plan=iter(()),
        job_id=None,
    )
    if oom:
        # Default OOM recovery splits work without the explicit retry policy.
        job.map_task = BackfillUDFTask(
            udfs={"b": attrs.evolve(_retrying_udf, error_handling=None)}
        )

    pending: deque[ScheduledReadTask] = deque()
    script = iter(events)
    pool = MagicMock()
    pool._num_actors = 1
    pool._drained_buffer = []
    pool.has_buffered_results.side_effect = lambda: ActorPool.has_buffered_results(pool)
    pool.submission_capacity.side_effect = lambda: max(0, 1 - len(pending))
    pool.has_next.side_effect = lambda: bool(pending)
    pool.submit.side_effect = lambda fn, scheduled: pending.append(scheduled)
    pool.last_hardware_fault = None

    def drain_ready(timeout: float) -> list:
        delay, outcome = next(script)
        clock.now += delay
        if outcome == "poll":
            raise PollTimeoutError
        scheduled = pending.popleft()
        current = scheduled.task
        if outcome == "complete":
            return [(current, [], None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]
        if outcome in ("partial", "recover"):
            rows = current.num_rows()
            if outcome == "partial":
                rows //= 2
            start = current.dest_offset()
            key = job.map_task.checkpoint_key(
                dataset_uri=current.table_uri(),
                frag_id=current.dest_frag_id(),
                start=start,
                end=start + rows,
            )
            batch = pa.record_batch(
                [
                    pa.array(range(rows), type=f.type)
                    for f in job.map_task.output_schema()
                ],
                schema=job.map_task.output_schema(),
            )
            job.checkpoint_store[key] = stamp_checkpoint_num_rows(batch)
        cause = (
            pipeline.FatalWorkerOOMError("worker OOM")
            if oom
            else FatalWorkerExitError("worker exited")
        )
        raise ActorPoolTaskError(scheduled, cause)

    pool.drain_ready.side_effect = drain_ready
    fwm = MagicMock()
    fwm._reconciled_rows_checkpointed_total = 0
    fwm._reconciled_written_fragments_total = 0
    fwm._reconciled_rows_committed_total = 0

    def ingest(task: object, checkpoints: list) -> None:
        fwm._reconciled_rows_checkpointed_total += sum(c.span for c in checkpoints)

    fwm.ingest_task.side_effect = ingest
    fwm.ingest_recovered_checkpoints.side_effect = ingest
    monkeypatch.setattr(pipeline, "time", SimpleNamespace(monotonic=lambda: clock.now))
    monkeypatch.setattr(pipeline, "PIPELINE_STALL_TIMEOUT_S", 6.0)
    monkeypatch.setattr(pipeline, "FragmentWriterManager", lambda *a, **k: fwm)
    monkeypatch.setattr(pipeline, "_ClusterStatusRefresher", MagicMock())
    monkeypatch.setattr(pipeline, "_emit_otel_metrics", lambda *a, **k: None)
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_inputplans",
        lambda self: (
            iter(attrs.evolve(task, offset=8 * i) for i in range(num_tasks)),
            Counter({0: num_tasks}),
            num_tasks,
        ),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_writertracker",
        lambda self, count: (SimpleNamespace(uri="memory://tbl", version=1), 1),
    )
    monkeypatch.setattr(ColumnAddPipelineJob, "setup_actorpool", lambda self: pool)
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_ensure_driver_checkpoint_identity_sidecar",
        lambda *a: None,
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_refresh_cluster_status", lambda self: None
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_get_k8s_pod_statuses", lambda self: None
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_k8s_pod_diagnostics", lambda self: "no pods"
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob, "_cluster_status_age_str", lambda self: "0s"
    )
    return job, clock, pool, fwm


@pytest.mark.parametrize("oom", [False, True], ids=["retry", "oom-split"])
def test_worker_failures_without_poll_timeout_exhaust_idle_budget(
    monkeypatch: pytest.MonkeyPatch, oom: bool
) -> None:
    job, clock, pool, fwm = _scripted_job(
        monkeypatch, [(4, "fail"), (4, "fail"), (0, "complete")], oom=oom
    )

    with pytest.raises(TimeoutError, match="Pipeline stalled") as exc_info:
        job.run()

    assert isinstance(exc_info.value.__cause__, FatalWorkerError)
    assert clock.now == 8
    assert pool.drain_ready.call_count == 2
    assert fwm._reconciled_rows_checkpointed_total == 0
    pool.shutdown.assert_called_once()


def test_poll_timeout_after_failure_uses_original_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job, clock, pool, _ = _scripted_job(monkeypatch, [(4, "fail"), (3, "poll")])
    with pytest.raises(TimeoutError, match="Pipeline stalled"):
        job.run()
    assert clock.now == 7
    pool.shutdown.assert_called_once()


@pytest.mark.parametrize("outcome", ["partial", "recover", "complete"])
def test_useful_recovery_and_task_completion_renew_idle_budget(
    monkeypatch: pytest.MonkeyPatch, outcome: str
) -> None:
    job, clock, pool, fwm = _scripted_job(
        monkeypatch,
        [(4, outcome), (4, "poll"), (1, "complete")],
        num_tasks=1 if outcome == "partial" else 2,
    )

    job.run()

    assert clock.now > 6
    if outcome != "complete":
        assert fwm._reconciled_rows_checkpointed_total > 0
    pool.shutdown.assert_called_once()


def test_recovery_does_not_give_subsequent_failures_a_new_budget(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job, clock, pool, _ = _scripted_job(
        monkeypatch, [(4, "partial"), (4, "fail"), (3, "poll")]
    )
    with pytest.raises(TimeoutError, match="Pipeline stalled"):
        job.run()
    assert clock.now == 11
    pool.shutdown.assert_called_once()


@pytest.mark.parametrize("later_failures", [False, True], ids=["success", "stall"])
def test_buffered_success_is_ingested_before_declaring_stall(
    monkeypatch: pytest.MonkeyPatch, later_failures: bool
) -> None:
    events = [(7, "complete"), (0, "fail")]
    events.extend([(4, "fail"), (3, "fail")] if later_failures else [(0, "complete")])
    job, clock, pool, fwm = _scripted_job(monkeypatch, events, num_tasks=2)
    # Use the real drain methods: a successful first result is buffered when
    # resolving the next ready future raises the recoverable worker failure.
    pool._num_actors = 2
    pool.submission_capacity.side_effect = None
    pool.submission_capacity.return_value = 2
    scripted_drain = pool.drain_ready.side_effect
    pool._drained_buffer = []
    future = object()
    pool._future_to_actor = {future: None}
    pool.get_next_unordered.side_effect = lambda timeout=None: scripted_drain(timeout)[
        0
    ]

    def resolve_future(future: object) -> tuple:
        pool._future_to_actor.clear()
        return scripted_drain(0)[0]

    pool._resolve_future.side_effect = resolve_future
    pool._drain_ready_now.side_effect = lambda results: ActorPool._drain_ready_now(
        pool, results
    )
    pool.drain_ready.side_effect = lambda timeout=None: ActorPool.drain_ready(
        pool, timeout
    )
    monkeypatch.setattr(
        "geneva.runners.ray.actor_pool.ray.wait",
        lambda futures, **kwargs: (list(futures), []),
    )

    if later_failures:
        with pytest.raises(TimeoutError, match="Pipeline stalled"):
            job.run()
        assert clock.now == 14
        assert fwm.ingest_task.call_count == 1
    else:
        job.run()
        assert clock.now == 7
        assert fwm.ingest_task.call_count == 2
    assert pool._drained_buffer == []
    pool.shutdown.assert_called_once()


@pytest.mark.parametrize(
    ("oom", "events"),
    [
        (False, [(0, "complete"), (0, "complete")]),
        (False, [(0, "complete"), (0, "fail"), (0, "complete")]),
        (True, [(0, "complete"), (0, "fail"), (0, "complete"), (0, "complete")]),
    ],
    ids=["no-failure", "retry", "oom-split"],
)
def test_idle_appliers_released_only_once_the_feeder_is_dry(
    monkeypatch: pytest.MonkeyPatch, oom: bool, events: list[tuple[float, str]]
) -> None:
    """With release_idle_appliers on, the loop releases idle appliers only after
    the feeder has handed out every task, including late replacement work from
    a retry or an OOM split, and never while that work is still queued."""
    job, _clock, pool, _fwm = _scripted_job(monkeypatch, events, oom=oom, num_tasks=2)
    job.config = attrs.evolve(
        job.config, release_idle_appliers=True, release_idle_appliers_after_s=5.0
    )
    drains_at_release: list[int] = []

    def release_idle_actors(**kwargs: object) -> int:
        assert kwargs == {"idle_grace_s": 5.0, "cleanup_method": "flush_telemetry"}
        drains_at_release.append(pool.drain_ready.call_count)
        return 0

    pool.release_idle_actors.side_effect = release_idle_actors

    job.run()

    assert drains_at_release == [len(events)]
    pool.shutdown.assert_called_once()


def test_idle_appliers_kept_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Release is opt-in: a default JobConfig keeps every applier until the
    job ends."""
    job, _clock, pool, _fwm = _scripted_job(
        monkeypatch, [(0, "complete"), (0, "complete")], num_tasks=2
    )

    job.run()

    pool.release_idle_actors.assert_not_called()
    pool.shutdown.assert_called_once()


def test_idle_appliers_released_with_default_grace_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Once enabled, the default 60s idle grace applies."""
    job, _clock, pool, _fwm = _scripted_job(
        monkeypatch, [(0, "complete"), (0, "complete")], num_tasks=2
    )
    job.config = attrs.evolve(job.config, release_idle_appliers=True)
    pool.release_idle_actors.return_value = 0

    job.run()

    pool.release_idle_actors.assert_called_with(
        idle_grace_s=60.0, cleanup_method="flush_telemetry"
    )
    pool.shutdown.assert_called_once()


def test_idle_appliers_release_is_checked_on_every_poll_during_a_tail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Once the feeder is dry, the loop asks the pool to release after every
    result and every poll timeout, while the last task still runs. Polls wait
    POLL_INTERVAL_S at most, so an applier goes within one poll of the end of
    its grace."""
    job, clock, pool, _fwm = _scripted_job(
        monkeypatch,
        [(0, "complete"), (1, "poll"), (1, "poll"), (1, "complete")],
        num_tasks=2,
    )
    # Two appliers: both tasks start at once and the second is the tail.
    pool._num_actors = 2
    pool.submission_capacity.side_effect = None
    pool.submission_capacity.return_value = 3
    job.config = attrs.evolve(
        job.config, release_idle_appliers=True, release_idle_appliers_after_s=2.5
    )
    release_times: list[float] = []

    def release_idle_actors(**kwargs: object) -> int:
        assert kwargs == {"idle_grace_s": 2.5, "cleanup_method": "flush_telemetry"}
        release_times.append(clock.now)
        return 0

    pool.release_idle_actors.side_effect = release_idle_actors

    job.run()

    assert release_times == [0, 1, 2, 3]
    drain_timeouts = {c.kwargs["timeout"] for c in pool.drain_ready.call_args_list}
    assert drain_timeouts == {pipeline.POLL_INTERVAL_S}
    pool.shutdown.assert_called_once()


@pytest.mark.parametrize(
    ("env_value", "expected"), [(None, False), ("false", False), ("true", True)]
)
def test_release_idle_appliers_env_var(
    monkeypatch: pytest.MonkeyPatch, env_value: str | None, expected: bool
) -> None:
    """JOB__RELEASE_IDLE_APPLIERS=true opts in to the off-by-default release."""
    if env_value is None:
        monkeypatch.delenv("JOB__RELEASE_IDLE_APPLIERS", raising=False)
    else:
        monkeypatch.setenv("JOB__RELEASE_IDLE_APPLIERS", env_value)

    config = JobConfig.from_loader(loader(from_env()))

    assert config.release_idle_appliers is expected


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [(None, 60.0), ("0", 0.0), ("2.5", 2.5), ("-3", 0.0)],
)
def test_release_idle_appliers_after_s_env_var(
    monkeypatch: pytest.MonkeyPatch, env_value: str | None, expected: float
) -> None:
    """JOB__RELEASE_IDLE_APPLIERS_AFTER_S sets the idle grace; 0 (or a
    negative value) releases idle appliers immediately."""
    if env_value is None:
        monkeypatch.delenv("JOB__RELEASE_IDLE_APPLIERS_AFTER_S", raising=False)
    else:
        monkeypatch.setenv("JOB__RELEASE_IDLE_APPLIERS_AFTER_S", env_value)

    config = JobConfig.from_loader(loader(from_env()))

    assert config.release_idle_appliers_after_s == expected
