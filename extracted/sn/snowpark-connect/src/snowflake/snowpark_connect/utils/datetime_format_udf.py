#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""java.time-based datetime formatting/parsing UDF fallbacks (SNOW-3585737).

When a Spark datetime format pattern contains tokens that Snowflake's
``TO_CHAR`` / ``TO_TIMESTAMP`` cannot faithfully reproduce (era ``G``, quarter
``q``/``Q``, day-of-year ``D``, day-of-week-in-month ``F``, hour-of-am-pm
``K``, timezone identity ``VV``/``z``/``O`` ...), the whole pattern is routed
through these UDFs which delegate to ``java.time.format.DateTimeFormatter`` and
therefore match Spark 3.5 exactly.

The handlers live in the ``java_udfs`` subproject
(``com.snowflake.snowpark_connect.udfs.DatetimeFormatUdfs``) and are registered
as native Java UDFs via :func:`register_cached_java_udf` -- this avoids JPype and
the cost of starting an in-process JVM on the Snowflake Python sandbox.

The Spark engine substitutes ``y`` (year-of-era) with ``u`` (proleptic year)
when the pattern contains no era designator, to keep support for negative
years (see ``DateTimeFormatterHelper.convertIncompatiblePattern``). We replicate
that substitution at plan time via :func:`substitute_proleptic_year` so the pattern
handed to ``DateTimeFormatter.ofPattern`` behaves like Spark's.
"""

from __future__ import annotations

from collections.abc import Callable

from snowflake.snowpark import Column
from snowflake.snowpark_connect.date_time_format_mapping import (
    _iter_spark_pattern_fields,
)
from snowflake.snowpark_connect.utils.udf_cache import register_cached_java_udf

_DATE_FORMAT_DATE_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.DatetimeFormatUdfs.format_date"
)
_DATE_FORMAT_NTZ_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.DatetimeFormatUdfs.format_timestamp_ntz"
)
_DATE_FORMAT_LTZ_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.DatetimeFormatUdfs.format_timestamp_ltz"
)
_DATETIME_PARSE_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.DatetimeFormatUdfs.parse_datetime"
)


def substitute_proleptic_year(spark_format: str) -> str:
    """Replicate Spark's ``y`` -> ``u`` substitution outside of quoted literals
    when the pattern contains no era (``G``) designator.

    This does *not* fully parse Spark patterns; it only rewrites the year token.
    The single-quote scan below preserves each character's inside/outside-literal
    classification (which is all the ``y`` -> ``u`` decision needs) but not the
    literal *segment structure*: a mid-literal ``''`` escape (e.g. ``'it''s'``) is
    internally read as two adjacent literals rather than one. That is harmless
    here because ``''`` is two adjacent quotes with no character between them, so
    no literal char is ever misclassified as outside a literal. Do not reuse this
    scan for a transformation that depends on literal boundaries.
    """
    has_era = any(
        letter == "G" for letter, _, _ in _iter_spark_pattern_fields(spark_format)
    )
    if has_era:
        return spark_format

    result: list[str] = []
    i = 0
    n = len(spark_format)
    while i < n:
        ch = spark_format[i]
        if ch == "'":
            # Copy the quoted literal block verbatim.
            result.append(ch)
            i += 1
            if i <= n and spark_format[i - 1 : i + 1] == "''":
                result.append("'")
                i += 1
                continue
            while i < n:
                result.append(spark_format[i])
                if spark_format[i] == "'":
                    i += 1
                    break
                i += 1
            continue
        result.append("u" if ch == "y" else ch)
        i += 1
    return "".join(result)


def get_java_format_timestamp_ntz_udf() -> Callable[..., Column]:
    """Register (and cache) the Java UDF that formats a TIMESTAMP_NTZ column directly.

    Accepts the column as ``TIMESTAMP_NTZ`` (``java.sql.Timestamp``); no ``TO_CHAR``
    call is needed on the SQL side.  UDF signature: ``(ts, java_pattern) -> str``.
    """
    return register_cached_java_udf(
        _DATE_FORMAT_NTZ_HANDLER,
        ["TIMESTAMP_NTZ", "STRING"],
        "STRING",
    )


def get_java_format_timestamp_ltz_udf() -> Callable[..., Column]:
    """Register (and cache) the Java UDF that formats a TIMESTAMP_LTZ column directly.

    Accepts the column as ``TIMESTAMP_LTZ`` (``java.sql.Timestamp``); no ``TO_CHAR``
    call is needed on the SQL side.  UDF signature: ``(ts, java_pattern) -> str``.

    A TIMESTAMP_TZ column reuses this same UDF: the caller casts it to
    ``TIMESTAMP_LTZ`` first (the cast preserves the exact instant and only drops
    the per-row display offset), which is all this handler needs.
    """
    return register_cached_java_udf(
        _DATE_FORMAT_LTZ_HANDLER,
        ["TIMESTAMP_LTZ", "STRING"],
        "STRING",
    )


def get_java_format_date_udf() -> Callable[..., Column]:
    """Register (and cache) the Java UDF that formats a DATE column directly.

    Accepts the column as ``DATE`` (``java.sql.Date``); no ``TO_CHAR`` call is
    needed on the SQL side.  UDF signature: ``(d, java_pattern) -> str``.
    """
    return register_cached_java_udf(
        _DATE_FORMAT_DATE_HANDLER,
        ["DATE", "STRING"],
        "STRING",
    )


def get_java_parse_datetime_udf() -> Callable[..., Column]:
    """Register (and cache) the native Java UDF that parses a string into a
    canonical ``yyyy-MM-dd HH:mm:ss.SSSSSS`` wall-clock string using a java.time
    pattern.

    UDF signature: ``(value_str, java_pattern, ansi_enabled, target_kind) -> str``.
    ``target_kind`` controls zone handling: ``"timestamp_ntz"`` keeps parsed
    wall-clock fields and discards the zone; anything else normalizes to the session
    timezone via ``withZoneSameInstant``.  Returns NULL on parse failure when
    ``ansi_enabled`` is false; throws a marker-prefixed exception when true so the
    caller can re-raise ``CANNOT_PARSE_TIMESTAMP``.
    """
    return register_cached_java_udf(
        _DATETIME_PARSE_HANDLER,
        ["STRING", "STRING", "BOOLEAN", "STRING"],
        "STRING",
    )
