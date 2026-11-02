"""Exception hierarchy. Everything raised by this package derives from LakehouseError."""

from __future__ import annotations


class LakehouseError(Exception):
    """Base for every error this package raises."""


class ConfigurationError(LakehouseError):
    """Settings are missing, incomplete, or mutually inconsistent."""


class ConnectionNotConfigured(ConfigurationError):
    """A named Airflow connection could not be resolved.

    Raised rather than silently falling back to local storage: a typo'd conn_id
    or an expired secret must fail the task, not redirect a production write to
    an ephemeral pod filesystem.
    """

    def __init__(self, conn_id: str, reason: str = "") -> None:
        """Record the ``conn_id`` and an optional human-readable ``reason``."""
        self.conn_id = conn_id
        self.reason = reason
        suffix = f": {reason}" if reason else ""
        super().__init__(f"Airflow connection {conn_id!r} could not be resolved{suffix}")


class AuthenticationError(LakehouseError):
    """Acquiring an access token failed."""


class RemoteSigningUnavailable(LakehouseError):
    """Remote-signed object storage was requested but the runtime cannot do it.

    Usually means `obstore-databaas` is not installed: `RemoteSignedS3Store`
    ships only in that distribution, and it shares the top-level module name
    `obstore` with upstream obstore.
    """


class SignError(LakehouseError):
    """Lakekeeper's signer refused or failed to sign a request."""
