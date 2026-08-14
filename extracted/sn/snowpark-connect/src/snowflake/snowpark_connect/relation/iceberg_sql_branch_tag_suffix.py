#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Resolve Iceberg SQL ``.<table>.branch_<name>`` / ``.<table>.tag_<name>``
identifier suffixes into the canonical Iceberg DataFrame reader option form
handled by ``map_read_table.py``.

Native Spark/Iceberg (with ``IcebergSparkSessionExtensions``) treats a trailing
multipart identifier whose last segment matches ``branch_<name>`` or
``tag_<name>`` as a WAP branch or version-tag read. SCOS mirrors that at the
``UnresolvedRelation`` layer so SQL reads converge on the same Snowpark
``read.option("branch" | "tag", ...).table(...)`` path as DataFrame reads and
``VERSION AS OF`` time travel.

Examples::

    SELECT * FROM db.schema.t.branch_audit
    SELECT * FROM schema.t.tag_first_load
    SELECT * FROM t.`branch_audit-branch`

Scope
-----
Read-only table references parsed into ``UnresolvedRelation``. Requires
``spark.sql.extensions`` to include the Iceberg extension class — same gate as
SQL ``VERSION AS OF`` / explicit ``option("branch")`` reads.

Branch/tag vs literal table name (known limitation)
----------------------------------------------------
When Iceberg SQL extensions are enabled, SCOS gives **precedence to the branch
or tag suffix** whenever the last dot-separated segment matches
``branch_<name>`` or ``tag_<name>``. There is no catalog lookup to see whether
a real table exists with that full multipart name.

For example, ``SELECT * FROM db.schema.branch_foo`` is rewritten to a branch
read of ``db.schema`` at branch ``foo``, not a read of a table literally named
``branch_foo``. Native Iceberg resolves the parent identifier as a table first
and only treats the trailing segment as a branch/tag selector when that parent
resolves.

If customers later need literal ``branch_*`` / ``tag_*`` table names to win,
SCOS would need a metadata probe (e.g. catalog ``SHOW TABLES`` /
``information_schema``) and only apply suffix stripping when the parent table
exists and the suffixed name does not resolve as a table. That lookup is
deferred until there is a concrete requirement.
"""

from __future__ import annotations

import re

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name_with_quoting,
)

_BRANCH_SUFFIX_RE = re.compile(r"^branch_(.*)$")
_TAG_SUFFIX_RE = re.compile(r"^tag_(.*)$")


def _format_multipart_spark_identifier(
    parts: list[str], backtick_flags: list[bool]
) -> str:
    """Rebuild a dot-separated Spark identifier, preserving per-part backticks."""
    rendered: list[str] = []
    for part, quoted in zip(parts, backtick_flags):
        if quoted:
            rendered.append(f"`{part.replace('`', '``')}`")
        else:
            rendered.append(part)
    return ".".join(rendered)


def _suffix_kind_and_name(
    last_part: str, backtick_quoted: bool
) -> tuple[str, str] | None:
    """Return ``(kind, name)`` for ``branch`` / ``tag`` when the last segment matches.

    ``last_part`` is the unquoted form from
    ``split_fully_qualified_spark_name_with_quoting``. When the SQL surface used
    backticks around the suffix segment (``.`branch_audit-branch` ``), we still
    match on the unquoted text — the ``backtick_quoted`` flag is accepted for
    call-site clarity and future validation but matching is always on the
    unquoted ``branch_<name>`` / ``tag_<name>`` prefix.
    """
    _ = backtick_quoted
    branch_match = _BRANCH_SUFFIX_RE.match(last_part)
    if branch_match is not None:
        return "branch", branch_match.group(1)
    tag_match = _TAG_SUFFIX_RE.match(last_part)
    if tag_match is not None:
        return "tag", tag_match.group(1)
    return None


def try_parse_iceberg_branch_tag_suffix(
    table_name: str,
) -> tuple[str, dict[str, str]] | None:
    """If ``table_name`` ends with ``.branch_<name>`` or ``.tag_<name>``, return
    ``(base_table_name, iceberg_reader_options)``.

    ``iceberg_reader_options`` uses the same keys as
    ``spark.read.format("iceberg").option(...)`` — ``branch`` or ``tag``.
    Returns ``None`` when the identifier does not carry a recognized suffix.

    Callers must gate on ``is_iceberg_sql_extensions_enabled()`` before
    treating a match as an Iceberg branch/tag read. Without the Iceberg SQL
    extension, names like ``db.schema.branch_report`` are ordinary multipart
    table identifiers, not WAP branch refs.

    When extensions are enabled, a matching suffix always wins over a literal
    table name (see module docstring). No catalog existence check is performed.
    """
    parts, backtick_flags = split_fully_qualified_spark_name_with_quoting(table_name)
    if len(parts) < 2:
        return None

    suffix = _suffix_kind_and_name(parts[-1], backtick_flags[-1])
    if suffix is None:
        return None

    kind, ref_name = suffix
    if not ref_name.strip():
        _raise_empty_suffix_name(kind)

    base_name = _format_multipart_spark_identifier(parts[:-1], backtick_flags[:-1])
    if kind == "branch":
        return base_name, {"branch": ref_name}
    return base_name, {"tag": ref_name}


def try_parse_iceberg_branch_tag_suffix_parts(
    parts: list[str],
) -> tuple[list[str], dict[str, str]] | None:
    """Parse a branch/tag suffix from Catalyst multipart segments.

    Unlike ``try_parse_iceberg_branch_tag_suffix``, this does **not** split the
    identifier on ``.`` — required when an earlier segment itself contains dots
    (e.g. Spark database ``blah.@#$`` with table ``$.%``).
    """
    if len(parts) < 2:
        return None

    suffix = _suffix_kind_and_name(parts[-1], False)
    if suffix is None:
        return None

    kind, ref_name = suffix
    if not ref_name.strip():
        _raise_empty_suffix_name(kind)

    base_parts = parts[:-1]
    if kind == "branch":
        return base_parts, {"branch": ref_name}
    return base_parts, {"tag": ref_name}


def iceberg_branch_tag_suffix_extensions_disabled_exception() -> AnalysisException:
    """Build the customer-visible error when extensions are unset."""
    exception = AnalysisException(
        "Iceberg SQL branch/tag identifier suffixes "
        "('SELECT * FROM <table>.branch_<name>' / "
        "'<table>.tag_<name>') are gated on the "
        "'spark.sql.extensions' config naming the Iceberg Spark SQL "
        "extensions class. SCOS implements these reads natively (no extra "
        "JAR install is required), but the customer-visible support "
        "contract still requires the flag. Set it on the SCOS server "
        "(e.g. in spark-defaults.conf or via the "
        "SPARK_CONF_spark__sql__extensions env var) to: "
        "'org.apache.iceberg.spark.extensions."
        "IcebergSparkSessionExtensions'. This is a static config — "
        "``spark.conf.set()`` from the client is rejected on purpose "
        "by Spark's config rules."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def _raise_empty_suffix_name(kind: str) -> None:
    exception = AnalysisException(
        f"Iceberg SQL '{kind}_<name>' suffix requires a non-empty {kind} "
        f"name after the '{kind}_' prefix."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
    raise exception
