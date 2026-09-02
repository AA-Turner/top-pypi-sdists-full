"""Tests for logging configuration."""

import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest
import structlog

from runlayer_cli.logging import (
    attach_system_scan_log_handler,
    ensure_base_logging_configured,
    setup_logging,
    _get_log_file_path,
)

requires_nonroot_posix = pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="chmod-based permission denial needs a non-root POSIX user",
)


@pytest.fixture
def _reset_structlog():
    """Reset structlog to unconfigured defaults around a test.

    ``ensure_base_logging_configured`` / ``setup_logging`` mutate global structlog
    config; reset so ``structlog.is_configured()`` starts False and the config
    doesn't leak into other tests.
    """
    structlog.reset_defaults()
    yield
    structlog.reset_defaults()


@pytest.fixture
def _close_added_root_handlers():
    original_handlers = tuple(logging.root.handlers)
    yield
    for handler in tuple(logging.root.handlers):
        if handler not in original_handlers:
            logging.root.removeHandler(handler)
            handler.close()


def test_ensure_base_logging_silences_debug_to_stderr(
    capsys, monkeypatch, _reset_structlog
):
    """Default level: debug is filtered, info renders to stderr, stdout stays clean."""
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    ensure_base_logging_configured()
    logger = structlog.get_logger("test")
    logger.debug("hidden_debug_line")
    logger.info("shown_info_line")

    captured = capsys.readouterr()
    # Never stdout — protects the ``runlayer run`` stdio protocol channel.
    assert captured.out == ""
    assert "hidden_debug_line" not in captured.err
    assert "shown_info_line" in captured.err


def test_ensure_base_logging_shows_debug_under_debug_level(
    capsys, monkeypatch, _reset_structlog
):
    """LOG_LEVEL=DEBUG surfaces the debug line (still on stderr, not stdout)."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    ensure_base_logging_configured()
    structlog.get_logger("test").debug("visible_debug_line")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "visible_debug_line" in captured.err


def test_ensure_base_logging_is_idempotent(_reset_structlog):
    """A second call is a no-op once structlog is configured."""
    ensure_base_logging_configured()
    with patch("structlog.configure") as configure:
        ensure_base_logging_configured()
    configure.assert_not_called()


def test_ensure_base_logging_does_not_clobber_setup_logging(
    tmp_path, monkeypatch, _reset_structlog
):
    """When ``setup_logging`` already configured file logging, ensure is a no-op
    and file logging keeps working."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)

    setup_logging(command="run", quiet_console=True)
    with patch("structlog.configure") as configure:
        ensure_base_logging_configured()
    configure.assert_not_called()

    structlog.get_logger("test").info("still_to_file", key="value")
    log_dir = tmp_path / ".runlayer" / "logs"
    log_files = list(log_dir.glob("*-run-*.log"))
    assert len(log_files) == 1
    assert "still_to_file" in log_files[0].read_text()


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


def test_setup_logging_removes_daily_logs_older_than_retention(tmp_path, monkeypatch):
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    old_date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
    recent_date = (datetime.now() - timedelta(days=13)).strftime("%Y-%m-%d")
    old_log = log_dir / f"runlayer-v0-0-0-scan-{old_date}.log"
    recent_log = log_dir / f"runlayer-v0-0-0-scan-{recent_date}.log"
    old_log.write_text("old")
    recent_log.write_text("recent")
    old_mtime = (datetime.now() - timedelta(days=30)).timestamp()
    os.utime(old_log, None)
    os.utime(recent_log, (old_mtime, old_mtime))

    setup_logging(command="scan", quiet_console=True)

    assert not old_log.exists()
    assert recent_log.exists()


def test_setup_logging_caps_daily_logs_oldest_date_then_name(tmp_path, monkeypatch):
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    monkeypatch.setattr("runlayer_cli.logging.DAILY_LOG_TOTAL_CAP_BYTES", 8)
    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    oldest_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    newer_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    first_by_name = log_dir / f"runlayer-v0-0-0-a-{oldest_date}.log"
    second_by_name = log_dir / f"runlayer-v0-0-0-b-{oldest_date}.log"
    newer_log = log_dir / f"runlayer-v0-0-0-scan-{newer_date}.log"
    for path in (first_by_name, second_by_name, newer_log):
        path.write_bytes(b"1234")

    setup_logging(command="scan", quiet_console=True)

    assert not first_by_name.exists()
    assert second_by_name.exists()
    assert newer_log.exists()


