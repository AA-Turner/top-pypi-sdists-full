import pymssql
from gable.cli.readers.constants import (
    PROXY_DB_CONNECTION_RETIRES,
    PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
)
from loguru import logger


def create_mssql_connection(
    user: str,
    password: str,
    db: str,
    host: str = "localhost",
    port: int = 1433,
    connect_timeout: int = PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
    connect_retries: int = PROXY_DB_CONNECTION_RETIRES,
) -> pymssql.Connection:
    """
    Create a connection to a MSSQL database.

    :param user:     The database user name.
    :param password: The database password.
    :param db:       The database name.
    :param host:     The database host.
    :param port:     The database port.
    :return:         A pymssql connection instance.
    """
    logger.debug(
        f'Connecting to "Server={host},{port};Database={db};User Id={user};Password=******;"'
    )
    attempt = 0
    while True:
        try:
            conn = pymssql.connect(
                database=db,
                user=user,
                password=password,
                host=host,
                port=str(port),
                encryption="request",
                login_timeout=connect_timeout,
            )
            logger.debug(f"Successfully connected to {host}:{port}")
            return conn
        except pymssql.OperationalError as e:
            attempt += 1
            logger.debug(f"Connection attempt {attempt}/{connect_retries} failed...")
            logger.trace(str(e))
            if attempt >= connect_retries:
                logger.error(
                    f"Unable to connect to 'Server={host},{port}' after {attempt} attempts"
                )
                raise e
