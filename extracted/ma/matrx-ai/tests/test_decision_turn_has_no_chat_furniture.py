"""A decision turn sends its message parts and nothing else.

THE BREAK THIS CATCHES: on 2026-09-23 the Sonnet twin of the feedback-triage
agent paid 45,739 input tokens for a decision its native twin answered in 729.
The verbalized path handed the provider everything a chat turn carries — twenty
tool schemas (the agent's one attached ``records`` tool plus nineteen platform
tools), the membership catalog in the system prompt and the per-turn context
block. Read off the persisted ``chat.request_snapshot`` of that run.

This drives the REAL Anthropic translator on the config the verbalized path
leaves behind, so the assertion is about the bytes on the wire, not a flag.
Remove ``overlay.suspended = suspend_chat_furniture(config)`` from
``prepare_verbalized_decision`` and every wire assertion here goes red; remove
the restore in ``UnifiedAIClient.execute`` and the round-trip one does.

Use case (same as test_decision_translator.py): All Green Recycling's portal —
a resident reports a pickup marked complete with no truck; triage asks whether
it is a defect, which surface owns it, and how urgent it is.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.decisions.translate import prepare_verbalized_decision
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

INSTRUCTION = "You triage reports from the All Green Recycling customer portal."
REPORT = (
    "Pickup for 1418 Birch Lane was marked complete at 9:12 but no truck came. "
    "The bins are still at the curb."
)
CATALOG = '<org_catalog>\n  org 5dc930e9 "All Green Recycling"\n</org_catalog>'
SURFACE = "<surface_intro>You are on the live chat route.</surface_intro>"

QUESTIONS = [
    {
        "name": "is_defect",
        "type": "noul",
        "instructions": "Is this a defect in existing behaviour?",
        "criteria": {"true": "existing behaviour is wrong", "false": "new behaviour"},
        "suggested_threshold": 0.7,
    },
    {
        "name": "owning_surface",
        "type": "choice",
        "instructions": "Which surface owns this?",
        "criteria": {"frontend": "the portal", "server": "the route service"},
    },
]

RECORDS_TOOL = {
    "name": "records",
    "description": "Read and write rows in the organization's tables.",
    "parameters": {"table": {"type": "string", "description": "table", "required": True}},
}


def _profile():
    return make_profile(
        model_name="claude-sonnet-5",
        wire_format="anthropic_chat",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": ["function_calling", "structured_output"],
            "interaction": "turn",
        },
    )


def _chat_config(*, with_questions: bool) -> UnifiedConfig:
    content = [TextContent(text=REPORT)]
    if with_questions:
        content.append(DecisionQuestionsContent(questions=[dict(q) for q in QUESTIONS]))
    config = UnifiedConfig(
        model="claude-sonnet-5",
        messages=[UnifiedMessage(role="user", content=content)],
        system_instruction=SystemInstruction(base_instruction=INSTRUCTION),
        custom_tools=[RECORDS_TOOL],
        internal_web_search=True,
    )
    # Exactly how the host injects the membership catalog (context_utils.py).
    config.system_instruction.inject_context_block(CATALOG)
    config.messages.attach_turn_context(SURFACE, slot="surface")
    return config


def test_a_chat_turn_still_carries_its_tools_and_context():
    """The control: the same config WITHOUT questions keeps everything."""
    wire = AnthropicTranslator().to_anthropic(_chat_config(with_questions=False), _profile())
    names = {t.get("name") for t in wire.get("tools", [])}
    assert {"records", "web_search"} <= names
    system = str(wire.get("system"))
    assert "<org_catalog>" in system and "<surface_intro>" in system


def test_a_decision_turn_sends_no_tools_no_catalog_no_turn_context():
    config = _chat_config(with_questions=True)
    overlay = prepare_verbalized_decision(
        config, model_name="claude-sonnet-5", supports_structured_output=True
    )
    assert overlay is not None
    wire = AnthropicTranslator().to_anthropic(config, _profile())

    assert not wire.get("tools"), f"decision turn sent tools: {wire.get('tools')}"
    system = str(wire.get("system") or "")
    assert "<org_catalog>" not in system
    assert "<surface_intro>" not in system
    # The authored instruction and the report still reach the model — through
    # the state, exactly as the native route sends them.
    prose = str(wire["messages"])
    assert INSTRUCTION in prose
    assert "1418 Birch Lane" in prose
    assert "Which surface owns this?" in prose
    # Nothing of the catalog leaked into the state either.
    assert "All Green Recycling\\\"" not in prose and "org_catalog" not in prose


@pytest.mark.asyncio
async def test_the_conversation_gets_its_tools_back_after_the_decision_turn(monkeypatch):
    config = _chat_config(with_questions=True)
    seen: dict[str, object] = {}

    async def _dispatch(_self, request):
        from matrx_ai.providers import unified_client as mod

        cfg = request.config
        overlay = prepare_verbalized_decision(
            cfg, model_name="claude-sonnet-5", supports_structured_output=True
        )
        cfg.metadata[mod._VERBALIZED_DECISION_KEY] = overlay
        seen["tools_during"] = list(cfg.custom_tools)
        seen["system_during"] = cfg.system_instruction
        raise RuntimeError("provider down")  # the restore must run on failure too

    monkeypatch.setattr(UnifiedAIClient, "_execute_dispatch", _dispatch)
    config.metadata = {}
    with pytest.raises(RuntimeError):
        await UnifiedAIClient().execute(
            AIMatrixRequest(conversation_id="triage-decision-scope", config=config)
        )

    assert seen["tools_during"] == [] and seen["system_during"] is None
    assert [t.name for t in config.custom_tools] == ["records"]
    assert config.internal_web_search is True
    assert "<org_catalog>" in str(config.system_instruction)
    assert config.messages.render_turn_context() and SURFACE in config.messages.render_turn_context()
