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


async def render_agent_provider_request(agent: Any) -> RenderedAgentRequest:
    """Agent → provider body, via the one validated translate chokepoint.

    The agent must already carry its variables/user input (callers use
    ``Agent.from_agent(..., variables=...)`` + ``set_user_input``); this
    applies them idempotently the same way ``Agent.execute`` does."""
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    if (agent.variable_values or agent.variable_defaults) and not agent._variables_applied:
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

    request = AIMatrixRequest(conversation_id="batch-render", config=agent.config)
    payload = await UnifiedAIClient().translate_request(request)
    # Live-path builders strip/attach streaming details; batch bodies must
    # never carry a stream flag.
    payload.pop("stream", None)
    model = str(payload.get("model") or agent.config.model)
    return RenderedAgentRequest(
        provider=provider,
        model=model,
        payload=payload,
        prefix_group_key=prefix_group_key_for(provider=provider, model=model, payload=payload),
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
      * openai    — ``{"response": {body: {choices: [{message: {content}}]}}}``
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
        choices = body.get("choices") or []
        if choices and isinstance(choices[0], dict):
            message = choices[0].get("message") or {}
            content = message.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return "\n".join(str(c.get("text") or "") for c in content if isinstance(c, dict))
        return ""
    if provider == "gemini":
        response = result_payload.get("response") or {}
        candidates = response.get("candidates") or []
        if candidates and isinstance(candidates[0], dict):
            content = candidates[0].get("content") or {}
            parts = content.get("parts") or []
            return "\n".join(
                str(p.get("text") or "") for p in parts if isinstance(p, dict) and p.get("text")
            )
        return ""
    return ""


__all__ = [
    "BATCHABLE_PROVIDERS",
    "RenderedAgentRequest",
    "render_agent_provider_request",
    "prefix_group_key_for",
    "output_text_from_batch_result",
]
