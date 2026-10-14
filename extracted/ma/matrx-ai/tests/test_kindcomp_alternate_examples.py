"""kindcomp_get_context hands the component author whole alternate example bodies."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from matrx_ai.tools.implementations.kind_component import (
    ALTERNATE_EXAMPLES_BUDGET_CHARS,
    _alternate_example_bodies,
)


def _ex(i: int, *, status: str = "passed", size: int = 10, canonical: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        id=f"ex-{i}",
        label=f"Example {i}",
        source="captured",
        validation_status=status,
        is_canonical=canonical,
        data={"__kind": "k", "text": "x" * size},
        updated_at=datetime(2026, 10, 1, tzinfo=UTC) + timedelta(minutes=i),
    )


def test_alternates_exclude_canonical_and_failed_newest_first() -> None:
    canonical = _ex(0, canonical=True)
    rows = [canonical, _ex(1), _ex(2, status="failed"), _ex(3)]
    out, note = _alternate_example_bodies(rows, canonical)
    assert [e["id"] for e in out] == ["ex-3", "ex-1"]
    assert out[0]["data"] == rows[3].data
    assert note is None


def test_an_example_that_does_not_fit_is_named_never_cut() -> None:
    canonical = _ex(0, canonical=True)
    big = _ex(5, size=ALTERNATE_EXAMPLES_BUDGET_CHARS)
    out, note = _alternate_example_bodies([canonical, _ex(1), big], canonical)
    assert [e["id"] for e in out] == ["ex-1"]
    assert note and "1 more" in note
