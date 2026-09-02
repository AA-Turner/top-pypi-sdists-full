"""The `security` catalogue category — every band, and every missing-evidence path.

Four checks, two subjects. `https_enforcement` is per-page (a single http://
page on an HTTPS site is the defect, so the verdict belongs to the page);
`tls_certificate`, `hsts_policy` and `security_headers` describe the HOST and
are recorded against the site.

The rule these tests exist to enforce is the one that makes a security check
worth anything: **a check never passes on evidence nobody collected.** A page
the site probe never sampled has no http:// verdict of its own, so that path
must answer `n_a` — naming what is missing — and must never answer `pass`.

Since 2026-08-13 the site probe DOES sample real page paths (`site_probe.
page_http_variants`), and `analysis.stamp_http_variant_evidence` decides which
evidence each page gets: its OWN probe when sampled, the site's http:// ORIGIN
probe otherwise. Those tests live here too, because the whole reason the
selection exists is that stamping the origin on every page scored a live
insecure deep path as `pass`.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from matrx_scraper.seo_audit import (
    HTTP_VARIANT_PERMANENT_REDIRECTS,
    SECURITY_RESPONSE_HEADERS,
    CheckOutcome,
    PageEvidence,
    RECRAWL_SITE,
    check_https_enforcement,
    security_response_headers,
)
from matrx_scraper.web_crawl.analysis import (
    BASELINE_SECURITY_HEADERS,
    HSTS_MIN_MAX_AGE_SECONDS,
    SECURITY_HEADER_MIN_SCORE,
    SECURITY_HEADER_MISSING_PENALTY,
    SECURITY_HEADER_SAMPLE_LIMIT,
    SITE_CHECKS,
    TLS_EXPIRY_CRITICAL_DAYS,
    TLS_EXPIRY_WARN_DAYS,
    PageFacts,
    SiteFacts,
    TlsFacts,
    _build_site_facts,
    _tls_facts_from_probe,
    stamp_http_variant_evidence,
)
from matrx_scraper.web_crawl.site_probe import SiteProbe, TlsCapture, UrlProbe

ALL_BASELINE = {
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "referrer-policy": "strict-origin-when-cross-origin",
    "content-security-policy": "default-src 'self'",
}
STRONG_HSTS = f"max-age={HSTS_MIN_MAX_AGE_SECONDS}; includeSubDomains"


def assert_db_valid(outcome: CheckOutcome) -> None:
    """Mirror of `analysis_result_status_score_valid` + `_status_valid`."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


def site(**overrides) -> SiteFacts:
    headers = overrides.pop(
        "headers", dict(ALL_BASELINE) | {"strict-transport-security": STRONG_HSTS}
    )
    pages = overrides.pop("pages", 3)
    facts = SiteFacts(site_id="site-1", https_pages=pages, **overrides)
    if headers is not None:
        facts.header_samples = [(f"https://example.com/{i}", dict(headers)) for i in range(pages)]
        facts.pages_with_evidence = pages
    return facts


# ---------------------------------------------------------------------------
# https_enforcement — page subject, weight 3.0


def page(url: str = "https://example.com/a", **overrides) -> PageEvidence:
    return PageEvidence(url=url, **overrides)


def test_http_page_is_the_catalogue_fail():
    outcome = check_https_enforcement(page("http://example.com/a"))
    assert (outcome.status, outcome.score) == ("fail", 5)
    assert_db_valid(outcome)


def test_https_without_a_probe_is_n_a_not_a_pass():
    """No http:// verdict for this page — nothing sampled it, nothing probed it.

    Passing here would claim "the HTTP duplicate redirects permanently" on
    evidence that was never collected. This is the whole point of the category.
    """
    outcome = check_https_enforcement(page())
    assert outcome.status == "n_a" and outcome.score is None
    # The wording is user-facing prose and may be reworded; what may NEVER
    # change is that it says the insecure copy is UNKNOWN, not absent.
    assert "insecure" in outcome.reasoning.lower()


@pytest.mark.parametrize("status", sorted(HTTP_VARIANT_PERMANENT_REDIRECTS))
def test_permanent_redirect_from_http_is_the_full_score(status):
    outcome = check_https_enforcement(
        page(http_variant_probe={"status": status, "location": "https://example.com/a"})
    )
    assert (outcome.status, outcome.score) == ("pass", 100)


@pytest.mark.parametrize("status", (302, 303, 307))
def test_temporary_redirect_from_http_scores_seventy(status):
    outcome = check_https_enforcement(
        page(http_variant_probe={"status": status, "location": "https://example.com/a"})
    )
    assert (outcome.status, outcome.score) == ("warn", 70)


