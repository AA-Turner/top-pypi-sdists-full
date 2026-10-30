"""Run Athena queries directly through the AWS API.

V4 managed-result executions use GetQueryResultStream and Apache Arrow IPC. V1-V3 executions and
customer-managed results use paginated GetQueryResults. Query-level EngineVersion overrides are
resolved from the completed query before selecting the reader, so a V3 workgroup can run a V4
managed query without being misclassified.

GetQueryResultStream and the query-level EngineVersion input are supplied by the internal Athena
model bundled at ``boto3_models/athena/2017-05-18/service-2.json``.
"""

import logging
import math
import re
import time
from collections import deque
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple

import pyarrow as pa
import pyarrow.ipc as ipc
from botocore.credentials import RefreshableCredentials
from botocore.exceptions import IncompleteReadError, ReadTimeoutError, ResponseStreamingError
from botocore.session import get_session
from pandas import DataFrame, Series

from sagemaker_studio.sql_engine.database_transformer import SqlStatement
from sagemaker_studio.sql_engine.sql_executor import SingleStatementResult

logger = logging.getLogger(__name__)

# First Athena engine version that uses the DuckDB/Arrow result path.
MIN_ENGINE_VERSION = 4
# Accepted names during the V4 -> Athena DuckDB transition. Service responses use the
# customer-facing names; internal names are accepted defensively during the regional rollout.
_V4_ENGINE_VERSION_NAMES = frozenset(
    {
        "Athena engine version 4",
        "Athena DuckDB",
        "KeplerSparkSQL-2.x",
        "DuckDB-2.x",
    }
)
_ENGINE_VERSION_NUMBER = re.compile(r"(\d+)\s*$")
_TERMINAL_STATES = ("SUCCEEDED", "FAILED", "CANCELLED")
# Poll quickly at first so short queries return fast, then settle at PyAthena's 1s interval.
_POLL_INITIAL_SECONDS = 0.2
_POLL_MAX_SECONDS = 1.0
# GetQueryResultStream reads: chunk size, and how many times a cut-off read is resumed with a
# Range request before giving up.
_STREAM_CHUNK_BYTES = 1 << 20
_MAX_STREAM_RESUMES = 3
# A read that ends early: fewer bytes than Content-Length, or the connection dropped mid-body.
_INTERRUPTED_READ_ERRORS = (IncompleteReadError, ReadTimeoutError, ResponseStreamingError)
# Statements whose result is a row count rather than rows (as PyAthena reports them).
_ROWCOUNT_SUBSTATEMENT_TYPES = frozenset(
    {
        "INSERT",
        "UPDATE",
        "DELETE",
        "MERGE",
        "CREATE_TABLE_AS_SELECT",
        "UNLOAD",
        "OPTIMIZE",
        "VACUUM",
    }
)

# (connection id or name, workgroup) -> what we read about the workgroup from GetWorkGroup.
_workgroup_infos: Dict[Tuple[str, str], "WorkgroupInfo"] = {}


class WorkgroupInfo(NamedTuple):
    """What a single GetWorkGroup call tells us about how a workgroup runs queries.

    ``managed_storage`` is True when the workgroup stores results in Athena managed storage (read
    with GetQueryResultStream), and False for a customer output location or when the signal is
    absent -- so the Arrow path is only taken on an explicit managed-storage signal.
    """

    engine_version: Optional[int]
    managed_storage: bool


class AthenaQueryError(RuntimeError):
    """An Athena query that ended FAILED or CANCELLED."""

    def __init__(self, query_execution_id: str, state: str, reason: str):
        super().__init__(f"Athena query {query_execution_id} {state}: {reason}")
        self.query_execution_id = query_execution_id
        self.state = state
        self.reason = reason


def _engine_version_number(engine_version: Optional[str]) -> Optional[int]:
    if not isinstance(engine_version, str):
        return None
    if engine_version in _V4_ENGINE_VERSION_NAMES:
        return MIN_ENGINE_VERSION
    match = _ENGINE_VERSION_NUMBER.search(engine_version)
    return int(match.group(1)) if match else None


