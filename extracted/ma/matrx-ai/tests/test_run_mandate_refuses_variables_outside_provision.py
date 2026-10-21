"""A Run Mandate step refuses the doer's variables fed outside ``provision_values`` (Arman, 2026-10-19).

A Run Mandate step hands the mandate its STATE by the provision's offered names and the binding
picks what the doer receives. A value fed under the doer's own variable names skips the binding,
so the step refuses BEFORE anything resolves or spends — proven here by a resolver that records
whether it was reached.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.graph_nodes import mandate_action
from matrx_ai.graph_nodes.mandate_action import MandateStartInput


class _Reached(Exception):
    pass


@pytest.fixture
def resolver_reached(monkeypatch):
    calls: list[str] = []

    async def fake_resolve(inputs, **_kwargs):
        calls.append(inputs.mandate_key)
        raise _Reached

    monkeypatch.setattr(mandate_action, "resolve_step_agent_full", fake_resolve)
    return calls


async def _run(payload: dict) -> None:
    ctx = SimpleNamespace(node_id="step", run_id="run")
    await mandate_action._mandate_start_body(ctx, MandateStartInput.model_validate(payload), None)


@pytest.mark.asyncio
async def test_a_variable_port_is_refused_before_resolution(resolver_reached):
    with pytest.raises(ValueError, match="outside provision_values") as err:
        await _run({"mandate_key": "podcast.post_prep_translation", "content": "x", "target_language": "fr"})
    assert "['content', 'target_language']" in str(err.value)
    assert "Run Agent" in str(err.value) and "hand_state_to_mandate" in str(err.value)
    assert resolver_reached == []


@pytest.mark.asyncio
async def test_a_variables_dict_is_refused_before_resolution(resolver_reached):
    with pytest.raises(ValueError, match="variables.kind"):
        await _run({"mandate_key": "content_ir.component_artisan", "variables": {"kind": "k"}})
    assert resolver_reached == []


@pytest.mark.asyncio
async def test_state_handed_over_as_provision_values_runs(resolver_reached):
    with pytest.raises(_Reached):
        await _run({"mandate_key": "podcast.post_prep_translation",
                    "provision_values": {"content": "x", "target_language": "fr"},
                    "user_input": "the run's own message is a field, never a variable"})
    assert resolver_reached == ["podcast.post_prep_translation"]


@pytest.mark.asyncio
async def test_a_broadcast_agent_result_is_bookkeeping_not_variables(resolver_reached):
    broadcast = {"final_text": "t", "messages": [], "request_id": "r", "usage": {}, "metadata": {}}
    with pytest.raises(_Reached):
        await _run({"mandate_key": "m", "provision_values": {"a": 1}, **broadcast})
    assert resolver_reached == ["m"]


@pytest.mark.asyncio
async def test_an_entry_steps_echo_of_its_own_state_is_not_fed_by_name(resolver_reached):
    """Defect 75: an entry step also gets the run's input as top-level fields; the same names with
    the same values it hands over as provision_values are its state, not values fed by name."""
    state = {"destination_city": "Mexico City", "move_number": "4471"}
    with pytest.raises(_Reached):
        await _run({"mandate_key": "m", "provision_values": dict(state), **state})
    assert resolver_reached == ["m"]


@pytest.mark.asyncio
async def test_a_top_level_value_that_differs_from_the_state_is_still_refused(resolver_reached):
    with pytest.raises(ValueError, match=r"\['destination_city'\]"):
        await _run({"mandate_key": "m", "provision_values": {"destination_city": "Mexico City"},
                    "destination_city": "Lima"})
    assert resolver_reached == []