@pytest.mark.parametrize("status", (200, 204))
def test_live_http_duplicate_scores_thirty(status):
    outcome = check_https_enforcement(page(http_variant_probe={"status": status}))
    assert (outcome.status, outcome.score) == ("fail", 30)


def test_redirect_that_stays_on_http_is_not_enforcement():
    outcome = check_https_enforcement(
        page(http_variant_probe={"status": 301, "location": "http://example.com/b"})
    )
    assert (outcome.status, outcome.score) == ("fail", 30)


def test_unreachable_http_variant_passes():
    """404/410/0 on http:// means no insecure duplicate exists to consolidate."""
    for status in (404, 410, 0, 500):
        outcome = check_https_enforcement(page(http_variant_probe={"status": status}))
        assert outcome.status == "pass", status
        assert_db_valid(outcome)


def test_a_non_http_url_is_n_a():
    assert check_https_enforcement(page("ftp://example.com/a")).status == "n_a"


def test_a_malformed_probe_is_n_a():
    for probe in ({}, {"status": "301"}, {"location": "https://example.com/a"}):
        assert check_https_enforcement(page(http_variant_probe=probe)).status == "n_a"


# ---------------------------------------------------------------------------
# Which http:// evidence each page gets — page probe first, origin as fallback


def _facts(url: str) -> PageFacts:
    return PageFacts(page_id=url, url=url)


def _probe_with(page_variants: list[UrlProbe], root_variants: list[UrlProbe]) -> SiteProbe:
    return SiteProbe(
        captured_at="2026-08-13T00:00:00+00:00",
        root_url="https://example.com/",
        variants=root_variants,
        page_http_variants=page_variants,
    )


ROOT_REDIRECTS = UrlProbe(
    url="http://example.com/",
    http_status=301,
    final_url="https://example.com/",
    final_status=200,
)


def test_a_sampled_page_is_scored_from_its_own_probe_not_the_origin():
    """The defect, pinned: the root redirects, the deep path does not.

    Stamping the origin here scored this page `pass` while an insecure copy of
    it was live — the entire reason the per-page probe exists.
    """
    live_http_page = UrlProbe(
        url="http://example.com/deep",
        http_status=200,
        final_url="http://example.com/deep",
        final_status=200,
    )
    facts = _facts("https://example.com/deep")
    degraded = stamp_http_variant_evidence(
        [facts], _probe_with([live_http_page], [ROOT_REDIRECTS]), "https://example.com/"
    )

    assert degraded is None
    assert facts.http_variant_probe["scope"] == "page"
    outcome = check_https_enforcement(facts)
    assert (outcome.status, outcome.score) == ("fail", 30)


def test_an_unsampled_page_falls_back_to_the_origin_and_says_so():
    sampled = _facts("https://example.com/deep")
    unsampled = _facts("https://example.com/other")
    probe = _probe_with(
        [UrlProbe(url="http://example.com/deep", http_status=301, final_url="https://x/")],
        [ROOT_REDIRECTS],
    )
    degraded = stamp_http_variant_evidence([sampled, unsampled], probe, "https://example.com/")

    assert degraded is None  # at least one page carries real page evidence
    assert sampled.http_variant_probe["scope"] == "page"
    assert unsampled.http_variant_probe["scope"] == "origin"


def test_no_page_probe_at_all_is_loud_but_never_fatal():
    facts = _facts("https://example.com/deep")
    degraded = stamp_http_variant_evidence(
        [facts], _probe_with([], [ROOT_REDIRECTS]), "https://example.com/"
    )

    assert degraded is not None and "ORIGIN" in degraded
    # Loud, but the sweep still scores — on the weaker evidence, labelled.
    assert facts.http_variant_probe["scope"] == "origin"
    assert check_https_enforcement(facts).status == "pass"


def test_no_probe_at_all_leaves_the_check_on_its_n_a_path():
    facts = _facts("https://example.com/deep")
    degraded = stamp_http_variant_evidence([facts], None, "https://example.com/")

    assert degraded is not None
    assert facts.http_variant_probe is None
    assert check_https_enforcement(facts).status == "n_a"


# ---------------------------------------------------------------------------
# security_headers — site subject, formula: 100 - 15 per missing, floor 40


def test_all_baseline_headers_present_passes():
    outcome = SITE_CHECKS["security_headers"](site())
    assert (outcome.status, outcome.score) == ("pass", 100)
    assert_db_valid(outcome)


