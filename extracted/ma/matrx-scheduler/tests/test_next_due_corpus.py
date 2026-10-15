"""The Python side of THE next-due corpus shared with @ai-matrx/data/scheduler.

apps/shared/data/src/scheduler/next-due.corpus.json holds the instants compute_next_due_at gives;
the TypeScript package's next-due.test.ts checks computeNextDueAt against the same file. A change
to either side that moves an instant turns one of the two red.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from matrx_scheduler.next_due import compute_next_due_at

CORPUS = Path(__file__).resolve().parents[3] / "apps/shared/data/src/scheduler/next-due.corpus.json"


def _cases() -> list[dict]:
    return json.loads(CORPUS.read_text())["cases"]


@pytest.mark.parametrize("case", _cases(), ids=lambda c: c["name"])
def test_python_matches_the_shared_corpus(case: dict) -> None:
    now = datetime.fromisoformat(case["now"].replace("Z", "+00:00"))
    got = compute_next_due_at(case["type"], case["config"], now)
    want = case["next_due_at"]
    if want is None:
        assert got is None
    else:
        assert got is not None
        assert got.astimezone(UTC) == datetime.fromisoformat(want.replace("Z", "+00:00"))
