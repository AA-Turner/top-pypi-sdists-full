"""Lab-performance checks — the `performance` half of the `web.analysis_item`
catalogue, scored from PageSpeed Insights (`seo.page_performance`).

Two things are pinned here, and they are the two ways this feature can rot:

1. **The published formulas.** Every band asserted below is copied from the
   catalogue row's own ``score_contract.formula`` — the row IS the contract.
   A boundary that drifts is a scoring change nobody agreed to.
2. **Never a score without a measurement.** PageSpeed is a separate, paid,
   minute-long remote render; a crawl cannot produce a Core Web Vital. So an
   unmeasured page must answer ``n_a`` WITH a one-click remediation, never a
   pass. A fabricated pass here would tell a user their slow page is fine.

The delivery/caching fixture is a REAL Lighthouse 13 projection captured from
`https://www.wikipedia.org/` through `matrx_seo.providers.pagespeed`, because
Lighthouse 13 renamed the entire opportunity family (`render-blocking-resources`
→ `render-blocking-insight`, `uses-long-cache-ttl` → `cache-insight`) and a
hand-invented shape would prove nothing about what PSI actually returns.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from matrx_scraper.seo_audit import (
    CACHE_WELL_CACHED_MIN_MS,
    LAB_PERFORMANCE_MAX_AGE_DAYS,
    LabPerformance,
    PageEvidence,
    check_asset_delivery,
    check_caching_policy,
    check_cwv_cls,
    check_cwv_inp_tbt,
    check_cwv_lcp,
    lab_performance_from_lighthouse,
)

NOW = datetime.now(UTC)
DAY_MS = 24 * 60 * 60 * 1_000


def _evidence(**lab: object) -> PageEvidence:
    evidence = PageEvidence(url="https://example.com/page")
    evidence.lab_performance = LabPerformance(strategy="mobile", observed_at=NOW, **lab)  # type: ignore[arg-type]
    return evidence


# --- The contract every check shares ---------------------------------------

ALL_CHECKS = (
    check_cwv_lcp,
    check_cwv_inp_tbt,
    check_cwv_cls,
    check_asset_delivery,
    check_caching_policy,
)


@pytest.mark.parametrize("check", ALL_CHECKS)
def test_no_measurement_is_n_a_with_a_one_click_fix(check) -> None:
    outcome = check(PageEvidence(url="https://example.com/page"))
    assert outcome.status == "n_a"
    assert outcome.score is None
    assert outcome.remediation is not None
    assert outcome.remediation.command == "pagespeed_collect"


@pytest.mark.parametrize("check", ALL_CHECKS)
def test_stale_measurement_is_n_a_not_a_score(check) -> None:
    evidence = PageEvidence(url="https://example.com/page")
    evidence.lab_performance = LabPerformance(
        strategy="mobile",
        observed_at=NOW - timedelta(days=LAB_PERFORMANCE_MAX_AGE_DAYS + 1),
        lcp_ms=800,
        tbt_ms=10,
        cls=0.01,
        delivery_savings_ms=0,
        cache_static_bytes=1_000_000,
    )
    outcome = check(evidence)
    assert outcome.status == "n_a"
    assert outcome.remediation is not None


@pytest.mark.parametrize("check", ALL_CHECKS)
def test_measured_but_metric_absent_is_n_a(check) -> None:
    """A PSI run that reported nothing for THIS metric still scores nothing."""
    outcome = check(_evidence())
    assert outcome.status == "n_a"
    assert outcome.score is None


@pytest.mark.parametrize("check", ALL_CHECKS)
def test_status_and_score_satisfy_the_db_constraint(check) -> None:
    """`analysis_result_status_score_valid`: pass/warn/fail ⇒ 1–100, n_a ⇒ NULL."""
    samples = [
        PageEvidence(url="https://example.com/page"),
        _evidence(),
        _evidence(lcp_ms=100, tbt_ms=0, cls=0.0, delivery_savings_ms=0, cache_static_bytes=500_000),
        _evidence(
            lcp_ms=99_000,
            tbt_ms=99_000,
            cls=9.9,
            delivery_savings_ms=99_000,
            delivery_audits={"unused-javascript": 99_000.0},
            cache_static_bytes=500_000,
            cache_short_ttl_resources=[
                {"url": "https://x/a.js", "cache_lifetime_ms": 0, "total_bytes": 500_000}
            ],
        ),
    ]
    for evidence in samples:
        outcome = check(evidence)
        assert outcome.status in {"pass", "warn", "fail", "n_a"}
        if outcome.status == "n_a":
            assert outcome.score is None
        else:
            assert outcome.score is not None and 1 <= outcome.score <= 100


# --- cwv_lcp: "lcp<=2500ms: 90-100; 2500-4000ms: 50-89; >4000: 49-(lcp-4000)/200"


@pytest.mark.parametrize(
    ("lcp_ms", "score", "status"),
    [
        (0, 100, "pass"),
        (2_500, 90, "pass"),
        (3_250, 70, "warn"),
        (4_000, 50, "warn"),
        (6_000, 39, "fail"),
        (14_000, 1, "fail"),
    ],
)
def test_cwv_lcp_bands(lcp_ms: int, score: int, status: str) -> None:
    outcome = check_cwv_lcp(_evidence(lcp_ms=float(lcp_ms)))
    assert (outcome.score, outcome.status) == (score, status)


# --- cwv_inp_tbt: "tbt<=200: 90-100; 200-600: 50-89; >600: 49-(tbt-600)/50" ---


@pytest.mark.parametrize(
    ("tbt_ms", "score", "status"),
    [
        (0, 100, "pass"),
        (200, 90, "pass"),
        (400, 70, "warn"),
        (600, 50, "warn"),
        (1_000, 41, "fail"),
    ],
)
def test_cwv_inp_tbt_bands(tbt_ms: int, score: int, status: str) -> None:
    outcome = check_cwv_inp_tbt(_evidence(tbt_ms=float(tbt_ms)))
    assert (outcome.score, outcome.status) == (score, status)


# --- cwv_cls: "cls<=0.1: 90-100; 0.1-0.25: 50-89; >0.25: 49-(cls-0.25)*100" ---


@pytest.mark.parametrize(
    ("cls", "score", "status"),
    [
        (0.0, 100, "pass"),
        (0.1, 90, "pass"),
        (0.175, 70, "warn"),
        (0.25, 50, "warn"),
        (0.5, 24, "fail"),
    ],
)
def test_cwv_cls_bands(cls: float, score: int, status: str) -> None:
    outcome = check_cwv_cls(_evidence(cls=cls))
    assert (outcome.score, outcome.status) == (score, status)


# --- asset_delivery: "<=250ms: 90-100; 250-1500: 50-89; >1500: max(10, 49-(s-1500)/100)"


@pytest.mark.parametrize(
    ("savings_ms", "score"),
    [(0, 100), (250, 90), (875, 70), (1_500, 50), (3_000, 34), (99_000, 10)],
)
def test_asset_delivery_bands(savings_ms: int, score: int) -> None:
    outcome = check_asset_delivery(
        _evidence(
            delivery_savings_ms=float(savings_ms),
            delivery_audits={"render-blocking-insight": float(savings_ms)},
        )
    )
    assert outcome.score == score


def test_asset_delivery_names_the_offenders_in_plain_language() -> None:
    outcome = check_asset_delivery(
        _evidence(
            delivery_savings_ms=2_000.0,
            delivery_audits={"render-blocking-insight": 1_500.0, "unused-javascript": 500.0},
        )
    )
    assert outcome.status in {"warn", "fail"}
    assert "files that block the page from drawing" in outcome.reasoning
    # The user-facing sentence must never leak a Lighthouse audit id.
    assert "render-blocking-insight" not in outcome.reasoning
    assert outcome.evidence is not None
    assert outcome.evidence["audits"]["render-blocking-insight"] == 1_500.0


# --- caching_policy: "round(100 * well_cached/static); 100 when negligible" ---


def test_caching_policy_negligible_static_bytes_scores_100() -> None:
    outcome = check_caching_policy(_evidence(cache_static_bytes=2_048.0))
    assert (outcome.status, outcome.score) == ("pass", 100)


def test_caching_policy_is_byte_weighted_not_file_counted() -> None:
    """One huge under-cached file must outweigh many small well-cached ones."""
    outcome = check_caching_policy(
        _evidence(
            cache_static_bytes=1_000_000.0,
            cache_short_ttl_resources=[
                {"url": "https://x/hero.png", "cache_lifetime_ms": DAY_MS, "total_bytes": 800_000},
            ],
        )
    )
    assert outcome.score == 20
    assert outcome.status == "fail"
    assert outcome.issue_count == 1


def test_caching_policy_ignores_resources_already_cached_long_enough() -> None:
    outcome = check_caching_policy(
        _evidence(
            cache_static_bytes=1_000_000.0,
            cache_short_ttl_resources=[
                # Reported by Lighthouse but at/above our 30-day bar — not a defect.
                {
                    "url": "https://x/a.js",
                    "cache_lifetime_ms": CACHE_WELL_CACHED_MIN_MS,
                    "total_bytes": 900_000,
                },
            ],
        )
    )
    assert (outcome.status, outcome.score) == ("pass", 100)


def test_caching_policy_cannot_score_below_zero_well_cached_bytes() -> None:
    """Lighthouse's byte accounting is its own; it may exceed our denominator."""
    outcome = check_caching_policy(
        _evidence(
            cache_static_bytes=100_000.0,
            cache_short_ttl_resources=[
                {"url": "https://x/a.js", "cache_lifetime_ms": 0, "total_bytes": 999_999_999},
            ],
        )
    )
    assert outcome.score == 1
    assert outcome.status == "fail"