def _effective_engine_version_number(engine_version: Optional[dict]) -> Optional[int]:
    return _engine_version_number((engine_version or {}).get("EffectiveEngineVersion"))


def _sql_literal(value: Any) -> str:
    """Render a Python value as an Athena SQL literal without changing surrounding SQL."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc)
        value = value.replace(tzinfo=None)
        precision = 3 if value.microsecond % 1000 == 0 else 6
        rendered = value.isoformat(sep=" ", timespec="seconds")
        if precision:
            rendered += "." + f"{value.microsecond:06d}"[:precision]
        return f"TIMESTAMP '{rendered}'"
    if isinstance(value, date):
        return f"DATE '{value.year:04d}-{value.month:02d}-{value.day:02d}'"
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError("Athena decimal parameters must be finite")
        return f"DECIMAL '{value:f}'"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Athena float parameters must be finite")
        return repr(value)
    if isinstance(value, (bytes, bytearray, memoryview)):
        return f"X'{bytes(value).hex()}'"
    if isinstance(value, (list, tuple, set)):
        return "(" + ", ".join(_sql_literal(item) for item in value) + ")"
    raise TypeError(f"Unsupported Athena query parameter type: {type(value).__name__}")


def _bind_parameters(statement: str, parameters: Any) -> str:
    """Substitute parameters at sqlglot token offsets, preserving comments and formatting."""
    if parameters is None:
        return statement

    from sqlglot.tokens import Tokenizer, TokenType

    tokens = Tokenizer(dialect="athena").tokenize(statement)
    replacements = []
    if isinstance(parameters, dict):
        for token in tokens:
            if token.token_type is not TokenType.COLON:
                continue
            match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", statement[token.end + 1 :])
            if match is None:
                continue
            name = match.group(0)
            if name not in parameters:
                raise ValueError(f"Missing Athena query parameter: {name}")
            replacements.append(
                (token.start, token.end + 1 + len(name), _sql_literal(parameters[name]))
            )
    elif isinstance(parameters, list):
        placeholders = [token for token in tokens if token.token_type is TokenType.PLACEHOLDER]
        if len(placeholders) != len(parameters):
            raise ValueError(
                f"Athena query has {len(placeholders)} positional placeholders but "
                f"{len(parameters)} values were supplied"
            )
        replacements.extend(
            (token.start, token.end + 1, _sql_literal(value))
            for token, value in zip(placeholders, parameters)
        )
    else:
        raise ValueError(
            "Athena query parameters must be supplied as a mapping or positional list."
        )

    for start, end, literal in reversed(replacements):
        statement = statement[:start] + literal + statement[end:]
    return statement


def split_query(query: str) -> List[SqlStatement]:
    """Split Athena SQL on real semicolon tokens while preserving each statement's text."""
    import sqlglot
    from sqlglot.tokens import Tokenizer, TokenType

    tokenizer = Tokenizer(dialect="athena")
    tokens = tokenizer.tokenize(query)
    boundaries = [token for token in tokens if token.token_type is TokenType.SEMICOLON]
    statements: List[SqlStatement] = []
    start = 0
    for boundary in [*boundaries, None]:
        end = boundary.start if boundary is not None else len(query)
        statement = query[start:end].strip()
        start = boundary.end + 1 if boundary is not None else len(query)
        if not statement or not tokenizer.tokenize(statement):
            continue
        try:
            parsed = sqlglot.parse_one(statement, read="athena")
            statement_type = parsed.key.upper() if parsed.key else "UNKNOWN"
        except Exception:
            statement_type = "UNKNOWN"
        statements.append(SqlStatement(statement=statement, statement_type=statement_type))
    return statements


