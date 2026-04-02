import psycopg2


class DBConnectionPsycopg2:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        timeout: int = 5,
        auto_commit: bool = True,
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
        self.timeout = timeout
        self.auto_commit = auto_commit

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            connect_timeout=self.timeout,
        )

        if self.auto_commit:
            self.conn.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
            )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
