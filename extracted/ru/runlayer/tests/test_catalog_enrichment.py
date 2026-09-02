"""Lock the ported catalog enrichment so it can't silently drift from backend."""

from runlayer_cli.catalog_client import (
    CatalogConnector,
    CatalogPackage,
    CatalogRemote,
)
from runlayer_cli.catalog_enrichment import enrich_connector

_PUBLISHER_KEY = "io.modelcontextprotocol.registry/publisher-provided"
_COMPUTED_KEY = "io.runlayer/computed"


def _connector(*, runlayer: dict | None = None, computed: dict | None = None, **kwargs):
    meta: dict = {}
    if runlayer is not None:
        meta[_PUBLISHER_KEY] = {"runlayer": runlayer}
    if computed is not None:
        meta[_COMPUTED_KEY] = computed
    return CatalogConnector(name="com.acme/mcp", meta=meta, **kwargs)


def test_defaults_when_meta_is_empty():
    view = enrich_connector(CatalogConnector(name="com.acme/mcp"))

    assert view.deployment_mode == "hosted"
    assert view.is_beta is False
    assert view.is_deploy_based is False
    assert view.is_official is True
    assert view.existing_count == 0
    assert view.transports == []
    assert view.status == "active"


def test_runlayer_meta_flattened():
    view = enrich_connector(
        _connector(
            runlayer={
                "deploymentMode": "local",
                "beta": True,
                "deployConfig": {"image": "acme/mcp"},
                "isUnofficial": True,
                "oauthBrokerVendor": "acme",
                "requiresManualOauthSetup": True,
                "helpUrl": "https://help",
                "iconUrl": "https://icon",
            },
            computed={"existing_count": 5},
        )
    )

    assert view.deployment_mode == "local"
    assert view.is_beta is True
    assert view.is_deploy_based is True
    assert view.is_official is False
    assert view.oauth_broker_vendor == "acme"
    assert view.requires_manual_oauth_setup is True
    assert view.help_url == "https://help"
    assert view.icon_url == "https://icon"
    assert view.existing_count == 5


def test_invalid_deployment_mode_falls_back_to_hosted():
    view = enrich_connector(_connector(runlayer={"deploymentMode": "bogus"}))

    assert view.deployment_mode == "hosted"


def test_non_int_existing_count_coerced_to_zero():
    view = enrich_connector(_connector(computed={"existing_count": "lots"}))

    assert view.existing_count == 0


def test_malformed_publisher_meta_is_ignored():
    connector = CatalogConnector(name="com.acme/mcp", meta={_PUBLISHER_KEY: "nope"})

    view = enrich_connector(connector)

    assert view.deployment_mode == "hosted"
    assert view.is_official is True


def test_transports_dedupe_sorted_packages_then_remotes():
    connector = CatalogConnector(
        name="com.acme/mcp",
        packages=[
            {"identifier": "acme", "transport": {"type": "stdio"}},
            {"identifier": "acme2", "transport": {"type": "stdio"}},
        ],
        remotes=[
            {"type": "streamable-http", "url": "https://example.com/mcp"},
            {"type": "sse", "url": "https://example.com/sse"},
        ],
    )

    view = enrich_connector(connector)

    assert view.transports == ["sse", "stdio", "streamable-http"]


def test_packages_and_remotes_carried_as_typed_models():
    connector = CatalogConnector(
        name="com.acme/mcp",
        packages=[{"identifier": "acme", "registryType": "oci"}],
        remotes=[{"type": "sse", "url": "https://example.com/sse"}],
    )

    view = enrich_connector(connector)

    # The typed models pass through untouched; serialization is a display concern.
    assert view.packages == [CatalogPackage(identifier="acme", registry_type="oci")]
    assert view.remotes == [CatalogRemote(type="sse", url="https://example.com/sse")]
    assert all(isinstance(package, CatalogPackage) for package in view.packages)
    assert all(isinstance(remote, CatalogRemote) for remote in view.remotes)
