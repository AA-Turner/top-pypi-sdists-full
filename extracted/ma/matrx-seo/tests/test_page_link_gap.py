from __future__ import annotations

from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_seo.contracts import CollectionReceipt
from matrx_seo.page_link_gap import (
    PageLinkGapOptions,
    PageLinkGapService,
    competitor_is_link_gap_eligible,
)


class _Rows:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    async def all(self) -> list[Any]:
        return self.rows


@dataclass
class _CollectionService:
    requests: list[Any] = field(default_factory=list)

    async def collect(self, _adapter: Any, request: Any, *, progress: Any = None):
        self.requests.append(request)
        return CollectionReceipt(run_id="page-gap-run")


def _competitor(**overrides: Any) -> SimpleNamespace:
    values = {
        "id": "competitor-1",
        "classification_status": "confirmed",
        "use_for_link_gap": None,
        "entity_role": "business",
        "business_overlap": "direct",
        **overrides,
    }
    return SimpleNamespace(**values)


def test_link_gap_eligibility_requires_confirmation_and_taxonomy() -> None:
    assert competitor_is_link_gap_eligible(_competitor())
    assert not competitor_is_link_gap_eligible(_competitor(classification_status="proposed"))
    assert not competitor_is_link_gap_eligible(_competitor(entity_role="publisher"))
    assert competitor_is_link_gap_eligible(
        _competitor(entity_role="publisher", use_for_link_gap=True)
    )
    assert not competitor_is_link_gap_eligible(_competitor(use_for_link_gap=False))


@pytest.mark.asyncio
async def test_page_gap_reuses_accepted_competitor_opportunities(monkeypatch) -> None:
    from matrx_seo import page_link_gap as module

    opportunities = [
        SimpleNamespace(
            id=f"opportunity-{index}",
            site_id="site-1",
            target_page_id="page-1",
            status="accepted",
            competitor_id=f"competitor-{index}",
            competitor_url=f"https://rival-{index}.example/exact-guide",
        )
        for index in (1, 2)
    ]
    competitors = [
        SimpleNamespace(
            id=f"competitor-{index}",
            classification_status="confirmed",
            use_for_link_gap=None,
            entity_role="business",
            business_overlap="adjacent",
        )
        for index in (1, 2)
    ]

    async def load_page(_page_id: str):
        return SimpleNamespace(id="page-1", site_id="site-1", url="https://ours.example/our-guide")

    monkeypatch.setattr(module.WebPage, "load_by_id_or_none", load_page)
    monkeypatch.setattr(
        module.m.CompetitorOpportunity,
        "filter",
        lambda **_kwargs: _Rows(opportunities),
    )
    monkeypatch.setattr(
        module.m.Competitor,
        "filter",
        lambda **_kwargs: _Rows(competitors),
    )
    collection_service = _CollectionService()
    receipt = await PageLinkGapService(collection_service).collect(  # type: ignore[arg-type]
        PageLinkGapOptions(
            organization_id="org-1",
            created_by="user-1",
            site_id="site-1",
            page_id="page-1",
            opportunity_ids=["opportunity-1", "opportunity-2"],
            limit=250,
            max_spam_score=25,
        )
    )

    assert receipt.receipt.run_id == "page-gap-run"
    [request] = collection_service.requests
    assert request.page_id == "page-1"
    assert request.operation == "backlinks.intersections"
    assert request.settings["endpoint"] == "/v3/backlinks/page_intersection/live"
    task = request.settings["tasks"][0]
    assert task["targets"] == {
        "1": "https://rival-1.example/exact-guide",
        "2": "https://rival-2.example/exact-guide",
    }
    assert task["exclude_targets"] == ["https://ours.example/our-guide"]
    assert task["limit"] == 250
    assert task["intersection_mode"] == "partial"
    assert task["filters"] == [
        ["1.backlink_spam_score", "<=", 25],
        "or",
        ["2.backlink_spam_score", "<=", 25],
    ]


@pytest.mark.asyncio
async def test_page_gap_rejects_unaccepted_page_proposals(monkeypatch) -> None:
    from matrx_seo import page_link_gap as module

    opportunities = [
        SimpleNamespace(
            id=f"opportunity-{index}",
            site_id="site-1",
            target_page_id="page-1",
            status="open" if index == 1 else "accepted",
            competitor_id=f"competitor-{index}",
            competitor_url=f"https://rival-{index}.example/guide",
        )
        for index in (1, 2)
    ]
    competitors = [
        SimpleNamespace(
            id=f"competitor-{index}",
            classification_status="confirmed",
            use_for_link_gap=True,
            entity_role="business",
            business_overlap="direct",
        )
        for index in (1, 2)
    ]

    async def load_page(_page_id: str):
        return SimpleNamespace(site_id="site-1", url="https://ours.example/guide")

    monkeypatch.setattr(module.WebPage, "load_by_id_or_none", load_page)
    monkeypatch.setattr(
        module.m.CompetitorOpportunity,
        "filter",
        lambda **_kwargs: _Rows(opportunities),
    )
    monkeypatch.setattr(
        module.m.Competitor,
        "filter",
        lambda **_kwargs: _Rows(competitors),
    )
    with pytest.raises(ValueError, match="not human-accepted"):
        await PageLinkGapService(_CollectionService()).collect(  # type: ignore[arg-type]
            PageLinkGapOptions(
                organization_id="org-1",
                created_by="user-1",
                site_id="site-1",
                page_id="page-1",
                opportunity_ids=["opportunity-1", "opportunity-2"],
            )
        )
