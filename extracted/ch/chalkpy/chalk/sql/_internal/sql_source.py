from __future__ import annotations

import asyncio
import contextlib
import inspect
import json
import logging
import os
import os.path
import traceback
import warnings
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import pyarrow as pa

from chalk.clogging import chalk_logger
from chalk.features import Feature, FeatureConverter, Features, FeatureWrapper, unwrap_feature
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.chalk_query import ChalkQuery
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql._internal.query_execution_parameters import (
    QueryExecutionParameters,
    query_execution_parameters_from_env_vars,
)
from chalk.sql._internal.string_chalk_query import StringChalkQuery
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, StringChalkQueryProtocol, TableIngestProtocol
from chalk.utils.async_helpers import async_null_context, to_async_iterable
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger, get_logging_context
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import sqlalchemy.ext.asyncio
    from sqlalchemy.engine import URL, Connection, Dialect, Engine
    from sqlalchemy.orm import Session
    from sqlalchemy.sql import Select
    from sqlalchemy.sql.compiler import SQLCompiler
    from sqlalchemy.sql.ddl import CreateTable, DropTable
    from sqlalchemy.sql.elements import Label
    from sqlalchemy.sql.schema import Table
    from sqlalchemy.types import TypeEngine


TTableIngestMixIn = TypeVar("TTableIngestMixIn", bound="TableIngestMixIn")
CHALK_QUERY_LOGGING = env_var_bool("CHALK_QUERY_LOGGING")

_logger = get_logger(__name__)


@dataclass
class TableIngestionPreferences:
    features: Type[Features]
    ignore_columns: Set[str]
    ignore_features: Set[str]
    require_columns: Set[str]
    require_features: Set[str]
    column_to_feature: Dict[str, str]
    cdc: Optional[Union[bool, IncrementalSettings]]


def _force_set_str(x: Optional[List[Any]]) -> Set[str]:
    return set() if x is None else set(map(str, x))


class UnsupportedEfficientExecutionError(ValueError):
    def __init__(self, msg: str, log_level: int) -> None:
        super().__init__(msg)
        self.log_level = log_level


def validate_dtypes_for_efficient_execution(stmt: Select, supported_types: Sequence[Type[TypeEngine]]):
    unsupported_columns = [
        x
        for x in stmt.column_descriptions
        # Using NOT IN rather than not isinstance() as subclasses may override the result processor,
        # which makes it not eligible for efficient execution
        if x["type"].__class__ not in supported_types
    ]
    if len(unsupported_columns) == 1 and unsupported_columns[0]["name"] == "*":
        _logger.warning(
            "Got '*' for select clause. Will try efficient execution and fallback if unsupported types are found."
        )
        return

    if len(unsupported_columns) > 0:
        unsupported_columns_and_dtypes = [(x["name"], x["type"].__class__.__name__) for x in unsupported_columns]
        supported_dtypes = [x.__name__ for x in supported_types]
        formatted_supported = ", ".join(supported_dtypes)
        formatted_unsupported = ", ".join([f"{name} ({dtype})" for (name, dtype) in unsupported_columns_and_dtypes])
        raise UnsupportedEfficientExecutionError(
            (
                "The SQL statement will be executed into SQLAlchemy objects, as the SQL query returns columns "
                "that cannot be loaded directly into a PyArrow table. For better performance, use only "
                f"the following types in your SQLAlchemy model: {formatted_supported}."
                f"The columns that contain unsupported types are: {formatted_unsupported}."
            ),
            log_level=logging.INFO,
        )


