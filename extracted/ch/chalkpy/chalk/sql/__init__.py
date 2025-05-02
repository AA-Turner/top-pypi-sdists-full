from __future__ import annotations

from os import PathLike
from typing import Any, Dict, Optional, Union, overload

from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.integrations.athena import AthenaSourceImpl
from chalk.sql._internal.integrations.bigquery import BigQuerySourceImpl
from chalk.sql._internal.integrations.clickhouse import ClickhouseSourceImpl
from chalk.sql._internal.integrations.cloudsql import CloudSQLSourceImpl
from chalk.sql._internal.integrations.databricks import DatabricksSourceImpl
from chalk.sql._internal.integrations.dynamodb import DynamoDBSourceImpl
from chalk.sql._internal.integrations.mysql import MySQLSourceImpl
from chalk.sql._internal.integrations.postgres import PostgreSQLSourceImpl
from chalk.sql._internal.integrations.redshift import RedshiftSourceImpl
from chalk.sql._internal.integrations.snowflake import SnowflakeSourceImpl
from chalk.sql._internal.integrations.spanner import SpannerSourceImpl
from chalk.sql._internal.integrations.sqlite import SQLiteSourceImpl
from chalk.sql._internal.integrations.trino import TrinoSourceImpl
from chalk.sql._internal.sql_file_resolver import make_sql_file_resolver
from chalk.sql._internal.sql_source_group import SQLSourceGroup
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import (
    BaseSQLSourceProtocol,
    ChalkQueryProtocol,
    SQLSourceWithTableIngestProtocol,
    StringChalkQueryProtocol,
    TableIngestProtocol,
)


@overload
def SnowflakeSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Snowflake database.

    If you have only one Snowflake connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource()
    """


@overload
def SnowflakeSource(*, name: str, engine_args: Optional[Dict[str, Any]] = ...) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SnowflakeSource(name="RISK")
    """
    ...


