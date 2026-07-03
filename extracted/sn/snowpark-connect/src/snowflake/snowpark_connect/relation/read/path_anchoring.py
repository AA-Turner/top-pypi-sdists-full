#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Anchor stage reads against Snowflake's prefix matching (SNOW-3428536).

Snowflake stage operations (``COPY INTO``, ``SELECT FROM @stage``, ``LIST``)
treat stage paths as **prefix matches**, not exact paths. As a result, a
naive read of ``@stage/dir/data.json`` would also pull in
``data.json.gz`` / ``data.json.bz2`` siblings, and reading
``@stage/prefix/my_data`` would also match ``@stage/prefix/my_data_v2/...``.

This module translates a list of user-supplied source paths into a
Snowflake ``PATTERN`` regex that anchors the read to *exactly* the
files / directories the user named. Directory reads are anchored
separately (by appending a trailing ``/`` to the stage path); this
module's job is the file / glob path anchoring via ``PATTERN``.

The PATTERN for explicit-file paths permits two shapes -- the literal
named entry **or** any *non-metadata* descendant inside it -- because
Spark's ``DataFrameReader`` accepts either a file or a directory at
the same path argument, and cloud / stage paths cannot be probed
locally to disambiguate. The descent branch deliberately excludes
files whose basename starts with ``_`` or ``.`` (e.g. ``_SUCCESS``,
``_common_metadata``, ``.crc``) since once this module sets
``PATTERN`` the standard metadata-exclusion regex no longer fires.
See :func:`compute_anchor_pattern` for the full regex shape.

Data flow::

    classify_source_path  ──► compute_anchor_pattern  ──► inject_anchor_pattern
    (per source path)        (combine across paths)      (write to options dict)

Public API:

    * :class:`PathClassification` -- typed result of classification.
    * :func:`classify_source_path` -- classify one path as dir / file / glob.
    * :func:`split_glob_scan_prefix` -- split a glob path into scan dir + suffix.
    * :func:`spark_glob_to_snowflake_regex` -- translate Spark-style glob.
    * :func:`compute_anchor_pattern` -- build the combined PATTERN regex.
    * :func:`inject_anchor_pattern` -- mutate read-options to anchor the scan.