class TableIngestMixIn(TableIngestProtocol):
    ingested_tables: Dict[str, TableIngestionPreferences]

    def with_table(
        self: TTableIngestMixIn,
        *,
        name: str,
        features: Type[Union[Features, Any]],
        ignore_columns: Optional[List[str]] = None,
        ignore_features: Optional[List[Union[str, Any]]] = None,
        require_columns: Optional[List[str]] = None,
        require_features: Optional[List[Union[str, Any]]] = None,
        column_to_feature: Optional[Dict[str, Any]] = None,
        cdc: Optional[Union[bool, IncrementalSettings]] = None,
    ) -> TTableIngestMixIn:
        if name in self.ingested_tables:
            raise ValueError(f"The table {name} is ingested twice.")
        self.ingested_tables[name] = TableIngestionPreferences(
            features=features,
            ignore_columns=_force_set_str(ignore_columns),
            ignore_features=_force_set_str(ignore_features),
            require_columns=_force_set_str(require_columns),
            require_features=_force_set_str(require_features),
            column_to_feature={k: str(v) for k, v in (column_to_feature or {}).items()},
            cdc=cdc,
        )
        return self


class SQLSourceKind(str, Enum):
    bigquery = "bigquery"
    clickhouse = "clickhouse"
    cloudsql = "cloudsql"
    databricks = "databricks"
    athena = "athena"
    duckdb = "duckdb"
    dynamodb = "dynamodb"
    mysql = "mysql"
    postgres = "postgres"
    redshift = "redshift"
    snowflake = "snowflake"
    spanner = "spanner"
    sqlite = "sqlite"
    trino = "trino"

    @staticmethod
    def convert_sql_source_kind(kind: str) -> SQLSourceKind:
        try:
            return SQLSourceKind(kind)
        except ValueError:
            raise ValueError(f"Unsupported SQL source kind: {kind}")


