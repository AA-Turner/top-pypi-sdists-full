"""A code call whose mandate a WORKFLOW holds — the one shared adapter.

WHY THIS EXISTS
---------------
A mandate is filled by an agent **or** a workflow, equally (MANDATE-SYSTEM.md
§1). ``matrx_ai.mandates.hold_code_call`` is the door most server code calls
use (labelers, judges, synthesizers, the content planner, the memory
observer…). Until 2026-09-26 it refused a workflow Holder in words and wrote a
``mandate_resolution_failed`` row, because a code call takes its model and
prompt from an agent — so binding a workflow to any of those jobs broke the
job. Arman's top priority: every mandate works equally whichever kind fills it.

HOW IT WORKS — one seam, zero per-site changes
----------------------------------------------
Every held site hands ``held.metadata`` (the Holder stamp) to the funnel it
calls — ``llm_to_text`` / ``llm_to_pydantic`` / ``llm_messages_to_pydantic``
and their measured/streaming twins, ``run_held_call`` / ``run_held_text`` /
``run_held_pydantic``, or ``execute_ai_request`` directly. They ALL reach a
provider only through ``execute_ai_request``, and that is where this adapter
sits: a request stamped ``holder_type="workflow"`` never reaches a provider.
Instead:

1. **Inputs.** The site's OFFERED values (``hold_code_call(variables=...)``)
   are the workflow's inputs; the host runs them through the ONE consumption
   pipeline onto the workflow's input surface. A site that composes its data
   into the user turn instead of offering it (a pre-provision residue) has
   that turn delivered as the ONE declared offered value it left unfilled —
   the "as the user turn" pattern. Anything else is left to the pipeline,
   which refuses a broken promise in words (never a guess).
2. **Run.** ``MandateResolution.run_workflow`` (injected by the host) runs the
   workflow as a durable child ``workflow.run`` — same identity for the same
   inputs, so a funnel's parse-repair retry reattaches instead of paying twice
   (and is answered from this holding's cache without a second call at all).
   The caller's emitter carries the child's events when the request streams;
   cancelling the caller cancels the awaited child.
3. **Answer.** The workflow's deliverable comes back as the assistant message
   of a ``CompletedRequest`` — text (JSON text for a structured answer, which
   ``llm_to_pydantic`` then validates exactly as it validates a model's), plus
   an image/audio part when the deliverable is media — with the child run's
   measured spend as the usage, so measured funnels report real dollars.
4. **Shape.** A deliverable that misses the mandate's declared kind or keys is
   a WARNING (Arman, 2026-09-25: validation offers, never blocks): the best
   answer is still returned, the miss is said on the request metadata
   (``workflow_holder.warnings``) and captured by the host.

``hold_code_call`` registers the holding here (weakly — it lives exactly as
long as the site's ``HeldCall``) and stamps its id into the Holder metadata;
``execute_ai_request`` looks it up with :func:`holding_for_metadata`.
"""

from __future__ import annotations

import hashlib
import json
import uuid
import weakref
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

#: Host runner: ``(supplied, *, correlation_key, stream) -> answer dict`` with
#: ``output`` / ``parsed`` / ``run_id`` / ``workflow_id`` / ``workflow_name`` /
#: ``warnings`` / ``cost`` (the host's run-cost summary).
WorkflowHolderRunner = Callable[..., Awaitable[dict[str, Any]]]

#: The key inside the ``mandate_holder`` stamp naming the live holding.
HELD_CALL_ID_KEY = "held_call_id"

_MEDIA_KINDS = ("image", "audio")

_HOLDINGS: weakref.WeakValueDictionary[str, WorkflowHolding] = weakref.WeakValueDictionary()