The kill-switch ``snowpark.connect.read.anchorStagePaths`` (default
``true``) reverts to the legacy unanchored behavior.
"""
from __future__ import annotations

import os
import re
from typing import Any, Literal, NamedTuple

from snowflake.snowpark_connect.config import is_anchor_stage_paths_enabled
from snowflake.snowpark_connect.relation.io_utils import (
    convert_file_prefix_path,
    is_cloud_path,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

PathKind = Literal["dir", "file", "glob"]

# Hive partition directory basename (``key=value``); shared by local upload
# walk filtering and non-recursive PATTERN branches (SNOW-3566246).
_HIVE_PARTITION_DIR_PATTERN = r"[^/=]+=[^/]+"
_HIVE_PARTITION_DIR_RE = re.compile(rf"^{_HIVE_PARTITION_DIR_PATTERN}$")


class RecursiveFileLookup(NamedTuple):
    """Resolved ``recursiveFileLookup`` semantics for a read-options dict (SNOW-3566246).

    ``is_recursive`` drives local upload depth, PATTERN/XML listing, and text
    slash-count filtering. When the option is absent, SCOS defaults to
    ``False`` (depth-0 listing plus arbitrary-depth Hive ``key=value/``
    segments), matching Spark.

    ``skip_partition_discovery`` follows Spark's partition-inference rule:
    Hive partition columns are discovered unless the user **explicitly**
    sets a truthy ``recursiveFileLookup`` value. When the key is absent,
    partition discovery stays enabled even though listing is depth-0.
    """

    is_recursive: bool
    skip_partition_discovery: bool


class PathClassification(NamedTuple):
    """Typed classification of a single source path.

    Exactly one of ``basename`` / ``regex`` is set, depending on
    ``kind``:

        * ``kind="dir"`` -- both ``basename`` and ``regex`` are ``None``.
          The directory is anchored by the trailing ``/`` on the stage
          path; no PATTERN is needed.
        * ``kind="file"`` -- ``basename`` is the basename of the
          requested entry. Used both for unambiguous file paths and
          for cloud / stage paths without a trailing slash whose true
          file-vs-directory nature cannot be probed. The PATTERN
          should anchor on this basename so prefix matching cannot pull
          in sibling entries with extra suffixes (e.g. ``data.json.gz``
          next to ``data.json``, or ``job_0_v2/`` next to ``job_0/``)
          while still permitting descent into the named entry when it
          turns out to be a directory (see ``compute_anchor_pattern``).
        * ``kind="glob"`` -- ``regex`` is the unanchored Snowflake regex
          translation of the stage-relative glob suffix. Callers should append
          ``$`` to anchor.
    """

    kind: PathKind
    basename: str | None = None
    regex: str | None = None


_GLOB_METACHARS = re.compile(r"[*?\[\{]")

# Characters in a file basename that Snowflake stage operations are
# known to URL-encode (or otherwise transform) in the relative paths
# returned by ``LIST`` / matched against ``PATTERN``. Re-using
# ``re.escape(basename)`` directly in the PATTERN would then never
# match, so we skip anchoring for such paths and accept the small
# residual prefix-bleed risk rather than producing a regex that
# excludes everything.
_PATTERN_UNSAFE_BASENAME_CHARS = re.compile(r"[\s$%#?&+=,;()'\"]")


def _first_glob_metachar_index(path: str) -> int | None:
    """Return the index of the first unescaped glob metachar, or ``None``.

    Scans ``path`` in its original (escaped) form so the returned index is a
    valid offset into that same string. A ``\\``-escaped character is skipped
    (``i += 2``) and never treated as a glob metachar -- escaped metacharacters
    are literals in Spark. Callers such as :func:`split_glob_scan_prefix` rely
    on the index aligning with the original string, so this must not run on the
    unescaped (and therefore shorter) copy.
    """
    i = 0
    length = len(path)
    while i < length:
        if path[i] == "\\" and i + 1 < length:
            i += 2
            continue
        if _GLOB_METACHARS.match(path[i]):
            return i
        i += 1
    return None


def _has_glob_metachars(path: str) -> bool:
    """True if ``path`` contains an unescaped Spark glob metacharacter.

    SNOW-3594869: escaped metacharacters (e.g. ``data\\*.json``) are literals
    and do not count. This is a deliberate behavior change from the prior
    unescape-then-search approach (which classified escaped-only paths as
    globs); it keeps classification consistent with
    :func:`split_glob_scan_prefix`, which would otherwise raise on such paths.
    """
    return _first_glob_metachar_index(path) is not None


def split_glob_scan_prefix(path: str) -> tuple[str, str]:
    """Split a glob path into a scan directory prefix and glob suffix (SNOW-3594869).

    The scan prefix is the longest leading portion of ``path`` that contains
    no glob metacharacters and ends at the last ``/`` before the first glob
    metachar. The suffix is the remainder used for Snowflake ``PATTERN``
    translation relative to that scan directory.
    """
    cleaned = path.strip("'\"")
    idx = _first_glob_metachar_index(cleaned)
    if idx is None:
        raise ValueError(f"Path has no glob metacharacters: {path!r}")

    slash_idx = cleaned.rfind("/", 0, idx)
    if slash_idx == -1:
        return "", cleaned
    return cleaned[: slash_idx + 1], cleaned[slash_idx + 1 :]


def _local_path_stage_relative_suffix(path: str) -> str:
    """Map a local path to the last-two-component suffix under a temp stage."""
    normalized = (
        convert_file_prefix_path(path.strip("'\"")).replace(os.sep, "/").rstrip("/")
    )
    parts = [part for part in normalized.split("/") if part]
    if len(parts) >= 2:
        return "/".join(parts[-2:])
    return parts[-1] if parts else ""


def _scan_prefix_stage_relative(scan_prefix: str) -> str:
    """Stage-relative path of a glob scan prefix for LIST result matching."""
    cleaned = scan_prefix.strip("'\"").rstrip("/")
    if cleaned.startswith("@"):
        return cleaned.split("/", 1)[1] if "/" in cleaned else ""
    if is_cloud_path(cleaned):
        scheme, rest = cleaned.split("://", 1)
        parts = rest.split("/")
        if scheme.lower() == "azure":
            return "/".join(parts[2:])
        return "/".join(parts[1:])
    return _local_path_stage_relative_suffix(cleaned)


def listed_path_matches_glob_suffix(
    listed_relative_path: str,
    clean_glob_path: str,
    glob_regex: str,
) -> bool:
    """Return whether a LIST-relative path matches a glob read path."""
    scan_prefix, _ = split_glob_scan_prefix(clean_glob_path)
    stage_rel_scan = _scan_prefix_stage_relative(scan_prefix)
    if stage_rel_scan:
        prefix = stage_rel_scan.rstrip("/") + "/"
        if listed_relative_path.startswith(prefix):
            tail = listed_relative_path[len(prefix) :]
        else:
            return False
    else:
        tail = listed_relative_path
    return re.fullmatch(f"{glob_regex}$", tail) is not None


def _basename_is_pattern_safe(basename: str) -> bool:
    """True if ``basename`` can be safely embedded in a Snowflake PATTERN.

    Snowflake stage operations sometimes URL-encode characters in the
    relative path returned by ``LIST``. If we anchor a PATTERN on
    a basename containing such characters, the encoded form on the
    stage will never match the literal form in the regex and the read
    silently returns zero rows. Better to skip anchoring entirely than
    to fabricate a pattern that excludes the user's data.
    """
    return _PATTERN_UNSAFE_BASENAME_CHARS.search(basename) is None


def _looks_like_explicit_file_path(path: str) -> bool:
    """True when ``path`` names a single file rather than a directory.

    Cloud/stage paths without a trailing ``/`` are classified as ``file`` even
    when the user meant a directory (e.g. ``@stage/tree/part-foo``). A dotted
    final component is a practical discriminator for explicit file reads.
    """
    base = os.path.basename(path.rstrip("/"))
    return "." in base and not base.startswith(".")


def _dir_prefix_unsafe_for_depth0_pattern(prefix: str) -> bool:
    """True when a depth-0 PATTERN on ``prefix`` would likely match nothing.

    Skips depth-0 injection for path components Snowflake URL-encodes and
    for literal directory names containing Spark glob metacharacters
    (``[]{}*?``) per SPARK-32810 -- rely on the stage path trailing ``/``
    bound instead.
    """
    for component in prefix.split("/"):
        if not component:
            continue
        if not _basename_is_pattern_safe(component):
            return True
        if _has_glob_metachars(component):
            return True
    return False


def _stage_relative_glob_path(glob_path: str) -> str:
    """Return the glob suffix matched by PATTERN under the scan prefix."""
    _, glob_suffix = split_glob_scan_prefix(glob_path)
    return glob_suffix


def spark_glob_to_snowflake_regex(glob_pattern: str) -> str:
    """Translate a Spark-style glob to a Snowflake-compatible regex.

    Mapping:
        * ``**`` -> ``.*`` (cross-component wildcard)
        * ``*``  -> ``[^/]*`` (within-component wildcard)
        * ``?``  -> ``[^/]`` (single non-separator char)
        * ``[abc]`` -> ``[abc]`` (character class kept verbatim)
        * ``{a,b,c}`` -> ``(?:a|b|c)`` (alternation group)
        * Backslash escapes (``\\*``, ``\\?``, ``\\[``, ``\\{``, ``\\}``)
          -> literal character.
        * Other regex metacharacters are escaped.

    The returned regex is *not* anchored -- callers are responsible for
    appending ``$`` so multiple expressions can be joined together with
    alternation.
    """
    out: list[str] = []
    i = 0
    pattern_len = len(glob_pattern)
    while i < pattern_len:
        current_char = glob_pattern[i]
        if (
            current_char == "\\"
            and i + 1 < pattern_len
            and glob_pattern[i + 1] in "*?[]{}\\"
        ):
            out.append(re.escape(glob_pattern[i + 1]))
            i += 2
            continue
        if current_char == "*":
            if i + 1 < pattern_len and glob_pattern[i + 1] == "*":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
            continue
        if current_char == "?":
            out.append("[^/]")
            i += 1
            continue
        if current_char == "[":
            close_bracket_idx = glob_pattern.find("]", i + 1)
            if close_bracket_idx == -1:
                out.append(re.escape(current_char))
                i += 1
            else:
                # Snowflake regex character classes share Spark/Java syntax.
                out.append(glob_pattern[i : close_bracket_idx + 1])
                i = close_bracket_idx + 1
            continue
        if current_char == "{":
            close_brace_idx = glob_pattern.find("}", i + 1)
            if close_brace_idx == -1:
                out.append(re.escape(current_char))
                i += 1
            else:
                parts = glob_pattern[i + 1 : close_brace_idx].split(",")
                out.append(
                    "(?:"
                    + "|".join(spark_glob_to_snowflake_regex(p) for p in parts)
                    + ")"
                )
                i = close_brace_idx + 1
            continue
        out.append(re.escape(current_char))
        i += 1
    return "".join(out)


# A Snowflake stage reference with no path component after the stage
# name (e.g. ``@my_stage`` or ``@db.schema.my_stage``). These are
# always directory-like roots, never files: you cannot have a file
# literally named ``@my_stage`` on a stage. Anchoring on the stage
# name as a basename is meaningless because Snowflake's PATTERN
# matches the *relative* file path inside the stage, which never
# contains the stage name itself.
_STAGE_ROOT_RE = re.compile(r"^@[^/]+/?$")


def classify_source_path(clean_path: str) -> PathClassification:
    """Classify a single source path as a directory, explicit file, or glob.

    Heuristics (applied in order):

        * Trailing ``/`` -> directory (works for both local and cloud).
        * Snowflake stage-root reference (``@stage`` with no ``/``
          after the stage name) -> directory. See ``_STAGE_ROOT_RE``.
        * Local path that exists and is a directory -> directory.
        * Local path that exists and is a file -> file (SPARK-32810: prevents
          a literal ``{`` or ``[`` in a parent directory name from being
          misidentified as a glob metacharacter and generating a broken PATTERN).
        * Contains glob metacharacters -> glob.
        * Otherwise -> file (see caveat below).

    The trailing-slash check comes first because it is the only signal
    available for cloud paths -- ``os.path.isdir`` cannot probe S3 / GCS
    / Azure URLs.

    Caveat: for cloud / stage paths without a trailing slash, the
    ``kind="file"`` classification is conservative -- the path *might*
    actually be a directory (e.g. Spark's ``df.write.parquet(
    "@stage/out/job_0")`` writes ``out/job_0/part-*.parquet`` and reads
    back via ``spark.read.parquet("@stage/out/job_0")``). The PATTERN
    built by :func:`compute_anchor_pattern` deliberately permits both
    interpretations; see its docstring for the regex shape.
    """
    if clean_path.endswith("/"):
        return PathClassification(kind="dir")

    if _STAGE_ROOT_RE.match(clean_path):
        return PathClassification(kind="dir")

    local_path = (
        convert_file_prefix_path(clean_path) if not is_cloud_path(clean_path) else None
    )
    if local_path is not None:
        if os.path.isdir(local_path):
            return PathClassification(kind="dir")
        # SPARK-32810: a file whose parent directory name contains glob
        # metacharacters (e.g. /tmp/{run}/data.json) would otherwise be
        # misclassified as a glob because _has_glob_metachars detects the
        # bare ``{`` in the clean (unescaped) path.  If the path resolves to
        # a real local file, trust the filesystem over the heuristic.
        if os.path.isfile(local_path):
            return PathClassification(
                kind="file", basename=os.path.basename(local_path)
            )

    if _has_glob_metachars(clean_path):
        return PathClassification(
            kind="glob",
            regex=spark_glob_to_snowflake_regex(_stage_relative_glob_path(clean_path)),
        )

    return PathClassification(kind="file", basename=os.path.basename(clean_path))


def compute_anchor_pattern(
    clean_source_paths: list[str],
    classifications: list[PathClassification] | None = None,
) -> str | None:
    """Compute a Snowflake PATTERN regex that anchors the user's source paths.

    Returns ``None`` when every path is a directory -- directories are
    bounded by the trailing ``/`` that the read dispatcher appends to
    the stage path, and the standard metadata-exclusion PATTERN handles
    hidden files. Otherwise returns an anchored regex matching exactly
    the user's intended files (alternation when multiple paths are
    given).

    The regex is matched against the full file path returned by
    Snowflake's stage scan, so we use ``(.*/)?`` to permit any leading
    directory component for explicit-file branches.

    File-branch shape ``(.*/)?<basename>(?:$|/(?:.*/)?[^_.][^/]*$)``
    -- "match the named entry exactly OR any non-metadata descendant
    inside it". This mirrors Spark's reader semantics where the same
    path argument may resolve to either a single file or a directory
    full of files (Hadoop ``FileSystem.getFileStatus`` probes the
    actual entry). Cloud / stage paths cannot be probed, so the regex
    permits both shapes:

        * Literal entry: ``(.*/)?data\\.json$`` -- matches the named
          file even if it starts with ``_`` / ``.`` (the user named
          it explicitly).
        * Descendant: ``(.*/)?data\\.json/(?:.*/)?[^_.][^/]*$`` --
          matches files under a directory named ``data.json``, but
          excludes Spark / Parquet metadata sidecars (``_SUCCESS``,
          ``_metadata``, ``_common_metadata``, ``.crc``, ``.DS_Store``
          and any file whose basename starts with ``_`` or ``.``).
          The metadata exclusion is built into the descent group
          rather than relying on a separate ``apply_metadata_exclusion_pattern``
          call, because once we set ``PATTERN`` ourselves the
          metadata-exclusion path no longer fires.

    Critically, this still rejects prefix-sharing siblings (e.g.
    ``data.json.gz``, ``job_0_v2/...``) because ``.`` and ``_`` are
    not ``/`` -- the descent group can only cross a real directory
    boundary.
    """
    if classifications is None:
        classifications = [classify_source_path(clean) for clean in clean_source_paths]
    else:
        assert len(classifications) == len(clean_source_paths)

    branches: list[str] = []
    for clean_path, classification in zip(clean_source_paths, classifications):
        if classification.kind == "dir":
            continue
        if classification.kind == "file":
            # basename is guaranteed by PathClassification's contract.
            basename = classification.basename
            assert basename is not None
            if not _basename_is_pattern_safe(basename):
                # Anchoring on a basename Snowflake may URL-encode
                # would silently exclude the user's file (matches
                # nothing on the stage). Bail out of anchoring for
                # the whole read -- accepting potential prefix bleed
                # is preferable to losing the user's data entirely.
                return None
            escaped_basename = re.escape(basename)
            branches.append(f"(.*/)?{escaped_basename}(?:$|/(?:.*/)?[^_.][^/]*$)")
        else:  # glob
            assert classification.regex is not None
            # SNOW-3594869: Snowflake matches PATTERN against the full
            # stage-relative LIST path (including the temp stage prefix), so
            # glob reads must embed the scan-directory prefix with the same
            # ``(.*/)?`` head used for file/dir anchoring. A suffix-only regex
            # silently excludes every staged file.
            scan_prefix, _ = split_glob_scan_prefix(clean_path)
            stage_rel_prefix = _scan_prefix_stage_relative(scan_prefix)
            if stage_rel_prefix:
                escaped_prefix = re.escape(stage_rel_prefix.rstrip("/") + "/")
                branches.append(f"(.*/)?{escaped_prefix}{classification.regex}$")
            else:
                branches.append(f"(.*/)?{classification.regex}$")
    if not branches:
        return None
    if len(branches) == 1:
        return branches[0]
    return "|".join(f"(?:{b})" for b in branches)


# Formats whose readers translate Spark's ``pathGlobFilter`` option into
# Snowflake's ``PATTERN`` clause via ``reader_config``. The list is
# kept explicit (rather than derived from ``reader_config``) for two
# reasons:
#
#   1. Avoid an import cycle -- ``reader_config`` is loaded lazily by
#      the format-specific readers from inside ``map_read._read_file``.
#   2. Anchoring is a behavioral change; new formats should be opted in
#      deliberately rather than picked up implicitly by adding
#      ``"pathGlobFilter"`` to a reader's supported_options.
#
# When adding a format here, confirm ``"pathGlobFilter"`` is also in
# its ``supported_options`` in ``relation/read/reader_config.py``.
#
# The text reader uses a different SQL path (LIST + per-file SELECT)
# and is therefore not anchored here -- its directory-bleed case is
# handled client-side in :func:`map_read_text.read_text` via
# :func:`filter_list_paths_for_non_recursive_read` when
# ``recursiveFileLookup=false`` is set.
#
# XML uses a per-file COPY INTO loop. Directory expansion in
# :func:`map_read_xml._generate_list_of_files` is gated on
# ``recursiveFileLookup`` (direct-child ``.xml`` when false, any depth
# when true). Including ``xml`` here adds PATTERN-based anchoring for
# explicit file paths and depth-0 regex when ``recursiveFileLookup=false``
# on dir reads (deeper files simply produce zero rows under the per-file
# PATTERN).
_FORMATS_HONORING_PATH_GLOB_FILTER = frozenset({"csv", "json", "parquet", "xml"})


# ---------------------------------------------------------------------------
# recursiveFileLookup=false support (SNOW-3295580)
# ---------------------------------------------------------------------------

# Lowercase form of the Spark option key ``recursiveFileLookup``. We compare
# against this lowercase form so callers can pop the key from ``options``
# without caring whether the user spelled it ``recursiveFileLookup``,
# ``RECURSIVEFILELOOKUP``, or any case in between.
_RECURSIVE_FILE_LOOKUP_KEY = "recursivefilelookup"


def _stage_relative_dir_prefix(clean_path: str) -> str:
    """Return the stage-relative directory prefix (with trailing ``/``) for a dir-kind path.

    Returns ``""`` for stage-root reads (e.g. ``@stage`` with no subpath) so
    callers can build the pattern ``[^_.][^/]*$`` without a leading slash.

    The returned prefix mirrors the stage-relative path that
    :mod:`stage_locator` puts files under so the PATTERN regex (matched
    by Snowflake against the *full* relative path within the stage) can
    actually align with the uploaded layout. In particular, local paths
    are uploaded under ``{stage}/<last_two_components>`` (see
    ``stage_locator.get_paths_from_stage``) -- if we returned just the
    basename here the PATTERN would silently exclude every file because
    ``parent_dir/file.csv`` does not match ``^dir/[^_.][^/]*$``.
    """
    stripped = clean_path.strip("'\"").rstrip("/")

    if stripped.startswith("@"):
        if "/" not in stripped:
            return ""
        return stripped.split("/", 1)[1] + "/"

    if is_cloud_path(stripped):
        scheme, rest = stripped.split("://", 1)
        parts = rest.split("/")
        subparts = parts[2:] if scheme.lower() == "azure" else parts[1:]
        rel = "/".join(subparts)
        return (rel + "/") if rel else ""

    local = convert_file_prefix_path(stripped)
    if not local:
        return ""
    # Mirror ``stage_locator.get_paths_from_stage``: local source dirs are
    # uploaded under ``{stage}/<last_two_components>`` so that's the prefix
    # the PATTERN regex must align with. Falling back to just the basename
    # (when the path has only one component) matches the same fallback in
    # ``stage_locator``.
    parts = local.replace(os.sep, "/").split("/")
    parts = [p for p in parts if p]
    if len(parts) >= 2:
        return "/".join(parts[-2:]) + "/"
    return (parts[0] + "/") if parts else ""


def _interpret_recursive_value(value: Any) -> bool:
    """Interpret an explicit ``recursiveFileLookup`` option value as a boolean (SNOW-3566246).

    Used only when the user set the key. Truthy means recursive listing;
    ``{"false", "0"}`` (case-insensitive, after stripping) means depth-0.
    When the key is absent, :func:`consume_recursive_file_lookup` defaults to
    non-recursive listing to match Spark.
    """
    return str(value).strip().lower() not in ("false", "0")


def consume_recursive_file_lookup(options: dict[str, Any]) -> RecursiveFileLookup:
    """Pop ``recursiveFileLookup`` and resolve listing vs partition semantics (SNOW-3566246).

    Listing (``is_recursive``): ``False`` when the key is missing (Spark's
    default). ``True`` only when the user explicitly sets a truthy value
    (anything other than ``{"false", "0"}``, case-insensitive).

    Partition discovery (``skip_partition_discovery``): ``True`` only when the
    user explicitly sets a truthy value. When the key is absent, partition
    discovery remains enabled even though listing defaults to depth-0.

    Mutates ``options`` in place by removing every key whose lowercase form
    matches ``recursivefilelookup`` so the value cannot leak through to
    Snowflake's COPY INTO via ``convert_to_snowpark_args``.
    """
    is_recursive = False
    skip_partition_discovery = False
    keys_to_pop = [
        k for k in list(options.keys()) if k.lower() == _RECURSIVE_FILE_LOOKUP_KEY
    ]
    for k in keys_to_pop:
        value = options.pop(k)
        if _interpret_recursive_value(value):
            is_recursive = True
            skip_partition_discovery = True
        else:
            is_recursive = False
            skip_partition_discovery = False
    return RecursiveFileLookup(is_recursive, skip_partition_discovery)


def _basename_not_hidden(path: str) -> bool:
    """Spark ``HiddenFileFilter`` parity for a path's basename."""
    base = os.path.basename(path)
    return not (base.startswith("_") or base.startswith("."))


def _suffix_is_hive_layout_data_file(suffix: str) -> bool:
    """True when ``suffix`` is ``(key=value/)*file`` with a non-hidden basename."""
    suffix = suffix.strip("/")
    if not suffix:
        return False
    parts = suffix.split("/")
    for segment in parts[:-1]:
        if not _HIVE_PARTITION_DIR_RE.fullmatch(segment):
            return False
    return _basename_not_hidden(parts[-1])


def _stage_relative_list_prefix(read_path: str) -> str:
    """Stage-relative path shape returned by ``read_text`` LIST (after upload)."""
    stripped = read_path.strip("'\"").rstrip("/")
    if stripped.startswith("@"):
        return stripped.split("/", 1)[1] if "/" in stripped else ""
    if is_cloud_path(stripped):
        scheme, rest = stripped.split("://", 1)
        parts = rest.split("/")
        subparts = parts[2:] if scheme.lower() == "azure" else parts[1:]
        return "/".join(subparts)
    local = convert_file_prefix_path(stripped)
    if not local:
        return ""
    parts = local.replace(os.sep, "/").split("/")
    parts = [p for p in parts if p]
    if len(parts) >= 2:
        return "/".join(parts[-2:])
    return parts[0] if parts else ""


def _non_recursive_read_is_explicit_file(
    read_path: str, classification: PathClassification
) -> bool:
    """True when ``read_path`` names one file, not a directory to list."""
    raw = read_path.strip("'\"")
    stripped = raw.rstrip("/")
    if raw.endswith("/"):
        return False
    local = convert_file_prefix_path(stripped) if not is_cloud_path(stripped) else None
    if local is not None:
        if os.path.isdir(local):
            return False
        if os.path.isfile(local):
            return True
    if _looks_like_explicit_file_path(stripped):
        return True
    basename = classification.basename
    if not basename:
        return False
    rel = _stage_relative_list_prefix(stripped)
    parts = [p for p in rel.split("/") if p]
    # ``a/b/c`` (3+ components) with terminal basename => staged file path.
    return bool(parts) and parts[-1] == basename and len(parts) >= 3


def filter_list_paths_for_non_recursive_read(
    file_paths: list[str],
    read_path: str,
) -> list[str]:
    """Keep LIST paths allowed under Spark ``recursiveFileLookup=false`` (SNOW-3566246).

    Mirrors :func:`compute_non_recursive_pattern`: depth-0 data files plus
    arbitrary-depth Hive ``key=value/`` segments, while rejecting hidden
    basenames and non-partition subtrees such as ``sub/nested/file.txt``.
    """
    stripped = read_path.strip("'\"").rstrip("/")
    classification = classify_source_path(stripped)
    if _non_recursive_read_is_explicit_file(read_path, classification):
        basename = classification.basename
        assert basename is not None
        rel_target = _stage_relative_list_prefix(stripped)
        return [
            fp
            for fp in file_paths
            if _basename_not_hidden(fp)
            and (fp.lstrip("/") == rel_target or os.path.basename(fp) == basename)
        ]

    rel = _stage_relative_list_prefix(stripped)
    if not rel:
        max_slashes = stripped.count("/")
        return [
            fp
            for fp in file_paths
            if fp.count("/") <= max_slashes and _basename_not_hidden(fp)
        ]

    norm_prefix = rel.rstrip("/") + "/"
    kept: list[str] = []
    for fp in file_paths:
        norm_fp = fp.lstrip("/")
        if norm_fp.startswith(norm_prefix):
            suffix = norm_fp[len(norm_prefix) :]
        else:
            continue
        if _suffix_is_hive_layout_data_file(suffix):
            kept.append(fp)
    return kept


def compute_non_recursive_pattern(
    clean_source_paths: list[str],
    classifications: list[PathClassification],
) -> str | None:
    """Build a depth-0 PATTERN regex for dir-kind source paths.

    Restricts Snowflake stage reads to files sitting *directly* inside the
    target directory (no subdirectory descent). Non-dir paths produce no
    branch (file/glob kinds already name specific files).

    The regex emitted for a prefixed dir is an alternation of two branches
    (SNOW-3707457)::

        (?:(.*/)?{escaped_prefix}{hive_tail})|(?:{hive_tail})

    where ``{hive_tail}`` is ``({_HIVE_PARTITION_DIR_PATTERN}/)*[^_.][^/]*$``.
    Zero ``{hive}/`` repetitions match depth-0 files; one or more match
    Hive-partitioned layouts while still rejecting arbitrary non-partition
    nesting such as ``sub/nested/file.csv`` (segments without ``=`` are not
    matched).

    The two branches exist because Snowflake's ``LIST`` / staged-``SELECT``
    ``PATTERN`` matching scope is **not consistent across deployments**, and
    nothing SCOS can observe (stage type, ``LIST`` row shape, version)
    distinguishes them:

      * Full-path scope: ``PATTERN`` is matched against the full
        stage-relative path (e.g. ``stage_name/dir/file`` for internal
        stages, or the full ``s3://bucket/.../file`` URL for external ones).
        The prefixed branch is required here; the bare ``{hive_tail}`` branch
        is inert because a real path always carries a leading stage/bucket
        component it cannot full-match.
      * Listed-dir scope: ``PATTERN`` is matched against the path *relative
        to the listed directory* (just ``file`` / ``part=1/file``). Here the
        prefixed branch matches nothing (the prefix never appears) and the
        bare ``{hive_tail}`` branch carries the read.

    Emitting both makes the depth-0 read return the right rows under either
    scope while still enforcing depth-0 in both (a nested ``sub/file``
    relative path cannot full-match ``{hive_tail}`` because ``[^/]`` will not
    cross ``/``). Verified live on two deployments that scope oppositely.

    Stage-root reads (no dir prefix) reduce to ``(.*/)?[^_.][^/]*$`` and
    have a known limitation: with no fixed prefix to anchor on, the
    ``(.*/)?`` head greedily eats any number of leading components,
    including a ``sub/`` directory we'd want to reject. Stage-root +
    ``recursiveFileLookup=false`` is therefore best-effort -- it works
    when files live directly at the stage root (the common case) but
    cannot strictly enforce depth-0 against arbitrary nested layouts at
    the root. Users wanting strict depth-0 should pass an explicit
    subdirectory. No separate relative branch is added for stage-root reads
    because the prefix-less full-path branch already permits relative paths.

    Metadata sidecars (``_SUCCESS``, ``.crc``) are excluded via
    ``[^_.]``.

    Returns ``None`` when no dir-kind paths are present, or when ANY dir
    prefix contains a character Snowflake URL-encodes in stage relative
    paths (mirrors :func:`_basename_is_pattern_safe`'s bail-out semantics
    in :func:`compute_anchor_pattern` -- producing a regex that silently
    excludes the user's data is worse than producing none at all).
    """
    hive_tail = f"({_HIVE_PARTITION_DIR_PATTERN}/)*[^_.][^/]*$"
    branches: list[str] = []
    saw_prefixed_dir = False
    for path, cls in zip(clean_source_paths, classifications):
        if cls.kind != "dir":
            continue
        prefix = _stage_relative_dir_prefix(path)
        if _dir_prefix_unsafe_for_depth0_pattern(prefix):
            return None
        escaped_prefix = re.escape(prefix)
        branches.append(f"(.*/)?{escaped_prefix}{hive_tail}")
        if escaped_prefix:
            saw_prefixed_dir = True
    if not branches:
        return None
    # SNOW-3707457: deployments that match PATTERN relative to the listed
    # directory need the prefix-less branch to return any rows. Added once
    # (it is prefix-independent) and only when at least one dir carried a
    # non-empty prefix -- stage-root branches already subsume it.
    if saw_prefixed_dir:
        branches.append(hive_tail)
    if len(branches) == 1:
        return branches[0]
    return "|".join(f"(?:{b})" for b in branches)


def _alternation(*regex_parts: str | None) -> str | None:
    """Join one or more regex strings with non-capturing alternation.

    ``None`` parts are filtered out. Returns ``None`` when every part is
    ``None``. A single non-``None`` part is returned unchanged so the
    common case (file-only or dir-only read) keeps the simple regex shape
    callers already assert on.
    """
    parts = [p for p in regex_parts if p]
    if not parts:
        return None
    if len(parts) == 1:
        return parts[0]
    return "|".join(f"(?:{p})" for p in parts)


def inject_anchor_pattern(
    clean_source_paths: list[str],
    options: dict[str, Any],
    read_format: str,
    classifications: list[PathClassification] | None = None,
    *,
    is_recursive: bool = True,
) -> None:
    """Inject a Snowflake PATTERN that anchors stage reads to user-named files.

    Defeats Snowflake stage prefix matching for explicit file and glob
    paths (SNOW-3428536) and, when ``is_recursive=False`` (i.e., the
    user set ``recursiveFileLookup=false``), additionally restricts
    directory branches to depth-0 (SNOW-3295580).

    Behavior:
        * Gated by the ``snowpark.connect.read.anchorStagePaths`` config
          (default true). Setting it to ``false`` is a safety hatch that
          reverts to the legacy unanchored AND recursive behavior.
        * Only applied to formats whose readers plumb ``pathGlobFilter``
          through to Snowflake's ``PATTERN`` (csv/json/parquet/xml). The
          text reader uses a different SQL path (LIST + per-file SELECT)
          and handles depth-0 client-side in ``map_read_text``.
        * If the user explicitly supplied ``pathGlobFilter`` / ``PATTERN``,
          the user's value is preserved and we do NOT inject -- combining
          a user glob with a regex anchor is unsafe and the rare case is
          better surfaced as a no-op than silently mangled. Callers can
          combine manually if needed.

    The ``is_recursive`` argument should be the result of
    :func:`consume_recursive_file_lookup` so the ``recursiveFileLookup``
    option is popped from ``options`` exactly once at the call site and
    cannot leak through to Snowflake.

    The injected key is the Spark-side ``pathGlobFilter`` so that the
    standard reader_config translation maps it to Snowflake's ``PATTERN``
    clause, which the csv/json/parquet/xml readers already plumb through
    to ``COPY INTO`` / staged-table SELECT.
    """
    if not is_anchor_stage_paths_enabled():
        return

    if read_format.lower() not in _FORMATS_HONORING_PATH_GLOB_FILTER:
        return

    # Honor user's explicit pathGlobFilter / PATTERN.
    for existing_key in ("pathGlobFilter", "pathglobfilter", "PATTERN"):
        if existing_key in options and options[existing_key]:
            return

    if classifications is None:
        classifications = [classify_source_path(p) for p in clean_source_paths]

    anchor = compute_anchor_pattern(clean_source_paths, classifications)
    depth0 = (
        compute_non_recursive_pattern(clean_source_paths, classifications)
        if not is_recursive
        else None
    )
    combined = _alternation(anchor, depth0)
    if combined is None:
        return

    options["pathGlobFilter"] = combined


def inject_non_recursive_pattern(
    clean_source_paths: list[str],
    options: dict[str, Any],
    classifications: list[PathClassification],
) -> None:
    """Backwards-compatible shim around :func:`inject_anchor_pattern`.

    No production callers; :func:`map_read._read_file` uses
    :func:`inject_anchor_pattern` instead. Unit tests in
    ``test_stage_path_anchoring`` still exercise this entry point.

    The behavior previously split between ``inject_anchor_pattern`` and
    ``inject_non_recursive_pattern`` is now handled in a single pass by
    :func:`inject_anchor_pattern`. This shim only exists for callers that
    invoked the legacy entry point directly; it consumes the
    ``recursiveFileLookup`` key and, when ``false``, writes the depth-0
    PATTERN into ``options["pathGlobFilter"]``.

    Prefer calling :func:`inject_anchor_pattern` (with
    ``is_recursive=consume_recursive_file_lookup(options).is_recursive``)
    instead -- the merged helper avoids the order-dependent override bug
    that the old two-step flow exhibited for mixed file+dir reads.
    """
    is_recursive = consume_recursive_file_lookup(options).is_recursive
    if is_recursive:
        return

    if not is_anchor_stage_paths_enabled():
        return

    pattern = compute_non_recursive_pattern(clean_source_paths, classifications)
    if pattern is None:
        return

    # The user-set pathGlobFilter case is genuinely ambiguous (Spark would
    # AND both filters; we override). Only warn when the value was set by
    # the *caller*, not by this module: callers using the modern unified
    # path go through :func:`inject_anchor_pattern` instead and never hit
    # this shim, so any ``pathGlobFilter`` we see here is user-supplied.
    for existing_key in ("pathGlobFilter", "pathglobfilter", "PATTERN"):
        if options.get(existing_key):
            logger.warning(
                "recursiveFileLookup=false overrides an existing pathGlobFilter/PATTERN "
                "value. The depth-0 restriction pattern will replace it."
            )
            break

    options["pathGlobFilter"] = pattern
