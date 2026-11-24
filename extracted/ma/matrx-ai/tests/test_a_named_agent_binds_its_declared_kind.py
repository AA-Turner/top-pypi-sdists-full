"""Forcing function: a NamedAgent run binds the mandate's declared kind, and still reads with its class.

Platform law (Content IR rule 30): a structured agent is born bound to the REGISTERED kind it names.
The mandate doors (``run_mandate``, ``/ai/mandates``, the workflow Run Mandate step) bind the declared
kind's schema at the provider boundary. The code lane (``NamedAgent.run``) bound ``cls.Output`` — the
same mandate answered under a different contract depending on which door ran it.

Now the host hands the kind schema in as ``provider_schema``: the provider is held to the kind, and the
answer is still parsed by ``cls.Output`` (the one typed reader every caller already uses). Gut check:
drop the pass-through in ``NamedAgent.run`` or the ``provider_schema`` branch in ``run_agent`` and
these fail.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from pydantic import BaseModel, Field

from matrx_ai.agents import named as named_mod
from matrx_ai.config import UnifiedConfig

KIND_SCHEMA = {
    "type": "object",
    "properties": {
        "__kind": {"type": "string", "const": "probe_answer"},
        "answer": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["__kind", "answer", "tags"],
    "additionalProperties": False,
}


class _In(BaseModel):
    topic: str = ""


class _Out(BaseModel):
    answer: str = ""
    tags: list[str] = Field(default_factory=list)


class _FakeAgent:
    variable_defaults: dict = {}
    request_metadata: dict = {}
    auto_tools_disabled = None
    config = SimpleNamespace(metadata={}, custom_tools=[])

    def set_variables(self, **_: object) -> None:
        return None


class _Source:
    async def load(self) -> _FakeAgent:
        return _FakeAgent()


class _Probe(named_mod.NamedAgent):
    name = "kind_binding_probe"
    Inputs = _In
    Output = _Out
    source = _Source()
    child_source_app = "test"
    child_source_feature = "test"


async def _named_run(monkeypatch, **kw) -> dict:
    seen: dict = {}

    async def fake_run_agent(agent, **kwargs):
        seen.update(kwargs)
        return SimpleNamespace(parsed=None, success=True)

    monkeypatch.setattr(named_mod, "run_agent", fake_run_agent)
    await _Probe.run(inputs=_In(), **kw)
    return seen


@pytest.mark.asyncio
async def test_the_declared_kind_reaches_the_executor_beside_the_reader(monkeypatch) -> None:
    seen = await _named_run(monkeypatch, provider_schema=KIND_SCHEMA)
    assert seen["provider_schema"] == KIND_SCHEMA, "the kind never reached the provider boundary"
    assert seen["json_schema"] is _Out, "the answer must still be read by the class's own Output"


@pytest.mark.asyncio
async def test_no_declared_kind_keeps_the_class_contract(monkeypatch) -> None:
    seen = await _named_run(monkeypatch)
    assert seen["provider_schema"] is None
    assert seen["json_schema"] is _Out


@pytest.mark.asyncio
async def test_run_agent_binds_the_kind_and_parses_with_the_class() -> None:
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="kind-binding-test"))
    config = UnifiedConfig.from_dict({"model": "test-model", "messages": [{"role": "user", "content": "go"}]})
    seen: dict = {}

    async def execute(user_input=None, *, max_iterations=None, **_kw):
        seen["response_format"] = config.response_format
        return SimpleNamespace(
            output=json.dumps({"__kind": "probe_answer", "answer": "yes", "tags": ["a"]}),
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="probe", config=config, output_schema=None, source_id=None, source_is_version=False, execute=execute
    )
    result = await run_agent(
        agent,
        label="probe",
        source_app="test",
        source_feature="probe",
        json_schema=_Out,
        provider_schema=KIND_SCHEMA,
        emit_lifecycle=False,
    )

    assert result.success is True, result.error
    bound = seen["response_format"]["json_schema"]["schema"]
    assert bound["properties"]["__kind"]["const"] == "probe_answer", "the provider was not held to the kind"
    assert isinstance(result.parsed, _Out), "the class's reader no longer read the answer"
    assert result.parsed.answer == "yes" and result.parsed.tags == ["a"]
