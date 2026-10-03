"""Live-DB exercise of OrmSeoRepository + the ORM identity/host resolvers.

Runs against the real hosted database (aidream's ``supabase_automation_matrix``
pool aliased to ``matrx_seo``) as the standard agent super-admin, and CLEANS UP
every row it creates. Skips cleanly when the DB environment is unavailable.

NOTE: the isolated live-database fixture imports ``db.models`` / ``aidream`` —
that is fine for TESTS (only ``matrx_seo/`` package source is boundary-checked);
the package source itself never touches the host.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from datetime import date as date_type
from decimal import Decimal
from uuid import uuid4

import pytest

from matrx_seo.contracts import (
    BacklinkDimensionItem,
    BacklinkItem,
    BacklinkSnapshotObservation,
    CollectionRequest,
    ProviderCallRecord,
    ProviderResponse,
    ProviderTaskCheckpoint,
    RankObservation,
    RawPayloadEnvelope,
    SearchPerformanceObservation,
    SeoCapability,
    SeoIdentityRequest,
)
from matrx_seo.identity import stable_hash

_PROVIDER = "orm-live-test"


@pytest.fixture()
def live_user(isolated_host_database: tuple[str, str] | None) -> str:
    if isolated_host_database is None:
        pytest.skip("live DB env unavailable (AGENT_USER_ID / DB registration missing)")
    return isolated_host_database[0]


_SWEPT_STALE_LEAKS = False


async def _sweep_stale_leaks() -> None:
    """Self-heal debris from PRIOR crashed/interrupted runs of this file.

    A killed pytest process (or an exception inside ``_cleanup``) leaks the
    ``live-orm-test-*`` web.site rows, their ``orm-live-test`` collection runs,
    and the ``Live ORM   Probe`` keywords into the LIVE database — where they
    show up in the Marketing sites UI and get picked up by real scheduled
    collectors. Best-effort, once per session, before the first site is minted.
    """
    global _SWEPT_STALE_LEAKS
    if _SWEPT_STALE_LEAKS:
        return
    _SWEPT_STALE_LEAKS = True
    from matrx_seo.db import models_seo as m

    stale_sites = await _writable_site_model().filter_items(
        name__startswith="live-orm-test-"
    )
    stale_runs = {str(r.id) for r in await m.CollectionRun.filter_items(provider=_PROVIDER)}
    for site in stale_sites:
        for run in await m.CollectionRun.filter_items(site_id=str(site.id)):
            stale_runs.add(str(run.id))
    try:
        await _cleanup(sorted(stale_runs), {})
    except Exception:
        pass
    for keyword in await m.Keyword.filter_items(phrase__startswith="Live ORM "):
        try:
            for market in await m.KeywordMarket.filter_items(keyword_id=str(keyword.id)):
                await market.delete()
            await keyword.delete()
        except Exception:
            pass
    for site in stale_sites:
        try:
            for target in await m.RankTarget.filter_items(site_id=str(site.id)):
                await target.delete()
            await site.delete()
        except Exception:
            pass


async def _create_site(org_id: str, user_id: str, probe: str) -> str:
    """Create a REAL web.site row for the test (create-then-cleanup pattern).

    The package's WebSite model is deliberately read-only (the vertical never
    mints sites), so the test declares its own writable model over the same
    table — tests may do what package source may not.
    """
    await _sweep_stale_leaks()
    site = await _writable_site_model().create(
        id=str(uuid4()),
        organization_id=org_id,
        name=f"live-orm-test-{probe}",
        root_url=f"https://live-orm-test-{probe}.example",
        domain=f"live-orm-test-{probe}.example",
        created_by=user_id,
        integrations={},
        # NEVER "active": every scheduled collector (rank/gsc/ga4/backlinks)
        # enumerates status="active" sites — a leaked active test site gets
        # REAL paid provider runs pointed at its fake .example domain.
        status="archived",
    )
    return str(site.id)


_WRITABLE_SITE_MODEL = None


def _writable_site_model():
    global _WRITABLE_SITE_MODEL
    if _WRITABLE_SITE_MODEL is None:
        from matrx_orm import JSONBField, Model, TextField, UUIDField

        class _TestWebSite(Model):
            id = UUIDField(primary_key=True, null=False)
            organization_id = UUIDField(null=False)
            name = TextField(null=False)
            root_url = TextField(null=False)
            domain = TextField(null=False)
            created_by = UUIDField()
            integrations = JSONBField(null=False, default={})
            status = TextField(null=False)
            _database = "supabase_automation_matrix"
            _table_name = "site"
            _db_schema = "web"

        _WRITABLE_SITE_MODEL = _TestWebSite
    return _WRITABLE_SITE_MODEL


async def _delete_site(site_id: str | None) -> None:
    if not site_id:
        return
    row = await _writable_site_model().load_by_id_or_none(site_id)
    if row is not None:
        await row.delete()


async def _resolve_org(user_id: str) -> str:
    """The organization this live test acts in — READ from the user's own active
    membership row (a durable record), never a personal-organization resolver
    choosing tenancy for it.
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


