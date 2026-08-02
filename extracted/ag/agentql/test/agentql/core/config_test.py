import pytest

from agentql._core._config import Config, configure


@pytest.fixture
def config():
    return Config()


def test_initialization(config):
    """Test that the Config object initializes with api_key set to None."""
    assert config.api_key is None


def test_update_with_api_key(config):
    """Test that the update method sets the api_key when provided."""
    test_key = "test_api_key"
    config.update(api_key=test_key)
    assert config.api_key == test_key


def test_configure_function():
    """Test the configure function updates the Config object."""
    test_key = "configure_api_key"
    configure(api_key=test_key)
    from agentql._core._config import config

    assert config.api_key == test_key
