"""Tests for _gh_json in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from tests.scripts.rederive_deferral_variants import rederive


def test_single_page_array_is_returned(monkeypatch: pytest.MonkeyPatch) -> None:
    """A single-page response parses as one array."""
    monkeypatch.setattr(rederive, "_run_gh", lambda args: '[{"id": 1}, {"id": 2}]')
    assert rederive._gh_json(["api", "x"]) == [{"id": 1}, {"id": 2}]


def test_concatenated_pages_are_merged(monkeypatch: pytest.MonkeyPatch) -> None:
    """gh api --paginate emits one array per page; the arrays are concatenated."""
    monkeypatch.setattr(rederive, "_run_gh", lambda args: '[{"id": 1}]\n[{"id": 2}, {"id": 3}]')
    assert rederive._gh_json(["api", "--paginate", "x"]) == [{"id": 1}, {"id": 2}, {"id": 3}]


def test_empty_output_is_an_empty_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """Whitespace-only output yields an empty corpus page, not an error."""
    monkeypatch.setattr(rederive, "_run_gh", lambda args: "   ")
    assert rederive._gh_json(["api", "x"]) == []


def test_a_non_array_page_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """A JSON object (e.g. a 404 body) is not a valid page."""
    monkeypatch.setattr(rederive, "_run_gh", lambda args: '{"message": "Not Found"}')
    with pytest.raises(RuntimeError, match="expected a JSON array"):
        rederive._gh_json(["api", "x"])


def test_malformed_json_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unparseable output raises rather than silently truncating the corpus."""
    monkeypatch.setattr(rederive, "_run_gh", lambda args: "not json at all")
    with pytest.raises(RuntimeError, match="non-JSON"):
        rederive._gh_json(["api", "x"])
