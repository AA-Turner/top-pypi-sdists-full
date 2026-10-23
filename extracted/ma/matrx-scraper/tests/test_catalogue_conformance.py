"""Standing guard: every SEO check scores the way its catalog row says it does.

Why this exists (2026-10-14 census): checks silently contradicted their own
``web.analysis_item.score_contract`` (a 51-60 char title flagged while the
contract says 30-60 passes). Nothing compared the two, so the drift was invisible.

How it works
------------
* ``fixtures/catalogue_contracts.json`` is a snapshot of every live,
  non-AI-rubric ``web.analysis_item`` row (key, tier, score_contract,
  severity_map, sha256 of the contract). The OFFLINE tests read only that file.
* Every case below is DERIVED FROM THE CONTRACT TEXT, never from the code: the
  expected score is the number the contract names for that input. ``clause`` must
  be a verbatim piece of the contract (checked), so editing a contract breaks the
  case that cites it.
* ``KNOWN_DISAGREEMENTS`` lists cases where the code does NOT give the contract's
  score today. They run as strict xfails: still disagreeing = reported, not red;
  FIXED = the strict xfail flips red and says "delete this entry". A NEW
  disagreement is a plain red failure. Nothing is hidden and nothing rots.
* The meta-test refuses a cataloged deterministic/formula key that has no case
  and no entry in ``NOT_CHECKABLE`` / ``NOT_IMPLEMENTED`` (with a reason).
* The severity test pins ``analysis_write.severity_for`` to the documented tier
  rule, using each row's own severity_map from the fixture.

Refreshing / verifying the snapshot (live, opt-in)
--------------------------------------------------
``pytest -m network tests/test_catalogue_conformance.py`` compares the fixture to
the live table and needs ``CATALOGUE_SUPABASE_URL`` + ``CATALOGUE_SUPABASE_KEY``
(falls back to ``SUPABASE_URL`` / ``SUPABASE_SERVICE_ROLE_KEY``); it SKIPS when
they are absent. Set ``CATALOGUE_REFRESH=1`` to rewrite the fixture instead.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from collections.abc import Callable
from typing import Any

import pytest

from matrx_scraper import seo_audit
from matrx_scraper.seo_audit import (
    PAGE_CHECKS as SEO_PAGE_CHECKS,
    CheckOutcome,
    LabPerformance,
    PageEvidence,
)
from matrx_scraper.web_crawl import analysis as A
from matrx_scraper.web_crawl.analysis import (
    CROSS_PAGE_CHECKS,
    SITE_CHECKS,
    GscPeriod,
    OrphanCensus,
    PageFacts,
    PageGscStats,
    PageLinkStats,
    SiteAggregates,
    SiteBusinessEvidence,
    SiteFacts,
    SiteGscEvidence,
    TlsFacts,
)
from matrx_scraper.web_crawl.analysis_write import SEVERITY_ORDER, severity_for
from matrx_scraper.web_crawl.gsc_cannibalization import GscCannibalizationEvidence
from matrx_scraper.web_crawl.near_duplicate import NearDuplicatePage, build_near_duplicate_report
from matrx_scraper.web_crawl.site_analysis import SiteEvidence, SitemapDocFacts
from matrx_scraper.web_crawl.site_probe import RobotsCapture, SiteProbe, SlashPairProbe, UrlProbe

FIXTURE = Path(__file__).parent / "fixtures" / "catalogue_contracts.json"


def _canonical_sha(contract: Any) -> str:
    return hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _load() -> dict[str, dict[str, Any]]:
    return json.loads(FIXTURE.read_text())["items"]


CATALOGUE = _load()


def _contract_text(key: str) -> str:
    return json.dumps(CATALOGUE[key]["score_contract"], ensure_ascii=False, sort_keys=True)


# ---------------------------------------------------------------------------
# Fixture integrity + live currency
# ---------------------------------------------------------------------------


def test_fixture_is_self_consistent():
    for key, row in CATALOGUE.items():
        assert row["sha256"] == _canonical_sha(row["score_contract"]), f"{key}: contract edited by hand"
        assert row["score_contract"].get("method") in ("deterministic_rules", "formula"), key
        assert row["severity_map"].get("bands"), f"{key}: no severity bands"


@pytest.mark.network
def test_fixture_matches_the_live_catalogue():
    import httpx

    url = os.environ.get("CATALOGUE_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    key = os.environ.get("CATALOGUE_SUPABASE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        pytest.skip("no catalog credentials (CATALOGUE_SUPABASE_URL / CATALOGUE_SUPABASE_KEY)")
    response = httpx.get(
        f"{url.rstrip('/')}/rest/v1/analysis_item",
        params={"select": "key,tier,score_contract,severity_map", "deleted_at": "is.null"},
        headers={"apikey": key, "Authorization": f"Bearer {key}", "Accept-Profile": "web"},
        timeout=30,
    )
    response.raise_for_status()
    live = {
        r["key"]: r
        for r in response.json()
        if (r["score_contract"] or {}).get("method") in ("deterministic_rules", "formula")
    }
    if os.environ.get("CATALOGUE_REFRESH") == "1":
        items = {
            k: {
                "tier": r["tier"],
                "score_contract": r["score_contract"],
                "severity_map": r["severity_map"],
                "sha256": _canonical_sha(r["score_contract"]),
            }
            for k, r in sorted(live.items())
        }
        FIXTURE.write_text(
            json.dumps(
                {"snapshot_date": date.today().isoformat(), "note": json.loads(FIXTURE.read_text())["note"], "items": items},
                indent=1,
                sort_keys=True,
            )
        )
        pytest.skip("fixture refreshed from live")
    assert set(live) == set(CATALOGUE), (
        f"catalog keys drifted: new={sorted(set(live) - set(CATALOGUE))} gone={sorted(set(CATALOGUE) - set(live))}"
    )
    changed = [
        k
        for k in live
        if _canonical_sha(live[k]["score_contract"]) != CATALOGUE[k]["sha256"]
        or live[k]["tier"] != CATALOGUE[k]["tier"]
        or live[k]["severity_map"] != CATALOGUE[k]["severity_map"]
    ]
    assert not changed, f"contracts changed since the snapshot - re-derive their cases: {changed}"


# ---------------------------------------------------------------------------
# Case machinery
# ---------------------------------------------------------------------------


@dataclass
class Case:
    key: str
    label: str
    clause: str  # verbatim fragment of the contract this case is derived from
    expected: Any  # int | (lo, hi) | set[int] | None (= n_a / null score)
    run: Callable[[], CheckOutcome]

    @property
    def cid(self) -> str:
        return f"{self.key}::{self.label}"


CASES: list[Case] = []


def case(key: str, label: str, clause: str, expected: Any):
    def register(fn: Callable[[], CheckOutcome]) -> Callable[[], CheckOutcome]:
        CASES.append(Case(key, label, clause, expected, fn))
        return fn

    return register


def _matches(score: int | None, expected: Any) -> bool:
    if expected is None:
        return score is None
    if score is None:
        return False
    if isinstance(expected, tuple):
        return expected[0] <= score <= expected[1]
    if isinstance(expected, set):
        return score in expected
    return score == expected


# --- evidence builders ------------------------------------------------------

OG = {
    "og:title": "T",
    "og:description": "D",
    "og:image": "https://example.com/i.jpg",
    "og:url": "https://example.com/a",
    "og:type": "website",
}


def ev(**kw) -> PageEvidence:
    base = dict(url="https://example.com/a", head_captured=True, og=dict(OG), twitter={"twitter:card": "summary"})
    base.update(kw)
    return PageEvidence(**base)


def page(key: str, **kw) -> CheckOutcome:
    return SEO_PAGE_CHECKS[key](ev(**kw))


def img(i: int = 0, **kw) -> dict:
    item = {"src": f"https://example.com/p{i}.jpg", "alt": "x", "width": 300, "height": 200}
    item.update(kw)
    return item


def images(items: list[dict]) -> dict:
    return dict(image_items=items, image_count=len(items))


def P(key: str, label: str, clause: str, expected: Any, **kw):
    """Register a single-page case: ``PAGE_CHECKS[key](ev(**kw))``."""

    def run() -> CheckOutcome:
        return page(key, **kw)

    CASES.append(Case(key, label, clause, expected, run))


# ---------------------------------------------------------------------------
# PER-PAGE CHECKS (seo_audit.PAGE_CHECKS)
# ---------------------------------------------------------------------------

# url_design_quality -- formula: 100 - (len>115: 15) - (params>2: 15) - (uppercase: 10) ...
_F = "score = 100 - (len>115: 15) - (params>2: 15) - (uppercase: 10) - (underscores: 10) - (non_ascii: 10) - (session_id_like_param: 25); clamp 1"
_BASE = "https://example.com/"
P("url_design_quality", "clean", _F, 100, url=_BASE + "a-page")
P("url_design_quality", "length 115 is not long", _F, 100, url=_BASE + "a" * (115 - len(_BASE)))
P("url_design_quality", "length 116 is long", _F, 85, url=_BASE + "a" * (116 - len(_BASE)))
P("url_design_quality", "2 params ok", _F, 100, url=_BASE + "a?x=1&y=2")
P("url_design_quality", "3 params", _F, 85, url=_BASE + "a?x=1&y=2&z=3")
P("url_design_quality", "uppercase", _F, 90, url=_BASE + "About")
P("url_design_quality", "underscore", _F, 90, url=_BASE + "a_page")
P("url_design_quality", "non-ascii", _F, 90, url=_BASE + "café")
P("url_design_quality", "session id", _F, 75, url=_BASE + "a?phpsessid=1")
P("url_design_quality", "combined", _F, 50, url=_BASE + "A_page")  # 100 -10 -10 ... see below
CASES[-1].expected = 80  # uppercase 10 + underscore 10

# title_presence
_R = "Title missing or empty"
P("title_presence", "missing", _R, 15, title=None)
P("title_presence", "empty", _R, 15, title="")
P("title_presence", "single descriptive", "Single descriptive title", 100, title="A descriptive page title")

# title_length -- 30..60 passes at 100; 60<len<=70 or 15<=len<30 -> 75; >70 -> 55; <15 -> 50
_T = "30 <= length <= 60"
for n, exp, why in [
    (71, 55, "Length > 70 chars (near-certain truncation)"),
    (70, 75, "60 < length <= 70 or 15 <= length < 30"),
    (61, 75, "60 < length <= 70 or 15 <= length < 30"),
    (60, 100, _T),
    (55, 100, _T),
    (51, 100, _T),
    (30, 100, _T),
    (29, 75, "60 < length <= 70 or 15 <= length < 30"),
    (15, 75, "60 < length <= 70 or 15 <= length < 30"),
    (14, 50, "Length < 15 chars"),
]:
    P("title_length", f"{n} chars", why, exp, title="x" * n)

# meta_description_presence
P("meta_description_presence", "missing", "Missing or empty", 45, description=None)
P("meta_description_presence", "present", "Single non-empty description", 100, description="A description")

# meta_description_length -- >165 -> 65; <50 -> 60; 70..155 -> 100; otherwise 80
for n, exp, why in [
    (166, 65, "Length > 165 chars (truncates)"),
    (165, 80, "Otherwise (borderline)"),
    (156, 80, "Otherwise (borderline)"),
    (155, 100, "70 <= length <= 155"),
    (70, 100, "70 <= length <= 155"),
    (69, 80, "Otherwise (borderline)"),
    (50, 80, "Otherwise (borderline)"),
    (49, 60, "Length < 50 chars"),
]:
    P("meta_description_length", f"{n} chars", why, exp, description="d" * n)

# h1_presence
P("h1_presence", "none", "H1 missing or empty", 30, h1_count=0)
P("h1_presence", "two", "Multiple H1 tags", 55, h1_count=2)
P("h1_presence", "one", "Single unique H1", 100, h1_count=1)


# heading_hierarchy
def _levels(levels: list[int], empty: int = 0) -> list[dict]:
    out = [{"level": lv, "text": "x"} for lv in levels]
    for i in range(empty):
        out[i]["text"] = ""
    return out


_H = ">3 skipped-level jumps or >30% empty headings"
_H2 = "1-3 skipped levels or some empty headings"
P("heading_hierarchy", "clean", "Clean hierarchy", 100, headings=_levels([1, 2, 3, 2]), word_count=500)
P("heading_hierarchy", "1 skip", _H2, 70, headings=_levels([1, 3]), word_count=500)
P("heading_hierarchy", "3 skips", _H2, 70, headings=_levels([1, 3, 1, 3, 1, 3]), word_count=500)
P("heading_hierarchy", "4 skips", _H, 45, headings=_levels([1, 3, 1, 3, 1, 3, 1, 3]), word_count=500)
P("heading_hierarchy", "30% empty is not over 30%", _H2, 70, headings=_levels([1] * 10, empty=3), word_count=500)
P("heading_hierarchy", "40% empty", _H, 45, headings=_levels([1] * 10, empty=4), word_count=500)
P("heading_hierarchy", "no headings, 301 words", "No headings at all on a >300-word page", 55, headings=[], word_count=301)
P("heading_hierarchy", "no headings, 300 words", "Clean hierarchy", 100, headings=[], word_count=300)

# thin_content
_TH = [
    (49, 20, "word_count < 50 on an indexable content page"),
    (50, 45, "50 <= word_count < 150"),
    (149, 45, "50 <= word_count < 150"),
    (150, 70, "150 <= word_count < 300"),
    (299, 70, "150 <= word_count < 300"),
    (300, 100, "word_count >= 300 or page type exempt"),
]
for n, exp, why in _TH:
    P("thin_content", f"{n} words", why, exp, word_count=n)

# content_depth
_ART = dict(url="https://example.com/blog/post", schema_types=["Article"])
_PROD = dict(url="https://example.com/shop/thing", schema_types=["Product"])
P("content_depth", "article 499", "Article/blog type with < 500 words", 55, word_count=499, **_ART)
P("content_depth", "article 500", "Article 500-900 words", 80, word_count=500, **_ART)
P("content_depth", "article 899", "Article 500-900 words", 80, word_count=899, **_ART)
P("content_depth", "article 901", "Meets or exceeds type expectation", 100, word_count=901, **_ART)
P("content_depth", "product 99", "Product/category with < 100 words of unique copy", 60, word_count=99, **_PROD)
P("content_depth", "product 100", "Meets or exceeds type expectation", 100, word_count=100, **_PROD)

# text_html_ratio -- <3% -> 50 ; 3-10% -> 75 ; >10% -> 100  (word_count >= 300 so it is not n_a)
_RATIO = {"word_count": 500, "response_bytes": 100_000}
P("text_html_ratio", "2.9%", "Ratio < 3% on an indexable content page", 50, text_bytes=2_900, **_RATIO)
P("text_html_ratio", "3.0%", "Ratio 3-10%", 75, text_bytes=3_000, **_RATIO)
P("text_html_ratio", "10.0%", "Ratio 3-10%", 75, text_bytes=10_000, **_RATIO)
P("text_html_ratio", "10.1%", "Ratio > 10%", 100, text_bytes=10_100, **_RATIO)

# image_alt_presence -- round(100 * images_with_alt/meaningful_images); 100 when no images
_IA = "score = round(100 * images_with_alt/meaningful_images); 100 when no images"
P("image_alt_presence", "all alt", _IA, 100, **images([img(i) for i in range(4)]))
P("image_alt_presence", "2 of 4 missing", _IA, 50, **images([img(0), img(1), img(2, alt=None), img(3, alt=None)]))
P("image_alt_presence", "1 of 3 missing", _IA, 67, **images([img(0), img(1), img(2, alt=None)]))
P("image_alt_presence", "decorative empty alt is not meaningful", _IA, 100, **images([img(0), img(1, alt="")]))

# image_dimension_attrs -- round(100 * images_with_dims/total_content_images); 100 when none
_ID = "score = round(100 * images_with_dims/total_content_images); 100 when none"
P("image_dimension_attrs", "all", _ID, 100, **images([img(i) for i in range(4)]))
P("image_dimension_attrs", "3 of 4", _ID, 75, **images([img(0), img(1), img(2), img(3, width=None)]))
P("image_dimension_attrs", "1 of 3", _ID, 33, **images([img(0, height=None), img(1, width=None), img(2)]))

# image_lazy_loading
_K = seo_audit.IMAGE_ABOVE_FOLD_DOM_COUNT
_eager = lambda i: img(i, loading="eager")  # noqa: E731
_lazy = lambda i: img(i, loading="lazy")  # noqa: E731
P("image_lazy_loading", "hero lazy", "LCP/hero image is lazy-loaded", 30, **images([_lazy(0), _lazy(1)]))
P(
    "image_lazy_loading",
    "correct both ways",
    "Correct policy both directions",
    100,
    **images([_eager(i) for i in range(_K)] + [_lazy(_K + i) for i in range(4)]),
)
P(
    "image_lazy_loading",
    "3 of 4 below-fold eager",
    ">50% of below-fold images eager-loaded",
    60,
    **images([_eager(i) for i in range(_K + 3)] + [_lazy(_K + 3)]),
)
P(
    "image_lazy_loading",
    "1 of 4 below-fold eager",
    "Some below-fold images eager (<50%)",
    80,
    **images([_eager(i) for i in range(_K + 1)] + [_lazy(_K + 1 + i) for i in range(3)]),
)

# image_modern_format -- round(100 * modern_bytes/(modern_bytes+convertible_legacy_bytes))
_IM = "score = round(100 * modern_bytes/(modern_bytes+convertible_legacy_bytes)); 100 when no significant raster images"


def _m(i, fmt, nbytes):
    return img(i, bytes=nbytes, capture_status="complete", actual_format=fmt)


P("image_modern_format", "all modern", _IM, 100, **images([_m(0, "webp", 500_000), _m(1, "avif", 500_000)]))
P("image_modern_format", "75% modern", _IM, 75, **images([_m(0, "webp", 3_000_000), _m(1, "jpg", 1_000_000)]))
P("image_modern_format", "25% modern", _IM, 25, **images([_m(0, "webp", 1_000_000), _m(1, "jpg", 3_000_000)]))


# image_oversized
def _o(width, natural, nbytes):
    return img(0, width=width, natural_width=natural, bytes=nbytes)


P("image_oversized", "appropriately sized", "All images appropriately sized", 100, **images([_o(800, 800, 20_000)]))
P("image_oversized", "minor oversizing", "Minor oversizing (waste < 500KB)", 80, **images([_o(400, 1000, 40_000)]))
P(
    "image_oversized",
    "300KB+ above rendered need",
    "Any image > 300KB above its rendered need, or waste 500KB-1.5MB",
    50,
    **images([_o(800, 1600, 400_000)]),
)
P(
    "image_oversized",
    "image over 1MB",
    "Any image > 1MB or total wasted image bytes > 1.5MB",
    25,
    **images([_o(800, 800, 1_100_000)]),
)

# broken_images
_bi = lambda n: images([img(i, http_status=404, content_type="text/html") for i in range(n)] + [img(99, http_status=200, content_type="image/png")])  # noqa: E731
P("broken_images", "3 broken", ">= 3 broken images on the page", 25, **_bi(3))
P("broken_images", "2 broken", "1-2 broken images", 50, **_bi(2))
P("broken_images", "1 broken", "1-2 broken images", 50, **_bi(1))
P("broken_images", "none", "No broken images", 100, **_bi(0))

# viewport_meta
P("viewport_meta", "missing", "Viewport meta missing", 20, head_meta={"viewport": None, "refresh": None})
P("viewport_meta", "fixed width", "Fixed-width viewport (no device-width)", 40, head_meta={"viewport": "width=1024", "refresh": None})
P("viewport_meta", "user-scalable=no", "user-scalable=no or maximum-scale<=1 (zoom blocked)", 60, head_meta={"viewport": "width=device-width, user-scalable=no", "refresh": None})
P("viewport_meta", "maximum-scale=1", "user-scalable=no or maximum-scale<=1 (zoom blocked)", 60, head_meta={"viewport": "width=device-width, maximum-scale=1", "refresh": None})
P("viewport_meta", "responsive", "Proper responsive viewport", 100, head_meta={"viewport": "width=device-width, initial-scale=1", "refresh": None})

# html_lang_validity
P("html_lang_validity", "missing", "lang attribute missing", 55, lang="")
P("html_lang_validity", "invalid", "lang invalid or mismatches detected content language", 45, lang="not a lang!")
P("html_lang_validity", "valid", "Valid and matching", 100, lang="en-US")

# og_image_validity
_og = lambda **o: {k: v for k, v in {**OG, **o}.items() if v is not None}  # noqa: E731
P("og_image_validity", "missing", "og:image missing or returns non-200", 45, og=_og(**{"og:image": None}))
P("og_image_validity", "unsupported format", "Image below 200x200 or unsupported format", 55, og=_og(**{"og:image": "https://example.com/i.svg"}))
P("og_image_validity", "valid", "Valid, recommended size", 100, og=_og())

# social_meta_completeness -- round(100 * present_required/4) - (og_url conflict: 20) - (no twitter card: 10); clamp 1
_SM = "score = round(100 * present_required/4) - (og_url_conflicts_canonical: 20) - (no_twitter_card: 10); clamp 1. Required: og:title, og:description, og:url, og:type. og:image is judged by og_image_validity only (2026-10-14: never reported twice)."
P("social_meta_completeness", "complete", _SM, 100, canonical_url="https://example.com/a")
P("social_meta_completeness", "no twitter card", _SM, 90, twitter={})
P("social_meta_completeness", "og:url conflicts canonical", _SM, 80, canonical_url="https://example.com/other")
P("social_meta_completeness", "missing og:type", _SM, 75, og=_og(**{"og:type": None}))
P("social_meta_completeness", "missing og:image is not counted", _SM, 100, og=_og(**{"og:image": None}))
P("social_meta_completeness", "2 of 4 + no card", _SM, 40, og=_og(**{"og:type": None, "og:url": None}), twitter={})
P("social_meta_completeness", "nothing, clamps to 1", _SM, 1, og={}, twitter={})

# meta_robots_conflicts
_MR = "noindex present, page not promoted internally (likely intentional)"
P("meta_robots_conflicts", "clean", "No restrictive directives", 100, meta_robots=None, noindex=False)
P("meta_robots_conflicts", "index + noindex", "Conflicting directives (e.g. index + noindex across meta and header)", 25, meta_robots="index, noindex", noindex=True)
P("meta_robots_conflicts", "nofollow", "nofollow at page level on an indexable page (wastes internal link equity)", 45, meta_robots="nofollow", noindex=False, nofollow=True)

# canonical_presence / conflicts
P("canonical_presence", "missing, indexable", "Canonical missing on an indexable page", 65, canonical_url=None)
P("canonical_presence", "relative", "Canonical is relative, malformed, or empty", 45, canonical_url="/a")
P("canonical_presence", "valid", "Single valid canonical (self or intentional cross)", 100, canonical_url="https://example.com/a")
P("canonical_conflicts", "self-referential", "No conflicts", 100, canonical_url="https://example.com/a", canonical_matches=True)

# meta_refresh_redirect
P("meta_refresh_redirect", "none", "None present", 100, head_meta={"viewport": "w", "refresh": None})
P("meta_refresh_redirect", "delay 0", "Meta refresh with delay 0 or JS redirect replacing an HTTP redirect", 35, head_meta={"viewport": "w", "refresh": "0; url=/x"})
P("meta_refresh_redirect", "delay 5", "Meta refresh with delay > 0 (interstitial-style)", 50, head_meta={"viewport": "w", "refresh": "5; url=/x"})

# broken_page_4xx -- bands depend on inlinks/sitemap/Google/past-life evidence only the sweep sees,
# so the cases run through PAGE_CHECKS (the wrapper `_weigh_broken_page`), never the bare function.
def _broken(inlinks: int = 0, sitemap: bool = False, worked: bool = False, status: int = 404):
    def build():
        me = facts("me", http_status=status)
        site = SiteAggregates()
        site.internal_edges_resolved = 50
        if inlinks:
            site.inlinks["me"] = {f"s{i}" for i in range(inlinks)}
        site.sitemap_page_ids = {"me"} if sitemap else set()
        site.ever_worked_page_ids = {"me"} if worked else set()
        return me, site

    return build


def Y(key: str, label: str, clause: str, expected: Any, build: Callable[[], tuple[PageFacts, SiteAggregates]]):
    """Register a case run through the sweep's wrapped per-page check: ``A.PAGE_CHECKS[key]``."""

    def run() -> CheckOutcome:
        f, site = build()
        return A.PAGE_CHECKS[key](f, site)

    CASES.append(Case(key, label, clause, expected, run))


