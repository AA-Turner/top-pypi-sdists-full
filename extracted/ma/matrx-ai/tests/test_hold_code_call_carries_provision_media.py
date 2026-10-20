"""A held code call whose mandate's provision declares media carries that media (AT-FOLLOW, 2026-10-19).

Found live (lane AT-IMAGE-AI): the host pipeline REFUSED any media a binding routed to a held code call, so the
seam dropped the picture value from the provision and attached blocks by hand. A host that offers
``materialize_media`` hands the blocks back and ``HeldCall.media_blocks`` carries them; a mandate without media
keeps the old contract.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.mandates as mandates
from matrx_ai.agents.variables import AgentVariable


class _Agent:
    def __init__(self, declared: dict[str, AgentVariable]) -> None:
        self.variable_defaults = declared
        self.name = "Fake Holder"
        self.bound: dict[str, Any] = {}
        self.config = SimpleNamespace(
            model="holder-model",
            system_instruction=None,
            resolved_system_instruction="SYSTEM",
            messages=[],
            temperature=0.2,
            max_output_tokens=900,
        )

    def apply_config_overrides(self, **_kwargs: Any) -> None:
        return None

    def with_variables(self, **variables: Any) -> _Agent:
        self.bound.update(variables)
        return self

    # The real Agent's async door: set → the pre-substitution step → apply.
    def set_variables(self, **variables: Any) -> _Agent:
        self.bound.update(variables)
        return self

    async def prepare_variables(self) -> _Agent:
        self.prepared = True
        return self

    def apply_variables(self) -> _Agent:
        assert getattr(self, "prepared", False), "substituted before the pre-substitution step"
        return self


class _Source:
    agent_id = "11111111-1111-1111-1111-111111111111"
    is_version = False

    def __init__(self, agent: _Agent) -> None:
        self._agent = agent

    async def load(self) -> _Agent:
        return self._agent


@pytest.fixture
def records(monkeypatch):
    captured: list[dict[str, Any]] = []

    async def _report(*, mandate_key, consumer, exc):
        captured.append({"mandate_key": mandate_key, "consumer": consumer, "reason": str(exc)})

    monkeypatch.setattr(mandates, "_report_resolution_failure", _report)
    return captured


def _install(monkeypatch, resolution: mandates.MandateResolution) -> None:
    async def _resolver(_key: str):
        return resolution

    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver)



BLOCK = {"type": "image", "file_id": "f-1", "mime_type": "image/png"}


async def test_a_media_provision_hands_its_blocks_to_the_held_call(monkeypatch, records) -> None:
    agent = _Agent({"body": AgentVariable(name="body")})

    async def _materialize_media(supplied: dict[str, Any]):
        return {"body": supplied["text"]}, [dict(BLOCK)]

    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(agent),
            consumption_map={"body": {"source": "text"}},
            materialize_media=_materialize_media,
        ),
    )
    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi", "pics": ["f-1"]})
    assert held.media_blocks == [BLOCK]
    assert agent.bound == {"body": "hi"}


async def test_a_mandate_without_media_carries_none(monkeypatch, records) -> None:
    agent = _Agent({"body": AgentVariable(name="body")})

    async def _materialize(supplied: dict[str, Any]) -> dict[str, Any]:
        return {"body": supplied["text"]}

    _install(
        monkeypatch,
        mandates.MandateResolution(
            source=_Source(agent), consumption_map={"body": {"source": "text"}}, materialize=_materialize
        ),
    )
    held = await mandates.hold_code_call("x.y", consumer="t", variables={"text": "hi"})
    assert held.media_blocks == []
