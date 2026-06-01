"""Spring Boot-style health actuator plugin."""

import inspect
import logging
from collections.abc import Mapping
from enum import Enum
from typing import Any

from fastapi import APIRouter, FastAPI

from ..base import ActuatorLink, BaseActuatorPlugin
from .auto import discover_indicators
from .indicators import (
    DiskSpaceHealthIndicator,
    HealthIndicator,
    LivenessIndicator,
    PingHealthIndicator,
    ReadinessIndicator,
)

logger = logging.getLogger(__name__)

# Spring Boot status precedence (worst first).
_STATUS_PRIORITY = ("DOWN", "OUT_OF_SERVICE", "UNKNOWN", "UP")


class Status(Enum):
    """Application health status, matching Spring Boot's ``Status`` enum."""

    UP = "UP"
    DOWN = "DOWN"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    UNKNOWN = "UNKNOWN"


class ShowDetails(Enum):
    """Controls visibility of component details in health responses.

    Mirrors Spring Boot's ``management.endpoint.health.show-details``.

    Members:
        NEVER: Only return top-level ``{"status": ...}``.
        ALWAYS: Include ``components`` with per-indicator status and details.
        WHEN_AUTHORIZED: Reserved; currently behaves like NEVER.
    """

    NEVER = "NEVER"
    ALWAYS = "ALWAYS"
    WHEN_AUTHORIZED = "WHEN_AUTHORIZED"


def _aggregate_status(statuses: list[str]) -> str:
    """Return the worst status from a list, using Spring Boot precedence."""
    for candidate in _STATUS_PRIORITY:
        if candidate in statuses:
            return candidate
    return "UNKNOWN"