def _statement_parameter_sets(statements: List[SqlStatement], parameters: Any) -> List[Any]:
    """Return the parameters belonging to each statement, validating before execution."""
    from sqlglot.tokens import Tokenizer, TokenType

    tokenizer = Tokenizer(dialect="athena")
    if isinstance(parameters, dict):
        names = []
        for item in statements:
            for token in tokenizer.tokenize(item.statement):
                if token.token_type is not TokenType.COLON:
                    continue
                match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", item.statement[token.end + 1 :])
                if match is not None:
                    names.append(match.group(0))
        missing = [name for name in dict.fromkeys(names) if name not in parameters]
        if missing:
            raise ValueError(f"Missing Athena query parameter: {missing[0]}")
        return [parameters] * len(statements)

    if not isinstance(parameters, list):
        return [parameters] * len(statements)

    counts = [
        sum(
            token.token_type is TokenType.PLACEHOLDER
            for token in tokenizer.tokenize(item.statement)
        )
        for item in statements
    ]
    expected = sum(counts)
    if expected != len(parameters):
        raise ValueError(
            f"Athena query has {expected} positional placeholders but "
            f"{len(parameters)} values were supplied"
        )
    result = []
    offset = 0
    for count in counts:
        result.append(parameters[offset : offset + count])
        offset += count
    return result


def execute_query_statements(
    executor: "AthenaV4Executor",
    query: str,
    error_strategy: Any,
    execute_method: Optional[Any] = None,
):
    """Execute split statements with parameters scoped to each statement."""
    from sagemaker_studio.sql_engine.sql_executor import SqlExecutor

    statements = split_query(query)
    parameter_sets = iter(_statement_parameter_sets(statements, executor.execution_parameters))
    execute = execute_method or executor.execute

    def execute_statement(statement: str):
        previous = executor.execution_parameters
        executor.execution_parameters = next(parameter_sets)
        try:
            return execute(statement)
        finally:
            executor.execution_parameters = previous

    return SqlExecutor.execute_statements(statements, execute_statement, error_strategy)


def _refreshable_credentials(credential_provider: Any) -> RefreshableCredentials:
    def refresh() -> Dict[str, Any]:
        credentials = credential_provider()
        required = ("access_key_id", "secret_access_key", "expiration")
        missing = [key for key in required if not credentials.get(key)]
        if missing:
            raise ValueError(f"credential_provider missing required keys: {missing}")
        return {
            "access_key": credentials["access_key_id"],
            "secret_key": credentials["secret_access_key"],
            "token": credentials.get("session_token"),
            "expiry_time": credentials["expiration"],
        }

    return RefreshableCredentials.create_from_metadata(
        metadata=refresh(),
        refresh_using=refresh,
        method="custom-provider",
        advisory_timeout=60,
    )


def _session_with_refreshable_credentials(credential_provider: Any) -> Any:
    session = get_session()
    model_path = str(Path(__file__).resolve().parents[1] / "boto3_models")
    loader = session.get_component("data_loader")
    if model_path not in loader.search_paths:
        loader.search_paths.insert(0, model_path)
    session._credentials = _refreshable_credentials(credential_provider)  # type: ignore[attr-defined]
    return session


def _uses_managed_storage(configuration: dict) -> bool:
    """Whether ``configuration`` (a WorkGroupConfiguration) stores results in Athena managed
    storage rather than a customer output location.

    The signal is ``ManagedQueryResultsConfiguration.Enabled``; a customer output location is
    ``ResultConfiguration.OutputLocation`` instead, and the two are mutually exclusive. Managed
    storage is reported only on an explicit ``Enabled`` truth; an absent or unexpected shape
    selects the native Row/Datum reader.
    """
    managed = configuration.get("ManagedQueryResultsConfiguration") or {}
    return bool(managed.get("Enabled"))


def workgroup_info(client: Any, work_group: str) -> WorkgroupInfo:
    """How ``work_group`` runs queries, from a single GetWorkGroup call: its major engine version
    (None when unknown) and whether it stores results in Athena managed storage."""
    response = client.get_work_group(WorkGroup=work_group)
    configuration = (response.get("WorkGroup") or {}).get("Configuration") or {}
    return WorkgroupInfo(
        engine_version=_effective_engine_version_number(configuration.get("EngineVersion")),
        managed_storage=_uses_managed_storage(configuration),
    )


def workgroup_engine_version(client: Any, work_group: str) -> Optional[int]:
    """The major Athena engine version ``work_group`` runs queries on, or None when unknown."""
    return workgroup_info(client, work_group).engine_version


