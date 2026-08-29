from __future__ import annotations

import collections
import contextlib
import csv
import functools
import io
import logging
import os
import time
import weakref
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Deque,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import pyarrow as pa
import pyarrow.csv
from packaging.version import parse

from chalk.features import Feature
from chalk.integrations.named import create_integration_variable, load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import (
    BaseSQLSource,
    SQLSourceKind,
    TableIngestMixIn,
    UnsupportedEfficientExecutionError,
    validate_dtypes_for_efficient_execution,
)
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.pl_helpers import polars_uses_schema_overrides
from chalk.utils.tracing import safe_add_metrics, safe_add_tags, safe_trace

if TYPE_CHECKING:
    import polars as pl
    from polars._typing import PolarsDataType
    from polars.type_aliases import PolarsTemporalType
    from sqlalchemy.engine import URL, Connection, Engine


@functools.cache
def _get_supported_sqlalchemy_types_for_pa_csv_querying() -> tuple[type, ...]:
    """Return SQLAlchemy types supported by PostgreSQL Arrow execution."""
    try:
        import sqlalchemy as sa
    except ImportError:
        return ()

    return (
        sa.BigInteger,
        sa.Boolean,
        sa.Float,
        sa.Integer,
        sa.String,
        sa.Text,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )


_logger = get_logger(__name__)


_PGHOST_NAME = "PGHOST"
_PGPORT_NAME = "PGPORT"
_PGDATABASE_NAME = "PGDATABASE"
_PGUSER_NAME = "PGUSER"
_PGPASSWORD_NAME = "PGPASSWORD"
_ENGINE_ARGUMENTS_NAME = "ENGINE_ARGUMENTS"
_PG_AWS_IAM_AUTH_NAME = "PG_AWS_IAM_AUTH"
_PG_AWS_REGION_NAME = "PG_AWS_REGION"
_PG_AWS_ROLE_ARN_NAME = "PG_AWS_ROLE_ARN"

_TRUTHY_VALUES = ("true", "1", "yes", "t", "y")

#: RDS caps an IAM auth token at 15 minutes. Re-minting a little early keeps a token
#: from expiring between the time we hand it to libpq and the time the handshake
#: completes, and the presign itself is local so re-minting is nearly free.
_RDS_IAM_TOKEN_TTL_SECONDS = 15 * 60
_RDS_IAM_TOKEN_REFRESH_MARGIN_SECONDS = 60

#: Role session name, so IAM-authenticated connections are attributable in CloudTrail.
_RDS_IAM_ROLE_SESSION_NAME = "ChalkRdsIamAuth"


def _parse_bool_integration_variable(value: str) -> bool:
    return value.strip().lower() in _TRUTHY_VALUES


