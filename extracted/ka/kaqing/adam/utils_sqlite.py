from collections.abc import Callable

import functools
import glob
import os
import sqlite3
import pandas

from adam.config import Config
from adam.utils import creating_dir, tabulize, log, wait_log
from adam.utils_context import Context

class CursorHandler:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = None

    def __enter__(self):
        self.cursor = self.conn.cursor()

        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()

        return False

class SQLiteConnectionHandler:
    def __init__(self, database: str, keyspace = None):
        self.database = database
        self.keyspace = keyspace
        self.conn = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = SQLite.connect(self.database, self.keyspace)

        self.conn.__enter__()

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.__exit__(exc_type, exc_val, exc_tb)

        return False

def sqlite(database: str, keyspace = None):
    return SQLiteConnectionHandler(database, keyspace=keyspace)

# no state utility class
class SQLite:
    def cursor(conn: sqlite3.Connection):
        return CursorHandler(conn)

    def local_db_dir():
        return creating_dir(Config().get('export.sqlite.local-db-dir', '/tmp/qing-db/q/export/db'))

    def keyspace(database: str):
        return '_'.join(database.replace(".db", "").split('_')[1:])

    @functools.lru_cache()
    def database_names(prefix: str = None):
        wait_log('Inspecting export databases...')

        pattern = f'{SQLite.local_db_dir()}/s*.db'
        if prefix:
            pattern = f'{SQLite.local_db_dir()}/{prefix}*'
        return [os.path.basename(f) for f in glob.glob(pattern)]

    def clear_cache(cache: str = None):
        SQLite.database_names.cache_clear()
        SQLite.table_names.cache_clear()

    @functools.lru_cache()
    def table_names(database: str):
      tokens = database.replace('.db', '').split('_')
      ts_prefix = tokens[0]
      keyspace = '_'.join(tokens[1:])

      conn = None
      tables = []
      try:
         conn = sqlite3.connect(f'{SQLite.local_db_dir()}/{ts_prefix}_{keyspace}.db')
         with SQLite.cursor(conn) as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

            tables = [row[0] for row in cursor.fetchall() if row[0] != "sqlite_sequence"]

         return tables
      except sqlite3.Error as e:
         print(f"Error connecting to or querying the database: {e}")
         return []
      finally:
         if conn:
               conn.close()

    def connect(database: str, keyspace: str = None):
        if keyspace:
            return sqlite3.connect(f'{SQLite.local_db_dir()}/{database}_{keyspace}.db')
        else:
            conn = sqlite3.connect(f'{SQLite.local_db_dir()}/{database}_root.db')
            with SQLite.cursor(conn) as cursor:
                for d in SQLite.database_names(database):
                    if d != f'{database}.db':
                        q = f"ATTACH DATABASE '{SQLite.local_db_dir()}/{d}' AS {SQLite.keyspace(d)}"
                        cursor.execute(q)

            return conn

    @functools.lru_cache()
    def column_names(tables: list[str] = [], database: str = None, function: str = 'audit', partition_cols_only = False):
        pass

    def run_query(query: str, database: str = None, ctx: Context = Context.NULL) -> int:
        with sqlite(database) as conn:
            return SQLite.run_query_with_conn(conn, query, ctx=ctx)

    def run_query_with_conn(conn, query: str, ctx: Context = Context.NULL) -> int:
        # log_file = None

        df = SQLite.query(conn, query)
        lines = ['\t'.join(map(str, line)) for line in df.values.tolist()]
        tabulize(lines, header='\t'.join(df.columns.tolist()), separator='\t', log_file=ctx.log_file)

        return len(lines)

    def query(conn, sql: str) -> tuple[str, str, list]:
        return pandas.read_sql_query(sql, conn)