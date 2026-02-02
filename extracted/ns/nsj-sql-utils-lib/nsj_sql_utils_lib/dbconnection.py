import enum

from nsj_sql_utils_lib.dbconnection_mysql_connector import DBConnectionMySQLConnector
from nsj_sql_utils_lib.dbconnection_psycopg2 import DBConnectionPsycopg2


class DBConnectionDriver(enum.Enum):
    POSTGRES = "POSTGRES"
    SINGLE_STORE = "SINGLE_STORE"
    MYSQL = "MYSQL"


class DBConnection:
    def __init__(
        self,
        driver: DBConnectionDriver,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        timeout: int = 5,
        auto_commit: bool = True,
    ):
        # Convertendo str para enum, se necessário
        try:
            driver = DBConnectionDriver(driver)
        except:
            raise Exception(
                f"Tipo de driver de banco não suportado: {driver}. Válidos: {', '.join([d.name for d in DBConnectionDriver])}"
            )

        if driver == DBConnectionDriver.POSTGRES:
            self.conn_aux = DBConnectionPsycopg2(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                timeout=timeout,
                auto_commit=auto_commit,
            )
        elif driver in (DBConnectionDriver.MYSQL, DBConnectionDriver.SINGLE_STORE):
            self.conn_aux = DBConnectionMySQLConnector(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                timeout=timeout,
                auto_commit=auto_commit,
            )
        else:
            raise Exception(
                f"Tipo de driver de banco não suportado: {driver}. Válidos: {', '.join([d.name for d in DBConnectionDriver])}"
            )

        self.conn = None

    def __enter__(self):
        self.open()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(exc_type, exc_val, exc_tb)

    def open(self):
        self._aux = self.conn_aux.__enter__()
        self.conn = self._aux.conn

    def close(self, exc_type=None, exc_val=None, exc_tb=None):
        self._aux.__exit__(exc_type, exc_val, exc_tb)