def test_setup_logging_preserves_current_log_when_it_alone_exceeds_cap(
    tmp_path, monkeypatch
):
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    monkeypatch.setattr("runlayer_cli.logging.__version__", "0.0.0")
    monkeypatch.setattr("runlayer_cli.logging.DAILY_LOG_TOTAL_CAP_BYTES", 5)
    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    old_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    current_date = datetime.now().strftime("%Y-%m-%d")
    old_log = log_dir / f"runlayer-v0-0-0-scan-{old_date}.log"
    current_log = log_dir / f"runlayer-v0-0-0-scan-{current_date}.log"
    old_log.write_bytes(b"old!")
    current_log.write_bytes(b"current-data")

    setup_logging(command="scan", quiet_console=True)

    assert not old_log.exists()
    assert current_log.read_bytes() == b"current-data"


def test_setup_logging_ignores_unknown_and_malformed_daily_log_names(
    tmp_path, monkeypatch
):
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    monkeypatch.setattr("runlayer_cli.logging.DAILY_LOG_TOTAL_CAP_BYTES", 1)
    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    unknown_logs = (
        log_dir / "runlayer.log",
        log_dir / "runlayer-v0-0-0-scan-not-a-date.log",
        log_dir / "runlayer-v0-0-0-scan-2026-99-99.log",
    )
    for path in unknown_logs:
        path.write_bytes(b"oversized")

    setup_logging(command="scan", quiet_console=True)

    assert all(path.read_bytes() == b"oversized" for path in unknown_logs)


def test_setup_logging_tolerates_daily_log_stat_and_unlink_errors(
    tmp_path, monkeypatch
):
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    old_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
    recent_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    unlink_error_log = log_dir / f"runlayer-v0-0-0-scan-{old_date}.log"
    stat_error_log = log_dir / f"runlayer-v0-0-0-scan-{recent_date}.log"
    unlink_error_log.write_text("cannot unlink")
    stat_error_log.write_text("cannot stat")
    original_stat = Path.stat
    original_unlink = Path.unlink

    def flaky_stat(path, *args, **kwargs):
        if path == stat_error_log:
            raise OSError("simulated stat failure")
        return original_stat(path, *args, **kwargs)

    def flaky_unlink(path, *args, **kwargs):
        if path == unlink_error_log:
            raise OSError("simulated unlink failure")
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", flaky_stat)
    monkeypatch.setattr(Path, "unlink", flaky_unlink)

    log_path = setup_logging(command="scan", quiet_console=True)
    structlog.get_logger("test").info("logging survived sweep failures")

    assert unlink_error_log.read_text() == "cannot unlink"
    assert stat_error_log.read_text() == "cannot stat"
    assert "logging survived sweep failures" in log_path.read_text()


def test_setup_logging_sweeps_temp_fallback_independently(tmp_path, monkeypatch):
    temp_dir = tmp_path / "tmp"
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(temp_dir))

    def fail_primary_log_path(_command):
        raise OSError("primary unavailable")

    monkeypatch.setattr(
        "runlayer_cli.logging._get_log_file_path", fail_primary_log_path
    )
    fallback_log_dir = temp_dir / "runlayer-logs"
    fallback_log_dir.mkdir(parents=True)
    old_date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
    old_log = fallback_log_dir / f"runlayer-v0-0-0-scan-{old_date}.log"
    old_log.write_text("old")

    log_path = setup_logging(command="scan", quiet_console=True)

    assert log_path.parent == fallback_log_dir
    assert not old_log.exists()


def test_attach_system_scan_log_handler_rotates_oversized_log(
    tmp_path, monkeypatch, _close_added_root_handlers
):
    log_path = tmp_path / "scheduled-task.log"
    backup_path = tmp_path / "scheduled-task.log.1"
    log_path.write_bytes(b"oversized")
    backup_path.write_bytes(b"stale")
    monkeypatch.setattr("runlayer_cli.logging.sys.platform", "win32")
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_PATH", log_path)
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_MAX_BYTES", 4)

    attached_path = attach_system_scan_log_handler()
    logging.getLogger("test").warning("written after rotation")

    assert attached_path == log_path
    assert backup_path.read_bytes() == b"oversized"
    assert b"written after rotation" in log_path.read_bytes()


