from dataclasses import (
    dataclass,
)

from redshift_client.sql_client import (
    SqlCursor,
)

from . import (
    _schema,
    _table,
)
from ._core import (
    SchemaClient,
    TableClient,
)


@dataclass(frozen=True)
class ClientFactory:
    @staticmethod
    def new_table_client(sql: SqlCursor) -> TableClient:
        """
        TableClient constructor.

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
        return _table.new_table_client(sql)

    @staticmethod
    def new_schema_client(sql: SqlCursor) -> SchemaClient:
        return _schema.new_schema_client(sql)