Y("broken_page_4xx", "10 inlinks", "4xx with >=10 internal inlinks or in sitemap", 5, _broken(inlinks=10))
Y("broken_page_4xx", "in sitemap", "4xx with >=10 internal inlinks or in sitemap", 5, _broken(sitemap=True))
Y("broken_page_4xx", "9 inlinks", "4xx with 1-9 internal inlinks", 15, _broken(inlinks=9))
Y("broken_page_4xx", "1 inlink", "4xx with 1-9 internal inlinks", 15, _broken(inlinks=1))
Y("broken_page_4xx", "once loaded", "4xx with no internal references, but Google shows the address, it once loaded, or a sitemap older than 30 days listed it", 40, _broken(worked=True))
Y("broken_page_4xx", "nothing vouches", "4xx that nothing vouches for (no inlinks, no sitemap entry, no Google impressions, never loaded)", None, _broken())
P("broken_page_4xx", "200", "Status 200", 100, http_status=200)


# meta_robots_conflicts: the noindex-not-promoted rule lives in the sweep wrapper (`_weigh_noindex_page`)
def _noindexed(inlinks: int = 0, sitemap: bool = False):
    def build():
        me = facts("me", meta_robots="noindex", noindex=True)
        site = SiteAggregates()
        site.internal_edges_resolved = 50
        site.orphans = OrphanCensus(complete=True, known_live_pages=100, captured_pages=100)
        if inlinks:
            site.inlinks["me"] = {f"s{i}" for i in range(inlinks)}
        site.sitemap_page_ids = {"me"} if sitemap else set()
        return me, site

    return build


