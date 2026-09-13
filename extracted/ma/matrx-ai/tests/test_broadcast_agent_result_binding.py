"""A broadcast ``agent_result`` is not a bag of variables (2026-09-12 defect).

THE LIVE FAILURE. In workflow run 51524ca9 ("Watson Parenting Adviser") the
Case Reader's ``agent_result`` rode three mapping-less pass-through edges into
the Prescriber step. ``AgentStartInput`` is ``extra="allow"``, so every key of
that result — ``content``, ``messages``, ``usage``, ``final_text``,
``request_id``, ``iterations``, … — folded into the agent's VARIABLES, and
``conversation_id`` bound the step's conversation field. The step then tried to
CONTINUE the Case Reader's conversation with its own variables and the binding
guard refused it:

    409 conversation_binding_mismatch … mismatched_variables:
    [age_band, cause_in_the_handling, content, duration_ms, final_message,
     final_text, finish_reason, governing_rules, iterations, machinery,
     messages, metadata, missing_facts, physician_first, physician_reason,
     request_id, routine_faults, structured_output, tool_calls_made, usage]

Two rules are pinned here:

1. the step starts its OWN conversation (``is_new`` True, a fresh id) —
   the engine withholds the upstream identity (``matrx_graph.types
   .identity_inputs``) and the node mints one, so the continuation branch
   that raises the 409 is never entered;
2. binding honours the DECLARATION — the result's bookkeeping is never a
   variable, and the one part of it that carries answers
   (``structured_output``) is projected onto the step's declared
   ``exposed_variables``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai import _ext
from matrx_ai.graph_nodes import agent_action
from matrx_ai.graph_nodes.agent_action import (
    AgentStartConfig,
    AgentStartInput,
    agent_start,
)

AGENT_ID = "0be8ad3f-7385-4e23-808e-559a8b0e3a4d"  # the live Watson Prescriber
UPSTREAM_CONVERSATION_ID = "95cce75d-e755-4a2e-a27a-ab806730f3d4"

#: The live Prescriber step's exposed variables, verbatim from the definition.
EXPOSED = [
    "situation",
    "child_age",
    "age_band",
    "cause_in_the_handling",
    "machinery",
    "governing_rules",
    "routine_faults",
    "physician_first",
    "physician_reason",
    "missing_facts",
]

#: What the pass-through delivered: the whole upstream ``agent_result``, MINUS
#: ``conversation_id`` — the engine withholds that before the node ever sees it
#: (guarded in matrx-graph's ``test_identity_input_broadcast``).
BROADCAST_AGENT_RESULT = {
    "request_id": "0ee8d27d-1111-4111-8111-111111111111",
    "iterations": 1,
    "finish_reason": "stop",
    "final_text": "Here is what the case says.",
    "final_message": {"role": "assistant", "content": "Here is what the case says."},
    "messages": [{"role": "user", "content": "…"}, {"role": "assistant", "content": "…"}],
    "usage": {"input_tokens": 900, "output_tokens": 300, "cost_usd": 0.02},
    "duration_ms": 8123,
    "tool_calls_made": 0,
    "metadata": {"status": "completed"},
    "content": [{"__kind": "markdown", "text": "…"}],
    "structured_output": {
        "age_band": "toddler",
        "cause_in_the_handling": "the bedtime hand-off",
        "machinery": "escalation loop",
        "governing_rules": ["one warning, then the consequence"],
        "routine_faults": ["no wind-down"],
        "physician_first": False,
        "physician_reason": "",
        "missing_facts": ["how long it has been going on"],
        # A structured field the step did NOT expose — never invented as a
        # variable just because it rode along.
        "internal_confidence": 0.8,
    },
}

#: Every bookkeeping key of an agent_result that used to become a variable.
BOOKKEEPING = {
    "request_id",
    "iterations",
    "finish_reason",
    "final_text",
    "final_message",
    "messages",
    "usage",
    "duration_ms",
    "tool_calls_made",
    "metadata",
    "content",
    "structured_output",
}


def _capture(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    captured: dict[str, object] = {}

    class FakeAgentStartRequest:
        @classmethod
        def model_validate(cls, payload):
            captured["payload"] = payload
            return SimpleNamespace()

    async def fake_agent_runner(agent_id, request, app_ctx):
        captured["agent_id"] = agent_id
        return "completed"

    monkeypatch.setitem(_ext._registry, "agent_runner", fake_agent_runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", FakeAgentStartRequest)
    monkeypatch.setattr(agent_action, "normalize_completed_result", lambda value, **_kwargs: value)
    return captured


def _step_ctx():
    return SimpleNamespace(
        app=SimpleNamespace(),
        node_id="n-5e3a67afcd",
        organization_id="8fd3a0e1-0000-4000-8000-000000000001",
    )


async def _run_prescriber(monkeypatch: pytest.MonkeyPatch) -> dict:
    captured = _capture(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": AGENT_ID,
            # The intake edge's explicit mappings — the two the author wired.
            "situation": "He melts down at bedtime.",
            "child_age": "3",
            # …and the pass-through's whole-payload broadcast.
            **BROADCAST_AGENT_RESULT,
        }
    )
    await agent_start(  # type: ignore[arg-type]
        _step_ctx(), inputs, AgentStartConfig(exposed_variables=EXPOSED)
    )
    return captured["payload"]  # type: ignore[return-value]


@pytest.mark.asyncio
async def test_the_step_starts_its_own_conversation(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = await _run_prescriber(monkeypatch)

    assert payload["is_new"] is True
    assert payload["conversation_id"] != UPSTREAM_CONVERSATION_ID
    assert payload["conversation_id"]  # a real, freshly minted id


@pytest.mark.asyncio
async def test_bookkeeping_is_never_a_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = await _run_prescriber(monkeypatch)
    variables = payload["variables"]

    leaked = sorted(BOOKKEEPING & set(variables))
    assert leaked == [], f"agent_result bookkeeping bound as variables: {leaked}"
    # …and it must not have been promoted to a stray top-level request field
    # either (dropping a variable is not the same as forwarding it).
    assert sorted(BOOKKEEPING & set(payload)) == []


@pytest.mark.asyncio
async def test_structured_output_is_projected_onto_declared_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = await _run_prescriber(monkeypatch)
    variables = payload["variables"]

    # The author's explicitly mapped variables survive untouched…
    assert variables["situation"] == "He melts down at bedtime."
    assert variables["child_age"] == "3"
    # …and the answers inside structured_output arrive under the names this
    # step DECLARES, not as a blob.
    assert variables["age_band"] == "toddler"
    assert variables["cause_in_the_handling"] == "the bedtime hand-off"
    assert variables["governing_rules"] == ["one warning, then the consequence"]
    assert variables["physician_first"] is False
    # A structured field the step never exposed is not invented as a variable.
    assert "internal_confidence" not in variables


@pytest.mark.asyncio
async def test_the_409_variable_set_can_no_longer_be_produced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The exact ``mismatched_variables`` list from the live 409, extinct.

    The guard that raised it (``_enforce_continuation_variable_binding``) is
    RIGHT and stays — it simply has nothing to fire on, because this step is
    not a continuation and its variables are its own declaration.
    """
    payload = await _run_prescriber(monkeypatch)
    live_409_variables = {
        "age_band",
        "cause_in_the_handling",
        "content",
        "duration_ms",
        "final_message",
        "final_text",
        "finish_reason",
        "governing_rules",
        "iterations",
        "machinery",
        "messages",
        "metadata",
        "missing_facts",
        "physician_first",
        "physician_reason",
        "request_id",
        "routine_faults",
        "structured_output",
        "tool_calls_made",
        "usage",
    }
    # Not a continuation — the branch that raises the 409 is never entered.
    assert payload["is_new"] is True
    # And the bookkeeping half of that list is gone from the variables entirely.
    assert not (live_409_variables & BOOKKEEPING) & set(payload["variables"])


@pytest.mark.asyncio
async def test_a_single_mapped_field_named_like_bookkeeping_still_binds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An author may legitimately name a variable ``content`` and MAP it.

    Only a whole broadcast agent_result (quorum of bookkeeping keys) is
    filtered — one explicitly mapped key never reaches quorum and must keep
    working, or the fix would break honest authoring.
    """
    captured = _capture(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {"agent_id": AGENT_ID, "content": "the article body", "topic": "pizza"}
    )
    await agent_start(_step_ctx(), inputs, AgentStartConfig())  # type: ignore[arg-type]

    assert captured["payload"]["variables"] == {  # type: ignore[index]
        "content": "the article body",
        "topic": "pizza",
    }
