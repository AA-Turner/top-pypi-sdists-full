#!/usr/bin/env python
"""Generate the per-page CHECK parity fixture (Python → matrx-frontend).

`matrx_scraper/seo_audit.py` owns every per-page SEO VERDICT. matrx-frontend
`features/marketing/seo/audit/checks.ts` is its byte-identical browser mirror,
so a UI can say "this title is too long — warn, score 60" without a round trip
and without re-inventing the rules in TSX.

This script runs `run_page_checks` over a table of evidence cases and dumps
what the Python answered. The frontend test
(`features/marketing/seo/audit/checks.parity.test.ts`) replays the same
evidence through `runPageChecks` and asserts identical output — status, score,
issue count, evidence payload, and the reasoning string character for
character. If it fails, ONE SIDE CHANGED WITHOUT THE OTHER: fix both in the
same unit of work and regenerate.

Same recipe as `generate_seo_audit_parity_fixture.py` (evidence layer) and the
`meta_metrics` / `audit_metrics` fixtures (metrics layer); this is the check
layer.

Run from the aidream repo root:
    .venv/bin/python packages/matrx-scraper/scripts/generate_page_checks_parity_fixture.py

Writes (committed):
    ../matrx-frontend/features/marketing/seo/audit/__fixtures__/page-checks-parity.json
"""

from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "packages" / "matrx-scraper"))

from matrx_scraper.meta_metrics import (  # noqa: E402
    calculate_meta_description_metrics,
    calculate_meta_title_metrics,
)
from matrx_scraper.seo_audit import (  # noqa: E402
    LabPerformance,
    PageEvidence,
    run_page_checks,
)

URL = "https://example.com/guides/seo-basics"

GOOD_TITLE = "SEO Basics: A Practical Guide for Teams"
GOOD_DESCRIPTION = (
    "A practical, example-led introduction to technical SEO for product teams "
    "who ship changes every week and need the basics right."
)
LONG_TITLE = (
    "The Complete, Exhaustive, Definitive and Frankly Overlong Guide to "
    "Every Single Aspect of Technical Search Engine Optimization"
)
SHORT_DESCRIPTION = "Too short."


# --- Full-evidence defaults -------------------------------------------------
#
# `healthy()` must carry EVERY field a check reads, or a check whose evidence
# is absent answers `n_a` in every case and the fixture only ever proves its
# "we haven't measured this" branch. Each defect case then removes or spoils
# exactly one of these.
#
# ⚠️ `observed_at` on the lab measurement is deliberately None. The staleness
# branch prints an age in days computed at RUN time, so a dated fixture would
# bake Python's answer today and disagree with the TypeScript tomorrow.

HEALTHY_HEADINGS: list[dict[str, Any]] = [
    {"level": 1, "text": "SEO Basics"},
    {"level": 2, "text": "Why it matters"},
    {"level": 3, "text": "Titles and descriptions"},
    {"level": 2, "text": "Where to start"},
]

HEALTHY_OG: dict[str, str] = {
    "og:title": "SEO Basics",
    "og:description": "A practical introduction to technical SEO.",
    "og:image": "https://cdn.example.com/share.png",
    "og:url": URL,
    "og:type": "article",
}

HEALTHY_HREFLANG: list[dict[str, Any]] = [
    {"lang": "en", "href": URL},
    {"lang": "es", "href": "https://example.com/es/guias/seo-basico"},
    {"lang": "x-default", "href": URL},
]


def healthy_images() -> list[dict[str, Any]]:
    """Eight images: correct dimensions, modern formats, fold-aware loading."""
    items: list[dict[str, Any]] = []
    for index in range(8):
        above_fold = index < 3
        items.append(
            {
                "src": f"https://cdn.example.com/photo-{index}.webp",
                "srcset": [f"https://cdn.example.com/photo-{index}-800.webp"],
                "srcset_widths": [800],
                "picture_formats": [],
                "sizes": None,
                "alt": f"Photo {index}",
                "width": 600,
                "height": 400,
                "loading": None if above_fold else "lazy",
                "featured": index == 0,
            }
        )
    return items


def healthy_structured_data() -> dict[str, Any]:
    """One Article block carrying every required AND recommended property."""
    return {
        "parse_errors": [],
        "json_ld_raw": ['{"@type":"Article"}'],
        "blocks": [
            {
                "source": "json-ld",
                "types": ["Article"],
                "data": {
                    "@type": "Article",
                    "headline": "SEO Basics",
                    "image": "https://cdn.example.com/share.png",
                    "author": {"@type": "Person", "name": "A. Writer"},
                    "datePublished": "2026-01-05",
                    "dateModified": "2026-02-02",
                    "publisher": {"@type": "Organization", "name": "Example"},
                },
            }
        ],
    }


