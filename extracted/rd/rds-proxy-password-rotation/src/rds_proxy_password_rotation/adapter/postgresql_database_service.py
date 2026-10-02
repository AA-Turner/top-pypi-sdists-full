import psycopg
from aws_lambda_powertools import Logger
from psycopg import Connection, sql, ClientCursor

from rds_proxy_password_rotation.model import DatabaseCredentials
from rds_proxy_password_rotation.services import DatabaseService


class PostgreSqlDatabaseService(DatabaseService):
    def __init__(self, logger: Logger):
        self.logger = logger

    def test_user_credentials(self, credentials: DatabaseCredentials) -> bool:
        with self._get_connection(credentials) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")

                return True

    def change_user_credentials(self, old_credentials: DatabaseCredentials, new_password: str):
        with self._get_connection(old_credentials) as conn:
            with ClientCursor(conn) as cur:
                cur.execute(sql.SQL("ALTER USER {} WITH PASSWORD %s").format(sql.Identifier(old_credentials.username)), (new_password,))
                conn.commit()

    def _get_connection(self, credentials: DatabaseCredentials) -> Connection:
        """
        Method is protected to allow testing.
        :param credentials: used to connect to the database
        :return: the database connection
        """
        connect_string = psycopg._connection_info.make_conninfo("", password=credentials.password, user=credentials.username, host=credentials.database_host, port=credentials.database_port, dbname=credentials.database_name, sslmode="require", connect_timeout=5)

        try:
            return psycopg.connect(connect_string)
        except psycopg.OperationalError as e:
            self.logger.error(f'Failed to connect to database {credentials.database_name} on {credentials.database_host}:{credentials.database_port} as {credentials.username}')

            raise e
