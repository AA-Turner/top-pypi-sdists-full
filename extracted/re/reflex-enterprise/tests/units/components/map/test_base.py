"""Tests for the InteractiveLeafletLayer event_handlers prop handling."""

import pytest
import reflex as rx
from reflex.event import EventChain, no_args_event_spec
from reflex.vars.base import Var

import reflex_enterprise as rxe
from reflex_enterprise.components.map.events import mouse_event_spec, popup_event_spec


class MapState(rx.State):
    """State for map event handler tests."""

    @rx.event
    def select(self, id: int):
        """Select a listing.

        Args:
            id: The id of the listing.
        """

    @rx.event
    def other(self):
        """Another handler."""


def _event_handlers_var(component: rx.Component):
    """Return the resolved ``event_handlers`` Var prop (or None) from a component."""
    return component.event_handlers  # pyright: ignore[reportAttributeAccessIssue]


def _event_handlers(component: rx.Component) -> dict:
    """Return the resolved event_handlers mapping (leaflet name -> EventChain)."""
    return _event_handlers_var(component)._var_value


def test_on_event_trigger_translated_to_event_handlers():
    """on_<event> props are moved into the eventHandlers mapping as EventChains."""
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        on_click=MapState.select(5),
    )

    # The on_click trigger should not leak as a standalone event trigger.
    assert "on_click" not in marker.event_triggers

    handlers = _event_handlers(marker)
    assert set(handlers) == {"click"}
    assert isinstance(handlers["click"], EventChain)
    # args_spec is taken from the on_click EventHandler annotation.
    assert handlers["click"].args_spec is mouse_event_spec
    # The chain renders as a JS function leaflet can invoke.
    assert "=>" in str(_event_handlers_var(marker))


def test_event_handlers_raw_handler_is_wrapped():
    """A raw EventType value passed in event_handlers is normalized to an EventChain.

    This is the case from ENG-9662: previously the value rendered as a bare
    event spec instead of a callable function.
    """
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers={"click": MapState.select(5)},
    )

    handlers = _event_handlers(marker)
    assert isinstance(handlers["click"], EventChain)
    assert handlers["click"].args_spec is mouse_event_spec
    rendered = str(_event_handlers_var(marker))
    assert "=>" in rendered
    assert "addEvents" in rendered


def test_event_handlers_explicit_event_chain_is_idempotent():
    """Passing an already-built EventChain is preserved as-is."""
    chain = rx.EventChain.create(
        value=MapState.select(5),
        args_spec=mouse_event_spec,  # pyright: ignore[reportArgumentType]
    )
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers={"click": chain},
    )

    handlers = _event_handlers(marker)
    assert handlers["click"] is chain


def test_event_handlers_list_of_handlers():
    """A list of handlers (EventType) is supported and chained together."""
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers={"click": [MapState.select(5), MapState.other()]},
    )

    handlers = _event_handlers(marker)
    assert isinstance(handlers["click"], EventChain)
    assert len(handlers["click"].events) == 2


def test_event_handlers_merged_with_on_event_trigger():
    """on_<event> props are merged into an explicitly provided event_handlers mapping."""
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        on_dblclick=MapState.other(),
        event_handlers={"click": MapState.select(5)},
    )

    handlers = _event_handlers(marker)
    assert set(handlers) == {"click", "dblclick"}
    assert all(isinstance(chain, EventChain) for chain in handlers.values())


def test_event_handlers_non_aliased_event_uses_mapping_spec():
    """An event without an on_<event> alias still gets its dedicated args_spec."""
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers={"popupopen": MapState.other()},
    )
    chain = _event_handlers(marker)["popupopen"]
    assert isinstance(chain, EventChain)
    assert chain.args_spec is popup_event_spec


def test_event_handlers_non_aliased_event_falls_back_to_no_args():
    """An event with no dedicated spec is still usable with the no-args spec."""
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers={"dragend": MapState.other()},
    )
    chain = _event_handlers(marker)["dragend"]
    assert isinstance(chain, EventChain)
    assert chain.args_spec is no_args_event_spec


def test_event_handlers_duplicate_key_raises():
    """Supplying an event via both on_<event> and event_handlers is an error."""
    with pytest.raises(ValueError, match="set both via"):
        rxe.map.marker(
            position={"lat": 1, "lng": 2},
            on_click=MapState.select(1),
            event_handlers={"click": MapState.select(2)},
        )


def test_event_handlers_invalid_event_name_rejected():
    """An event name outside the supported leaflet set is rejected."""
    with pytest.raises(TypeError):
        rxe.map.marker(
            position={"lat": 1, "lng": 2},
            event_handlers={"not_a_leaflet_event": MapState.other()},
        )


def test_event_handlers_input_not_mutated():
    """The caller's event_handlers dict is not mutated when merging triggers."""
    provided = {"click": MapState.select(5)}
    rxe.map.marker(
        position={"lat": 1, "lng": 2},
        on_dblclick=MapState.other(),
        event_handlers=provided,
    )
    assert set(provided) == {"click"}


def test_no_event_handlers():
    """No handlers means the event_handlers prop is not set."""
    marker = rxe.map.marker(position={"lat": 1, "lng": 2})
    assert _event_handlers_var(marker) is None


def test_event_handlers_var_passthrough():
    """A Var mapping is passed through untouched."""
    handlers_var = Var.create({"click": "noop"}).to(dict)
    marker = rxe.map.marker(
        position={"lat": 1, "lng": 2},
        event_handlers=handlers_var,
    )
    assert _event_handlers_var(marker) is handlers_var


def test_event_handlers_var_with_trigger_raises():
    """Combining a Var event_handlers with an on_<event> trigger is ambiguous."""
    handlers_var = Var.create({"click": "noop"}).to(dict)
    with pytest.raises(ValueError, match="Cannot combine"):
        rxe.map.marker(
            position={"lat": 1, "lng": 2},
            event_handlers=handlers_var,
            on_click=MapState.select(5),
        )


def test_vector_subclass_event_handlers():
    """Vector layers inherit the same event_handlers handling."""
    circle = rxe.map.circle(
        center={"lat": 1, "lng": 2},
        radius=5,
        event_handlers={"click": MapState.select(2)},
    )
    handlers = _event_handlers(circle)
    assert isinstance(handlers["click"], EventChain)
    assert handlers["click"].args_spec is mouse_event_spec
