"""`search_signals` — the checks that read GOOGLE'S OWN numbers.

Every other catalogue category is an inference: we look at a page and reason
about how it will perform. These two look at what Google reported it actually
did (`web.gsc_page_stat`, written by `gsc_sync` with dimensions date × page).

What these tests pin:

1. the documented bands of each `web.analysis_item.score_contract`, verbatim —
   including the boundaries, where an off-by-one silently changes a verdict;
2. the `n_a` ladder. A site with no Search Console property bound must SAY so
   and score nothing. A `pass` there would tell a user their pages are earning
   the clicks they deserve on the strength of data nobody ever fetched;
3. the window arithmetic, which is anchored to the freshest SYNCED day rather
   than to "today" — GSC lags reality by ~2 days, and a sweep run on a Monday
   must not read the missing weekend as a collapse.
"""

from __future__ import annotations

from datetime import date

import pytest

from matrx_scraper.web_crawl.analysis import (
    GSC_CTR_MIN_IMPRESSIONS,
    GSC_CTR_SEVERE_IMPRESSIONS,
    GSC_DECAY_MIN_BASELINE_CLICKS,
    GSC_DECAY_MIN_HISTORY_DAYS,
    GSC_PERIOD_DAYS,
    CROSS_PAGE_CHECKS,
    GscPeriod,
    PageFacts,
    PageGscStats,
    SiteAggregates,
    SiteGscEvidence,
    _check_gsc_ctr_opportunity,
    _check_gsc_performance_decay,
    _gsc_windows,
    expected_ctr_for_position,
)

PAGE_ID = "page-1"
LATEST = date(2026, 7, 26)
GSC_CHECKS = (_check_gsc_ctr_opportunity, _check_gsc_performance_decay)


def facts() -> PageFacts:
    return PageFacts(url="https://example.com/a", page_id=PAGE_ID)


def site(
    *,
    bound: bool = True,
    synced: bool = True,
    history_days: int = 365,
    current: GscPeriod | None = None,
    prior: GscPeriod | None = None,
    quarter: GscPeriod | None = None,
    page_id: str = PAGE_ID,
) -> SiteAggregates:
    """A site whose Google evidence is exactly what the test says it is."""
    evidence = SiteGscEvidence(bound=bound)
    if bound and synced:
        evidence.latest_date = LATEST
        evidence.earliest_date = date.fromordinal(LATEST.toordinal() - history_days + 1)
        if current or prior or quarter:
            evidence.by_page[page_id] = PageGscStats(
                current=current or GscPeriod(),
                prior=prior or GscPeriod(),
                quarter=quarter or GscPeriod(),
            )
    aggregates = SiteAggregates()
    aggregates.gsc = evidence
    return aggregates


