"""research_web reports are checked against the pages the run actually read (lane D, 2026-11-17).

Reported live: a report cited "Reddit and forum benchmarks" although every Reddit page failed to load; two
reports of one call cited in two styles ("[Page N]" and "[cite: N]"). The condenser is an LLM, so the
rule is enforced in code on its output: every citation is rewritten to an inline URL and checked against
the run's read pages; a citation of a page that was not read does not survive; a source written by the
vendor of the product discussed is labelled as such; every report ends with a code-written block of the
sources read and the sources that failed to load. Prose is never judged (fix round 1: keyword deletion of
sentences was removed).
"""

from __future__ import annotations

import re
from typing import Any

import pytest
from matrx_scraper.features.research_budget import PagePlan, page_marker, verify_report
from test_research_web_rebuild import _evidence_shaped_run

REDDIT_FAILURE = {"url": "https://www.reddit.com/r/bakery/comments/1/metrics/", "verdict": {"reason": "challenge"}}


def _condenser_citing(*lines: str):
    from matrx_ai.agent_runners.research import AgentResult

    async def run(**_: Any) -> AgentResult:
        return AgentResult(success=True, output="\n".join(lines))

    return run


def _urls_read(call: dict[str, Any]) -> dict[int, str]:
    return {int(n): u for n, u in re.findall(r"\u27e6P(\d+)\u27e7\nTitle: .*\nUrl: (\S+)", call["scraped_content"])}


def test_a_citation_of_an_unread_page_does_not_survive(monkeypatch: pytest.MonkeyPatch) -> None:
    condenser = _condenser_citing(
        "Owners review the scorecard every Monday \u27e6P1\u27e7.",
        "Three measures are tracked [cite: 2, 3].",
        "Throughput doubled \u27e6P99\u27e7.",
    )
    result, calls = _evidence_shaped_run(monkeypatch, condenser=condenser)
    report = result.output["reports"][0]["report"]
    read = _urls_read(calls[0])
    assert read[1] in report
    assert "\u27e6" not in report and "[cite" not in report
    assert "page 99 was not read" in report
    assert result.output["run"]["groups"][0]["citation_check"]["removed_citations"][0]["cited"] == "99"


def test_every_report_of_a_call_uses_inline_url_citations(monkeypatch: pytest.MonkeyPatch) -> None:
    result, calls = _evidence_shaped_run(
        monkeypatch, condenser=_condenser_citing("A rule \u27e6P1\u27e7.", "Another rule [cite: 2].", "A third [Page 1, 2].")
    )
    for report in result.output["reports"]:
        text = report["report"]
        assert not re.search(r"\u27e6|\[(?:page|cite)", text, re.I)
        assert len(re.findall(r"https://site\d\.example/page-\d", text)) >= 3


def test_a_plain_url_citation_of_an_unread_page_is_removed() -> None:
    page = PagePlan(url="https://a.example/1", title="t", group=1, query="q", search_rank=1, text="body", rank=1)
    text, check = verify_report(
        "Fact one (https://a.example/1). Fact two (https://never-read.example/x).",
        read_pages=[page], terms_text="q",
    )
    assert "(https://a.example/1)" in text and "https://never-read.example/x" not in text
    assert check["removed_citations"][0]["cited"] == "https://never-read.example/x"


def test_a_vendor_written_source_is_labelled() -> None:
    vendor = PagePlan(url="https://harborbakery.example/metrics", title="t", group=1, query="q", search_rank=1, text="b", rank=1)
    other = PagePlan(url="https://news.example/story", title="t", group=1, query="q", search_rank=2, text="b", rank=2)
    text, check = verify_report(
        "It is the fastest \u27e6P1\u27e7. A reviewer agrees \u27e6P2\u27e7.",
        read_pages=[vendor, other], terms_text="Harborbakery benchmark results",
    )
    assert "(https://harborbakery.example/metrics, vendor-authored)" in text
    assert "(https://news.example/story)" in text
    assert check["vendor_sources"] == ["https://harborbakery.example/metrics"]


