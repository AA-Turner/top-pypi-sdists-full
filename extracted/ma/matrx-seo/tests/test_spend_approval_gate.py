"""The spend-approval gate in the ONE collection funnel (OPENSEO-TOOLS-SPEC §6.1, T9a/T9e).

What these prove, each against the real ``SeoCollectionService.collect``:

* the approval is checked AFTER the reuse lookup and BEFORE ``start_run`` — a
  refusal leaves no ``collection_run`` row and makes no provider call (T9a);
* a request served by reuse never touches an approval, and the same request
  under two different approvals is a reuse hit the second time (T9e) — the
  approval id rides outside ``settings`` and outside every hash;
* the choke point re-checks headroom (a concurrent run may have drawn it) and a
  successful run draws its cost on the approval;
* a standalone install (no resolver) and an adapter with no price book both
  REFUSE an approval id — never treat it as approved.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from matrx_seo import (
    CollectionRequest,
    CollectionTrigger,
    FakeRankProvider,
    InMemorySeoRepository,
    SeoCapability,
    SeoCollectionService,
    configure,
    fake_collection_authorizer,
    fake_credential_resolver,
)
from matrx_seo.adapters import SeoProviderOperation
from matrx_seo.budget import (
    SpendApprovalExceededError,
    SpendApprovalResolver,
    SpendApprovalState,
    set_spend_approval_resolver,
)

configure(collection_authorizer=fake_collection_authorizer)

PRICE = Decimal("0.02")


class PricedProvider(FakeRankProvider):
    """A fake paid provider WITH a price book, and a reuse window."""

    def __init__(self, repository, *, calls: list[str]) -> None:
        super().__init__(repository, provider="dataforseo")
        self.operations = (
            SeoProviderOperation(
                name="serp.rank.live",
                capability=SeoCapability.SERP_RANK,
                credential_keys=(),
                freshness_ttl_seconds=86_400,
            ),
        )
        self._calls = calls

    def estimate_cost_usd(self, request: CollectionRequest) -> Decimal | None:
        return PRICE

    async def collect_response(self, request, execution):
        self._calls.append("provider_call")
        return await super().collect_response(request, execution)


class RecordingResolver(SpendApprovalResolver):
    def __init__(self, states: dict[str, list[SpendApprovalState]], calls: list[str]) -> None:
        self._states = states
        self._calls = calls
        self.charges: list[tuple[str, Decimal, str]] = []

    async def read(self, approval_id, request):
        self._calls.append(f"approval_read:{approval_id}")
        queue = self._states.get(approval_id) or []
        if not queue:
            return None
        return queue.pop(0) if len(queue) > 1 else queue[0]

    async def charge(self, approval_id, amount_usd, *, run_id):
        self._calls.append(f"approval_charge:{approval_id}")
        self.charges.append((approval_id, amount_usd, run_id))


class RecordingRepository(InMemorySeoRepository):
    def __init__(self, calls: list[str]) -> None:
        super().__init__()
        self._calls = calls

    async def find_fresh_completed(self, provider, request, freshness_ttl_seconds):
        self._calls.append("find_fresh_completed")
        return await super().find_fresh_completed(provider, request, freshness_ttl_seconds)

    async def start_run(self, provider, request):
        self._calls.append("start_run")
        return await super().start_run(provider, request)


def _state(approval_id: str, *, ceiling: str, spent: str = "0", status: str = "open"):
    return SpendApprovalState(
        approval_id=approval_id,
        status=status,
        ceiling_usd=Decimal(ceiling),
        spent_usd=Decimal(spent),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
        tool="seo_keywords",
        action="research",
    )


def _request(approval: str | None) -> CollectionRequest:
    return CollectionRequest(
        organization_id="org-1",
        created_by="user-1",
        capability=SeoCapability.SERP_RANK,
        operation="serp.rank.live",
        target_ref="target-1",
        observation_period="2026-09-27",
        trigger=CollectionTrigger.TEST,
        settings={
            "keyword_id": "keyword-1",
            "rank_target_id": "target-1",
            "engine": "google",
            "locale": "US",
            "target_domain": "example.com",
        },
        spend_approval_id=UUID(approval) if approval else None,
        spend_tool="seo_keywords" if approval else None,
        spend_action="research" if approval else None,
    )


@pytest.fixture(autouse=True)
def _no_resolver_leak():
    yield
    set_spend_approval_resolver(None)


@pytest.mark.asyncio
async def test_a_refused_approval_leaves_no_run_and_makes_no_provider_call() -> None:
    calls: list[str] = []
    approval = str(uuid4())
    set_spend_approval_resolver(
        RecordingResolver({approval: [_state(approval, ceiling="0.01")]}, calls)
    )
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError) as refused:
        await service.collect(PricedProvider(repository, calls=calls), _request(approval))

    # After the reuse lookup, before start_run — and nothing after it.
    assert calls == ["find_fresh_completed", f"approval_read:{approval}"]
    assert repository.runs == {}
    assert refused.value.recovery == {
        "handle_type": "spend_approval",
        "handle": approval,
        "resume_cost": "paid",
        "new_estimate_usd": "0.02",
    }


@pytest.mark.asyncio
async def test_approval_is_checked_after_the_reuse_lookup_and_before_start_run() -> None:
    calls: list[str] = []
    approval = str(uuid4())
    resolver = RecordingResolver({approval: [_state(approval, ceiling="1.00")]}, calls)
    set_spend_approval_resolver(resolver)
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    receipt = await service.collect(PricedProvider(repository, calls=calls), _request(approval))

    assert calls.index("find_fresh_completed") < calls.index(f"approval_read:{approval}")
    assert calls.index(f"approval_read:{approval}") < calls.index("start_run")
    assert calls.index("start_run") < calls.index("provider_call")
    # The run's cost (no reported cost → the price book) is drawn on the approval.
    assert resolver.charges == [(approval, PRICE, receipt.run_id)]


@pytest.mark.asyncio
async def test_same_request_under_two_approvals_is_a_reuse_hit_that_touches_neither() -> None:
    calls: list[str] = []
    first, second = str(uuid4()), str(uuid4())
    resolver = RecordingResolver(
        {first: [_state(first, ceiling="1.00")], second: [_state(second, ceiling="1.00")]},
        calls,
    )
    set_spend_approval_resolver(resolver)
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = PricedProvider(repository, calls=calls)

    original = await service.collect(provider, _request(first))
    calls.clear()
    reused = await service.collect(provider, _request(second))

    assert reused.from_cache is True
    assert reused.run_id == original.run_id
    # A reuse hit never reads, checks or draws on the second approval.
    assert calls == ["find_fresh_completed"]
    assert [charge[0] for charge in resolver.charges] == [first]


@pytest.mark.asyncio
async def test_fresh_run_for_is_a_read_that_matches_collect() -> None:
    calls: list[str] = []
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = PricedProvider(repository, calls=calls)

    assert await service.fresh_run_for(provider, _request(None)) is None
    assert "start_run" not in calls and repository.runs == {}
    done = await service.collect(provider, _request(None))
    twin = await service.fresh_run_for(provider, _request(None))
    assert twin is not None and twin.run_id == done.run_id


@pytest.mark.asyncio
async def test_the_choke_point_rechecks_headroom_a_concurrent_run_drew_down() -> None:
    calls: list[str] = []
    approval = str(uuid4())
    set_spend_approval_resolver(
        RecordingResolver(
            {
                approval: [
                    _state(approval, ceiling="0.05", spent="0.00"),  # pre-flight: fits
                    _state(approval, ceiling="0.05", spent="0.04"),  # choke point: drawn down
                ]
            },
            calls,
        )
    )
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError):
        await service.collect(PricedProvider(repository, calls=calls), _request(approval))

    assert "provider_call" not in calls
    (run,) = repository.runs.values()
    assert run["status"] == "failed"


@pytest.mark.asyncio
async def test_standalone_install_refuses_an_approval_id() -> None:
    calls: list[str] = []
    set_spend_approval_resolver(None)
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError, match="no spend-approval resolver"):
        await service.collect(PricedProvider(repository, calls=calls), _request(str(uuid4())))
    assert repository.runs == {}


@pytest.mark.asyncio
async def test_an_adapter_without_a_price_book_refuses_an_approval_id() -> None:
    calls: list[str] = []
    approval = str(uuid4())
    set_spend_approval_resolver(
        RecordingResolver({approval: [_state(approval, ceiling="1.00")]}, calls)
    )
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    unpriced = FakeRankProvider(repository, provider="dataforseo")

    with pytest.raises(SpendApprovalExceededError, match="no price book"):
        await service.collect(unpriced, _request(approval))
    assert repository.runs == {}


def test_the_approval_id_is_not_part_of_settings_or_any_hash() -> None:
    from matrx_seo.identity import stable_hash

    a = _request(str(uuid4()))
    b = _request(str(uuid4()))
    assert "spend_approval_id" not in a.settings
    assert stable_hash(a.settings) == stable_hash(b.settings)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("capability", "platform.points", "not provider spend"),
        ("site_id", "site-other", "different site"),
        ("approved_by", "user-other", "different person"),
    ],
)
async def test_an_approval_funds_only_what_it_was_minted_for(field, value, reason) -> None:
    """D2: a collection can only draw an approval minted for provider money, for its
    site, by the person whose collection it is — never merely one of its org's."""
    from dataclasses import replace

    calls: list[str] = []
    approval = str(uuid4())
    state = replace(_state(approval, ceiling="1.00"), **{field: value})
    set_spend_approval_resolver(RecordingResolver({approval: [state]}, calls))
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError, match=reason):
        await service.collect(PricedProvider(repository, calls=calls), _request(approval))
    assert repository.runs == {}
    assert "provider_call" not in calls


