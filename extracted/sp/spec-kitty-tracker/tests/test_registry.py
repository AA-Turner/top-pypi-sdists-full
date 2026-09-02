import pytest

from spec_kitty_tracker import ConnectorRegistry, InMemoryConnector
from spec_kitty_tracker.errors import ConnectorConfigError


def test_registry_register_get_list() -> None:
    registry = ConnectorRegistry()
    connector = InMemoryConnector(name="jira", workspace="demo")

    registry.register(connector)

    assert registry.get("jira") is connector
    assert registry.list_names() == ["jira"]


def test_registry_missing_connector() -> None:
    registry = ConnectorRegistry()

    try:
        registry.get("missing")
    except ConnectorConfigError:
        assert True
        return

    assert False, "Expected ConnectorConfigError"


def test_registry_rejects_empty_connector_name() -> None:
    """N22: register() with an empty/whitespace name -> ConnectorConfigError.

    TRK-M1-01 draft N22 pins this as existing behavior (registry.py:14-18).
    The companion half of N22 — "M1 hosts' construction paths never call
    load_entrypoints" — is a host-side grep guard in the CLI/SaaS
    consumer repos, out of TRK-M1-02's repo_scope (spec-kitty-tracker
    only); see load_entrypoints' docstring (A16) for the M1 host policy.
    """
    registry = ConnectorRegistry()
    connector = InMemoryConnector(name="   ", workspace="demo")

    with pytest.raises(ConnectorConfigError):
        registry.register(connector)
