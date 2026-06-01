"""Keyring helpers for Runlayer CLI."""

import keyring
import keyring.backends.fail
import keyring.errors
import typer

SERVICE_NAME = "runlayer-cli"


class KeyringCredentialStore:
    """Stores secrets in the OS credential store via the keyring library."""

    def get_secret(self, host_key: str) -> str | None:
        try:
            return keyring.get_password(SERVICE_NAME, host_key)
        except keyring.errors.KeyringLocked:
            return None
        except keyring.errors.KeyringError:
            return None

    def set_secret(self, host_key: str, secret: str) -> bool:
        try:
            keyring.set_password(SERVICE_NAME, host_key, secret)
            return True
        except keyring.errors.KeyringError:
            typer.secho(
                "Warning: Failed to save credentials to the system credential store.",
                fg=typer.colors.YELLOW,
                err=True,
            )
            return False

    def delete_secret(self, host_key: str) -> None:
        try:
            keyring.delete_password(SERVICE_NAME, host_key)
        except keyring.errors.KeyringError:
            pass

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
        keyring.get_password(SERVICE_NAME, "__probe__")
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
