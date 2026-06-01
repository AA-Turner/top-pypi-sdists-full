"""Tests for the proportional algorithm registry exposed by VThermAPI."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.vtherm_api.const import DOMAIN
from src.vtherm_api.interfaces import (
    InterfaceCycleScheduler,
    InterfacePropAlgorithmFactory,
    InterfacePropAlgorithmHandler,
    InterfaceThermostatRuntime,
)
from src.vtherm_api.vtherm_api import VThermAPI


class FakePropAlgorithmHandler(InterfacePropAlgorithmHandler):
    """Minimal handler used to validate the registry contract."""

    def init_algorithm(self) -> None:
        """Initialize the handler."""

    async def async_added_to_hass(self) -> None:
        """Run startup hooks when the thermostat is added."""

    async def async_startup(self) -> None:
        """Run startup hooks after thermostat initialization."""

    def remove(self) -> None:
        """Release handler resources."""

    async def control_heating(self, timestamp=None, force: bool = False) -> None:
        """Run one control iteration."""

    async def on_state_changed(self, changed: bool) -> None:
        """React to a thermostat state change."""
        del changed

    def on_scheduler_ready(self, scheduler: InterfaceCycleScheduler) -> None:
        """Bind the handler to the scheduler."""

    def should_publish_intermediate(self) -> bool:
        """Allow VT to publish intermediate states."""
        return True


class FakePropAlgorithmFactory(InterfacePropAlgorithmFactory):
    """Minimal factory used to validate the registry contract."""

    def __init__(self, name: str) -> None:
        """Store the factory name."""
        self._name = name

    @property
    def name(self) -> str:
        """Return the factory name."""
        return self._name

    def create(
        self,
        thermostat: InterfaceThermostatRuntime,
    ) -> InterfacePropAlgorithmHandler:
        """Create a fake handler for the provided thermostat."""
        del thermostat
        return FakePropAlgorithmHandler()


def _build_hass() -> SimpleNamespace:
    """Create a minimal Home Assistant-like object for VThermAPI tests."""
    return SimpleNamespace(
        data={DOMAIN: {}},
        config=SimpleNamespace(time_zone="UTC"),
    )


def test_prop_algorithm_registry_lifecycle() -> None:
    """The registry should support register, get, list, and unregister."""
    VThermAPI.reset_vtherm_api()
    hass = _build_hass()
    api = VThermAPI.get_vtherm_api(hass)

    alpha_factory = FakePropAlgorithmFactory("alpha")
    smart_pi_factory = FakePropAlgorithmFactory("smart_pi")
    zeta_factory = FakePropAlgorithmFactory("zeta")

    api.register_prop_algorithm(smart_pi_factory)
    api.register_prop_algorithm(zeta_factory)
    api.register_prop_algorithm(alpha_factory)

    assert api.get_prop_algorithm("smart_pi") is smart_pi_factory
    assert api.list_prop_algorithms() == ["alpha", "smart_pi", "zeta"]

    api.unregister_prop_algorithm("smart_pi")

    assert api.get_prop_algorithm("smart_pi") is None
    assert api.list_prop_algorithms() == ["alpha", "zeta"]

    VThermAPI.reset_vtherm_api()


def test_register_prop_algorithm_rejects_empty_names() -> None:
    """An empty factory name should be rejected."""
    VThermAPI.reset_vtherm_api()
    hass = _build_hass()
    api = VThermAPI.get_vtherm_api(hass)

    with pytest.raises(ValueError):
        api.register_prop_algorithm(FakePropAlgorithmFactory("   "))

    VThermAPI.reset_vtherm_api()


def test_reset_vtherm_api_recreates_an_empty_registry() -> None:
    """Resetting the API should drop the current registry content."""
    VThermAPI.reset_vtherm_api()
    hass = _build_hass()
    api = VThermAPI.get_vtherm_api(hass)
    api.register_prop_algorithm(FakePropAlgorithmFactory("smart_pi"))

    VThermAPI.reset_vtherm_api()

    recreated_api = VThermAPI.get_vtherm_api(hass)

    assert recreated_api is not api
    assert recreated_api.list_prop_algorithms() == []
