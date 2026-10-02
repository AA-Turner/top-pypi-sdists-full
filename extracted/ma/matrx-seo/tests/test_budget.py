"""WS-7 spend/quota enforcement tests.

Covers: spend aggregation math (in-memory + live ORM), under-ceiling pass,
over-ceiling reject BEFORE any provider call (with the typed streamed
event), and the four independent ceilings each firing on their own scope.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from matrx_seo import (
    BudgetExceededError,
    CollectionRequest,
    CollectionTrigger,
    FakeRankProvider,
    InMemorySeoRepository,
    SeoCapability,
    SeoCollectionService,
    SpendQuery,
    check_caller_daily_budget,
    check_global_daily_budget,
    check_global_provider_monthly_budget,
    check_org_provider_monthly_budget,
    configure,
    enforce_collection_budget,
    fake_collection_authorizer,
    fake_credential_resolver,
)
from matrx_seo.budget import current_day_bounds, current_month_bounds
from matrx_seo.knobs import usd_knob

configure(collection_authorizer=fake_collection_authorizer)


@pytest.fixture
def knobs(monkeypatch):
    """Supply the ceilings for tests that go through the DEFAULT gate.

    ``enforce_collection_budget`` reads its ceilings from
    ``platform.feature_knob`` and from the host's per-account allowance
    resolver, because a limit on this platform is a row an admin turns and not a
    constant (common-docs/policies/limits-are-knobs-agents-set-them.md). That
    means these tests have to SUPPLY the numbers — there is deliberately no
    module constant left to monkeypatch, and a package-level default would be
    the exact thing the policy bans.

    Yields the dict so a test can move a ceiling and re-run the gate."""
    import matrx_seo.budget as budget

    values = {
        "max_per_request_cost_usd": Decimal("0.25"),
        "unpriced_run_assumed_cost_usd": Decimal("0.01"),
        "org_provider_monthly_ceiling_usd": Decimal("50.00"),
        "global_provider_monthly_ceiling_usd": Decimal("750.00"),
        "caller_daily_ceiling_usd": Decimal("1.00"),
        "global_daily_ceiling_usd": Decimal("50.00"),
    }

    async def _usd_knob(feature: str, key: str) -> Decimal:
        assert feature == budget.KNOB_FEATURE, feature
        return values[key]

    monkeypatch.setattr(budget, "usd_knob", _usd_knob)
    # No host resolver installed: exactly what a standalone matrx-seo install
    # sees, so the org ceiling falls through to the operational knob.
    monkeypatch.setattr(budget, "_account_ceiling_resolver", None)
    return values


def _request(
    period: str, *, organization_id: str = "org-1", created_by: str = "user-1"
) -> CollectionRequest:
    return CollectionRequest(
        organization_id=organization_id,
        created_by=created_by,
        capability=SeoCapability.SERP_RANK,
        operation="serp.rank.live",
        target_ref="target-1",
        observation_period=period,
        trigger=CollectionTrigger.TEST,
        settings={
            "keyword_id": "keyword-1",
            "rank_target_id": "target-1",
            "engine": "google",
            "locale": "US",
            "target_domain": "example.com",
        },
    )


def _seed_completed_run(
    repository: InMemorySeoRepository,
    *,
    key: str,
    organization_id: str,
    provider: str,
    created_by: str,
    reported_cost: Decimal | None,
    estimated_cost: Decimal | None,
    completed_at: datetime,
    status: str = "completed",
    request_count: int = 1,
) -> None:
    """Directly seed a run row — a white-box shortcut matching the
    other package tests' style (e.g. test_dataforseo.py's provider-task
    inspection) rather than running a full paid collection per data point.

    ``started_at`` mirrors ``completed_at`` because spend is windowed on the
    moment a run was CLAIMED, not the moment it finished: a run billed in full
    and then failed never gets a ``completed_at`` at all, and excluding it is
    the defect this file's window test now guards against."""
    repository.runs[key] = {
        "id": str(uuid4()),
        "status": status,
        "execution_id": None,
        "lease_owner": None,
        "lease_expires_at": None,
        "raw_payload_id": None,
        "receipt": None,
        "attempt_count": 1,
        "request_count": request_count,
        "provider_cost": reported_cost,
        "estimated_cost": estimated_cost,
        "provider": provider,
        "request": _request("seed", organization_id=organization_id, created_by=created_by),
        "settings_hash": "seed",
        "started_at": completed_at,
        "completed_at": completed_at if status == "completed" else None,
    }


