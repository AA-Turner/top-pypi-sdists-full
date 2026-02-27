import pytest


@pytest.fixture(autouse=True)
def setup_cli_environment(monkeypatch):
    """Set up environment for CLI tests."""
    monkeypatch.setenv("LOCALSTACK_CLI", "1")
