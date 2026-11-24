from __future__ import annotations

from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORDS = 1_000
GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_CHARS = 80
GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_WORDS = 10

#: Symbols Google Ads refuses in a keyword. DataForSEO passes the keyword
#: straight through, so the rejection arrives as an opaque provider error —
#: "Invalid Field: 'keywords'. Keyword text has invalid characters or symbols" —
#: which on 2026-08-11 began failing the ENTIRE scheduled keyword volume sweep
#: on one phrase ending in '?', and had done so on every run since.
#:
#: Source: Google Ads Help, "Fix issues with your ads and keywords" — commas,
#: equals signs, exclamation points, grave accents, angle brackets, square
#: brackets, braces, parentheses, percent signs, pipes and question marks.
#: Checking it HERE, where the provider contract lives, means every caller of
#: the operation gets the same verdict before a request is ever paid for.
GOOGLE_ADS_DISALLOWED_KEYWORD_CHARS = frozenset(",=!`<>[]{}()%|?")


def google_ads_search_volume_keyword_rejection_reason(keyword: str) -> str | None:
    normalized = keyword.strip()
    if not normalized:
        return "keyword is blank"
    if len(normalized) > GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_CHARS:
        return f"keyword exceeds {GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_CHARS} characters"
    if len(normalized.split()) > GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_WORDS:
        return f"keyword exceeds {GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORD_WORDS} words"
    found = sorted(set(normalized) & GOOGLE_ADS_DISALLOWED_KEYWORD_CHARS)
    if found:
        return "keyword contains characters Google Ads refuses: " + " ".join(
            repr(char) for char in found
        )
    return None


class DataForSeoWorkflow(StrEnum):
    LIVE = "live"
    STANDARD = "standard"


class DataForSeoOperationName(StrEnum):
    SERP_GOOGLE_ORGANIC_ADVANCED = "serp.google.organic.advanced"
    SERP_GOOGLE_MAPS_ADVANCED = "serp.google.maps.advanced"
    SERP_GOOGLE_LOCAL_FINDER_ADVANCED = "serp.google.local_finder.advanced"
    SERP_BING_ORGANIC_ADVANCED = "serp.bing.organic.advanced"
    KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME = "keywords.google_ads.search_volume"
    KEYWORDS_GOOGLE_ADS_KEYWORDS_FOR_KEYWORDS = "keywords.google_ads.keywords_for_keywords"
    KEYWORDS_CLICKSTREAM_BULK_SEARCH_VOLUME = "keywords.clickstream.bulk_search_volume"
    LABS_LOCATIONS_AND_LANGUAGES = "labs.locations_and_languages"
    LABS_GOOGLE_KEYWORD_OVERVIEW = "labs.google.keyword_overview"
    LABS_GOOGLE_KEYWORD_IDEAS = "labs.google.keyword_ideas"
    LABS_GOOGLE_KEYWORD_SUGGESTIONS = "labs.google.keyword_suggestions"
    LABS_GOOGLE_RELATED_KEYWORDS = "labs.google.related_keywords"
    LABS_GOOGLE_KEYWORDS_FOR_SITE = "labs.google.keywords_for_site"
    LABS_GOOGLE_SEARCH_INTENT = "labs.google.search_intent"
    LABS_GOOGLE_BULK_KEYWORD_DIFFICULTY = "labs.google.bulk_keyword_difficulty"
    LABS_GOOGLE_RANKED_KEYWORDS = "labs.google.ranked_keywords"
    LABS_GOOGLE_COMPETITORS_DOMAIN = "labs.google.competitors_domain"
    LABS_GOOGLE_DOMAIN_INTERSECTION = "labs.google.domain_intersection"
    LABS_GOOGLE_PAGE_INTERSECTION = "labs.google.page_intersection"
    LABS_GOOGLE_RELEVANT_PAGES = "labs.google.relevant_pages"
    LABS_GOOGLE_SERP_COMPETITORS = "labs.google.serp_competitors"
    LABS_GOOGLE_DOMAIN_RANK_OVERVIEW = "labs.google.domain_rank_overview"
    LABS_GOOGLE_HISTORICAL_RANK_OVERVIEW = "labs.google.historical_rank_overview"
    LABS_GOOGLE_BULK_TRAFFIC_ESTIMATION = "labs.google.bulk_traffic_estimation"
    LABS_GOOGLE_HISTORICAL_BULK_TRAFFIC_ESTIMATION = (
        "labs.google.historical_bulk_traffic_estimation"
    )
    LABS_GOOGLE_HISTORICAL_KEYWORD_DATA = "labs.google.historical_keyword_data"
    LABS_GOOGLE_HISTORICAL_SERPS = "labs.google.historical_serps"
    BACKLINKS_CORE = "backlinks.core"
    BACKLINKS_INTERSECTIONS = "backlinks.intersections"
    BACKLINKS_HISTORY = "backlinks.history"
    BACKLINKS_BULK_METRICS = "backlinks.bulk_metrics"
    BACKLINKS_PAGES_COMPETITORS_TIMESERIES = "backlinks.pages_competitors_timeseries"
    ON_PAGE_CRAWL = "on_page.crawl"
    ON_PAGE_INSTANT_PAGES = "on_page.instant_pages"
    BUSINESS_LISTINGS_SEARCH = "business_data.business_listings.search"
    BUSINESS_LISTINGS_CATEGORIES = "business_data.business_listings.categories"
    BUSINESS_GOOGLE_MY_BUSINESS_INFO = "business_data.google.my_business_info"
    BUSINESS_GOOGLE_REVIEWS = "business_data.google.reviews"
    BUSINESS_GOOGLE_EXTENDED_REVIEWS = "business_data.google.extended_reviews"
    BUSINESS_GOOGLE_MY_BUSINESS_UPDATES = "business_data.google.my_business_updates"
    BUSINESS_GOOGLE_QUESTIONS_AND_ANSWERS = "business_data.google.questions_and_answers"
    AI_CHAT_GPT_LLM_RESPONSES = "ai_optimization.chat_gpt.llm_responses"
    AI_CLAUDE_LLM_RESPONSES = "ai_optimization.claude.llm_responses"
    AI_GEMINI_LLM_RESPONSES = "ai_optimization.gemini.llm_responses"
    AI_PERPLEXITY_LLM_RESPONSES = "ai_optimization.perplexity.llm_responses"
    AI_LLM_MENTIONS_SEARCH = "ai_optimization.llm_mentions.search"
    AI_LLM_MENTIONS_AGGREGATED_METRICS = "ai_optimization.llm_mentions.aggregated_metrics"
    AI_LLM_MENTIONS_CROSS_AGGREGATED_METRICS = (
        "ai_optimization.llm_mentions.cross_aggregated_metrics"
    )
    AI_LLM_MENTIONS_TOP_PAGES = "ai_optimization.llm_mentions.top_pages"