# --------------------------------------------------------------------------
# spend_summary aggregation math
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_spend_summary_aggregates_reported_and_estimated_separately() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="a",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("1.50"),
        estimated_cost=None,
        completed_at=now,
    )
    _seed_completed_run(
        repository,
        key="b",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=None,
        estimated_cost=Decimal("0.25"),
        completed_at=now,
    )
    # Different org — must NOT count toward org-1's total.
    _seed_completed_run(
        repository,
        key="c",
        organization_id="org-2",
        provider="dataforseo",
        created_by="user-2",
        reported_cost=Decimal("99.00"),
        estimated_cost=None,
        completed_at=now,
    )
    start, end = current_month_bounds(now)
    summary = await repository.spend_summary(
        SpendQuery(
            organization_id="org-1", provider="dataforseo", period_start=start, period_end=end
        )
    )
    assert summary.reported_cost == Decimal("1.50")
    assert summary.estimated_cost == Decimal("0.25")
    assert summary.effective_cost == Decimal(
        "1.75"
    )  # COALESCE(reported, estimated) per row, summed
    assert summary.run_count == 2


@pytest.mark.asyncio
async def test_spend_summary_windows_on_started_at_and_keeps_failed_runs() -> None:
    """A run that reached the provider is spend, whatever its status ends up as.

    This test used to assert the OPPOSITE — that only ``status='completed'``
    runs count. That was the defect: 45 live DataForSEO runs failed after being
    billed, 26 of them carrying a real reported cost, and every one of them was
    invisible to the ceiling that was supposed to stop the next one."""
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="in-window",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("2.00"),
        estimated_cost=None,
        completed_at=now,
    )
    _seed_completed_run(
        repository,
        key="last-month",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("50.00"),
        estimated_cost=None,
        completed_at=now - timedelta(days=40),
    )
    # Billed, then failed. Real money.
    _seed_completed_run(
        repository,
        key="failed-but-billed",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("0.50"),
        estimated_cost=None,
        completed_at=now,
        status="failed",
    )
    # Still in flight. The money is already committed.
    _seed_completed_run(
        repository,
        key="processing",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("0.25"),
        estimated_cost=None,
        completed_at=now,
        status="processing",
    )
    start, end = current_month_bounds(now)
    summary = await repository.spend_summary(
        SpendQuery(
            organization_id="org-1", provider="dataforseo", period_start=start, period_end=end
        )
    )
    assert summary.effective_cost == Decimal("2.75")
    assert summary.run_count == 3
    # Last month is still out of the window — only the STATUS filter went away.
    assert summary.effective_cost < Decimal("50.00")


@pytest.mark.asyncio
async def test_spend_summary_counts_unpriced_runs_instead_of_zeroing_them() -> None:
    """NULL is unmeasured, never zero.

    SerpAPI reports no cost at all. Under the old ``COALESCE(reported,
    estimated, 0)`` its 112 live runs summed to $0.00, so a SerpAPI-only
    organization could never reach any ceiling. A provider that REPORTS 0.00
    (Search Console, PageSpeed, our own crawl) has evidence and stays free."""
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="unpriced",
        organization_id="org-1",
        provider="serpapi",
        created_by="user-1",
        reported_cost=None,
        estimated_cost=None,
        completed_at=now,
    )
    _seed_completed_run(
        repository,
        key="measured-free",
        organization_id="org-1",
        provider="serpapi",
        created_by="user-1",
        reported_cost=Decimal("0.00"),
        estimated_cost=None,
        completed_at=now,
    )
    # Never reached the provider (this is the shape of a budget REJECTION):
    # charging it would make every rejection raise the next projection.
    _seed_completed_run(
        repository,
        key="never-dispatched",
        organization_id="org-1",
        provider="serpapi",
        created_by="user-1",
        reported_cost=None,
        estimated_cost=None,
        completed_at=now,
        status="failed",
        request_count=0,
    )
    start, end = current_month_bounds(now)
    summary = await repository.spend_summary(
        SpendQuery(organization_id="org-1", provider="serpapi", period_start=start, period_end=end)
    )
    assert summary.effective_cost == Decimal("0.00")
    assert summary.unpriced_run_count == 1
    assert summary.has_unmeasured_spend


