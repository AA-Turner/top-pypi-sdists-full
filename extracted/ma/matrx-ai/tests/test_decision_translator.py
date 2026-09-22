"""Forcing-function guards for the decision translator.

THE BREAKS THESE CATCH (each one names a production change that turns it red):

1. ``UnifiedAIClient`` stops translating a ``decision_questions`` part — it
   refuses again, drops the part, or hands the provider the raw message instead
   of a state object built from the sibling parts.
2. The provider's answers stop becoming a ``decision_answers`` part: a
   probability is lost, a noul verdict is read off the wrong side of its
   threshold, a choice winner is taken from somewhere other than the
   distribution, or a score legend is not echoed.
3. An image beside the questions is silently dropped instead of refused by
   name.
4. A text model's turn stops becoming the same answer shape, or its score
   answer stops being the probability-weighted level.
5. The kind contract stops refusing a malformed batch (a name that is not
   snake_case, a one-option choice, an eleven-level score, a duplicate name).

THE USE CASE all fixtures come from: All Green Recycling's customer portal.
A resident reports through the portal that their recycling pickup was marked
complete but no truck came; the triage decision is the declared
``feedback.item_triage_decision`` mandate — is it a defect, which surface owns
it, how urgent.

TWO forcing inputs everywhere a constant could survive: the same code must
produce two DIFFERENT answers, so ``return expected`` cannot pass.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.decisions.kinds import DecisionQuestions
from matrx_ai.decisions.translate import (
    DecisionCompatibilityError,
    build_decision_state,
    decision_answers_from_verbalized,
    finalize_verbalized_decision,
    prepare_verbalized_decision,
)
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.typesafe import SystemOneResult
from matrx_ai.providers.unified_client import UnifiedAIClient

# --- The real triage batch, verbatim from the typed-messages contract -------

TRIAGE_QUESTIONS = [
    {
        "name": "is_defect",
        "type": "noul",
        "instructions": (
            "Is this a defect in existing behaviour rather than a request for new "
            "behaviour?"
        ),
        "criteria": {
            "true": "existing behaviour is wrong",
            "false": "new behaviour is wanted",
        },
        "suggested_threshold": 0.7,
    },
    {
        "name": "owning_surface",
        "type": "choice",
        "instructions": "Which surface owns this?",
        "criteria": {
            "frontend": "the customer portal a resident clicks",
            "server": "the route service or a worker",
            "data": "a row that is wrong",
            "infrastructure": "hosting, DNS, certificates",
            "unclear": "the report does not say enough to place it",
        },
    },
    {
        "name": "urgency",
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": [
            "cosmetic",
            "minor friction",
            "a feature is blocked",
            "data or money at risk",
            "down for someone",
        ],
    },
]

REPORT_TEXT = (
    "Resident at 1420 Sycamore Ave says the portal marked Tuesday's recycling "
    "pickup complete at 9:14am, but the bin was never emptied and the truck "
    "never came down the street."
)
TRIAGE_INSTRUCTION = "You triage reports from the All Green Recycling customer portal."


def _triage_message() -> UnifiedMessage:
    return UnifiedMessage(
        role="user",
        content=[
            TextContent(text=REPORT_TEXT),
            DecisionQuestionsContent(questions=[dict(q) for q in TRIAGE_QUESTIONS]),
        ],
    )


def _decision_profile():
    return SimpleNamespace(
        wire_format="typesafe_systemone",
        client_attr="decision",
        capabilities=SimpleNamespace(interaction="decision"),
        byok_secret_key=None,
        provider_model_id="jev-1.13.0",
        base_url="https://api.typesafe.ai",
        model_name="jev-1.13",
        vendor="typesafe",
        endpoint_id="endpoint-typesafe",
        api_id="api-systemone",
        offering_id="offering-jev",
        resolution_route="pinned",
    )


class _Admission:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False


@pytest.fixture
def decision_wire(monkeypatch):
    """Stub exactly the three things outside the SUT: route, price, transport."""
    from matrx_ai.catalog import resolve as resolve_mod
    from matrx_ai.decisions import runner

    async def _profile(*_args, **_kwargs):
        return _decision_profile()

    async def _pricing():
        return {"offering-jev": object()}

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _profile)
    monkeypatch.setattr(runner, "ensure_pricing_lookup", _pricing)
    monkeypatch.setattr(runner.TokenUsage, "calculate_catalog_cost", lambda *_a: 0.00008)
    monkeypatch.setattr(runner, "admit_provider_call", lambda _p: _Admission())

    captured: dict = {}

    def install(answers: dict) -> None:
        async def _caller(request, **kwargs):
            captured["request"] = request
            captured["kwargs"] = kwargs
            return SystemOneResult.model_validate(
                {
                    "model": "jev-1.13.0",
                    "answers": answers,
                    "usage": {"input_tokens": 1830, "output_tokens": 0},
                    "request_id": "so-1",
                }
            )

        monkeypatch.setattr(runner, "call_system_one", _caller)

    return SimpleNamespace(install=install, captured=captured)


# Two DIFFERENT provider payloads with two DIFFERENT correct readings. The noul
# probability straddles the batch's 0.7 threshold in opposite directions, the
# choice winner moves, and the score mass moves — a constant answer cannot
# satisfy both rows.
_NATIVE_CASES = [
    pytest.param(
        {
            "is_defect": {"type": "noul", "noul": 0.91},
            "owning_surface": {
                "type": "choice",
                "choice": "data",
                "probabilities": {
                    "frontend": 0.1,
                    "server": 0.2,
                    "data": 0.62,
                    "infrastructure": 0.03,
                    "unclear": 0.05,
                },
                "confidence": 0.62,
            },
            "urgency": {
                "type": "score",
                "score": 3.4,
                "probabilities": {"1": 0.02, "2": 0.1, "3": 0.4, "4": 0.4, "5": 0.08},
                "confidence": 0.4,
                "legend": {
                    "1": "cosmetic",
                    "2": "minor friction",
                    "3": "a feature is blocked",
                    "4": "data or money at risk",
                    "5": "down for someone",
                },
            },
        },
        True,
        0.91,
        "data",
        3.4,
        id="a_real_missed_pickup_is_a_defect",
    ),
    pytest.param(
        {
            "is_defect": {"type": "noul", "noul": 0.44},
            "owning_surface": {
                "type": "choice",
                "choice": "frontend",
                "probabilities": {
                    "frontend": 0.71,
                    "server": 0.12,
                    "data": 0.09,
                    "infrastructure": 0.02,
                    "unclear": 0.06,
                },
                "confidence": 0.71,
            },
            "urgency": {
                "type": "score",
                "score": 1.8,
                "probabilities": {"1": 0.5, "2": 0.3, "3": 0.15, "4": 0.04, "5": 0.01},
                "confidence": 0.5,
                "legend": {
                    "1": "cosmetic",
                    "2": "minor friction",
                    "3": "a feature is blocked",
                    "4": "data or money at risk",
                    "5": "down for someone",
                },
            },
        },
        False,
        0.44,
        "frontend",
        1.8,
        id="a_wished_for_reschedule_button_is_not_a_defect",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider_answers", "defect", "probability", "surface", "score"), _NATIVE_CASES
)
async def test_native_decision_turn_carries_one_decision_answers_part(
    decision_wire, provider_answers, defect, probability, surface, score
):
    decision_wire.install(provider_answers)
    config = UnifiedConfig(
        model="jev-1.13",
        messages=[_triage_message()],
        system_instruction=TRIAGE_INSTRUCTION,
    )
    response = await UnifiedAIClient().execute(
        AIMatrixRequest(conversation_id="triage-1", config=config)
    )

    # The state reached the provider as a JSON object built from the SIBLING
    # parts — not from the questions part, and not as the raw message.
    state = decision_wire.captured["request"].state
    assert isinstance(state, dict)
    assert state["subject"] == REPORT_TEXT
    assert state["instructions"] == TRIAGE_INSTRUCTION
    assert "questions" not in state

    # The questions reached it as the typed System One map, by name.
    sent = decision_wire.captured["request"].questions
    assert set(sent) == {"is_defect", "owning_surface", "urgency"}
    assert sent["owning_surface"].criteria["data"] == "a row that is wrong"
    assert sent["urgency"].criteria[0] == "cosmetic"

    # ONE part comes back, and it is the answers kind.
    assert len(response.messages) == 1
    assert len(response.messages[0].content) == 1
    answers = response.messages[0].content[0].answers
    assert answers.method == "native"
    assert answers.model == "jev-1.13.0"
    assert answers.cost_usd == 0.00008
    assert answers.usage.input_tokens == 1830

    assert answers.answers["is_defect"].answer is defect
    assert answers.answers["is_defect"].probability == probability
    assert answers.answers["owning_surface"].answer == surface
    assert answers.answers["owning_surface"].probabilities[surface] == pytest.approx(
        provider_answers["owning_surface"]["probabilities"][surface]
    )
    assert answers.answers["urgency"].answer == score
    # The legend is echoed onto the answer, so a renderer never has to hold the
    # question to draw the answer.
    assert answers.answers["urgency"].legend["4"] == "data or money at risk"


@pytest.mark.asyncio
async def test_unanswered_question_is_named_unanswerable_not_guessed(decision_wire):
    decision_wire.install({"is_defect": {"type": "noul", "noul": 0.91}})
    config = UnifiedConfig(model="jev-1.13", messages=[_triage_message()])
    response = await UnifiedAIClient().execute(
        AIMatrixRequest(conversation_id="triage-2", config=config)
    )
    answers = response.messages[0].content[0].answers
    assert set(answers.answers) == {"is_defect"}
    assert set(answers.unanswerable) == {"owning_surface", "urgency"}
    assert "no answer" in answers.unanswerable["urgency"]


@pytest.mark.asyncio
async def test_an_image_beside_the_questions_is_refused_by_name(decision_wire):
    decision_wire.install({"is_defect": {"type": "noul", "noul": 0.91}})
    message = _triage_message()
    message.content.insert(1, ImageContent(url="https://example.com/bin.jpg"))
    config = UnifiedConfig(model="jev-1.13", messages=[message])

    with pytest.raises(DecisionCompatibilityError) as caught:
        await UnifiedAIClient().execute(
            AIMatrixRequest(conversation_id="triage-3", config=config)
        )
    sentence = str(caught.value)
    assert "an image" in sentence
    assert "TEXT ONLY" in sentence
    assert "silently dropped" in sentence
    # Refused BEFORE the wire: nothing was paid for.
    assert "request" not in decision_wire.captured


# --- The state -------------------------------------------------------------


def test_state_is_the_other_parts_of_the_message_in_order():
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="I reported this last week too.")]),
        _triage_message(),
    ]
    state = build_decision_state(messages, 1, system_instruction=TRIAGE_INSTRUCTION)
    assert state["instructions"] == TRIAGE_INSTRUCTION
    assert state["earlier_conversation"].endswith("I reported this last week too.")
    assert state["subject"] == REPORT_TEXT


def test_questions_with_no_state_at_all_are_refused():
    messages = [
        UnifiedMessage(
            role="user",
            content=[DecisionQuestionsContent(questions=[dict(q) for q in TRIAGE_QUESTIONS])],
        )
    ]
    with pytest.raises(DecisionCompatibilityError):
        build_decision_state(messages, 0)


# --- The verbalized (text-model) path --------------------------------------


def test_text_model_gets_prose_and_a_schema_bound_to_the_same_questions():
    config = UnifiedConfig(
        model="gpt-5.2",
        messages=[_triage_message()],
        system_instruction=TRIAGE_INSTRUCTION,
    )
    overlay = prepare_verbalized_decision(
        config, model_name="gpt-5.2", supports_structured_output=True
    )
    assert overlay is not None

    # The questions part is GONE from the wire and its content is prose.
    types = [getattr(block, "type", None) for block in config.messages[0].content]
    assert "decision_questions" not in types
    prose = config.messages[0].content[-1].text
    assert "Which surface owns this?" in prose
    assert "- data: a row that is wrong" in prose
    assert "- 3: data or money at risk" in prose
    assert REPORT_TEXT in prose

    # A PLAIN DICT. Every translator reads this field with isinstance(...,
    # dict) — Anthropic's `_build_anthropic_output_format` returns None on its
    # first line otherwise, so the schema is silently NOT enforced and the
    # model answers in prose (seen live on claude-sonnet-5, 2026-09-20).
    assert isinstance(config.response_format, dict), (
        "response_format must be the normalized dict, not the Pydantic model — "
        "UnifiedConfig is a dataclass and does not validate on assignment."
    )
    assert config.response_format["type"] == "json_schema"
    schema = config.response_format["json_schema"]["schema"]
    answers_schema = schema["properties"]["answers"]
    assert set(answers_schema["required"]) == {"is_defect", "owning_surface", "urgency"}
    assert answers_schema["properties"]["owning_surface"]["properties"]["answer"]["enum"] == [
        "frontend",
        "server",
        "data",
        "infrastructure",
        "unclear",
    ]
    # Zero-indexed, matching the native holder's own legend so a verbalized
    # answer and a native answer to the same question are the same number.
    assert answers_schema["properties"]["urgency"]["properties"]["probabilities"]["required"] == [
        "0",
        "1",
        "2",
        "3",
        "4",
    ]


def test_a_model_without_structured_output_is_refused_not_asked_in_prose():
    config = UnifiedConfig(model="tiny-1", messages=[_triage_message()])
    with pytest.raises(DecisionCompatibilityError) as caught:
        prepare_verbalized_decision(
            config, model_name="tiny-1", supports_structured_output=False
        )
    assert "structured output" in str(caught.value)


# Two distributions whose probability-weighted level differs, so the weighting
# cannot be a constant and cannot be read off a field the model supplied.
@pytest.mark.parametrize(
    ("distribution", "expected_level"),
    [
        ({"0": 0.0, "1": 0.0, "2": 0.6, "3": 0.4, "4": 0.0}, 2.4),
        ({"0": 0.5, "1": 0.3, "2": 0.2, "3": 0.0, "4": 0.0}, 0.7),
    ],
)
def test_verbalized_score_answer_is_the_probability_weighted_level(
    distribution, expected_level
):
    batch = DecisionQuestions(questions=[dict(q) for q in TRIAGE_QUESTIONS])
    answers = decision_answers_from_verbalized(
        {
            "answers": {
                "is_defect": {"answer": True, "probability": 0.88, "confidence": 0.88},
                "owning_surface": {
                    "answer": "server",
                    "probabilities": {
                        "frontend": 0.1,
                        "server": 0.7,
                        "data": 0.1,
                        "infrastructure": 0.05,
                        "unclear": 0.05,
                    },
                    "confidence": 0.7,
                },
                # No "answer" field for the score: the level is DERIVED from the
                # distribution the model was actually asked for.
                "urgency": {"probabilities": distribution, "confidence": 0.6},
            }
        },
        batch,
        model="gpt-5.2",
        input_tokens=900,
        output_tokens=120,
        cost_usd=0.0031,
    )
    assert answers.method == "verbalized"
    assert answers.answers["urgency"].answer == pytest.approx(expected_level)
    assert answers.answers["urgency"].legend["4"] == "down for someone"
    assert answers.answers["is_defect"].answer is True
    assert answers.answers["owning_surface"].answer == "server"


def test_finalize_turns_the_models_json_into_one_answers_part():
    config = UnifiedConfig(model="gpt-5.2", messages=[_triage_message()])
    overlay = prepare_verbalized_decision(
        config, model_name="gpt-5.2", supports_structured_output=True
    )
    reply = SimpleNamespace(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(
                        text=(
                            '{"answers": {'
                            '"is_defect": {"answer": true, "probability": 0.93, '
                            '"confidence": 0.93},'
                            '"owning_surface": {"answer": "data", "probabilities": '
                            '{"frontend": 0.08, "server": 0.14, "data": 0.7, '
                            '"infrastructure": 0.03, "unclear": 0.05}, "confidence": 0.7},'
                            '"urgency": {"probabilities": {"0": 0.0, "1": 0.1, "2": 0.2, '
                            '"3": 0.6, "4": 0.1}, "confidence": 0.6}}}'
                        )
                    )
                ],
            )
        ],
        usage=SimpleNamespace(input_tokens=1204, output_tokens=180),
        metadata={},
    )
    finalized = finalize_verbalized_decision(
        reply, overlay, model_name="gpt-5.2", cost_usd=0.0042
    )
    content = finalized.messages[-1].content
    assert len(content) == 1
    answers = content[0].answers
    assert answers.method == "verbalized"
    assert answers.answers["owning_surface"].answer == "data"
    assert answers.answers["urgency"].answer == pytest.approx(2.7)
    assert answers.cost_usd == 0.0042
    assert answers.usage.input_tokens == 1204
    assert finalized.metadata["method"] == "verbalized"


def test_unparseable_reply_raises_rather_than_reporting_a_refusal():
    config = UnifiedConfig(model="gpt-5.2", messages=[_triage_message()])
    overlay = prepare_verbalized_decision(
        config, model_name="gpt-5.2", supports_structured_output=True
    )
    reply = SimpleNamespace(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[TextContent(text="I think it's probably a routing bug.")],
            )
        ],
        usage=SimpleNamespace(input_tokens=10, output_tokens=10),
        metadata={},
    )
    with pytest.raises(DecisionCompatibilityError) as caught:
        finalize_verbalized_decision(reply, overlay, model_name="gpt-5.2", cost_usd=0.0)
    assert "not the structured answer" in str(caught.value)


# --- The kind contract ------------------------------------------------------


@pytest.mark.parametrize(
    ("batch", "reason"),
    [
        ([{"name": "Is Defect", "type": "noul", "instructions": "x"}], "snake_case"),
        (
            [{"name": "surface", "type": "choice", "instructions": "x", "criteria": {"a": "1"}}],
            "2–255",
        ),
        (
            [
                {
                    "name": "urgency",
                    "type": "score",
                    "instructions": "x",
                    "criteria": [str(i) for i in range(11)],
                }
            ],
            "2–10",
        ),
        (
            [
                {"name": "dup", "type": "noul", "instructions": "x"},
                {"name": "dup", "type": "noul", "instructions": "y"},
            ],
            "appears twice",
        ),
    ],
)
def test_the_kind_refuses_a_batch_that_breaks_the_contract(batch, reason):
    with pytest.raises(ValidationError) as caught:
        DecisionQuestions(questions=batch)
    assert reason in str(caught.value)


def test_a_valid_batch_round_trips_through_the_kind_with_its_marker():
    dumped = DecisionQuestions(questions=[dict(q) for q in TRIAGE_QUESTIONS]).model_dump(
        mode="json"
    )
    assert dumped["__kind"] == "decision_questions"
    assert [q["name"] for q in dumped["questions"]] == [
        "is_defect",
        "owning_surface",
        "urgency",
    ]


# --- 6. The answered turn must survive everything that asks what it produced --
#
# THE BREAK THIS CATCHES: a content class on the decision modality stops
# answering `get_output()`. Until 2026-09-20 neither did, and every consumer of
# "what did this run produce" raised AttributeError on a decision turn AFTER
# the provider had been paid and the answer persisted — `_emit_completion`
# (aidream services/ai_execution/ai_task.py) immediately before `send_end()`,
# `Agent._clean_up_response`, the parallel executor, and conversation
# rehydration. The run reported a failure while holding a correct answer.


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider_answers", "defect", "probability", "surface", "score"), _NATIVE_CASES
)
async def test_the_answered_turn_reports_its_answers_as_the_runs_output(
    decision_wire, provider_answers, defect, probability, surface, score
):
    decision_wire.install(provider_answers)
    config = UnifiedConfig(
        model="jev-1.13",
        messages=[_triage_message()],
        system_instruction=TRIAGE_INSTRUCTION,
    )
    response = await UnifiedAIClient().execute(
        AIMatrixRequest(conversation_id="triage-output", config=config)
    )

    # This is the exact call `_emit_completion` makes before `send_end()`.
    output = response.messages[0].get_output()
    assert output, "a decision turn reported no output at all"

    import json

    parsed = json.loads(output)
    assert parsed["__kind"] == "decision_answers"
    assert parsed["method"] == "native"
    assert set(parsed["answers"]) == {"is_defect", "owning_surface", "urgency"}
    # The two forcing cases disagree, so a hardcoded return cannot pass.
    assert parsed["answers"]["is_defect"]["answer"] is defect
    assert parsed["answers"]["owning_surface"]["answer"] == surface
    assert parsed["answers"]["urgency"]["answer"] == score


def test_the_questions_a_user_asked_are_never_the_runs_output():
    # A questions part rides a USER turn. If it answered `get_output()` with its
    # prose, the author's own questions would land in raw_response and in the
    # completion event as if the model had said them.
    asked = DecisionQuestionsContent(questions=[dict(q) for q in TRIAGE_QUESTIONS])
    assert asked.get_output() == ""
    assert "is_defect" in asked.to_prose()


# --- The live stream: a decision reaches the surface as it lands ------------
#
# THE BREAK THIS CATCHES: the decision routes stop emitting the
# `decision_answers` data event, or emit something other than the part they
# return. Both are invisible to every assertion above — the run succeeds, the
# part is correct, the response is correct — and both leave an agent-battle
# column reading "this run finished without writing an answer" over a paid
# decision (feedback efc7c841, 2026-09-21). The event IS the fix, so the event
# is what is asserted.


@pytest.fixture
def stream_recorder(monkeypatch):
    """Capture everything the decision path sends on the stream."""
    from matrx_ai.context import app_context as app_context_mod

    sent: list = []

    class _Emitter:
        async def send_data(self, payload):
            sent.append(payload)

    monkeypatch.setattr(
        app_context_mod,
        "try_get_app_context",
        lambda *_a, **_k: SimpleNamespace(emitter=_Emitter()),
    )
    return sent


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider_answers", "defect", "surface", "score"),
    [
        (
            {
                "is_defect": {"type": "noul", "noul": 0.91},
                "urgency": {
                    "type": "score",
                    "score": 3.4,
                    "probabilities": {"1": 0.0, "2": 0.1, "3": 0.4, "4": 0.4, "5": 0.1},
                    "confidence": 0.4,
                    "legend": {
                        "1": "cosmetic",
                        "2": "minor friction",
                        "3": "a feature is blocked",
                        "4": "data or money at risk",
                        "5": "down for someone",
                    },
                },
                "owning_surface": {
                    "type": "choice",
                    "choice": "data",
                    "probabilities": {
                        "frontend": 0.1,
                        "server": 0.2,
                        "data": 0.62,
                        "infrastructure": 0.03,
                        "unclear": 0.05,
                    },
                    "confidence": 0.62,
                },
            },
            True,
            "data",
            3.4,
        ),
        (
            {
                "is_defect": {"type": "noul", "noul": 0.21},
                "urgency": {
                    "type": "score",
                    "score": 1.2,
                    "probabilities": {"1": 0.6, "2": 0.3, "3": 0.05, "4": 0.03, "5": 0.02},
                    "confidence": 0.6,
                    "legend": {
                        "1": "cosmetic",
                        "2": "minor friction",
                        "3": "a feature is blocked",
                        "4": "data or money at risk",
                        "5": "down for someone",
                    },
                },
                "owning_surface": {
                    "type": "choice",
                    "choice": "frontend",
                    "probabilities": {
                        "frontend": 0.8,
                        "server": 0.1,
                        "data": 0.05,
                        "infrastructure": 0.03,
                        "unclear": 0.02,
                    },
                    "confidence": 0.8,
                },
            },
            False,
            "frontend",
            1.2,
        ),
    ],
)
async def test_native_decision_streams_the_same_part_it_returns(
    decision_wire, stream_recorder, provider_answers, defect, surface, score
):
    decision_wire.install(provider_answers)
    config = UnifiedConfig(model="jev-1.13", messages=[_triage_message()])
    response = await UnifiedAIClient().execute(
        AIMatrixRequest(conversation_id="triage-live", config=config)
    )

    events = [event for event in stream_recorder if getattr(event, "type", "") == "decision_answers"]
    assert len(events) == 1, (
        "A decision turn emits exactly ONE decision_answers event. Zero means the "
        "live surface shows nothing; more than one means a column would render "
        "the same verdict twice."
    )
    event = events[0]

    # The event and the returned part are the SAME decision, field for field.
    part = response.messages[0].content[0].answers
    assert event.model == part.model
    assert event.method == part.method == "native"
    assert event.cost_usd == part.cost_usd
    assert event.usage.input_tokens == part.usage.input_tokens
    assert set(event.answers) == set(part.answers)

    # The values are the RUN's, not a constant: both rows differ in all three.
    assert event.answers["is_defect"].answer is defect
    assert event.answers["owning_surface"].answer == surface
    assert event.answers["urgency"].answer == pytest.approx(score)

    # The kind marker is DATA and rides the event — the frontend dispatches on
    # it to commit the part (`__kind` law).
    assert event.model_dump(by_alias=True)["__kind"] == "decision_answers"


@pytest.mark.asyncio
@pytest.mark.parametrize("resolved_name", ["claude-sonnet-5", "gpt-5.2"])
async def test_verbalized_answer_records_the_resolved_model_name_not_the_uuid(
    monkeypatch, stream_recorder, resolved_name
):
    """THE BREAK: the answer's `model` goes back to reading ``config.model``.

    An agent names its model by the ``ai.model`` UUID, so that read wrote
    "0f9c…" into the answer while the native route wrote "jev-1.13.0" — the
    same fact spelled two ways, and unreadable in a battle's model column.
    """
    from matrx_ai.providers import unified_client as unified_client_mod

    agent_model_uuid = "6f0a3b52-2b77-4e64-9c3a-1f2ab0f5d901"
    config = UnifiedConfig(model=agent_model_uuid, messages=[_triage_message()])
    overlay = prepare_verbalized_decision(
        config, model_name=resolved_name, supports_structured_output=True
    )
    assert overlay is not None
    config.metadata = {unified_client_mod._VERBALIZED_DECISION_KEY: overlay}

    reply = SimpleNamespace(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    TextContent(
                        text=(
                            '{"answers": {'
                            '"is_defect": {"answer": true, "probability": 0.93, '
                            '"confidence": 0.93},'
                            '"owning_surface": {"answer": "data", "probabilities": '
                            '{"frontend": 0.08, "server": 0.14, "data": 0.7, '
                            '"infrastructure": 0.03, "unclear": 0.05}, "confidence": 0.7},'
                            '"urgency": {"probabilities": {"0": 0.0, "1": 0.1, "2": 0.2, '
                            '"3": 0.6, "4": 0.1}, "confidence": 0.6}}}'
                        )
                    )
                ],
            )
        ],
        usage=SimpleNamespace(input_tokens=1204, output_tokens=180),
        metadata={},
    )

    async def _dispatch(_self, _request):
        return reply

    monkeypatch.setattr(UnifiedAIClient, "_execute_dispatch", _dispatch)

    response = await UnifiedAIClient().execute(
        AIMatrixRequest(conversation_id="triage-verbalized", config=config)
    )
    answers = response.messages[-1].content[0].answers
    assert answers.model == resolved_name
    assert agent_model_uuid not in answers.model

    # And the verbalized route streams the identical event the native one does.
    events = [
        event for event in stream_recorder if getattr(event, "type", "") == "decision_answers"
    ]
    assert len(events) == 1
    assert events[0].model == resolved_name
    assert events[0].method == "verbalized"