class HealthActuatorPlugin(BaseActuatorPlugin):
    """Expose Spring-style ``/actuator/health`` with composable indicators.

    Built-in indicators (``ping``, ``diskSpace``) are registered by default.
    Custom indicators can be added via ``with_indicators()`` or by passing
    an ``indicators`` dict to the constructor.

    Health groups (e.g. ``liveness``, ``readiness``) aggregate named subsets
    of indicators and are exposed as ``/actuator/health/{group}`` endpoints.

    When ``auto_discover`` is ``True`` (the default), ``app.state`` is
    inspected on each health request and indicators are added automatically
    for detected service connections (RabbitMQ, Kafka, MongoDB,
    LaunchDarkly).  Auto-discovered services are also appended to the
    ``readiness`` group when one exists.
    """

    name = "health"

    def __init__(
        self,
        indicators: dict[str, HealthIndicator] | None = None,
        *,
        show_details: ShowDetails = ShowDetails.ALWAYS,
        with_defaults: bool = True,
        groups: dict[str, list[str]] | None = None,
        auto_discover: bool = True,
    ) -> None:
        super().__init__(cache_enabled=False)
        self._indicators: dict[str, HealthIndicator] = {}
        self._show_details = show_details
        self._groups: dict[str, list[str]] = groups or {}
        self._auto_discover = auto_discover
        self._app: FastAPI | None = None

        if with_defaults:
            self._indicators["ping"] = PingHealthIndicator()
            self._indicators["diskSpace"] = DiskSpaceHealthIndicator()
            self._indicators["livenessState"] = LivenessIndicator()
            self._indicators["readinessState"] = ReadinessIndicator()
            if not self._groups:
                self._groups = {
                    "liveness": ["livenessState"],
                    "readiness": ["readinessState", "ping", "diskSpace"],
                }

        if indicators:
            self._indicators.update(indicators)

    @classmethod
    def with_indicators(
        cls,
        *,
        show_details: ShowDetails = ShowDetails.ALWAYS,
        with_defaults: bool = True,
        groups: dict[str, list[str]] | None = None,
        auto_discover: bool = True,
        **indicators: HealthIndicator,
    ) -> "HealthActuatorPlugin":
        """Create a HealthActuatorPlugin with custom indicators.

        Args:
            show_details: Controls component detail visibility.
            with_defaults: Include built-in indicators (ping, diskSpace).
            groups: Named subsets of indicator keys.  Each group becomes a
                ``/actuator/health/{group}`` endpoint that aggregates only
                the listed indicators.  Example::

                    groups={
                        "liveness": ["livenessState"],
                        "readiness": ["readinessState", "mongo", "rabbit"],
                    }
            auto_discover: Automatically detect service connections on
                ``app.state`` and register matching health indicators.
            **indicators: Named health indicators to register.

        Returns:
            A new HealthActuatorPlugin instance.

        Example:
            >>> plugin = HealthActuatorPlugin.with_indicators(
            ...     groups={"liveness": ["livenessState"], "readiness": ["readinessState", "db"]},
            ...     livenessState=LivenessIndicator(),
            ...     readinessState=ReadinessIndicator(),
            ...     db=DatabaseHealthIndicator(),
            ... )
        """
        return cls(
            indicators=dict(indicators),
            show_details=show_details,
            with_defaults=with_defaults,
            groups=groups,
            auto_discover=auto_discover,
        )

    def _active_state(
        self,
    ) -> tuple[dict[str, HealthIndicator], dict[str, list[str]]]:
        """Return (indicators, groups) with auto-discovered services merged."""
        indicators = dict(self._indicators)
        groups = {k: list(v) for k, v in self._groups.items()}

        if self._auto_discover and self._app is not None:
            discovered = discover_indicators(self._app)
            auto_names: list[str] = []
            for name, indicator in discovered.items():
                if name not in indicators:
                    indicators[name] = indicator
                    auto_names.append(name)

            if auto_names and "readiness" in groups:
                for name in sorted(auto_names):
                    if name not in groups["readiness"]:
                        groups["readiness"].append(name)

        return indicators, groups

    def register(
        self,
        router: APIRouter,
        *,
        app: FastAPI,
        prefix: str,
    ) -> Mapping[str, ActuatorLink]:
        self._app = app

        @router.get("/health", include_in_schema=False)
        async def health() -> dict[str, Any]:
            return await self._build_health_response()

        @router.get("/health/{component}", include_in_schema=False)
        async def health_component(component: str) -> dict[str, Any]:
            indicators, groups = self._active_state()

            # Check groups first, then individual indicators
            if component in groups:
                return await self._build_group_response(component, indicators, groups)

            indicator = indicators.get(component)
            if indicator is None:
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Health component not found")
            return await self._evaluate_indicator(component, indicator)

        return {
            "health": self.build_link(prefix=prefix, route_path="/health"),
            "health-component": ActuatorLink(
                href=f"{prefix}/health/{{component}}",
                templated=True,
            ),
        }

    async def _build_health_response(self) -> dict[str, Any]:
        indicators, groups = self._active_state()
        components: dict[str, dict[str, Any]] = {}
        statuses: list[str] = []

        for name, indicator in indicators.items():
            result = await self._evaluate_indicator(name, indicator)
            components[name] = result
            statuses.append(result.get("status", "UNKNOWN"))

        overall = _aggregate_status(statuses)

        if self._show_details == ShowDetails.ALWAYS:
            response: dict[str, Any] = {"status": overall}
            if groups:
                response["groups"] = sorted(groups)
            response["components"] = components
            return response

        response = {"status": overall}
        if groups:
            response["groups"] = sorted(groups)
        return response

    async def _build_group_response(
        self,
        group_name: str,
        indicators: dict[str, HealthIndicator],
        groups: dict[str, list[str]],
    ) -> dict[str, Any]:
        """Build an aggregated response for a health group."""
        member_names = groups[group_name]
        components: dict[str, dict[str, Any]] = {}
        statuses: list[str] = []

        for name in member_names:
            indicator = indicators.get(name)
            if indicator is None:
                continue
            result = await self._evaluate_indicator(name, indicator)
            components[name] = result
            statuses.append(result.get("status", "UNKNOWN"))

        overall = _aggregate_status(statuses) if statuses else "UNKNOWN"

        if self._show_details == ShowDetails.ALWAYS:
            return {"status": overall, "components": components}

        return {"status": overall}

    async def _evaluate_indicator(self, name: str, indicator: HealthIndicator) -> dict[str, Any]:
        try:
            result = indicator.health()
            if inspect.isawaitable(result):
                result = await result
            return result
        except Exception:
            logger.exception("Health indicator '%s' failed", name)
            return {"status": "DOWN"}
