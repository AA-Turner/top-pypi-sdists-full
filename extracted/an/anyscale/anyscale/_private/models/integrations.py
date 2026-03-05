from dataclasses import dataclass, field
import re
from typing import ClassVar, Dict

from anyscale._private.models.model_base import ModelBase, ModelEnum
from anyscale.utils.name_utils import CONNECTION_NAME_VALIDATION_REGEX_PATTERN


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
    like Databricks Unity Catalog. Each connection is identified by its type and name.

    This feature is in beta preview. Contact [Anyscale support](mailto:support@anyscale.com) to request enablement.
    """

    __doc_py_example__ = """\
from anyscale._private.models.integrations import ConnectionConfig, ConnectionType

connection = ConnectionConfig(
    type=ConnectionType.DATABRICKS,
    name="my-databricks-connection",
)
"""

    __doc_yaml_example__ = """\
connections:
  - type: databricks
    name: my-databricks-connection
"""

    type: ConnectionType = field(
        metadata={"docstring": "The type of connection (e.g., DATABRICKS)."},
    )

    def _validate_type(self, type: ConnectionType) -> ConnectionType:  # noqa: A002
        if not isinstance(type, ConnectionType):
            raise TypeError(
                f"'type' must be a 'ConnectionType' (it is {type.__class__})."
            )
        return type

    name: str = field(
        metadata={
            "docstring": "The name of the connection as registered in the organization settings.",
        },
    )

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f"'name' must be a string (it is {type(name)}).")
        if not name:
            raise ValueError("'name' cannot be empty.")
        if not re.match(CONNECTION_NAME_VALIDATION_REGEX_PATTERN, name):
            raise ValueError(
                "'name' can only contain alphanumeric characters, "
                "periods, dashes, and underscores."
            )
