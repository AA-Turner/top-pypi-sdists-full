from decimal import Decimal
from types import SimpleNamespace

import pytest

from matrx_seo import backlink_enrichment as subject
from matrx_seo.backlink_enrichment import (
    backlink_identity_key,
    deterministic_assessment,
)
from matrx_seo.contracts import BacklinkItem


def test_identity_is_exact_source_page_to_target_page_relationship() -> None:
    baseline = backlink_identity_key(
        "site-1", "https://source.example/article", "https://brand.example/service"
    )

    assert baseline == backlink_identity_key(
        "site-1", "https://source.example/article", "https://brand.example/service"
    )
    assert baseline == backlink_identity_key(
        "site-1",
        "http://www.source.example/article/#fragment",
        "http://www.brand.example/service/",
    )
    assert baseline != backlink_identity_key(
        "site-1", "https://source.example/other", "https://brand.example/service"
    )
    assert baseline != backlink_identity_key(
        "site-1", "https://source.example/article", "https://brand.example/other"
    )


def test_identity_preserves_path_case_and_semantic_query_parameters() -> None:
    baseline = backlink_identity_key(
        "site-1", "https://source.example/Article?state=ca", "https://brand.example/"
    )

    assert baseline != backlink_identity_key(
        "site-1", "https://source.example/article?state=ca", "https://brand.example/"
    )
    assert baseline != backlink_identity_key(
        "site-1", "https://source.example/Article?state=ny", "https://brand.example/"
    )


def test_duplicate_aliases_merge_without_losing_strong_provider_facts() -> None:
    older = BacklinkItem(
        source_url="https://www.publisher.example/article/",
        target_url="http://www.brand.example/service/",
        source_rank=Decimal("314"),
        domain_rank=Decimal("298"),
        anchor_text="Brand service",
        extras={"older": True, "shared": "older"},
    )
    newer = BacklinkItem(
        source_url="https://publisher.example/article",
        target_url="https://brand.example/service",
        source_rank=Decimal("0"),
        domain_rank=Decimal("301"),
        extras={"newer": True, "shared": "newer"},
    )

    merged = subject._merge_duplicate_backlink_items([older, newer])

    assert merged.source_rank == Decimal("314")
    assert merged.domain_rank == Decimal("301")
    assert merged.anchor_text == "Brand service"
    assert merged.extras["shared"] == "newer"
    assert len(merged.extras["provider_url_variants"]) == 2


def test_provider_only_assessment_prioritizes_broken_targets_without_overclaiming() -> None:
    assessment = deterministic_assessment(
        BacklinkItem(
            source_url="https://publisher.example/useful-links",
            source_domain="publisher.example",
            target_url="https://brand.example/retired",
            anchor_text="Brand research",
            is_dofollow=True,
            source_rank=Decimal("71"),
            domain_rank=Decimal("84"),
            spam_score=Decimal("2"),
            extras={
                "semantic_location": "article",
                "is_broken": True,
                "url_to_status_code": 404,
                "text_pre": "See the independent study from",
            },
        )
    )

    assert assessment.provider_only is True
    assert assessment.recommended_action == "fix_or_redirect_target"
    assert assessment.priority == "high"
    assert "broken_target" in assessment.risks
    assert assessment.quality_vector["capture_quality"] == 20
    assert 0 <= assessment.overall_score <= 100


def test_directory_pattern_becomes_a_claim_or_improve_opportunity() -> None:
    assessment = deterministic_assessment(
        BacklinkItem(
            source_url="https://directory.example/listings/brand",
            target_url="https://brand.example/",
            anchor_text="Brand",
            extras={"page_from_title": "Local business directory listing"},
        )
    )

    assert assessment.page_type_guess == "directory"
    assert assessment.control_likelihood == "possible"
    assert assessment.recommended_action == "claim_or_improve_listing"
    assert "listing_enrichment" in assessment.opportunities


@pytest.mark.asyncio
async def test_target_urls_resolve_to_canonical_web_page_ids(monkeypatch) -> None:
    items = [
        BacklinkItem(
            source_url="https://publisher.example/article",
            target_url="http://www.brand.example/service/?b=2&a=1#section",
        ),
        BacklinkItem(
            source_url="https://publisher.example/other",
            target_url="https://brand.example/not-managed",
        ),
    ]

    class Query:
        async def values(self, *fields: str):
            assert fields == ("id", "url")
            return [
                {
                    "id": "page-service-www",
                    "url": "https://www.brand.example/service?b=2&a=1",
                },
                {
                    "id": "page-service",
                    "url": "https://brand.example/service?a=1&b=2",
                },
                {"id": "page-home", "url": "https://brand.example/"},
            ]

    monkeypatch.setattr(subject.WebPage, "filter", lambda **kwargs: Query())

    resolved = await subject.resolve_backlink_target_page_ids("site-1", items)

    assert resolved == {
        backlink_identity_key(
            "site-1",
            "https://publisher.example/article",
            "http://www.brand.example/service/?b=2&a=1#section",
        ): "page-service"
    }


