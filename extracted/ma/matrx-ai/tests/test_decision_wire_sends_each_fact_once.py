"""A verbalized decision turn puts every fact on the wire ONCE, and records what it sent.

THE BREAK THIS CATCHES (2026-09-26, Model Battle, "Feedback triage"). The
stored user message of conversation 61ba88e5 (Gemini 3.8 Flash) carried the
feedback report as its own text part AND again, JSON-escaped, as
``state.subject`` inside the rendered questions — the model paid for the
report twice. The same row recorded ``tools_on_call`` with the agent's tools
although the decision turn sent none.

Driven through the REAL translators of every text-model family the verbalized
path serves (Anthropic, Google, OpenAI, xAI), so the assertions are about the
bytes each provider receives. Remove the ``subject_above`` pop in
``prepare_verbalized_decision`` and the "exactly once" assertions go red;
remove the ``tools_on_call`` reset and the record assertion does.

Use case: the platform's own feedback-triage agent — a homeowner's quotes
board stuck on "Loading…" cards, asked is_defect / owning_surface / urgency.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.decisions.translate import prepare_verbalized_decision
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.providers.xai.translator import XAITranslator
from matrx_ai.testing.profile_factory import make_profile

INSTRUCTION = (
    "You triage incoming product feedback for the AI Matrx platform. Judge the "
    "item on its own evidence. A reporter's own type and priority are claims, "
    "not findings."
)
REPORT = (
    "Feedback item\n\nFiled as: bug, high priority\nPage: https://aimatrx.com/data-v2\n\n"
    'What the reporter described:\nBirchwood Avenue Renovation "quotes" Kanban board '
    'renders every card as a permanent "Loading..." placeholder.\n\n'
    "Comments added since:\nThe table view of the same quotes loads every row fine."
)
# A phrase that appears in the report and nowhere else in the prompt.
REPORT_MARK = "permanent"
INSTRUCTION_MARK = "claims, not findings"

QUESTIONS = [
    {
        "name": "is_defect",
        "type": "noul",
        "instructions": "Is this a defect in existing behaviour?",
        "criteria": {"true": "existing behaviour is wrong", "false": "new behaviour is wanted"},
        "suggested_threshold": 0.7,
    },
    {
        "name": "owning_surface",
        "type": "choice",
        "instructions": "Which surface owns this?",
        "criteria": {"frontend": "the browser UI", "server": "the Python API"},
    },
    {
        "name": "urgency",
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["cosmetic", "minor friction", "a feature is blocked"],
    },
]

TEN_TOOLS = [{"id": None, "name": f"tool_{i}", "kind": "registered"} for i in range(10)]

FEATURES = ["function_calling", "structured_output"]
CAPS = {"input": ["text"], "output": ["text"], "features": FEATURES, "interaction": "turn"}

FAMILIES = [
    ("anthropic", "claude-sonnet-5", "anthropic_chat", lambda c, p: AnthropicTranslator().to_anthropic(c, p)),
    ("google", "gemini-3.8-flash", "google_chat", lambda c, p: GoogleTranslator().to_google(c, p)),
    ("openai", "gpt-5.2", "openai_responses", lambda c, p: OpenAITranslator().to_openai(c, p)),
    ("xai", "grok-4", "xai_chat", lambda c, p: XAITranslator().to_xai(c, p)),
]


def _config(model: str) -> UnifiedConfig:
    message = UnifiedMessage(
        role="user",
        content=[
            TextContent(text=REPORT),
            DecisionQuestionsContent(questions=[dict(q) for q in QUESTIONS]),
        ],
    )
    message.metadata["tools_on_call"] = list(TEN_TOOLS)
    return UnifiedConfig(
        model=model,
        messages=[message],
        system_instruction=SystemInstruction(base_instruction=INSTRUCTION),
        custom_tools=[
            {
                "name": "records",
                "description": "Read rows.",
                "parameters": {"table": {"type": "string", "description": "t", "required": True}},
            }
        ],
    )


def _wire_text(wire: object) -> str:
    """Every string the provider receives, JSON-escapes undone, so a phrase
    counts the same whether it rode a text part or a JSON-encoded state."""
    raw = json.dumps(wire, default=str, ensure_ascii=False)
    return raw.encode().decode("unicode_escape", errors="ignore")


@pytest.mark.parametrize("family,model,wire_format,translate", FAMILIES)
def test_each_fact_reaches_the_provider_exactly_once(family, model, wire_format, translate):
    config = _config(model)
    overlay = prepare_verbalized_decision(config, model_name=model, supports_structured_output=True)
    assert overlay is not None
    profile = make_profile(model_name=model, wire_format=wire_format, capabilities=CAPS)
    text = _wire_text(translate(config, profile))

    assert text.count(REPORT_MARK) == 1, f"{family}: the report reached the wire {text.count(REPORT_MARK)} times"
    assert text.count(INSTRUCTION_MARK) == 1, (
        f"{family}: the instruction reached the wire {text.count(INSTRUCTION_MARK)} times"
    )
    # Every question is still asked.
    for question in QUESTIONS:
        assert question["instructions"] in text, f"{family}: {question['name']} missing"


def test_the_stored_message_holds_the_report_once_and_the_questions_as_prose():
    config = _config("gemini-3.8-flash")
    prepare_verbalized_decision(config, model_name="gemini-3.8-flash", supports_structured_output=True)
    parts = [block.text for block in config.messages[0].content]
    assert parts[0] == REPORT, "the author's text part stays first, untouched"
    assert parts[1].startswith(
        "You are answering a fixed set of decision questions about the message above."
    )
    assert REPORT_MARK not in parts[1]
    assert INSTRUCTION_MARK in parts[1]


def test_a_subject_only_in_resolved_text_is_kept_in_the_state():
    """When the translator would NOT send the subject (a block whose text lives
    only in ``metadata.resolved_text``), the state is its only copy and keeps it."""
    config = UnifiedConfig(
        model="gemini-3.8-flash",
        messages=[
            UnifiedMessage(
                role="user",
                content=[DecisionQuestionsContent(questions=[dict(q) for q in QUESTIONS])],
            )
        ],
    )
    # Placed after construction: config hygiene drops an empty-text block, so
    # this is the shape a late resolver would leave behind.
    config.messages[0].content.insert(0, TextContent(text="", metadata={"resolved_text": REPORT}))
    prepare_verbalized_decision(config, model_name="gemini-3.8-flash", supports_structured_output=True)
    prose = config.messages[0].content[-1].text
    assert "about the state below" in prose
    assert REPORT_MARK in prose


def test_the_call_record_lists_the_tools_this_call_offered_which_is_none():
    config = _config("claude-sonnet-5")
    assert len(config.messages[0].metadata["tools_on_call"]) == 10
    prepare_verbalized_decision(config, model_name="claude-sonnet-5", supports_structured_output=True)
    assert config.messages[0].metadata["tools_on_call"] == []
    assert config.custom_tools == [], "and the wire really carried none"


def test_the_answer_is_read_from_the_text_parts_never_the_thinking():
    """grok-4.7 (2026-09-26): the reply carried its reasoning as a thinking
    block BEFORE the JSON. Reading every block's ``.text`` handed the parser the
    draft reasoning, and every question came back "unanswerable" over a correct
    reply. The JSON also arrives split across text parts."""
    from types import SimpleNamespace

    from matrx_ai.config.unified_content import ThinkingContent
    from matrx_ai.decisions.translate import finalize_verbalized_decision

    config = _config("grok-4.7")
    overlay = prepare_verbalized_decision(config, model_name="grok-4.7", supports_structured_output=True)
    reply_json = (
        '{"answers":{"is_defect":{"answer":true,"probability":0.94,"confidence":0.9},'
        '"owning_surface":{"answer":"frontend","probabilities":{"frontend":0.8,"server":0.2},'
        '"confidence":0.72},"urgency":{"probabilities":{"0":0.1,"1":0.2,"2":0.7},"confidence":0.74}}}'
    )
    reply = SimpleNamespace(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ThinkingContent(
                        text='Draft: is_defect -> {"answer": true, "probability": 0.9} seems right.',
                        provider="xai",
                    ),
                    TextContent(text=reply_json[:57]),
                    TextContent(text=reply_json[57:]),
                ],
            )
        ],
        usage=SimpleNamespace(input_tokens=2181, output_tokens=118),
        metadata={},
    )
    finalized = finalize_verbalized_decision(reply, overlay, model_name="grok-4.7", cost_usd=0.005)
    answers = finalized.messages[-1].content[0].answers
    assert answers.unanswerable == {}
    assert set(answers.answers) == {"is_defect", "owning_surface", "urgency"}
    assert answers.answers["owning_surface"].answer == "frontend"
