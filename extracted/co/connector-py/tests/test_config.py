from pathlib import Path

import pytest
from connector.config import LOG_DIRECTORY_ENV_VAR, LOG_LEVEL_ENV_VAR, Config, LogLevel


@pytest.fixture
def clean_environment(monkeypatch):
    """Clear relevant environment variables before each test"""
    # monkeypatch.delenv removes env var if it exists, otherwise does nothing
    monkeypatch.delenv(LOG_LEVEL_ENV_VAR, raising=False)
    monkeypatch.delenv(LOG_DIRECTORY_ENV_VAR, raising=False)


def test_default_initialization(clean_environment):
    """Test that Config initializes with default values when no env vars are set"""
    config = Config()
    assert config.log_level == LogLevel.ERROR
    assert config.log_directory is None


def test_custom_log_level(monkeypatch):
    """Test that Config respects custom log level from environment"""
    monkeypatch.setenv(LOG_LEVEL_ENV_VAR, "DEBUG")
    config = Config()
    assert config.log_level == LogLevel.DEBUG


def test_custom_log_directory(monkeypatch):
    """Test that Config respects custom log directory from environment"""
    test_path = "/tmp/logs"
    monkeypatch.setenv(LOG_DIRECTORY_ENV_VAR, test_path)
    config = Config()
    assert config.log_directory == Path(test_path)


def test_invalid_log_level(monkeypatch):
    """Test that Config raises ValueError for invalid log level"""
    monkeypatch.setenv(LOG_LEVEL_ENV_VAR, "INVALID_LEVEL")
    with pytest.raises(ValueError) as exc_info:
        Config()
    assert "Invalid log level" in str(exc_info.value)
