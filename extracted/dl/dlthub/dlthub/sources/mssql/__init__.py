from functools import partial, update_wrapper
from typing import Any, Callable, Dict, Final, Iterator, List, Optional, Tuple, Union

try:
    import pyodbc as pyodbc
except ImportError:
    from dlt.common.exceptions import MissingDependencyException
    from dlthub import version

    raise MissingDependencyException(
        "dlthub mssql source",
        [f"{version.PKG_NAME}[mssql]"],
        "needs sqlalchemy, pyodbc and odbc binary driver for MSSQL",
    )

import dlt
from dlt.common.configuration.specs import ConnectionStringCredentials
from dlt.common.libs.sql_alchemy import Engine, MetaData, Table, TextClause, sa, Column
from dlt.common.schema.typing import TWriteDispositionConfig
from dlt.common.typing import TDataItem
from dlt.extract import DltResource, Incremental
from dlt.extract.state import resource_state
from dlt.sources.sql_database import (
    TableBackend,
    TTypeAdapter,
    TTableAdapter,
    sql_table,
)
from dlt.sources.sql_database.helpers import BaseTableLoader, get_table_loader_class
from dlt.sources.sql_database.schema_types import ReflectionLevel, SelectAny

from dlthub.common.license import require_license
from dlthub.sources.mssql.exceptions import ChangeTrackingVersionExpired

CT_CHECKED_VERSION_KEY = "ct_checked_version"
"""Resource state key with the database version all changes were read up to."""
CT_CURRENT_VERSION: Final = sa.func.CHANGE_TRACKING_CURRENT_VERSION(type_=sa.BigInteger)
"""Expression for the version of the last change committed in the database."""


@require_license(scope="dlthub.sources.mssql")
def get_current_change_tracking_version(engine: Engine) -> int:
    """Returns the current change tracking version of the SQL Server database."""
    try:
        with engine.connect() as conn:
            current_version = conn.execute(sa.select(CT_CURRENT_VERSION)).scalar()
            return int(current_version)
    except Exception as e:
        raise RuntimeError("Failed to retrieve change tracking version.") from e


def remove_nullability_adapter(table: Table) -> Table:
    """A table adapter that removes nullability from columns that are not primary keys"""
    for col in table.columns:
        # keep nullability on primary keys
        # subqueries may not have nullable attr
        if hasattr(col, "nullable") and col.primary_key is False:
            col.nullable = None
    return table


def add_change_tracking_columns(remove_nullability_info: bool) -> TTableAdapter:
    """
    Adds required tracking columns to the table if they do not exist.
    """

    def _add_change_tracking_columns(table: Table) -> None:
        if remove_nullability_info:
            # Remove nullability info from table, keep the one from sql_table
            table = remove_nullability_adapter(table)

        # SQL Server doesn't support bool type - column _dlt_deleted is text instead
        required_columns = [
            ("_dlt_sys_change_version", sa.BigInteger, {"nullable": True}),
            ("_dlt_deleted", sa.Text, {"default": None, "nullable": True}),
        ]

        for col_name, col_type, col_kwargs in required_columns:
            if col_name not in table.c:
                table.append_column(
                    sa.Column(col_name, col_type, **col_kwargs)  # type: ignore[arg-type]
                )

    return _add_change_tracking_columns


def placeholder_for_type(col_type: sa.types.TypeEngine[Any]) -> str:
    if isinstance(col_type, sa.String):
        return "''"
    elif isinstance(col_type, sa.Integer):
        return "0"
    elif isinstance(col_type, sa.Numeric):
        return "0"
    elif isinstance(col_type, sa.Boolean):
        # ISNULL for a boolean would still need a numeric or bit value.
        # SQL Server bit: 0 = False, 1 = True. We'll choose 0.
        return "0"
    elif isinstance(col_type, sa.Date):
        return "'1900-01-01'"
    elif isinstance(col_type, sa.DateTime):
        return "'1900-01-01'"
    elif isinstance(col_type, sa.Time):
        return "'00:00:00'"
    elif isinstance(col_type, sa.LargeBinary):
        # Empty binary placeholder
        return "0x0"
    elif isinstance(col_type, sa.dialects.mssql.UNIQUEIDENTIFIER):
        return "NEWID()"
    # Default fallback for any other type
    return "''"


