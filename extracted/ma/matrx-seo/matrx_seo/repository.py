from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from .contracts import (
    CollectionInProgressError,
    CollectionReceipt,
    CollectionRequest,
    CollectionRun,
    KeywordMarketObservation,
    ProviderCallRecord,
    ProviderResponse,
    ProviderTaskCheckpoint,
    RawPayloadEnvelope,
    RawPayloadReceipt,
    SeoObservation,
    SpendQuery,
    SpendSummary,
    UpsertReceipt,
)
from .identity import collection_identity, stable_hash
from .market_math import compute_market_stats, merge_monthly

RUN_LEASE_SECONDS = 300


class SeoRepository(ABC):
    @abstractmethod
    async def find_fresh_completed(
        self,
        provider: str,
        request: CollectionRequest,
        freshness_ttl_seconds: int,
    ) -> CollectionReceipt | None: ...

    @abstractmethod
    async def start_run(self, provider: str, request: CollectionRequest) -> CollectionRun: ...

    @abstractmethod
    async def renew_lease(self, run: CollectionRun) -> None: ...

    @abstractmethod
    async def persist_raw(
        self, run: CollectionRun, response: ProviderResponse, envelope: RawPayloadEnvelope
    ) -> RawPayloadReceipt: ...

    @abstractmethod
    async def persist_observations(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        observations: list[SeoObservation],
    ) -> UpsertReceipt: ...

    @abstractmethod
    async def complete_run(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        receipt: UpsertReceipt,
    ) -> CollectionReceipt: ...

    @abstractmethod
    async def fail_run(self, run: CollectionRun, error: dict[str, Any]) -> None: ...

    @abstractmethod
    async def cancel_run(self, run: CollectionRun, error: dict[str, Any]) -> None: ...

    @abstractmethod
    async def complete_command_run(
        self, run: CollectionRun, result: dict[str, Any]
    ) -> CollectionReceipt:
        """Terminal success for a COMMAND-style run (durable pre-AI job identity
        wrapping AI + provider work). Stores the final result document on the
        run row; observation receipts stay owned by the child provider runs."""
        ...

    @abstractmethod
    async def reclaim_run_by_id(self, run_id: str) -> CollectionRun:
        """Reclaim one existing run BY ID for continuation after process loss.

        Semantics mirror ``start_run`` reclamation, but keyed on the run id so
        identity never has to be recomputed (a force-refresh run's salted
        idempotency key is preserved exactly): a ``completed`` run returns
        unclaimed (read its receipt/result); ``failed``/``abandoned``/
        ``cancelled`` runs and ``processing`` runs whose lease expired are
        reclaimed with one compare-and-set; an actively leased run raises
        :class:`CollectionInProgressError`; a missing run raises
        :class:`LookupError`."""
        ...

    @abstractmethod
    async def receipt_for_run(self, run: CollectionRun) -> CollectionReceipt: ...

    @abstractmethod
    async def load_raw_payload(self, raw_payload_id: str) -> dict[str, Any] | list[Any] | None: ...

    @abstractmethod
    async def checkpoint_provider_task(
        self, run: CollectionRun, task: ProviderTaskCheckpoint
    ) -> None: ...

    @abstractmethod
    async def checkpoint_provider_tasks(
        self, run: CollectionRun, tasks: list[ProviderTaskCheckpoint]
    ) -> None: ...

    @abstractmethod
    async def list_provider_tasks(self, run: CollectionRun) -> list[ProviderTaskCheckpoint]: ...

    async def has_prior_observations(self, request: CollectionRequest) -> bool | None:
        """Has this site EVER landed an observation for this capability?

        Read ONLY to decide whether a zero-row run is an alarm or normal
        operation for a parked/brand-new property — so it runs only on the
        rare zero-row path, never on the hot path. `None` means "could not
        determine", which never alarms: a bookkeeping read must never invent
        a defect. Default implementation opts out."""
        return None

    @abstractmethod
    async def spend_summary(self, query: SpendQuery) -> SpendSummary:
        """Aggregate cost evidence over COMPLETED runs matching *query* — the
        one read every spend/budget check (``matrx_seo.budget``) is built on.
        Never re-derive spend totals anywhere else; extend this query instead."""
        ...


