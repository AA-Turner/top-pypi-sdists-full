"""Write flattened rows to CSV."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence


_META_COLUMNS = ("job_id", "created_at")


def write_csv(
    path: str | Path,
    rows: Iterable[dict],
    *,
    fields: Sequence[str] | None = None,
    utf8_sig: bool = False,
) -> tuple[int, list[str]]:
    """
    Write *rows* to *path*.

    Returns ``(row_count, fieldnames)``. When *fields* is omitted, column names
    are the union of keys seen across all rows (``job_id``, ``created_at`` first).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    buffered = list(rows)
    if fields:
        fieldnames = list(fields)
    else:
        fieldnames = _fieldnames_from_rows(buffered)

    encoding = "utf-8-sig" if utf8_sig else "utf-8"
    with path.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            restval="",
        )
        writer.writeheader()
        for row in buffered:
            writer.writerow({name: row.get(name, "") for name in fieldnames})

    return len(buffered), fieldnames


def _fieldnames_from_rows(rows: list[dict]) -> list[str]:
    seen: dict[str, None] = {}
    for row in rows:
        for key in row:
            if key not in seen:
                seen[key] = None
    ordered = [col for col in _META_COLUMNS if col in seen]
    for key in seen:
        if key not in _META_COLUMNS:
            ordered.append(key)
    return ordered