# ── fix round 2 (2026-11-17): only the code-labelled marker (and two legacy spellings) is a citation ──────


def _page(url: str, rank: int) -> PagePlan:
    return PagePlan(url=url, title="t", group=1, query="q", search_rank=rank, text="body", rank=rank)


#: Ordinary text that round 1's guessing rewrote or annotated. Every one must pass through byte-identical.
ORDINARY = [
    "The room is 20 m^2 wide.", "Energy is E=mc^2 for a rest mass.", "The fit gave r^2 of 0.9.", "About 10^6 users signed up.",
    "Read array[1] before arr[2].", 'The quoted changelog says "fixed [2] crashes" in v3.', "See (Page 1) of the contract.",
    "As Section [5] states.", "The 3^rd edition and [3.1] stay.", "Chapter two has page one of five, (Source: 1).",
    "Footnote^1 and [^1] are plain text here.", "Items [1] and [1-3] and [Page One] are plain.", "[Source 3] and [Pg. 1] and [cite 2] too.",
]


@pytest.mark.parametrize("text", ORDINARY)
def test_ordinary_text_passes_through_byte_identical(text: str) -> None:
    out, check = verify_report(text, read_pages=[_page("https://a.example/1", 1), _page("https://a.example/2", 2)], terms_text="q")
    assert out == text
    assert check["removed_citations"] == [] and check["cited"] == []


def test_the_marker_and_the_two_legacy_spellings_resolve() -> None:
    pages = [_page("https://a.example/1", 1), _page("https://a.example/2", 2), _page("https://a.example/3", 3)]
    out, check = verify_report(
        "A \u27e6P1\u27e7. B [Page 2]. C [cite: 3]. D [Page 1, 3]. E [cite: 2,3]. F \u27e6P1\u27e7\u27e6P2\u27e7.",
        read_pages=pages, terms_text="q",
    )
    assert out == ("A (https://a.example/1). B (https://a.example/2). C (https://a.example/3). "
                   "D (https://a.example/1; https://a.example/3). E (https://a.example/2; https://a.example/3). "
                   "F (https://a.example/1; https://a.example/2).")
    assert len(check["cited"]) == 3


def test_a_marker_of_a_page_not_read_is_removed_with_a_visible_note() -> None:
    out, check = verify_report("Fact \u27e6P7\u27e7, also [Page 8], [cite: 9].", read_pages=[_page("https://a.example/1", 1)], terms_text="q")
    assert out == ("Fact [citation removed: page 7 was not read in this run], also [citation removed: page 8 was not read in this run], "
                   "[citation removed: page 9 was not read in this run].")
    assert [r["cited"] for r in check["removed_citations"]] == ["7", "8", "9"]


def test_mixed_report_before_and_after(capsys: pytest.CaptureFixture[str]) -> None:
    before = ("The studio is 20 m^2 and E=mc^2 holds \u27e6P1\u27e7. Changelog: \"fixed [2] crashes\" [Page 2]. "
              "See (Page 1) of the contract, array[1], Section [5]. Reddit says otherwise \u27e6P9\u27e7.")
    out, _ = verify_report(before, read_pages=[_page("https://a.example/1", 1), _page("https://a.example/2", 2)], terms_text="q")
    with capsys.disabled():
        print("\nBEFORE:", before, "\nAFTER: ", out)
    assert out == ("The studio is 20 m^2 and E=mc^2 holds (https://a.example/1). Changelog: \"fixed [2] crashes\" (https://a.example/2). "
                   "See (Page 1) of the contract, array[1], Section [5]. Reddit says otherwise "
                   "[citation removed: page 9 was not read in this run].")


def test_pages_are_labelled_by_code_with_the_marker() -> None:
    from matrx_scraper.features.research_budget import GroupPlan

    group = GroupPlan(index=1, queries=["q"], pages=[_page("https://a.example/1", 1)])
    sent = group.scraped_content()
    assert f"{page_marker(1)}\nTitle: t\nUrl: https://a.example/1" in sent
    assert "[Page 1]" not in sent  # the citation instruction lives in the condenser agents' definitions, never in code


