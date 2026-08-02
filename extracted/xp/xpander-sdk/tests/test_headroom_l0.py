"""Unit tests for the Layer-0 headroom lossless compaction used by the agno
tool hook (`_headroom_compact` / `_get_headroom_crusher`).

These exercise the real Rust-backed `headroom` crusher — `headroom-ai` is a hard
dependency — so no mocking of the compressor is needed.
"""

from __future__ import annotations

import json

import pytest

from xpander_sdk.modules.backend.frameworks.agno import (
    _get_headroom_crusher,
    _headroom_compact,
)


def _round_trip(compacted: str) -> set:
    """Parse a CSV+schema compaction back into a set of (id, name) tuples so a
    test can assert no rows were dropped without depending on field order."""
    # The array is compacted into a single JSON string value whose body is
    # `[N]{schema}` followed by newline-separated CSV rows.
    body = json.loads(compacted)
    lines = [ln for ln in body.splitlines() if ln]
    header = lines[0]
    fields = header[header.index("{") + 1 : header.index("}")].split(",")
    name_idx = next(i for i, f in enumerate(fields) if f.startswith("name"))
    id_idx = next(i for i, f in enumerate(fields) if f.startswith("id"))
    rows = set()
    for ln in lines[1:]:
        cells = ln.split(",")
        rows.add((cells[id_idx], cells[name_idx]))
    return rows


def test_json_array_is_compacted_losslessly_and_shrinks():
    arr = [
        {"id": i, "name": f"item{i}", "status": "active", "score": i * 2}
        for i in range(30)
    ]
    src = json.dumps(arr)
    out = _headroom_compact(src)

    assert out is not None
    assert len(out) < len(src)
    assert "<<ccr:" not in out
    # Every original row survives (lossless): all 30 ids present.
    rows = _round_trip(out)
    assert len(rows) == 30
    assert ("0", "item0") in rows
    assert ("29", "item29") in rows


def test_dict_input_is_serialized_and_compacted():
    arr = [{"id": i, "v": "x" * 20} for i in range(20)]
    out = _headroom_compact(arr)  # pass the list object, not a string
    assert out is not None
    assert len(out) < len(json.dumps(arr))


def test_non_json_string_returns_none():
    # Must NOT raise (the Rust panic path is avoided by the json.loads guard).
    assert _headroom_compact("hello world, not json") is None


def test_incompressible_payload_returns_none():
    # Already-minified JSON that cannot shrink is left alone (None = keep original).
    assert _headroom_compact('{"a":1}') is None


def test_crusher_is_a_cached_singleton():
    assert _get_headroom_crusher() is _get_headroom_crusher()
