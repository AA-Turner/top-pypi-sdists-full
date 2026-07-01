#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Shared directory-vs-file resolution for the file readers.

Every reader receives a list of quoted stage paths that the read layer
(``map_read._read_file``) has already classified as either a single file or a
*directory prefix* (directory paths carry a trailing slash). This module is the
single source of truth for:

* :func:`is_directory_stage_path` — the trailing-slash directory predicate,
  shared by every format (CSV, JSON, Parquet, Text, XML) so the rule for "is
  this path a directory?" lives in one place.
* :func:`generate_stage_path_groups_for_read` — the multi-path
  ``INFER_SCHEMA`` / ``COPY INTO`` grouping used by the COPY-based formats
  (CSV, JSON, Parquet). Each directory prefix becomes its own single-path group
  so it takes the recurse-from-prefix branch instead of being collapsed into a
  ``FILES=[...]`` list of directory names (SNOW-3591574).
* :func:`expand_dir_to_stage_files` — the ``LIST``-based directory expansion
  used by the formats that load file-by-file (Text).
"""

from __future__ import annotations

from snowflake import snowpark
from snowflake.snowpark_connect.relation.read.utils import (
    cloud_list_path_to_relative,
    extract_stage_from_path,
    generate_stage_path_groups,
)


def detach_infer_schema_options(
    options: dict, *, files: list[str] | None = None
) -> dict:
    """Return a copy of ``options`` with a fresh ``INFER_SCHEMA_OPTIONS`` dict.

    Snowpark's ``INFER_SCHEMA`` resolves a directory prefix to a concrete file
    list and writes it back into ``INFER_SCHEMA_OPTIONS["FILES"]`` *in place*.
    The reader options are reused across per-directory groups, so a single
    shared inner dict would leak one group's resolved ``FILES`` into the next
    group and make it infer against the wrong files (SNOW-3591574).

    This always returns a fresh outer dict **and** a fresh inner
    ``INFER_SCHEMA_OPTIONS`` dict, preserving any other inner keys (e.g.
    ``ON_ERROR``). When ``files`` is given, ``INFER_SCHEMA_OPTIONS["FILES"]`` is
    set to it; otherwise the inner dict is left for snowpark to populate. This
    is the single idiom every COPY/INFER-based reader (CSV, JSON, Parquet) uses
    so the private-copy fix cannot drift between call sites.
    """
    inner = dict(options.get("INFER_SCHEMA_OPTIONS") or {})
    if files is not None:
        inner["FILES"] = files
    return {**options, "INFER_SCHEMA_OPTIONS": inner}


def is_directory_stage_path(path: str) -> bool:
    """Whether a quoted stage path denotes a directory prefix, not a single file.

    Precondition: ``path`` must already have been classified by
    ``classify_source_path`` (via ``map_read._read_file``), which stats the
    filesystem for non-stage paths and appends a trailing slash to every path it
    classified as ``kind == "dir"`` before quoting. This predicate only checks
    that trailing-slash marker — it does **not** stat the filesystem — so it
    returns wrong answers for unclassified inputs (e.g. a local directory or a
    bare ``@stage/dir`` cloud directory path without a trailing slash). Always
    route paths through ``classify_source_path`` before calling this.
    """
    return path.strip("'").endswith("/")


def generate_stage_path_groups_for_read(
    paths: list[str],
) -> list[tuple[str, list[str]]]:
    """Group quoted stage paths for multi-path ``INFER_SCHEMA`` / ``COPY INTO``.

    Like :func:`~snowflake.snowpark_connect.relation.read.utils.generate_stage_path_groups`,
    but each **directory-prefix** path (trailing slash) is kept in its own
    single-path group instead of being batched together with sibling
    directories.

    Downstream readers treat a single-path group as a stage *prefix* (Snowpark
    ``reader.csv(prefix)`` / ``COPY INTO ... FROM prefix``), which Snowflake
    recurses into to find the data files. Batching multiple directories into one
    group instead routes them through the ``FILES=[...]`` parameter, which only
    accepts explicit file names — so the directory names match nothing and the
    read silently yields an empty result. Isolating each directory lets
    ``spark.read.json([dir1, dir2])`` / ``spark.read.csv([dir1, dir2])`` infer
    and load each directory independently and union the results, matching
    PySpark (SNOW-3591574).

    Explicit file paths keep the original per-stage batching so a single
    ``INFER_SCHEMA`` / ``COPY INTO`` call still covers many files.

    Group order follows the user-supplied input order: a run of explicit files
    is flushed (per-stage batched) before each directory group it precedes.
    Spark merges schemas in input order (first-seen column casing / nullability
    wins, types are then widened), so preserving order keeps the merged column
    order and casing aligned with Spark for mixed ``read([file, dir])`` inputs.

    No cross-group de-duplication is performed: every input path is read
    independently and the results are unioned. Passing the same directory
    twice, or a directory together with files it already contains, therefore
    reads those rows more than once. This matches Spark, which also does not
    de-duplicate the scan — it flat-maps over the input ``rootPaths`` (the
    listing cache only de-dupes the catalog, not the scan), so a parent dir
    plus a file inside it counts that file twice (SNOW-3591574).
    """
    result: list[tuple[str, list[str]]] = []
    pending_files: list[str] = []

    def flush_pending_files() -> None:
        if pending_files:
            result.extend(generate_stage_path_groups(pending_files))
            pending_files.clear()

    for path in paths:
        if is_directory_stage_path(path):
            # Emit the preceding run of explicit files before this directory so
            # the unioned/merged result preserves user-supplied input order.
            flush_pending_files()
            result.append((extract_stage_from_path(path), [path]))
        else:
            pending_files.append(path)
    flush_pending_files()
    return result


def expand_dir_to_stage_files(
    path: str,
    session: snowpark.Session,
    *,
    skip_success_markers: bool = True,
) -> list[str]:
    """Expand a stage path into its concrete stage-relative file paths via ``LIST``.

    Snowflake's ``LIST`` is always recursive and returns rows rooted at the
    cloud bucket (``s3://bucket/...``, ``gcs://bucket/...``,
    ``azure://account.host/container/...``) or the stage name. This strips that
    leading component so callers get paths relative to the stage root
    (e.g. ``dir/file.txt``), which is the shape Text's ``SELECT ... FROM
    '@stage/<relative>'`` reads expect.

    ``skip_success_markers`` drops Spark's ``_SUCCESS`` sentinel files. Depth /
    hidden-file filtering for ``recursiveFileLookup=false`` is left to the
    caller because it depends on the input path depth.
    """
    file_paths: list[str] = []
    for listed_path_row in session.sql(f"LIST {path}").collect():
        listed = listed_path_row[0]
        if skip_success_markers and listed.endswith("_SUCCESS"):
            continue

        relative = cloud_list_path_to_relative(listed)
        if relative is None:
            # Stage-name-rooted path (e.g. ``stage/dir/file``): drop the leading
            # stage-name component.
            relative = "/".join(listed.split("/")[1:])
        file_paths.append(relative)
    return file_paths
