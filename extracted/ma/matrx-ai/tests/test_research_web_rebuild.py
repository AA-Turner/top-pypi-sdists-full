"""research_web rebuild — one test per numbered problem (research-tool-repair PROBLEMS.md 1-12, 16-21, 24).

The evidence run (2026-11-08): 4 queries at depth "deep", 71 results, 19 pages = 515,422 chars sent
to ONE condenser call, one off-topic page alone 146,889 chars, ~34,000 chars of image markup, an
/amp duplicate; the tail chopped at 400,000; the condenser refused for size, its reason thrown away;
"scraped content provided below" with none below; the stats never returned; listings before the
report, the whole cut at 45,000; success=True. ``_evidence_shaped_run`` rebuilds that SHAPE with
neutral invented content and drives the real ``research_web`` with the search, scrape and condenser
doubled at their seams.
"""

from __future__ import annotations

import asyncio
import json
import types
from typing import Any

import pytest
from matrx_scraper.features.research_budget import (
    NOT_READ_LABEL,
    Budgets,
    GroupPlan,
    PagePlan,
    canonical_url,
    clean_page_text,
    fit_group_budget,
    group_queries,
)

QUERIES = [
    "harbor bakery cooperative weekly metrics",
    "harbor bakery cooperative scorecard",
    "harbor bakery cooperative owner interviews",
    "site:harborbakery.example measure",
]
INSTRUCTIONS = "Find every rule the Harbor Bakery Cooperative gives about weekly metrics and scorecards, quoted."
IMAGE_LINE = "![a photo of bread](https://cdn.harborbakery.example/img/loaf-0001.jpg)\n"


