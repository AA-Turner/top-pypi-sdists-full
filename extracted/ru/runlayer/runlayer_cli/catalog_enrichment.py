"""Flatten raw MCP catalog connector metadata into explicit display fields.

This is the CLI counterpart to the backend ``_catalog_entry_helpers``
(``app/domains/runlayer_mcp/tools/catalog.py``) and the webapp ``enrichCatalogItem``.
Keeping the meta-parsing in one function avoids the drift that comes from each
surface re-deriving deployment mode / beta / transports from the nested
``_meta`` blob.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runlayer_cli.catalog_client import (
    CatalogConnector,
    CatalogPackage,
    CatalogRemote,
)

_PUBLISHER_META_KEY = "io.modelcontextprotocol.registry/publisher-provided"
_COMPUTED_META_KEY = "io.runlayer/computed"
_VALID_DEPLOYMENT_MODES = ("hosted", "local")
_DEFAULT_DEPLOYMENT_MODE = "hosted"


@dataclass(frozen=True)
class ConnectorView:
    """Flattened connector fields derived from a raw catalog entry."""

    name: str
    title: str | None
    description: str | None
    version: str | None
    status: str
    deployment_mode: str
    is_beta: bool
    is_deploy_based: bool
    is_official: bool
    existing_count: int
    transports: list[str]
    website_url: str | None
    repository: dict[str, Any] | None
    help_url: str | None
    icon_url: str | None
    oauth_broker_vendor: str | None
    requires_manual_oauth_setup: bool | None
    mcp_fingerprint: str | None
    version_fingerprint: str | None
    packages: list[CatalogPackage]
    remotes: list[CatalogRemote]


def _runlayer_meta(meta: dict[str, Any]) -> dict[str, Any]:
    publisher = meta.get(_PUBLISHER_META_KEY)
    if not isinstance(publisher, dict):
        return {}
    runlayer = publisher.get("runlayer")
    return runlayer if isinstance(runlayer, dict) else {}


def _computed_meta(meta: dict[str, Any]) -> dict[str, Any]:
    computed = meta.get(_COMPUTED_META_KEY)
    return computed if isinstance(computed, dict) else {}


def _transport_kinds(connector: CatalogConnector) -> list[str]:
    """Distinct transport types, package transports first then remotes."""
    kinds: list[str] = []
    for package in connector.packages:
        if package.transport and package.transport.type:
            kinds.append(package.transport.type)
    for remote in connector.remotes:
        if remote.type:
            kinds.append(remote.type)
    return sorted(dict.fromkeys(kinds))


def enrich_connector(connector: CatalogConnector) -> ConnectorView:
    """Derive flattened, explicit fields from a raw catalog connector entry."""
    runlayer = _runlayer_meta(connector.meta)
    computed = _computed_meta(connector.meta)

    deployment_mode = runlayer.get("deploymentMode")
    if deployment_mode not in _VALID_DEPLOYMENT_MODES:
        deployment_mode = _DEFAULT_DEPLOYMENT_MODE

    existing_count = computed.get("existing_count", 0)
    if not isinstance(existing_count, int):
        existing_count = 0

    return ConnectorView(
        name=connector.name,
        title=connector.title,
        description=connector.description,
        version=connector.version,
        status=connector.status or "active",
        deployment_mode=deployment_mode,
        is_beta=runlayer.get("beta") is True,
        is_deploy_based=isinstance(runlayer.get("deployConfig"), dict),
        is_official=not bool(runlayer.get("isUnofficial")),
        existing_count=existing_count,
        transports=_transport_kinds(connector),
        website_url=connector.website_url,
        repository=connector.repository,
        help_url=runlayer.get("helpUrl"),
        icon_url=runlayer.get("iconUrl"),
        oauth_broker_vendor=runlayer.get("oauthBrokerVendor"),
        requires_manual_oauth_setup=runlayer.get("requiresManualOauthSetup"),
        mcp_fingerprint=connector.mcp_fingerprint,
        version_fingerprint=connector.version_fingerprint,
        packages=connector.packages,
        remotes=connector.remotes,
    )