def _request(
    org_id: str, user_id: str, probe: str, site_id: str | None = None
) -> CollectionRequest:
    return CollectionRequest(
        organization_id=org_id,
        created_by=user_id,
        capability=SeoCapability.SERP_RANK,
        operation="orm.live.cycle",
        target_ref=f"live-{probe}",
        site_id=site_id,
        observation_period="live-acceptance",
        settings={"probe": probe},
        execution_id=uuid4(),
    )


async def _cleanup(run_ids: list[str], identity_rows: dict[str, str | None]) -> None:
    """Delete everything the test created, children before parents."""
    from matrx_seo.db import models_seo as m

    # seo.keyword_market.source_observation_id references
    # seo.keyword_market_observation(id) — the cache row must go BEFORE its
    # source history row, which itself must go before the raw_payload/run
    # rows it references (WS-8/DEF-21).
    keyword_id = identity_rows.get("keyword_id")
    if keyword_id:
        for market in await m.KeywordMarket.filter_items(keyword_id=keyword_id):
            await market.delete()

    for run_id in run_ids:
        for snapshot in await m.BacklinkSnapshot.filter_items(run_id=run_id):
            for child in await m.BacklinkObservation.filter_items(snapshot_id=str(snapshot.id)):
                await child.delete()
            for child in await m.BacklinkDimensionSnapshot.filter_items(
                snapshot_id=str(snapshot.id)
            ):
                await child.delete()
            await snapshot.delete()
        for snapshot in await m.SerpSnapshot.filter_items(run_id=run_id):
            for child in await m.SerpResult.filter_items(snapshot_id=str(snapshot.id)):
                await child.delete()
            await snapshot.delete()
        for model in (
            m.RankObservation,
            m.SearchPerformanceDaily,
            m.WebAnalyticsDaily,
            m.PagePerformance,
            m.KeywordMarketObservation,
            m.ProviderCall,
            m.ProviderTask,
            m.RawPayload,
        ):
            for row in await model.filter_items(run_id=run_id):
                await row.delete()
        run_row = await m.CollectionRun.load_by_id_or_none(run_id)
        if run_row is not None:
            await run_row.delete()

    rank_target_id = identity_rows.get("rank_target_id")
    if rank_target_id:
        row = await m.RankTarget.load_by_id_or_none(rank_target_id)
        if row is not None:
            await row.delete()
    location_id = identity_rows.get("location_id")
    if location_id:
        row = await m.Location.load_by_id_or_none(location_id)
        if row is not None:
            await row.delete()
    if keyword_id:
        row = await m.Keyword.load_by_id_or_none(keyword_id)
        if row is not None:
            await row.delete()


