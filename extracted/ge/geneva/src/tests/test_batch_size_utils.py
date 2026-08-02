# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging

import pytest

from geneva.table import Table
from geneva.utils.batch_size import (
    default_task_size,
    resolve_batch_size,
    resolve_task_size,
)


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


def test_resolve_task_size_uses_dynamic_default() -> None:
    assert resolve_task_size(task_size=None, row_count=100, num_workers=4) == 12
    assert default_task_size(row_count=40, num_workers=8) == 2


def test_resolve_task_size_respects_override_and_fallback() -> None:
    assert resolve_task_size(task_size=25, row_count=10, num_workers=2) == 25
    assert resolve_task_size(task_size=None, row_count=None, num_workers=2) == 100
