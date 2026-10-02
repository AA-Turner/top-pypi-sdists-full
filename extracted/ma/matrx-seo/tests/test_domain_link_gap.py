"""Site-wide competitor link gap — the seed rule is what these tests defend.

A gap run is a paid call whose whole value is decided by who was in the request.
So the tests that matter are the ones about who gets in, who does not, and what
the user is told when nobody does.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_seo.contracts import CollectionReceipt
from matrx_seo.domain_link_gap import (
    DomainLinkGapOptions,
    DomainLinkGapService,
    NoEligibleCompetitors,
    site_domain_from_root_url,
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
        return CollectionReceipt(run_id="domain-gap-run")


def _competitor(index: int, **overrides: Any) -> SimpleNamespace:
    values: dict[str, Any] = {
        "id": f"competitor-{index}",
        "normalized_domain": f"rival-{index}.example",
        "classification_status": "confirmed",
        "use_for_link_gap": None,
        "entity_role": "business",
        "business_overlap": "direct",
        "market_overlap": "different_market",
        **overrides,
    }
    return SimpleNamespace(**values)


def _wire(monkeypatch, competitors: list[Any], *, root_url: str = "https://ours.example/") -> None:
    from matrx_seo import domain_link_gap as module

    async def load_site(_site_id: str):
        return SimpleNamespace(id="site-1", organization_id="org-1", root_url=root_url)

    monkeypatch.setattr(module.WebSite, "load_by_id_or_none", load_site)
    monkeypatch.setattr(module.m.Competitor, "filter", lambda **_k: _Rows(competitors))


def _options(**overrides: Any) -> DomainLinkGapOptions:
    return DomainLinkGapOptions(
        organization_id="org-1", created_by="user-1", site_id="site-1", **overrides
    )


@pytest.mark.parametrize(
    ("root_url", "expected"),
    [
        ("https://www.ours.example/", "ours.example"),
        ("http://ours.example/some/path?x=1", "ours.example"),
        ("ours.example", "ours.example"),
        ("https://ours.example:8443", "ours.example"),
        ("https://sub.ours.example/", "sub.ours.example"),
    ],
)
def test_site_domain_is_normalized_like_the_stored_gap_domains(
    root_url: str, expected: str
) -> None:
    assert site_domain_from_root_url(root_url) == expected


def test_site_domain_refuses_garbage_rather_than_guessing() -> None:
    with pytest.raises(ValueError, match="no usable domain"):
        site_domain_from_root_url("not-a-domain")


@pytest.mark.asyncio
async def test_only_confirmed_eligible_competitors_seed_a_paid_run(monkeypatch) -> None:
    competitors = [
        _competitor(1),
        _competitor(2, classification_status="proposed"),  # not ruled on
        _competitor(3, entity_role="marketplace"),  # linkers link to WHAT it is
        _competitor(4, business_overlap="none"),  # confirmed, but not our industry
        _competitor(5, entity_role="publisher", use_for_link_gap=True),  # human override
    ]
    _wire(monkeypatch, competitors)
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]

    seeded, excluded = await service.select_competitors(_options())

    assert [row.domain for row in seeded] == ["rival-1.example", "rival-5.example"]
    assert next(r for r in seeded if r.domain == "rival-5.example").explicitly_enabled
    # The confirmed-but-ineligible ones are REPORTED, never silently dropped.
    assert any("rival-3.example" in reason for reason in excluded)
    assert any("rival-4.example" in reason for reason in excluded)
    assert not any("rival-2.example" in reason for reason in excluded)


@pytest.mark.asyncio
async def test_no_competitors_at_all_says_what_to_do(monkeypatch) -> None:
    _wire(monkeypatch, [])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(NoEligibleCompetitors) as caught:
        await service.select_competitors(_options())
    assert caught.value.total == 0
    assert "Add or discover competitors" in str(caught.value)


@pytest.mark.asyncio
async def test_nothing_confirmed_yet_is_the_human_gate_working(monkeypatch) -> None:
    """The live state on 2026-08-15: 84 proposed, 0 confirmed.

    Seeding nothing is CORRECT here. The refusal has to read as "your turn",
    not as a breakage.
    """
    _wire(monkeypatch, [_competitor(i, classification_status="proposed") for i in (1, 2, 3)])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(NoEligibleCompetitors) as caught:
        await service.select_competitors(_options())
    assert caught.value.confirmed == 0
    assert "3 competitors are waiting for your review" in str(caught.value)


@pytest.mark.asyncio
async def test_the_refusal_reads_as_english_for_one_competitor(monkeypatch) -> None:
    """This copy is the whole surface a user sees when nothing can run — a live
    render caught it saying "1 competitors are waiting"."""
    _wire(monkeypatch, [_competitor(1, classification_status="proposed")])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(NoEligibleCompetitors) as caught:
        await service.select_competitors(_options())
    assert "1 competitor is waiting for your review" in str(caught.value)

    _wire(monkeypatch, [_competitor(1, entity_role="marketplace")])
    with pytest.raises(NoEligibleCompetitors) as caught:
        await service.select_competitors(_options())
    assert "Your 1 confirmed competitor is not the kind" in str(caught.value)


@pytest.mark.asyncio
async def test_confirmed_but_all_wrong_kind_explains_the_taxonomy(monkeypatch) -> None:
    _wire(
        monkeypatch,
        [_competitor(1, entity_role="reference"), _competitor(2, entity_role="community")],
    )
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(NoEligibleCompetitors) as caught:
        await service.select_competitors(_options())
    assert caught.value.confirmed == 2
    assert "marketplaces, directories and publishers" in str(caught.value)
    assert "None of your 2 confirmed competitors are" in str(caught.value)


@pytest.mark.asyncio
async def test_request_puts_competitors_in_targets_and_us_in_exclude(monkeypatch) -> None:
    _wire(monkeypatch, [_competitor(1), _competitor(2)], root_url="https://www.ours.example/")
    collection_service = _CollectionService()
    receipt = await DomainLinkGapService(collection_service).collect(  # type: ignore[arg-type]
        _options(limit=500, max_spam_score=20, enrich_authority=False)
    )

    assert receipt.receipt.run_id == "domain-gap-run"
    assert receipt.site_domain == "ours.example"
    [request] = collection_service.requests
    assert request.operation == "backlinks.intersections"
    assert request.target_ref == "web.site:site-1"
    assert request.page_id is None
    assert request.settings["endpoint"] == "/v3/backlinks/domain_intersection/live"
    task = request.settings["tasks"][0]
    # THE INVERSION TRAP: competitors are the targets; we are the exclusion.
    assert task["targets"] == {"1": "rival-1.example", "2": "rival-2.example"}
    assert task["exclude_targets"] == ["ours.example"]
    assert task["limit"] == 500
    # Never the provider's default ordering — it returns link farms first.
    assert task["order_by"] == ["1.rank,desc"]
    assert task["filters"] == [
        ["1.backlinks_spam_score", "<=", 20],
        "or",
        ["2.backlinks_spam_score", "<=", 20],
    ]


@pytest.mark.asyncio
async def test_duplicate_domains_do_not_burn_two_target_slots(monkeypatch) -> None:
    _wire(monkeypatch, [_competitor(1), _competitor(2, normalized_domain="rival-1.example")])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    seeded, _ = await service.select_competitors(_options())
    assert [row.domain for row in seeded] == ["rival-1.example"]


@pytest.mark.asyncio
async def test_over_the_provider_limit_truncates_loudly(monkeypatch) -> None:
    _wire(monkeypatch, [_competitor(i) for i in range(1, 26)])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    seeded, excluded = await service.select_competitors(_options())
    assert len(seeded) == 20
    assert len([r for r in excluded if "over the provider" in r]) == 5


@pytest.mark.asyncio
async def test_explicit_selection_must_belong_to_this_site(monkeypatch) -> None:
    _wire(monkeypatch, [_competitor(1)])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="do not belong to this site"):
        await service.select_competitors(_options(competitor_ids=["competitor-99"]))


class _Query:
    """A `.filter(...).limit(n).all()` chain over a fixed row list."""

    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    def limit(self, count: int) -> _Query:
        return _Query(self.rows[:count])

    async def all(self) -> list[Any]:
        return self.rows


class _GapRow(SimpleNamespace):
    def __init__(self, domain: str) -> None:
        super().__init__(
            normalized_domain=domain,
            metadata={},
            written={},
        )

    async def update(self, **values: Any) -> _GapRow:
        self.written = values
        return self


def _wire_gap_rows(monkeypatch, rows: list[Any]) -> list[dict[str, Any]]:
    """Capture the enrichment filter and hand it a fixed set of gap rows."""
    from matrx_seo import domain_link_gap as module

    seen: list[dict[str, Any]] = []

    def gap_filter(**kwargs: Any) -> _Query:
        seen.append(kwargs)
        return _Query(rows)

    monkeypatch.setattr(module.m.LinkGapDomain, "filter", gap_filter)
    return seen


@pytest.mark.asyncio
async def test_gap_run_measures_own_authority_for_unenriched_domains(monkeypatch) -> None:
    """The round-1 gap: `domain_intersection` returns no own link counts.

    A gap domain therefore sat at `partial` confidence forever. The run now
    calls the SAME bulk pass SERP prospecting uses, so both methods produce one
    score on one scale — and it asks ONLY for rows never measured, because
    re-measuring a domain's own link profile is paid work that a gap re-run
    learns nothing new from.
    """
    from matrx_seo import authority_enrichment as enrichment_module
    from matrx_seo.authority_enrichment import DomainAuthorityMetrics

    _wire(monkeypatch, [_competitor(1)])
    row = _GapRow("rival-linker.example")
    seen_filters = _wire_gap_rows(monkeypatch, [row])

    async def fake_metrics(_self, options: Any, *, progress: Any = None):
        assert options.domains == ["rival-linker.example"]
        return {
            "rival-linker.example": DomainAuthorityMetrics(
                domain="rival-linker.example",
                domain_rank=Decimal(620),
                spam_score=Decimal(3),
                referring_domains=4200,
            )
        }

    monkeypatch.setattr(
        enrichment_module.AuthorityEnrichmentService, "collect_metrics", fake_metrics
    )

    receipt = await DomainLinkGapService(_CollectionService()).collect(  # type: ignore[arg-type]
        _options()
    )

    assert seen_filters == [{"site_id": "site-1", "enriched_at": None}]
    assert receipt.enriched_domains == 1
    assert receipt.unmeasured_domains == 0
    # The three OWN-profile numbers land; `total_backlinks` is NEVER written —
    # on a gap row it counts links sent to the COMPETITORS, and scoring that as
    # authority is the misfeeding trap that put a newspaper below link farms.
    assert row.written["referring_domains"] == 4200
    assert "total_backlinks" not in row.written
    assert row.written["priority_score"] is not None
    assert row.written["metadata"]["matrx_authority"]["confidence"] == "measured"


@pytest.mark.asyncio
async def test_gap_domain_the_provider_cannot_measure_stays_unscored(monkeypatch) -> None:
    """Unmeasured is NULL and COUNTED — never a 0 that sorts like worthlessness."""
    from matrx_seo import authority_enrichment as enrichment_module

    _wire(monkeypatch, [_competitor(1)])
    row = _GapRow("silent.example")
    _wire_gap_rows(monkeypatch, [row])

    async def no_metrics(_self, _options: Any, *, progress: Any = None):
        return {}

    monkeypatch.setattr(enrichment_module.AuthorityEnrichmentService, "collect_metrics", no_metrics)

    receipt = await DomainLinkGapService(_CollectionService()).collect(  # type: ignore[arg-type]
        _options()
    )
    assert (receipt.enriched_domains, receipt.unmeasured_domains) == (0, 1)
    assert row.written == {}


@pytest.mark.asyncio
async def test_enrich_authority_false_spends_nothing_extra(monkeypatch) -> None:
    """The gap pass alone is still a complete, valid run — enrichment is opt-out."""
    from matrx_seo import authority_enrichment as enrichment_module

    _wire(monkeypatch, [_competitor(1)])

    async def explode(_self, _options: Any, *, progress: Any = None):
        raise AssertionError("enrichment must not run when the caller opted out")

    monkeypatch.setattr(enrichment_module.AuthorityEnrichmentService, "collect_metrics", explode)
    receipt = await DomainLinkGapService(_CollectionService()).collect(  # type: ignore[arg-type]
        _options(enrich_authority=False)
    )
    assert receipt.enriched_domains == 0


@pytest.mark.asyncio
async def test_site_from_another_org_is_refused(monkeypatch) -> None:
    _wire(monkeypatch, [_competitor(1)])
    service = DomainLinkGapService(_CollectionService())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="not a site in this organization"):
        await service.collect(
            DomainLinkGapOptions(organization_id="org-other", created_by="user-1", site_id="site-1")
        )
