# custom_components/versatile_thermostat/thermostat_interface.py
from __future__ import annotations
from collections.abc import Callable
from typing import Any
from datetime import datetime

from typing import Protocol, runtime_checkable
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import HomeAssistant, CALLBACK_TYPE

from .commons_type import ConfigData


@runtime_checkable
class InterfaceThermostat(Protocol):
    """Contrat minimal commun pour manipuler un thermostat VTherm."""

    @property
    def name(self) -> str:
        """Get the name of the thermostat."""
        ...

    def register_manager(self, manager: InterfaceFeatureManager):
        """Register a feature manager to the thermostat."""
        ...

    @property
    def unique_id(self) -> str:
        """Get the unique ID of the thermostat."""
        ...

    @property
    def device_info(self) -> DeviceInfo | None:
        """Get the device information."""
        ...


@runtime_checkable
class InterfaceFeatureManager(Protocol):
    """Contrat commun pour tous les FeatureManagers."""

    def post_init(self, entry_infos: ConfigData | dict[str, Any]) -> None:
        """Initialise le manager avec la configuration fusionnée."""
        ...

    async def start_listening(self, force: bool = False) -> None:
        """Abonne le manager aux événements nécessaires."""
        ...

    def stop_listening(self) -> bool | None:
        """Désabonne les listeners du manager."""
        ...

    async def refresh_state(self) -> bool:
        """Rafraîchit l'état interne et retourne True si changement."""
        ...

    def restore_state(self, old_state: Any) -> None:
        """Restaure l'état du manager depuis un ancien state HA."""
        ...

    def add_listener(self, func: CALLBACK_TYPE) -> None:
        """Ajoute un callback à désinscrire au stop."""
        ...

    @property
    def is_configured(self) -> bool:
        """Le manager est-il correctement configuré ?"""
        ...

    @property
    def is_detected(self) -> bool:
        """Le manager détecte-t-il actuellement sa condition ?"""
        ...

    @property
    def name(self) -> str:
        """Nom logique du manager."""
        ...

    @property
    def hass(self) -> HomeAssistant:
        """Instance Home Assistant."""
        ...


@runtime_checkable
class InterfaceThermostatRuntime(Protocol):
    """Runtime view of a VTherm exposed to a proportional algorithm plugin."""

    prop_algorithm: Any
    minimal_activation_delay: int
    minimal_deactivation_delay: int

    @property
    def hass(self) -> HomeAssistant:
        """Return the Home Assistant instance."""
        ...

    @property
    def entity_id(self) -> str:
        """Return the Home Assistant entity identifier."""
        ...

    @property
    def name(self) -> str:
        """Return the thermostat name."""
        ...

    @property
    def unique_id(self) -> str:
        """Return the thermostat unique identifier."""
        ...

    @property
    def entry_infos(self) -> ConfigData | dict[str, Any]:
        """Return the merged thermostat configuration."""
        ...

    @property
    def current_temperature(self) -> float | None:
        """Return the current room temperature."""
        ...

    @property
    def current_outdoor_temperature(self) -> float | None:
        """Return the current outdoor temperature."""
        ...

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        ...

    @property
    def last_temperature_slope(self) -> float | None:
        """Return the latest computed temperature slope."""
        ...

    @property
    def vtherm_hvac_mode(self) -> str | None:
        """Return the VTherm HVAC mode."""
        ...

    @property
    def hvac_action(self) -> str | None:
        """Return the current HVAC action."""
        ...

    @property
    def hvac_off_reason(self) -> str | None:
        """Return the current HVAC off reason."""
        ...

    @property
    def cycle_min(self) -> int:
        """Return the cycle duration in minutes."""
        ...

    @property
    def cycle_scheduler(self) -> "InterfaceCycleScheduler | None":
        """Return the cycle scheduler when available."""
        ...

    @property
    def is_device_active(self) -> bool:
        """Return True when at least one underlying device is active."""
        ...

    @property
    def is_overpowering_detected(self) -> bool:
        """Return True when power shedding is currently active."""
        ...

    async def async_underlying_entity_turn_off(self) -> None:
        """Turn off the underlying entities."""
        ...

    async def async_control_heating(
        self,
        timestamp: datetime | None = None,
        force: bool = False,
    ) -> bool:
        """Run the thermostat control loop."""
        ...

    def update_custom_attributes(self) -> None:
        """Refresh the thermostat state attributes."""
        ...

    def async_write_ha_state(self) -> None:
        """Publish the thermostat state to Home Assistant."""
        ...


@runtime_checkable
class InterfaceCycleScheduler(Protocol):
    """Contract exposed by the VTherm cycle scheduler."""

    @property
    def is_cycle_running(self) -> bool:
        """Return True when a cycle is active or transitioning."""
        ...

    def register_cycle_start_callback(self, callback: Callable[..., Any]) -> None:
        """Register a callback fired at the start of each cycle."""
        ...

    def register_cycle_end_callback(self, callback: Callable[..., Any]) -> None:
        """Register a callback fired at the end of each cycle."""
        ...

    async def start_cycle(
        self,
        hvac_mode: Any,
        on_percent: float,
        force: bool = False,
    ) -> None:
        """Start or update a cycle."""
        ...

    async def cancel_cycle(self) -> None:
        """Cancel the current cycle."""
        ...


@runtime_checkable
class InterfacePropAlgorithmHandler(Protocol):
    """Lifecycle contract implemented by an external proportional algorithm handler."""

    def init_algorithm(self) -> None:
        """Initialize the runtime algorithm state."""
        ...

    async def async_added_to_hass(self) -> None:
        """Run startup actions when the thermostat entity is added."""
        ...

    async def async_startup(self) -> None:
        """Run startup actions after thermostat initialization."""
        ...

    def remove(self) -> None:
        """Release resources held by the handler."""
        ...

    async def control_heating(
        self,
        timestamp: datetime | None = None,
        force: bool = False,
    ) -> None:
        """Execute one proportional control iteration."""
        ...

    async def on_state_changed(self, changed: bool) -> None:
        """React to a thermostat state change."""
        ...

    def on_scheduler_ready(self, scheduler: InterfaceCycleScheduler) -> None:
        """Bind the handler to the cycle scheduler."""
        ...

    def should_publish_intermediate(self) -> bool:
        """Return True when VT may publish intermediate thermostat states."""
        ...


@runtime_checkable
class InterfacePropAlgorithmFactory(Protocol):
    """Factory used by external integrations to register a proportional algorithm."""

    @property
    def name(self) -> str:
        """Return the proportional algorithm identifier."""
        ...

    def create(
        self,
        thermostat: InterfaceThermostatRuntime,
    ) -> InterfacePropAlgorithmHandler:
        """Create a proportional algorithm handler bound to the runtime thermostat."""
        ...
