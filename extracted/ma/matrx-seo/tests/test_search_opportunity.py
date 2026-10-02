"""Search opportunity scorer (OPENSEO-TOOLS-SPEC §5.5 item 6, §9 T6 unit half).

Every expectation here is the method's own arithmetic (OpenSEO
SearchOpportunityService at 0ffff93), worked by hand — not a snapshot of what
the code happens to print.
"""

from __future__ import annotations

import math

import pytest

from matrx_seo.search_opportunity import (
    Ga4LandingRow,
    GscPageRow,
    Weights,
    normalize_page_key,
    percentile_ranks,
    score_search_opportunities,
)

W = Weights(demand=0.5, value=0.3, reach=0.2)


def ga4(path: str, *, sessions=100.0, key_events=5.0, ekr=0.05, er=0.6, host="example.com"):
    return Ga4LandingRow(
        host=host,
        landing_page=path,
        sessions=sessions,
        engaged_sessions=None,
        engagement_rate=er,
        key_events=key_events,
        session_key_event_rate=ekr,
    )


def gsc(url: str, *, impressions=100, clicks=1, position=10.0):
    return GscPageRow(page=url, clicks=clicks, impressions=impressions, position=position)


def run(gsc_rows, ga4_rows, **kw):
    kw.setdefault("weights", W)
    kw.setdefault("position_min", 4)
    kw.setdefault("position_max", 20)
    kw.setdefault("limit", 100)
    return score_search_opportunities(gsc_rows, ga4_rows, **kw)


# ── join key ────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("raw", "key"),
    [
        ("https://Example.com/Blog/", "example.com/Blog"),  # host lowercased, path case kept
        ("http://example.com:80/a", "example.com/a"),  # default port dropped
        ("https://example.com:443/a?x=1#f", "example.com/a"),  # query/fragment ignored
        ("https://example.com:8443/a", "example.com:8443/a"),  # non-default port kept
        ("https://example.com/", "example.com/"),  # root keeps its slash
        ("https://www.example.com/a", "www.example.com/a"),  # www is not the apex
        ("example.com/a/", "example.com/a"),  # GA4 host+path, no scheme
    ],
)
def test_join_key(raw: str, key: str) -> None:
    assert normalize_page_key(raw) == key


@pytest.mark.parametrize("raw", ["(not set)", "", "   ", "https://example.com:notaport/", None])
def test_unjoinable_values_are_none(raw) -> None:
    assert normalize_page_key(raw) is None


def test_www_and_apex_do_not_join() -> None:
    result = run([gsc("https://www.example.com/a")], [ga4("/a")])
    assert result.rows[0]["join_status"] == "gsc_only"


# ── percentile ranks ────────────────────────────────────────────────────────


def test_percentile_ties_share_a_rank_and_n_1_is_one() -> None:
    assert percentile_ranks([5.0]) == [1.0]
    assert percentile_ranks([]) == []
    # count(values < v) / (n - 1): 1 → 0/3, 2 → 1/3, 2 → 1/3, 9 → 3/3
    assert percentile_ranks([1.0, 2.0, 2.0, 9.0]) == [0.0, 1 / 3, 1 / 3, 1.0]


# ── the score ───────────────────────────────────────────────────────────────


def test_score_is_the_weighted_percentile_sum() -> None:
    rows = [
        gsc("https://example.com/a", impressions=1000, position=5.0),
        gsc("https://example.com/b", impressions=10, position=15.0),
    ]
    result = run(rows, [ga4("/a", ekr=0.10), ga4("/b", ekr=0.01)])
    a, b = result.rows
    # /a wins every component (rank 1), /b loses every one (rank 0).
    assert a["page"].endswith("/a") and a["score"] == 100
    assert b["score"] == 0
    assert a["components"] == {"demand": 1.0, "value": 1.0, "reach": 1.0}


def test_weights_are_knobs_not_constants() -> None:
    rows = [
        gsc("https://example.com/a", impressions=1000, position=15.0),
        gsc("https://example.com/b", impressions=10, position=5.0),
    ]
    only_reach = Weights(demand=0, value=0, reach=1)
    result = run(rows, [ga4("/a"), ga4("/b")], weights=only_reach)
    assert result.rows[0]["page"].endswith("/b") and result.rows[0]["score"] == 100


def test_candidates_are_the_position_band_only() -> None:
    rows = [
        gsc("https://example.com/top", position=2.0),
        gsc("https://example.com/mid", position=12.0),
    ]
    result = run(rows, [ga4("/top"), ga4("/mid")])
    assert [r["page"] for r in result.rows] == ["https://example.com/mid"]


def test_engagement_fallback_when_no_joined_row_has_a_key_event() -> None:
    rows = [gsc("https://example.com/a"), gsc("https://example.com/b")]
    result = run(
        rows,
        [ga4("/a", key_events=0, ekr=0.0, er=0.9), ga4("/b", key_events=0, ekr=0.0, er=0.1)],
    )
    assert result.engagement_fallback is True
    assert result.value_metric == "engagementRate"
    by = {r["page"][-1]: r for r in result.rows}
    assert by["a"]["components"]["value"] == 1.0 and by["b"]["components"]["value"] == 0.0


