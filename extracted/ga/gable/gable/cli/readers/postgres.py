import psycopg2  # type: ignore
from gable.cli.readers.constants import (
    PROXY_DB_CONNECTION_RETIRES,
    PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
)
from loguru import logger


def create_postgres_connection(
    user: str,
    password: str,
    db: str,
    host: str = "localhost",
    port: int = 5432,
    connect_timeout: int = PROXY_DB_CONNECTION_TIMEOUT_SECONDS,
    connect_retries: int = PROXY_DB_CONNECTION_RETIRES,
) -> psycopg2.extensions.connection:  # type: ignore
    """
    Create a connection to a PostgreSQL database.

    :param user:     The database user name.
    :param password: The database password.
    :param db:       The database name.
    :param host:     The database host.
    :param port:     The database port.
    :return:         A psycopg2 connection instance.
    """
    logger.debug(f'Connecting to "postgres://{user}:******@{host}:{port}/{db}"...')
    attempt = 0
    while True:
        try:
            conn = psycopg2.connect(
                dbname=db,
                user=user,
                password=password,
                host=host,
                port=port,
                sslmode="prefer",
                connect_timeout=connect_timeout,
            )
            logger.debug(f"Successfully connected to {host}:{port}")
            return conn
        except psycopg2.OperationalError as e:
            attempt += 1
            logger.debug(f"Connection attempt {attempt}/{connect_retries} failed...")
            logger.trace(str(e))
            if attempt >= connect_retries:
                logger.error(
                    f"Unable to connect to {host}:{port} after {attempt} attempts"
                )
                raise e
