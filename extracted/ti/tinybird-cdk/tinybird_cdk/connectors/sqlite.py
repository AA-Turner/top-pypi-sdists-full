import sqlite3

from tinybird_cdk import config, connector, errors, export, formats


# WARNING: THIS CONNECTOR WAS JUST PROTOTYPED TO HELP DESIGN THE CDK, BUT IT IS
# NOT USED AND IT DOES NOT HAVE TESTS.
class Connector(connector.SQLConnector):
    def __init__(self):
        super().__init__()
        self.database = config.get('SQLITE_DATABASE')

    def get_scopes(self):
        raise Exception('Not implemented')

    def list_scope(self, _parents={}):
        raise Exception('Not implemented')

    def suggest_schema(self, _scopes):
        raise Exception('Not implemented')

    def _query(self, sql):
        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor]

    def _export(self, query, fmt, row_limit):
        with sqlite3.connect(self.database) as connection:
            if fmt == formats.NDJSON:
                connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM ({query})')

            if fmt == formats.CSV:
                fname = self._to_csv_tempfile(cursor)
            elif fmt == formats.NDJSON:
                # We pass a generator expression that yields each row as a
                # dictionary because rows themselves are not serializable.
                fname = self._to_ndjson_tempfile((dict(row) for row in cursor))
            else:
                raise errors.UnsupportedFormatError(fmt)

        return export.LocalFile(fname)
