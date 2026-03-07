#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import os
import shutil
import uuid
from contextlib import suppress
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.commands_pb2 as commands_proto
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.errors.exceptions.connect import IllegalArgumentException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.functions import col, lit, object_construct, sql_expr, when
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DateType,
    MapType,
    StringType,
    StructType,
    TimestampType,
    VariantType,
    _NumericType,
)
from snowflake.snowpark_connect.config import (
    auto_uppercase_column_identifiers,
    get_parquet_metadata_generation_enabled,
    get_success_file_generation_enabled,
    global_config,
    sessions_config,
    str_to_bool,
)
from snowflake.snowpark_connect.constants import SPARK_VERSION
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    convert_file_prefix_path,
    get_compression_for_source_and_options,
    is_cloud_path,
)
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.neo4j_utils import (
    transform_neo4j_to_jdbc_options,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.relation.read.reader_config import CsvWriterConfig
from snowflake.snowpark_connect.relation.stage_locator import get_paths_from_stage
from snowflake.snowpark_connect.relation.utils import (
    generate_spark_compatible_filename,
    random_string,
)
from snowflake.snowpark_connect.type_mapping import (
    map_pyspark_types_to_pyarrow_types,
    map_snowpark_to_pyspark_types,
)
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.identifiers import (
    spark_to_sf_single_id,
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.io_utils import (
    PartitionSpec,
    get_overwrite_condition,
    get_partition_spec,
    get_table_type,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.utils.udf_cache import register_cached_sproc

_column_order_for_write = "name"

# Available values for TARGET_FILE_SIZE
#   reference:https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table
TARGET_FILE_SIZE_ACCEPTABLE_VALUES = ("AUTO", "16MB", "32MB", "64MB", "128MB")


# TODO: We will revise/refactor this after changes for all formats are finalized.
def clean_params(params):
    """
    Clean params for write operation. This, for now, allows us to use the same parameter code that
    read operations use.
    """
    # INFER_SCHEMA does not apply to writes
    if "INFER_SCHEMA" in params["format_type_options"]:
        del params["format_type_options"]["INFER_SCHEMA"]


def get_param_from_options(params, options, source):
    match source:
        case "csv":
            config = CsvWriterConfig(options)
            snowpark_args = config.convert_to_snowpark_args()

            if "header" in options:
                params["header"] = str_to_bool(options["header"])
            params["single"] = False

            params["format_type_options"] = snowpark_args
            clean_params(params)
        case "json":
            params["format_type_options"]["FILE_EXTENSION"] = source
        case "parquet":
            params["header"] = True
        case "text":
            config = CsvWriterConfig(options)
            params["format_type_options"]["FILE_EXTENSION"] = "txt"
            params["format_type_options"]["ESCAPE_UNENCLOSED_FIELD"] = "NONE"
            if "lineSep" in options:
                params["format_type_options"]["RECORD_DELIMITER"] = config.get(
                    "linesep"
                )

    if (
        source in ("csv", "parquet", "json") and "nullValue" in options
    ):  # TODO: Null value handling if not specified
        params["format_type_options"]["NULL_IF"] = options["nullValue"]


def _spark_to_snowflake(multipart_id: str) -> str:
    return ".".join(
        spark_to_sf_single_id(part)
        for part in split_fully_qualified_spark_name(multipart_id)
    )


def _validate_table_exist_and_of_type(
    snowpark_table_name: str,
    session: snowpark.Session,
    table_type: str,
    table_schema_or_error: DataType | SnowparkSQLException,
) -> None:
    if not isinstance(table_schema_or_error, DataType):
        exception = AnalysisException(
            f"[TABLE_OR_VIEW_NOT_FOUND] The table or view `{snowpark_table_name}` cannot be found."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception
    _validate_table_type(snowpark_table_name, session, table_type)


def _validate_table_type(
    snowpark_table_name: str,
    session: snowpark.Session,
    table_type: str,
) -> None:
    actual_type = get_table_type(snowpark_table_name, session)
    if table_type == "iceberg":
        if actual_type not in ("ICEBERG", "TABLE"):
            exception = AnalysisException(
                f"Table {snowpark_table_name} is not an iceberg table"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
    elif table_type == "fdn":
        if actual_type not in ("NORMAL", "TABLE"):
            exception = AnalysisException(
                f"Table {snowpark_table_name} is not a FDN table"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
    else:
        raise ValueError(
            f"Invalid table_type: {table_type}. Must be 'iceberg' or 'fdn'"
        )


def _validate_table_does_not_exist(
    snowpark_table_name: str,
    table_schema_or_error: DataType | SnowparkSQLException,
) -> None:
    if isinstance(table_schema_or_error, DataType):
        exception = AnalysisException(f"Table {snowpark_table_name} already exists")
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception


def _validate_partition_columns_match_spec(
    partition_cols: list[str],
    table_partition_spec: PartitionSpec,
) -> None:
    """
    Checks if all given partition_columns are present in the partition_spec.
    All columns from the spec should be in partition_cols, in the same order.
    """
    if table_partition_spec is None:
        if partition_cols:
            exception = IllegalArgumentException(
                "The provided partitioning does not match the table partitioning: "
                f"provided [{', '.join(partition_cols)}] but table has no partition columns."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        return

    table_partition_cols = [
        spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
        for c in table_partition_spec.columns()
    ]
    provided_partition_cols = [
        spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
        for c in partition_cols
    ]

    if provided_partition_cols != table_partition_cols:
        exception = IllegalArgumentException(
            "The provided partitioning does not match the table partitioning: "
            f"provided [{', '.join(partition_cols)}] vs table [{', '.join(table_partition_spec.columns())}]."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def map_write(request: proto_base.ExecutePlanRequest):
    write_op = request.plan.command.write_operation
    telemetry.report_io_write(write_op.source, dict(write_op.options))
    if write_op.path and write_op.options.get("path"):
        raise AnalysisException(
            "There is a 'path' option set and save() is called with a path parameter. "
            "Either remove the path option, or call save() without the parameter."
        )

    write_mode = None
    match write_op.mode:
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_APPEND:
            write_mode = "append"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_ERROR_IF_EXISTS:
            write_mode = "errorifexists"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_OVERWRITE:
            # the dataframe API doesn't seem to respect spark.sql.sources.partitionOverwriteMode
            # overwrite-mode is used instead
            overwrite_mode = write_op.options.get("overwrite-mode", "static")
            if (
                overwrite_mode.lower() == "dynamic"
                and write_op.source == "iceberg"
                and write_op.partitioning_columns
            ):
                write_mode = "overwrite_partitions"
            else:
                write_mode = "overwrite"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_IGNORE:
            write_mode = "ignore"

    # immediately exclude hidden columns for writing
    result = map_relation(write_op.input).without_hidden_columns()
    input_df, snowpark_column_names = handle_column_names(result, write_op.source)

    # Create updated container with transformed dataframe, then filter METADATA$FILENAME columns
    updated_result = DataFrameContainer.create_with_column_mapping(
        dataframe=input_df,
        spark_column_names=result.column_map.get_spark_columns(),
        snowpark_column_names=snowpark_column_names,
        column_metadata=result.column_map.column_metadata,
        column_qualifiers=result.column_map.get_qualifiers(),
        parent_column_name_map=result.column_map.get_parent_column_name_map(),
        table_name=result.table_name,
        alias=result.alias,
        partition_hint=result.partition_hint,
    )
    updated_result = without_internal_columns(updated_result)
    input_df = updated_result.dataframe

    session: snowpark.Session = get_or_create_snowpark_session()

    # Check for partition hint early to determine precedence over single option
    partition_hint = (
        result.partition_hint if hasattr(result, "partition_hint") else None
    )

    # Snowflake saveAsTable doesn't support format
    if (
        write_op.HasField("table")
        and write_op.HasField("source")
        and write_op.source in ("csv", "parquet", "json", "text")
    ):
        write_op.source = ""

    should_write_to_single_file = str_to_bool(write_op.options.get("single", "false"))

    # Support Snowflake-specific snowflake_max_file_size option. This is NOT a spark option.
    max_file_size = None
    if (
        "snowflake_max_file_size" in write_op.options
        and int(write_op.options["snowflake_max_file_size"]) > 0
    ):
        max_file_size = int(write_op.options["snowflake_max_file_size"])
    elif should_write_to_single_file:
        # providing default size as 1GB for single file write
        max_file_size = 1073741824
    match write_op.source:
        case "csv" | "parquet" | "json" | "text":
            # TODO: Extend SaveMode.Ignore support to csv, json, and text formats.
            #  The path-existence check logic already implemented for parquet
            #  (see the "ignore" block below) is format-agnostic and can be
            #  reused directly for these formats.
            if write_mode == "ignore" and write_op.source != "parquet":
                exception = SnowparkConnectNotImplementedError(
                    f"Write mode {write_mode} is not supported for {write_op.source}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            write_path = get_paths_from_stage(
                [write_op.path],
                session=session,
            )[0]

            # Handle ignore mode for parquet: if the path already exists,
            # silently skip the write.  Per Spark's SaveMode.Ignore semantics,
            # existing data must not be changed.
            if write_mode == "ignore":
                is_local_path = not is_cloud_path(write_op.path)
                path_exists = False
                if is_local_path:
                    path_exists = os.path.exists(write_op.path) and (
                        os.path.isfile(write_op.path)
                        or (os.path.isdir(write_op.path) and os.listdir(write_op.path))
                    )
                else:
                    with suppress(SnowparkSQLException):
                        list_command = f"LIST '{write_path}/'"
                        result = session.sql(list_command).collect()
                        if result:
                            path_exists = True
                if path_exists:
                    return

            # Handle error/errorifexists mode - check if file exists before writing
            if write_mode in (None, "error", "errorifexists"):
                is_local_path = not is_cloud_path(write_op.path)

                if is_local_path:
                    # Check if local path exists
                    if os.path.exists(write_op.path) and (
                        os.path.isfile(write_op.path)
                        or (os.path.isdir(write_op.path) and os.listdir(write_op.path))
                    ):
                        exception = AnalysisException(
                            f"Path {write_op.path} already exists."
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception
                else:
                    # Check if stage/cloud path exists by listing files
                    # If the path does not exist, SnowparkSQLException is suppressed (expected for error mode).
                    with suppress(SnowparkSQLException):
                        # TODO: Optimize this check by using a more efficient way to check if the path exists.
                        list_command = f"LIST '{write_path}/'"
                        result = session.sql(list_command).collect()
                        if result:
                            exception = AnalysisException(
                                f"Path {write_op.path} already exists."
                            )
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_OPERATION
                            )
                            raise exception

            # Generate Spark-compatible filename with proper extension
            extension = write_op.source if write_op.source != "text" else "txt"

            compression = get_compression_for_source_and_options(
                write_op.source, write_op.options, from_read=False
            )
            if compression is not None:
                write_op.options["compression"] = compression

            # Generate Spark-compatible filename or prefix
            # we need a random prefix to support "append" mode
            # otherwise copy into with overwrite=False will fail if the file already exists
            overwrite = (
                write_op.mode
                == commands_proto.WriteOperation.SaveMode.SAVE_MODE_OVERWRITE
            )

            if overwrite:
                # Trailing slash is required as calling remove with just write_path would remove everything in the
                # stage path with the same prefix.

                partition_overwrite_mode = global_config.get(
                    "spark.sql.sources.partitionOverwriteMode", "static"
                )
                if (
                    write_op.partitioning_columns
                    and partition_overwrite_mode == "dynamic"
                ):
                    partitioning_columns = write_op.partitioning_columns
                    snowpark_partitioning_columns = [
                        quote_name_without_upper_casing(partition_column)
                        for partition_column in partitioning_columns
                    ]
                    distinct_values = (
                        input_df.select(*snowpark_partitioning_columns)
                        .distinct()
                        .collect()
                    )
                    partition_paths = set()
                    for row in distinct_values:
                        paths = []
                        for key, value in zip(partitioning_columns, row):
                            if value is None:
                                value = "__HIVE_DEFAULT_PARTITION__"
                            paths.append(f"{key}={value}")
                        if paths:
                            partition_paths.add("/".join(paths))

                    for partition_path in partition_paths:
                        # There is no concurrent remove of the directory hence it has to be done sequentially
                        remove_command = (
                            f"REMOVE '{write_path}' PATTERN = '.*/{partition_path}.*'"
                        )
                        session.sql(remove_command).collect()
                        logger.info(
                            f"Successfully cleared partition directory: {write_path}/{partition_path}"
                        )
                else:
                    remove_command = f"REMOVE '{write_path}'"
                    session.sql(remove_command).collect()
                    logger.info(f"Successfully cleared directory: {write_path}")

            if should_write_to_single_file and partition_hint is None:
                # Single file: generate complete filename with extension
                spark_filename = generate_spark_compatible_filename(
                    task_id=0,
                    attempt_number=0,
                    compression=compression,
                    format_ext=extension,
                )
                temp_file_prefix_on_stage = f"{write_path}/{spark_filename}"
            else:
                # Multiple files: generate prefix without extension (Snowflake will add extensions)
                spark_filename_prefix = generate_spark_compatible_filename(
                    task_id=0,
                    attempt_number=0,
                    compression=None,
                    format_ext="",  # No extension for prefix
                )
                temp_file_prefix_on_stage = f"{write_path}/{spark_filename_prefix}"

            parameters = {
                "location": temp_file_prefix_on_stage,
                "file_format_type": write_op.source
                if write_op.source != "text"
                else "csv",
                "format_type_options": {
                    "COMPRESSION": compression,
                },
            }
            # Download from the base write path to ensure we fetch whatever Snowflake produced.
            # Using the base avoids coupling to exact filenames/prefixes.
            download_stage_path = write_path

            # Apply max_file_size for both single and multi-file scenarios
            # This helps control when Snowflake splits files into multiple parts
            if max_file_size:
                parameters["max_file_size"] = max_file_size
            # Only apply single option if no partition hint is present (partition hint takes precedence)
            if should_write_to_single_file and partition_hint is None:
                parameters["single"] = True
            rewritten_df: snowpark.DataFrame = rewrite_df(input_df, write_op.source)
            get_param_from_options(parameters, write_op.options, write_op.source)
            if write_op.partitioning_columns:
                # Build Spark-style directory structure: col1=value1/col2=value2/...
                # Example produced expression (Snowflake SQL):
                #   'department=' || TO_VARCHAR("department") || '/' || 'region=' || TO_VARCHAR("region")
                partitioning_column_names = list(write_op.partitioning_columns)

                if (
                    len(
                        set(updated_result.column_map.get_spark_columns())
                        - set(partitioning_column_names)
                    )
                    == 0
                ):
                    exception = AnalysisException(
                        "[ALL_PARTITION_COLUMNS_NOT_ALLOWED] Cannot use all columns for partition columns."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
                partition_expr_parts: list[str] = []
                for col_name in partitioning_column_names:
                    if write_op.source == "json":
                        quoted = f"{rewritten_df.columns[0]}['{col_name}']"
                        segment = f"'{col_name}=' || COALESCE(TO_VARCHAR({quoted}), '__HIVE_DEFAULT_PARTITION__')"
                    else:
                        quoted = f'"{col_name}"'
                        segment = f"'{col_name}=' || COALESCE(TO_VARCHAR({quoted}), '__HIVE_DEFAULT_PARTITION__')"
                    partition_expr_parts.append(segment)
                parameters["partition_by"] = " || '/' || ".join(partition_expr_parts)
                # When using PARTITION BY, Snowflake writes into subdirectories under the base path.
                # Download from the base write path to preserve partition directories locally.
                download_stage_path = write_path

            # If a partition hint is present (from DataFrame.repartition(n)), optionally split the
            # write into n COPY INTO calls by assigning a synthetic partition id. Controlled by config.
            # Note: This affects only the number of output files, not computation semantics.
            # Partition hints take precedence over single option (matches Spark behavior) when enabled.
            repartition_for_writes_enabled = (
                global_config.snowflake_repartition_for_writes
            )
            if repartition_for_writes_enabled and partition_hint and partition_hint > 0:
                # Create a stable synthetic file number per row using ROW_NUMBER() over a
                # randomized order, then modulo partition_hint. We rely on sql_expr to avoid
                # adding new helpers.
                file_num_col = "_sas_file_num"
                partitioned_df = rewritten_df.withColumn(
                    file_num_col,
                    sql_expr(
                        f"(ROW_NUMBER() OVER (ORDER BY RANDOM())) % {partition_hint}"
                    ),
                )

                # Execute multiple COPY INTO operations, one per target file.
                # Since we write per-partition with distinct prefixes, download from the base write path.
                download_stage_path = write_path

                # We need to create a new set of parameters with single=True
                shared_uuid = str(uuid.uuid4())
                part_params = copy.deepcopy(dict(parameters))
                part_params["single"] = True
                for part_idx in range(partition_hint):
                    # Preserve Spark-like filename prefix per partition so downloaded basenames
                    # match the expected Spark pattern (with possible Snowflake counters appended).
                    per_part_prefix = generate_spark_compatible_filename(
                        task_id=part_idx,
                        attempt_number=0,
                        compression=compression,
                        format_ext=extension,
                        shared_uuid=shared_uuid,
                    )
                    part_params["location"] = f"{write_path}/{per_part_prefix}"
                    (
                        partitioned_df.filter(col(file_num_col) == lit(part_idx))
                        .drop(file_num_col)
                        .write.copy_into_location(**part_params)
                    )
            else:
                rewritten_df.write.copy_into_location(**parameters)

            is_local_path = not is_cloud_path(write_op.path)
            if is_local_path:
                store_files_locally(
                    download_stage_path,
                    write_op.path,
                    overwrite,
                    session,
                )

            _generate_metadata_files(
                write_op.source,
                write_op.path,
                download_stage_path,
                input_df.schema,
                session,
                parameters,
                is_local_path,
            )
        case "jdbc":
            from snowflake.snowpark_connect.relation.write.map_write_jdbc import (
                map_write_jdbc,
            )

            options = dict(write_op.options)
            if write_mode is None:
                write_mode = "errorifexists"
            map_write_jdbc(result, session, options, write_mode)
        case "org.neo4j.spark.DataSource":
            from snowflake.snowpark_connect.relation.write.map_write_jdbc import (
                map_write_jdbc,
            )

            options = dict(write_op.options)
            # Transform Neo4j Spark Connector options to JDBC options
            # See neo4j_utils.py for pros/cons of this approach
            jdbc_options = transform_neo4j_to_jdbc_options(options, "write")
            if write_mode is None:
                write_mode = "append"  # Default to append for Neo4j
            map_write_jdbc(result, session, jdbc_options, write_mode)
        case "iceberg":
            table_name = (
                write_op.path
                if write_op.path is not None and write_op.path != ""
                else write_op.table.table_name
            )
            snowpark_table_name = _spark_to_snowflake(table_name)
            partition_cols = (
                list(write_op.partitioning_columns)
                if write_op.partitioning_columns
                else None
            )

            iceberg_config = _build_iceberg_config(
                options=dict(write_op.options),
                partition_cols=partition_cols,
            )

            match write_mode:
                case None | "error" | "errorifexists":
                    table_schema_or_error = _get_table_schema_or_error(
                        snowpark_table_name, session
                    )
                    _validate_table_does_not_exist(
                        snowpark_table_name, table_schema_or_error
                    )
                    _get_writer_for_table_creation(input_df).saveAsTable(
                        table_name=snowpark_table_name,
                        mode="errorifexists",
                        column_order=_column_order_for_write,
                        iceberg_config=iceberg_config,
                    )
                case "append":
                    table_schema_or_error = _get_table_schema_or_error(
                        snowpark_table_name, session
                    )
                    if isinstance(table_schema_or_error, DataType):  # Table exists
                        _validate_table_type(snowpark_table_name, session, "iceberg")
                    _validate_schema_and_get_writer(
                        input_df, "append", snowpark_table_name, table_schema_or_error
                    ).saveAsTable(
                        table_name=snowpark_table_name,
                        mode="append",
                        column_order=_column_order_for_write,
                        iceberg_config=iceberg_config,
                    )
                case "ignore":
                    table_schema_or_error = _get_table_schema_or_error(
                        snowpark_table_name, session
                    )
                    if not isinstance(
                        table_schema_or_error, DataType
                    ):  # Table not exists
                        _get_writer_for_table_creation(input_df).saveAsTable(
                            table_name=snowpark_table_name,
                            mode="ignore",
                            column_order=_column_order_for_write,
                            iceberg_config=iceberg_config,
                        )
                case "overwrite":
                    table_schema_or_error = _get_table_schema_or_error(
                        snowpark_table_name, session
                    )
                    table_exists = isinstance(table_schema_or_error, DataType)
                    if table_exists:
                        _validate_table_type(snowpark_table_name, session, "iceberg")
                    writer = (
                        _validate_schema_and_get_writer(
                            input_df,
                            "overwrite",
                            snowpark_table_name,
                            table_schema_or_error if table_exists else None,
                        )
                        if table_exists
                        else _get_writer_for_table_creation(input_df)
                    )
                    _overwrite_iceberg_with_fallback(
                        writer=writer,
                        snowpark_table_name=snowpark_table_name,
                        iceberg_config=iceberg_config,
                        session=session,
                        input_df=input_df,
                    )
                case "overwrite_partitions":
                    table_schema_or_error = _get_table_schema_or_error(
                        snowpark_table_name, session
                    )
                    _validate_table_exist_and_of_type(
                        snowpark_table_name, session, "iceberg", table_schema_or_error
                    )

                    table_partition_spec = get_partition_spec(
                        snowpark_table_name, session
                    )
                    _validate_partition_columns_match_spec(
                        partition_cols, table_partition_spec
                    )

                    partition_column_names = updated_result.column_map.get_snowpark_column_names_from_spark_column_names(
                        partition_cols
                    )
                    distinct_partitions_df = input_df.select(
                        *partition_column_names
                    ).distinct()

                    overwrite_condition = get_overwrite_condition(
                        distinct_partitions_df,
                        partition_column_names,
                    )
                    _validate_schema_and_get_writer(
                        input_df,
                        "overwrite",
                        snowpark_table_name,
                        table_schema_or_error,
                    ).saveAsTable(
                        table_name=snowpark_table_name,
                        table_exists=True,
                        mode="overwrite",
                        column_order=_column_order_for_write,
                        overwrite_condition=overwrite_condition,
                        iceberg_config=iceberg_config,
                    )
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"Write mode {write_mode} is not supported"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
        case _:
            snowpark_table_name = _spark_to_snowflake(write_op.table.table_name)
            save_method = write_op.table.save_method

            if (
                write_op.source == "snowflake"
                and write_op.table.save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_UNSPECIFIED
            ):
                save_method = (
                    commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_SAVE_AS_TABLE
                )
                if len(write_op.table.table_name) == 0:
                    dbtable_name = write_op.options.get("dbtable", "")
                    if len(dbtable_name) == 0:
                        exception = SnowparkConnectNotImplementedError(
                            "Save command is not supported without a table name"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
                    else:
                        snowpark_table_name = _spark_to_snowflake(dbtable_name)

            if (
                save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_SAVE_AS_TABLE
            ):
                match write_mode:
                    case "overwrite":
                        table_schema_or_error = _get_table_schema_or_error(
                            snowpark_table_name, session
                        )
                        if isinstance(table_schema_or_error, DataType):  # Table exists
                            _validate_table_type(snowpark_table_name, session, "fdn")

                        write_mode = "overwrite"
                        _validate_schema_and_get_writer(
                            input_df,
                            write_mode,
                            snowpark_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            copy_grants=True,
                            column_order=_column_order_for_write,
                        )
                    case "append":
                        table_schema_or_error = _get_table_schema_or_error(
                            snowpark_table_name, session
                        )
                        if isinstance(table_schema_or_error, DataType):  # Table exists
                            _validate_table_type(snowpark_table_name, session, "fdn")

                        _validate_schema_and_get_writer(
                            input_df,
                            write_mode,
                            snowpark_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            column_order=_column_order_for_write,
                        )
                    case _:
                        _validate_schema_and_get_writer(
                            input_df, write_mode, snowpark_table_name
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            column_order=_column_order_for_write,
                        )
            elif (
                save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_INSERT_INTO
            ):
                _validate_schema_and_get_writer(
                    input_df, write_mode, snowpark_table_name
                ).saveAsTable(
                    table_name=snowpark_table_name,
                    mode=write_mode or "append",
                    column_order=_column_order_for_write,
                )
            else:
                exception = SnowparkConnectNotImplementedError(
                    f"Save command not supported: {save_method}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception


def map_write_v2(request: proto_base.ExecutePlanRequest):
    write_op = request.plan.command.write_operation_v2

    snowpark_table_name = _spark_to_snowflake(write_op.table_name)
    result = map_relation(write_op.input)
    input_df, snowpark_column_names = handle_column_names(result, "table")

    # Create updated container with transformed dataframe, then filter METADATA$FILENAME columns
    updated_result = DataFrameContainer.create_with_column_mapping(
        dataframe=input_df,
        spark_column_names=result.column_map.get_spark_columns(),
        snowpark_column_names=snowpark_column_names,
        column_metadata=result.column_map.column_metadata,
        column_qualifiers=result.column_map.get_qualifiers(),
        parent_column_name_map=result.column_map.get_parent_column_name_map(),
        table_name=result.table_name,
        alias=result.alias,
        partition_hint=result.partition_hint,
    )
    updated_result = without_internal_columns(updated_result)
    input_df = updated_result.dataframe

    session: snowpark.Session = get_or_create_snowpark_session()

    if write_op.table_name is None or write_op.table_name == "":
        exception = SnowparkConnectNotImplementedError(
            "Write operation V2 only support table writing now"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    is_iceberg = write_op.provider.lower() == "iceberg"
    table_type = "iceberg" if is_iceberg else "fdn"
    partition_cols = (
        [
            i.unresolved_attribute.unparsed_identifier
            for i in write_op.partitioning_columns
        ]
        if write_op.partitioning_columns
        else None
    )

    iceberg_config = (
        _build_iceberg_config(
            options=dict(write_op.table_properties),
            partition_cols=partition_cols,
        )
        if is_iceberg
        else None
    )

    match write_op.mode:
        case commands_proto.WriteOperationV2.MODE_CREATE:
            table_schema_or_error = _get_table_schema_or_error(
                snowpark_table_name, session
            )
            _validate_table_does_not_exist(snowpark_table_name, table_schema_or_error)
            _get_writer_for_table_creation(input_df).saveAsTable(
                table_name=snowpark_table_name,
                mode="errorifexists",
                column_order=_column_order_for_write,
                iceberg_config=iceberg_config,
            )

        case commands_proto.WriteOperationV2.MODE_APPEND:
            table_schema_or_error = _get_table_schema_or_error(
                snowpark_table_name, session
            )
            _validate_table_exist_and_of_type(
                snowpark_table_name, session, table_type, table_schema_or_error
            )
            _validate_schema_and_get_writer(
                input_df, "append", snowpark_table_name, table_schema_or_error
            ).saveAsTable(
                table_name=snowpark_table_name,
                mode="append",
                column_order=_column_order_for_write,
                iceberg_config=iceberg_config,
            )

        case commands_proto.WriteOperationV2.MODE_OVERWRITE | commands_proto.WriteOperationV2.MODE_OVERWRITE_PARTITIONS:
            # TODO: handle the filter condition for MODE_OVERWRITE
            table_schema_or_error = _get_table_schema_or_error(
                snowpark_table_name, session
            )
            _validate_table_exist_and_of_type(
                snowpark_table_name, session, table_type, table_schema_or_error
            )
            writer = _validate_schema_and_get_writer(
                input_df, "overwrite", snowpark_table_name, table_schema_or_error
            )
            if is_iceberg:
                _overwrite_iceberg_with_fallback(
                    writer=writer,
                    snowpark_table_name=snowpark_table_name,
                    iceberg_config=iceberg_config,
                    session=session,
                    input_df=input_df,
                )
            else:
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    mode="overwrite",
                    column_order=_column_order_for_write,
                )

        case commands_proto.WriteOperationV2.MODE_REPLACE:
            table_schema_or_error = _get_table_schema_or_error(
                snowpark_table_name, session
            )
            _validate_table_exist_and_of_type(
                snowpark_table_name, session, table_type, table_schema_or_error
            )
            writer = _validate_schema_and_get_writer(
                input_df, "replace", snowpark_table_name, table_schema_or_error
            )
            if is_iceberg:
                _overwrite_iceberg_with_fallback(
                    writer=writer,
                    snowpark_table_name=snowpark_table_name,
                    iceberg_config=iceberg_config,
                    session=session,
                    input_df=input_df,
                )
            else:
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    mode="overwrite",
                    column_order=_column_order_for_write,
                )

        case commands_proto.WriteOperationV2.MODE_CREATE_OR_REPLACE:
            writer = _validate_schema_and_get_writer(
                input_df, "create_or_replace", snowpark_table_name
            )
            if is_iceberg:
                _overwrite_iceberg_with_fallback(
                    writer=writer,
                    snowpark_table_name=snowpark_table_name,
                    iceberg_config=iceberg_config,
                    session=session,
                    input_df=input_df,
                )
            else:
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    mode="overwrite",
                    column_order=_column_order_for_write,
                )

        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Write mode {commands_proto.WriteOperationV2.Mode.Name(write_op.mode)} is not supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _get_table_schema_or_error(
    snowpark_table_name: str, snowpark_session: snowpark.Session
) -> DataType | SnowparkSQLException:
    try:
        return snowpark_session.table(snowpark_table_name).schema
    except SnowparkSQLException as e:
        return e


def _get_writer_for_table_creation(df: snowpark.DataFrame) -> snowpark.DataFrameWriter:
    # When creating a new table, if case sensitivity is not enabled, we need to rename the columns
    # to upper case so they are case-insensitive in Snowflake.
    if auto_uppercase_column_identifiers():
        for field in df.schema.fields:
            col_name = field.name
            # Uppercasing is fine, regardless of whether the original name was quoted or not.
            # In Snowflake these are equivalent "COL" == COL == col == coL
            uppercased_name = col_name.upper()
            if col_name != uppercased_name:
                df = df.withColumnRenamed(col_name, uppercased_name)
    return df.write


def _validate_schema_and_get_writer(
    input_df: snowpark.DataFrame,
    write_mode: str,
    snowpark_table_name: str,
    table_schema_or_error: DataType | SnowparkSQLException | None = None,
) -> snowpark.DataFrameWriter:
    if write_mode is not None and write_mode.lower() in (
        "replace",
        "create_or_replace",
        "overwrite",
    ):
        return _get_writer_for_table_creation(input_df)

    table_schema = None
    if table_schema_or_error is not None:
        if isinstance(table_schema_or_error, SnowparkSQLException):
            msg = table_schema_or_error.message
            if "SQL compilation error" in msg and "does not exist" in msg:
                pass
            else:
                attach_custom_error_code(
                    table_schema_or_error, ErrorCodes.INTERNAL_ERROR
                )
                raise table_schema_or_error
        elif isinstance(table_schema_or_error, DataType):
            table_schema = table_schema_or_error
    else:
        try:
            table_schema = (
                get_or_create_snowpark_session().table(snowpark_table_name).schema
            )
        except SnowparkSQLException as e:
            msg = e.message
            if "SQL compilation error" in msg and "does not exist" in msg:
                pass
            else:
                attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
                raise e

    if table_schema is None:
        # If table does not exist, we can skip the schema validation
        return _get_writer_for_table_creation(input_df)

    _validate_schema_for_append(table_schema, input_df.schema, snowpark_table_name)

    # If table exists, rename/cast columns to match the existing table schema using a
    # single select() instead of per-column withColumnRenamed/withColumn to avoid
    # generating deeply nested SQL.
    if auto_uppercase_column_identifiers():
        select_cols = []
        needs_rewrite = False
        for field in input_df.schema.fields:
            col_name = field.name
            # Find the matching field in the table schema (case-insensitive)
            matching_field = next(
                (
                    f
                    for f in table_schema.fields
                    if unquote_if_quoted(f.name).upper()
                    == unquote_if_quoted(col_name).upper()
                ),
                None,
            )
            target_name = (
                matching_field.name
                if matching_field is not None and matching_field.name != col_name
                else col_name
            )
            needs_cast = (
                matching_field is not None and field.datatype != matching_field.datatype
            )

            if needs_cast:
                if isinstance(matching_field.datatype, StructType):
                    select_cols.append(
                        col(col_name)
                        .cast(matching_field.datatype, rename_fields=True)
                        .alias(target_name)
                    )
                else:
                    select_cols.append(
                        col(col_name).cast(matching_field.datatype).alias(target_name)
                    )
                needs_rewrite = True
            elif target_name != col_name:
                select_cols.append(col(col_name).alias(target_name))
                needs_rewrite = True
            else:
                select_cols.append(col(col_name))
        if needs_rewrite:
            input_df = input_df.select(select_cols)
    else:
        # Case-sensitive mode: only cast to VariantType (other type mismatches handled by Snowflake)
        select_cols = []
        needs_rewrite = False
        for field in input_df.schema.fields:
            col_name = field.name
            matching_field = next(
                (
                    f
                    for f in table_schema.fields
                    if unquote_if_quoted(f.name) == unquote_if_quoted(col_name)
                ),
                None,
            )
            if (
                matching_field is not None
                and field.datatype != matching_field.datatype
                and isinstance(matching_field.datatype, VariantType)
            ):
                select_cols.append(
                    col(col_name).cast(matching_field.datatype).alias(col_name)
                )
                needs_rewrite = True
            else:
                select_cols.append(col(col_name))
        if needs_rewrite:
            input_df = input_df.select(select_cols)
    return input_df.write


def _validate_schema_for_append(
    table_schema: DataType,
    data_schema: DataType,
    snowpark_table_name: str,
    compare_structs: bool = False,
):
    match (table_schema, data_schema):
        case (_, _) if table_schema == data_schema:
            return

        case (StructType() as table_struct, StructType() as data_struct):

            def _comparable_col_name(col: str) -> str:
                name = col.upper() if auto_uppercase_column_identifiers() else col
                if compare_structs:
                    return name
                else:
                    return unquote_if_quoted(name)

            def invalid_struct_schema():
                exception = AnalysisException(
                    f"Cannot resolve columns for the existing table {snowpark_table_name} ({table_schema.simple_string()}) with the data schema ({data_schema.simple_string()})."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

            if len(table_struct.fields) != len(data_struct.fields):
                exception = AnalysisException(
                    f"The column number of the existing table {snowpark_table_name} ({table_schema.simple_string()}) doesn't match the data schema ({data_schema.simple_string()}).)"
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

            table_field_names = {
                _comparable_col_name(field.name) for field in table_struct.fields
            }
            data_field_names = {
                _comparable_col_name(field.name) for field in data_struct.fields
            }

            if table_field_names != data_field_names:
                invalid_struct_schema()

            for data_field in data_struct.fields:
                matching_table_field = next(
                    (
                        f
                        for f in table_struct.fields
                        if _comparable_col_name(f.name)
                        == _comparable_col_name(data_field.name)
                    ),
                    None,
                )

                if matching_table_field is None:
                    invalid_struct_schema()
                else:
                    _validate_schema_for_append(
                        matching_table_field.datatype,
                        data_field.datatype,
                        snowpark_table_name,
                        compare_structs=True,
                    )

            return

        case (StringType(), _) if not isinstance(
            data_schema, (StructType, ArrayType, MapType, TimestampType, DateType)
        ):
            return

        case (_, _) if isinstance(table_schema, _NumericType) and isinstance(
            data_schema, _NumericType
        ):
            return

        case (ArrayType() as table_array, ArrayType() as data_array):
            _validate_schema_for_append(
                table_array.element_type, data_array.element_type, snowpark_table_name
            )

        case (MapType() as table_map, MapType() as data_map):
            _validate_schema_for_append(
                table_map.key_type, data_map.key_type, snowpark_table_name
            )
            _validate_schema_for_append(
                table_map.value_type, data_map.value_type, snowpark_table_name
            )

        case (TimestampType(), _) if isinstance(data_schema, (DateType, TimestampType)):
            return
        case (DateType(), _) if isinstance(data_schema, (DateType, TimestampType)):
            return
        case (VariantType(), _):
            return
        case (_, _):
            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] Cannot write incompatible data for the table {snowpark_table_name}: Cannot safely cast {data_schema.simple_string()} to {table_schema.simple_string()}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception


def _validate_target_file_size(target_file_size: str | None):
    # validate target file size is in the acceptable values
    if target_file_size is None:
        return

    if target_file_size not in TARGET_FILE_SIZE_ACCEPTABLE_VALUES:
        exception = AnalysisException(
            f"Invalid value '{target_file_size}' for TARGET_FILE_SIZE. Allowed values: {', '.join(TARGET_FILE_SIZE_ACCEPTABLE_VALUES)}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception


def _build_iceberg_config(
    options: dict,
    partition_cols: list[str] | None = None,
) -> dict | None:
    config: dict = {}

    ev = options.get("external_volume") or options.get("iceberg.external_volume")
    if not ev:
        ev = sessions_config.get(get_spark_session_id(), {}).get(
            "snowpark.connect.iceberg.external_volume", None
        )
    if ev:
        config["external_volume"] = ev

    for key in ("catalog", "base_location", "storage_serialization_policy"):
        val = options.get(key) or options.get(f"iceberg.{key}")
        if val:
            config[key] = val

    if "catalog" not in config:
        config["catalog"] = "SNOWFLAKE"

    if "base_location" not in config:
        location = options.get("location")
        if location and location != "":
            config["base_location"] = location

    tfs = options.get("write.target-file-size") or options.get("target_file_size")
    if tfs:
        _validate_target_file_size(tfs)
        config["target_file_size"] = tfs

    if partition_cols:
        config["partition_by"] = partition_cols

    return config if config else None


def _is_external_catalog_error(exc: SnowparkSQLException) -> bool:
    """Return ``True`` when *exc* indicates the table belongs to an external
    catalog and therefore cannot be overwritten via CREATE OR REPLACE."""

    # Snowflake SQL error codes that indicate an external catalog table cannot be
    # overwritten via CREATE OR REPLACE (CTAS).  When we encounter these during an
    # iceberg overwrite we fall back to TRUNCATE + APPEND which preserves the
    # existing table definition (and its catalog integration).
    #   091378 – "Column specifications are only allowed for Iceberg tables using
    #            the Snowflake catalog or Iceberg tables created within a
    #            catalog-linked database."
    #   093664 – "CTAS is not supported for this table type."
    _EXTERNAL_CATALOG_OVERWRITE_ERROR_CODES = {91378, 93664}
    error_code = getattr(exc, "sql_error_code", None)
    if (
        error_code is not None
        and int(error_code) in _EXTERNAL_CATALOG_OVERWRITE_ERROR_CODES
    ):
        return True
    # Belt-and-suspenders: also match on message substrings in case the
    # numeric code is not surfaced in the exception object.
    msg = str(exc)
    return (
        "Column specifications are only allowed for Iceberg tables using the Snowflake catalog"
        in msg
        or "CTAS is not supported for this table type" in msg
        or "CREATE ICEBERG TABLE with COPY GRANTS is not supported in Catalog-Linked Databases"
        in msg
    )


def _overwrite_iceberg_with_fallback(
    writer: snowpark.DataFrameWriter,
    snowpark_table_name: str,
    iceberg_config: dict | None,
    session: snowpark.Session,
    input_df: snowpark.DataFrame | None = None,
) -> None:
    """Try a normal Snowpark ``mode='overwrite'`` (CREATE OR REPLACE).

    If the table belongs to an external catalog (Glue, Foundry, …) the
    CREATE OR REPLACE will fail. In that case we fall back to
    TRUNCATE TABLE + INSERT (mode='append') which preserves the table
    definition and its catalog integration.

    Schema evolution is not supported for external catalog tables via
    this path – the customer must ALTER the table through the external
    catalog first.

    To prevent data loss the fallback validates that the DataFrame
    schema is compatible with the target table *before* truncating.
    If the subsequent INSERT still fails for an unexpected reason
    (network error, etc.) a clear error is logged.
    """
    try:
        writer.saveAsTable(
            table_name=snowpark_table_name,
            mode="overwrite",
            column_order=_column_order_for_write,
            iceberg_config=iceberg_config,
            copy_grants=True,
        )
    except SnowparkSQLException as e:
        if _is_external_catalog_error(e):
            logger.info(
                "Overwrite failed for external-catalog iceberg table %s; "
                "falling back to TRUNCATE + APPEND.",
                snowpark_table_name,
            )

            # Validate that the DataFrame schema is compatible with the
            # target table BEFORE truncating.  Without this check a
            # schema mismatch would cause the INSERT to fail *after*
            # the TRUNCATE, leaving the table empty (data loss).
            if input_df is not None:
                try:
                    table_schema = session.table(snowpark_table_name).schema
                    _validate_schema_for_append(
                        table_schema, input_df.schema, snowpark_table_name
                    )
                except SnowparkSQLException:
                    raise
                except AnalysisException:
                    raise  # schema mismatch – fail fast, no data lost

            session.sql(f"TRUNCATE TABLE IF EXISTS {snowpark_table_name}").collect()
            writer.saveAsTable(
                table_name=snowpark_table_name,
                mode="append",
                column_order=_column_order_for_write,
                iceberg_config=iceberg_config,
            )
        else:
            raise


def _is_complex_structured_type(dt: DataType) -> bool:
    """Return True if the datatype is a structured complex type (ARRAY, MAP, STRUCT)."""
    if isinstance(dt, (ArrayType, MapType, StructType)):
        return getattr(dt, "structured", False)
    return False


def _rewrite_df_for_parquet(input_df: snowpark.DataFrame) -> snowpark.DataFrame:
    """
    Cast structured complex-type columns to VARIANT before COPY INTO.

    Snowflake's COPY INTO cannot serialize structured types (ARRAY(T), MAP(K,V),
    STRUCT) directly to Parquet — it fails with "Cannot determine equivalent
    parquet data type".  Casting to VARIANT converts the data to semi-structured
    form that Snowflake *can* write to Parquet.

    On read, the FLATTEN-based schema discovery in map_read_parquet.py detects
    VARIANT columns, infers the nested schema, and casts back to structured types.
    """
    new_cols = []
    needs_rewrite = False
    for co in input_df.columns:
        field_dt = input_df.schema[co].datatype
        if _is_complex_structured_type(field_dt):
            new_cols.append(col(co).cast(VariantType()).alias(co))
            needs_rewrite = True
        else:
            new_cols.append(col(co))

    if not needs_rewrite:
        return input_df

    return input_df.select(new_cols)


def rewrite_df(input_df: snowpark.DataFrame, source: str) -> snowpark.DataFrame:
    """
    Rewrite dataframe if needed.
        json: construct the dataframe to 1 column in json format
            1. Append columns which represents the column name
            2. Use object_construct to aggregate the dataframe into 1 column
        csv:
            Use "" to replace empty string
    """
    match source:
        case "json":
            rand_salt = random_string(10, "_")
            rewritten_df = input_df.with_columns(
                [co + rand_salt for co in input_df.columns],
                [lit(unquote_if_quoted(co)) for co in input_df.columns],
            )
            construct_key_values = []
            for co in input_df.columns:
                construct_key_values.append(col(co + rand_salt))
                construct_key_values.append(col(co))
            return rewritten_df.select(object_construct(*construct_key_values))
        case "csv":
            new_cols = []
            for co in input_df.columns:
                if isinstance(input_df.schema[co].datatype, StringType):
                    new_col = col(co)
                    new_col = when(
                        new_col.isNotNull() & (new_col == ""), lit('""')
                    ).otherwise(new_col)
                    new_cols.append(new_col.alias(co))
                else:
                    new_cols.append(col(co))
            return input_df.select(new_cols)
        case "parquet":
            return _rewrite_df_for_parquet(input_df)
        case _:
            return input_df


def handle_column_names(
    container: DataFrameContainer, source: str
) -> tuple[snowpark.DataFrame, list[str]]:
    """
    Handle column names before write so they match spark schema.

    Returns:
        A tuple of (dataframe, snowpark_column_names) where snowpark_column_names
        are the resulting column names after any renaming. Only visible columns are
        included in the output.
    """
    df = container.dataframe
    column_map = container.column_map

    if source == "jdbc":
        # don't change column names for jdbc sources as we directly use spark column names for writing to the destination tables.
        return df, column_map.get_snowpark_columns()

    snowpark_column_names = []
    for column in column_map.columns:
        new_name = quote_name_without_upper_casing(column.spark_name)
        df = df.withColumnRenamed(column.snowpark_name, new_name)
        snowpark_column_names.append(new_name)

    return df, snowpark_column_names


def _generate_metadata_files(
    source: str,
    write_path: str,
    stage_path: str,
    schema: StructType,
    session: snowpark.Session,
    parameters: dict,
    is_local_path: bool,
) -> None:
    """
    Generate marker and metadata files after write completes.

    Handles _SUCCESS marker files and Parquet _common_metadata generation
    for both local and cloud/stage paths.

    Args:
        source: Write format (csv, parquet, json, etc.)
        write_path: Original write path (local or cloud)
        stage_path: Stage path where files were written
        schema: DataFrame schema
        session: Snowpark session
        parameters: Write parameters
        is_local_path: Whether writing to local filesystem
    """
    generate_success = get_success_file_generation_enabled()
    generate_parquet_metadata = (
        source == "parquet" and get_parquet_metadata_generation_enabled()
    )

    if is_local_path:
        # Local path: write files directly
        if generate_success:
            _write_success_file_locally(write_path)
        if generate_parquet_metadata:
            _write_parquet_metadata_files_locally(write_path, schema)
    else:
        # Cloud/stage path: upload via stage operations
        if generate_success:
            _write_success_file_to_stage(stage_path, session, parameters)
        if generate_parquet_metadata:
            _upload_common_metadata_to_stage(stage_path, schema, session)


def _write_success_file_locally(directory_path: str) -> None:
    """
    Write a _SUCCESS marker file to a local directory.
    """
    try:
        success_file = Path(directory_path) / "_SUCCESS"
        success_file.touch()
        logger.debug(f"Created _SUCCESS file at {directory_path}")
    except Exception as e:
        logger.warning(f"Failed to create _SUCCESS file at {directory_path}: {e}")


def _write_success_file_to_stage(
    stage_path: str,
    session: snowpark.Session,
    parameters: dict,
) -> None:
    """
    Write a _SUCCESS marker file to a stage location.
    """
    try:
        # Create a dummy dataframe with one row containing "SUCCESS"
        success_df = session.create_dataframe([["SUCCESS"]]).to_df(["STATUS"])
        success_params = copy.deepcopy(parameters)

        success_params.pop("partition_by", None)

        success_params["location"] = f"{stage_path}/_SUCCESS"
        success_params["single"] = True
        success_params["header"] = True

        # Set CSV format with explicit no compression for _SUCCESS file
        success_params["file_format_type"] = "csv"
        success_params["format_type_options"] = {
            "COMPRESSION": "NONE",
        }

        success_df.write.copy_into_location(**success_params)

        logger.debug(f"Created _SUCCESS file at {stage_path}")
    except Exception as e:
        logger.warning(f"Failed to create _SUCCESS file at {stage_path}: {e}")


def _get_metadata_upload_sproc() -> str:
    """
    Get the cached metadata upload stored procedure.

    Returns:
        Fully qualified name of the cached stored procedure
    """
    sproc_body = """import base64
import tempfile
import os

def upload_file(session, file_content_b64: str, file_name: str, target_stage: str):
    import base64
    import tempfile
    import os

    # Decode base64 content
    file_content = base64.b64decode(file_content_b64)

    # Create temp directory and write file with exact name
    temp_dir = tempfile.mkdtemp()
    tmp_file_path = os.path.join(temp_dir, file_name)

    with open(tmp_file_path, 'wb') as f:
        f.write(file_content)

    try:
        # Use session.file.put() - works for both internal and external stages in sproc context
        result = session.file.put(
            tmp_file_path,
            target_stage,
            auto_compress=False,
            overwrite=True
        )

        # Extract status from result
        if result and len(result) > 0:
            status = result[0].status if hasattr(result[0], 'status') else str(result[0])
        else:
            status = "uploaded"

        return "Uploaded " + file_name + " Status: " + status
    finally:
        # Clean up temp files
        try:
            os.unlink(tmp_file_path)
            os.rmdir(temp_dir)
        except (OSError, IOError):
            pass"""

    # Use the cached sproc system for better performance and schema/database change handling
    return register_cached_sproc(
        sproc_body=sproc_body,
        handler_name="upload_file",
        input_arg_types=["STRING", "STRING", "STRING"],
        return_type="STRING",
        runtime_version="3.11",
        packages=["snowflake-snowpark-python"],
    )


def _upload_file_to_stage_via_sproc(
    local_file_path: Path, stage_path: str, session: snowpark.Session
) -> None:
    """
    Upload a file to a stage using the reusable stored procedure. We cannot directly use session.file.put() as it doesn't support external stages.

    Args:
        local_file_path: Local file to upload
        stage_path: Target stage path (e.g., @STAGE_NAME/path)
        session: Snowpark session
    """
    import base64

    sproc_name = _get_metadata_upload_sproc()

    with open(local_file_path, "rb") as f:
        file_content = f.read()

    file_content_b64 = base64.b64encode(file_content).decode("utf-8")
    file_name = "_common_metadata"
    session.call(sproc_name, file_content_b64, file_name, stage_path)

    logger.debug(f"Uploaded {file_name} to {stage_path} via stored procedure")


def _upload_common_metadata_to_stage(
    stage_path: str, snowpark_schema: StructType, session: snowpark.Session
) -> None:
    """
    Generate and upload _common_metadata file to a stage.

    Converts Snowpark → PySpark → Spark JSON, creates PyArrow schema with Spark metadata,
    then uploads to stage via temporary stored procedure (supports internal and external stages).

    Args:
        stage_path: Stage path where to upload _common_metadata (e.g., @STAGE/path)
        snowpark_schema: DataFrame schema (already in memory)
        session: Snowpark session for uploading
    """
    try:
        import tempfile

        spark_only_schema = _create_spark_schema_from_snowpark(snowpark_schema)

        with tempfile.NamedTemporaryFile(
            suffix="_common_metadata", delete=False
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)
            pq.write_metadata(spark_only_schema, tmp_path)
            _upload_file_to_stage_via_sproc(tmp_path, stage_path, session)
            tmp_path.unlink()

        logger.debug(f"Created _common_metadata at {stage_path}")

    except ImportError:
        logger.warning(
            "PyArrow is required to generate Parquet metadata files. "
            "Install with: pip install pyarrow"
        )
    except Exception as e:
        logger.warning(f"Failed to create _common_metadata file: {e}")


def _create_spark_schema_from_snowpark(snowpark_schema: StructType) -> pa.Schema:
    """
    Create PyArrow schema with Spark metadata from Snowpark schema.
    """
    # Unquote field names (Snowpark may have quoted names like "ab")
    unquoted_fields = []
    for field in snowpark_schema.fields:
        unquoted_name = unquote_if_quoted(field.name)
        unquoted_fields.append(
            snowpark.types.StructField(
                unquoted_name, field.datatype, field.nullable, _is_column=False
            )
        )
    unquoted_snowpark_schema = snowpark.types.StructType(
        unquoted_fields, structured=snowpark_schema.structured
    )
    pyspark_schema = map_snowpark_to_pyspark_types(unquoted_snowpark_schema)
    spark_schema_json = pyspark_schema.json()

    spark_metadata = {
        b"org.apache.spark.version": SPARK_VERSION.encode("utf-8"),
        b"org.apache.spark.sql.parquet.row.metadata": spark_schema_json.encode("utf-8"),
    }

    # Convert PySpark to PyArrow for the physical schema structure
    # NOTE: Spark reads schema from the JSON metadata above, NOT from the Parquet schema!
    # However, correct Parquet types are needed as fallback if JSON parsing fails,
    # and for compatibility with non-Spark tools (PyArrow, Dask, Presto, etc.)
    arrow_fields = []
    for field in pyspark_schema.fields:
        pa_type = map_pyspark_types_to_pyarrow_types(field.dataType)
        arrow_fields.append(pa.field(field.name, pa_type, nullable=field.nullable))

    return pa.schema(arrow_fields, metadata=spark_metadata)


def _write_parquet_metadata_files_locally(
    write_path: str, snowpark_schema: StructType
) -> None:
    """
    Generate _common_metadata file for local Parquet datasets.

    Only generates _common_metadata (not _metadata) for consistency with cloud paths,
    where downloading all files for row group statistics would be inefficient.
    """
    try:
        local_path = Path(write_path)
        spark_only_schema = _create_spark_schema_from_snowpark(snowpark_schema)
        pq.write_metadata(spark_only_schema, local_path / "_common_metadata")

        logger.debug(f"Created _common_metadata at {write_path}")

    except ImportError:
        logger.warning(
            "PyArrow is required to generate Parquet metadata files. "
            "Install with: pip install pyarrow"
        )
    except Exception as e:
        logger.warning(f"Failed to create _common_metadata file: {e}")


def store_files_locally(
    stage_path: str, target_path: str, overwrite: bool, session: snowpark.Session
) -> None:
    target_path = convert_file_prefix_path(target_path)
    real_path = (
        Path(target_path).expanduser()
        if target_path.startswith("~/")
        else Path(target_path)
    )
    if overwrite and os.path.isdir(target_path):
        _truncate_directory(real_path)
    # Per Snowflake docs: "The command does not preserve stage directory structure when transferring files to your client machine"
    # https://docs.snowflake.com/en/sql-reference/sql/get
    # Preserve directory structure under stage_path by listing files and
    # downloading each into its corresponding local subdirectory when partition subdirs exist.
    # Otherwise, fall back to a direct GET which flattens.

    # TODO(SNOW-2326973): This can be parallelized further. Its not done here because it only affects
    # write to local storage.

    ls_dataframe = session.sql(f"LS {stage_path}")
    ls_iterator = ls_dataframe.toLocalIterator()

    # Build a normalized base prefix from stage_path to compute relatives
    # Example: stage_path='@MY_STAGE/prefix' -> base_prefix='my_stage/prefix/'
    base_prefix = stage_path.lstrip("@").rstrip("/") + "/"
    base_prefix_lower = base_prefix.lower()

    # Group by parent directory under the base prefix, then issue a GET per directory.
    # This gives a small parallelism advantage if we have many files per partition directory.
    parent_dirs: set[str] = set()
    for row in ls_iterator:
        name: str = row[0]
        name_lower = name.lower()
        rel_start = name_lower.find(base_prefix_lower)
        relative = name[rel_start + len(base_prefix) :] if rel_start != -1 else name
        parent_dir = os.path.dirname(relative)
        if parent_dir and parent_dir != ".":
            parent_dirs.add(parent_dir)

    # If no parent directories were discovered (non-partitioned unload prefix), use direct GET.
    if not parent_dirs:
        snowpark.file_operation.FileOperation(session).get(stage_path, str(real_path))
        return

    file_op = snowpark.file_operation.FileOperation(session)
    for parent_dir in sorted(parent_dirs):
        local_dir = real_path / parent_dir
        if os.path.isfile(local_dir):
            temp_file_name = f"{local_dir}.tmp"
            os.rename(local_dir, temp_file_name)
            os.makedirs(local_dir, exist_ok=True)
            shutil.move(temp_file_name, f"{local_dir}/{local_dir.name}")
        else:
            os.makedirs(local_dir, exist_ok=True)

        src_dir = f"@{base_prefix}{parent_dir}"
        file_op.get(src_dir, str(local_dir))


def _truncate_directory(directory_path: Path) -> None:
    if not directory_path.exists():
        exception = FileNotFoundError(
            f"The specified directory {directory_path} does not exist."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    # Iterate over all the files and directories in the specified directory
    for file in directory_path.iterdir():
        # Check if it is a file or directory and remove it
        if file.is_file() or file.is_symlink():
            file.unlink()
        elif file.is_dir():
            shutil.rmtree(file)
