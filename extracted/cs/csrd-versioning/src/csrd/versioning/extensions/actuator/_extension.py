"""Actuator extension — built-in extension for Spring-style management endpoints."""

from collections.abc import Sequence

from fastapi import FastAPI

from .._types import ExtensionContext
from .plugins.base import ActuatorPlugin


class ActuatorExtension:
    """Built-in extension that registers ``/actuator`` management endpoints.

    Wraps :func:`register_actuator_router` behind the unified
    :class:`Extension` protocol.  Consumers inject sub-plugins via
    ``VersionedApiConfig.actuator_plugins``; the orchestration layer
    calls :meth:`add_plugins` before :meth:`apply`.

    Parameters
    ----------
    prefix:
        URL prefix for actuator routes.  Default ``"/actuator"``.
    enabled:
        Set to ``False`` to disable this extension.
    """

    name: str = "actuator"
    order: int = 50
    enabled: bool = True

    def __init__(
        self,
        *,
        prefix: str = "/actuator",
        enabled: bool = True,
    ) -> None:
        self._prefix = prefix
        self.enabled = enabled
        self._plugins: list[ActuatorPlugin] = []

    def add_plugins(self, plugins: Sequence[ActuatorPlugin]) -> None:
        """Inject consumer-provided actuator plugins.

        Called by the orchestration layer before :meth:`apply`.
        These plugins are merged with defaults inside
        :func:`register_actuator_router` using by-name override.
        """
        self._plugins.extend(plugins)

    def apply(self, app: FastAPI, ctx: ExtensionContext) -> None:
        """Register actuator router on *app*."""
        from .actuator import register_actuator_router

        register_actuator_router(
            app,
            plugins=self._plugins or None,
            prefix=self._prefix,
        )
