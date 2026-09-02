"""Tests for the CLI command-perf telemetry contract (vocab + detection)."""

from unittest.mock import patch

from runlayer_cli import command_contract
from runlayer_cli.command_contract import (
    COMMAND_VOCAB,
    OS_VALUES,
    SOURCES,
    detect_os,
    detect_os_version,
    detect_source,
    sanitize_command,
)


class TestSanitizeCommand:
    def test_top_level_command(self):
        assert sanitize_command(["runlayer", "scan"]) == "scan"

    def test_update_command(self):
        assert sanitize_command(["runlayer", "update"]) == "update"

    def test_status_command(self):
        assert sanitize_command(["runlayer", "status", "--json"]) == "status"

    def test_aiwatch_daemon_command(self):
        assert sanitize_command(["aiwatch", "daemon"]) == "daemon"

    def test_aiwatch_config_show_command(self):
        assert sanitize_command(["aiwatch", "config", "show"]) == "config.show"

    def test_aiwatch_config_sync_command(self):
        assert sanitize_command(["aiwatch", "config", "sync"]) == "config.sync"

    def test_aiwatch_update_now_command(self):
        assert sanitize_command(["aiwatch", "update-now"]) == "update-now"

    def test_aiwatch_self_update_command(self):
        assert sanitize_command(["aiwatch", "self-update"]) == "self-update"

    def test_known_subcommand(self):
        assert sanitize_command(["runlayer", "plugins", "install"]) == "plugins.install"

    def test_keychain_adopt_subcommand(self):
        assert sanitize_command(["runlayer", "keychain", "adopt"]) == "keychain.adopt"

    def test_setup_config_subcommand(self):
        assert (
            sanitize_command(
                [
                    "aiwatch",
                    "setup",
                    "config",
                    "--host",
                    "https://tenant.example",
                    "--org-api-key",
                    "rl_org_secret",
                ]
            )
            == "setup.config"
        )

    def test_unknown_subcommand_falls_back_to_top_level(self):
        assert sanitize_command(["runlayer", "plugins", "frobnicate"]) == "plugins"

    def test_unknown_command_is_other(self):
        assert sanitize_command(["runlayer", "wat"]) == "other"

    def test_value_option_and_value_skipped(self):
        # --host consumes its value; the command is still found.
        assert sanitize_command(["runlayer", "--host", "https://x", "scan"]) == "scan"

    def test_short_value_option_skipped(self):
        assert sanitize_command(["runlayer", "-s", "sekret", "logs"]) == "logs"

    def test_boolean_flag_skipped(self):
        assert sanitize_command(["aiwatch", "--version"]) == "version"

    def test_bare_invocation_is_other(self):
        assert sanitize_command(["runlayer"]) == "other"

    def test_leading_uuid_maps_to_run(self):
        uuid = "12345678-1234-1234-1234-123456789abc"
        assert sanitize_command(["runlayer", uuid]) == "run"

    def test_every_result_is_in_vocab(self):
        # Sanitizer output must always be a valid closed-vocab value.
        for argv in (
            ["runlayer", "scan"],
            ["runlayer", "plugins", "install"],
            ["runlayer", "wat"],
            ["runlayer"],
            ["aiwatch", "--version"],
        ):
            assert sanitize_command(argv) in COMMAND_VOCAB


class TestDetectOs:
    def test_darwin(self):
        with patch.object(command_contract.sys, "platform", "darwin"):
            assert detect_os() == "darwin"

    def test_windows(self):
        with patch.object(command_contract.sys, "platform", "win32"):
            assert detect_os() == "windows"

    def test_linux(self):
        with patch.object(command_contract.sys, "platform", "linux"):
            assert detect_os() == "linux"

    def test_known_values_are_in_vocab(self):
        for platform_name in ("darwin", "win32", "linux"):
            with patch.object(command_contract.sys, "platform", platform_name):
                assert detect_os() in OS_VALUES

    def test_os_version_is_coarse_or_none(self):
        version = detect_os_version()
        assert version is None or ("." not in version)


class TestDetectSource:
    def test_pypi_when_not_frozen(self):
        with (
            patch.object(command_contract.sys, "frozen", False, create=True),
            patch("runlayer_cli.runtime.is_aiwatch_runtime", return_value=False),
        ):
            assert detect_source() == "runlayer-pypi"

    def test_runlayer_binary_when_frozen_not_aiwatch(self):
        with (
            patch.object(command_contract.sys, "frozen", True, create=True),
            patch("runlayer_cli.runtime.is_aiwatch_runtime", return_value=False),
        ):
            assert detect_source() == "runlayer-binary"

    def test_aiwatch_binary_when_aiwatch_runtime(self):
        with patch("runlayer_cli.runtime.is_aiwatch_runtime", return_value=True):
            assert detect_source() == "aiwatch-binary"

    def test_result_is_in_vocab(self):
        assert detect_source() in SOURCES
