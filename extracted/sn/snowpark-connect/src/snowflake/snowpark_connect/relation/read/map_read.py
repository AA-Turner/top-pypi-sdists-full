#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures
import glob
import json
import logging
import os
import re
from pathlib import Path

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    build_input_file_name_uri_prefix,
    collapse_redundant_slashes,
    convert_file_prefix_path,
    get_compression_for_source_and_options,
    infer_compression_from_file_extension,
    is_cloud_path,
    preserve_trailing_slash,
    unescape_glob_metacharacters,
)
from snowflake.snowpark_connect.relation.neo4j_utils import (
    transform_neo4j_to_jdbc_options,
)
from snowflake.snowpark_connect.relation.read.map_read_table import map_read_table
from snowflake.snowpark_connect.relation.read.metadata_utils import populate_metadata
from snowflake.snowpark_connect.relation.read.modification_time_filter import (
    consume_modified_time_filters,
    empty_file_read_result,
    expand_paths_for_modification_time_filter,
)
from snowflake.snowpark_connect.relation.read.partition_pruning import (
    get_hive_partition_pruning_hint,
    should_skip_read_cache_for_pruning,
)
from snowflake.snowpark_connect.relation.read.path_anchoring import (
    _HIVE_PARTITION_DIR_RE,
    PathClassification,
    classify_source_path,
    consume_recursive_file_lookup,
    inject_anchor_pattern,
    split_glob_scan_prefix,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    CsvReaderConfig,
    JsonReaderConfig,
    ParquetReaderConfig,
    XmlReaderConfig,
)
from snowflake.snowpark_connect.relation.stage_locator import get_paths_from_stage
from snowflake.snowpark_connect.relation.utils import (
    assert_sf_connector_context_matches,
)
from snowflake.snowpark_connect.type_mapping import (
    _parse_ddl_with_spark_scala,
    map_json_schema_to_snowpark,
)
from snowflake.snowpark_connect.utils.cache import df_cache_map_put_if_absent
from snowflake.snowpark_connect.utils.context import (
    get_should_skip_file_read_cache_result,
    get_spark_session_id,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)

logger = logging.getLogger("snowflake_connect_server")


def _parse_data_source_schema(
    rel: relation_proto.Relation, read_format: str
) -> StructType | None:
    if rel.read.data_source.schema == "":
        return None
    try:
        parsed_schema = json.loads(rel.read.data_source.schema)
    except json.JSONDecodeError:
        # Scala clients send DDL-formatted strings like
        # "billing_account_id STRING, cost STRING" or "struct<id:bigint>"
        spark_datatype = _parse_ddl_with_spark_scala(rel.read.data_source.schema)
        parsed_schema = json.loads(spark_datatype.json())
    # For XML format, don't quote schema field names because Snowpark
    # will quote them internally, leading to double-quoting
    quote_fields = read_format.lower() != "xml"
    return map_json_schema_to_snowpark(
        parsed_schema, quote_struct_fields_names=quote_fields
    )


def _read_file_from_data_source(
    rel: relation_proto.Relation,
    session: snowpark.Session,
    clean_source_paths: list[str],
    options: dict,
    read_format: str,
) -> DataFrameContainer:
    """Read paths for a data_source relation (used by partition-pruning rule)."""
    schema = _parse_data_source_schema(rel, read_format)
    return _read_file(clean_source_paths, options, read_format, rel, schema, session)


