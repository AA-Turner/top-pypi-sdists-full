"""The reuse lookup and fresh-purchase identity on the REAL ORM repository.

Live database, as the agent super-admin, cleaning up every row it creates (same
conventions as ``test_orm_repository_live.py``; skips without the DB env). Each
assertion fails if its mechanism in ``orm_repository.py`` is mutated away: the
window/narrowing cutoff, the scheduled-period filter, the verdict, and the
``identity_salt`` key.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from matrx_seo.contracts import (
    CollectionRequest,
    CollectionTrigger,
    ProviderResponse,
    RawPayloadEnvelope,
    SeoCapability,
)
from matrx_seo.identity import stable_hash

from test_orm_repository_live import _PROVIDER, _cleanup, _resolve_org  # noqa: E402


@pytest.fixture()
def live_user(isolated_host_database: tuple[str, str] | None) -> str:
    if isolated_host_database is None:
        pytest.skip("live DB env unavailable (AGENT_USER_ID / DB registration missing)")
    return isolated_host_database[0]


def _request(org_id: str, user_id: str, probe: str, **update) -> CollectionRequest:
    return CollectionRequest(
        organization_id=org_id,
        created_by=user_id,
        capability=SeoCapability.RAW_PROVIDER,
        operation="orm.live.reuse",
        target_ref=f"live-reuse-{probe}",
        observation_period="2026-10-05",
        settings={"probe": probe},
    ).model_copy(update=update)


@pytest.mark.asyncio(loop_scope="module")
async def test_reuse_lookup_and_fresh_identity_on_the_orm_repository(live_user: str) -> None:
    from matrx_seo.db import models_seo as m
    from matrx_seo.orm_repository import OrmSeoRepository

    org_id = await _resolve_org(live_user)
    probe = str(uuid4())
    repository = OrmSeoRepository()
    request = _request(org_id, live_user, probe)
    run_ids: list[str] = []
    try:
        run = await repository.start_run(_PROVIDER, request)
        run_ids.append(run.id)
        response = ProviderResponse(raw={"probe": probe})
        raw = await repository.persist_raw(
            run,
            response,
            RawPayloadEnvelope(payload=response.raw, checksum=stable_hash(response.raw), size_bytes=16),
        )
        await repository.complete_run(
            run, raw, response, await repository.persist_observations(run, raw, response, [])
        )
        aged = datetime.now(UTC) - timedelta(hours=3)
        update = await m.CollectionRun.update_where({"id": run.id}, completed_at=aged)
        assert update.rows_affected == 1

        # Inside the 24-hour window: reused, with a verdict naming the run and when.
        hit = await repository.find_fresh_completed(_PROVIDER, request, 24 * 3600)
        assert hit is not None and hit.run_id == run.id
        assert hit.reuse is not None and hit.reuse.decision == "reused"
        assert hit.reuse.reused_completed_at is not None
        assert abs((hit.reuse.reused_completed_at - aged).total_seconds()) < 2
        assert hit.freshness_ttl_seconds == 24 * 3600

        # Narrowing: a 1-hour requirement (or a 1-hour window) rejects a 3-hour-old run.
        assert (
            await repository.find_fresh_completed(
                _PROVIDER, request, 24 * 3600, require_fresh_within_seconds=3600
            )
            is None
        )
        assert await repository.find_fresh_completed(_PROVIDER, request, 3600) is None
        # A window of 0 never reuses.
        assert await repository.find_fresh_completed(_PROVIDER, request, 0) is None

        # A scheduled reading reuses only its own period.
        scheduled = request.model_copy(update={"trigger": CollectionTrigger.SCHEDULED})
        assert (await repository.find_fresh_completed(_PROVIDER, scheduled, 24 * 3600)) is not None
        other_period = scheduled.model_copy(update={"observation_period": "2026-10-06"})
        assert await repository.find_fresh_completed(_PROVIDER, other_period, 24 * 3600) is None
        # ...while an on-demand request reuses across periods (a rolling window).
        on_demand_other = request.model_copy(update={"observation_period": "2026-10-06"})
        assert (
            await repository.find_fresh_completed(_PROVIDER, on_demand_other, 24 * 3600)
        ) is not None

        # The fresh-purchase identity: a salt gives a NEW run beside the completed
        # one; the same salt collapses onto it; another salt is another run.
        base_again = await repository.start_run(_PROVIDER, request)
        assert base_again.id == run.id and base_again.status == "completed"
        salted = await repository.start_run(_PROVIDER, request, identity_salt="window:60:1")
        run_ids.append(salted.id)
        assert salted.id != run.id and salted.claimed is True and salted.created is True
        same = await repository.start_run(_PROVIDER, request, identity_salt="window:60:1")
        assert same.id == salted.id and same.created is False
        other = await repository.start_run(_PROVIDER, request, identity_salt="purchase:x")
        run_ids.append(other.id)
        assert other.id not in {run.id, salted.id}
        for leftover in (salted, other):
            await repository.fail_run(leftover, {"type": "LiveTestComplete", "message": "cleanup"})
    finally:
        await _cleanup(run_ids, {})
