"""
Connection providers: the one seam that knows WHERE connection definitions come from.

:class:`~sagemaker_studio.connections.ConnectionService` resolves every connection through a
provider, and so does a :class:`~sagemaker_studio.connections.connection.Connection` when it
fetches itself again for credentials. Which provider is decided once, when the service is built:
by default :mod:`~sagemaker_studio.connections.providers.datazone`, the DataZone calls every
existing caller relies on (SageMaker Unified Studio spaces and any other remote kernel). An AWS
Notebook local kernel has no DataZone in the picture, so it injects the provider that asks the
desktop app's local API (:mod:`~sagemaker_studio.connections.providers.app_api`), which answers
the record and its credentials the way ``GetConnection`` ``withSecret`` does. Nothing downstream
branches on the mode for a lookup.

Records are plain mappings in DataZone's ``GetConnection`` wire shape (``connectionId``,
``name``, ``type``, ``props``, ``physicalEndpoints``, optional ``connectionCredentials`` ...).
Everything downstream -- :class:`~sagemaker_studio.connections.connection.Connection`, its
documented ``.data`` surface, the SQL helpers -- consumes that shape already, so a provider
that emits it needs no consumer changes. Keeping the record a mapping (rather than a typed
wrapper that consumers unwrap anyway) is deliberate: the wire shape IS the contract here.

Providers must not log a record wholesale: ``connectionCredentials`` carries live secrets.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional, Protocol, Sequence, runtime_checkable

ConnectionRecord = Mapping[str, Any]


class ConnectionNotFoundError(LookupError):
    """No connection matches the requested identifier, name or type."""


class ConnectionAccessError(RuntimeError):
    """The connection exists but could not be fetched (permissions, malformed definition ...)."""


@runtime_checkable
class ConnectionProvider(Protocol):
    """
    Source of connection records for one scope.

    The ``get_*`` lookups raise :class:`ConnectionNotFoundError` when nothing matches and
    :class:`ConnectionAccessError` when a match could not be fetched, so callers handle one
    pair of error types regardless of provider. ``ConnectionService`` translates both into the
    exception types its public API has always raised. Errors from the
    :mod:`sagemaker_studio.exceptions` context hierarchy (no credentials, a lookup the provider
    cannot do) pass through untranslated so kernels can act on their type. One exception, kept
    for compatibility: the DataZone provider's ``get_connection_by_id`` raises DataZone's
    ``ClientError``, which ``ConnectionService.get_connection_by_id`` has always documented.

    Method bodies below are docstrings only (not ``...``) so coverage tooling does not count
    the Protocol as unexecuted statements.
    """

    #: Whether asking for a connection again shortly before its credentials' ``expiration``
    #: yields fresh credentials. True for the AWS Notebook app, which vends them from the user's
    #: current session, so connections re-ask before theirs lapse and the AWS clients built on
    #: them refresh themselves. False for DataZone, whose connections keep the credentials they
    #: were vended, as they always have.
    refreshes_credentials: bool

    @property
    def name(self) -> str:
        """Stable provider identifier, e.g. ``"datazone"``, ``"aws-notebook-app"``."""

    @property
    def domain_id(self) -> Optional[str]:
        """Domain identifier this provider is scoped to, or ``None`` when it has none."""

    @property
    def project_id(self) -> Optional[str]:
        """Project identifier this provider is scoped to, or ``None`` when it has none."""

    def get_connection_by_id(
        self, connection_id: str, with_secret: bool = True
    ) -> ConnectionRecord:
        """
        Retrieve a connection by identifier: ``GetConnection``, ``withSecret`` by default so the
        record carries ``connectionCredentials`` when the source has them.
        """

    def get_connection_by_name(self, name: str) -> ConnectionRecord:
        """Retrieve a connection by name, with credentials when the source has them."""

    def get_connection_by_type(self, connection_type: str) -> ConnectionRecord:
        """Retrieve the provider's default connection of a type."""

    def list_connections(self) -> Sequence[ConnectionRecord]:
        """List every connection in scope, without credentials."""


__all__ = [
    "ConnectionAccessError",
    "ConnectionNotFoundError",
    "ConnectionProvider",
    "ConnectionRecord",
]
