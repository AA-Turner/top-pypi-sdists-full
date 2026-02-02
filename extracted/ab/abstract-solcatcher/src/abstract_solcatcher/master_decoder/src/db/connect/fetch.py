
from ..imports import sql,logging
from .core import query_data


log = logging.getLogger(__name__)

def fetch_any_combo(
    *,
    tableName,
    columnNames="*",
    searchColumn=None,
    searchValue=None,
    anyValue=False,
    zip_rows=True,
    schema="public",
):
    if not tableName:
        raise ValueError("tableName is required")

    if columnNames == "*":
        select_cols = sql.SQL("*")
    else:
        select_cols = sql.SQL(", ").join(
            sql.Identifier(c.strip()) for c in columnNames.split(",")
        )

    query = sql.SQL("SELECT {} FROM {}.{}").format(
        select_cols,
        sql.Identifier(schema),
        sql.Identifier(tableName),
    )

    params = []
    if searchColumn and searchValue is not None:
        if anyValue:
            query += sql.SQL(" WHERE {} = ANY(%s)").format(sql.Identifier(searchColumn))
            params.append(
                searchValue if isinstance(searchValue, list) else [searchValue]
            )
        else:
            query += sql.SQL(" WHERE {} = %s").format(sql.Identifier(searchColumn))
            params.append(searchValue)

    return query_data(query, params, zip_rows=zip_rows)
