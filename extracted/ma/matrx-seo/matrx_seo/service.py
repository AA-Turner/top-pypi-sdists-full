from __future__ import annotations

import asyncio
import json
import logging
from contextlib import suppress
from datetime import date
from decimal import Decimal
from typing import Any
from uuid import uuid4

from matrx_utils import capture_error

from .adapters import ProviderExecutionContext, SeoProgressCallback, SeoProviderAdapter
from .budget import (
    BudgetExceededError,
    SpendApprovalExceededError,
    charge_spend_approval,
    check_spend_approval,
    enforce_collection_budget,
)
from .collection_outcome import CollectionOutcomeEvent, emit_collection_outcome
from .config import (
    CollectionAuthorizer,
    CredentialResolver,
    PayloadStore,
    get_collection_authorizer,
    get_credential_resolver,
    get_payload_store,
)
from .contracts import (
    CollectionInProgressError,
    CollectionReceipt,
    CollectionRequest,
    NormalizationContext,
    ProviderResponse,
    ProviderResponseError,
    RawPayloadEnvelope,
)
from .identity import stable_hash
from .knobs import int_knob
from .repository import SeoRepository

RUN_LEASE_HEARTBEAT_SECONDS = 60
logger = logging.getLogger(__name__)


def _prepare_provider_response(
    response: ProviderResponse,
    *,
    include_progress_payload: bool,
) -> tuple[dict[str, Any] | None, bytes, str]:
    """Serialize and fingerprint a provider response away from the event loop."""
    progress_payload = response.model_dump(mode="json") if include_progress_payload else None
    encoded = json.dumps(
        response.raw,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode()
    return progress_payload, encoded, stable_hash(response.raw)


async def _emit_progress(
    progress: SeoProgressCallback | None,
    event: str,
    **payload: Any,
) -> None:
    if progress is None:
        return
    try:
        await progress(event, payload)
    except Exception:
        logger.exception("SEO progress callback failed for event %s", event)


async def _heartbeat_run_lease(repository: SeoRepository, run) -> None:
    while True:
        await asyncio.sleep(RUN_LEASE_HEARTBEAT_SECONDS)
        await repository.renew_lease(run)


async def _stop_lease_heartbeat(
    heartbeat: asyncio.Task[None],
    *,
    suppress_failure: bool = False,
) -> None:
    heartbeat.cancel()
    try:
        await heartbeat
    except asyncio.CancelledError:
        return
    except Exception:
        if not suppress_failure:
            raise


class _UnconfiguredIdentityResolver:
    async def resolve(self, *_args, **_kwargs):
        raise RuntimeError("SEO identity persistence is not configured")

    async def resolve_many(self, *_args, **_kwargs):
        raise RuntimeError("SEO identity persistence is not configured")


class _UnconfiguredHostBindingResolver:
    async def resolve(self, *_args, **_kwargs):
        raise RuntimeError("SEO host binding persistence is not configured")


#: The feature these knobs belong to (``platform.feature_knob.feature``).
KNOB_FEATURE = "seo"


class SeoCollectionService:
    """The ONE collection funnel.

    **Where a raw provider payload lives** is not a constant in this file. It is
    the ``seo.inline_payload_max_bytes`` knob: anything bigger goes to the
    injected payload store (S3, through the host's file pipeline) and the row
    keeps a ``cloud_file_id`` pointer; anything smaller stays inline as JSONB.
    A constant here was worth 2.5 GB of Postgres — see
    ``common-docs/policies/limits-are-knobs-agents-set-them.md``.
    """

    def __init__(
        self,
        repository: SeoRepository,
        *,
        credential_resolver: CredentialResolver | None = None,
        identity_resolver: object | None = None,
        host_binding_resolver: object | None = None,
        payload_store: PayloadStore | None = None,
        inline_payload_max_bytes: int | None = None,
        collection_authorizer: CollectionAuthorizer | None = None,
    ) -> None:
        self.repository = repository
        self.credential_resolver = credential_resolver
        self.identity_resolver = identity_resolver or _UnconfiguredIdentityResolver()
        self.host_binding_resolver = host_binding_resolver or _UnconfiguredHostBindingResolver()
        self.payload_store = payload_store
        self._inline_payload_max_bytes_override = inline_payload_max_bytes
        self.collection_authorizer = collection_authorizer

    async def inline_payload_max_bytes(self) -> int:
        """Payloads at or under this many bytes stay inline in Postgres.

        A knob row, never a constant: an admin moves it without a deploy, and a
        missing row RAISES rather than silently restoring the 1 MB ceiling that
        kept 6,552 rows (2.5 GB) of provider evidence in the database."""
        if self._inline_payload_max_bytes_override is not None:
            return self._inline_payload_max_bytes_override
        return await int_knob(KNOB_FEATURE, "inline_payload_max_bytes")

    def _validated_request(
        self, adapter: SeoProviderAdapter, request: CollectionRequest
    ) -> tuple[CollectionRequest, int]:
        """Adapter capability/operation validation + adapter-owned credential
        keys. Shared verbatim by ``collect`` and ``resume`` — one gate."""
        freshness_ttl_seconds = 0
        if request.capability not in adapter.capabilities:
            raise ValueError(
                f"{adapter.provider} does not declare capability {request.capability.value}"
            )
        if adapter.operations:
            operation = next(
                (item for item in adapter.operations if item.name == request.operation), None
            )
            if operation is None or request.capability not in operation.capabilities:
                raise ValueError(
                    f"{adapter.provider} does not approve operation {request.operation!r} "
                    f"for {request.capability.value}"
                )
            if request.credential_reference_kind not in operation.reference_kinds:
                raise ValueError(
                    f"{adapter.provider} operation {request.operation!r} does not allow "
                    f"credential reference kind {request.credential_reference_kind.value}"
                )
            if request.credential_keys and request.credential_keys != operation.credential_keys:
                raise ValueError("provider credential keys are adapter-owned")
            request = request.model_copy(update={"credential_keys": operation.credential_keys})
            freshness_ttl_seconds = operation.freshness_ttl_seconds
        unsupported = adapter.unsupported_request_reason(request)
        if unsupported is not None:
            raise ValueError(f"{adapter.provider} cannot complete this collection: {unsupported}")
        return request, freshness_ttl_seconds

    async def preflight_credentials(
        self,
        adapter: SeoProviderAdapter,
        request: CollectionRequest,
    ) -> None:
        """Require usable provider credentials without creating a run.

        Interactive workflows can call this before doing upstream planning or
        AI work. It deliberately shares the exact adapter validation,
        collection authorization, and credential resolver used by ``collect``;
        success exposes no plaintext and failure happens before persistence,
        budget accounting, or provider I/O.
        """
        request, _ = self._validated_request(adapter, request)
        authorize = self.collection_authorizer or get_collection_authorizer()
        request = await authorize(request)
        resolver = self.credential_resolver or get_credential_resolver()
        credential = await resolver(request, adapter.provider)
        missing = [key for key in request.credential_keys if not credential.values.get(key)]
        if missing:
            raise ValueError(
                f"{adapter.provider} credential is missing active values for: {', '.join(missing)}"
            )

    async def fresh_run_for(
        self,
        adapter: SeoProviderAdapter,
        request: CollectionRequest,
    ) -> CollectionReceipt | None:
        """The fresh completed twin ``collect`` would reuse for ``request`` — or None.

        A READ with no side effect: no run, no budget, no provider I/O, no
        approval touched. Paid tools ask this per run BEFORE estimating, so runs
        that will be reused cost nothing and a request served entirely from reuse
        never asks a person to approve spend (OPENSEO-TOOLS-SPEC §6.1 step 1). It
        is the same validation, authorization and ``find_fresh_completed`` lookup
        ``collect`` performs, in the same order, so the two can never disagree."""
        request, freshness_ttl_seconds = self._validated_request(adapter, request)
        authorize = self.collection_authorizer or get_collection_authorizer()
        request = await authorize(request)
        if not freshness_ttl_seconds or request.force_refresh:
            return None
        return await self.repository.find_fresh_completed(
            adapter.provider, request, freshness_ttl_seconds
        )

    @staticmethod
    def _approval_estimate(adapter: SeoProviderAdapter, request: CollectionRequest) -> Decimal:
        """The price-book estimate an approval check compares against. An adapter
        with no price book cannot be checked against an approved number, so a
        request carrying an approval there is REFUSED — never waved through."""
        estimate = adapter.estimate_cost_usd(request)
        if estimate is None:
            raise SpendApprovalExceededError(
                approval_id=str(request.spend_approval_id),
                reason=(
                    f"{adapter.provider} keeps no price book, so no approved amount "
                    "can be checked"
                ),
                limit_usd=Decimal(0),
                spent_usd=Decimal(0),
                projected_usd=Decimal(0),
                new_estimate_usd=Decimal(0),
                scope={"organization_id": request.organization_id, "operation": request.operation},
            )
        return estimate

    async def collect(
        self,
        adapter: SeoProviderAdapter,
        request: CollectionRequest,
        *,
        progress: SeoProgressCallback | None = None,
        credential_resolver_override: CredentialResolver | None = None,
    ) -> CollectionReceipt:
        request, freshness_ttl_seconds = self._validated_request(adapter, request)
        authorize = self.collection_authorizer or get_collection_authorizer()
        request = await authorize(request)
        await _emit_progress(
            progress,
            "authorized",
            provider=adapter.provider,
            operation=request.operation,
            capability=request.capability.value,
            site_id=request.site_id,
            page_id=request.page_id,
        )
        if freshness_ttl_seconds and not request.force_refresh:
            cached = await self.repository.find_fresh_completed(
                adapter.provider,
                request,
                freshness_ttl_seconds,
            )
            if cached is not None:
                await _emit_progress(
                    progress,
                    "cache_hit",
                    receipt=cached.model_dump(mode="json"),
                )
                return cached
        # THE APPROVAL GATE (OPENSEO-TOOLS-SPEC §6.1.7): after the reuse lookup —
        # a reuse hit never touches an approval — and BEFORE start_run, so a
        # refusal leaves no collection_run row and makes no provider call.
        if request.spend_approval_id is not None:
            await check_spend_approval(request, self._approval_estimate(adapter, request))
        if request.force_refresh and not request.request_id:
            request = request.model_copy(update={"request_id": str(uuid4())})
        run = await self.repository.start_run(adapter.provider, request)
        await _emit_progress(
            progress,
            "run_claimed" if run.claimed else "run_reused",
            run=run.model_dump(mode="json"),
        )
        if not run.claimed and run.status == "completed":
            receipt = await self.repository.receipt_for_run(run)
            await _emit_progress(
                progress,
                "completed",
                receipt=receipt.model_dump(mode="json"),
            )
            return receipt
        if not run.claimed:
            raise CollectionInProgressError(run.id)
        return await self._execute_claimed(
            adapter,
            request,
            run,
            progress,
            credential_resolver_override=credential_resolver_override,
        )

    async def resume(
        self,
        adapter: SeoProviderAdapter,
        run_id: str,
        *,
        progress: SeoProgressCallback | None = None,
    ) -> CollectionReceipt:
        """Continue one persisted run BY ID after process loss or failure.

        Reclaims the run with the repository's compare-and-set (an actively
        leased run cannot be stolen; a completed run returns its receipt), then
        re-executes the claimed portion of ``collect``. Provider adapters that
        persist task checkpoints (DataForSEO standard workflows) resume from
        those checkpoints instead of re-submitting paid work."""
        run = await self.repository.reclaim_run_by_id(run_id)
        request, _ = self._validated_request(adapter, run.request)
        authorize = self.collection_authorizer or get_collection_authorizer()
        request = await authorize(request)
        run.request = request
        if run.status == "completed" and not run.claimed:
            receipt = await self.repository.receipt_for_run(run)
            await _emit_progress(
                progress,
                "completed",
                receipt=receipt.model_dump(mode="json"),
            )
            return receipt
        await _emit_progress(
            progress,
            "run_reclaimed",
            run=run.model_dump(mode="json"),
        )
        return await self._execute_claimed(adapter, request, run, progress)

    async def _charge_approval(
        self,
        adapter: SeoProviderAdapter,
        request: CollectionRequest,
        response: ProviderResponse,
        run,
    ) -> None:
        """Draw what this run cost from its approval — the provider's reported
        cost, else its estimate, else the price book. The money is already spent
        when this runs, so a failure to RECORD it never fails the run (the data
        is real and paid for); it is captured loudly instead."""
        amount = response.reported_cost
        if amount is None:
            amount = response.estimated_cost
        if amount is None:
            amount = adapter.estimate_cost_usd(request) or Decimal(0)
        try:
            await charge_spend_approval(request, amount, run_id=str(run.id))
        except Exception as exc:  # noqa: BLE001 — see docstring
            logger.exception(
                "SEO spend approval %s: could not record $%s for run %s",
                request.spend_approval_id,
                amount,
                run.id,
            )
            await capture_error(
                exc,
                kind="seo_spend_approval_charge_failed",
                context={
                    "run_id": str(run.id),
                    "spend_approval_id": str(request.spend_approval_id),
                    "amount_usd": str(amount),
                },
            )

    def _outcome_event(
        self,
        *,
        request: CollectionRequest,
        run,
        adapter_provider: str,
        status: str,
        observations: list | None = None,
        upsert=None,
        receipt: CollectionReceipt | None = None,
        error: dict | None = None,
    ) -> CollectionOutcomeEvent:
        """Assemble the expected-vs-actual outcome. Pure bookkeeping — it
        never touches the DB and never raises (a malformed settings dict
        must not turn a healthy run into a failure)."""
        settings = request.settings if isinstance(request.settings, dict) else {}
        start = settings.get("start_date")
        end = settings.get("end_date")
        expected_days: int | None = None
        try:
            if isinstance(start, str) and isinstance(end, str):
                expected_days = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
        except ValueError:
            expected_days = None
        profiles = settings.get("profiles")
        distinct_dates = 0
        if observations:
            distinct_dates = len(
                {getattr(o, "date", None) for o in observations if getattr(o, "date", None)}
            )
        return CollectionOutcomeEvent(
            provider=adapter_provider,
            capability=str(getattr(request.capability, "value", request.capability)),
            operation=request.operation,
            run_id=str(run.id),
            site_id=request.site_id,
            organization_id=request.organization_id,
            trigger=str(getattr(request.trigger, "value", request.trigger)),
            status=status,  # type: ignore[arg-type]
            window_start=start if isinstance(start, str) else None,
            window_end=end if isinstance(end, str) else None,
            expected_days=expected_days,
            profiles=tuple(str(p) for p in profiles) if isinstance(profiles, list | tuple) else (),
            observation_count=len(observations) if observations else 0,
            created=(
                upsert.created if upsert else (receipt.created_observations if receipt else 0)
            ),
            existing=(
                upsert.existing if upsert else (receipt.existing_observations if receipt else 0)
            ),
            distinct_dates=distinct_dates,
            reused=bool(receipt and (receipt.reused_completed_run or receipt.from_cache)),
            is_backfill="backfill"
            in str(getattr(request.trigger, "value", request.trigger)).lower(),
            error=error,
        )

    async def _emit_outcome(
        self, event: CollectionOutcomeEvent, request: CollectionRequest
    ) -> None:
        """Resolve the one fact the classifier can't infer, then emit.

        Split from `_outcome_event` because this ONE read touches the DB: it
        runs only when the run persisted nothing, which is the only case where
        the answer changes an alarm into normal operation."""
        if (
            event.status == "completed"
            and not event.reused
            and not event.is_backfill
            and event.created == 0
            and event.existing == 0
        ):
            try:
                event.site_has_prior_data = await self.repository.has_prior_observations(request)
            except Exception as exc:  # noqa: BLE001 — observability, never a failure
                logger.warning("collection outcome: prior-data probe failed: %s", exc)
        emit_collection_outcome(event)

    async def _execute_claimed(
        self,
        adapter: SeoProviderAdapter,
        request: CollectionRequest,
        run,
        progress: SeoProgressCallback | None,
        *,
        credential_resolver_override: CredentialResolver | None = None,
    ) -> CollectionReceipt:
        # WS-7 spend/quota gate — the ONE choke point every provider adapter
        # (host + standalone, on-demand + scheduled) funnels through, checked
        # BEFORE credential resolution or any paid provider I/O. See
        # matrx_seo.budget for the ceilings and their ARMAN_TBD placeholders.
        try:
            budget_summary = await enforce_collection_budget(
                self.repository, request, adapter.provider
            )
        except BudgetExceededError as exc:
            error = exc.as_error_payload()
            await self.repository.fail_run(run, error)
            # A spend ceiling that silently stops nightly ingestion is the
            # SAME outage shape this seam exists for — `status='failed'` rows
            # and nobody told. It is a terminal outcome of this body and it
            # alarms like every other one.
            await self._emit_outcome(
                self._outcome_event(
                    request=request,
                    run=run,
                    adapter_provider=adapter.provider,
                    status="failed",
                    error=error,
                ),
                request,
            )
            await _emit_progress(
                progress,
                "budget_rejected",
                run_id=run.id,
                provider=adapter.provider,
                **exc.as_event_payload(),
            )
            exc.run_id = run.id  # type: ignore[attr-defined]
            raise
        if request.spend_approval_id is not None:
            # Headroom RE-CHECK only (§6.1.7b): a concurrent run under the same
            # approval may have drawn it down since the pre-flight.
            try:
                await check_spend_approval(request, self._approval_estimate(adapter, request))
            except SpendApprovalExceededError as exc:
                error = exc.as_error_payload()
                await self.repository.fail_run(run, error)
                await self._emit_outcome(
                    self._outcome_event(
                        request=request,
                        run=run,
                        adapter_provider=adapter.provider,
                        status="failed",
                        error=error,
                    ),
                    request,
                )
                await _emit_progress(
                    progress,
                    "budget_rejected",
                    run_id=run.id,
                    provider=adapter.provider,
                    **exc.as_event_payload(),
                )
                exc.run_id = run.id  # type: ignore[attr-defined]
                raise
        await _emit_progress(
            progress,
            "budget_checked",
            run_id=run.id,
            provider=adapter.provider,
            spent_usd=str(budget_summary.effective_cost),
            run_count=budget_summary.run_count,
        )
        resolver = (
            credential_resolver_override or self.credential_resolver or get_credential_resolver()
        )
        heartbeat = asyncio.create_task(_heartbeat_run_lease(self.repository, run))
        try:
            credential = await resolver(request, adapter.provider)
            await _emit_progress(
                progress,
                "credentials_resolved",
                run_id=run.id,
                provider=adapter.provider,
                reference_id=credential.reference_id,
                reference_kind=(
                    credential.reference_kind.value
                    if credential.reference_kind is not None
                    else None
                ),
            )
            await adapter.authenticate(credential)
            await _emit_progress(
                progress,
                "provider_authenticated",
                run_id=run.id,
                provider=adapter.provider,
            )

            async def emit_provider_progress(event: str, payload: dict[str, Any]) -> None:
                await _emit_progress(progress, event, **payload)

            execution = ProviderExecutionContext(
                self.repository,
                run,
                emit_provider_progress if progress is not None else None,
            )
            await _emit_progress(
                progress,
                "provider_request_started",
                run_id=run.id,
                provider=adapter.provider,
                operation=request.operation,
                target_ref=request.target_ref,
                settings=request.settings,
            )
            response = await adapter.collect_response(request, execution)
            if request.spend_approval_id is not None:
                await self._charge_approval(adapter, request, response, run)
            await self.repository.renew_lease(run)
            response_payload, encoded, checksum = await asyncio.to_thread(
                _prepare_provider_response,
                response,
                include_progress_payload=progress is not None,
            )
            await _emit_progress(
                progress,
                "provider_response",
                run_id=run.id,
                provider=adapter.provider,
                response=response_payload,
            )
            envelope = RawPayloadEnvelope(
                payload=response.raw,
                checksum=checksum,
                size_bytes=len(encoded),
            )
            if len(encoded) > await self.inline_payload_max_bytes():
                try:
                    store = self.payload_store or get_payload_store()
                    stored = await store(request, adapter.provider, encoded, checksum)
                    envelope = RawPayloadEnvelope(
                        cloud_file_id=stored.cloud_file_id,
                        checksum=stored.checksum,
                        size_bytes=stored.size_bytes,
                        content_type=stored.content_type,
                    )
                except Exception as exc:
                    envelope = envelope.model_copy(
                        update={
                            "offload_error": {
                                "type": type(exc).__name__,
                                "message": str(exc),
                            }
                        }
                    )
            raw = await self.repository.persist_raw(run, response, envelope)
            await _emit_progress(
                progress,
                "raw_persisted",
                run_id=run.id,
                raw_payload=raw.model_dump(mode="json"),
            )
            if response.error is not None:
                raise ProviderResponseError(response.error)
            observations = await adapter.normalize(
                response,
                NormalizationContext(
                    request=request,
                    run=run,
                    raw_payload_id=raw.id,
                    identity_resolver=self.identity_resolver,
                    host_binding_resolver=self.host_binding_resolver,
                ),
            )
            await _emit_progress(
                progress,
                "normalized",
                run_id=run.id,
                observation_count=len(observations),
                observations=[observation.model_dump(mode="json") for observation in observations],
            )
            upsert = await self.repository.persist_observations(run, raw, response, observations)
            await _emit_progress(
                progress,
                "observations_persisted",
                run_id=run.id,
                receipt=upsert.model_dump(mode="json"),
            )
            await self.repository.renew_lease(run)
            await _stop_lease_heartbeat(heartbeat)
            receipt = await self.repository.complete_run(run, raw, response, upsert)
            success_outcome = self._outcome_event(
                request=request,
                run=run,
                adapter_provider=adapter.provider,
                status="completed",
                observations=observations,
                upsert=upsert,
                receipt=receipt,
            )
            await _emit_progress(
                progress,
                "completed",
                receipt=receipt.model_dump(mode="json"),
            )
        except asyncio.CancelledError:
            # Terminalize before propagating: without this, a cancelled collect
            # leaves the run 'processing' until the lifecycle watchdog abandons
            # it. The terminal write must outlive the cancellation that caused
            # it, and cancellation can arrive repeatedly during shutdown — keep
            # the inner task and re-shield until it lands.
            await _stop_lease_heartbeat(heartbeat, suppress_failure=True)
            error = {
                "type": "CancelledError",
                "message": "SEO collection task was cancelled",
            }
            write = asyncio.create_task(self.repository.cancel_run(run, error))
            while not write.done():
                # asyncio.wait never propagates the awaited task's exception
                # (unlike shield, which re-raises it at the await point), so
                # the loop reliably drains to done() and the logging +
                # CancelledError re-raise below always run.
                with suppress(asyncio.CancelledError):
                    await asyncio.wait({write})
            if write.exception() is not None:
                write_exc = write.exception()
                logger.error(
                    "Failed to persist cancellation for SEO collection run %s",
                    run.id,
                    exc_info=write_exc,
                )
                await capture_error(
                    write_exc,
                    kind="seo_collection_cancellation_finalize_failed",
                    context={"run_id": run.id, "provider": adapter.provider},
                )
            await _emit_progress(progress, "cancelled", run_id=run.id, error=error)
            raise
        except ProviderResponseError as exc:
            await _stop_lease_heartbeat(heartbeat, suppress_failure=True)
            await self.repository.fail_run(run, exc.error)
            await self._emit_outcome(
                self._outcome_event(
                    request=request,
                    run=run,
                    adapter_provider=adapter.provider,
                    status="failed",
                    error=exc.error,
                ),
                request,
            )
            exc.run_id = run.id
            await _emit_progress(
                progress,
                "failed",
                run_id=run.id,
                error=exc.error,
            )
            raise
        except Exception as exc:
            await _stop_lease_heartbeat(heartbeat, suppress_failure=True)
            error = {"type": type(exc).__name__, "message": str(exc)}
            await self.repository.fail_run(run, error)
            await self._emit_outcome(
                self._outcome_event(
                    request=request,
                    run=run,
                    adapter_provider=adapter.provider,
                    status="failed",
                    error=error,
                ),
                request,
            )
            await _emit_progress(progress, "failed", run_id=run.id, error=error)
            raise
        finally:
            if not heartbeat.done():
                heartbeat.cancel()
                with suppress(asyncio.CancelledError):
                    await heartbeat
        # OUTSIDE the try on purpose. Inside it, any raise from the outcome
        # path would land in the generic `except`, which calls `fail_run` on a
        # run `complete_run` already released — turning a fully persisted
        # ingest into a client-visible failure. Observability may never be
        # able to fail a run that succeeded.
        await self._emit_outcome(success_outcome, request)
        return receipt
