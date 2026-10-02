"""OpenSEO Wave 1 core: the DataForSEO registration points every lane builds on.

Pins, against the adapter as it is constructed everywhere (no arguments):

* SERP prospecting keeps working — a prospect-tagged organic payload still
  normalizes to prospect observations through the registered ``serp_organic``
  normalizer, and an untagged one names its owner (Lane B) instead;
* the Labs keyword normalizer is registered for every Labs keyword operation
  (its behavior is pinned in ``test_labs_keywords_normalizer.py``);
* ``llm_mentions`` operations are raw provider evidence and can never reach
  the answer normalizer, even though they share the ``ai_optimization.`` family;
* the price book refuses an operation it cannot price, rounds each metered call
  on its own, and knows the new operations.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from matrx_seo.contracts import (
    CollectionRequest,
    NormalizationContext,
    ProviderResponse,
    ResolvedCredential,
    SeoCapability,
)
from matrx_seo.providers.dataforseo import DataForSeoAdapter
from matrx_seo.providers.dataforseo.serp_prospect import (
    SERP_ORGANIC_OPERATION,
    encode_prospect_tag,
    normalize_serp_prospect_payload,
)
from matrx_seo.providers.dataforseo.transport import ReplayTransport
from matrx_seo.repository import InMemorySeoRepository
from matrx_seo.service import SeoCollectionService

FETCHED_AT = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)


def _request(operation: str, capability: SeoCapability, **update: object) -> CollectionRequest:
    return CollectionRequest(
        organization_id=str(uuid4()),
        created_by=str(uuid4()),
        capability=capability,
        operation=operation,
        target_ref="openseo-core",
        observation_period="2026-09-27",
        execution_id=uuid4(),
    ).model_copy(update=update)


async def _context(request: CollectionRequest) -> NormalizationContext:
    run = await InMemorySeoRepository().start_run("dataforseo", request)
    return NormalizationContext(
        request=request,
        run=run,
        raw_payload_id="raw-id",
        identity_resolver=object(),
        host_binding_resolver=object(),
    )


def _serp_payload(*, tagged: bool) -> dict:
    data = {"keyword": "dental implants"}
    if tagged:
        data["tag"] = encode_prospect_tag(
            variant="keyword", seed_keyword="dental implants", exclude_domain="mysite.com"
        )
    return {
        "version": "3",
        "status_code": 20000,
        "tasks": [
            {
                "id": "task-0",
                "status_code": 20000,
                "data": data,
                "result": [
                    {
                        "items": [
                            {
                                "type": "organic",
                                "rank_absolute": 3,
                                "rank_group": 2,
                                "url": "https://blog-a.com/post",
                                "domain": "blog-a.com",
                                "title": "blog-a",
                                "description": "snippet",
                            }
                        ]
                    }
                ],
            }
        ],
    }


def _live_envelope(task: dict, result: list) -> dict:
    return {
        "version": "3.0",
        "status_code": 20000,
        "status_message": "Ok.",
        "cost": "0.101",
        "tasks_count": 1,
        "tasks_error": 0,
        "tasks": [
            {
                "id": "mentions-task",
                "status_code": 20000,
                "status_message": "Ok.",
                "cost": "0.101",
                "result_count": 1,
                "path": ["v3", "ai_optimization", "llm_mentions", "search", "live"],
                "data": task,
                "result": result,
            }
        ],
    }


async def _credential(*_: object) -> ResolvedCredential:
    return ResolvedCredential(
        values={
            "DATA_FOR_SEO_EMAIL": "fixture@example.invalid",
            "DATA_FOR_SEO_PASSWORD": "fixture",
        }
    )


async def _authorize(request: CollectionRequest) -> CollectionRequest:
    return request


# --- SERP organic: prospecting still works; untagged names Lane B ----------


@pytest.mark.asyncio
async def test_prospect_tagged_organic_payload_still_normalizes_as_prospects() -> None:
    from matrx_seo.providers.dataforseo.serp_organic import normalize_serp_organic

    adapter = DataForSeoAdapter()
    assert adapter._normalizers[SERP_ORGANIC_OPERATION] is normalize_serp_organic
    request = _request(SERP_ORGANIC_OPERATION, SeoCapability.SERP_RANK, site_id="site-1")
    assert adapter.unsupported_request_reason(request) is None
    raw = _serp_payload(tagged=True)
    observations = await adapter.normalize(
        ProviderResponse(raw=raw, fetched_at=FETCHED_AT), await _context(request)
    )
    expected = list(
        normalize_serp_prospect_payload(raw=raw, site_id="site-1", fetched_at=FETCHED_AT)
    )
    assert observations and observations == expected
    assert {observation.kind for observation in observations} == {
        observation.kind for observation in expected
    }

    # The site_id requirement travels with the route, exactly as before.
    no_site = _request(SERP_ORGANIC_OPERATION, SeoCapability.SERP_RANK)
    with pytest.raises(ValueError, match="must carry site_id"):
        await adapter.normalize(
            ProviderResponse(raw=raw, fetched_at=FETCHED_AT), await _context(no_site)
        )


@pytest.mark.asyncio
async def test_untagged_organic_payload_is_a_rank_snapshot_never_prospects() -> None:
    """Lane B filled the untagged branch (tests/test_serp_organic_rank_snapshot.py
    pins its counting): an untagged payload is a rank snapshot, never prospects."""
    from matrx_seo.contracts import ResolvedSeoIdentity

    class _Identity:
        async def resolve(self, request, identity):
            return ResolvedSeoIdentity(keyword_id="kw-1")

    adapter = DataForSeoAdapter()
    request = _request(SERP_ORGANIC_OPERATION, SeoCapability.SERP_RANK, site_id="site-1")
    context = (await _context(request)).model_copy(update={"identity_resolver": _Identity()})
    observations = await adapter.normalize(
        ProviderResponse(raw=_serp_payload(tagged=False), fetched_at=FETCHED_AT), context
    )
    assert [o.kind for o in observations] == ["serp_snapshot"]
    assert observations[0].results[0].organic_rank == 1


# --- Labs keywords --------------------------------------------------------
# Lane A filled the registered normalizer and removed its ``pending_owner``; the
# gate is open and the operations run through the funnel. Pinned in
# ``test_labs_keywords_normalizer.py`` against real provider payloads.


# --- llm_mentions: raw evidence, never the answer normalizer ---------------


@pytest.mark.asyncio
async def test_llm_mentions_collects_as_raw_and_never_reaches_answer_normalizer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.providers.dataforseo import ai_answers

    async def explode(*_: object, **__: object) -> list:
        raise AssertionError("normalize_ai_answer_response must never see llm_mentions")

    monkeypatch.setattr(ai_answers, "normalize_ai_answer_response", explode)

    task = {
        "target": [{"domain": "dataforseo.com"}],
        "platform": "google",
        "location_code": 2840,
        "language_code": "en",
        "limit": 1,
    }
    transport = ReplayTransport(
        [_live_envelope(task, [{"total_count": 1, "items_count": 1, "items": [{"question": "q"}]}])]
    )
    adapter = DataForSeoAdapter(transport=transport)
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository, credential_resolver=_credential, collection_authorizer=_authorize
    )
    request = _request(
        "ai_optimization.llm_mentions.search",
        SeoCapability.RAW_PROVIDER,
        settings={"workflow": "live", "tasks": [task]},
    )
    receipt = await service.collect(adapter, request)
    assert [run["status"] for run in repository.runs.values() if run["id"] == receipt.run_id] == [
        "completed"
    ]
    assert [path for _, path, _ in transport.requests] == [
        "/v3/ai_optimization/llm_mentions/search/live"
    ]

    # Even a (hypothetical) non-raw normalize call on a mentions operation must
    # not be routed to the answer normalizer: the branch is by name, not prefix.
    for operation in (
        "ai_optimization.llm_mentions.search",
        "ai_optimization.llm_mentions.aggregated_metrics",
        "ai_optimization.llm_mentions.cross_aggregated_metrics",
        "ai_optimization.llm_mentions.top_pages",
    ):
        observations = await adapter.normalize(
            ProviderResponse(raw=_live_envelope(task, []), fetched_at=FETCHED_AT),
            await _context(_request(operation, SeoCapability.SERP_RANK)),
        )
        assert observations == []


# --- Price book ------------------------------------------------------------


def test_unpriced_operation_refuses_an_estimate(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_seo.providers.dataforseo import pricing

    with pytest.raises(
        pricing.UnpricedOperationError, match="no price for .*add it to the price book"
    ):
        pricing.estimate("labs.google.not_an_operation", {"tasks": [{}]})

    # A registered operation whose pricing key has no entry refuses too — never zero.
    monkeypatch.delitem(pricing.PRICE_BOOK, "business_profile")
    with pytest.raises(
        pricing.UnpricedOperationError,
        match=r"^no price for business_data\.google\.my_business_info; add it to the price book$",
    ):
        DataForSeoAdapter().estimate_cost_usd(
            _request(
                "business_data.google.my_business_info",
                SeoCapability.RAW_PROVIDER,
                settings={"workflow": "live", "tasks": [{"keyword": "x"}]},
            )
        )


def test_each_metered_call_is_rounded_before_summing(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_seo.providers.dataforseo import pricing

    # A price below the billing quantum: each call rounds UP on its own, so two
    # calls cost two quanta; summing first would round 0.0000008 up to one.
    monkeypatch.setitem(pricing.PRICE_BOOK, "serp_10_result", lambda *_: Decimal("0.0000004"))
    two_tasks = {
        "workflow": "standard",
        "tasks": [{"keyword": "a", "location_code": 2840}, {"keyword": "b", "location_code": 2840}],
    }
    assert pricing.estimate(SERP_ORGANIC_OPERATION, two_tasks) == Decimal("0.000002")


def test_price_book_seeds() -> None:
    from matrx_seo.providers.dataforseo.pricing import estimate

    def live(task: dict) -> dict:
        return {"workflow": "live", "tasks": [task]}

    # SERP live: $0.002 + $0.0015 per further 10 of depth.
    assert estimate(SERP_ORGANIC_OPERATION, live({"keyword": "a", "depth": 10})) == Decimal("0.002")
    assert estimate(SERP_ORGANIC_OPERATION, live({"keyword": "a", "depth": 30})) == Decimal("0.005")
    # Labs: $0.012 per task + $0.00012 per requested row (this account's 1.2x of list).
    assert estimate(
        "labs.google.keyword_ideas", live({"keywords": ["a"], "limit": 150})
    ) == Decimal("0.03")
    # Google Ads keywords_for_keywords, and the free provider lists.
    assert estimate(
        "keywords.google_ads.keywords_for_keywords", live({"keywords": ["a"]})
    ) == Decimal("0.09")
    assert estimate("labs.locations_and_languages", live({})) == Decimal("0")
    assert estimate("business_data.business_listings.categories", live({})) == Decimal("0")
    # Every new Wave 1 operation is priced (none refuses).
    for operation, settings in (
        ("ai_optimization.llm_mentions.search", live({"target": [], "limit": 1})),
        ("ai_optimization.llm_mentions.aggregated_metrics", live({"target": []})),
        ("ai_optimization.llm_mentions.cross_aggregated_metrics", live({"targets": []})),
        ("ai_optimization.llm_mentions.top_pages", live({"target": []})),
        ("business_data.google.questions_and_answers", live({"keyword": "x"})),
        ("business_data.google.reviews", {"workflow": "standard", "tasks": [{"keyword": "x"}]}),
        (
            "business_data.google.extended_reviews",
            {"workflow": "standard", "tasks": [{"keyword": "x"}]},
        ),
        (
            "business_data.google.my_business_updates",
            {"workflow": "standard", "tasks": [{"keyword": "x"}]},
        ),
    ):
        assert estimate(operation, settings) > 0, operation
