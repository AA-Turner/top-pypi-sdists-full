# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pytest

from geneva.apply.task import ScanTask, SparseRangeTask
from geneva.config.loader import from_env, loader
from geneva.errors import FatalWorkerOOMError
from geneva.runners.ray.oom_recovery_budget import (
    METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED,
    METRIC_FATAL_WORKER_OOM_RECOVERIES,
    OOMRecoveryBudgetConfig,
    OOMRecoveryBudgetTracker,
    init_oom_recovery_metrics,
    oom_recovery_target_split_fanout,
    oom_recovery_task_ranges,
    read_task_oom_range_key,
    record_oom_recovery_attempt,
    row_ids_oom_range_key,
)
from geneva.table import TableReference


def _oom() -> FatalWorkerOOMError:
    return FatalWorkerOOMError("worker pod was OOMKilled")


def _tracker(
    *,
    enabled: bool = True,
    max_total: int = 10,
    max_same_range: int = 3,
) -> OOMRecoveryBudgetTracker:
    return OOMRecoveryBudgetTracker(
        config=OOMRecoveryBudgetConfig(
            enabled=enabled,
            max_total_oom_recoveries=max_total,
            max_same_range_oom_recoveries=max_same_range,
        )
    )


def _table_ref() -> TableReference:
    return TableReference(table_id=["tbl"], version=None, db_uri="db://example")


def _scan_task(**overrides: object) -> ScanTask:
    values = {
        "uri": "s3://bucket/table",
        "table_ref": _table_ref(),
        "columns": ["a", "b"],
        "frag_id": 7,
        "offset": 123,
        "limit": 456,
        "version": 12,
        "where": "a > 5",
        "src_files_hash": "files-sha",
    }
    values.update(overrides)
    return ScanTask(**values)  # type: ignore[arg-type]


def _sparse_task(**overrides: object) -> SparseRangeTask:
    values = {
        "uri": "s3://bucket/table",
        "table_ref": _table_ref(),
        "frag_ids": [3, 5, 8],
        "where": "a > 5",
        "output_column": "embedding",
        "version": 12,
    }
    values.update(overrides)
    return SparseRangeTask(**values)  # type: ignore[arg-type]


def test_total_budget_fails_on_eleventh_recovery() -> None:
    tracker = _tracker(max_total=10, max_same_range=100)

    for i in range(10):
        attempt = tracker.record(
            job_id="job-1",
            range_key=f"range-{i}",
            oom_exc=_oom(),
        )
        assert attempt is not None
        assert attempt.total_count == i + 1

    with pytest.raises(FatalWorkerOOMError) as exc_info:
        tracker.record(job_id="job-1", range_key="range-10", oom_exc=_oom())

    message = str(exc_info.value)
    assert "job_id=job-1" in message
    assert "total=11/10" in message
    assert "same_range=1/100" in message
    assert "range_key=range-10" in message
    assert "original_oom=worker pod was OOMKilled" in message


def test_same_range_budget_fails_on_fourth_recovery() -> None:
    tracker = _tracker(max_total=100, max_same_range=3)

    for i in range(3):
        attempt = tracker.record(job_id="job-1", range_key="range-a", oom_exc=_oom())
        assert attempt is not None
        assert attempt.same_range_count == i + 1

    with pytest.raises(FatalWorkerOOMError) as exc_info:
        tracker.record(job_id="job-1", range_key="range-a", oom_exc=_oom())

    message = str(exc_info.value)
    assert "job_id=job-1" in message
    assert "total=4/100" in message
    assert "same_range=4/3" in message
    assert "range_key=range-a" in message
    assert "original_oom=worker pod was OOMKilled" in message


def test_different_exact_ranges_count_separately_but_share_total() -> None:
    tracker = _tracker(max_total=10, max_same_range=3)

    first = tracker.record(job_id="job-1", range_key="range-a", oom_exc=_oom())
    second = tracker.record(job_id="job-1", range_key="range-a", oom_exc=_oom())
    third = tracker.record(job_id="job-1", range_key="range-b", oom_exc=_oom())

    assert first is not None
    assert first.total_count == 1
    assert first.same_range_count == 1
    assert second is not None
    assert second.total_count == 2
    assert second.same_range_count == 2
    assert third is not None
    assert third.total_count == 3
    assert third.same_range_count == 1


