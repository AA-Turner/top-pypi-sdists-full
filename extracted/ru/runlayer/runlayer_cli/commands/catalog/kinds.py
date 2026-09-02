"""One registry entry per catalog resource type.

`skills` / `plugins` / `connectors` / `search` / `info` all drive off this
registry, so a reader holds one mental model instead of three parallel flows.
The per-type differences (which API call, which fields) are isolated to the
small callables wired up here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Generic, TypeVar

from runlayer_cli.api import PluginDetail, RunlayerClient, SkillDetail
from runlayer_cli.catalog_enrichment import ConnectorView, enrich_connector
from runlayer_cli.commands.catalog import display, resolve

T = TypeVar("T")


class CatalogInfoType(str, Enum):
    SKILL = "skill"
    PLUGIN = "plugin"
    CONNECTOR = "connector"


@dataclass(frozen=True)
class CatalogKind(Generic[T]):
    """How to list, resolve, sort, and render one catalog resource type."""

    noun: str
    info_type: CatalogInfoType
    # Beta is a connector-only catalog concept (it lives in the catalog `_meta`
    # blob). `supports_beta` lets callers decide per kind whether to forward
    # `--include-beta` rather than passing a flag that a kind would silently
    # drop; only beta-capable kinds' `list_items` accept `include_beta`.
    supports_beta: bool
    list_items: Callable[..., list[T]]
    resolve_ref: Callable[[RunlayerClient, str], T]
    sort_key: Callable[[T], tuple[str, str]]
    render_row: Callable[[T], str]
    to_summary: Callable[[T], dict[str, Any]]
    to_detail: Callable[[T], dict[str, Any]]


def _list_skills(
    api: RunlayerClient,
    *,
    query: str | None,
    namespace: str | None,
) -> list[SkillDetail]:
    return api.list_skills(namespace=namespace, filter="all", query=query)


def _list_plugins(
    api: RunlayerClient,
    *,
    query: str | None,
    namespace: str | None,
) -> list[PluginDetail]:
    return api.list_plugins_detailed(namespace=namespace, filter="all", query=query)


def _matches_query(*values: str | None, query: str | None) -> bool:
    if not query:
        return True
    needle = query.lower()
    return any(value is not None and needle in value.lower() for value in values)


def _filter_connectors(
    connectors: list[ConnectorView],
    *,
    query: str | None,
    include_beta: bool,
) -> list[ConnectorView]:
    """Apply the beta + free-text filter shared by `connectors` and `search`."""
    return [
        connector
        for connector in connectors
        if (include_beta or not connector.is_beta)
        and _matches_query(
            connector.name,
            connector.title,
            connector.description,
            query=query,
        )
    ]


def _list_connectors(
    api: RunlayerClient,
    *,
    query: str | None,
    namespace: str | None = None,
    include_beta: bool = False,
) -> list[ConnectorView]:
    connectors = [enrich_connector(item) for item in api.list_catalog_connectors()]
    return _filter_connectors(connectors, query=query, include_beta=include_beta)


SKILL_KIND: CatalogKind[SkillDetail] = CatalogKind(
    noun="skill",
    info_type=CatalogInfoType.SKILL,
    supports_beta=False,
    list_items=_list_skills,
    resolve_ref=resolve.resolve_skill,
    sort_key=display.skill_sort_key,
    render_row=display.render_skill_row,
    to_summary=display.skill_summary,
    to_detail=display.skill_detail,
)

PLUGIN_KIND: CatalogKind[PluginDetail] = CatalogKind(
    noun="plugin",
    info_type=CatalogInfoType.PLUGIN,
    supports_beta=False,
    list_items=_list_plugins,
    resolve_ref=resolve.resolve_plugin,
    sort_key=display.plugin_sort_key,
    render_row=display.render_plugin_row,
    to_summary=display.plugin_summary,
    to_detail=display.plugin_detail,
)

CONNECTOR_KIND: CatalogKind[ConnectorView] = CatalogKind(
    noun="connector",
    info_type=CatalogInfoType.CONNECTOR,
    supports_beta=True,
    list_items=_list_connectors,
    resolve_ref=resolve.resolve_connector,
    sort_key=display.connector_sort_key,
    render_row=display.render_connector_row,
    to_summary=display.connector_summary,
    to_detail=display.connector_detail,
)

# Search renders sections in this order.
ALL_KINDS: list[CatalogKind[Any]] = [CONNECTOR_KIND, SKILL_KIND, PLUGIN_KIND]
KIND_BY_INFO_TYPE: dict[CatalogInfoType, CatalogKind[Any]] = {
    kind.info_type: kind for kind in ALL_KINDS
}
