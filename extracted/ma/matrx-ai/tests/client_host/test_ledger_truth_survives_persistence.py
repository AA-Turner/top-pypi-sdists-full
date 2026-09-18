"""THE DURABLE half of the ledger-truth override, driven end to end.

The break this guards (live, 2026-09-15): the Sandbox Specialist agent ran
through ``POST /api/v2/ai/agents/{id}``, its first ``shell_execute`` errored
(``[mtx new] … already exists and is not empty``), and the answer STORED on
conversations ``74bcf027…`` / ``ed621e74…`` said *"Successfully set up the
Python project …"* with ``"tools_failed": []``. The ledger override shipped in
``ab9fff8e7`` was live — but it corrected only the EPHEMERAL parsed copy handed
to the stream event. The turn's assistant TEXT, which is the only durable record
and the thing every later consumer re-parses (frontend, v1/v2 API callers,
``graph_nodes.shared._extract_structured_output``, a resume, a human reading
``chat.message``), kept the model's lie.

So this test asserts the DURABLE artifact, not the event: after a real run whose
tool failed, the text the persistence layer was handed must itself name the
failure. Remove ``_apply_ledger_truth_to_turn_text`` from either persistence
seam in ``matrx_ai.orchestrator.executor`` and this test goes red.

Nothing inside the system under test is stubbed: the real orchestrator loop, the
real tool registry and executor, the real ``ToolExecutionLogger`` (which feeds
the ledger), the real parse funnel, the real mock provider following the real
provider path. The doubles are the provider's network (MockChat), the emitter,
and the conversation store — the same three the sibling client-host tests use.
"""

from __future__ import annotations

import json
import uuid
from typing import Any

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)

# The sibling harness's mock model declares no structured_output capability, so
# the send boundary DOWNGRADES a json_schema response_format to plain text and
# the structured contract never reaches the chokepoint. This run is about that
# contract, so the model declares it.
_STRUCTURED_MOCK_MODEL = {
    **_MOCK_MODEL,
    "id": str(uuid.uuid4()),
    "name": "mock-model-structured",
    "capabilities": {
        **_MOCK_MODEL["capabilities"],
        "features": [*_MOCK_MODEL["capabilities"]["features"], "structured_output"],
    },
}

FAILING_TOOL = "ledger_truth_probe_shell"
FAILING_COMMAND = "mtx new python revcheck1 && uv run pytest -q"
TOOL_ERROR_TEXT = "[mtx new] /home/agent/projects/revcheck1 already exists and is not empty"

# The Sandbox Specialist's report contract, trimmed to the fields that matter.
REPORT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer", "tools_worked", "tools_failed", "commands_run"],
    "properties": {
        "answer": {"type": "string"},
        "tools_worked": {"type": "array", "items": {"type": "string"}},
        "tools_failed": {"type": "array", "items": {"type": "string"}},
        "commands_run": {"type": "array", "items": {"type": "string"}},
    },
}

# Verbatim shape of the lie: a confident answer, an empty failure list, and the
# failed tool listed as having WORKED.
LYING_ANSWER = {
    "answer": "Successfully set up the Python project revcheck1 using mtx new python.",
    "tools_worked": [FAILING_TOOL],
    "tools_failed": [],
    "commands_run": [FAILING_COMMAND],
}


