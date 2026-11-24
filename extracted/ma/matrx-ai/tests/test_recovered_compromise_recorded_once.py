"""A recovered structured-output compromise is a capability FACT about one
(model, shape, agent, compromise) — written once per process, not on every call.

Live 2026-11-12: ``structured_output.enforcement_dropped`` landed 633 events in
7 days, 261 of them one identical fact (Agent Structure Builder's
``CreateAgentDefinitionEnvelope`` on claude-opus-5-5: open maps a strict
Anthropic decoder would force empty, so the schema rides as a prompt contract)
and every one judged ON CONTRACT. The open issue said nothing new after the
first. An UNRECOVERED occurrence (call failed, answer off contract) is news
every time and is always written.
"""

from __future__ import annotations

import pytest

from matrx_ai.ops import issue_capture
from matrx_ai.providers import structured_output_findings as findings


@pytest.fixture
def written(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    calls: list[dict] = []

    async def _capture(key, **kwargs):
        calls.append({"key": key, **kwargs})

    monkeypatch.setattr(issue_capture, "capture_issue", _capture)
    findings.forget_recorded_facts()
    yield calls
    findings.forget_recorded_facts()


def _detail(fp: str = "6cc3b8e0fc016689", action: str = "json_schema → json_object: maps") -> dict:
    return {"schema_name": "Envelope", "schema_fingerprint": fp, "action": action, "agent_id": "a1"}


async def _record(detail: dict, *, recovered: bool, key: str = findings.ENFORCEMENT_DROPPED) -> None:
    await findings.record_structured_output_finding(
        key, provider="anthropic", model="claude-opus-5-5", detail=detail, was_recovered=recovered
    )


@pytest.mark.asyncio
async def test_identical_recovered_compromise_is_written_once(written):
    for _ in range(5):
        await _record(_detail(), recovered=True)
    assert len(written) == 1
    assert "once per process" in written[0]["detail"]["recorded"]


@pytest.mark.asyncio
async def test_unrecovered_compromise_is_written_every_time(written):
    await _record(_detail(), recovered=True)
    for _ in range(3):
        await _record(_detail(), recovered=False)
    assert len(written) == 4
    assert [w["was_recovered"] for w in written] == [True, False, False, False]


@pytest.mark.asyncio
async def test_a_different_shape_model_or_compromise_is_its_own_fact(written):
    await _record(_detail(), recovered=True)
    await _record(_detail(fp="ffff"), recovered=True)
    await _record(_detail(action="something else"), recovered=True)
    await _record(_detail(), recovered=True, key=findings.TOOLS_SHED)
    await findings.record_structured_output_finding(
        findings.ENFORCEMENT_DROPPED,
        provider="anthropic",
        model="claude-sonnet-5-5",
        detail=_detail(),
        was_recovered=True,
    )
    assert len(written) == 5


@pytest.mark.asyncio
async def test_answer_off_contract_is_never_collapsed(written):
    for _ in range(3):
        await _record(_detail(), recovered=True, key=findings.ANSWER_OFF_CONTRACT)
    assert len(written) == 3