@overload
def SnowflakeSource(
    *,
    name: str | None = ...,
    account_identifier: str | None = ...,
    warehouse: str = ...,
    user: str | None = ...,
    password: str | None = ...,
    db: str | None = ...,
    schema: str | None = ...,
    role: str | None = ...,
    private_key_b64: str | None = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this PostgresSQLSource is used within SQL File Resolvers.
    account_identifier
        Your Snowflake account identifier.
    warehouse
        Snowflake warehouse to use.
    user
        Username to connect to Snowflake.
    password
        The password to use.
    db
        Database to use.
    schema
        Snowflake schema in the database to use.
    role
        Snowflake role name to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> snowflake = SnowflakeSource(
    ...     db=os.getenv("SNOWSQL_DATABASE"),
    ...     schema=os.getenv("SNOWSQL_SCHEMA"),
    ...     role=os.getenv("SNOWSQL_ROLE"),
    ...     warehouse=os.getenv("SNOWSQL_WAREHOUSE"),
    ...     user=os.getenv("SNOWSQL_USER"),
    ...     password=os.getenv("SNOWSQL_PWD"),
    ...     account_identifier=os.getenv("SNOWSQL_ACCOUNT_IDENTIFIER")
    ... )
    """
    ...


def SnowflakeSource(
    *,
    name: Optional[str] = None,
    account_identifier: Optional[str] = None,
    warehouse: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    db: Optional[str] = None,
    schema: Optional[str] = None,
    role: Optional[str] = None,
    private_key_b64: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Snowflake data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return SnowflakeSourceImpl(
        name=name,
        account_identifier=account_identifier,
        warehouse=warehouse,
        user=user,
        password=password,
        db=db,
        schema=schema,
        role=role,
        private_key_b64=private_key_b64,
        engine_args=engine_args,
    )


@overload
def PostgreSQLSource() -> SQLSourceWithTableIngestProtocol:
    """Connect to the only configured PostgreSQL database.

    If you have only one PostgreSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> pg = PostgreSQLSource()
    """
    ...


@overload
def PostgreSQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """If you have only one PostgreSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = PostgreSQLSource(name="RISK")
    """
    ...


@overload
def PostgreSQLSource(
    *,
    name: str | None = ...,
    host: str | None = ...,
    port: int | str | None = ...,
    db: str | None = ...,
    user: str | None = ...,
    password: str | None = ...,
    engine_args: dict[str, Any] | None = ...,
    async_engine_args: dict[str, Any] | None = ...,
) -> SQLSourceWithTableIngestProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this PostgresSQLSource is used within SQL File Resolvers.
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        PostgreSQL username to connect as.
    password
        The password to be used if the server demands password authentication.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> pg = PostgreSQLSource(
    ...     host=os.getenv("PGHOST"),
    ...     port=os.getenv("PGPORT"),
    ...     db=os.getenv("PGDATABASE"),
    ...     user=os.getenv("PGUSER"),
    ...     password=os.getenv("PGPASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return pg.query_string("select name from users where id = 4").one()
    """
    ...


def PostgreSQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> TableIngestProtocol:
    """Create a PostgreSQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return PostgreSQLSourceImpl(
        host,
        port,
        db,
        user,
        password,
        name,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


@overload
def MySQLSource() -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> mysql = MySQLSource()
    """
    ...


@overload
def MySQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """If you have only one MySQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = MySQLSource(name="RISK")
    """
    ...


@overload
def MySQLSource(
    *,
    name: str | None = ...,
    host: str,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> SQLSourceWithTableIngestProtocol:
    """
    You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        MySQL username to connect as.
    password
        The password to be used if the server demands password authentication.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args:
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> mysql = MySQLSource(
    ...     host=os.getenv("PGHOST"),
    ...     port=os.getenv("PGPORT"),
    ...     db=os.getenv("PGDATABASE"),
    ...     user=os.getenv("PGUSER"),
    ...     password=os.getenv("PGPASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return mysql.query_string("select name from users where id = 4").one()
    """
    ...


def MySQLSource(
    *,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Create a MySQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return MySQLSourceImpl(
        host,
        port,
        db,
        user,
        password,
        name,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


def SQLiteInMemorySource(
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Testing SQL source.

    If you have only one SQLiteInMemorySource integration, there's no need to provide
    a distinguishing name.

    Parameters
    ----------
    name
        The name of the integration.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SQLiteInMemorySource(name="RISK")
    """
    return SQLiteSourceImpl(name=name, engine_args=engine_args, async_engine_args=async_engine_args)


def SQLiteFileSource(
    filename: Union[str, PathLike],
    name: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> SQLSourceWithTableIngestProtocol:
    """Create a SQLite source for a file.

    Parameters
    ----------
    filename
        The name of the file.
    name
        The name to use in testing
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    SQLSourceWithTableIngestProtocol
        The SQL source for use in Chalk resolvers.
    """
    return SQLiteSourceImpl(
        filename=filename,
        name=name,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


@overload
def RedshiftSource() -> BaseSQLSourceProtocol:
    """If you have only one Redshift connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource()
    """
    ...


@overload
def RedshiftSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Redshift integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = RedshiftSource(name="RISK")
    """
    ...


@overload
def RedshiftSource(
    *,
    name: str | None = ...,
    host: str = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    port: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        The name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    host
        Name of host to connect to.
    db
        The database name.
    user
        Redshify username to connect as.
    password
        The password for the Redshift database.
    port
        The port number to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> redshift = RedshiftSource(
    ...     host=os.getenv("REDSHIFT_HOST"),
    ...     db=os.getenv("REDSHIFT_DB"),
    ...     user=os.getenv("REDSHIFT_USER"),
    ...     password=os.getenv("REDSHIFT_PASSWORD"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return redshift.query_string("select name from users where id = 4").one()
    """
    ...


def RedshiftSource(
    *,
    host: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    name: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Redshift data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return RedshiftSourceImpl(host, db, user, password, name, port, engine_args=engine_args)


@overload
def SpannerSource() -> BaseSQLSourceProtocol:
    """If you have only one Spanner connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SpannerSource()
    """
    ...


@overload
def SpannerSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Spanner integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = SpannerSource(name="RISK")
    """
    ...


@overload
def SpannerSource(
    *,
    name: str | None = None,
    project: str | None = None,
    instance: str | None = None,
    database: str | None = None,
    credentials_base64: str | None = None,
    emulator_host: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    project
        The name of the GCP project for the Spanner instance.
    instance
        The name of the Spanner instance.
    database
        The name of the database in the Spanner instance.
    credentials_base64
        The credentials to use to connect, encoded as a base64 string.
    emulator_host
        Location of Spanner emulator, if desired.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> source = SpannerSource(
    ...     project=os.getenv("SPANNER_PROJECT"),
    ...     instance=os.getenv("SPANNER_INSTANCE"),
    ...     database=os.getenv("SPANNER_DATABASE"),
    ...     credentials_base64=os.getenv("SPANNER_CREDENTIALS_BASE64"),
    ... )
    """
    ...


def SpannerSource(
    name: str | None = None,
    project: str | None = None,
    instance: str | None = None,
    database: str | None = None,
    credentials_base64: str | None = None,
    emulator_host: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """Create a Spanner data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return SpannerSourceImpl(
        name=name,
        project=project,
        instance=instance,
        database=database,
        credentials_base64=credentials_base64,
        emulator_host=emulator_host,
        engine_args=engine_args,
    )


@overload
def BigQuerySource() -> BaseSQLSourceProtocol:
    """If you have only one BigQuery connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource()
    """
    ...


@overload
def BigQuerySource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one BigQuery integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = BigQuerySource(name="RISK")
    """
    ...


@overload
def BigQuerySource(
    *,
    name: str | None = ...,
    project: Optional[str] = ...,
    dataset: Optional[str] = ...,
    location: Optional[str] = ...,
    credentials_base64: Optional[str] = ...,
    credentials_path: Optional[str] = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    project
        The name of the GCP project for the BigQuery instance.
    dataset
        The name of the BigQuery dataset.
    location
        The location of the BigQuery instance.
    credentials_base64
        The credentials to use to connect, encoded as a base64 string.
    credentials_path
        The path to the credentials file to use to connect.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> source = BigQuerySource(
    ...     project=os.getenv("BIGQUERY_PROJECT"),
    ...     dataset=os.getenv("BIGQUERY_DATASET"),
    ...     location=os.getenv("BIGQUERY_LOCATION"),
    ...     credentials_base64=os.getenv("BIGQUERY_CREDENTIALS_BASE64"),
    ... )
    """
    ...


def BigQuerySource(
    *,
    name: Optional[str] = None,
    project: Optional[str] = None,
    dataset: Optional[str] = None,
    location: Optional[str] = None,
    credentials_base64: Optional[str] = None,
    credentials_path: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a BigQuery data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return BigQuerySourceImpl(
        name=name,
        project=project,
        dataset=dataset,
        location=location,
        credentials_base64=credentials_base64,
        credentials_path=credentials_path,
        engine_args=engine_args,
    )


@overload
def CloudSQLSource() -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource()
    """
    ...


@overload
def CloudSQLSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """If you have only one CloudSQL integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = CloudSQLSource(name="RISK")
    """
    ...


@overload
def CloudSQLSource(
    *,
    name: str | None = ...,
    instance_name: Optional[str] = ...,
    db: Optional[str] = ...,
    user: Optional[str] = ...,
    password: Optional[str] = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    instance_name
        The name of the Cloud SQL instance, as defined in your GCP console.
    db
        Database to use.
    user
        Username to use.
    password
        The password to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> CloudSQLSource(
    ...     instance_name=os.getenv("CLOUDSQL_INSTANCE_NAME"),
    ...     db=os.getenv("CLOUDSQL_DB"),
    ...     user=os.getenv("CLOUDSQL_USER"),
    ...     password=os.getenv("CLOUDSQL_PASSWORD"),
    ... )
    """


def CloudSQLSource(
    *,
    name: Optional[str] = None,
    instance_name: Optional[str] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a CloudSQL data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return CloudSQLSourceImpl(
        name=name,
        instance_name=instance_name,
        db=db,
        user=user,
        password=password,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


@overload
def TrinoSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Trino database.

    If you have only one Trino connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = TrinoSource()
    """
    ...


@overload
def TrinoSource(*, name: str, engine_args: Optional[Dict[str, Any]] = ...) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = TrinoSource(name="RISK")
    """
    ...


@overload
def TrinoSource(
    *,
    name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    host
        Your Trino host.
    port
        Port number to use.
    catalog
        Catalog to use.
    schema
        Schema to use.
    user
        Trino username.
    password
        Trino password.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> trino = TrinoSource(
    ...     host=os.getenv("TRINO_HOST"),
    ...     port=os.getenv("TRINO_PORT"),
    ...     catalog=os.getenv("TRINO_CATALOG"),
    ...     schema=os.getenv("TRINO_SCHEMA"),
    ...     user=os.getenv("TRINO_USER"),
    ...     password=os.getenv("TRINO_PASSWORD"),
    ... )
    """
    ...


def TrinoSource(
    *,
    name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Trino data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return TrinoSourceImpl(host, port, catalog, schema, user, password, name, engine_args=engine_args)


@overload
def DatabricksSource() -> BaseSQLSourceProtocol:
    """Connect to the only configured Databricks database.

    If you have only one Databricks connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DatabricksSource()
    """


@overload
def DatabricksSource(*, name: str, engine_args: Optional[Dict[str, Any]] = ...) -> BaseSQLSourceProtocol:
    """Chalk's injects environment variables to support data integrations.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DatabricksSource(name="RISK")
    """
    ...


@overload
def DatabricksSource(
    *,
    name: str | None = ...,
    host: str = ...,
    http_path: str = ...,
    access_token: str = ...,
    db: str = ...,
    port: str = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    host
        Your Databricks host.
    http_path
        Databricks HTTP path to use.
    access_token
        Access token to connect to Databricks.
    db
        Database to use.
    port
        Port number to use.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> databricks = DatabricksSource(
    ...     host=os.getenv("DATABRICKS_HOST"),
    ...     http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    ...     access_token=os.getenv("DATABRICKS_TOKEN"),
    ...     db=os.getenv("DATABRICKS_DATABASE"),
    ...     port=os.getenv("DATABRICKS_PORT"),
    ... )
    """
    ...


def DatabricksSource(
    *,
    name: Optional[str] = None,
    host: Optional[str] = None,
    http_path: Optional[str] = None,
    access_token: Optional[str] = None,
    db: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Databricks data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return DatabricksSourceImpl(
        host=host,
        http_path=http_path,
        access_token=access_token,
        db=db,
        port=port,
        name=name,
        engine_args=engine_args,
    )


@overload
def DynamoDBSource() -> BaseSQLSourceProtocol:
    """If you have only one DynamoDB connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.
    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.
    Examples
    --------
    >>> source = DynamoDBSource()
    """
    ...


@overload
def DynamoDBSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one DynamoDB integration, there's no need to provide
    a distinguishing name.
    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        The name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DynamoDBSource(name="RISK")
    """
    ...


@overload
def DynamoDBSource(
    *,
    name: str | None = None,
    aws_client_id_override: str | None = None,
    aws_client_secret_override: str | None = None,
    aws_role_arn_override: str | None = None,
    aws_region_override: str | None = None,
    endpoint_override: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        The name of the integration. Not required unless if this SQL Source
        is used within SQL File Resolvers.
    aws_client_id_override
        Optionally override the credentials using an AWS client id, must be
        provided with a client secret override.
    aws_client_secret_override
        Optionally override the credentials using an AWS client secret, must
        be provided with a client id override.
    aws_role_arn_override
        Optionally override the credentials using an AWS role ARN.
    aws_region_override
        The AWS region code to connect to, such as `"us-east-1"`.
    endpoint_override
        Override for the DynamoDB endpoint if hosted elsewhere.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = DynamoDBSource(name="RISK")
    """
    ...


def DynamoDBSource(
    name: str | None = None,
    aws_client_id_override: str | None = None,
    aws_client_secret_override: str | None = None,
    aws_role_arn_override: str | None = None,
    aws_region_override: str | None = None,
    endpoint_override: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """Create a DynamoDB data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details. DynamoDBSources can be queried via PartiQL SQL
    resolvers.

    You may override the ambient AWS credentials by providing
    either a client ID and secret, or a role ARN.
    """
    return DynamoDBSourceImpl(
        name=name,
        aws_client_id_override=aws_client_id_override,
        aws_client_secret_override=aws_client_secret_override,
        aws_role_arn_override=aws_role_arn_override,
        aws_region_override=aws_region_override,
        endpoint_override=endpoint_override,
        engine_args=engine_args,
    )


@overload
def AthenaSource() -> BaseSQLSourceProtocol:
    """If you have only one Athena connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.
    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.
    Examples
    --------
    >>> source = AthenaSource()
    """
    ...


@overload
def AthenaSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Athena integration, there's no need to provide
    a distinguishing name.
    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        The name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = AthenaSource(name="RISK")
    """
    ...


@overload
def AthenaSource(
    *,
    name: str | None = None,
    aws_region: str | None = None,
    aws_access_key_id: str | None = None,
    aws_access_key_secret: str | None = None,
    s3_staging_dir: str | None = None,
    catalog_name: str | None = None,
    schema_name: str | None = None,
    role_arn: str | None = None,
    work_group: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        The name of the integration. Not required unless if this SQL Source
        is used within SQL File Resolvers.
    aws_access_key_id
        Optionally override the credentials using an AWS client id, must be
        provided with a client secret override.
    aws_access_key_secret
        Optionally override the credentials using an AWS client secret, must
        be provided with a client id override.
    role_arn
        Optionally override the credentials using an AWS role ARN.
    aws_region
        The AWS region code to connect to, such as `"us-east-1"`.
    s3_staging_dir
        The query result location to store query results within s3.
    work_group
        Optionally provide an Athena work group to query from.
    catalog_name
        The catalog name to query. Defaults to "default".
    schema_name
        The schema (database) name to query. Defaults to "awsdatacatalog".
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = AthenaSource(name="RISK")
    """
    ...


def AthenaSource(
    name: str | None = None,
    aws_region: str | None = None,
    aws_access_key_id: str | None = None,
    aws_access_key_secret: str | None = None,
    s3_staging_dir: str | None = None,
    catalog_name: str | None = None,
    schema_name: str | None = None,
    role_arn: str | None = None,
    work_group: str | None = None,
    engine_args: Dict[str, Any] | None = None,
) -> BaseSQLSourceProtocol:
    """Create an Amazon Athena data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details. DynamoDBSources can be queried via PartiQL SQL
    resolvers.

    You may override the ambient AWS credentials by providing
    either a client ID and secret, or a role ARN.
    """
    return AthenaSourceImpl(
        name=name,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_access_key_secret=aws_access_key_secret,
        s3_staging_dir=s3_staging_dir,
        schema_name=schema_name,
        catalog_name=catalog_name,
        work_group=work_group,
        role_arn=role_arn,
        engine_args=engine_args,
    )


@overload
def ClickhouseSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Clickhouse connection that you'd like
    to add to Chalk, you do not need to specify any arguments
    to construct the source in your code.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = ClickhouseSource()
    """
    ...


@overload
def ClickhouseSource(
    *,
    name: str,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """If you have only one Clickhouse integration, there's no need to provide
    a distinguishing name.

    But what happens when you have two data sources of the same kind?
    When you create a new data source from your dashboard,
    you have an option to provide a name for the integration.
    You can then reference this name in the code directly.

    Parameters
    ----------
    name
        Name of the integration, as configured in your dashboard.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine. These arguments will be
        merged with any default arguments from the named integration.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> source = ClickhouseSource(name="RISK")
    """
    ...


@overload
def ClickhouseSource(
    *,
    name: str | None = ...,
    host: str,
    port: Union[int, str] = ...,
    db: str = ...,
    user: str = ...,
    password: str = ...,
    use_tls: Union[bool, str] = ...,
    engine_args: Optional[Dict[str, Any]] = ...,
    async_engine_args: Optional[Dict[str, Any]] = ...,
) -> BaseSQLSourceProtocol:
    """
    You can also configure the integration directly using environment
    variables on your local machine or from those added through the
    generic environment variable support (https://docs.chalk.ai/docs/env-vars).

    Parameters
    ----------
    name
        Name of the integration. Not required unless if this SQL Source is used within SQL File Resolvers.
    host
        Name of host to connect to.
    port
        The port number to connect to at the server host.
    db
        The database name.
    user
        Clickhouse username to connect as.
    password
        The password to be used if the server demands password authentication.
    use_tls
        Whether to use tls protocol when communicating with the clickhouse engine, required for certain ports.
        See https://clickhouse.com/docs/guides/sre/network-ports for more details. Defaults to True.
    engine_args
        Additional arguments to use when constructing the SQLAlchemy engine.
    async_engine_args:
        Additional arguments to use when constructing an async SQLAlchemy engine.

    Returns
    -------
    BaseSQLSourceProtocol
        The SQL source for use in Chalk resolvers.

    Examples
    --------
    >>> import os
    >>> source = ClickhouseSource(
    ...     host=os.getenv("CLICKHOUSE_HOST"),
    ...     port=os.getenv("CLICKHOUSE_PORT"),
    ...     db=os.getenv("CLICKHOUSE_DATABASE"),
    ...     user=os.getenv("CLICKHOUSE_USER"),
    ...     password=os.getenv("CLICKHOUSE_PASSWORD"),
    ...     use_tls=os.getenv("CLICKHOUSE_USE_TLS"),
    ... )
    >>> from chalk.features import online
    >>> @online
    ... def resolver_fn() -> User.name:
    ...     return source.query_string("select name from users where id = 4").one()
    """
    ...


def ClickhouseSource(
    *,
    name: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[Union[int, str]] = None,
    db: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    use_tls: Optional[Union[bool, str]] = None,
    engine_args: Optional[Dict[str, Any]] = None,
    async_engine_args: Optional[Dict[str, Any]] = None,
) -> BaseSQLSourceProtocol:
    """Create a Clickhouse data source. SQL-based data sources
    created without arguments assume a configuration in your
    Chalk Dashboard. Those created with the `name=` keyword
    argument will use the configuration for the integration
    with the given name. And finally, those created with
    explicit arguments will use those arguments to configure
    the data source. See the overloaded signatures for more
    details.
    """
    return ClickhouseSourceImpl(
        name=name,
        host=host,
        port=port,
        db=db,
        user=user,
        password=password,
        use_tls=use_tls,
        engine_args=engine_args,
        async_engine_args=async_engine_args,
    )


__all__ = (
    "AthenaSource",
    "BaseSQLSourceProtocol",
    "BigQuerySource",
    "ChalkQueryProtocol",
    "ClickhouseSource",
    "CloudSQLSource",
    "DatabricksSource",
    "DynamoDBSource",
    "FinalizedChalkQuery",
    "IncrementalSettings",
    "MySQLSource",
    "PostgreSQLSource",
    "RedshiftSource",
    "SQLSourceGroup",
    "SQLSourceWithTableIngestProtocol",
    "SQLiteFileSource",
    "SQLiteInMemorySource",
    "SnowflakeSource",
    "SpannerSource",
    "StringChalkQueryProtocol",
    "TableIngestProtocol",
    "TrinoSource",
    "make_sql_file_resolver",
)