@pytest.fixture
def failing_tool_registered():
    """Register a real local tool that RAISES; restore the registry after."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    saved_by_id = dict(registry._tools_by_id)
    saved_loaded = registry._loaded

    async def _explode(args: dict[str, Any], ctx: Any) -> dict[str, Any]:
        raise RuntimeError(TOOL_ERROR_TEXT)

    registry.register_local(
        FAILING_TOOL,
        _explode,
        description="probe shell tool that always fails",
        parameters={"command": {"type": "string", "description": "shell command"}},
    )
    registry._loaded = True
    try:
        yield registry
    finally:
        registry._tools.clear()
        registry._tools.update(saved_tools)
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved_by_id)
        registry._loaded = saved_loaded


def _set_context(emitter: FakeEmitter) -> tuple[str, str, str]:
    from matrx_connect.context.app_context import AppContext, set_app_context

    conversation_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=user_id,
            request_id=request_id,
            conversation_id=conversation_id,
            is_internal_agent=True,
            store=True,
            source_app="client_host_tests",
            source_feature="test",
        )
    )
    return conversation_id, request_id, user_id


class _CapturingEmitter(FakeEmitter):
    """FakeEmitter plus the one seam the structured-output chokepoint needs."""

    def __init__(self) -> None:
        super().__init__()
        self.structured: list[Any] = []

    async def send_structured_output(self, payload: Any) -> None:
        self.structured.append(payload)


async def _run_lying_agent() -> tuple[Any, _CapturingEmitter, InMemoryStore]:
    store = InMemoryStore()
    configure_ext(
        conversation_store=store,
        model_catalog=StaticCatalog([_STRUCTURED_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )
    emitter = _CapturingEmitter()
    conversation_id, request_id, _user_id = _set_context(emitter)

    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    config = UnifiedConfig(
        model="mock-model-structured",
        messages=MessageList(
            _messages=[
                UnifiedMessage(
                    role="user",
                    content=[TextContent(text="Set up a Python project called revcheck1.")],
                )
            ]
        ),
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "sandbox_report", "strict": True, "schema": REPORT_SCHEMA},
        },
        tools=[FAILING_TOOL],
        metadata={
            "mock": {
                "latency_ms": 1,
                "ttft_ms": 0,
                "chunks": 1,
                "mode": "text",
                "text": json.dumps(LYING_ANSWER, indent=2),
                "tool_calls": [
                    {"name": FAILING_TOOL, "arguments": {"command": FAILING_COMMAND}}
                ],
            }
        },
    )
    request = AIMatrixRequest(
        conversation_id=conversation_id,
        config=config,
        request_id=request_id,
    )
    completed = await execute_until_complete(request, UnifiedAIClient())
    return completed, emitter, store


def _durable_answer(completed: Any) -> dict[str, Any]:
    """The structured answer as it exists in the text handed to persistence —
    parsed the same way every downstream consumer parses it."""
    text = completed.request.config.get_last_output() or ""
    from matrx_ai.agents.output import parse_agent_output

    extraction = parse_agent_output(
        text, {"name": "sandbox_report", "schema": REPORT_SCHEMA}
    )
    assert extraction.success, f"durable turn text did not parse: {text!r}"
    assert isinstance(extraction.data, dict)
    return extraction.data


@pytest.mark.asyncio
async def test_durable_turn_text_carries_the_tool_failure(failing_tool_registered):
    """A run whose tool errored may not leave a 'tools_failed: []' answer behind."""
    completed, _emitter, _store = await _run_lying_agent()

    answer = _durable_answer(completed)

    assert answer["tools_failed"], (
        "THE BUG: the stored answer still claims no tool failed, while the run's own "
        f"tool ledger holds an errored {FAILING_TOOL} call. "
        f"durable answer = {answer!r}"
    )
    failure_text = " ".join(str(item) for item in answer["tools_failed"])
    assert FAILING_TOOL in failure_text
    assert "already exists and is not empty" in failure_text
    assert FAILING_TOOL not in answer["tools_worked"], (
        "a tool that errored may never be listed as having worked"
    )


@pytest.mark.asyncio
async def test_emitted_structured_output_carries_the_tool_failure(failing_tool_registered):
    """The ephemeral half stays correct too — belt and braces, one truth."""
    _completed, emitter, _store = await _run_lying_agent()

    assert emitter.structured, "no structured_output event was emitted"
    data = emitter.structured[-1].data
    assert isinstance(data, dict)
    assert data["tools_failed"], f"emitted structured output still lies: {data!r}"
    assert FAILING_TOOL not in data["tools_worked"]


@pytest.mark.asyncio
async def test_commands_run_comes_from_the_ledger_not_the_model(failing_tool_registered):
    """The command the platform actually dispatched, not the one the model recalls."""
    completed, _emitter, _store = await _run_lying_agent()

    answer = _durable_answer(completed)
    assert answer["commands_run"] == [FAILING_COMMAND]


def test_v1_and_v2_entry_points_share_this_one_loop():
    """Both product routes reach the corrected loop — no second lane exists.

    ``POST /ai/agents/{id}`` (v1) runs ``run_ai_task``; ``POST /api/v2/ai/agents/{id}``
    (v2) runs ``run_ai_task_on_spine``, which is ``run_ai_task`` wrapped in the
    runtime spine. Both bottom out in ``execute_until_complete`` — the function the
    tests above drive — so a fix there is a fix on every route. If that ever stops
    being true, this fails and the behavioural tests above must be duplicated for
    the new lane.
    """
    from aidream.services.ai_execution import ai_task
    from aidream.services.runtime import conversation

    spine_src = stable_source(conversation.run_ai_task_on_spine)
    assert "run_ai_task(" in spine_src, (
        "the v2 spine no longer delegates to run_ai_task — it has grown a second "
        "execution lane that the ledger-truth chokepoint does not cover."
    )
    v1_src = stable_source(ai_task)
    assert "execute_until_complete" in v1_src, (
        "run_ai_task no longer reaches execute_until_complete — the ledger-truth "
        "chokepoint is no longer on the v1/v2 path."
    )