@pytest.mark.asyncio
async def test_an_approval_minted_for_this_site_and_person_funds_it() -> None:
    from dataclasses import replace

    calls: list[str] = []
    approval = str(uuid4())
    state = replace(_state(approval, ceiling="1.00"), approved_by="user-1", site_id=None)
    set_spend_approval_resolver(RecordingResolver({approval: [state]}, calls))
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    await service.collect(PricedProvider(repository, calls=calls), _request(approval))
    assert "provider_call" in calls


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("request_update", "state_update", "reason"),
    [
        ({"spend_tool": "seo_domain"}, {}, "not seo_domain.research"),
        ({"spend_action": "metrics"}, {}, "not seo_keywords.metrics"),
        ({"spend_tool": None, "spend_action": None}, {}, "not None.None"),
        ({}, {"tool": None, "action": None}, "names no job"),
        ({"site_id": "site-1"}, {"site_id": None}, "different site"),
        ({}, {"site_id": "site-1"}, "different site"),
    ],
)
async def test_an_approval_funds_only_the_job_the_person_approved(
    request_update, state_update, reason
) -> None:
    """Ruling on D2: bound to the tool + action that asked; a site-less approval
    funds only a site-less call."""
    from dataclasses import replace

    calls: list[str] = []
    approval = str(uuid4())
    state = replace(_state(approval, ceiling="1.00"), **state_update)
    set_spend_approval_resolver(RecordingResolver({approval: [state]}, calls))
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError, match=reason):
        await service.collect(
            PricedProvider(repository, calls=calls),
            _request(approval).model_copy(update=request_update),
        )
    assert repository.runs == {}
    assert "provider_call" not in calls


