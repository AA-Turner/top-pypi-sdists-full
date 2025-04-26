import mysql.connector

from tinybird_cdk import config, connector, errors, export, formats


# WARNING: THIS CONNECTOR WAS JUST PROTOTYPED TO HELP DESIGN THE CDK, BUT IT IS
# NOT USED AND IT DOES NOT HAVE TESTS.
#
# The environment variables supported by this connector are documented here:
#
#     https://dev.mysql.com/doc/refman/8.0/en/environment-variables.html
#
class Connector(connector.SQLConnector):
    def __init__(self):
        super().__init__()
        self.database = config.get('MYSQL_DATABASE')

    def get_scopes(self):
        raise Exception('Not implemented')

    def list_scope(self, _parents={}):
        raise Exception('Not implemented')

    def suggest_schema(self, _scopes):
        raise Exception('Not implemented')

    def _query(self, sql):
        with mysql.connector.connect(database=self.database) as conn:
            with conn.cursor(dictionary=True, buffered=True) as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def _export(self, query, fmt, row_limit):
        if fmt == formats.CSV:
            dictionary = False
        elif fmt == formats.NDJSON:
            dictionary = True
        else:
            raise errors.UnsupportedFormatError(fmt)

        with mysql.connector.connect(database=self.database) as connection:
            with connection.cursor(dictionary=dictionary) as cursor:
                cursor.execute(query)
                if fmt == formats.CSV:
                    fname = self._to_csv_tempfile(cursor)
                elif formats.NDJSON:
                    fname = self._to_ndjson_tempfile(cursor)
        return export.LocalFile(fname)