class WorkflowHolding:
    """One ``hold_code_call`` resolved to a workflow: what to deliver, how to run."""

    def __init__(
        self,
        *,
        mandate_key: str,
        consumer: str,
        workflow_id: str,
        workflow_version_id: str | None,
        output_kind: str | None,
        offered_values: tuple[Any, ...],
        supplied: dict[str, Any],
        runner: WorkflowHolderRunner,
    ) -> None:
        self.held_call_id = str(uuid.uuid4())
        self.mandate_key = mandate_key
        self.consumer = consumer
        self.workflow_id = workflow_id
        self.workflow_version_id = workflow_version_id
        self.output_kind = output_kind
        self.offered_values = tuple(offered_values)
        self.supplied = dict(supplied)
        self.runner = runner
        #: correlation key → the host's answer, so a repeat of the SAME inputs
        #: (a strict-JSON repair retry) is answered without a second run.
        self._answers: dict[str, dict[str, Any]] = {}
        #: The most recent answer, for ``HeldCall.finish`` (cost + run id).
        self.last_answer: dict[str, Any] | None = None
        _HOLDINGS[self.held_call_id] = self

    # ── inputs ─────────────────────────────────────────────────────────────

    def delivered_values(self, user_text: str) -> tuple[dict[str, Any], list[str]]:
        """The values the workflow receives, and a note for each fill made."""
        delivered = dict(self.supplied)
        notes: list[str] = []
        declared = [v for v in self.offered_values if getattr(v, "name", "")]
        missing = [v for v in declared if delivered.get(v.name) in (None, "")]
        if user_text.strip() and len(missing) == 1:
            target = missing[0]
            if str(getattr(target, "kind", "") or "") in ("file", *_MEDIA_KINDS, "video"):
                notes.append(
                    f"the call site sends its {target.name!r} ({target.kind}) inside the user "
                    "turn instead of offering it, and a media value cannot be read back out of "
                    "a composed turn — offer it by name through hold_code_call(variables=...)"
                )
            else:
                delivered[target.name] = user_text
                notes.append(
                    f"the call site composed its user turn instead of offering {target.name!r}; "
                    "that turn was delivered as the value"
                )
        return delivered, notes

    def correlation_key(self, delivered: dict[str, Any]) -> str:
        digest = hashlib.sha256(
            json.dumps(delivered, sort_keys=True, default=str, ensure_ascii=False).encode()
        ).hexdigest()[:24]
        return f"{self.held_call_id}:{digest}"

    # ── the run ────────────────────────────────────────────────────────────

    async def answer(self, config: Any, metadata: dict[str, Any] | None) -> Any:
        """Run the workflow for this request and return a ``CompletedRequest``."""
        user_text = last_user_text(config)
        delivered, notes = self.delivered_values(user_text)
        key = self.correlation_key(delivered)
        cached = self._answers.get(key)
        reattached = cached is not None
        if cached is None:
            vcprint(
                f"[mandates] {self.mandate_key} ({self.consumer}) is held by WORKFLOW "
                f"{self.workflow_id} — running it as a child run "
                f"(inputs: {sorted(delivered)})",
                color="cyan",
            )
            cached = await self.runner(
                delivered,
                correlation_key=key,
                stream=bool(getattr(config, "stream", False)),
            )
            self._answers[key] = cached
        self.last_answer = cached
        return completed_from_answer(
            config,
            metadata,
            cached,
            workflow_id=self.workflow_id,
            notes=notes,
            # A repeat of the same inputs was already paid for once.
            charge=not reattached,
        )


def register_holding(**kwargs: Any) -> WorkflowHolding:
    return WorkflowHolding(**kwargs)


def holding_for_metadata(metadata: dict[str, Any] | None) -> WorkflowHolding | None | bool:
    """The live holding a request's metadata names.

    ``None`` — the request is not workflow-held (the normal case).
    ``False`` — it IS stamped workflow-held but the holding is gone (the
    ``HeldCall`` was dropped, or the metadata crossed a process): the caller
    must refuse in words, never send a provider a workflow's name as a model.
    """
    if not isinstance(metadata, dict):
        return None
    from matrx_ai.orchestrator.mandate_carrier import MANDATE_HOLDER_METADATA_KEY

    stamp = metadata.get(MANDATE_HOLDER_METADATA_KEY)
    if not isinstance(stamp, dict) or stamp.get("holder_type") != "workflow":
        return None
    held_id = str(stamp.get(HELD_CALL_ID_KEY) or "")
    holding = _HOLDINGS.get(held_id) if held_id else None
    return holding if holding is not None else False


