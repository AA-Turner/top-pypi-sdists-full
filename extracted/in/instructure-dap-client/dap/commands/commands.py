import asyncclick as click
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional, Type


from .. import ui
from ..actions.download_incremental import download_incremental
from ..actions.download_schema import download_schema
from ..actions.download_snapshot import download_snapshot
from ..actions.drop_db import drop_db
from ..actions.init_db import init_db
from ..actions.list_tables import list_tables
from ..actions.sync_db import sync_db
from ..dap_types import Credentials, Format
from ..integration.database import get_parameters
from ..log import set_namespace, set_table
from ..timestamp import valid_utc_datetime
from .global_options import GlobalOptions, pass_global_options

logger: logging.Logger = logging.getLogger(__name__)


class EnumType(click.Choice):
    enum_class: Type[Enum]

    def __init__(self, enum_class: Type[Enum]) -> None:
        self.enum_class = enum_class
        super().__init__([e.value for e in enum_class])

    def convert(
        self, value: Any, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> Any:
        if value is None:
            return None

        return self.enum_class(super().convert(value, param, ctx))


def dap_command(help_text: str) -> Callable:
    def decorator(f: Callable) -> Any:
        return click.command(help=help_text, short_help=help_text)(f)

    return decorator


def namespace_option_callback(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    set_namespace(value)
    return value


def namespace_option(f: Callable) -> Callable:
    return click.option(
        "--namespace",
        type=click.STRING,
        required=True,
        metavar="NAMESPACE",
        help="Identifies the data source.",
        callback=namespace_option_callback,
    )(f)


def table_option_callback(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    set_table(value)
    return value


def table_option(f: Callable) -> Callable:
    return click.option(
        "--table",
        type=click.STRING,
        required=True,
        metavar="TABLE",
        help="Table name or comma separated list of table names whose data to fetch. Use 'all' to fetch all tables in the namespace.",
        callback=table_option_callback,
    )(f)


def format_option(f: Callable) -> Callable:
    return click.option(
        "--format",
        type=EnumType(Format),
        default=Format.JSONL.value,
        show_default=True,
        help="Data output format.",
    )(f)


def output_dir_option(f: Callable) -> Callable:
    return click.option(
        "--output-directory",
        type=click.Path(exists=False, writable=True),
        default="downloads",
        show_default=True,
        metavar="DIR",
        help="Directory where the query result will be downloaded to. Can be an absolute or relative path.",
    )(f)


def since_option(f: Callable) -> Callable:
    return click.option(
        "--since",
        type=valid_utc_datetime,
        required=True,
        metavar="DATETIME",
        help="Start timestamp for an incremental query. Examples: 2022-06-13T09:30:00Z or 2022-06-13T09:30:00+02:00.",
    )(f)


def until_option(f: Callable) -> Callable:
    return click.option(
        "--until",
        type=valid_utc_datetime,
        default=None,
        show_default=True,
        metavar="DATETIME",
        help="End timestamp for an incremental query. Examples: 2022-06-13T09:30:00Z or 2022-06-13T09:30:00+02:00.",
    )(f)


def connection_string_option_callback(
    ctx: click.Context, param: click.Parameter, value: Any
) -> Any:
    if not value:
        raise ValueError(
            "Missing database connection string. Please provide a valid connection string."
        )

    logger.debug("Checking for valid database connection string")
    try:
        _, _ = get_parameters(value)

        return value
    except ValueError:
        err_str = (
            "Invalid database connection string. "
            "Please verify its format and ensure special characters are properly URL-encoded."
        )

        ui.error(err_str)
        logger.error(err_str)
        raise


def connection_string_option(f: Callable) -> Callable:
    return click.option(
        "--connection-string",
        type=click.STRING,
        metavar="DBCONNSTR",
        help="The connection string used to connect to the target database. May be set via environment variable DAP_CONNECTION_STRING.",
        envvar="DAP_CONNECTION_STRING",
        callback=connection_string_option_callback,
    )(f)


@dap_command(
    "Lists the name of all tables available for querying in the specified namespace.",
)
@pass_global_options
@namespace_option
async def list(
    global_options: GlobalOptions,
    namespace: str,
) -> None:
    logger.debug(
        "Running list command with parameters: namespace=%s",
        namespace,
    )

    await list_tables(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        namespace=namespace,
        tracking=global_options.tracking,
    )


@dap_command("Returns the JSON schema that records in the table conform to.")
@pass_global_options
@namespace_option
@table_option
@output_dir_option
async def schema(
    global_options: GlobalOptions, namespace: str, table: str, output_directory: str
) -> None:
    logger.debug(
        "Running schema command with parameters: namespace=%s, table=%s",
        namespace,
        table,
    )

    await download_schema(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        namespace=namespace,
        table=table,
        output_directory=output_directory,
        tracking=global_options.tracking,
    )


@dap_command("Performs a snapshot query.")
@pass_global_options
@namespace_option
@table_option
@format_option
@output_dir_option
async def snapshot(
    global_options: GlobalOptions,
    namespace: str,
    table: str,
    format: Format,
    output_directory: str,
) -> None:
    logger.debug(
        "Running snapshot command with parameters: namespace=%s, table=%s, format=%s, output_directory=%s",
        namespace,
        table,
        format,
        output_directory,
    )

    await download_snapshot(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        namespace=namespace,
        table=table,
        format=format,
        output_directory=output_directory,
        tracking=global_options.tracking,
    )


@dap_command(
    "Performs an incremental query with a given start, and (optionally) end timestamp.",
)
@pass_global_options
@namespace_option
@table_option
@format_option
@output_dir_option
@since_option
@until_option
async def incremental(
    global_options: GlobalOptions,
    namespace: str,
    table: str,
    format: Format,
    output_directory: str,
    since: datetime,
    until: Optional[datetime],
) -> None:
    logger.debug(
        "Running incremental command with parameters: namespace=%s, table=%s, format=%s, output_directory=%s, since=%s, until=%s",
        namespace,
        table,
        format,
        output_directory,
        since.isoformat(),
        until.isoformat() if until else "None",
    )

    await download_incremental(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        namespace=namespace,
        table=table,
        format=format,
        output_directory=output_directory,
        since=since,
        until=until,
        tracking=global_options.tracking,
    )


@dap_command(
    "Performs a snapshot query and persists the result in the database for given table(s).",
)
@pass_global_options
@namespace_option
@table_option
@connection_string_option
async def initdb(
    global_options: GlobalOptions, namespace: str, table: str, connection_string: str
) -> None:
    logger.debug(
        "Running initdb command with parameters: namespace=%s, table=%s, connection_string=%s",
        namespace,
        table,
        connection_string,
    )

    await init_db(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        connection_string=connection_string,
        namespace=namespace,
        table_names=table,
        tracking=global_options.tracking,
    )


@dap_command(
    "Performs an incremental query and persists the result in the database for given table(s).",
)
@pass_global_options
@namespace_option
@table_option
@connection_string_option
async def syncdb(
    global_options: GlobalOptions, namespace: str, table: str, connection_string: str
) -> None:
    logger.debug(
        "Running syncdb command with parameters: namespace=%s, table=%s, connection_string=%s",
        namespace,
        table,
        connection_string,
    )

    await sync_db(
        base_url=global_options.base_url,
        credentials=Credentials.create(
            client_id=global_options.client_id,
            client_secret=global_options.client_secret,
        ),
        connection_string=connection_string,
        namespace=namespace,
        table_names=table,
        tracking=global_options.tracking,
    )


@dap_command("Drops table(s) from the database.")
@namespace_option
@table_option
@connection_string_option
async def dropdb(namespace: str, table: str, connection_string: str) -> None:
    logger.debug(
        "Running dropdb command with parameters: namespace=%s, table=%s, connection_string=%s",
        namespace,
        table,
        connection_string,
    )

    await drop_db(
        connection_string=connection_string,
        namespace=namespace,
        table_names=table,
    )
