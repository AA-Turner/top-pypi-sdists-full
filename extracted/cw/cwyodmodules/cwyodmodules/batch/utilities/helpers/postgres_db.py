from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from mgmt_config import identity, logger
from .env_helper import EnvHelper

class PostgresDB:
    def __init__(self):
        self.env_helper = EnvHelper()
        self.conn_string = self._get_conn_string()

    def _get_conn_string(self):
        try:
            user = self.env_helper.POSTGRESQL_USER
            host = self.env_helper.POSTGRESQL_HOST
            dbname = self.env_helper.POSTGRESQL_DATABASE
            
            access_information = identity.get_token(
                scopes="https://ossrdbms-aad.database.windows.net/.default"
            )
            token = access_information.token
            return f"host={host} user={user} dbname={dbname} password={token}"
        except Exception as e:
            logger.error(f"Error generating connection string for PostgreSQL: {e}")
            raise

    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            keepalive_kwargs = {
                "keepalives": 1,
                "keepalives_idle": 60,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            }
            conn = psycopg2.connect(self.conn_string, **keepalive_kwargs)
            yield conn
        except Exception as e:
            logger.error(f"Error establishing a connection to PostgreSQL: {e}")
            raise
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_db_cursor(self, commit=False, cursor_factory=None):
        with self.get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                if commit:
                    conn.commit()
            finally:
                cursor.close()

    def execute_query(self, query, params=None, fetch=None, commit=False, cursor_factory=RealDictCursor):
        with self.get_db_cursor(commit=commit, cursor_factory=cursor_factory) as cur:
            cur.execute(query, params)
            if fetch == "one":
                return cur.fetchone()
            if fetch == "all":
                return cur.fetchall()
            return None 