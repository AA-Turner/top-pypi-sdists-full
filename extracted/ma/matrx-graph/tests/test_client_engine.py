"""The ``client`` engine — a client Action runs in the person's browser; on the server the ONE
router answers the typed hand-off ``ActionOnClient`` (never 501 / engine_not_registered), and
every client Action is in the catalog with a typed input agents can read.

Fails if the client runner is removed, if a client Action's input stops being validated, or if
a kind action key the client runs is missing from the server catalog.
"""

from __future__ import annotations

import asyncio

import pytest
from pydantic import ValidationError

from matrx_graph.actions import ActionOnClient, dump_result, registered_engines, restore_result, run_action
from matrx_graph.actions.client import CLIENT_ACTION_INPUTS, client_action_name, declare_client_actions
from matrx_graph.actions.registry import ActionRegistry


class _App:
    user_id = "u-1"
    organization_id = "o-1"
    is_admin = False


def test_the_client_engine_has_a_runner():
    assert "client" in registered_engines()


def test_a_client_action_answers_run_it_on_the_client():
    registry = ActionRegistry()
    specs = declare_client_actions(action_registry=registry)
    assert {s.name for s in specs} == {client_action_name(k) for k in CLIENT_ACTION_INPUTS}
    assert all(s.engine == "client" for s in specs)
    out = asyncio.run(
        run_action("kind.copy", {"text": "hi"}, app=_App(), door="api", registry=registry)
    )
    assert isinstance(out, ActionOnClient)
    assert out.action == "kind.copy" and out.input == {"text": "hi"}
    spec = registry.get("kind.copy")
    stored = dump_result(spec, out)
    assert stored == {"status": "client", "action": "kind.copy", "input": {"text": "hi"}}
    assert isinstance(restore_result(spec, stored), ActionOnClient)


def test_a_client_action_input_is_typed():
    registry = ActionRegistry()
    declare_client_actions(action_registry=registry)
    with pytest.raises(ValidationError):
        asyncio.run(run_action("kind.open_url", {}, app=_App(), door="api", registry=registry))
    # Declaring twice is a no-op (idempotent host wiring).
    assert len(declare_client_actions(action_registry=registry)) == len(CLIENT_ACTION_INPUTS)


def test_open_place_is_a_typed_client_action():
    """PF-L4.6: `kind.open_place` opens a place in the app by its NAME (a surface or an in-app path) — the
    same navigation a page's `link` item and an HTML page's `matrx.open` make. Agents see it typed."""
    registry = ActionRegistry()
    declare_client_actions(action_registry=registry)
    out = asyncio.run(
        run_action(
            "kind.open_place",
            {"to": "crm/contact", "params": {"contactId": "c-1"}},
            app=_App(),
            door="api",
            registry=registry,
        )
    )
    assert isinstance(out, ActionOnClient)
    assert out.input == {"to": "crm/contact", "params": {"contactId": "c-1"}}
    # A table's records place takes an object `filter` and a `label` (what matrx.open takes), delivered untouched.
    ask = {"to": "data/tables", "params": {"tableId": "t-1", "filter": {"status": "Booked"}, "label": "Still booked"}}
    out = asyncio.run(run_action("kind.open_place", ask, app=_App(), door="api", registry=registry))
    assert isinstance(out, ActionOnClient)
    assert out.input == ask
    with pytest.raises(ValidationError):
        asyncio.run(run_action("kind.open_place", {"to": ""}, app=_App(), door="api", registry=registry))
    with pytest.raises(ValidationError):
        asyncio.run(run_action("kind.open_place", {"url": "https://x"}, app=_App(), door="api", registry=registry))


def test_open_record_is_a_typed_client_action():
    """P5-ACTIONS: `kind.open_record` opens the card's OWN record; input is only an optional mode, listed by GET /actions."""
    registry = ActionRegistry()
    declare_client_actions(action_registry=registry)
    assert registry.has("kind.open_record")
    for ask in ({}, {"mode": "page"}, {"mode": "panel"}):
        out = asyncio.run(run_action("kind.open_record", ask, app=_App(), door="api", registry=registry))
        assert isinstance(out, ActionOnClient)
        assert out.action == "kind.open_record" and out.input.get("mode") == ask.get("mode")
    with pytest.raises(ValidationError):
        asyncio.run(run_action("kind.open_record", {"mode": "tab"}, app=_App(), door="api", registry=registry))
    with pytest.raises(ValidationError):
        asyncio.run(run_action("kind.open_record", {"table_id": "t"}, app=_App(), door="api", registry=registry))
