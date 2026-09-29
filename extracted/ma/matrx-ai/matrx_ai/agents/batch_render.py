"""Render a DB agent into a provider request body WITHOUT executing it.

The platform Batch system submits agent work through provider Batch APIs
(~50% price). The whole point of the design is that batch reuses the
EXISTING agent machinery — same DB agents, same variable templating, same
catalog resolution, same translators — with only the dispatch deferred.
This module is that seam:

* :func:`render_agent_provider_request` — Agent (variables applied, user
  input set) → the exact provider-flavoured body the live path would have
  sent, via ``UnifiedAIClient.translate_request`` (the validated build-only
  chokepoint every live call already goes through). Never a hand-built
  payload, never a second prompt renderer.
* :func:`prefix_group_key_for` — stable fingerprint of the shared prefix
  (provider, model, system, tools). Work items sharing a key share one
  provider batch, which is what makes prompt caching pay (Anthropic: batch
  50% × cache-read 0.1× stack).
* :func:`output_text_from_batch_result` — the inverse seam: pull the
  assistant text out of a stored batch result payload so slot/agent parse
  funnels can consume it exactly as they consume a live output.
* :func:`conform_batch_answer` — the batch answer's pass through the SAME
  step every live answer takes at the dispatch seam
  (``schema.answer_contract.conform_answer_to_contract`` +
  ``verify_answer_and_record``), against the AUTHOR's contract captured at
  render time (:attr:`RenderedAgentRequest.answer_contract`). matrx-batch's
  handler dispatcher calls it (host slot ``answer_conformer``) before any result
  handler reads the answer.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

_WIRE_FORMAT_PROVIDER: dict[str, str] = {
    "openai_chat": "openai",
    "anthropic_chat": "anthropic",
    "google_chat": "gemini",
    "cerebras_chat": "cerebras",
    "together_chat": "together",
    "groq_chat": "groq",
    "xai_chat": "xai",
    "huggingface_chat": "generic_openai",
    "generic_openai_chat": "generic_openai",
}

BATCHABLE_PROVIDERS = ("anthropic", "openai", "gemini")
"""Providers the Batch system can submit to today (all 50% off; Anthropic
also stacks prompt caching). Others fall back to live dispatch."""


@dataclass(frozen=True)
class RenderedAgentRequest:
    provider: str
    model: str
    payload: dict[str, Any]
    prefix_group_key: str
    #: The contract the AUTHOR declared, as the live dispatch seam binds it —
    #: ``{"schema", "name", "enforced", "dropped_because"?, "agent_id", ...}`` —
    #: or ``None`` when the agent declares no structured output. Rides the work
    #: item (``WorkItemSpec.answer_contract``) so the answer, hours later, is
    #: conformed and checked against THIS, never the provider's wire copy.
    answer_contract: dict[str, Any] | None = None


async def render_agent_provider_request(agent: Any) -> RenderedAgentRequest:
    """Agent → provider body, via the one validated translate chokepoint.

    The agent must already carry its variables/user input (callers use
    ``Agent.from_agent(..., variables=...)`` + ``set_user_input``); this
    applies them idempotently the same way ``Agent.execute`` does."""
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    if (agent.variable_values or agent.variable_defaults) and not agent._variables_applied:
        await agent.prepare_variables()  # the pre-substitution step, as execute runs it
        agent.apply_variables()

    from matrx_ai.catalog.resolve import resolve_call_profile

    profile = await resolve_call_profile(
        agent.config.model, offering_id=getattr(agent.config, "routing_offering_id", None)
    )
    provider = _WIRE_FORMAT_PROVIDER.get(profile.wire_format or "")
    if provider is None:
        raise ValueError(
            f"render_agent_provider_request: wire_format {profile.wire_format!r} "
            f"(model={agent.config.model!r}) has no provider mapping."
        )

    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        declared_output_contract,
        release_declared_output_contract,
    )

    request = AIMatrixRequest(conversation_id="batch-render", config=agent.config)
    # Bound exactly as the live seam binds it (before the capability gates can
    # replace ``response_format``), so a translator that drops enforcement for
    # this model marks it here too, and the contract read back after the build is
    # the one the live path would have judged the answer against.
    contract_token = bind_declared_output_contract(getattr(agent.config, "response_format", None))
    try:
        payload = await UnifiedAIClient().translate_request(request, batch=True)
        contract = declared_output_contract()
    finally:
        release_declared_output_contract(contract_token)
    answer_contract: dict[str, Any] | None = None
    if contract is not None:
        answer_contract = {
            **contract,
            "agent_id": str(getattr(agent, "source_id", None) or "") or None,
            "agent_is_version": bool(getattr(agent, "source_is_version", False)),
            "agent_name": getattr(agent, "name", None),
        }
    # Live-path builders strip/attach streaming details; batch bodies must
    # never carry a stream flag.
    payload.pop("stream", None)
    model = str(payload.get("model") or agent.config.model)
    return RenderedAgentRequest(
        provider=provider,
        model=model,
        payload=payload,
        prefix_group_key=prefix_group_key_for(provider=provider, model=model, payload=payload),
        answer_contract=answer_contract,
    )


def prefix_group_key_for(*, provider: str, model: str, payload: dict[str, Any]) -> str:
    """Stable sha256 over the shared prefix: provider + model + system + tools.

    Items with the same key share one provider batch → contiguous same-prefix
    requests → best-effort cache hits."""
    config = payload.get("config") if isinstance(payload.get("config"), dict) else {}
    system = (
        payload.get("system")
        or payload.get("instructions")
        or config.get("system_instruction")
        or ""
    )
    tools = payload.get("tools") or config.get("tools") or []
    blob = json.dumps(
        {"provider": provider, "model": model, "system": system, "tools": tools},
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def output_text_from_batch_result(provider: str, result_payload: dict[str, Any] | None) -> str:
    """Assistant text from a stored ``batch.work_item.result`` payload.

    Shapes (as landed by matrx_batch.poller):
      * anthropic — ``{"message": {content: [{type: "text", text: ...}, ...]}}``
      * openai    — ``{"response": {body: {choices: [{message: {content}}]}}}`` (chat)
                    or ``{"response": {body: {output: [{type: "message", content: [{type: "output_text", text}]}]}}}`` (responses)
    """
    if not result_payload:
        return ""
    if provider == "anthropic":
        message = result_payload.get("message") or {}
        parts = [
            str(block.get("text") or "")
            for block in (message.get("content") or [])
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "\n".join(p for p in parts if p)
    if provider == "openai":
        response = result_payload.get("response") or {}
        body = response.get("body") or response
        # Chat Completions shape.
        choices = body.get("choices") or []
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message") or {}
            content = message.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "\n".join(str(c.get("text") or "") for c in content if isinstance(c, dict))
        # Responses API shape (what the OpenAI translator emits; batch endpoint
        # /v1/responses): output[] message items → content[] output_text parts.
        parts: list[str] = []
        for item in body.get("output") or []:
            if not isinstance(item, dict) or item.get("type") not in (None, "message"):
                continue
            for part in item.get("content") or []:
                if isinstance(part, dict) and part.get("type") == "output_text":
                    parts.append(str(part.get("text") or ""))
        return "\n".join(p for p in parts if p)
    if provider == "gemini":
        response = result_payload.get("response") or {}
        candidates = response.get("candidates") or []
        if candidates and isinstance(candidates[0], dict):
            content = candidates[0].get("content") or {}
            parts = content.get("parts") or []
            return "\n".join(
                str(p.get("text") or "")
                for p in parts
                if isinstance(p, dict) and p.get("text") and not p.get("thought")
            )
        return ""
    return ""


def _batch_result_calls_tool(provider: str, result_payload: dict[str, Any] | None) -> bool:
    """Whether the stored answer is a TOOL-CALL turn rather than the answer.

    The live check judges only the turn that answers (``_turn_is_final``); a
    batch answer is judged by the same rule, read off the provider's own shape."""
    if not result_payload:
        return False
    if provider == "anthropic":
        message = result_payload.get("message") or {}
        if message.get("stop_reason") == "tool_use":
            return True
        return any(
            isinstance(b, dict) and b.get("type") == "tool_use"
            for b in message.get("content") or []
        )
    if provider == "openai":
        response = result_payload.get("response") or {}
        body = response.get("body") or response
        for choice in body.get("choices") or []:
            if isinstance(choice, dict) and (
                choice.get("finish_reason") == "tool_calls"
                or (choice.get("message") or {}).get("tool_calls")
            ):
                return True
        return any(
            isinstance(i, dict) and i.get("type") == "function_call" for i in body.get("output") or []
        )
    if provider == "gemini":
        response = result_payload.get("response") or {}
        for candidate in response.get("candidates") or []:
            for part in ((candidate or {}).get("content") or {}).get("parts") or []:
                if isinstance(part, dict) and part.get("functionCall"):
                    return True
    return False