def _on_topic(i: int | str, chars: int) -> str:
    sentence = (
        f"Rule {i}: the harbor bakery cooperative reviews its weekly metrics scorecard every Monday "
        "and each owner tracks three measures. "
    )
    body = (sentence * (chars // len(sentence) + 1))[:chars]
    return body + "\n" + IMAGE_LINE * 40


def _off_topic(chars: int) -> str:
    sentence = "Generic guide to spreadsheets for any company, unrelated advice about fonts and colours. "
    return (sentence * (chars // len(sentence) + 1))[:chars]


#: Extra characters on every search snippet (Brave's real snippets with extra_snippets run 600-1,500).
SNIPPET_PAD = 0


def _results(qi: int, n: int) -> dict[str, Any]:
    return {
        "web": {
            "results": [
                {
                    "title": f"Result {qi}-{r}",
                    "url": f"https://site{qi}.example/page-{r}",
                    "description": f"snippet about harbor bakery metrics {qi}-{r}" + " more words of snippet text" * (SNIPPET_PAD // 28),
                }
                for r in range(n)
            ]
        },
        "news": {"results": []},
    }


def _evidence_shaped_run(
    monkeypatch: pytest.MonkeyPatch,
    *,
    condenser: Any = None,
    depth: str = "deep",
    queries: list[str] | None = None,
    report_chars: int = 3_000,
    failures: list[dict[str, Any]] | None = None,
    knobs: dict[str, int] | None = None,
) -> tuple[Any, list[dict[str, Any]]]:
    """Run the real research_web on an evidence-shaped corpus; return (ToolResult, condenser calls)."""
    from matrx_ai import _ext
    from matrx_ai.agent_runners import research as research_runner
    from matrx_ai.agent_runners.research import AgentResult
    from matrx_ai.tools.implementations import web as web_impl
    from matrx_scraper.features import mcp_tool_helpers

    queries = queries or QUERIES
    search = {q: _results(i, 18 if i < 3 else 17) for i, q in enumerate(queries)}
    # The /amp copy of page 0 of query 0, and one huge off-topic page in query 1.
    search[queries[0]]["web"]["results"].insert(1, {"title": "Result amp", "url": "https://site0.example/page-0/amp/"})

    def _page(url: str, title: str, content: str) -> dict[str, Any]:
        return {"url": url, "requested_url": url, "title": title, "date_info": "", "content": content,
                "char_count": len(content), "is_good_scrape": len(content) >= 1000}

    async def fake_brave(*, query: str, **_: Any) -> dict[str, Any]:
        return search[query]

    seeded_failures = failures

    async def fake_scrape(*, search_result: dict[str, Any], failures: Any = None, **_: Any) -> list[dict[str, Any]]:
        if failures is not None and seeded_failures:
            failures.extend(seeded_failures)
        pages = []
        for r in search_result["web"]["results"][:5]:
            url = r["url"]
            if url == "https://site1.example/page-1":
                pages.append(_page(url, "Spreadsheet basics", _off_topic(146_889)))
            elif url.endswith("/amp/"):
                pages.append(_page(url, "Rules amp", _on_topic("https://site0.example/page-0", 24_000)))
            else:
                pages.append(_page(url, f"Harbor bakery cooperative weekly metrics {url[-7:]}", _on_topic(url, 24_000)))
        return pages

    calls: list[dict[str, Any]] = []

    async def default_condenser(**kw: Any) -> AgentResult:
        return AgentResult(success=True, output="R" * report_chars)

    async def recording(**kw: Any) -> Any:
        calls.append(kw)
        return await (condenser or default_condenser)(**kw)

    class _Stream:
        def __init__(self, *_: Any) -> None: ...
        async def progress(self, *_: Any, **__: Any) -> None: ...
        async def step(self, *_: Any, **__: Any) -> None: ...

    monkeypatch.setitem(_ext._registry, "brave_search", {"async_brave_search": fake_brave})
    monkeypatch.setattr(mcp_tool_helpers, "scrape_urls_from_search_result", fake_scrape)
    monkeypatch.setattr(research_runner, "scrape_research_condenser_agent_1", recording)
    monkeypatch.setattr(web_impl, "ToolStreamManager", _Stream)
    ctx = types.SimpleNamespace(emitter=None, call_id="call-1", organization_id=None)
    args = {"queries": queries, "instructions": INSTRUCTIONS, "research_depth": depth}
    if knobs is not None:
        async def _knobs(_org: Any) -> dict[str, int]:
            return knobs
        monkeypatch.setattr(web_impl, "_RESEARCH_BUDGETS_RESOLVER", _knobs)
    try:
        return asyncio.run(web_impl.research_web(args, ctx)), calls
    finally:
        if knobs is not None:
            monkeypatch.setattr(web_impl, "_RESEARCH_BUDGETS_RESOLVER", None)


#: Every report ends with the code-written sources block (fix round 1); the writer's own text is what precedes it.
SOURCES_BLOCK_MARK = "\n\n---\nSources read"


def _failing(reason: str) -> Any:
    from matrx_ai.agent_runners.research import AgentResult

    async def run(**_: Any) -> AgentResult:
        return AgentResult(success=False, error=reason)

    return run


# ── 1. keywords are condensed in groups of 2-3, one report each ─────────────────



def _body(report: dict[str, Any]) -> str:
    """The writer's text as it arrived: without the code-written citation notice (fix round 3) a filler report carries."""
    text = report["report"].split(SOURCES_BLOCK_MARK)[0]
    return text.split("\n\n", 1)[1] if (report.get("citations") or {}).get("read_pages_cited") == 0 else text

def test_1_four_queries_are_two_condensed_reports_of_two(monkeypatch: pytest.MonkeyPatch) -> None:
    table = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [3, 2, 2], 8: [3, 3, 2], 9: [3, 3, 3], 10: [3, 3, 2, 2]}
    for n, sizes in table.items():
        assert [len(g) for g in group_queries([f"q{i}" for i in range(n)])] == sizes, n
    result, calls = _evidence_shaped_run(monkeypatch)
    assert [c["queries"].count(",") + 1 for c in calls] == [2, 2]
    assert len(result.output["reports"]) == 2


def test_1_research_takes_up_to_ten_queries() -> None:
    from matrx_ai.tools.arg_models.web_args import WebResearchArgs

    assert len(WebResearchArgs(queries=[f"q{i}" for i in range(10)], instructions="x").queries) == 10


# ── 2 + 12. one page is capped, and the cap is marked for condenser and parent ──


def test_2_and_12_a_huge_page_is_capped_and_marked_for_condenser_and_parent(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_scraper.features.research_budget import build_listings, plan_groups

    pages = [
        {"url": "https://a.example/1", "title": "Spreadsheet basics", "content": _off_topic(146_889)},
        {"url": "https://a.example/2", "title": "Harbor bakery weekly metrics", "content": _on_topic(2, 9_000)},
    ]
    listings = build_listings([("harbor bakery weekly metrics", _results(0, 3))], {p["url"] for p in pages})
    groups, records = plan_groups(
        queries=["harbor bakery weekly metrics"], instructions=INSTRUCTIONS, listings=listings, pages=pages, budgets=Budgets()
    )
    assert "[Page capped: 20,000 of 146,889 characters kept]" in groups[0].scraped_content()
    huge = next(r.record() for r in records if r.title == "Spreadsheet basics")
    assert huge["capped"] is True and huge["chars_scraped"] == 146_889 and huge["chars_sent"] < 21_000
    assert "CAPPED" in groups[0].run_facts()
    # And through the tool: the parent's run.pages says which pages were capped.
    result, _ = _evidence_shaped_run(monkeypatch)
    assert any(p["capped"] for p in result.output["run"]["pages"])


# ── 3. a total budget bounds every condense ─────────────────────────────────────


def test_3_no_condense_exceeds_its_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    _, calls = _evidence_shaped_run(monkeypatch)
    budgets = Budgets()
    for call in calls:
        assert len(call["scraped_content"]) <= budgets.condense_max_chars
        assert len(call["search_results"]) <= budgets.listings_max_chars


# ── 4. the least relevant page ranks last ──────────────────────────────────────


def test_4_an_off_topic_page_ranks_below_on_topic_pages(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch)
    group_pages = [p for p in result.output["run"]["pages"] if p["group"] == 1 and not p.get("duplicate_of")]
    off = next(p for p in group_pages if p["title"] == "Spreadsheet basics")
    assert off["rank_in_group"] == max(p["rank_in_group"] for p in group_pages)


# ── 5. duplicates go once ──────────────────────────────────────────────────────


def test_5_the_amp_copy_and_the_listings_are_sent_once(monkeypatch: pytest.MonkeyPatch) -> None:
    assert canonical_url("https://www.site0.example/page-0/amp/?utm_source=x") == canonical_url("https://site0.example/page-0")
    result, calls = _evidence_shaped_run(monkeypatch)
    dupes = [p for p in result.output["run"]["pages"] if p.get("duplicate_of")]
    assert len(dupes) == 1
    for call in calls:
        assert "snippet about harbor bakery metrics" not in call["scraped_content"]
        assert call["search_results"].count("snippet about harbor bakery metrics 0-2") <= 1


# ── 6. image markup never reaches the condenser ────────────────────────────────


def test_6_image_markup_is_cleaned_out(monkeypatch: pytest.MonkeyPatch) -> None:
    assert clean_page_text("a\n" + IMAGE_LINE * 3 + "\n\n\n\nb") == "a\n\nb"
    _, calls = _evidence_shaped_run(monkeypatch)
    assert all("cdn.harborbakery.example/img" not in c["scraped_content"] for c in calls)


# ── 7. research_depth chooses page count; size is the budget's ─────────────────


def test_7_depth_sets_how_many_pages_not_how_big(monkeypatch: pytest.MonkeyPatch) -> None:
    shallow, s_calls = _evidence_shaped_run(monkeypatch, depth="shallow")
    deep, d_calls = _evidence_shaped_run(monkeypatch, depth="deep")
    sent = lambda r: sum(g["pages_sent"] for g in r.output["run"]["groups"])  # noqa: E731
    assert sent(shallow) < sent(deep)
    assert sent(shallow) <= 2 * len(QUERIES)
    assert max(len(c["scraped_content"]) for c in d_calls) <= Budgets().condense_max_chars


# ── 8 + 9. fitting is a declared cut order, never a tail chop ──────────────────


def _plan(url: str, score: float, chars: int) -> PagePlan:
    return PagePlan(url=url, title=url, group=1, query="q", search_rank=0, text="w" * chars, score=score, chars_clean=chars)


def test_8_the_condenser_runner_never_chops_the_tail(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agent_runners import research as research_runner
    from matrx_ai.agents.executor import AgentRunResult

    offered: list[Any] = []

    class _Offer:
        @classmethod
        def from_inputs(cls, _agent: Any, *, inputs: Any, **_: Any) -> Any:
            offered.append(inputs)
            return inputs

    class _Runner:
        async def run(self, *_: Any, **__: Any) -> Any:
            return types.SimpleNamespace(raw=AgentRunResult(success=True, output="report"))

    monkeypatch.setattr(research_runner, "Offer", _Offer)
    monkeypatch.setattr(research_runner, "get_mandate_runner", lambda: _Runner())
    monkeypatch.setattr(research_runner, "carried_principal", lambda: None)
    planned = "best page " * 50_000  # 500,000 chars: past the old 400,000 tail cut
    ctx = types.SimpleNamespace(call_id="c", tool_name="research_web", parent_agent_name=None)
    asyncio.run(research_runner.scrape_research_condenser_agent_1(
        instructions="i", scraped_content=planned, queries="q", search_results="s", ctx=ctx,
    ))
    assert offered[0].scraped_content == planned

    # The budget is met by the cut order instead: the best page survives even when it comes last.
    pages = [_plan("low", 0.1, 60_000), _plan("mid", 0.5, 60_000), _plan("best", 0.9, 60_000)]
    fit_group_budget(pages, 120_000, 2_000)
    assert pages[2].text == "w" * 60_000 and not pages[2].reduced
    assert sum(len(p.text) for p in pages) <= 120_000


def test_9_lowest_ranked_largest_first_each_to_its_floor_then_dropped() -> None:
    pages = [_plan("best", 0.9, 50_000), _plan("small-low", 0.1, 10_000), _plan("big-low", 0.1, 40_000), _plan("mid", 0.5, 40_000)]
    reductions = fit_group_budget(pages, 60_000, 2_000)
    assert [r["url"] for r in reductions] == ["big-low", "small-low", "mid"]
    assert pages[0].text == "w" * 50_000
    assert len(pages[1].text) <= 2_000 and len(pages[2].text) <= 2_000
    assert sum(len(p.text) for p in pages) <= 60_000
    # Past every floor, the lowest-ranked pages drop to listing-only first.
    pages = [_plan("best", 0.9, 3_000), _plan("low", 0.1, 3_000), _plan("mid", 0.5, 3_000)]
    reductions = fit_group_budget(pages, 4_100, 2_000)
    assert [p.dropped is not None for p in pages] == [False, True, False]
    assert sum(len(p.text) for p in pages if not p.dropped) <= 4_100
    # Through the tool: in every group, a page that lost text ranks below every page that kept all of it.


def test_9_through_the_tool_only_lower_ranked_pages_lose_text(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch)
    for group in result.output["run"]["groups"]:
        pages = [p for p in result.output["run"]["pages"] if p["group"] == group["group"] and not p.get("duplicate_of")]
        cut = [p["rank_in_group"] for p in pages if p["reduced"] or p.get("dropped")]
        whole = [p["rank_in_group"] for p in pages if not (p["reduced"] or p.get("dropped"))]
        assert cut and whole and min(cut) > max(whole)


# ── 10 + 11. reports are never cut; listings go first ──────────────────────────


def test_10_and_11_a_long_report_arrives_whole_and_listings_are_trimmed(monkeypatch: pytest.MonkeyPatch) -> None:
    # Full listings on request (knob listings_detail=2): the compact default is too small to need trimming.
    result, _ = _evidence_shaped_run(monkeypatch, report_chars=60_000, knobs={"listings_detail": 2})
    assert [len(_body(r)) for r in result.output["reports"]] == [60_000, 60_000]
    assert result.output["run"]["listings_trimmed"]["results_removed"] > 0
    assert result.output_self_capped is True


def test_11b_a_trimmed_result_with_its_note_stays_under_the_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    """The "listings were trimmed" note is part of the result it describes.

    Live, 2026-11-17: reports that fit, listings trimmed to the limit, then the note added on top:
    50,155 characters against the 50,000 limit, and the settled overflow class re-opened.
    """
    from matrx_ai.tools.models import tool_output_text
    from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS

    trimmed_runs = 0
    for report_chars in range(15_000, 24_001, 500):
        result, _ = _evidence_shaped_run(monkeypatch, report_chars=report_chars, knobs={"listings_detail": 2})
        size = len(tool_output_text(result.output)[0])
        if "listings_trimmed" not in result.output["run"]:
            assert size < TOOL_RESULT_SOFT_CAP_CHARS
            continue
        assert [len(_body(r)) for r in result.output["reports"]] == [report_chars, report_chars]
        kept = sum(len(e["results"]) for e in result.output["listings"])
        if not kept:
            continue  # run + reports alone pass the limit; they arrive whole by design (test 10/11)
        trimmed_runs += 1
        assert size < TOOL_RESULT_SOFT_CAP_CHARS, f"report_chars={report_chars}: {size:,} characters"
    assert trimmed_runs, "no run in the sweep kept some listings after trimming; the test proves nothing"


# ── 16 + 17. a failed condense says its real reason and delivers page text ─────


def test_16_the_condenser_failure_reason_is_kept(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agent_runners.research import _to_agent_result
    from matrx_ai.agents.executor import AgentRunResult

    assert _to_agent_result(AgentRunResult(success=False, error="input over the 200,000-token limit"), "c").error == (
        "input over the 200,000-token limit"
    )
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_failing("input over the 200,000-token limit"))
    assert all(g["reason"] == "input over the 200,000-token limit" for g in result.output["run"]["groups"])


def test_17_a_failed_group_carries_its_top_pages_and_promises_nothing_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch, condenser=_failing("refused"))
    text = json.dumps(result.output)
    assert "provided below" not in text
    for report in result.output["reports"]:
        assert report["status"] == "failed" and report["fallback_pages"]
        assert sum(len(p["text"]) for p in report["fallback_pages"]) <= Budgets().fallback_max_chars + 100
        assert "harbor bakery cooperative" in report["fallback_pages"][0]["text"]


# ── 18 + 19. the run facts are structured and always returned ──────────────────


def test_18_the_run_stats_are_returned(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch)
    timing = result.output["run"]["timing"]
    for key in ("urls_attempted", "urls_scraped", "good_scrapes", "thin_scrapes", "failed_scrapes"):
        assert key in timing
    assert result.output["run"]["results_per_query"][QUERIES[0]] == 19


def test_19_run_facts_survive_any_size_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    result, calls = _evidence_shaped_run(monkeypatch, report_chars=60_000)
    run = result.output["run"]
    assert isinstance(run, dict) and run["groups"] and run["pages"] and run["budgets"]
    assert all(c["scraped_content"].startswith("=== RUN FACTS") for c in calls)


# ── 20. success is honest ──────────────────────────────────────────────────────


def test_20_success_partial_and_failure_are_honest(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agent_runners.research import AgentResult

    seen = {"n": 0}

    async def one_fails(**_: Any) -> AgentResult:
        seen["n"] += 1
        return AgentResult(success=seen["n"] == 1, output="report" if seen["n"] == 1 else "", error=None if seen["n"] == 1 else "refused")

    ok, _ = _evidence_shaped_run(monkeypatch)
    assert ok.success and ok.output["run"]["status"] == "success" and not ok.output["run"]["partial"]
    partial, _ = _evidence_shaped_run(monkeypatch, condenser=one_fails)
    assert partial.success and partial.output["run"]["partial"] is True

    from matrx_ai.tools.implementations.web import research_output

    group = GroupPlan(index=1, queries=["q"])
    output, _, outcome = research_output(
        queries=["q"], research_depth="deep", groups=[group], page_plans=[], outcomes=[AgentResult(success=False, error="refused")],
        listings=[], read_failures=[], budgets=Budgets(), timing={}, result_limit=50_000,
    )
    assert outcome == "failed" and output["reports"][0]["reason"] == "refused"


# ── 21. every page names how to reach its full text ────────────────────────────


def test_21_every_page_names_how_to_read_it_in_full(monkeypatch: pytest.MonkeyPatch) -> None:
    result, _ = _evidence_shaped_run(monkeypatch)
    for page in result.output["run"]["pages"]:
        assert page["full_text"] == f"web action='read' urls=['{page['url']}']"


# ── 24. a snippet is labelled as a snippet ─────────────────────────────────────


def test_24_unread_listings_say_snippet_only(monkeypatch: pytest.MonkeyPatch) -> None:
    result, calls = _evidence_shaped_run(monkeypatch)
    rows = [r for e in result.output["listings"] for r in e["results"]]
    read_urls = {canonical_url(p["url"]) for p in result.output["run"]["pages"]}
    for row in rows:
        assert row["read"] == ("read in full" if canonical_url(row["url"]) in read_urls else NOT_READ_LABEL)
    assert any(r["read"] == NOT_READ_LABEL for r in rows)
    assert NOT_READ_LABEL in calls[0]["search_results"]


# ── 25. the result fits its DECLARED output contract ───────────────────────────


def test_25_every_outcome_fits_the_declared_output_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    """The stored tool.definition.output_schema said ``string`` after the rebuild made the result
    ``{run, reports, listings}``, so every successful call filed a ToolOutputContractDrift
    (2026-11-17). The live row is written from RESEARCH_WEB_OUTPUT_SCHEMA; every outcome must fit it,
    and the old string declaration must not (the check can fail)."""
    from matrx_ai.agent_runners.research import AgentResult
    from matrx_ai.tools.implementations.web import RESEARCH_WEB_OUTPUT_SCHEMA, research_output
    from matrx_graph.contract_kinds import check_schema

    seen = {"n": 0}

    async def one_fails(**_: Any) -> AgentResult:
        seen["n"] += 1
        return AgentResult(success=seen["n"] == 1, output="report" if seen["n"] == 1 else "", error=None if seen["n"] == 1 else "refused")

    ok, _ = _evidence_shaped_run(monkeypatch)
    partial, _ = _evidence_shaped_run(monkeypatch, condenser=one_fails)
    trimmed, _ = _evidence_shaped_run(monkeypatch, report_chars=60_000)
    failed, _, _ = research_output(
        queries=["q"], research_depth="deep", groups=[GroupPlan(index=1, queries=["q"])], page_plans=[],
        outcomes=[AgentResult(success=False, error="refused")], listings=[], read_failures=[],
        budgets=Budgets(), timing={}, result_limit=50_000,
    )
    for output in (ok.output, partial.output, trimmed.output, failed):
        wire = json.loads(json.dumps(output))
        verdict = check_schema(wire, RESEARCH_WEB_OUTPUT_SCHEMA)
        assert verdict.checked and not verdict.errors, verdict.errors

    stale = check_schema(json.loads(json.dumps(ok.output)), {"type": "string"})
    assert stale.checked and stale.errors