_NP = "noindex/none present AND page is in the sitemap or has >=5 internal inlinks"
Y("meta_robots_conflicts", "noindex, not promoted", _MR, 85, _noindexed())
Y("meta_robots_conflicts", "noindex, 4 inlinks is not promoted", _MR, 85, _noindexed(inlinks=4))
Y("meta_robots_conflicts", "noindex, 5 inlinks", _NP, 10, _noindexed(inlinks=5))
Y("meta_robots_conflicts", "noindex, in sitemap", _NP, 10, _noindexed(sitemap=True))

# server_error_5xx -- one rule: a confirmed 5xx or no response is 5
_5 = "5xx or no response, confirmed by a live recheck"
P("server_error_5xx", "500", _5, 5, http_status=500)
P("server_error_5xx", "no response", _5, 5, http_status=0)
P("server_error_5xx", "200", "Status 200", 100, http_status=200)


# redirect_chain -- hops: 1 -> 85, 2 -> 60, 3 -> 40, >=4 -> 20, none -> 100
def _chain(hops: int) -> dict:
    urls = [f"https://example.com/h{i}" for i in range(hops + 1)]
    return dict(redirect_chain=[{"url": u, "status": 301} for u in urls], http_status=200)


P("redirect_chain", "no redirect", "No redirect", 100, redirect_chain=[], http_status=200)
P("redirect_chain", "1 hop", "1 hop (single clean redirect)", 85, **_chain(1))
P("redirect_chain", "2 hops", "2 hops", 60, **_chain(2))
P("redirect_chain", "3 hops", "3 hops", 40, **_chain(3))
P("redirect_chain", "4 hops", ">=4 hops to reach final URL", 20, **_chain(4))
P("redirect_chain", "6 hops", ">=4 hops to reach final URL", 20, **_chain(6))

# redirect_loop
P("redirect_loop", "loop", "Loop detected in redirect trace", 1, redirect_chain=[{"url": "https://example.com/a"}, {"url": "https://example.com/b"}, {"url": "https://example.com/a"}])
P("redirect_loop", "no loop", "No loop", 100, redirect_chain=[{"url": "https://example.com/a"}, {"url": "https://example.com/b"}])

