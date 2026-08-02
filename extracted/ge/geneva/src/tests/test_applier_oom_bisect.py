# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit test: bisect path inside ``_handle_fatal_task_failure``.

``test_on_error.py`` already covers the *outcome* of actor-death +
``skip_on_error()`` (null checkpoint, ``FatalWorkerExitError`` record
in ``geneva_errors``). That suite uses small fragments and
``concurrency=1`` and tends to null-checkpoint the failing row via the
checkpoint-recovery shortcut rather than walking through the bisect
loop in ``pipeline.py:1155-1183``.

This test specifically forces the *bisect loop* to run by sizing the
failing task wide enough that ``_replacement_scan_tasks`` returns
multi-row replacements, then asserts that at least one
null-checkpointed row's ``ErrorRecord.bisect_depth`` is greater than
zero -- proving the failing ScanTask was actually halved on the way
down to a single row.

Crash mechanism: ``os._exit(137)`` from inside the UDF kills the
worker process immediately. Ray's framework surfaces this as
``ActorDiedError`` on the driver side, which is the same surface as a
real kernel cgroup OOM kill.
"""

from __future__ import annotations

import logging
import os
import uuid
from typing import TYPE_CHECKING

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import udf
from geneva.debug.error_store import ErrorStore, skip_on_error
from geneva.errors import FatalWorkerError

if TYPE_CHECKING:
    from pathlib import Path

_LOG = logging.getLogger(__name__)


# Sized so the initial failing ScanTask has limit > 1, forcing the
# bisect loop to halve the range several times before isolating the
# bad row.
ROWS = 16
BAD_ROW_INDICES = (7,)
APPLIER_CONCURRENCY = 2
URL_BATCH_SIZE = 4


@udf(
    data_type=pa.binary(),
    batch_size=URL_BATCH_SIZE,
    on_error=skip_on_error(),
)
def crash_on_bad_row(row_id: int) -> bytes:
    if row_id in BAD_ROW_INDICES:
        os._exit(137)
    return b"\x00"


@udf(data_type=pa.binary(), batch_size=URL_BATCH_SIZE)
def crash_on_bad_row_no_skip(row_id: int) -> bytes:
    if row_id in BAD_ROW_INDICES:
        os._exit(137)
    return b"\x00"


def _build_input_table(uri: str, rows: int = ROWS) -> None:
    tbl = pa.Table.from_pydict({"row_id": list(range(rows))})
    lance.write_dataset(tbl, uri, max_rows_per_file=rows)


def _setup_table(tmp_path: Path, udf_fn, rows: int = ROWS) -> tuple:  # noqa: ANN001
    uri = str(tmp_path / "input")
    _build_input_table(uri, rows=rows)
    db = geneva.connect(str(tmp_path))
    src = lance.dataset(uri).to_table()
    table_name = f"crash-{uuid.uuid4().hex[:8]}"
    tbl = db.create_table(table_name, src)
    tbl.add_columns({"img": udf_fn})
    return db, tbl


_ACTOR_DEATH_ERROR_TYPES = (
    "FatalWorkerOOMError",
    "FatalWorkerCrashError",
    "FatalWorkerExitError",
    "OutOfMemoryError",
)


@pytest.mark.ray
@pytest.mark.timeout(180)
def test_bisect_loop_runs_to_single_row(
    local_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
) -> None:
    """Bisect loop halves a multi-row failing task down to one row and
    null-checkpoints it. ``bisect_depth > 0`` on the resulting error
    record is the evidence that the loop ran (as opposed to the
    failing task being null-checkpointed in one shot via the
    checkpoint-recovery shortcut)."""
    db, tbl = _setup_table(tmp_path, crash_on_bad_row)
    job_id = uuid.uuid4().hex
    result = tbl.backfill(
        "img",
        concurrency=APPLIER_CONCURRENCY,
        intra_applier_concurrency=1,
        commit_granularity=1,
        _admission_check=False,
        job_id=job_id,
    )
    assert result.status == "DONE", f"unexpected status: {result.status}"

    store = ErrorStore(db)
    all_errors = store.get_errors(job_id=job_id)
    actor_errors = [e for e in all_errors if e.error_type in _ACTOR_DEATH_ERROR_TYPES]
    planted = len(BAD_ROW_INDICES)
    if not actor_errors:
        type_counts: dict[str, int] = {}
        for e in all_errors:
            type_counts[e.error_type] = type_counts.get(e.error_type, 0) + 1
        raise AssertionError(
            f"expected >= {planted} actor-death records, got 0. "
            f"All error types: {type_counts}"
        )
    assert len(actor_errors) >= planted
    depths = [getattr(e, "bisect_depth", None) for e in actor_errors]
    assert any(d is not None and d > 0 for d in depths), (
        f"expected at least one record with bisect_depth > 0 "
        f"(proves the bisect loop ran); got depths={depths}. "
        f"If this fails, the failing task was null-checkpointed via the "
        f"checkpoint-recovery shortcut rather than the bisect loop."
    )
    max_depth = max((d for d in depths if d is not None), default=0)
    types_seen = sorted({e.error_type for e in actor_errors})
    _LOG.info(
        "bisect summary: planted=%d actor_errors=%d types=%s depths=%s max_depth=%d",
        planted,
        len(actor_errors),
        types_seen,
        depths,
        max_depth,
    )

    arrow_tbl = tbl.to_arrow().sort_by("row_id")
    img = arrow_tbl["img"].to_pylist()
    for idx in BAD_ROW_INDICES:
        assert img[idx] is None, f"row {idx} should be null; got {img[idx]!r}"
    populated = sum(1 for v in img if v is not None)
    assert populated == ROWS - len(BAD_ROW_INDICES)


@pytest.mark.ray
@pytest.mark.timeout(180)
def test_no_on_error_raises_fatal_worker(
    local_ray_context: None,  # noqa: ARG001
    tmp_path: Path,
) -> None:
    """No ``on_error`` and the actor crashes: backfill raises with
    ``FatalWorkerError`` in the cause chain. Companion to
    ``test_bisect_loop_runs_to_single_row`` proving the no-skip path
    exits cleanly rather than running the bisect loop."""
    _db, tbl = _setup_table(tmp_path, crash_on_bad_row_no_skip)
    with pytest.raises((RuntimeError, FatalWorkerError)) as exc_info:
        tbl.backfill(
            "img",
            concurrency=APPLIER_CONCURRENCY,
            intra_applier_concurrency=1,
            commit_granularity=1,
            _admission_check=False,
        )
    chain: list[BaseException] = []
    cur: BaseException | None = exc_info.value
    while cur is not None:
        chain.append(cur)
        cur = cur.__cause__ or cur.__context__
    assert any(isinstance(e, FatalWorkerError) for e in chain), (
        f"expected FatalWorker* in exception chain; got "
        f"{[type(e).__name__ + ': ' + str(e)[:120] for e in chain]}"
    )