@pytest.mark.asyncio
async def test_site_wide_upsert_persists_resolved_target_page_id(monkeypatch) -> None:
    item = BacklinkItem(
        source_url="https://publisher.example/article",
        source_domain="publisher.example",
        target_url="https://brand.example/service",
    )
    identity_key = backlink_identity_key("site-1", item.source_url, item.target_url)
    link_rows: list[dict] = []

    async def resolve(_site_id: str, _items: list[BacklinkItem]):
        return {identity_key: "page-service"}

    async def upsert(model, rows, **_kwargs):
        if model is subject.m.ReferringDomainProfile:
            return [{"id": "profile-1", "normalized_domain": "publisher.example"}]
        link_rows.extend(rows)
        return [{"id": "backlink-1", "identity_key": identity_key}]

    monkeypatch.setattr(subject, "resolve_backlink_target_page_ids", resolve)
    monkeypatch.setattr(subject, "bulk_upsert_increment", upsert)

    await subject.upsert_current_backlinks(
        organization_id="org-1",
        created_by="user-1",
        site_id="site-1",
        page_id=None,
        provider="provider",
        snapshot_id="snapshot-1",
        items=[item],
    )

    assert link_rows[0]["page_id"] == "page-service"


@pytest.mark.asyncio
async def test_expired_claims_return_to_queue_or_dead_letter(monkeypatch) -> None:
    rows = [
        SimpleNamespace(id="retry", enrichment_attempt_count=2),
        SimpleNamespace(id="exhausted", enrichment_attempt_count=4),
    ]
    updates: list[tuple[dict, dict]] = []

    class Query:
        def order_by(self, *_args):
            return self

        def limit(self, _limit: int):
            return self

        async def all(self, *, use_cache: bool):
            assert use_cache is False
            return rows

    async def update_where(where: dict, **values):
        updates.append((where, values))
        return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(subject.m.Backlink, "filter", lambda **_kwargs: Query())
    monkeypatch.setattr(subject.m.Backlink, "update_where", update_where)

    recovered = await subject.reclaim_expired_enrichment_claims("site-1")

    assert recovered == 2
    assert updates[0][1]["enrichment_status"] == "failed"
    assert updates[0][1]["next_enrichment_at"] is not None
    assert updates[1][1]["enrichment_status"] == "dead_letter"
    assert updates[1][1]["next_enrichment_at"] is None
    assert all(update[1]["claimed_by"] is None for update in updates)


@pytest.mark.asyncio
async def test_candidates_prioritize_new_links_then_due_completed_reviews(monkeypatch) -> None:
    fresh = [SimpleNamespace(id="fresh-1"), SimpleNamespace(id="fresh-2")]
    due = [SimpleNamespace(id="completed-review")]
    filters: list[dict] = []

    class Query:
        def __init__(self, rows: list[SimpleNamespace]) -> None:
            self.rows = rows

        def order_by(self, *_args):
            return self

        def limit(self, limit: int):
            self.rows = self.rows[:limit]
            return self

        async def all(self, *, use_cache: bool):
            assert use_cache is False
            return self.rows

    def filter_rows(**kwargs):
        filters.append(kwargs)
        return Query(fresh if kwargs.get("next_enrichment_at__isnull") else due)

    async def no_stale(_site_id: str, *, limit: int = 100) -> int:
        return 0

    monkeypatch.setattr(subject, "reclaim_expired_enrichment_claims", no_stale)
    monkeypatch.setattr(subject.m.Backlink, "filter", filter_rows)

    rows = await subject.list_enrichment_candidates("site-1", limit=3)

    assert [row.id for row in rows] == ["fresh-1", "fresh-2", "completed-review"]
    assert filters[1]["enrichment_status__in"] == ["pending", "failed", "completed"]


@pytest.mark.asyncio
async def test_targeted_candidates_preserve_request_order_and_can_force_dead_letter(
    monkeypatch,
) -> None:
    rows = [SimpleNamespace(id="dead"), SimpleNamespace(id="complete")]
    captured_filters: list[dict] = []

    class Query:
        async def all(self, *, use_cache: bool):
            assert use_cache is False
            return rows

    def filter_rows(**kwargs):
        captured_filters.append(kwargs)
        return Query()

    async def no_stale(_site_id: str, *, limit: int = 100) -> int:
        return 0

    monkeypatch.setattr(subject, "reclaim_expired_enrichment_claims", no_stale)
    monkeypatch.setattr(subject.m.Backlink, "filter", filter_rows)

    result = await subject.list_enrichment_candidates(
        "site-1",
        limit=2,
        force=True,
        backlink_ids=["complete", "dead"],
    )

    assert [row.id for row in result] == ["complete", "dead"]
    assert captured_filters[0]["id__in"] == ["complete", "dead"]
    assert captured_filters[0]["enrichment_status__in"] == [
        "pending",
        "failed",
        "completed",
        "dead_letter",
    ]
