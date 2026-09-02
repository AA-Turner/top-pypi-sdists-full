"""A mandated NamedAgent carries mandate_key and no source."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel

from matrx_ai.agents.named import AgentRecordSource, NamedAgent
from matrx_ai.mandates import MandateResolution


class _Inputs(BaseModel):
    topic: str


class _BothSourceAndMandate(NamedAgent[_Inputs, BaseModel]):
    name = "test_both_source_and_mandate"
    mandate_key = "test.both"
    source = AgentRecordSource(agent_id="seed-id", is_version=False)
    Inputs = _Inputs


class _MandateOnly(NamedAgent[_Inputs, BaseModel]):
    name = "test_mandate_only"
    mandate_key = "test.mandate_only"
    Inputs = _Inputs


def test_check_definition_refuses_mandate_plus_source() -> None:
    with pytest.raises(TypeError, match="BOTH mandate_key"):
        _BothSourceAndMandate._check_definition()


@pytest.mark.asyncio
async def test_validate_reports_both_instead_of_crashing() -> None:
    report = await _BothSourceAndMandate.validate()
    assert report.ok is False
    assert any("BOTH mandate_key" in error for error in report.errors)


class _ResolvedSource:
    agent_id = "live-id"

    async def load(self) -> object:
        return object()


@pytest.mark.asyncio
async def test_validate_resolves_mandate_when_class_has_no_source(monkeypatch) -> None:
    resolved = _ResolvedSource()
    monkeypatch.setattr(
        "matrx_ai.mandates.resolve_mandate_for",
        AsyncMock(return_value=MandateResolution(source=resolved)),  # type: ignore[arg-type]
    )
    monkeypatch.setattr(
        "matrx_ai.agents.named._declared_variable_names",
        lambda _agent: {"topic"},
    )
    monkeypatch.setattr(
        "matrx_ai.agents.named._declared_context_names",
        lambda _agent: set(),
    )
    monkeypatch.setattr(
        "matrx_ai.agents.named._required_variable_names",
        lambda _agent: {"topic"},
    )

    report = await _MandateOnly.validate()
    assert report.ok is True
    assert report.validation_target == "resolved"
    assert report.source_kind == "_ResolvedSource"