def clear_cache() -> None:
    """Forget the workgroup engine versions and result-storage modes read so far."""
    _workgroup_infos.clear()


def _is_athena_connection(conn: Any) -> bool:
    """Return whether ``conn`` executes SQL through Athena."""
    if conn is None:
        return False
    engine_type = getattr(conn, "sql_engine_type", None)
    if not isinstance(engine_type, str):
        engine_type = getattr(conn, "type", None)
    return engine_type == "ATHENA"


def _connection_identity(conn: Any) -> Tuple[Optional[str], Optional[str]]:
    data_work_group = getattr(getattr(conn, "data", None), "workgroup_name", None)
    connection_work_group = getattr(conn, "athena_workgroup", None)
    work_group = (
        data_work_group
        if isinstance(data_work_group, str) and data_work_group
        else connection_work_group
    )
    if not isinstance(work_group, str) or not work_group:
        work_group = None
    conn_key = next(
        (
            value
            for value in (getattr(conn, "id", None), getattr(conn, "name", None))
            if isinstance(value, str) and value
        ),
        None,
    )
    return work_group, conn_key


def _cached_workgroup_info(client: Any, conn_key: str, work_group: str) -> WorkgroupInfo:
    key = (conn_key, work_group)
    if key not in _workgroup_infos:
        _workgroup_infos[key] = workgroup_info(client, work_group)
    return _workgroup_infos[key]


def athena_executor(
    conn: Any,
    catalog: Optional[str] = None,
    schema: Optional[str] = None,
    selected_engine_version: Optional[str] = None,
    parameters: Optional[Any] = None,
    credential_provider: Optional[Any] = None,
) -> Optional["AthenaV4Executor"]:
    """Build the SDK-owned executor for any Athena connection.

    V4 executions with managed results use Arrow. Older engines and customer-managed results use
    paginated GetQueryResults. A query-level ``EngineVersion`` override takes precedence over the
    workgroup's engine when selecting the result reader.
    """
    if not _is_athena_connection(conn):
        return None
    work_group, conn_key = _connection_identity(conn)
    if not isinstance(work_group, str) or not work_group or conn_key is None:
        return None

    if credential_provider is not None:
        client = conn._create_client_with_session(
            "athena",
            _session_with_refreshable_credentials(credential_provider),
        )
    else:
        client = conn.create_client("athena")
    try:
        info = _cached_workgroup_info(client, conn_key, work_group)
    except Exception as error:
        logger.warning(
            "Could not read Athena workgroup %s; using the native row reader: %s: %s",
            work_group,
            type(error).__name__,
            error,
        )
        info = WorkgroupInfo(engine_version=None, managed_storage=False)

    override = selected_engine_version
    if override is None:
        data = getattr(conn, "data", None)
        override = getattr(data, "selected_engine_version", None)
        if override is None:
            override = getattr(data, "engine_version", None)
    if isinstance(override, int) and not isinstance(override, bool):
        override = str(override)
    elif override is not None and not isinstance(override, str):
        override = None

    if parameters is not None and not isinstance(parameters, (dict, list)):
        raise ValueError(
            "Athena query parameters must be supplied as a mapping or positional list."
        )

    if catalog is None:
        connection_catalog = getattr(getattr(conn, "data", None), "catalog", None)
        if isinstance(connection_catalog, str) and connection_catalog:
            catalog = connection_catalog

    return AthenaV4Executor(
        client,
        work_group,
        catalog=catalog,
        schema=schema,
        managed_storage=info.managed_storage,
        workgroup_engine_version=info.engine_version,
        selected_engine_version=override,
        execution_parameters=parameters,
    )


def _arrow_values(column: Any) -> List[Any]:
    """Convert an Arrow column to Python values across supported PyArrow versions."""
    try:
        return column.to_pylist(maps_as_pydicts="lossy")
    except TypeError:
        values = column.to_pylist()
        if pa.types.is_map(column.type):
            return [dict(value) if value is not None else None for value in values]
        return values