# content_needs_rendering -- an unrendered app frame (knob mirror: 20 visible words)
_R1 = "2xx page with an app root, an executable script, fewer than knowledge.scraper.audit.js_shell_word_limit visible words, no headings, links or images, and at most knowledge.scraper.audit.js_shell_root_text_words words of server-rendered text inside the app root"
_SHELL = dict(http_status=200, app_root=True, executable_script=True, headings=[], h1_count=0, link_count=0, internal_link_count=0, image_count=0, noindex=False)
P("content_needs_rendering", "shell, 19 words", _R1, 20, word_count=19, **_SHELL)
P("content_needs_rendering", "shell markup, 20 words", "Content is in the fetched HTML", 100, word_count=20, **_SHELL)
P("content_needs_rendering", "shell, 3 root words", _R1, 20, word_count=3, root_text_words=3, **_SHELL)
P("content_needs_rendering", "4 server-rendered root words", "Content is in the fetched HTML", 100, word_count=4, root_text_words=4, **_SHELL)
P("content_needs_rendering", "shell markup with a link", "Content is in the fetched HTML", 100, word_count=5, **{**_SHELL, "link_count": 1, "internal_link_count": 1})

# dead_end_page
_D1 = "Indexable 2xx page, not an app shell, with zero internal links"
_PAGE = dict(http_status=200, noindex=False, canonical_matches=True, app_root=False, executable_script=True, word_count=400, headings=[{"level": 1, "text": "x"}], h1_count=1, image_count=0, link_count=0)
P("dead_end_page", "no internal links", _D1, 70, internal_link_count=0, **_PAGE)
P("dead_end_page", "one internal link", "At least one internal link", 100, internal_link_count=1, **{**_PAGE, "link_count": 1})

# temporary_redirect_usage (the 3-session band needs history a page does not carry)
P("temporary_redirect_usage", "302 in latest session", "302/307 seen in latest session", 65, redirect_chain=[{"url": "https://example.com/a", "status": 302}], http_status=200)
P("temporary_redirect_usage", "301 only", "301/308 or no redirect", 100, redirect_chain=[{"url": "https://example.com/a", "status": 301}], http_status=200)

# soft_404_detection
_S1 = "200 page matches 404-template hash or title contains not-found phrasing with word_count < 50"
P("soft_404_detection", "not-found title, 49 words", _S1, 15, http_status=200, title="Page not found", word_count=49, headings=[{"level": 1, "text": "x"}], h1_count=1)
P("soft_404_detection", "not-found title, 50 words", "One weak signal only", 70, http_status=200, title="Page not found", word_count=50, headings=[{"level": 1, "text": "x"}], h1_count=1)
P("soft_404_detection", "blank page, 29 words", "200 page with word_count < 30 and no meaningful extracted content", 40, http_status=200, title="Welcome", word_count=29, headings=[], h1_count=0)
P("soft_404_detection", "real page", "No soft-404 signals", 100, http_status=200, title="Welcome", word_count=400, headings=[{"level": 1, "text": "x"}], h1_count=1)

# pagination_markup
P("pagination_markup", "self-referencing next", "rel=next or rel=prev points at the page itself", 25, pagination={"next": "https://example.com/a"})
P("pagination_markup", "coherent", "Coherent rel=prev/next declared", 100, pagination={"next": "https://example.com/a?p=2"})
P("pagination_markup", "none declared", "No pagination declared", None, pagination={})

# mixed_content
P("mixed_content", "none", "None", 100, mixed_content=[])
P("mixed_content", "active (script)", "Active mixed content (script/stylesheet/iframe over HTTP)", 20, mixed_content=["http://cdn.example.com/app.js"])
P("mixed_content", "passive (image)", "Passive mixed content only (images/media over HTTP)", 50, mixed_content=["http://cdn.example.com/p.png"])

# https_enforcement
P("https_enforcement", "served over http", "Page served over HTTP (final_url http://)", 5, url="http://example.com/a")
P("https_enforcement", "http variant 200", "HTTPS page but HTTP variant returns 200 (duplicate, no redirect)", 30, http_variant_probe={"status": 200, "location": None})
P("https_enforcement", "http variant 302", "HTTP variant redirects with 302 instead of 301", 70, http_variant_probe={"status": 302, "location": "https://example.com/a"})
P("https_enforcement", "http variant 301", "HTTPS with proper 301 from HTTP", 100, http_variant_probe={"status": 301, "location": "https://example.com/a"})

# page_weight -- > 5MB -> 40; <= 5MB -> 100
_MB5 = 5_000_000
P("page_weight", "5,000,000 bytes exactly", "<= 5MB HTML document", 100, response_bytes=_MB5)
P("page_weight", "5,000,001 bytes", "> 5MB HTML document", 40, response_bytes=_MB5 + 1)
P("page_weight", "500KB", "<= 5MB HTML document", 100, response_bytes=500_000)


# ttfb_server_response -- formula implemented independently from the contract text
def _ttfb_formula(t: int) -> int:
    if t <= 800:
        return 100 - math.floor(10 * t / 800)
    if t <= 1800:
        return 89 - math.floor(39 * (t - 800) / 1000)
    return max(1, 49 - math.floor((t - 1800) / 100))


_TF = "ttfb<=800ms: 100 - floor(10*ttfb/800) (pass, 90-100); 800<ttfb<=1800ms: 89 - floor(39*(ttfb-800)/1000) (warn, 50-89); ttfb>1800ms: max(1, 49 - floor((ttfb-1800)/100)) (fail)"
for t in (0, 1, 400, 799, 800, 801, 1300, 1800, 1801, 2800, 6700, 50_000):
    P("ttfb_server_response", f"{t}ms", _TF, _ttfb_formula(t), ttfb_ms=t)

# structured_data_validity
_sd = lambda *blocks, errors=(): {"blocks": list(blocks), "parse_errors": list(errors), "json_ld_raw": ["{"]}  # noqa: E731
P("structured_data_validity", "parse error", "Parse errors (invalid JSON-LD) present", 30, structured_data=_sd(errors=[{"index": 0, "source": "json-ld", "message": "bad"}]))
P("structured_data_validity", "required missing", "Required properties missing for a rich-result type in use", 50, structured_data=_sd({"source": "json-ld", "types": ["Product"], "data": {"description": "d"}}))
P(
    "structured_data_validity",
    "recommended missing",
    "Only recommended properties missing",
    75,
    structured_data=_sd({"source": "json-ld", "types": ["Article"], "data": {"headline": "h"}}),
)
P(
    "structured_data_validity",
    "all valid",
    "All markup valid (or no markup present - coverage item handles absence)",
    100,
    structured_data=_sd(
        {
            "source": "json-ld",
            "types": ["Article"],
            "data": {
                "headline": "h",
                "image": "https://example.com/i.jpg",
                "author": {"@type": "Person", "name": "A"},
                "datePublished": "2026-01-01",
                "dateModified": "2026-01-02",
                "publisher": {"@type": "Organization", "name": "O"},
            },
        }
    ),
)

# hreflang_validity
_hl = lambda *pairs: [{"lang": a, "href": b} for a, b in pairs]  # noqa: E731
_SELF = ("en", "https://example.com/a")
_FR = ("fr", "https://example.com/fr/a")
_XD = ("x-default", "https://example.com/a")
P("hreflang_validity", "invalid code", "Invalid language/region codes or relative URLs", 30, hreflang=_hl(_SELF, ("zz-ZZ-bogus!", "https://example.com/fr/a"), _XD))
P("hreflang_validity", "relative URL", "Invalid language/region codes or relative URLs", 30, hreflang=_hl(_SELF, ("fr", "/fr/a"), _XD))
P("hreflang_validity", "self-reference missing", "Hreflang set present but self-reference missing", 45, hreflang=_hl(_FR, ("de", "https://example.com/de/a"), ("x-default", "https://example.com/xd")))
P("hreflang_validity", "conflicts with canonical", "Hreflang URL conflicts with canonical (annotating a non-canonical URL)", 40, hreflang=_hl(_SELF, _FR, _XD), canonical_url="https://example.com/other")
P("hreflang_validity", "no x-default", "Missing x-default only", 80, hreflang=_hl(_SELF, _FR), canonical_url="https://example.com/a")
P("hreflang_validity", "valid", "Valid set (or page has no hreflang and site is single-language)", 100, hreflang=_hl(_SELF, _FR, _XD), canonical_url="https://example.com/a")


# --- lab performance (PageSpeed) -------------------------------------------


def _lab(**kw) -> dict:
    return dict(lab_performance=LabPerformance(strategy="mobile", observed_at=datetime.now(UTC), **kw))


# cwv_lcp: <=2500: 90-100 linear; 2500-4000: 50-89 linear; >4000: max(1, 49 - (lcp-4000)/200)
_L = "lcp<=2500ms: 90-100 linear; 2500-4000ms: 50-89 linear; >4000ms: max(1, 49 - (lcp-4000)/200)"
for v, exp in [(0, 100), (1250, (90, 100)), (2500, 90), (2501, (50, 89)), (3250, (50, 89)), (4000, 50), (4001, (48, 49)), (4200, 48), (30_000, 1)]:
    P("cwv_lcp", f"{v}ms", _L, exp, **_lab(lcp_ms=v))
# cwv_inp_tbt: tbt<=200: 90-100; 200-600: 50-89; >600: max(1, 49 - (tbt-600)/50)
_I = "tbt<=200ms: 90-100; 200-600ms: 50-89 linear; >600ms: max(1, 49 - (tbt-600)/50)"
for v, exp in [(0, 100), (200, 90), (201, (50, 89)), (400, (50, 89)), (600, 50), (650, 48), (5000, 1)]:
    P("cwv_inp_tbt", f"{v}ms", _I, exp, **_lab(tbt_ms=v))