def build_change_tracking_query(
    query: SelectAny,
    table: Table,
    incremental: Incremental[Any] = None,
    engine: Engine = None,
    *,
    start_version: Optional[int] = None,
) -> TextClause:
    """Builds a CHANGETABLE query for changes after `start_version` or the cursor."""
    if start_version is None:
        start_version = incremental.last_value
    table_fullname = table.fullname

    # Exclude tracking columns from selection
    columns = [
        col for col in table.columns if col.name not in ("_dlt_sys_change_version", "_dlt_deleted")
    ]
    primary_key_columns = [pk.name for pk in table.primary_key.columns]

    def build_column_expression(col: Column[Any]) -> str:
        expr_source = "ct" if col.name in primary_key_columns else "t"
        base_expr = f"{expr_source}.[{col.name}]"
        if col.nullable is False:  # and not col.primary_key:
            # use ISNULL to provide a placeholder for NULL values
            placeholder = placeholder_for_type(col.type)
            return f"ISNULL({base_expr}, {placeholder}) AS [{col.name}]"
        else:
            return f"{base_expr} AS [{col.name}]"

    # Build the list of columns to select, choosing from 'ct' or 't' based on primary key
    column_names_str = ", ".join(build_column_expression(col) for col in columns)

    join_conditions = " AND ".join(f"ct.[{pk}] = t.[{pk}]" for pk in primary_key_columns)

    # Construct the query using CHANGETABLE
    t_query = sa.text(f"""
    SELECT
        {column_names_str},
        ct.SYS_CHANGE_VERSION AS _dlt_sys_change_version,
        CASE WHEN ct.SYS_CHANGE_OPERATION = 'D' THEN 'D' ELSE NULL END AS _dlt_deleted
    FROM
        CHANGETABLE(CHANGES {table_fullname}, :last_version) AS ct
        LEFT JOIN {table_fullname} AS t
            ON {join_conditions}
    WHERE
        ct.SYS_CHANGE_VERSION > :last_version
    ORDER BY
        ct.SYS_CHANGE_VERSION ASC
    """).bindparams(last_version=start_version)

    return t_query


def _newer_change_tracking_version(*versions: Optional[int]) -> Optional[int]:
    """Returns the highest of the versions that are not `None`, or `None`."""
    return max((version for version in versions if version is not None), default=None)


def _read_change_tracking_versions(
    engine: Engine, table: Table
) -> Tuple[Optional[int], Optional[int]]:
    """Returns the current database version and the min valid version of `table`."""
    object_name = engine.dialect.identifier_preparer.format_table(table)
    min_valid_version = sa.func.CHANGE_TRACKING_MIN_VALID_VERSION(
        sa.func.OBJECT_ID(object_name), type_=sa.BigInteger
    )
    with engine.connect() as conn:
        current_version, min_valid = conn.execute(
            sa.select(CT_CURRENT_VERSION, min_valid_version)
        ).one()
    return current_version, min_valid


