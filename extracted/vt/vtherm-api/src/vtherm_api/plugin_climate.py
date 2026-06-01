"""Plugin climate entity helpers."""

from collections.abc import Callable
from typing import Any

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import Event, HomeAssistant, Context, ServiceResponse
from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN

from .const import EventType, DOMAIN
from .log_collector import get_vtherm_logger

_LOGGER = get_vtherm_logger(__name__)


class PluginClimate:
    """Simple climate plugin that can be linked to a VTherm instance."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the plugin climate."""
        self._hass: HomeAssistant = hass
        self._linked_vtherm: Any = None
        self._removed_listeners: list[Callable[[], None]] = []
        self._event_data: dict[EventType, dict[str, Any]] = {
            event_type: {} for event_type in EventType
        }
        self._last_event_type: EventType | None = None
        self._handlers: dict[str, Callable[[Event], None]] = {
            EventType.SAFETY_EVENT.value: self.handle_safety_event,
            EventType.POWER_EVENT.value: self.handle_power_event,
            EventType.TEMPERATURE_EVENT.value: self.handle_temperature_event,
            EventType.HVAC_MODE_EVENT.value: self.handle_hvac_mode_event,
            EventType.CENTRAL_BOILER_EVENT.value: self.handle_central_boiler_event,
            EventType.PRESET_EVENT.value: self.handle_preset_event,
            EventType.WINDOW_AUTO_EVENT.value: self.handle_window_auto_event,
            EventType.AUTO_START_STOP_EVENT.value: self.handle_auto_start_stop_event,
            EventType.TIMED_PRESET_EVENT.value: self.handle_timed_preset_event,
            EventType.HEATING_FAILURE_EVENT.value: self.handle_heating_failure_event,
        }

    @property
    def linked_vtherm(self) -> Any:
        """Return the linked VTherm instance."""
        return self._linked_vtherm

    def link_to_vtherm(self, vtherm: Any) -> None:
        """Attach a VTherm instance to this plugin climate."""
        self.remove_listeners()
        self._linked_vtherm = vtherm

        for event_type in EventType:
            self._removed_listeners.append(
                self._hass.bus.async_listen(
                    event_type.value,
                    self._handle_vtherm_event,
                )
            )

    def remove_listeners(self) -> None:
        """Remove all listeners."""
        for remove_listener in self._removed_listeners:
            remove_listener()
        self._removed_listeners.clear()

    def handle_vtherm_event(self, event: Event) -> None:
        """Public entrypoint used by tests and external callers."""
        self._handle_vtherm_event(event)

    def _handle_vtherm_event(self, event: Event) -> None:
        """Handle VTherm events."""
        if not self._is_linked_event(event):
            return

        handler = self._handlers.get(event.event_type)
        if handler is not None:
            self._last_event_type = EventType(event.event_type)
            self._event_data[self._last_event_type] = dict(
                getattr(event, "data", {}) or {})
            handler(event)

    def _is_linked_event(self, event: Event) -> bool:
        """Return True if the event belongs to the linked VTherm entity."""
        if self._linked_vtherm is None:
            return False

        linked_entity_id = getattr(self._linked_vtherm, "entity_id", None)
        if linked_entity_id is None:
            return False

        event_entity_id = self._get_event_entity_id(event)
        return event_entity_id == linked_entity_id

    @staticmethod
    def _get_event_entity_id(event: Event) -> str | None:
        """Extract the VTherm entity_id from an event payload."""
        event_data = getattr(event, "data", None) or {}
        entity_id = event_data.get("entity_id")
        if entity_id is not None:
            return entity_id
        return getattr(event, "entity_id", None)

    def handle_safety_event(self, event: Event) -> None:
        """Handle a safety event."""

    def handle_power_event(self, event: Event) -> None:
        """Handle a power event."""

    def handle_temperature_event(self, event: Event) -> None:
        """Handle a temperature event."""

    def handle_hvac_mode_event(self, event: Event) -> None:
        """Handle an HVAC mode event."""

    def handle_central_boiler_event(self, event: Event) -> None:
        """Handle a central boiler event."""

    def handle_preset_event(self, event: Event) -> None:
        """Handle a preset event."""

    def handle_window_auto_event(self, event: Event) -> None:
        """Handle a window auto event."""

    def handle_auto_start_stop_event(self, event: Event) -> None:
        """Handle an auto start/stop event."""

    def handle_timed_preset_event(self, event: Event) -> None:
        """Handle a timed preset event."""

    def handle_heating_failure_event(self, event: Event) -> None:
        """Handle a heating failure event."""

    @property
    def last_event_type(self) -> EventType | None:
        """Return the latest handled event type."""
        return self._last_event_type

    def get_event_data(self, event_type: EventType) -> dict[str, Any]:
        """Return the latest payload stored for an event type."""
        return dict(self._event_data[event_type])

    async def call_linked_vtherm_action(self, action_name: str, action_data: dict[str, Any] | None = None, blocking: bool = False, context: Context | None = None, return_response: bool = False) -> Any:
        """Call an action method on the linked VTherm entity.

        The method supports both sync and async action implementations.
        """
        if self._linked_vtherm is None:
            raise RuntimeError("No linked VTherm configured")

        try:
            target = {ATTR_ENTITY_ID: self._linked_vtherm.entity_id}
            response: ServiceResponse = await self._hass.services.async_call(CLIMATE_DOMAIN, action_name, action_data, blocking, context, target, return_response)
            return response
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error(
                "%s - Error calling service %s.%s: %s. The underlying will not change its state.", self, CLIMATE_DOMAIN, action_name, err)