@pytest.mark.asyncio
async def test_unpriced_runs_are_charged_against_a_ceiling(monkeypatch) -> None:
    """The half that makes the count matter: an unpriced run must MOVE a gate."""
    import matrx_seo.budget as budget

    async def _assumed() -> Decimal:
        return Decimal("0.10")

    monkeypatch.setattr(budget, "unpriced_run_cost_usd", _assumed)

    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    for index in range(9):
        _seed_completed_run(
            repository,
            key=f"unpriced-{index}",
            organization_id="org-1",
            provider="serpapi",
            created_by="user-1",
            reported_cost=None,
            estimated_cost=None,
            completed_at=now,
        )

    with pytest.raises(BudgetExceededError) as excinfo:
        await check_org_provider_monthly_budget(
            repository,
            organization_id="org-1",
            provider="serpapi",
            ceiling_usd=Decimal("1.00"),
            max_request_usd=Decimal("0.20"),
            now=now,
        )
    # 9 unpriced runs x $0.10 = $0.90 measured-as-assumed, + $0.20 head-room.
    assert excinfo.value.spent_usd == Decimal("0.90")
    assert excinfo.value.projected_usd == Decimal("1.10")


# --------------------------------------------------------------------------
# individual ceiling checks
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_org_provider_monthly_budget_passes_under_ceiling() -> None:
    repository = InMemorySeoRepository()
    summary = await check_org_provider_monthly_budget(
        repository,
        organization_id="org-1",
        provider="dataforseo",
        ceiling_usd=Decimal("50.00"),
        max_request_usd=Decimal("5.00"),
    )
    assert summary.effective_cost == Decimal("0")


@pytest.mark.asyncio
async def test_org_provider_monthly_budget_rejects_over_ceiling() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="a",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("48.00"),
        estimated_cost=None,
        completed_at=now,
    )
    with pytest.raises(BudgetExceededError) as excinfo:
        await check_org_provider_monthly_budget(
            repository,
            organization_id="org-1",
            provider="dataforseo",
            ceiling_usd=Decimal("50.00"),
            max_request_usd=Decimal("5.00"),
            now=now,
        )
    exc = excinfo.value
    assert exc.ceiling == "org_provider_monthly"
    assert exc.spent_usd == Decimal("48.00")
    assert exc.limit_usd == Decimal("50.00")
    assert exc.scope == {"organization_id": "org-1", "provider": "dataforseo", "period": "month"}
    # A different organization is completely unaffected.
    summary = await check_org_provider_monthly_budget(
        repository,
        organization_id="org-2",
        provider="dataforseo",
        ceiling_usd=Decimal("50.00"),
        max_request_usd=Decimal("5.00"),
        now=now,
    )
    assert summary.effective_cost == Decimal("0")


@pytest.mark.asyncio
async def test_global_provider_monthly_budget_sums_across_organizations() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="a",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("300.00"),
        estimated_cost=None,
        completed_at=now,
    )
    _seed_completed_run(
        repository,
        key="b",
        organization_id="org-2",
        provider="dataforseo",
        created_by="user-2",
        reported_cost=Decimal("300.00"),
        estimated_cost=None,
        completed_at=now,
    )
    with pytest.raises(BudgetExceededError) as excinfo:
        await check_global_provider_monthly_budget(
            repository,
            provider="dataforseo",
            ceiling_usd=Decimal("500.00"),
            max_request_usd=Decimal("5.00"),
            now=now,
        )
    assert excinfo.value.ceiling == "global_platform_monthly"
    assert excinfo.value.spent_usd == Decimal("600.00")


