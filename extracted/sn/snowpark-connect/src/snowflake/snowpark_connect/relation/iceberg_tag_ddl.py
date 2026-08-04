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
``ALTER TABLE``. The snapshot-id binding for ``CREATE VERSION_TAG`` is
expressed as a trailing ``AS OF VERSION <id>`` clause and is currently
**required** by the Snowflake parser (server-side probe 2026-06-12: any
``CREATE VERSION_TAG <name>`` form without a trailing ``AS OF VERSION``
errors with ``unexpected '<EOF>'``, whether the SQL reaches Snowflake
through SCOS translation or through SCOS SQL passthrough mode
``snowpark.connect.sql.passthrough=true`` — the restriction is
Snowflake-server-side, not SCOS-side, so passthrough is **not** an
escape hatch for the bare form)::

    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE OR REPLACE VERSION_TAG <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG IF NOT EXISTS <name> AS OF VERSION <id>
    ALTER ICEBERG TABLE <tbl> CREATE VERSION_TAG IF NOT EXISTS <name> AS OF TIMESTAMP <ts>
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
* Bare ``REPLACE TAG`` (no CREATE) raises ``UNSUPPORTED_OPERATION``.
  Snowflake doesn't expose a bare REPLACE form for ``VERSION_TAG``,
  and silently rewriting to ``CREATE OR REPLACE`` would change the
  failure-on-missing semantics that Iceberg's bare ``REPLACE TAG``
  guarantees.
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
* The bare ``CREATE TAG <name>`` form (no ``AS OF VERSION``) — which
  is Iceberg's canonical "tag the current head" idiom — raises
  ``UNSUPPORTED_OPERATION`` with an actionable message. We chose
  early-surface over pass-through because:

  - Snowflake's parser currently rejects ``CREATE VERSION_TAG <name>``
    with ``unexpected '<EOF>'`` (server probe 2026-06-12), so passing
    through silently produces an opaque SQL compilation error 200
    frames deep that's hard for customers to map back to a tag-DDL
    cause.
  - The restriction is Snowflake-server-side; SCOS SQL passthrough
    mode is **not** an escape hatch — the bare form fails the same
    way when sent verbatim.
  - Customers who want head-snapshot semantics today must resolve
    the head snapshot id explicitly via
    ``INFORMATION_SCHEMA.GET_TABLE_VERSIONS('<fqn>')`` (see
    ``tests/sas_tests/test_iceberg_snapshot_id_sample.py`` and
    ``tests/sas_tests/test_iceberg_version_tag_sample.py``) and pass
    it in as ``CREATE TAG <name> AS OF VERSION <id>``.

  If a future Snowflake release defaults the snapshot id to head, this
  branch can be relaxed to emit the bare form transparently — the
  unit tests pin the current behavior so the relaxation is a
  deliberate, reviewable change.
* ``RETAIN <N> DAYS`` raises ``UNSUPPORTED_OPERATION``: Snowflake's
  surface for tag retention is not documented as supported via the
  ``CREATE VERSION_TAG`` DDL today, and emitting a guessed spelling
  would risk silently dropping the retention bound.
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


