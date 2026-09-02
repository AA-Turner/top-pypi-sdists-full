"""Helpers for writing records to Labric tables, mixed into the exported client (see client.py).

`client.write_core_table` and `client.write_labric_table` send data to the write endpoint in a
single request by default. Set rows_per_batch to split a large data list across multiple requests
instead, e.g.:

    client.write_labric_table(
        "measurements", data=rows, rows_per_batch=1000,
        on_progress=lambda written, total: logger.info(f"{written}/{total} written"),
    )

Each batch is also capped at MAX_BATCH_BYTES of serialized JSON, so wide rows can't
push a single request over the API's body size limit even when rows_per_batch would
otherwise allow it.

Each batch is its own request and therefore its own transaction: if a batched write
fails partway through, the earlier batches remain committed and the rest are not
retried, since replaying a batch that already landed would duplicate rows in
mode="create". Pass on_progress to track how many rows were written before a
failure.

Pass job_execution_id (or set the LABRIC_JOB_EXECUTION_ID environment variable) to
record every batch against a single job execution, so the whole write can be
reverted or inspected as one unit. Without it, each batch gets its own job
execution.

Pass collect_output=False unless you need the written rows back -- otherwise every
row is echoed back by the API and accumulated in memory.
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable

# A reasonable rows_per_batch for append-only writes (mode="create"). Upserts need
# far fewer rows per batch: the create-or-update path runs several queries per row,
# so a few hundred rows can already take longer than the API's 60s worker timeout.
DEFAULT_ROWS_PER_BATCH = 5000

# Ceiling on the serialized JSON size of the rows in one request, comfortably under
# the API's 2.5 MB body limit so the surrounding request fields still fit.
# rows_per_batch alone can't guarantee this -- wide rows exceed the limit long before
# the row count does -- so batches are also cut on size. Measuring it costs one JSON
# encode per row on top of the encode the client performs when sending the request,
# which is negligible next to the network round trip each batch makes.
MAX_BATCH_BYTES = 2_000_000


class WriteWrappers:
    """`tools.write` shorthands, mixed into the exported client (see client.py).

    `job_execution_id` falls back to the environment variable the job runner sets, so
    writes made from a job script attach to that execution without being told about it.
    """

    def write_core_table(
        self,
        target_name: str,
        data: list[dict[str, Any]],
        params_to_match_for_update: list[str] | None = None,
        mode: str = "create-or-update",
        defaults: dict[str, str] | None = None,
        collect_output: bool = True,
        rows_per_batch: int | None = None,
        on_progress: Callable[[int, int], None] | None = None,
        job_execution_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Write records to a core table, splitting across multiple requests of rows_per_batch rows when set."""
        return _write(
            self,
            data,
            rows_per_batch,
            on_progress,
            job_execution_id,
            target_type="core-table",
            target_name=target_name,
            mode=mode,
            params_to_match_for_update=params_to_match_for_update,
            defaults=defaults,
            collect_output=collect_output,
        )

    def write_labric_table(
        self,
        target_name: str,
        data: list[dict[str, Any]],
        params_to_match_for_update: list[str] | None = None,
        mode: str = "create-or-update",
        defaults: dict[str, str] | None = None,
        batch_insert_ok: bool = False,
        collect_output: bool = True,
        rows_per_batch: int | None = None,
        on_progress: Callable[[int, int], None] | None = None,
        job_execution_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Write records to a Labric table, splitting across multiple requests of rows_per_batch rows when set."""
        return _write(
            self,
            data,
            rows_per_batch,
            on_progress,
            job_execution_id,
            target_type="table",
            target_name=target_name,
            mode=mode,
            params_to_match_for_update=params_to_match_for_update,
            defaults=defaults,
            batch_insert_ok=batch_insert_ok,
            collect_output=collect_output,
        )


def _write(
    client,
    data: list[dict[str, Any]],
    rows_per_batch: int | None,
    on_progress: Callable[[int, int], None] | None,
    job_execution_id: str | None,
    **write_arguments: Any,
) -> list[dict[str, Any]]:
    """Write data in a single request, or split across multiple requests of rows_per_batch rows each.

    on_progress is called after each batch with the number of rows written so far and
    the total, letting callers track progress without reimplementing the batching loop.
    """
    write_arguments["job_execution_id"] = job_execution_id or os.getenv(
        "LABRIC_JOB_EXECUTION_ID"
    )
    if rows_per_batch is None:
        return client.tools.write(data=data, **write_arguments)
    if rows_per_batch < 1:
        raise ValueError(f"rows_per_batch must be at least 1, got {rows_per_batch}")
    records: list[dict[str, Any]] = []
    rows_written = 0
    for batch in _batches(data, rows_per_batch):
        records.extend(client.tools.write(data=batch, **write_arguments) or [])
        rows_written += len(batch)
        if on_progress is not None:
            on_progress(rows_written, len(data))
    return records


def _batches(data: list[dict[str, Any]], rows_per_batch: int):
    """Split data into batches of at most rows_per_batch rows and MAX_BATCH_BYTES of JSON.

    A row that exceeds MAX_BATCH_BYTES by itself still gets a batch of its own: rows
    are never split, so the API rejects it rather than the SDK dropping it silently.
    """
    batch: list[dict[str, Any]] = []
    batch_bytes = 0
    for row in data:
        row_bytes = len(json.dumps(row, default=str))
        if batch and (
            len(batch) >= rows_per_batch or batch_bytes + row_bytes > MAX_BATCH_BYTES
        ):
            yield batch
            batch, batch_bytes = [], 0
        batch.append(row)
        batch_bytes += row_bytes
    if batch:
        yield batch
