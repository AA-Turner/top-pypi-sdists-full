#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import logging
import os
import warnings
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException, IllegalArgumentException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    random_name_for_temp_object,
)
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    IntegerType,
    LongType,
    MapType,
    StringType,
    StructField,
    StructType,
    TimestampTimeZone,
    TimestampType,
    _FractionalType,
    _IntegralType,
)
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    get_string_session_config_param,
    str_to_bool,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_unresolved_function import (
    _find_common_type,
)
from snowflake.snowpark_connect.relation.read.map_read import CsvReaderConfig
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _add_partition_columns,
    discover_partition_columns_if_recursive,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
    add_filename_metadata_to_reader,
    get_non_metadata_fields,
    populate_metadata,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    apply_drop_malformed_on_error,
    apply_permissive_on_error,
)
from snowflake.snowpark_connect.relation.read.source_resolution import (
    detach_infer_schema_options,
    generate_stage_path_groups_for_read,
)
from snowflake.snowpark_connect.relation.read.utils import (
    INDEXED_COLUMN_NAME_PATTERN,
    _load_file_with_copy_into,
    apply_metadata_exclusion_pattern,
    copy_stage_target,
    ensure_corrupt_record_metadata_allowed,
    extract_relative_file_path,
    get_spark_column_names_from_snowpark_columns,
    normalized_file_source_column_merge_key,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import (
    _integral_types_conversion_enabled,
    emulate_integral_types,
)
from snowflake.snowpark_connect.utils.context import _normalize as _norm_case
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

logger = logging.getLogger("snowflake_connect_server")


def _get_nan_inf_config(options: "CsvReaderConfig") -> dict[str, str | None]:
    """Return {nanvalue, positiveinf, negativeinf} option values (None when unset).

    SNOW-3245116: Spark's CSV reader lets users name the string tokens that
    should parse as NaN / +Inf / -Inf in float/double columns.
    """
    return {
        k: options.config.get(k) for k in ("nanvalue", "positiveinf", "negativeinf")
    }


def map_read_csv(
    rel: relation_proto.Relation,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: CsvReaderConfig,
    *,
    skip_partition_discovery: bool = False,
) -> DataFrameContainer:
    """
    Read a CSV file into a Snowpark DataFrame.

    We leverage the stage that is already created in the map_read function that
    calls this.
    """
    # SPARK-35912: File sources like CSV can always contain NULL values,
    # so Spark automatically converts non-nullable user schemas to nullable.
    # This is controlled by snowpark.connect.io.validations.mode:
    # - "lenient" (default): preserve original nullable settings
    # - "strict": convert all fields to nullable (Spark behavior)
    # Note: CSV and JSON reads support this config. Parquet may be added in the future.
    io_validations_mode = (
        get_string_session_config_param("snowpark.connect.io.validations.mode")
        .strip()
        .lower()
        or "lenient"
    )

    if schema is not None and io_validations_mode == "strict":
        schema = _make_schema_nullable(schema)

    # Validate lineSep option - must not be empty (SPARK-35912 compatible behavior)
    line_sep = options.config.get("linesep")
    if line_sep is not None and line_sep == "":
        exception = IllegalArgumentException(
            "requirement failed: 'lineSep' cannot be an empty string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for CSV files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        # Read mode before convert_to_snowpark_args() pops it.
        mode = options.config.get("mode", "PERMISSIVE")

        # Deprecated: snowpark.connect.csv.continueOnError → use mode=DROPMALFORMED.
        if get_boolean_session_config_param("snowpark.connect.csv.continueOnError"):
            warnings.warn(
                "snowpark.connect.csv.continueOnError is deprecated. "
                "Use .option('mode', 'DROPMALFORMED') instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            mode = "DROPMALFORMED"

        converted_snowpark_options = options.convert_to_snowpark_args()
        parse_header = str_to_bool(
            str(converted_snowpark_options.get("PARSE_HEADER", "false"))
        )

        # SNOW-3245116: nanValue/positiveInf/negativeInf tokens. The default
        # (fallback) handling adds them to COPY INTO's NULL_IF so exact-match
        # cells load as NULL instead of failing the cast (e.g. DROPMALFORMED,
        # no-schema, or any read that does not take the positional path below).
        # The float-preserving positional CASE WHEN path (when active) strips
        # these tokens back out of its own file-format copy so the raw token
        # reaches the CASE WHEN comparison. NULL_IF must be a tuple: it feeds
        # the cached_file_format hash key.
        nan_inf_config = _get_nan_inf_config(options)
        # Dedupe while preserving order: a user may set the same token for more
        # than one option (e.g. nanValue == positiveInf).
        nan_inf_tokens = list(dict.fromkeys(v for v in nan_inf_config.values() if v))
        if nan_inf_tokens:
            existing_null_if = converted_snowpark_options.get("NULL_IF")
            existing_seq = (
                list(existing_null_if)
                if isinstance(existing_null_if, (list, tuple))
                else ([existing_null_if] if existing_null_if else [])
            )
            converted_snowpark_options["NULL_IF"] = tuple(
                existing_seq + [t for t in nan_inf_tokens if t not in existing_seq]
            )

        # SNOW-3295571: Surface CSV column-count mismatches when the user asks
        # for strict parsing. The default (set by csv_convert_to_snowpark_args)
        # is FALSE so Snowflake silently null-pads / truncates short or long
        # rows. We override it to TRUE only for ``mode=FAILFAST`` — Spark also
        # raises on column-count mismatch in FAILFAST. ``DROPMALFORMED`` is
        # intentionally NOT overridden: Spark with an explicit schema in
        # DROPMALFORMED null-pads short rows / truncates extras (the row is
        # not considered malformed for column count alone) and only drops
        # rows that fail type-cast. Forcing TRUE here would make SCOS drop
        # rows Spark keeps.
        # When INCLUDE_METADATA is active (partitioned reads or metadata
        # populate) we must keep the default FALSE: Snowflake checks the file's
        # column count against the data + metadata column union, so a strict
        # check would report spurious mismatches by design (see SNOW-3554281).
        # KNOWN GAP: this means partitioned / ``populateFileMetadata`` FAILFAST
        # reads still silently null-pad/truncate column-count mismatches —
        # tracked as a Spark-parity gap pending a Snowflake-side fix that lets
        # INCLUDE_METADATA preserve the strict check on data columns only.
        # ``errorOnColumnCountMismatch`` is also a SCOS-specific user option;
        # a deliberate user override survives by skipping this branch when
        # the user passed the option themselves (raw lowercase key in
        # ``options.config``).
        raw_options = rel.read.data_source.options
        partition_columns, partition_types = discover_partition_columns_if_recursive(
            session, paths[0], "csv", skip_partition_discovery=skip_partition_discovery
        )
        needs_populate_metadata = populate_metadata(raw_options)
        use_include_metadata = bool(partition_columns) or needs_populate_metadata
        mode_upper = mode.upper()
        user_set_column_count_check = "errorOnColumnCountMismatch".lower() in {
            k.lower() for k in options.config
        }
        if (
            mode_upper == "FAILFAST"
            and not use_include_metadata
            and not user_set_column_count_check
        ):
            converted_snowpark_options["ERROR_ON_COLUMN_COUNT_MISMATCH"] = True

        csv_file_format_options = _snowflake_csv_file_format_options(
            converted_snowpark_options, parse_header=parse_header
        )

        merge_schema = str_to_bool(str(options.config.get("mergeschema", "false")))

        file_format = cached_file_format(session, "csv", csv_file_format_options)

        snowpark_reader_options = dict()
        snowpark_reader_options["FORMAT_NAME"] = file_format
        snowpark_reader_options["ENFORCE_EXISTING_FILE_FORMAT"] = True
        snowpark_reader_options["INFER_SCHEMA"] = converted_snowpark_options.get(
            "INFER_SCHEMA", False
        )
        snowpark_reader_options[
            "INFER_SCHEMA_OPTIONS"
        ] = converted_snowpark_options.get("INFER_SCHEMA_OPTIONS", {})

        # Always use ON_ERROR=CONTINUE for schema inference so that corrupted
        # records don't abort type detection (SNOW-3308282).
        # Gate behind ENABLE_SCOS_FEATURE until the parameter is available on
        # all deployments.
        enable_scos_feature = getattr(session, "_enable_scos_feature", False)
        if enable_scos_feature:
            snowpark_reader_options["INFER_SCHEMA_OPTIONS"]["ON_ERROR"] = "CONTINUE"

        # Map Spark mode to Snowflake ON_ERROR for COPY INTO (SNOW-3308282).
        # INFER_SCHEMA always uses CONTINUE (PERMISSIVE is not a valid value
        # for INFER_SCHEMA's ON_ERROR). COPY INTO distinguishes the two modes:
        #   PERMISSIVE    → ON_ERROR=PERMISSIVE — null-pads short rows,
        #                   truncates extras, producing a partial load
        #                   (matches Spark's PERMISSIVE semantics).
        #   DROPMALFORMED → ON_ERROR=CONTINUE — file-level errors reject the
        #                   whole file, row-level errors drop the row.
        #   FAILFAST      → no ON_ERROR (Snowflake default aborts on first error).
        # SNOW-3245116 note: DROPMALFORMED is intentionally NOT upgraded for
        # nanValue/positiveInf/negativeInf. A *partial* token (e.g. "223823.NAN"
        # when nanValue="NAN") fails the cast and Spark's full parse drops that
        # row too — verified empirically: real Spark returns collect()==5 for the
        # OSS "nulls, NaNs and Infinity" data, while its count()==8 is only a
        # count-pushdown artifact (count() skips column parsing). SCOS loads via
        # COPY INTO so count() always equals the materialized row count; matching
        # Spark's *parsed* output (drop the row) is the correct behavior.
        if enable_scos_feature:
            mode_upper = mode.upper()
            if mode_upper == "PERMISSIVE":
                apply_permissive_on_error(snowpark_reader_options)
            elif mode_upper == "DROPMALFORMED":
                apply_drop_malformed_on_error(snowpark_reader_options)

        # Use Try_cast to avoid schema inference errors
        if snowpark_reader_options.get("INFER_SCHEMA", False):
            snowpark_reader_options["TRY_CAST"] = True

        apply_metadata_exclusion_pattern(converted_snowpark_options)
        snowpark_reader_options["PATTERN"] = converted_snowpark_options.get(
            "PATTERN", None
        )

        relax_types_to_infer_schema = (
            converted_snowpark_options.pop("relaxtypestoinferschema", False)
            or _integral_types_conversion_enabled
        )
        infer_schema = options._get_config_setting("inferschema")
        enforce_schema = options._get_config_setting("enforceschema")

        # Resolve the Spark ``columnNameOfCorruptRecord`` column up front so the
        # enforceSchema=false header/column-count validation can ignore it: it is
        # a synthetic column never present in the CSV file (SPARK-27873).
        corrupt_record_col = _resolve_corrupt_record_column(options, schema)

        logical_data_schema, needs_positional_dedup_load = _resolve_csv_schemas(
            session=session,
            schema=schema,
            all_paths=paths,
            snowpark_reader_options=snowpark_reader_options,
            parse_header=parse_header,
            infer_schema=infer_schema,
            relax_types_to_infer_schema=relax_types_to_infer_schema,
            partition_columns=partition_columns,
            merge_schema=merge_schema,
            enforce_schema=enforce_schema,
            corrupt_record_col=corrupt_record_col,
            csv_file_format_options=csv_file_format_options,
            # SNOW-3385963: only recover duplicate/empty headers via Spark-style
            # dedup + positional load in PERMISSIVE mode (matches the positional
            # COPY path below). Other modes keep the legacy error behaviour.
            allow_header_dedup=(mode.upper() == "PERMISSIVE"),
        )

        # SNOW-3443841 / SNOW-3348324: _corrupt_record wiring (Spark CSV parity,
        # verified vs PySpark 3.5.3):
        #   * PERMISSIVE -> native COPY INTO INCLUDE_METADATA =>
        #     METADATA$CORRUPT_RECORD. Strip from COPY schema, append to
        #     loading_schema, then reshuffle to user order post-load. Works
        #     for both parse_header=true (header→name match) and =false
        #     (positional match) thanks to SNOW-3348324.
        #   * DROPMALFORMED / FAILFAST -> COPY drops/aborts bad rows; re-add
        #     as ``lit(None)`` post-load (Spark NULLs survivors too).
        # ``original_user_schema`` is snapshotted so the post-load reshuffle
        # can restore the user's column order.
        original_user_schema = schema
        copy_corrupt_record_col: str | None = None
        add_corrupt_record_postload = False
        mode_upper = mode.upper()
        if corrupt_record_col is not None:
            # Lazy patch: extend Snowpark's INCLUDE_METADATA allowlist on first
            # use so an upstream rename surfaces here, not at server startup.
            ensure_corrupt_record_metadata_allowed()
            target_key = _norm_case(corrupt_record_col)
            # Snowpark wraps quoted names as ``'"foo"'``; unquote before
            # the case-folded compare (mirrors partition-strip below).
            logical_data_schema = StructType(
                [
                    f
                    for f in logical_data_schema.fields
                    if _norm_case(unquote_if_quoted(f.name)) != target_key
                ]
            )
            if mode_upper == "PERMISSIVE":
                copy_corrupt_record_col = corrupt_record_col
            else:
                # DROPMALFORMED / FAILFAST: COPY drops/aborts bad rows;
                # re-add NULL post-load to match Spark's output shape.
                add_corrupt_record_postload = True
        csv_copy_file_format_options = copy.copy(csv_file_format_options)

        # SNOW-3216131 sub-fix 2: when the user supplies an explicit schema and
        # PARSE_HEADER=TRUE, force *positional* COPY semantics. Spark's CSV
        # reader uses the user schema's positions (not its names) when an
        # explicit schema is provided, but Snowflake's PARSE_HEADER + default
        # MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE matches by name -- which
        # silently produces wrong data (or COLUMN_NOT_FOUND) when the user's
        # schema names differ from the file header. The fix: switch the COPY
        # file format to PARSE_HEADER=FALSE + SKIP_HEADER=1 (consume the
        # header line as bytes, do not extract column names from it) and
        # supply explicit positional transformations (``$1::T1, $2::T2, ...``)
        # so each file column is loaded into the user's schema position.
        #
        # Initial scope is intentionally narrow to avoid known interactions
        # we have not yet verified end-to-end:
        # - Out: non-PERMISSIVE modes (``DROPMALFORMED`` / ``FAILFAST``).
        #   ``ON_ERROR=CONTINUE`` interacts with positional ``$N`` casts in
        #   ways that drop rows the existing path keeps; needs separate
        #   investigation before broadening.
        positional_target_columns: list[str] | None = None
        positional_transformations: list[Any] | None = None
        # Track whether the positional path is being used in
        # corrupt-record-capture mode so the COPY ON_ERROR override below
        # can force PERMISSIVE — see the comment block on
        # ``_build_positional_csv_transforms(use_copy_cast=...)``.
        positional_use_copy_cast = False
        # SNOW-3216131 sub-fix 2 scope: positional COPY only runs in
        # PERMISSIVE mode.  DROPMALFORMED and FAILFAST keep the legacy
        # ``PARSE_HEADER=TRUE`` / ``MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE``
        # path because the per-mode ``ON_ERROR`` mapping for the positional
        # path hasn't been validated end-to-end (DROPMALFORMED requires
        # ``ON_ERROR=CONTINUE``, FAILFAST relies on the default fail-fast
        # behaviour, and the ON_ERROR=PERMISSIVE override below is needed
        # for the corrupt-record-capture case).  Known D2 compatibility
        # gap: explicit-schema reads with ``header=true`` in non-PERMISSIVE
        # modes can still silently misalign data on column-name mismatch
        # (the legacy MBCN path matches by name, so renamed columns won't
        # error the way Spark does).  Tracked as a follow-up — broaden the
        # gate (with separate ``ON_ERROR`` per mode) once we have parity
        # tests for DROPMALFORMED / FAILFAST positional reads.
        #
        # SNOW-3385963: the same positional COPY path also serves the
        # duplicate/empty-header dedup case (``needs_positional_dedup_load``).
        # There ``logical_data_schema`` already holds the Spark-deduplicated
        # all-StringType names (``a0,b,a2`` / ``_c{i}``) and there is no user
        # schema, so the transforms map ``$1::STRING AS "a0", ...`` and the
        # physical header (still ``a,b,a``) is consumed as bytes via
        # PARSE_HEADER=FALSE / SKIP_HEADER=1 — MATCH_BY_COLUMN_NAME cannot be
        # used because the deduped names no longer match the file header.
        if (
            (original_user_schema is not None or needs_positional_dedup_load)
            and parse_header
            and mode_upper == "PERMISSIVE"
        ):
            # SCOS partitioned CSV writes embed the partition column in the
            # *file body* (in addition to the directory path), so the file
            # has more columns than ``logical_data_schema`` (which has them
            # stripped).  Map each user data field to a non-partition file
            # position by inspecting the file header.  Without this skip,
            # ``$1, $2, ...`` would slide the partition-column slot into a
            # data field and produce silent data corruption.
            positional_file_positions: list[int] | None = None
            if partition_columns:
                positional_file_positions = _file_positions_excluding_partitions(
                    session=session,
                    all_paths=paths,
                    snowpark_reader_options=snowpark_reader_options,
                    partition_columns=partition_columns,
                    user_data_schema=logical_data_schema,
                )
            # When the user asks for a corrupt-record column the positional
            # transforms must NOT use TRY_CAST: TRY_CAST silently null-pads
            # cast failures, which means COPY never flags the row as
            # corrupt and ``METADATA$CORRUPT_RECORD`` always comes back
            # ``NULL``.  Switch to plain ``$N`` / ``TO_*`` casts so failures
            # surface as row-level errors, then force ON_ERROR=PERMISSIVE
            # below so COPY null-pads the failing cell *and* populates
            # ``METADATA$CORRUPT_RECORD`` (mirrors the JSON path's
            # raw-path strategy in ``_generate_json_path_reference``).
            positional_use_copy_cast = copy_corrupt_record_col is not None
            (
                positional_target_columns,
                positional_transformations,
            ) = _build_positional_csv_transforms(
                logical_data_schema,
                date_format=csv_copy_file_format_options.get("DATE_FORMAT", "AUTO"),
                timestamp_format=csv_copy_file_format_options.get(
                    "TIMESTAMP_FORMAT", "AUTO"
                ),
                binary_format=csv_copy_file_format_options.get("BINARY_FORMAT", "HEX"),
                file_positions=positional_file_positions,
                use_copy_cast=positional_use_copy_cast,
                nan_inf_config=nan_inf_config,
            )
            # SNOW-3245116: when the positional path will emit the NaN/Inf
            # CASE WHEN (tokens set and not the corrupt-record copy-cast mode),
            # strip those tokens from this COPY's NULL_IF so the raw token text
            # reaches the CASE WHEN comparison (NULL_IF fires before the SELECT
            # transforms, so a token left in NULL_IF would null the cell first
            # and the CASE WHEN would never match). Non-nan/inf NULL_IF entries
            # (e.g. from nullValue) are preserved.
            if nan_inf_tokens and not positional_use_copy_cast:
                token_set = set(nan_inf_tokens)
                existing = csv_copy_file_format_options.get("NULL_IF", ())
                if isinstance(existing, str):
                    existing = (existing,)
                filtered = tuple(t for t in existing if t not in token_set)
                if filtered:
                    csv_copy_file_format_options["NULL_IF"] = filtered
                elif "NULL_IF" in csv_copy_file_format_options:
                    del csv_copy_file_format_options["NULL_IF"]
            csv_copy_file_format_options["PARSE_HEADER"] = False
            csv_copy_file_format_options["SKIP_HEADER"] = 1

        copy_reader_opts = dict(snowpark_reader_options)
        copy_reader_opts["INFER_SCHEMA"] = False
        copy_reader_opts.pop("TRY_CAST", None)
        copy_reader_opts["FORMAT_NAME"] = cached_file_format(
            session, "csv", csv_copy_file_format_options
        )

        reader = add_filename_metadata_to_reader(
            session.read.options(copy_reader_opts), raw_options
        )

        # SNOW-3308282: COPY INTO with ON_ERROR=PERMISSIVE null-pads short rows,
        # truncates extras, and NULLs individual cells that fail to cast —
        # matching Spark's PERMISSIVE semantics on a *typed* target table. We
        # therefore load directly into a table shaped like ``logical_data_schema``
        # and skip the old STRING-staging + TRY_CAST post-step. This also lets
        # COPY INTO honor ``DATE_FORMAT`` / ``TIMESTAMP_FORMAT`` from the file
        # format during parsing, which ``TRY_CAST`` did not.
        configured_on_error = snowpark_reader_options.get("ON_ERROR")
        on_error = (
            configured_on_error
            if configured_on_error in ("CONTINUE", "PERMISSIVE")
            else None
        )
        # When the positional path is operating in corrupt-record-capture
        # mode it relies on COPY's PERMISSIVE row-error handling to (a)
        # null-pad cast failures and (b) populate ``METADATA$CORRUPT_RECORD``.
        # The upstream ``apply_permissive_on_error`` call is gated on the
        # SCOS feature flag, so on older deployments ``on_error`` may be
        # ``None`` here even though the user picked ``mode=PERMISSIVE``.
        # Force PERMISSIVE in that case — without it, plain (non-TRY_) casts
        # in the transforms would abort the COPY and the corrupt-record
        # column would never see the bad rows.
        if positional_use_copy_cast:
            on_error = "PERMISSIVE"
        temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
        total_files_processed = 0

        for i, (stage_name, stage_files) in enumerate(
            generate_stage_path_groups_for_read(paths)
        ):
            copy_stage, copy_files = copy_stage_target(stage_name, stage_files)
            copy_result = _load_file_with_copy_into(
                reader=reader,
                session=session,
                target=temp_table_name,
                stage_file_paths=copy_files,
                stage=copy_stage,
                schema=logical_data_schema,
                file_format_options=csv_copy_file_format_options,
                file_format="csv",
                on_error=on_error,
                needs_metadata=use_include_metadata,
                corrupt_record_column=copy_corrupt_record_col,
                target_columns=positional_target_columns,
                transformations=positional_transformations,
                table_already_exists=(i > 0),
            )
            for row in copy_result or []:
                rows_loaded = getattr(row, "rows_loaded", 0) or 0
                errors_seen = getattr(row, "errors_seen", 0) or 0
                status = (getattr(row, "status", None) or "").upper()
                # Count a file as processed if Snowflake attempted to load it,
                # even when all rows were rejected. With ON_ERROR=CONTINUE or
                # ON_ERROR=PERMISSIVE a file-level parse error can cause
                # Snowflake to skip every row while still "seeing" the file.
                # An empty file legitimately reports status=LOADED with both
                # counters at zero, so we also honour an explicit LOADED
                # status. Only files that never matched the pattern remain
                # uncounted, which is what the "No data files matched" error
                # below is meant to detect.
                if rows_loaded > 0 or errors_seen > 0 or status == "LOADED":
                    total_files_processed += 1
            if on_error in ("CONTINUE", "PERMISSIVE") and copy_result:
                row = copy_result[0]
                errors_seen = getattr(row, "errors_seen", 0) or 0
                if errors_seen:
                    rows_loaded = getattr(row, "rows_loaded", 0) or 0
                    logger.warning(
                        "CSV read: %s valid rows loaded, %s rows "
                        "skipped due to parse errors. Stage: %s",
                        rows_loaded,
                        errors_seen,
                        copy_stage,
                    )

        if total_files_processed == 0:
            raise AnalysisException(
                "Unable to load CSV files. No data files matched the "
                "specified pattern or all matched files are empty."
            )

        df = session.table(temp_table_name)

        if partition_columns:
            df = _add_partition_columns(df, partition_columns, partition_types)
        if use_include_metadata and not needs_populate_metadata:
            df = df.drop(METADATA_FILENAME_COLUMN)

        if add_corrupt_record_postload:
            # DROPMALFORMED / FAILFAST: COPY already dropped (or aborted on)
            # the bad rows, so the corrupt-record column is uniformly NULL
            # for the surviving good rows -- matches Spark.
            from snowflake.snowpark.functions import lit

            df = df.with_column(
                quote_name_without_upper_casing(corrupt_record_col),
                lit(None).cast(StringType()),
            )

        if original_user_schema is not None and corrupt_record_col is not None:
            # _corrupt_record lands at the end of ``df`` (INCLUDE_METADATA or
            # post-load lit), so reshuffle to the user's positional order.
            # Scoped to the corrupt-record case to avoid the per-read
            # identifier re-resolution cost on the plain path.
            select_names = [f.name for f in original_user_schema.fields]
            # Preserve METADATA$FILENAME when populateFileMetadata is on: it
            # feeds ``input_file_name()`` / the ``_metadata`` struct
            # downstream and would otherwise be dropped by the user-schema
            # projection above.
            if needs_populate_metadata and METADATA_FILENAME_COLUMN in df.columns:
                select_names.append(METADATA_FILENAME_COLUMN)
            df = df.select(*select_names)

        # SNOW-3389610: when the user sets `emptyValue`, rewrite non-NULL ""
        # in string columns to that token. NULL stays NULL. COPY keeps Snowflake's
        # default EMPTY_FIELD_AS_NULL=TRUE (see csv_convert_to_snowpark_args):
        # bare `,,` -> NULL (matches Spark default nullValue=""); quoted `""` ->
        # "" in `df`, then this projection maps it to emptyValue.
        empty_value = options.config.get("emptyvalue")
        if empty_value is not None:
            from snowflake.snowpark.functions import col, lit, when

            empty_str = lit("")
            empty_token = lit(empty_value)
            new_cols = []
            for f in df.schema.fields:
                c = col(f.name)
                if isinstance(f.datatype, StringType):
                    c = (
                        when(c.is_not_null() & (c == empty_str), empty_token)
                        .otherwise(c)
                        .alias(f.name)
                    )
                new_cols.append(c)
            df = df.select(*new_cols)

        # Snowflake only generates synthetic 1-indexed positional names
        # (c1, c2, …) when the CSV is read with neither a user schema nor a
        # header. In every other case the names are user/header chosen and
        # must not be decremented (SNOW-3587964). Partition columns come from
        # the directory path and are excluded too, even on the synthetic path.
        columns_are_synthetic_positional = (
            original_user_schema is None and not parse_header
        )
        spark_column_names = get_spark_column_names_from_snowpark_columns(
            df.columns,
            apply_positional_normalization=columns_are_synthetic_positional,
            skip_names=partition_columns or [],
        )

        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        # COPY INTO already materializes the result into ``temp_table_name``,
        # so a subsequent ``cache_result()`` (triggered by df_cache_map's
        # materialization step) would create a redundant second temp table.
        # Suppress that materialization while still allowing the container to
        # be memoized in df_cache_map — using ``can_be_cached=False`` would
        # short-circuit df_cache_map entirely and cause every downstream
        # access on the same plan_id to re-execute the COPY INTO.
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                relax_csv_types(f.datatype)
                if relax_types_to_infer_schema
                else f.datatype
                for f in df.schema.fields
            ],
        ).without_materialization()


_csv_file_format_allowed_options = {
    "COMPRESSION",
    "RECORD_DELIMITER",
    "FIELD_DELIMITER",
    "MULTI_LINE",
    "FILE_EXTENSION",
    "PARSE_HEADER",
    "SKIP_HEADER",
    "SKIP_BLANK_LINES",
    "DATE_FORMAT",
    "TIME_FORMAT",
    "TIMESTAMP_FORMAT",
    "BINARY_FORMAT",
    "ESCAPE",
    "ESCAPE_UNENCLOSED_FIELD",
    "TRIM_SPACE",
    "FIELD_OPTIONALLY_ENCLOSED_BY",
    "NULL_IF",
    "ERROR_ON_COLUMN_COUNT_MISMATCH",
    "REPLACE_INVALID_CHARACTERS",
    "EMPTY_FIELD_AS_NULL",
    "SKIP_BYTE_ORDER_MARK",
    "ENCODING",
}


def _build_positional_csv_transforms(
    user_schema: StructType,
    *,
    date_format: str = "AUTO",
    timestamp_format: str = "AUTO",
    binary_format: str = "HEX",
    file_positions: list[int] | None = None,
    use_copy_cast: bool = False,
    nan_inf_config: dict[str, str | None] | None = None,
) -> tuple[list[str], list[Any]]:
    """Build positional COPY INTO transformations for CSV reads with explicit schema.

    Returns ``(target_columns, transformations)`` where each transformation
    maps a file column (``$N``) into the user schema's *k*-th field using an
    explicit type cast that honours the caller-supplied format strings.

    By default (``file_positions=None``) field *k* (0-indexed) is fed by
    file column ``${k+1}``.  When ``file_positions`` is supplied, field *k*
    is instead fed by ``${file_positions[k]}`` — used to skip file columns
    that should not feed any user schema field (e.g. partition columns
    that SCOS partitioned writes embed in the file body in addition to the
    directory path).

    SNOW-3216131 sub-fix 2: forces position-based loading (instead of
    Snowflake's default name-based ``MATCH_BY_COLUMN_NAME`` behaviour) so that
    a user schema like ``(x INT, y INT, z INT)`` lines up with file columns
    1, 2, 3 regardless of what the file's header actually says — matching
    Spark's behaviour when an explicit schema is provided.

    ``use_copy_cast`` selects between two strategies for type conversion:

    - ``False`` (default): wrap each ``$N`` in ``TRY_CAST`` (or
      ``TRY_TO_DATE``/``TRY_TO_TIMESTAMP``/``TRY_TO_BINARY`` for those types).
      Cast failures silently produce ``NULL``; matches Spark PERMISSIVE
      semantics without depending on COPY's ``ON_ERROR``.

    - ``True``: pass the raw ``$N`` (or plain ``TO_DATE`` / ``TO_TIMESTAMP``
      / ``TO_BINARY`` for format-sensitive types) and let COPY's implicit
      cast at INSERT time surface the failure.  This requires the caller
      to set ``ON_ERROR=PERMISSIVE`` on the COPY INTO call so cast failures
      become row-level errors that null the failing column **and** populate
      ``METADATA$CORRUPT_RECORD``.  Used when ``copy_corrupt_record_col`` is
      configured: ``TRY_CAST`` would silently null the column and prevent
      Snowflake from ever flagging the row as corrupt, so the
      ``_corrupt_record`` column would always come back ``NULL``.

    Notes:
    - ``$N`` for ``N > file_column_count`` evaluates to NULL, so a user schema
      that is wider than the file produces trailing NULL columns (matches
      Spark's "missing columns are NULL").
    - File columns beyond the schema's width are dropped (matches Spark's
      "extra columns are discarded with explicit schema").
    - Caller must ensure the COPY file format uses ``PARSE_HEADER=FALSE``
      (with ``SKIP_HEADER=1`` if the file has a real header line) so that
      the header row is consumed without being interpreted as data.
    - ``date_format`` / ``timestamp_format`` / ``binary_format`` should be
      the already-converted Snowflake format strings from the COPY file format
      options (e.g. ``"AUTO"``, ``"YYYY-MM-DD"``, ``"DD/MM/YYYY HH24:MI:SS"``).
    """
    from snowflake.snowpark.functions import lit, sql_expr, when

    # SNOW-3245116: when the user named NaN/+Inf/-Inf tokens, float/double
    # columns map those exact tokens to real Snowflake float literals via a
    # CASE WHEN (preserving IEEE-754 NaN/Infinity) instead of letting them
    # null out. Only applied on the TRY_CAST path: the ``use_copy_cast`` path
    # passes raw ``$N`` so COPY can flag corrupt records, and a CASE WHEN there
    # would suppress that signal — those reads fall back to the NULL_IF mapping.
    nan_tok = (nan_inf_config or {}).get("nanvalue")
    pos_tok = (nan_inf_config or {}).get("positiveinf")
    neg_tok = (nan_inf_config or {}).get("negativeinf")
    nan_inf_active = (not use_copy_cast) and any((nan_tok, pos_tok, neg_tok))

    target_columns: list[str] = []
    transformations: list[Any] = []
    for k, field in enumerate(user_schema.fields):
        # ``field.name`` is sometimes already wrapped in double quotes by
        # upstream Snowpark schema handling. Round-trip through
        # ``unquote_if_quoted`` first so we do not double-quote it here
        # (which would produce ``"""x"""`` and trigger an invalid-identifier
        # error in COPY INTO).
        target_columns.append(
            quote_name_without_upper_casing(unquote_if_quoted(field.name))
        )
        # Pick the file column position. ``file_positions`` shorter than the
        # user schema falls back to NULL for the trailing fields (the same
        # Spark "missing columns are NULL" semantics applied to the
        # partition-aware mapping).
        if file_positions is not None and k < len(file_positions):
            file_pos = file_positions[k]
        elif file_positions is not None:
            file_pos = None
        else:
            file_pos = k + 1
        col_ref = f"${file_pos}" if file_pos is not None else "NULL"
        if isinstance(field.datatype, DateType):
            fmt = date_format.replace("'", "''")
            fn = "TO_DATE" if use_copy_cast else "TRY_TO_DATE"
            expr = sql_expr(f"{fn}({col_ref}, '{fmt}')")
        elif isinstance(field.datatype, TimestampType):
            fmt = timestamp_format.replace("'", "''")
            tz = getattr(field.datatype, "tz", None)
            if tz == TimestampTimeZone.NTZ:
                base = "TO_TIMESTAMP_NTZ"
            elif tz == TimestampTimeZone.TZ:
                base = "TO_TIMESTAMP_TZ"
            else:
                base = "TO_TIMESTAMP_LTZ"
            fn = base if use_copy_cast else f"TRY_{base}"
            expr = sql_expr(f"{fn}({col_ref}, '{fmt}')")
        elif isinstance(field.datatype, BinaryType):
            fmt = binary_format.replace("'", "''")
            fn = "TO_BINARY" if use_copy_cast else "TRY_TO_BINARY"
            expr = sql_expr(f"{fn}({col_ref}, '{fmt}')")
        elif use_copy_cast:
            # Pass through the raw ``$N`` value; COPY's implicit cast to the
            # target column type runs under ``ON_ERROR=PERMISSIVE`` and a
            # cast failure both nulls the column and populates
            # ``METADATA$CORRUPT_RECORD``.
            expr = sql_expr(col_ref)
        elif nan_inf_active and isinstance(field.datatype, _FractionalType):
            # SNOW-3245116: map the user-configured NaN/+Inf/-Inf tokens to
            # real Snowflake float literals so isnan()/== float('inf') work and
            # NaN rows survive dropna(); every other value still goes through
            # TRY_CAST (cast failure -> NULL, matching PERMISSIVE).
            ref = sql_expr(col_ref)
            # Cast the special-value literals to the column's own float width.
            # Snowflake FLOAT and DOUBLE are both IEEE-754 64-bit today (so this
            # is currently equivalent to ``::DOUBLE``), but keying off the target
            # type future-proofs against a true 32-bit FLOAT and keeps the literal
            # consistent with the ``TRY_CAST(... AS <type>)`` in ``.otherwise()``.
            sf_type = "DOUBLE" if isinstance(field.datatype, DoubleType) else "FLOAT"
            branches = [
                (nan_tok, f"'NaN'::{sf_type}"),
                (pos_tok, f"'Infinity'::{sf_type}"),
                (neg_tok, f"'-Infinity'::{sf_type}"),
            ]
            expr = None
            for token, sf_literal in branches:
                if not token:
                    continue
                if expr is None:
                    expr = when(ref == lit(token), sql_expr(sf_literal))
                else:
                    expr = expr.when(ref == lit(token), sql_expr(sf_literal))
            # ``expr`` is non-None here because ``nan_inf_active`` guarantees at
            # least one token; fall back defensively just in case.
            expr = (
                expr.otherwise(ref.try_cast(field.datatype, permissive=True))
                if expr is not None
                else ref.try_cast(field.datatype, permissive=True)
            )
        else:
            # Use TRY_CAST so cast failures produce NULL rather than aborting
            # the row -- matches Spark's PERMISSIVE-mode handling on a typed
            # target. Stricter modes (FAILFAST/DROPMALFORMED) are handled
            # upstream via ``ON_ERROR`` and ``ERROR_ON_COLUMN_COUNT_MISMATCH``.
            expr = sql_expr(col_ref).try_cast(field.datatype, permissive=True)
        transformations.append(expr)
    return target_columns, transformations


def _file_positions_excluding_partitions(
    *,
    session: snowpark.Session,
    all_paths: list[str],
    snowpark_reader_options: dict[str, Any],
    partition_columns: list[str],
    user_data_schema: StructType,
) -> list[int]:
    """Map ``user_data_schema`` fields to file column positions, skipping
    file columns that match partition column names.

    SCOS partitioned CSV writes embed the partition column in the file
    body in addition to the directory path, so a positional read against
    a partition-stripped ``user_data_schema`` would slide the partition
    slot into a data field unless we skip it.  This helper inspects the
    file header (via ``INFER_SCHEMA``) and returns the 1-indexed file
    positions of the *non*-partition columns, in file order, capped at
    ``len(user_data_schema.fields)`` so trailing fields without a file
    column fall through to NULL via the caller's normal "missing column"
    handling.

    Returns positions for the user data fields that have a corresponding
    file column.  Caller treats indices beyond this list as missing
    (NULL) — same Spark "missing columns are NULL" semantics.

    Caveats / known limitations:
    - Layout is inferred from the **first file only** for cost (avoid an
      ``INFER_SCHEMA`` round-trip per file).  All files in a partitioned
      read are assumed to share the same column ordering / partition-column
      placement.  This matches Spark's own behaviour for the relevant code
      paths: explicit-schema CSV reads in Spark are strictly positional, so
      files with divergent column orders would silently misalign data in
      Spark too; inferred-schema reads with ``enforceSchema=true`` (the
      default) also derive the schema from the first file and assume the
      rest match.  In practice the assumption also holds for SCOS-written
      partitioned output (the writer emits a single schema per dataset).
    - Partition slots are skipped by **header name** match against
      ``partition_columns``.  In the unlikely case a non-partition data
      column happens to share its name with a partition column (e.g. a
      data column ``year`` alongside a Hive ``year=2020/`` partition),
      that data column would be silently dropped and the remaining data
      fields would shift.  We emit a ``logger.warning`` below when this
      yields fewer non-partition file positions than ``user_data_schema``
      has fields, so the misalignment is at least visible at runtime.
    """
    if not all_paths:
        return []
    inferred = _infer_csv_schema_for_stage_chunk(
        session,
        [all_paths[0]],
        snowpark_reader_options,
        relax_types_to_infer_schema=False,
    )
    partition_set = {_norm_case(unquote_if_quoted(p)) for p in partition_columns}
    non_partition_positions: list[int] = []
    for i, f in enumerate(inferred.fields, start=1):
        if _norm_case(unquote_if_quoted(f.name)) in partition_set:
            continue
        non_partition_positions.append(i)
    positions = non_partition_positions[: len(user_data_schema.fields)]
    if len(positions) < len(user_data_schema.fields):
        # Either the file has fewer columns than the user schema (Spark-style
        # "missing trailing columns are NULL" — expected, not all-cause), or
        # a non-partition data column collided with a partition name and got
        # dropped (the second caveat above — silent shift).  Logging both
        # cases is acceptable: the legitimate case is rare in production
        # writes, and the collision case is precisely what we want surfaced.
        logger.warning(
            "positional CSV read: inferred %d non-partition file positions for "
            "%d user data fields (file=%s, partition_columns=%s, file_header=%s). "
            "Trailing fields will be NULL; if this is unexpected, check whether "
            "a data column shares a name with a partition column.",
            len(positions),
            len(user_data_schema.fields),
            all_paths[0],
            list(partition_columns),
            [f.name for f in inferred.fields],
        )
    return positions


def _snowflake_csv_file_format_options(
    converted_snowpark_options: dict[str, Any],
    *,
    parse_header: bool,
) -> dict[str, Any]:
    """Snowflake CSV ``FILE_FORMAT`` options shared by infer, read, and ``COPY INTO``.

    Copies allowlisted type options from the converted reader config, then sets
    ``SKIP_BLANK_LINES``, ``PARSE_HEADER`` from the logical header flag, and
    ``SKIP_HEADER = 0`` (required when ``PARSE_HEADER`` is true). The same dict is
    used for the cached infer format and for COPY ``format_type_options``.

    SNOW-3295599: ``SKIP_BLANK_LINES`` is configurable. Precedence (highest first):
    1. Per-read user option ``skipBlankLines`` (already translated to
       ``SKIP_BLANK_LINES`` and copied via the allowlist loop below).
    2. Session config ``snowpark.connect.csv.skipBlankLines``.
    3. Default ``True`` (matches Spark's effective behavior — Univocity defaults
       to skipping empty lines and there is no public Spark opt-out).
    """
    opts: dict[str, Any] = {}
    has_user_skip_blank = False
    for key, value in converted_snowpark_options.items():
        upper_key = key.upper()
        if upper_key not in _csv_file_format_allowed_options:
            continue
        if upper_key in ("PARSE_HEADER", "SKIP_HEADER"):
            continue
        opts[upper_key] = value
        if upper_key == "SKIP_BLANK_LINES":
            has_user_skip_blank = True
    if not has_user_skip_blank:
        opts["SKIP_BLANK_LINES"] = get_boolean_session_config_param(
            "snowpark.connect.csv.skipBlankLines"
        )
    opts["PARSE_HEADER"] = parse_header
    opts["SKIP_HEADER"] = 0
    return opts


def _widen_csv_inferred_types(a: DataType, b: DataType) -> DataType:
    """Widen two CSV-inferred scalar types to their common supertype.

    Delegates to :func:`_find_common_type` with ``widen_to_string=True`` so
    that incompatible types fall back to ``StringType`` instead of raising.
    CSV inference only produces flat scalar types so the nested-type branches
    of ``_find_common_type`` are never reached.
    """
    return _find_common_type([a, b], widen_to_string=True)


def _merge_inferred_csv_struct_schemas(
    left: StructType | None, right: StructType
) -> StructType:
    """Union columns across inferred CSV schemas (mergeSchema across stage groups)."""
    if left is None:
        return right
    key_to_field: dict[str, StructField] = {}
    order: list[str] = []
    for sf in left.fields:
        k = normalized_file_source_column_merge_key(sf.name)
        key_to_field[k] = sf
        order.append(k)
    for sf in right.fields:
        k = normalized_file_source_column_merge_key(sf.name)
        if k not in key_to_field:
            key_to_field[k] = sf
            order.append(k)
        else:
            ex = key_to_field[k]
            merged_type = _widen_csv_inferred_types(ex.datatype, sf.datatype)
            key_to_field[k] = StructField(
                ex.name, merged_type, ex.nullable or sf.nullable
            )
    return StructType([key_to_field[k] for k in order])


def _spark_make_safe_header(names: list[str], case_sensitive: bool) -> list[str]:
    """Deduplicate CSV header names the way Spark's ``CSVUtils.makeSafeHeader`` does.

    Matches OSS Spark (verified vs PySpark 3.5.3):

    * an empty cell at position ``i`` becomes ``_c{i}`` (Spark replaces empty /
      ``nullValue`` header cells with positional names);
    * a name that collides with another — case-folded when ``case_sensitive`` is
      false — gets its 0-based position appended, e.g. ``a,b,a -> a0,b,a2`` and
      ``ab,AB -> ab0,AB1`` (caseSensitive=false);
    * every other name is returned unchanged.

    ``case_sensitive`` mirrors ``spark.sql.caseSensitive``.

    Limitation: Spark also treats cells equal to ``options.nullValue`` as empty.
    This implementation only handles the literal empty string (Spark's default
    nullValue).  A custom ``nullValue`` (e.g. ``"NA"``) in the header is not
    replaced with ``_c{i}`` here.  Threading the user's nullValue option through
    to this point is straightforward but out of scope for the initial fix.
    """

    def fold(name: str) -> str:
        return name if case_sensitive else name.lower()

    def is_empty(name: str) -> bool:
        # Spark treats a header cell as missing when it is empty or equals
        # options.nullValue.  We only handle the literal empty string (Spark's
        # default nullValue); custom nullValue is a known limitation (see above).
        return name is None or name == ""

    counts: dict[str, int] = {}
    for name in names:
        if is_empty(name):
            continue
        folded = fold(name)
        counts[folded] = counts.get(folded, 0) + 1
    duplicates = {key for key, count in counts.items() if count > 1}

    safe: list[str] = []
    for i, name in enumerate(names):
        if is_empty(name):
            safe.append(f"_c{i}")
        elif fold(name) in duplicates:
            safe.append(f"{name}{i}")
        else:
            safe.append(name)
    return safe


def _read_csv_header_names_from_stage(
    session: snowpark.Session,
    stage_path: str,
    snowpark_reader_options: dict[str, Any],
    csv_file_format_options: dict[str, Any] | None = None,
    *,
    require_single_line: bool,
) -> list[str] | None:
    """Read a staged CSV file's header row as raw text and return its cells.

    Reads the file with a text FILE_FORMAT (mirroring the user's PATTERN /
    COMPRESSION / RECORD_DELIMITER so it sees the same bytes INFER_SCHEMA saw),
    then parses the first non-empty line with the configured FIELD_DELIMITER /
    FIELD_OPTIONALLY_ENCLOSED_BY. Returns the raw column-name cells — which may
    contain duplicates or empty strings; the caller decides how to handle those
    — or ``None`` if no usable header line is found.

    ``require_single_line`` enforces the header-only contract (exactly one
    non-empty line) used by :func:`_read_header_line_schema_from_stage`. When
    ``False`` (the duplicate/empty-header dedup path, SNOW-3385963) the first
    non-empty line is used even when data rows follow. Parsed cells containing
    NUL bytes or non-printable characters are rejected so binary garbage from a
    COMPRESSION mismatch can't be passed off as a header.
    """
    import csv as _csv
    import io as _io

    from snowflake.snowpark.exceptions import SnowparkSQLException
    from snowflake.snowpark_connect.utils.io_utils import file_format as _ff

    # Prefer values from ``csv_file_format_options`` (the file format we
    # actually built) over ``snowpark_reader_options`` — the latter only
    # carries ``FORMAT_NAME`` / ``PATTERN`` / ``INFER_SCHEMA`` keys, so
    # falling back to it for ``COMPRESSION`` / ``FIELD_DELIMITER`` /
    # ``FIELD_OPTIONALLY_ENCLOSED_BY`` / ``RECORD_DELIMITER`` would silently
    # default the read to "comma + double-quote + uncompressed", which
    # breaks header round-trips for gzip / tab-delimited / unusual quote-char
    # files.
    csv_fmt_opts = csv_file_format_options or {}

    def _opt(key: str, default: Any) -> Any:
        # Fall through: file-format dict (built from user options) → reader
        # options (legacy) → static default.
        if key in csv_fmt_opts and csv_fmt_opts[key] is not None:
            return csv_fmt_opts[key]
        v = snowpark_reader_options.get(key)
        return v if v is not None else default

    # Mirror the user's compression so a gzipped file isn't read as raw bytes.
    user_compression = _opt("COMPRESSION", "none")
    # Mirror the user's record delimiter (default \n) so non-standard line
    # terminators don't split the header into garbage.
    user_record_delimiter = _opt("RECORD_DELIMITER", "\n")
    # Mirror the user's PATTERN so we see the same file set INFER_SCHEMA saw
    # (e.g. when pathGlobFilter restricts the read to specific files).
    user_pattern = snowpark_reader_options.get("PATTERN")

    try:
        text_fmt = _ff(
            session, str(user_compression).lower(), str(user_record_delimiter)
        )
        select_clauses = [f"FILE_FORMAT => {text_fmt}"]
        if user_pattern:
            escaped_pattern = str(user_pattern).replace("'", "''")
            select_clauses.append(f"PATTERN => '{escaped_pattern}'")
        clause_sql = ", ".join(select_clauses)
        rows = session.sql(
            f"SELECT T.$1 AS LINE FROM {stage_path} ({clause_sql}) AS T LIMIT 10"
        ).collect()
    except SnowparkSQLException as exc:
        # Narrow to ``SnowparkSQLException`` so genuine infrastructure errors
        # (auth, network, permissions) propagate instead of being swallowed.
        logger.warning(
            "header text read: could not read %s as text (%s)",
            stage_path,
            exc,
        )
        return None

    non_empty = [row[0] for row in rows if row[0] and row[0].strip()]
    if require_single_line and len(non_empty) != 1:
        # A genuine header-only file has exactly ONE non-empty line. Anything
        # else means INFER_SCHEMA failed for a different reason.
        logger.info(
            "header-only fallback: refusing to fall back for %s "
            "(expected exactly 1 non-empty line, found %d)",
            stage_path,
            len(non_empty),
        )
        return None
    if not non_empty:
        return None
    header_line = non_empty[0]

    # Parse the header using the configured delimiter / quote char.
    delimiter = _opt("FIELD_DELIMITER", ",") or ","
    # Snowflake FIELD_OPTIONALLY_ENCLOSED_BY default is NONE; Spark default quote is '"'.
    quote_char = _opt("FIELD_OPTIONALLY_ENCLOSED_BY", '"') or '"'
    if quote_char.upper() in ("NONE", "\\0"):
        quote_char = ""

    try:
        if quote_char:
            reader = _csv.reader(
                _io.StringIO(header_line), delimiter=delimiter, quotechar=quote_char
            )
        else:
            reader = _csv.reader(
                _io.StringIO(header_line), delimiter=delimiter, quoting=_csv.QUOTE_NONE
            )
        col_names = next(reader)
    except (_csv.Error, StopIteration) as exc:
        # Narrow to the CSV parser's own exceptions: ``_csv.Error`` (malformed
        # quoting, etc.) and ``StopIteration`` (empty iterator). Any other
        # exception type is genuinely unexpected and should propagate.
        logger.warning(
            "header text read: could not parse header line %r (%s)",
            header_line,
            exc,
        )
        return None

    if not col_names:
        return None

    # Reject column names that look like binary garbage — guards against the
    # case where COMPRESSION mismatches and we're really reading raw gzip bytes
    # that happen to have one 0x0a byte and no others.
    for name in col_names:
        if "\x00" in name or any(not (c.isprintable() or c in "\t ") for c in name):
            logger.info(
                "header text read: refusing header for %s "
                "(non-printable bytes in parsed header %r)",
                stage_path,
                col_names,
            )
            return None

    return col_names


def _read_header_line_schema_from_stage(
    session: snowpark.Session,
    stage_path: str,
    snowpark_reader_options: dict[str, Any],
    csv_file_format_options: dict[str, Any] | None = None,
) -> StructType | None:
    """SNOW-3565051: fallback for header-only CSV files that INFER_SCHEMA cannot handle.

    When a staged CSV file has only a header row and no data rows, Snowflake's
    INFER_SCHEMA raises "Given path '...' returned no results from INFER_SCHEMA".
    This helper reads the file as raw text via
    :func:`_read_csv_header_names_from_stage` (requiring exactly one non-empty
    line) and returns a StructType whose columns are all StringType.

    To avoid masking *other* INFER_SCHEMA failures it stays narrow: it requires
    a single non-empty line and refuses blank/whitespace-only header cells
    (Snowflake PARSE_HEADER rejects them; the duplicate/empty-header dedup path
    in :func:`_resolve_deduped_header_schema` handles those instead).

    Returns None on any guard failure so the caller re-raises the original
    INFER_SCHEMA error.
    """
    col_names = _read_csv_header_names_from_stage(
        session,
        stage_path,
        snowpark_reader_options,
        csv_file_format_options=csv_file_format_options,
        require_single_line=True,
    )
    if not col_names:
        return None

    # Reject any blank/whitespace-only header cells.  Snowflake ``PARSE_HEADER``
    # rejects them and Spark would synthesize ``_cN`` placeholders instead —
    # this fallback's contract is "the file looked like a header-only CSV with
    # well-formed column names", so refuse rather than fabricate names that
    # would diverge from both engines' real behaviour.
    if any(not name or not name.strip() for name in col_names):
        logger.info(
            "header-only fallback: refusing to fall back for %s "
            "(blank/whitespace-only header cell in parsed header %r)",
            stage_path,
            col_names,
        )
        return None

    logger.info(
        "header-only fallback: INFER_SCHEMA returned no rows for %s; "
        "using header line with %d column(s): %s",
        stage_path,
        len(col_names),
        col_names,
    )
    # Snowflake INFER_SCHEMA with PARSE_HEADER returns column names as
    # double-quoted identifiers (e.g. '"id"') to preserve the exact case from
    # the header row.  Snowpark Python then stores them as '"id"' in
    # StructField.name, and get_spark_column_names_from_snowpark_columns strips
    # the quotes to give the plain lowercase name ("id").  We must mimic this
    # by wrapping each column name in double quotes so the downstream
    # COPY INTO table schema and the Spark column mapping both see the correct
    # case-preserved identifier.
    return StructType(
        [StructField(f'"{name.strip()}"', StringType(), True) for name in col_names]
    )


def _resolve_deduped_header_schema(
    session: snowpark.Session,
    stage_path: str,
    snowpark_reader_options: dict[str, Any],
    csv_file_format_options: dict[str, Any] | None,
    *,
    case_sensitive: bool,
) -> StructType | None:
    """SNOW-3385963: recover a Spark-deduplicated schema from a CSV header that
    Snowflake INFER_SCHEMA rejects for duplicate or empty column names.

    Snowflake's CSV scanner rejects exact-duplicate (``a,b,a``) and empty
    (``a,,b``) header cells, so INFER_SCHEMA returns no rows. OSS Spark instead
    deduplicates (``a,b,a -> a0,b,a2``) and replaces empty cells with positional
    names (``_c{i}``). This reads the raw header line, applies Spark's
    ``makeSafeHeader`` (:func:`_spark_make_safe_header`), and returns an all-
    ``StringType`` schema with the safe names (quoted to preserve case).

    Returns ``None`` when the header has no duplicate/empty cells — i.e. the
    INFER_SCHEMA failure was for some other reason and the caller should
    re-raise the original error.
    """
    col_names = _read_csv_header_names_from_stage(
        session,
        stage_path,
        snowpark_reader_options,
        csv_file_format_options=csv_file_format_options,
        require_single_line=False,
    )
    if not col_names:
        return None
    safe_names = _spark_make_safe_header(col_names, case_sensitive)
    if safe_names == col_names:
        # No duplicates or empty cells -> not the case this path handles.
        return None
    logger.info(
        "CSV header dedup (SNOW-3385963): %r -> %r for %s",
        col_names,
        safe_names,
        stage_path,
    )
    return StructType(
        [
            StructField(quote_name_without_upper_casing(name), StringType(), True)
            for name in safe_names
        ]
    )


def _infer_csv_schema_for_stage_chunk(
    session: snowpark.Session,
    chunk_paths: list[str],
    snowpark_reader_options: dict[str, Any],
    *,
    relax_types_to_infer_schema: bool,
    csv_file_format_options: dict[str, Any] | None = None,
    names_only: bool = False,
) -> StructType:
    """Run Snowpark CSV ``INFER_SCHEMA`` for one COPY chunk (same stage, ``FILES`` when needed).

    Always forces ``INFER_SCHEMA=True`` regardless of the caller's reader
    options because this function is the schema-discovery step — the user's
    ``inferSchema`` flag only controls whether inferred types are kept or
    coerced to ``StringType`` afterward.

    SNOW-3659505: when ``names_only`` is set (the ``inferSchema=false``
    first-path cases), the caller discards the inferred types, so we only need
    the column names (header) / count (headerless). We therefore cap discovery
    to a single record of a single file (``MAX_RECORDS_PER_FILE=1``,
    ``MAX_FILE_COUNT=1``) instead of the default 20k-record-per-file sample, to
    avoid scanning the whole input just to throw the types away. ``MAX_FILE_COUNT``
    cannot target a specific file, so for heterogeneous header-less inputs the
    chosen file's column count may differ from Spark's strict first-file rule
    (D1); this is only used where Snowflake's own "consistent file structures"
    assumption already holds. If the cap yields nothing — e.g. a leading blank
    line consumes the single-record budget under ``SKIP_BLANK_LINES`` — we fall
    through to the uncapped sample so discovery still succeeds.

    SNOW-3565051: if INFER_SCHEMA raises because the file is header-only (no
    data rows), fall back to reading the first line as raw text and building a
    StringType schema from the header column names.
    """

    def _do_infer(apply_cap: bool) -> StructType:
        infer_opts = copy.copy(snowpark_reader_options)
        infer_opts["INFER_SCHEMA"] = True
        if apply_cap:
            infer_opts["INFER_SCHEMA_OPTIONS"] = {
                **infer_opts.get("INFER_SCHEMA_OPTIONS", {}),
                "MAX_RECORDS_PER_FILE": 1,
                "MAX_FILE_COUNT": 1,
            }
        if len(chunk_paths) == 1:
            # Detach INFER_SCHEMA_OPTIONS so snowpark's in-place ``FILES``
            # resolution cannot leak across per-directory chunks (SNOW-3591574).
            infer_opts = detach_infer_schema_options(infer_opts)
            infer_df = session.read.options(infer_opts).csv(chunk_paths[0])
        else:
            clean_paths = [p.strip("'") for p in chunk_paths]
            common = os.path.commonprefix(clean_paths)
            dir_idx = common.rfind("/")
            if dir_idx >= 0:
                common = common[: dir_idx + 1]
            common_stage_prefix = f"'{common}'"
            relative_files = [
                extract_relative_file_path(path, common_stage_prefix)
                for path in chunk_paths
            ]
            infer_opts = detach_infer_schema_options(infer_opts, files=relative_files)
            infer_df = session.read.options(infer_opts).csv(common_stage_prefix)
        inferred_fields = get_non_metadata_fields(infer_df.schema.fields)
        logical = StructType(
            [StructField(f.name, f.datatype, f.nullable) for f in inferred_fields]
        )
        if relax_types_to_infer_schema:
            logical = relax_csv_types(logical)
        return logical

    if names_only:
        try:
            capped = _do_infer(apply_cap=True)
            if capped.fields:
                return capped
        except Exception:
            pass

    try:
        return _do_infer(apply_cap=False)
    except Exception as infer_exc:
        # SNOW-3565051: INFER_SCHEMA fails on header-only files (no data rows).
        # "Given path '...' returned no results from INFER_SCHEMA".
        # Fall back to reading the first line as raw text and constructing a
        # StringType schema from the column names.  Only attempt the fallback
        # for single-path calls (multi-path = mergeSchema case; rare for empty
        # writes).  PARSE_HEADER lives in the FILE_FORMAT (via FORMAT_NAME) not
        # directly in snowpark_reader_options, so we don't gate on that flag —
        # instead we let the header-line reader fail gracefully (returns None)
        # if no usable header is found.
        if len(chunk_paths) == 1:
            exc_str = str(infer_exc)
            # Trigger the header-only fallback only for the canonical INFER_SCHEMA
            # "returned no results" message Snowflake emits for a stage path
            # that scans to zero data rows.  The narrower string match keeps us
            # from accidentally falling through on other INFER_SCHEMA failures
            # (compression mismatches, PARSE_HEADER rejecting duplicate columns,
            # genuinely missing stages with a different error wording, etc.).
            # The header-line reader has its own per-row guards so the
            # fallback still returns ``None`` cleanly if the file isn't actually
            # header-only — the gating here is a fast exit, not a safety net.
            #
            # Limitation inherited from snowpark-python: when INFER_SCHEMA
            # returns zero rows, snowpark synthesises a single
            # ``FileNotFoundError`` with message "Given path: '...' returned no
            # results from INFER_SCHEMA. The path may be empty/missing, or file
            # format options may have filtered every row/header." — i.e. it
            # conflates "stage path missing", "files exist but are empty", and
            # "files exist but file-format options filtered everything" into
            # one exception type and one message.  We can't disambiguate from
            # the exception alone, so we always attempt the header-line read
            # below; if the file is genuinely missing the SELECT raises
            # ``SnowparkSQLException`` (caught inside the helper, returns
            # ``None``) and the original FileNotFoundError re-raises.  If
            # snowpark-python ever surfaces distinct error types or a
            # Snowflake errno for the empty-results case, this match should
            # be replaced with that more specific signal.
            if "returned no results from INFER_SCHEMA" in exc_str:
                fallback = _read_header_line_schema_from_stage(
                    session,
                    chunk_paths[0],
                    snowpark_reader_options,
                    csv_file_format_options=csv_file_format_options,
                )
                if fallback is not None:
                    return fallback
        raise


def _csv_struct_all_string_fields(st: StructType) -> StructType:
    """Spark ``inferSchema=false``: treat every column as string while keeping Snowflake names."""
    return StructType([StructField(f.name, StringType(), True) for f in st.fields])


def _validate_user_schema_against_file(
    user_schema: StructType,
    file_schema: StructType,
    enforce_schema: bool,
    corrupt_record_col: str | None = None,
) -> None:
    """Compare user-provided schema against inferred file schema by column names and count.

    When ``enforce_schema`` is ``True`` (default), mismatches produce a warning.
    When ``False``, mismatches raise an ``AnalysisException``.

    The Spark ``columnNameOfCorruptRecord`` column (``corrupt_record_col``) is a
    synthetic column that is never present in the CSV header/file, so it is
    excluded from the name/count comparison (SPARK-27873: disabling
    ``enforceSchema`` must not fail ``columnNameOfCorruptRecord``). It stays in
    the user schema returned for downstream use; only this comparison ignores it.
    """
    corrupt_key = (
        normalized_file_source_column_merge_key(corrupt_record_col)
        if corrupt_record_col
        else None
    )
    user_names = [
        normalized_file_source_column_merge_key(f.name)
        for f in user_schema.fields
        if corrupt_key is None
        or normalized_file_source_column_merge_key(f.name) != corrupt_key
    ]
    file_names = [
        normalized_file_source_column_merge_key(f.name) for f in file_schema.fields
    ]

    mismatches: list[str] = []
    if len(user_names) != len(file_names):
        mismatches.append(
            f"Column count mismatch: schema has {len(user_names)} columns, "
            f"file has {len(file_names)} columns."
        )
    if set(user_names) != set(file_names):
        missing_in_file = set(user_names) - set(file_names)
        extra_in_file = set(file_names) - set(user_names)
        parts: list[str] = []
        if missing_in_file:
            parts.append(
                f"columns in schema but not in file: {sorted(missing_in_file)}"
            )
        if extra_in_file:
            parts.append(f"columns in file but not in schema: {sorted(extra_in_file)}")
        mismatches.append("Column name mismatch: " + "; ".join(parts))

    if not mismatches:
        return

    message = "CSV schema validation: " + " ".join(mismatches)
    if enforce_schema:
        logger.warning(message)
    else:
        exception = AnalysisException(message)
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception


def _sort_headerless_csv_fields_by_position(schema: StructType) -> StructType:
    """Restore positional order for a header-less CSV inferred schema.

    Snowflake ``INFER_SCHEMA`` names header-less columns ``c1``, ``c2``, … and
    returns them ordered by ``ORDER_ID, COLUMN_NAME`` (snowpark-python
    SNOW-2866374). For synthetic positional columns ``ORDER_ID`` is not
    distinct, so the ``COLUMN_NAME`` tiebreaker decides the order — and that
    sorts *lexicographically* (``c1, c10, c11, …, c19, c2, …``) rather than
    numerically. Snowpark renames ``cN`` → Spark's ``_c{N-1}`` positionally, so
    without this re-sort a CSV with ≥10 columns surfaces a scrambled column
    order (``_c0, _c9, _c10, …, _c1, …``) instead of ``_c0, _c1, _c2, …``.

    Sort numerically by the ``cN`` index to guarantee true positional order,
    independent of how INFER_SCHEMA / snowpark order their rows. Fields whose
    names don't match the positional ``cN`` pattern keep their original
    relative order (stable sort), so this is a no-op for any non-positional
    schema.
    """

    def position_key(field: StructField) -> tuple[int, int]:
        match = INDEXED_COLUMN_NAME_PATTERN.match(field.name)
        if match is None:
            return (1, 0)
        return (0, int(match.group(2)))

    return StructType(sorted(schema.fields, key=position_key))


def _resolve_csv_schemas(
    session: snowpark.Session,
    schema: StructType | None,
    all_paths: list[str],
    snowpark_reader_options: dict[str, Any],
    parse_header: bool,
    infer_schema: bool,
    relax_types_to_infer_schema: bool,
    partition_columns: list[str],
    merge_schema: bool,
    enforce_schema: bool,
    corrupt_record_col: str | None = None,
    csv_file_format_options: dict[str, Any] | None = None,
    allow_header_dedup: bool = False,
) -> tuple[StructType, bool]:
    """Return ``(logical CSV data schema, needs_positional_dedup_load)`` for unified COPY.

    Schema layout and column names come from Snowflake CSV ``INFER_SCHEMA`` via
    Snowpark ``session.read.options(..., INFER_SCHEMA=True).csv(...)``.

    **Header row present** (``parse_header``): column names come from the file header
    (via inference). ``mergeSchema`` is honored **only when** ``inferSchema`` is
    true — if ``inferSchema`` is false, the schema is taken from the **first path
    only** (``mergeSchema`` is ignored). If ``inferSchema`` is true and
    ``mergeSchema`` is true and there are multiple paths, schemas from **all**
    path groups are merged; if ``mergeSchema`` is false, only the **first** path
    is inferred.

    **No header**: column names are Snowflake’s positional names (Spark-style
    ``_c0``, ``_c1``, …). The schema is inferred from the **first path only**
    to match Spark’s behavior of determining column count from the first row
    of the first file.

    Without ``inferSchema``, inferred types are coerced to ``StringType`` in the
    logical schema (Spark ``inferSchema=false``).

    ``FILE_FORMAT`` options for COPY are built in ``map_read_csv`` via
    :func:`_snowflake_csv_file_format_options`; ``PARSE_HEADER`` there drives
    ``MATCH_BY_COLUMN_NAME`` in :func:`_load_file_with_copy_into`.

    SNOW-3385963: when ``parse_header`` and no user schema is given and
    ``allow_header_dedup`` is set, a header with exact-duplicate or empty column
    names (which Snowflake INFER_SCHEMA rejects) is recovered by reading the raw
    header and deduplicating it the way Spark does (``a,b,a -> a0,b,a2``; empty
    -> ``_c{i}``). In that case the second tuple element
    (``needs_positional_dedup_load``) is ``True`` and the caller must load the
    data positionally — the deduped names no longer match the physical header,
    so ``MATCH_BY_COLUMN_NAME`` cannot be used. Every other path returns
    ``False``.
    """
    partition_set = set(partition_columns)
    first_path = all_paths[0]

    if schema is not None:
        user_data_schema = StructType(
            [f for f in schema.fields if unquote_if_quoted(f.name) not in partition_set]
        )
        if parse_header and not enforce_schema:
            merged_file_schema: StructType | None = None
            for _stage, chunk in generate_stage_path_groups_for_read(all_paths):
                chunk_schema = _infer_csv_schema_for_stage_chunk(
                    session,
                    chunk,
                    snowpark_reader_options,
                    relax_types_to_infer_schema=False,
                    csv_file_format_options=csv_file_format_options,
                )
                merged_file_schema = _merge_inferred_csv_struct_schemas(
                    merged_file_schema, chunk_schema
                )
            _validate_user_schema_against_file(
                user_data_schema,
                merged_file_schema,
                enforce_schema,
                corrupt_record_col=corrupt_record_col,
            )
        return user_data_schema, False

    if parse_header:
        if merge_schema and len(all_paths) > 1:
            # NOTE: duplicate/empty-header dedup (SNOW-3385963) is not applied
            # here — mergeSchema + duplicates is unsupported.  If any file in
            # the merge set has a header Snowflake rejects, INFER_SCHEMA will
            # propagate the error unchanged.
            merged: StructType | None = None
            for _stage, chunk in generate_stage_path_groups_for_read(all_paths):
                chunk_schema = _infer_csv_schema_for_stage_chunk(
                    session,
                    chunk,
                    snowpark_reader_options,
                    relax_types_to_infer_schema=relax_types_to_infer_schema,
                    csv_file_format_options=csv_file_format_options,
                )
                merged = _merge_inferred_csv_struct_schemas(merged, chunk_schema)
            if not infer_schema:
                merged = _csv_struct_all_string_fields(merged)
            return merged, False

        try:
            logical = _infer_csv_schema_for_stage_chunk(
                session,
                [first_path],
                snowpark_reader_options,
                relax_types_to_infer_schema=relax_types_to_infer_schema,
                csv_file_format_options=csv_file_format_options,
                names_only=not infer_schema,
            )
        except Exception as infer_exc:
            # SNOW-3385963: Snowflake INFER_SCHEMA rejects exact-duplicate
            # (``a,b,a``) and empty (``a,,b``) CSV headers, returning no rows.
            # Spark deduplicates them instead. Recover the Spark-deduplicated
            # schema from the raw header and signal a positional load. Scoped to
            # PERMISSIVE (``allow_header_dedup``) to match the positional COPY
            # path; for any other failure / mode, re-raise unchanged.
            #
            # Why ``except Exception`` (not a narrower type): snowpark-python
            # synthesises a ``FileNotFoundError`` for the zero-row INFER_SCHEMA
            # case, but other INFER_SCHEMA failures may surface as
            # ``SnowparkSQLException`` or future exception types.  We catch
            # broadly and immediately re-raise unless the message matches the
            # specific "returned no results" wording, so no errors are swallowed.
            #
            # Coupling note: the ``"returned no results from INFER_SCHEMA"``
            # substring match is coupled to the exact server/snowpark error
            # message. If the wording changes, this path silently stops firing
            # and users see the raw INFER_SCHEMA error (safe degradation, not
            # data corruption).  Same pattern as the header-only fallback in
            # ``_infer_csv_schema_for_stage_chunk`` (line ~1290).
            if not allow_header_dedup or (
                "returned no results from INFER_SCHEMA" not in str(infer_exc)
            ):
                raise
            from snowflake.snowpark_connect.config import global_config

            deduped = _resolve_deduped_header_schema(
                session,
                first_path,
                snowpark_reader_options,
                csv_file_format_options,
                case_sensitive=global_config.spark_sql_caseSensitive,
            )
            if deduped is None:
                raise
            # Already all-StringType (Spark inferSchema=false default; types are
            # unavailable once the header is rejected).
            return deduped, True
        if not infer_schema:
            logical = _csv_struct_all_string_fields(logical)
        return logical, False

    # No header: positional names (_c0, …). Spark determines column count
    # from the first row of the first file, so we infer from the first path only.
    logical = _infer_csv_schema_for_stage_chunk(
        session,
        [first_path],
        snowpark_reader_options,
        relax_types_to_infer_schema=infer_schema and relax_types_to_infer_schema,
        csv_file_format_options=csv_file_format_options,
        names_only=not infer_schema,
    )
    logical = _sort_headerless_csv_fields_by_position(logical)
    if not infer_schema:
        logical = _csv_struct_all_string_fields(logical)
    return logical, False


def relax_csv_types(t: DataType) -> DataType:
    """Widen numeric types to match OSS Spark's CSV schema inference rules.

    Snowpark's USE_RELAXED_TYPES (most_permissive_type) which incorrectly maps all numerics to DoubleType.
    We now handle relaxation ourselves for all clients, replacing USE_RELAXED_TYPES with these Spark-compatible rules.

    After applying relax_csv_types, converts to Spark CSV types:
    - IntegerType, ShortType, ByteType -> IntegerType
    - LongType -> LongType
    - DecimalType with scale > 0 -> DoubleType
    - DecimalType with precision > 18 -> DecimalType (too big for long)
    - DecimalType with precision > 9 -> LongType
    - DecimalType with precision <= 9 -> IntegerType
    - FloatType, DoubleType -> DoubleType
    """
    if isinstance(t, StructType):
        for sf in t.fields:
            sf.datatype = relax_csv_types(sf.datatype)
        return t
    elif isinstance(t, ArrayType):
        if t.element_type is not None:
            t.element_type = relax_csv_types(t.element_type)
        return t
    elif isinstance(t, MapType):
        t.key_type = relax_csv_types(t.key_type)
        t.value_type = relax_csv_types(t.value_type)
        return t

    # First apply standard integral type conversion
    t = emulate_integral_types(t)

    if isinstance(t, LongType):
        return LongType()
    elif isinstance(t, _IntegralType):
        # ByteType, ShortType, IntegerType -> IntegerType
        return IntegerType()
    elif isinstance(t, DecimalType):
        # DecimalType with scale > 0 means it has decimal places -> DoubleType
        if t.scale > 0:
            return DoubleType()
        # DecimalType with scale = 0 is integral
        if t.precision > 18:
            # Too big for long, keep as DecimalType
            return DecimalType(t.precision, 0)
        if t.precision > 9:
            return LongType()
        return IntegerType()
    elif isinstance(t, _FractionalType):
        # FloatType, DoubleType -> DoubleType
        return DoubleType()

    return t


def _resolve_corrupt_record_column(
    options: CsvReaderConfig,
    schema: StructType | None,
) -> str | None:
    """Resolve the Spark ``_corrupt_record`` column for a CSV read, if any.

    Resolution order for the column name:
      1. ``option("columnNameOfCorruptRecord")``
      2. session conf ``spark.sql.columnNameOfCorruptRecord``
      3. Spark default ``_corrupt_record``

    Returns the matched column name (in the user's exact spelling) whenever
    the user supplied a schema that contains a field matching the resolved
    name (case-folded per ``spark.sql.caseSensitive``). Returns ``None``
    otherwise. Resolution is mode-agnostic; the caller decides how to wire
    the column for PERMISSIVE/DROPMALFORMED/FAILFAST.

    Spark CSV (unlike JSON) does **not** auto-inject the column -- it must be
    present in the user schema.

    Raises ``AnalysisException`` if the matched field is not a ``StringType``.
    The nullable half of Spark's ``ExprUtils.verifyColumnNameOfCorruptRecord``
    rule is **not** enforced because Spark itself does not enforce it on the
    CSV path -- ``StringType, nullable=False`` is silently accepted there
    (verified against Spark 3.5.3). Callers must still coerce the field to
    nullable before it reaches the typed COPY INTO target table because
    Snowflake's CSV ingest path does not apply Spark's silent-coercion
    semantics (see the nullable normalization in ``map_read_csv``).
    """
    if schema is None:
        return None

    requested = options.config.get("columnnameofcorruptrecord")
    if not requested:
        requested = get_string_session_config_param(
            "spark.sql.columnNameOfCorruptRecord"
        )
    if not requested:
        return None

    target_key = _norm_case(requested)
    matched_field: StructField | None = None
    matched_user_name: str | None = None
    for f in schema.fields:
        # ``f.name`` reflects Snowflake's identifier normalization: quoted Spark
        # names round-trip through Snowpark as ``'"foo"'`` while bare names are
        # upper-cased. ``unquote_if_quoted`` recovers the user's intended Spark
        # spelling so the case-folded comparison hits.
        user_name = unquote_if_quoted(f.name)
        if _norm_case(user_name) == target_key:
            matched_field = f
            matched_user_name = user_name
            break
    if matched_field is None or matched_user_name is None:
        return None

    if not isinstance(matched_field.datatype, StringType):
        # Spark CSV only enforces the *type* half of
        # ``ExprUtils.verifyColumnNameOfCorruptRecord`` (verified against
        # Spark 3.5.3 in every mode); ``nullable=False`` is silently
        # accepted, so we match that and let the caller normalize the
        # field to nullable=True before the typed COPY target table.
        exception = AnalysisException(
            "The field for corrupt records must be string type"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    return matched_user_name


def _make_schema_nullable(schema: StructType) -> StructType:
    """
    Convert all fields in a schema to nullable for CSV reading.

    SPARK-35912: CSV file sources can always contain NULL values,
    so Spark automatically converts non-nullable user schemas to nullable.
    This matches that behavior when snowpark.connect.io.validations.mode="strict".

    Args:
        schema: The schema to convert.

    Returns:
        A new StructType with all fields set to nullable=True.
    """

    def _make_type_nullable(data_type: DataType) -> DataType:
        """Recursively make nested types nullable."""
        if isinstance(data_type, StructType):
            return StructType(
                [
                    StructField(f.name, _make_type_nullable(f.datatype), nullable=True)
                    for f in data_type.fields
                ]
            )
        elif isinstance(data_type, ArrayType):
            element_type = data_type.element_type
            if element_type is not None:
                return ArrayType(
                    _make_type_nullable(element_type),
                    contains_null=True,
                )
            return data_type
        elif isinstance(data_type, MapType):
            key_type = data_type.key_type
            value_type = data_type.value_type
            if key_type is not None and value_type is not None:
                return MapType(
                    _make_type_nullable(key_type),
                    _make_type_nullable(value_type),
                    value_contains_null=True,
                )
            return data_type
        return data_type

    return StructType(
        [
            StructField(f.name, _make_type_nullable(f.datatype), nullable=True)
            for f in schema.fields
        ]
    )
