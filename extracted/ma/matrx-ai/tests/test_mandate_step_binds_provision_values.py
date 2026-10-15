"""``ai.mandate.start`` hands THE STATE (``provision_values``) to the mandate's BINDING, never to the doer unbound."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

import pytest

from matrx_ai.graph_nodes.mandate_action import MandateStartInput, _bind_provision_values, _state_as_extras


@dataclass
class _Resolved:
    materialize: Any = None
    consumption_map: dict[str, Any] | None = None


def _inputs(**kw: Any) -> MandateStartInput:
    return MandateStartInput.model_validate({"mandate_key": "feature.job", **kw})


async def _bind(state: dict[str, Any]) -> dict[str, Any]:
    return {"evidence": state["a"] + "\n\n" + state["b"]}


def test_the_binding_turns_the_state_into_the_doers_variables() -> None:
    out = asyncio.run(_bind_provision_values(_inputs(provision_values={"a": "x", "b": "y"}, edge_var="e"),
                                             _Resolved(materialize=_bind, consumption_map={"evidence": []})))
    extra = out.model_extra or {}
    assert extra["evidence"] == "x\n\ny" and extra["edge_var"] == "e"
    assert "a" not in extra and out.provision_values is None


def test_no_state_leaves_the_step_unchanged() -> None:
    inputs = _inputs(edge_var="e")
    assert asyncio.run(_bind_provision_values(inputs, _Resolved())) is inputs


@pytest.mark.parametrize(("state", "resolved", "words"), [
    ({}, _Resolved(materialize=_bind, consumption_map={"evidence": []}), "empty state"),
    ({"a": "x"}, _Resolved(materialize=None, consumption_map={"evidence": []}), "no consumption pipeline"),
    ({"a": "x"}, _Resolved(materialize=_bind, consumption_map=None), "no binding map"),
])
def test_the_step_refuses_rather_than_run_unbound(state: dict, resolved: _Resolved, words: str) -> None:
    with pytest.raises(ValueError, match=words):
        asyncio.run(_bind_provision_values(_inputs(provision_values=state), resolved))


def test_a_workflow_holder_gets_the_state_as_its_supplied_offer() -> None:
    out = _state_as_extras(_inputs(provision_values={"a": "x"}, edge_var="e"))
    assert (out.model_extra or {}) == {"a": "x", "edge_var": "e"} and out.provision_values is None
