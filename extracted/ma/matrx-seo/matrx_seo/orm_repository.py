"""Canonical ORM-backed :class:`SeoRepository` over the live ``seo.*`` schema.

Mirrors :class:`matrx_seo.repository.InMemorySeoRepository` semantics exactly:
idempotent ``start_run`` keyed on ``idempotency_key``, lease-fenced writes,
dedup-keyed observation upserts (insert-if-absent, never replace), provider-call
cost rollup onto the run row, and receipts recomputed from the tables. All
access goes through matrx-orm models — zero raw SQL.
"""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from matrx_orm.core.expressions import (
    Case,
    Coalesce,
    ColumnComparison,
    DbFunction,
    Excluded,
    F,
    Greatest,
    Is,
    JsonbConcat,
    Now,
    When,
)
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk
from matrx_orm import retry_on_transient
from matrx_orm.session.fallback import SYSTEM_ORGANIZATION_ID
from matrx_orm.operations.conflict_writes import (
    bulk_insert_ignore,
    bulk_upsert_increment,
    insert_ignore,
)

from .authority_score import AuthorityInputs, score_authority
from .backlink_enrichment import backlink_identity_key, upsert_current_backlinks
from .config import get_payload_fetcher
from .contracts import (
    BacklinkSnapshotObservation,
    CollectionInProgressError,
    CollectionReceipt,
    CollectionRequest,
    CollectionRun,
    CollectionTrigger,
    CredentialReferenceKind,
    KeywordMarketObservation,
    LinkGapDomainItem,
    LinkGapObservation,
    PagePerformanceObservation,
    ProviderCallRecord,
    ProviderResponse,
    ProviderTaskCheckpoint,
    RankObservation,
    RawPayloadEnvelope,
    RawPayloadReceipt,
    SearchPerformanceObservation,
    SeoCapability,
    SeoObservation,
    SerpProspectObservation,
    SerpSnapshotObservation,
    SpendQuery,
    SpendSummary,
    UpsertReceipt,
    WebAnalyticsObservation,
)
from .db import models_seo as m
from .identity import collection_identity, stable_hash
from .market_math import compute_market_stats, merge_monthly
from .repository import RUN_LEASE_SECONDS, SeoRepository

# seo.search_performance_daily write shape (see _persist_search_performance_batch):
# rows per INSERT / dedup-key reload, and total attempts per statement on a
# transient DB failure (QueryTimeoutError / PoolAcquireTimeoutError).
_SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS = 500
_SEARCH_PERFORMANCE_WRITE_ATTEMPTS = 3

# Run-scoped observation tables (all carry run_id). seo.keyword_market is NOT
# here — it is a current-state cache keyed (keyword_id, location_code), not a
# per-run observation, so cached-run receipts don't recount it.
_OBSERVATION_MODELS: tuple[type, ...] = (
    m.SerpSnapshot,
    m.RankObservation,
    m.SearchPerformanceDaily,
    m.WebAnalyticsDaily,
    m.PagePerformance,
    m.BacklinkSnapshot,
    m.KeywordMarketObservation,
)


#: Where a finished run records how many observation rows carry its ``run_id`` (``metadata`` JSONB,
#: so no column). Backfilled for older runs by the window script
#: ``common-docs/projects/access-by-person-not-selection/window/seo-run-counts-window.sql``.
OBSERVATION_COUNT_KEY = "observation_count"


def stored_observation_count(row: Any) -> int | None:
    """The count a run wrote about itself, or None (older run: the caller counts exactly)."""
    meta = getattr(row, "metadata", None)
    if isinstance(meta, dict) and isinstance(meta.get(OBSERVATION_COUNT_KEY), int):
        return int(meta[OBSERVATION_COUNT_KEY])
    return None


def _now() -> datetime:
    return datetime.now(UTC)


def _carries_volume(observation: KeywordMarketObservation) -> bool:
    """Whether a keyword-market observation reports volume metrics at all — as
    opposed to a difficulty-only observation, which must never overwrite them."""
    return (
        observation.search_volume is not None
        or observation.cpc is not None
        or observation.competition is not None
        or observation.competition_index is not None
        or observation.low_top_of_page_bid is not None
        or observation.high_top_of_page_bid is not None
        or bool(observation.monthly_searches)
    )