class DataForSeoTask(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    status_code: int
    status_message: str
    time: str | None = None
    cost: Decimal | None = None
    result_count: int = 0
    path: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)
    result: list[Any] | dict[str, Any] | None = None


class DataForSeoEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: str | None = None
    status_code: int
    status_message: str
    time: str | None = None
    cost: Decimal | None = None
    tasks_count: int = 0
    tasks_error: int = 0
    tasks: list[DataForSeoTask] = Field(default_factory=list)


class DataForSeoCollectionSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tasks: list[dict[str, Any]]
    workflow: DataForSeoWorkflow = DataForSeoWorkflow.LIVE
    endpoint: str | None = None
    priority: str = "normal"
    target_aliases: list[str] = Field(default_factory=list)
    #: Total items to collect across pages for a paginated live endpoint. One
    #: provider request returns at most 1000 items, so anything larger than that
    #: is a paged collection — the client loops on ``search_after_token`` (or
    #: ``offset``) and merges every page into one result. ``None`` keeps the
    #: historical single-request behavior.
    max_items: int | None = Field(default=None, ge=1, le=100_000)

    @field_validator("tasks")
    @classmethod
    def require_tasks(cls, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not tasks:
            raise ValueError("DataForSEO requires at least one task")
        if len(tasks) > 100:
            raise ValueError("DataForSEO accepts at most 100 tasks per request")
        return tasks

    @model_validator(mode="after")
    def validate_live_cardinality(self) -> DataForSeoCollectionSettings:
        # Second layer in front of DataForSeoClient._execute_live's guard: a
        # live endpoint completes inside the POST and takes exactly one task,
        # so a batched live request is a caller bug. Catching it here fails the
        # request while it is still being BUILT — before a seo.collection_run
        # row, a lease, and three retry attempts are spent discovering the same
        # thing from inside the collection service.
        if self.workflow is DataForSeoWorkflow.LIVE and len(self.tasks) != 1:
            raise ValueError(
                "DataForSEO live endpoints accept exactly one task; this request carries "
                f"{len(self.tasks)}. Send one live request per task (fan out at the call "
                "site), or use workflow='standard' if the operation supports it."
            )
        return self


#: Labs operations whose ``target`` DataForSEO accepts ONLY as a bare hostname (no scheme,
#: no ``www.``, no path, no query).
BARE_DOMAIN_TARGET_OPERATIONS: frozenset[str] = frozenset(
    {"labs.google.domain_rank_overview", "labs.google.historical_rank_overview"}
)


def normalize_domain_target(operation: str, task: dict[str, Any]) -> dict[str, Any]:
    """Return ``task`` with a bare-hostname ``target`` for operations that only accept one.

    A value that is not a recognisable hostname is left exactly as given, so the provider's own
    refusal still reaches the caller rather than a made-up domain."""
    if str(operation) not in BARE_DOMAIN_TARGET_OPERATIONS:
        return task
    raw = task.get("target")
    if not isinstance(raw, str) or not raw.strip():
        return task
    from urllib.parse import urlsplit

    text = raw.strip()
    parts = urlsplit(text if "://" in text else f"//{text}")
    host = (parts.hostname or "").lower().removeprefix("www.")
    if not host or "." not in host or parts.username or parts.password:
        return task
    return {**task, "target": host}


class DataForSeoOperationRequest(DataForSeoCollectionSettings):
    operation: DataForSeoOperationName

    @model_validator(mode="after")
    def coerce_single_keyword_to_list(self) -> DataForSeoOperationRequest:
        # A stored or on-demand payload that carries ``keywords`` as one bare
        # string for an endpoint whose provider contract takes a list is a
        # one-item list. Sending the string is rejected by DataForSEO ("Invalid
        # Field: 'keywords'") and burns a collection run (111 such failures).
        from .operations import DATAFORSEO_ENDPOINT_EXAMPLE_TASKS, get_operation

        endpoints = get_operation(self.operation).endpoints
        takes_list = any(
            isinstance(DATAFORSEO_ENDPOINT_EXAMPLE_TASKS.get(endpoint, {}).get("keywords"), list)
            for endpoint in endpoints
        )
        if takes_list:
            for task in self.tasks:
                if isinstance(task.get("keywords"), str):
                    task["keywords"] = [task["keywords"]]
        return self

    @model_validator(mode="after")
    def coerce_domain_target_to_hostname(self) -> DataForSeoOperationRequest:
        # Labs domain-rank operations accept ``target`` ONLY as a bare hostname. A URL
        # ("https://www.example.com/pricing") is refused ("Invalid Field: 'target'") and burns a
        # collection run (seo_collection_failed, /seo/collections, 2026-11-20). Every caller reaches
        # the provider through this request, so the one normalization lives here.
        for index, task in enumerate(self.tasks):
            self.tasks[index] = normalize_domain_target(self.operation, task)
        return self

    @model_validator(mode="after")
    def validate_operation_limits(self) -> DataForSeoOperationRequest:
        if self.operation is not DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME:
            return self
        for task_index, task in enumerate(self.tasks):
            keywords = task.get("keywords")
            if not isinstance(keywords, list) or not all(
                isinstance(keyword, str) for keyword in keywords
            ):
                raise ValueError(
                    "DataForSEO Google Ads search volume requires a string keywords list "
                    f"for task {task_index}"
                )
            if len(keywords) > GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORDS:
                raise ValueError(
                    "DataForSEO Google Ads search volume accepts at most "
                    f"{GOOGLE_ADS_SEARCH_VOLUME_MAX_KEYWORDS} keywords per task"
                )
            rejected = [
                (keyword, reason)
                for keyword in keywords
                if (reason := google_ads_search_volume_keyword_rejection_reason(keyword))
                is not None
            ]
            if rejected:
                preview = "; ".join(f"{keyword!r}: {reason}" for keyword, reason in rejected[:5])
                suffix = f"; and {len(rejected) - 5} more" if len(rejected) > 5 else ""
                raise ValueError(
                    "DataForSEO Google Ads search volume rejected invalid keywords "
                    f"in task {task_index}: {preview}{suffix}"
                )
        return self


class DataForSeoLocation(BaseModel):
    model_config = ConfigDict(extra="allow")

    location_code: int
    location_name: str
    location_name_parent: str | None = None
    country_iso_code: str | None = None
    location_type: str | None = None


class DataForSeoLanguage(BaseModel):
    model_config = ConfigDict(extra="allow")

    language_name: str
    language_code: str
