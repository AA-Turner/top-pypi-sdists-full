"""The seed for the platform's data-source catalog (``scraper.data_source``).

Pure: turns the bundled census (``catalog_census.json``, every collector our account can run) and
the curated routes in ``site_catalog.CATALOG`` into one flat list of row dicts. The HOST owns the
table and the insert (a script upserts these by ``key``); the table is the one catalog at runtime.

Merge rule: a curated entry keeps its key (jobs, agents and tables already name it) and takes the
census entry's group, description and output fields; the census twin (same dataset, same mode) is
dropped so one thing is listed once. Curated entries that cannot be collected at all
(``supports_collection`` false) are not seeded. Nothing here names the provider in a user-facing
field; ``dataset_id`` is internal and is never granted to clients.
"""

from __future__ import annotations

import json
from importlib import resources
from typing import Any

from matrx_scraper.vendors.site_catalog import CATALOG, CatalogEntry

#: Curated entries that fail every collection attempt: not seeded (their census twins, if any, are).
NOT_SEEDED = frozenset({"airbnb_listing", "booking_hotel", "g2_product", "google_ads_transparency"})

#: Plain-English problems for census entries (the curated ones carry theirs on the entry).
CENSUS_ISSUES: dict[str, str] = {
    "yelp_businesses": "This site blocks collection right now.",
    "yelp_reviews": "This site blocks collection right now.",
    "google_maps_reviews": "Reviews are hidden behind a sign-in wall right now, so this may return nothing.",
    "airbnb_listings": "Collection failed in our last tests.",
    "indeed_jobs": "Searching by keyword does not finish right now; give a job link instead.",
    "google_news": "Our last test returned no stories; treat this one as experimental.",
    "github_repositories": "Our last test returned an empty record; treat this one as experimental.",
    "meta_ad_library": "Searching by ad type is not confirmed yet; give the link of an ad page.",
}

#: ~40 best for a no-code AI platform, across groups. Every key must exist in the seed (tested).
FEATURED: tuple[str, ...] = (
    # social
    "instagram_profiles", "instagram_posts", "tiktok_profiles", "tiktok_posts", "youtube_videos",
    "youtube_channels", "x_posts", "x_profiles", "reddit_posts", "linkedin_posts", "facebook_pages",
    # reviews and reputation
    "trustpilot_reviews", "amazon_reviews", "g2_reviews", "glassdoor_reviews", "google_play_reviews",
    "app_store_reviews",
    # places and local
    "google_maps_place",
    # jobs
    "linkedin_job", "linkedin_jobs_search", "glassdoor_jobs", "indeed_jobs",
    # people and companies
    "linkedin_people", "linkedin_company", "crunchbase_company", "glassdoor_company", "lawyers_directory",
    # products
    "amazon_product", "amazon_product_search", "walmart_product", "ebay_listings", "etsy_listings",
    "google_shopping", "facebook_marketplace",
    # real estate
    "zillow_listing", "zoopla_listings", "realtor_international",
    # news, apps, reference
    "wikipedia_articles", "google_play_app", "app_store_apps", "imdb_titles",
)

#: Output fields the census lacks but the collector really returns (company-level, repeated on each record).
#: Appended after the census fields so the seed and the live table agree.
EXTRA_OUTPUT_FIELDS: dict[str, tuple[str, ...]] = {
    "trustpilot_reviews": ("company_overall_rating", "company_rating_name", "company_total_reviews"),
}

#: Fields a person looks for first, put at the top of a source's ``output_fields`` (the table and the
#: comparison hide everything past the first few by default, so a census order that buries the rating
#: at position 11 hides the one number people came for). Seed order wins over live on a re-seed.
LEAD_OUTPUT_FIELDS: dict[str, tuple[str, ...]] = {
    "google_maps_place": ("name", "rating", "reviews_count", "category", "address"),
}


#: The provider spells some output keys wrong (``Review_auther``, ``Eelite_status`` on Yelp reviews). The
#: catalog lists the right spelling; aidream's ``data_fetch.mapper.VENDOR_KEY_FIXES`` renames the records.
OUTPUT_FIELD_FIXES: dict[str, str] = {"Review_auther": "review_author", "Eelite_status": "elite_status"}


