"""Census fixes for the performance checks (2026-10-14 live census B).

Each test fails on the pre-fix behaviour: stale lab numbers stated as fact, lab
graded against field thresholds, summed overlapping savings, third-party cache
files and the provider cap presented as the owner's problem, TTFB without a
date, and tracking pixels / tiny pages failing the modern-format check.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from matrx_seo.providers.pagespeed import _delivery_facts

from matrx_scraper.seo_audit import (
    LAB_PERFORMANCE_MAX_AGE_DAYS,
    LabPerformance,
    PageEvidence,
    check_asset_delivery,
    check_caching_policy,
    check_cwv_cls,
    check_cwv_inp_tbt,
    check_cwv_lcp,
    check_image_modern_format,
    check_ttfb_server_response,
    lab_performance_from_lighthouse,
)

NOW = datetime.now(UTC)
MONTH_MS = 31 * 24 * 60 * 60 * 1000


def _ev(url: str = "https://example.com/p", observed: datetime | None = None, **lab: object):
    ev = PageEvidence(url=url)
    ev.lab_performance = LabPerformance(
        strategy="mobile", observed_at=observed or NOW, **lab  # type: ignore[arg-type]
    )
    return ev


def _crux(metric: str, percentile: float, category: str, level: str = "origin") -> dict:
    return {
        level: {
            "available": True,
            "metrics": {metric: {"percentile": percentile, "category": category}},
        }
    }


# 1. freshness ---------------------------------------------------------------


def test_window_is_thirty_days_and_a_31_day_old_run_is_n_a() -> None:
    assert LAB_PERFORMANCE_MAX_AGE_DAYS == 30
    old = NOW - timedelta(days=31)
    for check, kw in (
        (check_cwv_lcp, {"lcp_ms": 3200.0}),
        (check_cwv_cls, {"cls": 0.8}),
        (check_cwv_inp_tbt, {"tbt_ms": 900.0}),
    ):
        outcome = check(_ev(observed=old, **kw))
        assert outcome.status == "n_a"
        assert outcome.remediation is not None
    assert check_cwv_lcp(_ev(observed=NOW - timedelta(days=10), lcp_ms=3200.0)).status == "warn"


# 2. field first -------------------------------------------------------------


def test_field_fast_overrides_a_failing_lab_number() -> None:
    lab = lab_performance_from_lighthouse(
        {"metrics": {"lcp_ms": {"numeric_value": 15000}, "cls": {"numeric_value": 0.8},
                     "tbt_ms": {"numeric_value": 1100}}},
        strategy="mobile",
        observed_at=NOW,
        crux={
            "origin": {
                "available": True,
                "metrics": {
                    "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2100, "category": "FAST"},
                    "INTERACTION_TO_NEXT_PAINT": {"percentile": 89, "category": "FAST"},
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 5, "category": "FAST"},
                },
            }
        },
    )
    ev = PageEvidence(url="https://example.com/")
    ev.lab_performance = lab
    for check in (check_cwv_lcp, check_cwv_inp_tbt, check_cwv_cls):
        outcome = check(ev)
        assert outcome.status == "pass", outcome.reasoning
        assert "real visitors" in outcome.reasoning
        assert outcome.evidence["source"] == "field"


def test_field_slow_fails_even_when_lab_is_fine() -> None:
    ev = _ev(lcp_ms=1000.0, field_metrics={"lcp_ms": {"value": 6000.0, "category": "SLOW", "level": "page"}})
    outcome = check_cwv_lcp(ev)
    assert outcome.status == "fail"
    assert "real visitors to this page" in outcome.reasoning


def test_lab_only_is_labelled_an_estimate_and_tbt_is_not_a_ranking_signal() -> None:
    lcp = check_cwv_lcp(_ev(lcp_ms=6000.0))
    assert "simulated phone test on" in lcp.reasoning
    assert "lab estimate" in lcp.reasoning
    tbt = check_cwv_inp_tbt(_ev(tbt_ms=900.0))
    assert "ranking signal" in tbt.reasoning and "not itself a ranking signal" in tbt.reasoning
    assert "measures it directly" not in tbt.reasoning
    assert "simulated phone test on" in tbt.reasoning


# 3. asset_delivery ----------------------------------------------------------


def test_asset_delivery_headlines_the_largest_single_saving_not_the_sum() -> None:
    audits = {"render-blocking-insight": 2100.0, "document-latency-insight": 950.0,
              "unused-css-rules": 750.0}
    outcome = check_asset_delivery(_ev(delivery_savings_ms=sum(audits.values()), delivery_audits=audits))
    assert "files that block the page from drawing" in outcome.reasoning
    assert "2.1s" in outcome.reasoning
    assert "3.8s" not in outcome.reasoning and "3.9s" not in outcome.reasoning
    assert "not additive" in outcome.reasoning
    assert outcome.evidence["largest_saving_audit"] == "render-blocking-insight"


# 4. caching -----------------------------------------------------------------


def test_third_party_files_are_listed_never_judged() -> None:
    resources = [
        {"url": "https://connect.facebook.net/fbevents.js", "cache_lifetime_ms": 0, "total_bytes": 900_000},
        {"url": "https://static.cloudflareinsights.com/b.js", "cache_lifetime_ms": 0, "total_bytes": 90_000},
    ]
    outcome = check_caching_policy(
        _ev(cache_static_bytes=1_000_000.0, cache_short_ttl_resources=resources,
            cache_static_bytes_by_host={"example.com": 10_000_000 / 10, "connect.facebook.net": 900_000.0})
    )
    assert outcome.status == "pass"
    assert "not yours to change" in outcome.reasoning
    assert outcome.evidence["third_party_hosts"]


def test_own_cdn_subdomain_is_first_party() -> None:
    resources = [{"url": "https://cdn.example.com/a.js", "cache_lifetime_ms": 0, "total_bytes": 800_000}]
    outcome = check_caching_policy(_ev(cache_static_bytes=1_000_000.0, cache_short_ttl_resources=resources))
    assert outcome.status == "fail"


def test_provider_cap_is_reported_as_at_least() -> None:
    resources = [{"url": f"https://example.com/{i}.js", "cache_lifetime_ms": 0, "total_bytes": 20_000}
                 for i in range(50)]
    lab = lab_performance_from_lighthouse(
        {"delivery": {"cache": {"measured": True, "static_bytes": 2_000_000.0,
                                "short_ttl_resources": resources}}},
        strategy="mobile", observed_at=NOW,
    )
    ev = PageEvidence(url="https://example.com/")
    ev.lab_performance = lab
    outcome = check_caching_policy(ev)
    assert "at least 50 files" in outcome.reasoning
    assert outcome.reasoning.startswith("At least")


def test_provider_flags_truncation_and_records_bytes_by_host() -> None:
    items = [{"url": f"https://example.com/{i}.js", "cacheLifetimeMs": 0, "totalBytes": 10}
             for i in range(60)]
    facts = _delivery_facts({
        "cache-insight": {"details": {"items": items}},
        "network-requests": {"details": {"items": [
            {"url": "https://example.com/a.js", "resourceType": "Script", "transferSize": 100},
            {"url": "https://t.example.net/b.js", "resourceType": "Script", "transferSize": 50},
        ]}},
    })
    cache = facts["cache"] if "cache" in facts else facts
    assert cache["short_ttl_truncated"] is True
    assert len(cache["short_ttl_resources"]) == 50
    assert cache["static_bytes_by_host"] == {"example.com": 100.0, "t.example.net": 50.0}


# 5. ttfb --------------------------------------------------------------------


def test_ttfb_names_the_measured_date_and_stale_samples_are_n_a() -> None:
    fresh = PageEvidence(url="https://example.com/", ttfb_ms=1200, ttfb_measured_at=NOW)
    out = check_ttfb_server_response(fresh)
    assert f"measured {NOW.date().isoformat()}" in out.reasoning
    stale = PageEvidence(url="https://example.com/", ttfb_ms=5518,
                         ttfb_measured_at=NOW - timedelta(days=60))
    out = check_ttfb_server_response(stale)
    assert out.status == "n_a" and out.remediation is not None


def test_ttfb_never_falls_back_to_total_elapsed_time() -> None:
    ev = PageEvidence(url="https://example.com/", response_time_ms=26276)
    assert check_ttfb_server_response(ev).status == "n_a"


# 6. image_modern_format ----------------------------------------------------


def _img(src: str, size: int) -> dict:
    return {"src": src, "final_url": src, "bytes": size, "capture_status": "complete",
            "actual_format": "jpeg"}


def _image_ev(items: list[dict]) -> PageEvidence:
    from matrx_scraper import seo_audit

    ev = PageEvidence(url="https://example.com/")
    ev.image_inventory = items  # type: ignore[attr-defined]
    return ev


def test_tracking_pixel_is_not_an_image_and_tiny_pages_pass(monkeypatch) -> None:
    from matrx_scraper import seo_audit

    def run(items):
        ev = PageEvidence(url="https://example.com/")
        monkeypatch.setattr(seo_audit, "_inventory_or_reason", lambda e: (items, None))
        return check_image_modern_format(ev)

    tiny = run([_img("https://example.com/a.jpg", 20_000)])
    assert tiny.status == "pass"
    pixel = run([_img("https://px.ads.linkedin.com/collect/?fmt=gif", 200_000)])
    assert pixel.status == "n_a"
    big = run([_img("https://example.com/hero.jpg", 400_000)])
    assert big.status in {"warn", "fail"}