def with_output_text(
    provider: str, result_payload: dict[str, Any], text: str
) -> dict[str, Any]:
    """The inverse of :func:`output_text_from_batch_result`: a COPY of the stored
    payload whose answer text is ``text``. Every non-text block (tool use,
    thinking, citations metadata) stays where it was; the answer's text parts
    collapse into one part at the position of the first, so
    :func:`output_text_from_batch_result` returns exactly ``text``."""
    import copy

    payload = copy.deepcopy(result_payload)

    def _collapse(parts: list[Any], is_text: Any, make: Any) -> list[Any]:
        out: list[Any] = []
        placed = False
        for part in parts:
            if is_text(part):
                if not placed:
                    out.append(make(part))
                    placed = True
                continue
            out.append(part)
        if not placed:
            out.append(make(None))
        return out

    if provider == "anthropic":
        message = payload.setdefault("message", {})
        message["content"] = _collapse(
            list(message.get("content") or []),
            lambda b: isinstance(b, dict) and b.get("type") == "text",
            lambda _b: {"type": "text", "text": text},
        )
        return payload
    if provider == "openai":
        response = payload.setdefault("response", {})
        body = response["body"] if isinstance(response.get("body"), dict) else response
        choices = body.get("choices") or []
        if choices and isinstance(choices[0], dict):
            choices[0].setdefault("message", {})["content"] = text
            return payload
        for item in body.get("output") or []:
            if isinstance(item, dict) and item.get("type") in (None, "message"):
                item["content"] = _collapse(
                    list(item.get("content") or []),
                    lambda p: isinstance(p, dict) and p.get("type") == "output_text",
                    lambda p: {**(p or {"type": "output_text", "annotations": []}), "text": text},
                )
                return payload
        raise ValueError("openai batch result carries no answer message to rewrite")
    if provider == "gemini":
        response = payload.setdefault("response", {})
        candidates = response.get("candidates") or []
        if not candidates or not isinstance(candidates[0], dict):
            raise ValueError("gemini batch result carries no candidate to rewrite")
        content = candidates[0].setdefault("content", {})
        content["parts"] = _collapse(
            list(content.get("parts") or []),
            lambda p: isinstance(p, dict) and p.get("text") and not p.get("thought"),
            lambda _p: {"text": text},
        )
        return payload
    raise ValueError(f"no batch result shape known for provider {provider!r}")


