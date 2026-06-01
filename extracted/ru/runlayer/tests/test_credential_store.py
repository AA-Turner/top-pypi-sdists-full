"""Tests for keyring availability and fallback behavior."""

from unittest.mock import MagicMock, patch

import keyring.backends.fail
import keyring.errors
import pytest

from runlayer_cli.credential_store import (
    SERVICE_NAME,
    KeyringCredentialStore,
    get_keyring_store,
    reset_credential_store,
)


@pytest.fixture(autouse=True)
def _reset_store():
    reset_credential_store()
    yield
    reset_credential_store()


class TestKeyringCredentialStore:
    def test_set_secret_failure_signals_file_fallback(self):
        store = KeyringCredentialStore()
        with patch(
            "keyring.set_password",
            side_effect=keyring.errors.PasswordSetError("locked"),
        ):
            assert store.set_secret("example.com", "x") is False

    def test_get_secret_locked_falls_back_to_yaml(self):
        store = KeyringCredentialStore()
        with patch(
            "keyring.get_password",
            side_effect=keyring.errors.KeyringLocked("locked"),
        ):
            assert store.get_secret("example.com") is None


class TestGetKeyringStore:
    def test_returns_singleton_when_backend_works(self):
        mock_backend = MagicMock()
        with patch(
            "keyring.get_keyring", return_value=mock_backend
        ) as mock_get_keyring:
            with patch("keyring.get_password", return_value=None):
                a = get_keyring_store()
                b = get_keyring_store()
                assert isinstance(a, KeyringCredentialStore)
                assert a is b
                mock_get_keyring.assert_called_once()

    def test_returns_none_for_fail_backend(self):
        with patch("keyring.get_keyring", return_value=keyring.backends.fail.Keyring()):
            assert get_keyring_store() is None

    def test_probe_failure_cached_with_single_warning(self):
        mock_backend = MagicMock()
        with (
            patch("keyring.get_keyring", return_value=mock_backend),
            patch(
                "keyring.get_password",
                side_effect=keyring.errors.KeyringError("dbus unavailable"),
            ) as mock_get_password,
            patch("typer.secho") as mock_secho,
        ):
            assert get_keyring_store() is None
            assert get_keyring_store() is None

        mock_get_password.assert_called_once_with(SERVICE_NAME, "__probe__")
        mock_secho.assert_called_once()
