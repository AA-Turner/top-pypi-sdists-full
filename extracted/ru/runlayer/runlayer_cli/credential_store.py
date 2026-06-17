"""Keyring helpers for Runlayer CLI."""

import sys

import keyring
import keyring.backends.fail
import keyring.errors
import typer

from runlayer_cli.runtime import is_frozen_aiwatch_bundle


def _service_name() -> str:
    """Keychain service name. Splits the frozen-darwin *aiwatch* bundle off
    `runlayer-cli` so the aiwatch .pkg writes to a service with no legacy ACL,
    killing the macOS auth prompt on install / every `aiwatch hook` fire.

    The full `runlayer` frozen bundle (`runlayer.spec`) codesigns with a
    different identifier (`com.runlayer.cli`) and must NOT inherit the aiwatch
    service — so gate on the bundle's exe name, not just `sys.frozen`. Dev
    `uvx runlayer`, Linux, and Windows keep `runlayer-cli` untouched."""
    if sys.platform == "darwin" and is_frozen_aiwatch_bundle():
        return "runlayer-aiwatch"
    return "runlayer-cli"


class KeyringCredentialStore:
    """Stores secrets in the OS credential store via the keyring library."""

    def get_secret(self, host_key: str) -> str | None:
        try:
            return keyring.get_password(_service_name(), host_key)
        except keyring.errors.KeyringLocked:
            return None
        except keyring.errors.KeyringError:
            return None

    def set_secret(self, host_key: str, secret: str) -> bool:
        try:
            keyring.set_password(_service_name(), host_key, secret)
            return True
        except keyring.errors.KeyringError:
            typer.secho(
                "Warning: Failed to save credentials to the system credential store.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            return False

    def delete_secret(self, host_key: str) -> bool:
        """Delete a secret. Returns True when the secret is gone from the store.

        A missing entry (``PasswordDeleteError``) counts as success — the secret
        is already absent. Any other ``KeyringError`` (locked keychain, denied
        ACL prompt) returns False: the secret may still be there, so callers must
        not claim the credential was cleared.
        """
        try:
            keyring.delete_password(_service_name(), host_key)
            return True
        except keyring.errors.PasswordDeleteError:
            return True
        except keyring.errors.KeyringError:
            return False

    def delete_all_secrets(self, host_keys: list[str]) -> None:
        for key in host_keys:
            self.delete_secret(key)


_cached_store: KeyringCredentialStore | None = None
_keyring_probe_failed = False
_keyring_warning_shown = False


def get_keyring_store() -> KeyringCredentialStore | None:
    """Return keyring store if available, else None.

    Result is cached for the process lifetime.
    """
    global _cached_store, _keyring_probe_failed, _keyring_warning_shown

    if _cached_store is not None:
        return _cached_store
    if _keyring_probe_failed:
        return None

    try:
        backend = keyring.get_keyring()
        if isinstance(backend, keyring.backends.fail.Keyring):
            raise RuntimeError("null keyring backend")

        # Smoke test: try a get to verify the backend works
        keyring.get_password(_service_name(), "__probe__")
        _cached_store = KeyringCredentialStore()
    except Exception:
        _keyring_probe_failed = True
        if not _keyring_warning_shown:
            typer.secho(
                "Warning: System credential store unavailable. Credentials will be stored in ~/.runlayer/config.yaml.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            _keyring_warning_shown = True
        return None

    return _cached_store


def reset_credential_store() -> None:
    """Reset cached keyring store. Used in tests."""
    global _cached_store, _keyring_probe_failed, _keyring_warning_shown
    _cached_store = None
    _keyring_probe_failed = False
    _keyring_warning_shown = False
