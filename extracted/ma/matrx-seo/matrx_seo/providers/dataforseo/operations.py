from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...adapters import SeoProviderOperation
from ...contracts import SeoCapability
from .contracts import DataForSeoOperationName, DataForSeoWorkflow

DATAFORSEO_CREDENTIAL_KEYS = ("DATA_FOR_SEO_EMAIL", "DATA_FOR_SEO_PASSWORD")

#: One live backlink request returns at most this many items, whatever ``limit``
#: says.  A site with more links than this is SILENTLY truncated unless the
#: caller pages — which is exactly how two managed sites sat at exactly 1000
#: stored backlinks while their own summary rows reported far more.
LIVE_PAGE_MAX_LIMIT = 1_000

#: The provider caps ``offset`` at 20 000; past that only ``search_after_token``
#: can advance the cursor.  We prefer the token whenever a page returns one and
#: keep ``offset`` as the fallback for a page that does not.
LIVE_OFFSET_CEILING = 20_000

#: Live endpoints whose result carries ``total_count`` + ``search_after_token``
#: and therefore supports the paged collection loop in ``DataForSeoClient``.
#: Membership is a claim about the PROVIDER's contract — do not add an endpoint
#: here without checking that its result actually paginates.
PAGINATED_LIVE_ENDPOINTS = frozenset(
    {
        "/v3/backlinks/backlinks/live",
        "/v3/backlinks/referring_domains/live",
        "/v3/backlinks/anchors/live",
    }
)

#: Provider list endpoints that are plain ``GET`` requests with no task body
#: (DataForSEO answers a POST to them with an error). An operation whose live
#: endpoint is listed here carries exactly one empty task ``{}`` so it still
#: fits the one-live-task contract; ``DataForSeoClient._execute_live`` sends it
#: as a bodiless GET.
GET_LIST_ENDPOINTS = frozenset(
    {
        "/v3/dataforseo_labs/locations_and_languages",
        "/v3/business_data/business_listings/categories",
    }
)


@dataclass(frozen=True)
class DataForSeoEndpointExample:
    endpoint: str
    workflow: DataForSeoWorkflow
    task: dict[str, Any]


@dataclass(frozen=True)
class DataForSeoOperation:
    provider_operation: SeoProviderOperation
    family: str
    endpoints: tuple[str, ...]
    workflows: tuple[DataForSeoWorkflow, ...]
    pricing_key: str
    raw_only: bool = False

    @property
    def name(self) -> DataForSeoOperationName:
        return DataForSeoOperationName(self.provider_operation.name)

    @property
    def capabilities(self) -> tuple[SeoCapability, ...]:
        return self.provider_operation.capabilities

    @property
    def endpoint_examples(self) -> tuple[DataForSeoEndpointExample, ...]:
        return tuple(
            DataForSeoEndpointExample(
                endpoint=endpoint,
                workflow=(
                    DataForSeoWorkflow.STANDARD
                    if "task_post" in endpoint
                    else DataForSeoWorkflow.LIVE
                ),
                task=dict(DATAFORSEO_ENDPOINT_EXAMPLE_TASKS[endpoint]),
            )
            for endpoint in self.endpoints
            if "{task_id}" not in endpoint
            and not (
                self.name is DataForSeoOperationName.ON_PAGE_CRAWL
                and endpoint != "/v3/on_page/task_post"
            )
        )

    def endpoint_for(self, workflow: DataForSeoWorkflow, selected: str | None) -> str:
        candidates = tuple(
            endpoint
            for endpoint in self.endpoints
            if "{task_id}" not in endpoint
            and (
                (workflow is DataForSeoWorkflow.STANDARD and "task_post" in endpoint)
                or (workflow is DataForSeoWorkflow.LIVE and "task_post" not in endpoint)
            )
        )
        if selected is not None:
            if selected not in candidates:
                raise ValueError(f"endpoint {selected!r} is not approved for {self.name.value}")
            return selected
        if len(candidates) != 1:
            raise ValueError(f"operation {self.name.value} requires one exact approved endpoint")
        return candidates[0]

    def task_get_endpoint(self, task_id: str) -> str:
        patterns = tuple(endpoint for endpoint in self.endpoints if "{task_id}" in endpoint)
        if len(patterns) != 1:
            raise ValueError(f"operation {self.name.value} has no unambiguous task GET")
        return patterns[0].format(task_id=task_id)


