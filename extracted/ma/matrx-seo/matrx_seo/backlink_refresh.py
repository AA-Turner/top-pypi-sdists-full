"""Site-scoped DataForSEO backlink refresh profiles.

This is the reusable orchestration seam shared by manual HTTP refreshes and the
future scheduler handler.  It deliberately composes the existing collection
service so raw payload capture, costs, cache rules, and normalized persistence
remain identical to every other SEO collection.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from .adapters import SeoProgressCallback
from .contracts import (
    CollectionReceipt,
    CollectionRequest,
    CollectionTrigger,
    HostBindingRequest,
    SeoCapability,
)
from .providers.dataforseo import DataForSeoAdapter
from .providers.dataforseo.operations import PAGINATED_LIVE_ENDPOINTS
from .rank_matching import canonicalize_domain
from .service import SeoCollectionService


class BacklinkRefreshProfile(StrEnum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    BOOTSTRAP = "bootstrap"


class BacklinkRefreshOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_id: str
    created_by: str
    site_id: str
    profile: BacklinkRefreshProfile = BacklinkRefreshProfile.BOOTSTRAP
    #: Rows per provider request. The provider hard-caps a page at 1000.
    detail_limit: int = Field(default=1000, ge=1, le=1000)
    #: Rows to collect per paginated dataset for this site, across pages. The
    #: provider truncates every dataset at ``detail_limit`` per request, so
    #: without a budget above 1000 a large site stores exactly 1000 backlinks
    #: and every downstream count is quietly wrong. Each additional page is a
    #: separately billed request (~$0.036 / 1000 rows), which is why this is a
    #: bounded budget and not "collect everything".
    detail_max_rows: int = Field(default=10_000, ge=1, le=100_000)
    force_refresh: bool = True
    request_id: str | None = None
    source_crawl_session_id: str | None = None
    trigger: CollectionTrigger = CollectionTrigger.ON_DEMAND


class BacklinkDatasetReceipt(BaseModel):
    dataset: str
    operation: str
    endpoint: str
    receipt: CollectionReceipt


class BacklinkRefreshReceipt(BaseModel):
    site_id: str
    target: str
    profile: BacklinkRefreshProfile
    datasets: list[BacklinkDatasetReceipt]


@dataclass(frozen=True)
class _DatasetSpec:
    dataset: str
    operation: str
    endpoint: str
    limited: bool = False
    #: The provider result carries ``search_after_token`` / accepts ``offset``,
    #: so this dataset can be collected past one 1000-row page. Must stay in
    #: sync with ``PAGINATED_LIVE_ENDPOINTS`` — the client refuses a paging
    #: budget for anything else.
    paginated: bool = False


_SUMMARY = _DatasetSpec("summary", "backlinks.core", "/v3/backlinks/summary/live")
_BACKLINKS = _DatasetSpec(
    "backlinks",
    "backlinks.core",
    "/v3/backlinks/backlinks/live",
    limited=True,
    paginated=True,
)
_REFERRING_DOMAINS = _DatasetSpec(
    "referring_domains",
    "backlinks.core",
    "/v3/backlinks/referring_domains/live",
    limited=True,
    paginated=True,
)
_ANCHORS = _DatasetSpec(
    "anchors",
    "backlinks.core",
    "/v3/backlinks/anchors/live",
    limited=True,
    paginated=True,
)
_HISTORY = _DatasetSpec("history", "backlinks.history", "/v3/backlinks/history/live")
_DOMAIN_PAGES = _DatasetSpec(
    "domain_pages",
    "backlinks.pages_competitors_timeseries",
    "/v3/backlinks/domain_pages/live",
    limited=True,
)
_DOMAIN_PAGES_SUMMARY = _DatasetSpec(
    "domain_pages_summary",
    "backlinks.pages_competitors_timeseries",
    "/v3/backlinks/domain_pages_summary/live",
    limited=True,
)
_TIMESERIES_SUMMARY = _DatasetSpec(
    "timeseries_summary",
    "backlinks.pages_competitors_timeseries",
    "/v3/backlinks/timeseries_summary/live",
)
_TIMESERIES_NEW_LOST = _DatasetSpec(
    "timeseries_new_lost_summary",
    "backlinks.pages_competitors_timeseries",
    "/v3/backlinks/timeseries_new_lost_summary/live",
)
_COMPETITORS = _DatasetSpec(
    "competitors",
    "backlinks.pages_competitors_timeseries",
    "/v3/backlinks/competitors/live",
    limited=True,
)

_PROFILE_DATASETS: dict[BacklinkRefreshProfile, tuple[_DatasetSpec, ...]] = {
    BacklinkRefreshProfile.WEEKLY: (_SUMMARY, _TIMESERIES_NEW_LOST),
    BacklinkRefreshProfile.MONTHLY: (
        _SUMMARY,
        _BACKLINKS,
        _REFERRING_DOMAINS,
        _ANCHORS,
        _DOMAIN_PAGES_SUMMARY,
        _COMPETITORS,
    ),
    BacklinkRefreshProfile.BOOTSTRAP: (
        _SUMMARY,
        _BACKLINKS,
        _REFERRING_DOMAINS,
        _ANCHORS,
        _HISTORY,
        _DOMAIN_PAGES,
        _DOMAIN_PAGES_SUMMARY,
        _TIMESERIES_SUMMARY,
        _TIMESERIES_NEW_LOST,
        _COMPETITORS,
    ),
}


_MISDECLARED_PAGINATION = {
    spec.endpoint for specs in _PROFILE_DATASETS.values() for spec in specs if spec.paginated
} - PAGINATED_LIVE_ENDPOINTS
if _MISDECLARED_PAGINATION:
    # Second layer in front of the client's own refusal. A spec that claims
    # pagination the provider contract does not list would spend a real request
    # to discover it, once per site, on a schedule.
    raise RuntimeError(
        "backlink refresh specs claim pagination for endpoints the DataForSEO client "
        f"does not page: {sorted(_MISDECLARED_PAGINATION)}"
    )


def backlink_refresh_datasets(profile: BacklinkRefreshProfile) -> tuple[str, ...]:
    """Return the canonical ordered dataset roster for a refresh profile."""

    return tuple(spec.dataset for spec in _PROFILE_DATASETS[profile])


class BacklinkRefreshService:
    def __init__(
        self,
        collection_service: SeoCollectionService,
        *,
        adapter_factory: Callable[[], DataForSeoAdapter] = DataForSeoAdapter,
    ) -> None:
        self.collection_service = collection_service
        self.adapter_factory = adapter_factory

    async def refresh_site(
        self,
        options: BacklinkRefreshOptions,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> BacklinkRefreshReceipt:
        requested_at = datetime.now(UTC)
        request_group_id = options.request_id or str(uuid4())
        binding_request = CollectionRequest(
            organization_id=options.organization_id,
            created_by=options.created_by,
            capability=SeoCapability.BACKLINKS,
            operation=_SUMMARY.operation,
            target_ref=f"web.site:{options.site_id}",
            site_id=options.site_id,
            source_crawl_session_id=options.source_crawl_session_id,
            observation_period=requested_at.date().isoformat(),
            trigger=options.trigger,
            settings={"workflow": "live", "endpoint": _SUMMARY.endpoint, "tasks": []},
        )
        binding = await self.collection_service.host_binding_resolver.resolve(
            binding_request,
            HostBindingRequest(resource_kind="web_site", resource_id=options.site_id),
        )
        target = canonicalize_domain(binding.canonical_url)
        if not target:
            raise ValueError(f"web.site {options.site_id} has no canonical domain in root_url")

        specs = _PROFILE_DATASETS[options.profile]
        receipts: list[BacklinkDatasetReceipt] = []
        for index, spec in enumerate(specs):
            if progress is not None:
                await progress(
                    "backlink_dataset_started",
                    {
                        "dataset": spec.dataset,
                        "operation": spec.operation,
                        "endpoint": spec.endpoint,
                        "dataset_index": index,
                        "dataset_count": len(specs),
                    },
                )
            task: dict[str, object] = {
                "target": target,
                "include_subdomains": True,
                "exclude_internal_backlinks": True,
            }
            if spec.limited:
                task["limit"] = options.detail_limit
            settings: dict[str, object] = {
                "workflow": "live",
                "endpoint": spec.endpoint,
                "tasks": [task],
            }
            if spec.paginated and options.detail_max_rows > options.detail_limit:
                settings["max_items"] = options.detail_max_rows
            collection = binding_request.model_copy(
                update={
                    "operation": spec.operation,
                    "observation_period": f"{requested_at.isoformat()}:{spec.dataset}",
                    "settings": settings,
                    "request_id": f"{request_group_id}:{spec.dataset}",
                    "force_refresh": options.force_refresh,
                }
            )
            dataset_progress: SeoProgressCallback | None = None
            if progress is not None:
                outer_progress = progress
                dataset_name = spec.dataset

                async def dataset_progress(  # noqa: E731 - closure over loop vars pinned above
                    event: str,
                    payload: dict[str, object],
                    _emit: SeoProgressCallback = outer_progress,
                    _dataset: str = dataset_name,
                ) -> None:
                    await _emit(event, {"dataset": _dataset, **payload})

            if dataset_progress is None:
                receipt = await self.collection_service.collect(self.adapter_factory(), collection)
            else:
                receipt = await self.collection_service.collect(
                    self.adapter_factory(), collection, progress=dataset_progress
                )
            receipts.append(
                BacklinkDatasetReceipt(
                    dataset=spec.dataset,
                    operation=spec.operation,
                    endpoint=spec.endpoint,
                    receipt=receipt,
                )
            )
            if progress is not None:
                await progress(
                    "backlink_dataset_completed",
                    {
                        "dataset": spec.dataset,
                        "dataset_index": index,
                        "dataset_count": len(specs),
                        "receipt": receipt.model_dump(mode="json"),
                    },
                )
        return BacklinkRefreshReceipt(
            site_id=binding.site_id,
            target=target,
            profile=options.profile,
            datasets=receipts,
        )