# --- The ONE deserializer of `seo.page_performance.lighthouse` --------------

# Real Lighthouse 13.4.1 projection, captured live from PSI through
# `matrx_seo.providers.pagespeed::_delivery_facts` (2026-08-09).
LIVE_LIGHTHOUSE = {
    "data_kind": "lab",
    "version": "13.4.1",
    "metrics": {
        "cls": {"numeric_value": 0.010427502130298012, "numeric_unit": "unitless", "score": 1},
        "lcp_ms": {
            "numeric_value": 3232.4744364219664,
            "numeric_unit": "millisecond",
            "score": 0.71,
        },
        "tbt_ms": {"numeric_value": 0, "numeric_unit": "millisecond", "score": 1},
        "ttfb_ms": {"numeric_value": 102, "numeric_unit": "millisecond", "score": 1},
    },
    "delivery": {
        "audits": {
            "render-blocking-insight": {"score": 1, "savings_ms": 0.0, "wasted_bytes": None},
            "image-delivery-insight": {"score": 0, "savings_ms": 150.0, "wasted_bytes": None},
            "unused-javascript": {"score": 1, "savings_ms": 0.0, "wasted_bytes": 0.0},
        },
        "total_savings_ms": 150.0,
        "measured_audits": [
            "image-delivery-insight",
            "render-blocking-insight",
            "unused-javascript",
        ],
        "cache": {
            "measured": True,
            "static_bytes": 69656.0,
            "static_requests": 4,
            "short_ttl_resources": [
                {
                    "url": "https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@2x.png",
                    "cache_lifetime_ms": 86400000.0,
                    "total_bytes": 38642.0,
                }
            ],
        },
    },
}