def fix_output_fields(fields: list[str]) -> list[str]:
    return [OUTPUT_FIELD_FIXES.get(f, f) for f in fields]


def lead_first(key: str, fields: list[str]) -> list[str]:
    lead = [f for f in LEAD_OUTPUT_FIELDS.get(key, ()) if f in fields]
    return lead + [f for f in fields if f not in lead]


#: Columns a person curates in the live table: the seed fills them only while NULL, never overwrites.
FILL_ONLY_FIELDS = ("featured", "known_issue", "sort_order")

#: ``metadata.records_are`` = what one collected record is: "items" (one record per review/post/job/listing/
#: search hit) or "entity" (one record per profile/company/page/product). Sources not listed are "entity".
#: Explicit list, taken from the live split (60 items); the rule is irregular by site so it is not derived.
RECORDS_ARE_ITEMS = frozenset((
    "airbnb_listings",
    "amazon_product_search",
    "amazon_reviews",
    "amazon_search",
    "app_store_reviews",
    "bilibili_videos",
    "bluesky_posts",
    "booking_search",
    "ebay_listings",
    "etsy_listings",
    "facebook_comments",
    "facebook_company_reviews",
    "facebook_group_posts",
    "facebook_marketplace",
    "facebook_marketplace_search",
    "facebook_page_posts",
    "facebook_post",
    "g2_reviews",
    "glassdoor_jobs",
    "glassdoor_jobs_search",
    "glassdoor_reviews",
    "google_maps_reviews",
    "google_play_reviews",
    "google_search",
    "google_shopping",
    "google_shopping_products_search_us_products",
    "google_shopping_search",
    "indeed_jobs",
    "indeed_jobs_search",
    "indeed_new_jobs",
    "instagram_comments",
    "instagram_posts",
    "lawyers_directory",
    "lazada_products_search_gmv_products",
    "lazada_reviews",
    "linkedin_jobs_search",
    "linkedin_posts",
    "outdoor_research_products",
    "pinterest_posts",
    "properati_listings",
    "quora_post",
    "realtor_international",
    "reddit_comments",
    "reddit_posts",
    "search_results_html",
    "snapchat_posts",
    "threads_posts",
    "tiktok_comments",
    "tiktok_posts",
    "tiktok_posts_by_keyword",
    "trustpilot_reviews",
    "trustradius_reviews",
    "vinted_listings",
    "walmart_product_search",
    "walmart_reviews",
    "x_posts",
    "yelp_reviews",
    "youtube_comments",
    "youtube_comments_extended",
    "zoopla_listings",
))


def records_are(key: str) -> str:
    return "items" if key in RECORDS_ARE_ITEMS else "entity"


def merge_metadata(seed: dict[str, Any], live: dict[str, Any] | None) -> dict[str, Any]:
    """Key by key: every live key survives untouched; seed keys fill only the missing ones."""
    return {**seed, **(live or {})}


def merge_list(seed: list, live: list | None) -> list:
    """Union: seed order first, then live-only extras (order kept, no duplicates)."""
    out = list(seed)
    for v in live or []:
        if v not in out:
            out.append(v)
    return out


def merge_fields(seed_fields: dict[str, Any], live: dict[str, Any]) -> dict[str, Any]:
    """The changes a re-seed may make to an existing row. Never clobbers live-curated data:
    ``output_fields`` is unioned; FILL_ONLY_FIELDS are set only where the live value is NULL;
    ``verified_live`` is never turned off once true; everything else in ``seed_fields`` is seed-owned and rewritten."""
    changes: dict[str, Any] = {}
    for k, v in seed_fields.items():
        cur = live.get(k)
        if k == "output_fields":
            v = merge_list(v, fix_output_fields(list(cur or [])))
        elif k == "metadata":
            v = merge_metadata(v, cur)
        elif k in FILL_ONLY_FIELDS:
            if cur is not None or v is None:
                continue
        elif k == "verified_live":
            if cur is True:  # proven live (a confirmation sweep set it): a re-seed never downgrades it
                continue
        if cur != v:
            changes[k] = v
    return changes