def dataframe_from_arrow(table: "pa.Table") -> DataFrame:
    """Build the result DataFrame from an Arrow table, one column at a time.

    Same dtypes and values as ``DataFrame(rows, columns=names)`` over positional rows (what the
    PyAthena cursor fetch builds), duplicate column names kept.
    """
    series = {}
    for i in range(table.num_columns):
        series[i] = Series(_arrow_values(table.column(i)), dtype=None)
    frame = DataFrame(series, index=None if series else range(table.num_rows))
    frame.columns = [field.name for field in table.schema]
    return frame


class AthenaV4Executor:
    """Runs Athena statements directly and selects Arrow or Row/Datum per execution."""

    def __init__(
        self,
        client: Any,
        work_group: str,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        managed_storage: bool = True,
        workgroup_engine_version: Optional[int] = MIN_ENGINE_VERSION,
        selected_engine_version: Optional[str] = None,
        execution_parameters: Optional[Any] = None,
    ):
        self.client = client
        self.work_group = work_group
        self.catalog = catalog
        self.schema = schema
        self.managed_storage = managed_storage
        self.workgroup_engine_version = workgroup_engine_version
        self.selected_engine_version = selected_engine_version
        self.execution_parameters = execution_parameters
        self._executions: Dict[str, dict] = {}

    def _prepare_statement(self, statement: str) -> str:
        return _bind_parameters(statement, self.execution_parameters)

    def start(self, statement: str) -> str:
        """Start one query using the workgroup or an explicit query-level engine override."""
        statement = self._prepare_statement(statement)
        request: Dict[str, Any] = {"QueryString": statement, "WorkGroup": self.work_group}
        context = {}
        if self.catalog:
            context["Catalog"] = self.catalog
        if self.schema:
            context["Database"] = self.schema
        if context:
            request["QueryExecutionContext"] = context
        if _engine_version_number(self.selected_engine_version) is not None:
            request["EngineVersion"] = self.selected_engine_version
        return self.client.start_query_execution(**request)["QueryExecutionId"]

    def wait(self, query_execution_id: str) -> dict:
        """Poll GetQueryExecution until the query finishes; returns its ``QueryExecution``.

        Raises ``AthenaQueryError`` when it FAILED or was CANCELLED. An interrupt (Ctrl-C) stops
        the query with StopQueryExecution before re-raising.
        """
        delay = _POLL_INITIAL_SECONDS
        try:
            while True:
                execution = self.client.get_query_execution(QueryExecutionId=query_execution_id)[
                    "QueryExecution"
                ]
                status = execution.get("Status") or {}
                state = status.get("State")
                if state in _TERMINAL_STATES:
                    break
                time.sleep(delay)
                delay = min(delay * 2, _POLL_MAX_SECONDS)
        except KeyboardInterrupt:
            try:
                self.client.stop_query_execution(QueryExecutionId=query_execution_id)
            except Exception:
                logger.debug("Failed to stop Athena query %s", query_execution_id, exc_info=True)
            raise
        if state != "SUCCEEDED":
            raise AthenaQueryError(
                query_execution_id,
                state,
                status.get("StateChangeReason")
                or (status.get("AthenaError") or {}).get("ErrorMessage")
                or "no reason given",
            )
        self._executions[query_execution_id] = execution
        return execution

    def _execution_version(self, execution: Optional[dict]) -> Optional[int]:
        version = _effective_engine_version_number((execution or {}).get("EngineVersion"))
        if version is not None:
            return version
        selected_version = _engine_version_number(self.selected_engine_version)
        if selected_version is not None:
            return selected_version
        return self.workgroup_engine_version

    def _uses_arrow(self, query_execution_id: str, execution: Optional[dict] = None) -> bool:
        if execution is None:
            execution = self._executions.get(query_execution_id)
        version = self._execution_version(execution)
        return self.managed_storage and version is not None and version >= MIN_ENGINE_VERSION

    @staticmethod
    def _skip_row_header(execution: Optional[dict]) -> bool:
        """Whether GetQueryResults prepends its column-label row.

        V1-V3 SELECT executions report ``StatementType=DML``. V4 customer-managed SELECTs
        currently omit both statement fields but still return the same header echo.
        """
        statement_type = (execution or {}).get("StatementType")
        return statement_type == "DML" or statement_type is None

    def read_table(self, query_execution_id: str) -> "pa.Table":
        """The query's result as an Arrow table, from GetQueryResultStream."""
        started = time.monotonic()
        body = self._read_stream(query_execution_id)
        table = ipc.open_stream(body).read_all()
        logger.info(
            "Athena query %s: read %d rows (%d bytes) with GetQueryResultStream in %.2fs",
            query_execution_id,
            table.num_rows,
            len(body),
            time.monotonic() - started,
        )
        return table

    def _read_stream(self, query_execution_id: str) -> bytes:
        """The whole GetQueryResultStream body, resuming a cut-off read.

        A read that ends before the advertised Content-Length is resumed from the bytes received
        so far with ``Range: bytes=<received>-``, up to ``_MAX_STREAM_RESUMES`` times. A 206
        answer is appended; a 200 (the service sent the whole body again) replaces what was read.
        Raises when a resume brings no new bytes, when the body ends up longer than advertised,
        or after the last resume.
        """
        response = self.client.get_query_result_stream(QueryExecutionId=query_execution_id)
        expected = _content_length(response)
        body, error = _read_available(response["Body"])
        resumes = 0
        while error is not None or (expected is not None and len(body) < expected):
            if expected is None:
                raise error  # type: ignore[misc]  # no length to resume against
            if resumes >= _MAX_STREAM_RESUMES:
                raise RuntimeError(
                    f"GetQueryResultStream for {query_execution_id} was cut off at {len(body)} "
                    f"of {expected} bytes after {resumes} resumes"
                ) from error
            resumes += 1
            logger.info(
                "Athena query %s: result stream cut off at %d of %d bytes (%s); resuming",
                query_execution_id,
                len(body),
                expected,
                type(error).__name__ if error is not None else "short read",
            )
            response = self.client.get_query_result_stream(
                QueryExecutionId=query_execution_id, Range=f"bytes={len(body)}-"
            )
            chunk, error = _read_available(response["Body"])
            if _status(response) == 200:
                body = chunk
            elif chunk:
                body += chunk
            elif error is None:
                raise RuntimeError(
                    f"GetQueryResultStream resume for {query_execution_id} at byte {len(body)} "
                    "returned no data"
                )
        if expected is not None and len(body) > expected:
            raise RuntimeError(
                f"GetQueryResultStream for {query_execution_id} returned {len(body)} bytes, "
                f"more than the advertised {expected}"
            )
        return bytes(body)

    def read_chunks(
        self, query_execution_id: str
    ) -> "Tuple[List[str], Iterator[List[List[Any]]], Optional[int]]":
        """Read a finished result through Arrow or the native Row/Datum API."""
        execution = self._executions.get(query_execution_id)
        if not self._uses_arrow(query_execution_id, execution):
            from sagemaker_studio.utils.sqlutils_async_reader import read_athena_result

            return read_athena_result(
                self.client,
                query_execution_id,
                skip_header=self._skip_row_header(execution),
            )

        # Stream the Arrow IPC body one record batch at a time instead of building the whole
        # pyarrow.Table up front (read_table/read_all) and capturing it in the generator. The
        # resume/Content-Length contract is unchanged: _read_stream still assembles and validates
        # the full body; only the Arrow decode is incremental. read_table stays eager for the
        # synchronous execute() path.
        started = time.monotonic()
        body = self._read_stream(query_execution_id)
        reader = ipc.open_stream(body)
        # Column names come straight from the stream schema, available before any batch is read.
        columns = [field.name for field in reader.schema]
        # Callers (and the positional-total contract) read ``total`` eagerly, before the chunk
        # iterator is consumed, and Arrow IPC carries no cheap row count -- so hold the decoded
        # batches in a list to report an exact total now. This still avoids the ~2x doubling of
        # the old path: no pyarrow.Table is ever materialized, and each batch is released as the
        # generator yields it, so at most the not-yet-yielded batches stay resident (never the
        # whole table plus a full Python-list copy at once).
        batches = deque(batch for batch in reader if batch.num_rows > 0)
        total = sum(batch.num_rows for batch in batches)
        logger.info(
            "Athena query %s: read %d rows (%d bytes) with GetQueryResultStream in %.2fs",
            query_execution_id,
            total,
            len(body),
            time.monotonic() - started,
        )

        def _chunks() -> "Iterator[List[List[Any]]]":
            while batches:
                # Pop from the front and drop the reference so the batch (and its Arrow buffers)
                # is freed once its Python rows have been yielded -- the converted rows and the
                # source batch never coexist across the whole result.
                batch = batches.popleft()
                converted = [_arrow_values(column) for column in batch.columns]
                del batch
                yield [list(row) for row in zip(*converted)]

        return columns, _chunks(), total

    def get_resources(
        self, resource_type: Optional[str], parents: Optional[Dict[str, str]] = None
    ) -> List[Any]:
        """Discover Athena resources through metadata APIs without a SQLAlchemy driver."""
        from sagemaker_studio.sql_engine.database_resource import DatabaseResource
        from sagemaker_studio.sql_engine.database_transformer import DatabaseTransformer

        catalog = self.catalog or "AwsDataCatalog"
        parents = parents or {}
        common = {"CatalogName": catalog, "WorkGroup": self.work_group}

        if resource_type not in ("DATABASE", "TABLE", "COLUMN", None):
            raise ValueError(f"Unsupported resource type: {resource_type!r}")

        if resource_type in ("DATABASE", None):
            items = self._metadata_pages("list_databases", "DatabaseList", **common)
            return [DatabaseResource(item["Name"], "DATABASE", ["TABLE"]) for item in items]

        database = DatabaseTransformer.get_required_resource_parent(parents, "DATABASE")
        if resource_type == "TABLE":
            items = self._metadata_pages(
                "list_table_metadata", "TableMetadataList", DatabaseName=database, **common
            )
            return [DatabaseResource(item["Name"], "TABLE", ["COLUMN"]) for item in items]

        if resource_type == "COLUMN":
            table = DatabaseTransformer.get_required_resource_parent(parents, "TABLE")
            response = self.client.get_table_metadata(
                DatabaseName=database, TableName=table, **common
            )
            columns = (response.get("TableMetadata") or {}).get("Columns") or []
            return [DatabaseResource(column["Name"], "COLUMN", []) for column in columns]

        raise ValueError(f"Unsupported resource type: {resource_type!r}")

    def _metadata_pages(self, operation_name: str, result_key: str, **request) -> List[dict]:
        items: List[dict] = []
        operation = getattr(self.client, operation_name)
        while True:
            response = operation(**request)
            items.extend(response.get(result_key) or [])
            token = response.get("NextToken")
            if not token:
                return items
            request["NextToken"] = token

    def rowcount(self, execution: dict) -> int:
        """Row count for a statement without a result set: GetQueryResults' UpdateCount for
        writes (as PyAthena reports it), -1 when there is none (DDL)."""
        substatement_type = execution.get("SubstatementType")
        if (
            execution.get("StatementType") == "DDL"
            and substatement_type not in _ROWCOUNT_SUBSTATEMENT_TYPES
        ):
            return -1
        try:
            response = self.client.get_query_results(
                QueryExecutionId=execution["QueryExecutionId"], MaxResults=1
            )
        except Exception:
            logger.debug("Failed to read the Athena update count", exc_info=True)
            return -1
        count = response.get("UpdateCount")
        return count if isinstance(count, int) else -1

    def execute(self, statement: str) -> SingleStatementResult:
        """Run ``statement`` and return its DataFrame (or row count) with execution metadata."""
        query_execution_id = self.start(statement)
        execution = self.wait(query_execution_id)
        metadata = execution_metadata(execution)
        metadata["result_reader"] = (
            "get_query_result_stream"
            if self._uses_arrow(query_execution_id, execution)
            else "get_query_results"
        )
        if not returns_rows(execution):
            return SingleStatementResult(
                result=self.rowcount(execution), execution_metadata=metadata
            )
        if self._uses_arrow(query_execution_id, execution):
            result = dataframe_from_arrow(self.read_table(query_execution_id))
        else:
            columns, chunks, _total = self.read_chunks(query_execution_id)
            rows = [row for chunk in chunks for row in chunk]
            result = DataFrame(rows, columns=columns)
        return SingleStatementResult(result=result, execution_metadata=metadata)

    def execute_without_fetch(self, statement: str) -> SingleStatementResult:
        """Run ``statement`` for the async path: rows are read later by execution id
        (``read_chunks``). Returns an ``AsyncResultMarker`` for a result set, else the row
        count."""
        from sagemaker_studio.utils.sqlutils_async import AsyncResultMarker

        query_execution_id = self.start(statement)
        execution = self.wait(query_execution_id)
        metadata = execution_metadata(execution)
        metadata["result_reader"] = (
            "get_query_result_stream"
            if self._uses_arrow(query_execution_id, execution)
            else "get_query_results"
        )
        if not returns_rows(execution):
            return SingleStatementResult(
                result=self.rowcount(execution), execution_metadata=metadata
            )
        return SingleStatementResult(
            result=AsyncResultMarker(execution_id=query_execution_id), execution_metadata=metadata
        )