def healthy_lab() -> LabPerformance:
    return LabPerformance(
        strategy="mobile",
        observed_at=None,
        lcp_ms=1800.0,
        tbt_ms=120.0,
        cls=0.03,
        delivery_savings_ms=120.0,
        delivery_audits={"unused-javascript": 90.0, "unminified-css": 30.0},
        cache_static_bytes=500_000.0,
        cache_short_ttl_resources=[],
    )


def healthy(**overrides: Any) -> PageEvidence:
    """A page with nothing wrong with it; override one field per defect case."""
    base: dict[str, Any] = {
        "url": URL,
        "title": GOOD_TITLE,
        "title_metrics": calculate_meta_title_metrics(GOOD_TITLE),
        "description": GOOD_DESCRIPTION,
        "description_metrics": calculate_meta_description_metrics(GOOD_DESCRIPTION),
        "meta_robots": "index, follow",
        "canonical_url": URL,
        "canonical_matches": True,
        "noindex": False,
        "nofollow": False,
        "h1_count": 1,
        "headings": HEALTHY_HEADINGS,
        "word_count": 1200,
        "text_bytes": 18_000,
        "schema_types": ["Article"],
        "image_count": 8,
        "images_missing_alt": 0,
        "image_items": healthy_images(),
        "http_status": 200,
        "redirect_chain": [],
        "mixed_content": [],
        "response_headers": {"strict-transport-security": "max-age=63072000"},
        "http_variant_probe": {"status": 301, "location": URL},
        "response_bytes": 120_000,
        "response_time_ms": 320,
        "ttfb_ms": 180,
        "pagination": {},
        "hreflang": HEALTHY_HREFLANG,
        "structured_data": healthy_structured_data(),
        "head_captured": True,
        "lang": "en",
        "og": dict(HEALTHY_OG),
        "twitter": {"twitter:card": "summary_large_image"},
        "head_meta": {"viewport": "width=device-width, initial-scale=1", "refresh": None},
        "lab_performance": healthy_lab(),
    }
    base.update(overrides)
    return PageEvidence(**base)


