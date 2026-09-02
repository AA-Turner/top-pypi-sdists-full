"""Tests for the frozen-darwin keychain service split.

Frozen *aiwatch* on macOS writes to `runlayer-aiwatch` so the .pkg doesn't
inherit a stale ACL from any pre-existing `runlayer-cli/<host_key>` item
left behind by an older `uvx runlayer` install (different Designated
Requirement => macOS auth prompt). The full frozen `runlayer` bundle
codesigns with a different identifier (`com.runlayer.cli`) and stays on
`runlayer-cli`, as do dev / Linux / Windows so existing users see no churn.
"""

from contextlib import contextmanager
from unittest.mock import patch

from runlayer_cli.credential_store import KeyringCredentialStore, _service_name

_AIWATCH_EXE = "/usr/local/lib/runlayer/aiwatch/aiwatch"
_RUNLAYER_EXE = "/usr/local/lib/runlayer/runlayer/runlayer"


@contextmanager
def _patch_sys(platform: str, executable: str, frozen: bool):
    """Patch ``sys`` in both modules that drive the service-name decision.

    ``_service_name`` reads ``sys.platform`` from ``credential_store`` and
    delegates the frozen-bundle check to ``runtime.is_frozen_aiwatch_bundle``,
    which reads ``sys`` from ``runtime`` — so both must be patched in sync.
    """
    with (
        patch("runlayer_cli.credential_store.sys") as cred_sys,
        patch("runlayer_cli.runtime.sys") as rt_sys,
    ):
        for mock_sys in (cred_sys, rt_sys):
            mock_sys.platform = platform
            mock_sys.executable = executable
            if frozen:
                mock_sys.frozen = True
            else:
                del mock_sys.frozen
        yield


class TestServiceName:
    def test_frozen_darwin_aiwatch_returns_aiwatch(self):
        with _patch_sys("darwin", _AIWATCH_EXE, frozen=True):
            assert _service_name() == "runlayer-aiwatch"

    def test_frozen_darwin_full_cli_returns_cli(self):
        with _patch_sys("darwin", _RUNLAYER_EXE, frozen=True):
            assert _service_name() == "runlayer-cli"

    def test_frozen_linux_aiwatch_returns_cli(self):
        with _patch_sys("linux", _AIWATCH_EXE, frozen=True):
            assert _service_name() == "runlayer-cli"

    def test_frozen_windows_aiwatch_returns_cli(self):
        with _patch_sys("win32", _AIWATCH_EXE, frozen=True):
            assert _service_name() == "runlayer-cli"

    def test_dev_darwin_returns_cli(self):
        with _patch_sys("darwin", "/usr/bin/python3", frozen=False):
            assert _service_name() == "runlayer-cli"


class TestSetSecretUsesServiceName:
    def test_set_secret_frozen_darwin_aiwatch_writes_aiwatch_service(self):
        store = KeyringCredentialStore()
        with _patch_sys("darwin", _AIWATCH_EXE, frozen=True):
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-aiwatch", "example.com", "s")

    def test_set_secret_frozen_darwin_full_cli_writes_cli_service(self):
        store = KeyringCredentialStore()
        with _patch_sys("darwin", _RUNLAYER_EXE, frozen=True):
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-cli", "example.com", "s")

    def test_set_secret_dev_darwin_writes_cli_service(self):
        store = KeyringCredentialStore()
        with _patch_sys("darwin", "/usr/bin/python3", frozen=False):
            with patch("keyring.set_password") as mock_set:
                assert store.set_secret("example.com", "s") is True
        mock_set.assert_called_once_with("runlayer-cli", "example.com", "s")