@dataclass(frozen=True)
class CreateTagAsOfTimestampMatch:
    """Parsed ``ALTER TABLE … CREATE TAG … AS OF TIMESTAMP …`` SQL."""

    table_sql: str
    tag_name: str
    if_not_exists: bool
    create_or_replace: bool
    timestamp_sql: str


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
        exception = AnalysisException(
            f"Iceberg 'ALTER TABLE … REPLACE TAG {tag_name!r}' (without "
            "CREATE) is not translated by Snowpark Connect: Snowflake "
            "does not expose a bare REPLACE form for VERSION_TAG, and "
            "automatically lowering this to 'CREATE OR REPLACE' would "
            "change the semantics (Iceberg's bare REPLACE TAG fails if "
            "the tag is missing; CREATE OR REPLACE creates it). If "
            "create-or-update semantics are acceptable, rewrite the "
            "statement as 'CREATE OR REPLACE TAG'; otherwise use "
            "Snowflake-native DDL directly."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    exception = AnalysisException(
        "Internal: Iceberg CreateOrReplaceTag plan has neither "
        "'create' nor 'replace' flag set; this is a parser invariant "
        "violation, please report it."
    )
    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
    raise exception


def _build_create_version_tag_sql(
    *,
    table_name_sql: str,
    action: str,
    quoted_tag: str,
    as_of_clause: str,
) -> str:
    return (
        f"ALTER ICEBERG TABLE {table_name_sql} {action} {quoted_tag} " f"{as_of_clause}"
    )


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

    if snapshot_retain_opt.isDefined():
        # RETAIN <N> DAYS: Iceberg's tag retention policy. Snowflake's
        # surface for tag retention (if any) is not documented as
        # supported in the SCOS-aligned design. Same posture as the
        # ``AS OF VERSION`` branch.
        exception = AnalysisException(
            f"Iceberg 'ALTER TABLE … CREATE TAG {tag_name!r} RETAIN <N> "
            "DAYS' is not translated by Snowpark Connect: the "
            "Snowflake-side syntax for VERSION_TAG retention is not yet "
            "documented as supported. Configure tag retention directly "
            "through Snowflake."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

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
    else:
        # The bare ``CREATE TAG <name>`` form (no ``AS OF VERSION``) is
        # Iceberg's canonical "tag the current head" idiom. Snowflake's
        # parser currently *requires* a trailing ``AS OF VERSION <id>``
        # on ``CREATE VERSION_TAG`` (server probe 2026-06-12: any bare
        # form is rejected with ``unexpected '<EOF>'``), so passing the
        # translation through verbatim would surface as an opaque SQL
        # compilation error 200 frames deep that's hard to attribute
        # back to tag DDL. We surface a clear, actionable error here
        # instead.
        #
        # Importantly, this is a Snowflake-server-side restriction, not
        # a SCOS-side one — SCOS SQL passthrough mode
        # (``snowpark.connect.sql.passthrough=true``) has the same
        # behavior, so we explicitly tell the customer "passthrough
        # won't help" to head off the natural workaround attempt.
        exception = AnalysisException(
            f"Iceberg 'ALTER TABLE … CREATE TAG {tag_name!r}' (without "
            "'AS OF VERSION <id>' or 'AS OF TIMESTAMP <ts>') is not "
            "translated by Snowpark Connect: Snowflake's "
            "'CREATE VERSION_TAG' grammar requires an explicit "
            "'AS OF VERSION <snapshot_id>' or 'AS OF TIMESTAMP <ts>' "
            "clause today. This is a Snowflake-server restriction; SCOS "
            "SQL passthrough mode (snowpark.connect.sql.passthrough=true) "
            "does not lift it. To tag the current head snapshot, resolve "
            "the id first via "
            "'SELECT * FROM TABLE(<cld>.INFORMATION_SCHEMA."
            "GET_TABLE_VERSIONS(''<fqn>''))' and pass it explicitly: "
            f"'ALTER TABLE … CREATE TAG {tag_name!r} AS OF VERSION "
            "<snapshot_id>'."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    quoted_tag = quote_name_without_upper_casing(tag_name)
    return _build_create_version_tag_sql(
        table_name_sql=table_name_sql,
        action=action,
        quoted_tag=quoted_tag,
        as_of_clause=as_of_clause,
    )


def translate_drop_tag(rel: TypingAny, table_name_sql: str) -> str:
    """Translate ``ALTER TABLE … DROP TAG [IF EXISTS] <name>`` to Snowflake."""
    tag_name = str(rel.tag())
    if_exists = bool(rel.ifExists())

    action = "DROP VERSION_TAG"
    if if_exists:
        action += " IF EXISTS"
    quoted_tag = quote_name_without_upper_casing(tag_name)
    return f"ALTER ICEBERG TABLE {table_name_sql} {action} {quoted_tag}"
