import mysql.connector


class DBConnectionMySQLConnector:
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
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            connect_timeout=self.timeout,
            autocommit=self.auto_commit,
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
