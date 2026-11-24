"""Run Typed Agent validates a list answer per item (``config.invalid_list_elements``, default set_aside): the valid
items land, the wrong ones ride beside the kind as ``invalid_elements`` + ``invalid_element_count``, the step is
flagged for review, and the engine is told those keys are not the kind's. Never silent, never kept in the answer.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph import kinds

from matrx_ai.graph_nodes import agent_produce_action as produce
from matrx_ai.graph_nodes.agent_produce_action import TypedAgentConfig


class _Ctx:
    def __init__(self) -> None:
        self.flags: list[tuple[str, str, dict[str, Any]]] = []

    async def flag_for_review(self, label: str, message: str, **kw: Any) -> bool:
        self.flags.append((label, message, kw))
        return True


def _check_ids(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _check(value: Any, slug: str) -> kinds.KindCheck:
        errors = [f"rankings.{i}: 'id' is a required property"
                  for i, r in enumerate(value.get("rankings", [])) if "id" not in r]
        return kinds.KindCheck(checked=True, errors=errors)

    monkeypatch.setattr(kinds, "check_against_kind", _check)


@pytest.mark.asyncio
async def test_wrong_items_are_set_aside_reported_counted_and_flagged(monkeypatch: pytest.MonkeyPatch) -> None:
    _check_ids(monkeypatch)
    ctx = _Ctx()
    payload = {"__kind": "k", "rankings": [{"id": "a"}, {"score": 1}, {"id": "c"}]}
    out, fields = await produce._set_aside_invalid_elements(ctx, payload, "k", "judge")  # type: ignore[arg-type]
    assert out["rankings"] == [{"id": "a"}, {"id": "c"}]
    assert out["invalid_element_count"] == 1
    assert out["invalid_elements"][0]["field"] == "rankings" and out["invalid_elements"][0]["index"] == 1
    assert fields == ["invalid_elements", "invalid_element_count"]
    assert ctx.flags and ctx.flags[0][0] == "agent.invalid_list_elements"


@pytest.mark.asyncio
async def test_a_clean_answer_carries_no_extra_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    _check_ids(monkeypatch)
    ctx = _Ctx()
    payload = {"__kind": "k", "rankings": [{"id": "a"}]}
    assert await produce._set_aside_invalid_elements(ctx, payload, "k", "n") == (payload, [])  # type: ignore[arg-type]
    assert ctx.flags == []


@pytest.mark.asyncio
async def test_a_kind_that_owns_the_names_is_never_overwritten(monkeypatch: pytest.MonkeyPatch) -> None:
    _check_ids(monkeypatch)
    payload = {"__kind": "k", "rankings": [{"score": 1}, {"id": "b"}], "invalid_element_count": 9}
    assert await produce._set_aside_invalid_elements(_Ctx(), payload, "k", "n") == (payload, [])  # type: ignore[arg-type]


def test_set_aside_is_the_default_and_fail_is_a_choice() -> None:
    assert TypedAgentConfig().invalid_list_elements == "set_aside"
    assert TypedAgentConfig(invalid_list_elements="fail").invalid_list_elements == "fail"
