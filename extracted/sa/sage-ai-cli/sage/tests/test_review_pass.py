"""Tests for review_pass."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from sage.core.review_pass import (
    _parse_review,
    regenerate_for_gaps,
    review_and_repair,
    review_file,
)


def _gen(responses: list[str]) -> Callable[[str], str]:
    it = iter(responses)
    return lambda _: next(it, "")


class TestParseReview:
    def test_extracts_score_and_gaps(self) -> None:
        raw = json.dumps({"score": 8.5, "gaps": ["a", "b"], "notes": "ok"})
        r = _parse_review(raw)
        assert r.score == 8.5
        assert r.gaps == ["a", "b"]

    def test_extracts_from_prose(self) -> None:
        raw = "Sure, here:\n" + json.dumps({"score": 7.0, "gaps": [], "notes": "fine"})
        r = _parse_review(raw)
        assert r.score == 7.0

    def test_handles_garbage(self) -> None:
        r = _parse_review("not json")
        assert r.score == 5.0  # default

    def test_handles_empty(self) -> None:
        r = _parse_review("")
        assert r.score == 5.0


class TestReviewFile:
    def test_reads_and_scores(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def x(): return 1\n")
        gen = _gen([json.dumps({"score": 9.0, "gaps": [], "notes": "great"})])
        r = review_file(p, "x", "fastapi", gen)
        assert r.score == 9.0

    def test_missing_file_returns_zero(self, tmp_path: Path) -> None:
        r = review_file(tmp_path / "missing.py", "x", "fastapi", _gen([""]))
        assert r.score == 0.0


class TestReviewAndRepair:
    def test_passes_immediately_when_high_score(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def x(): return 1\n")
        gen = _gen([json.dumps({"score": 9.0, "gaps": [], "notes": "ok"})])
        result = review_and_repair(p, "x", "fastapi", gen, lambda s: s, threshold=7.0)
        assert result.score == 9.0

    def test_regenerates_then_succeeds(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def x(): return 1\n")
        gen = _gen([
            json.dumps({"score": 5.0, "gaps": ["missing docstring"], "notes": "low"}),
            'def x():\n    """docstring."""\n    return 1\n',
            json.dumps({"score": 8.0, "gaps": [], "notes": "good"}),
        ])
        result = review_and_repair(p, "x", "fastapi", gen, lambda s: s, threshold=7.0)
        assert result.score == 8.0
        # File was rewritten
        assert "docstring" in p.read_text()

    def test_stops_after_max_rounds(self, tmp_path: Path) -> None:
        p = tmp_path / "x.py"
        p.write_text("def x(): return 1\n")
        # Always low score → must stop at max_rounds and report
        gen = _gen([
            json.dumps({"score": 3.0, "gaps": ["x"], "notes": ""}),
            "regen attempt 1",
            json.dumps({"score": 3.0, "gaps": ["x"], "notes": ""}),
            "regen attempt 2",
            json.dumps({"score": 3.0, "gaps": ["x"], "notes": ""}),
        ])
        result = review_and_repair(
            p, "x", "fastapi", gen, lambda s: s, threshold=7.0, max_rounds=2
        )
        assert result.score == 3.0  # never improved
