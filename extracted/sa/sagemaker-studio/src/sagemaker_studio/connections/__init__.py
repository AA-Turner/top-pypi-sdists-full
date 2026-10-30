import logging
from dataclasses import dataclass
from typing import Callable, List, Optional

from botocore.client import BaseClient

from sagemaker_studio.connections.connection import Connection
from sagemaker_studio.connections.providers import (
    ConnectionAccessError,
    ConnectionNotFoundError,
    ConnectionProvider,
    ConnectionRecord,
)
from sagemaker_studio.connections.providers.datazone import DataZoneConnectionProvider
from sagemaker_studio.data_models import ClientConfig

logger = logging.getLogger(__name__)


@dataclass
class ConnectionService:
    """
    Provides methods for interacting with connections within a SageMaker Unified Studio project.

    Every lookup goes through one
    :class:`~sagemaker_studio.connections.providers.ConnectionProvider` and wraps the wire-shaped record it answers in a :class:`Connection`. The provider is
    :class:`~sagemaker_studio.connections.providers.datazone.DataZoneConnectionProvider` over
    ``datazone_api`` unless one is injected (an AWS Notebook local kernel injects the app's).

    Args:
        project_id (str): The unique identifier of the project.
        domain_id (str): The unique identifier of the domain.
        datazone_api (BaseClient): The DataZone client.
        glue_api (BaseClient): The Glue client.
        provider: Optional :class:`~sagemaker_studio.connections.providers.ConnectionProvider`
            used instead of DataZone (an AWS Notebook local kernel, or tests).
    """

    def __init__(
        self,
        project_id: str,
        domain_id: str,
        datazone_api: Optional[BaseClient],
        glue_api: BaseClient,
        secrets_manager_api: BaseClient,
        kms_api: BaseClient,
        project_config: ClientConfig,
        provider: Optional[ConnectionProvider] = None,
    ):
        """
        Initializes a new instance of the ConnectionService class.

        Args:
            project_id (str): The unique identifier of the project.
            domain_id (str): The unique identifier of the domain.
            datazone_api (BaseClient): The DataZone client. May be ``None`` when a ``provider``
                is supplied.
            glue_api (BaseClient): The Glue client.
            kms_api (BaseClient): The KMS client.
            provider: Optional connection provider. When omitted, connections resolve
                through ``datazone_api`` exactly as before.
        """
        self.project_id = project_id
        self.domain_id = domain_id
        self.datazone_api = datazone_api
        self.glue_api = glue_api
        self.secrets_manager_api = secrets_manager_api
        self.project_config = project_config
        self.kms_api = kms_api
        self.provider: ConnectionProvider = (
            provider
            if provider is not None
            else DataZoneConnectionProvider(datazone_api, domain_id, project_id)
        )

    def _to_connection(self, record: ConnectionRecord) -> Connection:
        """
        Wrap a provider record (DataZone wire shape) in the public Connection type.

        The connection keeps the provider so it can fetch itself again (``GetConnection``
        ``withSecret``) when it needs credentials it does not have.
        """
        return Connection(
            connection_data=dict(record),
            glue_api=self.glue_api,
            datazone_api=self.datazone_api,
            secrets_manager_api=self.secrets_manager_api,
            kms_api=self.kms_api,
            project_config=self.project_config,
            provider=self.provider,
        )

    def _resolve(self, lookup: Callable[[], ConnectionRecord]) -> Connection:
        """Run a provider lookup, translating its errors into the public API's types."""
        try:
            return self._to_connection(lookup())
        except ConnectionNotFoundError as e:
            raise AttributeError(str(e))
        except ConnectionAccessError as e:
            raise RuntimeError(str(e))

    def get_connection_by_name(self, name: str) -> Connection:
        """
        Retrieves a connection by its name.

        Args:
            name (str): The name of the connection.

        Returns:
            Connection: The connection object.

        Raises:
            AttributeError: If no connection is found with the specified name.
            RuntimeError: If the user does not have access to the connection.
        """
        return self._resolve(lambda: self.provider.get_connection_by_name(name))

    def get_connection_by_id(self, connection_id: str) -> Connection:
        """
        Retrieves a connection by its ID.

        Args:
            connection_id (str): The ID of the connection.

        Returns:
            Connection: The connection object.

        Raises:
            ClientError: If the user does not have access to the connection or if the connection is not found.
        """
        # No error translation here on purpose: DataZone raises ClientError for both "not found"
        # and "denied", so another provider's LookupError/RuntimeError are the closest
        # equivalents and are left as they are.
        return self._to_connection(self.provider.get_connection_by_id(connection_id))

    def get_connection_by_type(self, type: str) -> Connection:
        """
        Retrieves a connection by its type.

        For SPARK_CONNECT, prefers the Athena connection (identified by athenaProperties in props)
        as the default fallback. Falls back to the first connection if no Athena connection is found.

        Args:
            type (str): The type of the connection.

        Returns:
            Connection: The connection object.

        Raises:
            AttributeError: If no connection is found with the specified type.
            RuntimeError: If the user does not have access to the connection.
        """
        return self._resolve(lambda: self.provider.get_connection_by_type(type))

    def list_connection_records(self) -> List[ConnectionRecord]:
        """
        Retrieves the project's connections as the provider answers them: one record per
        connection in the DataZone wire shape, not wrapped in :class:`Connection` and carrying no
        credentials (for ``sqlutils.attach_local_catalogs()``).

        Returns:
            List[ConnectionRecord]: The connection records.

        Raises:
            RuntimeError: If the user does not have access to the project's connections.
        """
        try:
            return list(self.provider.list_connections())
        except ConnectionAccessError as e:
            raise RuntimeError(str(e))

    def list_connections(self) -> List[Connection]:
        """
        Retrieves a list of all connections in the project.

        Returns:
            List[Connection]: A list of connection objects.

        Raises:
            RuntimeError: If the user does not have access to the project's connections.
        """
        return [self._to_connection(record) for record in self.list_connection_records()]