@pytest.mark.asyncio(loop_scope="module")
async def test_full_cycle_idempotency_and_fail_reclaim_live(live_user: str) -> None:
    from matrx_seo.orm_identity import OrmSeoIdentityResolver
    from matrx_seo.orm_repository import OrmSeoRepository

    org_id = await _resolve_org(live_user)
    probe = str(uuid4())
    # DEF-25: rank_target is never minted without a REAL site — create one.
    site_id = await _create_site(org_id, live_user, probe)
    request = _request(org_id, live_user, probe, site_id=site_id)
    repository = OrmSeoRepository()
    run_ids: list[str] = []
    identity_rows: dict[str, str | None] = {}
    try:
        run = await repository.start_run(_PROVIDER, request)
        run_ids.append(run.id)
        assert run.created is True
        assert run.claimed is True
        assert run.status == "processing"

        identity = await OrmSeoIdentityResolver().resolve(
            request,
            SeoIdentityRequest(
                keyword=f"  Live ORM   Probe {probe} ",
                engine="google",
                device="desktop",
                search_type="organic",
                target_domain="example.com",
                country_code="US",
                city=f"Live Test {probe}",
            ),
        )
        identity_rows.update(
            keyword_id=identity.keyword_id,
            location_id=identity.location_id,
            rank_target_id=identity.rank_target_id,
        )
        assert identity.rank_target_id is not None
        assert identity.location_id is not None

        response = ProviderResponse(
            raw={"probe": probe, "rank": 3},
            reported_cost=Decimal("0.01"),
            estimated_cost=Decimal("0.01"),
        )
        checksum = stable_hash(response.raw)
        raw = await repository.persist_raw(
            run,
            response,
            RawPayloadEnvelope(payload=response.raw, checksum=checksum, size_bytes=32),
        )
        assert raw.created is True
        replay = await repository.persist_raw(
            run,
            response,
            RawPayloadEnvelope(payload=response.raw, checksum=checksum, size_bytes=32),
        )
        assert replay.created is False
        assert replay.id == raw.id

        observed_at = datetime.now(UTC)
        observations = [
            RankObservation(
                keyword_id=identity.keyword_id,
                rank_target_id=identity.rank_target_id,
                location_id=identity.location_id,
                engine="google",
                locale="en-US",
                matched_domain="example.com",
                matched_url="https://example.com/",
                organic_rank=3,
                absolute_rank=3,
                observed_at=observed_at,
            ),
            SearchPerformanceObservation(
                site_id=site_id,
                keyword_id=identity.keyword_id,
                date=date_type(2026, 7, 21),
                query=f"live orm probe {probe}",
                clicks=2,
                impressions=10,
            ),
        ]
        upsert = await repository.persist_observations(run, raw, response, observations)
        assert upsert.created == 2
        assert upsert.existing == 0
        again = await repository.persist_observations(run, raw, response, observations)
        assert again.created == 0
        assert again.existing == 2
        assert sorted(again.observation_ids) == sorted(upsert.observation_ids)

        await repository.checkpoint_provider_task(
            run,
            ProviderTaskCheckpoint(external_task_id=f"task-{probe}", status="completed"),
        )
        tasks = await repository.list_provider_tasks(run)
        assert [task.external_task_id for task in tasks] == [f"task-{probe}"]

        receipt = await repository.complete_run(run, raw, response, upsert)
        assert receipt.created_observations == 2
        assert receipt.raw_payload_id == raw.id

        rerun = await repository.start_run(_PROVIDER, request)
        assert rerun.created is False
        assert rerun.claimed is False
        assert rerun.status == "completed"
        reused = await repository.receipt_for_run(rerun)
        assert reused.reused_completed_run is True
        assert reused.existing_observations == 2
        assert reused.raw_payload_id == raw.id

        payload = await repository.load_raw_payload(raw.id)
        assert payload == {"probe": probe, "rank": 3}

        # fail path → reclaim increments attempt_count
        fail_request = _request(org_id, live_user, f"{probe}-fail")
        fail_run = await repository.start_run(_PROVIDER, fail_request)
        run_ids.append(fail_run.id)
        assert fail_run.claimed is True
        await repository.fail_run(fail_run, {"type": "LiveTestError", "message": "expected"})
        reclaimed = await repository.start_run(_PROVIDER, fail_request)
        assert reclaimed.id == fail_run.id
        assert reclaimed.created is False
        assert reclaimed.claimed is True
        assert reclaimed.status == "processing"
        assert reclaimed.attempt_count == 2
        from matrx_seo.db import models_seo as m

        reclaimed_row = await m.CollectionRun.load_by_id_or_none(reclaimed.id)
        assert reclaimed_row is not None
        assert reclaimed_row.error is None

        retry_response = ProviderResponse(raw={"probe": probe, "retry": True})
        retry_raw = await repository.persist_raw(
            reclaimed,
            retry_response,
            RawPayloadEnvelope(
                payload=retry_response.raw,
                checksum=stable_hash(retry_response.raw),
                size_bytes=32,
            ),
        )
        await reclaimed_row.update(error={"type": "stale-error-defense-probe"})
        await repository.complete_run(
            reclaimed,
            retry_raw,
            retry_response,
            await repository.persist_observations(reclaimed, retry_raw, retry_response, []),
        )
        completed_row = await m.CollectionRun.load_by_id_or_none(reclaimed.id)
        assert completed_row is not None
        assert completed_row.status == "completed"
        assert completed_row.error is None

        # crashed-worker path → an expired processing lease is reclaimed by CAS
        stale_request = _request(org_id, live_user, f"{probe}-stale")
        stale_run = await repository.start_run(_PROVIDER, stale_request)
        run_ids.append(stale_run.id)
        stale_owner = stale_run.lease_owner
        expired_at = datetime.now(UTC) - timedelta(seconds=1)
        update = await m.CollectionRun.update_where(
            {"id": stale_run.id, "lease_owner": stale_owner},
            lease_expires_at=expired_at,
        )
        assert update.rows_affected == 1

        stale_reclaimed = await repository.start_run(_PROVIDER, stale_request)
        assert stale_reclaimed.id == stale_run.id
        assert stale_reclaimed.claimed is True
        assert stale_reclaimed.attempt_count == 2
        assert stale_reclaimed.lease_owner != stale_owner
        assert stale_reclaimed.lease_expires_at is not None
        assert stale_reclaimed.lease_expires_at > datetime.now(UTC)
        await repository.fail_run(
            stale_reclaimed,
            {"type": "LiveTestComplete", "message": "cleanup"},
        )
    finally:
        try:
            await _cleanup(run_ids, identity_rows)
        finally:
            await _delete_site(site_id)