def test_disabled_budget_does_not_count_or_fail() -> None:
    tracker = _tracker(enabled=False, max_total=0, max_same_range=0)

    for _ in range(5):
        assert (
            tracker.record(job_id="job-1", range_key="range-a", oom_exc=_oom()) is None
        )

    assert tracker.total_oom_recoveries == 0


def test_config_base_env_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GENEVA_OOM_RECOVERY_BUDGET__ENABLED", "false")
    monkeypatch.setenv("GENEVA_OOM_RECOVERY_BUDGET__MAX_TOTAL_OOM_RECOVERIES", "17")
    monkeypatch.setenv("GENEVA_OOM_RECOVERY_BUDGET__MAX_SAME_RANGE_OOM_RECOVERIES", "9")
    monkeypatch.setenv("GENEVA_OOM_RECOVERY_BUDGET__TARGET_SPLIT_FANOUT", "10")

    config = loader(from_env()).load(OOMRecoveryBudgetConfig)

    assert config.enabled is False
    assert config.max_total_oom_recoveries == 17
    assert config.max_same_range_oom_recoveries == 9
    assert config.target_split_fanout == 10


def test_config_target_split_fanout_defaults_to_adaptive() -> None:
    assert OOMRecoveryBudgetConfig().target_split_fanout is None


@pytest.mark.parametrize(
    ("task_size", "expected"),
    [
        (999, 2),
        (1_000, 10),
        (999_999, 10),
        (1_000_000, 100),
    ],
)
def test_oom_recovery_target_split_fanout_is_adaptive(
    task_size: int, expected: int
) -> None:
    assert oom_recovery_target_split_fanout(task_size) == expected


@pytest.mark.parametrize(
    ("total_rows", "target_split_fanout", "expected_sizes"),
    [
        (20, 2, [10, 10]),
        (23, 10, [3, 3, 3, 2, 2, 2, 2, 2, 2, 2]),
    ],
    ids=["two-way", "ten-way-remainder"],
)
def test_oom_recovery_task_ranges_are_balanced_and_deterministic(
    total_rows: int,
    target_split_fanout: int,
    expected_sizes: list[int],
) -> None:
    ranges = oom_recovery_task_ranges(
        total_rows=total_rows,
        covered=[],
        target_split_fanout=target_split_fanout,
    )
    assert [size for _, size in ranges] == expected_sizes
    assert [start for start, _ in ranges] == [
        sum(expected_sizes[:index]) for index in range(len(expected_sizes))
    ]


def test_oom_recovery_task_ranges_preserve_fragmented_checkpoint_gaps() -> None:
    assert oom_recovery_task_ranges(
        total_rows=32,
        covered=[(4, 8), (12, 16), (20, 24)],
        target_split_fanout=10,
    ) == [
        (0, 2),
        (2, 2),
        (8, 2),
        (10, 2),
        (16, 2),
        (18, 2),
        (24, 2),
        (26, 2),
        (28, 2),
        (30, 2),
    ]


def test_oom_recovery_task_ranges_normalize_checkpoint_coverage() -> None:
    assert oom_recovery_task_ranges(
        total_rows=20,
        covered=[(12, 16), (-3, 3), (2, 6), (10, 14), (25, 30)],
        target_split_fanout=4,
    ) == [(6, 2), (8, 2), (16, 2), (18, 2)]


def test_oom_recovery_task_ranges_can_exceed_target_for_disjoint_gaps() -> None:
    assert oom_recovery_task_ranges(
        total_rows=9,
        covered=[(1, 2), (3, 4), (5, 6), (7, 8)],
        target_split_fanout=2,
    ) == [(0, 1), (2, 1), (4, 1), (6, 1), (8, 1)]


def test_oom_recovery_task_ranges_validate_edge_cases() -> None:
    assert (
        oom_recovery_task_ranges(
            total_rows=12,
            covered=[(0, 12)],
            target_split_fanout=10,
        )
        == []
    )
    with pytest.raises(ValueError, match="target_split_fanout must be at least 2"):
        oom_recovery_task_ranges(
            total_rows=10,
            covered=[],
            target_split_fanout=1,
        )
    with pytest.raises(ValueError, match="must be >= 2"):
        OOMRecoveryBudgetConfig(target_split_fanout=1)


