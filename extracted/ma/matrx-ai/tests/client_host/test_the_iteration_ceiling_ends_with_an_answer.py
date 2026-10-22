"""A run that reaches its iteration ceiling ends with an ANSWER, never a bare tool call.

THE DEFECT (2026-10-21 audit of conversation 9b224bf5). Background helpers started
by the harness ``agent`` tool ran into the library ceiling (100 rounds) mid-task.
The loop just fell out after its 100th tool round: the run's last turn was a tool
call, there was no prose, the caller was handed raw tool-call JSON as the helper's
"answer", and the run settled ``paused`` (waiting for a person to type "continue")
in a conversation no person was in.

What each test is FOR (the production change that turns it red):

* the ceiling's wrap-up turn — delete the ``iteration >= max_iterations`` block in
  ``execute_until_complete`` and the run ends on a tool call with no answer turn;
* tools really are off in that turn — drop the ``config.tools = []`` and the wrap-up
  call is offered tools again;
* a model that calls a tool anyway runs nothing past the ceiling — drop the
  wrap-up dispatch guard and one more tool call executes;
* the wrap-up instruction is a HOST notice, never text added to a person's message;
* a sub-agent's ceiling stop settles terminal-with-reason, a person's chat still
  pauses — drop the ``resumed_by_caller`` stamp or the PERSON_RESUMES branch and the
  sub-agent row goes back to ``paused``.

The provider is the in-repo mock (no network). It is made to behave like a real
model that ALWAYS reaches for a tool while it has one: it emits a tool call on
every turn whose request offers tools, and only text when offered none.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)

TOOL = "ceiling_probe_tool"
WRAP_UP_TEXT = "Stopped at the step limit. Done: probed 3 files. Left: the fourth. Next: probe it."


@pytest.fixture
def probe_tool():
    """A real local tool that returns instantly; counts how many times it RAN."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    saved_by_id = dict(registry._tools_by_id)
    saved_loaded = registry._loaded
    ran: list[str] = []

    async def _probe(args: dict[str, Any], ctx: Any) -> dict[str, Any]:
        ran.append(str((args or {}).get("path")))
        return {"probed": (args or {}).get("path")}

    registry.register_local(
        TOOL,
        _probe,
        description="probe one path",
        parameters={"path": {"type": "string", "description": "a path"}},
    )
    registry._loaded = True
    try:
        yield ran
    finally:
        registry._tools.clear()
        registry._tools.update(saved_tools)
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved_by_id)
        registry._loaded = saved_loaded


def _tool_hungry_model(monkeypatch, *, ignores_empty_tool_list: bool) -> list[list[str]]:
    """Make the mock call the tool on EVERY turn (fresh arguments each time, so the
    loop guard's repeated-call rule never ends the run first). Returns the tools
    offered on each provider call, in order."""
    from matrx_ai.providers.mock.mock_api import MockChat

    offered: list[list[str]] = []
    original_raw_spec = MockChat._raw_spec
    monkeypatch.setattr(
        MockChat, "_history_has_tool_result", staticmethod(lambda unified_config: False)
    )

    def _raw_spec(unified_config):
        raw = dict(original_raw_spec(unified_config) or {})
        tools = [str(t) for t in (unified_config.tools or [])] + [
            str(getattr(t, "name", t)) for t in (unified_config.custom_tools or [])
        ]
        offered.append(tools)
        if tools or ignores_empty_tool_list:
            raw["tool_calls"] = [{"name": TOOL, "arguments": {"path": f"file-{len(offered)}"}}]
        else:
            raw["tool_calls"] = []
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    return offered


def _configure() -> None:
    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )


def _set_context(*, sub_agent: bool) -> None:
    from matrx_connect.context.app_context import AppContext, set_app_context

    set_app_context(
        AppContext(
            emitter=FakeEmitter(),
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            # A sub-agent is a fork with a parent conversation; a person's chat is not.
            parent_conversation_id=str(uuid.uuid4()) if sub_agent else None,
            is_internal_agent=sub_agent,
            store=True,
            source_app="client_host_tests",
            source_feature="test",
            metadata={},
        )
    )


def _config() -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model="mock-model",
        tools=[TOOL],
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="probe every file")])]
        ),
        metadata={
            "mock": {"latency_ms": 1, "ttft_ms": 0, "chunks": 1, "mode": "text", "text": WRAP_UP_TEXT}
        },
    )


