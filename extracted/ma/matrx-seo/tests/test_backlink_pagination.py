"""The 1000-row provider ceiling, and the paging that gets past it.

Two managed sites sat at EXACTLY 1000 stored backlinks while their own summary
rows reported far more: one live request returns at most 1000 items whatever
``limit`` says, and nothing looped. Every count downstream was quietly wrong.

These tests pin the loop, the merge (one result, not one per page), and the
money rules — a page that fails after page one must never discard the pages we
already paid for.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest

from matrx_seo.adapters import ProviderExecutionContext
from matrx_seo.backlink_refresh import (
    BacklinkRefreshOptions,
    BacklinkRefreshProfile,
    BacklinkRefreshService,
)
from matrx_seo.contracts import (
    BacklinkSnapshotObservation,
    CollectionReceipt,
    CollectionRequest,
    NormalizationContext,
    ResolvedCredential,
    ResolvedHostBinding,
    SeoCapability,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter
from matrx_seo.providers.dataforseo.client import DataForSeoClient
from matrx_seo.providers.dataforseo.contracts import (
    DataForSeoOperationRequest,
    DataForSeoWorkflow,
)
from matrx_seo.providers.dataforseo.transport import ReplayTransport
from matrx_seo.repository import InMemorySeoRepository

BACKLINKS_ENDPOINT = "/v3/backlinks/backlinks/live"


def _items(start: int, count: int) -> list[dict[str, Any]]:
    return [
        {
            "type": "backlink",
            "url_from": f"https://ref{index}.example/page",
            "domain_from": f"ref{index}.example",
            "url_to": "https://example.com/",
            "anchor": f"anchor {index}",
            "dofollow": True,
            "page_from_rank": 10,
            "domain_from_rank": 20,
        }
        for index in range(start, start + count)
    ]


def _page(
    *,
    task_id: str,
    items: list[dict[str, Any]],
    total_count: int,
    search_after_token: str | None,
    status_code: int = 20000,
    status_message: str = "Ok.",
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "target": "example.com",
        "total_count": total_count,
        "items_count": len(items),
        "items": items,
    }
    if search_after_token is not None:
        result["search_after_token"] = search_after_token
    return {
        "version": "0.1.20260722",
        "status_code": 20000,
        "status_message": "Ok.",
        "cost": 0.036,
        "tasks_count": 1,
        "tasks_error": 0 if status_code == 20000 else 1,
        "tasks": [
            {
                "id": task_id,
                "status_code": status_code,
                "status_message": status_message,
                "cost": 0.036,
                "result_count": 1,
                "result": [result],
            }
        ],
    }


def _paged_request(max_items: int, *, limit: int = 1000) -> DataForSeoOperationRequest:
    return DataForSeoOperationRequest(
        operation="backlinks.core",
        workflow=DataForSeoWorkflow.LIVE,
        endpoint=BACKLINKS_ENDPOINT,
        tasks=[{"target": "example.com", "limit": limit}],
        max_items=max_items,
    )


def _merged_items(response: Any) -> list[dict[str, Any]]:
    return response.raw["tasks"][0]["result"][0]["items"]


@pytest.mark.asyncio
async def test_paging_follows_search_after_token_and_merges_into_one_result() -> None:
    transport = ReplayTransport(
        [
            _page(task_id="p1", items=_items(0, 1000), total_count=2500, search_after_token="t1"),
            _page(
                task_id="p2", items=_items(1000, 1000), total_count=2500, search_after_token="t2"
            ),
            _page(task_id="p3", items=_items(2000, 500), total_count=2500, search_after_token="t3"),
        ]
    )
    client = DataForSeoClient(transport)

    response = await client.execute(_paged_request(10_000))

    assert len(transport.requests) == 3
    bodies = [request[2][0] for request in transport.requests]
    assert "search_after_token" not in bodies[0]
    assert bodies[1]["search_after_token"] == "t1"
    assert bodies[2]["search_after_token"] == "t2"
    # Every page keeps the caller's own task fields.
    assert all(body["target"] == "example.com" for body in bodies)

    # ONE result, every item in it. Per-page results would collapse to a single
    # observation row on the (run, site, dataset, target, observed_at) dedup key
    # and only page one's links would survive.
    assert len(response.raw["tasks"]) == 1
    assert len(response.raw["tasks"][0]["result"]) == 1
    merged = _merged_items(response)
    assert len(merged) == 2500
    assert merged[0]["url_from"] == "https://ref0.example/page"
    assert merged[-1]["url_from"] == "https://ref2499.example/page"
    assert response.raw["tasks"][0]["result"][0]["items_count"] == 2500
    assert response.raw["tasks"][0]["result"][0]["total_count"] == 2500
    assert response.error is None

    pagination = response.raw["_matrx_pagination"]
    assert pagination["collected"] == 2500
    assert pagination["total_count"] == 2500
    assert pagination["stop_reason"] == "complete"
    assert pagination["truncated"] is False
    assert [page["items"] for page in pagination["pages"]] == [1000, 1000, 500]

    # Every page is separately billed and must show up as its own call record.
    assert [record.provider_call_key for record in response.call_records] == ["p1", "p2", "p3"]
    assert response.request_count == 3
    assert float(response.reported_cost) == pytest.approx(0.108)


@pytest.mark.asyncio
async def test_paging_falls_back_to_offset_when_no_token_is_returned() -> None:
    transport = ReplayTransport(
        [
            _page(task_id="p1", items=_items(0, 1000), total_count=1500, search_after_token=None),
            _page(task_id="p2", items=_items(1000, 500), total_count=1500, search_after_token=None),
        ]
    )
    client = DataForSeoClient(transport)

    response = await client.execute(_paged_request(10_000))

    bodies = [request[2][0] for request in transport.requests]
    assert "offset" not in bodies[0]
    assert bodies[1]["offset"] == 1000
    assert len(_merged_items(response)) == 1500
    assert response.raw["_matrx_pagination"]["stop_reason"] == "complete"


@pytest.mark.asyncio
async def test_budget_stops_the_loop_and_marks_the_dataset_truncated() -> None:
    transport = ReplayTransport(
        [
            _page(task_id="p1", items=_items(0, 1000), total_count=9000, search_after_token="t1"),
            _page(task_id="p2", items=_items(1000, 500), total_count=9000, search_after_token="t2"),
        ]
    )
    client = DataForSeoClient(transport)

    response = await client.execute(_paged_request(1500))

    assert len(transport.requests) == 2
    # The last page asks only for what the budget still allows.
    assert transport.requests[1][2][0]["limit"] == 500
    assert len(_merged_items(response)) == 1500
    pagination = response.raw["_matrx_pagination"]
    assert pagination["stop_reason"] == "budget_reached"
    assert pagination["truncated"] is True
    assert pagination["collected"] == 1500
    assert pagination["total_count"] == 9000


@pytest.mark.asyncio
async def test_a_failure_after_page_one_keeps_every_page_already_paid_for() -> None:
    transport = ReplayTransport(
        [
            _page(task_id="p1", items=_items(0, 1000), total_count=5000, search_after_token="t1"),
            _page(
                task_id="p2",
                items=[],
                total_count=0,
                search_after_token=None,
                status_code=40501,
                status_message="Internal Error.",
            ),
        ]
    )
    client = DataForSeoClient(transport)

    response = await client.execute(_paged_request(5000))

    # response.error would fail the run and drop all 1000 rows we just bought.
    assert response.error is None
    assert len(_merged_items(response)) == 1000
    pagination = response.raw["_matrx_pagination"]
    assert pagination["stop_reason"] == "provider_error"
    assert pagination["truncated"] is True
    assert pagination["stop_error"]["status_code"] == 20000
    assert "Internal Error." in pagination["stop_error"]["message"]


@pytest.mark.asyncio
async def test_a_failure_on_page_one_still_fails_the_run() -> None:
    transport = ReplayTransport(
        [
            _page(
                task_id="p1",
                items=[],
                total_count=0,
                search_after_token=None,
                status_code=40501,
                status_message="Internal Error.",
            )
        ]
    )
    client = DataForSeoClient(transport)

    response = await client.execute(_paged_request(5000))

    assert response.error is not None
    assert response.raw["_matrx_pagination"]["collected"] == 0


@pytest.mark.asyncio
async def test_a_budget_on_an_unpaginated_endpoint_is_refused_before_the_first_request() -> None:
    transport = ReplayTransport([])
    client = DataForSeoClient(transport)
    request = DataForSeoOperationRequest(
        operation="backlinks.core",
        workflow=DataForSeoWorkflow.LIVE,
        endpoint="/v3/backlinks/summary/live",
        tasks=[{"target": "example.com"}],
        max_items=5000,
    )

    with pytest.raises(ValueError, match="does not paginate"):
        await client.execute(request)
    assert transport.requests == []


@pytest.mark.asyncio
async def test_more_than_one_thousand_backlinks_normalize_into_one_snapshot() -> None:
    """The defect, end to end: 2500 provider rows must reach persistence.

    Before paging this produced exactly 1000 items — the number two live sites
    were stuck at.
    """
    adapter = DataForSeoAdapter(
        transport=ReplayTransport(
            [
                _page(
                    task_id="p1", items=_items(0, 1000), total_count=2500, search_after_token="t1"
                ),
                _page(
                    task_id="p2",
                    items=_items(1000, 1000),
                    total_count=2500,
                    search_after_token="t2",
                ),
                _page(
                    task_id="p3", items=_items(2000, 500), total_count=2500, search_after_token="t3"
                ),
            ]
        )
    )
    await adapter.authenticate(
        ResolvedCredential(
            values={
                "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
                "DATA_FOR_SEO_PASSWORD": "fixture",
            }
        )
    )
    request = CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=SeoCapability.BACKLINKS,
        operation="backlinks.core",
        target_ref="web.site:site-1",
        site_id="site-1",
        observation_period=datetime.now(UTC).isoformat(),
        settings={
            "workflow": "live",
            "endpoint": BACKLINKS_ENDPOINT,
            "tasks": [{"target": "example.com", "limit": 1000}],
            "max_items": 10_000,
        },
        force_refresh=True,
    )
    repository = InMemorySeoRepository()
    run = await repository.start_run("dataforseo", request)

    response = await adapter.collect_response(request, ProviderExecutionContext(repository, run))
    observations = await adapter.normalize(
        response,
        NormalizationContext(
            request=request,
            run=run,
            raw_payload_id="raw-id",
            identity_resolver=object(),
            host_binding_resolver=object(),
        ),
    )

    assert len(observations) == 1
    snapshot = observations[0]
    assert isinstance(snapshot, BacklinkSnapshotObservation)
    assert snapshot.dataset == "backlinks"
    assert len(snapshot.backlinks) == 2500
    assert len({item.source_url for item in snapshot.backlinks}) == 2500
    # The provider's own total stays the reported metric.
    assert snapshot.total_backlinks == 2500


class _HostResolver:
    async def resolve(self, request: Any, binding: Any) -> ResolvedHostBinding:
        assert request.site_id == binding.resource_id
        return ResolvedHostBinding(
            site_id=binding.resource_id,
            canonical_url="https://www.example.com/",
        )


@dataclass
class _CollectionService:
    host_binding_resolver: Any = field(default_factory=_HostResolver)
    requests: list[Any] = field(default_factory=list)

    async def collect(self, _adapter: Any, request: Any) -> CollectionReceipt:
        self.requests.append(request)
        return CollectionReceipt(run_id=f"run-{len(self.requests)}")


@pytest.mark.asyncio
async def test_refresh_sends_a_paging_budget_only_where_the_provider_pages() -> None:
    collection_service = _CollectionService()
    service = BacklinkRefreshService(
        collection_service,  # type: ignore[arg-type]
        adapter_factory=lambda: object(),  # type: ignore[arg-type,return-value]
    )

    await service.refresh_site(
        BacklinkRefreshOptions(
            organization_id="org-1",
            created_by="user-1",
            site_id="site-1",
            profile=BacklinkRefreshProfile.BOOTSTRAP,
            detail_max_rows=25_000,
        )
    )

    budgets = {
        request.settings["endpoint"]: request.settings.get("max_items")
        for request in collection_service.requests
    }
    assert budgets["/v3/backlinks/backlinks/live"] == 25_000
    assert budgets["/v3/backlinks/referring_domains/live"] == 25_000
    assert budgets["/v3/backlinks/anchors/live"] == 25_000
    assert budgets["/v3/backlinks/summary/live"] is None
    assert budgets["/v3/backlinks/competitors/live"] is None


@pytest.mark.asyncio
async def test_a_budget_at_or_below_one_page_stays_a_single_request() -> None:
    collection_service = _CollectionService()
    service = BacklinkRefreshService(
        collection_service,  # type: ignore[arg-type]
        adapter_factory=lambda: object(),  # type: ignore[arg-type,return-value]
    )

    await service.refresh_site(
        BacklinkRefreshOptions(
            organization_id="org-1",
            created_by="user-1",
            site_id="site-1",
            profile=BacklinkRefreshProfile.MONTHLY,
            detail_limit=1000,
            detail_max_rows=1000,
        )
    )

    assert all("max_items" not in request.settings for request in collection_service.requests)
