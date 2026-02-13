from dataclasses import dataclass, field
from typing import ClassVar, Dict

from anyscale._private.models.model_base import ModelBase, ModelEnum


class ConnectionType(ModelEnum):
    """Type of third-party connection."""

    DATABRICKS = "DATABRICKS"

    __docstrings__: ClassVar[Dict[str, str]] = {
        DATABRICKS: "Databricks connection for Unity Catalog access",
    }


class _ConnectionMethodType:
    """Internal connection method type strings (not user-facing)."""

    DATABRICKS_U2M = "databricks_U2M"


_CONNECTION_METHOD_TO_CONNECTION_TYPE: Dict[str, ConnectionType] = {
    _ConnectionMethodType.DATABRICKS_U2M: ConnectionType.DATABRICKS,  # type: ignore[dict-item]
}


@dataclass(frozen=True)
class ConnectionConfig(ModelBase):
    """Configuration for a third-party connection.

    Connections allow workloads (jobs, workspaces, etc.) to access external services
    like Databricks Unity Catalog. Each connection is identified by its connection
    type and name.

    This feature is in beta preview. Contact [Anyscale support](mailto:support@anyscale.com)
    to request enablement.
    """

    __doc_py_example__ = """\
from anyscale._private.models.integrations import ConnectionConfig, ConnectionType

connection = ConnectionConfig(
    connection_type=ConnectionType.DATABRICKS,
    connection_name="my-databricks-connection",
)
"""

    __doc_yaml_example__ = """\
connections:
  - connection_type: databricks
    connection_name: my-databricks-connection
"""

    connection_type: ConnectionType = field(
        metadata={"docstring": "The type of connection (e.g., DATABRICKS)."},
    )

    def _validate_connection_type(
        self, connection_type: ConnectionType
    ) -> ConnectionType:
        if not isinstance(connection_type, ConnectionType):
            raise TypeError(
                f"'connection_type' must be a 'ConnectionType' (it is {type(connection_type)})."
            )
        return connection_type

    connection_name: str = field(
        metadata={
            "docstring": "The name of the connection as registered in the organization settings.",
        },
    )

    def _validate_connection_name(self, connection_name: str):
        if not isinstance(connection_name, str):
            raise TypeError(
                f"'connection_name' must be a string (it is {type(connection_name)})."
            )
        if not connection_name:
            raise ValueError("'connection_name' cannot be empty.")
