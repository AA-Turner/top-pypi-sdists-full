"""Cross-process exclusion for scheduled AI Watch scans."""

import os
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from runlayer_cli.commands.scan import app
from runlayer_cli.scan import run_lock
from runlayer_cli.scan.run_lock import ScanRunLockError, acquire_scan_run_lock

runner = CliRunner()


def test_only_one_scan_process_holds_user_lock(tmp_path):
    path = tmp_path / "aiwatch-scan.lock"
    first = acquire_scan_run_lock(path)
    assert first is not None
    try:
        assert acquire_scan_run_lock(path) is None
    finally:
        first.close()

    replacement = acquire_scan_run_lock(path)
    assert replacement is not None
    replacement.close()


def test_default_lock_path_is_private_and_never_unlinked(tmp_path, monkeypatch):
    monkeypatch.setattr(run_lock, "get_runlayer_dir", lambda: tmp_path)

    lock = acquire_scan_run_lock()
    assert lock is not None
    lock.close()

    path = tmp_path / "aiwatch-scan.lock"
    assert path.exists()
    if os.name == "posix":
        assert path.stat().st_mode & 0o777 == 0o600


def test_lock_setup_error_is_distinct_from_busy(tmp_path):
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("x")

    with pytest.raises(ScanRunLockError):
        acquire_scan_run_lock(parent_file / "aiwatch-scan.lock")


@pytest.mark.parametrize("args", [["--dry-run"], ["--all-users"]])
def test_busy_scan_exits_successfully_before_credentials_or_scan(tmp_path, args):
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.commands.scan.acquire_scan_run_lock",
            return_value=None,
            create=True,
        ),
        patch("runlayer_cli.commands.scan.resolve_credentials") as credentials,
        patch("runlayer_cli.commands.scan.scan_all_clients") as scan_all,
    ):
        result = runner.invoke(app, args)

    assert result.exit_code == 0, result.output
    credentials.assert_not_called()
    scan_all.assert_not_called()


def test_scan_releases_lock_when_scan_raises(tmp_path):
    lock = Mock()
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.commands.scan.acquire_scan_run_lock",
            return_value=lock,
        ),
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": None, "host": None},
        ),
        patch(
            "runlayer_cli.commands.scan.scan_all_clients",
            side_effect=RuntimeError("scan failed"),
        ),
    ):
        result = runner.invoke(app, ["--dry-run"])

    assert result.exit_code == 1
    lock.close.assert_called_once_with()


def test_lock_infrastructure_error_fails_open(tmp_path):
    with (
        patch(
            "runlayer_cli.commands.scan.setup_logging",
            return_value=tmp_path / "scan.log",
        ),
        patch(
            "runlayer_cli.commands.scan.acquire_scan_run_lock",
            side_effect=ScanRunLockError("lock open failed"),
        ),
        patch(
            "runlayer_cli.commands.scan.resolve_credentials",
            return_value={"secret": None, "host": None},
        ),
        patch("runlayer_cli.commands.scan._run_scan") as run_scan,
    ):
        result = runner.invoke(app, ["--dry-run"])

    assert result.exit_code == 0, result.output
    run_scan.assert_called_once()