def _prepare_search_performance_rows(
    run: CollectionRun,
    raw: RawPayloadReceipt,
    observations: list[SearchPerformanceObservation],
    now: datetime,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Build the CPU-heavy bulk-write shape outside the request event loop."""
    rows: list[dict[str, Any]] = []
    dedup_keys: list[str] = []
    for observation in observations:
        dedup_key = _observation_dedup_key(
            run.idempotency_key, run.request.organization_id, run.provider, observation
        )
        dedup_keys.append(dedup_key)
        rows.append(
            {
                "id": str(uuid4()),
                "organization_id": run.request.organization_id,
                "created_by": run.request.created_by,
                "run_id": run.id,
                "raw_payload_id": raw.id,
                "provider": run.provider,
                "dedup_key": dedup_key,
                "site_id": observation.site_id,
                "page_id": observation.page_id,
                "keyword_id": observation.keyword_id,
                "date": observation.date,
                "query": observation.query,
                "country": observation.country,
                "device": observation.device,
                "dimension_profile": observation.dimension_profile,
                "search_appearance": observation.search_appearance,
                "clicks": observation.clicks,
                "impressions": observation.impressions,
                "ctr": observation.ctr,
                "average_position": observation.average_position,
                "extras": observation.extras,
                "created_at": now,
            }
        )
    return rows, dedup_keys


def request_from_row(row: Any) -> CollectionRequest:
    """Rebuild the contract-level :class:`CollectionRequest` from a persisted
    ``seo.collection_run`` row. The ONE row→request projection — reads,
    resume/reclaim, and the standalone app all delegate here so a second
    deserializer can never drift."""
    reference_kind = row.credential_reference_kind or CredentialReferenceKind.PLATFORM_SECRET.value
    return CollectionRequest(
        organization_id=str(row.organization_id),
        created_by=str(row.created_by),
        capability=SeoCapability(row.capability),
        operation=row.operation,
        target_ref=row.target_ref,
        site_id=str(row.site_id) if row.site_id else None,
        page_id=str(row.page_id) if row.page_id else None,
        source_crawl_session_id=(
            str(row.source_crawl_session_id) if row.source_crawl_session_id else None
        ),
        observation_period=row.observation_period,
        settings=row.settings or {},
        trigger=CollectionTrigger(row.trigger),
        credential_reference_id=row.credential_reference_id,
        credential_reference_kind=CredentialReferenceKind(reference_kind),
        request_id=row.request_id,
        execution_id=row.execution_id,
    )


def run_from_row(row: Any, *, claimed: bool = False) -> CollectionRun:
    """Rebuild the contract-level :class:`CollectionRun` from a persisted row
    (unclaimed by default — reclaiming is a repository CAS, never a rebuild)."""
    return CollectionRun(
        id=str(row.id),
        provider=row.provider,
        request=request_from_row(row),
        settings_hash=row.settings_hash,
        idempotency_key=row.idempotency_key,
        status=row.status,
        created=False,
        claimed=claimed,
        lease_owner=row.lease_owner,
        lease_expires_at=row.lease_expires_at,
        attempt_count=row.attempt_count,
    )


async def _promote_existing_raw_payload_offload(
    existing: Any,
    envelope: RawPayloadEnvelope,
) -> None:
    if envelope.cloud_file_id is None or existing.cloud_file_id is not None:
        return
    if (
        str(existing.checksum) != envelope.checksum
        or int(existing.size_bytes) != envelope.size_bytes
    ):
        raise RuntimeError("refusing raw payload offload promotion: checksum or size mismatch")
    await existing.update(
        cloud_file_id=envelope.cloud_file_id,
        payload=None,
        offload_error=None,
    )


def _authority_ranking(domain: LinkGapDomainItem) -> dict[str, Any]:
    """Rank one gap domain with the Matrx Authority Score as it lands.

    Ranking at persist time rather than in a later pass is what makes the very
    first render of a prospect list useful: a non-technical user opens it and
    the best opportunities are already on top, each with a sentence saying why.

    Two rules encoded here:

    * **An unmeasured domain keeps a NULL priority, never a 0.** A zero sorts
      identically to "we measured this and it is worthless", which is a lie the
      user cannot see through.
    * **This ORDERS the list; it never filters it.** No row is withheld because
      it scored badly — only a human removes a row (the review gate).

    The AI ranking layer may later overwrite ``priority_score``/``priority_reason``
    by design, so the full deterministic breakdown is also kept under
    ``metadata['matrx_authority']`` where it stays auditable.
    """
    # 🚨 `total_backlinks` is deliberately NOT passed as `own_backlinks`. On an
    # intersection response it is the number of links this domain sends to the
    # COMPETITORS — a relationship measure, not the domain's own link profile —
    # and feeding it as authority scores a newspaper below a link farm (see
    # AuthorityInputs' misfeeding trap). `match_count` is the relationship
    # signal and is already the list's primary sort. True own-profile counts
    # come from the bulk enrichment pass (`matrx_seo.authority_enrichment`),
    # which the gap run now calls straight after persisting — so this score is
    # the honest *pre-enrichment* one (rank + spam, `partial` confidence) and
    # `enrich_rows` overwrites it with the measured three-signal score moments
    # later. Both are written by the SAME scorer, so they never disagree in
    # meaning, only in confidence.
    score = score_authority(
        AuthorityInputs(
            domain_rank=domain.domain_rank,
            own_referring_domains=domain.referring_domains,
            spam_score=domain.spam_score,
        )
    )
    values: dict[str, Any] = {
        "metadata": {"matrx_authority": score.model_dump(mode="json")},
    }
    if score.value is not None:
        values["priority_score"] = score.value
        values["priority_reason"] = score.why
    return values


def _observation_dedup_key(
    collection_identity_key: str,
    organization_id: str,
    provider: str,
    observation: SeoObservation,
) -> str:
    """Stable hash of one observation within its durable collection identity.

    Retries of the same run remain idempotent, while an explicit fresh run owns
    its own observation rows and therefore keeps a truthful run receipt.
    """
    base: dict[str, Any] = {
        "kind": observation.kind,
        "collection_identity_key": collection_identity_key,
        "organization_id": organization_id,
        "provider": provider,
    }
    if isinstance(observation, RankObservation | SerpSnapshotObservation):
        base.update(
            keyword_id=observation.keyword_id,
            rank_target_id=observation.rank_target_id,
            location_id=observation.location_id,
            engine=observation.engine,
            language=observation.language,
            device=observation.device,
            search_type=observation.search_type,
            observed_at=observation.observed_at,
        )
    elif isinstance(observation, KeywordMarketObservation):
        # WS-8/DEF-21: identity = provider + collection run + keyword +
        # location + when the provider says it observed the value — a
        # replay of the SAME run never duplicates history, while a genuinely
        # later collection (new run, or the same run's next distinct
        # observed_at) always lands its own row.
        base.update(
            keyword_id=observation.keyword_id,
            location_code=observation.location_code,
            observed_at=observation.observed_at,
        )
    elif isinstance(observation, SearchPerformanceObservation):
        base.update(
            site_id=observation.site_id,
            page_id=observation.page_id,
            keyword_id=observation.keyword_id,
            date=observation.date.isoformat(),
            query=observation.query,
            country=observation.country,
            device=observation.device,
            dimension_profile=observation.dimension_profile,
            search_appearance=observation.search_appearance,
        )
    elif isinstance(observation, WebAnalyticsObservation):
        base.update(
            site_id=observation.site_id,
            page_id=observation.page_id,
            date=observation.date.isoformat(),
            source=observation.source,
            medium=observation.medium,
            channel=observation.channel,
            campaign=observation.campaign,
            device=observation.device,
            landing_page=observation.landing_page,
        )
    elif isinstance(observation, PagePerformanceObservation):
        base.update(
            page_id=observation.page_id,
            strategy=observation.strategy,
            observed_at=observation.observed_at,
        )
    elif isinstance(observation, BacklinkSnapshotObservation):
        base.update(
            site_id=observation.site_id,
            page_id=observation.page_id,
            dataset=observation.dataset,
            target=observation.target,
            target_type=observation.target_type,
            observed_at=observation.observed_at,
        )
    else:
        raise NotImplementedError(
            f"SEO observation kind {observation.kind!r} has no seo.* table — "
            "persisting it requires a schema addition, not a silent skip"
        )
    return stable_hash(base)


#: How many archived runs in a row one collection identity may walk past before
#: start_run refuses (an archival loop is a defect, never a normal state).
_ARCHIVED_SUCCESSOR_LIMIT = 8


class OrmSeoRepository(SeoRepository):
    async def _claimed_row(self, run: CollectionRun) -> Any:
        row = await m.CollectionRun.load_by_id_or_none(run.id)
        if row is None or row.lease_owner != run.lease_owner:
            raise CollectionInProgressError(run.id)
        return row

    async def find_fresh_completed(
        self,
        provider: str,
        request: CollectionRequest,
        freshness_ttl_seconds: int,
    ) -> CollectionReceipt | None:
        settings_hash = stable_hash(request.settings)
        rows = (
            await m.CollectionRun.filter(
                organization_id=request.organization_id,
                provider=provider,
                capability=request.capability.value,
                operation=request.operation,
                target_ref=request.target_ref,
                site_id=request.site_id,
                page_id=request.page_id,
                source_crawl_session_id=request.source_crawl_session_id,
                settings_hash=settings_hash,
                status="completed",
                deleted_at__isnull=True,
            )
            .order_by("-completed_at")
            .limit(1)
            .all()
        )
        if not rows or rows[0].completed_at is None:
            return None
        completed_at = rows[0].completed_at
        if completed_at < _now() - timedelta(seconds=freshness_ttl_seconds):
            return None
        run = CollectionRun(
            id=str(rows[0].id),
            provider=provider,
            request=request,
            settings_hash=settings_hash,
            idempotency_key=rows[0].idempotency_key,
            status="completed",
            created=False,
            claimed=False,
            lease_owner=rows[0].lease_owner,
            attempt_count=rows[0].attempt_count,
        )
        receipt = await self.receipt_for_run(run)
        age = max(int((_now() - completed_at).total_seconds()), 0)
        return receipt.model_copy(
            update={
                "from_cache": True,
                "cache_age_seconds": age,
                "freshness_ttl_seconds": freshness_ttl_seconds,
            }
        )

    async def start_run(self, provider: str, request: CollectionRequest) -> CollectionRun:
        settings_hash = stable_hash(request.settings)
        key = collection_identity(
            request.organization_id,
            provider,
            request.capability.value,
            request.operation,
            request.target_ref,
            settings_hash,
            request.observation_period,
            site_id=request.site_id,
            page_id=request.page_id,
            source_crawl_session_id=request.source_crawl_session_id,
        )
        if request.force_refresh:
            key = stable_hash([key, "force_refresh", request.request_id or str(uuid4())])
        now = _now()
        lease_owner = str(uuid4())
        lease_expires_at = now + timedelta(seconds=RUN_LEASE_SECONDS)
        # AN ARCHIVED RUN IS ABSENT. A run archived (``deleted_at`` set) was
        # deliberately taken out of reuse — e.g. a billed empty provider answer —
        # yet it still holds its idempotency key (a full UNIQUE index), so the
        # insert below used to lose to it and the same-day request was handed the
        # archived run back as its result. A new request now gets a new run under
        # a SUCCESSOR key derived from the archived run's id: deterministic, so two
        # identical concurrent requests still collapse onto one run, and a chain
        # of archivals keeps walking (bounded).
        for _successor in range(_ARCHIVED_SUCCESSOR_LIMIT):
            archived = await self._archived_holder(key)
            if archived is None:
                break
            key = stable_hash([key, "after_archived", archived])
        else:
            raise RuntimeError(
                f"collection identity {key!r} has {_ARCHIVED_SUCCESSOR_LIMIT} archived runs "
                "in a row; refusing to walk further"
            )
        inserted = await insert_ignore(
            m.CollectionRun,
            {
                "id": str(uuid4()),
                "organization_id": request.organization_id,
                "created_by": request.created_by,
                "provider": provider,
                "capability": request.capability.value,
                "operation": request.operation,
                "trigger": request.trigger.value,
                "status": "processing",
                "target_ref": request.target_ref,
                "site_id": request.site_id,
                "page_id": request.page_id,
                "source_crawl_session_id": request.source_crawl_session_id,
                "observation_period": request.observation_period,
                "settings": request.settings,
                "settings_hash": settings_hash,
                "idempotency_key": key,
                "credential_reference_id": request.credential_reference_id,
                "credential_reference_kind": request.credential_reference_kind.value,
                "request_id": request.request_id,
                "execution_id": str(request.execution_id) if request.execution_id else None,
                "attempt_count": 1,
                "lease_owner": lease_owner,
                "lease_expires_at": lease_expires_at,
                "requested_at": now,
                "started_at": now,
                "created_at": now,
                "updated_at": now,
            },
            on_conflict=["idempotency_key"],
        )
        if inserted is not None:
            return CollectionRun(
                id=str(inserted["id"]),
                provider=provider,
                request=request,
                settings_hash=settings_hash,
                idempotency_key=key,
                status="processing",
                created=True,
                claimed=True,
                lease_owner=lease_owner,
                lease_expires_at=lease_expires_at,
                attempt_count=1,
            )

        row = await m.CollectionRun.get(idempotency_key=key)
        claimed = False
        reclaim_filters: dict[str, Any] | None = None
        if row.status == "failed":
            reclaim_filters = {
                "id": str(row.id),
                "status": "failed",
                "lease_owner": row.lease_owner,
            }
        elif row.status == "processing" and row.lease_expires_at is not None:
            if row.lease_expires_at < now:
                reclaim_filters = {
                    "id": str(row.id),
                    "status": "processing",
                    "lease_owner": row.lease_owner,
                    "lease_expires_at__lt": now,
                }
        elif (
            row.status == "processing"
            and row.lease_expires_at is None
            and row.updated_at < now - timedelta(seconds=RUN_LEASE_SECONDS)
        ):
            reclaim_filters = {
                "id": str(row.id),
                "status": "processing",
                "lease_owner": row.lease_owner,
                "lease_expires_at__isnull": True,
                "updated_at__lt": now - timedelta(seconds=RUN_LEASE_SECONDS),
            }
        if reclaim_filters is not None:
            result = await m.CollectionRun.update_where(
                reclaim_filters,
                status="processing",
                error=None,
                lease_owner=lease_owner,
                lease_expires_at=lease_expires_at,
                attempt_count=row.attempt_count + 1,
                execution_id=str(request.execution_id) if request.execution_id else None,
                request_id=request.request_id,
                credential_reference_id=request.credential_reference_id,
                started_at=now,
                updated_at=now,
            )
            if result.rows_affected == 1:
                row = await m.CollectionRun.get(use_cache=False, idempotency_key=key)
                claimed = True
            else:
                row = await m.CollectionRun.get(use_cache=False, idempotency_key=key)
        elif (
            request.resume_existing
            and row.status == "processing"
            and request.execution_id is not None
            and str(row.execution_id or "") == str(request.execution_id)
        ):
            row = await row.update(
                lease_owner=lease_owner,
                lease_expires_at=lease_expires_at,
                attempt_count=row.attempt_count + 1,
                updated_at=now,
            )
            claimed = True
        return CollectionRun(
            id=str(row.id),
            provider=provider,
            request=request,
            settings_hash=settings_hash,
            idempotency_key=key,
            status=row.status,
            created=False,
            claimed=claimed,
            lease_owner=row.lease_owner,
            lease_expires_at=row.lease_expires_at,
            attempt_count=row.attempt_count,
        )

    @staticmethod
    async def _archived_holder(key: str) -> str | None:
        """The id of an ARCHIVED run holding ``key``, or None (no run, or a live one)."""
        rows = await (
            m.CollectionRun.filter(idempotency_key=key, deleted_at__isnull=False).limit(1).all()
        )
        return str(rows[0].id) if rows else None

    async def renew_lease(self, run: CollectionRun) -> None:
        expires_at = _now() + timedelta(seconds=RUN_LEASE_SECONDS)
        result = await m.CollectionRun.update_where(
            {
                "id": run.id,
                "status": "processing",
                "lease_owner": run.lease_owner,
            },
            lease_expires_at=expires_at,
            updated_at=_now(),
        )
        if result.rows_affected != 1:
            raise CollectionInProgressError(run.id)
        run.lease_expires_at = expires_at

    async def _merge_provider_calls_batch(
        self, run: CollectionRun, records: list[ProviderCallRecord]
    ) -> None:
        """Insert/merge a WHOLE batch of provider-call evidence rows in ONE
        round trip (DEF-11 — "provider tasks/calls persisted in per-record
        loops"), never insert-ignore a retry's improved request/cost/metadata
        away (DEF-19, 2026-07-23).

        A retried provider call reuses the same ``(run_id, provider_call_key)``
        identity (the run is lease-fenced to one active writer). The conflict
        SET clause below is expressed entirely in SQL — ``GREATEST``/
        ``COALESCE``/jsonb ``||`` referencing the table's OWN old value versus
        ``EXCLUDED`` — so the "never regress a field" merge (prefer non-null
        over null, the larger request count and cost, the union of metadata
        keys with new values winning on collision, the later fetched_at) runs
        entirely inside ONE ``INSERT ... ON CONFLICT DO UPDATE`` statement —
        no read-then-write round trip at all, batched or not. Two records in
        the SAME batch sharing a ``provider_call_key`` are pre-merged in
        Python first (a single multi-row ``ON CONFLICT DO UPDATE`` cannot
        affect the same target row twice)."""
        if not records:
            return
        merged_by_key: dict[str, ProviderCallRecord] = {}
        for record in records:
            existing = merged_by_key.get(record.provider_call_key)
            if existing is None:
                merged_by_key[record.provider_call_key] = record
                continue
            merged_by_key[record.provider_call_key] = record.model_copy(
                update={
                    "external_task_id": record.external_task_id or existing.external_task_id,
                    "request_count": max(existing.request_count or 0, record.request_count or 0),
                    "reported_cost": (
                        record.reported_cost
                        if record.reported_cost is not None
                        else existing.reported_cost
                    ),
                    "estimated_cost": (
                        record.estimated_cost
                        if record.estimated_cost is not None
                        else existing.estimated_cost
                    ),
                    "currency": record.currency or existing.currency,
                    "fetched_at": max(existing.fetched_at, record.fetched_at),
                    "metadata": {**(existing.metadata or {}), **(record.metadata or {})},
                }
            )
        table = m.ProviderCall._meta.qualified_table_name
        rows = [
            {
                "id": str(uuid4()),
                "run_id": run.id,
                "provider_call_key": record.provider_call_key,
                "external_task_id": record.external_task_id,
                "request_count": record.request_count,
                "reported_cost": record.reported_cost,
                "estimated_cost": record.estimated_cost,
                "currency": record.currency,
                "fetched_at": record.fetched_at,
                "metadata": record.metadata,
            }
            for record in merged_by_key.values()
        ]
        await bulk_upsert_increment(
            m.ProviderCall,
            rows,
            on_conflict=["run_id", "provider_call_key"],
            set_fields={
                "external_task_id": Coalesce(
                    Excluded("external_task_id"), F(f"{table}.external_task_id")
                ),
                "request_count": Greatest(
                    Coalesce(F(f"{table}.request_count"), 0),
                    Coalesce(Excluded("request_count"), 0),
                ),
                "reported_cost": Coalesce(Excluded("reported_cost"), F(f"{table}.reported_cost")),
                "estimated_cost": Coalesce(
                    Excluded("estimated_cost"), F(f"{table}.estimated_cost")
                ),
                "currency": Coalesce(Excluded("currency"), F(f"{table}.currency")),
                "fetched_at": Greatest(F(f"{table}.fetched_at"), Excluded("fetched_at")),
                "metadata": JsonbConcat(F(f"{table}.metadata"), Excluded("metadata")),
            },
        )

    async def persist_raw(
        self, run: CollectionRun, response: ProviderResponse, envelope: RawPayloadEnvelope
    ) -> RawPayloadReceipt:
        run_row = await self._claimed_row(run)
        now = _now()
        inserted = await insert_ignore(
            m.RawPayload,
            {
                "id": str(uuid4()),
                "run_id": run.id,
                "checksum": envelope.checksum,
                "size_bytes": envelope.size_bytes,
                "content_type": envelope.content_type,
                "payload": envelope.payload,
                "cloud_file_id": envelope.cloud_file_id,
                "provider_schema_version": response.provider_schema_version,
                "external_task_id": response.external_task_id,
                "fetched_at": response.fetched_at,
                "offload_error": envelope.offload_error,
                "created_at": now,
            },
            on_conflict=["run_id", "checksum"],
        )
        if inserted is not None:
            payload_id = str(inserted["id"])
            created = True
        else:
            existing = await m.RawPayload.get(run_id=run.id, checksum=envelope.checksum)
            await _promote_existing_raw_payload_offload(existing, envelope)
            payload_id = str(existing.id)
            created = False

        call_records = response.call_records or [
            ProviderCallRecord(
                provider_call_key=response.external_task_id
                or stable_hash([run.provider, run.id, response.fetched_at, envelope.checksum]),
                external_task_id=response.external_task_id,
                request_count=response.request_count,
                reported_cost=response.reported_cost,
                estimated_cost=response.estimated_cost,
                currency=response.currency,
                fetched_at=response.fetched_at,
            )
        ]
        await self._merge_provider_calls_batch(run, call_records)
        run_calls = await m.ProviderCall.filter_items(run_id=run.id)
        reported = [call.reported_cost for call in run_calls]
        estimated = [call.estimated_cost for call in run_calls]
        await run_row.update(
            request_count=sum(call.request_count for call in run_calls),
            reported_cost=(
                sum(value for value in reported if value is not None)
                if reported and all(value is not None for value in reported)
                else None
            ),
            estimated_cost=(
                sum(value for value in estimated if value is not None)
                if estimated and all(value is not None for value in estimated)
                else None
            ),
            updated_at=now,
        )
        return RawPayloadReceipt(id=payload_id, checksum=envelope.checksum, created=created)

    async def _ensure_location_codes(self, location_codes: set[int]) -> None:
        """DEF-9: ``seo.keyword_market.location_code`` is FK'd into
        ``seo.location.location_code`` (the one location model) — get-or-create
        the identity rows before the market upsert so a provider code this
        platform has never seen before doesn't violate the constraint. A
        code-only row (no geo tuple) is a legitimate ``seo.location`` shape.

        Batched: ONE idempotent bulk insert for every distinct code in the
        batch, instead of one ``get_or_create`` round trip per observation
        (DEF-11)."""
        if not location_codes:
            return
        now = _now()
        rows = [
            {"id": str(uuid4()), "location_code": code, "created_at": now}
            for code in location_codes
        ]
        await bulk_insert_ignore(m.Location, rows, on_conflict=["location_code"])

    async def _persist_keyword_market_observations_batch(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        observations: list[KeywordMarketObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        """WS-8/DEF-21: append-only ``seo.keyword_market_observation`` history,
        ONE round trip via the same dedup-batch helper every other observation
        table uses (never a duplicate row for a replayed run)."""
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "keyword_id": observation.keyword_id,
                    "location_code": observation.location_code,
                    "observed_at": observation.observed_at,
                    "search_volume": observation.search_volume,
                    "competition": observation.competition,
                    "competition_index": observation.competition_index,
                    "cpc": observation.cpc,
                    "low_top_of_page_bid": observation.low_top_of_page_bid,
                    "high_top_of_page_bid": observation.high_top_of_page_bid,
                    "monthly_searches": [
                        item.model_dump() for item in observation.monthly_searches
                    ],
                    "metrics_task_id": observation.metrics_task_id,
                    "raw": observation.raw,
                }
            )
        return await self._persist_dedup_batch(m.KeywordMarketObservation, rows, dedup_keys)

    async def _upsert_keyword_markets_batch(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        observations: list[KeywordMarketObservation],
        base: dict[str, Any],
    ) -> list[tuple[str, bool]]:
        """Persist the append-only history (WS-8/DEF-21) for the whole batch,
        then derive/update the ``seo.keyword_market`` current-projection cache
        in ONE round trip (plus one location-identity round trip and one
        stats-write round trip) instead of the previous per-observation
        upsert -> reload -> update N+1 (DEF-11).

        Precedence (kept deliberately simple, no framework — handoff item 8):
        the cache's scalar fields (search_volume, cpc, competition, ...) are
        overwritten ONLY when this observation's ``observed_at`` is >= the
        cache's current ``last_observed_at`` (or the cache has none yet) —
        a stale replay or an out-of-order older provider report can never
        clobber fresher already-cached data. ``monthly_searches`` keeps
        merging unconditionally (a monthly time series only grows — additive,
        never a "whose data is right" question). The winning observation's
        provider/id/observed_at are stamped onto ``source_provider`` /
        ``source_observation_id`` / ``last_observed_at`` so the cache always
        records which observation it reflects.

        Two or more observations in the SAME batch for the identical
        ``(keyword_id, location_code)`` are pre-merged in Python (a single
        multi-row ``... ON CONFLICT DO UPDATE`` cannot affect the same target
        row twice); the group's WINNER (by ``observed_at``, ties keep batch
        order) supplies the scalar cache fields exactly like the cross-call
        guard above.

        Returns ``(keyword_market_id, created)`` in the SAME order as
        ``observations``.
        """
        if not observations:
            return []
        await self._ensure_location_codes({obs.location_code for obs in observations})
        history_ids, _history_created = await self._persist_keyword_market_observations_batch(
            run, raw, observations, base
        )
        now = _now()
        table = m.KeywordMarket._meta.qualified_table_name

        group_order: list[tuple[str, int]] = []
        groups: dict[tuple[str, int], list[tuple[KeywordMarketObservation, str]]] = {}
        for obs, history_id in zip(observations, history_ids, strict=True):
            key = (obs.keyword_id, obs.location_code)
            if key not in groups:
                group_order.append(key)
                groups[key] = []
            groups[key].append((obs, history_id))

        rows: list[dict[str, Any]] = []
        for key in group_order:
            group = groups[key]
            monthly: list[dict[str, Any]] = []
            for obs, _hid in group:
                monthly = merge_monthly(
                    monthly, [item.model_dump() for item in obs.monthly_searches]
                )
            # The volume fields' winner is the newest observation that carries
            # volume metrics at all. A difficulty-only observation (Labs
            # bulk_keyword_difficulty) is never a volume observation: were it the
            # winner, its None volume/CPC/raw would overwrite the stored ones
            # under the newer-or-equal guard below. With no volume observation in
            # the group, the row's last_observed_at stays NULL, which the guard
            # reads as "not authoritative" against any stored value.
            carries_volume = [pair for pair in group if _carries_volume(pair[0])]
            winner, winner_history_id = max(
                carries_volume or group, key=lambda pair: pair[0].observed_at
            )
            volume_observed_at = winner.observed_at if carries_volume else None
            # Difficulty has its OWN winner: the newest observation in the group
            # that carries difficulty at all. A volume-only observation is never
            # a difficulty observation, so it can never null a stored score.
            scored = [pair for pair in group if pair[0].difficulty is not None]
            difficulty_winner = (
                max(scored, key=lambda pair: pair[0].observed_at)[0] if scored else None
            )
            rows.append(
                {
                    "id": str(uuid4()),
                    # The keyword x location metrics cache is shared by every
                    # site: a PLATFORM row, named — never a column default.
                    "organization_id": SYSTEM_ORGANIZATION_ID,
                    "keyword_id": winner.keyword_id,
                    "location_code": winner.location_code,
                    "search_volume": winner.search_volume,
                    "competition": winner.competition,
                    "competition_index": winner.competition_index,
                    "cpc": winner.cpc,
                    "low_top_of_page_bid": winner.low_top_of_page_bid,
                    "high_top_of_page_bid": winner.high_top_of_page_bid,
                    "monthly_searches": monthly,
                    "metrics_fetched_at": now,
                    "metrics_task_id": winner.metrics_task_id,
                    "raw": winner.raw,
                    "source_provider": run.provider,
                    "source_observation_id": winner_history_id,
                    "last_observed_at": volume_observed_at,
                    "difficulty": (
                        difficulty_winner.difficulty if difficulty_winner is not None else None
                    ),
                    "difficulty_source": (
                        run.request.operation if difficulty_winner is not None else None
                    ),
                    "difficulty_observed_at": (
                        difficulty_winner.observed_at if difficulty_winner is not None else None
                    ),
                    "created_at": now,
                    "updated_at": now,
                }
            )

        # "Newer-or-equal observed_at wins" — evaluated per row against the
        # PRE-EXISTING cache value, so an older/out-of-order report can never
        # clobber a fresher one already cached under a different provider.
        def _authoritative():
            current = F(f"{table}.last_observed_at")
            return Is(current, None) | ColumnComparison(
                Excluded("last_observed_at"),
                ">=",
                current,
            )

        def _guarded(col: str) -> Case:
            return Case(
                When(_authoritative(), then=Excluded(col)),
                default=F(f"{table}.{col}"),
            )

        # Difficulty's OWN newer-or-equal guard (OPENSEO-TOOLS-SPEC §4.1): only an
        # incoming row that carries a difficulty observation may write, and only
        # when it is at least as new as the stored one. Independent of
        # last_observed_at, so a newer volume-only refresh never nulls it and an
        # older Labs replay never overwrites a fresher score.
        def _difficulty_authoritative():
            current = F(f"{table}.difficulty_observed_at")
            incoming = Excluded("difficulty_observed_at")
            return Is(incoming, None, negated=True) & (
                Is(current, None) | ColumnComparison(incoming, ">=", current)
            )

        def _difficulty_guarded(col: str) -> Case:
            return Case(
                When(_difficulty_authoritative(), then=Excluded(col)),
                default=F(f"{table}.{col}"),
            )

        upserted = await bulk_upsert_increment(
            m.KeywordMarket,
            rows,
            on_conflict=["keyword_id", "location_code"],
            set_fields={
                "search_volume": _guarded("search_volume"),
                "competition": _guarded("competition"),
                "competition_index": _guarded("competition_index"),
                "cpc": _guarded("cpc"),
                "low_top_of_page_bid": _guarded("low_top_of_page_bid"),
                "high_top_of_page_bid": _guarded("high_top_of_page_bid"),
                "monthly_searches": DbFunction(
                    "seo.fn_merge_monthly",
                    F(f"{table}.monthly_searches"),
                    Excluded("monthly_searches"),
                ),
                "metrics_fetched_at": Now(),
                "metrics_task_id": _guarded("metrics_task_id"),
                "raw": _guarded("raw"),
                "source_provider": _guarded("source_provider"),
                "source_observation_id": _guarded("source_observation_id"),
                "last_observed_at": Case(
                    When(_authoritative(), then=Excluded("last_observed_at")),
                    default=F(f"{table}.last_observed_at"),
                ),
                "difficulty": _difficulty_guarded("difficulty"),
                "difficulty_source": _difficulty_guarded("difficulty_source"),
                "difficulty_observed_at": _difficulty_guarded("difficulty_observed_at"),
                "updated_at": Now(),
            },
            returning=True,
        )
        by_key: dict[tuple[str, int], dict[str, Any]] = {
            (str(row["keyword_id"]), int(row["location_code"])): row for row in upserted
        }

        stats_rows: list[dict[str, Any]] = []
        result_by_key: dict[tuple[str, int], tuple[str, bool]] = {}
        for key in group_order:
            row = by_key[key]
            merged = row["monthly_searches"]
            if isinstance(merged, str):
                merged = json.loads(merged)
            stats = compute_market_stats(merged if isinstance(merged, list) else [])
            market_id = str(row["id"])
            result_by_key[key] = (market_id, bool(row["_matrx_inserted"]))
            stats_rows.append(
                {
                    "id": market_id,
                    "demand_trajectory": stats.demand_trajectory,
                    "growth_rate": stats.growth_rate,
                    "seasonality_index": stats.seasonality_index,
                    "data_months": stats.data_months,
                    "updated_at": _now(),
                }
            )
        if stats_rows:
            await bulk_update_by_pk(
                m.KeywordMarket,
                stats_rows,
                casts={
                    "id": "uuid",
                    "demand_trajectory": "text",
                    "growth_rate": "numeric",
                    "seasonality_index": "numeric",
                    "data_months": "smallint",
                    "updated_at": "timestamptz",
                },
            )

        results: list[tuple[str, bool]] = []
        seen_created: set[tuple[str, int]] = set()
        for obs in observations:
            key = (obs.keyword_id, obs.location_code)
            market_id, inserted = result_by_key[key]
            created = inserted and key not in seen_created
            seen_created.add(key)
            results.append((market_id, created))
        return results

    async def _persist_dedup_batch(
        self,
        model_cls: type,
        rows: list[dict[str, Any]],
        dedup_keys: list[str],
    ) -> tuple[list[str], list[bool]]:
        """Batch insert-if-absent rows keyed on ``dedup_key`` in ONE round trip
        (``ON CONFLICT (dedup_key) DO NOTHING ... RETURNING *``), plus at most
        one reload for whichever keys already existed — instead of an
        ``insert_ignore``-per-observation loop (DEF-11). Duplicate
        ``dedup_key`` values WITHIN the batch are safe for ``DO NOTHING``
        (Postgres skips the later duplicate against the row the same
        statement just inserted).

        Returns ``(ids, created_flags)`` in the SAME order as ``dedup_keys``/
        ``rows`` — only the FIRST occurrence of a freshly-created key is
        flagged ``created``, matching the sequential-loop semantics a caller
        that hands in two identical observations would have seen."""
        if not rows:
            return [], []
        inserted_rows = await bulk_insert_ignore(
            model_cls, rows, on_conflict=["dedup_key"], returning=True
        )
        ids_by_key: dict[str, str] = {str(r["dedup_key"]): str(r["id"]) for r in inserted_rows}
        created_keys = set(ids_by_key)
        missing = [key for key in dedup_keys if key not in ids_by_key]
        if missing:
            persisted = await model_cls.filter(dedup_key__in=list(dict.fromkeys(missing))).values(
                "id", "dedup_key"
            )
            for row in persisted:
                ids_by_key[str(row["dedup_key"])] = str(row["id"])
        still_missing = [key for key in dedup_keys if key not in ids_by_key]
        if still_missing:
            raise RuntimeError(
                f"bulk persistence could not reload {len(still_missing)} landed "
                f"{model_cls.__name__} observations"
            )
        seen: set[str] = set()
        created_flags: list[bool] = []
        for key in dedup_keys:
            created_flags.append(key in created_keys and key not in seen)
            seen.add(key)
        return [ids_by_key[key] for key in dedup_keys], created_flags

    async def _persist_serp_snapshots_batch(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        observations: list[SerpSnapshotObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "keyword_id": observation.keyword_id,
                    "rank_target_id": observation.rank_target_id,
                    "location_id": observation.location_id,
                    "engine": observation.engine,
                    "language": observation.language,
                    "device": observation.device,
                    "search_type": observation.search_type,
                    "observed_at": observation.observed_at,
                    "query_settings": observation.query_settings,
                    "serp_features": observation.serp_features,
                }
            )
        ids, created_flags = await self._persist_dedup_batch(m.SerpSnapshot, rows, dedup_keys)

        child_rows: list[dict[str, Any]] = []
        for observation, snapshot_id, created in zip(observations, ids, created_flags):
            if not created:
                continue
            for result in observation.results:
                child_rows.append(
                    {
                        "id": str(uuid4()),
                        "snapshot_id": snapshot_id,
                        "result_type": result.result_type,
                        "organic_rank": result.organic_rank,
                        "absolute_rank": result.absolute_rank,
                        "url": result.url,
                        "domain": result.domain,
                        "title": result.title,
                        "snippet": result.snippet,
                        "extras": result.extras,
                    }
                )
        if child_rows:
            await bulk_insert_ignore(
                m.SerpResult,
                child_rows,
                on_conflict=["snapshot_id", "result_type", "absolute_rank"],
            )
        return ids, created_flags

    async def _persist_rank_observations_batch(
        self,
        run: CollectionRun,
        observations: list[RankObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "keyword_id": observation.keyword_id,
                    "rank_target_id": observation.rank_target_id,
                    "location_id": observation.location_id,
                    "engine": observation.engine,
                    "language": observation.language,
                    "device": observation.device,
                    "search_type": observation.search_type,
                    "matched_domain": observation.matched_domain,
                    "matched_url": observation.matched_url,
                    "organic_rank": observation.organic_rank,
                    "absolute_rank": observation.absolute_rank,
                    "result_type": observation.result_type,
                    "match_rule": observation.match_rule,
                    "observed_at": observation.observed_at,
                    "query_settings": observation.query_settings,
                    "serp_features": observation.serp_features,
                    "title": observation.title,
                    "snippet": observation.snippet,
                    "extras": observation.extras,
                }
            )
        return await self._persist_dedup_batch(m.RankObservation, rows, dedup_keys)

    async def _persist_web_analytics_batch(
        self,
        run: CollectionRun,
        observations: list[WebAnalyticsObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "site_id": observation.site_id,
                    "page_id": observation.page_id,
                    "date": observation.date,
                    "source": observation.source,
                    "medium": observation.medium,
                    "channel": observation.channel,
                    "campaign": observation.campaign,
                    "device": observation.device,
                    "landing_page": observation.landing_page,
                    "currency_code": observation.currency_code,
                    "property_timezone": observation.property_timezone,
                    "sessions": observation.sessions,
                    "users": observation.users,
                    "engaged_sessions": observation.engaged_sessions,
                    "views": observation.views,
                    "engagement_rate": observation.engagement_rate,
                    "key_events": observation.key_events,
                    "conversions": observation.conversions,
                    "revenue": observation.revenue,
                    "extras": observation.extras,
                }
            )
        return await self._persist_dedup_batch(m.WebAnalyticsDaily, rows, dedup_keys)

    async def _persist_page_performance_batch(
        self,
        run: CollectionRun,
        observations: list[PagePerformanceObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "page_id": observation.page_id,
                    "site_id": observation.site_id,
                    "strategy": observation.strategy,
                    "performance_score": observation.performance_score,
                    "accessibility_score": observation.accessibility_score,
                    "best_practices_score": observation.best_practices_score,
                    "seo_score": observation.seo_score,
                    "lighthouse": observation.lighthouse,
                    "crux": observation.crux,
                    "diagnostics": observation.diagnostics,
                    "observed_at": observation.observed_at,
                }
            )
        return await self._persist_dedup_batch(m.PagePerformance, rows, dedup_keys)

    async def _persist_backlink_snapshots_batch(
        self,
        run: CollectionRun,
        observations: list[BacklinkSnapshotObservation],
        base: dict[str, Any],
    ) -> tuple[list[str], list[bool]]:
        rows: list[dict[str, Any]] = []
        dedup_keys: list[str] = []
        for observation in observations:
            if run.request.site_id is None:
                raise ValueError("backlink persistence requires collection_run.site_id")
            if observation.site_id != run.request.site_id:
                raise ValueError("backlink observation site_id must match collection run")
            if observation.page_id != run.request.page_id:
                raise ValueError("backlink observation page_id must match collection run")
            dedup_key = _observation_dedup_key(
                run.idempotency_key, base["organization_id"], run.provider, observation
            )
            dedup_keys.append(dedup_key)
            rows.append(
                {
                    **base,
                    "id": str(uuid4()),
                    "dedup_key": dedup_key,
                    "site_id": observation.site_id,
                    "page_id": observation.page_id,
                    "dataset": observation.dataset,
                    "target": observation.target,
                    "target_type": observation.target_type,
                    "total_backlinks": observation.total_backlinks,
                    "referring_domains": observation.referring_domains,
                    "referring_ips": observation.referring_ips,
                    "referring_subnets": observation.referring_subnets,
                    "dofollow_backlinks": observation.dofollow_backlinks,
                    "nofollow_backlinks": observation.nofollow_backlinks,
                    "new_backlinks": observation.new_backlinks,
                    "lost_backlinks": observation.lost_backlinks,
                    "broken_backlinks": observation.broken_backlinks,
                    "rank_score": observation.rank_score,
                    "spam_score": observation.spam_score,
                    "observed_at": observation.observed_at,
                    "extras": observation.extras,
                }
            )
        ids, created_flags = await self._persist_dedup_batch(m.BacklinkSnapshot, rows, dedup_keys)

        backlink_rows: list[dict[str, Any]] = []
        dimension_rows: list[dict[str, Any]] = []
        for observation, snapshot_id, created in zip(observations, ids, created_flags):
            if not created:
                continue
            backlink_ids = await upsert_current_backlinks(
                organization_id=base["organization_id"],
                created_by=base["created_by"],
                site_id=observation.site_id,
                page_id=observation.page_id,
                provider=run.provider,
                snapshot_id=snapshot_id,
                items=observation.backlinks,
            )
            for backlink in observation.backlinks:
                backlink_id = backlink_ids[
                    backlink_identity_key(
                        observation.site_id,
                        backlink.source_url,
                        backlink.target_url,
                    )
                ]
                child_dedup = stable_hash(
                    {
                        "snapshot_id": snapshot_id,
                        "backlink_id": backlink_id,
                        "source_url": backlink.source_url,
                        "target_url": backlink.target_url,
                        "first_seen_at": backlink.first_seen_at,
                        "last_seen_at": backlink.last_seen_at,
                        "state": backlink.state,
                    }
                )
                backlink_rows.append(
                    {
                        **base,
                        "id": str(uuid4()),
                        "snapshot_id": snapshot_id,
                        "backlink_id": backlink_id,
                        "dedup_key": child_dedup,
                        "site_id": observation.site_id,
                        "page_id": observation.page_id,
                        "source_url": backlink.source_url,
                        "source_domain": backlink.source_domain,
                        "target_url": backlink.target_url,
                        "anchor_text": backlink.anchor_text,
                        "link_type": backlink.link_type,
                        "is_dofollow": backlink.is_dofollow,
                        "first_seen_at": backlink.first_seen_at,
                        "last_seen_at": backlink.last_seen_at,
                        "lost_at": backlink.lost_at,
                        "state": backlink.state,
                        "source_rank": backlink.source_rank,
                        "domain_rank": backlink.domain_rank,
                        "spam_score": backlink.spam_score,
                        "extras": backlink.extras,
                    }
                )
            for dimension in observation.dimensions:
                child_dedup = stable_hash(
                    {
                        "snapshot_id": snapshot_id,
                        "dimension_kind": dimension.dimension_kind,
                        "dimension_key": dimension.dimension_key,
                    }
                )
                dimension_rows.append(
                    {
                        **base,
                        "id": str(uuid4()),
                        "snapshot_id": snapshot_id,
                        "dedup_key": child_dedup,
                        "site_id": observation.site_id,
                        "dimension_kind": dimension.dimension_kind,
                        "dimension_key": dimension.dimension_key,
                        "label": dimension.label,
                        "url": dimension.url,
                        "backlinks": dimension.backlinks,
                        "referring_domains": dimension.referring_domains,
                        "rank_score": dimension.rank_score,
                        "spam_score": dimension.spam_score,
                        "first_seen_at": dimension.first_seen_at,
                        "last_seen_at": dimension.last_seen_at,
                        "extras": dimension.extras,
                    }
                )
        if backlink_rows:
            await bulk_insert_ignore(
                m.BacklinkObservation, backlink_rows, on_conflict=["dedup_key"]
            )
        if dimension_rows:
            await bulk_insert_ignore(
                m.BacklinkDimensionSnapshot, dimension_rows, on_conflict=["dedup_key"]
            )
        return ids, created_flags

    async def persist_observations(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        observations: list[SeoObservation],
    ) -> UpsertReceipt:
        await self._claimed_row(run)
        if not observations:
            return UpsertReceipt()
        if all(isinstance(item, LinkGapObservation) for item in observations):
            return await self._persist_link_gaps(run, observations)  # type: ignore[arg-type]
        if all(isinstance(item, SerpProspectObservation) for item in observations):
            return await self._persist_serp_prospects(run, observations)  # type: ignore[arg-type]
        if all(
            isinstance(observation, SearchPerformanceObservation) for observation in observations
        ):
            return await self._persist_search_performance_batch(run, raw, observations)

        organization_id = run.request.organization_id
        created_by = run.request.created_by
        now = _now()
        base = {
            "organization_id": organization_id,
            "created_by": created_by,
            "run_id": run.id,
            "raw_payload_id": raw.id,
            "provider": run.provider,
            "created_at": now,
        }

        # Partition by observation kind, keeping each item's ORIGINAL index so
        # the returned receipt preserves input order across the mixed batch —
        # each kind is then persisted with ONE (or a small constant number of)
        # round trip(s) regardless of how many observations of that kind are
        # in the batch (DEF-11).
        by_kind: dict[type, list[int]] = {}
        for index, observation in enumerate(observations):
            kind_key = type(observation)
            if kind_key not in (
                KeywordMarketObservation,
                SerpSnapshotObservation,
                RankObservation,
                SearchPerformanceObservation,
                WebAnalyticsObservation,
                PagePerformanceObservation,
                BacklinkSnapshotObservation,
            ):
                raise NotImplementedError(
                    f"SEO observation kind {observation.kind!r} has no seo.* table — "
                    "persisting it requires a schema addition, not a silent skip"
                )
            by_kind.setdefault(kind_key, []).append(index)

        ids: list[str | None] = [None] * len(observations)
        created_flags: list[bool] = [False] * len(observations)

        async def _apply(
            indices: list[int], batch_ids: list[str], batch_created: list[bool]
        ) -> None:
            for offset, index in enumerate(indices):
                ids[index] = batch_ids[offset]
                created_flags[index] = batch_created[offset]

        if KeywordMarketObservation in by_kind:
            indices = by_kind[KeywordMarketObservation]
            results = await self._upsert_keyword_markets_batch(
                run,
                raw,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, [r[0] for r in results], [r[1] for r in results])

        if SerpSnapshotObservation in by_kind:
            indices = by_kind[SerpSnapshotObservation]
            batch_ids, batch_created = await self._persist_serp_snapshots_batch(
                run,
                raw,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, batch_ids, batch_created)

        if RankObservation in by_kind:
            indices = by_kind[RankObservation]
            batch_ids, batch_created = await self._persist_rank_observations_batch(
                run,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, batch_ids, batch_created)

        if SearchPerformanceObservation in by_kind:
            indices = by_kind[SearchPerformanceObservation]
            sub_receipt = await self._persist_search_performance_batch(
                run,
                raw,
                [observations[i] for i in indices],  # type: ignore[misc]
            )
            sub_created = [False] * len(indices)
            for offset in range(sub_receipt.created):
                sub_created[offset] = True
            await _apply(indices, sub_receipt.observation_ids, sub_created)

        if WebAnalyticsObservation in by_kind:
            indices = by_kind[WebAnalyticsObservation]
            batch_ids, batch_created = await self._persist_web_analytics_batch(
                run,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, batch_ids, batch_created)

        if PagePerformanceObservation in by_kind:
            indices = by_kind[PagePerformanceObservation]
            batch_ids, batch_created = await self._persist_page_performance_batch(
                run,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, batch_ids, batch_created)

        if BacklinkSnapshotObservation in by_kind:
            indices = by_kind[BacklinkSnapshotObservation]
            batch_ids, batch_created = await self._persist_backlink_snapshots_batch(
                run,
                [observations[i] for i in indices],
                base,  # type: ignore[misc]
            )
            await _apply(indices, batch_ids, batch_created)

        assert all(item_id is not None for item_id in ids)
        return UpsertReceipt(
            created=sum(created_flags),
            existing=len(observations) - sum(created_flags),
            observation_ids=[str(item_id) for item_id in ids],
        )

    async def _persist_link_gaps(
        self, run: CollectionRun, observations: list[LinkGapObservation]
    ) -> UpsertReceipt:
        """Upsert current domain opportunities and replace their match evidence."""
        now = _now()
        receipt = UpsertReceipt()
        for observation in observations:
            if observation.site_id != run.request.site_id:
                raise ValueError("link-gap observation site_id must match collection run")
            competitors = await m.Competitor.filter(site_id=observation.site_id).all()
            by_domain = {
                str(row.normalized_domain or "").lower().removeprefix("www."): row
                for row in competitors
            }
            page_opportunities: dict[tuple[str, str], m.CompetitorOpportunity] = {}
            if run.request.page_id:
                from .rank_matching import canonicalize_rank_url

                accepted = await m.CompetitorOpportunity.filter(
                    site_id=observation.site_id,
                    target_page_id=run.request.page_id,
                    status="accepted",
                ).all()
                for opportunity in accepted:
                    competitor_url = canonicalize_rank_url(str(opportunity.competitor_url or ""))
                    if opportunity.competitor_id and competitor_url:
                        page_opportunities[(str(opportunity.competitor_id), competitor_url)] = (
                            opportunity
                        )
            for domain in observation.domains:
                if domain.match_count < 2:
                    continue
                existing = await m.LinkGapDomain.filter(
                    site_id=observation.site_id, normalized_domain=domain.normalized_domain
                ).first()
                values = {
                    "display_domain": domain.display_domain,
                    "match_count": domain.match_count,
                    "domain_rank": domain.domain_rank,
                    "spam_score": domain.spam_score,
                    "total_backlinks": domain.total_backlinks,
                    "referring_domains": domain.referring_domains,
                    "first_seen_at": domain.first_seen_at,
                    "last_seen_at": domain.last_seen_at,
                    "observed_at": observation.observed_at,
                    "latest_run_id": run.id,
                    "provider_metrics": domain.extras,
                    "updated_at": now,
                    **_authority_ranking(domain),
                }
                if existing is None:
                    existing = await m.LinkGapDomain.create(
                        id=str(uuid4()),
                        site_id=observation.site_id,
                        normalized_domain=domain.normalized_domain,
                        organization_id=run.request.organization_id,
                        created_by=run.request.created_by,
                        created_at=now,
                        review_status="pending",
                        **values,
                    )
                    receipt.created += 1
                else:
                    existing = await existing.update(**values)
                    receipt.existing += 1
                receipt.observation_ids.append(str(existing.id))
                for match in domain.matches:
                    key = match.competitor_domain.lower().removeprefix("www.")
                    competitor = by_domain.get(key)
                    if competitor is None or str(competitor.classification_status) != "confirmed":
                        raise ValueError(f"link-gap evidence names unconfirmed competitor {key!r}")
                    if run.request.page_id:
                        from .rank_matching import canonicalize_rank_url

                        target_url = canonicalize_rank_url(str(match.target_url or ""))
                        opportunity = page_opportunities.get((str(competitor.id), target_url))
                        if opportunity is None:
                            raise ValueError(
                                "page link-gap evidence has no human-accepted competitor "
                                f"opportunity for {match.target_url!r}"
                            )
                        explicit = competitor.use_for_link_gap
                        eligible = (
                            bool(explicit)
                            if explicit is not None
                            else (
                                str(competitor.entity_role) == "business"
                                and str(competitor.business_overlap) in {"direct", "adjacent"}
                            )
                        )
                        if not eligible:
                            raise ValueError(
                                f"page link-gap competitor {key!r} is not link-gap eligible"
                            )
                        # `Model.update_or_create` does not exist (measured
                        # live 2026-08-16 on the SERP twin of this code), and
                        # the operations twin would setattr the fresh `id`
                        # over the PK on update. get-or-create + PK-safe
                        # update instead.
                        page_refresh = {
                            "competitor_opportunity_id": str(opportunity.id),
                            "competitor_domain": match.competitor_domain,
                            "backlinks": match.backlinks,
                            "domain_rank": match.domain_rank,
                            "spam_score": match.spam_score,
                            "is_dofollow": match.is_dofollow,
                            "first_seen_at": match.first_seen_at,
                            "last_seen_at": match.last_seen_at,
                            "provider_metrics": match.extras,
                        }
                        page_match_row, page_match_created = await m.LinkGapMatch.get_or_create(
                            link_gap_domain_id=str(existing.id),
                            competitor_id=str(competitor.id),
                            page_id=run.request.page_id,
                            source_url=match.source_url,
                            target_url=match.target_url,
                            defaults={
                                "id": str(uuid4()),
                                "organization_id": run.request.organization_id,
                                "created_by": run.request.created_by,
                                "created_at": now,
                                "updated_at": now,
                                **page_refresh,
                            },
                        )
                        if not page_match_created:
                            await page_match_row.update(updated_at=now, **page_refresh)
                        continue
                    domain_refresh = {
                        "competitor_domain": match.competitor_domain,
                        "source_url": match.source_url,
                        "target_url": match.target_url,
                        "backlinks": match.backlinks,
                        "domain_rank": match.domain_rank,
                        "spam_score": match.spam_score,
                        "first_seen_at": match.first_seen_at,
                        "provider_metrics": {
                            "referring_pages": match.referring_pages,
                            "lost_at": match.lost_at.isoformat() if match.lost_at else None,
                            **match.extras,
                        },
                    }
                    match_row, match_created = await m.LinkGapMatch.get_or_create(
                        link_gap_domain_id=str(existing.id),
                        competitor_id=str(competitor.id),
                        defaults={
                            "id": str(uuid4()),
                            "organization_id": run.request.organization_id,
                            "created_by": run.request.created_by,
                            "created_at": now,
                            "updated_at": now,
                            **domain_refresh,
                        },
                    )
                    if not match_created:
                        await match_row.update(updated_at=now, **domain_refresh)
        return receipt

    async def _persist_serp_prospects(
        self, run: CollectionRun, observations: list[SerpProspectObservation]
    ) -> UpsertReceipt:
        """Upsert SERP opportunities and their query-mention evidence.

        The evidence rows are the source of truth: ``mention_count`` /
        ``best_rank`` / ``variants`` are recomputed from ALL of an
        opportunity's mentions after insert, so overlapping runs with
        different query sets accumulate instead of clobbering each other.

        A row that has already been authority-enriched keeps its metrics and
        score — a SERP re-observation says nothing about the domain's own
        link profile.
        """
        now = _now()
        receipt = UpsertReceipt()
        for observation in observations:
            if observation.site_id != run.request.site_id:
                raise ValueError("serp-prospect observation site_id must match collection run")
            for domain in observation.domains:
                existing = await m.SerpOpportunity.filter(
                    site_id=observation.site_id,
                    normalized_domain=domain.normalized_domain,
                ).first()
                values: dict[str, Any] = {
                    "display_domain": domain.display_domain,
                    "observed_at": observation.observed_at,
                    "latest_run_id": run.id,
                    "updated_at": now,
                }
                if existing is None:
                    unmeasured = score_authority(AuthorityInputs())
                    existing = await m.SerpOpportunity.create(
                        id=str(uuid4()),
                        site_id=observation.site_id,
                        normalized_domain=domain.normalized_domain,
                        organization_id=run.request.organization_id,
                        created_by=run.request.created_by,
                        created_at=now,
                        review_status="pending",
                        mention_count=domain.mention_count,
                        best_rank=domain.best_rank,
                        variants=list(domain.variants),
                        metadata={"matrx_authority": unmeasured.model_dump(mode="json")},
                        **values,
                    )
                    receipt.created += 1
                else:
                    existing = await existing.update(**values)
                    receipt.existing += 1
                receipt.observation_ids.append(str(existing.id))
                for mention in domain.mentions:
                    # NOTE: `Model.update_or_create` does not exist (it cost
                    # this method its first live run, 2026-08-16), and the
                    # operations-module twin setattrs EVERY default — a fresh
                    # `id` in defaults would rewrite the PK on the update
                    # path. get-or-create, then a PK-safe update.
                    refresh = {
                        "variant": mention.variant,
                        "seed_keyword": mention.seed_keyword,
                        "title": mention.title,
                        "snippet": mention.snippet,
                        "rank": mention.rank,
                        "result_type": mention.result_type,
                        "observed_at": observation.observed_at,
                        "run_id": run.id,
                        "extras": mention.extras,
                    }
                    mention_row, mention_created = await m.SerpMention.get_or_create(
                        serp_opportunity_id=str(existing.id),
                        query=mention.query,
                        url=mention.url,
                        defaults={
                            "id": str(uuid4()),
                            "organization_id": run.request.organization_id,
                            "created_by": run.request.created_by,
                            "created_at": now,
                            "updated_at": now,
                            **refresh,
                        },
                    )
                    if not mention_created:
                        await mention_row.update(updated_at=now, **refresh)
                # Evidence is the source of truth for the aggregates.
                all_mentions = await m.SerpMention.filter(
                    serp_opportunity_id=str(existing.id)
                ).all()
                ranks = [int(row.rank) for row in all_mentions if row.rank is not None]
                await existing.update(
                    mention_count=len({str(row.query) for row in all_mentions}),
                    best_rank=min(ranks) if ranks else None,
                    variants=sorted({str(row.variant) for row in all_mentions}),
                    updated_at=now,
                )
        return receipt

    async def _persist_search_performance_batch(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        observations: list[SearchPerformanceObservation],
    ) -> UpsertReceipt:
        now = _now()
        rows, dedup_keys = await asyncio.to_thread(
            _prepare_search_performance_rows, run, raw, observations, now
        )

        # Bounded statements + an honest, bounded retry. WHY (2026-09-26,
        # `seo_collection_failed:gsc:search_performance`): the nightly GSC run
        # wrote each window as ~1,500-row INSERTs (the ORM's 32k bind-param
        # budget / 21 columns) into a 17.7M-row, 20-index table with three
        # parent-lookup triggers per row, and on 2026-09-16 and 2026-09-21 one
        # such statement blew the pool's 10 s command_timeout mid-run — no lock
        # convoy, no correlated timeouts, just one oversized write — failing
        # the whole window. Smaller statements finish well inside the ceiling,
        # and each is `ON CONFLICT (dedup_key) DO NOTHING` keyed on a
        # retry-stable dedup key, so re-issuing one after a timeout can never
        # double-write (the only effect of an ambiguous first attempt is that
        # its rows count as `existing` rather than `created`). Bounded at
        # three attempts and LOUD on every retry (`retry_on_transient`), so a
        # genuinely slow table still fails the run instead of hiding.
        created = 0
        for start in range(0, len(rows), _SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS):
            chunk = rows[start : start + _SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS]

            async def _write(chunk: list[dict[str, Any]] = chunk) -> int | Any:
                return await bulk_insert_ignore(
                    m.SearchPerformanceDaily,
                    chunk,
                    on_conflict=["dedup_key"],
                )

            landed = await retry_on_transient(
                _write,
                attempts=_SEARCH_PERFORMANCE_WRITE_ATTEMPTS,
                base_backoff=1.0,
                jitter_ratio=0.5,
                label=(
                    f"seo.search_performance_daily insert run={run.id} "
                    f"rows[{start}:{start + len(chunk)}]"
                ),
            )
            if not isinstance(landed, int):
                raise RuntimeError(
                    "bulk search performance persistence returned a non-count result"
                )
            created += landed

        unique_keys = list(dict.fromkeys(dedup_keys))
        persisted: list[dict[str, Any]] = []
        for start in range(0, len(unique_keys), _SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS):
            persisted.extend(
                await m.SearchPerformanceDaily.filter(
                    dedup_key__in=unique_keys[start : start + _SEARCH_PERFORMANCE_WRITE_CHUNK_ROWS]
                ).values("id", "dedup_key")
            )
        ids_by_key = {str(row["dedup_key"]): str(row["id"]) for row in persisted}
        missing = [key for key in unique_keys if key not in ids_by_key]
        if missing:
            raise RuntimeError(
                "bulk search performance persistence could not reload "
                f"{len(missing)} landed observations"
            )
        return UpsertReceipt(
            created=created,
            existing=len(observations) - created,
            observation_ids=[ids_by_key[key] for key in dedup_keys],
        )

    async def complete_run(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        receipt: UpsertReceipt,
    ) -> CollectionReceipt:
        row = await self._claimed_row(run)
        now = _now()
        # The run's observation count, written ONCE here — a finished run never changes, and the
        # runs list used to count 17.8M search_performance rows per page to say it again.
        total = (await self._observation_totals([str(run.id)])).get(str(run.id), 0)
        await row.update(
            status="completed",
            error=None,
            lease_owner=None,
            lease_expires_at=None,
            completed_at=now,
            metadata={**(row.metadata if isinstance(row.metadata, dict) else {}), OBSERVATION_COUNT_KEY: total},
            # Persist WHAT LANDED, not just that the run ended. Without this
            # `result` stayed NULL on every collection, so "did last night
            # actually ingest anything?" was unanswerable after the fact —
            # the blind spot that let a five-day zero-row outage hide.
            result={
                "created_observations": receipt.created,
                "existing_observations": receipt.existing,
                "observation_ids": len(receipt.observation_ids or []),
            },
            updated_at=now,
        )
        return CollectionReceipt(
            run_id=run.id,
            raw_payload_id=raw.id,
            created_observations=receipt.created,
            existing_observations=receipt.existing,
        )

    async def fail_run(self, run: CollectionRun, error: dict[str, Any]) -> None:
        row = await self._claimed_row(run)
        await row.update(
            status="failed",
            error=error,
            lease_owner=None,
            lease_expires_at=None,
            updated_at=_now(),
        )

    async def cancel_run(self, run: CollectionRun, error: dict[str, Any]) -> None:
        """Best-effort terminal write for a cancelled collect.

        Conditional on the row still being OURS and still in flight: if the
        lifecycle watchdog (or a reclaim) terminalized it first, their status
        and error stamp win — zero rows affected is success, not a conflict."""
        await m.CollectionRun.update_where(
            {"id": run.id, "status": "processing", "lease_owner": run.lease_owner},
            status="cancelled",
            error=error,
            lease_owner=None,
            lease_expires_at=None,
            updated_at=_now(),
        )

    async def complete_command_run(
        self, run: CollectionRun, result: dict[str, Any]
    ) -> CollectionReceipt:
        now = _now()
        outcome = await m.CollectionRun.update_where(
            {"id": run.id, "status": "processing", "lease_owner": run.lease_owner},
            status="completed",
            error=None,
            result=result,
            lease_owner=None,
            lease_expires_at=None,
            completed_at=now,
            updated_at=now,
        )
        if outcome.rows_affected != 1:
            raise CollectionInProgressError(run.id)
        return CollectionReceipt(run_id=run.id)

    async def reclaim_run_by_id(self, run_id: str) -> CollectionRun:
        row = await m.CollectionRun.load_by_id_or_none(run_id)
        if row is None:
            raise LookupError(f"SEO collection run {run_id} does not exist")
        if row.status == "completed":
            return run_from_row(row)
        now = _now()
        lease_owner = str(uuid4())
        lease_expires_at = now + timedelta(seconds=RUN_LEASE_SECONDS)
        reclaim_filters: dict[str, Any] | None = None
        if row.status in {"failed", "abandoned", "cancelled", "pending"}:
            reclaim_filters = {
                "id": run_id,
                "status": row.status,
                "lease_owner": row.lease_owner,
            }
        elif row.status == "processing":
            if row.lease_expires_at is not None and row.lease_expires_at < now:
                reclaim_filters = {
                    "id": run_id,
                    "status": "processing",
                    "lease_owner": row.lease_owner,
                    "lease_expires_at__lt": now,
                }
            elif row.lease_expires_at is None and row.updated_at < now - timedelta(
                seconds=RUN_LEASE_SECONDS
            ):
                reclaim_filters = {
                    "id": run_id,
                    "status": "processing",
                    "lease_owner": row.lease_owner,
                    "lease_expires_at__isnull": True,
                    "updated_at__lt": now - timedelta(seconds=RUN_LEASE_SECONDS),
                }
        if reclaim_filters is None:
            raise CollectionInProgressError(run_id)
        outcome = await m.CollectionRun.update_where(
            reclaim_filters,
            status="processing",
            error=None,
            lease_owner=lease_owner,
            lease_expires_at=lease_expires_at,
            attempt_count=row.attempt_count + 1,
            started_at=now,
            updated_at=now,
        )
        if outcome.rows_affected != 1:
            raise CollectionInProgressError(run_id)
        fresh = await m.CollectionRun.get(use_cache=False, id=run_id)
        return run_from_row(fresh, claimed=True)

    async def receipt_for_run(self, run: CollectionRun) -> CollectionReceipt:
        row = await m.CollectionRun.load_by_id_or_none(run.id)
        if row is None or row.status != "completed":
            raise RuntimeError(f"SEO collection run {run.id} is not completed")
        payloads = await m.RawPayload.filter(run_id=run.id).order_by("-created_at").limit(1).all()
        # Aggregate COUNT per table — a fixed number of round trips (one per
        # observation table, never proportional to row count) instead of
        # hydrating every observation row just to len() it (DEF-11).
        stored = stored_observation_count(row)
        if stored is not None:
            total = stored
        else:
            total = 0
            for model in _OBSERVATION_MODELS:
                total += await model.count(run_id=run.id)
        return CollectionReceipt(
            run_id=run.id,
            raw_payload_id=str(payloads[0].id) if payloads else None,
            created_observations=0,
            existing_observations=total,
            reused_completed_run=True,
        )

    async def _observation_totals(self, run_ids: list[str]) -> dict[str, int]:
        """Exact observation count per run — one grouped count per observation table, together."""
        import asyncio

        from matrx_orm import Count

        if not run_ids:
            return {}

        async def counted(model: type) -> dict[str, int]:
            rows = await (
                model.filter(run_id__in=run_ids)
                .annotate(n=Count("id"))
                .group_by("run_id")
                .values("run_id", "n")
            )
            return {str(r["run_id"]): int(r["n"] or 0) for r in rows}

        counts = await asyncio.gather(*(counted(mod) for mod in _OBSERVATION_MODELS))
        return {rid: sum(c.get(rid, 0) for c in counts) for rid in run_ids}

    async def receipts_for_runs(
        self, runs: list[CollectionRun], stored_counts: dict[str, int] | None = None
    ) -> dict[str, CollectionReceipt]:
        """:meth:`receipt_for_run` for MANY completed runs in a CONSTANT number of round trips —
        a list of 25 runs was 71s asked one receipt at a time. ``stored_counts`` are the counts a
        run wrote about itself when it finished (``metadata.observation_count``; a run does not
        change afterwards): those runs skip the count, which on ``search_performance_daily``
        (17.8M rows) was the whole cost. A run without one falls back to the exact count."""
        import asyncio

        ids = [str(r.id) for r in runs]
        if not ids:
            return {}
        stored = {k: int(v) for k, v in (stored_counts or {}).items() if k in set(ids)}

        async def payloads() -> dict[str, str]:
            rows = await (
                m.RawPayload.filter(run_id__in=ids).order_by("-created_at").values("run_id", "id")
            )
            first: dict[str, str] = {}
            for r in rows:  # newest first: keep the first seen per run
                first.setdefault(str(r["run_id"]), str(r["id"]))
            return first

        first, exact = await asyncio.gather(
            payloads(), self._observation_totals([i for i in ids if i not in stored])
        )
        totals = {**exact, **stored}
        return {
            rid: CollectionReceipt(
                run_id=rid,
                raw_payload_id=first.get(rid),
                created_observations=0,
                existing_observations=totals.get(rid, 0),
                reused_completed_run=True,
            )
            for rid in ids
        }

    async def has_prior_observations(self, request: CollectionRequest) -> bool | None:
        # Only `search_performance` has a site-keyed observation table today;
        # for anything else we do not know, and "do not know" never alarms.
        capability = str(getattr(request.capability, "value", request.capability))
        if capability != "search_performance" or not request.site_id:
            return None
        try:
            return await m.SearchPerformanceDaily.exists(site_id=request.site_id)
        except Exception:  # noqa: BLE001 — a bookkeeping read must never fail a run
            return None

    async def load_raw_payload(self, raw_payload_id: str) -> dict[str, Any] | list[Any] | None:
        """One raw provider payload, wherever it physically lives.

        Inline JSONB and an offloaded ``cloud_file_id`` are the SAME payload to
        every caller — the offload is a storage decision, never a contract
        change. Callers must not grow their own file-fetch fallback: a caller
        that knows about `cloud_file_id` is a caller that will be forgotten
        when the next one is written (two already were, and both would have
        started returning None the moment the offload threshold dropped)."""
        row = await m.RawPayload.load_by_id_or_none(raw_payload_id)
        if row is None:
            return None
        payload = row.payload
        if isinstance(payload, dict | list):
            return payload
        if not row.cloud_file_id:
            return None
        fetcher = get_payload_fetcher()
        content = await fetcher(str(row.cloud_file_id))
        restored = json.loads(content)
        return restored if isinstance(restored, dict | list) else None

    async def checkpoint_provider_task(
        self, run: CollectionRun, task: ProviderTaskCheckpoint
    ) -> None:
        await self.checkpoint_provider_tasks(run, [task])

    async def checkpoint_provider_tasks(
        self, run: CollectionRun, tasks: list[ProviderTaskCheckpoint]
    ) -> None:
        """Persist a whole batch of provider-task checkpoints in a small,
        CONSTANT number of round trips (one collision-scan query + one
        cross-run-owner lookup + one upsert), never one per task (DEF-11)."""
        await self._claimed_row(run)
        if not tasks:
            return
        external_ids = list({task.external_task_id for task in tasks})

        # Cross-run collision check, batched: every OTHER run currently
        # holding one of these external task ids, in ONE query, then ONE
        # lookup for the distinct owning runs' providers.
        other_task_rows = (
            await m.ProviderTask.filter(external_task_id__in=external_ids)
            .exclude(run_id=run.id)
            .values("run_id", "external_task_id")
        )
        if other_task_rows:
            other_run_ids = list({str(row["run_id"]) for row in other_task_rows})
            other_runs = await m.CollectionRun.filter(id__in=other_run_ids).values("id", "provider")
            provider_by_run = {str(row["id"]): row["provider"] for row in other_runs}
            for row in other_task_rows:
                if provider_by_run.get(str(row["run_id"])) == run.provider:
                    raise ValueError(
                        "provider task id is already attached to another collection run"
                    )

        # De-duplicate same-key checkpoints WITHIN this batch (last write
        # wins, matching what a sequential loop would leave behind) — a
        # single ``ON CONFLICT DO UPDATE`` statement cannot affect the same
        # target row twice.
        by_task_id: dict[str, ProviderTaskCheckpoint] = {}
        for task in tasks:
            by_task_id[task.external_task_id] = task
        rows = [
            {
                "id": str(uuid4()),
                "run_id": run.id,
                "external_task_id": task.external_task_id,
                "endpoint": task.endpoint,
                "status": task.status,
                "request_payload": task.request_payload,
                "response_payload": task.response_payload,
                "request_count": task.request_count,
                "provider_cost": task.provider_cost,
                "estimated_cost": task.estimated_cost,
                "currency": task.currency,
                "submitted_at": task.submitted_at,
                "last_polled_at": task.last_polled_at,
                "completed_at": task.completed_at,
                "error": task.error,
            }
            for task in by_task_id.values()
        ]
        await bulk_upsert_increment(
            m.ProviderTask,
            rows,
            on_conflict=["run_id", "external_task_id"],
            set_fields={
                "endpoint": Excluded("endpoint"),
                "status": Excluded("status"),
                "request_payload": Excluded("request_payload"),
                "response_payload": Excluded("response_payload"),
                "request_count": Excluded("request_count"),
                "provider_cost": Excluded("provider_cost"),
                "estimated_cost": Excluded("estimated_cost"),
                "currency": Excluded("currency"),
                "submitted_at": Excluded("submitted_at"),
                "last_polled_at": Excluded("last_polled_at"),
                "completed_at": Excluded("completed_at"),
                "error": Excluded("error"),
            },
        )

    async def list_provider_tasks(self, run: CollectionRun) -> list[ProviderTaskCheckpoint]:
        await self._claimed_row(run)
        rows = await m.ProviderTask.filter_items(run_id=run.id)
        return [
            ProviderTaskCheckpoint(
                external_task_id=row.external_task_id,
                endpoint=row.endpoint,
                status=row.status,
                request_payload=row.request_payload or {},
                response_payload=row.response_payload,
                request_count=row.request_count,
                provider_cost=row.provider_cost,
                estimated_cost=row.estimated_cost,
                currency=row.currency,
                submitted_at=row.submitted_at,
                last_polled_at=row.last_polled_at,
                completed_at=row.completed_at,
                error=row.error,
            )
            for row in rows
        ]

    async def spend_summary(self, query: SpendQuery) -> SpendSummary:
        """Aggregate cost evidence directly from ``seo.collection_run`` —
        every run already carries the rolled-up ``reported_cost`` /
        ``estimated_cost`` (from ``_merge_provider_call``'s per-run rollup in
        ``persist_raw``), so budget checks read this ONE table via plain
        SQL aggregates rather than a second rollup table or a Python loop over
        ``provider_call`` rows.

        🚨 **Two things this deliberately does NOT do, both of which reported
        $0.00 for money we actually spent** (fixed 2026-08-20):

        1. **It never coalesces an absent cost to zero.** ``COALESCE(reported,
           estimated, 0)`` made a run nobody priced indistinguishable from a run
           that was genuinely free — 112 live SerpAPI runs, which report no cost
           at all, summed to $0.00 against every ceiling. The coalesce now has
           two arguments, so an unpriced run contributes NULL (ignored by SUM)
           and is COUNTED instead, in ``unpriced_run_count``; ``matrx_seo.budget``
           charges each one the ``seo.unpriced_run_assumed_cost_usd`` knob.
        2. **It no longer looks only at ``status='completed'``.** A run that
           failed or was cancelled after reaching the provider was billed in
           full and was excluded from spend entirely (45 failed DataForSEO runs,
           26 of them carrying a real reported cost). The window is now
           ``started_at`` — set the moment a run is claimed — so in-flight and
           failed runs count too.

        A run is treated as unpriced spend only when ``request_count > 0``: it
        reached the provider. That is what keeps a run the budget gate itself
        rejected (``request_count = 0``, no cost columns) from being charged,
        which would make every rejection raise the next projection.

        A free first-party provider (Search Console, Bing Webmaster, PageSpeed,
        our own crawl) reports a real ``0.00`` and is therefore priced and free —
        the policy's "free first-party data is unmetered" holds by construction.
        The one conservative edge: such a provider *failing* after it contacted
        the API leaves no cost row and is charged the assumed unit. The correct
        fix for that is in the adapter (report ``0.00`` on failure too), not
        here — over-counting a ceiling is the safe direction.
        """
        from matrx_orm import Coalesce, Count, Sum

        def _scope(qb):
            if query.organization_id is not None:
                qb = qb.filter(organization_id=query.organization_id)
            if query.provider is not None:
                qb = qb.filter(provider=query.provider)
            if query.created_by is not None:
                qb = qb.filter(created_by=query.created_by)
            return qb

        window = {
            "started_at__gte": query.period_start,
            "started_at__lt": query.period_end,
        }
        priced = Coalesce("reported_cost", "estimated_cost")

        rows = await (
            _scope(m.CollectionRun.filter(**window))
            .annotate(
                reported_total=Coalesce(Sum("reported_cost"), 0),
                estimated_total=Coalesce(Sum("estimated_cost"), 0),
                effective_total=Coalesce(Sum(priced), 0),
                run_count=Count("*"),
            )
            .values("reported_total", "estimated_total", "effective_total", "run_count")
        )
        row = rows[0] if rows else {}

        # Second aggregate, restricted to runs that actually reached a provider:
        # everything here minus the priced ones is real spend nobody measured.
        reached_rows = await (
            _scope(m.CollectionRun.filter(request_count__gt=0, **window))
            .annotate(
                reached_count=Count("*"),
                reached_priced=Count(priced),
            )
            .values("reached_count", "reached_priced")
        )
        reached = reached_rows[0] if reached_rows else {}
        unpriced = int(reached.get("reached_count") or 0) - int(reached.get("reached_priced") or 0)

        return SpendSummary(
            query=query,
            reported_cost=Decimal(row.get("reported_total") or 0),
            estimated_cost=Decimal(row.get("estimated_total") or 0),
            effective_cost=Decimal(row.get("effective_total") or 0),
            unpriced_run_count=max(unpriced, 0),
            run_count=int(row.get("run_count") or 0),
        )


__all__ = ["OrmSeoRepository"]
