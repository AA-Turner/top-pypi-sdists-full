"""Credential precedence: flags, environment, keyring, then prompt."""

from __future__ import annotations

import os
from urllib.parse import urlsplit

from labqoat.cli.auth.credentials import Credentials
from labqoat.cli.auth.keyring_store import KeyringStore
from labqoat.cli.config.profile import Profile


class CredentialResolver:
    """Resolve credentials without putting passwords in history."""

    def __init__(self, store: KeyringStore | None = None) -> None:
        """Inject the keyring adapter, defaulting to the OS backend."""
        self._store = store if store is not None else KeyringStore.default()

    def resolve(
        self,
        profile: Profile,
        username: str | None = None,
        password: str | None = None,
        prompt: bool = True,
    ) -> Credentials:
        """Apply flag, environment, keyring, and prompt precedence."""
        name = username if username is not None else self.env_username(profile)
        secret = password if password is not None else self.env_password()
        if name and secret:
            return Credentials(username=name, password=secret)
        saved = self.saved_password(profile, name) if name else None
        if saved is not None and name is not None:
            return Credentials(username=name, password=saved)
        if prompt:
            return self.prompt_credentials(profile, name)
        raise CredentialResolver.missing_error(profile)

    def saved_password(self, profile: Profile, username: str) -> str | None:
        """Read the keyring without prompting."""
        return self._store.load(self.origin(profile.base_url), profile.name, username)

    def store_password(self, profile: Profile, username: str, password: str) -> None:
        """Persist a verified password in the keyring."""
        self._store.save(self.origin(profile.base_url), profile.name, username, password)

    def delete_password(self, profile: Profile, username: str) -> None:
        """Forget a stored password."""
        self._store.delete(self.origin(profile.base_url), profile.name, username)

    def origin(self, base_url: str) -> str:
        """Normalize an API origin for credential scoping."""
        parts = urlsplit(base_url)
        host = parts.hostname or ""
        port = f":{parts.port}" if parts.port else ""
        return f"{parts.scheme}://{host}{port}"

    def env_username(self, profile: Profile) -> str | None:
        """Prefer explicit environment usernames over profiles."""
        return os.environ.get("LABQOAT_USERNAME") or profile.username or None

    def env_password(self) -> str | None:
        """Read one-command environment passwords."""
        return os.environ.get("LABQOAT_PASSWORD")

    def prompt_credentials(self, profile: Profile, username: str | None) -> Credentials:
        """Prompt for missing values without echoing the password."""
        import click

        resolved_name = username or click.prompt("Username", default=profile.username or "", err=True)
        secret: str = click.prompt("Password", hide_input=True, confirmation_prompt=False, err=True)
        return Credentials(username=resolved_name, password=secret)

    @staticmethod
    def missing_error(profile: Profile) -> Exception:
        """Explain how to provide credentials non-interactively."""
        from labqoat.cli.output.cli_failure import CliFailure

        return CliFailure(
            f"No credentials for profile {profile.name!r}. "
            "Set LABQOAT_USERNAME/LABQOAT_PASSWORD or run 'labqoat auth login'.",
            1,
        )