# cwv_cls: <=0.1: 90-100; 0.1-0.25: 50-89; >0.25: max(1, 49 - (cls-0.25)*100)
_C = "cls<=0.1: 90-100; 0.1-0.25: 50-89 linear; >0.25: max(1, 49 - (cls-0.25)*100)"
for v, exp in [(0.0, 100), (0.1, 90), (0.11, (50, 89)), (0.25, 50), (0.26, 48), (1.0, 1)]:
    P("cwv_cls", f"{v}", _C, exp, **_lab(cls=v))
# asset_delivery: largest_saving<=250: 90-100; 250-1500: 50-89; >1500: max(10, 49 - (s-1500)/100)
_A = "largest_saving<=250ms: 90-100; 250-1500ms: 50-89 linear; >1500ms: max(10, 49 - (largest_saving-1500)/100)"
for v, exp in [(0, 100), (250, 90), (251, (50, 89)), (1500, 50), (1600, 48), (20_000, 10)]:
    P("asset_delivery", f"{v}ms", _A, exp, **_lab(delivery_savings_ms=float(v), delivery_audits={"render-blocking-resources": float(v)} if v else {}))
# caching_policy: round(100 * well_cached_bytes/static_bytes); 100 when negligible static bytes
_CP = "score = round(100 * well_cached_bytes/static_bytes); 100 when negligible static bytes"
_res = lambda nbytes: [{"url": "https://example.com/a.js", "cache_lifetime_ms": 0, "total_bytes": nbytes}]  # noqa: E731
P("caching_policy", "negligible static bytes", _CP, 100, **_lab(cache_static_bytes=100.0))
P("caching_policy", "all well cached", _CP, 100, **_lab(cache_static_bytes=1_000_000.0))
P("caching_policy", "25% poorly cached", _CP, 75, **_lab(cache_static_bytes=1_000_000.0, cache_short_ttl_resources=_res(250_000)))
P("caching_policy", "all poorly cached", _CP, 0 + 0, **_lab(cache_static_bytes=1_000_000.0, cache_short_ttl_resources=_res(1_000_000)))
CASES[-1].expected = (0, 1)  # round(100 * 0) = 0, scores are clamped to 1..100


# ---------------------------------------------------------------------------
# CROSS-PAGE CHECKS (web_crawl.analysis.CROSS_PAGE_CHECKS)
# ---------------------------------------------------------------------------


def facts(pid: str = "p0", **kw) -> PageFacts:
    base = dict(url=f"https://example.com/{pid}", page_id=pid, head_captured=True, og=dict(OG), twitter={})
    base.update(kw)
    return PageFacts(**base)


def X(key: str, label: str, clause: str, expected: Any, build: Callable[[], tuple[PageFacts, SiteAggregates]]):
    def run() -> CheckOutcome:
        f, site = build()
        return CROSS_PAGE_CHECKS[key](f, site)

    CASES.append(Case(key, label, clause, expected, run))


def _shared(group_attr: str, field_name: str, value: str, partners: int):
    def build():
        me = facts("me", **{field_name: value})
        others = [facts(f"o{i}", **{field_name: value}) for i in range(partners)]
        site = SiteAggregates()
        getattr(site, group_attr)[A._norm_text(value)] = [me, *others]
        return me, site

    return build


# title_duplication / meta_description_duplication
for n, exp, why in [
    (0, 100, "Title unique on site"),
    (1, 65, "Title shared with exactly 1 other page"),
    (2, 45, "Title shared with 2-9 other pages"),
    (9, 45, "Title shared with 2-9 other pages"),
    (10, 25, "Title shared with >= 10 other pages"),
]:
    X("title_duplication", f"{n} others", why, exp, _shared("pages_by_title", "title", "Same Title", n))
for n, exp, why in [
    (0, 100, "Unique"),
    (1, 60, "Shared with 1-9 other pages"),
    (9, 60, "Shared with 1-9 other pages"),
    (10, 40, "Shared with >= 10 other pages"),
]:
    X("meta_description_duplication", f"{n} others", why, exp, _shared("pages_by_description", "description", "Same description", n))


def _links(**kw):
    def build():
        me = facts("me")
        site = SiteAggregates()
        site.link_stats["me"] = PageLinkStats(**kw)
        return me, site

    return build


_urls = lambda n, tag="u": [f"https://example.com/{tag}{i}" for i in range(n)]  # noqa: E731

for n, exp, why in [
    (0, 100, "None"),
    (1, 65, "1-2 broken internal links"),
    (2, 65, "1-2 broken internal links"),
    (3, 45, "3-9 broken internal links"),
    (9, 45, "3-9 broken internal links"),
    (10, 20, ">= 10 broken internal links"),
]:
    X("broken_internal_links", f"{n} broken", why, exp, _links(checked=40, broken=_urls(n)))
for n, exp, why in [
    (0, 100, "No broken external targets"),
    (1, 65, "1 broken external target"),
    (2, 45, "2-4 broken external targets"),
    (4, 45, "2-4 broken external targets"),
    (5, 25, ">= 5 broken external targets"),
]:
    X("broken_external_links", f"{n} broken", why, exp, _links(checked=1, external_checked=20, external_broken=_urls(n)))

_IR = "score = round(100 * (1 - redirecting_outlinks/internal_outlinks)); floor 40 when redirecting_outlinks >= 20"
X("internal_redirect_links", "none", _IR, 100, _links(checked=10, internal_outlinks=10, outlinks_total=10))
X("internal_redirect_links", "2 of 10", _IR, 80, _links(checked=10, internal_outlinks=10, outlinks_total=10, redirecting=_urls(2)))
X("internal_redirect_links", "5 of 10", _IR, 50, _links(checked=10, internal_outlinks=10, outlinks_total=10, redirecting=_urls(5)))
X("internal_redirect_links", "20 of 25 floors at 40", _IR, 40, _links(checked=25, internal_outlinks=25, outlinks_total=25, redirecting=_urls(20)))


# duplicate_content_exact (the cluster case is a SITE ratio - see NOT_CHECKABLE_NOTES)
def _dup_unique():
    me = facts("me", exact_sha256="a" * 64, fingerprint_version=1)
    site = SiteAggregates()
    site.pages_by_sha[(1, "a" * 64)] = [me]
    return me, site


X("duplicate_content_exact", "unique", "score = round(100 * (1 - unconsolidated_dup_pages/indexable_pages)); min 10 when any cluster >= 10 pages", 100, _dup_unique)

# excessive_outlinks / nofollow_internal_links
for n, exp, why in [
    (150, 100, "<= 150 links"),
    (151, 85, "151-300 links"),
    (300, 85, "151-300 links"),
    (301, 65, "301-500 links"),
    (500, 65, "301-500 links"),
    (501, 45, "> 500 links on page"),
]:
    X("excessive_outlinks", f"{n} links", why, exp, _links(outlinks_total=n, internal_outlinks=n))
for n, exp, why in [
    (0, 100, "None"),
    (1, 70, "1-9 nofollowed internal links"),
    (9, 70, "1-9 nofollowed internal links"),
    (10, 45, ">= 10 nofollowed internal links on page"),
]:
    X("nofollow_internal_links", f"{n} nofollowed", why, exp, _links(outlinks_total=30, internal_outlinks=30, nofollow_internal_count=n, nofollow_internal_samples=_urls(min(n, 3))))

_AN = "score = round(100 * descriptive_anchors/internal_outlinks); 100 when no internal links"
X("anchor_text_descriptiveness", "all descriptive", _AN, 100, _links(outlinks_total=10, internal_outlinks=10, descriptive_anchors=10))
X("anchor_text_descriptiveness", "7 of 10", _AN, 70, _links(outlinks_total=10, internal_outlinks=10, descriptive_anchors=7, generic_anchor_targets=_urls(3)))
X("anchor_text_descriptiveness", "none descriptive", _AN, 0, _links(outlinks_total=10, internal_outlinks=10, descriptive_anchors=0, generic_anchor_targets=_urls(10)))
CASES[-1].expected = (0, 1)
X("anchor_text_descriptiveness", "no internal links", _AN, 100, _links(outlinks_total=4, internal_outlinks=0))


# crawl_depth / internal_inlink_coverage (graph must be representative or the checks say n_a)
def _graph(depth: int | None = None, inlinks: int | None = None):
    def build():
        me = facts("me")
        site = SiteAggregates()
        site.homepage_page_id = "home"
        site.internal_edges_resolved = 50
        site.orphans = OrphanCensus(complete=True, known_live_pages=100, captured_pages=100)
        if depth is not None:
            site.depth_by_page["me"] = depth
        if inlinks is not None:
            site.inlinks["me"] = {f"s{i}" for i in range(inlinks)}
        return me, site

    return build


for d, exp, why in [
    (3, 100, "Depth <= 3"),
    (4, 75, "Depth 4"),
    (5, 55, "Depth 5"),
    (6, 35, "Depth >= 6"),
    (12, 35, "Depth >= 6"),
]:
    X("crawl_depth", f"depth {d}", why, exp, _graph(depth=d))
for n, exp, why in [
    (1, 45, "1 unique inlink"),
    (2, 70, "2-4 unique inlinks"),
    (4, 70, "2-4 unique inlinks"),
    (5, 100, ">= 5 unique inlinks"),
]:
    X("internal_inlink_coverage", f"{n} inlinks", why, exp, _graph(inlinks=n))