@pytest.mark.asyncio(loop_scope="module")
async def test_backlink_snapshot_children_and_receipt_live(live_user: str) -> None:
    from matrx_seo.orm_repository import OrmSeoRepository

    org_id = await _resolve_org(live_user)
    probe = str(uuid4())
    site_id = await _create_site(org_id, live_user, probe)
    request = CollectionRequest(
        organization_id=org_id,
        created_by=live_user,
        capability=SeoCapability.BACKLINKS,
        operation="orm.backlinks.live",
        target_ref=f"web.site:{site_id}",
        site_id=site_id,
        observation_period="live-acceptance",
        settings={"probe": probe},
    )
    repository = OrmSeoRepository()
    run_ids: list[str] = []
    try:
        run = await repository.start_run(_PROVIDER, request)
        run_ids.append(run.id)
        response = ProviderResponse(raw={"probe": probe, "dataset": "backlinks"})
        raw = await repository.persist_raw(
            run,
            response,
            RawPayloadEnvelope(
                payload=response.raw,
                checksum=stable_hash(response.raw),
                size_bytes=64,
            ),
        )
        observation = BacklinkSnapshotObservation(
            site_id=site_id,
            dataset="backlinks",
            target="example.com",
            total_backlinks=1,
            observed_at=datetime.now(UTC),
            backlinks=[
                BacklinkItem(
                    source_url="https://referrer.example/article",
                    source_domain="referrer.example",
                    target_url="https://example.com/landing",
                    anchor_text="example",
                    is_dofollow=True,
                )
            ],
            dimensions=[
                BacklinkDimensionItem(
                    dimension_kind="referring_domain",
                    dimension_key="referrer.example",
                    label="referrer.example",
                    backlinks=1,
                )
            ],
        )

        first = await repository.persist_observations(run, raw, response, [observation])
        replay = await repository.persist_observations(run, raw, response, [observation])
        assert first.created == 1
        assert replay.existing == 1

        from matrx_seo.db import models_seo as m

        snapshots = await m.BacklinkSnapshot.filter_items(run_id=run.id)
        backlinks = await m.BacklinkObservation.filter_items(run_id=run.id)
        dimensions = await m.BacklinkDimensionSnapshot.filter_items(run_id=run.id)
        assert len(snapshots) == len(backlinks) == len(dimensions) == 1
        assert len({str(snapshots[0].id), str(backlinks[0].id), str(dimensions[0].id)}) == 3

        await repository.complete_run(run, raw, response, first)
        receipt = await repository.receipt_for_run(run)
        assert receipt.existing_observations == 1
    finally:
        try:
            await _cleanup(run_ids, {})
        finally:
            await _delete_site(site_id)


