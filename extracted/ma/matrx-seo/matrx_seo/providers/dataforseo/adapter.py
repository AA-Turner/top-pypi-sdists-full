from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from datetime import UTC
from decimal import Decimal
from typing import Any

from ...adapters import ProviderExecutionContext, SeoProviderAdapter
from ...contracts import (
    CollectionRequest,
    KeywordMarketObservation,
    MonthlySearch,
    NormalizationContext,
    ProviderResponse,
    ResolvedCredential,
    SeoCapability,
    SeoIdentityRequest,
    SeoObservation,
)
from .backlinks import normalize_backlink_payload, supports_backlink_endpoint
from .client import DataForSeoClient
from .contracts import (
    DataForSeoCollectionSettings,
    DataForSeoOperationName,
    DataForSeoOperationRequest,
)
from .labs_keywords import NORMALIZED_OPERATIONS as LABS_KEYWORD_OPERATIONS
from .labs_keywords import normalize_labs_keywords
from .link_gap import normalize_link_gap_payload, supports_intersection_endpoint
from .operations import APPROVED_OPERATIONS, DATAFORSEO_CREDENTIAL_KEYS, get_operation
from .pricing import estimate as estimate_operation_cost
from .serp_organic import normalize_serp_organic
from .serp_prospect import SERP_ORGANIC_OPERATION
from .transport import AsyncHttpTransport, DataForSeoTransport

DataForSeoNormalizer = Callable[
    [ProviderResponse, NormalizationContext], Awaitable[list[SeoObservation]]
]

#: The four answer-engine operations ``normalize_ai_answer_response`` owns.
#: Named, never a ``startswith("ai_optimization.")`` prefix: the
#: ``llm_mentions`` operations share the family and are provider-index reads,
#: not answers.
AI_ANSWER_OPERATIONS = frozenset(
    {
        DataForSeoOperationName.AI_CHAT_GPT_LLM_RESPONSES.value,
        DataForSeoOperationName.AI_CLAUDE_LLM_RESPONSES.value,
        DataForSeoOperationName.AI_GEMINI_LLM_RESPONSES.value,
        DataForSeoOperationName.AI_PERPLEXITY_LLM_RESPONSES.value,
    }
)

#: Every normalizer module registered by default. The adapter is constructed
#: with no arguments everywhere, so this map IS the registration point; each
#: lane fills its own module and never edits this file. A normalizer carrying a
#: ``pending_owner`` attribute is registered but not built — the pre-run gate
#: refuses it (``unsupported_request_reason``).
DEFAULT_NORMALIZERS: dict[str, DataForSeoNormalizer] = {
    SERP_ORGANIC_OPERATION: normalize_serp_organic,
    **{operation: normalize_labs_keywords for operation in LABS_KEYWORD_OPERATIONS},
}

logger = logging.getLogger(__name__)


