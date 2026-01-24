from redshift_client.client._core import (
    SchemaClient,
)
from redshift_client.sql_client import (
    SqlCursor,
)

from . import (
    _methods,
)


def new_schema_client(sql: SqlCursor) -> SchemaClient:
    return SchemaClient(
        _methods.all_schemas(sql),
        lambda s: _methods.table_ids(sql, s),
        lambda s: _methods.exist(sql, s),
        lambda s: _methods.delete(sql, s, False),
        lambda s: _methods.delete(sql, s, True),
        lambda o, n: _methods.rename(sql, o, n),
        lambda s: _methods.create(sql, s, False),
        lambda s: _methods.create(sql, s, True),
        lambda s: _methods.recreate(sql, s, False),
        lambda s: _methods.recreate(sql, s, True),
        lambda s, t: _methods.migrate(sql, s, t),
        lambda s, t: _methods.move(sql, s, t),
        lambda s, p: _methods.set_policy(sql, s, p),
    )
