"""No check may RAISE on a real `PageFacts` — a crash is a silently lost rule.

The sweep runs every registry entry against a `PageFacts` built by
`analysis._extract_page_facts` from a live snapshot. `PageFacts` is not the
`PageEvidence` the per-page checks are unit-tested against: it is assembled from
snapshot jsonb, so a check can read a field the evidence class has and the facts
class does not. That failure is invisible — the check raises, the sweep drops
that one verdict, and the catalogue row simply never gets a result row. It looks
exactly like "nothing to report".

Both halves of this actually happened on 2026-08-09, hours apart, while the
whole suite stayed green:

  * `image_modern_format` → `NameError: _image_format is not defined`  (318/321 pages)
  * `ttfb_server_response` → `AttributeError: 'PageFacts' has no attribute 'ttfb_ms'`  (321/321)

The existing per-check tests could not catch either, because they build
`PageEvidence` directly and never go through the fact extractor. These tests
close that seam: every check, over a fully-populated snapshot AND over an empty
legacy one, must return a verdict. A check with no evidence answers `n_a` — it
never explodes.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_scraper.seo_audit import PAGE_CHECKS as SEO_PAGE_CHECKS
from matrx_scraper.web_crawl import analysis
from matrx_scraper.web_crawl.analysis import PAGE_CHECKS as SWEEP_CHECKS, SiteAggregates

VALID_STATUSES = {"pass", "warn", "fail", "n_a"}


def _page():
    return SimpleNamespace(id="11111111-1111-1111-1111-111111111111", url="https://example.com/a")


def _rich_snapshot():
    """A snapshot carrying every evidence field the extractor knows how to read."""
    return SimpleNamespace(
        id="22222222-2222-2222-2222-222222222222",
        head_tags={
            "title": "A perfectly reasonable page title for testing purposes",
            "meta_description": (
                "A meta description of an entirely unremarkable length that sits "
                "comfortably inside the recommended window for search snippets."
            ),
            "meta_robots": "index, follow",
            "canonical_url": "https://example.com/a",
        },
        seo_metrics={"title": {"ok": True}, "description": {"ok": True}},
        audit_metrics={
            "indexability": {"canonical_matches": True, "noindex": False, "nofollow": False},
            "headings": {"h1_count": 1},
        },
        headings={"h1_count": 1, "all": [{"level": 1, "text": "Heading"}]},
        images={
            "items": [
                {
                    "src": "https://example.com/a.webp",
                    "alt": "descriptive alt",
                    "width": 800,
                    "height": 600,
                    "loading": "lazy",
                }
            ]
        },
        extracted={
            "redirect_chain": [],
            "mixed_content": [],
            "pagination": {},
            "response_headers": {"strict-transport-security": "max-age=63072000"},
            "text_bytes": 4096,
            "fingerprint": {"version": 1, "exact_sha256": "a" * 64},
        },
        structured_data={"schema_types": ["Article"]},
        perf={"bytes": 128_000, "response_time_ms": 900, "ttfb_ms": 210},
        word_count=1200,
        http_status=200,
    )


def _empty_snapshot():
    """The legacy snapshot: captured before half these fields existed."""
    return SimpleNamespace(
        id="33333333-3333-3333-3333-333333333333",
        head_tags=None,
        seo_metrics=None,
        audit_metrics=None,
        headings=None,
        images=None,
        extracted=None,
        structured_data=None,
        perf=None,
        word_count=None,
        http_status=None,
    )


@pytest.fixture(params=["rich", "empty"])
def facts(request):
    snapshot = _rich_snapshot() if request.param == "rich" else _empty_snapshot()
    return analysis._extract_page_facts(_page(), snapshot)


@pytest.mark.parametrize("key", sorted(SEO_PAGE_CHECKS))
def test_per_page_check_never_raises_on_real_page_facts(key, facts):
    """`PageFacts` must satisfy every per-page check's read surface."""
    outcome = SEO_PAGE_CHECKS[key](facts)
    assert outcome.status in VALID_STATUSES, f"{key} returned {outcome.status!r}"


@pytest.mark.parametrize("key", sorted(SWEEP_CHECKS))
def test_sweep_registry_check_never_raises(key, facts):
    """The same guarantee through the sweep's own registry, cross-page included."""
    outcome = SWEEP_CHECKS[key](facts, SiteAggregates())
    assert outcome.status in VALID_STATUSES, f"{key} returned {outcome.status!r}"


def test_missing_evidence_is_an_n_a_not_a_crash(facts):
    """An empty snapshot must produce verdicts for every check, never an error."""
    outcomes = {key: check(facts, SiteAggregates()) for key, check in SWEEP_CHECKS.items()}
    assert len(outcomes) == len(SWEEP_CHECKS)
    assert all(o.status in VALID_STATUSES for o in outcomes.values())


def test_ttfb_is_read_from_ttfb_ms_and_never_backfilled():
    """The exact regression: `ttfb_ms` must reach `PageFacts` from `perf`.

    It must also stay independent of `response_time_ms` — back-filling one from
    the other scores a fast server as slow on a heavy page.
    """
    snapshot = _rich_snapshot()
    snapshot.perf = {"bytes": 128_000, "response_time_ms": 9_000}
    facts = analysis._extract_page_facts(_page(), snapshot)
    assert facts.ttfb_ms is None, "ttfb_ms was back-filled from response_time_ms"
    assert SEO_PAGE_CHECKS["ttfb_server_response"](facts).status == "n_a"

    snapshot.perf = {"bytes": 128_000, "response_time_ms": 9_000, "ttfb_ms": 120}
    facts = analysis._extract_page_facts(_page(), snapshot)
    assert facts.ttfb_ms == 120
    assert SEO_PAGE_CHECKS["ttfb_server_response"](facts).status == "pass"