# internal_link_equity -- only prioritized pages (target_keyword set) are judged; others 100; n_a under 30 scored pages
def _equity(percentile: int, keyword: str | None, scored: int = 41):
    def build():
        me = facts("me", link_score=0.5, target_keyword=keyword)
        site = SiteAggregates()
        site.link_equity_percentile_by_page = {f"q{i}": 50 for i in range(scored - 1)}
        site.link_equity_percentile_by_page["me"] = percentile
        return me, site

    return build


_LE = "prioritized page: score = pagerank_percentile, min(score, 40) when percentile < 25; non-prioritized page: 100"
X("internal_link_equity", "percentile 90, no keyword", _LE, 100, _equity(90, None))
X("internal_link_equity", "percentile 10, no keyword", _LE, 100, _equity(10, None))
X("internal_link_equity", "percentile 24, keyword", _LE, 24, _equity(24, "plumber"))
X("internal_link_equity", "percentile 25, keyword", _LE, 25, _equity(25, "plumber"))
X("internal_link_equity", "percentile 70, keyword", _LE, 70, _equity(70, "plumber"))
X("internal_link_equity", "under 30 pages scored", _LE, None, _equity(70, "plumber", scored=29))


# orphan_pages -- the SITE formula (per-page verdict is deliberately a fixed score; see NOTES)
@dataclass
class _Census:
    orphans: int
    known: int
    expected: int | tuple[int, int]


for orphans, known, exp in [(0, 100, 100), (2, 100, 98), (10, 100, 90), (50, 100, 50), (51, 100, 49), (100, 100, 5), (60, 100, 40)]:
    exp = exp
    CASES.append(
        Case(
            "orphan_pages",
            f"site formula {orphans}/{known}",
            "score = round(100 * (1 - orphan_count/known_live_pages)); floor 5 when orphan_count>0 and ratio>50%",
            exp,
            lambda o=orphans, k=known: CheckOutcome("pass", OrphanCensus(complete=True, known_live_pages=k, captured_pages=k, crawled_orphan_ids={f"o{i}" for i in range(o)}).site_score(), "site formula"),
        )
    )


# gsc_ctr_opportunity / gsc_performance_decay
def _gsc(current: GscPeriod, prior: GscPeriod | None = None, quarter: GscPeriod | None = None, history_days: int = 200):
    def build():
        me = facts("me")
        site = SiteAggregates()
        today = A._gsc_today()
        site.gsc = SiteGscEvidence(bound=True, earliest_date=today - timedelta(days=history_days), latest_date=today)
        site.gsc.by_page["me"] = PageGscStats(current=current, prior=prior or GscPeriod(), quarter=quarter or GscPeriod())
        return me, site

    return build


def _ctr_case(ratio: float, impressions: int):
    expected_ctr = A.expected_ctr_for_position(1.0)
    clicks = round(ratio * expected_ctr * impressions)
    return _gsc(GscPeriod(clicks=clicks, impressions=impressions, position=1.0))


_CT = "CTR < 30% of expected-for-position and impressions >= 1000"
X("gsc_ctr_opportunity", "20% of expected, 5000 impressions", _CT, 35, _ctr_case(0.20, 5000))
X("gsc_ctr_opportunity", "20% of expected, 500 impressions", "CTR < 50% of expected-for-position", 55, _ctr_case(0.20, 500))
X("gsc_ctr_opportunity", "40% of expected", "CTR < 50% of expected-for-position", 55, _ctr_case(0.40, 5000))
X("gsc_ctr_opportunity", "60% of expected", "CTR 50-80% of expected", 75, _ctr_case(0.60, 5000))
X("gsc_ctr_opportunity", "90% of expected", "CTR >= 80% of expected", 100, _ctr_case(0.90, 5000))


def _decay(drop: float):
    # clicks fell `drop` against BOTH comparison windows
    return _gsc(
        GscPeriod(clicks=round(1000 * (1 - drop)), impressions=20_000, position=5.0),
        GscPeriod(clicks=1000, impressions=20_000, position=5.0),
        GscPeriod(clicks=1000, impressions=20_000, position=5.0),
    )


X("gsc_performance_decay", "down 60%", "Clicks down > 50% vs prior period and vs last quarter", 30, _decay(0.60))
X("gsc_performance_decay", "down 50% exactly", "Clicks down 25-50% across both comparisons", 55, _decay(0.50))
X("gsc_performance_decay", "down 25%", "Clicks down 25-50% across both comparisons", 55, _decay(0.25))
X("gsc_performance_decay", "down 24%", "Clicks down 10-25%", 75, _decay(0.24))
X("gsc_performance_decay", "down 10%", "Clicks down 10-25%", 75, _decay(0.10))
X("gsc_performance_decay", "down 9%", "Stable or growing", 100, _decay(0.09))
X("gsc_performance_decay", "growing", "Stable or growing", 100, _decay(-0.30))


# local_business_markup
def _biz(*entities: dict, pages: int = 5):
    def build():
        me = facts("me")
        site = SiteAggregates()
        site.business = SiteBusinessEvidence(pages_captured=pages, entities=list(entities))
        return me, site

    return build


_NAP = {"types": ["LocalBusiness"], "name": "Acme", "address": "1 Main St", "telephone": "+1 555 0100"}
X("local_business_markup", "no entity anywhere", "No Organization/LocalBusiness markup anywhere on site", 50, _biz())
X("local_business_markup", "missing 2 core NAP", "Markup present but missing >= 2 core NAP properties", 65, _biz({"types": ["Organization"], "name": "Acme"}))
X("local_business_markup", "conflicting NAP", "Inconsistent NAP values across own pages", 55, _biz(_NAP, {**_NAP, "telephone": "+1 555 0199"}))
X("local_business_markup", "complete", "Complete, consistent entity markup", 100, _biz(_NAP, dict(_NAP)))


# hreflang_reciprocity -- round(100 * reciprocal_targets/declared_targets); n_a when no hreflang
def _recip(reciprocal: int, declared: int):
    def build():
        me_url = "https://example.com/p0"
        targets = [f"https://example.com/t{i}" for i in range(declared)]
        me = facts("p0", url=me_url, hreflang=[{"lang": "en", "href": me_url}] + [{"lang": f"l{i}", "href": t} for i, t in enumerate(targets)])
        site = SiteAggregates()
        for i, t in enumerate(targets):
            site.hreflang_targets[A.normalized_url_key(t)] = {A.normalized_url_key(me_url)} if i < reciprocal else set()
        return me, site

    return build


_HR = "score = round(100 * reciprocal_targets/declared_targets); not applicable when the page declares no hreflang"
X("hreflang_reciprocity", "4 of 4", _HR, 100, _recip(4, 4))
X("hreflang_reciprocity", "3 of 4", _HR, 75, _recip(3, 4))
X("hreflang_reciprocity", "1 of 3", _HR, 33, _recip(1, 3))
X("hreflang_reciprocity", "no hreflang", _HR, None, lambda: (facts("me"), SiteAggregates()))


# ---------------------------------------------------------------------------
# SITE CHECKS (web_crawl.analysis.SITE_CHECKS)
# ---------------------------------------------------------------------------


def S_(key: str, label: str, clause: str, expected: Any, build: Callable[[], SiteFacts]):
    def run() -> CheckOutcome:
        return SITE_CHECKS[key](build())

    CASES.append(Case(key, label, clause, expected, run))


_H4 = ("x-content-type-options", "x-frame-options", "referrer-policy", "content-security-policy")


def _headers(present: int):
    def build():
        sf = SiteFacts(site_id="s", https_pages=3)
        headers = {name: "v" for name in _H4[:present]}
        sf.header_samples = [(f"https://example.com/{i}", dict(headers)) for i in range(3)]
        return sf

    return build


_SH = "score = 100 - 15*missing_header_count (of the 4 baseline headers); clamp 40 minimum"
for present, exp in [(4, 100), (3, 85), (2, 70), (1, 55), (0, 40)]:
    S_("security_headers", f"{4 - present} missing", _SH, exp, _headers(present))


def _hsts(value: str | None):
    def build():
        sf = SiteFacts(site_id="s", https_pages=3)
        hdr = {"strict-transport-security": value} if value else {}
        sf.header_samples = [(f"https://example.com/{i}", dict(hdr)) for i in range(3)]
        return sf

    return build


S_("hsts_policy", "no header", "No HSTS header on HTTPS site", 55, _hsts(None))
S_("hsts_policy", "max-age one second short of 6 months", "HSTS present but max-age < 6 months", 75, _hsts("max-age=15551999"))
S_("hsts_policy", "max-age exactly 6 months", "HSTS with adequate max-age", 100, _hsts("max-age=15552000"))
S_("hsts_policy", "max-age 1 year", "HSTS with adequate max-age", 100, _hsts("max-age=31536000; includeSubDomains"))


def _tls(**kw):
    return lambda: SiteFacts(site_id="s", tls=TlsFacts(**kw))


S_("tls_certificate", "expired", "Certificate expired, untrusted, or hostname mismatch", 1, _tls(expired=True, days_to_expiry=-3))
S_("tls_certificate", "untrusted", "Certificate expired, untrusted, or hostname mismatch", 1, _tls(trusted=False, days_to_expiry=200))
S_("tls_certificate", "hostname mismatch", "Certificate expired, untrusted, or hostname mismatch", 1, _tls(hostname_match=False, days_to_expiry=200))
S_("tls_certificate", "7 days", "Expires within 7 days", 20, _tls(days_to_expiry=7))
S_("tls_certificate", "8 days", "Expires within 21 days", 50, _tls(days_to_expiry=8))
S_("tls_certificate", "21 days", "Expires within 21 days", 50, _tls(days_to_expiry=21))
S_("tls_certificate", "22 days", "Valid, > 21 days to expiry", 100, _tls(days_to_expiry=22))


