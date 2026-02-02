from .fetch import fetch_any_combo
from .columns import ColumnNamesManager

cols = ColumnNamesManager()

def zip_rows(table, rows, schema="public"):
    names = cols.get(table, schema)
    return [dict(zip(names, row)) for row in rows]

def get_pair(pair_id=None, mint=None, signature=None):
    if pair_id:
        rows = fetch_any_combo(
            tableName="pairs", searchColumn="id", searchValue=pair_id
        )
    elif mint:
        rows = fetch_any_combo(
            tableName="pairs", searchColumn="mint", searchValue=mint
        )
    elif signature:
        rows = fetch_any_combo(
            tableName="pairs", searchColumn="signature", searchValue=signature
        )
    else:
        return []

    return rows