class PostgreSQLSourceImpl(BaseSQLSource, TableIngestMixIn, SQLSourceWithTableIngestProtocol):
    kind = SQLSourceKind.postgres

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[Union[int, str]] = None,
        db: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        name: Optional[str] = None,
        engine_args: Optional[Dict[str, Any]] = None,
        async_engine_args: Optional[Dict[str, Any]] = None,
        integration_variable_override: Optional[Mapping[str, str]] = None,
        permission_tags: list[str] | None = None,
        # Appended rather than inserted next to `password`: the `PostgreSQLSource` factory
        # passes host/port/db/user/password/name positionally, so inserting here would
        # silently shift those arguments.
        aws_iam_auth: Optional[Union[bool, str]] = None,
        aws_region: Optional[str] = None,
        aws_role_arn: Optional[str] = None,
    ):
        try:
            import psycopg  # Used for the async driver
            import psycopg2  # Used for the sync driver
            from sqlalchemy.dialects import registry  # pyright: ignore
        except ImportError:
            raise missing_dependency_exception("chalkpy[postgresql]")
        del psycopg2  # unused
        del psycopg  # unused
        if "postgresql.psycopg" not in registry.impls:
            registry.register(
                "postgresql.psycopg", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect"
            )
        if "postgresql.psycopg_async" not in registry.impls:
            registry.register(
                "postgresql.psycopg_async", "chalk.sql._internal.integrations.psycopg3.psycopg_dialect", "dialect_async"
            )
        self.name = name
        self.host = host or load_integration_variable(
            integration_name=name, name=_PGHOST_NAME, override=integration_variable_override
        )
        self.port = (
            int(port)
            if port is not None
            else load_integration_variable(
                integration_name=name, name=_PGPORT_NAME, parser=int, override=integration_variable_override
            )
        )
        self.db = db or load_integration_variable(
            integration_name=name, name=_PGDATABASE_NAME, override=integration_variable_override
        )
        self.user = user or load_integration_variable(
            integration_name=name, name=_PGUSER_NAME, override=integration_variable_override
        )
        self.password = password or load_integration_variable(
            integration_name=name, name=_PGPASSWORD_NAME, override=integration_variable_override
        )
        # The dashboard stores this as the string "true"/"false" (integration variables are all
        # strings), while Python callers pass a real bool -- accept both.
        self.aws_iam_auth: bool = bool(
            aws_iam_auth
            if isinstance(aws_iam_auth, bool)
            else (
                _parse_bool_integration_variable(aws_iam_auth)
                if isinstance(aws_iam_auth, str)
                else load_integration_variable(
                    integration_name=name,
                    name=_PG_AWS_IAM_AUTH_NAME,
                    parser=_parse_bool_integration_variable,
                    override=integration_variable_override,
                )
            )
        )
        self.aws_region = aws_region or load_integration_variable(
            integration_name=name, name=_PG_AWS_REGION_NAME, override=integration_variable_override
        )
        self.aws_role_arn = aws_role_arn or load_integration_variable(
            integration_name=name, name=_PG_AWS_ROLE_ARN_NAME, override=integration_variable_override
        )
        #: Cached (client, expiry_epoch_seconds) for RDS IAM token minting. The boto3 client is what
        #: is expensive to build; the token itself is a local presign, so it is minted per connection.
        self._rds_iam_client_cache: Optional[Tuple[Any, float]] = None
        self._rds_iam_listener_engines: "weakref.WeakSet[Any]" = weakref.WeakSet()
        self.ingested_tables: Dict[str, Any] = {}
        if engine_args is None:
            engine_args = {}
        if async_engine_args is None:
            async_engine_args = {}

        if name:
            engine_args_from_ui = self._load_env_engine_args(name, override=integration_variable_override)
            for k, v in engine_args_from_ui.items():
                engine_args.setdefault(k, v)
                async_engine_args.setdefault(k, v)

        chalk_default_engine_args = {
            "pool_size": 20,
            "max_overflow": 60,
            "pool_recycle": 90,
            "connect_args": {
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        }
        for k, v in chalk_default_engine_args.items():
            engine_args.setdefault(k, v)
            async_engine_args.setdefault(k, v)

        # RDS refuses IAM authentication over cleartext connections, so an IAM source must
        # negotiate TLS. Default it here rather than making every config remember the connect
        # arg; an explicit `sslmode` in `connect_args` still wins. Runs after the chalk
        # defaults merge above so a source without user `connect_args` keeps the keepalive
        # defaults alongside `sslmode`.
        if self.aws_iam_auth:
            for args in (engine_args, async_engine_args):
                connect_args = args.setdefault("connect_args", {})
                if isinstance(connect_args, dict):
                    connect_args.setdefault("sslmode", "require")

        # We set the default isolation level to autocommit since the SQL sources are read-only, and thus
        # transactions are not needed
        # Setting the isolation level on the engine, instead of the connection, avoids
        # a DBAPI statement to reset the transactional level back to the default before returning the
        # connection to the pool
        engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        async_engine_args.setdefault("isolation_level", os.environ.get("CHALK_SQL_ISOLATION_LEVEL", "AUTOCOMMIT"))
        BaseSQLSource.__init__(
            self,
            name=name,
            engine_args=engine_args,
            async_engine_args=async_engine_args,
            permission_tags=permission_tags,
        )

    def get_sqlglot_dialect(self) -> str | None:
        return "postgres"

    def _get_rds_iam_client(self) -> Any:
        """A boto3 RDS client for minting IAM auth tokens.

        The client is cached because building one (and assuming a role, when configured) is the
        expensive part; minting a token off it is a local signing operation. When a role is assumed
        the cache is bounded by the STS credentials' own expiry, since those creds stop working
        roughly an hour in and a stale client would then fail every new connection.
        """
        cached = self._rds_iam_client_cache
        if cached is not None and cached[1] > time.time():
            return cached[0]

        try:
            import boto3
        except ImportError as e:
            # Deliberately not `chalkpy[postgresql]`: boto3 is not part of that extra, so naming it
            # would send the user to an install that does not fix the problem.
            raise missing_dependency_exception("boto3", e)

        if self.aws_role_arn:
            sts = boto3.client("sts", region_name=self.aws_region)
            assumed = sts.assume_role(RoleArn=self.aws_role_arn, RoleSessionName=_RDS_IAM_ROLE_SESSION_NAME)
            credentials = assumed["Credentials"]
            session = boto3.Session(
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
                region_name=self.aws_region,
            )
            # Re-assume slightly before the credentials lapse rather than exactly at expiry.
            expiry = credentials["Expiration"].timestamp() - _RDS_IAM_TOKEN_REFRESH_MARGIN_SECONDS
        else:
            session = boto3.Session(region_name=self.aws_region)
            expiry = float("inf")

        client = session.client("rds", region_name=self.aws_region)
        self._rds_iam_client_cache = (client, expiry)
        return client

    def generate_rds_iam_token(self) -> str:
        """Mints an RDS IAM auth token for this source's endpoint and user.

        Valid for 15 minutes, but RDS only checks it during the connection handshake, so this is
        called once per connection attempt rather than cached.
        """
        if self.host is None or self.user is None:
            raise ValueError("PostgreSQL RDS IAM authentication requires both a host and a user")
        return self._get_rds_iam_client().generate_db_auth_token(
            DBHostname=self.host,
            # The port is covered by the token's signature, so it must match the port dialed.
            # libpq's default when unset is 5432, so sign for that.
            Port=self.port if self.port is not None else 5432,
            DBUsername=self.user,
            Region=self.aws_region,
        )

    def _inject_rds_iam_token(self, _dialect: Any, _conn_rec: Any, _cargs: Any, cparams: Dict[str, Any]) -> None:
        """SQLAlchemy ``do_connect`` hook that swaps in a freshly minted token as the password.

        Both psycopg2 and psycopg take the password through ``cparams``. This has to happen per
        connection rather than being baked into the engine URL: a token is only valid for 15
        minutes, so a URL built once would stop authenticating as soon as the pool replaced a
        connection.
        """
        cparams["password"] = self.generate_rds_iam_token()

    def _register_rds_iam_listener(self, engine: Any) -> Any:
        """Attaches the token hook to ``engine`` exactly once."""
        if not self.aws_iam_auth or engine in self._rds_iam_listener_engines:
            return engine
        from sqlalchemy import event

        event.listen(engine, "do_connect", self._inject_rds_iam_token)
        self._rds_iam_listener_engines.add(engine)
        return engine

    def get_engine(self) -> Engine:
        # Registered here rather than in __init__ so enabling IAM auth does not force an engine to
        # be built at import time.
        return self._register_rds_iam_listener(super().get_engine())

    def get_async_engine(self) -> Any:
        engine = super().get_async_engine()
        # Async engines wrap a sync Engine, and `do_connect` fires on that inner engine.
        self._register_rds_iam_listener(engine.sync_engine)
        return engine

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def async_local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        return URL.create(
            drivername="postgresql+psycopg_async",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        )

    def _get_parsed_table_via_polars(
        self,
        finalized_query: FinalizedChalkQuery,
        connection: Optional[Connection],
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        query_execution_parameters: QueryExecutionParameters,
    ) -> pyarrow.Table:
        with safe_trace("_get_parsed_table_via_polars"):
            import polars as pl

            buffer = self._get_result_csv_buffer(
                finalized_query,
                connection=connection,
                escape_char='"',
                query_execution_parameters=query_execution_parameters,
            )
            first_line = buffer.readline()
            column_names = list(
                csv.reader(
                    [first_line.decode("utf8")],
                    doublequote=True,
                    quoting=csv.QUOTE_MINIMAL,
                )
            )[0]
            buffer.seek(0)
            features = columns_to_features(column_names)

            parse_dtypes: Dict[str, PolarsDataType] = {}
            boolean_columns: List[str] = []
            date_columns: List[str] = []
            datetime_col_to_dtype: Dict[str, pl.Datetime] = {}
            for col_name, feature in features.items():
                dtype = feature.converter.polars_dtype
                if dtype == pl.Boolean:  # pyright: ignore[reportUnnecessaryComparison]
                    # Parsing "t" and "f" as booleans fails.
                    # We will parse the column as a string, and then
                    # convert it to a boolean later.
                    parse_dtypes[col_name] = pl.Utf8
                    boolean_columns.append(col_name)
                elif dtype == pl.List:  # pyright: ignore[reportUnnecessaryComparison]
                    # We will parse the list as a string, and then
                    # convert it to a list later. Polars does not
                    # support parsing lists directly from CSV.
                    parse_dtypes[col_name] = pl.Utf8
                elif dtype == pl.Datetime:  # pyright: ignore[reportUnnecessaryComparison]
                    # Parse as str, convert to datetime later.
                    # It's important to parse datetimes as strings,
                    # because `polars.read_csv()` just turns
                    # unparsable datetimes into nulls, a huge no-no.
                    parse_dtypes[col_name] = pl.Utf8
                    # Make linter happy
                    dtype = cast(pl.Datetime, dtype)
                    datetime_col_to_dtype[col_name] = dtype
                elif dtype == pl.Date:  # pyright: ignore[reportUnnecessaryComparison]
                    # Parse as str, convert to date later.
                    # It's important to parse dates as strings,
                    # because `polars.read_csv()` just turns
                    # unparsable dates into nulls, a huge no-no.
                    parse_dtypes[col_name] = pl.Utf8
                    date_columns.append(col_name)
                else:
                    parse_dtypes[col_name] = dtype

            """
            CSV -> Polars -> Pyarrow table
            """
            # Previously we were using `pyarrow.csv.read_csv` but performance
            # degraded over time up till the next reboot.
            #
            # pl.read_csv(use_pyarrow=True) has the same performance degradation,
            # UNLESS a `dtypes` arg is provided.

            # 'dtypes' deprecated for 'schema_overrides' in polars 0.20.31+
            if polars_uses_schema_overrides:
                pl_table = pl.read_csv(buffer, schema_overrides=parse_dtypes)  # pyright: ignore[reportCallIssue]
            else:
                pl_table = pl.read_csv(buffer, dtypes=parse_dtypes)  # pyright: ignore[reportCallIssue]
            if boolean_columns:
                # DO NOT use map_dict. Causes a segfault when multiple uvicorn workers are handling
                # requests in parallel.
                boolean_when_mappings = [
                    pl.when(pl.col(bool_col).is_null())
                    .then(None)
                    .otherwise(pl.col(bool_col) == "t")
                    .cast(pl.Boolean)
                    .alias(bool_col)
                    for bool_col in boolean_columns
                ]
                pl_table = pl_table.with_columns(*boolean_when_mappings)
            if date_columns:
                for date_col in date_columns:
                    pl_table = _get_df_with_parsed_dt_column(
                        pl_table=pl_table,
                        col_name=date_col,
                        parser_formats=["%Y-%m-%d", "%D", "%m/%d/%Y"],
                        target_dtype=pl.Date,
                    )
            if datetime_col_to_dtype:
                from polars.type_aliases import TimeUnit

                for dt_col, dt_type in datetime_col_to_dtype.items():
                    unit_to_precision: Dict[TimeUnit, str] = {
                        "ms": "%.3f",
                        "us": "%.6f",
                        "ns": "%.9f",
                    }
                    precision = (
                        unit_to_precision[dt_type.time_unit]
                        if dt_type.time_unit and dt_type.time_unit in unit_to_precision
                        else "%.6f"
                    )
                    dt_format = f"%Y-%m-%d %H:%M:%S{precision}"
                    dt_format_with_tz = f"{dt_format}%#z"
                    datetime_parser_formats = [dt_format, dt_format_with_tz, "%Y-%m-%d"]
                    pl_table = _get_df_with_parsed_dt_column(
                        pl_table=pl_table,
                        col_name=dt_col,
                        parser_formats=datetime_parser_formats,
                        target_dtype=dt_type,
                    )

            parsed_table = pl_table.to_arrow()

            safe_add_metrics(
                {
                    "postgresl_polars_row_count": len(parsed_table),
                    "postgresl_polars_bytes": parsed_table.nbytes,
                }
            )
            return parsed_table

    def _get_result_csv_buffer(
        self,
        finalized_query: FinalizedChalkQuery,
        connection: Optional[Connection],
        escape_char: str,
        query_execution_parameters: QueryExecutionParameters,
    ) -> io.BytesIO:
        with safe_trace("_get_result_csv_buffer"):
            import psycopg2.sql

            stmt, positional_params, named_params = self.compile_query(finalized_query, paramstyle="named")
            assert len(positional_params) == 0, "should not have any positional params"

            # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects
            # Forcing quote so the unquoted empty string will represent null values
            stmt = _reformat_compiled_query_string_for_csv_output(
                stmt,
                escape_char=escape_char,
                named_params=named_params,
            )
            if (
                env_var_bool("CHALK_SKIP_PG_DATETIME_ZONE_CAST")
                or query_execution_parameters.postgres.skip_datetime_timezone_cast
            ):
                with safe_trace("skip_datetime_timezone_cast"):
                    formatted_stmt = psycopg2.sql.SQL(stmt).format(
                        **{
                            k: psycopg2.sql.Literal(str(v)) if isinstance(v, datetime) else psycopg2.sql.Literal(v)
                            for (k, v) in named_params.items()
                        }
                    )
            else:
                formatted_stmt = psycopg2.sql.SQL(stmt).format(
                    **{k: psycopg2.sql.Literal(v) for (k, v) in named_params.items()}
                )
            with self.get_engine().connect() if connection is None else contextlib.nullcontext(connection) as cnx:
                dbapi = cnx.connection
                with dbapi.cursor() as cursor:
                    buffer = io.BytesIO()
                    with safe_trace("copy_expert"):
                        safe_add_tags({"query": formatted_stmt.as_string(cursor)[0:2000]})
                        cursor.copy_expert(formatted_stmt, buffer)
                        written_bytes = buffer.getbuffer().nbytes
                        safe_add_metrics({"postgresl_bytes": written_bytes})

            buffer.seek(0)

            return buffer

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        with safe_trace("postgres.execute_query_efficient"):
            from sqlalchemy.sql import Select

            if finalized_query.finalizer in (Finalizer.FIRST, Finalizer.ONE, Finalizer.ONE_OR_NONE):
                raise UnsupportedEfficientExecutionError(
                    (
                        f"Falling back to SQLAlchemy execution for finalizer '{finalized_query.finalizer.value}', "
                        "as it is faster for small results."
                    ),
                    log_level=logging.DEBUG,
                )

            if isinstance(finalized_query.query, Select):
                validate_dtypes_for_efficient_execution(
                    finalized_query.query, _get_supported_sqlalchemy_types_for_pa_csv_querying()
                )

            assert len(finalized_query.temp_tables) == 0, "Should not create temp tables with postgres source"

            if query_execution_parameters.postgres.polars_read_csv:
                _logger.debug("postgres: doing force polars CSV reader")
                parsed_table = self._get_parsed_table_via_polars(
                    finalized_query, connection, columns_to_features, query_execution_parameters
                )
            else:
                buffer = self._get_result_csv_buffer(
                    finalized_query,
                    connection=connection,
                    escape_char="\\",
                    query_execution_parameters=query_execution_parameters,
                )
                buffer.seek(0)
                parsed_table = pyarrow.csv.read_csv(
                    buffer,
                    parse_options=pyarrow.csv.ParseOptions(
                        newlines_in_values=True,
                        escape_char="\\",
                        double_quote=False,
                    ),
                    convert_options=pyarrow.csv.ConvertOptions(
                        true_values=["t"],
                        false_values=["f"],
                        strings_can_be_null=True,
                        quoted_strings_can_be_null=False,
                    ),
                )

            features = columns_to_features(parsed_table.column_names)

            restricted_schema = pa.schema([pa.field(k, v.converter.pyarrow_dtype) for (k, v) in features.items()])
            parsed_table = parsed_table.select(list(features.keys()))
            parsed_table = parsed_table.cast(restricted_schema)
            parsed_table = parsed_table.rename_columns([x.root_fqn for x in features.values()])
            if len(parsed_table) > 0:
                yield parsed_table.combine_chunks().to_batches()[0]
            if len(parsed_table) == 0 and query_execution_parameters.yield_empty_batches:
                yield pa.RecordBatch.from_pydict({k: [] for k in parsed_table.schema.names}, parsed_table.schema)
            return

    def execute_query_efficient_raw(
        self,
        finalized_query: FinalizedChalkQuery,
        expected_output_schema: pa.Schema,
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ) -> Iterable[pa.RecordBatch]:
        """Execute query efficiently for PostgreSQL and return raw PyArrow RecordBatches."""
        import pyarrow.compute as pc
        from sqlalchemy.sql import Select

        if finalized_query.finalizer in (Finalizer.FIRST, Finalizer.ONE, Finalizer.ONE_OR_NONE):
            raise UnsupportedEfficientExecutionError(
                (
                    f"Falling back to SQLAlchemy execution for finalizer '{finalized_query.finalizer.value}', "
                    "as it is faster for small results."
                ),
                log_level=logging.DEBUG,
            )

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(
                finalized_query.query, _get_supported_sqlalchemy_types_for_pa_csv_querying()
            )

        assert len(finalized_query.temp_tables) == 0, "Should not create temp tables with postgres source"

        # Use the existing CSV export mechanism
        if query_execution_parameters.postgres.polars_read_csv:
            buffer = self._get_result_csv_buffer(
                finalized_query,
                connection=connection,
                escape_char='"',
                query_execution_parameters=query_execution_parameters,
            )
            first_line = buffer.readline()
            _ = list(
                csv.reader(
                    [first_line.decode("utf8")],
                    doublequote=True,
                    quoting=csv.QUOTE_MINIMAL,
                )
            )[0]
            buffer.seek(0)

            import polars as pl

            parse_dtypes: Dict[str, PolarsDataType] = {}
            for field in expected_output_schema:
                # Convert PyArrow types to Polars types for parsing
                if pa.types.is_boolean(field.type):
                    parse_dtypes[field.name] = pl.Utf8  # Parse as string, convert later
                elif pa.types.is_list(field.type):
                    parse_dtypes[field.name] = pl.Utf8  # Parse as string
                elif pa.types.is_date32(field.type) or pa.types.is_date64(field.type):
                    parse_dtypes[field.name] = pl.Utf8  # Parse as string, convert later
                elif pa.types.is_timestamp(field.type):
                    parse_dtypes[field.name] = pl.Utf8  # Parse as string, convert later
                elif pa.types.is_integer(field.type):
                    parse_dtypes[field.name] = pl.Int64
                elif pa.types.is_floating(field.type):
                    parse_dtypes[field.name] = pl.Float64
                else:
                    parse_dtypes[field.name] = pl.Utf8

            # 'dtypes' deprecated for 'schema_overrides' in polars 0.20.31+
            if polars_uses_schema_overrides:
                pl_table = pl.read_csv(buffer, schema_overrides=parse_dtypes)  # pyright: ignore[reportCallIssue]
            else:
                pl_table = pl.read_csv(buffer, dtypes=parse_dtypes)  # pyright: ignore[reportCallIssue]

            # Convert to arrow and map to expected schema
            arrow_table = pl_table.to_arrow()
        else:
            buffer = self._get_result_csv_buffer(
                finalized_query,
                connection=connection,
                escape_char="\\",
                query_execution_parameters=query_execution_parameters,
            )
            buffer.seek(0)
            arrow_table = pyarrow.csv.read_csv(
                buffer,
                parse_options=pyarrow.csv.ParseOptions(
                    newlines_in_values=True,
                    escape_char="\\",
                    double_quote=False,
                ),
                convert_options=pyarrow.csv.ConvertOptions(
                    true_values=["t"],
                    false_values=["f"],
                    strings_can_be_null=True,
                    quoted_strings_can_be_null=False,
                ),
            )

        # Map columns to expected schema
        arrays: list[pa.Array] = []
        for field in expected_output_schema:
            if field.name in arrow_table.column_names:
                col = arrow_table.column(field.name)
                if isinstance(col, pa.ChunkedArray):
                    col = col.combine_chunks()
                # Cast to expected type if needed
                if col.type != field.type:
                    col = pc.cast(col, field.type)
                arrays.append(col)
            else:
                # Column not found, create null array
                arrays.append(pa.nulls(len(arrow_table), field.type))

        batch = pa.RecordBatch.from_arrays(arrays, schema=expected_output_schema)
        if len(batch) > 0 or query_execution_parameters.yield_empty_batches:
            yield batch

    def _recreate_integration_variables(self) -> dict[str, str]:
        return {
            k: v
            for k, v in [
                create_integration_variable(_PGHOST_NAME, self.name, self.host),
                create_integration_variable(_PGPORT_NAME, self.name, self.port),
                create_integration_variable(_PGDATABASE_NAME, self.name, self.db),
                create_integration_variable(_PGUSER_NAME, self.name, self.user),
                create_integration_variable(_PGPASSWORD_NAME, self.name, self.password),
                # Serialized lower-case: `create_integration_variable` would otherwise emit
                # "True"/"False", which the truthy parsers used on the way back in are
                # case-sensitive about.
                create_integration_variable(
                    _PG_AWS_IAM_AUTH_NAME, self.name, str(self.aws_iam_auth).lower() if self.aws_iam_auth else None
                ),
                create_integration_variable(_PG_AWS_REGION_NAME, self.name, self.aws_region),
                create_integration_variable(_PG_AWS_ROLE_ARN_NAME, self.name, self.aws_role_arn),
            ]
            if v is not None
        }


def _reformat_compiled_query_string_for_csv_output(
    stmt: str,
    *,
    escape_char: str,
    named_params: Mapping[str, Any],
) -> str:
    """
    - Replaces named parameters like `:foo` with the python3-style `{foo}` which is what `psycopg2.sql.SQL.format`
    expects to see in its inputs.

    - Wraps the provided `stmt` in a `COPY _ to STDOUT` declaration to format it as a CSV.
    """
    # Forcing quote so the unquoted empty string will represent null values

    # Convert the param style to python3-style {}, which is what psycopg2.sql.SQL.format expects

    original_stmt = stmt
    import sqlglot
    import sqlglot.expressions

    try:
        stmt_expression = sqlglot.parse_one(stmt, read="postgres")
        for placeholder in list(stmt_expression.find_all(sqlglot.expressions.Placeholder)):
            if isinstance(placeholder.this, str) and placeholder.this in named_params:
                # If this is a known placeholder like `:foo`, replace it verbatim with `{foo}`.
                # The use of the 'var' node here is incidental - it accepts any string as argument,
                # and sqlglot will reproduce that string verbatim as output.
                placeholder.replace(sqlglot.expressions.var("{" + placeholder.this + "}"))
        stmt = stmt_expression.sql(dialect="postgres")

        stmt = f"COPY ({stmt}) TO STDOUT (FORMAT CSV, HEADER true, FORCE_QUOTE *, ESCAPE '{escape_char}')"
    except Exception as e:
        raise ValueError(
            f"Failed to parse and convert postgres output {repr(original_stmt)} with named parameters {repr(list(named_params.keys()))} into valid psycopg2-compatible CSV OUTPUT statement: {e}"
        ) from e

    return stmt


def _get_df_with_parsed_dt_column(
    pl_table: pl.DataFrame, col_name: str, parser_formats: Sequence[str], target_dtype: PolarsTemporalType
):
    import polars as pl

    use_new_parsing = parse(pl.__version__) >= parse("0.18.4")
    num_nulls_original = pl_table[col_name].null_count()
    original_dt_clone: pl.Series = pl_table[col_name].clone()

    def parsing_complete(table: pl.DataFrame) -> bool:
        if table[col_name].dtype != target_dtype:
            # Never parsed
            return False
        return table[col_name].null_count() == num_nulls_original

    parser_formats_deque: Deque[Union[str, None]] = collections.deque(parser_formats)
    # When `format=None`, polars will raise a `ComputeError` if it
    # fails parsing, even if `strict=False`. Then, we will fallback
    # to the arrow CSV reader, which will raise a useful error.
    # TODO: Don't depend on pyarrow to raise pyarrow.ArrowInvalid,
    #       instead raise a custom parser error and handle that in
    #       the engine.
    parser_formats_deque.append(None)

    # strptime always outputs a datetime in UTC, so we do the
    # parsing in UTC first, and convert to target timezone later.
    parsing_dtype = target_dtype
    original_target_tz = None
    if target_dtype == pl.Datetime:
        target_dtype = cast(pl.Datetime, target_dtype)
        original_target_tz = target_dtype.time_zone
        if use_new_parsing:
            assert target_dtype.time_unit is not None, f"polars dtype {target_dtype} incorrectly set with no time unit."
            parsing_dtype = pl.Datetime(time_zone="UTC", time_unit=target_dtype.time_unit)
        else:
            target_dtype = pl.Datetime
            parsing_dtype = target_dtype

    # You might think this strptime call can be included in the for
    # loop below, but this is intentionally left out of the for loop
    # because we want to avoid calling `pl.coalesce` for the first pass.
    # Otherwise, the result of the coalescence will be a column of
    # `pl.Utf8` instead of the target date or datetime type.
    pl_table = pl_table.with_columns(
        original_dt_clone.str.strptime(
            cast("PolarsTemporalType", parsing_dtype),
            parser_formats_deque.popleft(),
            strict=False,
        ).alias(col_name)
    )

    # Incrementally coalesce so that we don't have to do all
    # passes of parsing - only as many as needed.
    while len(parser_formats_deque) > 0 and not parsing_complete(pl_table):
        fmt = parser_formats_deque.popleft()
        formatted_col = original_dt_clone.str.strptime(
            cast("PolarsTemporalType", parsing_dtype),
            fmt,
            strict=False,
        ).alias(col_name)
        coalesced_col = pl.coalesce(
            pl.col(col_name),
            formatted_col,
        )
        pl_table = pl_table.with_columns(coalesced_col)

    if target_dtype == pl.Datetime and use_new_parsing:
        # Convert to target timezone
        if original_target_tz is None:
            pl_table = pl_table.with_columns(pl.col(col_name).dt.replace_time_zone(None))
        else:
            pl_table = pl_table.with_columns(pl.col(col_name).dt.convert_time_zone(original_target_tz))

    # We would have raised if there was an error parsing with `format=None`.
    assert parsing_complete(pl_table)

    return pl_table
