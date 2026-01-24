#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import typing

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.utils import (
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.io_utils import file_format
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def get_file_paths_from_stage(
    path: str,
    session: snowpark.Session,
) -> typing.List[str]:
    files_paths = []
    for listed_path_row in session.sql(f"LIST {path}").collect():
        # Skip _SUCCESS marker files
        if listed_path_row[0].endswith("_SUCCESS"):
            continue

        listed_path = listed_path_row[0].split("/")
        if listed_path_row[0].startswith("s3://") or listed_path_row[0].startswith(
            "s3a://"
        ):
            listed_path = listed_path[3:]
        elif listed_path_row[0].startswith("azure://"):
            listed_path = listed_path[4:]
        else:
            listed_path = listed_path[1:]
        files_paths.append("/".join(listed_path))
    return files_paths


def read_text(
    path: str,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    options: typing.MutableMapping[str, str],
) -> snowpark.DataFrame:
    # TODO: handle stage name with double quotes
    files_paths = get_file_paths_from_stage(path, session)
    # Remove matching quotes from both ends of the path to get the stage name, if present.
    if path and len(path) > 1 and path[0] == path[-1] and path[0] in ('"', "'"):
        unquoted_path = path[1:-1]
    else:
        unquoted_path = path
    stage_name = unquoted_path.split("/")[0]
    line_sep = options.get("lineSep") or "\n"
    column_name = (
        schema[0].name if schema is not None and len(schema.fields) > 0 else '"value"'
    )
    default_column_name = "TEXT"

    result = []
    separator = (
        None if options.get("wholetext", "False").lower() == "true" else line_sep
    )
    text_file_format = file_format(
        session, options.get("compression", "auto"), separator
    )
    for fp in files_paths:
        content = session.sql(
            f"SELECT T.$1 AS {default_column_name} FROM '{stage_name}/{fp}' (FILE_FORMAT => {text_file_format}) AS T"
        ).collect()
        for row in content:
            result.append(row[0])
    return session.createDataFrame(result, [column_name])


def map_read_text(
    rel: relation_proto.Relation,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    paths: list[str],
) -> DataFrameContainer:
    """
    Read a TEXT file into a Snowpark DataFrame.
    """
    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for CSV files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    df = read_text(paths[0], schema, session, rel.read.data_source.options)
    if len(paths) > 1:
        for p in paths[1:]:
            df = df.union_all(
                read_text(
                    p,
                    schema,
                    session,
                    rel.read.data_source.options,
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
