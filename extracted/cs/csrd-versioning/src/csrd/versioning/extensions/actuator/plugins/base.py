from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from fastapi import APIRouter, FastAPI


@dataclass(frozen=True)
class ActuatorLink:
    """Link metadata rendered by the actuator root endpoint."""

    href: str
    templated: bool = False


class ActuatorPlugin(Protocol):
    """Contract for actuator plugins that register routes and expose links."""

    name: str

    def register(
        self,
        router: APIRouter,
        *,
        app: FastAPI,
        prefix: str,
    ) -> Mapping[str, ActuatorLink]:
        """Register endpoints on *router* and return link entries."""


class BaseActuatorPlugin:
    """Shared helpers for actuator plugins.

    Provides optional in-memory memoization of endpoint payloads and a
    consistent link-construction helper.
    """

    def __init__(self, *, cache_enabled: bool = True) -> None:
        self._cache_enabled = cache_enabled
        self._payload_cache: dict[str, dict[str, Any]] = {}
        self._property_source_providers: dict[str, Any] = {}

    def memoized_payload(
        self,
        *,
        cache_key: str,
        loader: Callable[[], dict[str, Any]],
    ) -> dict[str, Any]:
        if not self._cache_enabled:
            return loader()

        cached = self._payload_cache.get(cache_key)
        if cached is not None:
            return cached

        payload = loader()
        self._payload_cache[cache_key] = payload
        return payload

    def clear_payload_cache(self) -> None:
        self._payload_cache.clear()

    def register_property_source_provider(self, *, name: str, provider: Any) -> None:
        """Register a property source provider contribution from this plugin.

        Contributions are auto-wired into the env actuator plugin when
        ``register_actuator_router`` resolves the plugin set.
        """
        self._property_source_providers[name] = provider

    def property_source_providers(self) -> Mapping[str, Any]:
        """Return this plugin's property source provider contributions."""
        return dict(self._property_source_providers)

    @staticmethod
    def build_link(*, prefix: str, route_path: str) -> ActuatorLink:
        return ActuatorLink(href=f"{prefix}{route_path}")
