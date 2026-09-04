#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Source Parquet rows from Snowflake **Parquet Direct** (loose-parquet Iceberg table).

Enabled via the ``snowpark.connect.parquet_direct.enabled`` Spark config (default off). Eligible
sources are either named external ``@stage`` parquet paths, or raw AWS ``s3://`` paths read with
**role-based** S3 credentials (``AWS_ROLE`` + SSE-KMS) — in that mode SCOS mints a role-based
external stage over the bucket and PD reads through it. Either way the data already lives in cloud
storage, so **nothing is uploaded**. Key/credential-based S3 stages are rejected server-side for
PD (099223), and ``azure://``/``gcs://``/local paths use the normal read path (see
``can_use_parquet_direct``).

Integration contract: SCOS's existing schema-inference is left **unchanged** — it still computes
the final schema (``discovered_schema`` / user ``schema``, honoring mergeSchema, first-file
semantics, etc.). This module only replaces the *data read* that happens afterwards: for each
distinct source ``(stage, sub-path)`` it creates a loose-parquet Iceberg table (all declared with
the SAME merged column set), ``UNION ALL``-s the per-table reads, then **projects those rows onto
SCOS's already-computed final schema** — including Hive **partition columns** (parsed from
``METADATA$FILENAME``) and the ``METADATA$FILENAME`` **metadata column** (for
``input_file_name()``). A single source path degenerates to one table and no UNION.

