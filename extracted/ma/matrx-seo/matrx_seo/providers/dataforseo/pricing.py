"""DataForSEO price book: what one collection request will cost, before it runs.

``estimate(operation, settings)`` prices a request PER METERED CALL — each
provider task (a live request, a queued ``task_post`` task, or one page of a
paged live collection) is priced and rounded on its own, then the rounded calls
are summed. Never summed-then-rounded: the provider bills each task separately,
so rounding the total would under-state a many-task request.

An operation the book does not price raises ``UnpricedOperationError`` — never
a zero. A zero estimate would read as "free" to every spend gate downstream.

Sources, in precedence order:

1. **Account prices** from the reviewed capability matrix
   (``aidream/docs/seo/dataforseo_capability_matrix.json`` ``pricing_catalog``,
   audited 2026-07-21). This account is billed 1.2x DataForSEO's published list
   price on every family except SERP — e.g. Labs list $0.01/task +
   $0.0001/row (OpenSEO's metering constants) is billed $0.012 + $0.00012,
   Google Ads list $0.075/task is billed $0.09. The reported costs below confirm
   it to the micro-dollar.
2. **SERP** from OpenSEO's metering (``src/shared/rank-tracking.ts`` at
   every-app/open-seo@0ffff93): live $0.002 for the first 10 results + $0.0015
   per further 10; queued $0.0006 + $0.00045; high priority doubles the queued
   price. Billed at list price on this account (reported $0.002 / $0.0006).
3. **Median reported cost** in ``seo.provider_call`` where neither exists
   (account-dependent families: LLM responses, backlinks history, Labs
   historical SERPs) and for every operation first proven live by OpenSEO Wave 1.

Median reported cost per call, ``seo.provider_call`` joined to
``seo.collection_run`` (provider ``dataforseo``), queried read-only 2026-09-27:

    ai_optimization.chat_gpt.llm_responses     n=27  median 0.084265
    ai_optimization.claude.llm_responses       n=18  median 0.053881
    ai_optimization.gemini.llm_responses       n=22  median 0.0370515
    ai_optimization.perplexity.llm_responses   n=18  median 0.005941
    backlinks.core summary/live                n=11  median 0.024036  (= 0.024 + 1 row x 0.000036)
    backlinks.history                          n=7   median 0.02706
    business_data.google.my_business_info      n=20  median 0.0054
    keywords.google_ads.search_volume live     n=93  median 0.09 ; task_post 0.06
    keywords.clickstream.bulk_search_volume    n=1   0.01212      (= 0.012 + 1 x 0.00012)
    labs.google.* (limit 1 / one keyword)      n=1 each 0.01212   (= 0.012 + 1 x 0.00012)
    labs.google.competitors_domain             n=11  median 0.01632
    labs.google.historical_rank_overview       n=1   0.1272
    labs.google.historical_bulk_traffic_est.   n=1   0.1212       (= 0.12 + 1 x 0.0012)
    labs.google.historical_serps               n=1   0.00084
    on_page.crawl (1 page) / instant_pages     n=1 each 0.00015
    serp.* live                                0.002 ; standard 0.0006

OpenSEO Wave 1 operations, each from its live one-task proof (L = live) through
``SeoCollectionService.collect`` (2026-09-27, US/en, admin test org):

    labs.locations_and_languages                 0          run 82becbd5-dcfb-48e3-a781-561445488449
    business_data.business_listings.categories   0          run 471ace8c-b08c-45e6-942c-775ae1ae1a91
    llm_mentions.search (limit 1)                0.101      run a0415df0-92b9-4bd8-b44f-525106c584e6
    llm_mentions.aggregated_metrics              0.101      run 0a7dd8ff-818c-4470-b6fc-a451c4e4a254
    llm_mentions.cross_aggregated_metrics        0.101      run c06ee4f3-01d1-42b6-8c91-b2d13d362c9c
    llm_mentions.top_pages                       0.101      run 3a29f0c2-9d0c-447f-82a9-0ea6049944d1
    keywords.google_ads.keywords_for_keywords    0.09 L     run bcbebe72-bd33-475d-9b5e-f6d921488eb4
    google.questions_and_answers                 0.0054 L   run 26db9dfe-f4fa-4ca6-9698-93288b1fdc75
    google.reviews (depth 10, high priority)     0.0015     run c83ae8ad-26ee-48ef-8d48-39f90f951896
    google.extended_reviews (depth 10, high)     0.0045     run c9baa766-cc71-4f05-8892-12b4abc7178a
    google.my_business_updates (depth 10, high)  0.0045     run 653f4a24-d3eb-472a-a9ed-6cb2583df977

LLM mentions bill at list ($0.1 per task + $0.001 per row — no 1.2x). Queued
business tasks were proven at high priority (``priority: 2``); normal priority is
priced at half, the same high/normal ratio the SERP and business-profile prices
show — the calibration test will flag it if the provider disagrees.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from decimal import ROUND_UP, Decimal
from typing import Any

from .contracts import DataForSeoCollectionSettings, DataForSeoWorkflow
from .operations import (
    LIVE_PAGE_MAX_LIMIT,
    PAGINATED_LIVE_ENDPOINTS,
    DataForSeoOperation,
    get_operation,
)

#: Every metered call is rounded UP to the provider's billing precision on its
#: own before calls are summed. DataForSEO reports task cost to the micro-dollar.
PER_CALL_QUANTUM = Decimal("0.000001")

ZERO = Decimal("0")


class UnpricedOperationError(ValueError):
    """The price book has no price for this operation. Raised loudly — an
    unknown price is never estimated as zero."""


def _d(value: str) -> Decimal:
    return Decimal(value)


# --- SERP (OpenSEO metering; list price on this account) --------------------
_SERP_LIVE_FIRST = _d("0.002")
_SERP_STANDARD_FIRST = _d("0.0006")
_SERP_STANDARD_HIGH_FIRST = _d("0.0012")
#: Every further page costs 75% of the first.
_SERP_EXTRA_PAGE_FACTOR = _d("0.75")
#: Results per billed page, by pricing key and device (capability matrix).
_SERP_PAGE_SIZE: dict[str, dict[str, int]] = {
    "serp_10_result": {"desktop": 10, "mobile": 10},
    "serp_maps": {"desktop": 100, "mobile": 20},
    "serp_local": {"desktop": 20, "mobile": 10},
}

# --- Account prices (capability matrix pricing_catalog; list x 1.2) ---------
_GOOGLE_ADS_LIVE = _d("0.09")
_GOOGLE_ADS_STANDARD = _d("0.06")
_CLICKSTREAM_REQUEST = _d("0.012")
_CLICKSTREAM_ITEM = _d("0.00012")
_LABS_TASK = _d("0.012")
_LABS_ROW = _d("0.00012")
_LABS_HISTORICAL_TASK = _d("0.12")
_LABS_HISTORICAL_ROW = _d("0.0012")
_BACKLINKS_REQUEST = _d("0.024")
_BACKLINKS_ROW = _d("0.000036")
_ONPAGE_PAGE = {
    "basic": _d("0.00015"),
    "load_resources": _d("0.00045"),
    "enable_javascript": _d("0.0015"),
    "enable_browser_rendering": _d("0.0051"),
}
_BUSINESS_LISTING_TASK = _d("0.012")
_BUSINESS_LISTING_ITEM = _d("0.00036")
_BUSINESS_PROFILE = {"live": _d("0.0054"), "standard": _d("0.0015"), "high": _d("0.003")}

# --- Median reported cost (account-dependent families) ----------------------
_BACKLINKS_HISTORY_OBSERVED = _d("0.02706")
_LABS_HISTORICAL_SERP_OBSERVED = _d("0.00084")
_LLM_RESPONSES_OBSERVED: dict[str, Decimal] = {
    "ai_optimization.chat_gpt.llm_responses": _d("0.084265"),
    "ai_optimization.claude.llm_responses": _d("0.053881"),
    "ai_optimization.gemini.llm_responses": _d("0.0370515"),
    "ai_optimization.perplexity.llm_responses": _d("0.005941"),
}

#: Labs endpoints that return a row list; the provider bills per returned row,
#: so an absent ``limit`` is priced at the provider's default of 100.
_LABS_DEFAULT_LIMIT = 100
_BACKLINKS_DEFAULT_LIMIT = 100

#: Backlinks row lists bill $0.000036 per row RETURNED, and a live collection stops
#: paging when the target runs out of rows — so ``limit`` / ``max_items`` is a CAP,
#: not the bill. Pricing at the cap put the book 2.4x over every observed
#: backlinks.core run (10 pages x $0.06 = $0.60 against a billed $0.10 for a
#: 10,000-item pull). The expected yield per endpoint is the median rows a real
#: request returned, derived from ``seo.provider_call`` (rows = (cost - $0.024 x
#: calls) / $0.000036) over every backlinks.core run with limit >= 1000, queried
#: read-only 2026-09-28:
#:     anchors            rows 12,12,143,194,195,197,686       median 194
#:     referring_domains  rows 23,23,228,426,427,437,851       median 427
#:     backlinks          rows 36,36,444,1000*,1000*,1544,1606 median 1000  (*limit-capped)
#: and the same derivation over backlinks.pages_competitors_timeseries (limit 1000):
#:     competitors            rows 1,46,93,93,172          median 93
#:     domain_pages           rows 1,1,357,408,408,1000    median 383
#:     domain_pages_summary   rows 11,118,121,121,122,682  median 121
#: A request is priced at min(its cap, this yield). The calibration test checks
#: the result against billed cost and fails when a target mix moves the median.
_BACKLINKS_EXPECTED_ROWS: dict[str, int] = {
    "/v3/backlinks/anchors/live": 194,
    "/v3/backlinks/referring_domains/live": 427,
    "/v3/backlinks/backlinks/live": 1000,
    "/v3/backlinks/competitors/live": 93,
    "/v3/backlinks/domain_pages/live": 383,
    "/v3/backlinks/domain_pages_summary/live": 121,
}

#: Time series bill one row per period returned (no ``limit``): observed
#: timeseries_summary 22,22,91,91,91,92 and timeseries_new_lost_summary
#: 22,22,22,91,91,91,92,92 — median 91 for both (the default date range).
_BACKLINKS_SERIES_ROWS = 91
_BACKLINKS_SERIES_SUFFIXES = (
    "/timeseries_summary/live",
    "/timeseries_new_lost_summary/live",
)
_BUSINESS_LISTING_DEFAULT_LIMIT = 100

# --- OpenSEO Wave 1 operations, from their live one-task proofs ------------
_LLM_MENTIONS_TASK = _d("0.1")
_LLM_MENTIONS_ROW = _d("0.001")
_LLM_MENTIONS_DEFAULT_LIMIT = 100
_BUSINESS_QUESTIONS_LIVE = _d("0.0054")
#: Queued business tasks, per 10 of ``depth`` at HIGH priority (proven); normal
#: priority is half.
_BUSINESS_TASK_HIGH_PER_10: dict[str, Decimal] = {
    "business_reviews": _d("0.0015"),
    "business_extended_reviews": _d("0.0045"),
    "business_updates": _d("0.0045"),
}

PriceRule = Callable[[DataForSeoOperation, DataForSeoWorkflow, str, dict[str, Any]], Decimal]


def _unpriced(operation: str) -> UnpricedOperationError:
    return UnpricedOperationError(f"no price for {operation}; add it to the price book")


def _int(task: dict[str, Any], key: str, default: int) -> int:
    value = task.get(key)
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _serp(
    op: DataForSeoOperation, workflow: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    device = "mobile" if str(task.get("device") or "").lower() == "mobile" else "desktop"
    page_size = _SERP_PAGE_SIZE[op.pricing_key][device]
    depth = max(_int(task, "depth", page_size), 1)
    pages = math.ceil(depth / page_size)
    if workflow is DataForSeoWorkflow.LIVE:
        first = _SERP_LIVE_FIRST
    elif _int(task, "priority", 1) == 2:
        first = _SERP_STANDARD_HIGH_FIRST
    else:
        first = _SERP_STANDARD_FIRST
    return first + (pages - 1) * first * _SERP_EXTRA_PAGE_FACTOR


def _google_ads(
    _op: DataForSeoOperation, workflow: DataForSeoWorkflow, _e: str, _t: dict[str, Any]
) -> Decimal:
    return _GOOGLE_ADS_LIVE if workflow is DataForSeoWorkflow.LIVE else _GOOGLE_ADS_STANDARD


def _clickstream(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    keywords = task.get("keywords")
    count = len(keywords) if isinstance(keywords, list) else 1
    return _CLICKSTREAM_REQUEST + count * _CLICKSTREAM_ITEM


def _limit(task: dict[str, Any], default_limit: int) -> int:
    return max(_int(task, "limit", default_limit), 1)


def _count(task: dict[str, Any]) -> int:
    """Items named in the request (keywords or targets), at least one."""
    for key in ("keywords", "targets"):
        value = task.get(key)
        if isinstance(value, list | dict):
            return max(len(value), 1)
    return 1


_LABS_ROW_LIST_ENDPOINT_SUFFIXES = (
    "/keyword_ideas/live",
    "/keyword_suggestions/live",
    "/related_keywords/live",
    "/keywords_for_site/live",
    "/ranked_keywords/live",
    "/competitors_domain/live",
    "/domain_intersection/live",
    "/page_intersection/live",
    "/relevant_pages/live",
    "/serp_competitors/live",
)


def _labs(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, endpoint: str, task: dict[str, Any]
) -> Decimal:
    if endpoint.endswith(_LABS_ROW_LIST_ENDPOINT_SUFFIXES):
        rows = _limit(task, _LABS_DEFAULT_LIMIT)
    else:
        rows = _count(task)
    price = _LABS_TASK + rows * _LABS_ROW
    return price * 2 if task.get("include_clickstream_data") else price


def _labs_historical_rank(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    price = _LABS_HISTORICAL_TASK + _count(task) * _LABS_HISTORICAL_ROW
    return price * 2 if task.get("include_clickstream_data") else price


def _labs_historical_serp(*_: Any) -> Decimal:
    return _LABS_HISTORICAL_SERP_OBSERVED


_BACKLINK_SINGLE_ROW_SUFFIXES = ("/summary/live",)


def _backlinks(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, endpoint: str, task: dict[str, Any]
) -> Decimal:
    if endpoint.endswith(_BACKLINKS_SERIES_SUFFIXES):
        rows = _BACKLINKS_SERIES_ROWS
    elif endpoint.endswith(_BACKLINK_SINGLE_ROW_SUFFIXES):
        rows = 1
    elif "/bulk_" in endpoint:
        rows = _count(task)
    else:
        rows = _limit(task, _BACKLINKS_DEFAULT_LIMIT)
        expected = _BACKLINKS_EXPECTED_ROWS.get(endpoint)
        if expected is not None:
            rows = min(rows, expected)
    return _BACKLINKS_REQUEST + rows * _BACKLINKS_ROW


def _backlinks_history(*_: Any) -> Decimal:
    return _BACKLINKS_HISTORY_OBSERVED


def _onpage(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, endpoint: str, task: dict[str, Any]
) -> Decimal:
    if task.get("enable_browser_rendering"):
        per_page = _ONPAGE_PAGE["enable_browser_rendering"]
    elif task.get("enable_javascript"):
        per_page = _ONPAGE_PAGE["enable_javascript"]
    elif task.get("load_resources"):
        per_page = _ONPAGE_PAGE["load_resources"]
    else:
        per_page = _ONPAGE_PAGE["basic"]
    pages = 1 if endpoint.endswith("/instant_pages") else max(_int(task, "max_crawl_pages", 1), 1)
    return pages * per_page


def _business_listing(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    limit = _limit(task, _BUSINESS_LISTING_DEFAULT_LIMIT)
    return _BUSINESS_LISTING_TASK + limit * _BUSINESS_LISTING_ITEM


def _business_profile(
    _op: DataForSeoOperation, workflow: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    if workflow is DataForSeoWorkflow.LIVE:
        return _BUSINESS_PROFILE["live"]
    return _BUSINESS_PROFILE["high" if _int(task, "priority", 1) == 2 else "standard"]


def _llm_responses(op: DataForSeoOperation, *_: Any) -> Decimal:
    price = _LLM_RESPONSES_OBSERVED.get(op.name.value)
    if price is None:
        raise _unpriced(op.name.value)
    return price


def _free(*_: Any) -> Decimal:
    return ZERO


def _llm_mentions(
    _op: DataForSeoOperation, _w: DataForSeoWorkflow, endpoint: str, task: dict[str, Any]
) -> Decimal:
    # search returns a row list billed per row; the aggregate endpoints return
    # one result row.
    rows = _limit(task, _LLM_MENTIONS_DEFAULT_LIMIT) if endpoint.endswith("/search/live") else 1
    return _LLM_MENTIONS_TASK + rows * _LLM_MENTIONS_ROW


def _business_questions(*_: Any) -> Decimal:
    return _BUSINESS_QUESTIONS_LIVE


def _business_task(
    op: DataForSeoOperation, _w: DataForSeoWorkflow, _e: str, task: dict[str, Any]
) -> Decimal:
    high = _BUSINESS_TASK_HIGH_PER_10[op.pricing_key]
    per_10 = high if _int(task, "priority", 1) == 2 else high / 2
    return math.ceil(max(_int(task, "depth", 10), 1) / 10) * per_10


#: The price book, keyed by each operation's ``pricing_key``.
PRICE_BOOK: dict[str, PriceRule] = {
    "serp_10_result": _serp,
    "serp_maps": _serp,
    "serp_local": _serp,
    "google_ads_task": _google_ads,
    "clickstream_bulk": _clickstream,
    "labs_general": _labs,
    "labs_historical_rank": _labs_historical_rank,
    "labs_historical_serp": _labs_historical_serp,
    "backlinks_core": _backlinks,
    "backlinks_history_verify": _backlinks_history,
    "onpage": _onpage,
    "business_listing": _business_listing,
    "business_profile": _business_profile,
    "ai_llm_responses": _llm_responses,
    #: Provider list endpoints DataForSEO does not bill.
    "free_list": _free,
    "ai_llm_mentions": _llm_mentions,
    "business_questions": _business_questions,
    "business_reviews": _business_task,
    "business_extended_reviews": _business_task,
    "business_updates": _business_task,
}


def _metered_calls(
    endpoint: str,
    settings: DataForSeoCollectionSettings,
) -> list[dict[str, Any]]:
    """One task body per call the provider will bill. A paged live collection
    (``max_items`` above one page) is one billed request per 1000-item page."""
    if (
        settings.workflow is DataForSeoWorkflow.LIVE
        and settings.max_items is not None
        and settings.max_items > LIVE_PAGE_MAX_LIMIT
        and endpoint in PAGINATED_LIVE_ENDPOINTS
    ):
        task = settings.tasks[0]
        # Paging stops when the rows run out: price the pages the expected yield
        # fills, not every page ``max_items`` would allow (see _BACKLINKS_EXPECTED_ROWS).
        total = settings.max_items
        expected = _BACKLINKS_EXPECTED_ROWS.get(endpoint)
        if expected is not None:
            total = min(total, max(expected, 1))
        pages = math.ceil(total / LIVE_PAGE_MAX_LIMIT)
        calls = []
        for page in range(pages):
            remaining = total - page * LIVE_PAGE_MAX_LIMIT
            calls.append({**task, "limit": min(remaining, LIVE_PAGE_MAX_LIMIT)})
        return calls
    return list(settings.tasks)


def round_call(amount: Decimal) -> Decimal:
    """One metered call's price at the provider's billing precision, rounded up."""
    return amount.quantize(PER_CALL_QUANTUM, rounding=ROUND_UP)


def estimate(operation: str, settings: dict[str, Any]) -> Decimal:
    """Estimated USD cost of collecting ``operation`` with ``settings``.

    Raises ``UnpricedOperationError`` when the book has no price."""
    try:
        op = get_operation(operation)
    except ValueError as exc:
        raise _unpriced(operation) from exc
    rule = PRICE_BOOK.get(op.pricing_key)
    if rule is None:
        raise _unpriced(operation)
    parsed = DataForSeoCollectionSettings.model_validate(settings)
    endpoint = op.endpoint_for(parsed.workflow, parsed.endpoint)
    return sum(
        (
            round_call(rule(op, parsed.workflow, endpoint, task))
            for task in _metered_calls(endpoint, parsed)
        ),
        ZERO,
    )


__all__ = [
    "PER_CALL_QUANTUM",
    "PRICE_BOOK",
    "UnpricedOperationError",
    "estimate",
    "round_call",
]
