"""A mandated NamedAgent carries mandate_key and no source — and validates
against the agent the MANDATE resolves to, never a seed.

SUTs: ``NamedAgent._check_definition`` and ``NamedAgent.validate``. The only
doubles are external: the host mandate resolver (installed through the real
``matrx_ai.mandates`` door) and the agent record load (a source whose
``load()`` returns the loaded agent's declared variable contract, built from
the real ``AgentVariable`` model).

Breaks these tests name:
* the BOTH-mandate-and-source refusal is removed (a hardcoded "just in case" id);
* a class with neither is accepted (nothing says which agent runs);
* validate skips resolution and checks nothing / a seed;
* validate checks a contract other than the resolved agent's;
* a failed or missing resolver is reported as ok (silent fallback).
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel

from matrx_ai import mandates
from matrx_ai.agents.named import AgentRecordSource, NamedAgent
from matrx_ai.agents.variables import AgentVariable


class _Inputs(BaseModel):
    topic: str


class _BothSourceAndMandate(NamedAgent[_Inputs, BaseModel]):
    name = "test_both_source_and_mandate"
    mandate_key = "test.both"
    source = AgentRecordSource(agent_id="seed-id", is_version=False)
    Inputs = _Inputs


class _NeitherSourceNorMandate(NamedAgent[_Inputs, BaseModel]):
    name = "test_neither"
    Inputs = _Inputs


class _MandateOnly(NamedAgent[_Inputs, BaseModel]):
    name = "test_mandate_only"
    mandate_key = "test.mandate_only"
    Inputs = _Inputs


def test_check_definition_refuses_mandate_plus_source() -> None:
    with pytest.raises(TypeError, match="declares BOTH mandate_key='test.both' and a hardcoded source"):
        _BothSourceAndMandate._check_definition()


def test_check_definition_refuses_a_class_that_names_no_agent_at_all() -> None:
    with pytest.raises(
        TypeError,
        match=r"missing required class attribute\(s\): mandate_key \(or, for an un-mandated agent, source\)",
    ):
        _NeitherSourceNorMandate._check_definition()


def test_check_definition_accepts_mandate_only() -> None:
    _MandateOnly._check_definition()


@pytest.mark.asyncio
async def test_validate_reports_both_instead_of_crashing() -> None:
    report = await _BothSourceAndMandate.validate()
    assert report.ok is False
    assert report.source_kind == "invalid"
    assert len(report.errors) == 1
    assert "BOTH mandate_key='test.both'" in report.errors[0]


class _LoadedAgent:
    """The loaded agent's declared contract, as ``Agent`` exposes it."""

    def __init__(self, variables: list[AgentVariable]) -> None:
        self.variable_defaults = {v.name: v for v in variables}
        self.context_policies: list[dict[str, Any]] = []


class _ResolvedRecordSource:
    def __init__(self, agent_id: str, agent: _LoadedAgent) -> None:
        self.agent_id = agent_id
        self._agent = agent
        self.loads = 0

    async def load(self) -> _LoadedAgent:
        self.loads += 1
        return self._agent


def _install_resolver(monkeypatch: pytest.MonkeyPatch, source: _ResolvedRecordSource) -> list[str]:
    asked: list[str] = []

    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        asked.append(mandate_key)
        return mandates.MandateResolution(source=source)  # type: ignore[arg-type]

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", resolver)
    return asked


@pytest.mark.asyncio
async def test_validate_passes_against_the_resolved_agents_contract(monkeypatch) -> None:
    source = _ResolvedRecordSource(
        "live-id", _LoadedAgent([AgentVariable(name="topic", required=True)])
    )
    asked = _install_resolver(monkeypatch, source)

    report = await _MandateOnly.validate()

    assert asked == ["test.mandate_only"]
    assert source.loads == 1
    assert report.ok is True
    assert report.errors == []
    assert report.validation_target == "resolved"
    assert report.source_kind == "_ResolvedRecordSource"


@pytest.mark.asyncio
async def test_validate_fails_when_the_resolved_agent_requires_an_unsupplied_variable(
    monkeypatch,
) -> None:
    source = _ResolvedRecordSource(
        "live-id",
        _LoadedAgent(
            [
                AgentVariable(name="topic", required=True),
                AgentVariable(name="audience", required=True),
            ]
        ),
    )
    _install_resolver(monkeypatch, source)

    report = await _MandateOnly.validate()

    assert report.ok is False
    assert report.errors == [
        "agent requires variable(s) ['audience'] but the Inputs contract supplies ['topic']."
    ]


@pytest.mark.asyncio
async def test_validate_reports_a_failed_resolver_as_not_ok(monkeypatch) -> None:
    async def broken_resolver(mandate_key: str) -> mandates.MandateResolution:
        raise RuntimeError("binding table unreachable")

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", broken_resolver)
    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: None)

    report = await _MandateOnly.validate()

    assert report.ok is False
    assert report.validation_target == "resolved"
    assert len(report.errors) == 1
    assert report.errors[0].startswith("failed to resolve mandate 'test.mandate_only': ")
    assert "binding table unreachable" in report.errors[0]


@pytest.mark.asyncio
async def test_validate_with_no_resolver_installed_is_not_ok(monkeypatch) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    report = await _MandateOnly.validate()

    assert report.ok is False
    assert len(report.errors) == 1
    assert "no mandate resolver is installed" in report.errors[0]