def _near_dups(total: int, cluster: int):
    def build():
        pages = [NearDuplicatePage(page_id=f"p{i}", url=f"https://example.com/{i}", fingerprint_version=1, simhash64=f"{(i + 1) * 0x0101010101010101 % (1 << 64):016x}" if i >= cluster else "00000000000000ff") for i in range(total)]
        sf = SiteFacts(site_id="s")
        sf.near_duplicates = build_near_duplicate_report(pages)
        return sf

    return build


_ND = "score = round(100 * (1 - near_dup_pages/indexable_pages))"
S_("near_duplicate_content", "no near-duplicates", _ND, 100, _near_dups(20, 0))
S_("near_duplicate_content", "4 of 20 in one cluster", _ND, 80, _near_dups(20, 4))
S_("near_duplicate_content", "10 of 20 in one cluster", _ND, 50, _near_dups(20, 10))


def _cannibal(significant: int, cannibalized: int):
    def build():
        sf = SiteFacts(site_id="s")
        sf.gsc_cannibalization = GscCannibalizationEvidence(available=True, latest_date=date.today(), significant_queries=significant, cannibalized_queries=cannibalized)
        return sf

    return build


_GC = "score = round(100 * (1 - cannibalized_queries/significant_queries)); 100 when no significant queries"
S_("gsc_keyword_cannibalization", "no significant queries", _GC, 100, _cannibal(0, 0))
S_("gsc_keyword_cannibalization", "2 of 10", _GC, 80, _cannibal(10, 2))
S_("gsc_keyword_cannibalization", "1 of 3", _GC, 67, _cannibal(3, 1))
S_("gsc_keyword_cannibalization", "all", _GC, (1, 1), _cannibal(10, 10))


# --- crawlability (site_analysis) -------------------------------------------

ROOT = "https://example.com/"


def _evidence(**kw) -> SiteEvidence:
    return SiteEvidence(site_id="s", root_url=ROOT, canonical_host_form="https://example.com", **kw)


def _robots(status: int, content: str | None):
    def build():
        probe = SiteProbe(captured_at="2026-10-14T00:00:00Z", root_url=ROOT, robots=RobotsCapture(url=ROOT + "robots.txt", http_status=status, content=content))
        return SiteFacts(site_id="s", crawlability=_evidence(probe=probe))

    return build


S_("robots_txt_health", "5xx", "robots.txt responds 5xx (search engines treat the whole site as blocked)", 5, _robots(503, None))
S_("robots_txt_health", "Disallow: / for all", "Disallow: / applies to major search engine user-agents", 5, _robots(200, "User-agent: *\nDisallow: /\n"))
S_("robots_txt_health", "Disallow: / for Googlebot", "Disallow: / applies to major search engine user-agents", 5, _robots(200, "User-agent: Googlebot\nDisallow: /\n"))
S_("robots_txt_health", "invalid directive", "Invalid/unparseable directives or unsupported syntax present", 55, _robots(200, "User-agent: *\nDisalow: /x\nthis is not a directive\n"))
S_("robots_txt_health", "missing (404)", "robots.txt missing (404) - permitted but unmanaged", 80, _robots(404, None))
S_("robots_txt_health", "valid", "Valid file, no conflicts", 100, _robots(200, "User-agent: *\nDisallow: /admin/\nSitemap: https://example.com/sitemap.xml\n"))


def _sitemap(**kw):
    def build():
        docs = kw.pop("docs", [SitemapDocFacts(url=ROOT + "sitemap.xml", kind="urlset", status_code=200, fetch_error=None, url_count=100, is_active=True, last_fetched_at=None)])
        base = dict(sitemap_sync_ran=True, sitemaps=docs, sitemap_entries_total=100)
        base.update(kw)
        return SiteFacts(site_id="s", crawlability=_evidence(**base))

    return build


def _gone_probe():
    probe = SiteProbe(captured_at="2026-10-14T00:00:00Z", root_url=ROOT, sitemap_locations=[UrlProbe(url=ROOT + "sitemap.xml", http_status=404, final_url=ROOT + "sitemap.xml", final_status=404)])
    return SiteFacts(site_id="s", crawlability=_evidence(probe=probe))


S_("sitemap_health", "none found", "No sitemap found at declared/robots location and none discoverable", 50, _gone_probe)
S_(
    "sitemap_health",
    "declared but 404",
    "Sitemap unreachable (4xx/5xx) or XML unparseable",
    20,
    _sitemap(docs=[SitemapDocFacts(url=ROOT + "sitemap.xml", kind="urlset", status_code=404, fetch_error=None, url_count=None, is_active=True, last_fetched_at=None)], sitemap_entries_total=0),
)
S_("sitemap_health", "11% junk", ">10% of sitemap URLs are non-200, redirected, noindexed or robots-blocked", 35, _sitemap(junk_entry_count=11, junk_by_class={"non-200": _urls(11)}))
S_("sitemap_health", "10% junk", "1-10% junk entries", 65, _sitemap(junk_entry_count=10, junk_by_class={"non-200": _urls(10)}))
S_("sitemap_health", "1% junk", "1-10% junk entries", 65, _sitemap(junk_entry_count=1, junk_by_class={"non-200": _urls(1)}))
S_("sitemap_health", "missing lastmod only", "Minor issues only (missing lastmod, >50k/50MB split advisory)", 85, _sitemap(entries_missing_lastmod=30))
S_("sitemap_health", "clean", "Clean sitemap", 100, _sitemap())


def _coverage(total: int, covered: int, undiscovered: int = 0):
    return _sitemap(indexable_total=total, indexable_in_sitemap=covered, undiscovered_count=undiscovered, crawl_complete=True)


_SC = "score = round(100 * covered_indexable/indexable_total) - min(20, 2*sitemap_only_orphan_pct)"
S_("sitemap_coverage", "full", _SC, 100, _coverage(100, 100))
S_("sitemap_coverage", "90%", _SC, 90, _coverage(100, 90))
S_("sitemap_coverage", "full, 5% sitemap-only orphans", _SC, 90, _coverage(100, 100, undiscovered=5))
S_("sitemap_coverage", "full, 15% orphans capped at 20", _SC, 80, _coverage(100, 100, undiscovered=15))
S_("sitemap_coverage", "70% + 5% orphans", _SC, 60, _coverage(100, 70, undiscovered=5))


def _host(variants: list[UrlProbe], slash: list[SlashPairProbe] | None = None, link_forms: set[str] | None = None):
    def build():
        probe = SiteProbe(captured_at="2026-10-14T00:00:00Z", root_url=ROOT, variants=variants, slash_pairs=slash or [])
        return SiteFacts(site_id="s", crawlability=_evidence(probe=probe, internal_link_host_forms=link_forms or {"https://example.com"}))

    return build


_canon = UrlProbe(url="https://example.com/", http_status=200, final_url="https://example.com/", final_status=200)


def _redirect(url: str, status: int, hops: int = 1):
    return UrlProbe(url=url, http_status=status, final_url="https://example.com/", final_status=200, redirect_chain=[{"url": url, "status": status}] * hops)


_live_www = UrlProbe(url="https://www.example.com/", http_status=200, final_url="https://www.example.com/", final_status=200)
_live_http = UrlProbe(url="http://example.com/", http_status=200, final_url="http://example.com/", final_status=200)
_dup_slash = SlashPairProbe(
    path="/about",
    bare=UrlProbe(url="https://example.com/about", http_status=200, final_url="https://example.com/about", final_status=200),
    slashed=UrlProbe(url="https://example.com/about/", http_status=200, final_url="https://example.com/about/", final_status=200),
)
S_("host_protocol_consistency", "2 variants answer 200", ">= 2 host/protocol variants return 200 without redirecting to canonical form", 25, _host([_canon, _live_www, _live_http]))
S_("host_protocol_consistency", "variant redirects with 302", "Variants redirect but with 302 or chains", 60, _host([_canon, _redirect("http://example.com/", 302)]))
S_("host_protocol_consistency", "variant redirect chain of 3", "Variants redirect but with 302 or chains", 60, _host([_canon, _redirect("http://example.com/", 301, hops=3)]))
S_("host_protocol_consistency", "trailing-slash duplicate", "A sampled path serves its own 200 at BOTH <path> and <path>/ (trailing-slash duplicate)", 65, _host([_canon, _redirect("http://example.com/", 301)], slash=[_dup_slash]))
S_("host_protocol_consistency", "mixed internal link hosts", "Internal links mix host forms (even if redirected)", 70, _host([_canon, _redirect("http://example.com/", 301)], link_forms={"https://example.com", "https://www.example.com"}))
S_("host_protocol_consistency", "single canonical form", "Single canonical form, clean 301s from all variants", 100, _host([_canon, _redirect("http://example.com/", 301)]))


# ---------------------------------------------------------------------------
# Known disagreements (code vs contract), found when this guard was first run
# ---------------------------------------------------------------------------
# cid -> what the code does instead. Strict xfail: fixing the code (or the
# contract) turns the case red until the entry is deleted.

KNOWN_DISAGREEMENTS: dict[str, str] = {}

# ---------------------------------------------------------------------------
# Coverage meta-test: every deterministic/formula key has a case or a reason
# ---------------------------------------------------------------------------

