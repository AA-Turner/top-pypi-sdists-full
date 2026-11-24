"""THE FIXED REPLAY SET — the byte referee for P1a (prompt blocks / static seal, PLAN §9 P1a).

Every fixture is built through the REAL assembly: ``SystemInstruction`` render → ``prepare_for_send``
(``STAGE_LOOP``) → the provider wire clone → the provider's translator. The referee is the final
outbound snapshot's canonical bytes (``providers/final_outbound_snapshot.canonical_bytes``): what the
seal check fingerprints, with ``cache_control`` / ``prompt_cache_key`` / ``stream`` excluded.

Matrix: wire shape (Anthropic messages, OpenAI Responses, Chat Completions, Google) × turn phase
(T1, T2 cache hit, T2 cache miss, tool round) × the blocks matrx-ai owns (pinned date, Kind
Directives, org catalog, RAG / safety / memory append sections, opening turn, conversation
instructions, a per-turn slot). Door families are an aidream concern: the injectors that differ by
door (``turn_assembly.INJECTOR_RULES``) are covered by their own aidream tests.

The golden file (``golden/replay_set.json``) was written BEFORE the first extraction. Regenerate it
only for a change that is MEANT to move bytes (never in P1a): ``PROMPT_BLOCKS_REGEN_GOLDEN=1``.
"""

from __future__ import annotations

import hashlib
import importlib
from typing import Any
from unittest.mock import patch

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.providers.final_outbound_snapshot import canonical_bytes
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

SHAPES: dict[str, tuple[str, str, str]] = {
    "anthropic": (
        "matrx_ai.providers.anthropic.translator",
        "AnthropicTranslator",
        "anthropic_chat",
    ),
    "openai_responses": (
        "matrx_ai.providers.openai.translator",
        "OpenAITranslator",
        "openai_responses",
    ),
    "chat_completions": ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    "google": ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
}
PHASES = ("t1", "t2_cache_hit", "t2_cache_miss", "tool_round")
VARIANTS = ("plain", "every_block")

CONV = "0b1c2d3e-4f50-6172-8394-a5b6c7d8e9f0"
AUTHORED = "You are the receiving desk. Answer briefly."
TYPED = "Please send the line."


def _system(variant: str) -> SystemInstruction:
    if variant == "plain":
        return SystemInstruction(
            base_instruction=AUTHORED, include_date=True, date_anchor="2026-11-13"
        )
    si = SystemInstruction(
        base_instruction=AUTHORED,
        include_date=True,
        date_anchor="2026-11-13",
        action_types=["create_note", "update_task"],
        prepend_sections=["<available_skills>\nskill-a: does a\n</available_skills>"],
        append_sections=[
            "You can search the knowledge store `docs`.",
            "The person is under 18: keep it age-appropriate.",
            "<memory>Prefers short answers.</memory>",
        ],
        opening_turn="Start by greeting the desk.",
    )
    si.inject_context_block("<org_catalog>\nAcme (active)\n</org_catalog>")
    return si


def _messages(phase: str) -> list[UnifiedMessage]:
    first = UnifiedMessage(
        role="user", content=[TextContent(text="Draft the reply for this ticket.")]
    )
    first.metadata = {"cache_template": "stable"}
    if phase == "t1":
        return [first]
    reply = UnifiedMessage(role="assistant", content=[TextContent(text="Here is the draft.")])
    if phase == "tool_round":
        call = UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="call_1", name="lookup", arguments={"q": "ticket"})],
        )
        result = UnifiedMessage(
            role="tool",
            content=[
                ToolResultContent(
                    tool_use_id="call_1",
                    call_id="call_1",
                    name="lookup",
                    content=[{"type": "text", "text": "found"}],
                )
            ],
        )
        return [first, call, result]
    return [first, reply]


def _config(variant: str, phase: str) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=_messages(phase)))
    config.system_instruction = _system(variant)
    if phase != "tool_round":
        config.messages.append_or_extend_user_input(TYPED)
    config.messages.attach_turn_context("<live_date>It is now 09:00.</live_date>", slot="live_date")
    if variant == "every_block":
        config.conversation_instructions = "Answer in French."
    return config


def _cache_state(phase: str) -> dict[str, Any] | None:
    if phase == "t2_cache_hit":
        return {"provider": "x", "last_call_at": "2099-01-01T00:00:00+00:00", "warm": True}
    return None


async def build(shape: str, phase: str, variant: str) -> bytes:
    module, cls, wire_format = SHAPES[shape]
    reset_loop_state(CONV)
    config = _config(variant, phase)
    profile = make_profile(model_name="m", wire_format=wire_format)

    async def _profile(*_a: Any, **_k: Any) -> Any:
        return profile

    with patch("matrx_ai.catalog.resolve.resolve_call_profile", _profile):
        prep = await _prepare(config, phase)
    wire = prep.wire_config if prep.wire_config is not None else config
    translator = getattr(importlib.import_module(module), cls)()
    request = translator.build_request(_build_provider_wire_config(wire, profile), profile)
    if shape == "google":
        cfg = request["config"]
        request = {
            "contents": [_jsonable(c) for c in request["contents"]],
            "system": str(cfg.system_instruction),
            "tools": [_jsonable(t) for t in (cfg.tools or [])],
        }
    reset_loop_state(CONV)
    return canonical_bytes(request)


def _jsonable(value: Any) -> Any:
    dump = getattr(value, "model_dump", None)
    return dump(mode="json", exclude_none=True) if callable(dump) else value


async def _prepare(config: UnifiedConfig, phase: str) -> Any:
    return await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONV,
        request_id="r-replay",
        iteration=2 if phase == "tool_round" else 1,
        cache_state=_cache_state(phase),
        policy=TrimPolicy(),
    )


def cases() -> list[tuple[str, str, str]]:
    return [(s, p, v) for s in SHAPES for p in PHASES for v in VARIANTS]


def key(shape: str, phase: str, variant: str) -> str:
    return f"{shape}/{phase}/{variant}"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()
