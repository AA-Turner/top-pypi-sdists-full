"""Secure OS keyring access for CLI passwords."""

from __future__ import annotations

from labqoat.cli.auth.keyring_backend import KeyringBackend
from labqoat.errors.credential_store_error import CredentialStoreError


class KeyringStore:
    """Password storage keyed by API origin, profile, and username."""

    def __init__(self, backend: KeyringBackend) -> None:
        """Inject the keyring module backing this store."""
        self._backend = backend

    @staticmethod
    def default() -> KeyringStore:
        """Build a store on the real OS keyring."""
        import keyring

        return KeyringStore(backend=keyring)

    def service_name(self, origin: str, profile: str) -> str:
        """Derive the keyring service name for an origin and profile."""
        return f"labqoat:{profile}@{origin}"

    def save(self, origin: str, profile: str, username: str, password: str) -> None:
        """Store a password, verifying a secure backend first."""
        import keyring.errors

        self.ensure_backend()
        try:
            self._backend.set_password(self.service_name(origin, profile), username, password)
        except keyring.errors.KeyringError as error:
            raise CredentialStoreError("Could not save credentials.") from error

    def load(self, origin: str, profile: str, username: str) -> str | None:
        """Load a password, returning None when absent."""
        import keyring.errors

        self.ensure_backend()
        try:
            password = self._backend.get_password(self.service_name(origin, profile), username)
        except keyring.errors.KeyringError as error:
            raise CredentialStoreError("Could not read credentials.") from error
        if password is None:
            return None
        return str(password)

    def delete(self, origin: str, profile: str, username: str) -> None:
        """Forget a stored password, ignoring absent entries."""
        import keyring.errors

        self.ensure_backend()
        try:
            self._backend.delete_password(self.service_name(origin, profile), username)
        except keyring.errors.PasswordDeleteError:
            return
        except keyring.errors.KeyringError as error:
            raise CredentialStoreError("Could not delete credentials.") from error

    def ensure_backend(self) -> None:
        """Fail when no secure backend is available."""
        try:
            self._backend.get_keyring()
        except Exception as error:
            raise CredentialStoreError("No secure credential backend is available.") from error