EXAMPLES: dict[str, str] = {
    "trustpilot_reviews": "https://www.trustpilot.com/review/www.apple.com",
    "google_maps_place": "https://www.google.com/maps/place/data=!4m2!3m1!1s0x80dcdd5f8d1b5ba3:0x9f2d1f6d6b0b0b0b",
    "glassdoor_company": "https://www.glassdoor.com/Overview/Working-at-Google-EI_IE9079.11,17.htm",
    "glassdoor_reviews": "https://www.glassdoor.com/Reviews/Google-Reviews-E9079.htm",
    "indeed_company": "https://www.indeed.com/cmp/Google",
    "linkedin_company": "https://www.linkedin.com/company/google/",
    "crunchbase_company": "https://www.crunchbase.com/organization/google",
    "amazon_product": "https://www.amazon.com/dp/B0D1XD1ZV3",
    "amazon_reviews": "https://www.amazon.com/product-reviews/B0D1XD1ZV3",
    "walmart_product": "https://www.walmart.com/ip/5113183757",
    "zillow_listing": "https://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/",
    "g2_reviews": "https://www.g2.com/products/slack/reviews",
    "google_play_app": "https://play.google.com/store/apps/details?id=com.spotify.music",
    "google_play_reviews": "https://play.google.com/store/apps/details?id=com.spotify.music",
    "vimeo_video": "https://vimeo.com/76979871",
}

#: Examples the confirmation sweep found dead or wrong-shaped, replaced by a stable public page that a capped
#: live fetch returned a record for (2026-10-11). Applied to curated AND census rows, so a re-seed keeps them.
EXAMPLE_OVERRIDES: dict[str, str] = {
    "walmart_product": "https://www.walmart.com/ip/Great-Value-Singles-American-Pasteurized-Prepared-Cheese-Product-16-oz-24-Count/10452423",
    "crunchbase_company": "https://www.crunchbase.com/organization/openai",
    "instagram_posts": "https://www.instagram.com/p/CYe25UdpkFx/",
    "instagram_comments": "https://www.instagram.com/p/CYe25UdpkFx/",
    "linkedin_posts": "https://www.linkedin.com/posts/alexeheath_satya-nadella-on-microsofts-agent-bet-and-activity-7509275131022794752-lULZ",
    "tiktok_posts": "https://www.tiktok.com/@bbcnews/video/7623948383312465174",
}
LABELS = {"keyword": "Search words", "keyword_search": "Search words", "keywords": "Search words",
          "location": "Location", "city": "City", "country": "Country", "domain": "Site",
          "days": "Days back", "url": "Page address"}


def _title(name: str) -> str:
    return name.replace("_", " ").strip().capitalize()


def census() -> list[dict[str, Any]]:
    return json.loads(resources.files("matrx_scraper.vendors").joinpath("catalog_census.json").read_text("utf-8"))


def _field(name: str, label: str | None, required: bool, example: str | None) -> dict[str, Any]:
    return {"name": name, "label": LABELS.get(name) or label or _title(name), "required": required,
            "example": example, "type": "url" if name == "url" else "text"}


def _curated_spec(e: CatalogEntry, twin: dict[str, Any] | None) -> dict[str, Any]:
    if e.input_kind == "url":
        fields = [_field("url", None, True, EXAMPLES.get(e.key))]
        extra = [f for f in e.required_fields if f != "url" and f not in e.defaults]
    else:
        fields = []
        extra = [f for f in e.required_fields if f not in e.defaults]
        if e.query_field and e.query_field not in extra:
            extra.insert(0, e.query_field)
    fields += [_field(f, None, True, None) for f in extra]
    twin_in = (twin or {}).get("inputs", {})
    return {"mode": e.input_kind, "fields": fields, "required_fields": list(e.required_fields),
            "defaults": dict(e.defaults), "query_field": e.query_field, "location_field": e.location_field,
            "limit_field": e.limit_field, "discover_by": [e.discover_by] if e.discover_by else [],
            "discover_requires": twin_in.get("discover_requires") or {}}


def _census_spec(item: dict[str, Any]) -> dict[str, Any]:
    inp = item["inputs"]
    fields = [_field(f["name"], f.get("label"), bool(f.get("required")), f.get("example")) for f in inp["fields"]]
    return {"mode": inp["mode"], "fields": fields,
            "required_fields": [f["name"] for f in fields if f["required"]],
            "defaults": {}, "query_field": None, "location_field": None, "limit_field": None,
            "discover_by": list(inp.get("discover_by") or []),
            "discover_requires": inp.get("discover_requires") or {}}