def test_deserializer_reads_a_live_lighthouse_13_payload() -> None:
    lab = lab_performance_from_lighthouse(LIVE_LIGHTHOUSE, strategy="mobile", observed_at=NOW)
    assert lab.lcp_ms == pytest.approx(3232.47, abs=0.01)
    assert lab.tbt_ms == 0.0
    assert lab.cls == pytest.approx(0.0104, abs=0.0001)
    assert lab.delivery_savings_ms == 150.0
    assert lab.delivery_audits["image-delivery-insight"] == 150.0
    assert lab.cache_static_bytes == 69656.0
    assert len(lab.cache_short_ttl_resources) == 1


def test_deserializer_degrades_to_n_a_on_a_pre_delivery_payload() -> None:
    """Rows written before the delivery projection existed must not score 0."""
    legacy = {k: v for k, v in LIVE_LIGHTHOUSE.items() if k != "delivery"}
    lab = lab_performance_from_lighthouse(legacy, strategy="mobile", observed_at=NOW)
    assert lab.lcp_ms is not None
    assert lab.delivery_savings_ms is None
    assert lab.cache_static_bytes is None

    evidence = PageEvidence(url="https://example.com/page")
    evidence.lab_performance = lab
    assert check_cwv_lcp(evidence).status != "n_a"
    assert check_asset_delivery(evidence).status == "n_a"
    assert check_caching_policy(evidence).status == "n_a"


@pytest.mark.parametrize("payload", [None, {}, {"metrics": "not-a-dict"}, {"delivery": []}])
def test_deserializer_never_raises_on_a_malformed_payload(payload) -> None:
    lab = lab_performance_from_lighthouse(payload, strategy="mobile")
    assert lab.lcp_ms is None
    assert lab.delivery_savings_ms is None


def test_zero_static_bytes_is_measured_not_missing() -> None:
    """A page with no static assets passes; a page never measured does not."""
    outcome = check_caching_policy(_evidence(cache_static_bytes=0.0))
    assert (outcome.status, outcome.score) == ("pass", 100)
