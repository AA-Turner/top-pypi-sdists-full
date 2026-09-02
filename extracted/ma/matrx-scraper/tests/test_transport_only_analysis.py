"""A URL that never produced a snapshot is still audited for transport.

The sweep's evidence used to be *only* the latest accepted `web.snapshot`, so a
URL that 404s, 500s, times out, or loops through redirects — the URLs most
likely to HAVE a transport defect — produced no snapshot and was dropped from
the analysis entirely. `broken_page_4xx`, `server_error_5xx`, `redirect_chain`,
and `redirect_loop` could therefore never fire for the pages they exist for.

`web.crawl_url` already carried the evidence (`http_status` +
`metadata.redirect_chain`, written at insert by
`persistence.crawl_url_fetch_metadata`); nothing read it. These tests pin the
two halves of the fix:

1. the crawl_url record becomes `PageFacts` with the transport evidence intact,
2. running the REAL check registry over those facts produces the right verdicts
   — and every content check answers `n_a`, never a pass on nothing.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from matrx_scraper.web_crawl.analysis import (
    CROSS_PAGE_CHECKS,
    PAGE_CHECKS,
    SiteAggregates,
    _crawl_url_recency,
    _extract_transport_facts,
)
from matrx_scraper.web_crawl.persistence import crawl_url_fetch_metadata

# Checks whose answer is genuinely knowable from transport evidence alone.
TRANSPORT_CHECKS = frozenset(
    {
        "broken_page_4xx",
        "server_error_5xx",
        "redirect_chain",
        "redirect_loop",
        # Both read hop statuses / the response status only. A URL that answers
        # 404 is, by definition, NOT a soft 404 — no content needed to say so.
        "temporary_redirect_usage",
        "soft_404_detection",
    }
)
# A check whose "no evidence" state is a real pass, not an unknown — mirrors
# `test_seo_checks_single_source._CLEAN_ON_ABSENCE`.
CLEAN_ON_ABSENCE = frozenset({"meta_robots_conflicts", "mixed_content"})
# Checks that grade the URL STRING and nothing else. These are not exempt
# because "absence is clean" — they have their full evidence: `web.page.url` is
# known for every URL the crawler attempted, snapshot or not, and
# `_extract_transport_facts` carries it onto `PageFacts.url`. A 404 whose URL is
# short, lowercase and parameter-free genuinely HAS a well-designed URL, and the
# live `web.analysis_item` row agrees — its sources are `web.page.url / path.`
# with no capture gaps. Nothing here can be fabricated from missing content, so
# a pass is honest; the sibling pin `test_seo_checks_single_source` exempts the
# same key for the same reason.
URL_ONLY_CHECKS = frozenset({"url_design_quality"})
# Cross-page checks need the site aggregates, not page evidence.
# Derived, never hand-listed: a new cross-page check must not silently start
# failing this pin (nor be silently exempted from it) because someone forgot to
# edit a copy of the registry.
CROSS_PAGE = frozenset(CROSS_PAGE_CHECKS)


def page(page_id: str = "p1", url: str = "https://example.com/gone") -> SimpleNamespace:
    return SimpleNamespace(id=page_id, url=url)


def crawl_url(
    *,
    http_status: int | None,
    redirect_chain: list[dict] | None = None,
    completed_at: datetime | None = None,
    sequence: int = 1,
) -> dict:
    """A `web.crawl_url` row as the analysis loader reads it — a `.values()`
    projection dict, not a hydrated model (the loader stopped hydrating 176k-
    row ledgers, 2026-08-12).

    `metadata` goes through the REAL producer so a change to the hop shape
    breaks this test instead of silently changing what analysis reads.
    """
    return {
        "http_status": http_status,
        "metadata": crawl_url_fetch_metadata(redirect_chain),
        "completed_at": completed_at,
        "discovered_at": datetime(2026, 8, 9, tzinfo=UTC),
        "sequence": sequence,
    }


def verdicts(facts) -> dict[str, str]:
    return {key: check(facts, SiteAggregates()).status for key, check in PAGE_CHECKS.items()}


def assert_content_checks_are_never_a_pass(statuses: dict[str, str]) -> None:
    """No content evidence was captured — nothing may claim the page is fine."""
    for key, status in statuses.items():
        if (
            key in TRANSPORT_CHECKS
            or key in CLEAN_ON_ABSENCE
            or key in CROSS_PAGE
            or key in URL_ONLY_CHECKS
        ):
            continue
        assert status != "pass", f"{key} passed a page whose content was never captured"


def test_snapshotless_404_is_analyzed_and_fails_the_right_check():
    facts = _extract_transport_facts(
        page(),
        crawl_url(
            http_status=404,
            redirect_chain=[{"status": 404, "url": "https://example.com/gone"}],
        ),
    )
    assert facts.page_id == "p1"
    assert facts.http_status == 404
    # No snapshot: the content half of the evidence is genuinely unknown.
    assert facts.latest_snapshot_id == ""
    assert facts.title is None and facts.word_count is None

    statuses = verdicts(facts)
    assert statuses["broken_page_4xx"] == "fail"
    assert statuses["server_error_5xx"] == "pass"  # 404 is not a server error
    assert statuses["redirect_chain"] == "pass"
    assert statuses["redirect_loop"] == "pass"
    # The checks that CAN say "not measured" must say exactly that.
    assert statuses["thin_content"] == "n_a"
    assert statuses["title_length"] == "n_a"
    assert statuses["meta_description_length"] == "n_a"
    assert statuses["h1_presence"] == "n_a"
    assert statuses["image_alt_presence"] == "n_a"
    assert statuses["page_weight"] == "n_a"
    assert statuses["ttfb_server_response"] == "n_a"
    assert statuses["duplicate_content_exact"] == "n_a"
    assert_content_checks_are_never_a_pass(statuses)


def test_snapshotless_redirect_loop_is_analyzed_and_fails_the_right_check():
    facts = _extract_transport_facts(
        page(url="https://example.com/loop"),
        crawl_url(
            http_status=None,  # a loop never terminates in a real response
            redirect_chain=[
                {"status": 301, "url": "https://example.com/loop"},
                {"status": 301, "url": "https://example.com/loop-b"},
                {"status": 301, "url": "https://example.com/loop"},
            ],
        ),
    )
    assert [hop["url"] for hop in facts.redirect_chain] == [
        "https://example.com/loop",
        "https://example.com/loop-b",
        "https://example.com/loop",
    ]

    statuses = verdicts(facts)
    assert statuses["redirect_loop"] == "fail"
    # No terminal status was ever observed — the status checks must not guess.
    assert statuses["broken_page_4xx"] == "n_a"
    assert statuses["server_error_5xx"] == "n_a"
    assert_content_checks_are_never_a_pass(statuses)


def test_snapshotless_5xx_and_no_response_reach_the_server_error_check():
    for status in (503, 0):
        facts = _extract_transport_facts(page(), crawl_url(http_status=status))
        statuses = verdicts(facts)
        assert statuses["server_error_5xx"] == "fail", status
        assert_content_checks_are_never_a_pass(statuses)


def test_every_check_stays_db_valid_on_transport_only_evidence():
    """status/score pairing must satisfy `analysis_result_status_score_valid`."""
    facts = _extract_transport_facts(page(), crawl_url(http_status=404))
    for key, check in PAGE_CHECKS.items():
        outcome = check(facts, SiteAggregates())
        assert outcome.status in ("pass", "warn", "fail", "n_a"), key
        if outcome.status in ("pass", "warn", "fail"):
            assert outcome.score is not None and 1 <= outcome.score <= 100, key
        else:
            assert outcome.score is None, key
        assert outcome.reasoning, key


def test_a_crawl_url_with_no_hop_chain_is_not_a_fabricated_pass():
    """A pre-2026-08-08 row has no chain — that is unknown, not "no redirect"."""
    row = crawl_url(http_status=404)
    row["metadata"] = {}  # capability marker absent entirely
    facts = _extract_transport_facts(page(), row)
    assert facts.redirect_chain == []
    assert verdicts(facts)["broken_page_4xx"] == "fail"


@pytest.mark.parametrize(
    ("older", "newer"),
    [
        # A completed attempt beats one that never completed.
        (
            crawl_url(http_status=None, sequence=9),
            crawl_url(http_status=404, completed_at=datetime(2026, 8, 9, 1, tzinfo=UTC)),
        ),
        # Same completion instant → the later session sequence wins.
        (
            crawl_url(
                http_status=500, completed_at=datetime(2026, 8, 9, 1, tzinfo=UTC), sequence=1
            ),
            crawl_url(
                http_status=404, completed_at=datetime(2026, 8, 9, 1, tzinfo=UTC), sequence=2
            ),
        ),
    ],
)
def test_newest_attempt_wins(older, newer):
    assert _crawl_url_recency(newer) > _crawl_url_recency(older)