def test_gsc_only_rows_are_kept_unscored_and_last() -> None:
    rows = [
        gsc("https://example.com/unmatched", impressions=99_999, position=4.0),
        gsc("https://example.com/a", impressions=1),
    ]
    result = run(rows, [ga4("/a")])
    assert [r["join_status"] for r in result.rows] == ["joined", "gsc_only"]
    last = result.rows[-1]
    assert last["score"] is None and last["sessions"] is None and last["key_event_rate"] is None
    assert result.coverage["unmatched_gsc"] == 1 and result.coverage["matched"] == 1


def test_a_missing_value_metric_stays_unknown_never_zero() -> None:
    """Coordinator heads-up: a joined page whose GA4 value metric is missing must not be
    ranked as 0 — it stays visible, unscored, and says why; the others rank without it."""
    rows = [gsc("https://example.com/a"), gsc("https://example.com/b"), gsc("https://example.com/c")]
    result = run(rows, [ga4("/a", ekr=0.2), ga4("/b", ekr=0.1), ga4("/c", ekr=None)])
    by = {r["page"][-1]: r for r in result.rows}
    assert by["c"]["score"] is None and "not scored" in by["c"]["note"]
    assert by["c"]["key_event_rate"] is None
    # With c excluded, a and b rank against each other only (not against a fake 0).
    assert by["a"]["components"]["value"] == 1.0 and by["b"]["components"]["value"] == 0.0
    assert result.rows[-1]["page"].endswith("/c")


def test_duplicate_ga4_rows_merge_instead_of_last_wins() -> None:
    rows = [gsc("https://example.com/a")]
    result = run(rows, [ga4("/a", sessions=10), ga4("/a/", sessions=30)])
    assert result.rows[0]["sessions"] == 40


def test_offering_worth_path_ranks_worth_and_falls_back_per_row() -> None:
    rows = [gsc("https://example.com/a"), gsc("https://example.com/b"), gsc("https://example.com/c")]
    worth = {"example.com/a": 5.0, "example.com/b": 50.0}
    result = run(
        rows,
        [ga4("/a", ekr=0.9), ga4("/b", ekr=0.0), ga4("/c", ekr=0.3)],
        value_source="offering_worth",
        offering_worth=worth,
    )
    by = {r["page"][-1]: r for r in result.rows}
    # Worth decides a vs b even though GA4 would rank them the other way.
    assert by["b"]["components"]["value"] == 1.0 and by["a"]["components"]["value"] == 0.0
    assert by["a"]["value_basis"] == "offering_worth"
    assert by["c"]["value_basis"] == "sessionKeyEventRate" and "No offering" in by["c"]["note"]
    assert result.coverage["value_from_offering_worth"] == 2


def test_offering_worth_is_ignored_when_value_source_is_ga4() -> None:
    rows = [gsc("https://example.com/a"), gsc("https://example.com/b")]
    result = run(
        rows,
        [ga4("/a", ekr=0.9), ga4("/b", ekr=0.0)],
        offering_worth={"example.com/b": 99.0},
    )
    by = {r["page"][-1]: r for r in result.rows}
    assert by["a"]["components"]["value"] == 1.0
    assert "value_basis" not in by["a"]


def test_sort_is_score_then_impressions_and_limit_truncates() -> None:
    rows = [gsc(f"https://example.com/p{i}", impressions=10 * (i + 1)) for i in range(5)]
    result = run(rows, [ga4(f"/p{i}") for i in range(5)], limit=2)
    assert len(result.rows) == 2 and result.truncated["candidates"] is True
    assert result.rows[0]["score"] >= result.rows[1]["score"]


def test_demand_uses_log1p_impressions() -> None:
    # Ranks are order-only, so log1p preserves order; the formula text names it.
    result = run([gsc("https://example.com/a")], [ga4("/a")])
    assert "log1p(impressions)" in result.formula
    assert math.isclose(result.rows[0]["components"]["demand"], 1.0)


def test_weights_from_knob_rejects_bad_shapes() -> None:
    assert Weights.from_knob({"demand": 0.5, "value": 0.3, "reach": 0.2}) == W
    with pytest.raises(ValueError):
        Weights.from_knob({"demand": 0.5})
    with pytest.raises(ValueError):
        Weights.from_knob({"demand": -1, "value": 0, "reach": 0})


def test_ga4_never_read_reports_its_numbers_as_unknown_not_zero() -> None:
    """D-1: when GA4 was not read at all, nothing about GA4 is a known 0 or false."""
    result = run(
        [gsc("https://example.com/a")], [], ga4_read=False
    )
    assert result.rows[0]["score"] is None and result.rows[0]["join_status"] == "gsc_only"
    assert result.coverage["ga4_rows_considered"] is None
    assert result.coverage["unmatched_ga4"] is None
    assert result.coverage["unparseable_ga4"] is None
    assert result.coverage["matched"] is None
    assert result.engagement_fallback is None
    assert result.value_metric is None
    assert result.truncated["ga4"] is None
    out = result.to_dict()
    assert out["engagement_fallback"] is None and out["value_metric"] is None
