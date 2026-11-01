"""ParquetRecords: Parquet files -- first rows as JSONL and the footer's row count, only when pyarrow is already imported."""

from __future__ import annotations
import json
import sys
from probe.sdk.artifact.record_formats.lines import PREVIEW_MAX_BYTES, PREVIEW_MAX_RECORDS


def _parquet_sample(path: str) -> tuple[bytes, int, str] | None:
    if "pyarrow" not in sys.modules:
        return None  # never imported for this (R27): no sample
    try:
        import pyarrow.parquet as pq

        batch = next(pq.ParquetFile(path).iter_batches(batch_size=PREVIEW_MAX_RECORDS), None)
        if batch is None:
            return None
        out = b""
        records = 0
        for row in batch.to_pylist():
            line = (json.dumps(row, default=str, ensure_ascii=False) + "\n").encode("utf-8")
            if len(out) + len(line) > PREVIEW_MAX_BYTES:
                break
            out += line
            records += 1
        return (out, records, ".jsonl") if records else None
    except Exception:  # noqa: BLE001 - no sample, never a failure
        return None
