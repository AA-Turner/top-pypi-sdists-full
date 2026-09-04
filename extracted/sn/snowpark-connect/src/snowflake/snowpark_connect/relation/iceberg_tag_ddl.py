#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Translate Iceberg Spark SQL Extension tag DDL to Snowflake SQL.

Background
----------
The Iceberg Spark SQL Extensions add DDL for managing snapshot refs on
Iceberg tables. This module translates the **tag** subset of that DDL.
The Spark tag DDL surface, from the Iceberg docs
(https://iceberg.apache.org/docs/latest/spark-ddl/), is::

    ALTER TABLE <tbl> CREATE TAG <name>
    ALTER TABLE <tbl> CREATE TAG IF NOT EXISTS <name>
    ALTER TABLE <tbl> CREATE OR REPLACE TAG <name>
    ALTER TABLE <tbl> CREATE TAG <name> AS OF VERSION <snapshot_id>
    ALTER TABLE <tbl> CREATE TAG <name> AS OF VERSION <id> RETAIN <N> DAYS
    ALTER TABLE <tbl> REPLACE TAG <name> AS OF VERSION <id> [RETAIN <N> DAYS]
    ALTER TABLE <tbl> DROP TAG <name>
    ALTER TABLE <tbl> DROP TAG IF EXISTS <name>

Snowflake's surface (per internal design doc, alignment confirmed with
the SCOS owners on 2026-06-11) renames the keyword ``TAG`` to
``VERSION_TAG`` and uses ``ALTER ICEBERG TABLE`` instead of the bare
``ALTER TABLE``. Snapshot binding is expressed as a trailing
``AS OF VERSION <id>`` or ``AS OF TIMESTAMP <ts>`` clause when the Spark
SQL supplies one; bare ``CREATE TAG <name>`` omits the clause and
Snowflake binds the tag to the current head snapshot::

    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG <name>
    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE OR REPLACE VERSION_TAG <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG IF NOT EXISTS <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG IF NOT EXISTS <name> AS OF TIMESTAMP <ts>
    ALTER ICEBERG TABLE <tbl> ALTER VERSION_TAG <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> DROP VERSION_TAG <name>
    ALTER ICEBERG TABLE <tbl> DROP VERSION_TAG IF EXISTS <name>

Snowflake bridged the IF NOT EXISTS / CREATE OR REPLACE / AS OF TIMESTAMP
forms for ``CREATE VERSION_TAG`` in 2026-Q3 (server-side TAG SQL gap
closure). SCOS emits those Snowflake shapes when the Iceberg logical
plan (or a Snowflake-extended ``AS OF TIMESTAMP`` SQL string that the
stock Iceberg parser does not yet model) supplies the binding.

The renaming avoids a clash with Snowflake's own object-level ``TAG``
concept (governance tags on tables / columns / databases) which is
unrelated to Iceberg's snapshot-ref tags. SCOS bridges the two surfaces
at translation time.

JVM source
----------
The Iceberg Spark SQL Extensions parser
(``iceberg-spark-extensions-3.5_2.12-1.9.2.jar``) emits the following
logical plan classes; the relevant accessors used by this module are
listed alongside each one.

* ``org.apache.spark.sql.catalyst.plans.logical.CreateOrReplaceTag``

  - ``table(): Seq[String]`` — the multipart table identifier.
  - ``tag(): String`` — the tag name (unquoted; Iceberg's parser strips
    the backticks that the user writes around special characters).
  - ``tagOptions(): TagOptions`` — see below.
  - ``create(): Boolean`` — true when the source SQL uses ``CREATE``.
  - ``replace(): Boolean`` — true when the source SQL uses ``REPLACE``.
    ``CREATE OR REPLACE`` sets both ``create`` and ``replace``.
  - ``ifNotExists(): Boolean`` — true when the source SQL uses
    ``IF NOT EXISTS``.

* ``org.apache.spark.sql.catalyst.plans.logical.DropTag``

  - ``table(): Seq[String]``
  - ``tag(): String``
  - ``ifExists(): Boolean``

* ``org.apache.spark.sql.catalyst.plans.logical.TagOptions``

  - ``snapshotId(): Option[Long]`` — the ``AS OF VERSION <id>`` clause.
  - ``snapshotRefRetain(): Option[Long]`` — the ``RETAIN <N> DAYS``
    clause, encoded as a millisecond duration.
  - Optional future accessors (``snapshotTimestamp()`` /
    ``asOfTimestamp()``) — if a future Iceberg extension jar adds an
    ``AS OF TIMESTAMP`` binding, SCOS will translate it to Snowflake's
    trailing ``AS OF TIMESTAMP <ts>`` clause without a code change.

