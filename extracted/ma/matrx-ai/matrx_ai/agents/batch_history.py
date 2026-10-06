"""A provider-batch unit's history, kept the ONE way every AI run keeps it.

Owner ruling (Arman, 2026-10-05): every AI run keeps its history through the
same conversation + messages + cost + request snapshot every chat gets, so it
opens and reads like any chat. A unit sent through a provider Batch API never
touches ``execute_ai_request``, so without this module it left only a
``batch.work_item`` row.

This module is the smallest adapter onto the EXISTING writers — no parallel
writer:

* :func:`completed_request_from_batch` — the stored batch answer in the exact
  ``CompletedRequest`` shape a provider turn comes back in (the rendered
  request's messages + the assistant answer + one usage row whose cost is the
  ACTUAL batch cost).
* :func:`record_batch_unit` — hands that turn to the shared
  ``matrx_ai.agents.run_history.record_turn`` (conversation gate →
  ``persist_completed_request`` → the executor's ``_write_request_snapshot``,
  inside one standalone Coordinator) — the same adapter every off-engine call
  (probes, replays, realtime sessions) records through.

The conversation id is DERIVED from the work item id
(:func:`batch_conversation_id`), so a result handler that runs later finds the
conversation without being told, and a re-drive never writes a second one.

The caller (the host's ``history_recorder``) supplies the ambient AppContext —
actor + organization of the work item. This module only narrows it to the run
(conversation id, request id, persisting system run that keeps its transcript).
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any

#: Namespace for :func:`batch_conversation_id` — fixed forever.
_BATCH_CONVERSATION_NS = uuid.UUID("6b0c9d1e-3f57-4a52-9a1e-b47c0de5a7c1")

#: Where the render seam's canonical request rides the work item metadata.
UNIFIED_REQUEST_METADATA_KEY = "unified_request"


def batch_conversation_id(work_item_id: str) -> str:
    """The conversation a batch work item's run is kept in. Deterministic."""
    return str(uuid.uuid5(_BATCH_CONVERSATION_NS, f"batch.work_item:{work_item_id}"))


def batch_request_id(work_item_id: str) -> str:
    """The ``chat.user_request`` id of a batch work item's run. Deterministic."""
    return str(uuid.uuid5(_BATCH_CONVERSATION_NS, f"batch.user_request:{work_item_id}"))


def _batch_usage_class() -> type:
    from matrx_ai.config.usage_config import TokenUsage

    @dataclass
    class BatchTokenUsage(TokenUsage):
        """A batch call's usage. Its COST is what the provider batch charged
        (the poller's batch-rate price); the catalog's live-rate cost stays
        available as ``calculate_catalog_cost`` — the request row records it as
        ``metadata.catalog_cost_usd``, the live equivalent."""

        batch_cost_usd: float | None = None

        def calculate_cost(self, pricing_lookup: Any = None) -> float | None:  # type: ignore[override]
            if self.batch_cost_usd is not None:
                return float(self.batch_cost_usd)
            return super().calculate_cost(pricing_lookup)

    return BatchTokenUsage


@dataclass(frozen=True)
class BatchUnit:
    """One finished batch work item, as the recorder receives it."""

    work_item_id: str
    provider: str
    model: str
    #: The provider body exactly as submitted (``batch.work_item.payload``).
    provider_request: dict[str, Any]
    #: ``AIMatrixRequest.to_dict()`` captured at render time, or None.
    unified_request: dict[str, Any] | None
    succeeded: bool
    result: dict[str, Any] | None
    error: dict[str, Any] | None
    tokens_in: int = 0
    tokens_out: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    actual_cost_usd: float | None = None


