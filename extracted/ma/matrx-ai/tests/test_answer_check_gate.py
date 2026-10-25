"""L6e guard: the finishing-exit ANSWER CHECK sends a structured answer that breaks its kind's rules back once.

Passes when a JSON answer with ``__kind`` is handed to the host check, its problems force ONE corrective turn (the
notice names each problem), the budget then discloses instead of looping, and a prose or kind-less answer never asks.
"""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from matrx_ai import _ext
from matrx_ai.orchestrator import answer_checks as ac
from matrx_ai.orchestrator import executor


def test_only_a_kind_instance_is_checked():
    assert ac.structured_answer('{"__kind": "brand_element_options", "elements": []}') == {
        "__kind": "brand_element_options", "elements": []}
    assert ac.structured_answer("Here is the plan.") is None
    assert ac.structured_answer('{"elements": []}') is None


def test_force_once_then_disclose():
    report = ac.AnswerCheckReport.from_host({"kind": "k", "problems": ["x says y"], "correction_turns": 1})
    assert ac.decide_answer_check_action(report, corrections_used=0) == "force"
    assert ac.decide_answer_check_action(report, corrections_used=1) == "disclose"
    assert ac.decide_answer_check_action(None, corrections_used=0) == "proceed"
    assert "x says y" in ac.correction_notice(report)


async def test_the_gate_asks_the_host_with_the_answer(monkeypatch: pytest.MonkeyPatch):
    seen = {}

    async def check(*, answer, kind, **_kw):
        seen.update(kind=kind, answer=answer)
        return {"kind": kind, "problems": ['h7 option 2 says "Founded in 2000"'], "correction_turns": 1}

    answer = {"__kind": "brand_element_options", "elements": []}
    monkeypatch.setitem(_ext._registry, "answer_check", check)
    monkeypatch.setattr(executor, "_assistant_text_from_response", lambda _r: json.dumps(answer))
    state = SimpleNamespace(answer_check_corrections=0)
    action, report = await executor._answer_check_gate(SimpleNamespace(metadata={}), object(), state)
    assert action == "force" and seen["kind"] == "brand_element_options" and seen["answer"] == answer
    assert "Founded in 2000" in ac.correction_notice(report)
    state.answer_check_corrections = 1
    assert (await executor._answer_check_gate(SimpleNamespace(metadata={}), object(), state))[0] == "disclose"