@pytest.mark.asyncio(loop_scope="module")
async def test_link_keyword_to_project_round_trip_live(live_user: str) -> None:
    from matrx_seo.db import models_seo as m
    from matrx_seo.db.models_host import PlatformAssociation, WorkspaceProject
    from matrx_seo.orm_identity import (
        KEYWORD_ENTITY_TOKEN,
        KEYWORD_PROJECT_ROLE,
        PROJECT_ENTITY_TOKEN,
        link_keyword_to_project,
        unlink_keyword_from_project,
    )

    org_id = await _resolve_org(live_user)
    projects = await WorkspaceProject.filter(organization_id=org_id).limit(1).all()
    if not projects:
        pytest.skip(
            "no projects.projects row exists for the agent org and the package "
            "project model is read-only — cannot create one from the vertical"
        )
    project_id = str(projects[0].id)
    probe = str(uuid4())
    now = datetime.now(UTC)
    keyword = await m.Keyword.create(
        id=str(uuid4()),
        organization_id=org_id,
        phrase=f"live link probe {probe}",
        normalized_phrase=f"live link probe {probe}",
        language="en",
        created_by=live_user,
        created_at=now,
        updated_at=now,
        metadata={},
    )
    try:
        settings = {"target_rank": 3, "priority": "high"}
        edge = await link_keyword_to_project(
            str(keyword.id),
            project_id,
            org_id=org_id,
            user_id=live_user,
            settings=settings,
        )
        assert edge.metadata == settings
        assert edge.role == KEYWORD_PROJECT_ROLE
        assert edge.source_type == KEYWORD_ENTITY_TOKEN
        assert edge.target_type == PROJECT_ENTITY_TOKEN

        updated_settings = {"target_rank": 1, "priority": "urgent"}
        repeat = await link_keyword_to_project(
            str(keyword.id),
            project_id,
            org_id=org_id,
            user_id=live_user,
            settings=updated_settings,
        )
        assert str(repeat.id) == str(edge.id)
        assert repeat.metadata == updated_settings

        removed = await unlink_keyword_from_project(str(keyword.id), project_id, org_id=org_id)
        assert removed == 1
        leftover = await PlatformAssociation.filter_items(
            source_type=KEYWORD_ENTITY_TOKEN,
            source_id=str(keyword.id),
            target_type=PROJECT_ENTITY_TOKEN,
            target_id=project_id,
        )
        assert leftover == []
    finally:
        for edge_row in await PlatformAssociation.filter_items(
            source_type=KEYWORD_ENTITY_TOKEN, source_id=str(keyword.id)
        ):
            await edge_row.delete()
        await keyword.delete()


@pytest.mark.asyncio(loop_scope="module")
async def test_keyword_market_upsert_merge_and_trajectory_live(live_user: str) -> None:
    """The §F volume trial: keyword via fn_upsert_keyword, keyword_market
    upserted with merged monthly_searches + computed trajectory, and a second
    identical run producing no duplicates and an unchanged history."""
    import json as json_lib

    from matrx_seo.contracts import KeywordMarketObservation, MonthlySearch
    from matrx_seo.db import models_seo as m
    from matrx_seo.orm_identity import upsert_keyword
    from matrx_seo.orm_repository import OrmSeoRepository

    org_id = await _resolve_org(live_user)
    probe = str(uuid4())
    phrase = f"live market probe {probe}"
    request = CollectionRequest(
        organization_id=org_id,
        created_by=live_user,
        capability=SeoCapability.KEYWORD_METRICS,
        operation="orm.keyword_market.live",
        target_ref=f"live-{probe}",
        observation_period="live-acceptance",
        settings={"probe": probe},
        execution_id=uuid4(),
    )
    repository = OrmSeoRepository()
    run_ids: list[str] = []
    identity_rows: dict[str, str | None] = {}
    try:
        keyword_id, created = await upsert_keyword(phrase)
        identity_rows["keyword_id"] = keyword_id
        assert created is True
        keyword_id_again, created_again = await upsert_keyword(f"  {phrase.upper()}  ")
        assert keyword_id_again == keyword_id  # normalization dedupe
        assert created_again is False
        keyword_row = await m.Keyword.load_by_id_or_none(keyword_id)
        assert keyword_row is not None
        # intent/category are DROPPED — the retired columns must not resurface
        assert not hasattr(keyword_row, "intent") and not hasattr(keyword_row, "category")

        run = await repository.start_run(_PROVIDER, request)
        run_ids.append(run.id)
        response = ProviderResponse(raw={"probe": probe})
        raw = await repository.persist_raw(
            run,
            response,
            RawPayloadEnvelope(
                payload=response.raw, checksum=stable_hash(response.raw), size_bytes=16
            ),
        )
        observation = KeywordMarketObservation(
            keyword_id=keyword_id,
            location_code=2840,
            search_volume=100,
            competition="HIGH",
            competition_index=87,
            cpc=Decimal("4.25"),
            monthly_searches=[
                MonthlySearch(year=2026, month=month, search_volume=80 + month)
                for month in range(1, 7)
            ],
            metrics_task_id=f"task-{probe}",
            raw={"keyword": phrase, "search_volume": 100},
            observed_at=datetime.now(UTC),
        )
        first = await repository.persist_observations(run, raw, response, [observation])
        assert first.created == 1 and first.existing == 0

        def _monthly(market_row) -> list[dict]:
            value = market_row.monthly_searches
            return json_lib.loads(value) if isinstance(value, str) else value

        markets = await m.KeywordMarket.filter_items(keyword_id=keyword_id)
        assert len(markets) == 1
        market = markets[0]
        assert market.location_code == 2840
        assert market.competition == "HIGH" and market.competition_index == 87
        assert market.metrics_fetched_at is not None
        assert market.data_months == 6
        assert market.demand_trajectory is not None
        first_monthly = _monthly(market)
        assert len(first_monthly) == 6

        second = await repository.persist_observations(run, raw, response, [observation])
        assert second.created == 0 and second.existing == 1
        markets = await m.KeywordMarket.filter_items(keyword_id=keyword_id)
        assert len(markets) == 1  # no duplicates
        assert _monthly(markets[0]) == first_monthly  # history unchanged

        # A later fetch MERGES: old months retained, new month added.
        newer = observation.model_copy(
            update={
                "monthly_searches": [
                    MonthlySearch(year=2026, month=7, search_volume=200),
                    MonthlySearch(year=2026, month=6, search_volume=99),
                ]
            }
        )
        third = await repository.persist_observations(run, raw, response, [newer])
        assert third.existing == 1
        merged = _monthly((await m.KeywordMarket.filter_items(keyword_id=keyword_id))[0])
        assert len(merged) == 7  # 6 original months + July; June overwritten
        by_month = {(item["year"], item["month"]): item["search_volume"] for item in merged}
        assert by_month[(2026, 7)] == 200
        assert by_month[(2026, 6)] == 99  # new data wins on collision
        assert by_month[(2026, 1)] == 81  # old months retained
        await repository.complete_run(
            run, raw, response, await repository.persist_observations(run, raw, response, [])
        )
    finally:
        await _cleanup(run_ids, identity_rows)


