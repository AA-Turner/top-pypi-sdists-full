#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import typing

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark.types import (
    DataType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _extract_partitions_from_path,
    discover_partition_columns_if_recursive,
)
from snowflake.snowpark_connect.relation.read.path_anchoring import (
    PathClassification,
    consume_recursive_file_lookup,
    filter_list_paths_for_non_recursive_read,
    listed_path_matches_glob_suffix,
)
from snowflake.snowpark_connect.relation.read.source_resolution import (
    expand_dir_to_stage_files,
)
from snowflake.snowpark_connect.relation.read.utils import (
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.io_utils import (
    db_schema_from_stage_path,
    file_format,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def _coerce_partition_value(value: str, datatype: DataType) -> str | int | float:
    if isinstance(datatype, IntegerType):
        return int(value)
    if isinstance(datatype, DoubleType):
        return float(value)
    return value


def get_file_paths_from_stage(
    path: str,
    session: snowpark.Session,
) -> typing.List[str]:
    """List the files under a stage path as stage-relative paths.

    Thin wrapper over the shared :func:`expand_dir_to_stage_files` so the
    ``LIST`` + bucket-strip + ``_SUCCESS`` skip logic stays consistent across
    formats. Depth / hidden-file filtering for ``recursiveFileLookup=false``
    is applied by :func:`read_text`.
    """
    return expand_dir_to_stage_files(path, session)


def read_text(
    path: str,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    options: typing.MutableMapping[str, str],
    *,
    recursive: bool = True,
    skip_partition_discovery: bool = False,
    list_filter_path: str | None = None,
    clean_source_path: str | None = None,
    path_classification: PathClassification | None = None,
) -> snowpark.DataFrame:
    # TODO: handle stage name with double quotes
    files_paths = get_file_paths_from_stage(path, session)
    # Remove matching quotes from both ends of the path to get the stage name, if present.
    if path and len(path) > 1 and path[0] == path[-1] and path[0] in ('"', "'"):
        unquoted_path = path[1:-1]
    else:
        unquoted_path = path
    stage_name = unquoted_path.split("/")[0]

    partition_columns, partition_types = discover_partition_columns_if_recursive(
        session, path, "text", skip_partition_discovery=skip_partition_discovery
    )

    if (
        path_classification is not None
        and path_classification.kind == "glob"
        and clean_source_path is not None
        and path_classification.regex is not None
    ):
        files_paths = [
            fp
            for fp in files_paths
            if listed_path_matches_glob_suffix(
                fp, clean_source_path, path_classification.regex
            )
        ]

    if not recursive:
        files_paths = filter_list_paths_for_non_recursive_read(
            files_paths,
            list_filter_path if list_filter_path is not None else unquoted_path,
        )
    # Handle both camelCase (lineSep) and lowercase (linesep) option names
    line_sep = options.get("lineSep") or options.get("linesep") or "\n"
    column_name = (
        schema[0].name if schema is not None and len(schema.fields) > 0 else '"value"'
    )
    default_column_name = "TEXT"

    result: list[tuple[typing.Any, ...]] = []
    separator = (
        None if options.get("wholetext", "False").lower() == "true" else line_sep
    )
    text_file_format = file_format(
        session,
        options.get("compression", "auto"),
        separator,
        db_schema_fallback=db_schema_from_stage_path(path),
    )
    for fp in files_paths:
        content = session.sql(
            f"SELECT T.$1 AS {default_column_name} FROM '{stage_name}/{fp}' (FILE_FORMAT => {text_file_format}) AS T"
        ).collect()
        path_partitions = _extract_partitions_from_path(fp)
        for row in content:
            row_values: list[typing.Any] = [row[0]]
            for part_col in partition_columns:
                raw = path_partitions.get(part_col, None)
                if raw is None:
                    row_values.append(None)
                else:
                    row_values.append(
                        _coerce_partition_value(raw, partition_types[part_col])
                    )
            result.append(tuple(row_values))

    if partition_columns:
        fields = [StructField(column_name, StringType(), True)]
        for part_col in partition_columns:
            fields.append(StructField(part_col, partition_types[part_col], True))
        return session.createDataFrame(result, schema=StructType(fields))
    return session.createDataFrame(result, [column_name])


def map_read_text(
    rel: relation_proto.Relation,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    paths: list[str],
    *,
    recursive: bool | None = None,
    skip_partition_discovery: bool = False,
    list_filter_source_paths: list[str] | None = None,
    clean_source_paths: list[str] | None = None,
    path_classifications: list[PathClassification] | None = None,
) -> DataFrameContainer:
    """
    Read a TEXT file into a Snowpark DataFrame.

    ``recursive`` is normally supplied by ``map_read._read_file`` after it
    consumed ``recursiveFileLookup`` from the protobuf options; pass
    ``None`` (or omit) to fall back to a self-contained scan of
    ``rel.read.data_source.options`` for the standalone test entry path.
    """
    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for CSV files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    raw_options = dict(rel.read.data_source.options)
    if recursive is None:
        lookup = consume_recursive_file_lookup(raw_options)
        recursive = lookup.is_recursive
        skip_partition_discovery = lookup.skip_partition_discovery

    filter_paths = list_filter_source_paths or paths
    df = read_text(
        paths[0],
        schema,
        session,
        raw_options,
        recursive=recursive,
        skip_partition_discovery=skip_partition_discovery,
        list_filter_path=filter_paths[0],
        clean_source_path=(clean_source_paths[0] if clean_source_paths else None),
        path_classification=(path_classifications[0] if path_classifications else None),
    )
    if len(paths) > 1:
        for idx, p in enumerate(paths[1:], start=1):
            df = df.union_all(
                read_text(
                    p,
                    schema,
                    session,
                    raw_options,
                    recursive=recursive,
                    skip_partition_discovery=skip_partition_discovery,
                    list_filter_path=filter_paths[idx],
                    clean_source_path=(
                        clean_source_paths[idx] if clean_source_paths else None
                    ),
                    path_classification=(
                        path_classifications[idx] if path_classifications else None
                    ),
                )
            )

    spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)

    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=renamed_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[
            emulate_integral_types(f.datatype) for f in df.schema.fields
        ],
    )