Translation policy
------------------
* The base forms ``CREATE TAG`` / ``DROP TAG`` are translated directly.
* ``IF NOT EXISTS`` (for CREATE) and ``IF EXISTS`` (for DROP) pass
  through to Snowflake — both are Snowflake-standard idioms.
* ``CREATE OR REPLACE`` passes through — again, Snowflake-standard.
* Bare ``REPLACE TAG … AS OF VERSION <id>`` (no CREATE) maps to
  ``ALTER VERSION_TAG … AS OF VERSION <id>``. ``REPLACE TAG`` without
  an ``AS OF VERSION`` / ``AS OF TIMESTAMP`` binding raises
  ``UNSUPPORTED_OPERATION``.
* ``AS OF VERSION <id>`` (snapshot-pinned tag creation) is translated
  to a trailing ``AS OF VERSION <id>`` clause on the Snowflake
  ``CREATE VERSION_TAG`` DDL. The server-side surface was confirmed
  by direct parser probing on 2026-06-12.
* ``AS OF TIMESTAMP <ts>`` (timestamp-pinned tag creation) is translated
  to a trailing ``AS OF TIMESTAMP <ts>`` clause when the binding is
  available. The stock ``iceberg-spark-extensions`` parser (1.10.x)
  does not yet emit this in ``TagOptions``; SCOS also accepts the
  Snowflake-extended Spark SQL string
  ``ALTER TABLE … CREATE TAG [IF NOT EXISTS] <name> AS OF TIMESTAMP …``
  via a pre-parse hook in ``map_sql.py`` (see
  ``match_create_tag_as_of_timestamp_sql``).
* The bare ``CREATE TAG <name>`` form (no ``AS OF VERSION``) — Iceberg's
  canonical "tag the current head" idiom — is translated to bare
  ``CREATE VERSION_TAG <name>`` and Snowflake binds the tag to the
  current head snapshot. Explicit ``AS OF VERSION <id>`` / ``AS OF
  TIMESTAMP <ts>`` bindings still pass through when supplied.
* ``RETAIN <N> DAYS`` is translated to a trailing ``RETAIN <N> DAYS``
  clause when ``TagOptions.snapshotRefRetain()`` is set. Iceberg encodes
  the duration in milliseconds; SCOS lowers it to whole-day literals for
  Snowflake's ``CREATE VERSION_TAG`` / ``ALTER VERSION_TAG`` grammar.
* The emitted SQL always uses ``ALTER ICEBERG TABLE`` (not the
  type-detecting ``_execute_alter`` helper): tag DDL only makes sense
  on Iceberg-backed tables, so skipping the catalog round-trip is
  both correct and faster. If the customer points the DDL at a
  non-Iceberg table, Snowflake's parser returns a clear error.

Identifier handling
-------------------
* The table identifier is converted by the caller using
  ``_spark_to_snowflake`` (the standard SCOS multipart-id resolver
  that honors per-part backtick state).
* The tag name is wrapped with
  ``quote_name_without_upper_casing`` — this always emits
  ``"<escaped-name>"`` form with embedded double quotes doubled,
  making the emitted SQL safe against tag names that contain hyphens
  (``audit-tag``), spaces, or stray double quotes. Snowflake accepts
  both quoted and unquoted identifiers; defensive quoting is the
  simpler invariant to maintain on the SCOS boundary.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any as TypingAny

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.telemetry import telemetry


@dataclass(frozen=True)
class CreateTagAsOfTimestampMatch:
    """Parsed ``ALTER TABLE … CREATE TAG … AS OF TIMESTAMP …`` SQL."""

    table_sql: str
    tag_name: str
    if_not_exists: bool
    create_or_replace: bool
    timestamp_sql: str


_MILLIS_PER_DAY = 24 * 60 * 60 * 1000

_CREATE_TAG_AS_OF_TIMESTAMP_SQL = re.compile(
    r"""
    (?is)
    ^ALTER\s+TABLE\s+
    (?P<table>.+?)\s+
    CREATE\s+
    (?:(?P<or_replace>OR\s+REPLACE)\s+)?
    TAG\s+
    (?:(?P<if_not_exists>IF\s+NOT\s+EXISTS)\s+)?
    (?P<tag>`(?:[^`]|``)*`|"(?:[^"]|"")*"|'(?:[^']|'')*'|[^\s]+)
    \s+AS\s+OF\s+TIMESTAMP\s+
    (?P<timestamp>'(?:[^']|'')*'|\d+)
    \s*$
    """,
    re.VERBOSE,
)


