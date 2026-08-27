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

from collections.abc import Callable
from itertools import chain

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
    path_filter: Callable[[str], bool] | None = None,
    max_results: int | None = None,
) -> list[str]:
    """Expand a stage path into its concrete stage-relative file paths via ``LIST``.

    Snowflake's ``LIST`` is always recursive and returns rows rooted at the
    cloud bucket (``s3://bucket/...``, ``gcs://bucket/...``,
    ``azure://account.host/container/...``) or the stage name. This strips that
    leading component so callers get paths relative to the stage root
    (e.g. ``dir/file.txt``), which is the shape Text's ``SELECT ... FROM
    '@stage/<relative>'`` reads expect.

    For a **named external stage** whose URL carries a non-root prefix
    (``CREATE STAGE ... URL='s3://bucket/<prefix>'``), the ``LIST`` rows still
    include ``<prefix>``. Stripping only scheme+bucket would leave ``<prefix>``
    in the "relative" path, so the per-file ``SELECT ... FROM '@stage/<rel>'``
    would re-root under the stage and double-count the prefix — reading nothing
    (SNOW-3723843). We therefore resolve the stage's own URL via
    ``DESCRIBE STAGE`` and strip that full prefix (matching on the bucket+key
    portion with the scheme ignored, so an ``s3://`` vs ``s3a://`` or trailing-slash
    difference between ``LIST`` and ``DESCRIBE STAGE`` still matches), yielding a
    genuinely stage-relative path -- the shape
    ``path_anchoring._stage_relative_list_prefix`` (used by the non-recursive / glob
    filters) expects. Internal stages (no URL) and direct cloud paths fall back to
    the scheme+bucket strip.

    ``skip_success_markers`` drops Spark's ``_SUCCESS`` sentinel files. Depth /
    hidden-file filtering for ``recursiveFileLookup=false`` is left to the
    caller because it depends on the input path depth.

    When ``path_filter`` or ``max_results`` is supplied, rows are streamed so an
    existence check can stop after its first qualifying path instead of collecting
    an arbitrarily large directory listing. Default callers retain the original
    eager-list behavior.
    """
    from snowflake.snowpark_connect.relation.io_utils import (
        get_stage_url_prefix,
        is_external_cloud_url,
    )

    if max_results is not None:
        if max_results < 0:
            raise ValueError("max_results must be non-negative")
        if max_results == 0:
            return []

    listed_dataframe = session.sql(f"LIST {path}")
    if path_filter is None and max_results is None:
        listed_rows = listed_dataframe.collect()
        first_row = listed_rows[0] if listed_rows else None
        has_external_cloud_rows = any(
            is_external_cloud_url(row[0]) for row in listed_rows
        )
    else:
        listed_iterator = iter(listed_dataframe.to_local_iterator())
        first_row = next(listed_iterator, None)
        listed_rows = chain(() if first_row is None else (first_row,), listed_iterator)
        # One LIST result set has one root shape; inspecting the first row avoids
        # consuming the streaming iterator before filtering can stop early.
        has_external_cloud_rows = first_row is not None and is_external_cloud_url(
            first_row[0]
        )

    # Only a named *external* stage needs its own URL prefix stripped: its LIST
    # rows are rooted at the stage's cloud URL (bucket + the stage's prefix), and
    # stripping just scheme+bucket would leave that prefix behind (SNOW-3723843).
    # Internal stages list stage-name-rooted paths, so gate the DESCRIBE STAGE
    # lookup on the LIST output actually being cloud-rooted -- this skips a wasted
    # round-trip on the common internal-stage path and only pays it when it can
    # change the result.
    #
    # We match on the bucket+key portion with the scheme dropped so a scheme
    # difference between LIST and DESCRIBE STAGE (e.g. ``s3://`` vs ``s3a://``) or
    # a trailing slash cannot cause a silent miss that falls back to the broken
    # scheme+bucket strip.
    stage_url_rest: str | None = None
    stripped_path = path
    if (
        len(stripped_path) >= 2
        and stripped_path[0] == stripped_path[-1]
        and stripped_path[0] in ("'", '"')
    ):
        stripped_path = stripped_path[1:-1]
    if stripped_path.startswith("@") and has_external_cloud_rows:
        stage_name = stripped_path[1:].split("/", 1)[0]
        stage_url = get_stage_url_prefix(stage_name, session)
        if stage_url and is_external_cloud_url(stage_url):
            stage_url_rest = stage_url.split("://", 1)[-1].strip("/")

    file_paths: list[str] = []
    for listed_path_row in listed_rows:
        listed = listed_path_row[0]
        if skip_success_markers and listed.endswith("_SUCCESS"):
            continue

        relative: str | None = None
        if stage_url_rest:
            # External stage with a URL prefix: strip the full stage URL (scheme
            # ignored) so the path is relative to the stage root, not the bucket.
            listed_rest = listed.split("://", 1)[-1]
            if listed_rest.startswith(stage_url_rest + "/"):
                relative = listed_rest[len(stage_url_rest) + 1 :]
        if relative is None:
            relative = cloud_list_path_to_relative(listed)
            if relative is None:
                # Stage-name-rooted path (e.g. ``stage/dir/file``): drop the
                # leading stage-name component.
                relative = "/".join(listed.split("/")[1:])
        if path_filter is not None and not path_filter(relative):
            continue
        file_paths.append(relative)
        if max_results is not None and len(file_paths) >= max_results:
            break
    return file_paths