#: Cataloged, deterministic/formula, and NO check function exists - the row is
#: scored by nothing today. If someone implements one, this entry must go and
#: a conformance case must be written (the meta-test enforces both).
NOT_IMPLEMENTED: dict[str, str] = {
    "a11y_lab_basics": "no check function: formula over the Lighthouse accessibility score is not implemented anywhere",
    "content_freshness": "no check function: nothing scores 'unchanged > 24 months'",
    "gsc_index_coverage": "no check function: the indexed/indexable_known formula is not implemented",
    "mobile_usability_lab": "no check function: the tap-target/font-size/content-width formula is not implemented",
    "owned_domain_redirect": "no check function (same contract text as host_protocol_consistency, tier NULL); nothing is registered under this key",
    "readability": "no check function: Flesch-band formula is not implemented",
    "title_keyword_alignment": "no check function: keyword/title token matching is not implemented",
}

#: Registered, but the contract cannot be exercised as a pure function of the
#: evidence the check receives. Cases (if any) cover only the part that can be.
NOT_CHECKABLE: dict[str, str] = {}

NOT_CHECKABLE_NOTES = """
duplicate_content_exact : contract is a SITE ratio (unconsolidated_dup_pages/indexable_pages); the per-page check scores cluster size. Only the 'unique -> 100' band is exercised.
orphan_pages            : contract is the SITE formula (OrphanCensus.site_score, exercised); the per-page verdict is a documented fixed score (ORPHAN_PAGE_SCORE).
"""


def test_every_catalogued_check_has_a_conformance_case_or_a_reason():
    registered = set(SEO_PAGE_CHECKS) | set(CROSS_PAGE_CHECKS) | set(SITE_CHECKS)
    covered = {c.key for c in CASES}
    problems: list[str] = []
    for key in CATALOGUE:
        if key in NOT_IMPLEMENTED:
            if key in registered:
                problems.append(f"{key}: now implemented - delete it from NOT_IMPLEMENTED and write cases")
            continue
        if key not in registered:
            problems.append(f"{key}: cataloged but has no check function and is not in NOT_IMPLEMENTED")
        elif key in NOT_CHECKABLE:
            continue
        elif key not in covered:
            problems.append(f"{key}: registered check without a conformance case")
    for key in set(NOT_IMPLEMENTED) | set(NOT_CHECKABLE):
        if key not in CATALOGUE:
            problems.append(f"{key}: allowlisted but not in the catalog snapshot")
    for key in registered - set(CATALOGUE):
        problems.append(f"{key}: registered check with no catalog row")
    assert not problems, "\n".join(problems)


def test_every_case_cites_a_real_piece_of_its_contract():
    bad = [c.cid for c in CASES if c.clause not in _contract_text(c.key).replace('\\"', '"')]
    assert not bad, f"clause not found verbatim in the contract: {bad}"


#: Contract bands the check's INPUT cannot express, so no case can reach them. Each
#: is a gap between catalog and code (the evidence the band needs is never handed
#: to the check). Stale entries are refused: an entry must be a real rule and must
#: NOT also be cited by a case.
UNREACHABLE_BANDS: dict[tuple[str, str], str] = {
    ("title_presence", "Multiple title tags"): "PageEvidence carries one title string, no tag count",
    ("title_presence", "Title present but only site/brand name (no page-specific words)"): "no brand/site-name evidence reaches the check",
    ("canonical_presence", "Multiple canonical tags with different targets"): "PageEvidence carries one canonical_url, no tag count",
    ("meta_description_presence", "Multiple meta description tags"): "PageEvidence carries one description string, no tag count",
    ("canonical_conflicts", "Canonical target returns 4xx/5xx or is noindexed/robots-blocked"): "needs a fetch of the canonical target; page evidence has none",
    ("canonical_conflicts", "Canonical target redirects (chain) or itself canonicalizes elsewhere"): "needs a fetch of the canonical target; page evidence has none",
    ("canonical_conflicts", "Canonical contradicts og:url, hreflang self-reference, or sitemap URL form"): "check only has canonical_matches; code scores off-domain 25 / noindex 20 / other 55, none of which the contract names",
    ("temporary_redirect_usage", "302/307 stable across >=3 crawl sessions"): "crawl-session history never reaches the check",
    ("h1_presence", "H1 duplicated on other pages of the site"): "H1 text is not collected and the check is per-page, so duplicates are never detected",
    ("og_image_validity", "Image below recommended 1200x630"): "image dimensions never reach the check; a valid-looking og:image always scores 100",
    ("robots_txt_health", "Directives block URLs that are listed in the XML sitemap or are marked indexable"): "needs sitemap membership + indexable URL list inside SiteEvidence",
}


def test_every_rule_band_and_boundary_is_exercised():
    """Each deterministic rule's `when` text is cited by at least one case, or is a
    band the page-level evidence cannot express (listed, with the reason)."""
    unreachable_bands = UNREACHABLE_BANDS
    cited = {(c.key, c.clause) for c in CASES}
    missing: list[str] = []
    for key, row in CATALOGUE.items():
        if key in NOT_IMPLEMENTED or key in NOT_CHECKABLE:
            continue
        for rule in row["score_contract"].get("rules") or []:
            when = rule["when"]
            if (key, when) not in cited and (key, when) not in unreachable_bands:
                missing.append(f"{key}: '{when}'")
    assert not missing, "contract rules with no case:\n" + "\n".join(missing)


# ---------------------------------------------------------------------------
# The conformance table itself
# ---------------------------------------------------------------------------


def _params():
    out = []
    for c in CASES:
        marks = []
        if c.cid in KNOWN_DISAGREEMENTS:
            marks.append(pytest.mark.xfail(strict=True, reason=KNOWN_DISAGREEMENTS[c.cid]))
        out.append(pytest.param(c, id=c.cid, marks=marks))
    return out


@pytest.mark.parametrize("c", _params())
def test_check_scores_what_its_contract_says(c: Case):
    outcome = c.run()
    got = outcome.score
    assert _matches(got, c.expected), (
        f"{c.key} [{c.label}]\n  contract says: {c.clause!r} -> {c.expected}\n  code gives: status={outcome.status} score={got}\n  reasoning: {outcome.reasoning[:200]}"
    )


# ---------------------------------------------------------------------------
# Severity follows the documented tier rule
# ---------------------------------------------------------------------------


@dataclass
class _Item:
    tier: str | None
    severity_map: dict = field(default_factory=dict)


def _band(severity_map: dict, score: int) -> str:
    for band in severity_map["bands"]:
        if score <= band["max"]:
            return band["severity"]
    return "info"


def _step(sev: str, by: int) -> str:
    return SEVERITY_ORDER[max(0, min(len(SEVERITY_ORDER) - 1, SEVERITY_ORDER.index(sev) + by))]


def _rank(sev: str) -> int:
    return SEVERITY_ORDER.index(sev)


def _documented_tier_rule(tier: str | None, base: str) -> str:
    """The rule as the docstring states it - written out independently."""
    if base == "info":
        return "info"
    if tier == "D":
        return "info"
    if tier == "A":  # one step up, never below high once failing
        sev = _step(base, 1)
        return sev if _rank(sev) >= _rank("high") else "high"
    if tier == "B":  # capped at high
        return base if _rank(base) <= _rank("high") else "high"
    if tier == "C":  # capped at low
        return base if _rank(base) <= _rank("low") else "low"
    return base


@pytest.mark.parametrize("key", sorted(CATALOGUE))
def test_severity_follows_the_tier_rule(key: str):
    row = CATALOGUE[key]
    item = _Item(tier=row["tier"], severity_map=row["severity_map"])
    for score in range(1, 101):
        expected = _documented_tier_rule(row["tier"], _band(row["severity_map"], score))
        assert severity_for(item, score) == expected, f"{key} tier={row['tier']} score={score}"
    # scoreless outcomes carry no judgment, whatever the tier
    assert severity_for(item, None) == "info"


@pytest.mark.parametrize("tier", ["A", "B", "C", "D"])
def test_tier_extremes_hold_for_any_band_set(tier: str):
    """Independent of the live rows: the cap/floor invariants themselves."""
    wide = {"bands": [{"max": 10, "severity": "critical"}, {"max": 30, "severity": "high"}, {"max": 60, "severity": "med"}, {"max": 85, "severity": "low"}, {"max": 100, "severity": "info"}]}
    item = _Item(tier=tier, severity_map=wide)
    worst = severity_for(item, 1)
    mild = severity_for(item, 80)  # band 'low'
    passing = severity_for(item, 100)
    assert passing == "info"
    if tier == "A":
        assert worst == "critical" and _rank(mild) >= _rank("high")
    elif tier == "B":
        assert worst == "high" and mild == "low"
    elif tier == "C":
        assert worst == "low" and mild == "low"
    else:
        assert worst == "info" and mild == "info"
    # homepage failure moves one step up, except tier D
    homepage = severity_for(item, 80, on_homepage=True)
    assert (homepage == "info") if tier == "D" else (_rank(homepage) > _rank(mild) or homepage == "critical")


def test_unreachable_band_list_has_no_stale_entries():
    real = {(k, r["when"]) for k, row in CATALOGUE.items() for r in row["score_contract"].get("rules") or []}
    cited = {(c.key, c.clause) for c in CASES}
    stale = [e for e in UNREACHABLE_BANDS if e not in real]
    now_reachable = [e for e in UNREACHABLE_BANDS if e in cited]
    assert not stale, f"not a rule in the contract any more: {stale}"
    assert not now_reachable, f"a case now reaches these - delete them from UNREACHABLE_BANDS: {now_reachable}"
