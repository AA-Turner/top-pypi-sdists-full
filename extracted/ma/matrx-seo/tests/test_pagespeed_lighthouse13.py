"""Lighthouse 13 capture — the delivery + caching evidence must survive PSI.

🚨 Why this file exists. PageSpeed Insights now runs Lighthouse 13, which
RENAMED the entire performance-opportunity family: `render-blocking-resources`,
`uses-text-compression` and `uses-long-cache-ttl` no longer exist, their
successors are the `*-insight` audits, and every one of them reports
`scoreDisplayMode: "metricSavings"`. That mode was missing from this module's
keep-list, so PSI's whole delivery fix-list was discarded before it ever
reached `seo.page_performance` — silently, with a green test suite, because the
only fixture in the repo was a Lighthouse 12 payload.

So: the fixture below is a REAL Lighthouse 13.4.1 response (trimmed, captured
live from `https://www.wikipedia.org/` on 2026-08-09), and these tests assert
against the audit ids PSI actually serves today. The Lighthouse 12 fixture in
`test_pagespeed_provider.py` stays — it pins backward compatibility — but it can
no longer be the only evidence.

Consumers: `matrx_scraper.seo_audit`'s `asset_delivery` / `caching_policy`
catalogue checks read exactly the shape produced here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from matrx_seo.providers.pagespeed import _delivery_facts, _diagnostic_audits

FIXTURE = Path(__file__).parent / "fixtures/pagespeed/mobile_lighthouse13.json"


@pytest.fixture(scope="module")
def audits() -> dict[str, Any]:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return payload["lighthouseResult"]["audits"]


def test_fixture_is_a_lighthouse_13_payload() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    version = payload["lighthouseResult"]["lighthouseVersion"]
    assert version.startswith("13."), version


def test_lighthouse_12_opportunity_names_are_gone(audits: dict[str, Any]) -> None:
    """The regression guard: if these ever come back, the mapping below is stale."""
    for retired in ("render-blocking-resources", "uses-text-compression", "uses-long-cache-ttl"):
        assert retired not in audits


def test_metric_savings_audits_are_captured_not_dropped(audits: dict[str, Any]) -> None:
    diagnostics = _diagnostic_audits(audits)
    assert "cache-insight" in diagnostics
    entry = diagnostics["cache-insight"]
    assert entry["score_display_mode"] == "metricSavings"
    # The savings are the whole point — a captured audit with no numbers is
    # the same data loss wearing a key.
    assert entry["metric_savings"]["LCP"] > 0


def test_delivery_savings_are_summed_from_the_insight_audits(audits: dict[str, Any]) -> None:
    delivery = _delivery_facts(audits)
    assert "render-blocking-insight" in delivery["audits"]
    assert "image-delivery-insight" in delivery["audits"]
    # Wikipedia's portal has exactly one delivery opportunity: its logo image.
    assert delivery["audits"]["image-delivery-insight"]["savings_ms"] == 150.0
    assert delivery["total_savings_ms"] == pytest.approx(
        sum(entry["savings_ms"] for entry in delivery["audits"].values())
    )


def test_caching_is_not_double_charged_to_delivery(audits: dict[str, Any]) -> None:
    """`cache-insight` has its own catalogue item; counting it twice would
    penalise one defect under two scores."""
    delivery = _delivery_facts(audits)
    assert "cache-insight" not in delivery["audits"]
    assert delivery["cache"]["measured"] is True


def test_cache_facts_carry_the_denominator_and_the_offenders(audits: dict[str, Any]) -> None:
    cache = _delivery_facts(audits)["cache"]
    # The denominator counts static assets only — never the HTML document,
    # which is normally uncacheable by design.
    document_bytes = 32162
    assert cache["static_bytes"] > 0
    assert cache["static_bytes"] != document_bytes
    assert cache["static_requests"] >= 1
    offender = cache["short_ttl_resources"][0]
    assert set(offender) == {"url", "cache_lifetime_ms", "total_bytes"}
    assert offender["cache_lifetime_ms"] > 0


def test_a_payload_with_no_delivery_audits_reports_nothing_rather_than_zero() -> None:
    delivery = _delivery_facts({})
    assert delivery["audits"] == {}
    assert delivery["cache"]["measured"] is False


def test_savings_never_double_count_one_metric_against_another() -> None:
    """`metricSavings: {LCP: 300, FCP: 300}` is 300ms of work, not 600."""
    delivery = _delivery_facts(
        {
            "render-blocking-insight": {
                "scoreDisplayMode": "metricSavings",
                "score": 0,
                "metricSavings": {"LCP": 300, "FCP": 300},
            }
        }
    )
    assert delivery["total_savings_ms"] == 300.0


def test_pre_13_overall_savings_still_read() -> None:
    """A stored Lighthouse 12 response must keep scoring after the upgrade."""
    delivery = _delivery_facts(
        {
            "unused-javascript": {
                "scoreDisplayMode": "numeric",
                "score": 0,
                "details": {"overallSavingsMs": 450, "overallSavingsBytes": 91_000},
            }
        }
    )
    assert delivery["audits"]["unused-javascript"]["savings_ms"] == 450.0
    assert delivery["audits"]["unused-javascript"]["wasted_bytes"] == 91_000.0
