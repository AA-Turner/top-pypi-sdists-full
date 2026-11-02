"""Unit tests for ``_now_iso``."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.aggregation import (
    _now_iso,
    _parse_iso,
)


def test_now_iso_returns_parseable_utc_timestamp() -> None:
    ts = _now_iso()
    parsed = _parse_iso(ts)
    assert parsed.tzinfo is not None
