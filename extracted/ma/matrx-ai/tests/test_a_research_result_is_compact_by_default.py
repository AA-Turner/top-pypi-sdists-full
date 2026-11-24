"""research_web's default result is compact (lane D, 2026-11-17).

Reported live: one 4-query call returned about 50,000 characters even after trimming, a good share of it
search-listing snippets and per-page character counts. Now: listings carry rank, title, link and the
read label only; per-page character counts and the per-cut ledger are off; both come back on request
through the organization knobs ``agents.research_web`` ``listings_detail`` (2 = full) and
``page_char_counts`` (1).
"""

from __future__ import annotations

import json

import pytest
import test_research_web_rebuild as harness
from matrx_ai.tools.implementations.web import tool_output_text
from test_research_web_rebuild import _evidence_shaped_run


def _size(result) -> int:
    return len(tool_output_text(result.output)[0])


def test_default_listings_are_compact_and_counts_are_off(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, report_chars=6_000)
    rows = [r for e in result.output["listings"] for r in e["results"]]
    assert rows and all(set(r) == {"rank", "title", "url", "read"} for r in rows)
    for page in result.output["run"]["pages"]:
        assert not any(k.startswith("chars_") for k in page)
        assert "capped" in page and "reduced" in page and page["full_text"]
    for group in result.output["run"]["groups"]:
        assert "chars_sent" not in group and "reductions" not in group


def test_full_detail_comes_back_on_request(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, report_chars=6_000, knobs={"listings_detail": 2, "page_char_counts": 1})
    rows = [r for e in result.output["listings"] for r in e["results"]]
    assert all("snippet" in r for r in rows)
    assert all("chars_scraped" in p and "chars_sent" in p for p in result.output["run"]["pages"])
    assert all("chars_sent" in g for g in result.output["run"]["groups"])


def test_listings_can_be_turned_off(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, knobs={"listings_detail": 0})
    assert result.output["listings"] == []
    assert result.output["run"]["listings_detail"] == "none"


def test_the_compact_default_is_much_smaller_than_full(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(harness, "SNIPPET_PAD", 700)
    compact, _ = _evidence_shaped_run(monkeypatch, report_chars=6_000)
    full, _ = _evidence_shaped_run(monkeypatch, report_chars=6_000, knobs={"listings_detail": 2, "page_char_counts": 1})
    # Full detail is what the result carried before this change (listings with snippets, every count).
    assert _size(compact) < 0.6 * _size(full)
    assert json.loads(json.dumps(compact.output))["run"]["status"] == "success"