def completed_request_from_batch(unit: BatchUnit, *, conversation_id: str, request_id: str) -> Any:
    """The batch answer as the ``CompletedRequest`` a live provider turn returns."""
    from matrx_ai.agents.batch_render import output_text_from_batch_result
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_config import UnifiedConfig, UnifiedResponse
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    if not isinstance(unit.unified_request, dict):
        raise ValueError(
            f"batch work item {unit.work_item_id} carries no {UNIFIED_REQUEST_METADATA_KEY!r} — "
            "it was enqueued before the render seam captured the canonical request, so its "
            "messages cannot be kept as a conversation"
        )
    request = AIMatrixRequest.from_dict(dict(unit.unified_request))
    request.conversation_id = conversation_id
    request.request_id = request_id
    if not isinstance(request.config, UnifiedConfig):  # pragma: no cover - from_dict contract
        raise ValueError("unified_request.config did not deserialize to a UnifiedConfig")

    text = output_text_from_batch_result(unit.provider, unit.result) if unit.succeeded else ""
    usage = _batch_usage_class()(
        input_tokens=int(unit.tokens_in or 0) + int(unit.cache_write_tokens or 0),
        output_tokens=int(unit.tokens_out or 0),
        cached_input_tokens=int(unit.cache_read_tokens or 0),
        matrx_model_name=unit.model,
        provider_model_name=unit.model,
        api=unit.provider,
        metadata={"iteration": 1, "lane": "batch", "work_item_id": unit.work_item_id},
        batch_cost_usd=unit.actual_cost_usd,
    )
    request.add_usage(usage)
    messages = [UnifiedMessage(role="assistant", content=[TextContent(text=text)])] if text else []
    status = "success" if (unit.succeeded and text) else "failed"
    final = UnifiedResponse(
        messages=messages,
        usage=usage,
        finish_reason="stop" if status == "success" else "error",
        stop_reason="end_turn" if status == "success" else "error",
        metadata={"lane": "batch", "work_item_id": unit.work_item_id},
    )
    if messages:
        request = AIMatrixRequest.add_response(request, final)
    meta: dict[str, Any] = {
        "status": status,
        "finish_reason": final.finish_reason,
        "lane": "batch",
        "work_item_id": unit.work_item_id,
    }
    if status == "failed":
        meta["error"] = unit.error or {"kind": "no_output_text"}
    return CompletedRequest(request=request, iterations=1, final_response=final, metadata=meta)


@dataclass(frozen=True)
class BatchHistoryRecord:
    conversation_id: str
    request_id: str
    message_ids: list[str]
    request_ids: list[str]
    snapshot_id: str


async def record_batch_unit(unit: BatchUnit, *, source_feature: str) -> BatchHistoryRecord:
    """Keep ``unit`` as a conversation through the ordinary funnel.

    Needs an ambient AppContext carrying the work item's actor + organization.
    Idempotent per work item: a conversation already on disk is left alone.
    Raises on failure — the caller decides how loudly (it must never block the
    batch result landing)."""
    # A fresh task gets a COPY of the ambient context, so every override below
    # stays inside this run and never leaks into the caller's context.
    return await asyncio.create_task(_record(unit, source_feature=source_feature))


async def _record(unit: BatchUnit, *, source_feature: str) -> BatchHistoryRecord:
    from matrx_ai.agents.run_history import RunTurn, record_turn

    conversation_id = batch_conversation_id(unit.work_item_id)
    request_id = batch_request_id(unit.work_item_id)
    if await _conversation_exists(conversation_id):
        return BatchHistoryRecord(conversation_id, request_id, [], [], "")

    completed = completed_request_from_batch(
        unit, conversation_id=conversation_id, request_id=request_id
    )
    message_count = len(completed.request.config.messages.to_list())
    record = await record_turn(
        RunTurn(
            completed=completed,
            provider=unit.provider,
            model=unit.model,
            trigger_position=max(
                0, message_count - (2 if completed.final_response.messages else 1)
            ),
            assistant_position=message_count - 1,
            # The provider body exactly as submitted, and its own answer
            # verbatim — or its error envelope.
            request_payload=unit.provider_request,
            unified_payload=unit.unified_request,
            response_payload=unit.result if unit.result is not None else (unit.error or {}),
            metadata={"batch_work_item_id": unit.work_item_id},
            # The whole rendered request is new: every message is written.
            write_from=0,
        ),
        source_feature=source_feature,
        system_run=True,
        new_conversation=True,
        reason="batch_unit_history",
    )
    return BatchHistoryRecord(
        conversation_id=record.conversation_id,
        request_id=record.request_id,
        message_ids=record.message_ids,
        request_ids=record.request_ids,
        snapshot_id=record.snapshot_id,
    )


async def _conversation_exists(conversation_id: str) -> bool:
    from matrx_ai.db.cx_managers import cxm

    try:
        row = await cxm.conversation.load_conversation_by_id(conversation_id)
    except Exception:  # noqa: BLE001 — "not found" raises on some manager versions
        return False
    return row is not None


__all__ = [
    "UNIFIED_REQUEST_METADATA_KEY",
    "BatchHistoryRecord",
    "BatchUnit",
    "batch_conversation_id",
    "batch_request_id",
    "completed_request_from_batch",
    "record_batch_unit",
]