def map_read(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Read a file into a Snowpark DataFrame.

    Currently, the supported read formats are `csv`, `json`, `parquet`, `text`, and `xml`.
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
                telemetry.report_io_read("iceberg", dict(rel.read.data_source.options))
                return map_read_table(rel)

            schema = _parse_data_source_schema(rel, read_format)
            options = dict(rel.read.data_source.options)
            telemetry.report_io_read(read_format, options)
            session: snowpark.Session = get_or_create_snowpark_session()
            if len(rel.read.data_source.paths) > 0:
                if options.get("path"):
                    raise AnalysisException(
                        "There is a 'path' or 'paths' option set and load() is called with path parameters. "
                        "Either remove the path option if it's the same as the path parameter, "
                        "or add it to the load() parameter if you do want to read multiple paths."
                    )
                # Normalize paths to ensure consistent behavior
                # Unescape glob metacharacters for local paths (e.g., \[abc\] -> [abc])
                # Spark allows escaping glob metacharacters with backslashes.
                # Preserve a user-supplied trailing slash so downstream code
                # can distinguish directory paths from file paths even after
                # `Path(...)` normalization (SNOW-3428536). Collapse redundant
                # slashes so cloud/stage paths match Spark (SNOW-3585393).
                clean_source_paths = [
                    _normalize_read_source_path(path)
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
                    case "net.snowflake.spark.snowflake" | "snowflake":
                        options = {k.lower(): v for k, v in options.items()}
                        QUERY_OPTION = "query"
                        DBTABLE_OPTION = "dbtable"

                        # Reads return a lazy DataFrame — the SQL is not sent to
                        # Snowflake until the client triggers an action (collect,
                        # show, …).  Mutating session context here would leave
                        # the lazy plan evaluating against the wrong context.
                        # Instead: sfUser/sfRole/sfWarehouse must match the session
                        # (error otherwise); sfDatabase/sfSchema must also match
                        # (error with FQN instruction otherwise).
                        assert_sf_connector_context_matches(session, options)
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

    if get_should_skip_file_read_cache_result():
        # SNOW-3262791: If the result of this read will be persisted by saveAsTable, do not cache the result.
        result = result.without_materialization()

    if should_skip_read_cache_for_pruning():
        # Pruned reads are filter-specific; caching under the read plan_id would
        # poison later unfiltered reads of the same Read relation (SNOW-3295586).
        return result

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
        telemetry.report_io_read(read_format, options)
        session: snowpark.Session = get_or_create_snowpark_session()

        # Preserve any trailing slash in the SQL-quoted path so the read
        # path classifier can tell directories from files (SNOW-3428536).
        clean_source_paths = [
            _normalize_read_source_path(
                re.sub(
                    rf"^{read_format}\.`([^`]+)`$",
                    r"\1",
                    rel.read.named_table.unparsed_identifier,
                )
            )
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


def _normalize_read_source_path(path: str) -> str:
    """Normalize a read source path for stage mapping and INFER_SCHEMA.

    Collapses redundant slashes (SNOW-3585393). For local paths, also
    unescapes glob metacharacters and preserves a user trailing slash
    (SNOW-3428536).
    """
    original = path
    collapsed = collapse_redundant_slashes(path)
    if is_cloud_path(collapsed):
        return collapsed
    return preserve_trailing_slash(
        original,
        str(Path(unescape_glob_metacharacters(collapsed))),
    )


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


def _resolve_read_compression(
    stage_paths: list[str],
    clean_source_paths: list[str],
    read_format: str,
    options: dict,
    session: snowpark.Session,
) -> None:
    """Resolve the compression option for reads.

    If the user explicitly set a compression option, use it. Otherwise, infer
    from file extensions. For types Snowflake's AUTO can detect (GZIP, BZ2),
    we skip the override to avoid interfering with format-specific readers.
    """
    user_compression = get_compression_for_source_and_options(
        read_format, options, from_read=True
    )
    if user_compression is not None:
        options["compression"] = user_compression
        return

    compression = infer_compression_from_file_extension(stage_paths, read_format)

    # For directory paths (no file extension), scan actual filenames to infer
    # compression. Skip this for specific file paths — Snowflake's LIST treats
    # paths as prefixes, so listing "file.jsonl" would also match
    # "file.jsonl.gz", "file.jsonl.bz2", etc.
    if compression == "AUTO" and _paths_are_directories(clean_source_paths):
        source_files = _list_local_files(clean_source_paths)
        if not source_files:
            source_files = _list_stage_files(stage_paths, session)
        if source_files:
            compression = infer_compression_from_file_extension(
                source_files, read_format
            )

    if compression not in ("AUTO", "GZIP", "BZ2"):
        options["compression"] = compression


def _paths_are_directories(source_paths: list[str]) -> bool:
    """Check if source paths look like directories (no file extension)."""
    from os.path import splitext

    for path in source_paths:
        _, ext = splitext(path.rstrip("/"))
        if ext:
            return False
    return True


def _list_local_files(source_paths: list[str]) -> list[str]:
    """List filenames from local directories in source_paths."""
    files: list[str] = []
    for src in source_paths:
        if os.path.isdir(src):
            files.extend(os.listdir(src))
    return files


def _list_stage_files(stage_paths: list[str], session: snowpark.Session) -> list[str]:
    """List filenames on a Snowflake stage via LIST command."""
    files: list[str] = []
    for path in stage_paths:
        cleaned = path.strip("'\"").replace("'", "\\'")
        try:
            for row in session.sql(f"LIST '{cleaned}'").collect():
                name = row[0]
                if not name.endswith("_SUCCESS"):
                    files.append(name)
        except Exception as e:
            logger.warning(f"Failed to list stage files at '{cleaned}': {e}")
    return files


def _read_file(
    clean_source_paths: list[str],
    options: dict,
    read_format: str,
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
) -> DataFrameContainer:
    read_format = read_format.lower()

    # Capture the file-metadata opt-in before format readers consume options.
    needs_file_metadata = populate_metadata(options)

    pruning_hint = get_hive_partition_pruning_hint()
    if pruning_hint is not None:
        clean_source_paths = list(pruning_hint.pruned_clean_source_paths)

    # Pop recursiveFileLookup once and route the resolved semantics to
    # local-upload depth, PATTERN injection, and partition discovery.
    # Single consumption point guarantees the option never reaches
    # Snowflake's COPY INTO regardless of which downstream branch is taken.
    recursive_lookup = consume_recursive_file_lookup(options)
    is_recursive = recursive_lookup.is_recursive
    skip_partition_discovery = recursive_lookup.skip_partition_discovery

    path_classifications = [
        classify_source_path(source_path) for source_path in clean_source_paths
    ]

    paths = get_paths_from_stage(
        clean_source_paths,
        session,
    )
    upload_files_if_needed(
        paths,
        clean_source_paths,
        session,
        read_format,
        recursive=is_recursive,
        path_classifications=path_classifications,
    )

    # Snowflake stage operations use prefix matching. A read from
    # "@stage/dir" also matches "@stage/dir_v2/file.csv". Appending a
    # trailing slash ensures the reader only picks up files directly
    # inside the intended directory and not sibling directories whose
    # names share the same prefix (SNOW-3428536). Glob reads use the
    # longest non-glob scan prefix the same way (SNOW-3594869).
    paths = [
        path + "/"
        if classification.kind in ("dir", "glob") and not path.endswith("/")
        else path
        for classification, path in zip(path_classifications, paths)
    ]

    paths = [_quote_stage_path(path) for path in paths]

    if read_format in ("csv", "text", "json", "parquet"):
        _resolve_read_compression(
            paths, clean_source_paths, read_format, options, session
        )

    # Mod-time expansion LISTs files and selects explicit paths. Run before
    # inject_anchor_pattern so the injected pathGlobFilter regex is not
    # mistaken for a user glob during LIST filtering.
    mod_filters = consume_modified_time_filters(options, session)
    mod_time_expanded_paths = False
    if mod_filters.is_active:
        paths = expand_paths_for_modification_time_filter(
            paths,
            session,
            mod_filters,
            read_format=read_format,
            is_recursive=is_recursive,
            clean_source_paths=clean_source_paths,
            path_classifications=path_classifications,
            options=options,
        )
        if paths:
            mod_time_expanded_paths = True
            # Explicit file paths make pathGlobFilter/PATTERN redundant and can
            # cause COPY INTO to match zero files when the regex shape differs.
            for key in list(options.keys()):
                if key.lower() in ("pathglobfilter", "pattern"):
                    options.pop(key)
        else:
            return empty_file_read_result(read_format, rel, schema, session)

    # Anchor file/glob reads via PATTERN so Snowflake's stage prefix
    # matching cannot pull in siblings with extra suffixes (e.g.
    # ``data.json.gz`` next to ``data.json``). When the user set
    # ``recursiveFileLookup=false``, the same call also restricts dir
    # branches to depth-0 -- both filters are joined into one PATTERN
    # so there's no override race between them. See SNOW-3428536 /
    # SNOW-3295580 and ``relation.read.path_anchoring`` for details.
    if not mod_time_expanded_paths:
        inject_anchor_pattern(
            clean_source_paths,
            options,
            read_format,
            path_classifications,
            is_recursive=is_recursive,
        )

    match read_format:
        case "csv":
            from snowflake.snowpark_connect.relation.read.map_read_csv import (
                map_read_csv,
            )

            result = map_read_csv(
                rel,
                schema,
                session,
                paths,
                CsvReaderConfig(options),
                skip_partition_discovery=skip_partition_discovery,
            )
        case "json":
            from snowflake.snowpark_connect.relation.read.map_read_json import (
                map_read_json,
            )

            # JSON already materializes the table internally
            result = map_read_json(
                rel,
                schema,
                session,
                paths,
                JsonReaderConfig(options),
                skip_partition_discovery=skip_partition_discovery,
            ).without_materialization()

        case "parquet":
            from snowflake.snowpark_connect.relation.read.map_read_parquet import (
                map_read_parquet,
            )

            result = map_read_parquet(
                rel,
                schema,
                session,
                paths,
                ParquetReaderConfig(options),
                skip_partition_discovery=skip_partition_discovery,
            )
        case "text":
            from snowflake.snowpark_connect.relation.read.map_read_text import (
                map_read_text,
            )

            result = map_read_text(
                rel,
                schema,
                session,
                paths,
                recursive=is_recursive,
                skip_partition_discovery=skip_partition_discovery,
                list_filter_source_paths=clean_source_paths,
                clean_source_paths=clean_source_paths,
                path_classifications=path_classifications,
            )
        case "xml":
            from snowflake.snowpark_connect.relation.read.map_read_xml import (
                map_read_xml,
            )

            # XML uses Snowpark's UDTF-based reader which materializes by default
            result = map_read_xml(
                rel,
                schema,
                session,
                paths,
                XmlReaderConfig(options),
                is_recursive=is_recursive,
            ).without_materialization()
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported format: {read_format}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    # GAP-014 / SNOW-3295582: rewrite the stage-relative METADATA$FILENAME into
    # Spark's full source URI so input_file_name() matches Spark. Only when the
    # user opted in to file metadata and we can reconstruct an unambiguous prefix
    # from the original source paths; otherwise the stage-relative value is as-is.
    if needs_file_metadata:
        uri_prefix = build_input_file_name_uri_prefix(clean_source_paths)
        if uri_prefix is not None:
            result = result.with_rewritten_metadata_filename(uri_prefix)

    return result


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


def _glob_scan_prefix_norm(source_glob: str) -> str:
    scan_prefix, _ = split_glob_scan_prefix(source_glob)
    scan_prefix_local = (
        convert_file_prefix_path(scan_prefix) if scan_prefix else os.getcwd()
    )
    return os.path.normpath(scan_prefix_local)


def _glob_expanded_local_files(source_glob: str, *, recursive: bool) -> list[str]:
    """Expand a local glob path to concrete files.

    ``recursiveFileLookup`` depth pruning applies to directory reads, not glob
    paths -- the glob metacharacters already bound which files match (see
    ``compute_non_recursive_pattern`` docstring on file/glob kinds).
    """
    _ = recursive
    local_glob = convert_file_prefix_path(source_glob)
    return sorted(
        path for path in glob.glob(local_glob, recursive=True) if os.path.isfile(path)
    )


def _remove_stage_prefix(session: snowpark.Session, target: str) -> str:
    """Clear a session temp-stage subprefix before re-uploading local files.

    ``target`` is the mapped upload prefix under the per-session temp stage
    created by ``StageLocator`` (``@spark_connect_stage_local_*``), not a
    user ``@stage`` path. The local glob pattern (e.g. ``*.csv``) is expanded
    client-side and never appears in the REMOVE command.
    """
    target = target.rstrip("/")
    remove_command = f"REMOVE '{target}/'"
    assert (
        "//" not in remove_command
    ), f"Remove command {remove_command} contains double slash"
    session.sql(remove_command).collect()
    return target


def upload_files_if_needed(
    stage_target_paths: list[str],
    source_paths: list[str],
    session: snowpark.Session,
    read_format: str,
    *,
    recursive: bool = True,
    path_classifications: list[PathClassification] | None = None,
) -> None:
    """
    Uploads file to stage if needed, preserving the underlying directory structure.
    For parquet, the most common issue is a _SUCCESS.gz that causes reading to fail.
    :param stage_target_paths: The paths to the staged files. They should be equal to the source_paths but with the stage name prefixed.
    :param source_paths: The paths to the source files.
    :param session: The Snowpark session.
    :param read_format: The format for reading. Parquet formatting implies additional file skipping logic.
    :param recursive: When False, only top-level files in local directories are uploaded (SNOW-3295580).
    """

    assert len(source_paths) == len(
        stage_target_paths
    ), "Source and target paths must have same length"

    if path_classifications is None:
        path_classifications = [classify_source_path(p) for p in source_paths]

    def _upload_glob(target: str, source_glob: str) -> None:
        files = _glob_expanded_local_files(source_glob, recursive=recursive)
        if not files:
            exception = AnalysisException(
                f"Path does not exist: {convert_file_prefix_path(source_glob)}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
            raise exception

        target = _remove_stage_prefix(session, target)

        scan_prefix_norm = _glob_scan_prefix_norm(source_glob)

        for file_path in files:
            if _skip_upload(file_path, read_format):
                continue
            rel_path = os.path.relpath(file_path, scan_prefix_norm)
            rel_dir = os.path.dirname(rel_path)
            if rel_dir and rel_dir != ".":
                file_dir_target = f"{target}/{rel_dir.replace(os.sep, '/')}/"
            else:
                file_dir_target = f"{target}/"
            try:
                session.file.put(
                    glob.escape(file_path),
                    file_dir_target,
                    auto_compress=False,
                    overwrite=True,
                )
            except Exception as e:
                logger.error(f"Error uploading glob match {file_path} to {target}: {e}")
                raise

    def _upload_dir(target: str, source: str) -> None:
        # Tolerate a dir-marker trailing slash on `target` (preserved from
        # the user input by `preserve_trailing_slash`) so we don't end up
        # with a double slash in the REMOVE / PUT paths (SNOW-3428536).
        target = _remove_stage_prefix(session, target)

        try:
            # Walk through all subdirectories (or only depth-0 when recursive=False).
            # ``topdown=True`` lets us prune ``dirs`` in place so os.walk skips
            # subtrees instead of descending into them just to ``continue``.
            for root, dirs, files in os.walk(source, topdown=True):
                # Capture whether THIS directory has subdirectories before
                # we mutate ``dirs`` for the recursive=False prune. The
                # glob-based ``*`` upload below relies on the directory
                # being subdirectory-free (otherwise ``session.file.put``
                # raises "Not a file but a directory" on the subdir
                # entries the glob picks up).
                dir_had_subdirs = bool(dirs)
                if not recursive:
                    # Depth-0 files plus Hive ``key=value/`` segments at any
                    # depth. Spark still reads partition subdirs when
                    # ``recursiveFileLookup=false``; arbitrary nesting is
                    # suppressed (SNOW-3295580 / SNOW-3566246).
                    dirs[:] = [d for d in dirs if _HIVE_PARTITION_DIR_RE.fullmatch(d)]
                if not files:
                    continue

                rel_path = os.path.relpath(root, source)

                curr_target = target
                if rel_path != ".":
                    curr_target = f"{curr_target}/{rel_path}"

                # If there are no directories, and this is not parquet where we need to filter files,
                # we can use * to upload all files
                if not dir_had_subdirs and read_format != "parquet":
                    # Escape glob metacharacters in the directory path to prevent
                    # characters like [ ] { } from being interpreted as glob patterns
                    file_pattern = os.path.join(glob.escape(root), "*")
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
                # matches a directory.
                else:
                    # ``session.file.put`` interprets a target without a
                    # trailing slash as a directory and appends the source
                    # basename, so passing the full ``curr_target/<file>``
                    # would land the file at ``curr_target/<file>/<file>``.
                    # Use the directory target (with trailing slash) and let
                    # PUT re-use the source basename -- mirrors
                    # ``_upload_file`` below.
                    file_dir_target = f"{curr_target}/"
                    for file in files:
                        file_path = os.path.join(root, file)
                        if _skip_upload(file_path, read_format):
                            continue
                        try:
                            # Escape glob metacharacters in the file path to prevent
                            # characters like [ ] { } from being interpreted as glob patterns
                            session.file.put(
                                glob.escape(file_path),
                                file_dir_target,
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
        target_dir = os.path.dirname(target)
        if target_dir:
            target_dir = target_dir + "/"
        else:
            # No directory in path, use the original target
            target_dir = target
        # Escape glob metacharacters in the source path to prevent
        # characters like [ ] { } from being interpreted as glob patterns
        session.file.put(
            glob.escape(source), target_dir, auto_compress=False, overwrite=True
        )

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=4, thread_name_prefix="LocalFileUploader_"
    ) as exc:
        futures = []

        for i, (source_path, target_path) in enumerate(
            zip(source_paths, stage_target_paths)
        ):
            if is_cloud_path(source_path):
                continue

            local_source = convert_file_prefix_path(source_path)
            classification = path_classifications[i]
            if classification.kind == "glob":
                futures.append(exc.submit(_upload_glob, target_path, local_source))
            elif os.path.isdir(local_source):
                futures.append(exc.submit(_upload_dir, target_path, local_source))
            else:
                futures.append(exc.submit(_upload_file, target_path, local_source))

        # Check for exceptions - if we don't do this, they will be lost in the thread.
        for future in concurrent.futures.as_completed(futures):
            future.result()
