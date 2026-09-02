"""Tests for packaged-macOS keychain entry adoption."""

from __future__ import annotations

from unittest.mock import call, patch

import keyring.errors
import pytest
from typer.testing import CliRunner

from runlayer_cli import runtime
from runlayer_cli.commands import keychain
from runlayer_cli.config import Config
from runlayer_cli.credential_store import readopt_entry
from runlayer_cli.main import app

_AIWATCH_EXE = "/usr/local/lib/runlayer/aiwatch/aiwatch"
_RUNLAYER_EXE = "/usr/local/lib/runlayer/runlayer/runlayer"

runner = CliRunner()


class TestFrozenRunlayerBundle:
    def test_frozen_macos_runlayer(self):
        with (
            patch.object(runtime.sys, "platform", "darwin"),
            patch.object(runtime.sys, "executable", _RUNLAYER_EXE),
            patch.object(runtime.sys, "frozen", True, create=True),
        ):
            assert runtime.is_frozen_runlayer_bundle() is True

    @pytest.mark.parametrize(
        ("platform", "executable", "frozen"),
        [
            ("darwin", _AIWATCH_EXE, True),
            ("darwin", "/usr/bin/python3", False),
            ("linux", _RUNLAYER_EXE, True),
        ],
    )
    def test_other_runtimes(self, platform: str, executable: str, frozen: bool):
        with (
            patch.object(runtime.sys, "platform", platform),
            patch.object(runtime.sys, "executable", executable),
            patch.object(runtime.sys, "frozen", frozen, create=True),
        ):
            assert runtime.is_frozen_runlayer_bundle() is False


class TestReadoptEntry:
    def test_recreates_existing_secret(self):
        with (
            patch("keyring.get_password", return_value="rl_secret") as get_password,
            patch("keyring.delete_password") as delete_password,
            patch("keyring.set_password") as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "adopted"
        get_password.assert_called_once_with("runlayer-cli", "app.runlayer.com")
        delete_password.assert_called_once_with("runlayer-cli", "app.runlayer.com")
        set_password.assert_called_once_with(
            "runlayer-cli", "app.runlayer.com", "rl_secret"
        )

    def test_missing_entry_does_nothing(self):
        with (
            patch("keyring.get_password", return_value=None),
            patch("keyring.delete_password") as delete_password,
            patch("keyring.set_password") as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "nothing"
        delete_password.assert_not_called()
        set_password.assert_not_called()

    def test_denied_read_preserves_entry(self):
        with (
            patch(
                "keyring.get_password",
                side_effect=keyring.errors.KeyringLocked("denied"),
            ),
            patch("keyring.delete_password") as delete_password,
            patch("keyring.set_password") as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "denied"
        delete_password.assert_not_called()
        set_password.assert_not_called()

    def test_delete_failure_does_not_overwrite_entry(self):
        with (
            patch("keyring.get_password", return_value="rl_secret"),
            patch(
                "keyring.delete_password",
                side_effect=keyring.errors.KeyringError("delete failed"),
            ),
            patch("keyring.set_password") as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "failed"
        set_password.assert_not_called()

    def test_set_failure_retries_once(self):
        with (
            patch("keyring.get_password", return_value="rl_secret"),
            patch("keyring.delete_password"),
            patch(
                "keyring.set_password",
                side_effect=[
                    keyring.errors.PasswordSetError("locked"),
                    None,
                ],
            ) as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "adopted"
        assert set_password.call_count == 2

    def test_both_set_attempts_fail_after_delete_reports_lost(self):
        with (
            patch("keyring.get_password", return_value="rl_secret"),
            patch("keyring.delete_password"),
            patch(
                "keyring.set_password",
                side_effect=keyring.errors.PasswordSetError("locked"),
            ) as set_password,
        ):
            result = readopt_entry("app.runlayer.com")

        assert result == "lost"
        assert set_password.call_count == 2


def _config(*host_keys: str) -> Config:
    return Config(
        default_host=f"https://{host_keys[0]}" if host_keys else None,
        hosts={host_key: {"url": f"https://{host_key}"} for host_key in host_keys},
    )


class TestMaybeAutoAdopt:
    def test_non_frozen_runtime_skips(self):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=False),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt("login")
        readopt.assert_not_called()

    def test_non_tty_skips(self):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=False),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt("login")
        readopt.assert_not_called()

    @pytest.mark.parametrize(
        "command",
        [
            "keychain",
            "run",
            "scan",
            "status",
            "__handle-url",
            "__self-update-root",
        ],
    )
    def test_skipped_commands(self, command: str):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt(command)
        readopt.assert_not_called()

    def test_root_context_skips(self):
        """Sudo re-exec (e.g. privileged self-update) must never touch keychains."""
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain.os, "geteuid", return_value=0, create=True),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt("login")
        readopt.assert_not_called()

    def test_existing_marker_skips(self, tmp_path):
        marker = tmp_path / ".keychain-adopted-app.runlayer.com"
        marker.touch()
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt("login")
        readopt.assert_not_called()

    @pytest.mark.parametrize("result", ["adopted", "nothing", "denied", "lost"])
    def test_completed_attempt_writes_marker(self, tmp_path, result: str):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value=result),
        ):
            keychain.maybe_auto_adopt("login")

        assert (tmp_path / ".keychain-adopted-app.runlayer.com").exists()

    def test_lost_attempt_tells_user_to_relogin(self, tmp_path, capsys):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="lost"),
        ):
            keychain.maybe_auto_adopt("login")

        stderr = capsys.readouterr().err
        assert "was removed but could not be recreated" in stderr
        assert "runlayer login" in stderr

    def test_failed_attempt_does_not_write_marker(self, tmp_path):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="failed"),
        ):
            keychain.maybe_auto_adopt("login")

        assert not (tmp_path / ".keychain-adopted-app.runlayer.com").exists()

    def test_unexpected_error_degrades_to_warning(self, tmp_path, capsys):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(
                keychain,
                "readopt_entry",
                side_effect=RuntimeError("could not resolve home directory"),
            ),
        ):
            keychain.maybe_auto_adopt("login")

        assert "Skipped the keychain adoption check" in capsys.readouterr().err

    def test_marker_path_error_degrades_to_warning(self, capsys):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain.sys.stderr, "isatty", return_value=True),
            patch.object(
                keychain,
                "adoption_marker_path",
                side_effect=RuntimeError("could not resolve home directory"),
            ),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry") as readopt,
        ):
            keychain.maybe_auto_adopt("login")

        readopt.assert_not_called()
        assert "Skipped the keychain adoption check" in capsys.readouterr().err


