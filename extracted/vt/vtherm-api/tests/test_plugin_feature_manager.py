"""Tests for the VTherm API singleton."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from typing import Any

import pytest
from homeassistant.core import CALLBACK_TYPE, HomeAssistant

from src.vtherm_api.const import DOMAIN
from src.vtherm_api.interfaces import InterfaceFeatureManager, InterfaceThermostat
from src.vtherm_api.vtherm_api import VThermAPI


class OddMinuteFeatureManager(InterfaceFeatureManager):
    """Concrete feature manager used to validate the protocol contract."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the manager state."""
        self._hass = hass
        self._is_configured = False
        self._is_detected = False
        self._listeners: list[CALLBACK_TYPE] = []
        self._restored_state: Any = None

    def post_init(self, entry_infos: dict[str, Any]) -> None:
        """Store the provided configuration."""
        self._is_configured = bool(entry_infos)

    async def start_listening(self, force: bool = False) -> None:
        """No-op listener setup for tests."""

    def stop_listening(self) -> bool:
        """Remove all registered listeners."""
        for listener in list(self._listeners):
            listener()
        self._listeners.clear()
        return True

    async def refresh_state(self) -> bool:
        """Detect only on even minutes."""
        api = VThermAPI.get_vtherm_api(self._hass)
        self._is_detected = bool(api and api.now.minute % 2 == 0)
        return self._is_detected

    def restore_state(self, old_state: Any) -> None:
        """Store the previous state."""
        self._restored_state = old_state

    def add_listener(self, func: CALLBACK_TYPE) -> None:
        """Register a callback for later removal."""
        self._listeners.append(func)

    @property
    def is_configured(self) -> bool:
        """Return whether the manager has been configured."""
        return self._is_configured

    @property
    def is_detected(self) -> bool:
        """Return the current detection state."""
        return self._is_detected

    @property
    def name(self) -> str:
        """Return the logical manager name."""
        return "OddMinuteFeatureManager"

    @property
    def hass(self) -> HomeAssistant:
        """Return the Home Assistant instance."""
        return self._hass


class FakeVTherm(InterfaceThermostat):
    """Minimal thermostat implementation compatible with the VTherm API."""

    def __init__(self) -> None:
        """Initialize the fake thermostat."""
        self.entity_id = "climate.fake_vtherm"
        self._registered_managers: list[InterfaceFeatureManager] = []

    @property
    def name(self) -> str:
        """Return the thermostat name."""
        return "FakeVTherm"

    def register_manager(self, manager: InterfaceFeatureManager) -> None:
        """Store the manager registered by the API."""
        self._registered_managers.append(manager)

    @property
    def unique_id(self) -> str:
        """Return a stable unique ID."""
        return "fake-vtherm"

    @property
    def device_info(self) -> dict[str, str]:
        """Return device info matching the VTherm domain filter."""
        return {"model": DOMAIN}

    @property
    def registered_managers(self) -> list[InterfaceFeatureManager]:
        """Return all managers registered on the fake thermostat."""
        return self._registered_managers


@pytest.mark.asyncio
async def test_register_manager_accepts_concrete_interface_feature_manager() -> None:
    """A concrete feature manager should be instantiable and registerable."""
    VThermAPI.reset_vtherm_api()
    hass = SimpleNamespace(
        data={DOMAIN: {}, "climate": SimpleNamespace(entities=[FakeVTherm()])},
        config=SimpleNamespace(time_zone="UTC"),
    )
    api = VThermAPI.get_vtherm_api(hass)
    fake_vtherm = hass.data["climate"].entities[0]
    manager = OddMinuteFeatureManager(hass)

    manager.post_init({"enabled": True})
    api._set_now(datetime(2024, 1, 1, 12, 2))
    await manager.refresh_state()
    api.register_manager(manager)

    assert isinstance(manager, InterfaceFeatureManager)
    assert isinstance(fake_vtherm, InterfaceThermostat)
    assert manager.is_configured is True
    assert manager.is_detected is True
    assert fake_vtherm.registered_managers == [manager]

    api._set_now(datetime(2024, 1, 1, 12, 3))
    await manager.refresh_state()

    assert manager.is_detected is False

    VThermAPI.reset_vtherm_api()
