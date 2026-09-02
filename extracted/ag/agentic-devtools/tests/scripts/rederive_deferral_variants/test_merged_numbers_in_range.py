"""Tests for merged_numbers_in_range in rederive_deferral_variants."""

from __future__ import annotations

import json
from collections.abc import Mapping

import pytest

from tests.scripts.rederive_deferral_variants import rederive


def _fake_gh(
    monkeypatch,
    highest: int,
    merged: list[int],
    merged_at: Mapping[int, str | None] | None = None,
) -> list[list[str]]:
    """Stub _run_gh with a repo whose highest PR is *highest*; record the calls."""
    calls: list[list[str]] = []

    def fake(args: list[str]) -> str:
        calls.append(args)
        if "--state" in args and args[args.index("--state") + 1] == "all":
            return json.dumps([{"number": highest}] if highest else [])
        limit = int(args[args.index("--limit") + 1])
        newest_first = sorted(merged, reverse=True)
        rows: list[dict] = []
        for n in newest_first[:limit]:
            row: dict = {"number": n}
            if merged_at is not None:
                row["mergedAt"] = merged_at.get(n)
            rows.append(row)
        return json.dumps(rows)

    monkeypatch.setattr(rederive, "_run_gh", fake)
    return calls


def test_returns_only_numbers_inside_the_range(monkeypatch: pytest.MonkeyPatch) -> None:
    """Numbers outside the requested window are dropped."""
    _fake_gh(monkeypatch, highest=60, merged=[10, 25, 30, 45, 60])
    assert rederive.merged_numbers_in_range("o/r", 25, 45) == [25, 30, 45]


def test_the_limit_covers_pull_requests_newer_than_the_range(monkeypatch: pytest.MonkeyPatch) -> None:
    """A range-sized limit would drop the oldest wanted PRs once newer ones exist."""
    merged = list(range(10, 61))
    calls = _fake_gh(monkeypatch, highest=60, merged=merged)

    assert rederive.merged_numbers_in_range("o/r", 10, 12) == [10, 11, 12]

    limit = int(calls[-1][calls[-1].index("--limit") + 1])
    assert limit >= len(merged)


def test_an_empty_repository_yields_no_numbers(monkeypatch: pytest.MonkeyPatch) -> None:
    """A repo with no pull requests still produces a valid (positive) limit."""
    calls = _fake_gh(monkeypatch, highest=0, merged=[])

    assert rederive.merged_numbers_in_range("o/r", 100, 200) == []

    assert int(calls[-1][calls[-1].index("--limit") + 1]) >= 1


def test_rejects_an_inverted_range(monkeypatch: pytest.MonkeyPatch) -> None:
    """An inverted range is a typo, not an empty result to be silently returned."""
    _fake_gh(monkeypatch, highest=60, merged=[10])
    with pytest.raises(ValueError, match="Empty pull request range"):
        rederive.merged_numbers_in_range("o/r", 50, 10)


def test_merged_before_excludes_pull_requests_merged_at_or_after_the_cutoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A number in range but merged after the freeze instant must not be included."""
    merged_at = {
        10: "2026-08-10T00:00:00Z",
        11: "2026-08-11T08:00:00Z",
        12: "2026-08-11T09:05:00Z",
        13: "2026-08-12T00:00:00Z",
    }
    _fake_gh(monkeypatch, highest=20, merged=[10, 11, 12, 13], merged_at=merged_at)
    assert rederive.merged_numbers_in_range("o/r", 10, 13, merged_before="2026-08-11T09:00:00Z") == [10, 11]


def test_merged_before_excludes_a_pull_request_with_no_merge_timestamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A merged PR the API reports without a timestamp cannot be proven in-window."""
    merged_at = {10: "2026-08-10T00:00:00Z", 11: None}
    _fake_gh(monkeypatch, highest=20, merged=[10, 11], merged_at=merged_at)
    assert rederive.merged_numbers_in_range("o/r", 10, 11, merged_before="2026-08-11T00:00:00Z") == [10]
