"""Swagger UI plugin protocol, contribution dataclass, and resolution logic."""

import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from fastapi import FastAPI

from csrd.versioning._types import VersionKey

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SchemaContext:
    """Read-only metadata passed to schema patchers."""

    app: FastAPI
    """The versioned sub-app whose schema is being built."""

    version_key: VersionKey
    """The version key (e.g. ``Versions.V1``) being rendered."""

    prefix: str
    """Normalised API prefix, e.g. ``"/api"``."""


@dataclass(frozen=True)
class SwaggerPluginContribution:
    """Static data returned by :meth:`SwaggerPlugin.contribute`."""

    extra_css: str | None = None
    extra_js: str = ""
    bundle_plugins: tuple[str, ...] = ()
    schema_patcher: Callable[[dict, SchemaContext], dict] | None = None


@runtime_checkable
class SwaggerPlugin(Protocol):
    """Protocol for Swagger UI plugins."""

    name: str

    def contribute(self) -> SwaggerPluginContribution: ...


def _extract_css_class_names(css: str) -> set[str]:
    return set(re.findall(r"\.([\w-]+)", css))


def _warn_css_conflicts(
    contributions: dict[str, SwaggerPluginContribution],
) -> None:
    plugin_classes: dict[str, set[str]] = {}
    for name, contrib in contributions.items():
        if contrib.extra_css:
            plugin_classes[name] = _extract_css_class_names(contrib.extra_css)

    names = list(plugin_classes.keys())
    for i, name_a in enumerate(names):
        for name_b in names[i + 1 :]:
            overlap = plugin_classes[name_a] & plugin_classes[name_b]
            if overlap:
                logger.warning(
                    "SwaggerPlugins '%s' and '%s' both define CSS rules for: %s",
                    name_a,
                    name_b,
                    ", ".join(f".{cls}" for cls in sorted(overlap)),
                )


def _resolve_swagger_plugins(
    global_plugins: list[SwaggerPlugin] | None,
    per_version_plugins: list[SwaggerPlugin] | None = None,
) -> tuple[SwaggerPlugin, ...]:

    if global_plugins is not None and len(global_plugins) == 0:
        return ()

    resolved: dict[str, SwaggerPlugin] = {p.name: p for p in _default_swagger_plugins()}
    if global_plugins:
        for p in global_plugins:
            resolved[p.name] = p

    if per_version_plugins is not None and len(per_version_plugins) == 0:
        return ()
    if per_version_plugins:
        for p in per_version_plugins:
            resolved[p.name] = p

    return tuple(resolved.values())


def _default_swagger_plugins() -> list[SwaggerPlugin]:
    from .file_upload import FileUploadExamplesPlugin

    return [FileUploadExamplesPlugin()]


def _collect_contributions(
    plugins: tuple[SwaggerPlugin, ...],
) -> dict[str, SwaggerPluginContribution]:
    contributions: dict[str, SwaggerPluginContribution] = {}
    for plugin in plugins:
        try:
            contributions[plugin.name] = plugin.contribute()
        except Exception:
            logger.warning(
                "SwaggerPlugin '%s' failed in contribute()",
                plugin.name,
                exc_info=True,
            )
    return contributions


def _aggregate_css(contributions: dict[str, SwaggerPluginContribution]) -> str:
    parts = [c.extra_css for c in contributions.values() if c.extra_css]
    return "\n".join(parts)


def _aggregate_js(contributions: dict[str, SwaggerPluginContribution]) -> str:
    parts = [c.extra_js for c in contributions.values() if c.extra_js]
    return "\n".join(parts)


def _aggregate_bundle_plugins(
    contributions: dict[str, SwaggerPluginContribution],
) -> str:
    names: list[str] = []
    for c in contributions.values():
        names.extend(c.bundle_plugins)
    return ", ".join(names)


def _collect_schema_patchers(
    contributions: dict[str, SwaggerPluginContribution],
) -> list[Callable[[dict, SchemaContext], dict]]:
    return [c.schema_patcher for c in contributions.values() if c.schema_patcher]


def apply_schema_patchers(
    schema: dict,
    ctx: SchemaContext,
    patchers: list[Callable[[dict, SchemaContext], dict]],
) -> dict:
    for patcher in patchers:
        try:
            schema = patcher(schema, ctx)
        except Exception:
            logger.warning("schema_patcher from plugin failed", exc_info=True)
    return schema