CASES: list[dict[str, Any]] = [
    {
        "name": "healthy_page",
        "why": "Nothing wrong — every measurable check passes; only genuinely "
        "absent facts (pagination) may answer n_a.",
        "evidence": healthy(),
    },
    {
        "name": "url_design_multiple_deductions",
        "why": "Every catalogue deduction accumulates exactly once, including "
        "a normalized session-identifier parameter name.",
        "evidence": healthy(
            url=("https://example.com/Über_Long_Path/" + "x" * 90 + "?a=1&b=2&c=3&PHPSESSID=abc")
        ),
    },
    {
        "name": "url_design_repeated_session_parameter",
        "why": "A repeated session parameter is one design defect, not one "
        "penalty per repeated value.",
        "evidence": healthy(url="https://example.com/page?sid=one&sid=two"),
    },
    {
        "name": "missing_title",
        "why": "title_presence fails; title_length must go n_a, never pass.",
        "evidence": healthy(title=None, title_metrics={}),
    },
    {
        "name": "title_too_long",
        "why": "Length verdict comes from the metrics dict, whose issue strings "
        "are themselves a mirror — this pins the wrapper wording AND the score band.",
        "evidence": healthy(
            title=LONG_TITLE, title_metrics=calculate_meta_title_metrics(LONG_TITLE)
        ),
    },
    {
        "name": "title_metrics_absent_from_snapshot",
        "why": "An old snapshot has the title but no metrics — n_a with the "
        "re-crawl wording, not a guessed verdict.",
        "evidence": healthy(title_metrics={}),
    },
    {
        "name": "missing_meta_description",
        "why": "meta_description_presence fails; length goes n_a.",
        "evidence": healthy(description=None, description_metrics={}),
    },
    {
        "name": "meta_description_too_short",
        "why": "Two bad flags vs one changes the score (40 vs 60).",
        "evidence": healthy(
            description=SHORT_DESCRIPTION,
            description_metrics=calculate_meta_description_metrics(SHORT_DESCRIPTION),
        ),
    },
    {
        "name": "no_h1",
        "why": "Zero H1 is a fail; the count itself is the evidence.",
        "evidence": healthy(h1_count=0),
    },
    {
        "name": "multiple_h1",
        "why": "issue_count is h1_count - 1, not 1.",
        "evidence": healthy(h1_count=4),
    },
    {
        "name": "thin_content_warn_band",
        "why": "250 words — between CONTENT_WARN_WORDS and CONTENT_OK_WORDS.",
        "evidence": healthy(word_count=250),
    },
    {
        "name": "thin_content_lower_warn_band",
        "why": "150 words — between CONTENT_FAIL_WORDS and CONTENT_WARN_WORDS; "
        "still warn, but score 40 and different wording.",
        "evidence": healthy(word_count=150),
    },
    {
        "name": "thin_content_fail_band",
        "why": "Under CONTENT_FAIL_WORDS is a fail.",
        "evidence": healthy(word_count=40),
    },
    {
        "name": "images_missing_alt_warn",
        "why": "Below both fail bounds — warn, with a ratio-derived score that "
        "must use Python's banker's rounding.",
        "evidence": healthy(image_count=8, images_missing_alt=2),
    },
    {
        "name": "images_missing_alt_fail_by_ratio",
        "why": "ratio >= IMAGE_ALT_FAIL_RATIO escalates to fail.",
        "evidence": healthy(image_count=6, images_missing_alt=3),
    },
    {
        "name": "images_missing_alt_fail_by_count",
        "why": "missing >= IMAGE_ALT_FAIL_COUNT escalates even at a low ratio.",
        "evidence": healthy(image_count=100, images_missing_alt=10),
    },
    {
        "name": "images_missing_alt_banker_rounding",
        "why": "95 * (1 - 97/190) = 46.5 exactly — Python rounds to 46, "
        "JavaScript's Math.round would say 47. The one case that proves the "
        "mirror ported round(), not Math.round().",
        "evidence": healthy(image_count=190, images_missing_alt=97),
    },
    {
        "name": "no_images",
        "why": "Zero images is n_a, not a pass.",
        "evidence": healthy(image_count=0, images_missing_alt=0),
    },
    {
        "name": "noindex",
        "why": "Fail with the meta_robots evidence payload attached.",
        "evidence": healthy(meta_robots="noindex, follow", noindex=True),
    },
    {
        "name": "robots_index_and_noindex_conflict",
        "why": "The conflict branch wins over the plain-noindex branch.",
        "evidence": healthy(meta_robots="index, noindex", noindex=True),
    },
    {
        "name": "nofollow",
        "why": "Warn, not fail; evidence payload attached.",
        "evidence": healthy(meta_robots="index, nofollow", nofollow=True),
    },
    {
        "name": "no_canonical",
        "why": "canonical_presence warns; canonical_conflicts goes n_a.",
        "evidence": healthy(canonical_url=None, canonical_matches=None),
    },
    {
        "name": "relative_canonical",
        "why": "A relative canonical warns at 45 and blocks the conflicts check.",
        "evidence": healthy(canonical_url="/guides/seo-basics", canonical_matches=None),
    },
    {
        "name": "canonical_to_other_page_same_site",
        "why": "Warn — deliberate duplicate or a leak, we cannot tell.",
        "evidence": healthy(
            canonical_url="https://example.com/guides/other", canonical_matches=False
        ),
    },
    {
        "name": "canonical_off_domain",
        "why": "Different registrable host is a fail — and the host comparison "
        "must strip www. without WHATWG URL normalization.",
        "evidence": healthy(
            canonical_url="https://www.someoneelse.com/guides/seo-basics",
            canonical_matches=False,
        ),
    },
    {
        "name": "canonical_conflict_and_noindex",
        "why": "Two de-indexing signals — the noindex branch of the conflict check.",
        "evidence": healthy(
            canonical_url="https://example.com/guides/other",
            canonical_matches=False,
            meta_robots="noindex",
            noindex=True,
        ),
    },
    {
        "name": "http_404",
        "why": "broken_page_4xx fails; server_error_5xx still passes (they are "
        "separate catalogue items with separate weights).",
        "evidence": healthy(http_status=404),
    },
    {
        "name": "http_503",
        "why": "server_error_5xx fails; broken_page_4xx passes.",
        "evidence": healthy(http_status=503),
    },
    {
        "name": "no_response_at_all",
        "why": "status 0 is the crawler's 'never answered' — scored with the 5xx.",
        "evidence": healthy(http_status=0),
    },
    {
        "name": "url_answers_301",
        "why": "A 3xx short-circuits redirect_chain before the hop count.",
        "evidence": healthy(
            http_status=301,
            redirect_chain=[{"url": URL, "status": 301}],
        ),
    },
    {
        "name": "long_redirect_chain",
        "why": "More than REDIRECT_CHAIN_MAX_HOPS entries — hops reported are "
        "entries minus one, and the sample is capped.",
        "evidence": healthy(
            redirect_chain=[
                {"url": "https://example.com/a", "status": 301},
                {"url": "https://example.com/b", "status": 301},
                {"url": "https://example.com/c", "status": 301},
                {"url": "https://example.com/d", "status": 301},
                {"url": "https://example.com/e", "status": 301},
                {"url": "https://example.com/f", "status": 301},
                {"url": URL, "status": 200},
            ],
        ),
    },
    {
        "name": "short_redirect_chain",
        "why": "At the limit — still a pass, with the hop count in the wording.",
        "evidence": healthy(
            redirect_chain=[
                {"url": "https://example.com/a", "status": 301},
                {"url": URL, "status": 200},
            ],
        ),
    },
    {
        "name": "redirect_loop",
        "why": "A repeated URL is a loop — categorically worse than a long chain.",
        "evidence": healthy(
            redirect_chain=[
                {"url": "https://example.com/a", "status": 301},
                {"url": "https://example.com/b", "status": 301},
                {"url": "https://example.com/a", "status": 301},
            ],
        ),
    },
    {
        "name": "pagination_coherent",
        "why": "Declared prev/next that point elsewhere pass, and the pass "
        "carries the pagination evidence.",
        "evidence": healthy(
            pagination={
                "prev": "https://example.com/guides/seo-basics?page=1",
                "next": "https://example.com/guides/seo-basics?page=3",
            }
        ),
    },
    {
        "name": "pagination_self_reference",
        "why": "rel=next pointing at this page traps the crawler — fail. The "
        "comparison strips trailing slashes on both sides.",
        "evidence": healthy(pagination={"next": URL + "/"}),
    },
    {
        "name": "mixed_content",
        "why": "Score is 70 - 5n, clamped; the sample is capped at five URLs.",
        "evidence": healthy(
            mixed_content=[f"http://cdn.example.com/img-{i}.png" for i in range(7)]
        ),
    },
    {
        "name": "large_page",
        "why": "Over LARGE_PAGE_BYTES — the byte counts are thousands-separated.",
        "evidence": healthy(response_bytes=6_400_000),
    },
    {
        "name": "ttfb_needs_improvement",
        "why": "Between TTFB_GOOD_MS and TTFB_POOR_MS — warn, on the linear "
        "89→50 ramp. Scored by FLOOR division in both languages so Python's "
        "banker's rounding can never disagree with Math.round.",
        "evidence": healthy(ttfb_ms=1_300),
    },
    {
        "name": "ttfb_poor",
        "why": "Over TTFB_POOR_MS — fail, 49 minus one point per 100 ms.",
        "evidence": healthy(ttfb_ms=3_000),
    },
    {
        "name": "ttfb_never_measured",
        "why": "A total response time was recorded but TTFB was not — the "
        "check must answer n_a, NEVER fall back to the total. This is the "
        "shape of every snapshot captured before TTFB was measured.",
        "evidence": healthy(response_time_ms=8_400, ttfb_ms=None),
    },
    # --- Outline, depth, and markup-to-text ---------------------------------
    {
        "name": "heading_outline_skips_and_empties",
        "why": "Skips are counted between CONSECUTIVE headings only, and empty "
        "headings are counted separately — both feed one issue_count.",
        "evidence": healthy(
            headings=[
                {"level": 1, "text": "Top"},
                {"level": 4, "text": "Jumped two"},
                {"level": 2, "text": ""},
                {"level": 5, "text": "Jumped three"},
            ]
        ),
    },
    {
        "name": "heading_outline_single_gap",
        "why": "One skip is the 70 band, not the 45 band.",
        "evidence": healthy(
            headings=[
                {"level": 1, "text": "Top"},
                {"level": 3, "text": "Skipped h2"},
            ]
        ),
    },
    {
        "name": "no_headings_on_a_long_page",
        "why": "Captured-and-empty is a real verdict; never-captured is n_a.",
        "evidence": healthy(headings=[]),
    },
    {
        "name": "no_headings_on_a_short_page",
        "why": "Too little content to need headings — a genuine pass.",
        "evidence": healthy(headings=[], word_count=120),
    },
    {
        "name": "content_depth_short_article",
        "why": "Declared Article under the min-words bar.",
        "evidence": healthy(word_count=300),
    },
    {
        "name": "content_depth_article_below_target",
        "why": "A PASS carrying an 80 AND an issue_count of 1 — the odd shape "
        "the catalogue row asks for, and the easiest one to get wrong.",
        "evidence": healthy(word_count=700),
    },
    {
        "name": "content_depth_commerce_empty",
        "why": "A product page's expectation is far lower than an article's.",
        "evidence": healthy(
            schema_types=["Product"], og={**HEALTHY_OG, "og:type": "product"}, word_count=40
        ),
    },
    {
        "name": "content_depth_utility_exempt",
        "why": "Utility types are exempt by declaration, not by length.",
        "evidence": healthy(schema_types=["ContactPage"], word_count=40),
    },
    {
        "name": "text_html_ratio_bloated",
        "why": "Under the fail band; the percent is formatted to one decimal "
        "with Python's half-to-even rule, and the byte counts are grouped.",
        "evidence": healthy(text_bytes=2_000, response_bytes=120_000),
    },
    {
        "name": "text_html_ratio_low_but_ordinary",
        "why": "The advisory band: a PASS at 75 with an issue_count of 1.",
        "evidence": healthy(text_bytes=9_000, response_bytes=120_000),
    },
    # --- Images -------------------------------------------------------------
    {
        "name": "images_without_dimensions",
        "why": "Coverage drives both the score and the fail/warn split.",
        "evidence": healthy(
            image_items=[
                {**item, "width": None, "height": None} if index >= 2 else item
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    {
        "name": "hero_image_lazy_loaded",
        "why": "Lazy above the fold outranks every below-fold problem.",
        "evidence": healthy(
            image_items=[
                {**item, "loading": "lazy"} if index == 0 else item
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    {
        "name": "images_eager_below_fold",
        "why": "The eager-below ratio picks 60 vs 80.",
        "evidence": healthy(image_items=[{**item, "loading": None} for item in healthy_images()]),
    },
    {
        "name": "legacy_image_formats",
        "why": "Count-weighted coverage; a <picture> offering AVIF counts as "
        "modern even when the <img> fallback is a JPEG.",
        "evidence": healthy(
            image_items=[
                {
                    **item,
                    "src": f"https://cdn.example.com/photo-{index}.jpg",
                    "srcset": [],
                    "srcset_widths": [],
                    "picture_formats": ["avif"] if index == 0 else [],
                }
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    {
        "name": "images_without_declared_format",
        "why": "Extension-less CDN sources are unjudgeable, not legacy.",
        "evidence": healthy(
            image_items=[
                {
                    **item,
                    "src": "https://cdn.example.com/cdn-cgi/image/w=800/hero",
                    "srcset": [],
                    "srcset_widths": [],
                }
                for item in healthy_images()
            ]
        ),
    },
    {
        "name": "oversized_image_severe",
        "why": "3200px into a 200px slot is 16x — the fail band, and the ratio "
        "is printed to one decimal.",
        "evidence": healthy(
            image_items=[
                {**item, "width": 200, "srcset_widths": [3200]} if index == 0 else item
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    {
        "name": "oversized_image_quarter_ratio",
        "why": "900px into a 400px slot is exactly 2.25x — Python's :.1f says "
        "2.2 (half-to-even) where JavaScript's toFixed says 2.3.",
        "evidence": healthy(
            image_items=[
                {**item, "width": 400, "srcset_widths": [900]} if index == 0 else item
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    {
        "name": "broken_images_status_checked",
        "why": "The capture-gap branch lights up the moment statuses exist.",
        "evidence": healthy(
            image_items=[
                {**item, "http_status": 404 if index < 3 else 200}
                for index, item in enumerate(healthy_images())
            ]
        ),
    },
    # --- Mobile, language, social -------------------------------------------
    {
        "name": "no_viewport_tag",
        "why": "Captured head, absent tag — a fail, not an n_a.",
        "evidence": healthy(head_meta={"viewport": None, "refresh": None}),
    },
    {
        "name": "viewport_fixed_width",
        "why": "A width that is not device-width names itself in the sentence.",
        "evidence": healthy(head_meta={"viewport": "width=1024, initial-scale=1", "refresh": None}),
    },
    {
        "name": "viewport_blocks_zoom",
        "why": "Both lockouts at once — the joined list and the issue_count.",
        "evidence": healthy(
            head_meta={
                "viewport": "width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1.0",
                "refresh": None,
            }
        ),
    },
    {
        "name": "no_html_lang",
        "why": "Declared nothing — a warn, and never a code-shape claim.",
        "evidence": healthy(lang=""),
    },
    {
        "name": "invalid_html_lang",
        "why": "Structural BCP-47 only; the regex is the shared one.",
        "evidence": healthy(lang="english"),
    },
    {
        "name": "og_image_missing",
        "why": "No share image at all.",
        "evidence": healthy(og={k: v for k, v in HEALTHY_OG.items() if k != "og:image"}),
    },
    {
        "name": "og_image_relative",
        "why": "Relative share images are never resolved by the networks.",
        "evidence": healthy(og={**HEALTHY_OG, "og:image": "/share.png"}),
    },
    {
        "name": "og_image_unsupported_format",
        "why": "The supported list is sorted into the sentence.",
        "evidence": healthy(og={**HEALTHY_OG, "og:image": "https://cdn.example.com/share.svg"}),
    },
    {
        "name": "social_tags_incomplete",
        "why": "Coverage score minus both penalties, and the problems joined.",
        "evidence": healthy(
            og={"og:title": "SEO Basics", "og:url": URL},
            twitter={},
        ),
    },
    {
        "name": "social_og_url_conflicts_with_canonical",
        "why": "The og:url/canonical comparison ignores case and the trailing "
        "slash and nothing else.",
        "evidence": healthy(og={**HEALTHY_OG, "og:url": "https://example.com/guides/other-page"}),
    },
    # --- Markup redirects, transport ----------------------------------------
    {
        "name": "meta_refresh_instant",
        "why": "A zero-delay refresh is an HTTP redirect substitute.",
        "evidence": healthy(
            head_meta={
                "viewport": "width=device-width, initial-scale=1",
                "refresh": "0; url=https://example.com/guides/new",
            }
        ),
    },
    {
        "name": "meta_refresh_interstitial",
        "why": "Above the instant bound the page is a real interstitial.",
        "evidence": healthy(
            head_meta={
                "viewport": "width=device-width, initial-scale=1",
                "refresh": "5; url='https://example.com/guides/new'",
            }
        ),
    },
    {
        "name": "meta_refresh_self_reload",
        "why": "A refresh with no target is not a redirect at all.",
        "evidence": healthy(
            head_meta={
                "viewport": "width=device-width, initial-scale=1",
                "refresh": "30",
            }
        ),
    },
    {
        "name": "temporary_redirect_302",
        "why": "Temporary statuses are de-duplicated and sorted NUMERICALLY — "
        "JavaScript's default sort is lexicographic and would say 302/307 "
        "wrong for three-digit sets.",
        "evidence": healthy(
            http_status=200,
            redirect_chain=[
                {"url": "https://example.com/old", "status": 307},
                {"url": "https://example.com/older", "status": 302},
                {"url": URL, "status": 200},
            ],
        ),
    },
    {
        "name": "permanent_redirects_only",
        "why": "301/308 hops are the pass branch, with its own wording.",
        "evidence": healthy(
            redirect_chain=[
                {"url": "https://example.com/old", "status": 301},
                {"url": URL, "status": 200},
            ]
        ),
    },
    {
        "name": "redirect_chain_without_hop_statuses",
        "why": "URLs but no statuses — unjudgeable, so n_a with the recapture.",
        "evidence": healthy(redirect_chain=[{"url": "https://example.com/old"}, {"url": URL}]),
    },
    {
        "name": "soft_404_phrasing_and_empty",
        "why": "Both signals together is the fail; the title is quoted back.",
        "evidence": healthy(title="404 — Page not found", word_count=20),
    },
    {
        "name": "soft_404_phrasing_only",
        "why": "Error phrasing on a full page is a warn, not a fail.",
        "evidence": healthy(title="Page not found", word_count=800),
    },
    {
        "name": "soft_404_empty_only",
        "why": "Under the empty bound with an ordinary title.",
        "evidence": healthy(word_count=12),
    },
    {
        "name": "https_variant_serves_200",
        "why": "An insecure duplicate that answers 200 is the worst case.",
        "evidence": healthy(http_variant_probe={"status": 200, "location": None}),
    },
    {
        "name": "https_variant_redirects_temporarily",
        "why": "302 to https is a warn; 301/308 is the pass.",
        "evidence": healthy(http_variant_probe={"status": 302, "location": URL}),
    },
    {
        "name": "https_variant_never_probed",
        "why": "The declared capture gap — n_a with the scheme as evidence.",
        "evidence": healthy(http_variant_probe=None),
    },
    {
        "name": "page_served_over_http",
        "why": "The page's own scheme is the free half of this check.",
        "evidence": healthy(url="http://example.com/guides/seo-basics"),
    },
    # --- Structured data and hreflang ---------------------------------------
    {
        "name": "structured_data_parse_error",
        "why": "A parse error voids the script and outranks any missing "
        "property; the snippet is truncated by code points.",
        "evidence": healthy(
            structured_data={
                "parse_errors": [
                    {"source": "json-ld", "message": "Expecting ',' delimiter", "index": 0}
                ],
                "json_ld_raw": ['{"@type":"Article" "headline":"broken"}'],
                "blocks": [],
            }
        ),
    },
    {
        "name": "structured_data_missing_required",
        "why": "Required beats recommended, and the alias table decides what counts as declared.",
        "evidence": healthy(
            structured_data={
                "parse_errors": [],
                "json_ld_raw": [],
                "blocks": [
                    {
                        "source": "json-ld",
                        "types": ["Product"],
                        "data": {"@type": "Product", "name": "Widget"},
                    }
                ],
            }
        ),
    },
    {
        "name": "structured_data_missing_recommended",
        "why": "Valid markup, thinner rich result — a warn at 75.",
        "evidence": healthy(
            structured_data={
                "parse_errors": [],
                "json_ld_raw": [],
                "blocks": [
                    {
                        "source": "json-ld",
                        "types": ["Article"],
                        "data": {"@type": "Article", "headline": "SEO Basics"},
                    }
                ],
            }
        ),
    },
    {
        "name": "structured_data_local_business_subtype",
        "why": "A Restaurant HAS declared a LocalBusiness, and `location` is an "
        "accepted spelling of `address`.",
        "evidence": healthy(
            structured_data={
                "parse_errors": [],
                "json_ld_raw": [],
                "blocks": [
                    {
                        "source": "json-ld",
                        "types": ["Restaurant"],
                        "data": {
                            "@type": "Restaurant",
                            "name": "Cafe",
                            "location": {"@type": "PostalAddress", "streetAddress": "1 Main St"},
                            "telephone": "+1 555 0100",
                            "openingHoursSpecification": [{"opens": "09:00"}],
                            "geo": {"latitude": 1, "longitude": 2},
                            "sameAs": ["https://example.com"],
                            "url": URL,
                            "image": "https://cdn.example.com/cafe.png",
                            "priceRange": "$$",
                        },
                    }
                ],
            }
        ),
    },
    {
        "name": "structured_data_unclaimed_types",
        "why": "Markup with no published rich-result contract still passes.",
        "evidence": healthy(
            structured_data={
                "parse_errors": [],
                "json_ld_raw": [],
                "blocks": [
                    {"source": "json-ld", "types": ["WebSite"], "data": {"@type": "WebSite"}}
                ],
            }
        ),
    },
    {
        "name": "hreflang_invalid_code_and_relative",
        "why": "Both problems are joined into one sentence, in this order.",
        "evidence": healthy(
            hreflang=[
                {"lang": "english", "href": URL},
                {"lang": "es", "href": "/es/guias"},
            ]
        ),
    },
    {
        "name": "hreflang_no_self_reference",
        "why": "A cluster that never names itself is invalid outright.",
        "evidence": healthy(
            hreflang=[
                {"lang": "es", "href": "https://example.com/es/guias"},
                {"lang": "fr", "href": "https://example.com/fr/guides"},
            ]
        ),
    },
    {
        "name": "hreflang_conflicts_with_canonical",
        "why": "Self-reference vs canonical is compared on the normalized key.",
        "evidence": healthy(
            canonical_url="https://example.com/guides/canonical-one",
            canonical_matches=False,
            hreflang=[
                {"lang": "en", "href": URL},
                {"lang": "x-default", "href": URL},
            ],
        ),
    },
    {
        "name": "hreflang_without_x_default",
        "why": "Valid but no fallback — the 80 warn.",
        "evidence": healthy(
            hreflang=[
                {"lang": "en", "href": URL},
                {"lang": "es", "href": "https://example.com/es/guias"},
            ]
        ),
    },
    # --- Lab performance ----------------------------------------------------
    {
        "name": "cwv_all_poor",
        "why": "Every CWV band past 'poor', where the score is a formula rather "
        "than a linear map; LCP seconds and CLS are decimal-formatted.",
        "evidence": healthy(
            lab_performance=LabPerformance(
                strategy="mobile",
                observed_at=None,
                lcp_ms=6200.0,
                tbt_ms=1400.0,
                cls=0.42,
                delivery_savings_ms=2600.0,
                delivery_audits={
                    "render-blocking-insight": 1200.0,
                    "unused-javascript": 800.0,
                    "image-delivery-insight": 400.0,
                    "font-display-insight": 150.0,
                    "unminified-css": 50.0,
                },
                cache_static_bytes=800_000.0,
                cache_short_ttl_resources=[
                    {
                        "url": "https://cdn.example.com/app.js",
                        "cache_lifetime_ms": 3_600_000,
                        "total_bytes": 500_000,
                    }
                ],
            )
        ),
    },
    {
        "name": "cwv_middle_bands",
        "why": "The linear map between good and poor, on all three metrics.",
        "evidence": healthy(
            lab_performance=LabPerformance(
                strategy="desktop",
                observed_at=None,
                lcp_ms=3200.0,
                tbt_ms=400.0,
                cls=0.18,
                delivery_savings_ms=800.0,
                delivery_audits={"legacy-javascript-insight": 800.0},
                cache_static_bytes=200_000.0,
                cache_short_ttl_resources=[
                    {
                        "url": "https://cdn.example.com/style.css",
                        "cache_lifetime_ms": 86_400_000,
                        "total_bytes": 40_000,
                    }
                ],
            )
        ),
    },
    {
        "name": "lab_metrics_partially_reported",
        "why": "A measurement that reported nothing usable is per-metric n_a, never a zero.",
        "evidence": healthy(
            lab_performance=LabPerformance(
                strategy="mobile",
                observed_at=None,
                lcp_ms=None,
                tbt_ms=None,
                cls=None,
                delivery_savings_ms=None,
                delivery_audits={},
                cache_static_bytes=None,
                cache_short_ttl_resources=[],
            )
        ),
    },
    {
        "name": "caching_negligible_static_bytes",
        "why": "Below the floor, caching is not a lever — a flat 100.",
        "evidence": healthy(
            lab_performance=LabPerformance(
                strategy="mobile",
                observed_at=None,
                lcp_ms=1500.0,
                tbt_ms=80.0,
                cls=0.01,
                delivery_savings_ms=50.0,
                delivery_audits={"unminified-css": 50.0},
                cache_static_bytes=4_000.0,
                cache_short_ttl_resources=[],
            )
        ),
    },
    {
        "name": "no_pagespeed_measurement",
        "why": "Every CWV check answers n_a with the one-click measure — a "
        "crawl cannot produce these numbers.",
        "evidence": healthy(lab_performance=None),
    },
    {
        "name": "all_evidence_missing",
        "why": "Nothing captured. Every MEASURED check must answer n_a (or fail "
        "on a genuinely absent required tag) — never a silent pass. The checks "
        "whose subject is the ABSENCE itself (no robots directives, no redirect "
        "chain, no insecure resources) legitimately pass; that is the fact.",
        "evidence": PageEvidence(url=URL),
    },
]


def build() -> dict[str, Any]:
    cases = []
    for case in CASES:
        evidence: PageEvidence = case["evidence"]
        outcomes = run_page_checks(evidence)
        cases.append(
            {
                "name": case["name"],
                "why": case["why"],
                "evidence": dataclasses.asdict(evidence),
                "expected": {key: dataclasses.asdict(value) for key, value in outcomes.items()},
            }
        )
    return {
        "_readme": (
            "GENERATED — do not hand-edit. Source of truth: "
            "matrx_scraper/seo_audit.py::run_page_checks. Regenerate with "
            ".venv/bin/python packages/matrx-scraper/scripts/"
            "generate_page_checks_parity_fixture.py from the aidream repo root. "
            "If checks.parity.test.ts fails, one side changed without the "
            "other — fix BOTH in the same unit of work."
        ),
        "source": "packages/matrx-scraper/matrx_scraper/seo_audit.py::run_page_checks",
        "generator": "packages/matrx-scraper/scripts/generate_page_checks_parity_fixture.py",
        "check_names": list(run_page_checks(PageEvidence(url=URL)).keys()),
        "cases": cases,
    }


def main() -> int:
    payload = build()
    body = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    target = (
        REPO_ROOT.parent
        / "matrx-frontend/features/marketing/seo/audit/__fixtures__/page-checks-parity.json"
    )
    if not target.parent.parent.exists():
        print(f"SKIP (repo not present): {target}")
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    print(f"wrote {len(payload['cases'])} cases -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