def _read_available(body: Any) -> "Tuple[bytearray, Optional[Exception]]":
    """Read ``body`` to the end; returns the bytes received and the error that cut it off, if
    any."""
    data = bytearray()
    try:
        for chunk in body.iter_chunks(chunk_size=_STREAM_CHUNK_BYTES):
            data += chunk
    except _INTERRUPTED_READ_ERRORS as e:
        return data, e
    return data, None


def _content_length(response: dict) -> Optional[int]:
    """The response's Content-Length, or None when absent or not a number."""
    raw = ((response.get("ResponseMetadata") or {}).get("HTTPHeaders") or {}).get("content-length")
    try:
        return int(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None


def _status(response: dict) -> Optional[int]:
    status = (response.get("ResponseMetadata") or {}).get("HTTPStatusCode")
    return status if isinstance(status, int) else None


def returns_rows(execution: dict) -> bool:
    """Whether a finished query has a result set (DDL and writes report a row count instead)."""
    if execution.get("StatementType") == "DDL":
        return False
    return execution.get("SubstatementType") not in _ROWCOUNT_SUBSTATEMENT_TYPES


def execution_metadata(execution: dict) -> Dict[str, Any]:
    """Execution metadata from ``QueryExecution``, with the keys the PyAthena path reports
    (``AthenaTransformer.get_execution_metadata``)."""
    statistics = execution.get("Statistics") or {}
    status = execution.get("Status") or {}
    metadata: Dict[str, Any] = {"query_execution_id": execution.get("QueryExecutionId")}
    for key, field in (
        ("data_scanned_bytes", "DataScannedInBytes"),
        ("engine_execution_time_ms", "EngineExecutionTimeInMillis"),
        ("total_execution_time_ms", "TotalExecutionTimeInMillis"),
        ("query_queue_time_ms", "QueryQueueTimeInMillis"),
        ("query_planning_time_ms", "QueryPlanningTimeInMillis"),
        ("service_processing_time_ms", "ServiceProcessingTimeInMillis"),
    ):
        if statistics.get(field) is not None:
            metadata[key] = statistics[field]
    for key, field in (
        ("submission_time", "SubmissionDateTime"),
        ("completion_time", "CompletionDateTime"),
    ):
        value = status.get(field)
        if value is not None:
            metadata[key] = value.isoformat() if hasattr(value, "isoformat") else value
    state = status.get("State")
    if state:
        metadata["state"] = state
    output_location = (execution.get("ResultConfiguration") or {}).get("OutputLocation")
    if output_location:
        metadata["output_location"] = output_location
    engine = (execution.get("EngineVersion") or {}).get("EffectiveEngineVersion")
    if engine:
        metadata["engine_version"] = engine
    return metadata
