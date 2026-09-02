"""🚨 THE TWO-NAME TRUTH — an offer is checked in the CALL SITE's vocabulary.

The 2026-08-27 production incident: every PDF cleanup refused with
``guaranteed offered value(s) ['content'] were not supplied by the call site``
while ``content`` was supplied on every single call. ``PdfCleanerAgent``
declares ``variable_map = {"content": "text_extracted_from_pdf"}``, and the
offer check read ``prepare_variables`` output — the HOLDER's post-rename
variables — against a Provision declared in the CALL SITE's names. Every
renaming mandated agent was dead on arrival, and nothing in the suite noticed
because no test agent renamed anything.

These tests pin BOTH halves: a renamed value satisfies the promise, and a
genuinely absent one still refuses (a check that cannot fail is worse than
none).
"""

from __future__ import annotations

from typing import ClassVar

import pytest
from pydantic import BaseModel

from matrx_ai import mandates
from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.agents.named import AgentRecordSource


class _Inputs(BaseModel):
    content: str | None = None


class _RenamingAgent:
    """Mirrors the shipped ``PdfCleanerAgent`` contract."""

    mandate_key = "test.renaming"
    Inputs = _Inputs
    variable_map: ClassVar[dict[str, str]] = {"content": "text_extracted_from_pdf"}
    ran: ClassVar[bool] = False

    @classmethod
    def prepare_variables(cls, inputs: BaseModel) -> dict[str, object]:
        return {
            cls.variable_map.get(field, field): value
            for field, value in inputs.model_dump().items()
        }

    @classmethod
    async def run(cls, **kwargs) -> AgentRunResult:
        cls.ran = True
        return AgentRunResult(success=True, output="cleaned")


class _CombiningAgent(_RenamingAgent):
    """``prepare_variables`` SYNTHESIZES the offered name out of two fields."""

    mandate_key = "test.combining"

    class Inputs(BaseModel):  # type: ignore[misc]
        head: str = ""
        tail: str = ""

    @classmethod
    def prepare_variables(cls, inputs: BaseModel) -> dict[str, object]:
        data = inputs.model_dump()
        return {"content": f"{data['head']}{data['tail']}" or None}


def _resolver(*values: mandates.OfferedValueSpec):
    async def resolve(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id="resolved-agent", is_version=False),
            provision_key="test.provision",
            offered_values=values,
        )

    return resolve


_CONTENT = mandates.OfferedValueSpec(name="content", kind="text", guaranteed=True)


@pytest.mark.asyncio
async def test_renamed_guaranteed_value_satisfies_the_promise(monkeypatch) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver(_CONTENT))
    _RenamingAgent.ran = False

    result = await mandates.run_mandated(
        _RenamingAgent, inputs=_RenamingAgent.Inputs(content="raw pdf text")
    )

    assert result.success is True
    assert _RenamingAgent.ran is True


@pytest.mark.asyncio
async def test_absent_guaranteed_value_still_refuses(monkeypatch) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver(_CONTENT))
    _RenamingAgent.ran = False

    with pytest.raises(mandates.BrokenOfferPromise) as excinfo:
        await mandates.run_mandated(
            _RenamingAgent, inputs=_RenamingAgent.Inputs(content=None)
        )

    assert excinfo.value.missing == ["content"]
    assert _RenamingAgent.ran is False, "the run must refuse BEFORE the agent runs"


@pytest.mark.asyncio
async def test_synthesized_value_satisfies_the_promise(monkeypatch) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver(_CONTENT))
    _CombiningAgent.ran = False

    result = await mandates.run_mandated(
        _CombiningAgent, inputs=_CombiningAgent.Inputs(head="a", tail="b")
    )

    assert result.success is True
    assert _CombiningAgent.ran is True


@pytest.mark.asyncio
async def test_synthesized_value_absent_still_refuses(monkeypatch) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", _resolver(_CONTENT))
    _CombiningAgent.ran = False

    with pytest.raises(mandates.BrokenOfferPromise):
        await mandates.run_mandated(
            _CombiningAgent, inputs=_CombiningAgent.Inputs(head="", tail="")
        )

    assert _CombiningAgent.ran is False


@pytest.mark.asyncio
async def test_shipped_pdf_cleaner_offer_matches_its_declared_provision() -> None:
    """The real class + the real Provision names — the incident itself."""
    from matrx_ai.agent_runners.content_cleaner import PdfCleanerAgent
    from matrx_ai.agents.named import offer_view

    view = offer_view(PdfCleanerAgent, PdfCleanerAgent.Inputs(content="hello"))

    assert view["content"] == "hello", "the call-site name must be visible to the offer check"
    assert view["text_extracted_from_pdf"] == "hello", "the holder name must survive too"