class ChangeTrackingTableLoader(BaseTableLoader):
    """Loads changes with the backend's loader and records the checked version."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._loader_args = args
        self._loader_kwargs = kwargs

    def load_rows(self, backend_kwargs: Dict[str, Any] = None) -> Iterator[TDataItem]:
        tracks_checked_version = self.last_value is not None and self.end_value is None
        state = resource_state(self.incremental.resource_name)
        start_version = self.last_value
        if tracks_checked_version:
            start_version = _newer_change_tracking_version(
                start_version, state.get(CT_CHECKED_VERSION_KEY)
            )
        current_version = None
        if start_version is not None:
            # read before the change query so changes committed meanwhile are not skipped
            current_version, min_valid = _read_change_tracking_versions(self.engine, self.table)
            if min_valid is not None and start_version < min_valid:
                raise ChangeTrackingVersionExpired(self.table.fullname, start_version, min_valid)

        query_adapter = update_wrapper(
            partial(build_change_tracking_query, start_version=start_version),
            build_change_tracking_query,
        )
        loader = get_table_loader_class(self.backend)(
            *self._loader_args,
            **{**self._loader_kwargs, "query_adapter_callback": query_adapter},
        )
        yield from loader.load_rows(backend_kwargs)

        # reached only when all changes were yielded, not on error or early close
        if tracks_checked_version:
            checked_version = _newer_change_tracking_version(
                current_version, state.get(CT_CHECKED_VERSION_KEY)
            )
            if checked_version is not None:
                state[CT_CHECKED_VERSION_KEY] = checked_version


@require_license(scope="dlthub.sources.mssql")
def create_change_tracking_table(
    credentials: Union[ConnectionStringCredentials, Engine, str] = dlt.secrets.value,
    table: str = dlt.config.value,
    schema: Optional[str] = dlt.config.value,
    metadata: Optional[MetaData] = None,
    initial_tracking_version: int = None,
    hard_delete: bool = True,
    write_disposition: TWriteDispositionConfig = "merge",
    chunk_size: int = 50000,
    backend: TableBackend = "sqlalchemy",
    backend_kwargs: Dict[str, Any] = None,
    reflection_level: Optional[ReflectionLevel] = "full",
    defer_table_reflect: Optional[bool] = None,
    type_adapter_callback: Optional[TTypeAdapter] = None,
    included_columns: Optional[List[str]] = None,
    resolve_foreign_keys: bool = False,
    engine_adapter_callback: Callable[[Engine], Engine] = None,
) -> DltResource:
    """
    Creates a DLT resource to incrementally load data from a SQL Server table using change tracking.

    This resource leverages SQL Server's change tracking feature to detect and load incremental
    changes (inserts, updates, and deletes) from the specified table. It supports both hard and
    soft deletes in the destination based on the `hard_delete` flag.

    Args:
        credentials (Union[ConnectionStringCredentials, Engine, str]): Database credentials or an
            `Engine` instance representing the database connection.

        table (str): Name of the table or view to load.

        schema (Optional[str]): Optional name of the schema the table belongs to.

        metadata (Optional[MetaData]): Optional `sqlalchemy.MetaData` instance. If provided, the
            `schema` argument is ignored.

        initial_tracking_version (int): The starting change tracking version from the SQL Server
            database.
            This version indicates the point in time from which the resource will begin tracking and
            loading data changes. Use the current change tracking version of your SQL Server
            database to ensure all subsequent changes are captured.
            You provide this value only during the initial load to initialize incremental state.
            It is ignored in the subsequent loads, so you are free to skip it.

        hard_delete (bool): Determines whether to perform hard deletes in the destination when data
            is deleted in the source.
            If `True`, rows deleted in the source will be permanently removed from the destination
                dataset.
            If `False`, deleted rows will be soft deleted in the destination (typically marked as
                deleted but not physically removed). Defaults to `True`.

        write_disposition (TTableHintTemplate[TWriteDispositionConfig]): Controls how to write data
            to a table. Accepts a shorthand string literal or configuration dictionary.
            Allowed shorthand string literals: `append` will always add new data at the end of the
            table. `replace` will replace existing data with new data. `skip` will prevent data from
            loading. "merge" will deduplicate and merge data based on "primary_key" and "merge_key"
            hints. Defaults to "merge".
            Write behavior can be further customized through a configuration dictionary.
            For example, to obtain an SCD2 table provide
            `write_disposition={"disposition": "merge", "strategy": "scd2"}`.
            This argument also accepts a callable that is used to dynamically create tables for
            stream-like resources yielding many datatypes.

        chunk_size (int): Number of rows yielded in one batch. SQL Alchemy will create additional
            internal rows buffer twice the chunk size.

        backend (TableBackend): Type of backend to generate table data.
            One of: "sqlalchemy", "pyarrow", and "pandas".
            "sqlalchemy" yields batches as lists of Python dictionaries, and "pyarrow" yield batches
                as arrow tables, "pandas" yields panda frames.
            "sqlalchemy" is the default and does not require additional dependencies,
                "pyarrow" creates stable destination schemas with correct data types.

        backend_kwargs (**kwargs): kwargs passed to table backend.

        reflection_level: (ReflectionLevel): Specifies how much information should be reflected from
            the source database schema.
            "minimal": Only table names, nullability and primary keys are reflected.
                Data types are inferred from the data.
            "full": Data types will be reflected on top of "minimal". `dlt` will coerce the data
                into reflected types if necessary. This is the default option.
            "full_with_precision": Sets precision and scale on supported data types
                (ie. decimal, text, binary). Creates big and regular integer types.

        defer_table_reflect (bool): Will connect and reflect table schema only when yielding data.
            Enable this option when running on Airflow. Available on dlt 0.4.4 and later

        type_adapter_callback(Optional[Callable]): Callable to override type inference when
            reflecting columns.
            Argument is a single sqlalchemy data type (`TypeEngine` instance) and it should return
            another sqlalchemy data type, or `None` (type will be inferred from data)

        included_columns (Optional[List[str]): List of column names to select from the table.
            If not provided, all columns are loaded.

        resolve_foreign_keys (bool): Translate foreign keys in the same schema to `references`
            table hints. May incur additional database calls as all referenced tables are reflected.

        engine_adapter_callback (Callable[[Engine], Engine]): Callback to configure, modify
            and Engine instance that will be used to open a connection
            ie. to set transaction isolation level.

    Returns:
        DltResource: The dlt resource for loading data from the SQL Server database table.
    """
    incremental = dlt.sources.incremental(
        "_dlt_sys_change_version",
        on_cursor_value_missing="include",
        row_order="asc",
        primary_key=(),  # disable dedup primary key
        initial_value=initial_tracking_version,
    )

    resource = sql_table(
        credentials=credentials,
        schema=schema,
        table=table,
        incremental=incremental,
        reflection_level=reflection_level,
        table_adapter_callback=add_change_tracking_columns(remove_nullability_info=not hard_delete),
        query_adapter_callback=build_change_tracking_query,
        table_loader_class=ChangeTrackingTableLoader,
        engine_adapter_callback=engine_adapter_callback,
        backend=backend,
        metadata=metadata,
        chunk_size=chunk_size,
        defer_table_reflect=defer_table_reflect,
        backend_kwargs=backend_kwargs,
        type_adapter_callback=type_adapter_callback,
        included_columns=included_columns,
        resolve_foreign_keys=resolve_foreign_keys,
        write_disposition=write_disposition,
    )

    resource.apply_hints(columns={"_dlt_deleted": {"hard_delete": hard_delete}})

    return resource
