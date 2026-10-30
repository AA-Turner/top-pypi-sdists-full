"""
Connection provider backed by DataZone, the source of a SageMaker Unified Studio project's
connections.

This is the provider :class:`~sagemaker_studio.connections.ConnectionService` builds when none is
injected, so every remote kernel resolves connections through it. Its lookups are the DataZone
calls the service made inline before providers existed (``ListConnections`` filtered by name or
type followed by ``GetConnection`` ``withSecret``, paginated ``ListConnections`` for listings),
and it raises what those calls raised:

* ``get_connection_by_id`` re-raises DataZone's ``ClientError`` (code and message kept), the
  documented contract of ``ConnectionService.get_connection_by_id``.
* ``get_connection_by_name`` / ``get_connection_by_type`` raise
  :class:`~sagemaker_studio.connections.providers.ConnectionNotFoundError` when the listing is
  empty and :class:`~sagemaker_studio.connections.providers.ConnectionAccessError` when the
  matched connection cannot be fetched, with the messages the service always surfaced as
  ``AttributeError`` / ``RuntimeError``. A failing ``ListConnections`` propagates as the
  ``ClientError`` it is.
* ``list_connections`` raises ``ConnectionAccessError`` when ``ListConnections`` fails.

Records are DataZone's own responses, so nothing is normalized.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Sequence

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from sagemaker_studio.connections.providers import (
    ConnectionAccessError,
    ConnectionNotFoundError,
    ConnectionRecord,
)
from sagemaker_studio.exceptions import AWSClientException

logger = logging.getLogger(__name__)

PROVIDER_NAME = "datazone"

_DEFAULT_SPARK_CONNECT_CONNECTION_NAMES = [
    "default.athena.spark",
    "serverless.spark",
]


class DataZoneConnectionProvider:
    """
    :class:`~sagemaker_studio.connections.providers.ConnectionProvider` over a DataZone client.

    Args:
        datazone_api: The DataZone client.
        domain_id: The domain the connections belong to (``domainIdentifier``).
        project_id: The project the connections belong to (``projectIdentifier``).
    """

    #: DataZone-vended credentials are used until they lapse, as they always were.
    refreshes_credentials = False

    def __init__(
        self,
        datazone_api: Optional[BaseClient],
        domain_id: Optional[str],
        project_id: Optional[str],
    ):
        self._datazone_api = datazone_api
        self._domain_id = domain_id
        self._project_id = project_id

    @property
    def name(self) -> str:
        return PROVIDER_NAME

    @property
    def domain_id(self) -> Optional[str]:
        return self._domain_id

    @property
    def project_id(self) -> Optional[str]:
        return self._project_id

    def get_connection_by_id(
        self, connection_id: str, with_secret: bool = True
    ) -> ConnectionRecord:
        """
        ``GetConnection`` for ``connection_id``, ``withSecret`` by default.

        Raises:
            ClientError: DataZone refused or does not know the connection; re-raised with its
                error code and message, as ``ConnectionService.get_connection_by_id`` documents.
        """
        try:
            return self._datazone_api.get_connection(  # type: ignore
                domainIdentifier=self._domain_id,
                identifier=connection_id,
                withSecret=with_secret,
            )
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_message = e.response.get("Error", {}).get("Message", str(e))
            raise ClientError(
                error_response={"Error": {"Code": error_code, "Message": error_message}},
                operation_name=e.operation_name,
            ) from e

    def get_connection_by_name(self, name: str) -> ConnectionRecord:
        connections = self._list(name=name)
        if not connections:
            raise ConnectionNotFoundError(f"No connection found with name '{name}'")
        return self._get_with_secret(connections[0].get("connectionId"), f"'{name}'")

    def get_connection_by_type(self, connection_type: str) -> ConnectionRecord:
        """
        The project's default connection of ``connection_type``: the first one listed, except that
        ``SPARK_CONNECT`` prefers the Athena connection (identified by ``athenaProperties`` in
        ``props``), and among several of those the well-known default name.
        """
        connections = self._list(type=connection_type)
        if not connections:
            raise ConnectionNotFoundError(f"No connection found with type '{connection_type}'")
        connection_id = connections[0].get("connectionId")
        if connection_type == "SPARK_CONNECT":
            athena_candidates = [c for c in connections if "athenaProperties" in c.get("props", {})]
            if athena_candidates:
                default = next(
                    (
                        c
                        for c in athena_candidates
                        if c.get("name") in _DEFAULT_SPARK_CONNECT_CONNECTION_NAMES
                    ),
                    athena_candidates[0],
                )
                connection_id = default.get("connectionId")
                logger.info(
                    f"Resolved default Athena Spark Connect connection: id={connection_id}, name={default.get('name')}"
                )
            else:
                logger.info(
                    f"No Athena connection (athenaProperties) found among {len(connections)} SPARK_CONNECT connections, using first: id={connection_id}"
                )
        return self._get_with_secret(connection_id, f"'{connection_id}'")

    def list_connections(self) -> Sequence[ConnectionRecord]:
        """Every connection of the project, as ``ListConnections`` summaries (no credentials)."""
        records: List[ConnectionRecord] = []
        next_token = None
        first_call = True
        try:
            while next_token is not None or first_call:
                first_call = False
                params: Dict[str, Any] = {
                    "domainIdentifier": self._domain_id,
                    "projectIdentifier": self._project_id,
                }
                if next_token:
                    params["nextToken"] = next_token
                response = self._datazone_api.list_connections(**params)  # type: ignore
                records.extend(response.get("items", []))
                next_token = response.get("nextToken")
        except ClientError as e:
            raise ConnectionAccessError(
                f"Encountered an error while listing connections for project: {self._project_id} in domain: {self._domain_id}, {AWSClientException(e)}"
            ) from e
        return records

    def _list(self, **filters: Any) -> List[ConnectionRecord]:
        """The first page of ``ListConnections`` under ``filters``; a ``ClientError`` propagates."""
        response = self._datazone_api.list_connections(  # type: ignore
            domainIdentifier=self._domain_id, projectIdentifier=self._project_id, **filters
        )
        return list(response.get("items", []))

    def _get_with_secret(self, connection_id: Any, label: str) -> ConnectionRecord:
        """``GetConnection`` ``withSecret`` for a listed connection; a refusal names ``label``."""
        try:
            return self._datazone_api.get_connection(  # type: ignore
                domainIdentifier=self._domain_id, identifier=connection_id, withSecret=True
            )
        except ClientError as e:
            raise ConnectionAccessError(
                f"Unable to access connection {label}, {AWSClientException(e)}"
            ) from e

    def __repr__(self) -> str:
        return (
            f"DataZoneConnectionProvider(domain={self._domain_id!r}, project={self._project_id!r})"
        )


__all__ = ["PROVIDER_NAME", "DataZoneConnectionProvider"]