def _text_of(message: Any) -> str:
    from matrx_ai.config import TextContent

    return "".join(c.text for c in (message.content or []) if isinstance(c, TextContent))


def _tool_calls_in(message: Any) -> int:
    from matrx_ai.config.tools_config import ToolCallContent

    return sum(1 for c in (message.content or []) if isinstance(c, ToolCallContent))


@pytest.mark.asyncio
@pytest.mark.parametrize(("ceiling", "warned"), [(3, False), (5, True)])
async def test_a_ceiling_run_ends_with_a_tool_less_answer_turn(
    probe_tool, monkeypatch, ceiling, warned
):
    from matrx_ai.orchestrator.executor import execute_ai_request

    offered = _tool_hungry_model(monkeypatch, ignores_empty_tool_list=False)
    _configure()
    _set_context(sub_agent=False)

    completed = await execute_ai_request(_config(), max_iterations=ceiling)
    meta = completed.metadata or {}

    # Exactly `ceiling` tool rounds RAN, then ONE more provider call — the answer.
    assert len(probe_tool) == ceiling, f"{len(probe_tool)} tool rounds ran under a ceiling of {ceiling}"
    assert len(offered) == ceiling + 1, f"{len(offered)} provider calls; expected {ceiling} + the wrap-up"
    assert completed.iterations == ceiling + 1, "the wrap-up turn was not counted as an iteration"
    assert all(offered[:ceiling]), "a tool round was offered no tools"
    assert offered[-1] == [], f"the wrap-up turn was offered tools: {offered[-1]}"

    # The run ENDS on the model's own words, not on a tool call.
    messages = list(completed.request.config.messages)
    last = messages[-1]
    assert last.role == "assistant", f"the run ended on a {last.role} turn"
    assert _tool_calls_in(last) == 0
    assert _text_of(last) == WRAP_UP_TEXT

    # Still recorded as the ceiling stop it is, never a clean completion.
    assert meta.get("status") == "max_iterations_exceeded"
    assert meta.get("max_iterations") == ceiling
    assert "iteration ceiling" in str(meta.get("error") or "")

    # The instruction is a HOST notice; the person's message is untouched.
    users = [m for m in messages if m.role == "user"]
    assert _text_of(users[0]) == "probe every file"
    host = [m for m in users[1:] if (m.metadata or {}).get("authored_by") == "host"]
    reasons = [(m.metadata or {}).get("authored_reason") for m in host]
    assert "iteration_ceiling_wrap_up" in reasons
    assert ("iteration_ceiling_approaching" in reasons) is warned
    assert all(m.user_content == [] for m in host), "a host notice claimed a person wrote it"
    assert all(m in host for m in users[1:]), "a non-host user turn appeared mid-run"


@pytest.mark.asyncio
async def test_a_model_that_calls_a_tool_anyway_runs_nothing_past_the_ceiling(
    probe_tool, monkeypatch
):
    from matrx_ai.orchestrator.executor import execute_ai_request

    offered = _tool_hungry_model(monkeypatch, ignores_empty_tool_list=True)
    _configure()
    _set_context(sub_agent=False)

    completed = await execute_ai_request(_config(), max_iterations=2)

    assert len(probe_tool) == 2, f"{len(probe_tool)} tool calls ran under a ceiling of 2"
    assert offered[-1] == [], "the wrap-up turn was offered tools"
    assert (completed.metadata or {}).get("status") == "max_iterations_exceeded"


@pytest.mark.asyncio
@pytest.mark.parametrize(("sub_agent", "expected"), [(True, "completed"), (False, "paused")])
async def test_who_resumes_a_ceiling_stop_decides_how_it_settles(
    probe_tool, monkeypatch, sub_agent, expected
):
    """A person's chat pauses (they are there to say continue); a sub-agent's run
    settles terminal-with-reason (its caller continues it, nobody types in it)."""
    from matrx_ai.orchestrator.executor import execute_ai_request

    _tool_hungry_model(monkeypatch, ignores_empty_tool_list=False)
    _configure()
    _set_context(sub_agent=sub_agent)

    completed = await execute_ai_request(_config(), max_iterations=2)
    summary = completed.build_request_summary()

    assert (completed.metadata or {}).get("status") == "max_iterations_exceeded"
    assert summary["status"] == expected
    assert "iteration ceiling" in str(summary.get("error") or ""), (
        "the ceiling's reason was dropped from the settled row"
    )
