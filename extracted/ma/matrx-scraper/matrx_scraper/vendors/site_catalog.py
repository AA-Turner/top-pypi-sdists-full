"""The curated catalog of NON-SOCIAL sites Bright Data returns structured records for.

Social profiles and posts (Instagram, TikTok, YouTube, X, Threads, Reddit,
Pinterest, Facebook posts, LinkedIn people/posts) belong to matrx-social and are
deliberately absent.

``required_fields`` were read off Bright Data's own free 400 validation answer
(2026-10-11). ``verified=False`` entries either answered "This dataset does not support
collection" on our account or failed every live call (blocked, sign-in wall,
never finished); each says which. They are listed so the gap is visible, and
both ``match()`` and ``get_entry(..., verified_only=True)`` skip them.

``auto_route`` = a URL matching this entry is routed to site data BEFORE the
plain HTTP fetch in ``read_page``. Where two entries share a host the general
one routes (place info beats reviews); the other is reachable by key.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal
from urllib.parse import urlparse


@dataclass(frozen=True)
class CatalogEntry:
    key: str
    label: str
    dataset_id: str
    input_kind: Literal["url", "discover"]
    host_pattern: str = ""
    path_pattern: str = ""
    discover_by: str | None = None
    required_fields: tuple[str, ...] = ("url",)
    #: The input field a free-text ``query`` fills (discover entries).
    query_field: str | None = None
    #: The input field a free-text ``location`` fills, when the mode takes one.
    location_field: str | None = None
    #: An input field that caps records per input (filled with ``max_records``).
    limit_field: str | None = None
    #: ``path_pattern`` is searched against ``path?query``.
    #: Inputs filled in when the caller leaves them out.
    defaults: dict[str, Any] = field(default_factory=dict)
    auto_route: bool = False
    verified: bool = True
    #: The record field that names ONE record across fetches (a review id, a place id, an ASIN)
    #: — what a stored table upserts on. ``None`` = the record's ``url``. A record missing it is
    #: keyed by the next lawful identity (see aidream ``services/data_fetch/mapper.py``).
    key_field: str | None = None
    #: Said plainly to the person when a fetch from this source runs anyway (it still runs:
    #: defaults lean open) — ``None`` = no known problem.
    known_issue: str | None = None
    #: A disabled entry is not resolvable at all (an admin switched it off).
    enabled: bool = True
    #: Keyword-style ways to ask a link-mode source for records without a link: option name
    #: -> the input fields that option needs (e.g. ``{"keywords": ("keywords",)}``).
    discover_options: dict[str, tuple[str, ...]] = field(default_factory=dict)
    #: A link source that also takes a business NAME (+ city/area) in place of its link: a row with ``name`` and
    #: no ``url`` becomes ``keyword = "<name> <city>"`` plus these defaults (``{"country": "US"}``), which is the
    #: source's own ``location`` discover option. Empty = the source does not take a name. A row with a link is
    #: never touched.
    name_search: dict[str, Any] = field(default_factory=dict)

    def apply_name_search(self, row: dict[str, Any]) -> None:
        """Rewrite a link-less ``name`` (+ ``city``/``area``) row into the keyword row the vendor takes."""
        if not self.name_search or row.get("url") not in (None, "") or row.get("keyword") not in (None, ""):
            return
        name = str(row.get("name") or "").strip()
        if not name:
            return
        where = next((str(row[k]).strip() for k in ("city", "area", "location") if str(row.get(k) or "").strip()), "")
        row["keyword"] = f"{name} {where}".strip()
        for k in ("name", "city", "area", "location"):
            row.pop(k, None)
        for k, v in self.name_search.items():
            row.setdefault(k, v)

    def discover_for(self, row: dict[str, Any]) -> str | None:
        """The discover option a link-less input row asks for, or ``None`` (use the link)."""
        if self.input_kind == "discover":
            return self.discover_by
        if row.get("url") not in (None, ""):
            return None
        for name, needs in self.discover_options.items():
            if needs and all(row.get(f) not in (None, "") for f in needs):
                return name
        return None

    def missing(self, row: dict[str, Any]) -> list[str]:
        """The input fields this row lacks (a link-less keyword row needs its option's fields)."""
        option = self.discover_for(row) if self.input_kind == "url" else None
        needed = self.discover_options.get(option, ()) if option else self.required_fields
        return [f for f in needed if row.get(f) in (None, "")]

    def matches(self, url: str) -> bool:
        if self.input_kind != "url" or not self.host_pattern:
            return False
        try:
            parsed = urlparse(url)
        except ValueError:
            return False
        host = (parsed.hostname or "").lower()
        if not re.search(self.host_pattern, host):
            return False
        target = (parsed.path or "/") + (f"?{parsed.query}" if parsed.query else "")
        return not self.path_pattern or bool(re.search(self.path_pattern, target))


def _u(key: str, label: str, dataset_id: str, host: str, path: str = "", **kw: Any) -> CatalogEntry:
    return CatalogEntry(key=key, label=label, dataset_id=dataset_id, input_kind="url",
                        host_pattern=host, path_pattern=path, **kw)


def _d(key: str, label: str, dataset_id: str, *, discover_by: str, required: tuple[str, ...],
       query_field: str, location_field: str | None = None, **kw: Any) -> CatalogEntry:
    return CatalogEntry(key=key, label=label, dataset_id=dataset_id, input_kind="discover",
                        discover_by=discover_by, required_fields=required, query_field=query_field,
                        location_field=location_field, **kw)


_GOOGLE = r"(^|\.)google\.[a-z.]+$"

CATALOG: tuple[CatalogEntry, ...] = (
    # ── Local businesses and reviews ─────────────────────────────────────
    _u("google_maps_place", "Google Maps place", "gd_m8ebnr0q2qlklc02fz", _GOOGLE,
       # Only place_id-style URLs (…/data=…!1s0x…): name-only /maps/place/<name> URLs come back
       # dead_page "Got place without category value" (live, 2026-10-11).
       r"^/maps/place/.*(data=.*!1s0x|[?&]q=place_id:)", auto_route=True, key_field="place_id",
       # Without a link: a business name (+ city) or a place id — the vendor's own discover options.
       discover_options={"location": ("country", "keyword"), "place_id": ("place_id",), "cid": ("CID",)},
       name_search={"country": "US"}),
    # crawl_error "Sign in modal hides the Reviews" on every live call (2026-10-11).
    _u("google_maps_reviews", "Google Maps reviews", "gd_luzfs1dn2oa0teb81", _GOOGLE, r"^/maps/place/",
       verified=False, key_field="review_id",
       known_issue="Reviews are hidden behind a sign-in wall right now, so this may return nothing."),
    _u("yelp_business", "Yelp business", "gd_lgugwl0519h1p14rwk", r"(^|\.)yelp\.[a-z.]+$", r"^/biz/",
       verified=False,  # "You have been blocked" on both live URLs (2026-10-11)
       known_issue="This site blocks collection right now."),
    _u("yelp_reviews", "Yelp reviews", "gd_lgzhlu9323u3k24jkv", r"(^|\.)yelp\.[a-z.]+$", r"^/biz/",
       verified=False, key_field="review_id",  # same block as yelp_business
       known_issue="This site blocks collection right now."),
    _u("trustpilot_reviews", "Trustpilot reviews", "gd_lm5zmhwd2sni130p", r"(^|\.)trustpilot\.com$",
       r"^/review/", limit_field="num_of_reviews_limit", auto_route=True, key_field="review_id"),
    # ── Companies and jobs ───────────────────────────────────────────────
    _u("glassdoor_company", "Glassdoor company", "gd_l7j0bx501ockwldaqf", r"(^|\.)glassdoor\.[a-z.]+$",
       r"^/Overview/", auto_route=True, key_field="company_id"),
    _u("glassdoor_reviews", "Glassdoor reviews", "gd_l7j1po0921hbu0ri1z", r"(^|\.)glassdoor\.[a-z.]+$",
       r"^/Reviews/", required_fields=("url", "days"), defaults={"days": 365}, auto_route=True, key_field="review_id"),
    _u("glassdoor_jobs", "Glassdoor job listing", "gd_lpfbbndm1xnopbrcr0", r"(^|\.)glassdoor\.[a-z.]+$",
       r"^/job-listing/", auto_route=True, key_field="job_posting_id"),
    _d("glassdoor_jobs_search", "Glassdoor job search", "gd_lpfbbndm1xnopbrcr0", discover_by="keyword",
       required=("keyword", "location"), query_field="keyword", location_field="location", key_field="job_posting_id"),
    _u("indeed_jobs", "Indeed job listing", "gd_l4dx9j9sscpvs7no2", r"(^|\.)indeed\.[a-z.]+$",
       r"^/(viewjob|rc/clk|m/viewjob)", auto_route=True, key_field="jobid"),
    _d("indeed_jobs_search", "Indeed job search", "gd_l4dx9j9sscpvs7no2", discover_by="keyword",
       required=("keyword_search", "location", "country", "domain"), query_field="keyword_search",
       location_field="location", defaults={"country": "US", "domain": "indeed.com"},
       verified=False, key_field="jobid",  # discover never finished
       known_issue="Searching by keyword does not finish right now; give a job link instead."),  #: >15 min and >180 s on two live tries (2026-10-11)
    _u("indeed_company", "Indeed company", "gd_l7qekxkv2i7ve6hx1s", r"(^|\.)indeed\.[a-z.]+$", r"^/cmp/",
       auto_route=True),
    _u("linkedin_company", "LinkedIn company", "gd_l1vikfnt1wgvvqz95w", r"(^|\.)linkedin\.com$",
       r"^/company/", auto_route=True),
    _u("linkedin_job", "LinkedIn job listing", "gd_lpfll7v5hcqtkxl6l", r"(^|\.)linkedin\.com$",
       r"^/jobs/view/", auto_route=True, key_field="job_posting_id"),
    _d("linkedin_jobs_search", "LinkedIn job search", "gd_lpfll7v5hcqtkxl6l", discover_by="keyword",
       required=("location",), query_field="keyword", location_field="location", key_field="job_posting_id"),
    _u("crunchbase_company", "Crunchbase company", "gd_l1vijqt9jfj7olije", r"(^|\.)crunchbase\.com$",
       r"^/organization/", auto_route=True),
    # ── Shopping ─────────────────────────────────────────────────────────
    _u("amazon_product", "Amazon product", "gd_l7q7dkf244hwjntr0", r"(^|\.)amazon\.[a-z.]+$",
       r"(/dp/|/gp/product/)", auto_route=True, key_field="asin"),
    _d("amazon_product_search", "Amazon product search", "gd_l7q7dkf244hwjntr0", discover_by="keyword",
       required=("keyword",), query_field="keyword", key_field="asin"),
    _u("amazon_reviews", "Amazon reviews", "gd_le8e811kzy4ggddlq", r"(^|\.)amazon\.[a-z.]+$",
       r"/product-reviews/", auto_route=True, key_field="review_id"),
    _u("amazon_search", "Amazon search results page", "gd_lwdb4vjm1ehb499uxs", r"(^|\.)amazon\.[a-z.]+$",
       r"^/s(\?|$)", required_fields=("keyword", "url"), key_field="asin"),
    _u("walmart_product", "Walmart product", "gd_l95fol7l1ru6rlo116", r"(^|\.)walmart\.com$", r"^/ip/",
       auto_route=True, key_field="product_id"),
    _d("walmart_product_search", "Walmart product search", "gd_l95fol7l1ru6rlo116", discover_by="keyword",
       required=("keyword", "domain"), query_field="keyword", defaults={"domain": "https://www.walmart.com/"}, key_field="product_id"),
    _u("google_shopping", "Google Shopping product", "gd_ltppk50q18kdw67omz", _GOOGLE, r"^/shopping/product/",
       auto_route=True),
    _d("google_shopping_search", "Google Shopping search", "gd_ltppk50q18kdw67omz", discover_by="keyword",
       required=("keyword", "country"), query_field="keyword", defaults={"country": "US"}),
    _u("facebook_marketplace", "Facebook Marketplace listing", "gd_lvt9iwuh6fbcwmx1a",
       r"(^|\.)facebook\.com$", r"^/marketplace/item/", auto_route=True),
    _d("facebook_marketplace_search", "Facebook Marketplace search", "gd_lvt9iwuh6fbcwmx1a",
       discover_by="keyword", required=("keyword", "city"), query_field="keyword", location_field="city"),
    # ── Real estate and travel ───────────────────────────────────────────
    _u("zillow_listing", "Zillow listing", "gd_lfqkr8wm13ixtbd8f5", r"(^|\.)zillow\.com$", r"^/homedetails/",
       auto_route=True),
    _u("airbnb_listing", "Airbnb listing", "gd_ld7llo0n20qqycm0kt", r"(^|\.)airbnb\.[a-z.]+$", r"^/rooms/",
       verified=False, known_issue="Collection failed in our last tests."),
    _u("booking_hotel", "Booking.com hotel", "gd_lbknif9rvpu1yd7bg", r"(^|\.)booking\.com$", r"^/hotel/",
       verified=False, known_issue="Collection failed in our last tests."),
    # ── Software, apps, events, Q&A, video, ads ──────────────────────────
    _u("g2_product", "G2 product", "gd_l88xp4k01qnhvyqlvw", r"(^|\.)g2\.com$", r"^/products/[^/]+/?$",
       verified=False, known_issue="Collection failed in our last tests."),
    _u("g2_reviews", "G2 reviews", "gd_l88xvdka1uao86xvlb", r"(^|\.)g2\.com$", r"^/products/[^/]+/reviews",
       auto_route=True, key_field="review_id"),
    _u("google_play_app", "Google Play app", "gd_lsk382l8xei8vzm4u", r"^play\.google\.com$",
       r"^/store/apps/details", auto_route=True),
    _u("google_play_reviews", "Google Play reviews", "gd_m6zagkt024uwvvwuyu", r"^play\.google\.com$",
       r"^/store/apps/details", key_field="review_id"),
    _u("facebook_event", "Facebook event", "gd_m14sd0to1jz48ppm51", r"(^|\.)facebook\.com$", r"^/events/\d",
       auto_route=True),
    _u("quora_post", "Quora question", "gd_lvz1rbj81afv3m6n5y", r"(^|\.)quora\.com$", r"^/(?!profile/|topic/|search|spaces?/)[^/]+/?$",
       auto_route=True),
    _u("vimeo_video", "Vimeo video", "gd_lxk88z3v1ketji4pn", r"(^|\.)vimeo\.com$", r"^/\d+", auto_route=True),
    _u("google_ads_transparency", "Google Ads Transparency advertiser", "gd_mrlukk9z16grjek1gv",
       r"^adstransparency\.google\.com$", r"^/advertiser/", verified=False,
       known_issue="Collection failed in our last tests."),
)

# ── the live catalog ─────────────────────────────────────────────────────
# ``CATALOG`` above is only the BUNDLED SEED (what ``catalog_seed`` turns into the platform's
# ``scraper.data_source`` rows, and what a bare standalone install resolves against). A host
# that owns the real catalog registers ``configure_ext(site_catalog_loader=async () -> list[
# CatalogEntry])``; every async entry point calls ``ensure_catalog()`` first, which installs
# what the loader returns. One catalog at runtime: the host's.

_ENTRIES: tuple[CatalogEntry, ...] = CATALOG
_BY_KEY: dict[str, CatalogEntry] = {e.key: e for e in CATALOG}
EXT_CATALOG_LOADER = "site_catalog_loader"


def install_catalog(entries: list[CatalogEntry] | tuple[CatalogEntry, ...]) -> None:
    """Replace the resolvable catalog wholesale (disabled entries are dropped)."""
    global _ENTRIES, _BY_KEY
    live = tuple(e for e in entries if e.enabled)
    _ENTRIES = live
    _BY_KEY = {e.key: e for e in live}


def current_catalog() -> tuple[CatalogEntry, ...]:
    return _ENTRIES


async def ensure_catalog() -> None:
    """Install the host's catalog when one is registered (no host loader = keep the seed)."""
    from matrx_scraper._ext import get_ext, has_ext

    if has_ext(EXT_CATALOG_LOADER) and get_ext(EXT_CATALOG_LOADER) is not None:
        install_catalog(await get_ext(EXT_CATALOG_LOADER)())


def get_entry(key: str, *, verified_only: bool = False) -> CatalogEntry | None:
    """An enabled entry by key. Defaults lean open: a source with a ``known_issue`` still resolves
    (the caller says the issue); ``verified_only=True`` narrows to live-verified ones."""
    entry = _BY_KEY.get(key)
    if entry is None or (verified_only and not entry.verified):
        return None
    return entry


def match(url: str) -> CatalogEntry | None:
    """The verified, auto-routing entry for a URL, or ``None`` (read it the normal way)."""
    for entry in _ENTRIES:
        if entry.verified and entry.auto_route and entry.matches(url):
            return entry
    return None


def entries_for_url(url: str) -> list[CatalogEntry]:
    """Every verified entry whose pattern accepts the URL (e.g. place info AND reviews)."""
    return [e for e in _ENTRIES if e.verified and e.matches(url)]


def verified_entries() -> list[CatalogEntry]:
    return [e for e in _ENTRIES if e.verified]


__all__ = ["CATALOG", "CatalogEntry", "current_catalog", "ensure_catalog", "entries_for_url", "get_entry",
           "install_catalog", "match", "verified_entries"]