def _strip_spark_identifier_quotes(identifier: str) -> str:
    text = identifier.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"`", '"', "'"}:
        inner = text[1:-1]
        if text[0] == "`":
            return inner.replace("``", "`")
        return inner.replace(text[0] * 2, text[0])
    return text


def _format_tag_as_of_timestamp_literal(value: TypingAny) -> str:
    """Format a timestamp binding for Snowflake ``AS OF TIMESTAMP``."""
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("'") and stripped.endswith("'"):
            return stripped
        escaped = stripped.replace("'", "''")
        return f"'{escaped}'"
    if isinstance(value, int):
        return str(value)
    return str(value)


def _get_tag_snapshot_timestamp(options: TypingAny) -> str | None:
    for accessor in ("snapshotTimestamp", "asOfTimestamp"):
        if not hasattr(options, accessor):
            continue
        timestamp_opt = getattr(options, accessor)()
        if timestamp_opt.isDefined():
            return _format_tag_as_of_timestamp_literal(timestamp_opt.get())
    return None


def _build_create_version_tag_action(
    *,
    tag_name: str,
    create: bool,
    replace: bool,
    if_not_exists: bool,
) -> str:
    if create and replace:
        return "CREATE OR REPLACE VERSION_TAG"
    if create:
        action = "CREATE VERSION_TAG"
        if if_not_exists:
            action += " IF NOT EXISTS"
        return action
    if replace:
        return "ALTER VERSION_TAG"
    exception = AnalysisException(
        "Internal: Iceberg CreateOrReplaceTag plan has neither "
        "'create' nor 'replace' flag set; this is a parser invariant "
        "violation, please report it."
    )
    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
    raise exception


