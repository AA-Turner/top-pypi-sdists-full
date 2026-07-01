#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Resolve Iceberg SQL ``VERSION AS OF`` / ``TIMESTAMP AS OF`` time-travel
clauses from a parsed Spark logical plan into the option-key/value form
that ``map_read_table.py`` already knows how to route.

Spark 3.5's parser (and the Iceberg Spark SQL Extensions parser) produces
an ``org.apache.spark.sql.catalyst.plans.logical.RelationTimeTravel`` node
when the customer writes::

    SELECT * FROM <table> VERSION AS OF <id>
    SELECT * FROM <table> TIMESTAMP AS OF <expr>

The node carries:

* ``version`` — ``scala.Option[String]`` (parsed from the literal after
  ``VERSION AS OF``; the string form preserves arbitrary-precision ids).
* ``timestamp`` — ``scala.Option[Expression]`` (a foldable expression
  after ``TIMESTAMP AS OF``; typically a string literal but Spark also
  accepts ``Cast`` wrappers and numeric literals).

This module converts those into the canonical Iceberg DataFrame reader
option set already handled by ``map_read_table.get_table_from_name``:

* ``snapshot-id`` (int) — translated to Snowflake ``AT(VERSION => N)``
* ``as-of-timestamp`` (milliseconds since the Unix epoch, as a string)
  — translated to Snowflake ``AT(TIMESTAMP => TO_TIMESTAMP_TZ(...))``
* ``tag`` (string) — translated to Snowflake
  ``AT(VERSION_TAG => '<name>')``. Spark Iceberg overloads
  ``VERSION AS OF`` to accept *either* a numeric snapshot id *or* a
  string-quoted tag/branch name (see Iceberg's spark-queries docs
  "Time travel" section). The parser delivers both through the same
  ``Option[String]`` field on ``RelationTimeTravel``, so we distinguish
  them on the SCOS side via a simple lexical heuristic:

    * a value that parses as a signed 64-bit integer is treated as a
      snapshot id (mirrors ``VERSION AS OF 12345``);
    * anything else is treated as a tag name (mirrors
      ``VERSION AS OF 'historical-snapshot'``).

  This heuristic is ambiguous for tag names that happen to be all
  digits (e.g. ``'12345'``). Iceberg has the same ambiguity in its own
  ``VERSION AS OF`` surface, so we document the convention here rather
  than try to look up the catalog at parse time: customers with
  all-digit tag names should use the DataFrame option form,
  ``option("tag", "12345")``, where the intent is unambiguous.

  Branches are not yet supported on SCOS (the Snowflake server-side
  catalog surface for branches is in development); when it lands, the
  same code path will be extended to emit ``ON(BRANCH => '<name>')``
  and the SQL exit shape will just carry a fourth option key.

Keeping the SQL path's "exit shape" identical to the DataFrame option
path means there is exactly **one** code path that talks to Snowpark for
Iceberg time travel; the SQL surface is just a different front door to
the same translation.

Scope
-----
This module only covers the SQL **read** time-travel surface introduced
by the Iceberg Spark SQL Extensions. It is gated by the caller — when
``spark.sql.extensions`` does not include the Iceberg extension class,
the case in ``map_sql.py`` raises an UNSUPPORTED_OPERATION pointing to
``pip install 'snowpark-connect[iceberg]'`` and the helpers here are
never invoked.

