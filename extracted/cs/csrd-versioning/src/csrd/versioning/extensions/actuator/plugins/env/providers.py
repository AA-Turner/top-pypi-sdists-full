"""Property source providers for the env actuator."""

import os
import platform
import sys
from typing import Any, Protocol


class PropertySourceProvider(Protocol):
    """Contract for objects that provide property sources.

    Property sources are aggregated by the EnvActuatorPlugin and exposed
    via the /actuator/env and /actuator/env/{toMatch} endpoints.
    """

    def get_sources(self, to_match: str | None = None) -> list[dict[str, Any]]:
        """Return property sources, optionally filtered by to_match key.

        Args:
            to_match: Optional case-insensitive substring to filter property keys.
                      If provided, only properties with matching keys are returned.

        Returns:
            List of property source dicts with 'name' and 'properties' keys.
            Empty list if no sources match the filter.
        """


class SystemEnvironmentProvider:
    """Expose OS environment variables as a property source."""

    def get_sources(self, to_match: str | None = None) -> list[dict[str, Any]]:
        """Return environment variables, optionally filtered by key."""
        if not to_match:
            # Return all env vars with Spring-style {"value": ...} wrapper
            properties = {key: {"value": value} for key, value in os.environ.items()}
            return [{"name": "systemEnvironment", "properties": properties}]

        # Filter by to_match
        needle = to_match.strip().lower()
        matched = {
            key: {"value": value} for key, value in os.environ.items() if needle in key.lower()
        }

        if not matched:
            return []

        return [{"name": "systemEnvironment", "properties": matched}]


class SystemPropertiesProvider:
    """Expose system information as a property source."""

    def get_sources(self, to_match: str | None = None) -> list[dict[str, Any]]:
        """Return system properties (Python version, platform, etc)."""
        raw = {
            "python.version": sys.version,
            "python.implementation": sys.implementation.name,
            "platform.system": platform.system(),
            "platform.release": platform.release(),
            "platform.machine": platform.machine(),
            "os.name": os.name,
            "process.pid": str(os.getpid()),
        }

        if not to_match:
            properties = {k: {"value": v} for k, v in raw.items()}
            return [{"name": "systemProperties", "properties": properties}]

        # Filter by to_match
        needle = to_match.strip().lower()
        matched = {k: {"value": v} for k, v in raw.items() if needle in k.lower()}

        if not matched:
            return []

        return [{"name": "systemProperties", "properties": matched}]


class DockerConfigProvider:
    """Expose Docker environment variables as a property source."""

    def get_sources(self, to_match: str | None = None) -> list[dict[str, Any]]:
        """Return Docker-related environment variables."""
        docker_vars = {
            key: value
            for key, value in os.environ.items()
            if key.startswith(("DOCKER_", "CONTAINER_"))
        }

        if not docker_vars:
            return []

        if not to_match:
            properties = {k: {"value": v} for k, v in docker_vars.items()}
            return [{"name": "dockerConfig", "properties": properties}]

        # Filter by to_match
        needle = to_match.strip().lower()
        matched = {k: {"value": v} for k, v in docker_vars.items() if needle in k.lower()}

        if not matched:
            return []

        return [{"name": "dockerConfig", "properties": matched}]