@pytest.mark.asyncio
async def test_caller_daily_budget_is_per_created_by() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, 10, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="a",
        organization_id="org-1",
        provider="brave",
        created_by="guest-1",
        reported_cost=None,
        estimated_cost=Decimal("0.90"),
        completed_at=now,
    )
    with pytest.raises(BudgetExceededError) as excinfo:
        await check_caller_daily_budget(
            repository,
            created_by="guest-1",
            ceiling_usd=Decimal("1.00"),
            max_request_usd=Decimal("0.20"),
            now=now,
        )
    assert excinfo.value.ceiling == "caller_daily"
    # A different caller on the same day is unaffected.
    summary = await check_caller_daily_budget(
        repository,
        created_by="guest-2",
        ceiling_usd=Decimal("1.00"),
        max_request_usd=Decimal("0.20"),
        now=now,
    )
    assert summary.effective_cost == Decimal("0")
    # Yesterday doesn't count toward today's cap.
    start, end = current_day_bounds(now)
    assert start <= now < end


@pytest.mark.asyncio
async def test_caller_daily_budget_can_count_only_caller_owned_command_runs() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, 10, tzinfo=UTC)
    _seed_completed_run(
        repository,
        key="provider-child",
        organization_id="org-1",
        provider="dataforseo",
        created_by="platform-credential-owner",
        reported_cost=Decimal("0.91"),
        estimated_cost=None,
        completed_at=now,
    )
    _seed_completed_run(
        repository,
        key="caller-command",
        organization_id="org-1",
        provider="aidream",
        created_by="guest-1",
        reported_cost=None,
        estimated_cost=Decimal("0.50"),
        completed_at=now,
    )

    summary = await check_caller_daily_budget(
        repository,
        created_by="guest-1",
        provider="aidream",
        ceiling_usd=Decimal("1.00"),
        max_request_usd=Decimal("0.50"),
        now=now,
    )
    assert summary.effective_cost == Decimal("0.50")

    with pytest.raises(BudgetExceededError):
        await check_caller_daily_budget(
            repository,
            created_by="guest-1",
            provider="aidream",
            ceiling_usd=Decimal("0.99"),
            max_request_usd=Decimal("0.50"),
            now=now,
        )


@pytest.mark.asyncio
async def test_global_daily_budget_sums_every_caller() -> None:
    repository = InMemorySeoRepository()
    now = datetime(2026, 7, 15, 10, tzinfo=UTC)
    for i in range(3):
        _seed_completed_run(
            repository,
            key=f"g{i}",
            organization_id="org-1",
            provider="brave",
            created_by=f"guest-{i}",
            reported_cost=None,
            estimated_cost=Decimal("8.00"),
            completed_at=now,
        )
    with pytest.raises(BudgetExceededError) as excinfo:
        await check_global_daily_budget(
            repository, ceiling_usd=Decimal("25.00"), max_request_usd=Decimal("2.00"), now=now
        )
    assert excinfo.value.ceiling == "global_daily"
    assert excinfo.value.spent_usd == Decimal("24.00")


# --------------------------------------------------------------------------
# integration through SeoCollectionService — the real choke point
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_collect_proceeds_when_under_ceiling(knobs) -> None:
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="dataforseo")
    receipt = await service.collect(provider, _request("2026-07-24-under"))
    assert receipt.created_observations == 1
    assert provider.fetch_count == 1
    assert provider.authenticated is True


@pytest.mark.asyncio
async def test_collect_rejects_over_ceiling_before_any_provider_call(knobs) -> None:
    """The core WS-7 guarantee: a rejection happens BEFORE credential
    resolution or the provider adapter is ever touched, streams a typed
    'budget_rejected' event naming the ceiling, and the run lands
    status='failed' — never a silent skip, never a crash-shaped 500."""
    repository = InMemorySeoRepository()
    service = SeoCollectionService(repository, credential_resolver=fake_credential_resolver)
    provider = FakeRankProvider(repository, provider="dataforseo")

    # REAL current time, not a fixed date. These two tests exercise
    # `enforce_collection_budget` / `collect`, which take no `now` and read
    # the CURRENT calendar month — a hardcoded July seed lands outside the
    # month-to-date window from August 1st onward, so month-to-date spend is
    # 0, nothing is rejected, and the test fails for a reason that has
    # nothing to do with the guard. (It did exactly that on 2026-08-01.)
    # Every other test here injects `now=` and may pin a date; these cannot.
    now = datetime.now(UTC)
    _seed_completed_run(
        repository,
        key="pre-existing-spend",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("49.99"),
        estimated_cost=None,
        completed_at=now,
    )

    events: list[tuple[str, dict]] = []

    async def progress(event: str, payload: dict) -> None:
        events.append((event, payload))

    with pytest.raises(BudgetExceededError) as excinfo:
        await service.collect(provider, _request("2026-07-24-over"), progress=progress)

    # No paid work was ever attempted.
    assert provider.fetch_count == 0
    assert provider.authenticated is False

    names = [event for event, _ in events]
    assert names == ["authorized", "run_claimed", "budget_rejected"]
    rejected_payload = events[-1][1]
    assert rejected_payload["ceiling"] == "org_provider_monthly"
    assert rejected_payload["spent_usd"] == "49.99"

    assert excinfo.value.ceiling == "org_provider_monthly"

    # The run is recorded FAILED (not left stuck "processing" forever) —
    # a future request with the same identity can retry once budget frees up.
    key = collection_identity_for_test(repository, "org-1", "dataforseo")
    assert repository.runs[key]["status"] == "failed"
    assert repository.runs[key]["error"]["type"] == "BudgetExceededError"
    assert repository.runs[key]["error"]["ceiling"] == "org_provider_monthly"
    assert repository.runs[key]["error"] == excinfo.value.as_error_payload()