def test_attach_system_scan_log_handler_does_not_rotate_at_threshold(
    tmp_path, monkeypatch, _close_added_root_handlers
):
    log_path = tmp_path / "scheduled-task.log"
    log_path.write_bytes(b"1234")
    monkeypatch.setattr("runlayer_cli.logging.sys.platform", "win32")
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_PATH", log_path)
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_MAX_BYTES", 4)

    attached_path = attach_system_scan_log_handler()

    assert attached_path == log_path
    assert log_path.read_bytes() == b"1234"
    assert not (tmp_path / "scheduled-task.log.1").exists()


def test_attach_system_scan_log_handler_appends_when_rotation_fails(
    tmp_path, monkeypatch, _close_added_root_handlers
):
    log_path = tmp_path / "scheduled-task.log"
    log_path.write_bytes(b"oversized")
    monkeypatch.setattr("runlayer_cli.logging.sys.platform", "win32")
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_PATH", log_path)
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_MAX_BYTES", 4)
    original_replace = Path.replace

    def fail_log_replace(path, target):
        if path == log_path:
            raise OSError("simulated concurrent open handle")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_log_replace)

    attached_path = attach_system_scan_log_handler()
    logging.getLogger("test").warning("appended after failed rotation")

    assert attached_path == log_path
    contents = log_path.read_bytes()
    assert contents.startswith(b"oversized")
    assert b"appended after failed rotation" in contents
    assert not (tmp_path / "scheduled-task.log.1").exists()


def test_attach_system_scan_log_handler_tolerates_unwritable_log(
    tmp_path, monkeypatch, _close_added_root_handlers
):
    log_path = tmp_path / "scheduled-task.log"
    monkeypatch.setattr("runlayer_cli.logging.sys.platform", "win32")
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_PATH", log_path)
    monkeypatch.setattr("runlayer_cli.logging.SCHEDULED_TASK_LOG_MAX_BYTES", 4)

    def fail_file_handler(*_args, **_kwargs):
        raise PermissionError("simulated unwritable log")

    monkeypatch.setattr(logging, "FileHandler", fail_file_handler)

    assert attach_system_scan_log_handler() is None


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


@requires_nonroot_posix
def test_setup_logging_survives_unwritable_log_file(tmp_path, monkeypatch):
    """An unwritable log file (e.g. created by a prior sudo run) must not crash startup."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path / "tmp"))

    log_dir = tmp_path / ".runlayer" / "logs"
    log_dir.mkdir(parents=True)
    unwritable = _get_log_file_path("run")
    unwritable.touch()
    unwritable.chmod(0o000)

    try:
        log_file_path = setup_logging(command="run", quiet_console=True)
    finally:
        unwritable.chmod(0o644)

    # Falls back to a temp-dir log file so logs are still captured
    assert log_file_path != unwritable
    logger = structlog.get_logger("test")
    logger.info("still alive")
    assert "still alive" in log_file_path.read_text()


@requires_nonroot_posix
def test_setup_logging_survives_unwritable_log_dir(tmp_path, monkeypatch):
    """An unwritable ~/.runlayer (root-owned) must not crash startup."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path / "tmp"))

    runlayer_dir = tmp_path / ".runlayer"
    runlayer_dir.mkdir()
    runlayer_dir.chmod(0o555)

    try:
        log_file_path = setup_logging(command="run", quiet_console=True)
    finally:
        runlayer_dir.chmod(0o755)

    logger = structlog.get_logger("test")
    logger.info("still alive")
    assert "still alive" in log_file_path.read_text()


@requires_nonroot_posix
def test_setup_logging_survives_all_log_targets_unwritable(
    tmp_path, monkeypatch, capsys
):
    """Even with no writable log location at all, setup_logging must not raise,
    and quiet_console must keep stderr silent (stdio protocol sessions)."""
    monkeypatch.setattr("runlayer_cli.logging.Path.home", lambda: tmp_path)
    unwritable_tmp = tmp_path / "tmp"
    unwritable_tmp.mkdir()
    unwritable_tmp.chmod(0o555)
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(unwritable_tmp))

    runlayer_dir = tmp_path / ".runlayer"
    runlayer_dir.mkdir()
    runlayer_dir.chmod(0o555)

    try:
        log_file_path = setup_logging(command="run", quiet_console=True)
        logger = structlog.get_logger("test")
        logger.info("still alive")  # must not raise either
    finally:
        runlayer_dir.chmod(0o755)
        unwritable_tmp.chmod(0o755)

    assert log_file_path is not None
    assert capsys.readouterr().err == ""


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
