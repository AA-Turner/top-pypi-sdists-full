"""LineRecords: CSV/TSV/JSONL files -- a preview cut at whole lines within the byte cap, rows counted from the hashing read."""

from __future__ import annotations
import os
#: A preview sample: at most this many records, and at most this many bytes.
PREVIEW_MAX_RECORDS = 100
PREVIEW_MAX_BYTES = 256 * 1024
#: Line-record formats a preview (and a row count) reads as text.
_LINE_SUFFIXES = (".jsonl", ".ndjson", ".csv", ".tsv", ".txt")
_HEADER_SUFFIXES = (".csv", ".tsv")


# ---------------------------------------------------------------------------
# Preview samples (C11)
# ---------------------------------------------------------------------------


def preview_sample(path: str) -> tuple[bytes, int, str] | None:
    """First `PREVIEW_MAX_RECORDS` records (CSV/TSV: plus the header), cut at a whole
    line within `PREVIEW_MAX_BYTES`; Parquet's first rows as JSONL only if `pyarrow`
    is already imported. ``(bytes, records, extension)``, or None if nothing to show."""
    from ...capture import lineage as inputs

    ext = os.path.splitext(path)[1].lower()
    if ext == ".parquet":
        from probe.sdk.artifact.record_formats.parquet import _parquet_sample  # call time: parquet imports this module

        with inputs.internal():  # Probe's own read, never one of the run's
            return _parquet_sample(path)
    if ext not in _LINE_SUFFIXES:
        return None
    try:
        with inputs.internal(), open(path, "rb") as handle:
            head = handle.read(PREVIEW_MAX_BYTES + 1)
    except OSError:
        return None
    lines = head.splitlines(keepends=True)
    if len(head) > PREVIEW_MAX_BYTES and lines and not lines[-1].endswith((b"\n", b"\r")):
        lines = lines[:-1]  # cut at the last whole line
    keep = PREVIEW_MAX_RECORDS + (1 if ext in _HEADER_SUFFIXES else 0)
    kept = lines[:keep]
    out = b"".join(kept)
    while len(out) > PREVIEW_MAX_BYTES and kept:
        kept = kept[:-1]
        out = b"".join(kept)
    records = len(kept) - (1 if ext in _HEADER_SUFFIXES and kept else 0)
    if records <= 0:
        return None
    return out, records, ".jsonl" if ext == ".ndjson" else ext
