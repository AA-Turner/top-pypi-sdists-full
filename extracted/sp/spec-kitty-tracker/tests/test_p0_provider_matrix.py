from spec_kitty_tracker.connectors import __all__ as connector_exports


def test_p0_provider_connectors_are_exported() -> None:
    required = {"JiraConnector", "LinearConnector", "GitHubConnector", "GitLabConnector"}
    assert required.issubset(set(connector_exports))