def _op(
    name: DataForSeoOperationName,
    family: str,
    capability: SeoCapability | tuple[SeoCapability, ...],
    endpoints: str,
    workflows: tuple[DataForSeoWorkflow, ...],
    pricing_key: str,
    *,
    raw_only: bool = False,
    freshness_ttl_seconds: int | None = None,
) -> DataForSeoOperation:
    capabilities = capability if isinstance(capability, tuple) else (capability,)
    if SeoCapability.RAW_PROVIDER not in capabilities:
        capabilities = (*capabilities, SeoCapability.RAW_PROVIDER)
    return DataForSeoOperation(
        provider_operation=SeoProviderOperation(
            name=name.value,
            capabilities=capabilities,
            credential_keys=DATAFORSEO_CREDENTIAL_KEYS,
            freshness_ttl_seconds=(
                freshness_ttl_seconds
                if freshness_ttl_seconds is not None
                else _freshness_ttl_seconds(family, capabilities)
            ),
        ),
        family=family,
        endpoints=tuple(endpoints.split("|")),
        workflows=workflows,
        pricing_key=pricing_key,
        raw_only=raw_only,
    )


def _freshness_ttl_seconds(
    family: str,
    capabilities: tuple[SeoCapability, ...],
) -> int:
    if family == "backlinks":
        return 30 * 24 * 60 * 60
    # Matches the seo.keyword_market staleness policy: metrics refresh at 30
    # days (or explicit force_refresh), never sooner.
    if SeoCapability.KEYWORD_METRICS in capabilities:
        return 30 * 24 * 60 * 60
    if family in {"serp", "on_page"}:
        return 24 * 60 * 60
    return 7 * 24 * 60 * 60


_THIRTY_DAYS = 30 * 24 * 60 * 60

_LIVE = (DataForSeoWorkflow.LIVE,)
_STANDARD = (DataForSeoWorkflow.STANDARD,)
# Live first — lab UIs and catalog consumers take workflows[0] as the default.
# Standard task_post/poll can sleep minutes before the first GET with no response.
_BOTH = (DataForSeoWorkflow.LIVE, DataForSeoWorkflow.STANDARD)

