from nsj_multi_database_lib.env_config import EnvConfig

from flask import g

from nsj_multi_database_lib.settings import get_logger

import sqlalchemy
import re


def create_pool(database_conn_url):
    # Creating database connection pool
    db_pool = sqlalchemy.create_engine(
        database_conn_url,
        # pool_size=5,
        # max_overflow=2,
        # pool_timeout=30,
        # pool_recycle=1800,
        poolclass=sqlalchemy.pool.NullPool,
        # TODO: verificar se client_encoding aqui é necessário, pois segundo este link:
        # https://stackoverflow.com/questions/14783505/encoding-error-with-sqlalchemy-and-postgresql
        # o sqlalchemy usa, por padrão, o encoding da configuração do banco de dados
        # , client_encoding='utf8'
    )
    return db_pool


def create_url(
    username: str,
    password: str,
    host: str,
    port: str,
    database: str,
    db_dialect: str = "postgresql+pg8000",
):
    return str(
        sqlalchemy.engine.URL.create(
            db_dialect,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )
    )


def create_external_pool_with_default_credentials():
    external_database = g.external_database
    external_database_conn_url = create_url(
        username=EnvConfig.instance().default_external_database_user,
        password=EnvConfig.instance().default_external_database_password,
        host=external_database["host"],
        port=external_database["port"],
        database=external_database["name"],
    )
    line = re.sub(r":[^/]+@", ":********@", external_database_conn_url)
    get_logger().debug(f"URL Conexao 2: {line}")

    external_db_pool = create_pool(external_database_conn_url)
    return external_db_pool


def create_external_pool():
    external_database = g.external_database
    external_database_conn_url = create_url(
        username=external_database["user"],
        password=external_database["password"],
        host=external_database["host"],
        port=external_database["port"],
        database=external_database["name"],
    )
    line = re.sub(r":[^/]+@", ":********@", external_database_conn_url)
    get_logger().debug(f"URL Conexao: {line}")

    external_db_pool = create_pool(external_database_conn_url)
    return external_db_pool


def create_test_pool():
    import os

    conn_url = create_url(
        username=os.environ["TEST_DATABASE_USER"],
        password=os.environ["TEST_DATABASE_PASS"],
        host=os.environ["TEST_DATABASE_HOST"],
        port=os.environ["TEST_DATABASE_PORT"],
        database=os.environ["TEST_DATABASE_NAME"],
    )
    line = re.sub(r":[^/]+@", ":********@", conn_url)
    get_logger().debug(f"URL Conexao: {line}")

    return create_pool(conn_url)


def create_erpsql_pool():
    import os

    conn_url = create_url(
        username=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASS"],
        host=os.environ["DATABASE_HOST"],
        port=os.environ["DATABASE_PORT"],
        database=os.environ["DATABASE_NAME"],
    )
    line = re.sub(r":[^/]+@", ":********@", conn_url)
    get_logger().debug(f"URL Conexao: {line}")

    return create_pool(conn_url)