class DataForSeoAdapter(SeoProviderAdapter):
    provider = "dataforseo"
    capabilities = tuple(
        dict.fromkeys(
            capability for operation in APPROVED_OPERATIONS for capability in operation.capabilities
        )
    )
    operations = tuple(operation.provider_operation for operation in APPROVED_OPERATIONS)

    def __init__(
        self,
        *,
        transport: DataForSeoTransport | None = None,
        client: DataForSeoClient | None = None,
        normalizers: dict[str, DataForSeoNormalizer] | None = None,
    ) -> None:
        self._transport = transport
        self._configured_client = client
        self._client_context: ContextVar[DataForSeoClient | None] = ContextVar(
            f"dataforseo_client_{id(self)}", default=None
        )
        self._owned_client_context: ContextVar[bool] = ContextVar(
            f"dataforseo_owned_client_{id(self)}", default=False
        )
        self._response_context: ContextVar[ProviderResponse | None] = ContextVar(
            f"dataforseo_response_{id(self)}", default=None
        )
        self._normalizers = {**DEFAULT_NORMALIZERS, **(normalizers or {})}

    @property
    def last_response(self) -> ProviderResponse | None:
        return self._response_context.get()

    async def authenticate(self, credential: ResolvedCredential) -> None:
        missing = [key for key in DATAFORSEO_CREDENTIAL_KEYS if not credential.values.get(key)]
        if missing:
            raise ValueError(f"DataForSEO credential is missing: {', '.join(missing)}")
        client = self._configured_client
        owned = False
        if client is None:
            transport = self._transport
            if transport is None:
                transport = AsyncHttpTransport(
                    username=credential.values["DATA_FOR_SEO_EMAIL"],
                    password=credential.values["DATA_FOR_SEO_PASSWORD"],
                )
                owned = True
            client = DataForSeoClient(transport)
        self._client_context.set(client)
        self._owned_client_context.set(owned)

    def unsupported_request_reason(self, request: CollectionRequest) -> str | None:
        """Why this adapter can never complete ``request`` — or None.

        A normalized (non-``raw_provider``) collection needs a canonical
        normalizer for its operation. ``labs.google.competitors_domain`` (and
        every other COMPETITORS-capability operation) has none: competitor
        discovery reads that endpoint as ``raw_provider`` evidence
        (``competitor_autopsy.discover_and_classify_competitors``). Until
        2026-09-26 this refusal happened INSIDE ``collect_response`` — after a
        run was persisted — so the one request ever made for it (2026-08-11)
        became a failed run and a permanent high-severity
        ``seo_collection_failed:dataforseo:competitors`` platform alarm for a
        request that could never have succeeded. Answering here lets the
        service refuse BEFORE any run, budget, or provider I/O.
        """
        if request.capability is SeoCapability.RAW_PROVIDER:
            return None
        try:
            operation = get_operation(request.operation)
        except (KeyError, ValueError):
            return None  # the operation gate names an unknown operation itself
        if operation.raw_only:
            return None
        normalizer = self._normalizers.get(request.operation)
        if normalizer is not None:
            pending_owner = getattr(normalizer, "pending_owner", None)
            if pending_owner:
                return (
                    f"{request.operation} has no canonical normalizer for "
                    f"{request.capability.value} yet (owned by {pending_owner}) — collect "
                    "it as raw_provider evidence instead"
                )
            return None
        if (
            request.operation == "keywords.google_ads.search_volume"
            or request.operation in AI_ANSWER_OPERATIONS
        ):
            return None
        if request.capability is SeoCapability.BACKLINKS:
            try:
                endpoint = DataForSeoCollectionSettings.model_validate(request.settings).endpoint
            except ValueError:
                return None  # settings errors surface from collect_response unchanged
            if supports_backlink_endpoint(endpoint) or supports_intersection_endpoint(endpoint):
                return None
        return (
            f"{request.operation} has no registered canonical normalizer for "
            f"{request.capability.value} — collect it as raw_provider evidence instead"
        )

    async def collect_response(
        self,
        request: CollectionRequest,
        execution: ProviderExecutionContext,
    ) -> ProviderResponse:
        operation = get_operation(request.operation)
        if request.capability not in operation.capabilities:
            raise ValueError(f"{request.operation} cannot collect {request.capability.value}")
        settings = DataForSeoCollectionSettings.model_validate(request.settings)
        # Defensive twin of the pre-run gate (``unsupported_request_reason``,
        # enforced by ``SeoCollectionService._validated_request``): a run
        # persisted before that gate existed can still reach here on resume.
        reason = self.unsupported_request_reason(request)
        if reason is not None:
            raise NotImplementedError(reason)
        client = self._client_context.get()
        if client is None:
            raise RuntimeError("DataForSEO adapter must be authenticated before collection")
        response = await client.execute(
            DataForSeoOperationRequest(
                operation=operation.name,
                **settings.model_dump(),
            ),
            execution,
        )
        if self._owned_client_context.get():
            closer = getattr(client.transport, "aclose", None)
            if closer is not None:
                try:
                    await closer()
                except Exception as exc:
                    logger.exception(
                        "DataForSEO response captured but transport cleanup failed: %s",
                        exc,
                    )
            self._owned_client_context.set(False)
        self._response_context.set(response)
        return response

    async def normalize(
        self,
        response: ProviderResponse,
        context: NormalizationContext,
    ) -> list[SeoObservation]:
        if context.request.capability is SeoCapability.RAW_PROVIDER:
            return []
        normalizer = self._normalizers.get(context.request.operation)
        if normalizer is not None:
            return await normalizer(response, context)
        if context.request.operation == "keywords.google_ads.search_volume":
            return await normalize_google_ads_search_volume(response, context)
        if context.request.operation in AI_ANSWER_OPERATIONS:
            from .ai_answers import normalize_ai_answer_response

            return await normalize_ai_answer_response(response, context)
        if context.request.capability is SeoCapability.BACKLINKS:
            return _normalize_backlinks(response, context)
        return []

    def estimate_cost_usd(self, request: CollectionRequest) -> Decimal:
        """Price book estimate for ``request`` (``pricing.estimate``): summed
        per metered call, each call rounded on its own. Raises
        ``UnpricedOperationError`` for an operation the book does not price —
        never zero."""
        return estimate_operation_cost(request.operation, request.settings)

    async def aclose(self) -> None:
        client = self._client_context.get()
        if client is None or not self._owned_client_context.get():
            return
        closer = getattr(client.transport, "aclose", None)
        if closer is not None:
            await closer()
        self._owned_client_context.set(False)


