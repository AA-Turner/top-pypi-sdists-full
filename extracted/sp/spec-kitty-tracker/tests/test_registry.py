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
