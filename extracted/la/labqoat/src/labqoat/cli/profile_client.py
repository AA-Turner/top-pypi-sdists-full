"""The management client code outside the CLI acts as when it names none: the CLI's own, as the CLI resolves it."""

from labqoat.cli.auth.credential_resolver import CredentialResolver
from labqoat.cli.config.profile_store import ProfileStore
from labqoat.client import Client
from labqoat.projects.project_selection import ProjectSelection


class ProfileClient:
    """Build the client the CLI's default profile, its saved credentials and the selected project describe.

    Credentials come from ``LABQOAT_USERNAME`` and ``LABQOAT_PASSWORD`` or the keyring, never from a prompt; the
    project from ``LABQOAT_PROJECT``, then the nearest ``pyproject.toml``; with neither, no project is sent.
    """

    @staticmethod
    def default(store: ProfileStore | None = None, resolver: CredentialResolver | None = None) -> Client:
        """Return the client of the default profile, failing with the CLI's advice when it has no credentials."""
        profile = (store or ProfileStore()).load("default")
        credentials = (resolver or CredentialResolver()).resolve(profile, prompt=False)
        return Client(
            profile.base_url,
            credentials.username,
            credentials.password,
            timeout_seconds=profile.timeout_seconds,
            environment=profile.environment,
            project=ProjectSelection.resolve().name,
        )