def assert_db_valid(outcome) -> None:
    """Mirror of `analysis_result_status_score_valid` + `status_valid`."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


# ---------------------------------------------------------------------------
# 1. No Google property bound — the path that must never invent a verdict


@pytest.mark.parametrize("check", GSC_CHECKS)
def test_unbound_site_is_n_a_naming_the_missing_connection(check):
    outcome = check(facts(), site(bound=False))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert "Search Console" in outcome.reasoning
    assert "not connected" in outcome.reasoning
    # The prose stays in the user's language; the parser's own sentence (which
    # names a JSON path) rides along as evidence for whoever has to fix it.
    assert outcome.evidence["gsc_binding"]
    assert "integrations" not in outcome.reasoning


@pytest.mark.parametrize("check", GSC_CHECKS)
def test_a_bare_site_aggregate_is_treated_as_unbound(check):
    """The DEFAULT `SiteAggregates` — nobody loaded any evidence at all.

    This is the shape every unit test and any future caller that forgets the
    loader will produce. It must land on `n_a`, never a pass.
    """
    outcome = check(facts(), SiteAggregates())
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


@pytest.mark.parametrize("check", GSC_CHECKS)
def test_bound_but_never_synced_offers_the_sync_as_a_one_click_fix(check):
    outcome = check(facts(), site(synced=False))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert outcome.remediation is not None
    assert outcome.remediation.command == "gsc_sync"


@pytest.mark.parametrize("check", GSC_CHECKS)
def test_a_page_google_never_reported_is_n_a_not_a_pass(check):
    """Google has data for the site but none for this page."""
    outcome = check(facts(), site(page_id="some-other-page"))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


# ---------------------------------------------------------------------------
# 2. gsc_ctr_opportunity — the contract's four rules, first match top down


def test_ctr_below_the_impression_floor_is_skipped():
    outcome = _check_gsc_ctr_opportunity(
        facts(),
        site(current=GscPeriod(clicks=0, impressions=GSC_CTR_MIN_IMPRESSIONS - 1, position=3.0)),
    )
    assert outcome.status == "n_a"
    assert str(GSC_CTR_MIN_IMPRESSIONS) in outcome.reasoning


def test_ctr_at_the_impression_floor_is_scored():
    """The contract says ">= 100 impressions", so 100 itself is in scope."""
    outcome = _check_gsc_ctr_opportunity(
        facts(),
        site(current=GscPeriod(clicks=0, impressions=GSC_CTR_MIN_IMPRESSIONS, position=3.0)),
    )
    assert outcome.status in ("warn", "fail")
    assert outcome.score is not None


def test_ctr_impressions_without_a_position_cannot_be_judged():
    outcome = _check_gsc_ctr_opportunity(
        facts(), site(current=GscPeriod(clicks=5, impressions=500, position=None))
    )
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


@pytest.mark.parametrize(
    ("clicks", "impressions", "position", "expected_score", "expected_status"),
    [
        # position 3 -> expected CTR 11%.
        # rule 1: CTR < 30% of expected AND >= 1000 impressions -> 35
        (30, 2_000, 3.0, 35, "fail"),  # 1.5% vs 11% = 14% of expected
        # rule 1 needs BOTH conditions; the same ratio under 1000 impressions
        # falls through to rule 2.
        (2, 200, 3.0, 55, "warn"),  # 1.0% of a 200-impression page
        # rule 2: CTR < 50% of expected -> 55
        (80, 2_000, 3.0, 55, "warn"),  # 4% vs 11% = 36% of expected
        # rule 3: CTR 50-80% of expected -> 75
        (140, 2_000, 3.0, 75, "warn"),  # 7% vs 11% = 64% of expected
        # rule 4: CTR >= 80% of expected -> 100
        (200, 2_000, 3.0, 100, "pass"),  # 10% vs 11% = 91% of expected
        # comfortably above expectation is still the top band, not >100
        (600, 2_000, 3.0, 100, "pass"),
    ],
)
def test_ctr_bands_are_the_contract_rules(
    clicks, impressions, position, expected_score, expected_status
):
    outcome = _check_gsc_ctr_opportunity(
        facts(), site(current=GscPeriod(clicks=clicks, impressions=impressions, position=position))
    )
    assert_db_valid(outcome)
    assert outcome.score == expected_score
    assert outcome.status == expected_status


def test_ctr_severe_band_needs_the_volume_the_contract_names():
    """Exactly at 1000 impressions the severe band applies; one below, it does not."""
    severe = _check_gsc_ctr_opportunity(
        facts(),
        site(current=GscPeriod(clicks=1, impressions=GSC_CTR_SEVERE_IMPRESSIONS, position=1.0)),
    )
    assert severe.score == 35
    lighter = _check_gsc_ctr_opportunity(
        facts(),
        site(current=GscPeriod(clicks=1, impressions=GSC_CTR_SEVERE_IMPRESSIONS - 1, position=1.0)),
    )
    assert lighter.score == 55


def test_ctr_evidence_names_the_clicks_that_went_elsewhere():
    outcome = _check_gsc_ctr_opportunity(
        facts(), site(current=GscPeriod(clicks=30, impressions=2_000, position=3.0))
    )
    # 11% of 2,000 = 220 expected clicks; 30 landed.
    assert outcome.evidence["missed_clicks"] == 190
    assert outcome.evidence["impressions"] == 2_000
    assert outcome.evidence["average_position"] == 3.0
    assert outcome.evidence["window"]["ending"] == LATEST.isoformat()
    assert "190" in outcome.reasoning


@pytest.mark.parametrize(
    ("clicks", "impressions", "fragment"),
    [
        (1, 306, "1 person clicked"),
        (4, 1_324, "4 people clicked"),
        (0, 194, "0 people clicked"),
    ],
)
def test_ctr_reasoning_is_written_for_a_person(clicks, impressions, fragment):
    """Real rows from the live sweep read as English, not as a log line."""
    outcome = _check_gsc_ctr_opportunity(
        facts(), site(current=GscPeriod(clicks=clicks, impressions=impressions, position=6.7))
    )
    assert fragment in outcome.reasoning
    assert "time(s)" not in outcome.reasoning


def test_expected_ctr_curve_falls_away_with_position():
    assert expected_ctr_for_position(1.0) > expected_ctr_for_position(5.0)
    assert expected_ctr_for_position(5.0) > expected_ctr_for_position(15.0)
    assert expected_ctr_for_position(15.0) > expected_ctr_for_position(50.0)
    # A fractional average position rounds to the nearest whole rank.
    assert expected_ctr_for_position(1.4) == expected_ctr_for_position(1.0)
    # Nothing beyond the table raises or returns zero.
    assert expected_ctr_for_position(0.4) == expected_ctr_for_position(1.0)
    assert expected_ctr_for_position(900.0) > 0


# ---------------------------------------------------------------------------
# 3. gsc_performance_decay — the contract's four rules


def test_decay_needs_a_quarter_of_history_before_it_answers():
    outcome = _check_gsc_performance_decay(
        facts(),
        site(
            history_days=GSC_DECAY_MIN_HISTORY_DAYS - 1,
            current=GscPeriod(clicks=10),
            prior=GscPeriod(clicks=500),
        ),
    )
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert str(GSC_DECAY_MIN_HISTORY_DAYS) in outcome.reasoning
    assert outcome.remediation is not None and outcome.remediation.command == "gsc_sync"


def test_decay_below_the_baseline_click_floor_is_skipped():
    outcome = _check_gsc_performance_decay(
        facts(),
        site(
            current=GscPeriod(clicks=0),
            prior=GscPeriod(clicks=GSC_DECAY_MIN_BASELINE_CLICKS - 1),
            quarter=GscPeriod(clicks=200),
        ),
    )
    assert outcome.status == "n_a"
    assert str(GSC_DECAY_MIN_BASELINE_CLICKS) in outcome.reasoning


@pytest.mark.parametrize(
    ("current", "prior", "quarter", "expected_score", "expected_status"),
    [
        # rule 1: down > 50% against BOTH comparisons -> 30
        (40, 200, 200, 30, "fail"),  # -80% / -80%
        # rule 2: down 25-50% across both -> 55
        (140, 200, 200, 55, "warn"),  # -30% / -30%
        # rule 3: down 10-25% -> 75
        (170, 200, 200, 75, "warn"),  # -15% / -15%
        # rule 4: stable or growing -> 100
        (200, 200, 200, 100, "pass"),
        (400, 200, 200, 100, "pass"),
        # A collapse against the prior period that is a RISE against last
        # quarter fails the "both" requirement of rules 1-2 and lands on the
        # prior-period-only band. The prior period was the anomaly.
        (100, 300, 50, 75, "warn"),
        # No clicks a quarter ago (the page is newer than the window) — the
        # same rule applies: judged on the prior-period comparison alone.
        (100, 300, 0, 75, "warn"),
    ],
)
def test_decay_bands_are_the_contract_rules(
    current, prior, quarter, expected_score, expected_status
):
    outcome = _check_gsc_performance_decay(
        facts(),
        site(
            current=GscPeriod(clicks=current, impressions=current * 10),
            prior=GscPeriod(clicks=prior, impressions=prior * 10),
            quarter=GscPeriod(clicks=quarter, impressions=quarter * 10),
        ),
    )
    assert_db_valid(outcome)
    assert outcome.score == expected_score
    assert outcome.status == expected_status


def test_decay_band_boundaries_land_on_the_documented_side():
    def score(current: int) -> int:
        return _check_gsc_performance_decay(
            facts(),
            site(
                current=GscPeriod(clicks=current),
                prior=GscPeriod(clicks=1000),
                quarter=GscPeriod(clicks=1000),
            ),
        ).score

    assert score(499) == 30  # 50.1% down — "> 50%"
    assert score(500) == 55  # exactly 50% down is the 25-50% band
    assert score(750) == 55  # exactly 25% down is still that band
    assert score(751) == 75  # 24.9% down — the 10-25% band
    assert score(900) == 75  # exactly 10% down is a decline
    assert score(901) == 100  # 9.9% down is noise, not decay


def test_decay_evidence_carries_both_comparisons_and_their_windows():
    outcome = _check_gsc_performance_decay(
        facts(),
        site(
            current=GscPeriod(clicks=50, impressions=1_000),
            prior=GscPeriod(clicks=200, impressions=3_000),
            quarter=GscPeriod(clicks=300, impressions=4_000),
        ),
    )
    assert outcome.evidence["drop_vs_prior"] == 0.75
    assert outcome.evidence["drop_vs_quarter"] == pytest.approx(0.8333, abs=1e-4)
    (_, _), (prior_start, prior_end), (quarter_start, quarter_end) = _gsc_windows(LATEST)
    assert outcome.evidence["prior"]["from"] == prior_start.isoformat()
    assert outcome.evidence["prior"]["to"] == prior_end.isoformat()
    assert outcome.evidence["quarter"]["from"] == quarter_start.isoformat()
    assert outcome.evidence["quarter"]["to"] == quarter_end.isoformat()


def test_decay_with_no_quarter_data_says_so_rather_than_inventing_a_number():
    outcome = _check_gsc_performance_decay(
        facts(),
        site(current=GscPeriod(clicks=100), prior=GscPeriod(clicks=300), quarter=GscPeriod()),
    )
    assert outcome.evidence["drop_vs_quarter"] is None
    assert "a quarter ago" not in outcome.reasoning


# ---------------------------------------------------------------------------
# 4. The windows


def test_windows_are_contiguous_and_anchored_to_the_freshest_synced_day():
    (current_start, current_end), (prior_start, prior_end), (q_start, q_end) = _gsc_windows(LATEST)
    assert current_end == LATEST
    for start, end in ((current_start, current_end), (prior_start, prior_end), (q_start, q_end)):
        assert (end - start).days + 1 == GSC_PERIOD_DAYS
    # The prior window ends the day before the current one begins — no overlap,
    # no gap, so a click is counted in exactly one of them.
    assert (current_start - prior_end).days == 1
    # The quarter window sits a full quarter behind the freshest day.
    assert (LATEST - q_end).days == 90
    # And the whole span fits inside the minimum history the check demands.
    assert (LATEST - q_start).days + 1 == GSC_DECAY_MIN_HISTORY_DAYS


# ---------------------------------------------------------------------------
# 5. Registration


def test_both_checks_are_registered_as_cross_page():
    """They read a site-wide load, so they belong to the sweep, not `seo_audit`.

    `seo_audit` is standalone and never touches the database; a check whose
    evidence is `web.gsc_page_stat` rows structurally cannot live there.
    """
    assert CROSS_PAGE_CHECKS["gsc_ctr_opportunity"] is _check_gsc_ctr_opportunity
    assert CROSS_PAGE_CHECKS["gsc_performance_decay"] is _check_gsc_performance_decay