@pytest.mark.parametrize("missing_count", (1, 2, 3, 4))
def test_the_score_is_the_rows_formula(missing_count):
    headers = dict(ALL_BASELINE)
    for name in BASELINE_SECURITY_HEADERS[:missing_count]:
        headers.pop(name)
    outcome = SITE_CHECKS["security_headers"](site(headers=headers))
    expected = max(SECURITY_HEADER_MIN_SCORE, 100 - SECURITY_HEADER_MISSING_PENALTY * missing_count)
    assert (outcome.status, outcome.score) == ("warn", expected)
    assert outcome.issue_count == missing_count


def test_csp_frame_ancestors_substitutes_for_x_frame_options():
    headers = dict(ALL_BASELINE)
    headers.pop("x-frame-options")
    headers["content-security-policy"] = "default-src 'self'; frame-ancestors 'none'"
    outcome = SITE_CHECKS["security_headers"](site(headers=headers))
    assert (outcome.status, outcome.score) == ("pass", 100)


def test_a_header_on_only_some_pages_counts_as_missing():
    """Partial coverage IS the defect sampling exists to catch."""
    facts = site()
    facts.header_samples[1] = (
        facts.header_samples[1][0],
        {k: v for k, v in facts.header_samples[1][1].items() if k != "referrer-policy"},
    )
    outcome = SITE_CHECKS["security_headers"](facts)
    assert outcome.status == "warn"
    assert outcome.evidence["missing_headers"] == ["referrer-policy"]
    assert "some pages but not all" in outcome.reasoning


def test_no_captured_headers_is_n_a():
    outcome = SITE_CHECKS["security_headers"](SiteFacts(site_id="site-1", https_pages=3))
    assert outcome.status == "n_a" and outcome.score is None
    assert "re-crawl" in outcome.reasoning


# ---------------------------------------------------------------------------
# hsts_policy — site subject


def test_strong_hsts_passes():
    outcome = SITE_CHECKS["hsts_policy"](site())
    assert (outcome.status, outcome.score) == ("pass", 100)
    assert outcome.evidence["include_subdomains"] is True


def test_missing_include_subdomains_still_passes_but_says_so():
    outcome = SITE_CHECKS["hsts_policy"](
        site(
            headers=dict(ALL_BASELINE)
            | {"strict-transport-security": f"max-age={HSTS_MIN_MAX_AGE_SECONDS}"}
        )
    )
    assert outcome.status == "pass"
    assert "includeSubDomains" in outcome.reasoning


def test_short_max_age_scores_seventy_five():
    outcome = SITE_CHECKS["hsts_policy"](
        site(
            headers=dict(ALL_BASELINE)
            | {"strict-transport-security": f"max-age={HSTS_MIN_MAX_AGE_SECONDS - 1}"}
        )
    )
    assert (outcome.status, outcome.score) == ("warn", 75)


def test_no_hsts_header_scores_fifty_five():
    outcome = SITE_CHECKS["hsts_policy"](site(headers=dict(ALL_BASELINE)))
    assert (outcome.status, outcome.score) == ("warn", 55)


def test_hsts_without_a_readable_max_age_scores_fifty_five():
    outcome = SITE_CHECKS["hsts_policy"](
        site(headers=dict(ALL_BASELINE) | {"strict-transport-security": "includeSubDomains"})
    )
    assert (outcome.status, outcome.score) == ("warn", 55)


def test_the_weakest_sampled_page_sets_the_verdict():
    facts = site()
    facts.header_samples[2] = (
        facts.header_samples[2][0],
        dict(ALL_BASELINE) | {"strict-transport-security": "max-age=60"},
    )
    outcome = SITE_CHECKS["hsts_policy"](facts)
    assert (outcome.status, outcome.score) == ("warn", 75)
    assert outcome.evidence["min_max_age_seconds"] == 60


def test_hsts_is_n_a_without_headers_and_on_an_http_only_site():
    assert SITE_CHECKS["hsts_policy"](SiteFacts(site_id="s", https_pages=2)).status == "n_a"
    http_only = site(pages=2)
    http_only.https_pages = 0
    http_only.http_pages = 2
    outcome = SITE_CHECKS["hsts_policy"](http_only)
    assert outcome.status == "n_a" and "https_enforcement" in outcome.reasoning


# ---------------------------------------------------------------------------
# tls_certificate — site subject. Nothing captures the evidence yet.


