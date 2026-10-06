"""Check before buying again (OpenSEO Wave 2 item 2).

Every paid collection consults a reuse window that is a Feature Knob per
operation family (``seo.reuse_hours.<family>``, overridable per organization and
per person), a caller may only NARROW it (``require_fresh_within_seconds``), and
every receipt carries a plain verdict: reused (which run, from when) or bought
fresh, and why.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from matrx_seo import (
    CollectionRequest,
    CollectionTrigger,
    FakeRankProvider,
    InMemorySeoRepository,
    SeoCapability,
    SeoCollectionService,
)
from matrx_seo import knobs
from matrx_seo.adapters import SeoProviderOperation
from matrx_seo.fakes import fake_collection_authorizer
from matrx_seo.fakes import fake_credential_resolver as _credentials
from matrx_seo.reuse import REUSE_FAMILIES, reuse_knob_key


def _request(period: str = "2026-10-05", **update: Any) -> CollectionRequest:
    base = CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SERP_RANK,
        operation="serp.rank.live",
        target_ref="target-1",
        observation_period=period,
        trigger=CollectionTrigger.ON_DEMAND,
        settings={
            "keyword_id": "keyword-1",
            "rank_target_id": "target-1",
            "engine": "google",
            "locale": "US",
            "target_domain": "example.com",
        },
    )
    return base.model_copy(update=update)


def _provider(repository: InMemorySeoRepository, family: str | None = "serp") -> FakeRankProvider:
    provider = FakeRankProvider(repository, provider="dataforseo")
    provider.operations = (
        SeoProviderOperation(
            name="serp.rank.live",
            capability=SeoCapability.SERP_RANK,
            credential_keys=(),
            reuse_family=family,
        ),
    )
    return provider


def _age(repository: InMemorySeoRepository, run_id: str, hours: float) -> datetime:
    when = datetime.now(UTC) - timedelta(hours=hours)
    row = next(row for row in repository.runs.values() if row["id"] == run_id)
    row["completed_at"] = when
    return when


@pytest.fixture
def scoped_hours():
    """A host resolver: per (organization, person) overrides over the platform rows."""
    overrides: dict[tuple[str | None, str | None, str], int] = {}
    seen: list[tuple[str, str, str | None, str | None]] = []

    async def resolve(feature: str, key: str, organization_id: str | None, user_id: str | None):
        seen.append((feature, key, organization_id, user_id))
        for scope in ((organization_id, user_id, key), (organization_id, None, key)):
            if scope in overrides:
                return overrides[scope]
        return await knobs.int_knob(feature, key)

    knobs.set_scoped_knob_resolver(resolve)
    yield overrides, seen
    knobs.set_scoped_knob_resolver(None)


def test_every_family_has_a_registered_knob_and_no_constant_remains() -> None:
    from conftest import SEO_KNOB_VALUES

    import matrx_seo.keyword_plane as keyword_plane
    import matrx_seo.providers.dataforseo.operations as dfs_ops

    for family in REUSE_FAMILIES:
        assert reuse_knob_key(family) in SEO_KNOB_VALUES["seo"], family
    assert not hasattr(dfs_ops, "_freshness_ttl_seconds")
    assert not hasattr(dfs_ops, "_THIRTY_DAYS")
    assert not hasattr(keyword_plane, "VOLUME_REFRESH_TTL_DAYS")


def test_dataforseo_operations_declare_families_not_seconds() -> None:
    from matrx_seo.providers.dataforseo.operations import APPROVED_OPERATIONS, get_operation

    families = {op.name.value: op.provider_operation.reuse_family for op in APPROVED_OPERATIONS}
    assert families["serp.google.organic.advanced"] == "serp"
    assert get_operation("labs.google.keyword_overview").provider_operation.reuse_family == (
        "keyword_metrics"
    )
    assert all(family in REUSE_FAMILIES for family in families.values())
    assert not hasattr(APPROVED_OPERATIONS[0].provider_operation, "freshness_ttl_seconds")


def test_paid_rank_providers_check_before_buying() -> None:
    from matrx_seo.providers.brave import BraveSeoRankAdapter
    from matrx_seo.providers.serpapi import SERPAPI_GOOGLE_RANK_OPERATION

    assert SERPAPI_GOOGLE_RANK_OPERATION.reuse_family == "serp"
    assert BraveSeoRankAdapter.operations[0].reuse_family == "serp"


@pytest.mark.asyncio
async def test_window_is_the_family_knob_for_this_person(scoped_hours) -> None:
    overrides, seen = scoped_hours
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository)

    first = await service.collect(provider, _request())
    _age(repository, first.run_id, hours=3)

    # Platform default for serp is 24 hours: a 3-hour-old run is reused.
    reused = await service.collect(provider, _request())
    assert reused.run_id == first.run_id
    assert reused.reuse is not None and reused.reuse.decision == "reused"
    assert reused.reuse.reused_run_id == first.run_id
    assert reused.reuse.window_hours == 24
    assert ("seo", "reuse_hours.serp", "org-1", "user-1") in seen

    # This person narrows serp reuse to 2 hours: the same run is now too old.
    overrides[("org-1", "user-1", "reuse_hours.serp")] = 2
    fresh = await service.collect(provider, _request())
    assert fresh.run_id != first.run_id
    assert fresh.reuse is not None and fresh.reuse.decision == "bought_fresh"
    assert fresh.reuse.reason == "Bought fresh: nothing within 2 hours."
    assert provider.fetch_count == 2


@pytest.mark.asyncio
async def test_reused_verdict_names_the_run_and_when(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository)

    first = await service.collect(provider, _request())
    assert first.reuse is not None and first.reuse.decision == "bought_fresh"
    assert first.reuse.reason == "Bought fresh: nothing within 24 hours."
    when = _age(repository, first.run_id, hours=5)

    reused = await service.collect(provider, _request())
    verdict = reused.reuse
    assert verdict is not None
    assert verdict.reused_completed_at == when
    assert first.run_id in verdict.reason
    assert when.strftime("%A") in verdict.reason  # "reusing your research from Tuesday"
    assert "5 hours" in verdict.reason


@pytest.mark.asyncio
async def test_require_fresh_within_only_narrows(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository)

    first = await service.collect(provider, _request())
    _age(repository, first.run_id, hours=3)

    # Asking for a WIDER window than the family knob changes nothing.
    wide = await service.fresh_run_for(provider, _request(require_fresh_within_seconds=72 * 3600))
    assert wide is not None and wide.reuse.window_hours == 24
    # The lookup primitive itself narrows.
    assert (
        await repository.find_fresh_completed(
            "dataforseo", _request(), 86_400, require_fresh_within_seconds=3600
        )
        is None
    )
    narrow = await service.collect(provider, _request(require_fresh_within_seconds=3600))
    assert narrow.run_id != first.run_id
    assert narrow.reuse.reason == "Bought fresh: nothing within 1 hour."


@pytest.mark.asyncio
async def test_forced_fresh_says_the_person_asked(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository)
    await service.collect(provider, _request())

    forced = await service.collect(provider, _request(force_refresh=True, request_id="r-1"))
    assert forced.reuse.decision == "bought_fresh"
    assert forced.reuse.reason == "Bought fresh: the person asked for fresh."


@pytest.mark.asyncio
async def test_no_family_means_no_lookup_and_says_so(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository, family=None)
    first = await service.collect(provider, _request("2026-10-04"))
    second = await service.collect(provider, _request("2026-10-05"))
    assert second.run_id != first.run_id
    assert second.reuse.decision == "bought_fresh"
    assert second.reuse.reason == "Bought fresh: this operation keeps no reuse window."


@pytest.mark.asyncio
async def test_scheduled_reading_never_reuses_another_period(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    provider = _provider(repository)
    yesterday = await service.collect(
        provider, _request("2026-10-04", trigger=CollectionTrigger.SCHEDULED)
    )
    _age(repository, yesterday.run_id, hours=20)
    today = await service.collect(
        provider, _request("2026-10-05", trigger=CollectionTrigger.SCHEDULED)
    )
    assert today.run_id != yesterday.run_id
    assert today.reuse.decision == "bought_fresh"


@pytest.mark.asyncio
async def test_missing_family_knob_raises_never_defaults(scoped_hours, monkeypatch) -> None:
    from conftest import SEO_KNOB_VALUES

    monkeypatch.delitem(SEO_KNOB_VALUES["seo"], "reuse_hours.serp")
    knobs.clear_knob_cache()
    repository = InMemorySeoRepository()
    service = SeoCollectionService(
        repository,
        credential_resolver=_credentials,
        collection_authorizer=fake_collection_authorizer,
    )
    with pytest.raises(knobs.KnobNotRegisteredError):
        await service.collect(_provider(repository), _request())


# ── review fixes (2026-10-05): zero windows, races, unbounded re-buys, honest verdicts ──


def _svc(repository: InMemorySeoRepository) -> SeoCollectionService:
    return SeoCollectionService(
        repository, credential_resolver=_credentials, collection_authorizer=fake_collection_authorizer
    )


@pytest.mark.asyncio
async def test_a_zero_hour_knob_always_buys_fresh(scoped_hours) -> None:
    overrides, _ = scoped_hours
    repository = InMemorySeoRepository()
    service, provider = _svc(repository), _provider(repository)
    first = await service.collect(provider, _request())
    overrides[("org-1", "user-1", "reuse_hours.serp")] = 0
    second = await service.collect(provider, _request())  # same period, seconds later
    third = await service.collect(provider, _request())
    assert len({first.run_id, second.run_id, third.run_id}) == 3
    assert provider.fetch_count == 3
    assert second.reuse.reason == "Bought fresh: a fresh check was required."


@pytest.mark.asyncio
async def test_require_fresh_within_zero_always_buys_fresh(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service, provider = _svc(repository), _provider(repository)
    first = await service.collect(provider, _request())
    second = await service.collect(provider, _request(require_fresh_within_seconds=0))
    assert second.run_id != first.run_id
    assert provider.fetch_count == 2


@pytest.mark.asyncio
async def test_any_number_of_rebuys_never_returns_stale_as_reused(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service, provider = _svc(repository), _provider(repository)
    for i in range(12):
        receipt = await service.collect(provider, _request(require_fresh_within_seconds=60))
        assert receipt.reuse.decision == "bought_fresh", i
        for row in repository.runs.values():
            row["completed_at"] = datetime.now(UTC) - timedelta(hours=1)
    assert provider.fetch_count == 12


@pytest.mark.asyncio
async def test_a_run_completed_by_a_racing_request_is_reused_not_bought_again(
    scoped_hours,
) -> None:
    repository = InMemorySeoRepository()
    service, provider = _svc(repository), _provider(repository)
    first = await service.collect(provider, _request())
    _age(repository, first.run_id, hours=30)
    original = repository.find_fresh_completed
    raced: dict[str, str] = {}

    async def racing(*args: Any, **kwargs: Any):
        result = await original(*args, **kwargs)
        if not raced:
            raced["pending"] = "1"
            raced["s"] = (await service.collect(provider, _request())).run_id
        return result

    repository.find_fresh_completed = racing  # type: ignore[method-assign]
    a = await service.collect(provider, _request())
    assert provider.fetch_count == 2
    assert a.run_id == raced["s"]
    assert a.reuse.decision == "reused"


def test_nothing_within_zero_says_a_fresh_check_was_required() -> None:
    from matrx_seo.contracts import ReuseVerdict

    assert ReuseVerdict.nothing_within(0).reason == "Bought fresh: a fresh check was required."


@pytest.mark.asyncio
async def test_a_reclaimed_failed_run_says_it_resumed(scoped_hours) -> None:
    repository = InMemorySeoRepository()
    service, provider = _svc(repository), _provider(repository)
    run = await repository.start_run("dataforseo", _request())
    await repository.fail_run(run, {"type": "Crash", "message": "worker died"})
    receipt = await service.collect(provider, _request())
    assert receipt.run_id == run.id
    assert receipt.reuse.decision == "resumed"
    assert "earlier attempt" in receipt.reuse.reason