def test_scan_task_range_key_uses_exact_task_identity() -> None:
    task = _scan_task()
    key = read_task_oom_range_key(task)

    assert key.startswith("ScanTask:")
    assert "uri=s3://bucket/table" in key
    assert "version=12" in key
    assert "frag=7" in key
    assert "offset=123" in key
    assert "limit=456" in key
    assert "where=sha1:" in key
    assert "src_files_hash=files-sha" in key
    assert "a > 5" not in key

    assert key != read_task_oom_range_key(_scan_task(version=13))
    assert key != read_task_oom_range_key(_scan_task(frag_id=8))
    assert key != read_task_oom_range_key(_scan_task(offset=124))
    assert key != read_task_oom_range_key(_scan_task(limit=457))
    assert key != read_task_oom_range_key(_scan_task(where="a > 6"))
    assert key != read_task_oom_range_key(_scan_task(src_files_hash="other-files"))


def test_sparse_range_task_key_uses_exact_task_identity_with_frag_ids_digest() -> None:
    task = _sparse_task()
    key = read_task_oom_range_key(task)

    assert key.startswith("SparseRangeTask:")
    assert "uri=s3://bucket/table" in key
    assert "version=12" in key
    assert "where=sha1:" in key
    assert "output_column=embedding" in key
    assert "frag_ids=" in key
    assert "[3, 5, 8]" not in key

    assert key != read_task_oom_range_key(_sparse_task(version=13))
    assert key != read_task_oom_range_key(_sparse_task(where="a > 6"))
    assert key != read_task_oom_range_key(_sparse_task(output_column="caption"))
    assert key != read_task_oom_range_key(_sparse_task(frag_ids=[8, 5, 3]))


def test_row_ids_key_is_stable_digest_without_full_row_ids() -> None:
    row_ids = list(range(100))

    key = row_ids_oom_range_key(row_ids)

    assert key == row_ids_oom_range_key(tuple(row_ids))
    assert key.startswith("scalar_udtf_row_ids:")
    assert "count=100" in key
    assert "first=0" in key
    assert "last=99" in key
    assert "sha1=" in key
    assert str(row_ids) not in key
    assert len(key) < 100


class _FakeRemoteMethod:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []

    def remote(self, *args: object) -> None:
        self.calls.append(args)


class _FakeJobTracker:
    def __init__(self) -> None:
        self.set_desc = _FakeRemoteMethod()
        self.increment = _FakeRemoteMethod()


def test_metric_helpers_initialize_and_record_attempts() -> None:
    job_tracker = _FakeJobTracker()
    tracker = _tracker(max_total=1, max_same_range=10)

    init_oom_recovery_metrics(job_tracker)
    assert job_tracker.set_desc.calls == [
        (METRIC_FATAL_WORKER_OOM_RECOVERIES, "Fatal worker OOM recovery attempts"),
        (
            METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED,
            "Fatal worker OOM recovery budget exceeded",
        ),
    ]

    attempt = record_oom_recovery_attempt(
        tracker,
        job_tracker=job_tracker,
        job_id="job-1",
        range_key="range-a",
        oom_exc=_oom(),
    )
    assert attempt is not None
    assert job_tracker.increment.calls == [
        (METRIC_FATAL_WORKER_OOM_RECOVERIES, 1),
    ]

    with pytest.raises(FatalWorkerOOMError):
        record_oom_recovery_attempt(
            tracker,
            job_tracker=job_tracker,
            job_id="job-1",
            range_key="range-b",
            oom_exc=_oom(),
        )
    assert job_tracker.increment.calls[-2:] == [
        (METRIC_FATAL_WORKER_OOM_RECOVERIES, 1),
        (METRIC_FATAL_WORKER_OOM_BUDGET_EXCEEDED, 1),
    ]


def test_shrunk_recoveries_are_not_charged_and_never_fail() -> None:
    """Shrinking retries are progress: uncounted and exempt from fail-fast."""
    tracker = _tracker(max_total=2, max_same_range=1)

    # Far more shrinking recoveries than either limit allows.
    for i in range(10):
        attempt = tracker.record(
            job_id="job-1",
            range_key=f"range-{i % 2}",
            oom_exc=_oom(),
            shrunk=True,
        )
        assert attempt is not None
        assert attempt.total_count == 0
        assert attempt.same_range_count == 0

    assert tracker.total_oom_recoveries == 0

    # Non-shrinking recoveries still charge the budget and fail fast.
    assert tracker.record(job_id="job-1", range_key="stuck", oom_exc=_oom())
    with pytest.raises(FatalWorkerOOMError):
        tracker.record(job_id="job-1", range_key="stuck", oom_exc=_oom())