@pytest.mark.asyncio(loop_scope="module")
async def test_provider_call_retry_merges_evidence_live(live_user: str) -> None:
    """DEF-19 (2026-07-23) live proof: a retried provider call sharing the
    same (run_id, provider_call_key) MERGES its improved request_count/cost/
    metadata into the existing seo.provider_call row instead of the first,
    incomplete attempt winning by insert-ignore."""
    from matrx_seo.db import models_seo as m
    from matrx_seo.orm_repository import OrmSeoRepository

    org_id = await _resolve_org(live_user)
    probe = str(uuid4())
    request = CollectionRequest(
        organization_id=org_id,
        created_by=live_user,
        capability=SeoCapability.BACKLINKS,
        operation="orm.provider_call_merge.live",
        target_ref=f"live-{probe}",
        observation_period="live-acceptance",
        settings={"probe": probe},
        execution_id=uuid4(),
    )
    repository = OrmSeoRepository()
    run_ids: list[str] = []
    try:
        run = await repository.start_run(_PROVIDER, request)
        run_ids.append(run.id)

        first = ProviderResponse(
            raw={"transport_error": "timed out"},
            call_records=[
                ProviderCallRecord(
                    provider_call_key=f"call-{probe}",
                    request_count=1,
                    reported_cost=None,
                    metadata={"attempt": 1},
                )
            ],
        )
        await repository.persist_raw(
            run,
            first,
            RawPayloadEnvelope(
                payload=first.raw, checksum=stable_hash(["first", probe]), size_bytes=16
            ),
        )

        retry = ProviderResponse(
            raw={"tasks": [{"id": f"call-{probe}", "status_code": 20000}]},
            call_records=[
                ProviderCallRecord(
                    provider_call_key=f"call-{probe}",
                    external_task_id=f"call-{probe}",
                    request_count=2,
                    reported_cost=Decimal("0.0125"),
                    metadata={"attempt": 2, "status": "completed"},
                )
            ],
        )
        await repository.persist_raw(
            run,
            retry,
            RawPayloadEnvelope(
                payload=retry.raw, checksum=stable_hash(["retry", probe]), size_bytes=24
            ),
        )

        rows = await m.ProviderCall.filter_items(run_id=run.id, provider_call_key=f"call-{probe}")
        assert len(rows) == 1  # one row per call key — no duplicate paid-call record
        merged = rows[0]
        assert merged.external_task_id == f"call-{probe}"
        assert merged.request_count == 2
        assert merged.reported_cost == Decimal("0.0125")
        assert merged.metadata == {"attempt": 2, "status": "completed"}
    finally:
        await _cleanup(run_ids, {})