def _row(*, key: str, label: str, item: dict[str, Any], spec: dict[str, Any], dataset_id: str, kind: str,
         key_column: str | None, url_pattern: dict[str, str] | None, auto_route: bool, verified: bool,
         known_issue: str | None) -> dict[str, Any]:
    fields = spec["fields"]
    if key in EXAMPLE_OVERRIDES:
        for f in fields:
            if f["name"] == "url":
                f["example"] = EXAMPLE_OVERRIDES[key]
    example = next((f["example"] for f in fields if f["name"] == "url" and f.get("example")), None)
    return {
        "key": key, "label": label, "group_name": item["group"], "subgroup": item.get("subgroup"),
        "description": item.get("description") or "", "input_kind": kind, "input_spec": spec,
        "output_fields": lead_first(key, fix_output_fields(merge_list(
            list(item.get("output_fields") or []), list(EXTRA_OUTPUT_FIELDS.get(key, ()))))),
        "key_column": key_column,
        "url_pattern": url_pattern, "auto_route": auto_route, "enabled": True, "featured": False,
        "verified_live": verified, "known_issue": known_issue, "supports_collection": True,
        "dataset_id": dataset_id, "example_url": example, "metadata": {"records_are": records_are(key)},
    }


def build_rows() -> list[dict[str, Any]]:
    items = census()
    by_ds: dict[tuple[str, str], dict[str, Any]] = {(i["dataset_id"], i["inputs"]["mode"]): i for i in items}
    dropped: set[str] = set()
    rows: list[dict[str, Any]] = []
    for e in CATALOG:
        if e.key in NOT_SEEDED:
            continue
        twin = by_ds.get((e.dataset_id, e.input_kind)) or by_ds.get((e.dataset_id, "url"))
        item = twin or {"group": _group_of(e), "subgroup": None, "description": "", "output_fields": []}
        if twin is not None and e.input_kind == "url":
            dropped.add(twin["key"])
        spec = _curated_spec(e, twin)
        pattern = {"host": e.host_pattern, "path": e.path_pattern} if e.host_pattern else None
        rows.append(_row(key=e.key, label=e.label, item=item, spec=spec, dataset_id=e.dataset_id, kind=e.input_kind,
                         key_column=e.key_field, url_pattern=pattern, auto_route=e.auto_route, verified=e.verified,
                         known_issue=e.known_issue))
    for i in items:
        if i["key"] in dropped or not i.get("supports_collection", True):
            continue
        rows.append(_row(key=i["key"], label=i["label"].replace("\t", ""), item=i, spec=_census_spec(i),
                         dataset_id=i["dataset_id"], kind="discover" if i["inputs"]["mode"] == "discover" else "url",
                         key_column=None, url_pattern=None, auto_route=False, verified=bool(i["verified_live"]),
                         known_issue=CENSUS_ISSUES.get(i["key"])))
    featured = set(FEATURED)
    for n, r in enumerate(sorted(rows, key=lambda r: (r["group_name"], r["key"] not in featured, r["label"].lower()))):
        r["featured"] = r["key"] in featured
        r["sort_order"] = n
    return rows


_CURATED_GROUPS = (
    (("google_maps", "yelp"), "Places & local business"), (("trustpilot", "g2", "google_play_reviews"), "Reviews & reputation"),
    (("glassdoor", "indeed", "linkedin_job", "linkedin_jobs"), "Jobs & hiring"),
    (("linkedin_company", "crunchbase"), "Companies & funding"),
    (("amazon", "walmart", "google_shopping", "facebook_marketplace"), "Ecommerce & products"),
    (("zillow",), "Real estate"), (("airbnb", "booking"), "Travel & hospitality"),
    (("google_play",), "Apps & software"), (("facebook_event", "quora", "vimeo"), "Social"),
)


def _group_of(e: CatalogEntry) -> str:
    for prefixes, label in _CURATED_GROUPS:
        if e.key.startswith(prefixes):
            return label
    return "Other"