The table is created with ``PARQUET_DIRECT_EXTERNAL_STAGE=<stage>`` and **no** ``EXTERNAL_VOLUME``
or ``CATALOG``: the backend auto-provisions the catalog integration (SNOW-3748550, GS #477724) and
a hidden external volume nested under the temp table (SNOW-3748549), so no user-created catalog
integration / external volume and no ``ACCOUNTADMIN`` are required. The stage MUST be a
storage-integration-backed external stage with supported encryption; an incompatible stage raises a
clear, actionable error (``_ensure_pd_table``) rather than silently falling back.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

import snowflake.snowpark as snowpark

if TYPE_CHECKING:
    from snowflake.snowpark_connect.relation.read.path_anchoring import (
        PathClassification,
    )
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark.functions import lit, nullif, split_part
from snowflake.snowpark.types import (
    DataType,
    StringType,
    TimestampTimeZone,
    TimestampType,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
)
from snowflake.snowpark_connect.relation.read.utils import (
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# Parquet Direct tables are created in the session's CURRENT schema (no hardcoded db/schema)
# with a random suffix, as session-scoped TEMPORARY iceberg tables (SNOW-3748552; auto-on for
# SCOS sessions via ENABLE_TEMPORARY_PARQUET_DIRECT_TABLE_FOR_SCOS) so they are auto-reclaimed at
# session end — no manual drop/cleanup. Storage + catalog are auto-provisioned by the backend from
# the user's external stage (PARQUET_DIRECT_EXTERNAL_STAGE) — there is no external volume, catalog
# integration, bucket, or upload stage to configure.
PD_TABLE_PREFIX = "SCOS_PD_"


def _esc_sql_literal(s: str) -> str:
    """Double single-quotes so a user-controlled value is safe inside a SQL string literal.

    Stage keys / sub-paths can legitimately contain apostrophes (e.g. ``dir's data/``); without
    escaping, the value terminates the literal early and the CREATE ICEBERG DDL fails to parse.
    """
    return s.replace("'", "''")


# Server compilation errors raised when a stage cannot back a Parquet Direct table
# (099219 no storage provider, 099220 no resolvable location, 099221 unsupported encryption,
# 099222 not storage-integration-backed, 099223 credential/key-based integration-less stage —
# PD accepts only storage-integration-backed or role-based stages). With PD on by default, a user
# pointing at any of these external stages hits PD, so we catch all of them and surface a clear,
# actionable error instead of the raw server code.
_PD_INCOMPATIBLE_STAGE_ERRORS = ("099219", "099220", "099221", "099222", "099223")


class PdDirectContext:
    """Carries ONE Parquet Direct table's source scope (data already in cloud storage) and the
    lazily-created table for it. A read may have several of these — one per distinct source path —
    UNION ALL-ed together by ``pd_direct_container``. The scope uses the SAME primitives COPY INTO does:

      * ``file_path`` — a literal prefix within the stage (``FILE_PATH``); "" = stage root.
      * ``pattern`` — a server-side ``PATTERN`` regex: set for **glob** and **explicit-file** sources
        (the anchored regex from :func:`compute_anchor_pattern`, matched against the full
        stage-relative path — its file branch matches a named file OR a directory's contents) and for
        a **non-recursive directory** (a depth-0 regex from :func:`compute_non_recursive_pattern`).
        ``None`` for a recursive directory (FILE_PATH prefix alone).
    """

    def __init__(
        self,
        stage: str,
        file_path: str,
        pattern: str | None = None,
    ) -> None:
        self.stage = stage  # stage name WITHOUT leading '@', e.g. DB.SCHEMA.STAGE
        self.file_path = (
            file_path  # sub-path within the stage (FILE_PATH); "" = stage root
        )
        self.pattern = pattern  # server-side PATTERN regex; None = no PATTERN filter
        self.table: str | None = None


def parquet_direct_enabled() -> bool:
    """True when the ``snowpark.connect.parquet_direct.enabled`` Spark config is on."""
    from snowflake.snowpark_connect.config import global_config

    return bool(
        getattr(global_config, "snowpark_connect_parquet_direct_enabled", False)
    )


def _pd_force_eligible() -> bool:
    """Test-only: ``SCOS_PD_TEST=force`` bypasses per-read source eligibility so Parquet Direct is
    attempted on **every** parquet read regardless of source kind/creds.

    Used by the PD differential test harness / CI job to force the PD path for coverage; reads
    whose source genuinely cannot back PD (internal stage, key-based creds, azure/gcs) then error
    at ``prepare``/CREATE time, and the harness records that test as PD-incapable. NEVER set in
    production — the env var is absent there, so this is a no-op and normal eligibility applies.
    """
    import os

    return os.environ.get("SCOS_PD_TEST", "").strip().lower() == "force"


def _is_stage_source(path: str) -> bool:
    return path.strip().startswith("@")


def _all_stage_sources_external(
    session: snowpark.Session, clean_source_paths: list[str]
) -> bool:
    """True only if every ``@stage`` source is an EXTERNAL stage (``DESCRIBE STAGE`` reports a
    non-empty ``URL``).

    Only external, storage-integration-backed stages can back Parquet Direct. Internal stages
    (``PUT``-populated, no URL) cannot, and must fall through to the **normal** read path rather
    than error — with PD on by default, claiming an internal stage eligible turns an ordinary
    read into a hard failure (server 099219-099222 -> ValueError in ``_ensure_pd_table``). One
    ``DESCRIBE STAGE`` per distinct stage; any internal/undescribable stage makes the whole read
    ineligible for PD.
    """
    from snowflake.snowpark.functions import col, lit

    checked: dict[str, bool] = {}
    for path in clean_source_paths:
        name = path.strip().lstrip("@").split("/", 1)[0]
        if not name:
            return False
        if name not in checked:
            try:
                rows = (
                    session.sql(f"DESCRIBE STAGE {name}")
                    .filter(col('"property"') == lit("URL"))
                    .collect()
                )
                checked[name] = bool(rows) and rows[0]["property_value"] not in (
                    "",
                    None,
                )
            except Exception as e:
                logger.debug(
                    "DESCRIBE STAGE %s failed (%s); treating as PD-ineligible", name, e
                )
                checked[
                    name
                ] = False  # undescribable -> treat as PD-ineligible, fall back
        if not checked[name]:
            return False
    return True


def _is_aws_s3_source(path: str) -> bool:
    """True for a raw AWS S3 URL (``s3://`` / ``s3a://`` / ``s3n://``)."""
    return path.strip().strip("'\"").lower().startswith(("s3://", "s3a://", "s3n://"))


def _s3_bucket_relative(path: str) -> str | None:
    """Bucket-relative sub-path of an S3 URL, PRESERVING any trailing slash and glob suffix.

    ``s3://bkt/dir/*.parquet`` -> ``dir/*.parquet``; ``s3://bkt/dir/`` -> ``dir/``;
    ``s3://bkt/f.parquet`` -> ``f.parquet``; ``s3://bkt`` / ``s3://bkt/`` -> ``""`` (bucket root).
    ``None`` if ``path`` is not an S3 URL.
    """
    p = path.strip().strip("'\"")
    for scheme in ("s3://", "s3a://", "s3n://"):
        if p[: len(scheme)].lower() == scheme:
            rest = p[len(scheme) :]
            return rest.split("/", 1)[1] if "/" in rest else ""
    return None


def _session_is_aws_role_based(session: snowpark.Session) -> bool:
    """True when the Spark session's S3 credentials are AWS_ROLE-based (not access keys).

    Mirrors ``StageLocator.get_and_maybe_create_stage`` exactly: SCOS mints a role-based
    (``CREDENTIALS=(AWS_ROLE=…)``) stage only when access/secret keys are ABSENT and an
    assumed-role ARN + SSE-KMS key are present (keys take precedence). Parquet Direct requires a
    role-based stage — the server rejects a key/credential-based stage for
    ``PARQUET_DIRECT_EXTERNAL_STAGE`` (099223) — so direct-S3 PD is eligible only in this mode.
    """
    from snowflake.snowpark_connect.config import sessions_config
    from snowflake.snowpark_connect.utils.context import get_spark_session_id

    cred = sessions_config.get(get_spark_session_id(), None)
    if not cred:
        return False

    def _set(key: str) -> bool:
        v = cred.get(key)
        return v is not None and str(v).strip() != ""

    keys_present = _set("spark.hadoop.fs.s3a.access.key") and _set(
        "spark.hadoop.fs.s3a.secret.key"
    )
    role_present = _set("spark.hadoop.fs.s3a.assumed.role.arn") and _set(
        "spark.hadoop.fs.s3a.server-side-encryption.key"
    )
    return role_present and not keys_present


class PdReadReason:
    """Reason codes for a parquet read's path decision (emitted as PD read-path telemetry).

    ``ELIGIBLE`` means the sources qualify for Parquet Direct; every other value is why PD was
    NOT used for this read. ``EXTERNAL_TABLE_BRANCH`` is the opt-in single-path external-table read
    (a legitimate non-PD path). There is deliberately no "eligible but not prepared" reason: an
    eligible read goes through PD or raises (``map_read``) — it never silently falls back.
    """

    ELIGIBLE = "ELIGIBLE"  # sentinel: qualifies for PD (not emitted as a skip reason)
    PD_USED = "PD_USED"  # the read actually materialized rows through Parquet Direct
    CONFIG_DISABLED = (
        "CONFIG_DISABLED"  # snowpark.connect.parquet_direct.enabled is off
    )
    NO_PATHS = "NO_PATHS"
    INTERNAL_STAGE = "INTERNAL_STAGE"  # @stage source(s) not external (no URL)
    KEY_BASED_CREDS = "KEY_BASED_CREDS"  # raw s3 but access-key (not role-based) creds
    SOURCE_NOT_ELIGIBLE = (
        "SOURCE_NOT_ELIGIBLE"  # azure/gcs/local, or mixed source kinds
    )
    EXTERNAL_TABLE_BRANCH = (
        "EXTERNAL_TABLE_BRANCH"  # single-path external-table read, not PD
    )
    # Note: there is deliberately no "eligible but not prepared" reason. An eligible read either
    # goes through Parquet Direct or raises (see map_read.py) — it never silently falls back.


def parquet_direct_read_reason(
    session: snowpark.Session, clean_source_paths: list[str]
) -> str:
    """Return why a parquet read is/ isn't Parquet-Direct-eligible (a ``PdReadReason``).

    ``ELIGIBLE`` when the config is on AND the sources are either all named external ``@stage``
    paths, or all raw AWS ``s3://`` with role-based creds (``AWS_ROLE`` + SSE-KMS, no access keys).
    Everything else returns the specific reason PD is skipped. This is the single source of truth
    for the source-classification decision; :func:`can_use_parquet_direct` and the PD read-path
    telemetry both derive from it.

    Contract: an ``ELIGIBLE`` read goes through Parquet Direct or raises — it never silently falls
    back to the normal read path (the caller in ``map_read`` raises if a PD context cannot be built;
    an incompatible stage raises later at ``pd_direct_container`` CREATE time). The opt-in
    single-path external-table read is classified ``EXTERNAL_TABLE_BRANCH`` by the caller (a
    legitimate non-PD path, not a failure).
    """
    if not parquet_direct_enabled():
        return PdReadReason.CONFIG_DISABLED
    if not clean_source_paths:
        return PdReadReason.NO_PATHS
    if _pd_force_eligible():
        # Test-only (SCOS_PD_TEST=force): bypass source classification and attempt PD on every
        # parquet read. Ineligible sources surface a clear error at prepare/CREATE time, which the
        # PD differential harness records as "PD-incapable" (excluded from the eligible set).
        return PdReadReason.ELIGIBLE
    if all(_is_stage_source(p) for p in clean_source_paths):
        # Only EXTERNAL stages can back Parquet Direct. Internal (PUT-populated) stages must fall
        # back to the normal read path, not error — otherwise PD-on-by-default breaks every
        # internal-stage parquet read (099219-099222). See _all_stage_sources_external.
        return (
            PdReadReason.ELIGIBLE
            if _all_stage_sources_external(session, clean_source_paths)
            else PdReadReason.INTERNAL_STAGE
        )
    if all(_is_aws_s3_source(p) for p in clean_source_paths):
        return (
            PdReadReason.ELIGIBLE
            if _session_is_aws_role_based(session)
            else PdReadReason.KEY_BASED_CREDS
        )
    # azure://, gcs://, local, or a mix of source kinds
    return PdReadReason.SOURCE_NOT_ELIGIBLE


def can_use_parquet_direct(
    session: snowpark.Session, clean_source_paths: list[str]
) -> bool:
    """Parquet Direct is eligible when :func:`parquet_direct_read_reason` returns ``ELIGIBLE``.

    See that function for the full rule (config on + all-external-stage OR all-s3-role-based).
    """
    return (
        parquet_direct_read_reason(session, clean_source_paths) == PdReadReason.ELIGIBLE
    )


def resolve_parquet_direct_read(
    session: snowpark.Session,
    clean_source_paths: list[str],
    paths: list[str],
    path_classifications: list[PathClassification] | None = None,
    *,
    is_recursive: bool = True,
    path_glob_filter: str | None = None,
) -> tuple[str, list[PdDirectContext] | None]:
    """The single, authoritative Parquet-Direct routing decision for a parquet read.

    Returns ``(pd_read_reason, pd_direct)`` where ``pd_direct`` is the prepared PD context list (used
    by :func:`map_read_parquet`) or ``None``. The decision is made exactly once, here, so nothing
    downstream re-decides PD-vs-not:

      * ``EXTERNAL_TABLE_BRANCH`` — the opt-in single-path external-table read (``paths[0]`` +
        :func:`use_external_table`); a legitimate, kept non-PD path. Classified up front so PD is
        never prepared-then-discarded. ``use_external_table`` short-circuits when
        ``external_table_location()`` is ``None`` (the default), so no extra ``DESCRIBE STAGE`` in
        the common case, and it uses the same single-path condition as
        :func:`map_read_parquet`'s Branch A, so the two cannot disagree.
      * ``ELIGIBLE`` — the read goes through Parquet Direct, or **raises**. If a PD context cannot be
        built for an eligible source (unexpected for a genuine external-``@stage`` / role-based-s3
        source; reachable only for a bypassed or pathological source), we raise instead of silently
        reading via the normal path — an eligible read must never quietly skip PD.
      * any other reason — the normal COPY/INFER read path (``pd_direct`` is ``None``).
    """
    # Local import avoids a module-load import cycle (map_read_partitioned_file imports PD helpers).
    from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
        use_external_table,
    )

    pd_read_reason = parquet_direct_read_reason(session, clean_source_paths)
    if (
        pd_read_reason == PdReadReason.ELIGIBLE
        and len(paths) == 1
        and use_external_table(session, paths[0])
    ):
        pd_read_reason = PdReadReason.EXTERNAL_TABLE_BRANCH
    if pd_read_reason != PdReadReason.ELIGIBLE:
        return pd_read_reason, None
    pd_direct = prepare_parquet_direct(
        session,
        clean_source_paths,
        path_classifications,
        is_recursive=is_recursive,
        path_glob_filter=path_glob_filter,
    )
    if pd_direct is None:
        raise ValueError(
            f"Parquet Direct is eligible for {clean_source_paths} but a Parquet Direct read could "
            f"not be prepared for these sources. Refusing to silently fall back to the "
            f"non-Parquet-Direct read path. Disable 'snowpark.connect.parquet_direct.enabled' to "
            f"use the normal read path, or point at a compatible external stage / role-based S3 "
            f"source."
        )
    return pd_read_reason, pd_direct


# A PATTERN that no real stage-relative file path can equal, used to scope a Parquet Direct table to
# ZERO files (an explicit file excluded by a user pathGlobFilter) so it reads empty rather than
# falling back to the normal path. Snowflake PATTERN is a full match against the FILE_PATH-relative
# path; no object key equals this sentinel.
_PD_NEVER_MATCH_PATTERN = "__SCOS_PD_NO_FILE_MATCHES__"


def _stage_path_is_directory(session: snowpark.Session, stage_path: str) -> bool:
    """Whether a no-trailing-slash ``@stage`` path is a directory (has children) vs a lone file.

    A path string carries no reliable file-vs-directory signal in object storage -- Spark writes
    directories named ``x.parquet``, so neither the extension nor a missing trailing slash is a tell.
    The only source of truth is storage: ``LIST '<path>/'`` returns the objects strictly beneath
    ``<path>``, and the trailing slash makes it prefix-collision-safe (``foo/`` never matches a
    sibling ``foo2``). The path is a directory iff at least one child exists. Only the FIRST row is
    read (streamed, not collected), so the cost is one listing page regardless of how many files the
    directory holds. On any listing error we return ``False`` so the caller keeps the file anchor
    (bounded to the path) and never over-reads.
    """
    listing = (stage_path.rstrip("/") + "/").replace("'", "\\'")
    try:
        for _ in session.sql(f"LIST '{listing}'").to_local_iterator():
            return True
        return False
    except Exception:
        return False


def _pattern_matches_basename(pattern: str, stage_path: str) -> bool:
    """Whether a user ``pathGlobFilter`` (a Snowflake regex) full-matches the path's basename.

    Used only for a genuine single file, where pathGlobFilter is a within-file filter (k=1): COPY
    lists the file with the glob as PATTERN, so a matching basename keeps the file and a non-matching
    one drops it. Evaluated client-side (Snowflake PATTERN is RE2, close enough to Python ``re`` for
    the filename filters pathGlobFilter carries). On a regex we cannot compile we keep the file
    (return ``True``) -- at worst one extra file vs COPY for an exotic glob, never a sibling
    over-read.
    """
    import re

    basename = stage_path.rstrip("/").rsplit("/", 1)[-1]
    try:
        return re.fullmatch(pattern, basename) is not None
    except re.error:
        return True


def prepare_parquet_direct(
    session: snowpark.Session,
    clean_source_paths: list[str],
    path_classifications: list[PathClassification] | None = None,
    *,
    is_recursive: bool = True,
    path_glob_filter: str | None = None,
) -> list[PdDirectContext] | None:
    """Build the Parquet Direct context(s) from the user's external ``@stage`` source(s).

    The data already lives in the stage's cloud storage, so **nothing is uploaded**. The source
    list may be a **mixture** of directories, glob patterns, and explicit files (exactly what the
    normal read path handles); each is routed to the SAME Parquet Direct scan primitives COPY INTO
    uses, so a PD read covers every case the COPY path does:

      * **directory** (``@stage/dir/``) → one table with ``FILE_PATH='dir/'``. When
        ``recursiveFileLookup=false`` a depth-0 ``PATTERN`` is added so only files directly inside
        the directory are read (:func:`compute_non_recursive_pattern`).
      * **glob** (``@stage/dir/*.parquet``, ``@stage/y=*/f.parquet``) → one table whose
        ``FILE_PATH`` is the longest non-glob scan prefix and whose ``PATTERN`` is the anchored
        regex translation of the glob (:func:`compute_anchor_pattern`) — server-side file filter,
        no client-side LIST.
      * **explicit file** (``@stage/dir/part-0.parquet``) → one table with ``FILE_PATH`` = the file's
        parent prefix and ``PATTERN`` = :func:`compute_anchor_pattern`. A cloud/stage "file" path is
        ambiguous (it may be a real file OR a directory of part-files — classify_source_path can't
        probe it), and the anchor's file branch matches the named entry OR its non-metadata
        descendants, covering both. (This mirrors COPY INTO's PATTERN; ADD FILES would error 004143
        when the path is actually a directory.)

    ``pd_direct_container`` ``UNION ALL``-s the per-table reads onto a single merged schema, so a
    mixed source list (some dirs, some globs, some files, possibly across stages) reads as one
    relation. Sources are NOT de-duplicated: Spark unions repeated paths (``read([A, A])`` -> 2x
    rows), so each source becomes its own table even when ``(stage, file_path, pattern)`` collide.

    ``path_classifications`` (from :func:`classify_source_path`, one per source) and ``is_recursive``
    (the resolved ``recursiveFileLookup`` semantics) are threaded from the caller so PD matches the
    COPY path exactly; if omitted, classifications are computed here.

    Sources are either the user's ``@stage`` paths, or — for a raw AWS ``s3://`` read backed by
    role-based credentials (see :func:`can_use_parquet_direct`) — the ``@stage/<bucket-relative>``
    form over the role-based stage SCOS mints for the bucket. That form is reconstructed here via the
    cached ``StageLocator`` rather than reused from ``get_paths_from_stage`` because that helper
    reduces a glob to its scan prefix, dropping the glob suffix.

    Returns ``None`` (caller uses the normal read path) when the sources are not PD-eligible.
    """
    from snowflake.snowpark_connect.relation.read.path_anchoring import (
        classify_source_path,
        compute_anchor_pattern,
        compute_non_recursive_pattern,
        pattern_from_path_glob_filter,
        split_glob_scan_prefix,
    )
    from snowflake.snowpark_connect.relation.stage_locator import (
        separate_stage_and_file_from_path,
    )

    # Resolve sources to the @stage paths PD will actually read. User @stage paths are used as-is
    # (with the caller's classifications). Raw role-based S3 sources are rebuilt into
    # @stage/<bucket-relative> over SCOS's minted stage and re-classified so PATTERN/basename derive
    # from the real stage path. Anything else (key-based S3, azure, gcs, local, mixed) is ineligible.
    if all(_is_stage_source(p) for p in clean_source_paths):
        resolved_paths = [p.strip() for p in clean_source_paths]
        resolved_classifications = path_classifications or [
            classify_source_path(p) for p in resolved_paths
        ]
    elif all(
        _is_aws_s3_source(p) for p in clean_source_paths
    ) and _session_is_aws_role_based(session):
        from snowflake.snowpark_connect.relation.stage_locator import (
            StageLocator,
            _path_for_stage_mapping,
        )

        locator = StageLocator.get_instance(session)
        resolved_paths = []
        for orig in clean_source_paths:
            rel = _s3_bucket_relative(orig)
            if rel is None:
                return None
            # get_and_maybe_create_stage is cached per bucket (already created by
            # get_paths_from_stage before this call), so this is a cache hit — no new stage.
            stage = locator.get_and_maybe_create_stage(_path_for_stage_mapping(orig))
            resolved_paths.append(f"{stage}/{rel}" if rel else f"{stage}/")
        resolved_classifications = [classify_source_path(p) for p in resolved_paths]
    else:
        return None

    def _stage_and_sub(path: str) -> tuple[str, str] | None:
        """(stage-without-'@', sub-path-without-leading/trailing-'/') or None if not @stage."""
        stage, sub = separate_stage_and_file_from_path(path.strip())
        if not stage.startswith("@"):
            return None
        return stage[1:], sub.strip("/")

    contexts: list[PdDirectContext] = []

    # A user-supplied ``pathGlobFilter`` is a basename filter that wins over PD's path-derived /
    # depth-0 pattern (mirrors the non-PD "user pathGlobFilter wins" contract, SNOW-3428536 /
    # SNOW-3295580) so PD filters by basename exactly like the COPY / reference-Spark path. The
    # per-source ``FILE_PATH`` (scan prefix) is unchanged, so this ANDs with the directory scope.
    # ``None`` when unset/blank -> keep the path-derived pattern computed per branch below.
    pgf_pattern = pattern_from_path_glob_filter(path_glob_filter)

    for src, classification in zip(resolved_paths, resolved_classifications):
        clean = src.strip()

        if classification.kind == "file":
            # A cloud/stage "file" path is AMBIGUOUS — it may be a real file OR a directory Spark
            # wrote part-files into (classify_source_path can't probe cloud/stage paths, so it tags
            # any no-trailing-slash cloud path as "file"). Mirror the COPY path: FILE_PATH = the
            # file's parent prefix, PATTERN = compute_anchor_pattern, whose file branch matches the
            # named entry OR any non-metadata descendant under it — covering both. (ADD FILES can't:
            # it demands an EXACT file and errors 004143 when the path is actually a directory.)
            scan_prefix = (clean.rsplit("/", 1)[0] + "/") if "/" in clean else clean
            info = _stage_and_sub(scan_prefix)
            if info is None:
                return None
            stage_name, file_path = info
            pattern = compute_anchor_pattern(
                [clean], [classification], relative_scope_only=True
            )
        elif classification.kind == "glob":
            # FILE_PATH = longest non-glob scan prefix; PATTERN = anchored regex (matched by the
            # server against the full stage-relative path, same as COPY INTO's PATTERN).
            scan_prefix, _ = split_glob_scan_prefix(clean)
            info = _stage_and_sub(scan_prefix)
            if info is None:
                return None
            stage_name, file_path = info
            pattern = compute_anchor_pattern(
                [clean], [classification], relative_scope_only=True
            )
        else:  # dir
            info = _stage_and_sub(clean)
            if info is None:
                return None
            stage_name, file_path = info
            # Recursive dir: FILE_PATH prefix only. Non-recursive: add a depth-0 PATTERN so only
            # direct children (and hive-partition dirs) are read (None if the prefix is unsafe to
            # anchor, matching the COPY path's own bail-out).
            pattern = (
                None
                if is_recursive
                else compute_non_recursive_pattern(
                    [clean], [classification], relative_scope_only=True
                )
            )

        if pgf_pattern is not None:
            # pathGlobFilter is a filter applied WITHIN the read's scan location -- exactly like COPY
            # INTO, whose FROM clause is the source path and whose PATTERN filters within it. For
            # dir/glob sources FILE_PATH already IS that scan location, so the glob simply replaces
            # the path-derived pattern (the COPY path's "user pathGlobFilter wins" contract).
            #
            # A "file"-classified source is the exception: FILE_PATH is the file's PARENT prefix and
            # the file identity lives in the anchor PATTERN, so replacing that anchor with the glob
            # drops the file scope and re-reads every sibling under the parent -- up to the entire
            # stage when the path is really a no-trailing-slash directory (SNOW-3748550). Unlike
            # COPY's FROM, PARQUET_DIRECT's FILE_PATH cannot point at a file (it is a directory
            # prefix; a file path registers zero files), so we disambiguate file-vs-directory:
            if classification.kind != "file":
                pattern = pgf_pattern
            elif _stage_path_is_directory(session, clean):
                # Really a DIRECTORY: scope FILE_PATH to it and let the glob filter within, a
                # server-side scan that scales to any file count (mirrors COPY FROM=<dir>).
                dir_info = _stage_and_sub(clean)
                if dir_info is None:
                    return None
                stage_name, file_path = dir_info
                pattern = pgf_pattern
            elif _pattern_matches_basename(pgf_pattern, clean):
                # Genuine single FILE whose basename matches the glob: keep the file anchor (k=1).
                pass
            else:
                # Genuine single FILE excluded by the glob: register nothing (a never-matching
                # PATTERN -> a 0-row table), matching COPY's empty result for an excluded file.
                pattern = _PD_NEVER_MATCH_PATTERN

        # No dedup on (stage, file_path, pattern): Spark does NOT dedup repeated
        # source paths -- ``read([A, A])`` unions A's rows twice (2x). Emit one
        # PdDirectContext per source so ``pd_direct_container`` UNION ALLs them all
        # and duplicate/triple reads return the Spark-matching row multiple (SNOW-3748550).
        contexts.append(
            PdDirectContext(stage=stage_name, file_path=file_path, pattern=pattern)
        )

    if not contexts:
        return None
    return contexts


def _ensure_pd_table(
    session: snowpark.Session,
    ctx: PdDirectContext,
    explicit_columns: str | None = None,
    replace_invalid_characters: bool = True,
) -> str:
    """Create the Parquet Direct (loose-parquet Iceberg) table once for this context.

    In the common case the table is created with **explicit columns** derived from SCOS's final schema
    — ``explicit_columns`` is a ``"col" TYPE, …`` string built from the user schema (user-schema path)
    or from SCOS's discovered/merged schema (no-schema path). This is both the design (SCOS inference
    is the source of truth) AND a hard requirement for that path: with FEATURE_PARQUET_DIRECT enabled
    on the account the deprecated ``INFER_SCHEMA`` table option errors 091346 on its own (verified), so
    PD's own INFER is not an available fallback there.

    The ``else`` branch is **live** (not dead): it handles the degenerate partition-only user schema,
    where ``explicit_columns`` is empty because every requested column is a path-derived partition
    column (excluded from the DDL column list). With no file columns to declare, it creates the table
    with ``ENABLE_SCHEMA_INFERENCE=TRUE`` — which, unlike the deprecated ``INFER_SCHEMA`` option, is
    NOT rejected by 091346 under FEATURE_PARQUET_DIRECT. PD infers the file's real columns and
    ``pd_direct_container`` then projects down to the partition value (from ``METADATA$FILENAME``).
    Covered by ``test_parquet_direct_read_paths.py::test_pd_read_partition_only_schema``.
    """
    if ctx.table is not None:
        return ctx.table
    # Current session schema (no hardcoded db/schema); random name. The table is created as a
    # session-scoped TEMPORARY iceberg table (SNOW-3748552, auto-on for SCOS sessions), so it is
    # auto-reclaimed when the session ends — no manual drop/cleanup needed.
    table = f"{PD_TABLE_PREFIX}{uuid.uuid4().hex[:12]}"
    # Drive PD's case-matching from Spark's spark.sql.caseSensitive via the MATCH_BY_COLUMN_NAME
    # table option (bucket 5). Requires FEATURE_PARQUET_DIRECT enabled on the account (gates
    # ENABLE_MATCH_BY_COLUMN_NAME_TABLE_OPTION + ENABLE_ALLOW_MULTIPLE_PARQUET_NAME_MAPPINGS).
    #   caseSensitive=false -> CASE_INSENSITIVE: matches ID/id at top level AND nested struct keys,
    #     and unifies differently-cased same-column across files (no 091573/100489). Matches Spark.
    #   caseSensitive=true  -> CASE_SENSITIVE : exact match. NOTE two edge divergences vs Spark
    #     documented in scos_pd_read_diffs.md (top-level case-collision -> 100489 instead of NULL;
    #     nested struct field stays case-insensitive so a case-mismatched field still populates).
    from snowflake.snowpark_connect.config import global_config

    match_by = (
        "CASE_SENSITIVE"
        if global_config.spark_sql_caseSensitive
        else "CASE_INSENSITIVE"
    )
    # Thread the resolved replaceInvalidCharacters option (SCOS default TRUE, see
    # ParquetReaderConfig) into the loose-parquet CREATE DDL. TRUE makes the scan
    # substitute U+FFFD for malformed UTF-8 (matching Spark's lenient Parquet
    # reader) instead of erroring; the strict opt-out (replaceInvalidCharacters=
    # False) flows through as FALSE and the server rejects invalid UTF-8 on the
    # scan (ERR_INVALID_UTF8_STRING / 100144). The lenient TRUE substitution is
    # SNOW-3815407; the FALSE-honoring reject is server-side (SNOW-3832472),
    # verified on the test account (a False read of a lone-surrogate fixture raises
    # 100144) — confirm the deployed build carries SNOW-3832472 before relying on it.
    replace_invalid = "TRUE" if replace_invalid_characters else "FALSE"
    # FILE_PATH is a prefix within the stage; "" reads from the stage root. ALWAYS emit the clause
    # (as FILE_PATH='' for the stage-root / add-files case): the GS auto-catalog provisioning for a
    # PARQUET_DIRECT_EXTERNAL_STAGE create is gated on the presence of FILE_PATH (or BASE_LOCATION) in
    # the table options (SNOW-3748550, CreateParser). PARQUET_DIRECT_EXTERNAL_STAGE alone does NOT
    # trigger it — omitting FILE_PATH means no catalog is auto-provisioned and the create fails with
    # 091347 "Iceberg tables require a catalog integration". Using FILE_PATH='' (stage root) when the
    # sub-path is empty keeps that satisfied while the PATTERN (if any) scopes the actual files.
    file_path_clause = (
        f"FILE_PATH='{_esc_sql_literal(ctx.file_path)}/' "
        if ctx.file_path
        else "FILE_PATH='' "
    )
    # PATTERN is a server-side regex file filter (glob / explicit-file sources / non-recursive dir
    # depth-0). Under Parquet Direct it is matched against the path *relative to FILE_PATH* (the
    # scan-prefix is stripped from the matched subject), NOT the full stage-relative path -- so the
    # PATTERN builders (compute_anchor_pattern / compute_non_recursive_pattern) emit prefix-less,
    # scan-relative regexes for PD (relative_scope_only; verified live on SFCTEST0, SNOW-3748550).
    # Escape any embedded single-quote for the SQL string literal.
    pattern_clause = (
        f"PATTERN='{_esc_sql_literal(ctx.pattern)}' " if ctx.pattern else ""
    )
    if explicit_columns:
        # Explicit columns from SCOS's schema + MATCH_BY_COLUMN_NAME (maps file columns to the
        # DECLARED columns). This is the only working create path: INFER_SCHEMA is unsupported on the
        # FEATURE_PARQUET_DIRECT-enabled account (091346), so there is no INFER alternative.
        ddl = (
            f"CREATE OR REPLACE TEMPORARY ICEBERG TABLE {table} ({explicit_columns}) "
            f"PARQUET_DIRECT_EXTERNAL_STAGE='{_esc_sql_literal(ctx.stage)}' {file_path_clause}{pattern_clause}"
            f"MATCH_BY_COLUMN_NAME={match_by} "
            f"REPLACE_INVALID_CHARACTERS={replace_invalid} REFRESH_ON_CREATE=TRUE"
        )
    else:
        # FALLBACK for the degenerate partition-only user schema — explicit_columns is empty because
        # every requested column is a path-derived partition column (excluded from the DDL). We still
        # need a scannable table: a partition-only read returns ONE ROW PER PARQUET RECORD (partition
        # value repeated), so the files' row cardinality is required (LS yields paths/partition values
        # but not row counts). Use ENABLE_SCHEMA_INFERENCE (NOT INFER_SCHEMA — the latter is deprecated
        # by ENABLE_PARQUET_DIRECT_SPLIT_INFER_SCHEMA_OPTION under FEATURE_PARQUET_DIRECT and errors
        # 091346). PD infers the file's real columns; pd_direct_container's projection then keeps only
        # the partition column (from METADATA$FILENAME) and drops the inferred data columns.
        ddl = (
            f"CREATE OR REPLACE TEMPORARY ICEBERG TABLE {table} "
            f"PARQUET_DIRECT_EXTERNAL_STAGE='{_esc_sql_literal(ctx.stage)}' {file_path_clause}{pattern_clause}"
            f"ENABLE_SCHEMA_INFERENCE=TRUE "
            f"REPLACE_INVALID_CHARACTERS={replace_invalid} REFRESH_ON_CREATE=TRUE"
        )
    try:
        session.sql(ddl).collect()
    except Exception as e:
        # A stage that cannot back Parquet Direct (not storage-integration-backed / unsupported
        # encryption / no resolvable location — server 099219-099222): surface a clear,
        # actionable error rather than silently rerouting to the normal read path.
        if any(code in str(e) for code in _PD_INCOMPATIBLE_STAGE_ERRORS):
            raise ValueError(
                f"Stage '@{ctx.stage}' is not compatible with Parquet Direct (requires a "
                f"storage-integration-backed external stage with supported encryption). "
                f"Disable 'snowpark.connect.parquet_direct.enabled' to use the normal read "
                f"path, or point at a compatible stage."
            ) from e
        raise
    ctx.table = table
    return table


# Quote an identifier (wrap in double-quotes, escaping embedded ones). Alias to the shared
# analyzer helper (no local reimplementation); also imported by map_read_parquet.
_quote = analyzer_utils.quote_name_without_upper_casing


def type_to_pd_ddl(t: DataType) -> str:
    """Snowpark type → loose-parquet column DDL, preserving nested struct field-name CASE.

    ``_snowpark_type_to_iceberg_ddl`` routes nested struct field names through
    ``spark_to_sf_single_id``, which UPPERCASES them when ``spark.sql.caseSensitive=false`` — so a
    field ``uppername`` would be declared as ``UPPERNAME`` and surface uppercased. Spark preserves
    original field-name case for display regardless of caseSensitive (case-insensitivity is about
    matching, handled by MATCH_BY_COLUMN_NAME). So we quote nested field names case-preserved and
    only delegate scalar leaves to the shared helper.
    """
    from snowflake.snowpark.types import ArrayType, MapType, StructType
    from snowflake.snowpark_connect.relation.write.map_write import (
        _snowpark_type_to_iceberg_ddl,
    )

    if isinstance(t, StructType):
        inner = ", ".join(
            f"{_quote(analyzer_utils.unquote_if_quoted(f.name))} {type_to_pd_ddl(f.datatype)}"
            for f in t.fields
        )
        return f"OBJECT({inner})"
    if isinstance(t, ArrayType):
        return f"ARRAY({type_to_pd_ddl(t.element_type)})"
    if isinstance(t, MapType):
        return f"MAP({type_to_pd_ddl(t.key_type)}, {type_to_pd_ddl(t.value_type)})"
    if isinstance(t, TimestampType):
        # SNOW-3836201: the shared write-path helper _snowpark_type_to_iceberg_ddl compares the
        # TimestampTimeZone ENUM to a string literal ("ltz"/"tz"), which is ALWAYS False, so it
        # declares every timestamp -- including LTZ/TZ -- as TIMESTAMP_NTZ. For Parquet Direct that
        # silently downgrades an isAdjustedToUTC=true (instant / TIMESTAMP_LTZ) column to NTZ, so the
        # UTC instant is read back as a naive wall-clock (off by the session offset) vs Spark. SCOS's
        # schema discovery correctly infers LTZ (INFER_SCHEMA USE_LOGICAL_TYPE=TRUE); we must preserve
        # it in the loose-parquet DDL. str() of the enum yields 'ltz'/'ntz'/'tz'. (The same latent bug
        # affects the write path via that helper -- tracked separately.)
        tz = str(getattr(t, "tz", "ntz"))
        return {"ltz": "TIMESTAMP_LTZ", "tz": "TIMESTAMP_TZ"}.get(tz, "TIMESTAMP_NTZ")
    return _snowpark_type_to_iceberg_ddl(t)


def _reconcile_physical_field_names(
    discovered: DataType, physical: DataType
) -> DataType:
    """Merge SCOS's discovered type with the PD table's physical (``base.schema``) type.

    Returns the **discovered** type unchanged for scalars, so integer widths
    (``ByteType``/``ShortType``/``IntegerType``) survive instead of being widened to the
    loose-parquet read-back type (flag ① / SNOW-3821363). For nested types the discovered
    type is kept as-is except that struct field **names** are taken from ``physical`` — the
    returned ``OBJECT`` dict keys must match the declared ``StructType`` field names or
    Snowpark's ``cell_to_str`` KeyErrors (the original reason ``base.schema`` was adopted
    wholesale at this site). Only the name is borrowed; the type/width is not changed.

    On any container-shape disagreement (mismatched kinds or struct arities) the physical
    type is returned, preserving the original safe behavior.
    """
    from snowflake.snowpark.types import ArrayType, MapType, StructField, StructType

    if (
        isinstance(discovered, StructType)
        and isinstance(physical, StructType)
        and len(discovered.fields) == len(physical.fields)
    ):
        return StructType(
            [
                StructField(
                    pf.name,  # physical name → matches returned OBJECT keys
                    _reconcile_physical_field_names(df.datatype, pf.datatype),
                    df.nullable,
                    _is_column=df._is_column,
                )
                for df, pf in zip(discovered.fields, physical.fields)
            ],
            structured=discovered.structured,
        )
    if isinstance(discovered, ArrayType) and isinstance(physical, ArrayType):
        return ArrayType(
            _reconcile_physical_field_names(
                discovered.element_type, physical.element_type
            ),
            contains_null=discovered.contains_null,
            structured=discovered.structured,
        )
    if isinstance(discovered, MapType) and isinstance(physical, MapType):
        return MapType(
            _reconcile_physical_field_names(discovered.key_type, physical.key_type),
            _reconcile_physical_field_names(discovered.value_type, physical.value_type),
            value_contains_null=discovered.value_contains_null,
            structured=discovered.structured,
        )
    # Both scalar → keep discovered (width preserved). Any container involvement without a
    # matching shape → keep physical (original safe behavior, avoids cell_to_str KeyError).
    if isinstance(discovered, (StructType, ArrayType, MapType)) or isinstance(
        physical, (StructType, ArrayType, MapType)
    ):
        return physical
    return discovered


def pd_direct_container(
    session: snowpark.Session,
    contexts: list[PdDirectContext],
    plan_id: int | None,
    data_names: list[str],
    data_types: list[DataType],
    *,
    partition_columns: list[str] | None = None,
    partition_types: dict | None = None,
    partition_file_col_names: list[str] | None = None,
    needs_metadata: bool = False,
    explicit_columns: str | None = None,
    replace_invalid_characters: bool = True,
    infer_ntz: bool = True,
) -> DataFrameContainer:
    """Read PD rows and project them onto SCOS's final schema.

    ONE Parquet Direct table is created per source path (``contexts``); every table is declared
    with the SAME merged ``explicit_columns`` so their ``SELECT *`` outputs are UNION-compatible
    (a file missing a column reads NULL via MATCH_BY_COLUMN_NAME). The per-table reads are
    ``UNION ALL``-ed into a single base relation, then projected exactly as the single-path case
    (a single context degenerates to the previous single-table SELECT, no UNION).

    METADATA$FILENAME is first surfaced as a real column via raw SQL (a pseudo-column can't
    survive Snowpark's ``.select`` wrapping), then all projection/partition-parsing uses Snowpark
    Column ops so identifier quoting is correct. Column order matches SCOS: data → partitions →
    METADATA$FILENAME. Partition columns are read directly when Parquet Direct inferred them
    (from ``col=val`` dirs), else parsed from METADATA$FILENAME (per-row, so the union is safe).
    """
    # Create one PD table per distinct source path and UNION ALL their reads. Because every table
    # shares the same declared columns, ``SELECT *`` yields the same columns in the same order
    # across all tables (union-compatible); each row still carries its own METADATA$FILENAME for
    # per-file partition parsing.
    per_table_selects = [
        f"SELECT *, METADATA$FILENAME AS {_quote(METADATA_FILENAME_COLUMN)} FROM "
        + _ensure_pd_table(
            session,
            ctx,
            explicit_columns=explicit_columns,
            replace_invalid_characters=replace_invalid_characters,
        )
        for ctx in contexts
    ]
    base = session.sql(" UNION ALL ".join(per_table_selects))
    meta_col = base[_quote(METADATA_FILENAME_COLUMN)]
    # Key everything by Spark's caseSensitive so a data column ``Country`` and a partition/other
    # column ``country`` stay DISTINCT under caseSensitive=true (both survive) and collapse under
    # caseSensitive=false. Keying only by lowercase collided them and dropped/NULLed one.
    from snowflake.snowpark_connect.config import global_config

    _cs = global_config.spark_sql_caseSensitive

    def _normalize_col_key(col_name: str) -> str:
        unquoted = analyzer_utils.unquote_if_quoted(col_name)
        return unquoted if _cs else unquoted.lower()

    available = {_normalize_col_key(f.name): f.name for f in base.schema.fields}
    # Physical PD column types (from the table schema); using these keeps nested struct field names
    # consistent with the returned OBJECT dict keys (avoids Snowpark cell_to_str KeyError).
    avail_types = {_normalize_col_key(f.name): f.datatype for f in base.schema.fields}
    part_norm = {_normalize_col_key(c) for c in (partition_columns or [])}

    field_names: list[str] = []
    field_types: list[DataType] = []
    exprs = []

    for name, dtype in zip(data_names, data_types):
        key = _normalize_col_key(name)
        if key in part_norm:
            continue
        if key in available:
            col = base[available[key]]
            physical = avail_types.get(key)
            if physical is not None:
                # Keep SCOS's discovered TYPE so scalar integer widths (Byte/Short/Int)
                # survive instead of being widened to the loose-parquet read-back type
                # (flag ① / SNOW-3821363); borrow only the physical nested struct field
                # NAMES so the returned OBJECT dict keys still line up (avoids the
                # cell_to_str KeyError this override originally guarded against).
                dtype = _reconcile_physical_field_names(dtype, physical)
        else:
            col = lit(None).cast(dtype)
        exprs.append(col.alias(_quote(name)))
        field_names.append(name)
        field_types.append(dtype)

    for i, col_name in enumerate(partition_columns or []):
        key = _normalize_col_key(col_name)
        ptype = (partition_types or {}).get(col_name, StringType())
        if key in available:
            col = base[available[key]]  # PD inferred the partition column directly
        else:
            file_col = (
                partition_file_col_names[i] if partition_file_col_names else col_name
            )
            col = nullif(
                split_part(
                    split_part(meta_col, lit(f"{file_col}="), lit(2)), lit("/"), lit(1)
                ),
                lit("__HIVE_DEFAULT_PARTITION__"),
            ).try_cast(ptype, permissive=True)
        exprs.append(col.alias(_quote(col_name)))
        field_names.append(col_name)
        field_types.append(ptype)

    if needs_metadata:
        exprs.append(meta_col.alias(_quote(METADATA_FILENAME_COLUMN)))
        field_names.append(METADATA_FILENAME_COLUMN)
        field_types.append(StringType())

    projected = base.select(exprs)
    if not infer_ntz:
        # Honor spark.sql.parquet.inferTimestampNTZ.enabled=false: reinterpret
        # TIMESTAMP_NTZ columns as UTC instants -> LTZ, mirroring the non-PD read
        # path (_cast_ntz_to_ltz in map_read_parquet). The helper self-guards on
        # NTZ columns, so an already-LTZ column (e.g. a user-declared
        # TimestampType) is left untouched -- no double shift. Flip the reported
        # type of exactly the columns it converts so snowpark_column_types stays
        # in sync with the transformed df (without disturbing the other
        # field_types, which deliberately preserve SCOS's discovered widths).
        from snowflake.snowpark_connect.relation.read.map_read_parquet import (
            _cast_ntz_to_ltz,
        )

        ntz_positions = [
            i
            for i, f in enumerate(projected.schema.fields)
            if isinstance(f.datatype, TimestampType)
            and f.datatype.tz == TimestampTimeZone.NTZ
        ]
        if ntz_positions:
            projected = _cast_ntz_to_ltz(projected)
            ltz_type = TimestampType(TimestampTimeZone.LTZ)
            for i in ntz_positions:
                field_types[i] = ltz_type
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        projected, plan_id
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=renamed_df,
        spark_column_names=field_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[emulate_integral_types(t) for t in field_types],
        # Memoizable in df_cache_map, like the non-PD COPY path. The loose-parquet ICEBERG table
        # already materializes the read, so .without_materialization() skips a redundant
        # cache_result(); but the container must stay memoizable so repeated actions on the same
        # read reuse the SAME SCOS_PD table instead of re-running CREATE ICEBERG + LIST_FILES every
        # time. can_be_cached=False made every downstream access re-execute the full PD read (the
        # trap the non-PD path documents) — multiplying CREATE_ICEBERG/LIST cost by the #reads and
        # making read-heavy workloads 3-5x slower than non-PD (SNOW-3748550 perf).
        can_be_cached=True,
    ).without_materialization()
