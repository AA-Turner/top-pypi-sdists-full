#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Schema inference for the NSS read path via the official ``INFER_STAGE_FILE_SCHEMA`` TVF.

A schema-less file read needs a Spark schema up front (to build ``DATA_SCHEMA`` for
``STAGE_FILE_READER``). We infer it with Spark's *own* inference (via the TVF) rather than
Snowflake's ``INFER_SCHEMA`` — so the inferred types match exactly what the sandbox Spark
reader produces. The per-file inference + cross-file merge happen inside the TVF
(SNOW-3715056), so there is no manual aggregate / ``GROUP BY``.

The TVF's ``SPARK_TYPE`` (Spark ``DataType.json()``) is carried through **verbatim** as each
column's ``SPARK_DATA_TYPE`` — SCOS does not re-derive it or round-trip it through an
intermediate ``StructType``.
"""

import json

from pyspark.errors.exceptions.base import AnalysisException
from pyspark.sql.types import StructType as PyStructType

from snowflake import snowpark
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.nss.nss_scan_options import (
    NssColumn,
    _stringify_reader_option,
    build_locations_json,
    build_spark_conf,
    normalize_locations,
    quote_options_literal,
    raise_if_locations_unsupported,
    sql_quote_literal,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import telemetry


def empty_nss_file_read_result(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    stage_paths: list[str] | None = None,
) -> DataFrameContainer:
    """Resolve an inferred empty schema using Spark's matched-file contract.

    ``stage_paths`` carries the full multi-path list so the check matches the scope
    inference ran over — see ``ensure_nss_empty_schema_has_visible_files``.
    """
    ensure_nss_empty_schema_has_visible_files(
        session, stage_path, file_format, stage_paths=stage_paths
    )

    from snowflake.snowpark_connect.relation.map_local_relation import (
        _create_zero_column_relation,
    )

    # The helper resolves the same request-bound Snowpark session from context.
    return _create_zero_column_relation().without_materialization()


def ensure_nss_empty_schema_has_visible_files(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    stage_paths: list[str] | None = None,
) -> None:
    """Raise Spark's inference error when an empty schema matched no input files.

    ``stage_paths`` must be the same list inference ran over. Checking only the first
    element would raise ``UNABLE_TO_INFER_SCHEMA`` for a legitimately empty schema whenever
    the *first* path happens to hold nothing Spark-visible while a later one holds real rows
    — e.g. ``read.json(["@stg/markers/", "@stg/objs/"])`` where ``markers/`` has only a
    hidden ``_SUCCESS`` and ``objs/`` has ``{}`` records. Spark's contract is about whether
    the read matched *any* input, so one visible file anywhere is enough.
    """
    candidates = stage_paths or [stage_path]
    if not any(stage_location_has_spark_visible_files(session, p) for p in candidates):
        exception = AnalysisException(
            error_class="UNABLE_TO_INFER_SCHEMA",
            message_parameters={"format": file_format.upper()},
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def stage_location_has_spark_visible_files(
    session: snowpark.Session,
    stage_path: str,
) -> bool:
    """Return whether Spark file discovery would find an input at ``stage_path``.

    This check is intentionally format-agnostic: Spark's CSV and JSON readers do
    not select files by extension, so any non-hidden file under a requested
    directory is an input candidate. Parsing and schema inference remain the
    responsibility of the selected reader.

    Snowflake ``LIST`` returns prefix matches. After normalizing each result to a
    stage-relative path, accept either the exact requested entry or a descendant
    separated by ``/``. Thus ``file.csv`` and ``file.csv/part-00000`` can satisfy
    ``@stage/file.csv``, which may identify either a file or a directory, while
    the prefix sibling ``file.csv.bak`` cannot.

    During directory discovery, exclude any descendant path component beginning
    with ``_`` or ``.`` (for example ``_SUCCESS`` or ``.crc``), matching Spark's
    hidden-file rules. An exact match is accepted before this filter because Spark
    permits a hidden file when the user names that file explicitly.

    The result distinguishes an existing input whose NSS schema inference is empty
    from a location with no matched files; it does not inspect contents or size.

    This intentionally follows the current NSS stage scan's file set. NSS does not
    yet enforce Spark's ``recursiveFileLookup`` or ``pathGlobFilter`` during the
    stage scan; applying those filters only to this existence check would make schema
    inference and row scanning disagree.
    """
    from snowflake.snowpark_connect.relation.read.source_resolution import (
        expand_dir_to_stage_files,
    )
    from snowflake.snowpark_connect.relation.read.utils import (
        cloud_list_path_to_relative,
    )

    unquoted_path = stage_path
    if (
        len(unquoted_path) >= 2
        and unquoted_path[0] == unquoted_path[-1]
        and unquoted_path[0] in ("'", '"')
    ):
        unquoted_path = unquoted_path[1:-1]
    relative_location = cloud_list_path_to_relative(unquoted_path)
    if relative_location is None:
        relative_location = (
            unquoted_path.split("/", 1)[1] if "/" in unquoted_path else ""
        )
    relative_location = relative_location.rstrip("/")

    def is_visible(listed_path: str) -> bool:
        normalized = listed_path.strip("/")
        if normalized == relative_location:
            return True

        if relative_location:
            prefix = f"{relative_location}/"
            if not normalized.startswith(prefix):
                return False
            descendant = normalized[len(prefix) :]
        else:
            descendant = normalized

        return bool(descendant) and not any(
            part.startswith(("_", ".")) for part in descendant.split("/") if part
        )

    return bool(
        expand_dir_to_stage_files(
            f"'{sql_quote_literal(unquoted_path)}'",
            session,
            skip_success_markers=False,
            path_filter=is_visible,
            max_results=1,
        )
    )


def infer_via_stage_file_schema(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    infer_fqn: str = "INFER_STAGE_FILE_SCHEMA",
    multiline: str = "false",
    sampling_ratio: str = "1",
    mode: str = "PERMISSIVE",
    corrupt_record_column: str = "_corrupt_record",
    reader_options: dict | None = None,
    spark_conf: dict | None = None,
    stage_paths: list[str] | None = None,
) -> list[NssColumn]:
    """Infer the column list via the official ``INFER_STAGE_FILE_SCHEMA`` TVF.

    ``stage_paths`` carries more than one path as ``LOCATIONS`` (SNOW-3993064). Inferring
    over the union is the whole point rather than an optimization: GS merges the file sets
    and infers once, so columns present in only some paths still appear and a type clash
    widens the way Spark's own merge does. Per-path inference then reconciled client-side
    would have to reimplement those merge rules and would not match. Mutually exclusive
    with ``LOCATION``; a single path stays on the scalar form.

    Contract (SNOW-3715056): named args ``LOCATION`` / ``FILE_FORMAT`` / ``OPTIONS_JSON``
    (top-level ``sparkConf`` / ``readerOptions``, matched case-insensitively); output is one
    row per column ``(COLUMN_NAME, SPARK_TYPE, NULLABLE, ORDER_ID)`` sorted by ``ORDER_ID``.
    ``SPARK_TYPE`` (Spark ``DataType.json()``) is carried through verbatim. An empty result
    represents a valid inferred ``StructType([])`` only when the caller confirms that the
    location matched at least one Spark-visible file (SNOW-3968261).
    """
    # Forward the caller's format reader options so inference splits/labels columns exactly
    # as the read will. For CSV this is essential: header/sep/delimiter/quote/escape drive
    # column detection — Spark's CSVInferSchema honors them (native-spark-sandbox-extensions
    # fileformat-csv README). Without them a non-default separator infers a single column
    # (later COLUMN_NOT_FOUND) and header rows leak into the data.
    reader_opts = {
        str(k): _stringify_reader_option(v) for k, v in (reader_options or {}).items()
    }
    lower = {k.lower(): k for k in reader_opts}
    # samplingRatio must be a JSON *number* in (0, 1] for GS
    # (InferStageFileSchemaImpl.validateReaderOptions -> value.isNumber()); a JSON string is
    # rejected at compile time. Honor the caller's option if set (CSV forwards it via
    # reader_options, JSON via the sampling_ratio arg), else full-sample.
    sampling_key = lower.get("samplingratio")
    sampling = reader_opts.pop(sampling_key) if sampling_key else sampling_ratio
    reader_opts["samplingRatio"] = float(sampling)
    # Set the infer defaults only when the caller didn't already supply them (case-insensitive),
    # so we never emit duplicate multiline/mode/... keys.
    if "multiline" not in lower:
        reader_opts["multiLine"] = multiline
    if "mode" not in lower:
        reader_opts["mode"] = mode
    if corrupt_record_column and "columnnameofcorruptrecord" not in lower:
        reader_opts["columnNameOfCorruptRecord"] = corrupt_record_column
    # Forward the same decoding-relevant spark.sql.* confs the read path sends (SPARK_CONF).
    # Chiefly spark.sql.timestampType: without it the sandbox infers TIMESTAMP_NTZ columns as
    # LTZ (SNOW-3861942) — the read path already forwards it, so inference must match or the
    # inferred DATA_SCHEMA disagrees with the read. Also carries timeZone / ANSI / etc.
    conf = build_spark_conf() if spark_conf is None else spark_conf
    opts = json.dumps({"sparkConf": conf, "readerOptions": reader_opts})
    # Escape single quotes in the raw-interpolated literals so a path/format name
    # containing a ``'`` cannot break out of the SQL string. OPTIONS_JSON is wrapped by
    # quote_options_literal, which is safe even when the payload contains ``$$`` —
    # ``corrupt_record_column`` (user-controllable) or an inferred name can.
    # SELECT * — the TVF's fixed output schema is (COLUMN_NAME, SPARK_TYPE, NULLABLE,
    # ORDER_ID), matching the native-spark-sandbox-extensions README; ORDER BY ORDER_ID
    # yields file column order. Rows are read positionally below in that declared order.
    # Decide on the *distinct* count and emit that same list, so the branch and the payload
    # cannot disagree (see ``normalize_locations``).
    distinct_paths = normalize_locations(stage_paths)
    if len(distinct_paths) > 1:
        location_clause = f"    LOCATIONS    => {quote_options_literal(build_locations_json(distinct_paths))},\n"
    else:
        location_clause = f"    LOCATION     => '{sql_quote_literal(stage_path)}',\n"
    query = (
        f"SELECT * FROM TABLE({infer_fqn}(\n"
        f"{location_clause}"
        f"    FILE_FORMAT  => '{sql_quote_literal(file_format)}',\n"
        f"    OPTIONS_JSON => {quote_options_literal(opts)}\n"
        ")) ORDER BY ORDER_ID"
    )
    # NSS schema-inference path (keyword kept out of the customer-visible log message)
    logger.info(f"INFER_STAGE_FILE_SCHEMA query: {query}")
    telemetry.report_nss_tvf("INFER_STAGE_FILE_SCHEMA")
    try:
        rows = session.sql(query).collect()
    except SnowparkSQLException as exc:
        # Only rewrites the message for a LOCATIONS rejection and re-raises; anything else
        # propagates untouched. This is the one eagerly-executed TVF call on the multi-path
        # path, so it is where a gate-off or over-cap deployment can be caught and explained.
        # An explicit-schema read never reaches *here* -- it calls the same TVF in
        # schema-adapt mode (SNOW-3853392), which always passes the scalar ``LOCATION`` and
        # so cannot trip the LOCATIONS gate. Its reader-side LOCATIONS rejection is still
        # caught lazily at the first materialization in map_read_csv / map_read_json
        # (SNOW-4019817).
        if len(distinct_paths) > 1:
            raise_if_locations_unsupported(exc, len(distinct_paths))
        raise
    return _nss_columns_from_tvf_rows(rows)


def _nss_columns_from_tvf_rows(rows: list) -> list[NssColumn]:
    """Map the TVF's fixed output rows to ``NssColumn``s.

    Rows are read positionally in the TVF's declared order:
    ``(COLUMN_NAME, SPARK_TYPE, NULLABLE, ORDER_ID)``. Shared by the inference and
    schema-adapt calls so both decode the row contract in one place.
    """
    return [
        NssColumn(
            name=row[0],
            spark_type=row[1],
            nullable=bool(row[2]) if row[2] is not None else True,
        )
        for row in rows
    ]


def adapt_user_schema_via_stage_file_schema(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    user_schema_json: str,
    infer_fqn: str = "INFER_STAGE_FILE_SCHEMA",
) -> list[NssColumn]:
    """Convert a caller-supplied Spark schema into ``NssColumn``s via the TVF's adapt mode.

    Passing ``USER_SCHEMA`` puts INFER_STAGE_FILE_SCHEMA into *schema-adapt* mode
    (SNOW-3853392): GS validates the JSON and emits the caller's own fields back as the
    TVF's standard ``(COLUMN_NAME, SPARK_TYPE, NULLABLE, ORDER_ID)`` rows. It is a
    compile-time constant-row plan -- ``buildAdaptModePlan`` returns before the sandbox
    scan plan is built -- so **no file is read and no inference runs**. The user's schema
    is passed through unchanged; there is no conflict resolution with the file.

    Why route through the TVF at all when SCOS already holds the schema: *before* this
    change the two schema paths encoded the TVF's row contract independently -- the
    schema-less path from the TVF's own rows, the explicit-schema path from a hand-rolled
    client-side conversion. That contract has already changed once (DATA_SCHEMA replaced
    SNOWFLAKE_TABLE_SCHEMA), and only the schema-less path gets exercised heavily, so the
    hand-rolled copy was the one positioned to rot unnoticed. The TVF is now the primary
    encoding for both paths; the client-side conversion survives only as the fallback in
    :func:`columns_for_explicit_schema` and for zero-column schemas.

    ``OPTIONS_JSON`` is deliberately omitted: it is optional for the TVF and adapt mode
    ignores reader options entirely (it never opens the file). ``LOCATION`` and
    ``FILE_FORMAT`` remain required -- GS still resolves the stage and format object.

    Always the scalar ``LOCATION``, never ``LOCATIONS`` (SNOW-4019817): adapt mode opens no
    file, so the union of paths cannot change the answer -- the schema is the caller's either
    way. For a multi-path read that means only ``stage_paths[0]`` is resolved here, while the
    reader still receives every path. If that first path happens to be empty or missing,
    ``isErrorIfNoFiles=true`` refuses, the caller falls back to the client-side conversion,
    and the read proceeds over all paths unaffected.

    Raises whatever ``session.sql`` raises; callers are expected to fall back to building
    the columns client-side, since a deployment whose GS predates SNOW-3853392 rejects
    ``USER_SCHEMA`` as an unknown named argument.

    Not every refusal is a deployment condition, though. ``nameResolve`` runs
    ``finalizeStageReference(isErrorIfNoFiles=true)`` and ``validateResolvedFormat`` before
    it branches on ``USER_SCHEMA``, so an empty directory, a missing stage privilege or an
    unsupported resolved format raises here too -- per-request causes, which is why the
    caller falls back rather than translating the error into a read failure.

    Those two groups differ in what the fallback costs, and the difference matters:
    ``STAGE_FILE_READER`` calls the same ``finalizeStageReference(isErrorIfNoFiles=true)``
    (``StageFileReaderImpl.java:328-334``), so a stage / empty-directory / privilege error is
    only *deferred* -- the read re-raises it, and the customer still sees it. But
    ``validateResolvedFormat`` is private to ``InferStageFileSchemaImpl`` with no counterpart
    in the reader, so a format rejection is genuinely dropped. That is not a regression --
    explicit-schema reads never called INFER before this change, so they never had that
    validation -- but a format INFER rejects and the reader accepts would take the fallback
    on *every* read. Not reachable today: INFER accepts PARQUET/CSV/JSON/XML, a superset of
    the CSV+JSON that NSS routes here. It becomes reachable if reader-side ORC/AVRO support
    (SNOW-3916185) lands first, and the fallback counter is what would surface it.
    """
    query = (
        f"SELECT * FROM TABLE({infer_fqn}(\n"
        f"    LOCATION     => '{sql_quote_literal(stage_path)}',\n"
        f"    FILE_FORMAT  => '{sql_quote_literal(file_format)}',\n"
        f"    USER_SCHEMA  => {quote_options_literal(user_schema_json)}\n"
        ")) ORDER BY ORDER_ID"
    )
    logger.info(f"INFER_STAGE_FILE_SCHEMA (schema-adapt) query: {query}")
    # Counted like any other INFER_STAGE_FILE_SCHEMA invocation (SNOW-3957228): this really
    # does issue that TVF, and without the count an adapt-mode failure would leave a request
    # summary with no INFER entry, misattributing it to the scan.
    telemetry.report_nss_tvf("INFER_STAGE_FILE_SCHEMA")
    return _nss_columns_from_tvf_rows(session.sql(query).collect())


def columns_for_explicit_schema(
    session: snowpark.Session,
    stage_path: str,
    file_format: str,
    spark_schema: PyStructType,
    infer_fqn: str = "INFER_STAGE_FILE_SCHEMA",
) -> list[NssColumn]:
    """DATA_SCHEMA columns for a caller-supplied Spark schema.

    Prefers the TVF's schema-adapt mode (see
    :func:`adapt_user_schema_via_stage_file_schema`) so both schema paths share one
    encoding of the row contract, and falls back to the client-side conversion when the
    backend does not offer it -- a GS predating SNOW-3853392 rejects ``USER_SCHEMA`` as an
    unknown named argument, and the fallback is exactly the behaviour that shipped before
    this change, so a read can never fail *because* adapt mode is unavailable.

    The two paths agree on names, nullability and the *parsed* ``spark_type`` JSON. They
    agree byte for byte too, except when a **nested** field name contains a non-ASCII
    character: Spark's ``DataType.json()`` escapes it (``caf\\u00e9``) while GS re-emits the
    node with Jackson, whose ``ESCAPE_NON_ASCII`` is off (``café``). Every consumer of
    ``spark_type`` parses it -- ``build_data_schema`` does ``json.loads`` -- so that
    divergence is inert, but do not treat byte equality as the contract.

    Pass the schema **after** any nullability relaxation: adapt mode echoes ``nullable``
    verbatim, so relaxing afterwards would be lost.
    """
    from snowflake.snowpark_connect.nss.nss_scan_options import (
        columns_from_spark_schema,
    )

    # GS requires a non-empty ``fields`` array; an explicit zero-column schema can only be
    # handled client-side (which yields the empty column list the read path expects).
    if not spark_schema.fields:
        return columns_from_spark_schema(spark_schema)

    try:
        return adapt_user_schema_via_stage_file_schema(
            session, stage_path, file_format, spark_schema.json(), infer_fqn
        )
    except Exception as exc:  # noqa: BLE001 -- any backend refusal falls back, see above
        # Counted, not just logged (SNOW-3957228): the fallback returns equivalent columns,
        # so it is invisible in results, and its two main causes -- a GS predating
        # SNOW-3853392, or ENABLE_INFER_STAGE_FILE_SCHEMA_TVF off -- are whole-deployment
        # conditions that would silently affect every explicit-schema read. The Snowflake
        # error code goes with the class name because on its own the class does not
        # discriminate: every documented cause arrives as the same Snowpark exception type.
        telemetry.report_nss_schema_adapt_fallback(
            type(exc).__name__, getattr(exc, "sql_error_code", None)
        )
        # A backend refusal is an expected deployment/per-request condition -- WARNING. Any
        # other class means SCOS itself failed while building or decoding the adapt call
        # (e.g. the TVF's row contract changed under ``_nss_columns_from_tvf_rows``), which
        # is a defect in this module, not a property of the deployment. Same fallback either
        # way -- a read must never fail *because* adapt mode is unavailable -- but a defect
        # logged at WARNING alongside routine version skew is a defect nobody reads.
        expected_refusal = isinstance(exc, SnowparkSQLException)
        log = logger.warning if expected_refusal else logger.error
        log(
            "NSS schema-adapt (USER_SCHEMA) "
            f"{'unavailable' if expected_refusal else 'FAILED UNEXPECTEDLY'}, building "
            "DATA_SCHEMA columns client-side instead: "
            f"{type(exc).__name__}: {exc}"
        )
        return columns_from_spark_schema(spark_schema)
