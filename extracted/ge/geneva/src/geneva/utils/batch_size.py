# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Helpers for normalizing batch-size parameters.

``checkpoint_size`` controls **map-task** batch sizing (how frequently UDF
results are checkpointed), while ``task_size`` controls **read-task** sizing
(how many rows are fetched per worker task). Historically the two were coupled
via ``batch_size``; these utilities keep backward compatibility while allowing
them to diverge.
"""

from __future__ import annotations

import logging

_FALLBACK_TASK_SIZE = 100

_LOG = logging.getLogger(__name__)


def resolve_batch_size(
    *, batch_size: int | None = None, checkpoint_size: int | None = None
) -> int | None:
    """Return the map-task batch size, preferring ``checkpoint_size``.

    If both values are provided and differ, ``checkpoint_size`` wins and a warning
    is logged. When only ``batch_size`` is provided, a deprecation warning is
    emitted. ``None`` means callers should fall back to their own default.
    """
    if (
        batch_size is not None
        and checkpoint_size is not None
        and batch_size != checkpoint_size
    ):
        _LOG.warning(
            "checkpoint_size (%s) overrides batch_size (%s); values should match,"
            " batch_size is deprecated.",
            checkpoint_size,
            batch_size,
        )
        return checkpoint_size
    elif batch_size is not None and checkpoint_size is None:
        _LOG.warning(
            "batch_size is deprecated; please use checkpoint_size instead (value=%s).",
            batch_size,
        )
        return batch_size

    if checkpoint_size is not None:
        return checkpoint_size
    return batch_size


def default_task_size(*, row_count: int, num_workers: int) -> int:
    """Compute the dynamic default read-task size.

    The default is ``table.count_rows() // num_workers // 2`` with sane guards
    (at least 1 row; at least one worker). ``num_workers`` is typically the
    applier concurrency.
    """

    workers = max(1, int(num_workers))
    return max(1, int(row_count) // workers // 2)


def resolve_task_size(
    *,
    task_size: int | None,
    row_count: int | None,
    num_workers: int,
) -> int:
    """Resolve the read-task size, falling back to a dynamic default.

    ``task_size`` takes precedence when provided. When ``task_size`` is ``None``
    and ``row_count`` is available, the dynamic default from
    [`default_task_size`][default_task_size] is used. If ``row_count`` cannot
    be determined,
    the function falls back to a conservative 100 rows per task to avoid overly
    large reads. ``task_size`` of 0 or a negative value is preserved so callers
    can request "one task per fragment" semantics in downstream planners.
    """

    if task_size is not None:
        return int(task_size)

    if row_count is not None:
        return default_task_size(row_count=row_count, num_workers=num_workers)

    _LOG.warning(
        "Unable to compute dynamic task_size (missing row_count); falling back to %s",
        _FALLBACK_TASK_SIZE,
    )
    return _FALLBACK_TASK_SIZE
