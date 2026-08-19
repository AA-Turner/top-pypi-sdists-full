# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging

import pytest

from geneva.table import Table
from geneva.utils.batch_size import (
    default_task_size,
    resolve_batch_size,
    resolve_read_task_rows,
    resolve_task_size,
)

# JobConfig.applier_target_read_bytes default; passed explicitly so these stay
# pure sizing tests with no config dependency.
TARGET_READ_BYTES = 512 << 20


def test_resolve_batch_size_prefers_checkpoint_alias(
    caplog: pytest.LogCaptureFixture,
) -> None:
    assert resolve_batch_size(checkpoint_size=5) == 5
    assert resolve_batch_size(batch_size=7, checkpoint_size=7) == 7
    with caplog.at_level(logging.WARNING):
        assert resolve_batch_size(batch_size=4, checkpoint_size=9) == 9
    assert any("overrides batch_size" in rec.message for rec in caplog.records)
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        assert resolve_batch_size(batch_size=6) == 6
    assert any("batch_size is deprecated" in rec.message for rec in caplog.records)
    assert resolve_batch_size() is None


def test_table_normalize_backfill_checkpoint_size() -> None:
    kwargs = {"checkpoint_size": 12}
    Table._normalize_backfill_batch_kwargs(kwargs)
    assert kwargs == {"checkpoint_size": 12}


def test_table_normalize_backfill_conflict_raises(
    caplog: pytest.LogCaptureFixture,
) -> None:
    kwargs = {"batch_size": 8, "checkpoint_size": 4}
    with caplog.at_level(logging.WARNING):
        Table._normalize_backfill_batch_kwargs(kwargs)
    assert any("overrides batch_size" in rec.message for rec in caplog.records)
    assert kwargs == {"checkpoint_size": 4}


def test_table_normalize_backfill_preserves_task_size() -> None:
    kwargs = {"task_size": 5}
    Table._normalize_backfill_batch_kwargs(kwargs)
    assert kwargs == {"task_size": 5, "checkpoint_size": None}


def test_default_task_size_is_capped_by_largest_fragment() -> None:
    assert default_task_size(row_count=40, num_workers=8) == 2
    assert (
        default_task_size(
            row_count=10_000,
            num_workers=2,
            max_fragment_size=1_000,
        )
        == 1_000
    )


@pytest.mark.parametrize(
    ("task_size", "row_count", "num_workers", "max_fragment_size", "expected"),
    [
        (None, 100, 4, None, 12),
        (None, 100, 4, 50, 12),
        (None, 10_000, 2, 0, 1),
        (25, 10, 2, 3, 25),
        (0, 10, 2, 3, 0),
        (None, None, 2, 3, 100),
    ],
    ids=[
        "dynamic",
        "fragment-larger-than-dynamic",
        "empty-fragment-floor",
        "explicit",
        "whole-fragment",
        "missing-row-count-fallback",
    ],
)
def test_resolve_task_size_matrix(
    task_size: int | None,
    row_count: int | None,
    num_workers: int,
    max_fragment_size: int | None,
    expected: int,
) -> None:
    assert (
        resolve_task_size(
            task_size=task_size,
            row_count=row_count,
            num_workers=num_workers,
            max_fragment_size=max_fragment_size,
        )
        == expected
    )


class TestResolveReadTaskRows:
    """Read tasks are sized in rows, so the row-only default is blind to how
    wide a row is. These cover the byte-aware clamp that keeps a 150 KB image
    column from planning tens of GB of read buffer per task."""

    IMAGE_BYTES = 150 * 1024

    def _resolve(self, **kw) -> tuple[int, int]:
        params = {
            "task_size": None,
            "row_count": 1_000_000,
            "num_workers": 8,
            "max_fragment_size": None,
            "avg_row_bytes": None,
            "target_read_bytes": TARGET_READ_BYTES,
        }
        params.update(kw)
        return resolve_read_task_rows(**params)

    def test_narrow_rows_keep_the_row_default(self) -> None:
        # 8 B/row never approaches the budget -> the parallelism-driven default
        # stands, untouched.
        task_size, rows = self._resolve(avg_row_bytes=8)

        assert task_size == rows == 1_000_000 // 8 // 2

    def test_wide_rows_are_sized_from_the_byte_target(self) -> None:
        task_size, rows = self._resolve(avg_row_bytes=self.IMAGE_BYTES)
        target = TARGET_READ_BYTES

        assert task_size == rows
        assert rows < 1_000_000 // 8 // 2  # the row default would be 62,500
        assert rows & (rows - 1) == 0, "quantized to a power of two"
        # The whole point: a task reads about the target, not 9.6 GB.
        assert rows * self.IMAGE_BYTES <= target
        assert 2 * rows * self.IMAGE_BYTES > target, "and not needlessly small"

    def test_explicit_task_size_is_never_clamped(self) -> None:
        # The caller asked for a size; admission's advice covers it if it
        # doesn't fit. Silently shrinking it would be worse.
        task_size, rows = self._resolve(
            task_size=50_000, avg_row_bytes=self.IMAGE_BYTES
        )

        assert task_size == rows == 50_000

    def test_zero_target_disables_auto_sizing(self) -> None:
        task_size, rows = self._resolve(
            avg_row_bytes=self.IMAGE_BYTES, target_read_bytes=0
        )

        assert task_size == rows == 1_000_000 // 8 // 2

    def test_no_sample_keeps_the_row_default(self) -> None:
        task_size, rows = self._resolve(avg_row_bytes=None)

        assert task_size == rows == 1_000_000 // 8 // 2

    def test_one_task_per_fragment_reports_the_fragment_bound(self) -> None:
        # task_size <= 0 is a deliberate planner mode: keep it, and bound memory
        # by the largest fragment the task can span.
        task_size, rows = self._resolve(
            task_size=0, max_fragment_size=90_000, avg_row_bytes=self.IMAGE_BYTES
        )

        assert task_size == 0
        assert rows == 90_000

    def test_one_task_per_fragment_without_a_fragment_bound_uses_row_count(
        self,
    ) -> None:
        # The fragment probe can fail; a whole-fragment read priced at the 100-row
        # default would sail through admission. No fragment exceeds the table.
        task_size, rows = self._resolve(
            task_size=0, max_fragment_size=None, avg_row_bytes=self.IMAGE_BYTES
        )

        assert task_size == 0
        assert rows == 1_000_000

    def test_one_task_per_fragment_with_no_bound_at_all_warns(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.WARNING):
            task_size, rows = self._resolve(
                task_size=-1, row_count=None, max_fragment_size=None
            )

        assert (task_size, rows) == (-1, 100)
        assert "may understate" in caplog.text