def test_the_writer_is_told_which_sources_failed_in_its_own_input() -> None:
    from matrx_scraper.features.research_budget import GroupPlan

    group = GroupPlan(index=1, queries=["q"], pages=[_page("https://a.example/1", 1)],
                      failed_sources=[("https://www.reddit.com/r/x/", "challenge")])
    sent = group.scraped_content()
    assert "FAILED TO LOAD" in sent and "https://www.reddit.com/r/x/" in sent
    assert "Nothing may be attributed" in sent
    assert "FAILED TO LOAD" not in GroupPlan(index=1, queries=["q"]).scraped_content()


def test_prose_is_never_deleted_for_what_it_says() -> None:
    sentences = [
        "Users on r/bakery say weekly is best.",
        "Reddit and forum benchmarks show weekly is best.",
        "Reddit was unavailable, so no benchmark from there is included.",
    ]
    text, _ = verify_report(" ".join(sentences), read_pages=[_page("https://a.example/1", 1)], terms_text="q")
    assert text == " ".join(sentences)


def test_a_markdown_link_to_an_unread_page_reads_cleanly() -> None:
    text, _ = verify_report(
        "See [the thread](https://never.example/x) and [this](https://a.example/1).",
        read_pages=[_page("https://a.example/1", 1)], terms_text="q",
    )
    assert "the thread [citation removed: never.example was not read in this run]" in text
    assert "[this](https://a.example/1)" in text


# ── the sources block: once per tool result, on every path that returns anything ────────────────────────


def test_the_failed_list_is_stated_once_per_tool_result(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_condenser_citing("Owners review weekly \u27e6P1\u27e7."), failures=[REDDIT_FAILURE])
    assert len(result.output["reports"]) >= 2
    sources = result.output["sources"]
    assert "Sources read (" in sources and "Sources that failed to load (1):" in sources and "reddit.com/r/bakery" in sources
    for report in result.output["reports"]:
        assert "Sources that failed to load" not in report["report"]
    import json

    assert json.dumps(result.output).count("Sources that failed to load") == 1


def test_a_failed_condenser_with_fallback_pages_still_carries_the_sources_block(monkeypatch: pytest.MonkeyPatch) -> None:
    from test_research_web_rebuild import _failing

    result, _ = _evidence_shaped_run(monkeypatch, condenser=_failing("writer down"), failures=[REDDIT_FAILURE])
    assert result.success and any(r.get("fallback_pages") for r in result.output["reports"])
    assert all(r["status"] == "failed" for r in result.output["reports"])
    sources = result.output["sources"]
    assert "Sources read (" in sources and "- https://site" in sources
    assert "Sources that failed to load (1):" in sources and "reddit.com/r/bakery" in sources


def test_a_zero_evidence_run_says_what_failed(monkeypatch: pytest.MonkeyPatch) -> None:
    import asyncio
    import types

    from matrx_ai import _ext
    from matrx_ai.tools.implementations import web as web_impl
    from matrx_scraper.features import mcp_tool_helpers

    async def fake_brave(*, query: str, **_: Any) -> dict[str, Any]:
        return {"web": {"results": []}}

    async def fake_scrape(*, failures: Any = None, **_: Any) -> list[dict[str, Any]]:
        if failures is not None:
            failures.append(REDDIT_FAILURE)
        return []

    class _Stream:
        def __init__(self, *_: Any) -> None: ...
        async def progress(self, *_: Any, **__: Any) -> None: ...
        async def step(self, *_: Any, **__: Any) -> None: ...

    monkeypatch.setitem(_ext._registry, "brave_search", {"async_brave_search": fake_brave})
    monkeypatch.setattr(mcp_tool_helpers, "scrape_urls_from_search_result", fake_scrape)
    monkeypatch.setattr(web_impl, "ToolStreamManager", _Stream)
    ctx = types.SimpleNamespace(emitter=None, call_id="call-1", organization_id=None)
    result = asyncio.run(web_impl.research_web({"queries": ["bakery metrics"], "instructions": "x" * 30}, ctx))
    assert not result.success
    message = result.error.message
    assert "zero evidence" in message and "no usable search results" in message
    assert "Sources read (0):" in message and "Sources that failed to load (0):" in message
    # When pages did fail to load on the way to zero evidence, the same text names each with its reason.
    assert "Sources that failed to load (1):" in web_impl._sources_text([REDDIT_FAILURE]) and "reddit.com/r/bakery" in web_impl._sources_text([REDDIT_FAILURE])