def collection_identity_for_test(
    repository: InMemorySeoRepository, organization_id: str, provider: str
) -> str:
    for key, row in repository.runs.items():
        if (
            row["provider"] == provider
            and row["request"].organization_id == organization_id
            and row.get("status") == "failed"
        ):
            return key
    raise AssertionError("expected a failed run for this organization/provider")


@pytest.mark.asyncio
async def test_enforce_collection_budget_checks_org_scope_first(knobs) -> None:
    """When BOTH the org and global ceilings would reject, the org-scoped
    (more actionable) ceiling is the one that names itself — global is a
    pure backstop, never masking the tighter, more specific cause."""
    repository = InMemorySeoRepository()
    # Real current time — see the note above; this path takes no `now`.
    now = datetime.now(UTC)
    _seed_completed_run(
        repository,
        key="a",
        organization_id="org-1",
        provider="dataforseo",
        created_by="user-1",
        reported_cost=Decimal("999999.00"),
        estimated_cost=None,
        completed_at=now,
    )
    request = _request("2026-07-24-both", organization_id="org-1")
    with pytest.raises(BudgetExceededError) as excinfo:
        await enforce_collection_budget(repository, request, "dataforseo")
    assert excinfo.value.ceiling == "org_provider_monthly"


# --------------------------------------------------------------------------
# live ORM aggregation — skips cleanly without a DB environment
# --------------------------------------------------------------------------


@pytest.fixture()
def live_user(isolated_host_database: tuple[str, str] | None) -> str:
    if isolated_host_database is None:
        pytest.skip("live DB env unavailable (AGENT_USER_ID / DB registration missing)")
    return isolated_host_database[0]


async def _organization_for(user_id: str) -> str:
    """The organization this live test acts in — READ from the user's own active
    membership row (a durable record). Never a personal-organization resolver
    choosing tenancy for it; no membership is a refusal that names the user.
    """
    from db.models.iam import Memberships

    rows = (
        await Memberships.filter(
            user_id=user_id, status="active", deleted_at__isnull=True
        )
        .limit(1)
        .all()
    )
    if not rows:
        raise RuntimeError(
            f"No active organization membership for user {user_id} — this live test "
            "needs a real organization to act in; it never falls back to a personal one."
        )
    return str(rows[0].organization_id)