def test_the_job_rides_outside_settings_and_every_hash() -> None:
    from matrx_seo.identity import stable_hash

    a = _request(str(uuid4()))
    b = a.model_copy(update={"spend_tool": "seo_local", "spend_action": "rank_grid"})
    assert "spend_tool" not in a.settings
    assert stable_hash(a.settings) == stable_hash(b.settings)


@pytest.mark.asyncio
async def test_an_unknown_approval_says_so_and_names_no_recovery_handle() -> None:
    """Verification F: a bogus id read '$0 of $0 used' with a '(paid)' recovery
    handle naming the bogus id. It must say plainly there is no such usable
    approval, point at a NEW approval, and hand back no handle."""
    calls: list[str] = []
    bogus = str(uuid4())
    set_spend_approval_resolver(RecordingResolver({}, calls))
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError) as refused:
        await service.collect(PricedProvider(repository, calls=calls), _request(bogus))

    exc = refused.value
    assert exc.recovery is None
    assert exc.usable_approval is False
    assert "no such approval exists" in str(exc)
    assert "$0" not in exc.error_info.user_message
    assert "approve a new amount" in exc.error_info.user_message
    assert "WITHOUT spend_approval_id" in exc.next_step
    assert repository.runs == {}


@pytest.mark.asyncio
async def test_an_expired_approval_is_unusable_not_short() -> None:
    from dataclasses import replace

    calls: list[str] = []
    approval = str(uuid4())
    state = replace(
        _state(approval, ceiling="1.00"), expires_at=datetime.now(UTC) - timedelta(minutes=1)
    )
    set_spend_approval_resolver(RecordingResolver({approval: [state]}, calls))
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError, match="has expired") as refused:
        await service.collect(PricedProvider(repository, calls=calls), _request(approval))
    assert refused.value.recovery is None


@pytest.mark.asyncio
async def test_a_short_approval_keeps_its_recovery_handle() -> None:
    calls: list[str] = []
    approval = str(uuid4())
    set_spend_approval_resolver(
        RecordingResolver({approval: [_state(approval, ceiling="0.01")]}, calls)
    )
    repository = RecordingRepository(calls)
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)

    with pytest.raises(SpendApprovalExceededError) as refused:
        await service.collect(PricedProvider(repository, calls=calls), _request(approval))
    assert refused.value.usable_approval is True
    assert refused.value.recovery["handle"] == approval