class InMemorySeoRepository(SeoRepository):
    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}
        self.raw_payloads: dict[str, dict[str, Any]] = {}
        self.observations: dict[str, dict[str, Any]] = {}
        self.provider_tasks: dict[str, dict[str, Any]] = {}
        self.provider_calls: dict[str, dict[str, Any]] = {}
        # Mirrors seo.keyword_market — one row per (keyword_id, location_code),
        # monthly history merged (never replaced), stats recomputed post-merge.
        self.keyword_markets: dict[tuple[str, int], dict[str, Any]] = {}
        # Mirrors seo.keyword_market_observation (WS-8/DEF-21) — append-only,
        # keyed by the same dedup identity every other observation uses.
        self.keyword_market_observations: dict[str, dict[str, Any]] = {}

    async def find_fresh_completed(
        self,
        provider: str,
        request: CollectionRequest,
        freshness_ttl_seconds: int,
    ) -> CollectionReceipt | None:
        settings_hash = stable_hash(request.settings)
        cutoff = datetime.now(UTC) - timedelta(seconds=freshness_ttl_seconds)
        matches = [
            row
            for row in self.runs.values()
            if row["status"] == "completed"
            and row["provider"] == provider
            and row["request"].organization_id == request.organization_id
            and row["request"].capability == request.capability
            and row["request"].operation == request.operation
            and row["request"].target_ref == request.target_ref
            and row["request"].site_id == request.site_id
            and row["request"].page_id == request.page_id
            and row["request"].source_crawl_session_id == request.source_crawl_session_id
            and row["settings_hash"] == settings_hash
            and row.get("completed_at") is not None
            and row["completed_at"] >= cutoff
        ]
        if not matches:
            return None
        row = max(matches, key=lambda item: item["completed_at"])
        receipt = row.get("receipt")
        if receipt is None:
            return None
        age = max(int((datetime.now(UTC) - row["completed_at"]).total_seconds()), 0)
        return receipt.model_copy(
            update={
                "reused_completed_run": True,
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
        now = datetime.now(UTC)
        lease_expires_at = now + timedelta(seconds=RUN_LEASE_SECONDS)
        row = self.runs.get(key)
        if row is None:
            row = {
                "id": str(uuid4()),
                "status": "processing",
                "execution_id": request.execution_id,
                "lease_owner": str(uuid4()),
                "lease_expires_at": lease_expires_at,
                "raw_payload_id": None,
                "receipt": None,
                "attempt_count": 1,
                "request_count": 0,
                "started_at": now,
                "provider_cost": None,
                "estimated_cost": None,
                "provider": provider,
                "request": request.model_copy(deep=True),
                "settings_hash": settings_hash,
                "completed_at": None,
            }
            self.runs[key] = row
            created = True
        else:
            created = False
        claimed = created
        lease_expired = row["status"] == "processing" and (
            row.get("lease_expires_at") is None or row["lease_expires_at"] < now
        )
        if not created and (row["status"] == "failed" or lease_expired):
            row["status"] = "processing"
            row["error"] = None
            row["lease_owner"] = str(uuid4())
            row["lease_expires_at"] = lease_expires_at
            row["attempt_count"] += 1
            row["execution_id"] = request.execution_id
            row["request_id"] = request.request_id
            row["credential_reference_id"] = request.credential_reference_id
            claimed = True
        elif (
            not created
            and request.resume_existing
            and request.execution_id == row["execution_id"]
            and row["status"] == "processing"
        ):
            row["lease_owner"] = str(uuid4())
            row["lease_expires_at"] = lease_expires_at
            row["attempt_count"] += 1
            claimed = True
        return CollectionRun(
            id=row["id"],
            provider=provider,
            request=request,
            settings_hash=settings_hash,
            idempotency_key=key,
            status=row["status"],
            created=created,
            claimed=claimed,
            lease_owner=row["lease_owner"],
            lease_expires_at=row["lease_expires_at"],
            attempt_count=row["attempt_count"],
        )

    async def renew_lease(self, run: CollectionRun) -> None:
        row = self.runs.get(run.idempotency_key)
        if row is None or row["status"] != "processing" or row["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        expires_at = datetime.now(UTC) + timedelta(seconds=RUN_LEASE_SECONDS)
        row["lease_expires_at"] = expires_at
        run.lease_expires_at = expires_at

    async def persist_raw(
        self, run: CollectionRun, response: ProviderResponse, envelope: RawPayloadEnvelope
    ) -> RawPayloadReceipt:
        if self.runs[run.idempotency_key]["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        row = self.runs[run.idempotency_key]
        row["provider_response"] = response.model_copy(deep=True)
        checksum = envelope.checksum
        call_records = response.call_records or [
            ProviderCallRecord(
                provider_call_key=response.external_task_id
                or stable_hash([run.provider, run.id, response.fetched_at, checksum]),
                external_task_id=response.external_task_id,
                request_count=response.request_count,
                reported_cost=response.reported_cost,
                estimated_cost=response.estimated_cost,
                currency=response.currency,
                fetched_at=response.fetched_at,
            )
        ]
        observation_group = stable_hash(sorted(record.provider_call_key for record in call_records))
        key = stable_hash([run.id, observation_group, checksum])
        existing = self.raw_payloads.get(key)
        payload_id = existing["id"] if existing is not None else str(uuid4())
        if existing is None:
            self.raw_payloads[key] = {
                "id": payload_id,
                "run_id": run.id,
                "checksum": checksum,
                "payload": envelope.payload,
                "cloud_file_id": envelope.cloud_file_id,
                "offload_error": envelope.offload_error,
                "fetched_at": response.fetched_at,
            }
        # DEF-19 (2026-07-23): merge, never insert-ignore, a retried call —
        # see OrmSeoRepository._merge_provider_calls_batch for the full rationale.
        # Mirrors that method's field-by-field "never regress" merge so the
        # in-memory repository used by the fast offline test suite exercises
        # the same retry semantics as the live ORM path.
        new_records: list[ProviderCallRecord] = []
        for record in call_records:
            call_key = f"{run.id}:{record.provider_call_key}"
            existing_call = self.provider_calls.get(call_key)
            if existing_call is None:
                new_records.append(record)
                self.provider_calls[call_key] = {
                    "raw_payload_id": payload_id,
                    "external_task_id": record.external_task_id,
                    "request_count": record.request_count,
                    "provider_cost": record.reported_cost,
                    "estimated_cost": record.estimated_cost,
                    "metadata": record.metadata,
                    "fetched_at": record.fetched_at,
                }
                continue
            existing_call["external_task_id"] = (
                record.external_task_id or existing_call["external_task_id"]
            )
            existing_call["request_count"] = max(
                existing_call["request_count"] or 0, record.request_count or 0
            )
            existing_call["provider_cost"] = (
                record.reported_cost
                if record.reported_cost is not None
                else existing_call["provider_cost"]
            )
            existing_call["estimated_cost"] = (
                record.estimated_cost
                if record.estimated_cost is not None
                else existing_call["estimated_cost"]
            )
            existing_call["metadata"] = {
                **(existing_call.get("metadata") or {}),
                **(record.metadata or {}),
            } or None
            existing_call["fetched_at"] = max(
                existing_call.get("fetched_at") or record.fetched_at, record.fetched_at
            )
        run_calls = [
            call for key, call in self.provider_calls.items() if key.startswith(f"{run.id}:")
        ]
        row["request_count"] = sum(call["request_count"] for call in run_calls)
        reported = [call["provider_cost"] for call in run_calls]
        estimated = [call["estimated_cost"] for call in run_calls]
        row["provider_cost"] = (
            sum(value for value in reported if value is not None)
            if reported and all(value is not None for value in reported)
            else None
        )
        row["estimated_cost"] = (
            sum(value for value in estimated if value is not None)
            if estimated and all(value is not None for value in estimated)
            else None
        )
        self.runs[run.idempotency_key]["raw_payload_id"] = payload_id
        return RawPayloadReceipt(id=payload_id, checksum=checksum, created=existing is None)

    async def persist_observations(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        observations: list[SeoObservation],
    ) -> UpsertReceipt:
        if self.runs[run.idempotency_key]["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        receipt = UpsertReceipt()
        for observation in observations:
            if isinstance(observation, KeywordMarketObservation):
                # WS-8/DEF-21 — append-only history first, dedup-keyed exactly
                # like every other observation kind (a replay of the same run
                # never duplicates a history row).
                history_key = stable_hash(
                    {
                        "kind": observation.kind,
                        "run": run.idempotency_key,
                        "organization_id": run.request.organization_id,
                        "provider": run.provider,
                        "keyword_id": observation.keyword_id,
                        "location_code": observation.location_code,
                        "observed_at": observation.observed_at.isoformat(),
                    }
                )
                existing_history = self.keyword_market_observations.get(history_key)
                history_created = existing_history is None
                history_id = existing_history["id"] if existing_history else str(uuid4())
                if history_created:
                    self.keyword_market_observations[history_key] = {
                        "id": history_id,
                        "run_id": run.id,
                        "raw_payload_id": raw.id,
                        "provider": run.provider,
                        "organization_id": run.request.organization_id,
                        "created_by": run.request.created_by,
                        "observation": observation.model_copy(deep=True),
                    }

                market_key = (observation.keyword_id, observation.location_code)
                fresh_monthly = [item.model_dump() for item in observation.monthly_searches]
                existing_market = self.keyword_markets.get(market_key)
                merged = merge_monthly(
                    existing_market["monthly_searches"] if existing_market else [],
                    fresh_monthly,
                )
                stats = compute_market_stats(merged)
                market_id = existing_market["id"] if existing_market else str(uuid4())
                # Precedence (WS-8, kept simple — see orm_repository.py's
                # matching guard): only the observation with the LATEST
                # observed_at (>= whatever is currently cached) supplies the
                # scalar fields + provenance; an older/out-of-order report
                # never clobbers a fresher one already cached.
                current_last_observed_at = (
                    existing_market["last_observed_at"] if existing_market else None
                )
                is_authoritative = (
                    current_last_observed_at is None
                    or observation.observed_at >= current_last_observed_at
                )
                if is_authoritative:
                    scalar_fields = {
                        "search_volume": observation.search_volume,
                        "competition": observation.competition,
                        "competition_index": observation.competition_index,
                        "cpc": observation.cpc,
                        "low_top_of_page_bid": observation.low_top_of_page_bid,
                        "high_top_of_page_bid": observation.high_top_of_page_bid,
                        "metrics_task_id": observation.metrics_task_id,
                        "raw": observation.raw,
                        "source_provider": run.provider,
                        "source_observation_id": history_id,
                        "last_observed_at": observation.observed_at,
                    }
                else:
                    scalar_fields = {
                        key: existing_market[key]
                        for key in (
                            "search_volume",
                            "competition",
                            "competition_index",
                            "cpc",
                            "low_top_of_page_bid",
                            "high_top_of_page_bid",
                            "metrics_task_id",
                            "raw",
                            "source_provider",
                            "source_observation_id",
                            "last_observed_at",
                        )
                    }
                self.keyword_markets[market_key] = {
                    "id": market_id,
                    "keyword_id": observation.keyword_id,
                    "location_code": observation.location_code,
                    **scalar_fields,
                    "monthly_searches": merged,
                    "demand_trajectory": stats.demand_trajectory,
                    "growth_rate": stats.growth_rate,
                    "seasonality_index": stats.seasonality_index,
                    "data_months": stats.data_months,
                    "metrics_fetched_at": datetime.now(UTC),
                }
                if existing_market is None:
                    receipt.created += 1
                else:
                    receipt.existing += 1
                receipt.observation_ids.append(market_id)
                continue
            key = stable_hash(
                {
                    "run": run.idempotency_key,
                    "observation": observation.model_dump(mode="json"),
                }
            )
            existing = self.observations.get(key)
            if existing is not None:
                receipt.existing += 1
                receipt.observation_ids.append(existing["id"])
                continue
            observation_id = str(uuid4())
            self.observations[key] = {
                "id": observation_id,
                "run_id": run.id,
                "raw_payload_id": raw.id,
                "provider": run.provider,
                "observation": observation.model_copy(deep=True),
            }
            receipt.created += 1
            receipt.observation_ids.append(observation_id)
        return receipt

    async def complete_run(
        self,
        run: CollectionRun,
        raw: RawPayloadReceipt,
        response: ProviderResponse,
        receipt: UpsertReceipt,
    ) -> CollectionReceipt:
        row = self.runs[run.idempotency_key]
        if row["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        row["status"] = "completed"
        row["error"] = None
        row["completed_at"] = datetime.now(UTC)
        row["lease_owner"] = None
        row["lease_expires_at"] = None
        completed = CollectionReceipt(
            run_id=run.id,
            raw_payload_id=raw.id,
            created_observations=receipt.created,
            existing_observations=receipt.existing,
        )
        row["receipt"] = completed
        return completed

    async def fail_run(self, run: CollectionRun, error: dict[str, Any]) -> None:
        row = self.runs[run.idempotency_key]
        if row["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        row["status"] = "failed"
        row["error"] = error
        row["lease_owner"] = None
        row["lease_expires_at"] = None

    async def cancel_run(self, run: CollectionRun, error: dict[str, Any]) -> None:
        # Best-effort, conditional: if another authority (watchdog, reclaim)
        # already terminalized the row, their write wins — mirror the ORM
        # repository's zero-rows-affected-is-success semantics.
        row = self.runs[run.idempotency_key]
        if row["lease_owner"] != run.lease_owner or row["status"] != "processing":
            return
        row["status"] = "cancelled"
        row["error"] = error
        row["lease_owner"] = None
        row["lease_expires_at"] = None

    async def complete_command_run(
        self, run: CollectionRun, result: dict[str, Any]
    ) -> CollectionReceipt:
        row = self.runs[run.idempotency_key]
        if row["lease_owner"] != run.lease_owner or row["status"] != "processing":
            raise CollectionInProgressError(run.id)
        row["status"] = "completed"
        row["error"] = None
        row["result"] = result
        row["completed_at"] = datetime.now(UTC)
        row["lease_owner"] = None
        row["lease_expires_at"] = None
        completed = CollectionReceipt(run_id=run.id)
        row["receipt"] = completed
        return completed

    async def reclaim_run_by_id(self, run_id: str) -> CollectionRun:
        found: tuple[str, dict[str, Any]] | None = None
        for key, row in self.runs.items():
            if row["id"] == run_id:
                found = (key, row)
                break
        if found is None:
            raise LookupError(f"SEO collection run {run_id} does not exist")
        key, row = found
        now = datetime.now(UTC)
        if row["status"] == "completed":
            return CollectionRun(
                id=row["id"],
                provider=row["provider"],
                request=row["request"].model_copy(deep=True),
                settings_hash=row["settings_hash"],
                idempotency_key=key,
                status="completed",
                created=False,
                claimed=False,
                lease_owner=row["lease_owner"],
                lease_expires_at=row["lease_expires_at"],
                attempt_count=row["attempt_count"],
            )
        lease_expired = row["status"] == "processing" and (
            row.get("lease_expires_at") is None or row["lease_expires_at"] < now
        )
        reclaimable = row["status"] in {"failed", "abandoned", "cancelled", "pending"}
        if not reclaimable and not lease_expired:
            raise CollectionInProgressError(run_id)
        row["status"] = "processing"
        row["error"] = None
        row["lease_owner"] = str(uuid4())
        row["lease_expires_at"] = now + timedelta(seconds=RUN_LEASE_SECONDS)
        row["attempt_count"] += 1
        return CollectionRun(
            id=row["id"],
            provider=row["provider"],
            request=row["request"].model_copy(deep=True),
            settings_hash=row["settings_hash"],
            idempotency_key=key,
            status="processing",
            created=False,
            claimed=True,
            lease_owner=row["lease_owner"],
            lease_expires_at=row["lease_expires_at"],
            attempt_count=row["attempt_count"],
        )

    async def receipt_for_run(self, run: CollectionRun) -> CollectionReceipt:
        row = self.runs[run.idempotency_key]
        receipt = row.get("receipt")
        if receipt is None:
            raise RuntimeError(f"SEO collection run {run.id} is not completed")
        return receipt.model_copy(update={"reused_completed_run": True})

    async def load_raw_payload(self, raw_payload_id: str) -> dict[str, Any] | list[Any] | None:
        """Same contract as the ORM repository: inline and offloaded rows read
        identically, so the offline suite exercises the real read path."""
        import json

        from .config import get_payload_fetcher

        for row in self.raw_payloads.values():
            if row["id"] != raw_payload_id:
                continue
            payload = row.get("payload")
            if isinstance(payload, dict | list):
                return payload
            cloud_file_id = row.get("cloud_file_id")
            if not cloud_file_id:
                return None
            restored = json.loads(await get_payload_fetcher()(str(cloud_file_id)))
            return restored if isinstance(restored, dict | list) else None
        return None

    async def checkpoint_provider_task(
        self, run: CollectionRun, task: ProviderTaskCheckpoint
    ) -> None:
        await self.checkpoint_provider_tasks(run, [task])

    async def checkpoint_provider_tasks(
        self, run: CollectionRun, tasks: list[ProviderTaskCheckpoint]
    ) -> None:
        if self.runs[run.idempotency_key]["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        keys = [f"{run.provider}:{task.external_task_id}" for task in tasks]
        if any(
            key in self.provider_tasks and self.provider_tasks[key]["run_id"] != run.id
            for key in keys
        ):
            raise ValueError("provider task id is already attached to another collection run")
        for task in tasks:
            self.provider_tasks[f"{run.provider}:{task.external_task_id}"] = {
                "run_id": run.id,
                "task": task.model_copy(deep=True),
            }

    async def list_provider_tasks(self, run: CollectionRun) -> list[ProviderTaskCheckpoint]:
        row = self.runs[run.idempotency_key]
        if row["lease_owner"] != run.lease_owner:
            raise CollectionInProgressError(run.id)
        return [
            value["task"].model_copy(deep=True)
            for value in self.provider_tasks.values()
            if value["run_id"] == run.id
        ]

    def history(self, *, rank_target_id: str) -> list[SeoObservation]:
        rows = [
            value["observation"]
            for value in self.observations.values()
            if getattr(value["observation"], "rank_target_id", None) == rank_target_id
        ]
        return sorted(rows, key=lambda item: item.observed_at)

    async def spend_summary(self, query: SpendQuery) -> SpendSummary:
        """Byte-for-byte the same semantics as :meth:`OrmSeoRepository.spend_summary`
        — window on ``started_at`` (not ``completed_at``), no status filter, and
        an unpriced run that reached the provider is COUNTED, never summed as
        zero. Budget enforcement must behave identically in tests and
        production; read that method's docstring for why each of those is so."""
        reported = Decimal(0)
        estimated = Decimal(0)
        effective = Decimal(0)
        unpriced = 0
        run_count = 0
        for row in self.runs.values():
            started_at = row.get("started_at")
            if started_at is None or not (query.period_start <= started_at < query.period_end):
                continue
            request = row["request"]
            if (
                query.organization_id is not None
                and request.organization_id != query.organization_id
            ):
                continue
            if query.provider is not None and row["provider"] != query.provider:
                continue
            if query.created_by is not None and request.created_by != query.created_by:
                continue
            run_reported = row.get("provider_cost")
            run_estimated = row.get("estimated_cost")
            if run_reported is not None:
                reported += run_reported
                effective += run_reported
            elif run_estimated is not None:
                estimated += run_estimated
                effective += run_estimated
            elif (row.get("request_count") or 0) > 0:
                # Reached the provider, nobody priced it. Real spend, unmeasured.
                unpriced += 1
            run_count += 1
        return SpendSummary(
            query=query,
            reported_cost=reported,
            estimated_cost=estimated,
            effective_cost=effective,
            unpriced_run_count=unpriced,
            run_count=run_count,
        )