@pytest.mark.asyncio
async def test_orm_spend_summary_aggregates_live(live_user: str) -> None:
    """Seeds two bare ``seo.collection_run`` rows directly (no observation
    tables touched — this test is deliberately independent of any provider
    or identity-resolution code path) and proves ``OrmSeoRepository.
    spend_summary`` aggregates them correctly via a real SQL query."""
    from matrx_seo.contracts import SpendQuery as SQ
    from matrx_seo.db import models_seo as m
    from matrx_seo.orm_repository import OrmSeoRepository

    organization_id = await _organization_for(live_user)
    now = datetime.now(UTC)
    provider = f"budget-live-test-{uuid4()}"
    run_ids: list[str] = []
    try:
        for suffix, reported, estimated in (
            ("a", Decimal("1.23"), None),
            ("b", None, Decimal("0.50")),
        ):
            run_id = str(uuid4())
            run_ids.append(run_id)
            await m.CollectionRun.create(
                id=run_id,
                organization_id=organization_id,
                created_by=live_user,
                provider=provider,
                capability=SeoCapability.SERP_RANK.value,
                operation="budget.live.test",
                trigger=CollectionTrigger.TEST.value,
                status="completed",
                target_ref=f"budget-live-{suffix}",
                observation_period="live-budget-test",
                settings={},
                settings_hash=f"budget-live-{suffix}-{uuid4()}",
                idempotency_key=f"budget-live-{suffix}-{uuid4()}",
                requested_at=now,
                started_at=now,
                completed_at=now,
                request_count=1,
                reported_cost=reported,
                estimated_cost=estimated,
                currency="USD",
                created_at=now,
                updated_at=now,
            )
        repository = OrmSeoRepository()
        start, end = current_month_bounds(now)
        summary = await repository.spend_summary(
            SQ(
                organization_id=organization_id,
                provider=provider,
                period_start=start,
                period_end=end,
            )
        )
        assert summary.reported_cost == Decimal("1.23")
        assert summary.estimated_cost == Decimal("0.50")
        assert summary.effective_cost == Decimal("1.73")
        assert summary.run_count == 2
    finally:
        for run_id in run_ids:
            row = await m.CollectionRun.load_by_id_or_none(run_id)
            if row is not None:
                await row.delete()


# --------------------------------------------------------------------------
# limits-are-knobs invariants
# --------------------------------------------------------------------------


def test_no_ceiling_constants_remain() -> None:
    """The five ARMAN_TBD ceilings must never come back as module constants.

    A constant here would mean an admin turning the knob in the UI changed
    nothing — the silent failure the whole policy exists to end
    (common-docs/policies/limits-are-knobs-agents-set-them.md)."""
    import matrx_seo.budget as budget

    for name in (
        "DEFAULT_MAX_PER_REQUEST_COST_USD",
        "DEFAULT_ORG_PROVIDER_MONTHLY_CEILING_USD",
        "DEFAULT_GLOBAL_PROVIDER_MONTHLY_CEILING_USD",
        "DEFAULT_CALLER_DAILY_CEILING_USD",
        "DEFAULT_GLOBAL_DAILY_CEILING_USD",
    ):
        assert not hasattr(budget, name), f"{name} is back as a constant — every limit is a knob"


@pytest.mark.asyncio
async def test_missing_knob_raises_rather_than_guessing(monkeypatch) -> None:
    """No fallback value, anywhere. A knob the code names and the registry does
    not carry is a disagreement to fix, not a number to invent."""
    from matrx_seo import knobs as knobs_module

    async def _registry(feature: str) -> dict:
        return {"a_knob_that_exists": 1}

    monkeypatch.setattr(knobs_module, "_feature_values", _registry)
    with pytest.raises(knobs_module.KnobNotRegisteredError) as excinfo:
        await usd_knob("seo", "a_knob_nobody_seeded")
    # The message has to tell the next person what to DO, not just that it broke.
    assert "platform.feature_knob" in str(excinfo.value)


@pytest.mark.asyncio
async def test_every_ceiling_exceeds_the_head_room(knobs) -> None:
    """The interaction that made the old caller-daily ceiling unusable.

    ``max_per_request_cost_usd`` is head-room ADDED to measured spend before the
    comparison, so a ceiling at or below it rejects its own first call. The
    retired placeholders were $5.00 head-room against a $1.00 ceiling: nothing
    could ever pass that gate."""
    head_room = knobs["max_per_request_cost_usd"]
    for key, value in knobs.items():
        if key in ("max_per_request_cost_usd", "unpriced_run_assumed_cost_usd"):
            continue
        assert value > head_room, (
            f"{key}={value} does not exceed the ${head_room} head-room, so it "
            "would reject the very first call of every period"
        )

    repository = InMemorySeoRepository()
    # An empty history must PASS every ceiling. This is the regression test for
    # "the gate rejected before anyone had spent anything".
    await check_caller_daily_budget(repository, created_by="guest-1")
    await check_global_daily_budget(repository)
    await check_org_provider_monthly_budget(
        repository, organization_id="org-1", provider="dataforseo"
    )
    await check_global_provider_monthly_budget(repository, provider="dataforseo")
