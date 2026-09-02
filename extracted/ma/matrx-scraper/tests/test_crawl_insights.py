"""Derived crawl reads — clusters, link graph, progress series (no DB).

These pin the three things the legacy crawler's read layer did and the
canonical one did not: cluster shaping, graph capping, and a progress series
derived from the event ledger. The load_* functions are thin RLS-bound DB
reads around these algorithms, so the algorithms are what gets proven here.

The cap assertions are the point. Every one of these shapes is capped, and a
cap that is not reported is a lie about the site — `web.link_edge` holds
~610k rows, so "1,000 nodes" must never be presentable as "the whole graph".
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from matrx_scraper.web_crawl.analysis import (
    PageFacts,
    SiteAggregates,
    _check_duplicate_content_exact,
)
from matrx_scraper.web_crawl.contracts import DuplicatePage, LinkGraphNode, ProgressPoint
from matrx_scraper.web_crawl.insights import (
    _fingerprint_key,
    build_duplicate_clusters,
    build_progress_series,
    rank_and_cap_nodes,
)

# ---------------------------------------------------------------------------
# Duplicate-content clusters


def page(n: int, *, title: str | None = None, words: int | None = 100) -> DuplicatePage:
    return DuplicatePage(
        page_id=f"p{n}", url=f"https://example.com/{n}", title=title, word_count=words
    )


def test_clusters_need_two_pages():
    rows = [
        ((1, "aaa"), page(1)),
        ((1, "aaa"), page(2)),
        ((1, "bbb"), page(3)),
    ]
    report = build_duplicate_clusters(rows, site_id="s1")
    assert report.clusters_total == 1
    assert report.clusters[0].exact_sha256 == "aaa"
    assert report.clusters[0].page_count == 2
    assert report.duplicate_pages_total == 2
    assert report.pages_compared == 3


def test_fingerprint_version_is_part_of_cluster_identity():
    """Two extractor generations produce non-comparable hashes — a collision
    across versions must never merge into one cluster."""
    rows = [((1, "aaa"), page(1)), ((2, "aaa"), page(2))]
    report = build_duplicate_clusters(rows, site_id="s1")
    assert report.clusters_total == 0


def test_pages_without_a_fingerprint_are_counted_not_dropped_silently():
    rows = [(None, page(1)), (None, page(2)), ((1, "aaa"), page(3)), ((1, "aaa"), page(4))]
    report = build_duplicate_clusters(rows, site_id="s1")
    assert report.pages_without_fingerprint == 2
    assert report.clusters_total == 1


def test_cluster_caps_report_what_they_dropped():
    rows = [((1, f"h{i}"), page(n)) for i in range(5) for n in (i * 10, i * 10 + 1)]
    rows += [((1, "big"), page(500 + n)) for n in range(10)]
    report = build_duplicate_clusters(rows, site_id="s1", max_clusters=2, max_pages_per_cluster=3)
    assert report.clusters_total == 6
    assert report.clusters_returned == 2
    assert report.clusters_omitted == 4
    big = report.clusters[0]
    assert big.exact_sha256 == "big"  # largest cluster first
    assert big.page_count == 10
    assert len(big.pages) == 3
    assert big.pages_omitted == 7


def test_cluster_ordering_is_stable_across_calls():
    rows = [((1, h), page(n)) for h in ("b", "a", "c") for n in (hash(h) % 100, hash(h) % 100 + 1)]
    first = build_duplicate_clusters(rows, site_id="s1")
    second = build_duplicate_clusters(list(reversed(rows)), site_id="s1")
    assert [c.exact_sha256 for c in first.clusters] == [c.exact_sha256 for c in second.clusters]


@pytest.mark.parametrize(
    "extracted,expected",
    [
        ({"fingerprint": {"version": 1, "exact_sha256": "abc"}}, (1, "abc")),
        ({"fingerprint": {"version": 1}}, None),
        ({"fingerprint": {"version": "1", "exact_sha256": "abc"}}, None),
        ({"fingerprint": {"version": 1, "exact_sha256": ""}}, None),
        ({}, None),
        (None, None),
    ],
)
def test_fingerprint_key_extraction(extracted, expected):
    assert _fingerprint_key(extracted) == expected


def test_cluster_membership_matches_analysis_check():
    """Anti-drift: the cluster list and the per-page `duplicate_content_exact`
    verdict are two views of ONE fact. A page the check calls a duplicate must
    appear in a cluster, and a page it calls unique must not.
    """
    facts = [
        PageFacts(page_id="p1", url="u1", fingerprint_version=1, exact_sha256="aaa"),
        PageFacts(page_id="p2", url="u2", fingerprint_version=1, exact_sha256="aaa"),
        PageFacts(page_id="p3", url="u3", fingerprint_version=1, exact_sha256="bbb"),
        PageFacts(page_id="p4", url="u4", fingerprint_version=2, exact_sha256="aaa"),
        PageFacts(page_id="p5", url="u5"),
    ]
    site = SiteAggregates()
    for f in facts:
        if f.exact_sha256 is not None and f.fingerprint_version is not None:
            site.pages_by_sha.setdefault((f.fingerprint_version, f.exact_sha256), []).append(f)

    report = build_duplicate_clusters(
        [
            (
                (f.fingerprint_version, f.exact_sha256)
                if f.exact_sha256 is not None and f.fingerprint_version is not None
                else None,
                DuplicatePage(page_id=f.page_id, url=f.url),
            )
            for f in facts
        ],
        site_id="s1",
    )
    clustered = {p.page_id for c in report.clusters for p in c.pages}

    for f in facts:
        flagged = _check_duplicate_content_exact(f, site).status == "fail"
        assert flagged is (f.page_id in clustered), f.page_id


# ---------------------------------------------------------------------------
# Link graph


def node(
    n: int, *, inbound: int = 0, outbound: int = 0, link_score: float | None = None
) -> LinkGraphNode:
    return LinkGraphNode(
        page_id=f"p{n}",
        url=f"https://example.com/{n:03d}",
        link_score=link_score,
        inbound_internal_links=inbound,
        outbound_internal_links=outbound,
        status="active",
    )


def test_nodes_are_ranked_by_link_score_then_capped():
    candidates = [node(n, link_score=float(n)) for n in range(10)]
    kept = rank_and_cap_nodes(candidates, max_nodes=3)
    assert [n.page_id for n in kept] == ["p9", "p8", "p7"]


def test_unscored_pages_never_outrank_scored_ones():
    """`link_score` is NULL until a COMPLETED full crawl is scored. In-degree
    is a different scale, so an unscored page ranks BELOW every scored one
    instead of competing against a PageRank number."""
    candidates = [node(1, link_score=0.5), node(2, inbound=9_999)]
    kept = rank_and_cap_nodes(candidates, max_nodes=1)
    assert [n.page_id for n in kept] == ["p1"]


def test_in_degree_ranks_a_site_that_has_never_been_scored():
    candidates = [node(n, inbound=n) for n in range(10)]
    kept = rank_and_cap_nodes(candidates, max_nodes=3)
    assert [n.page_id for n in kept] == ["p9", "p8", "p7"]


def test_node_ranking_is_deterministic_on_ties():
    candidates = [node(n, inbound=5) for n in range(5)]
    first = rank_and_cap_nodes(candidates, max_nodes=3)
    second = rank_and_cap_nodes(list(reversed(candidates)), max_nodes=3)
    assert [n.page_id for n in first] == [n.page_id for n in second]
    assert [n.url for n in first] == sorted(n.url for n in first)


def test_orphan_pages_survive_when_under_the_cap():
    """A page with zero inbound links is the most interesting node on an SEO
    graph — it must not be ranked out of existence when there is room."""
    candidates = [node(1, inbound=9), node(2, inbound=0)]
    kept = rank_and_cap_nodes(candidates, max_nodes=10)
    assert {n.page_id for n in kept} == {"p1", "p2"}


# ---------------------------------------------------------------------------
# Progress series

BASE = datetime(2026, 8, 9, 12, 0, 0, tzinfo=UTC)


def point(i: int, *, fetched: int, seconds: int) -> ProgressPoint:
    return ProgressPoint(
        occurred_at=BASE + timedelta(seconds=seconds),
        sequence=i,
        elapsed_ms=seconds * 1000,
        pages_discovered=fetched * 2,
        pages_fetched=fetched,
        queue_depth=max(0, 100 - fetched),
    )


def test_empty_series_is_empty_not_an_error():
    series = build_progress_series([], session_id="s1")
    assert series.points == []
    assert series.points_total == 0


def test_rate_is_derived_between_returned_points():
    raw = [point(i, fetched=i * 10, seconds=i * 10) for i in range(1, 4)]
    series = build_progress_series(raw, session_id="s1")
    assert series.points_returned == 3
    assert series.points[0].pages_per_second == 1.0  # 10 pages in 10s since start
    assert series.points[1].pages_per_second == 1.0
    assert series.points[2].pages_per_second == 1.0


def test_downsampling_keeps_first_and_last_and_reports_the_drop():
    raw = [point(i, fetched=i, seconds=i) for i in range(100)]
    series = build_progress_series(raw, session_id="s1", max_points=10)
    assert series.points_total == 100
    assert series.points_returned <= 10
    assert series.points_omitted == 100 - series.points_returned
    assert series.sample_stride == 10
    assert series.points[0].sequence == raw[0].sequence
    assert series.points[-1].sequence == raw[-1].sequence


def test_downsampled_rate_spans_the_interval_it_is_drawn_across():
    """Rate is computed AFTER downsampling, so each plotted value describes
    exactly the span between the points actually shown."""
    raw = [point(i, fetched=i * 2, seconds=i) for i in range(21)]
    series = build_progress_series(raw, session_id="s1", max_points=3)
    assert series.points_returned <= 4
    for shown in series.points[1:]:
        assert shown.pages_per_second == pytest.approx(2.0)


def test_resumed_counters_report_no_rate_instead_of_a_negative_one():
    """A resumed session re-runs under the same session_id with counters back
    at zero; a negative throughput would be nonsense on a chart."""
    raw = [
        point(1, fetched=50, seconds=10),
        point(2, fetched=5, seconds=20),
    ]
    series = build_progress_series(raw, session_id="s1")
    assert series.points[1].pages_per_second is None


def test_zero_span_reports_no_rate():
    raw = [point(1, fetched=0, seconds=0), point(2, fetched=5, seconds=0)]
    series = build_progress_series(raw, session_id="s1")
    assert series.points[0].pages_per_second is None
    assert series.points[1].pages_per_second is None


def test_scan_truncation_is_surfaced():
    raw = [point(i, fetched=i, seconds=i) for i in range(5)]
    series = build_progress_series(raw, session_id="s1", scan_truncated=True)
    assert series.scan_truncated is True