def test_tls_without_capture_is_n_a_and_names_the_gap():
    outcome = SITE_CHECKS["tls_certificate"](site())
    assert outcome.status == "n_a" and outcome.score is None
    assert "capture" in outcome.reasoning.lower()
    assert outcome.remediation is RECRAWL_SITE


@pytest.mark.parametrize(
    "tls",
    (
        TlsFacts(days_to_expiry=-1, expired=True),
        TlsFacts(days_to_expiry=200, trusted=False),
        TlsFacts(days_to_expiry=200, hostname_match=False),
    ),
)
def test_unusable_certificate_scores_one(tls):
    outcome = SITE_CHECKS["tls_certificate"](site(tls=tls))
    assert (outcome.status, outcome.score) == ("fail", 1)
    assert_db_valid(outcome)


def test_expiry_proximity_bands():
    check = SITE_CHECKS["tls_certificate"]
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_CRITICAL_DAYS))).score == 20
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_CRITICAL_DAYS + 1))).score == 50
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_WARN_DAYS))).score == 50
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_WARN_DAYS + 1))).score == 100
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_CRITICAL_DAYS))).status == "fail"
    assert check(site(tls=TlsFacts(days_to_expiry=TLS_EXPIRY_WARN_DAYS))).status == "warn"
    assert check(site(tls=TlsFacts(days_to_expiry=90))).status == "pass"


def test_certificate_with_no_expiry_date_is_n_a():
    outcome = SITE_CHECKS["tls_certificate"](site(tls=TlsFacts()))
    assert outcome.status == "n_a" and outcome.score is None
    assert outcome.remediation is RECRAWL_SITE


def test_persisted_probe_certificate_becomes_scored_tls_facts():
    probe = SiteProbe(
        captured_at="2026-08-11T00:00:00+00:00",
        root_url="https://example.com/",
        tls=TlsCapture(
            hostname="example.com",
            trusted=True,
            hostname_match=True,
            expired=False,
            issuer="organizationName=Example CA",
            not_after="2026-09-10T00:00:00+00:00",
        ),
    )
    facts = _tls_facts_from_probe(
        probe,
        computed_at=datetime(2026, 8, 11, tzinfo=UTC),
    )

    assert facts is not None
    assert facts.days_to_expiry == 30
    assert facts.issuer == "organizationName=Example CA"
    assert SITE_CHECKS["tls_certificate"](site(tls=facts)).score == 100


# ---------------------------------------------------------------------------
# The evidence pipeline: capture -> snapshot -> site facts


def test_only_allowlisted_headers_survive_capture():
    """`set-cookie` and friends must never reach a persisted snapshot."""
    kept = security_response_headers(
        {
            "Strict-Transport-Security": "  max-age=1  ",
            "Set-Cookie": "session=secret",
            "Authorization": "Bearer nope",
            "X-Frame-Options": "DENY",
        }
    )
    assert kept == {"strict-transport-security": "max-age=1", "x-frame-options": "DENY"}
    assert "set-cookie" not in SECURITY_RESPONSE_HEADERS
    assert security_response_headers(None) == {}
    assert security_response_headers({}) == {}


def test_site_facts_fold_page_evidence():
    pages = [
        PageFacts(page_id="1", url="https://example.com/a", response_headers=dict(ALL_BASELINE)),
        PageFacts(page_id="2", url="http://example.com/b", response_headers={}),
        PageFacts(page_id="3", url="https://example.com/c"),  # never captured
    ]
    facts = _build_site_facts("site-1", pages)
    assert (facts.https_pages, facts.http_pages) == (2, 1)
    assert facts.pages_with_evidence == 2
    assert [url for url, _ in facts.header_samples] == [
        "https://example.com/a",
        "http://example.com/b",
    ]


def test_header_sampling_is_capped():
    pages = [
        PageFacts(
            page_id=str(i), url=f"https://example.com/{i}", response_headers=dict(ALL_BASELINE)
        )
        for i in range(SECURITY_HEADER_SAMPLE_LIMIT + 10)
    ]
    facts = _build_site_facts("site-1", pages)
    assert len(facts.header_samples) == SECURITY_HEADER_SAMPLE_LIMIT
    assert facts.pages_with_evidence == SECURITY_HEADER_SAMPLE_LIMIT + 10


def test_every_site_check_survives_completely_empty_evidence():
    empty = SiteFacts(site_id="site-1")
    for key, check in SITE_CHECKS.items():
        outcome = check(empty)
        assert_db_valid(outcome)
        assert outcome.status == "n_a", f"{key} answered {outcome.status} on no evidence at all"
