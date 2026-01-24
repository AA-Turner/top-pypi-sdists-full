#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures
import json
import logging
import os
import re
from pathlib import Path

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    convert_file_prefix_path,
    get_compression_for_source_and_options,
    is_cloud_path,
)
from snowflake.snowpark_connect.relation.neo4j_utils import (
    transform_neo4j_to_jdbc_options,
)
from snowflake.snowpark_connect.relation.read.map_read_table import map_read_table
from snowflake.snowpark_connect.relation.read.reader_config import (
    CsvReaderConfig,
    JsonReaderConfig,
    ParquetReaderConfig,
)
from snowflake.snowpark_connect.relation.stage_locator import get_paths_from_stage
from snowflake.snowpark_connect.type_mapping import (
    _parse_ddl_with_spark_scala,
    map_json_schema_to_snowpark,
)
from snowflake.snowpark_connect.utils.cache import df_cache_map_put_if_absent
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)

logger = logging.getLogger("snowflake_connect_server")


def map_read(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Read a file into a Snowpark DataFrame.

    Currently, the supported read formats are `csv`, `json` and `parquet`.
    """

    match rel.read.WhichOneof("read_type"):
        case "named_table":
            return map_read_table_or_file(rel)

        case "data_source":
            read_format = None
            if rel.read.data_source.HasField("format"):
                read_format = rel.read.data_source.format
            else:
                read_format = global_config.get("spark.sql.sources.default")
                if read_format is not None:
                    read_format = read_format.split(".")[-1]

            if not read_format:
                # TODO: This should come from the config `spark.sql.sources.default`
                # The default format is parquet, but users can override it.
                read_format = "parquet"

            if read_format.lower() == "iceberg":
                telemetry.report_io_read("iceberg")
                return map_read_table(rel)

            if rel.read.data_source.schema == "":
                schema = None
            else:
                try:
                    parsed_schema = json.loads(rel.read.data_source.schema)
                except json.JSONDecodeError:
                    # Scala clients send DDL-formatted strings like
                    # "billing_account_id STRING, cost STRING" or "struct<id:bigint>"
                    spark_datatype = _parse_ddl_with_spark_scala(
                        rel.read.data_source.schema
                    )
                    parsed_schema = json.loads(spark_datatype.json())
                schema = map_json_schema_to_snowpark(parsed_schema)
            options = dict(rel.read.data_source.options)
            telemetry.report_io_read(read_format)
            session: snowpark.Session = get_or_create_snowpark_session()
            if len(rel.read.data_source.paths) > 0:
                if options.get("path"):
                    raise AnalysisException(
                        "There is a 'path' or 'paths' option set and load() is called with path parameters. "
                        "Either remove the path option if it's the same as the path parameter, "
                        "or add it to the load() parameter if you do want to read multiple paths."
                    )
                # Normalize paths to ensure consistent behavior
                clean_source_paths = [
                    path if is_cloud_path(path) else str(Path(path))
                    for path in rel.read.data_source.paths
                ]

                result = _read_file(
                    clean_source_paths, options, read_format, rel, schema, session
                )
            else:
                match read_format:
                    case "socket":
                        from snowflake.snowpark_connect.relation.read.map_read_socket import (
                            map_read_socket,
                        )

                        return map_read_socket(rel, session, options)

                    case "jdbc":
                        from snowflake.snowpark_connect.relation.read.map_read_jdbc import (
                            map_read_jdbc,
                        )

                        return map_read_jdbc(rel, session, options)

                    case "org.neo4j.spark.DataSource":
                        from snowflake.snowpark_connect.relation.read.map_read_jdbc import (
                            map_read_jdbc,
                        )

                        # Transform Neo4j Spark Connector options to JDBC options
                        # See neo4j_utils.py for pros/cons of this approach
                        jdbc_options = transform_neo4j_to_jdbc_options(options, "read")
                        return map_read_jdbc(rel, session, jdbc_options)
                    case "net.snowflake.spark.snowflake":
                        options = {k.lower(): v for k, v in options.items()}
                        QUERY_OPTION = "query"
                        DBTABLE_OPTION = "dbtable"

                        def _identifiers_match(
                            desired: str, current: str | None
                        ) -> bool:
                            if current is None:
                                return False

                            desired_unquoted = unquote_if_quoted(desired)
                            current_unquoted = unquote_if_quoted(current)
                            desired_was_quoted = desired != desired_unquoted

                            # If both are quoted, exact match required. session.get* always returns quoted identifier
                            # name.
                            if desired_was_quoted:
                                return desired == current

                            return desired_unquoted.upper() == current_unquoted

                        if "sfrole" in options:
                            desired_role = options["sfrole"]
                            current_role = session.get_current_role()
                            if not _identifiers_match(desired_role, current_role):
                                logger.warning(
                                    f"Changing Role from {current_role} to {desired_role} via "
                                    "options. This will change the role for the entire session."
                                )
                                session.use_role(desired_role)

                        if "sfwarehouse" in options:
                            desired_warehouse = options["sfwarehouse"]
                            current_warehouse = session.get_current_warehouse()
                            if not _identifiers_match(
                                desired_warehouse, current_warehouse
                            ):
                                logger.warning(
                                    f"Changing Warehouse from {current_warehouse} to {desired_warehouse} via "
                                    "options. This will change the warehouse for the entire session."
                                )
                                session.use_warehouse(desired_warehouse)

                        if "sfdatabase" in options:
                            desired_database = options["sfdatabase"]
                            current_database = session.get_current_database()
                            if not _identifiers_match(
                                desired_database, current_database
                            ):
                                logger.warning(
                                    f"Changing Database from {current_database} to {desired_database} via "
                                    "options. This will change the database for the entire session."
                                )
                                session.use_database(desired_database)

                        if "sfschema" in options:
                            desired_schema = options["sfschema"]
                            current_schema = session.get_current_schema()
                            if not _identifiers_match(desired_schema, current_schema):
                                logger.warning(
                                    f"Changing Schema from {current_schema} to {desired_schema} via "
                                    "options. This will change the schema for the entire session."
                                )
                                session.use_schema(desired_schema)
                        if QUERY_OPTION in options.keys():
                            from .map_read_table import get_table_from_query

                            return get_table_from_query(
                                options[QUERY_OPTION], session, rel.common.plan_id
                            )
                        elif DBTABLE_OPTION in options.keys():
                            from .map_read_table import get_table_from_name

                            return get_table_from_name(
                                options[DBTABLE_OPTION], session, rel.common.plan_id
                            )
                    case other:
                        exception = SnowparkConnectNotImplementedError(
                            f"UNSUPPORTED FORMAT {other} WITH NO PATH"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
        case other:
            # TODO: Empty data source
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported read type: {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    return df_cache_map_put_if_absent(
        (get_spark_session_id(), rel.common.plan_id), lambda: result
    )


def map_read_table_or_file(rel) -> DataFrameContainer:
    read_named_table_from_file = (
        rel.read.named_table.unparsed_identifier
        and _get_supported_read_file_format(rel.read.named_table.unparsed_identifier)
    )
    if read_named_table_from_file:
        # This case handles when user reads the file using the raw SQL
        schema = None
        read_format = _get_supported_read_file_format(
            rel.read.named_table.unparsed_identifier
        )
        options = {}
        telemetry.report_io_read(read_format)
        session: snowpark.Session = get_or_create_snowpark_session()

        clean_source_paths = [
            re.sub(
                rf"^{read_format}\.`([^`]+)`$",
                r"\1",
                rel.read.named_table.unparsed_identifier,
            ).rstrip("/")
        ]

        return _read_file(
            clean_source_paths, options, read_format, rel, schema, session
        )
    else:
        return map_read_table(rel)


def _get_supported_read_file_format(unparsed_identifier: str) -> str | None:
    if unparsed_identifier.startswith("csv.`"):
        return "csv"
    elif unparsed_identifier.startswith("json.`"):
        return "json"
    elif unparsed_identifier.startswith("parquet.`"):
        return "parquet"
    elif unparsed_identifier.startswith("text.`"):
        return "text"
    return None


# TODO: [SNOW-2465948] Remove this once Snowpark fixes the issue with stage paths.
class StagePathStr(str):
    def partition(self, __sep):
        if str(self)[0] == "'":
            return str(self)[1:].partition(__sep)
        return str(self).partition(__sep)


def _quote_stage_path(stage_path: str) -> str:
    """
    Quote stage paths to escape any special characters.
    """
    if stage_path.startswith("@"):
        return StagePathStr(f"'{stage_path}'")
    return stage_path


def _read_file(
    clean_source_paths: list[str],
    options: dict,
    read_format: str,
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
) -> DataFrameContainer:
    paths = get_paths_from_stage(
        clean_source_paths,
        session,
    )
    upload_files_if_needed(paths, clean_source_paths, session, read_format)
    paths = [_quote_stage_path(path) for path in paths]

    if read_format in ("csv", "text", "json", "parquet"):
        compression = get_compression_for_source_and_options(
            read_format, options, from_read=True
        )
        if compression is not None:
            options["compression"] = compression

    match read_format:
        case "csv":
            from snowflake.snowpark_connect.relation.read.map_read_csv import (
                map_read_csv,
            )

            return map_read_csv(rel, schema, session, paths, CsvReaderConfig(options))
        case "json":
            from snowflake.snowpark_connect.relation.read.map_read_json import (
                map_read_json,
            )

            # JSON already materializes the table internally
            return map_read_json(
                rel, schema, session, paths, JsonReaderConfig(options)
            ).without_materialization()

        case "parquet":
            from snowflake.snowpark_connect.relation.read.map_read_parquet import (
                map_read_parquet,
            )

            return map_read_parquet(
                rel, schema, session, paths, ParquetReaderConfig(options)
            )
        case "text":
            from snowflake.snowpark_connect.relation.read.map_read_text import (
                map_read_text,
            )

            return map_read_text(rel, schema, session, paths)
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported format: {read_format}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _skip_upload(path: str, read_format: str):
    """
    Determines whether to skip the upload of a file based on its format.
    :param path: The path to the file.
    :param read_format: The format for reading. Parquet formatting implies additional file skipping logic.
    :return: True if the upload should be skipped, False otherwise.
    """
    if read_format == "parquet":
        # Skip uploading files that are not parquet
        return not path.endswith(".parquet")
    return False


def upload_files_if_needed(
    stage_target_paths: list[str],
    source_paths: list[str],
    session: snowpark.Session,
    read_format: str,
) -> None:
    """
    Uploads file to stage if needed, preserving the underlying directory structure.
    For parquet, the most common issue is a _SUCCESS.gz that causes reading to fail.
    :param stage_target_paths: The paths to the staged files. They should be equal to the source_paths but with the stage name prefixed.
    :param source_paths: The paths to the source files.
    :param session: The Snowpark session.
    :param read_format: The format for reading. Parquet formatting implies additional file skipping logic.
    """

    assert len(source_paths) == len(
        stage_target_paths
    ), "Source and target paths must have same length"

    def _upload_dir(target: str, source: str) -> None:
        # overwrite=True will not remove all stale files in the target prefix
        # Quote the target path to allow special characters.
        remove_command = f"REMOVE '{target}/'"
        assert (
            "//" not in remove_command
        ), f"Remove command {remove_command} contains double slash"
        session.sql(remove_command).collect()

        try:
            # Walk through all subdirectories
            for root, dirs, files in os.walk(source):
                if not files:
                    continue

                rel_path = os.path.relpath(root, source)

                curr_target = target
                if rel_path != ".":
                    curr_target = f"{curr_target}/{rel_path}"

                # If there are no directories, and this is not parquet where we need to filter files,
                # we can use * to upload all files
                if not dirs and read_format != "parquet":
                    file_pattern = os.path.join(root, "*")
                    # Ensure target ends with single slash
                    pattern_target = f"{curr_target}/"
                    try:
                        session.file.put(
                            file_pattern,
                            pattern_target,
                            auto_compress=False,
                            overwrite=True,
                        )
                    except Exception as e:
                        logger.error(
                            f"Error uploading files {file_pattern} to {target}: {e}"
                        )
                        raise
                # Otherwise, we need to upload files individually. Uploading with * pattern fails if the pattern
                # matches a directory.from
                else:
                    for file in files:
                        file_path = os.path.join(root, file)
                        if _skip_upload(file_path, read_format):
                            continue
                        # Avoid double slashes in target path
                        file_target = f"{curr_target}/{file}"
                        try:
                            session.file.put(
                                file_path,
                                file_target,
                                auto_compress=False,
                                overwrite=True,
                            )
                        except Exception as e:
                            logger.error(
                                f"Error uploading file {file_path} to {target}: {e}"
                            )
                            raise
        except Exception as e:
            logger.error(f"Error uploading directory {source} to {target}: {e}")
            raise

    def _upload_file(target: str, source: str) -> None:
        # Extract the directory from target path for PUT
        # target is like "@stage_name/dir/file.csv", we need "@stage_name/dir/"
        target_dir = "/".join(target.split("/")[:-1]) + "/"
        session.file.put(source, target_dir, auto_compress=False, overwrite=True)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=4, thread_name_prefix="LocalFileUploader_"
    ) as exc:
        futures = []

        for source_path, target_path in zip(source_paths, stage_target_paths):
            if is_cloud_path(source_path):
                continue

            source_path = convert_file_prefix_path(source_path)
            # Upload local files
            # since local files are the source of truth
            # any existing files should be overwritten in the target prefix
            if os.path.isdir(source_path):
                futures.append(exc.submit(_upload_dir, target_path, source_path))
            else:
                futures.append(exc.submit(_upload_file, target_path, source_path))

        # Check for exceptions - if we don't do this, they will be lost in the thread.
        for future in concurrent.futures.as_completed(futures):
            future.result()
