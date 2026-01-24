from snowflake_client._core.clients import (
    SchemaClient,
    TableClient,
)
from snowflake_client._core.cursor import (
    SnowflakeCursor,
)

from . import (
    _methods,
)


def new_schema_client(sql: SnowflakeCursor, table_client: TableClient) -> SchemaClient:
    return SchemaClient(
        all_schemas=_methods.all_schemas(sql),
        table_ids=lambda s: _methods.table_ids(sql, s),
        exist=lambda s: _methods.exist(sql, s),
        delete=lambda s: _methods.delete(sql, s, False),
        delete_cascade=lambda s: _methods.delete(sql, s, True),
        rename=lambda o, n: _methods.rename(sql, o, n),
        create=lambda s: _methods.create(sql, s, False),
        create_if_not_exist=lambda s: _methods.create(sql, s, True),
        recreate=lambda s: _methods.recreate(
            delete_schema=lambda h: _methods.delete(sql, h, False),
            create_schema=lambda s: _methods.create(sql, s, False),
            cursor=sql,
            schema=s,
        ),
        recreate_cascade=lambda s: _methods.recreate(
            delete_schema=lambda h: _methods.delete(sql, h, True),
            create_schema=lambda s: _methods.create(sql, s, False),
            cursor=sql,
            schema=s,
        ),
        migrate=lambda s, t: _methods.move_tables(sql, s, t, table_client.migrate),
        move=lambda s, t: _methods.move_tables(sql, s, t, table_client.move),
    )
