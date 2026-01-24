from redshift_client.client._core import (
    TableClient,
)
from redshift_client.sql_client import (
    SqlCursor,
)

from . import (
    _methods,
    _new,
)


def new_table_client(sql: SqlCursor) -> TableClient:
    return TableClient(
        lambda t, p, r: _methods.unload(sql, t, p, r),
        lambda t, m, r, h: _methods.load(sql, t, m, r, h),
        lambda t: _methods.get(sql, t),
        lambda t: _methods.exist(sql, t),
        lambda i, t, s, m: _methods.insert(sql, i, t, s, m),
        lambda i, g: _methods.named_insert(sql, i, g),
        lambda t, n: _methods.rename(sql, t, n),
        lambda t: _methods.delete(sql, t, False),
        lambda t: _methods.delete(sql, t, True),
        lambda t, c: _methods.add_column(sql, t, c),
        lambda t, d: _methods.add_columns(sql, t, d),
        lambda i, t, _: _new.new(sql, i, t, False),
        lambda i, t, _: _new.new(sql, i, t, True),
        lambda b, n: _methods.create_like(sql, b, n),
        lambda s, t: _methods.move_data(sql, s, t),
        lambda s, t: _methods.move(sql, s, t),
        lambda s, t: _methods.migrate(sql, s, t),
    )
