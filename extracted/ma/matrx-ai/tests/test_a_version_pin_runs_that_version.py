"""A server caller holding a version pin runs exactly that version (SB-03, PB-02 call 4).

Live 2026-10-17: ``mandate_call`` refused every version-pinned binding with
``unsupported_binding`` because its child-run funnel (``agent_call``) could only
load live definitions. ``agent_call`` now takes a host-only ``is_version``
keyword: the id names an ``agent.definition_version`` row, the run gate is the
PARENT definition's visibility, and ``Agent.from_agent(is_version=True)`` loads
the pinned version.

SUT: ``agent_call``. Doubles replace only what it CALLS: the definition and
version loaders, the access session, ``Agent.from_agent`` (recording what was
loaded) and ``run_agent``.

Breaks named: a pin that loads the live definition (``is_version`` dropped); a
pin gated on the version id instead of its agent; a missing version that runs
anything; ``is_version`` showing up on the model's tool schema.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_DEFINITION = "d7fbe234-1adf-415d-aeb5-9f5343df9725"
_VERSION_V3 = "bbbbbbbb-0000-4000-8000-000000000003"


async def _value(v: Any) -> Any:
    return v


def _desk() -> Any:
    from matrx_ai.agents.definition import Agent
    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.config.message_config import UnifiedMessage

    messages = MessageList()
    messages.append(UnifiedMessage.from_dict({"role": "system", "content": "Desk v3."}))
    messages.append(UnifiedMessage.from_dict({"role": "user", "content": "Write the line."}))
    return Agent(UnifiedConfig(model="claude-haiku-5-5", messages=messages), name="Compass Mandate Desk")


@pytest.fixture
def seen(monkeypatch) -> dict[str, list[Any]]:
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition, AgxDefinitionVersion  # noqa: F401

    record: dict[str, list[Any]] = {"definition_loads": [], "version_loads": [], "from_agent": [], "runs": []}

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)

    # A host-less test resolves both ORM names to ONE registry stub, so each
    # table gets its own loader: the version table knows only version ids, the
    # definition table only agent ids.
    def _loader(table: str):
        def _load(cls, row_id):
            record[f"{table}_loads"].append(row_id)
            if table == "version":
                found = row_id == _VERSION_V3
                row = SimpleNamespace(id=_VERSION_V3, agent_id=_DEFINITION, version_number=3)
            else:
                found = row_id == _DEFINITION
                row = SimpleNamespace(id=_DEFINITION, is_active=True, is_archived=False)
            return _value(row if found else None)

        return _load

    import importlib

    # By module path: the package re-exports a FUNCTION named agent_call.
    agent_call_mod = importlib.import_module("matrx_ai.tools.implementations.agent_call")

    monkeypatch.setattr(AgxDefinition, "load_by_id_or_none", classmethod(_loader("definition")))
    # The version door is a separate function; double the model it reads through
    # a distinct stand-in so the two tables never share one double.
    version_model = SimpleNamespace(
        _database=None, load_by_id_or_none=lambda row_id: _loader("version")(None, row_id)
    )
    monkeypatch.setattr(agent_call_mod, "_version_model", lambda: version_model)

    def _from_agent(_cls, agent_id, *a, is_version: bool = False, **k):
        record["from_agent"].append((agent_id, is_version))
        return _value(_desk())

    monkeypatch.setattr(Agent, "from_agent", classmethod(_from_agent))

    async def fake_run_agent(_agent: Any, **kwargs: Any) -> AgentRunResult:
        record["runs"].append(kwargs)
        return AgentRunResult(success=True, output="... Held by Compass desk v3", metadata={})

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    return record


async def _call(args: dict[str, Any], **kw: Any) -> Any:
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=_USER_ID))
    try:
        return await agent_call(args, ToolContext(call_id="call-pin"), **kw)
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_a_pinned_version_runs_that_version_gated_on_its_agent(seen) -> None:
    result = await _call({"agent_id": _VERSION_V3, "user_input": "Write the line."}, is_version=True)

    assert result.success is True, result.error
    assert seen["from_agent"] == [(_VERSION_V3, True)], "the pin was not what ran"
    assert seen["version_loads"] == [_VERSION_V3]
    assert seen["definition_loads"] == [_DEFINITION], "the run gate must be the parent agent"
    assert result.output["agent_id"] == _DEFINITION
    assert result.output["agent_version_id"] == _VERSION_V3
    assert len(seen["runs"]) == 1


@pytest.mark.asyncio
async def test_a_missing_version_runs_nothing(seen) -> None:
    missing = "bbbbbbbb-0000-4000-8000-0000000000ff"
    result = await _call({"agent_id": missing, "user_input": "x"}, is_version=True)

    assert result.success is False
    assert result.error.error_type == "not_found"
    assert seen["from_agent"] == [] and seen["runs"] == []


@pytest.mark.asyncio
async def test_without_the_keyword_the_live_definition_runs(seen) -> None:
    result = await _call({"agent_id": _DEFINITION, "user_input": "Write the line."})
    print("SEEN", seen)

    assert result.success is True, result.error
    assert seen["from_agent"] == [(_DEFINITION, False)]
    assert seen["version_loads"] == []


def test_is_version_is_never_on_the_model_schema() -> None:
    from matrx_ai.tools._generated_declarations import AgentCallArgs

    assert "is_version" not in AgentCallArgs.model_fields
