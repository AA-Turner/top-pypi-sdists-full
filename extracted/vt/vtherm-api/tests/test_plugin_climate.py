"""Tests for the PluginClimate helper."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.components.climate.const import DOMAIN as CLIMATE_DOMAIN

from src.vtherm_api.const import EventType
from src.vtherm_api.plugin_climate import PluginClimate


class FakeEventBus:
    """Minimal event bus for PluginClimate tests."""

    def __init__(self) -> None:
        """Initialize listeners storage."""
        self._listeners: dict[str, list] = {}

    def async_listen(self, event_type: str, callback):
        """Register a callback for an event type."""
        listeners = self._listeners.setdefault(event_type, [])
        listeners.append(callback)

        def _remove_listener() -> None:
            listeners.remove(callback)

        return _remove_listener

    def fire(self, event_type: str, data: dict[str, str]) -> None:
        """Emit an event to all registered listeners."""
        event = SimpleNamespace(event_type=event_type, data=data)
        for callback in list(self._listeners.get(event_type, [])):
            callback(event)


class RecordingPluginClimate(PluginClimate):
    """PluginClimate variant that records handler invocations."""

    def __init__(self, hass) -> None:
        """Initialize the recorder."""
        super().__init__(hass)
        self.called_handlers: list[tuple[EventType, dict[str, str]]] = []

    def _record(self, event_type: EventType, event) -> None:
        """Store a handler invocation for later assertions."""
        self.called_handlers.append((event_type, dict(event.data)))

    def handle_safety_event(self, event) -> None:
        self._record(EventType.SAFETY_EVENT, event)

    def handle_power_event(self, event) -> None:
        self._record(EventType.POWER_EVENT, event)

    def handle_temperature_event(self, event) -> None:
        self._record(EventType.TEMPERATURE_EVENT, event)

    def handle_hvac_mode_event(self, event) -> None:
        self._record(EventType.HVAC_MODE_EVENT, event)

    def handle_central_boiler_event(self, event) -> None:
        self._record(EventType.CENTRAL_BOILER_EVENT, event)

    def handle_preset_event(self, event) -> None:
        self._record(EventType.PRESET_EVENT, event)

    def handle_window_auto_event(self, event) -> None:
        self._record(EventType.WINDOW_AUTO_EVENT, event)

    def handle_auto_start_stop_event(self, event) -> None:
        self._record(EventType.AUTO_START_STOP_EVENT, event)

    def handle_timed_preset_event(self, event) -> None:
        self._record(EventType.TIMED_PRESET_EVENT, event)

    def handle_heating_failure_event(self, event) -> None:
        self._record(EventType.HEATING_FAILURE_EVENT, event)


def test_link_to_vtherm_stores_reference_and_registers_listeners() -> None:
    """The plugin climate should keep a reference and subscribe to events."""
    hass = MagicMock()
    remove_listener = MagicMock()
    hass.bus.async_listen.return_value = remove_listener
    plugin_climate = PluginClimate(hass)
    vtherm = SimpleNamespace(entity_id="climate.salon")

    plugin_climate.link_to_vtherm(vtherm)

    assert plugin_climate.linked_vtherm is vtherm
    assert hass.bus.async_listen.call_count == len(EventType)


@pytest.mark.parametrize("event_type", list(EventType))
def test_handle_event_updates_payload_for_supported_event_types(event_type: EventType) -> None:
    """Each supported VTherm event should be stored by its dedicated handler."""
    hass = MagicMock()
    hass.bus.async_listen.return_value = MagicMock()
    plugin_climate = PluginClimate(hass)
    plugin_climate.link_to_vtherm(SimpleNamespace(entity_id="climate.salon"))

    payload = {"entity_id": "climate.salon", "value": event_type.value}
    event = SimpleNamespace(event_type=event_type.value, data=payload)

    plugin_climate.handle_vtherm_event(event)

    assert plugin_climate.last_event_type == event_type
    assert plugin_climate.get_event_data(event_type) == payload


def test_handle_event_ignores_other_entities() -> None:
    """Events for another VTherm entity must be ignored."""
    hass = MagicMock()
    hass.bus.async_listen.return_value = MagicMock()
    plugin_climate = PluginClimate(hass)
    plugin_climate.link_to_vtherm(SimpleNamespace(entity_id="climate.salon"))

    payload = {"entity_id": "climate.bureau", "value": "ignored"}
    event = SimpleNamespace(
        event_type=EventType.SAFETY_EVENT.value, data=payload)

    plugin_climate.handle_vtherm_event(event)

    assert plugin_climate.last_event_type is None
    assert not plugin_climate.get_event_data(EventType.SAFETY_EVENT)


def test_bus_events_call_the_matching_handlers() -> None:
    """Events fired on the bus should invoke the dedicated handlers."""
    hass = SimpleNamespace(bus=FakeEventBus())
    plugin_climate = RecordingPluginClimate(hass)
    plugin_climate.link_to_vtherm(SimpleNamespace(entity_id="climate.salon"))

    expected_payloads: dict[EventType, dict[str, str]] = {}
    for event_type in EventType:
        payload = {"entity_id": "climate.salon", "value": event_type.value}
        expected_payloads[event_type] = payload
        hass.bus.fire(event_type.value, payload)

    assert plugin_climate.called_handlers == [
        (event_type, expected_payloads[event_type]) for event_type in EventType
    ]


@pytest.mark.parametrize(
    ("action_name", "action_data"),
    [
        ("set_hvac_mode", {"hvac_mode": "heat"}),
        ("set_preset_mode", {"preset_mode": "eco"}),
        ("set_target_temperature", {"temperature": 19.5}),
    ],
)
@pytest.mark.asyncio
async def test_call_linked_vtherm_action_calls_requested_action(
    action_name: str, action_data: dict[str, str | float]
) -> None:
    """The requested action should be relayed to the linked VTherm."""
    hass = MagicMock()
    hass.services.async_call = AsyncMock(return_value="ok")
    plugin_climate = PluginClimate(hass)
    plugin_climate.link_to_vtherm(SimpleNamespace(entity_id="climate.salon"))

    result = await plugin_climate.call_linked_vtherm_action(
        action_name, action_data=action_data
    )

    hass.services.async_call.assert_awaited_once_with(
        CLIMATE_DOMAIN,
        action_name,
        action_data,
        False,
        None,
        {ATTR_ENTITY_ID: "climate.salon"},
        False,
    )
    assert result == "ok"


@pytest.mark.asyncio
async def test_call_linked_vtherm_action_passes_optional_arguments() -> None:
    """Optional arguments should be forwarded to the HA service call."""
    hass = MagicMock()
    hass.services.async_call = AsyncMock(return_value="async-ok")
    plugin_climate = PluginClimate(hass)
    plugin_climate.link_to_vtherm(SimpleNamespace(entity_id="climate.salon"))

    context = object()
    action_data = {"hvac_mode": "heat"}

    result = await plugin_climate.call_linked_vtherm_action(
        "set_hvac_mode",
        action_data=action_data,
        blocking=True,
        context=context,
        return_response=True,
    )

    hass.services.async_call.assert_awaited_once_with(
        CLIMATE_DOMAIN,
        "set_hvac_mode",
        action_data,
        True,
        context,
        {ATTR_ENTITY_ID: "climate.salon"},
        True,
    )
    assert result == "async-ok"
