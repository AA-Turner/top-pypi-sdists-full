"""Tests for the frozen-darwin keychain service split.

Frozen *aiwatch* on macOS writes to `runlayer-aiwatch` so the .pkg doesn't
inherit a stale ACL from any pre-existing `runlayer-cli/<host_key>` item
left behind by an older `uvx runlayer` install (different Designated
Requirement => macOS auth prompt). The full frozen `runlayer` bundle
codesigns with a different identifier (`com.runlayer.cli`) and stays on
`runlayer-cli`, as do dev / Linux / Windows so existing users see no churn.
"""

from unittest.mock import patch

from runlayer_cli.credential_store import KeyringCredentialStore, _service_name

_AIWATCH_EXE = "/usr/local/lib/runlayer/aiwatch/aiwatch"
_RUNLAYER_EXE = "/usr/local/lib/runlayer/runlayer/runlayer"


class TestServiceName:
    def test_frozen_darwin_aiwatch_returns_aiwatch(self):
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.frozen = True
            mock_sys.executable = _AIWATCH_EXE
            assert _service_name() == "runlayer-aiwatch"

    def test_frozen_darwin_full_cli_returns_cli(self):
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.frozen = True
            mock_sys.executable = _RUNLAYER_EXE
            assert _service_name() == "runlayer-cli"

    def test_frozen_linux_aiwatch_returns_cli(self):
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "linux"
            mock_sys.frozen = True
            mock_sys.executable = _AIWATCH_EXE
            assert _service_name() == "runlayer-cli"

    def test_frozen_windows_aiwatch_returns_cli(self):
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "win32"
            mock_sys.frozen = True
            mock_sys.executable = _AIWATCH_EXE
            assert _service_name() == "runlayer-cli"

    def test_dev_darwin_returns_cli(self):
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.executable = "/usr/bin/python3"
            del mock_sys.frozen
            assert _service_name() == "runlayer-cli"


class TestSetSecretUsesServiceName:
    def test_set_secret_frozen_darwin_aiwatch_writes_aiwatch_service(self):
        store = KeyringCredentialStore()
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.frozen = True
            mock_sys.executable = _AIWATCH_EXE
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-aiwatch", "example.com", "s")

    def test_set_secret_frozen_darwin_full_cli_writes_cli_service(self):
        store = KeyringCredentialStore()
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.frozen = True
            mock_sys.executable = _RUNLAYER_EXE
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-cli", "example.com", "s")

    def test_set_secret_dev_darwin_writes_cli_service(self):
        store = KeyringCredentialStore()
        with patch("runlayer_cli.credential_store.sys") as mock_sys:
            mock_sys.platform = "darwin"
            mock_sys.executable = "/usr/bin/python3"
            del mock_sys.frozen
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-cli", "example.com", "s")