Expressions in ``TIMESTAMP AS OF`` must be foldable (Spark's own rule)
**and** be reducible to a literal value at parse time without running
the full Catalyst Analyzer. We support:

* ``Literal(<string>, StringType)`` — the canonical
  ``TIMESTAMP AS OF '1986-10-26 01:21:00'`` form.
* ``Literal(<long-micros>, TimestampType)`` — Spark's internal repr.
* ``Literal(<numeric>, IntegerType/LongType)`` — interpreted as
  **milliseconds** since the Unix epoch, matching the Iceberg
  DataFrame ``as-of-timestamp`` reader-option contract.
* ``Cast(<string-typed child>, TimestampType, ...)`` — unwrapped
  recursively so common ``TIMESTAMP AS OF CAST('...' AS TIMESTAMP)``
  forms resolve cleanly. The Spark semantics of
  ``Cast(StringType, TimestampType)`` (parse the string as a wall-clock
  timestamp) match the bare-string branch above exactly, so unwrapping
  is a safe no-op for the string case.

We intentionally do **not** support ``Cast(<numeric-typed child>,
TimestampType, ...)`` (Felix's PR #4384 review). Spark's
``Cast(LongType, TimestampType)`` interprets the long as **seconds**
since epoch, while the bare-numeric branch interprets a long as
**milliseconds** since epoch (Iceberg DataFrame option contract).
Silently picking either by stripping the Cast would surprise customers
in opposite ways, so the cast form raises INVALID_INPUT and points at
the unambiguous spellings: a string literal, or a bare long expressing
millis-since-epoch directly. Same reasoning rejects ``Cast(...)`` over
``TimestampType`` children and any other non-string Cast inner.

More complex expressions (``CURRENT_TIMESTAMP() - INTERVAL 1 HOUR``,
arithmetic on subqueries, ...) are rejected with INVALID_INPUT — they
require a Catalyst Analyzer pass that SCOS doesn't run at this layer.
"""

from __future__ import annotations

import datetime
from typing import Any as TypingAny

from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

_INT64_MIN = -(2**63)
_INT64_MAX = 2**63 - 1


def resolve_relation_time_travel(
    rel: TypingAny,
) -> tuple[int | None, int | None, str | None]:
    """Extract ``(snapshot_id, as_of_timestamp_millis, version_tag)`` from
    a JVM ``RelationTimeTravel`` node.

    Exactly one of the three return values is non-``None``; the parser
    guarantees ``VERSION`` and ``TIMESTAMP`` are mutually exclusive, and
    ``version_tag`` is a strict refinement of the ``VERSION`` branch, so
    by construction (snapshot_id, version_tag) are also mutually
    exclusive. We re-check defensively so a future parser change can't
    silently produce zero or two of them.

    The numeric ``as_of_timestamp_millis`` is the Iceberg DataFrame
    option's canonical encoding (milliseconds since the Unix epoch);
    downstream ``_extract_iceberg_as_of_timestamp`` converts it back to
    a tz-aware UTC ``datetime`` before handing off to Snowpark. The
    ``version_tag`` is the raw Iceberg tag name; downstream callers
    feed it to Snowpark's ``read.option("version_tag", ...)`` which
    emits the ``AT(VERSION_TAG => '<name>')`` SQL clause.
    """
    version_opt = rel.version()
    timestamp_opt = rel.timestamp()
    has_version = bool(version_opt.isDefined())
    has_timestamp = bool(timestamp_opt.isDefined())

    if has_version == has_timestamp:
        exception = AnalysisException(
            "Iceberg SQL time travel must specify exactly one of "
            "'VERSION AS OF <id>' or 'TIMESTAMP AS OF <ts>'."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if has_version:
        snapshot_id, version_tag = _resolve_version(str(version_opt.get()))
        return snapshot_id, None, version_tag

    return None, _evaluate_timestamp_expression_to_millis(timestamp_opt.get()), None


def _resolve_version(raw: str) -> tuple[int | None, str | None]:
    """Parse a ``VERSION AS OF`` value into either an int64 snapshot id
    *or* a tag name.

    Spark's Iceberg SQL parser delivers both ``VERSION AS OF 12345`` and
    ``VERSION AS OF 'historical-snapshot'`` through the same
    ``Option[String]`` field, so disambiguation has to happen here. The
    rule mirrors Iceberg's own ``VERSION AS OF`` documentation:

    * Pure-integer string that fits in int64 -> snapshot id (matches
      ``VERSION AS OF <number>``).
    * Anything else -> tag name (matches ``VERSION AS OF '<name>'``).

    This has an irreducible ambiguity for all-digit tag names — see the
    module docstring. Customers who need an all-digit tag should use the
    DataFrame option form ``option("tag", "12345")``, which carries the
    intent explicitly.

    Returns a 2-tuple ``(snapshot_id, version_tag)`` with exactly one
    side set. Raises ``AnalysisException`` (INVALID_INPUT) on the only
    real failure mode left: an empty / whitespace-only value (which
    we'd otherwise dispatch as an empty tag name).
    """
    stripped = raw.strip()
    if not stripped:
        exception = AnalysisException(
            "'VERSION AS OF' value must be a non-empty snapshot id or tag "
            f"name; got {raw!r}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Heuristic: only treat the value as a snapshot id when it looks
    # *exactly* like a signed decimal integer. Anything else — including
    # leading/trailing whitespace inside the original literal, embedded
    # punctuation, or hex/scientific notation — is treated as a tag
    # name, so we never accidentally truncate a legitimate tag like
    # ``"v1.0.0"`` into the snapshot-id branch.
    try:
        snapshot_id = int(stripped)
    except (TypeError, ValueError):
        return None, stripped

    if not _INT64_MIN <= snapshot_id <= _INT64_MAX:
        # The string parses as an integer, but doesn't fit in INT64.
        # Iceberg snapshot ids are 64-bit signed, so this can't be a
        # snapshot id — but it's ambiguous whether the customer
        # *meant* a tag name that happens to look like a giant
        # integer, or a snapshot id they got wrong. Surface the
        # ambiguity rather than silently picking either side.
        exception = AnalysisException(
            "'VERSION AS OF' value parses as an integer outside the int64 "
            f"range (got {snapshot_id}). If you intended a snapshot id, "
            "Iceberg snapshot ids must fit in a 64-bit signed integer "
            f"(range [{_INT64_MIN}, {_INT64_MAX}]). If you intended a tag "
            'name that happens to be all digits, use option("tag", "<name>")'
            " on the DataFrame reader instead so the intent is unambiguous."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return snapshot_id, None


def _evaluate_timestamp_expression_to_millis(ts_expr: TypingAny) -> int:
    """Evaluate a foldable ``TIMESTAMP AS OF`` expression to milliseconds
    since the Unix epoch (Iceberg DataFrame option encoding).

    See the module docstring for the supported expression shapes —
    notably, ``Cast(...)`` is only unwrapped when the (eventual)
    inner child is a ``StringType`` literal, because that is the only
    case where Spark's ``Cast(<inner>, TimestampType)`` semantics
    coincide with the branch we'd take on the unwrapped child.
    """
    # Walk down a (possibly nested) ``Cast`` chain. We track whether
    # we crossed any cast so the post-walk type check can reject the
    # ``Cast(<non-string>, TimestampType, ...)`` shapes — those have
    # Spark cast semantics distinct from what we'd otherwise do with
    # the unwrapped child, and silently picking either flavor would
    # surprise the customer. Felix's PR #4384 review.
    crossed_cast = False
    while str(ts_expr.getClass().getSimpleName()) == "Cast":
        crossed_cast = True
        ts_expr = ts_expr.child()

    expr_class = str(ts_expr.getClass().getSimpleName())
    if expr_class != "Literal":
        exception = AnalysisException(
            f"'TIMESTAMP AS OF' supports only literal expressions; got {expr_class!r}. "
            "Use a string literal like '1986-10-26 01:21:00', a long "
            "(milliseconds since epoch), or a TIMESTAMP literal."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    value = ts_expr.value()
    type_name = str(ts_expr.dataType().typeName())

    if value is None:
        exception = AnalysisException("'TIMESTAMP AS OF' value must not be NULL.")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if type_name == "string":
        # ``Cast(StringType, TimestampType)`` Spark semantics (parse
        # the string as a wall-clock timestamp in the session zone)
        # match ``_parse_timestamp_string_to_millis`` exactly, so it
        # is safe to ignore the surrounding cast (if any) and parse
        # the inner string directly.
        return _parse_timestamp_string_to_millis(str(value))

    if crossed_cast:
        # Reject ``Cast(<non-string>, TimestampType, ...)``. Concretely
        # this is the ``TIMESTAMP AS OF CAST(1700000000 AS TIMESTAMP)``
        # shape, where Spark's cast semantics interpret the long as
        # SECONDS since epoch — disagreeing with the bare-numeric
        # branch below (which is MILLISECONDS since epoch, per the
        # Iceberg DataFrame ``as-of-timestamp`` reader-option contract).
        # Faithfully implementing Spark cast semantics here would mean
        # silently flipping the unit interpretation based on a Cast
        # wrapper that the customer may not have noticed; instead, we
        # surface the ambiguity and point at the two unambiguous forms.
        exception = AnalysisException(
            "'TIMESTAMP AS OF CAST(<expr> AS TIMESTAMP)' with a "
            f"non-string child (got child type {type_name!r}) is not "
            "supported because Spark's cast semantics differ from the "
            "bare-literal interpretation Snowpark Connect uses. Use a "
            "string literal — TIMESTAMP AS OF 'YYYY-MM-DD HH:MM:SS' — "
            "or a bare long expressing milliseconds since the Unix "
            "epoch — TIMESTAMP AS OF <millis>."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if type_name == "timestamp":
        # Bare ``TimestampType`` literal: Spark's internal repr is
        # microseconds since the Unix epoch. Convert to milliseconds
        # for the option wire format; integer division here is safe
        # (any sub-millisecond precision is already below Iceberg's
        # snapshot resolution).
        return int(value) // 1000

    if type_name in ("integer", "long"):
        # Bare numeric literal: matches the Iceberg DataFrame
        # ``as-of-timestamp`` reader-option contract — milliseconds
        # since the Unix epoch. Out-of-range values are rejected
        # upstream when the option is re-parsed
        # (``_extract_iceberg_as_of_timestamp``).
        return int(value)

    exception = AnalysisException(
        "'TIMESTAMP AS OF' literal must be of type string, timestamp, integer, "
        f"or long; got {type_name!r}."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
    raise exception


def _parse_timestamp_string_to_millis(ts_str: str) -> int:
    """Parse a Spark-style timestamp literal to milliseconds since the
    Unix epoch (UTC).

    Accepted formats (matching the most common Spark Cast(string,
    TimestampType) inputs at the SQL surface):

    * ``YYYY-MM-DD HH:MM:SS[.fffffff]``
    * ``YYYY-MM-DD'T'HH:MM:SS[.fffffff][Z|±HH:MM]``
    * ``YYYY-MM-DD HH:MM``
    * ``YYYY-MM-DD``

    Strings without an explicit timezone are interpreted in
    ``spark.sql.session.timeZone`` (defaulting to UTC when unset), which
    matches Spark's Cast(string, TimestampType) semantics. Strings with
    an explicit offset / ``Z`` keep their offset.
    """
    cleaned = ts_str.strip()

    # ISO 8601 with an explicit offset / ``Z`` is unambiguous; let the
    # stdlib do the work. ``fromisoformat`` accepts the space and ``T``
    # separators in 3.11+; for 3.10 we normalize ``T`` to a space below
    # and only enter this branch when ``cleaned`` carries an explicit
    # offset (which fromisoformat does parse on 3.10).
    has_offset = (
        cleaned.endswith("Z")
        or "+" in cleaned[10:]  # offset never appears in the date part
        or (cleaned.count("-") > 2)  # YYYY-MM-DDTHH:MM:SS-HH:MM
    )
    if has_offset:
        try:
            iso_value = cleaned[:-1] + "+00:00" if cleaned.endswith("Z") else cleaned
            dt_aware = datetime.datetime.fromisoformat(iso_value)
            return _dt_to_utc_millis(dt_aware)
        except ValueError:
            pass

    # Pre-normalize the ``T`` separator so a single set of patterns
    # covers both ``YYYY-MM-DD HH:MM:SS`` and ``YYYY-MM-DDTHH:MM:SS``
    # without relying on the 3.11+ fromisoformat relaxations.
    normalized = cleaned.replace("T", " ", 1)
    parsed: datetime.datetime | None = None
    for fmt in (
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            parsed = datetime.datetime.strptime(normalized, fmt)
            break
        except ValueError:
            continue

    if parsed is None:
        exception = AnalysisException(
            f"'TIMESTAMP AS OF' could not parse timestamp literal {ts_str!r}. "
            "Expected formats: 'YYYY-MM-DD HH:MM:SS[.fff]', 'YYYY-MM-DD', or "
            "ISO 8601 with an explicit offset."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    return _dt_to_utc_millis(_localize_session(parsed))


def _localize_session(dt: datetime.datetime) -> datetime.datetime:
    """Attach the session timezone to a naive datetime, mirroring how
    Spark's Cast(string, TimestampType) interprets timezone-less inputs.
    """
    session_tz_id = global_config.spark_sql_session_timeZone or "UTC"
    try:
        from zoneinfo import ZoneInfo

        session_tz: datetime.tzinfo = ZoneInfo(session_tz_id)
    except Exception:
        # ZoneInfo may fail in stripped runtimes that lack tzdata; fall
        # back to UTC to keep parsing deterministic rather than crash.
        session_tz = datetime.timezone.utc
    return dt.replace(tzinfo=session_tz)


def _dt_to_utc_millis(dt: datetime.datetime) -> int:
    """Convert a tz-aware datetime to integer milliseconds since the
    Unix epoch in UTC.

    Uses ``timedelta``-based integer arithmetic rather than
    ``timestamp() * 1000`` to avoid the float-precision drift that can
    surface near the millisecond boundary for far-future / far-past
    timestamps.
    """
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = dt.astimezone(datetime.timezone.utc) - epoch
    # ``total_seconds()`` returns a float; recompose from integer
    # microseconds for full precision.
    micros = (
        delta.days * 86_400_000_000 + delta.seconds * 1_000_000 + delta.microseconds
    )
    return micros // 1000