APPROVED_OPERATIONS = (
    _op(
        DataForSeoOperationName.SERP_GOOGLE_ORGANIC_ADVANCED,
        "serp",
        SeoCapability.SERP_RANK,
        "/v3/serp/google/organic/task_post|/v3/serp/google/organic/task_get/advanced/{task_id}|/v3/serp/google/organic/live/advanced",
        _BOTH,
        "serp_10_result",
    ),
    _op(
        DataForSeoOperationName.SERP_GOOGLE_MAPS_ADVANCED,
        "serp",
        SeoCapability.SERP_RANK,
        "/v3/serp/google/maps/task_post|/v3/serp/google/maps/task_get/advanced/{task_id}|/v3/serp/google/maps/live/advanced",
        _BOTH,
        "serp_maps",
    ),
    _op(
        DataForSeoOperationName.SERP_GOOGLE_LOCAL_FINDER_ADVANCED,
        "serp",
        SeoCapability.SERP_RANK,
        "/v3/serp/google/local_finder/task_post|/v3/serp/google/local_finder/task_get/advanced/{task_id}|/v3/serp/google/local_finder/live/advanced",
        _BOTH,
        "serp_local",
    ),
    _op(
        DataForSeoOperationName.SERP_BING_ORGANIC_ADVANCED,
        "serp",
        SeoCapability.SERP_RANK,
        "/v3/serp/bing/organic/task_post|/v3/serp/bing/organic/task_get/advanced/{task_id}|/v3/serp/bing/organic/live/advanced",
        _BOTH,
        "serp_10_result",
    ),
    _op(
        DataForSeoOperationName.AI_CHAT_GPT_LLM_RESPONSES,
        "ai_optimization",
        SeoCapability.SERP_RANK,
        "/v3/ai_optimization/chat_gpt/llm_responses/live",
        _LIVE,
        "ai_llm_responses",
    ),
    _op(
        DataForSeoOperationName.AI_CLAUDE_LLM_RESPONSES,
        "ai_optimization",
        SeoCapability.SERP_RANK,
        "/v3/ai_optimization/claude/llm_responses/live",
        _LIVE,
        "ai_llm_responses",
    ),
    _op(
        DataForSeoOperationName.AI_GEMINI_LLM_RESPONSES,
        "ai_optimization",
        SeoCapability.SERP_RANK,
        "/v3/ai_optimization/gemini/llm_responses/live",
        _LIVE,
        "ai_llm_responses",
    ),
    _op(
        DataForSeoOperationName.AI_PERPLEXITY_LLM_RESPONSES,
        "ai_optimization",
        SeoCapability.SERP_RANK,
        "/v3/ai_optimization/perplexity/llm_responses/live",
        _LIVE,
        "ai_llm_responses",
    ),
    # LLM mentions (OpenSEO Wave 1, seo_ai_visibility). raw_only: these are
    # provider-index reads, never answers — they must never reach
    # normalize_ai_answer_response (the adapter routes only the four
    # llm_responses operations there, by name).
    _op(
        DataForSeoOperationName.AI_LLM_MENTIONS_SEARCH,
        "ai_optimization",
        SeoCapability.RAW_PROVIDER,
        "/v3/ai_optimization/llm_mentions/search/live",
        _LIVE,
        "ai_llm_mentions",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.AI_LLM_MENTIONS_AGGREGATED_METRICS,
        "ai_optimization",
        SeoCapability.RAW_PROVIDER,
        "/v3/ai_optimization/llm_mentions/aggregated_metrics/live",
        _LIVE,
        "ai_llm_mentions",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.AI_LLM_MENTIONS_CROSS_AGGREGATED_METRICS,
        "ai_optimization",
        SeoCapability.RAW_PROVIDER,
        "/v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live",
        _LIVE,
        "ai_llm_mentions",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.AI_LLM_MENTIONS_TOP_PAGES,
        "ai_optimization",
        SeoCapability.RAW_PROVIDER,
        "/v3/ai_optimization/llm_mentions/top_pages/live",
        _LIVE,
        "ai_llm_mentions",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME,
        "keywords_data",
        SeoCapability.KEYWORD_METRICS,
        "/v3/keywords_data/google_ads/search_volume/task_post|/v3/keywords_data/google_ads/search_volume/task_get/{task_id}|/v3/keywords_data/google_ads/search_volume/live",
        _BOTH,
        "google_ads_task",
    ),
    _op(
        DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_KEYWORDS_FOR_KEYWORDS,
        "keywords_data",
        SeoCapability.KEYWORD_METRICS,
        "/v3/keywords_data/google_ads/keywords_for_keywords/task_post|/v3/keywords_data/google_ads/keywords_for_keywords/task_get/{task_id}|/v3/keywords_data/google_ads/keywords_for_keywords/live",
        _BOTH,
        "google_ads_task",
    ),
    _op(
        DataForSeoOperationName.KEYWORDS_CLICKSTREAM_BULK_SEARCH_VOLUME,
        "keywords_data",
        SeoCapability.KEYWORD_METRICS,
        "/v3/keywords_data/clickstream_data/bulk_search_volume/live",
        _LIVE,
        "clickstream_bulk",
    ),
    # Labs market coverage (free GET list). Keyword research routes a market
    # Labs does not serve to Google Ads keywords_for_keywords; this list is the
    # provider fact that decides it, reused 30 days.
    _op(
        DataForSeoOperationName.LABS_LOCATIONS_AND_LANGUAGES,
        "dataforseo_labs",
        SeoCapability.RAW_PROVIDER,
        "/v3/dataforseo_labs/locations_and_languages",
        _LIVE,
        "free_list",
        raw_only=True,
        freshness_ttl_seconds=_THIRTY_DAYS,
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_KEYWORD_OVERVIEW,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/keyword_overview/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_KEYWORD_IDEAS,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/keyword_ideas/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_KEYWORD_SUGGESTIONS,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/keyword_suggestions/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_RELATED_KEYWORDS,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/related_keywords/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_KEYWORDS_FOR_SITE,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/keywords_for_site/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_SEARCH_INTENT,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/search_intent/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_BULK_KEYWORD_DIFFICULTY,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/bulk_keyword_difficulty/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_RANKED_KEYWORDS,
        "dataforseo_labs",
        (SeoCapability.SERP_RANK, SeoCapability.KEYWORD_METRICS),
        "/v3/dataforseo_labs/google/ranked_keywords/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_COMPETITORS_DOMAIN,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/competitors_domain/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_DOMAIN_INTERSECTION,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/domain_intersection/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_PAGE_INTERSECTION,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/page_intersection/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_RELEVANT_PAGES,
        "dataforseo_labs",
        SeoCapability.BACKLINKS,
        "/v3/dataforseo_labs/google/relevant_pages/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_SERP_COMPETITORS,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/serp_competitors/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_DOMAIN_RANK_OVERVIEW,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/domain_rank_overview/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_HISTORICAL_RANK_OVERVIEW,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/historical_rank_overview/live",
        _LIVE,
        "labs_historical_rank",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_BULK_TRAFFIC_ESTIMATION,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/bulk_traffic_estimation/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_HISTORICAL_BULK_TRAFFIC_ESTIMATION,
        "dataforseo_labs",
        SeoCapability.COMPETITORS,
        "/v3/dataforseo_labs/google/historical_bulk_traffic_estimation/live",
        _LIVE,
        "labs_historical_rank",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_HISTORICAL_KEYWORD_DATA,
        "dataforseo_labs",
        SeoCapability.KEYWORD_METRICS,
        "/v3/dataforseo_labs/google/historical_keyword_data/live",
        _LIVE,
        "labs_general",
    ),
    _op(
        DataForSeoOperationName.LABS_GOOGLE_HISTORICAL_SERPS,
        "dataforseo_labs",
        SeoCapability.SERP_RANK,
        "/v3/dataforseo_labs/google/historical_serps/live",
        _LIVE,
        "labs_historical_serp",
    ),
    _op(
        DataForSeoOperationName.BACKLINKS_CORE,
        "backlinks",
        SeoCapability.BACKLINKS,
        "/v3/backlinks/summary/live|/v3/backlinks/backlinks/live|/v3/backlinks/referring_domains/live|/v3/backlinks/anchors/live",
        _LIVE,
        "backlinks_core",
    ),
    _op(
        DataForSeoOperationName.BACKLINKS_INTERSECTIONS,
        "backlinks",
        # BACKLINKS is declared because the link-gap services collect under that
        # capability and `_normalize_backlinks` dispatches the intersection
        # normalizer for it. `raw_only=True` STAYS: it exempts the operation
        # from the "must have a canonical normalizer" precondition (the
        # intersection endpoints are not in SUPPORTED_BACKLINK_ENDPOINTS); it
        # has never suppressed normalization. Declaring only RAW_PROVIDER here
        # made `collect_response` reject every real caller before the HTTP call.
        SeoCapability.BACKLINKS,
        "/v3/backlinks/domain_intersection/live|/v3/backlinks/page_intersection/live",
        _LIVE,
        "backlinks_core",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BACKLINKS_HISTORY,
        "backlinks",
        SeoCapability.BACKLINKS,
        "/v3/backlinks/history/live",
        _LIVE,
        "backlinks_history_verify",
    ),
    _op(
        DataForSeoOperationName.BACKLINKS_BULK_METRICS,
        "backlinks",
        SeoCapability.BACKLINKS,
        "/v3/backlinks/bulk_ranks/live|/v3/backlinks/bulk_backlinks/live|/v3/backlinks/bulk_spam_score/live|/v3/backlinks/bulk_referring_domains/live|/v3/backlinks/bulk_new_lost_backlinks/live|/v3/backlinks/bulk_new_lost_referring_domains/live|/v3/backlinks/bulk_pages_summary/live",
        _LIVE,
        "backlinks_core",
    ),
    _op(
        DataForSeoOperationName.BACKLINKS_PAGES_COMPETITORS_TIMESERIES,
        "backlinks",
        (SeoCapability.BACKLINKS, SeoCapability.COMPETITORS),
        "/v3/backlinks/competitors/live|/v3/backlinks/domain_pages/live|/v3/backlinks/domain_pages_summary/live|/v3/backlinks/timeseries_summary/live|/v3/backlinks/timeseries_new_lost_summary/live",
        _LIVE,
        "backlinks_core",
    ),
    _op(
        DataForSeoOperationName.ON_PAGE_CRAWL,
        "on_page",
        SeoCapability.RAW_PROVIDER,
        "/v3/on_page/task_post|/v3/on_page/summary/{task_id}|/v3/on_page/pages|/v3/on_page/resources|/v3/on_page/duplicate_tags|/v3/on_page/keyword_density",
        (DataForSeoWorkflow.STANDARD,),
        "onpage",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.ON_PAGE_INSTANT_PAGES,
        "on_page",
        SeoCapability.RAW_PROVIDER,
        "/v3/on_page/instant_pages",
        _LIVE,
        "onpage",
        raw_only=True,
    ),
    # Business Data — local-listings intelligence (read-only). Approved matrix
    # entries use the same canonical operation names as this catalog; consumed by
    # services/seo/local_listings.py to fill web.location_listing.observed.
    _op(
        DataForSeoOperationName.BUSINESS_LISTINGS_SEARCH,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/business_listings/search/live",
        _LIVE,
        "business_listing",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BUSINESS_GOOGLE_MY_BUSINESS_INFO,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/google/my_business_info/live",
        _LIVE,
        "business_profile",
        raw_only=True,
    ),
    # OpenSEO Wave 1 (seo_local). Reviews, extended reviews and profile updates
    # exist only as queued tasks: task_post, then task_get/{task_id} — the
    # business_data google family has no /advanced suffix on task_get.
    _op(
        DataForSeoOperationName.BUSINESS_LISTINGS_CATEGORIES,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/business_listings/categories",
        _LIVE,
        "free_list",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BUSINESS_GOOGLE_REVIEWS,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/google/reviews/task_post|/v3/business_data/google/reviews/task_get/{task_id}",
        _STANDARD,
        "business_reviews",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BUSINESS_GOOGLE_EXTENDED_REVIEWS,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/google/extended_reviews/task_post|/v3/business_data/google/extended_reviews/task_get/{task_id}",
        _STANDARD,
        "business_extended_reviews",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BUSINESS_GOOGLE_MY_BUSINESS_UPDATES,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/google/my_business_updates/task_post|/v3/business_data/google/my_business_updates/task_get/{task_id}",
        _STANDARD,
        "business_updates",
        raw_only=True,
    ),
    _op(
        DataForSeoOperationName.BUSINESS_GOOGLE_QUESTIONS_AND_ANSWERS,
        "business_data",
        SeoCapability.RAW_PROVIDER,
        "/v3/business_data/google/questions_and_answers/live",
        _LIVE,
        "business_questions",
        raw_only=True,
    ),
)


