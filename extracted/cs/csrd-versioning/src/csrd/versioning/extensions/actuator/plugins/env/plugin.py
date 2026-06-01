"""Spring Boot-style env actuator plugin."""

import os
from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, FastAPI

from ..base import ActuatorLink, BaseActuatorPlugin
from .registry import (
    PropertySourceRegistry,
    SanitizationConfig,
    create_property_source_registry,
)


def _active_profiles() -> list[str]:
    """Parse SPRING_PROFILES_ACTIVE environment variable."""
    return [
        profile.strip()
        for profile in os.environ.get("SPRING_PROFILES_ACTIVE", "").split(",")
        if profile.strip()
    ]


def _default_profiles() -> list[str]:
    """Parse SPRING_PROFILES_DEFAULT environment variable, defaulting to 'default'."""
    return [
        profile.strip()
        for profile in os.environ.get("SPRING_PROFILES_DEFAULT", "default").split(",")
        if profile.strip()
    ]


class EnvActuatorPlugin(BaseActuatorPlugin):
    """Expose Spring-style ``/actuator/env`` runtime environment metadata.

    The plugin aggregates property sources (environment variables, system info,
    Docker config) and exposes them via the /env and /env/{toMatch} endpoints.
    """

    name = "env"

    def __init__(
        self,
        registry: PropertySourceRegistry | None = None,
        *,
        sanitization: SanitizationConfig | None = None,
    ) -> None:
        """Initialize the env plugin.

        Args:
            registry: PropertySourceRegistry for aggregating property sources.
                     If None, creates a default registry with built-in providers.
            sanitization: Redaction configuration passed to the default registry.
                         Ignored when ``registry`` is provided explicitly.

        Note:
            Runtime environment values may change during process lifetime,
            so caching is disabled (cache_enabled=False).
        """
        super().__init__(cache_enabled=False)
        self.registry = registry or create_property_source_registry(
            sanitization=sanitization,
        )

    @classmethod
    def with_providers(
        cls,
        *,
        sanitization: SanitizationConfig | None = None,
        **providers: Any,
    ) -> "EnvActuatorPlugin":
        """Create an EnvActuatorPlugin with custom property source providers.

        Args:
            sanitization: Redaction configuration for the registry.
            **providers: Named property source providers to register.
                        Each keyword argument becomes a provider name.

        Returns:
            A new EnvActuatorPlugin instance with the providers registered.

        Example:
            >>> plugin = EnvActuatorPlugin.with_providers(
            ...     sanitization=SanitizationConfig(show_values=ShowValues.ALWAYS),
            ...     database=DatabasePropertiesProvider(),
            ...     features=FeatureFlagsProvider(),
            ... )
        """
        plugin = cls(sanitization=sanitization)
        plugin.register_property_source_providers(providers)
        return plugin

    def register_property_source_providers(
        self,
        providers: Mapping[str, Any],
    ) -> None:
        """Register or override property source providers in the plugin registry."""
        for name, provider in providers.items():
            self.registry.register(name, provider)

    def register(
        self,
        router: APIRouter,
        *,
        app: FastAPI,
        prefix: str,
    ) -> Mapping[str, ActuatorLink]:
        """Register env endpoints on the router.

        Args:
            router: APIRouter to register endpoints on.
            app: FastAPI application instance.
            prefix: URL prefix for actuator endpoints (e.g., '/actuator').

        Returns:
            Mapping of link names to ActuatorLink objects for the root endpoint.
        """

        @router.get("/env", include_in_schema=False)
        async def env() -> dict[str, Any]:
            """List all property sources and active profiles."""
            return {
                "activeProfiles": _active_profiles(),
                "defaultProfiles": _default_profiles(),
                "propertySources": self.registry.get_all_sources(),
            }

        @router.get("/env/{toMatch}", include_in_schema=False)
        async def env_to_match(toMatch: str) -> dict[str, Any]:
            """List property sources filtered by key, and active profiles."""
            return {
                "activeProfiles": _active_profiles(),
                "defaultProfiles": _default_profiles(),
                "propertySources": self.registry.get_all_sources(to_match=toMatch),
            }

        return {
            "env": self.build_link(prefix=prefix, route_path="/env"),
            "env-toMatch": ActuatorLink(
                href=f"{prefix}/env/{{toMatch}}",
                templated=True,
            ),
        }
