from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_seo.backlink_refresh import (
    BacklinkRefreshOptions,
    BacklinkRefreshProfile,
    BacklinkRefreshService,
    backlink_refresh_datasets,
)
from matrx_seo.contracts import CollectionReceipt, ResolvedHostBinding


class _HostResolver:
    async def resolve(self, request, binding):
        assert request.site_id == binding.resource_id
        return ResolvedHostBinding(
            site_id=binding.resource_id,
            canonical_url="https://www.Example.com/path",
        )


@dataclass
class _CollectionService:
    host_binding_resolver: Any = field(default_factory=_HostResolver)
    requests: list[Any] = field(default_factory=list)

    async def collect(self, _adapter, request):
        self.requests.append(request)
        return CollectionReceipt(run_id=f"run-{len(self.requests)}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("profile", "datasets"),
    [
        (BacklinkRefreshProfile.WEEKLY, ["summary", "timeseries_new_lost_summary"]),
        (
            BacklinkRefreshProfile.MONTHLY,
            [
                "summary",
                "backlinks",
                "referring_domains",
                "anchors",
                "domain_pages_summary",
                "competitors",
            ],
        ),
        (
            BacklinkRefreshProfile.BOOTSTRAP,
            [
                "summary",
                "backlinks",
                "referring_domains",
                "anchors",
                "history",
                "domain_pages",
                "domain_pages_summary",
                "timeseries_summary",
                "timeseries_new_lost_summary",
                "competitors",
            ],
        ),
    ],
)
async def test_refresh_profiles_use_canonical_site_and_exact_endpoints(
    profile: BacklinkRefreshProfile, datasets: list[str]
) -> None:
    collection_service = _CollectionService()
    service = BacklinkRefreshService(
        collection_service,  # type: ignore[arg-type]
        adapter_factory=lambda: object(),  # type: ignore[arg-type,return-value]
    )

    result = await service.refresh_site(
        BacklinkRefreshOptions(
            organization_id="org-1",
            created_by="user-1",
            site_id="site-1",
            profile=profile,
            detail_limit=321,
            request_id="refresh-1",
        )
    )

    assert result.target == "example.com"
    assert [item.dataset for item in result.datasets] == datasets
    assert len(collection_service.requests) == len(datasets)
    for request, dataset in zip(collection_service.requests, datasets, strict=True):
        assert request.site_id == "site-1"
        assert request.target_ref == "web.site:site-1"
        assert request.force_refresh is True
        assert request.request_id == f"refresh-1:{dataset}"
        assert request.settings["workflow"] == "live"
        assert request.settings["endpoint"].endswith(f"/{dataset}/live")
        task = request.settings["tasks"][0]
        assert task["target"] == "example.com"
        assert task["include_subdomains"] is True
        assert task["exclude_internal_backlinks"] is True
        if dataset in {
            "backlinks",
            "referring_domains",
            "anchors",
            "domain_pages",
            "domain_pages_summary",
            "competitors",
        }:
            assert task["limit"] == 321
        else:
            assert "limit" not in task

    assert backlink_refresh_datasets(profile) == tuple(datasets)


def test_refresh_detail_limit_is_provider_bounded() -> None:
    with pytest.raises(ValueError):
        BacklinkRefreshOptions(
            organization_id="org-1",
            created_by="user-1",
            site_id="site-1",
            detail_limit=1001,
        )