_SERP_TASK = {
    "keyword": "ai workflow automation",
    "location_code": 2840,
    "language_code": "en",
}
_KEYWORD_LIST_TASK = {
    "keywords": ["ai workflow automation"],
    "location_code": 2840,
    "language_code": "en",
}
_DOMAIN_TASK = {
    "target": "dataforseo.com",
    "location_code": 2840,
    "language_code": "en",
}
_BACKLINK_TARGET_TASK = {"target": "dataforseo.com"}
_BACKLINK_TARGETS_TASK = {"targets": ["dataforseo.com"]}

_AI_LLM_TASK: dict[str, Any] = {
    "user_prompt": "What are the best IT asset disposition companies?",
    "model_name": "gpt-5.5",
    "web_search": True,
    "web_search_country_iso_code": "US",
    "max_output_tokens": 2048,
}

_LLM_MENTIONS_TASK: dict[str, Any] = {
    "target": [{"domain": "dataforseo.com"}],
    "platform": "google",
    "location_code": 2840,
    "language_code": "en",
}
_BUSINESS_TASK: dict[str, Any] = {
    "keyword": "Titanium Success Costa Mesa",
    "location_code": 2840,
    "language_code": "en",
    "depth": 10,
}

DATAFORSEO_ENDPOINT_EXAMPLE_TASKS: dict[str, dict[str, Any]] = {
    "/v3/serp/google/organic/task_post": _SERP_TASK,
    "/v3/serp/google/organic/live/advanced": _SERP_TASK,
    "/v3/ai_optimization/chat_gpt/llm_responses/live": _AI_LLM_TASK,
    "/v3/ai_optimization/claude/llm_responses/live": {
        **_AI_LLM_TASK,
        "model_name": "claude-sonnet-4-6",
    },
    "/v3/ai_optimization/gemini/llm_responses/live": {
        **_AI_LLM_TASK,
        "model_name": "gemini-3.5-flash",
    },
    "/v3/ai_optimization/perplexity/llm_responses/live": {
        **_AI_LLM_TASK,
        "model_name": "sonar",
    },
    "/v3/serp/google/maps/task_post": _SERP_TASK,
    "/v3/serp/google/maps/live/advanced": _SERP_TASK,
    "/v3/serp/google/local_finder/task_post": {
        **_SERP_TASK,
        "keyword": "local ai consultants",
    },
    "/v3/serp/google/local_finder/live/advanced": {
        **_SERP_TASK,
        "keyword": "local ai consultants",
    },
    "/v3/serp/bing/organic/task_post": _SERP_TASK,
    "/v3/serp/bing/organic/live/advanced": _SERP_TASK,
    "/v3/keywords_data/google_ads/search_volume/task_post": _KEYWORD_LIST_TASK,
    "/v3/keywords_data/google_ads/search_volume/live": _KEYWORD_LIST_TASK,
    "/v3/keywords_data/clickstream_data/bulk_search_volume/live": {
        "keywords": ["ai workflow automation"],
        "location_code": 2840,
    },
    "/v3/dataforseo_labs/google/keyword_overview/live": _KEYWORD_LIST_TASK,
    "/v3/dataforseo_labs/google/keyword_ideas/live": {
        **_KEYWORD_LIST_TASK,
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/keyword_suggestions/live": {
        "keyword": "ai workflow automation",
        "location_code": 2840,
        "language_code": "en",
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/related_keywords/live": {
        "keyword": "ai workflow automation",
        "location_code": 2840,
        "language_code": "en",
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/keywords_for_site/live": {**_DOMAIN_TASK, "limit": 1},
    "/v3/dataforseo_labs/google/search_intent/live": {
        "keywords": ["ai workflow automation"],
        "language_code": "en",
    },
    "/v3/dataforseo_labs/google/bulk_keyword_difficulty/live": _KEYWORD_LIST_TASK,
    "/v3/dataforseo_labs/google/ranked_keywords/live": {**_DOMAIN_TASK, "limit": 1},
    "/v3/dataforseo_labs/google/competitors_domain/live": {
        **_DOMAIN_TASK,
        "intersecting_domains": ["ahrefs.com", "semrush.com"],
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/domain_intersection/live": {
        "target1": "dataforseo.com",
        "target2": "ahrefs.com",
        "location_code": 2840,
        "language_code": "en",
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/page_intersection/live": {
        "pages": {"1": "https://dataforseo.com/", "2": "https://ahrefs.com/*"},
        "location_code": 2840,
        "language_code": "en",
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/relevant_pages/live": {**_DOMAIN_TASK, "limit": 1},
    "/v3/dataforseo_labs/google/serp_competitors/live": {
        **_KEYWORD_LIST_TASK,
        "limit": 1,
    },
    "/v3/dataforseo_labs/google/domain_rank_overview/live": _DOMAIN_TASK,
    "/v3/dataforseo_labs/google/historical_rank_overview/live": _DOMAIN_TASK,
    "/v3/dataforseo_labs/google/bulk_traffic_estimation/live": {
        "targets": ["dataforseo.com"],
        "location_code": 2840,
        "language_code": "en",
    },
    "/v3/dataforseo_labs/google/historical_bulk_traffic_estimation/live": {
        "targets": ["dataforseo.com"],
        "location_code": 2840,
        "language_code": "en",
    },
    "/v3/dataforseo_labs/google/historical_keyword_data/live": _KEYWORD_LIST_TASK,
    "/v3/dataforseo_labs/google/historical_serps/live": {
        "keyword": "ai workflow automation",
        "location_code": 2840,
        "language_code": "en",
    },
    "/v3/backlinks/summary/live": _BACKLINK_TARGET_TASK,
    "/v3/backlinks/backlinks/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/referring_domains/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/anchors/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/domain_intersection/live": {
        "targets": {"1": "moz.com", "2": "ahrefs.com"},
        "limit": 1,
    },
    "/v3/backlinks/page_intersection/live": {
        "targets": {"1": "football.com", "2": "fifa.com"},
        "limit": 1,
    },
    "/v3/backlinks/history/live": _BACKLINK_TARGET_TASK,
    "/v3/backlinks/bulk_ranks/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_backlinks/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_spam_score/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_referring_domains/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_new_lost_backlinks/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_new_lost_referring_domains/live": _BACKLINK_TARGETS_TASK,
    "/v3/backlinks/bulk_pages_summary/live": {
        "targets": ["https://dataforseo.com/solutions"],
    },
    "/v3/backlinks/competitors/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/domain_pages/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/domain_pages_summary/live": {**_BACKLINK_TARGET_TASK, "limit": 1},
    "/v3/backlinks/timeseries_summary/live": _BACKLINK_TARGET_TASK,
    "/v3/backlinks/timeseries_new_lost_summary/live": _BACKLINK_TARGET_TASK,
    "/v3/on_page/task_post": {
        "target": "dataforseo.com",
        "max_crawl_pages": 1,
        "load_resources": False,
        "enable_javascript": False,
    },
    "/v3/on_page/instant_pages": {"url": "https://dataforseo.com/"},
    "/v3/business_data/business_listings/search/live": {
        "categories": ["pizza_restaurant"],
        "location_coordinate": "40.7,-74.0,10",
        "limit": 1,
    },
    "/v3/business_data/google/my_business_info/live": {
        "keyword": "Titanium Success Costa Mesa",
        "location_code": 2840,
        "language_code": "en",
    },
    "/v3/business_data/business_listings/categories": {},
    "/v3/business_data/google/reviews/task_post": _BUSINESS_TASK,
    "/v3/business_data/google/extended_reviews/task_post": _BUSINESS_TASK,
    "/v3/business_data/google/my_business_updates/task_post": _BUSINESS_TASK,
    "/v3/business_data/google/questions_and_answers/live": _BUSINESS_TASK,
    "/v3/dataforseo_labs/locations_and_languages": {},
    "/v3/keywords_data/google_ads/keywords_for_keywords/task_post": _KEYWORD_LIST_TASK,
    "/v3/keywords_data/google_ads/keywords_for_keywords/live": _KEYWORD_LIST_TASK,
    "/v3/ai_optimization/llm_mentions/search/live": {**_LLM_MENTIONS_TASK, "limit": 1},
    "/v3/ai_optimization/llm_mentions/aggregated_metrics/live": {
        **_LLM_MENTIONS_TASK,
        "internal_list_limit": 1,
    },
    "/v3/ai_optimization/llm_mentions/cross_aggregated_metrics/live": {
        "targets": [
            {"aggregation_key": "dataforseo", "target": [{"domain": "dataforseo.com"}]},
            {"aggregation_key": "semrush", "target": [{"domain": "semrush.com"}]},
        ],
        "platform": "google",
        "location_code": 2840,
        "language_code": "en",
        "internal_list_limit": 1,
    },
    "/v3/ai_optimization/llm_mentions/top_pages/live": {
        **_LLM_MENTIONS_TASK,
        "links_scope": "sources",
        "items_list_limit": 1,
        "internal_list_limit": 1,
    },
}


def _validate_endpoint_examples() -> None:
    selectable = {
        example.endpoint
        for operation in APPROVED_OPERATIONS
        for example in operation.endpoint_examples
    }
    configured = set(DATAFORSEO_ENDPOINT_EXAMPLE_TASKS)
    if selectable != configured:
        raise RuntimeError(
            "DataForSEO endpoint examples do not match selectable endpoints: "
            f"missing={sorted(selectable - configured)}, "
            f"unexpected={sorted(configured - selectable)}"
        )


_validate_endpoint_examples()


_BY_NAME = {operation.name: operation for operation in APPROVED_OPERATIONS}


def get_operation(name: DataForSeoOperationName | str) -> DataForSeoOperation:
    try:
        normalized = DataForSeoOperationName(name)
    except ValueError as exc:
        raise ValueError(f"DataForSEO operation {name!r} is not approved") from exc
    return _BY_NAME[normalized]