# ── fix round 3 (2026-11-17): an uncited report says so; adjacent citations merge; quoted legacy forms stay ─────


def test_an_uncited_report_says_so_at_its_top_and_in_a_field(monkeypatch: pytest.MonkeyPatch) -> None:
    prose = ("Owners review the scorecard every Monday.", "", "Three measures are tracked across stores.")
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_condenser_citing(*prose))
    entry = result.output["reports"][0]
    assert entry["report"].startswith("[Uncited report:")
    assert "Owners review the scorecard every Monday." in entry["report"]  # prose is never deleted
    assert entry["citations"]["read_pages_cited"] == 0 and entry["citations"]["pages_read"] >= 1


def test_a_partly_cited_report_carries_no_notice_and_counts_distinct_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    lines = ("# Findings", "", "Owners review the scorecard \u27e6P1\u27e7.", "", "Nobody knows why.", "",
             "- one measure [cite: 2]", "- another measure")
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_condenser_citing(*lines))
    entry = result.output["reports"][0]
    assert entry["citations"]["read_pages_cited"] == 2 and entry["citations"]["pages_read"] >= 2
    assert set(entry["citations"]) == {"read_pages_cited", "pages_read"}
    assert not entry["report"].startswith("[")  # prose is never judged: no "partly cited" line


def test_a_fully_cited_report_carries_no_notice(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_condenser_citing("A rule \u27e6P1\u27e7.", "", "Another [cite: 2]."))
    entry = result.output["reports"][0]
    assert not entry["report"].startswith("[") and entry["citations"]["read_pages_cited"] == 2


def test_a_repeated_marker_is_one_citation() -> None:
    pages = [_page("https://a.example/1", 1), _page("https://a.example/2", 2)]
    out, _ = verify_report("A \u27e6P1\u27e7\u27e6P1\u27e7\u27e6P1\u27e7. B \u27e6P1\u27e7 \u27e6P2\u27e7 \u27e6P1\u27e7.", read_pages=pages, terms_text="q")
    assert out == "A (https://a.example/1). B (https://a.example/1; https://a.example/2)."


def test_a_leading_zero_is_never_read_as_a_page() -> None:
    pages = [_page("https://a.example/1", 1), _page("https://a.example/7", 7)]
    out, check = verify_report("A \u27e6P01\u27e7. See [Page 007] and [cite: 07].", read_pages=pages, terms_text="q")
    assert out == "A [citation removed: page 01 was not read in this run]. See [Page 007] and [cite: 07]."
    assert check["cited"] == []


def test_a_legacy_form_inside_quoted_page_text_is_left_as_written() -> None:
    pages = [_page("https://a.example/1", 1), _page("https://a.example/2", 2)]
    text = ('The manual says "see [Page 2] for wiring" [Page 1].\n> Step 4 [Page 2] torque values\n'
            "Code `x [cite: 2]` here, and \u201cthe guide [Page 2]\u201d \u27e6P2\u27e7.")
    out, _ = verify_report(text, read_pages=pages, terms_text="q")
    assert out == ('The manual says "see [Page 2] for wiring" (https://a.example/1).\n> Step 4 [Page 2] torque values\n'
                   "Code `x [cite: 2]` here, and \u201cthe guide [Page 2]\u201d (https://a.example/2).")