class BaseSQLSource(BaseSQLSourceProtocol):
    registry: ClassVar[List["BaseSQLSource"]] = []

    kind: SQLSourceKind

    def __init__(
        self,
        name: Optional[str],
        engine_args: Optional[Dict[str, Any]],
        async_engine_args: Optional[Dict[str, Any]],
    ):
        super().__init__()
        try:
            import sqlalchemy
        except ImportError:
            raise missing_dependency_exception("chalkpy[sql]")
        del sqlalchemy  # unused

        self._incremental_settings = None
        self._resolver_and_sqlfile_to_sqlstring: Dict[Tuple[str, str], str] = {}
        self.registry.append(self)
        self.name = name
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}
        if self.name is not None:
            for k, v in self._load_env_engine_args(name=self.name, override=None).items():
                engine_args.setdefault(k, v)
                async_engine_args.setdefault(k, v)
        if getattr(self, "kind", None) != SQLSourceKind.trino:
            engine_args.setdefault("pool_pre_ping", env_var_bool("USE_CLIENT_POOL_PRE_PING"))
            engine_args.setdefault("echo", CHALK_QUERY_LOGGING)
            async_engine_args.setdefault("pool_pre_ping", env_var_bool("USE_CLIENT_POOL_PRE_PING"))
            async_engine_args.setdefault("echo", CHALK_QUERY_LOGGING)
        self.engine_args = engine_args
        self.async_engine_args = async_engine_args
        self._engine = None
        self._async_engine = None

    @property
    def _engine_args(self):
        """Backcompat support for private subclassing of BaseSQLSource"""
        return self.engine_args

    @_engine_args.setter
    def _engine_args(self, args: dict[str, Any]):
        """Backcompat support for private subclassing of BaseSQLSource"""
        self.engine_args = args

    @property
    def _async_engine_args(self):
        """Backcompat support for private subclassing of BaseSQLSource"""
        return self.async_engine_args

    @_async_engine_args.setter
    def _async_engine_args(self, args: dict[str, Any]):
        """Backcompat support for private subclassing of BaseSQLSource"""
        self.async_engine_args = args

    def get_sqlglot_dialect(self) -> Union[str, None]:
        """Returns the name of the SQL dialect (if it has one) for `sqlglot` to parse the SQL string.
        This allows for use of dialect-specific syntax while parsing and modifying queries."""
        return None

    def supports_inefficient_fallback(self) -> bool:
        return True

    def query_sql_file(
        self,
        path: Union[str, bytes, PathLike],
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:
        sql_string = None
        if isinstance(path, bytes):
            path = path.decode("utf-8")

        resolver_fqn = get_logging_context().get("labels", {}).get("resolver_fqn")
        if resolver_fqn is not None:
            sql_string = self._resolver_and_sqlfile_to_sqlstring.get((resolver_fqn, str(path)))
        uncached = sql_string is None

        if uncached:
            _logger.info(f"SQL query for resolver '{resolver_fqn}' from file '{str(path)}' is not cached")
            if os.path.isfile(path):
                with open(path) as f:
                    sql_string = f.read()
            else:
                frame = inspect.currentframe()
                assert frame is not None
                caller_frame = frame.f_back
                assert caller_frame is not None
                while caller_frame.f_globals["__name__"].startswith("chalk.sql") and caller_frame.f_back is not None:
                    caller_frame = caller_frame.f_back
                dir_path = os.path.dirname(os.path.realpath(inspect.getframeinfo(caller_frame).filename))
                path = str(path)
                relative_path = os.path.join(dir_path, path)
                if os.path.isfile(relative_path):
                    with open(relative_path) as f:
                        sql_string = f.read()
        if sql_string is None:
            raise FileNotFoundError(f"No such file: '{str(path)}'")

        if uncached and resolver_fqn is not None:
            # Caching by the resolver fqn because the file path could be relative
            # to the file that the resolver is defined in
            self._resolver_and_sqlfile_to_sqlstring[(resolver_fqn, str(path))] = sql_string

        return self.query_string(
            query=sql_string,
            fields=fields,
            args=args,
        )

    def query_string(
        self,
        query: str,
        fields: Optional[Mapping[str, Union[Feature, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:
        fields = fields or {}
        fields = {f: unwrap_feature(v) if isinstance(v, FeatureWrapper) else v for (f, v) in fields.items()}
        return StringChalkQuery(source=self, query=query, fields=fields, params=args or {})

    def warm_up(self) -> None:
        from sqlalchemy import text

        with self.get_engine().connect() as cnx:
            cnx.execute(text("select 1"))

    def query(self, *entities: Any) -> ChalkQueryProtocol:
        targets: List[Label] = []
        features: Dict[str, Feature] = {}

        for e in entities:
            if isinstance(e, Features):
                _extract_features(e, e.__chalk_namespace__, targets, features)
            else:
                targets.append(e)

        return ChalkQuery(
            features=features,
            targets=targets,
            source=self,
        )

    def local_engine_url(self) -> URL:
        raise NotImplementedError

    def async_local_engine_url(self) -> URL:
        raise NotImplementedError

    def execute_query(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> Iterable[pa.RecordBatch]:
        if query_execution_parameters is None:
            """
            Sometimes, in tests or in development or in user resolver code,
            we may not have the query_execution_parameters argument
            passed in. Thus, we need to hack the env vars in.
            """
            query_execution_parameters = query_execution_parameters_from_env_vars()

        efficient_execution_failed: bool = False
        efficient_execution_traceback: str | None = None
        attempt_efficient_execution = query_execution_parameters.attempt_efficient_execution
        if attempt_efficient_execution:
            try:
                yield from self._execute_query_efficient(
                    finalized_query, columns_to_features, connection, query_execution_parameters
                )
                return
            except NotImplementedError:
                _logger.debug(
                    (
                        "The SQL statement will be executed into SQLAlchemy objects, as the database backend does "
                        "not support a more efficient execution mechanism."
                    )
                )
                pass
            except UnsupportedEfficientExecutionError as e:
                log_level = e.log_level
                _logger.log(log_level, str(e))
            except Exception:
                if (
                    query_execution_parameters.fallback_to_inefficient_execution
                    and self.supports_inefficient_fallback()
                ):
                    _logger.error(
                        (
                            f"Failed to efficiently execute query {finalized_query.query.compile(compile_kwargs={'literal_binds': True})} "
                            f"with parameters {finalized_query.params} due to an unexpected error. Falling back to inefficient execution."
                        ),
                        exc_info=True,
                    )
                    efficient_execution_failed = True
                    efficient_execution_traceback = traceback.format_exc()
                else:
                    raise
        try:
            batch = self._execute_query_inefficient(
                finalized_query, columns_to_features, connection, query_execution_parameters
            )
        except:
            raise
        else:
            if efficient_execution_failed:
                # This helps us collect into about the causes of errors in the 'efficient' code path.
                # i.e. are they code bugs we can fix, or actual errors e.g. in the database itself?
                _logger.info(
                    f"Failed to efficiently execute query, but inefficient code path succeeded. Original error was: {efficient_execution_traceback}"
                )
            if len(batch) > 0 or query_execution_parameters.yield_empty_batches:
                yield batch

    @contextlib.contextmanager
    def _create_temp_table(
        self,
        create_temp_table: CreateTable,
        temp_table: Table,
        drop_temp_table: DropTable,
        connection: sqlalchemy.engine.Connection,
        temp_value: pa.Table,
    ):
        chalk_logger.info(f"Creating temporary table {temp_table.name}.")
        connection.execute(create_temp_table)
        try:
            batch_size = insert_size_limit // temp_value.num_columns
            assert temp_value.num_columns <= insert_size_limit, "temp temp_value has too many columns to insert rowwise"
            for batch_start in range(0, len(temp_value), batch_size):
                batch_end = min(batch_start + batch_size, len(temp_value))
                connection.execute(
                    temp_table.insert(), temp_value.slice(batch_start, batch_end - batch_start).to_pylist()
                )
            yield
        finally:
            # "temp table", to snowflake, means that it belongs to the session. However, we keep using the same Snowflake session
            chalk_logger.info(f"Dropping temporary table {temp_table.name}.")
            connection.execute(drop_temp_table)

    @contextlib.asynccontextmanager
    async def _async_create_temp_table(
        self,
        create_temp_table: CreateTable,
        temp_table: Table,
        drop_temp_table: DropTable,
        connection: sqlalchemy.ext.asyncio.AsyncConnection,
        temp_value: pa.Table,
    ):
        chalk_logger.info(f"Creating temporary table {temp_table.name}.")
        await connection.execute(create_temp_table)
        try:
            batch_size = insert_size_limit // temp_value.num_columns
            assert temp_value.num_columns <= insert_size_limit, "temp temp_value has too many columns to insert rowwise"
            for batch_start in range(0, len(temp_value), batch_size):
                batch_end = min(batch_start + batch_size, len(temp_value))
                await connection.execute(
                    temp_table.insert(), temp_value.slice(batch_start, batch_end - batch_start).to_pylist()
                )
            yield
        finally:
            # "temp table", to snowflake, means that it belongs to the session. However, we keep using the same Snowflake session
            chalk_logger.info(f"Dropping temporary table {temp_table.name}.")
            await connection.execute(drop_temp_table)

    async def async_execute_query(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[sqlalchemy.ext.asyncio.AsyncConnection] = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> AsyncIterable[pa.RecordBatch]:
        if query_execution_parameters is None:
            query_execution_parameters = query_execution_parameters_from_env_vars()
        attempt_efficient_execution = query_execution_parameters.attempt_efficient_execution
        efficient_execution_failed: bool = False
        efficient_execution_traceback: str | None = None
        if attempt_efficient_execution:
            try:
                async for res in self._async_execute_query_efficient(
                    finalized_query, columns_to_features, connection, query_execution_parameters
                ):
                    yield res
                return
            except NotImplementedError:
                try:
                    async for batch in to_async_iterable(
                        self._execute_query_efficient(
                            finalized_query,
                            columns_to_features,
                            None,  # async connection is not compatible with a non-async connection
                            query_execution_parameters,
                        )
                    ):
                        yield batch
                    return
                except NotImplementedError:
                    _logger.debug(
                        (
                            "The SQL statement will be executed into SQLAlchemy objects, as the database backend does "
                            "not support a more efficient execution mechanism."
                        )
                    )
                    pass
                except UnsupportedEfficientExecutionError as e:
                    log_level = e.log_level
                    _logger.log(log_level, str(e))
                except Exception:
                    if query_execution_parameters.fallback_to_inefficient_execution:
                        _logger.error(
                            (
                                f"Failed to efficiently execute query {finalized_query.query.compile(compile_kwargs={'literal_binds': True})} "
                                f"with parameters {finalized_query.params} due to an unexpected error. Falling back to inefficient execution."
                            ),
                            exc_info=True,
                        )
                        efficient_execution_failed = True
                        efficient_execution_traceback = traceback.format_exc()
                    else:
                        raise
            except UnsupportedEfficientExecutionError as e:
                log_level = e.log_level
                _logger.log(log_level, str(e))
            except Exception:
                if query_execution_parameters.fallback_to_inefficient_execution:
                    _logger.error(
                        (
                            f"Failed to efficiently execute query {finalized_query.query.compile(compile_kwargs={'literal_binds': True})} "
                            f"with parameters {finalized_query.params} due to an unexpected error. Falling back to inefficient execution."
                        ),
                        exc_info=True,
                    )
                    efficient_execution_failed = True
                    efficient_execution_traceback = traceback.format_exc()
                else:
                    raise
        try:
            batch = await self._async_execute_query_inefficient(
                finalized_query, columns_to_features, connection, query_execution_parameters
            )
        except:
            raise
        else:
            if efficient_execution_failed:
                # This helps us collect into about the causes of errors in the 'efficient' code path.
                # i.e. are they code bugs we can fix, or actual errors e.g. in the database itself?
                _logger.info(
                    f"Failed to efficiently execute query, but inefficient code path succeeded. Original error was: {efficient_execution_traceback}"
                )
            if len(batch) > 0 or query_execution_parameters.yield_empty_batches:
                yield batch

    async def _async_execute_query_inefficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_feature: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[sqlalchemy.ext.asyncio.AsyncConnection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> pa.RecordBatch:
        if connection is None:
            try:
                eng = self.get_async_engine()
            except NotImplementedError:
                return await asyncio.get_running_loop().run_in_executor(
                    None,
                    self._execute_query_inefficient,
                    finalized_query,
                    columns_to_feature,
                    connection,
                    query_execution_parameters,
                )
            cnx_ctx = eng.connect()
        else:
            cnx_ctx = async_null_context(connection)
        async with cnx_ctx as cnx:
            async with contextlib.AsyncExitStack() as exit_stack:
                for (
                    _,
                    temp_value,
                    create_temp_table,
                    temp_table,
                    drop_temp_table,
                ) in finalized_query.temp_tables.values():
                    exit_stack.enter_context(
                        self._async_create_temp_table(  # pyright: ignore -- type stubs are wrong
                            create_temp_table, temp_table, drop_temp_table, cnx, temp_value
                        )
                    )
            res = await cnx.execute(finalized_query.query, finalized_query.params)
            desc = res.cursor.description  # type: ignore
            result_columns: list[str] = [col[0] for col in desc]
            features = columns_to_feature(result_columns)
            data: Dict[str, List[Any]] = {}
            for v in features.values():
                # Create an entry for the columns, so the pyarrow table will have the correct columns even
                # if there is no data
                data[v.root_fqn] = []
            for row in res.all():
                for k, v in zip(result_columns, row):
                    if k not in features:
                        # We are not interested in this column
                        continue
                    data[features[k].root_fqn].append(self.convert_db_types(v, features[k].converter))
            # Only keep the columns provided by the schema
            schema = pa.schema([pa.field(v.root_fqn, v.converter.pyarrow_dtype) for v in features.values()])
            return _convert_to_record_batch(data, schema=schema)

    def _execute_query_inefficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> pa.RecordBatch:
        with (
            self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx,
            cnx.begin(),
        ):
            with contextlib.ExitStack() as exit_stack:
                for (
                    _,
                    temp_value,
                    create_temp_table,
                    temp_table,
                    drop_temp_table,
                ) in finalized_query.temp_tables.values():
                    exit_stack.enter_context(
                        self._create_temp_table(create_temp_table, temp_table, drop_temp_table, cnx, temp_value)
                    )
                # TODO: postgres may have timestamp casting errors due to timezones here
                res = cnx.execute(finalized_query.query, finalized_query.params)
                desc = res.cursor.description
                result_columns: list[str] = [col[0] for col in desc]
                features = columns_to_features(result_columns)
                data: Dict[str, List[Any]] = {}
                for v in features.values():
                    # Create an entry for the columns, so the pyarrow table will have the correct columns even
                    # if there is no data
                    data[v.root_fqn] = []
                for row in res.all():
                    for k, v in zip(result_columns, row):
                        if k not in features:
                            # We are not interested in this column
                            continue
                        data[features[k].root_fqn].append(self.convert_db_types(v, features[k].converter))
                # Only keep the columns provided by the schema
                schema = pa.schema([pa.field(v.root_fqn, v.converter.pyarrow_dtype) for v in features.values()])
        return _convert_to_record_batch(data, schema=schema)

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        raise NotImplementedError

    def _async_execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[sqlalchemy.ext.asyncio.AsyncConnection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> AsyncIterable[pa.RecordBatch]:
        raise NotImplementedError

    def get_sqlalchemy_dialect(self, paramstyle: Optional[str] = None) -> Dialect:
        return self.local_engine_url().get_dialect()(paramstyle=paramstyle)

    def compile_query(
        self,
        finalized_query: FinalizedChalkQuery,
        paramstyle: Optional[str] = None,
    ) -> Tuple[str, Sequence[Any], Dict[str, Any]]:
        """Compile a query into a string and the bindparams"""
        compiled_query = self._get_compiled_query(finalized_query, paramstyle)
        query_string = compiled_query.string
        return query_string, compiled_query.positiontup or [], compiled_query.params or {}

    def _get_compiled_query(
        self,
        finalized_query: FinalizedChalkQuery,
        paramstyle: Optional[str] = None,
    ) -> SQLCompiler:
        """Compile a query into a string and the bindparams"""
        dialect = self.get_sqlalchemy_dialect(paramstyle=paramstyle)
        query = finalized_query.query.params(finalized_query.params)
        compiled_query = query.compile(dialect=dialect)
        return compiled_query

    def _load_env_engine_args(self, name: str, override: Optional[Mapping[str, str]]) -> Mapping[str, Any]:
        """
        Loads additional engine arguments from env var "{name}_ENGINE_ARGUMENTS"
        """

        extra_args = load_integration_variable(integration_name=name, name="ENGINE_ARGUMENTS", override=override)
        if extra_args is None:
            return {}
        else:
            extra_args = json.loads(extra_args)
            assert isinstance(extra_args, dict), "ENGINE_ARGUMENTS must be a JSON object"
            return extra_args

    def _check_engine_isolation_level(self):
        isolation_level = self.engine_args.get("isolation_level")
        if isolation_level == "AUTOCOMMIT":
            warnings.warn(
                UserWarning(
                    (
                        f"The SQL engine '{self.name}' is being created with the AUTOCOMMIT transaction isolation level, which helps improve "
                        "performance for SELECT statements by avoiding unnecessary transactions. If a different transaction level is needed for an "
                        "individual connection, use the `execution_options` method when retrieving a connection -- e.g. "
                        "`with get_engine().connect().execution_options(isolation_level='REPEATABLE READ') as cnx: ...`. "
                        "For more information, please see "
                        "https://docs.sqlalchemy.org/en/20/core/connections.html#setting-isolation-level-or-dbapi-autocommit-for-a-connection"
                    )
                )
            )

    def get_engine(self) -> Engine:
        from sqlalchemy.engine import create_engine

        if self._engine is None:
            self.register_sqlalchemy_compiler_overrides()
            self._check_engine_isolation_level()
            self._engine = create_engine(url=self.local_engine_url(), **self.engine_args)
        return self._engine

    def get_async_engine(self):
        from sqlalchemy.ext.asyncio import create_async_engine

        if self._async_engine is None:
            self.register_sqlalchemy_compiler_overrides()
            self._check_engine_isolation_level()
            self._async_engine = create_async_engine(url=self.async_local_engine_url(), **self.async_engine_args)
        return self._async_engine

    def raw_session(self) -> Session:
        from sqlalchemy.orm import Session

        warnings.warn(
            DeprecationWarning(
                (
                    "The method `raw_session()` is deprecated. Instead, please construct a session directly "
                    "from the underlying engine -- for example:"
                    "`from sqlalchemy.orm import Session; with Session(sql_source.get_engine()) as session: ...`"
                )
            )
        )
        return Session(self.get_engine())

    def convert_db_types(self, v: Any, converter: FeatureConverter):
        """
        Overload this if a given DB type needs custom type conversion
        """
        return converter.from_rich_to_primitive(v, missing_value_strategy="default_or_allow")

    def to_json(self) -> Dict[str, str]:
        return {"name": self.name or "", "kind": self.kind.value}

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        """Hook to register SQLAlchemy Compiler overrides. These hooks are registered by default in tests and in the engine"""
        return

    def _recreate_integration_variables(self) -> dict[str, str]:
        raise NotImplementedError


def _extract_features(feature_set: Features, prefix: str, targets: List[Label], features: Dict[str, Feature]):
    import sqlalchemy.sql.functions
    import sqlalchemy.sql.schema
    from sqlalchemy import column
    from sqlalchemy.orm import InstrumentedAttribute

    for f in feature_set.features:
        assert f.attribute_name is not None
        try:
            feature_value = getattr(feature_set, f.attribute_name)
        except AttributeError:
            continue
        if f.is_has_many:
            raise ValueError(
                f"Feature '{prefix}.{f.name}' is a nested has-many feature, which is not supported when querying from SQL"
            )
        root_fqn = f"{prefix}.{f.name}"
        if isinstance(feature_value, Features):
            # Nested sub-features
            _extract_features(feature_value, root_fqn, targets, features)
        elif isinstance(feature_value, str):
            # Treat it as a column name
            features[root_fqn] = Feature.from_root_fqn(root_fqn)
            targets.append(column(feature_value).label(root_fqn))
        elif isinstance(feature_value, (sqlalchemy.sql.functions.GenericFunction, InstrumentedAttribute)):
            features[root_fqn] = Feature.from_root_fqn(root_fqn)
            targets.append(feature_value.label(root_fqn))
        elif isinstance(feature_value, sqlalchemy.sql.schema.Column):
            features[root_fqn] = Feature.from_root_fqn(root_fqn)
            targets.append(feature_value.label(root_fqn))
        else:
            raise TypeError(
                (
                    f"Feature '{root_fqn}' has an unsupported value of type '{type(feature_value)}' for SQL queries. "
                    "All values must be a column, a column name string, a nested Features class, or an SQLAlchemy function"
                )
            )


insert_size_limit = 10_000


def _convert_to_record_batch(
    data: Mapping[str, List[Any]],
    schema: pa.Schema,
) -> pa.RecordBatch:
    """
    Converts the provided dict of fqn --> values into a `pa.RecordBatch`.
    This method will detect validation errors and report which FQN failed to be parsed,
    and the target Pyarrow type, which makes debugging much easier.
    """
    data_arrays: dict[str, pa.Array] = dict()
    for k, v in data.items():
        try:
            data_arrays[k] = pa.array(v, type=schema.field(k).type)
        except Exception as e:
            raise ValueError(
                f"Unable to convert values for feature '{k}' into pyarrow type '{schema.field(k).type}': {e}"
            )
    return pa.RecordBatch.from_pydict(data_arrays, schema=schema)
