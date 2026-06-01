"""Tests for logging configuration."""

import logging
from unittest.mock import patch
from datetime import datetime

import structlog

from runlayer_cli.logging import setup_logging, _get_log_file_path


def test_get_log_file_path_format(tmp_path):
    """Test that log file path follows expected format."""
    with (
        patch("runlayer_cli.logging.Path.home", return_value=tmp_path),
        patch("runlayer_cli.logging.__version__", "0.5.0"),
    ):
        log_path = _get_log_file_path("run")

        # Check format: runlayer-vX-X-X-command-YYYY-MM-DD.log
        assert log_path.name.startswith("runlayer-v0-5-0-run-")
        assert log_path.name.endswith(f"{datetime.now().strftime('%Y-%m-%d')}.log")
        assert log_path.parent.name == "logs"


def test_setup_logging_run_command_quiet_console(tmp_path, monkeypatch):
    """Test that run command logs to file only (no console output)."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)

    setup_logging(command="run", quiet_console=True)

    # Verify only file handler exists (no console handler)
    handlers = logging.root.handlers
    console_handlers = [
        h
        for h in handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
    ]
    file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]

    assert len(file_handlers) == 1
    assert len(console_handlers) == 0

    # Log something and verify it goes to file
    logger = structlog.get_logger("test")
    logger.info("Test message", key="value")

    log_dir = tmp_path / ".runlayer" / "logs"
    log_files = list(log_dir.glob("*-run-*.log"))
    assert len(log_files) == 1

    log_content = log_files[0].read_text()
    assert "Test message" in log_content
    assert "key=value" in log_content


def test_setup_logging_deploy_command_console_and_file(tmp_path, monkeypatch):
    """Test that deploy command logs to both console and file."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)

    setup_logging(command="deploy", quiet_console=False)

    # Verify both file and console handlers exist
    handlers = logging.root.handlers
    console_handlers = [
        h
        for h in handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
    ]
    file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]

    assert len(file_handlers) == 1
    assert len(console_handlers) == 1

    # Log something
    logger = structlog.get_logger("test")
    logger.info("Deploy message", service="test-service")

    # Verify log file was created and contains the message
    log_dir = tmp_path / ".runlayer" / "logs"
    log_files = list(log_dir.glob("*-deploy-*.log"))
    assert len(log_files) == 1

    log_content = log_files[0].read_text()
    assert "Deploy message" in log_content
    assert "service=test-service" in log_content


def test_setup_logging_creates_log_directory(tmp_path, monkeypatch):
    """Test that log directory is created if it doesn't exist."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)

    log_dir = tmp_path / ".runlayer" / "logs"
    assert not log_dir.exists()

    setup_logging(command="test", quiet_console=True)

    assert log_dir.exists()
    assert log_dir.is_dir()


def test_setup_logging_appends_to_existing_log_file(tmp_path, monkeypatch):
    """Test that logging appends to existing log file instead of overwriting."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)

    # Setup logging and write first message
    setup_logging(command="test", quiet_console=True)
    logger1 = structlog.get_logger("test1")
    logger1.info("First message")

    # Get the log file path
    log_dir = tmp_path / ".runlayer" / "logs"
    log_files = list(log_dir.glob("*-test-*.log"))
    assert len(log_files) == 1
    log_file = log_files[0]

    initial_content = log_file.read_text()
    assert "First message" in initial_content

    # Setup logging again (simulating new session)
    setup_logging(command="test", quiet_console=True)
    logger2 = structlog.get_logger("test2")
    logger2.info("Second message")

    # Should have both messages
    updated_content = log_file.read_text()
    assert "First message" in updated_content
    assert "Second message" in updated_content
