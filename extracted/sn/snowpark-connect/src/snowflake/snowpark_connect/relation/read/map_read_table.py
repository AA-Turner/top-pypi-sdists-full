#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import (
    SnowparkInvalidObjectNameException,
    SnowparkSQLException,
)
from snowflake.snowpark.types import StructField, StructType
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    make_column_names_snowpark_compatible,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import (
    global_config,
    is_iceberg_sql_extensions_enabled,
    sessions_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.utils import (
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.typed_column import FieldType
from snowflake.snowpark_connect.utils.context import (
    get_processed_views,
    get_spark_session_id,
)
from snowflake.snowpark_connect.utils.identifiers import (
    is_backtick_quoted,
    split_fully_qualified_spark_name,
    split_fully_qualified_spark_name_with_quoting,
    transform_identifier_for_snowflake,
)
from snowflake.snowpark_connect.utils.session import _get_current_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)
from snowflake.snowpark_connect.utils.temporary_view_helper import get_temp_view

# SNOW-3581131 / SNOW-3853933: `.entries` (current snapshot) and `.all_entries`
# (all snapshots) share one projection and differ only in the
# ICEBERG_TABLE_MANIFEST_ENTRIES `num_snapshots` argument, so both are built from a
# single template to keep them in sync.
_ICEBERG_CURRENT_SNAPSHOT = 1
_ICEBERG_ALL_SNAPSHOTS = -1


def _iceberg_entries_query(num_snapshots: int) -> str:
    # Envelope + data_file struct; spec_id via JOIN to ICEBERG_TABLE_MANIFESTS.
    # REDUCE types the data_file metric maps; `readable_metrics` is omitted
    # (separate gap). num_snapshots: 1 = current snapshot, -1 = all snapshots.
    return f"""
        WITH manifest_entries AS (
            SELECT
                REGEXP_SUBSTR(MANIFEST_FILE_NAME, '[^/]+$')   AS manifest_basename,
                MANIFEST_ENTRIES:status::INT                  AS status,
                MANIFEST_ENTRIES:snapshot_id::NUMBER          AS snapshot_id,
                MANIFEST_ENTRIES:sequence_number::NUMBER      AS sequence_number,
                MANIFEST_ENTRIES:file_sequence_number::NUMBER AS file_sequence_number,
                MANIFEST_ENTRIES:data_file                    AS df
            FROM TABLE(ICEBERG_TABLE_MANIFEST_ENTRIES(?, NULL, {num_snapshots}, TRUE))
        ),
        entry_manifests AS (
            SELECT DISTINCT
                REGEXP_SUBSTR(manifest_file:manifest_path::STRING, '[^/]+$') AS manifest_basename,
                manifest_file:partition_spec_id::INT                         AS spec_id
            FROM TABLE(ICEBERG_TABLE_MANIFESTS(?))
        )
        SELECT
            e.status,
            e.snapshot_id,
            e.sequence_number,
            e.file_sequence_number,
            CAST(OBJECT_CONSTRUCT_KEEP_NULL(
                'content',            e.df:content::INT,
                'file_path',          e.df:file_path::STRING,
                'file_format',        e.df:file_format::STRING,
                'spec_id',            m.spec_id,
                'partition',          e.df:partition,
                'record_count',       e.df:record_count::NUMBER,
                'file_size_in_bytes', e.df:file_size_in_bytes::NUMBER,
                'column_sizes',       REDUCE(e.df:column_sizes, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)),
                'value_counts',       REDUCE(e.df:value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)),
                'null_value_counts',  REDUCE(e.df:null_value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)),
                'nan_value_counts',   REDUCE(e.df:nan_value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)),
                'lower_bounds',       REDUCE(e.df:lower_bounds, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, TO_BINARY(x:value::STRING, 'HEX'))),
                'upper_bounds',       REDUCE(e.df:upper_bounds, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, TO_BINARY(x:value::STRING, 'HEX'))),
                'key_metadata',       TRY_CAST(e.df:key_metadata::STRING AS BINARY),
                'split_offsets',      e.df:split_offsets,
                'equality_ids',       e.df:equality_ids,
                'sort_order_id',      e.df:sort_order_id::INT,
                'referenced_data_file', e.df:referenced_data_file::STRING,
                -- V3 row-lineage / deletion-vector fields not exposed by the
                -- Snowflake manifest functions; NULL to match Spark's schema.
                'first_row_id',       CAST(NULL AS BIGINT),
                'content_offset',     CAST(NULL AS BIGINT),
                'content_size_in_bytes', CAST(NULL AS BIGINT)
            ) AS OBJECT(
                content               INT,
                file_path             VARCHAR,
                file_format           VARCHAR,
                spec_id               INT,
                partition             VARIANT,
                record_count          NUMBER,
                file_size_in_bytes    NUMBER,
                column_sizes          MAP(INT, BIGINT),
                value_counts          MAP(INT, BIGINT),
                null_value_counts     MAP(INT, BIGINT),
                nan_value_counts      MAP(INT, BIGINT),
                lower_bounds          MAP(INT, BINARY),
                upper_bounds          MAP(INT, BINARY),
                key_metadata          BINARY,
                split_offsets         ARRAY(BIGINT),
                equality_ids          ARRAY(INT),
                sort_order_id         INT,
                first_row_id          BIGINT,
                referenced_data_file  VARCHAR,
                content_offset        BIGINT,
                content_size_in_bytes BIGINT
            )) AS data_file
        FROM manifest_entries e
        LEFT JOIN entry_manifests m USING (manifest_basename)
    """


def _iceberg_files_query(num_snapshots: int) -> str:
    # SNOW-3471789: `.files` returns Spark's Iceberg `.files` schema (not the
    # Snowflake-native ICEBERG_TABLE_FILES columns). REDUCE folds Iceberg's
    # array-of-{key,value} metric fields into the object that MAP casts cleanly.
    # `.data_files`/`.delete_files` (current snapshot) and `.all_data_files`
    # (all snapshots) reuse this projection, differing only in num_snapshots.
    return f"""
        WITH manifest_entries AS (
            SELECT
                REGEXP_SUBSTR(MANIFEST_FILE_NAME, '[^/]+$')            AS manifest_basename,
                MANIFEST_ENTRIES:data_file:content::NUMBER             AS content,
                MANIFEST_ENTRIES:data_file:file_path::STRING           AS file_path,
                MANIFEST_ENTRIES:data_file:file_format::STRING         AS file_format,
                MANIFEST_ENTRIES:data_file:partition                  AS partition,
                MANIFEST_ENTRIES:data_file:record_count::NUMBER        AS record_count,
                MANIFEST_ENTRIES:data_file:file_size_in_bytes::NUMBER  AS file_size_in_bytes,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:column_sizes, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)) AS MAP(INT, BIGINT))       AS column_sizes,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)) AS MAP(INT, BIGINT))       AS value_counts,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:null_value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)) AS MAP(INT, BIGINT))       AS null_value_counts,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:nan_value_counts, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, x:value)) AS MAP(INT, BIGINT))       AS nan_value_counts,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:lower_bounds, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, TO_BINARY(x:value::STRING, 'HEX'))) AS MAP(INT, BINARY)) AS lower_bounds,
                CAST(REDUCE(MANIFEST_ENTRIES:data_file:upper_bounds, OBJECT_CONSTRUCT(),
                    (acc, x) -> OBJECT_INSERT(acc, x:key::STRING, TO_BINARY(x:value::STRING, 'HEX'))) AS MAP(INT, BINARY)) AS upper_bounds,
                TRY_CAST(MANIFEST_ENTRIES:data_file:key_metadata::STRING AS BINARY)    AS key_metadata,
                CAST(MANIFEST_ENTRIES:data_file:split_offsets AS ARRAY(BIGINT))        AS split_offsets,
                CAST(MANIFEST_ENTRIES:data_file:equality_ids  AS ARRAY(INT))          AS equality_ids,
                MANIFEST_ENTRIES:data_file:sort_order_id::NUMBER       AS sort_order_id,
                MANIFEST_ENTRIES:data_file:referenced_data_file::STRING AS referenced_data_file,
                -- V3 row-lineage / deletion-vector fields not exposed by the
                -- Snowflake manifest functions; NULL to match Spark's schema.
                CAST(NULL AS BIGINT)                                   AS first_row_id,
                CAST(NULL AS BIGINT)                                   AS content_offset,
                CAST(NULL AS BIGINT)                                   AS content_size_in_bytes
            FROM TABLE(ICEBERG_TABLE_MANIFEST_ENTRIES(?, NULL, {num_snapshots}, TRUE))
            WHERE MANIFEST_ENTRIES:status::NUMBER != 2
        ),
        entry_manifests AS (
            SELECT DISTINCT
                REGEXP_SUBSTR(manifest_file:manifest_path::STRING, '[^/]+$') AS manifest_basename,
                manifest_file:partition_spec_id::NUMBER                      AS spec_id
            FROM TABLE(ICEBERG_TABLE_MANIFESTS(?))
        )
        SELECT
            e.content,
            e.file_path,
            e.file_format,
            m.spec_id,
            e.partition,
            e.record_count,
            e.file_size_in_bytes,
            e.column_sizes,
            e.value_counts,
            e.null_value_counts,
            e.nan_value_counts,
            e.lower_bounds,
            e.upper_bounds,
            e.key_metadata,
            e.split_offsets,
            e.equality_ids,
            e.sort_order_id,
            e.first_row_id,
            e.referenced_data_file,
            e.content_offset,
            e.content_size_in_bytes
        FROM manifest_entries e
        LEFT JOIN entry_manifests m USING (manifest_basename)
    """


_MANIFESTS_REFERENCE_SNAPSHOT_ID = "REGEXP_SUBSTR(MANIFEST_LIST_FILE_NAME, 'snap-(-{0,1}[0-9]+)-', 1, 1, 'e', 1)::NUMBER"


def _iceberg_manifests_query(*, all_snapshots: bool) -> str:
    # SNOW-3527660: ICEBERG_TABLE_MANIFESTS returns every snapshot's manifest-list
    # entries, keyed by MANIFEST_LIST_FILE_NAME (`snap-<snapshot-id>-<n>-<uuid>`).
    # `.all_manifests` keeps every row and exposes that snapshot id as
    # `reference_snapshot_id`; `.manifests` is current-snapshot only, so it hides
    # that column and restricts to the manifest list whose embedded snapshot id
    # equals the current snapshot. Both share this projection so they stay in sync.
    reference_column = (
        f",\n            {_MANIFESTS_REFERENCE_SNAPSHOT_ID} AS reference_snapshot_id"
        if all_snapshots
        else ""
    )
    current_snapshot_filter = (
        ""
        if all_snapshots
        else (
            f"\n        WHERE {_MANIFESTS_REFERENCE_SNAPSHOT_ID} = ("
            '\n            SELECT METADATA:"current-snapshot-id"::NUMBER'
            "\n            FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA(?))"
            "\n        )"
        )
    )
    return f"""
        SELECT
            manifest_file:content::INT                                    AS content,
            manifest_file:manifest_path::STRING                           AS path,
            manifest_file:manifest_length::NUMBER                         AS length,
            manifest_file:partition_spec_id::INT                          AS partition_spec_id,
            manifest_file:added_snapshot_id::NUMBER                       AS added_snapshot_id,
            manifest_file:added_files_count::INT                          AS added_data_files_count,
            manifest_file:existing_files_count::INT                       AS existing_data_files_count,
            manifest_file:deleted_files_count::INT                        AS deleted_data_files_count,
            COALESCE(manifest_file:added_delete_files_count::INT, 0)      AS added_delete_files_count,
            COALESCE(manifest_file:existing_delete_files_count::INT, 0)   AS existing_delete_files_count,
            COALESCE(manifest_file:deleted_delete_files_count::INT, 0)    AS deleted_delete_files_count,
            CAST(manifest_file:partitions AS ARRAY(OBJECT(
                contains_null BOOLEAN,
                contains_nan  BOOLEAN,
                lower_bound   VARCHAR,
                upper_bound   VARCHAR
            )))                                                           AS partition_summaries{reference_column}
        FROM TABLE(ICEBERG_TABLE_MANIFESTS(?)){current_snapshot_filter}
    """


ICEBERG_METADATA_TABLE_QUERIES = {
    "files": _iceberg_files_query(_ICEBERG_CURRENT_SNAPSHOT),
    # SNOW-3471788: ICEBERG_TABLE_SNAPSHOTS replaces the earlier
    # ICEBERG_TABLE_METADATA + LATERAL FLATTEN approach; the dedicated
    # function returns Spark-compatible column names directly.
    "snapshots": (
        "SELECT"
        "  committed_at,"
        "  snapshot_id,"
        "  parent_id,"
        "  operation,"
        "  manifest_list,"
        "  CAST(summary AS MAP(VARCHAR, VARCHAR)) AS summary"
        " FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_SNAPSHOTS(?))"
    ),
    "manifests": _iceberg_manifests_query(all_snapshots=False),
    "refs": """
        SELECT
            ref.key AS name,
            UPPER(ref.value:"type"::STRING) AS type,
            ref.value:"snapshot-id"::NUMBER AS snapshot_id,
            ref.value:"max-ref-age-ms"::NUMBER AS max_reference_age_in_ms,
            ref.value:"min-snapshots-to-keep"::INT AS min_snapshots_to_keep,
            ref.value:"max-snapshot-age-ms"::NUMBER AS max_snapshot_age_in_ms
        FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA(?)) metadata,
             LATERAL FLATTEN(INPUT => metadata.METADATA:refs) ref
    """,
    "history": """
        WITH RECURSIVE
        metadata_raw AS (
            SELECT
                METADATA:"current-snapshot-id"::NUMBER AS current_snapshot_id,
                METADATA:snapshots                      AS snapshots_json,
                METADATA:"snapshot-log"                 AS snapshot_log_json
            FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA(?))
        ),
        snapshots_flat AS (
            SELECT
                snap.value:"snapshot-id"::NUMBER        AS snapshot_id,
                snap.value:"parent-snapshot-id"::NUMBER AS parent_id
            FROM metadata_raw,
                 LATERAL FLATTEN(INPUT => metadata_raw.snapshots_json) snap
        ),
        ancestors(snapshot_id) AS (
            SELECT current_snapshot_id FROM metadata_raw
            UNION ALL
            SELECT s.parent_id
            FROM snapshots_flat s
            INNER JOIN ancestors a ON s.snapshot_id = a.snapshot_id
            WHERE s.parent_id IS NOT NULL
        ),
        history_entries AS (
            SELECT
                TO_TIMESTAMP_NTZ(entry.value:"timestamp-ms"::NUMBER / 1000) AS made_current_at,
                entry.value:"snapshot-id"::NUMBER                            AS snapshot_id
            FROM metadata_raw,
                 LATERAL FLATTEN(INPUT => metadata_raw.snapshot_log_json) entry
        )
        SELECT
            h.made_current_at,
            h.snapshot_id,
            s.parent_id,
            (a.snapshot_id IS NOT NULL)::BOOLEAN AS is_current_ancestor
        FROM history_entries h
        LEFT JOIN snapshots_flat s ON h.snapshot_id = s.snapshot_id
        LEFT JOIN ancestors a ON h.snapshot_id = a.snapshot_id
    """,
    "metadata_log_entries": """
        WITH
        metadata_raw AS (
            SELECT
                METADATA_FILE_NAME                                       AS current_file,
                METADATA:"last-updated-ms"::NUMBER                       AS current_ts_ms,
                METADATA:"current-snapshot-id"::NUMBER                   AS current_snapshot_id,
                METADATA:snapshots                                       AS snapshots_json,
                METADATA:"snapshot-log"                                  AS snapshot_log_json,
                METADATA:"metadata-log"                                  AS metadata_log_json
            FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA(?))
        ),
        snapshots_flat AS (
            SELECT
                snap.value:"snapshot-id"::NUMBER                         AS snapshot_id,
                snap.value:"schema-id"::INT                              AS schema_id,
                snap.value:"sequence-number"::NUMBER                     AS sequence_number
            FROM metadata_raw,
                 LATERAL FLATTEN(INPUT => metadata_raw.snapshots_json) snap
        ),
        snapshot_log_flat AS (
            SELECT
                sl.value:"snapshot-id"::NUMBER                           AS snapshot_id,
                sl.value:"timestamp-ms"::NUMBER                          AS timestamp_ms
            FROM metadata_raw,
                 LATERAL FLATTEN(INPUT => metadata_raw.snapshot_log_json) sl
        ),
        historical_entries AS (
            SELECT
                TO_TIMESTAMP_NTZ(ml.ts_ms / 1000)       AS timestamp,
                ml.metadata_file                          AS file,
                MAX_BY(sl.snapshot_id, sl.timestamp_ms)  AS latest_snapshot_id
            FROM (
                SELECT
                    ml.value:"metadata-file"::STRING AS metadata_file,
                    ml.value:"timestamp-ms"::NUMBER  AS ts_ms
                FROM metadata_raw,
                     LATERAL FLATTEN(INPUT => metadata_raw.metadata_log_json) ml
            ) ml
            LEFT JOIN snapshot_log_flat sl
                   ON sl.timestamp_ms <= ml.ts_ms
            GROUP BY ml.metadata_file, ml.ts_ms
        ),
        all_entries AS (
            SELECT
                TO_TIMESTAMP_NTZ(current_ts_ms / 1000) AS timestamp,
                current_file                            AS file,
                current_snapshot_id                     AS latest_snapshot_id
            FROM metadata_raw
            UNION ALL
            SELECT timestamp, file, latest_snapshot_id FROM historical_entries
        )
        SELECT
            a.timestamp,
            a.file,
            a.latest_snapshot_id,
            s.schema_id                                                  AS latest_schema_id,
            s.sequence_number                                            AS latest_sequence_number
        FROM all_entries a
        LEFT JOIN snapshots_flat s ON a.latest_snapshot_id = s.snapshot_id
        ORDER BY a.timestamp
    """,
    "entries": _iceberg_entries_query(_ICEBERG_CURRENT_SNAPSHOT),
}

# SNOW-3834853: `.data_files` = `.files` restricted to data files (content 0;
# NULL on V1). Reuses the `.files` projection so the two stay in sync.
ICEBERG_METADATA_TABLE_QUERIES["data_files"] = (
    "SELECT * FROM ("
    + ICEBERG_METADATA_TABLE_QUERIES["files"]
    + ") WHERE COALESCE(content, 0) = 0"
)

# SNOW-3852580: `.delete_files` = `.files` restricted to delete files
# (position deletes content 1, equality deletes content 2). Mirror of
# `.data_files`; reuses the `.files` projection so the two stay in sync.
ICEBERG_METADATA_TABLE_QUERIES["delete_files"] = (
    "SELECT * FROM ("
    + ICEBERG_METADATA_TABLE_QUERIES["files"]
    + ") WHERE COALESCE(content, 0) != 0"
)

# SNOW-3853933: `.all_entries` is `.entries` across all snapshots (both data and
# delete files) - same projection, differing only in the num_snapshots argument.
ICEBERG_METADATA_TABLE_QUERIES["all_entries"] = _iceberg_entries_query(
    _ICEBERG_ALL_SNAPSHOTS
)

# SNOW-3527661: `.all_data_files` = `.data_files` across all snapshots. Same
# projection as `.files`/`.data_files`; only the ICEBERG_TABLE_MANIFEST_ENTRIES
# num_snapshots arg changes (1 = current snapshot, -1 = all), then restricted to
# data files (content 0). Derived from `.files` so the projections stay in sync.
ICEBERG_METADATA_TABLE_QUERIES["all_data_files"] = (
    "SELECT * FROM ("
    + _iceberg_files_query(_ICEBERG_ALL_SNAPSHOTS)
    + ") WHERE COALESCE(content, 0) = 0"
)

# SNOW-3527660: `.all_manifests` spans all snapshots and exposes
# reference_snapshot_id; `.manifests` (current snapshot) shares the same
# projection. Both are built by _iceberg_manifests_query.
ICEBERG_METADATA_TABLE_QUERIES["all_manifests"] = _iceberg_manifests_query(
    all_snapshots=True
)

# Times the base table name is bound (one per `?`). `files`/`entries`/`data_files`/
# `delete_files`/`all_entries`/`all_data_files` call two table functions; `manifests`
# now also binds ICEBERG_TABLE_METADATA for the current-snapshot filter;
# `all_manifests` binds once. Explicit so a literal `?` in a regex/comment can't
# miscount the binding. Kept in sync by a unit test.
ICEBERG_METADATA_TABLE_BIND_COUNTS = {
    "files": 2,
    "entries": 2,
    "data_files": 2,
    "delete_files": 2,
    "all_entries": 2,
    "all_data_files": 2,
    "manifests": 2,
}

WAP_BRANCH_SPARK_CONFIG = "spark.wap.branch"

UNSUPPORTED_ICEBERG_METADATA_TABLES = {
    "all_delete_files",
    "partitions",
    "position_deletes",
}


def _split_iceberg_metadata_table_name(
    name_parts: list[str],
) -> tuple[list[str], str | None]:
    # Metadata-table routing requires Iceberg SQL extensions (per the WAP
    # identifier-resolution spec). Without them any dotted suffix
    # (e.g. `.snapshots`, `.files`) is treated as a plain Snowflake table name to
    # avoid misrouting non-Iceberg workloads. This gate applies uniformly to
    # 2-, 3- and 4-part names.
    if not is_iceberg_sql_extensions_enabled():
        return name_parts, None

    if len(name_parts) < 2:
        return name_parts, None

    suffix = name_parts[-1].lower()
    if suffix in ICEBERG_METADATA_TABLE_QUERIES:
        return name_parts[:-1], suffix
    if suffix in UNSUPPORTED_ICEBERG_METADATA_TABLES:
        return name_parts[:-1], suffix
    return name_parts, None


def _refresh_iceberg_table_metadata(
    session: snowpark.Session, base_table_name: str
) -> None:
    """Force synchronous Iceberg metadata generation before reading snapshots.

    On Managed Iceberg the ``INFORMATION_SCHEMA.ICEBERG_TABLE_SNAPSHOTS`` table
    function is populated asynchronously (observed ~7-15s) after a write, so a
    read issued immediately after a write can miss the latest snapshot (or see
    zero rows). ``SYSTEM$GET_ICEBERG_TABLE_INFORMATION`` generates that metadata
    synchronously, so the subsequent snapshots query sees an up-to-date result
    without any polling/retry.

    Best-effort: on catalog-linked (Glue / Unity) or missing tables this call
    fails, but the snapshots query that follows raises the proper actionable
    error, so failures here are swallowed.
    """
    try:
        session.sql(
            "SELECT SYSTEM$GET_ICEBERG_TABLE_INFORMATION(?)",
            params=[base_table_name],
        ).collect()
    except Exception as e:  # noqa: BLE001 - best-effort refresh
        logger.debug(
            "SYSTEM$GET_ICEBERG_TABLE_INFORMATION refresh skipped for %s: %s",
            base_table_name,
            e,
        )


def _read_iceberg_metadata_table(
    table_name: str,
    base_table_parts: list[str],
    backtick_flags: list[bool],
    metadata_table_name: str,
    session: snowpark.Session,
    plan_id: int,
) -> DataFrameContainer:
    if metadata_table_name not in ICEBERG_METADATA_TABLE_QUERIES:
        exception = SnowparkConnectNotImplementedError(
            f"Iceberg metadata table '{metadata_table_name}' is not supported"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    base_table_name = ".".join(
        transform_identifier_for_snowflake(part, is_backtick_quoted=flag)
        for part, flag in zip(base_table_parts, backtick_flags)
    )

    # Every metadata table (incl. `.files`, now backed by the async
    # ICEBERG_TABLE_MANIFEST_ENTRIES) reads metadata Managed Iceberg generates
    # asynchronously, so force a synchronous refresh before reading.
    _refresh_iceberg_table_metadata(session, base_table_name)

    query = ICEBERG_METADATA_TABLE_QUERIES[metadata_table_name]
    # Bind the base table name once per `?` placeholder (see BIND_COUNTS).
    n_binds = ICEBERG_METADATA_TABLE_BIND_COUNTS.get(metadata_table_name, 1)
    df = session.sql(query, params=[base_table_name] * n_binds)
    try:
        # Force evaluation here. ``post_process_df`` rewrites Snowflake 2003 into a
        # generic TABLE_OR_VIEW_NOT_FOUND ``AnalysisException``, which would
        # bypass the CLD-specific translation below.
        _ = df.schema.fields
    except SnowparkInvalidObjectNameException as e:
        # SNOW-3471788 (Unity / Glue CLD client-side guard): before
        # Snowpark hands the call to Snowflake it validates the
        # ``params=[base_table_name]`` value as a Snowflake object name.
        # On Unity Iceberg REST tables the three-part name (and on some
        # current Glue rollouts too) fails this client-side check with
        # ``1500: The object name '<db>.<schema>.<table>' is invalid``,
        # so the SnowparkSQLException 2003 branch below never gets a
        # chance to fire. The root cause is identical (the
        # ``INFORMATION_SCHEMA.ICEBERG_TABLE_*`` functions don't accept
        # CLD-qualified names), so surface the same actionable error
        # whether the rejection happens client-side or server-side.
        if base_table_parts and _looks_like_cld_qualified_name(
            base_table_parts, session
        ):
            raise _iceberg_metadata_cld_unsupported(
                metadata_table_name, base_table_name
            ) from e
        raise
    except SnowparkSQLException as e:
        # SNOW-3471788: Snowflake's INFORMATION_SCHEMA.ICEBERG_TABLE_* table
        # functions only resolve managed-Iceberg tables — they return a hard
        # "object does not exist" (2003) on tables in catalog-linked
        # databases (Glue / Unity Iceberg REST) even though the table
        # itself is fully visible to `SELECT`. Surface this as an
        # actionable AnalysisException rather than letting the customer
        # think their table was deleted.
        if (
            getattr(e, "sql_error_code", None) == 2003
            and base_table_parts
            and _looks_like_cld_qualified_name(base_table_parts, session)
        ):
            raise _iceberg_metadata_cld_unsupported(
                metadata_table_name, base_table_name
            ) from e
        # SNOW-3471788 (Managed path): On Managed Iceberg tables the
        # `INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA` table function backing
        # `<table>.snapshots` is not yet generally available in every
        # Snowflake region/edition, so the SELECT fails with
        # 002004 (42601) "Invalid identifier
        # INFORMATION_SCHEMA.<func>" rather than the friendlier 2003 path.
        # The customer's `<base>.snapshots` reference looked perfectly
        # valid on the Spark side, so translate the cryptic compiler
        # error into something they can act on.
        if getattr(
            e, "sql_error_code", None
        ) == 2004 and _looks_like_missing_iceberg_metadata_function(
            e, metadata_table_name
        ):
            exception = AnalysisException(
                f"Iceberg metadata subtable '.{metadata_table_name}' "
                "requires the Snowflake "
                "`INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA` table "
                "function, which is not yet available in this Snowflake "
                "region/edition. Track availability with your Snowflake "
                "account team; in the meantime you can read the Iceberg "
                "metadata directly from the table's metadata.json file "
                f"on object storage. Base table: `{base_table_name}`."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception from e
        raise
    return post_process_df(df, plan_id, table_name)


def _iceberg_metadata_cld_unsupported(
    metadata_table_name: str, base_table_name: str
) -> AnalysisException:
    """Build the shared SNOW-3471788 AnalysisException for Iceberg
    metadata-table queries against CLD tables.

    Two call sites use the same message:

    1. ``SnowparkSQLException`` with sql_error_code 2003 — Snowflake
       server-side "object does not exist" coming out of
       ``INFORMATION_SCHEMA.ICEBERG_TABLE_*`` against a CLD table.
    2. ``SnowparkInvalidObjectNameException`` (code 1500) — Snowpark's
       client-side object-name validator rejects the CLD-qualified
       parameter before the request even leaves the process. Observed
       primarily on Unity Iceberg REST today.
    """
    exception = AnalysisException(
        f"Iceberg metadata table '.{metadata_table_name}' is not "
        "supported on Snowflake catalog-linked Iceberg tables "
        f"(`{base_table_name}`). Snowflake's "
        "`INFORMATION_SCHEMA.ICEBERG_TABLE_*` functions only "
        "resolve managed-Iceberg tables (this applies to both "
        "Glue and Unity Iceberg REST catalogs). Workarounds: "
        "(a) query the metadata file directly from the external "
        "catalog (e.g. AWS Glue's GetTable API or the Iceberg "
        "REST endpoint + manifest parsing), or (b) re-create the "
        "table as a Managed Iceberg table — Snowflake then "
        f"exposes `.{metadata_table_name}` via INFORMATION_SCHEMA."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def _looks_like_missing_iceberg_metadata_function(
    e: SnowparkSQLException,
    metadata_table_name: str,
) -> bool:
    """Best-effort match: is the Snowflake 2004 'Invalid identifier' error
    pointing at one of our `INFORMATION_SCHEMA.ICEBERG_TABLE_*` calls?

    Snowflake error text for the missing-function case looks like
    `Invalid identifier 'INFORMATION_SCHEMA.ICEBERG_TABLE_METADATA'`.
    We deliberately match on the family token (`ICEBERG_TABLE_`) rather
    than the exact function name so that a future rename
    (e.g. `ICEBERG_TABLE_SNAPSHOTS`) still gets the friendlier message.
    Returns False on any unexpected shape so the original
    `SnowparkSQLException` propagates intact.
    """
    if not metadata_table_name:
        return False
    msg = (getattr(e, "message", None) or str(e) or "").upper()
    return "ICEBERG_TABLE_" in msg and "INVALID IDENTIFIER" in msg


def _looks_like_cld_qualified_name(
    base_table_parts: list[str],
    session: snowpark.Session,
) -> bool:
    """Best-effort check: is the first part of the fully-qualified name a
    catalog-linked database? Avoids a Snowflake round-trip when SCOS's
    own CLD context flag is set; falls back to the per-database catalog
    cache otherwise. Returns False on any lookup error so the original
    SnowparkSQLException still propagates cleanly.
    """
    try:
        from snowflake.snowpark_connect.utils.cld_context import is_in_cld_context

        if is_in_cld_context():
            return True
    except Exception:
        pass

    if not base_table_parts:
        return False
    db_name = base_table_parts[0].strip('"').upper()
    if not db_name:
        return False
    try:
        rows = session.sql(
            "SELECT CATALOG_NAME FROM SNOWFLAKE.INFORMATION_SCHEMA.DATABASES "
            "WHERE DATABASE_NAME = ? AND CATALOG_NAME IS NOT NULL",
            params=[db_name],
        ).collect()
        return len(rows) > 0
    except Exception:
        return False


def post_process_df(
    df: snowpark.DataFrame, plan_id: int, source_table_name: str = None
) -> DataFrameContainer:
    try:
        true_names = list(map(lambda x: unquote_if_quoted(x), df.columns))
        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, plan_id
        )
        name_parts = split_fully_qualified_spark_name(source_table_name)

        # If table name is not fully qualified (only has table name, no database),
        # add current schema name to qualifiers so columns can be referenced with database prefix
        # Note: In Spark, "database" corresponds to Snowflake "schema"
        if source_table_name and len(name_parts) == 1:
            session = _get_current_snowpark_session()
            current_schema = session.get_current_schema()
            if current_schema:
                name_parts = [unquote_if_quoted(current_schema)] + name_parts

        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=true_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                FieldType(emulate_integral_types(f.datatype), f.nullable)
                for f in df.schema.fields
            ],
            column_qualifiers=(
                [{ColumnQualifier(tuple(name_parts))} for _ in true_names]
                if source_table_name
                else None
            ),
        )
    except SnowparkSQLException as e:
        # Check if this is a table/view not found error
        # Snowflake error codes: 002003 (42S02) - Object does not exist or not authorized
        if hasattr(e, "sql_error_code") and e.sql_error_code == 2003:
            exception = AnalysisException(
                f"[TABLE_OR_VIEW_NOT_FOUND] The table or view cannot be found. {source_table_name}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception from None  # Suppress original exception to reduce message size
        # Re-raise if it's not a table not found error
        raise


def _get_temporary_view(
    temp_view: DataFrameContainer, table_name: str, plan_id: int
) -> DataFrameContainer:
    if temp_view.has_zero_columns():
        return DataFrameContainer.create_with_column_mapping(
            dataframe=temp_view.dataframe.select("__DUMMY"),
            spark_column_names=["__DUMMY"],
            snowpark_column_names=["__DUMMY"],
            column_is_internal=[True],
        )

    view_schema_fields = temp_view.dataframe.schema.fields
    fields_names = [field.name for field in view_schema_fields]

    snowpark_column_names = make_column_names_snowpark_compatible(
        temp_view.column_map.get_spark_columns(), plan_id
    )
    # Rename columns in dataframe to prevent conflicting names during joins
    renamed_df = temp_view.dataframe.select(
        *(
            temp_view.dataframe.col(orig).alias(alias)
            for orig, alias in zip(fields_names, snowpark_column_names)
        )
    )
    # do not flatten initial rename when reading table
    # TODO: remove once SNOW-2203826 is done
    if renamed_df._select_statement is not None:
        renamed_df._select_statement.flatten_disabled = True

    new_column_map = ColumnNameMap(
        spark_column_names=temp_view.column_map.get_spark_columns(),
        snowpark_column_names=snowpark_column_names,
        column_metadata=temp_view.column_map.column_metadata,
        column_qualifiers=[
            {ColumnQualifier(tuple(split_fully_qualified_spark_name(table_name)))}
            for _ in range(len(temp_view.column_map.get_spark_columns()))
        ],
        parent_column_name_map=temp_view.column_map.get_parent_column_name_map(),
    )

    # TODO: this is a column, do we need _is_column=False?
    schema = StructType(
        [
            StructField(snp_name, f.datatype, f.nullable, _is_column=False)
            for snp_name, f in zip(snowpark_column_names, view_schema_fields)
        ]
    )
    return DataFrameContainer(
        dataframe=renamed_df,
        column_map=new_column_map,
        table_name=temp_view.table_name,
        alias=temp_view.alias,
        partition_hint=temp_view.partition_hint,
        cached_schema_getter=lambda: schema,
        sort_exprs=temp_view.sort_exprs,
    )


_INT64_MIN = -(2**63)
_INT64_MAX = 2**63 - 1


# Python's ``datetime`` only spans year 1..9999, so the safe range for
# millis-since-epoch values we'll convert with ``fromtimestamp`` is tighter
# than the 64-bit signed range. Pre-compute the boundaries here so the
# extractor can reject overflow at the SCOS boundary with a clear message
# (otherwise ``datetime.fromtimestamp`` raises a less actionable
# ``OverflowError`` / ``ValueError`` deep inside Snowpark).
#
# Implementation notes:
#  * We compute the bounds via ``datetime(...).timestamp()`` with explicit
#    ``tzinfo=UTC`` so the result is platform-independent (without a tz,
#    ``timestamp()`` would interpret the value as local time). On Python
#    3.11+ (SCOS's minimum) the behavior of ``timestamp()`` and the inverse
#    ``fromtimestamp(..., tz=UTC)`` is fully specified for the year 1..9999
#    range; on some pre-3.11 Windows builds ``fromtimestamp`` with negative
#    values is documented as platform-dependent, but that's outside our
#    support window.
#  * ``_DATETIME_MIN_MS`` is the count of millis from the Unix epoch back
#    to ``0001-01-01T00:00:00Z`` (a large negative number); ``_DATETIME_MAX_MS``
#    is millis forward to ``9999-12-31T23:59:59.999Z``. Any millis value
#    within ``[_DATETIME_MIN_MS, _DATETIME_MAX_MS]`` is guaranteed to round-
#    trip back to a valid ``datetime`` via ``fromtimestamp(millis/1000, tz=UTC)``.
_DATETIME_MIN_MS = int(
    datetime.datetime(1, 1, 1, tzinfo=datetime.timezone.utc).timestamp() * 1000
)
_DATETIME_MAX_MS = int(
    datetime.datetime(
        9999, 12, 31, 23, 59, 59, 999_000, tzinfo=datetime.timezone.utc
    ).timestamp()
    * 1000
)


def _extract_iceberg_as_of_timestamp(
    options: dict[str, str],
) -> datetime.datetime | None:
    """Pull the Spark Iceberg ``as-of-timestamp`` option out of a read
    options dict and convert it to a tz-aware UTC ``datetime``.

    The Spark Iceberg DataFrame reader contract is::

        spark.read.format("iceberg") \\
            .option("as-of-timestamp", <milliseconds-since-epoch>) \\
            .load("path/to/table")

    where the value is a 64-bit integer count of milliseconds since the
    Unix epoch (see https://iceberg.apache.org/docs/latest/spark-queries/
    "Time travel"). We convert to a tz-aware UTC ``datetime`` here so the
    downstream Snowpark ``read.option("as-of-timestamp", <dt>).table(...)``
    call emits ``AT(TIMESTAMP => TO_TIMESTAMP_TZ('...'))`` — i.e. an
    absolute, UTC-anchored timestamp that is independent of the
    session's ``TIMEZONE`` parameter.

    Returns ``None`` if neither ``as-of-timestamp`` nor ``as_of_timestamp``
    (case-insensitive) is set. Raises ``AnalysisException`` with
    ``INVALID_INPUT`` when:

    * the value is not a 64-bit integer (Iceberg's contract),
    * the value falls outside the INT64 range,
    * or the resulting timestamp falls outside Python's
      ``datetime`` representable range (year < 1 or > 9999).

    If a caller somehow supplies *both* the dashed and underscored variants
    with different values, the dashed form wins. This matches Spark
    Iceberg's preferred spelling and is consistent with how we resolve
    ``snapshot-id``; the resolution order is not part of the public
    contract.

    Iceberg's DataFrame-form alias ``timestampAsOf`` is handled upstream
    by ``_resolve_iceberg_dataframe_as_of_aliases``, which converts
    string and numeric values alike into the canonical
    millis-since-epoch form before this extractor runs.
    """
    # One-pass lowercase normalization, then dashed-preferred lookup.
    # If both keys are present and dictionary iteration order surfaces
    # both into ``normalized``, the explicit ``or`` chain below ensures
    # the dashed form wins regardless of insertion order.
    normalized = {k.lower(): v for k, v in options.items()}
    raw = normalized.get("as-of-timestamp")
    if raw is None:
        raw = normalized.get("as_of_timestamp")
    if raw is None:
        return None
    try:
        millis = int(raw)
    except (TypeError, ValueError):
        exception = AnalysisException(
            "Iceberg 'as-of-timestamp' option must be a 64-bit integer "
            f"count of milliseconds since the Unix epoch, got {raw!r}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if not _INT64_MIN <= millis <= _INT64_MAX:
        exception = AnalysisException(
            "Iceberg 'as-of-timestamp' option must fit in a 64-bit signed "
            f"integer (range [{_INT64_MIN}, {_INT64_MAX}]); got {millis}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if not _DATETIME_MIN_MS <= millis <= _DATETIME_MAX_MS:
        exception = AnalysisException(
            "Iceberg 'as-of-timestamp' option resolves to a timestamp "
            "outside the representable datetime range (year 1..9999); "
            f"got {millis} ms since epoch."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return datetime.datetime.fromtimestamp(millis / 1000.0, tz=datetime.timezone.utc)


def _extract_iceberg_snapshot_id(options: dict[str, str]) -> int | None:
    """Pull the Spark Iceberg ``snapshot-id`` option out of a read options dict.

    Returns the parsed ``int`` snapshot id, or ``None`` if neither
    ``snapshot-id`` nor ``snapshot_id`` (case-insensitive) is present.
    Raises ``AnalysisException`` (with INVALID_INPUT) when the value cannot
    be parsed as a 64-bit integer — matches Spark Iceberg, where
    ``option("snapshot-id", "not-a-number")`` fails fast.

    Out-of-range values (``|N| > 2**63 - 1``) are also rejected here so we
    fail fast on the SCOS boundary rather than letting the value flow into
    Snowpark and surface as a less-actionable SQL compile error.

    Iceberg's DataFrame-form alias ``versionAsOf`` (numeric value) is
    handled upstream by ``_resolve_iceberg_dataframe_as_of_aliases``,
    which rewrites it into ``snapshot-id`` before this extractor runs.
    """
    raw: str | None = None
    for key in ("snapshot-id", "snapshot_id"):
        for k, v in options.items():
            if k.lower() == key:
                raw = v
                break
        if raw is not None:
            break
    if raw is None:
        return None
    try:
        snapshot_id = int(raw)
    except (TypeError, ValueError):
        exception = AnalysisException(
            f"Iceberg 'snapshot-id' option must be a 64-bit integer snapshot id, got {raw!r}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if not _INT64_MIN <= snapshot_id <= _INT64_MAX:
        exception = AnalysisException(
            "Iceberg 'snapshot-id' option must fit in a 64-bit signed integer "
            f"(range [{_INT64_MIN}, {_INT64_MAX}]); got {snapshot_id}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return snapshot_id


def _extract_iceberg_incremental_snapshot_ids(
    options: dict[str, str],
) -> tuple[int | None, int | None]:
    """Pull Spark Iceberg incremental-read options from a read options dict.

    Returns ``(start_snapshot_id, end_snapshot_id)`` where each component
    is ``None`` when the corresponding option is absent. Raises
    ``AnalysisException`` (INVALID_INPUT) when a present value cannot be
    parsed as a 64-bit integer, when ``end-snapshot-id`` is supplied
    without ``start-snapshot-id``, or when both dashed and underscored
    variants disagree.
    """
    normalized = {k.lower(): v for k, v in options.items()}

    def _coalesce_snapshot_option(dashed_key: str, underscored_key: str) -> str | None:
        dashed_val = normalized.get(dashed_key)
        underscored_val = normalized.get(underscored_key)
        if (
            dashed_val is not None
            and underscored_val is not None
            and dashed_val != underscored_val
        ):
            exception = AnalysisException(
                f"Iceberg read options '{dashed_key}' and '{underscored_key}' "
                f"disagree: got {dashed_val!r} vs {underscored_val!r}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        return dashed_val if dashed_val is not None else underscored_val

    start_raw = _coalesce_snapshot_option("start-snapshot-id", "start_snapshot_id")
    end_raw = _coalesce_snapshot_option("end-snapshot-id", "end_snapshot_id")

    if start_raw is None and end_raw is None:
        return None, None
    if start_raw is None:
        exception = AnalysisException(
            "Iceberg incremental read requires 'start-snapshot-id'; "
            "'end-snapshot-id' cannot be used alone."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    def _parse_snapshot_id(raw: str, option_name: str) -> int:
        try:
            snapshot_id = int(raw)
        except (TypeError, ValueError):
            exception = AnalysisException(
                f"Iceberg '{option_name}' option must be a 64-bit integer "
                f"snapshot id, got {raw!r}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        if not _INT64_MIN <= snapshot_id <= _INT64_MAX:
            exception = AnalysisException(
                f"Iceberg '{option_name}' option must fit in a 64-bit signed "
                f"integer (range [{_INT64_MIN}, {_INT64_MAX}]); got {snapshot_id}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        return snapshot_id

    start_id = _parse_snapshot_id(start_raw, "start-snapshot-id")
    end_id = (
        _parse_snapshot_id(end_raw, "end-snapshot-id") if end_raw is not None else None
    )
    return start_id, end_id


def _resolve_iceberg_dataframe_as_of_aliases(
    options: dict[str, str],
) -> dict[str, str]:
    """Expand Iceberg's DataFrame-form ``VERSION AS OF`` / ``TIMESTAMP
    AS OF`` aliases (``versionAsOf`` / ``timestampAsOf``) into the
    canonical option keys the rest of the pipeline understands
    (``snapshot-id`` / ``version-ref`` / ``as-of-timestamp``).

    Iceberg's ``SparkReadOptions`` exposes these as a DataFrame-side
    spelling of the SQL time-travel surface (see iceberg/spark/v3.5/
    spark/src/main/java/org/apache/iceberg/spark/SparkReadOptions.java):

        public static final String VERSION_AS_OF = "versionAsOf";
        public static final String TIMESTAMP_AS_OF = "timestampAsOf";

    Both share the SQL surface's value-overloading semantics:

    * ``versionAsOf``: a value that parses as a signed 64-bit integer is
      a snapshot id; anything else is a named ref (tag, branch, or other
      Iceberg ref) routed like SQL ``VERSION AS OF '<name>'`` via
      ``version-ref`` → ``AT(VERSION_REF => ...)``. Same heuristic the
      SQL ``RelationTimeTravel`` resolver uses (see
      ``iceberg_sql_time_travel._resolve_version`` for the rationale and
      the all-digit-ref-name ambiguity).
    * ``timestampAsOf``: a value that parses as a signed 64-bit integer
      is millis-since-epoch (canonical Iceberg wire encoding); anything
      else is a wall-clock string parsed via the same routine the SQL
      path uses (``_parse_timestamp_string_to_millis``).

    Returns a *new* dict with the aliases expanded. Raises
    ``AnalysisException`` (INVALID_INPUT) when an alias conflicts with
    the corresponding canonical option already set by the customer
    (``option("versionAsOf", "v1").option("version-ref", "v2")``) — silently
    picking either side would be the kind of silent fallthrough this
    whole pipeline is designed to prevent.

    The alias lookup is case-insensitive (Spark Connect preserves source
    case, but Iceberg itself canonicalizes to lower case before
    matching).
    """
    # Local import: keeps this module's import cost stable when no
    # customer ever sets ``timestampAsOf``. The SQL-side helper has the
    # right wall-clock-string semantics (session timezone resolution,
    # ISO-with-offset support, ...) so re-implementing it here would
    # only invite a drift bug.
    from snowflake.snowpark_connect.relation.iceberg_sql_time_travel import (
        _parse_timestamp_string_to_millis,
    )

    resolved = dict(options)

    # --- versionAsOf -----------------------------------------------------
    version_as_of_key = next((k for k in resolved if k.lower() == "versionasof"), None)
    if version_as_of_key is not None:
        raw = resolved.pop(version_as_of_key)
        if raw is None or not str(raw).strip():
            exception = AnalysisException(
                "Iceberg 'versionAsOf' option must be a non-empty snapshot "
                f"id or ref name; got {raw!r}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        stripped = str(raw).strip()
        try:
            snapshot_id = int(stripped)
        except (TypeError, ValueError):
            # SNOW-3859177: Previously mapped non-integer versionAsOf to
            # canonical_keys=("tag",) → AT(VERSION_TAG => ...); changed to
            # version-ref → AT(VERSION_REF => ...) for parity with SQL
            # VERSION AS OF string overloading.
            #
            # Non-integer -> named ref (same as SQL VERSION AS OF string).
            # Snowflake ``AT(VERSION_REF => '<name>')`` resolves *both*
            # Iceberg tag and branch names — the unified overload form
            # Spark uses for string ``VERSION AS OF`` / ``versionAsOf``.
            # Explicit ``option("tag", ...)`` / ``option("branch", ...)``
            # remain on ``VERSION_TAG`` / ``BRANCH`` and must not be
            # combined with ``versionAsOf``.
            _named_ref_surface_conflicts = {
                "tag": "use option('tag', ...) alone for VERSION_TAG reads.",
                "branch": "use option('branch', ...) alone for BRANCH reads.",
            }
            for key in resolved:
                kind = key.lower()
                if kind in _named_ref_surface_conflicts:
                    exception = AnalysisException(
                        f"Iceberg 'versionAsOf' option conflicts with "
                        f"'{key}' option set to {resolved[key]!r}. "
                        "'versionAsOf' maps to VERSION_REF time travel; "
                        f"{_named_ref_surface_conflicts[kind]}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
            _inject_alias_value(
                resolved,
                canonical_keys=("version-ref", "version_ref"),
                alias_name="versionAsOf",
                alias_value=stripped,
            )
        else:
            if not _INT64_MIN <= snapshot_id <= _INT64_MAX:
                # Int-parseable but out of int64. Same ambiguity as the
                # SQL ``_resolve_version`` boundary: could be a
                # fat-fingered snapshot id, or an all-digit tag name
                # too large for int64. Surface the ambiguity rather
                # than silently picking either side.
                exception = AnalysisException(
                    "Iceberg 'versionAsOf' option parses as an integer "
                    f"outside the int64 range (got {snapshot_id}). If you "
                    "intended a snapshot id, Iceberg snapshot ids must fit "
                    f"in a 64-bit signed integer (range [{_INT64_MIN}, "
                    f"{_INT64_MAX}]). If you intended a tag name that "
                    'happens to be all digits, use option("tag", "<name>") '
                    "so the intent is unambiguous."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception
            _inject_alias_value(
                resolved,
                canonical_keys=("snapshot-id", "snapshot_id"),
                alias_name="versionAsOf",
                alias_value=str(snapshot_id),
            )

    # --- timestampAsOf ---------------------------------------------------
    timestamp_as_of_key = next(
        (k for k in resolved if k.lower() == "timestampasof"), None
    )
    if timestamp_as_of_key is not None:
        raw = resolved.pop(timestamp_as_of_key)
        if raw is None or not str(raw).strip():
            exception = AnalysisException(
                "Iceberg 'timestampAsOf' option must be a non-empty "
                f"millis-since-epoch integer or wall-clock string; got {raw!r}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        stripped = str(raw).strip()
        try:
            millis = int(stripped)
        except (TypeError, ValueError):
            # Wall-clock string. Reuse the SQL path's parser so the two
            # surfaces stay aligned on timezone resolution + accepted
            # formats. Errors from inside the parser bubble up with
            # their own clear INVALID_INPUT message; we don't try to
            # re-wrap them.
            millis = _parse_timestamp_string_to_millis(stripped)
        _inject_alias_value(
            resolved,
            canonical_keys=("as-of-timestamp", "as_of_timestamp"),
            alias_name="timestampAsOf",
            alias_value=str(millis),
        )

    return resolved


def _inject_alias_value(
    options: dict[str, str],
    canonical_keys: tuple[str, ...],
    alias_name: str,
    alias_value: str,
) -> None:
    """Inject the value resolved from an Iceberg alias (``versionAsOf``
    / ``timestampAsOf``) into the canonical option key.

    Conflict policy: if the canonical key is already present with a
    *different* value, reject as ambiguous. If the values agree, the
    alias is silently absorbed (customers occasionally double-spell the
    same intent and we shouldn't punish that).

    The first canonical key in ``canonical_keys`` is used for the
    injection target. Additional canonical keys are checked for
    conflicts but never written — they exist for symmetry with the
    extractors' existing case-insensitive synonym lookup (e.g.
    ``snapshot-id`` / ``snapshot_id``).
    """
    canonical_key = canonical_keys[0]
    # Hoist outside the loop — the set is invariant across iterations,
    # rebuilding it per-key is just churn on a hot path (alias resolution
    # runs on every Iceberg read that uses ``versionAsOf`` or
    # ``timestampAsOf``).
    canonical_keys_lower = {ck.lower() for ck in canonical_keys}
    for key in options:
        if key.lower() in canonical_keys_lower:
            if str(options[key]) != alias_value:
                exception = AnalysisException(
                    f"Iceberg '{alias_name}' option conflicts with "
                    f"'{key}' option set to {options[key]!r}. Specify "
                    "exactly one of the two; they are aliases for the "
                    "same time-travel surface."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception
            return  # already present with the same value
    options[canonical_key] = alias_value


def _extract_iceberg_version_tag(options: dict[str, str]) -> str | None:
    """Pull the Spark Iceberg ``tag`` option out of a read options dict.

    The Spark Iceberg DataFrame reader contract is::

        spark.read.format("iceberg") \\
            .option("tag", "<tag-name>") \\
            .load("path/to/table")

    where ``<tag-name>`` is a named reference to a specific snapshot
    (see https://iceberg.apache.org/docs/latest/spark-queries/
    "Time travel"). Java / Scala customers (and some PySpark users)
    spell the key via Iceberg's canonical constant
    ``org.apache.iceberg.spark.SparkReadOptions.TAG``, which is defined
    as the literal string ``"tag"`` — see iceberg/spark/v3.5/spark/src/
    main/java/org/apache/iceberg/spark/SparkReadOptions.java. Spark
    Connect serializes the resolved string, so
    ``option(SparkReadOptions.TAG, "<name>")`` and
    ``option("tag", "<name>")`` arrive identically here.

    SCOS translates the option to Snowflake's
    ``AT(VERSION_TAG => '<name>')`` clause via Snowpark's
    ``read.option("version_tag", "<name>").table(...)``.

    Lookup is case-insensitive — Spark Connect preserves option keys as
    set by the customer, but Spark Iceberg itself canonicalizes to lower
    case before matching. Both ``tag`` and ``TAG`` (and any mixed case)
    are accepted; the first non-empty value wins regardless of source
    case. Iceberg's option name is a single word with no canonical
    hyphenated alias, so we only normalize on case.

    Returns ``None`` when the option isn't present. Raises
    ``AnalysisException`` (with INVALID_INPUT) when the option is set
    but the value is empty / whitespace — silently dropping such inputs
    would surprise customers by returning rows from the *current*
    snapshot instead of failing fast.

    Iceberg's DataFrame-form alias ``versionAsOf`` (non-numeric value)
    is handled upstream by ``_resolve_iceberg_dataframe_as_of_aliases``,
    which rewrites it into ``version-ref`` before this extractor runs.
    """
    raw: str | None = None
    for k, v in options.items():
        if k.lower() == "tag":
            raw = v
            break
    if raw is None:
        return None
    # Coerce to ``str`` so a caller passing an already-stringified option
    # (e.g. when SCOS itself constructs the option dict from a SQL
    # ``RelationTimeTravel`` rewrite) takes the same code path as a
    # customer-supplied option from the DataFrame reader.
    tag = str(raw)
    stripped = tag.strip()
    if not stripped:
        exception = AnalysisException(
            "Iceberg 'tag' option must be a non-empty tag name; got an empty "
            "or whitespace-only string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    # Return the stripped value so the DataFrame path
    # (``option("tag", "  release_v1  ")``) and the SQL path
    # (``VERSION AS OF 'release_v1'`` — ``iceberg_sql_time_travel.
    # _resolve_version`` already strips internally) converge on the
    # same tag identifier when downstream code emits
    # ``AT(VERSION_TAG => '...')``. Without this, the two surfaces
    # would round-trip differently for whitespace-padded values, and
    # the SQL-vs-DataFrame convergence assertion in
    # ``tests/sas_tests/test_iceberg_version_tag_sample.py`` would
    # mask a real divergence on any tag name that happened to be
    # padded by an upstream serializer.
    return stripped


def _extract_iceberg_version_ref(options: dict[str, str]) -> str | None:
    """Pull the SQL ``VERSION AS OF '<name>'`` ref out of a read options dict.

    Only the SQL rewrite path (``map_sql`` → ``RelationTimeTravel``) injects
    the ``version-ref`` key. Explicit DataFrame ``option("tag", ...)`` and
    ``option("branch", ...)`` use their own keys and Snowflake clauses
    (``VERSION_TAG`` / ``BRANCH``).

    SCOS translates this option to Snowflake's unified named-ref form via
    Snowpark's ``read.option("version_ref", "<name>").table(...)``, which
    emits ``AT(VERSION_REF => '<name>')``.
    """
    raw: str | None = None
    for k, v in options.items():
        if k.lower() in ("version-ref", "version_ref"):
            raw = v
            break
    if raw is None:
        return None
    ref = str(raw).strip()
    if not ref:
        exception = AnalysisException(
            "Iceberg 'version-ref' option must be a non-empty ref name; got "
            "an empty or whitespace-only string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return ref


def _extract_iceberg_branch(options: dict[str, str]) -> str | None:
    """Pull the Spark Iceberg ``branch`` option out of a read options dict.

      Spark Iceberg WAP branch reads use::

          spark.read.format("iceberg")
              .option("branch", "audit-branch")
              .load("path/to/table")

    SCOS translates the option to Snowflake ``AT(BRANCH => '<name>')``
    via Snowpark's ``read.option("branch", "<name>").table(...)``.
    """
    raw: str | None = None
    for k, v in options.items():
        if k.lower() == "branch":
            raw = v
            break
    if raw is None:
        return None
    branch = str(raw).strip()
    if not branch:
        exception = AnalysisException(
            "Iceberg 'branch' option must be a non-empty branch name; got an "
            "empty or whitespace-only string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return branch


def _iceberg_branch_read_extensions_disabled_exception() -> AnalysisException:
    """Build the error when branch reads are requested without Iceberg extensions."""
    exception = AnalysisException(
        "Iceberg branch reads (via option('branch', ...) or the session config "
        "'spark.wap.branch') are gated on the 'spark.sql.extensions' config "
        "naming the Iceberg Spark SQL extensions class. SCOS implements branch "
        "time travel natively (no extra JAR install is required), but the "
        "customer-visible support contract still requires the flag so "
        "Snowpark Connect can distinguish Iceberg WAP branch reads from "
        "ordinary table reads. Set 'spark.sql.extensions' to "
        "'org.apache.iceberg.spark.extensions."
        "IcebergSparkSessionExtensions' (session override via spark.conf.set "
        "is supported for this key)."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def _require_iceberg_sql_extensions_for_branch_read() -> None:
    if not is_iceberg_sql_extensions_enabled():
        raise _iceberg_branch_read_extensions_disabled_exception()


def _get_spark_wap_branch() -> str | None:
    """Return the session ``spark.wap.branch`` value when set."""
    session_config = sessions_config[get_spark_session_id()]
    raw = session_config.get(WAP_BRANCH_SPARK_CONFIG) or global_config.get(
        WAP_BRANCH_SPARK_CONFIG
    )
    if raw is None:
        return None
    branch = str(raw).strip()
    return branch or None


def _resolve_iceberg_branch(
    options: dict[str, str],
    *,
    skip_session_wap_fallback: bool = False,
) -> str | None:
    """Resolve the Iceberg branch for a read.

    Per-option ``branch`` wins; otherwise fall back to the Spark session config
    ``spark.wap.branch`` (Iceberg WAP audit-branch pattern) unless the read
    already carries another explicit time-travel option (snapshot / timestamp /
    tag / incremental).
    """
    explicit_branch = _extract_iceberg_branch(options)
    if explicit_branch is not None:
        _require_iceberg_sql_extensions_for_branch_read()
        return explicit_branch
    if skip_session_wap_fallback:
        return None
    branch = _get_spark_wap_branch()
    if branch is not None:
        _require_iceberg_sql_extensions_for_branch_read()
    return branch


def get_table_from_name(
    table_name: str,
    session: snowpark.Session,
    plan_id: int,
    iceberg_snapshot_id: int | None = None,
    iceberg_as_of_timestamp: datetime.datetime | None = None,
    iceberg_version_tag: str | None = None,
    iceberg_version_ref: str | None = None,
    iceberg_start_snapshot_id: int | None = None,
    iceberg_end_snapshot_id: int | None = None,
    iceberg_branch: str | None = None,
) -> DataFrameContainer:
    """Resolve a Spark table identifier to a Snowpark DataFrame container.

    Identifier transformation is driven by the session-level CLD hint
    (`_current_cld_context`), so every part of the name follows the same
    CLD rules regardless of whether the identifier is 1-, 2-, or 3-part.

    When ``iceberg_snapshot_id`` is set, the table is read at the requested
    Iceberg snapshot via Snowpark's ``read.option("snapshot-id", N).table(...)``
    surface, which emits Snowflake ``AT(VERSION => N)``. If the server-side
    ``FEATURE_ICEBERG_TIME_TRAVEL`` parameter is off, Snowflake fails the
    compile naturally — no client-side gate.

    When ``iceberg_as_of_timestamp`` is set, the table is read at the
    requested wall-clock moment via Snowpark's
    ``read.option("as-of-timestamp", <datetime>).table(...)`` surface,
    which emits ``AT(TIMESTAMP => TO_TIMESTAMP_TZ('...'))``. For unmanaged
    Iceberg tables the catalog operator must opt the table into
    snapshot-metadata-based timestamp resolution with::

        ALTER ICEBERG TABLE <t> SET TIME_TRAVEL_TIMESTAMP_SOURCE = 'ICEBERG_METADATA';

    Without that, Snowflake falls back to its query-history-based time
    travel and the timestamp won't track Iceberg snapshot commit times.

    When ``iceberg_version_tag`` is set, the table is read at the snapshot
    referenced by an explicit Iceberg tag via Snowpark's
    ``read.option("version_tag", ...).table(...)`` surface, which emits
    ``AT(VERSION_TAG => '<name>')``.

    When ``iceberg_branch`` is set, the table is read at a WAP branch via
    Snowpark's ``read.option("branch", ...).table(...)`` surface, which
    emits ``AT(BRANCH => '<name>')``.

    When ``iceberg_version_ref`` is set (SQL ``VERSION AS OF '<name>'`` or
    DataFrame ``option("versionAsOf", "<name>")`` for non-integer values),
    the named ref is emitted via ``read.option("version_ref", ...)``, which
    maps to ``AT(VERSION_REF => '<name>')``. Integer ``VERSION AS OF N`` /
    ``versionAsOf`` values use ``iceberg_snapshot_id`` → ``AT(VERSION => N)``.

    The time-travel inputs are mutually exclusive — Spark Iceberg
    rejects any combination at plan time, and so do we, with a clear
    pointer to the single supported shape per read.

    Incremental read (``start-snapshot-id`` / ``end-snapshot-id``) is
    also mutually exclusive with the three time-travel inputs. It routes
    to Snowpark's ``CHANGES (INFORMATION => APPEND_ONLY) AT (VERSION =>
    ...) [END (VERSION => ...)]`` surface.
    """

    # Verify if recursive view read is not attempted
    if table_name in get_processed_views():
        exception = AnalysisException(
            f"[RECURSIVE_VIEW] Recursive view `{table_name}` detected (cycle: `{table_name}` -> `{table_name}`)"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception

    # Reject any combination of the three time-travel inputs together.
    # We do this as a single check (rather than three pairwise checks)
    # so the customer-visible message lists *all* the conflicting
    # options at once. Spark Iceberg rejects every combination
    # equivalently, so there's no precedence we need to preserve.
    time_travel_inputs = {
        "snapshot-id": iceberg_snapshot_id,
        "as-of-timestamp": iceberg_as_of_timestamp,
        "tag": iceberg_version_tag,
        "version-ref": iceberg_version_ref,
        "branch": iceberg_branch,
    }
    incremental_inputs = {
        "start-snapshot-id": iceberg_start_snapshot_id,
        "end-snapshot-id": iceberg_end_snapshot_id,
    }
    set_time_travel = [k for k, v in time_travel_inputs.items() if v is not None]
    set_incremental = [k for k, v in incremental_inputs.items() if v is not None]
    if len(set_time_travel) > 1:
        exception = AnalysisException(
            "Cannot specify multiple Iceberg time-travel options on the "
            f"same read; got {set_time_travel!r}. Choose one: 'snapshot-id' "
            "for a specific snapshot id, 'as-of-timestamp' for the "
            "snapshot current at a given wall-clock time, 'tag' for a "
            "named Iceberg tag, 'version-ref' for SQL VERSION AS OF "
            "string refs, or 'branch' for a WAP branch read."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if set_incremental and set_time_travel:
        exception = AnalysisException(
            "Cannot combine Iceberg incremental read options "
            f"({set_incremental!r}) with time-travel options "
            f"({set_time_travel!r}) on the same read."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if (
        "end-snapshot-id" in set_incremental
        and "start-snapshot-id" not in set_incremental
    ):
        # map_read_table validates options via _extract_iceberg_incremental_snapshot_ids
        # first; this guard covers direct get_table_from_name callers that pass parsed
        # iceberg_*_snapshot_id kwargs without going through option extraction.
        exception = AnalysisException(
            "Iceberg incremental read requires 'start-snapshot-id'; "
            "'end-snapshot-id' cannot be used alone."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Split the table name into parts and capture per-part backtick flags so
    # that `transform_identifier_for_snowflake` gets the right hint per part
    # without needing a request-global name-only lookup. The parts list itself
    # is identical to what `split_fully_qualified_spark_name` returns.
    parts, backtick_flags = split_fully_qualified_spark_name_with_quoting(table_name)

    base_table_parts, metadata_table_name = _split_iceberg_metadata_table_name(parts)
    if metadata_table_name is not None:
        # SNOW-3471788: time travel options (snapshot-id, as-of-timestamp,
        # tag, version-ref, branch, start/end-snapshot-id) are silently
        # ignored on metadata tables
        # — matching OSS Spark+Iceberg behaviour. Metadata tables always reflect
        # current state. Previous behaviour raised AnalysisException; callers
        # relying on that error will no longer receive it.
        return _read_iceberg_metadata_table(
            table_name,
            base_table_parts,
            backtick_flags[: len(base_table_parts)],
            metadata_table_name,
            session,
            plan_id,
        )

    # Check temp view first with quoted (but not uppercased) name
    # to preserve original behavior - temp views are stored with quoted names
    quoted_parts = [quote_name_without_upper_casing(part) for part in parts]
    quoted_name = ".".join(quoted_parts)

    temp_view = get_temp_view(quoted_name)
    if temp_view:
        if iceberg_snapshot_id is not None:
            exception = AnalysisException(
                "Iceberg snapshot-id time travel is not supported on temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if iceberg_as_of_timestamp is not None:
            exception = AnalysisException(
                "Iceberg as-of-timestamp time travel is not supported on "
                "temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if iceberg_version_tag is not None:
            exception = AnalysisException(
                "Iceberg tag time travel is not supported on temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if iceberg_version_ref is not None:
            exception = AnalysisException(
                "Iceberg version-ref time travel is not supported on "
                "temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if iceberg_branch is not None:
            exception = AnalysisException(
                "Iceberg branch time travel is not supported on temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        if iceberg_start_snapshot_id is not None or iceberg_end_snapshot_id is not None:
            exception = AnalysisException(
                "Iceberg incremental read is not supported on temporary views."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        return _get_temporary_view(temp_view, table_name, plan_id)

    # SCOS pins a session to a single Snowflake database; CLD-ness is therefore
    # a session-level property carried in `_current_cld_context` (set on session
    # attach). All parts of the table identifier — regardless of 1/2/3-part
    # shape, including Iceberg's `schema.table.metadata_table` form — read the
    # same hint via `transform_identifier_for_snowflake`. See `_spark_to_snowflake`
    # in map_sql.py for the full rationale.
    transformed_parts = [
        transform_identifier_for_snowflake(part, is_backtick_quoted=flag)
        for part, flag in zip(parts, backtick_flags)
    ]
    snowpark_name = ".".join(transformed_parts)

    if iceberg_snapshot_id is not None:
        df = session.read.option("snapshot-id", iceberg_snapshot_id).table(
            snowpark_name
        )
    elif iceberg_as_of_timestamp is not None:
        df = session.read.option("as-of-timestamp", iceberg_as_of_timestamp).table(
            snowpark_name
        )
    elif iceberg_branch is not None:
        df = session.read.option("branch", iceberg_branch).table(snowpark_name)
    elif iceberg_start_snapshot_id is not None:
        from snowflake.snowpark_connect.utils.cld_context import is_in_cld_context

        if is_in_cld_context():
            # CHANGES (incremental/changelog) is managed-only; CLD rejects it
            # (091947). A MINUS version-diff isn't faithful to append-only
            # semantics, so raise rather than approximate.
            exception = AnalysisException(
                "Iceberg incremental and changelog reads "
                "('start-snapshot-id' / 'end-snapshot-id') are not supported "
                "on catalog-linked databases."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        reader = session.read.option("start-snapshot-id", iceberg_start_snapshot_id)
        if iceberg_end_snapshot_id is not None:
            reader = reader.option("end-snapshot-id", iceberg_end_snapshot_id)
        df = reader.table(snowpark_name)
    elif iceberg_version_tag is not None:
        df = session.read.option("version_tag", iceberg_version_tag).table(
            snowpark_name
        )
    elif iceberg_version_ref is not None:
        df = session.read.option("version_ref", iceberg_version_ref).table(
            snowpark_name
        )
    else:
        df = session.read.table(snowpark_name)
    return post_process_df(df, plan_id, table_name)


def get_table_from_query(
    query: str, session: snowpark.Session, plan_id: int
) -> snowpark.DataFrame:
    # Strip trailing semicolons from user-provided SQL to match Spark behavior.
    # When SCOS wraps the query in SELECT ... FROM (user_sql), trailing semicolons
    # cause syntax errors. See SNOW-3201788.
    query = query.rstrip().rstrip(";")
    df = session.sql(query)
    return post_process_df(df, plan_id)


def map_read_table(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Read a table into a Snowpark DataFrame.

    Supports CLD-aware identifier transformation by detecting backtick-quoted identifiers
    and marking them for special handling.
    """
    session: snowpark.Session = _get_current_snowpark_session()
    iceberg_snapshot_id: int | None = None
    iceberg_as_of_timestamp: datetime.datetime | None = None
    iceberg_version_tag: str | None = None
    iceberg_version_ref: str | None = None
    iceberg_start_snapshot_id: int | None = None
    iceberg_end_snapshot_id: int | None = None
    iceberg_branch: str | None = None
    if rel.read.HasField("named_table"):
        # ``spark.read.table("t")`` can carry per-read ``option()`` values on
        # the named-table Connect path (see PySpark ``Read`` plan). Iceberg
        # WAP branch reads still use ``read.format("iceberg").load(...)``.
        table_identifier = rel.read.named_table.unparsed_identifier
        # No need to track backtick state in any side channel: the per-part
        # backtick flags are intrinsic to `table_identifier` itself and get
        # derived directly inside `get_table_from_name` via
        # `split_fully_qualified_spark_name_with_quoting`. Pure per-call
        # data flow, no request-global state.
        if is_backtick_quoted(table_identifier):
            logger.debug(
                "Backtick-quoted identifier detected in spark.table(): %s",
                table_identifier,
            )
    elif (
        rel.read.data_source.HasField("format")
        and rel.read.data_source.format.lower() == "iceberg"
    ):
        if len(rel.read.data_source.paths) != 1:
            exception = SnowparkConnectNotImplementedError(
                f"Unexpected paths: {rel.read.data_source.paths}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        table_identifier = rel.read.data_source.paths[0]
        options = dict(rel.read.data_source.options)
        # Iceberg's ``SparkReadOptions`` exposes ``versionAsOf`` /
        # ``timestampAsOf`` as DataFrame-form spellings of the SQL
        # ``VERSION AS OF`` / ``TIMESTAMP AS OF`` surface. Expand them
        # into the canonical option keys before the three extractors
        # run so the rest of the pipeline never has to know about the
        # alias spellings.
        options = _resolve_iceberg_dataframe_as_of_aliases(options)
        iceberg_snapshot_id = _extract_iceberg_snapshot_id(options)
        iceberg_as_of_timestamp = _extract_iceberg_as_of_timestamp(options)
        iceberg_version_tag = _extract_iceberg_version_tag(options)
        iceberg_version_ref = _extract_iceberg_version_ref(options)
        (
            iceberg_start_snapshot_id,
            iceberg_end_snapshot_id,
        ) = _extract_iceberg_incremental_snapshot_ids(options)
        has_explicit_time_travel = any(
            value is not None
            for value in (
                iceberg_snapshot_id,
                iceberg_as_of_timestamp,
                iceberg_version_tag,
                iceberg_version_ref,
                iceberg_start_snapshot_id,
                iceberg_end_snapshot_id,
            )
        )
        iceberg_branch = _resolve_iceberg_branch(
            options,
            skip_session_wap_fallback=has_explicit_time_travel,
        )
    else:
        exception = ValueError("The relation must have a table identifier.")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return get_table_from_name(
        table_identifier,
        session,
        rel.common.plan_id,
        iceberg_snapshot_id=iceberg_snapshot_id,
        iceberg_as_of_timestamp=iceberg_as_of_timestamp,
        iceberg_version_tag=iceberg_version_tag,
        iceberg_version_ref=iceberg_version_ref,
        iceberg_start_snapshot_id=iceberg_start_snapshot_id,
        iceberg_end_snapshot_id=iceberg_end_snapshot_id,
        iceberg_branch=iceberg_branch,
    )
