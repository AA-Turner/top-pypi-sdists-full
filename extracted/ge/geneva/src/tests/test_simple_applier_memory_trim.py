# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

from typing import TYPE_CHECKING

import pyarrow as pa

from geneva.apply.simple import SimpleApplier
from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, BackfillUDFTask, ReadTask
from geneva.debug.logger import NoOpErrorLogger
from geneva.transformer import udf

if TYPE_CHECKING:
    from collections.abc import Iterator

    import pytest


class _ReadTask(ReadTask):
    def __init__(self, batches: list[pa.RecordBatch]) -> None:
        self._batches = batches

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch]:
        yield from self._batches

    def checkpoint_key(self) -> str:
        return "dummy"

    def dest_frag_id(self) -> int:
        return 0

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return sum(batch.num_rows for batch in self._batches)

    def table_uri(self) -> str:
        return "memory://dummy"


@udf(data_type=pa.int64(), batch_size=1)
def _identity(a: int) -> int:
    return a


def _batch(value: int) -> pa.RecordBatch:
    return pa.record_batch(
        {
            "a": pa.array([value], type=pa.int64()),
            "_rowaddr": pa.array([value], type=pa.uint64()),
        }
    )


def test_simple_applier_trims_memory_every_eight_batches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def _record_trim() -> None:
        nonlocal calls
        calls += 1

    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)
    monkeypatch.setattr(
        "geneva.apply.simple.release_unused_process_memory",
        _record_trim,
    )

    read_task = _ReadTask([_batch(idx) for idx in range(9)])
    map_task = BackfillUDFTask(udfs={"b": _identity})
    applier = SimpleApplier(job_id="test")

    result_batches = list(
        applier.run(read_task, map_task, error_logger=NoOpErrorLogger())
    )

    assert len(result_batches) == 9
    assert calls == 1


def test_simple_applier_memory_trim_can_be_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def _record_trim() -> None:
        nonlocal calls
        calls += 1

    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "0")
    monkeypatch.setattr(
        "geneva.apply.simple.release_unused_process_memory",
        _record_trim,
    )

    read_task = _ReadTask([_batch(idx) for idx in range(9)])
    map_task = BackfillUDFTask(udfs={"b": _identity})
    applier = SimpleApplier(job_id="test")

    result_batches = list(
        applier.run(read_task, map_task, error_logger=NoOpErrorLogger())
    )

    assert len(result_batches) == 9
    assert calls == 0
