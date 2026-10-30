"""
Connection provider backed by the AWS Notebook app's local API.

On a local kernel the app is the control plane: ``connections.get`` answers a connection record in
DataZone's ``GetConnection`` wire shape and, with ``withSecret``, its ``connectionCredentials``;
``connections.list`` answers the records in the signed-in session's scope, without credentials
(none when signed out). The app identifies connections by id only (a name is a label and may hold
dots and spaces), so this provider resolves by id, lists, and refuses lookups by name or type with
:class:`~sagemaker_studio.exceptions.UnsupportedInModeError`. The notebook frontend forwards the
id of the connection attached to a cell, which is what reaches :func:`sagemaker_studio.sqlutils.sql`
as ``connection_id``; the listing is what ``sqlutils.attach_local_catalogs()`` attaches to DuckDB.

Records
-------
The app's rows are DataZone ``ConnectionSummary`` records minus the scope fields that mean
nothing on a laptop (``domainId``, ``domainUnitId``, ``projectId``, ``environmentId``, ``scope``),
plus two local fields: ``store`` (which of the app's files the row came from) and, for Athena,
``catalog``. :func:`normalize_record` fills the scope fields with stand-ins when absent so every
consumer sees a complete record, and passes everything else through.

Connection types the app vends today:

* ``S3``: ``props.s3Properties.s3Uri``. ``physicalEndpoints[0].awsLocation`` may be empty (the
  app's built-in ``default.s3`` names no account or region).
* ``ATHENA``: ``props.athenaProperties.workgroupName`` plus top-level ``catalog``.
* ``LAKEHOUSE`` (the catalog connection that replaces ``ATHENA``): the Athena workgroup to query
  the catalog with is in ``configurations`` as ``{"classification": "athena", "properties":
  {"workgroupName": ...}}``. :func:`athena_workgroup` reads it, and
  :attr:`~sagemaker_studio.connections.connection.Connection.sql_engine_type` reports such a
  connection as ``ATHENA`` so SQL runs on Athena against the catalog.

Credentials
-----------
``connectionCredentials`` is the source of AWS credentials on a local kernel: the SDK asks for it
directly, and DuckDB's ``credential_chain`` secrets reach it through the kernel server's container
credentials endpoint, which answers with the signed-in session's. Signed out, the app answers
``403 AccessDeniedException`` ("Sign in to AWS to use this connection's data."), raised here as
:class:`~sagemaker_studio.exceptions.CredentialsUnavailableError` before any AWS call. The kernel
records the outcome for :func:`sagemaker_studio.local_kernel.current_context`.

This module never logs a record wholesale: ``connectionCredentials`` carries live secrets.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Sequence

from sagemaker_studio.connections.providers import (
    ConnectionAccessError,
    ConnectionNotFoundError,
    ConnectionRecord,
)
from sagemaker_studio.exceptions import (
    CredentialsUnavailableError,
    LocalAppError,
    UnsupportedInModeError,
)
from sagemaker_studio.local_kernel import RuntimeMode

if TYPE_CHECKING:  # pragma: no cover
    from sagemaker_studio.local_kernel import LocalKernel

logger = logging.getLogger(__name__)

PROVIDER_NAME = "aws-notebook-app"

#: Stand-in scope identifiers of a local kernel's connections (the app reports none).
LOCAL_DOMAIN_ID = "dzd-local"
LOCAL_SCOPE_ID = "local"
LOCAL_SCOPE = "PROJECT"
_SCOPE_DEFAULTS = {
    "domainId": LOCAL_DOMAIN_ID,
    "domainUnitId": LOCAL_SCOPE_ID,
    "projectId": LOCAL_SCOPE_ID,
    "environmentId": LOCAL_SCOPE_ID,
    "scope": LOCAL_SCOPE,
}

TYPE_ATHENA = "ATHENA"
TYPE_LAKEHOUSE = "LAKEHOUSE"
#: The ``configurations`` entry of a LAKEHOUSE connection that names its Athena workgroup.
ATHENA_CLASSIFICATION = "athena"

#: What the app answers when the user is signed out and credentials were asked for.
ACCESS_DENIED = "AccessDeniedException"
_NOT_FOUND_CODES = ("ResourceNotFoundException", "ValidationException")

ID_ONLY_DETAIL = (
    "The AWS Notebook app identifies connections by id: pass connection_id=<id> (the notebook "
    "frontend forwards the id of the connection attached to the cell)."
)


def normalize_record(row: Mapping[str, Any]) -> Dict[str, Any]:
    """A copy of an app row with the DataZone scope fields filled in when the app omitted them."""
    record: Dict[str, Any] = dict(row)
    for key, default in _SCOPE_DEFAULTS.items():
        if not record.get(key):
            record[key] = default
    return record


def athena_workgroup(record: Mapping[str, Any]) -> Optional[str]:
    """
    The Athena workgroup a connection record names, if any.

    Looks at ``props.athenaProperties.workgroupName`` (an ``ATHENA`` connection), then at the
    ``athena`` entry of ``configurations`` (a ``LAKEHOUSE`` catalog connection), then at a
    top-level ``connectedWorkgroup``.
    """
    props = record.get("props")
    if isinstance(props, Mapping):
        athena_props = props.get("athenaProperties")
        if isinstance(athena_props, Mapping) and athena_props.get("workgroupName"):
            return str(athena_props["workgroupName"])
    configurations = record.get("configurations")
    if isinstance(configurations, Sequence) and not isinstance(configurations, (str, bytes)):
        for configuration in configurations:
            if not isinstance(configuration, Mapping):
                continue
            if str(configuration.get("classification", "")).lower() != ATHENA_CLASSIFICATION:
                continue
            properties = configuration.get("properties")
            if isinstance(properties, Mapping) and properties.get("workgroupName"):
                return str(properties["workgroupName"])
    connected = record.get("connectedWorkgroup")
    return str(connected) if connected else None


def aws_location(record: Mapping[str, Any]) -> Dict[str, Optional[str]]:
    """``{"account": ..., "region": ...}`` from the first physical endpoint, values ``None`` when absent."""
    endpoints = record.get("physicalEndpoints")
    location: Mapping[str, Any] = {}
    if isinstance(endpoints, Sequence) and endpoints and isinstance(endpoints[0], Mapping):
        found = endpoints[0].get("awsLocation")
        if isinstance(found, Mapping):
            location = found
    return {
        "account": location.get("awsAccountId") or None,
        "region": location.get("awsRegion") or None,
    }


class AppApiConnectionProvider:
    """
    :class:`~sagemaker_studio.connections.providers.ConnectionProvider` over the app's API.

    Args:
        kernel: The local kernel, for its API client and sign-in observation.
    """

    #: The app vends credentials from the user's current session on every request.
    refreshes_credentials = True

    def __init__(self, kernel: "LocalKernel"):
        self._kernel = kernel

    @property
    def name(self) -> str:
        return PROVIDER_NAME

    @property
    def domain_id(self) -> Optional[str]:
        return LOCAL_DOMAIN_ID

    @property
    def project_id(self) -> Optional[str]:
        return LOCAL_SCOPE_ID

    def get_connection_by_id(
        self, connection_id: str, with_secret: bool = True
    ) -> ConnectionRecord:
        """
        ``connections.get`` for ``connection_id``; with ``with_secret`` (the default) the record
        carries ``connectionCredentials``.

        Raises:
            ConnectionNotFoundError: The app knows no such connection (or the id is not an id).
            CredentialsUnavailableError: Credentials were asked for and the app refused them,
                typically because the user is signed out; carries the app's message.
            ConnectionAccessError: Any other refusal by the app.
            LocalAppUnavailableError: The app could not be reached.
        """
        feature = f"Connection {connection_id!r}"
        try:
            row = self._kernel.client.get_connection(connection_id, with_secret=with_secret)
        except LocalAppError as e:
            if e.code == ACCESS_DENIED and with_secret:
                self._kernel.observe_credentials(False, e.detail)
                raise CredentialsUnavailableError(feature, e.detail) from e
            if e.code in _NOT_FOUND_CODES:
                raise ConnectionNotFoundError(f"{feature}: {e.detail}") from e
            raise ConnectionAccessError(str(e)) from e
        if with_secret:
            if not isinstance(row.get("connectionCredentials"), Mapping):
                detail = "the AWS Notebook app returned the connection without credentials"
                self._kernel.observe_credentials(False, detail)
                raise CredentialsUnavailableError(feature, detail)
            self._kernel.observe_credentials(True)
        logger.debug("Resolved %s (%s) through the AWS Notebook app", feature, row.get("type"))
        return normalize_record(row)

    def get_connection_by_name(self, name: str) -> ConnectionRecord:
        raise self._id_only(f"Looking up connection {name!r} by name")

    def get_connection_by_type(self, connection_type: str) -> ConnectionRecord:
        raise self._id_only(f"Looking up a connection by type ({connection_type})")

    def list_connections(self, connection_type: Optional[str] = None) -> Sequence[ConnectionRecord]:
        """
        ``connections.list``: every connection in the signed-in session's scope, without
        credentials, as normalized records; with ``connection_type``, those of that type only.
        Signed out, the app has nothing in scope and the list is empty rather than an error.

        Raises:
            ConnectionAccessError: The app refused the listing.
            LocalAppUnavailableError: The app could not be reached.
        """
        try:
            rows = self._kernel.client.list_connections(connection_type)
        except LocalAppError as e:
            raise ConnectionAccessError(str(e)) from e
        logger.debug("Listed %d connection(s) through the AWS Notebook app", len(rows))
        return [normalize_record(row) for row in rows]

    @staticmethod
    def _id_only(feature: str) -> UnsupportedInModeError:
        return UnsupportedInModeError(
            feature, RuntimeMode.LOCAL, RuntimeMode.REMOTE, ID_ONLY_DETAIL
        )

    def __repr__(self) -> str:
        return f"AppApiConnectionProvider({self._kernel.client!r})"


__all__ = [
    "ACCESS_DENIED",
    "ATHENA_CLASSIFICATION",
    "AppApiConnectionProvider",
    "ID_ONLY_DETAIL",
    "LOCAL_DOMAIN_ID",
    "LOCAL_SCOPE",
    "LOCAL_SCOPE_ID",
    "PROVIDER_NAME",
    "TYPE_ATHENA",
    "TYPE_LAKEHOUSE",
    "athena_workgroup",
    "aws_location",
    "normalize_record",
]