async def normalize_google_ads_search_volume(
    response: ProviderResponse,
    context: NormalizationContext,
) -> list[SeoObservation]:
    """Normalize ``/v3/keywords_data/google_ads/search_volume`` into
    ``KeywordMarketObservation`` upserts.

    Keywords are identity-upserted (phrase + language only — the DB owns
    normalization and the Matrx System org). ``location_code`` is the
    provider's integer, stored directly — NO ``seo.location`` uuid indirection
    and NO location-catalog call. ``raw`` is the single keyword's result
    element only. Provider ``competition``/``competition_index`` are BOTH
    stored; provider intent/difficulty are dropped — the classifier owns
    intent."""
    raw = response.raw
    tasks = raw.get("tasks", []) if isinstance(raw, dict) else []
    rows: list[tuple[dict[str, Any], dict[str, Any], str | None]] = []
    requested_tasks = context.request.settings.get("tasks", [])
    for task_index, task in enumerate(tasks):
        if isinstance(task, dict) and isinstance(task.get("result"), list):
            task_data = task.get("data") if isinstance(task.get("data"), dict) else {}
            if task_index < len(requested_tasks) and isinstance(requested_tasks[task_index], dict):
                task_data = {**requested_tasks[task_index], **task_data}
            task_id = str(task.get("id")) if task.get("id") else None
            rows.extend(
                (item, task_data, task_id) for item in task["result"] if isinstance(item, dict)
            )
    identities = await context.resolve_identities(
        [
            SeoIdentityRequest(
                keyword=str(row.get("keyword") or "").strip(),
                language=str(row.get("language_code") or "en"),
            )
            for row, _task_data, _task_id in rows
            if str(row.get("keyword") or "").strip()
        ]
    )
    observations: list[SeoObservation] = []
    identity_index = 0
    for row, task_data, task_id in rows:
        if not str(row.get("keyword") or "").strip():
            continue
        identity = identities[identity_index]
        identity_index += 1
        location_code = row.get("location_code", task_data.get("location_code"))
        if location_code is None:
            raise ValueError(
                "DataForSEO search_volume result element has no location_code "
                f"(keyword {row.get('keyword')!r}) — refusing to guess a market"
            )
        monthly = [
            MonthlySearch(
                year=int(item["year"]),
                month=int(item["month"]),
                search_volume=int(item.get("search_volume") or 0),
            )
            for item in row.get("monthly_searches") or []
            if isinstance(item, dict) and item.get("year") and item.get("month")
        ]
        observations.append(
            KeywordMarketObservation(
                keyword_id=identity.keyword_id,
                location_code=int(location_code),
                search_volume=_optional_int(row.get("search_volume")),
                competition=(str(row["competition"]) if row.get("competition") else None),
                competition_index=_optional_int(row.get("competition_index")),
                cpc=_optional_decimal(row.get("cpc")),
                low_top_of_page_bid=_optional_decimal(row.get("low_top_of_page_bid")),
                high_top_of_page_bid=_optional_decimal(row.get("high_top_of_page_bid")),
                monthly_searches=monthly,
                metrics_task_id=task_id or response.external_task_id,
                raw=row,
                observed_at=response.fetched_at.astimezone(UTC),
            )
        )
    return observations


def _normalize_backlinks(
    response: ProviderResponse,
    context: NormalizationContext,
) -> list[SeoObservation]:
    request = context.request
    if request.site_id is None:
        raise ValueError("canonical backlink normalization requires site_id")
    settings = DataForSeoCollectionSettings.model_validate(request.settings)
    endpoint = get_operation(request.operation).endpoint_for(
        settings.workflow,
        settings.endpoint,
    )
    if supports_intersection_endpoint(endpoint):
        if not isinstance(response.raw, dict):
            raise ValueError("DataForSEO link-gap response must be a JSON object")
        task = settings.tasks[0] if settings.tasks else {}
        excluded = task.get("exclude_targets") or []
        return list(
            normalize_link_gap_payload(
                endpoint=endpoint,
                raw=response.raw,
                site_id=request.site_id,
                excluded_targets=excluded,
                fetched_at=response.fetched_at,
            )
        )
    if not supports_backlink_endpoint(endpoint):
        raise NotImplementedError(f"{endpoint} has no canonical backlink normalizer")
    targets = {
        str(task.get("target") or "").strip()
        for task in settings.tasks
        if str(task.get("target") or "").strip()
    }
    # Backstop. Every SUPPORTED_BACKLINK_ENDPOINTS entry is `/live`, and
    # DataForSeoCollectionSettings.validate_live_cardinality now rejects a
    # multi-task live request at build time — so this is unreachable through
    # today's endpoints and stays only to defend a future non-live one.
    if len(targets) != 1:
        raise ValueError(
            "canonical backlink collection requires every task to use one shared target"
        )
    if not isinstance(response.raw, dict):
        raise ValueError("DataForSEO backlink response must be a JSON object")
    return list(
        normalize_backlink_payload(
            endpoint=endpoint,
            raw=response.raw,
            site_id=request.site_id,
            page_id=request.page_id,
            target=next(iter(targets)),
            fetched_at=response.fetched_at,
        )
    )


def _optional_decimal(value: Any) -> Decimal | None:
    return Decimal(str(value)) if value is not None else None


def _optional_int(value: Any) -> int | None:
    return int(value) if value is not None else None
