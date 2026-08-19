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


def default_task_size(
    *,
    row_count: int,
    num_workers: int,
    max_fragment_size: int | None = None,
) -> int:
    """Compute the dynamic default read-task size.

    The default is the smaller of ``table.count_rows() // num_workers // 2``
    and the largest fragment, with sane guards (at least 1 row; at least one
    worker). ``num_workers`` is typically the applier concurrency.
    """

    workers = max(1, int(num_workers))
    task_size = max(1, int(row_count) // workers // 2)
    if max_fragment_size is not None:
        task_size = min(task_size, max(1, int(max_fragment_size)))
    return task_size


def resolve_task_size(
    *,
    task_size: int | None,
    row_count: int | None,
    num_workers: int,
    max_fragment_size: int | None = None,
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
        return default_task_size(
            row_count=row_count,
            num_workers=num_workers,
            max_fragment_size=max_fragment_size,
        )

    _LOG.warning(
        "Unable to compute dynamic task_size (missing row_count); falling back to %s",
        _FALLBACK_TASK_SIZE,
    )
    return _FALLBACK_TASK_SIZE


def resolve_read_task_rows(
    *,
    task_size: int | None,
    row_count: int | None,
    num_workers: int,
    max_fragment_size: int | None,
    avg_row_bytes: int | None,
    target_read_bytes: int,
    log: bool = True,
) -> tuple[int, int]:
    """Resolve the read-task size and the row bound its memory is sized from.

    Returns ``(task_size, max_rows_per_task)``. They differ only when
    ``task_size <= 0`` ("one task per fragment"), where the bound is the largest
    fragment.

    What we actually want to cap is the *bytes* a read pulls in, but read tasks
    are sized in rows, so the row-only default
    ([`resolve_task_size`][resolve_task_size]) is blind to row width: at
    150 KB/row it plans tens of GB per task, at 8 B/row it never comes close.
    So set the target size and derive the row count from it --
    ``target_read_bytes // avg_row_bytes`` -- capped by the parallelism-driven
    default (this only ever lowers it) and skipped when the caller named a
    ``task_size``. Narrow rows keep the row default untouched; a per-actor
    reservation then lands near a constant regardless of row width.

    This is the row half of the eventual read-API byte cap: once reads take a
    byte limit directly, the same target goes to the reader and the effective
    bound becomes min(rows, bytes).

    The row count is quantized down to a power of two so ordinary sample drift
    doesn't move task boundaries between runs -- ``ScanTask.checkpoint_key``
    hashes the task's offset/limit, so shifting boundaries would strand
    checkpoints written by an earlier run.
    """
    explicit = task_size is not None
    resolved = resolve_task_size(
        task_size=task_size,
        row_count=row_count,
        num_workers=num_workers,
        max_fragment_size=max_fragment_size,
    )
    if resolved <= 0:
        # "One task per fragment" is a deliberate planner mode; honor it and
        # bound memory by the largest fragment. When the metadata probe couldn't
        # give one, fall back to the table's row count -- no fragment exceeds it
        # -- rather than the small row default, which would price a
        # whole-fragment read at 100 rows and let it pass admission.
        bound = max_fragment_size or row_count
        if not bound or bound <= 0:
            _LOG.warning(
                "No fragment or row-count bound for a one-task-per-fragment read;"
                " sizing its memory from %s rows, which may understate a large"
                " fragment.",
                _FALLBACK_TASK_SIZE,
            )
            bound = _FALLBACK_TASK_SIZE
        return resolved, max(1, int(bound))

    target_bytes = int(target_read_bytes or 0)
    if explicit or target_bytes <= 0 or not avg_row_bytes or avg_row_bytes <= 0:
        return resolved, resolved

    fits = max(1, target_bytes // int(avg_row_bytes))
    if fits >= resolved:
        return resolved, resolved

    rows = 1 << (fits.bit_length() - 1)
    if log:
        _LOG.info(
            "Auto-sized task_size %s -> %s: at %.1f KB/row that reads %.0f MiB "
            "per task, against a %.0f MiB target. Pass task_size= to override.",
            resolved,
            rows,
            avg_row_bytes / 1024,
            rows * avg_row_bytes / (1 << 20),
            target_bytes / (1 << 20),
        )
    return rows, rows
