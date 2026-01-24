from dataclasses import (
    dataclass,
)

from snowflake_client._core.clients import (
    SchemaClient,
    TableClient,
)
from snowflake_client._core.cursor import (
    SnowflakeCursor,
)

from .connection import (
    ConnectionFactory,
)
from .cursor import (
    SnowflakeCursorFactory,
)
from .schema import (
    new_schema_client,
)
from .table import (
    new_table_client,
)


@dataclass(frozen=True)
class ClientFactory:
    @staticmethod
    def new_table_client(sql: SnowflakeCursor) -> TableClient:
        """
        Table client constructor.

        @move_data:
        This method moves data from source to target.
        - After the operation source will be empty.
        - Both tables must exists.
        @move:
        - create target if not exist
        - move_data (append) data from source into target
        - delete source table (that will be empty)
        @migrate:
        - delete target if exist
        - move source into target (see move method)
        """
        return new_table_client(sql)

    @staticmethod
    def new_schema_client(sql: SnowflakeCursor) -> SchemaClient:
        return new_schema_client(sql, new_table_client(sql))


__all__ = [
    "ConnectionFactory",
    "SnowflakeCursorFactory",
]
