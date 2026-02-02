from .core import query_data
from .imports import logging,SingletonMeta

log = logging.getLogger(__name__)

class ColumnNamesManager(metaclass=SingletonMeta):
    def __init__(self):
        self.cache = {}

    def get(self, table, schema="public"):
        key = (schema, table)
        if key not in self.cache:
            self.cache[key] = self._fetch(table, schema)
        return self.cache[key]

    def _fetch(self, table, schema):
        rows = query_data(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position
            """,
            [schema, table],
            zip_rows=False,
        )
        return [r[0] for r in rows]