def last_user_text(config: Any) -> str:
    """The text of the request's last user turn (what a composing site sent)."""
    messages = getattr(config, "messages", None)
    items = messages.to_list() if hasattr(messages, "to_list") else list(messages or [])
    for message in reversed(items):
        role = message.get("role") if isinstance(message, dict) else getattr(message, "role", "")
        if str(role).lower() != "user":
            continue
        content = (
            message.get("content") if isinstance(message, dict) else getattr(message, "content", None)
        )
        if isinstance(content, str):
            return content
        pieces: list[str] = []
        for part in content or []:
            if isinstance(part, str):
                pieces.append(part)
            elif isinstance(part, dict) and part.get("type") == "text":
                pieces.append(str(part.get("text") or ""))
            elif getattr(part, "type", None) == "text":
                pieces.append(str(getattr(part, "text", "") or ""))
        return "\n".join(p for p in pieces if p)
    return ""


def _media_part(parsed: Any) -> Any | None:
    """An image/audio deliverable as the content part a media site reads."""
    if not isinstance(parsed, dict):
        return None
    file_id = parsed.get("file_id")
    url = parsed.get("url") or parsed.get("public_url")
    mime = str(parsed.get("mime_type") or parsed.get("mime") or "")
    marker = str(parsed.get("__kind") or parsed.get("kind") or "")
    if not file_id or not url:
        return None
    if mime.startswith("image/") or marker == "image":
        from matrx_ai.config.media_config import ImageContent

        return ImageContent(url=str(url), file_id=str(file_id), mime_type=mime or "image/png")
    if mime.startswith("audio/") or marker == "audio":
        from matrx_ai.config.media_config import AudioContent

        return AudioContent(url=str(url), file_id=str(file_id), mime_type=mime or "audio/wav")
    return None


def completed_from_answer(
    config: Any,
    metadata: dict[str, Any] | None,
    answer: dict[str, Any],
    *,
    workflow_id: str,
    notes: list[str] | None = None,
    charge: bool = True,
) -> Any:
    """The workflow's answer in the exact shape a provider turn comes back in."""
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_config import UnifiedResponse
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.config.usage_config import (
        AggregatedUsage,
        ModelUsageSummary,
        TokenUsage,
        UsageTotals,
    )
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

    from matrx_connect.context.app_context import try_get_app_context

    output = answer.get("output")
    text = output if isinstance(output, str) else json.dumps(output, ensure_ascii=False, default=str)
    parts: list[Any] = [TextContent(text=text or "")]
    media = _media_part(answer.get("parsed"))
    if media is not None:
        parts.append(media)

    cost = dict(answer.get("cost") or {}) if charge else {}
    input_tokens = int(cost.get("total_input_tokens") or 0)
    output_tokens = int(cost.get("total_output_tokens") or 0)
    dollars = float(cost.get("total_cost_usd") or 0.0)
    label = f"workflow:{workflow_id}"
    usage = TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        matrx_model_name=label,
        api="workflow",
        metadata={"workflow_run_id": answer.get("run_id"), "cost_usd": dollars},
    )
    total = AggregatedUsage(
        by_model={
            label: ModelUsageSummary(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens,
                api="workflow",
                request_count=int(cost.get("request_count") or 0),
                cost=dollars,
            )
        },
        total=UsageTotals(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            total_requests=int(cost.get("request_count") or 0),
            unique_models=1,
            total_cost=dollars,
            known_cost_subtotal=dollars,
        ),
    )
    warnings = [*(answer.get("warnings") or []), *(notes or [])]
    facts = {
        "workflow_id": workflow_id,
        "workflow_version_id": answer.get("workflow_version_id"),
        "workflow_name": answer.get("workflow_name") or "",
        "run_id": answer.get("run_id"),
        "warnings": warnings,
        "reattached": not charge,
    }
    ctx = try_get_app_context()
    conversation_id = str(getattr(ctx, "conversation_id", "") or "") or str(uuid.uuid4())
    request = AIMatrixRequest(
        conversation_id=conversation_id,
        config=config,
        request_id=str(getattr(ctx, "request_id", "") or "") or None,
        organization_id=getattr(ctx, "organization_id", None),
        metadata={**dict(metadata or {}), "workflow_holder": facts},
    )
    final = UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=parts)],
        usage=usage,
        finish_reason="stop",
        stop_reason="end_turn",
        metadata={"workflow_holder": facts},
    )
    return CompletedRequest(
        request=request,
        iterations=1,
        final_response=final,
        total_usage=total,
        metadata={"status": "success", "holder_type": "workflow", "workflow_holder": facts},
    )