def _format_tag_retain_clause(retain_millis: int) -> str:
    """Lower Iceberg's millisecond ``snapshotRefRetain`` to ``RETAIN N DAYS``."""
    if retain_millis <= 0 or retain_millis % _MILLIS_PER_DAY != 0:
        telemetry.report_iceberg_wap(
            op="unsupported",
            surface="sql_call",
            ref_type="tag",
            ddl_action="create",
            outcome="rejected",
            error_code="UNSUPPORTED_OPERATION",
            detail="tag_retain_not_whole_days",
        )
        exception = AnalysisException(
            f"Iceberg RETAIN duration {retain_millis} ms cannot be translated "
            "to a whole number of DAYS for Snowflake VERSION_TAG DDL."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    days = retain_millis // _MILLIS_PER_DAY
    return f"RETAIN {days} DAYS"


def _build_create_version_tag_sql(
    *,
    table_name_sql: str,
    action: str,
    quoted_tag: str,
    as_of_clause: str | None = None,
    retain_clause: str | None = None,
) -> str:
    parts = [f"ALTER ICEBERG TABLE {table_name_sql}", action, quoted_tag]
    if as_of_clause is not None:
        parts.append(as_of_clause)
    if retain_clause is not None:
        parts.append(retain_clause)
    return " ".join(parts)


def match_create_tag_as_of_timestamp_sql(
    sql_string: str,
) -> CreateTagAsOfTimestampMatch | None:
    """Match Snowflake-extended ``CREATE TAG … AS OF TIMESTAMP`` SQL.

    The stock Iceberg Spark SQL Extensions parser (1.10.x) only models
    ``AS OF VERSION`` in ``TagOptions``; this matcher handles the
    timestamp binding that Snowflake accepts on ``CREATE VERSION_TAG``.
    """
    match = _CREATE_TAG_AS_OF_TIMESTAMP_SQL.match(sql_string.strip())
    if match is None:
        return None
    return CreateTagAsOfTimestampMatch(
        table_sql=match.group("table").strip(),
        tag_name=_strip_spark_identifier_quotes(match.group("tag")),
        if_not_exists=match.group("if_not_exists") is not None,
        create_or_replace=match.group("or_replace") is not None,
        timestamp_sql=match.group("timestamp").strip(),
    )


def translate_create_tag_as_of_timestamp_match(
    match: CreateTagAsOfTimestampMatch,
    table_name_sql: str,
) -> str:
    """Lower a parsed ``AS OF TIMESTAMP`` CREATE TAG statement."""
    if match.create_or_replace:
        action = "CREATE OR REPLACE VERSION_TAG"
    else:
        action = "CREATE VERSION_TAG"
        if match.if_not_exists:
            action += " IF NOT EXISTS"
    quoted_tag = quote_name_without_upper_casing(match.tag_name)
    as_of_clause = f"AS OF TIMESTAMP {match.timestamp_sql}"
    telemetry.report_iceberg_wap(
        op="tag_ddl",
        surface="sql_call",
        ref_type="tag",
        ddl_action="create",
    )
    return _build_create_version_tag_sql(
        table_name_sql=table_name_sql,
        action=action,
        quoted_tag=quoted_tag,
        as_of_clause=as_of_clause,
    )


def translate_create_or_replace_tag(rel: TypingAny, table_name_sql: str) -> str:
    """Translate ``ALTER TABLE … CREATE/REPLACE TAG …`` to Snowflake SQL.

    See module docstring for the translation policy. Raises
    ``AnalysisException`` with ``UNSUPPORTED_OPERATION`` for variants
    that cannot be confidently translated.
    """
    tag_name = str(rel.tag())
    create = bool(rel.create())
    replace = bool(rel.replace())
    if_not_exists = bool(rel.ifNotExists())

    options = rel.tagOptions()
    snapshot_id_opt = options.snapshotId()
    snapshot_retain_opt = options.snapshotRefRetain()

    snapshot_id: int | None
    if snapshot_id_opt.isDefined():
        # Cast through ``int`` so we don't embed a JPype ``java.lang.
        # Long`` representation into the emitted SQL — Snowflake's
        # parser expects a bare integer literal and any non-numeric
        # ``repr`` would silently break the DDL.
        snapshot_id = int(snapshot_id_opt.get())
    else:
        snapshot_id = None

    retain_clause: str | None = None
    if snapshot_retain_opt.isDefined():
        retain_clause = _format_tag_retain_clause(int(snapshot_retain_opt.get()))

    snapshot_timestamp = _get_tag_snapshot_timestamp(options)

    try:
        action = _build_create_version_tag_action(
            tag_name=tag_name,
            create=create,
            replace=replace,
            if_not_exists=if_not_exists,
        )
    except AnalysisException:
        raise

    if snapshot_id is not None:
        as_of_clause = f"AS OF VERSION {snapshot_id}"
    elif snapshot_timestamp is not None:
        as_of_clause = f"AS OF TIMESTAMP {snapshot_timestamp}"
    elif replace and not create:
        # Bare ``REPLACE TAG <name>`` (no ``AS OF VERSION`` / ``AS OF TIMESTAMP``):
        # Snowflake's ``ALTER VERSION_TAG`` requires an explicit snapshot binding
        # to repoint the tag, so we surface a clear error instead of emitting SQL
        # that would fail deep in the parser.
        telemetry.report_iceberg_wap(
            op="unsupported",
            surface="sql_call",
            ref_type="tag",
            ddl_action="replace",
            outcome="rejected",
            error_code="UNSUPPORTED_OPERATION",
            detail="replace_tag_no_version",
        )
        exception = AnalysisException(
            f"Iceberg 'ALTER TABLE … REPLACE TAG {tag_name!r}' (without "
            "'AS OF VERSION <id>' or 'AS OF TIMESTAMP <ts>') is not "
            "translated by Snowpark Connect: Snowflake's "
            "'ALTER VERSION_TAG' grammar requires an explicit snapshot "
            "binding. Rewrite as "
            f"'ALTER TABLE … REPLACE TAG {tag_name!r} AS OF VERSION "
            "<snapshot_id>'."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        as_of_clause = None

    quoted_tag = quote_name_without_upper_casing(tag_name)
    telemetry.report_iceberg_wap(
        op="tag_ddl",
        surface="sql_call",
        ref_type="tag",
        ddl_action="create",
    )
    return _build_create_version_tag_sql(
        table_name_sql=table_name_sql,
        action=action,
        quoted_tag=quoted_tag,
        as_of_clause=as_of_clause,
        retain_clause=retain_clause,
    )


def translate_drop_tag(rel: TypingAny, table_name_sql: str) -> str:
    """Translate ``ALTER TABLE … DROP TAG [IF EXISTS] <name>`` to Snowflake."""
    tag_name = str(rel.tag())
    if_exists = bool(rel.ifExists())

    action = "DROP VERSION_TAG"
    if if_exists:
        action += " IF EXISTS"
    quoted_tag = quote_name_without_upper_casing(tag_name)
    telemetry.report_iceberg_wap(
        op="tag_ddl",
        surface="sql_call",
        ref_type="tag",
        ddl_action="drop",
    )
    return f"ALTER ICEBERG TABLE {table_name_sql} {action} {quoted_tag}"
