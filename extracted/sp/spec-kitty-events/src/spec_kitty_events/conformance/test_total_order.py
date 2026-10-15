"""Packaged conformance runner for the total-order fixtures.

Drives :func:`spec_kitty_events.total_order.order_rows` through every case under
``producer_contract/fixtures/total_order/`` (the nine worked examples of
spec-kitty/spec-kitty#6185 plus edge cases), asserting the pinned result for each
permutation of the rows: the same ordered rows, collapsed count, conflict keys and error
rows however the input is arranged. A consumer that re-implements the order in another
language runs the same fixture files against its own comparator.

Cases of at most seven rows are checked against every permutation; larger cases against
a fixed-seed sample plus the sorted and reversed arrangements.
"""

from __future__ import annotations

import itertools
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest

from spec_kitty_events.total_order import OrderResult, order_rows

_CASES_DIR = (
    Path(__file__).resolve().parent.parent / "producer_contract" / "fixtures" / "total_order"
)
_EXHAUSTIVE_UP_TO = 7
_SAMPLE = 1500


def _case_paths() -> List[Path]:
    return sorted(_CASES_DIR.glob("*.json"))


def _load(path: Path) -> Dict[str, Any]:
    loaded: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return loaded


def _bytes(row: Any) -> bytes:
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def _arrangements(count: int) -> List[Tuple[int, ...]]:
    indexes = tuple(range(count))
    if count <= _EXHAUSTIVE_UP_TO:
        return list(itertools.permutations(indexes))
    rng = random.Random(41)
    sample = [tuple(rng.sample(indexes, count)) for _ in range(_SAMPLE)]
    return [indexes, tuple(reversed(indexes))] + sample


def _check(case: Dict[str, Any], arrangement: Tuple[int, ...]) -> OrderResult:
    labelled = case["rows"]
    rows = [labelled[i]["row"] for i in arrangement]
    labels = [labelled[i]["label"] for i in arrangement]
    result = order_rows(rows)
    expected = case["expected"]
    by_label = {item["label"]: item["row"] for item in labelled}

    assert result.read == expected["read"] == len(labelled)
    assert len(result.ordered) + len(result.errors) + result.collapsed == result.read
    # Ordered rows are compared by their bytes: a duplicate that collapses into an
    # equal-bytes twin may be either object.
    assert [_bytes(row) for row in result.ordered] == [
        _bytes(by_label[name]) for name in expected["ordered"]
    ]
    assert result.collapsed == expected["collapsed"]
    assert [list(key) for key in result.conflicts] == sorted(expected["conflicts"])
    got_errors = sorted((labels[e.position], e.reason) for e in result.errors)
    assert got_errors == sorted(expected["errors"].items())
    return result


def test_the_nine_worked_examples_are_present() -> None:
    ids = {_load(path)["id"][:2] for path in _case_paths()}
    assert {f"{n:02d}" for n in range(1, 10)} <= ids


@pytest.mark.parametrize("path", _case_paths(), ids=lambda p: p.stem)
def test_case_gives_one_result_for_every_arrangement(path: Path) -> None:
    case = _load(path)
    arrangements = _arrangements(len(case["rows"]))
    canonical = None
    for arrangement in arrangements:
        result = _check(case, arrangement)
        form = result.canonical()
        # Error rows are compared as a multiset with position excluded, so the canonical
        # form must be identical across arrangements.
        if canonical is None:
            canonical = form
        assert form == canonical, f"{case['id']}: arrangement {arrangement} changed the result"
    assert canonical is not None
