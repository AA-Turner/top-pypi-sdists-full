"""Spring Boot-style ``/actuator`` management endpoints for FastAPI."""

import logging
from collections.abc import Mapping, Sequence

from fastapi import APIRouter, FastAPI, Request

from .plugins import ActuatorLink, ActuatorPlugin, default_actuator_plugins

logger = logging.getLogger(__name__)


def register_actuator_router(
    app: FastAPI,
    *,
    plugins: Sequence[ActuatorPlugin] | None = None,
    prefix: str = "/actuator",
) -> None:
    """Register actuator routes directly on *app*."""
    router = APIRouter(prefix=prefix, tags=["Actuator"], include_in_schema=False)

    plugin_links = _register_plugins(
        router,
        app=app,
        prefix=prefix,
        plugins=_resolve_plugins(plugins),
    )

    @router.get("", include_in_schema=False)
    async def actuator_root(
        request: Request,
    ) -> dict[str, dict[str, dict[str, bool | str]]]:
        base = str(request.base_url).rstrip("/")
        links: dict[str, dict[str, bool | str]] = {
            "self": {"href": f"{base}{prefix}", "templated": False}
        }
        for name, link in plugin_links.items():
            links[name] = {
                "href": f"{base}{link.href}",
                "templated": link.templated,
            }
        return {"_links": links}

    app.include_router(router)


def _register_plugins(
    router: APIRouter,
    *,
    app: FastAPI,
    prefix: str,
    plugins: Sequence[ActuatorPlugin],
) -> dict[str, ActuatorLink]:
    links: dict[str, ActuatorLink] = {}
    for plugin in plugins:
        plugin_links = plugin.register(router, app=app, prefix=prefix)
        _merge_plugin_links(links, plugin_links)
    return links


def _merge_plugin_links(
    links: dict[str, ActuatorLink],
    plugin_links: Mapping[str, ActuatorLink],
) -> None:
    for name, link in plugin_links.items():
        links[name] = link


def _resolve_plugins(
    plugins: Sequence[ActuatorPlugin] | None,
) -> tuple[ActuatorPlugin, ...]:
    resolved: dict[str, ActuatorPlugin] = {
        plugin.name: plugin for plugin in default_actuator_plugins()
    }

    if plugins is not None:
        for plugin in plugins:
            if plugin.name in resolved:
                logger.debug("Actuator plugin '%s' overridden by consumer", plugin.name)
            resolved[plugin.name] = plugin

    _wire_env_property_sources(resolved)

    return tuple(resolved.values())


def _wire_env_property_sources(resolved: dict[str, ActuatorPlugin]) -> None:
    contributed: dict[str, object] = {}

    for plugin in resolved.values():
        providers_getter = getattr(plugin, "property_source_providers", None)
        if callable(providers_getter):
            providers = providers_getter()
            if isinstance(providers, Mapping):
                contributed.update(providers)

    if not contributed:
        return

    env_plugin = resolved.get("env")
    if env_plugin is None:
        return

    register_providers = getattr(env_plugin, "register_property_source_providers", None)
    if callable(register_providers):
        register_providers(contributed)
        logger.debug(
            "Auto-wired %d property source provider(s) into env plugin: %s",
            len(contributed),
            ", ".join(contributed),
        )
