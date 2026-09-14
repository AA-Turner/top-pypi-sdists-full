"""AN ASSIGNMENT ITEM'S ALL-ZERO ANSWER IS A FAILED ITEM, NEVER A COMPLETED ONE.

W59 closed the all-zero hole at ``normalize_completed_result`` — the one seam
every migrated ``ai.*`` graph node's answer is accepted by. Censusing its
sibling call sites on 2026-09-12 found ``ai.agent.assignment`` still calling
the BARE ``normalize_completed``, which only raises on a terminal provider
failure. So the node whose own docstring says it "converts each map into the
same strict host request used by ``ai.agent.start``" inherited none of that
seam's refusals: a turn cut off at the output ceiling, and the answer that
satisfies its schema while carrying nothing, were both written down as
COMPLETED items. A 200-row batch could deliver 200 hollow objects with nothing
anywhere saying so — and a batch is precisely where nobody reads each row.

WHY THIS IS A FORCING TEST, not a green rubber stamp:

* The empty payload is the REAL one, off live workflow run ``7e155d1a…``
  ("Newsroom Desk", 2026-09-12 18:16-18:28Z). Its ``n_audit`` step — the
  claim-by-claim sourcing audit, the accountability step — made three model
  calls, spent 571,468 input / 74,466 output tokens and $2.24, and returned
  ``{"cuts": [], "flags": [], "verdict": "", …}``. ``output_kind_ok`` was
  true, the run status was ``completed``, and the product presented that blank
  as the finished sourcing note. The schema is the real
  ``agent.definition.output_schema`` of "Sourcing Auditor"
  (``751ec459-1ca5-445b-822f-b677695a686f``), ``required`` list verbatim.
* It runs the REAL node body — ``run_agent_assignment_batch`` against a REAL
  ``AssignmentCoordinator`` over a REAL ``InMemoryAssignmentStore``, with the
  real planner, the real lease/attempt ladder and the real terminal
  bookkeeping. Only the provider boundary is a double (the host's
  ``agent_runner`` ext, exactly as ``test_node_handlers_execute.py`` does it).
  Nothing about the refusal is simulated.
* It fails on the code as it stood before this commit: put
  ``normalize_completed`` back in ``agent_assignment_action.py`` and
  ``test_the_empty_answer_becomes_a_failed_item`` goes red, because the item
  completes with the hollow object as its recorded value.
* The mirror case is asserted too: a partially-filled answer still COMPLETES.
  A guard that fails everything proves nothing.

Run with:
  uv run pytest packages/matrx-ai/tests/test_assignment_empty_answer_refusal.py -v
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from matrx_assignment import AssignmentSource, InMemoryAssignmentStore
from pydantic import BaseModel

from matrx_ai import _ext
from matrx_ai.graph_nodes.agent_assignment_action import (
    AgentAssignmentBatchInput,
    run_agent_assignment_batch,
)
from matrx_ai.graph_nodes.shared import configure_empty_structured_output

# The "Sourcing Auditor" contract, verbatim from agent.definition.output_schema.
SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "corrected_article",
        "sourcing_note",
        "cuts",
        "flags",
        "markers_left_in_place",
        "verdict",
    ],
    "properties": {
        "cuts": {"type": "array", "items": {"type": "object"}},
        "flags": {"type": "array", "items": {"type": "object"}},
        "verdict": {"type": "string"},
        "sourcing_note": {"type": "array", "items": {"type": "object"}},
        "corrected_article": {"type": "string"},
        "markers_left_in_place": {"type": "array", "items": {"type": "string"}},
    },
}

# What run 7e155d1a…'s n_audit step delivered, after 3 calls and $2.24.
EMPTY: dict[str, Any] = {
    "cuts": [],
    "flags": [],
    "verdict": "",
    "sourcing_note": [],
    "corrected_article": "",
    "markers_left_in_place": [],
}

# The same contract, answered. ONE field carrying anything is enough.
ANSWERED: dict[str, Any] = {
    "cuts": [],
    "flags": [],
    "verdict": "Clean against the ledger; two figures still lack their period.",
    "sourcing_note": [],
    "corrected_article": "",
    "markers_left_in_place": [],
}


class _PermissiveHostRequest(BaseModel):
    """Stands in for the host's ``AgentStartRequest`` — the host's own request
    validation is that host's test surface, not this package's."""

    model_config = {"extra": "allow"}


def _completed(payload: dict[str, Any]) -> Any:
    """A ``CompletedRequest`` carrying the real declared contract and the real
    assistant text — the two facts the acceptance seam reads."""
    from types import SimpleNamespace

    return SimpleNamespace(
        request=SimpleNamespace(
            config=SimpleNamespace(
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "sourcing_audit",
                        "schema": SCHEMA,
                        "strict": True,
                    },
                }
            ),
            conversation_id="37beba9e-257f-4570-8c48-008a2d10044a",
            request_id="481df405-aebc-4bf1-8d2e-aa7d29ba0295",
        ),
        final_response=SimpleNamespace(
            messages=[
                SimpleNamespace(
                    role="assistant",
                    content=[{"type": "text", "text": json.dumps(payload)}],
                )
            ],
            finish_reason="stop",
        ),
        total_usage=None,
        timing_stats={},
        tool_call_stats={"total_tool_calls": 2},
        iterations=3,
        metadata={"finish_reason": "stop", "matrx_model_name": "claude-sonnet-5"},
    )


@pytest.fixture(autouse=True)
def _platform_default_is_refuse():
    configure_empty_structured_output(allow_empty=False)
    yield
    configure_empty_structured_output(allow_empty=False)


@pytest.fixture
def host(monkeypatch: pytest.MonkeyPatch):
    """Wire the four host exts the node requires, with the REAL in-memory store
    behind the coordinator and only the provider call doubled."""
    store = InMemoryAssignmentStore()

    def _install(payload: dict[str, Any]) -> None:
        async def _agent_runner(_agent_id: str, _request: Any, _app: Any) -> Any:
            return _completed(payload)

        monkeypatch.setitem(_ext._registry, "agent_runner", _agent_runner)
        monkeypatch.setitem(_ext._registry, "AgentStartRequest", _PermissiveHostRequest)
        monkeypatch.setitem(_ext._registry, "assignment_store_factory", lambda _app: store)
        monkeypatch.setitem(
            _ext._registry, "assignment_conversation_exists", lambda _cid: False
        )

    return _install


def _inputs(**overrides: Any) -> AgentAssignmentBatchInput:
    return AgentAssignmentBatchInput.model_validate(
        {
            "agent": {"agent_id": "751ec459-1ca5-445b-822f-b677695a686f"},
            "plan": {
                "strategy": "coordinated_rows",
                "rows": [{"key": "row-1", "values": {"draft": "the article"}}],
            },
            "max_attempts": 1,
            **overrides,
        }
    )


class _PermissiveEmitter:
    """Answers any emitter method with an async no-op — which emitter method the
    node reaches for is not what this suite is checking."""

    async def _noop(self, *_a: Any, **_k: Any) -> None:
        return None

    def __getattr__(self, _name: str) -> Any:
        return self._noop


async def _run(inputs: AgentAssignmentBatchInput) -> Any:
    from matrx_connect.context.app_context import AppContext

    app = AppContext(
        emitter=_PermissiveEmitter(),
        user_id="test-user",
        is_authenticated=True,
        conversation_id="test-conv",
        request_id="test-req",
        organization_id="5dc930e9-bd65-44a1-8369-af773f6e1a5b",
    )
    return await run_agent_assignment_batch(
        app,
        inputs,
        source=AssignmentSource(kind="workflow", workflow_run_id="7e155d1a"),
        idempotency_key=f"test:{id(inputs)}",
        holder="test",
    )


@pytest.mark.asyncio
async def test_the_empty_answer_becomes_a_failed_item(host):
    """(i) The exact payload run 7e155d1a… shipped as a finished audit."""
    host(EMPTY)
    result = await _run(_inputs())

    assert result.session.failed_items == 1, (
        "the all-zero answer was recorded as a COMPLETED assignment item again"
    )
    assert result.session.completed_items == 0

    items = result.items
    assert len(items) == 1
    error = items[0].error
    assert error is not None, "a failed item must carry why"
    assert error.code == "structured_output_empty"
    assert "empty but valid" in error.message
    assert "sourcing_audit" in error.message, "the sentence must name what came back empty"
    assert "nothing to deliver" in error.message
    for field in SCHEMA["required"]:
        assert field in error.message
    assert "allow_empty_structured_output" in (error.details or {}).get("remedy", "")


@pytest.mark.asyncio
async def test_a_partly_filled_answer_still_completes(host):
    """(ii) The mirror: ONE field carrying content is a real answer."""
    host(ANSWERED)
    result = await _run(_inputs())

    assert result.session.completed_items == 1, (
        "a real answer was refused — the guard is over-firing"
    )
    assert result.session.failed_items == 0
    assert result.items[0].output["structured_output"]["verdict"].startswith("Clean")


@pytest.mark.asyncio
async def test_an_author_may_declare_the_step_may_answer_with_nothing(host):
    """(iii) The knob is real: a batch that legitimately empties says so once."""
    host(EMPTY)
    result = await _run(_inputs(allow_empty_structured_output=True))

    assert result.session.completed_items == 1
    assert result.session.failed_items == 0