class TestKeychainAdoptCommand:
    def test_single_configured_host(self, tmp_path):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="adopted") as readopt,
        ):
            result = runner.invoke(app, ["keychain", "adopt"])

        assert result.exit_code == 0
        readopt.assert_called_once_with("app.runlayer.com")

    def test_all_configured_hosts(self, tmp_path):
        config = _config("z.runlayer.com", "a.runlayer.com")
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(keychain, "load_config", return_value=config),
            patch.object(keychain, "readopt_entry", return_value="nothing") as readopt,
        ):
            result = runner.invoke(app, ["keychain", "adopt"])

        assert result.exit_code == 0
        assert readopt.call_args_list == [
            call("a.runlayer.com"),
            call("z.runlayer.com"),
        ]

    def test_host_filter(self, tmp_path):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="adopted") as readopt,
        ):
            result = runner.invoke(
                app,
                [
                    "keychain",
                    "adopt",
                    "--host",
                    "https://tenant.runlayer.com:8443",
                ],
            )

        assert result.exit_code == 0
        readopt.assert_called_once_with("tenant.runlayer.com:8443")

    def test_ignores_existing_marker(self, tmp_path):
        (tmp_path / ".keychain-adopted-app.runlayer.com").touch()
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="adopted") as readopt,
        ):
            result = runner.invoke(app, ["keychain", "adopt"])

        assert result.exit_code == 0
        readopt.assert_called_once_with("app.runlayer.com")

    def test_lost_result_fails_and_tells_user_to_relogin(self, tmp_path):
        with (
            patch.object(keychain, "is_frozen_runlayer_bundle", return_value=True),
            patch.object(keychain, "get_runlayer_dir", return_value=tmp_path),
            patch.object(
                keychain, "load_config", return_value=_config("app.runlayer.com")
            ),
            patch.object(keychain, "readopt_entry", return_value="lost"),
        ):
            result = runner.invoke(app, ["keychain", "adopt"])

        assert result.exit_code == 1
        assert "was removed but" in result.output
        assert "runlayer login" in result.output

    def test_rejects_non_packaged_runtime(self):
        with patch.object(keychain, "is_frozen_runlayer_bundle", return_value=False):
            result = runner.invoke(app, ["keychain", "adopt"])

        assert result.exit_code == 1
        assert "only available in the packaged macOS" in result.output
