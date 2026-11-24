"""A workflow step that runs a mandate offers the values it holds IN HAND (``given``), never as eager legacy.

Break this catches (ops.system_error ``mandate_offer_eager_legacy``, ~70 open rows 2026-11-02, e.g.
``brand_discovery.curate @ matrx_ai/graph_nodes/mandate_action.py:220`` and ``agent_factory.instructions @
matrx_ai/graph_nodes/agent_produce_action.py:399``): both graph nodes handed the host's consumption pipeline
(``resolved.materialize``) a PLAIN dict of the state / step variables, so every workflow step that ran a mandate
was announced as a not-yet-migrated eager-legacy call site. A value the run already holds is ``given``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.mandates import Offered


def _assert_in_hand(values: dict[str, Any], expected: dict[str, Any]) -> None:
    assert set(values) == set(expected)
    for name, value in values.items():
        assert isinstance(value, Offered), name
        assert value.in_hand and not value.legacy, name
        assert value.build(None) == expected[name], name


def _resolved(seen: dict[str, Any]) -> SimpleNamespace:
    async def materialize(supplied: dict[str, Any]) -> dict[str, Any]:
        seen["supplied"] = dict(supplied)
        return {"topic": "bound"}

    return SimpleNamespace(materialize=materialize, consumption_map={"topic": ["state.topic"]})


@pytest.mark.asyncio
async def test_the_mandate_step_offers_its_state_in_hand() -> None:
    from matrx_ai.graph_nodes.mandate_action import MandateStartInput, _bind_provision_values

    seen: dict[str, Any] = {}
    inputs = MandateStartInput.model_validate(
        {"mandate_key": "demo.job", "provision_values": {"topic": "tides", "count": 3}}
    )
    bound = await _bind_provision_values(inputs, _resolved(seen))
    _assert_in_hand(seen["supplied"], {"topic": "tides", "count": 3})
    assert bound.model_extra == {"topic": "bound"}


@pytest.mark.asyncio
async def test_the_produce_step_offers_its_variables_in_hand() -> None:
    from matrx_ai.graph_nodes.agent_produce_action import _apply_mandate_binding

    seen: dict[str, Any] = {}
    request = SimpleNamespace(variables={"topic": "tides"})
    out = await _apply_mandate_binding(request, _resolved(seen), "demo.job", "node-1")
    _assert_in_hand(seen["supplied"], {"topic": "tides"})
    assert out.variables == {"topic": "bound"}
