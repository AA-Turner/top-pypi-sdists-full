from snowflake_client._core import (
    SnowflakeCursor,
    TableClient,
)

from . import (
    _methods,
    _new,
)


def new_table_client(sql: SnowflakeCursor) -> TableClient:
    return TableClient(
        get=lambda t: _methods.get(sql, t),
        exist=lambda t: _methods.exist(sql, t),
        insert=lambda i, t, s, m: _methods.insert(sql, i, t, s, m),
        named_insert=lambda i, g: _methods.named_insert(sql, i, g),
        rename=lambda t, n: _methods.rename(sql, t, n),
        delete=lambda t: _methods.delete(sql, t, False),
        delete_cascade=lambda t: _methods.delete(sql, t, True),
        add_column=lambda t, c: _methods.add_column(sql, t, c),
        add_columns=lambda t, d: _methods.add_columns(sql, t, d),
        new=lambda i, t: _new.new(sql, i, t, False),
        new_if_not_exist=lambda i, t: _new.new(sql, i, t, True),
        create_like=lambda b, n: _methods.create_like(sql, b, n),
        move_data=lambda s, t: _methods.move(sql, s, t),
        move=lambda s, t: _methods.move(sql, s, t),
        migrate=lambda s, t: _methods.migrate(sql, s, t),
    )