async def conform_batch_answer(item: Any, *, record_findings: bool = True) -> list[str]:
    """Put a BATCH answer through the one step every live answer takes.

    ``item`` is a matrx-batch ``HandlerItem`` (``provider``, ``model``,
    ``result``, ``answer_contract``, ``id``, ``custom_id``, ``purpose``). The
    AUTHOR's contract captured at render time is re-bound, the stored answer is
    wrapped as the final assistant turn, and the SAME
    ``conform_answer_to_contract`` (a ``null`` the provider boundary asked for
    becomes the absence the author declared) and ``verify_answer_and_record``
    (an off-contract answer is recorded naming the agent and the shape) run on
    it. When conforming changed the answer, ``item.result`` is replaced by a
    copy carrying the conformed text — so every result handler, reading it with
    :func:`output_text_from_batch_result`, gets the author's shape.

    ``record_findings=False`` conforms without recording (a re-delivery of an
    item already judged). Returns the changes made plus the problems found.
    """
    from matrx_ai.config.message_config import UnifiedMessage
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.schema.answer_contract import (
        conform_answer_to_contract,
        release_declared_output_contract,
        use_declared_output_contract,
        verify_answer_and_record,
    )

    contract = getattr(item, "answer_contract", None)
    provider = str(getattr(item, "provider", "") or "")
    result = getattr(item, "result", None)
    if not isinstance(contract, dict) or not isinstance(result, dict):
        return []
    text = output_text_from_batch_result(provider, result)
    if not text:
        return []

    class _BatchAnswer:
        """The stored answer, in the shape the dispatch seam's step reads."""

        def __init__(self) -> None:
            self.messages = [UnifiedMessage(role="assistant", content=[TextContent(text=text)])]
            self.finish_reason = (
                "tool_calls" if _batch_result_calls_tool(provider, result) else "stop"
            )

    answer = _BatchAnswer()
    token = use_declared_output_contract(contract)
    try:
        changes = conform_answer_to_contract(answer)
        if changes:
            conformed = "".join(
                block.text
                for block in answer.messages[0].content
                if isinstance(block, TextContent)
            )
            item.result = with_output_text(provider, result, conformed)
        problems: list[str] = []
        if record_findings:
            identity = {
                key: contract.get(key)
                for key in ("agent_id", "agent_is_version", "agent_name")
                if contract.get(key) is not None
            }
            identity.update(
                {
                    "lane": "batch",
                    "batch_work_item_id": str(getattr(item, "id", "") or "") or None,
                    "batch_custom_id": str(getattr(item, "custom_id", "") or "") or None,
                    "source_feature": getattr(item, "purpose", None),
                    "agent_attribution": (
                        f"batch work item {getattr(item, 'custom_id', '?')} "
                        f"({getattr(item, 'purpose', '?')}), agent "
                        f"{contract.get('agent_name') or contract.get('agent_id') or 'unnamed'}"
                    ),
                }
            )
            problems = await verify_answer_and_record(
                answer,
                provider=provider,
                model=getattr(item, "model", None),
                identity={k: v for k, v in identity.items() if v is not None},
            )
        return [*changes, *problems]
    finally:
        release_declared_output_contract(token)


__all__ = [
    "BATCHABLE_PROVIDERS",
    "conform_batch_answer",
    "with_output_text",
    "RenderedAgentRequest",
    "render_agent_provider_request",
    "prefix_group_key_for",
    "output_text_from_batch_result",
]
