#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""The configuration contract for calling a native Snowflake function from Spark.

A user makes an arbitrary Snowflake built-in, or a UDF created outside the Spark session
(from SnowSight, SnowSQL, or any other client), callable from Spark by declaring it in the
session configuration::

    spark.conf.set("snowpark.connect.nativeFunction.jaro_winkler",
                   "MY_DB.MY_SCHEMA.JW_SIM:double")

Configuration is the transport because it is the only registration surface that behaves
identically across every Spark Connect client. ``spark.udf.*`` is not: the JVM client has no
``registerJava`` at all and emits ``scalar_scala_udf`` (a Java-serialised payload) for every
registration, while PySpark emits ``python_udf`` (cloudpickle) or ``java_udf`` (a class
name). Smuggling the target through a UDF body therefore needs a different byte-level
scheme per language, whereas ``RuntimeConfig.set``/``unset`` and
``functions.call_function`` exist in all of them.

One key per function, so removal is ``conf.unset`` and an override is a plain re-``set``.
The key suffix is the name to call the function by *from Spark*; it may contain dots, which
is how a caller opts into invoking the function by its qualified Snowflake spelling.

This module imports nothing beyond ``re`` so that it can be used by client-side code
without pulling in the server, and so both sides share one definition of what a valid
target looks like.
"""

import re

#: Conf keys are ``<prefix><spark function name>``.
CONF_PREFIX = "snowpark.connect.nativeFunction."

#: Upper bound on a target. Snowflake identifiers cap well below this; the limit keeps a
#: pathological conf value from reaching the SQL generator.
MAX_TARGET_LENGTH = 255

# A Snowflake identifier part: unquoted (case-folded to upper by Snowflake) or
# double-quoted (case-sensitive, may contain almost anything but a quote).
_PART = r'(?:[A-Za-z_][A-Za-z0-9_$]*|"[^"]+")'
# Bare name, SCHEMA.NAME, or DATABASE.SCHEMA.NAME.
_TARGET_RE = re.compile(rf"^{_PART}(?:\.{_PART}){{0,2}}$")
_PART_RE = re.compile(_PART)


def validate_native_target(target: str) -> None:
    """Raise ``ValueError`` unless ``target`` is a safe 1-, 2-, or 3-part identifier.

    This is the security boundary, not a convenience check. The target is interpolated
    verbatim into generated SQL: Snowpark's ``FunctionExpression.sql`` renders a function
    name with no quoting or escaping, so anything accepted here reaches the warehouse as
    written.
    """
    if not isinstance(target, str):
        raise ValueError(
            f"Native function target must be a string, got {type(target).__name__}."
        )
    if not target:
        raise ValueError("Native function target must not be empty.")
    if len(target) > MAX_TARGET_LENGTH:
        raise ValueError(
            f"Native function target exceeds {MAX_TARGET_LENGTH} characters: "
            f"{target[:60]!r}..."
        )
    if not _TARGET_RE.match(target):
        raise ValueError(
            f"Invalid native function target {target!r}. Expected a Snowflake function "
            "name as NAME, SCHEMA.NAME, or DATABASE.SCHEMA.NAME, where each part is an "
            'unquoted identifier or a double-quoted one (e.g. "myDb"."mySchema"."myFn").'
        )


def split_target(target: str) -> list[str]:
    """Split a validated target into its identifier parts, quoting retained.

    ``'MY_DB.MY_SCHEMA.FN'`` -> ``['MY_DB', 'MY_SCHEMA', 'FN']``
    ``'"a"."b"."c"'``        -> ``['"a"', '"b"', '"c"']``

    Prefer this over testing for ``"." in target``: a quoted part may itself contain a dot
    (``'"my.fn"'`` is a *single* part), so the naive test misreads such a target as
    qualified.
    """
    return _PART_RE.findall(target)


def parse_conf_value(value: str) -> tuple[str, str | None]:
    """Split a conf value into ``(target, spark_type_string_or_None)``.

    The separator is the first ``:`` **outside** double quotes. Both ends need that rule:
    a quoted identifier may contain a colon (``'"my:fn":double'``), and a Spark type string
    may too (``'FN:struct<a:int>'``), so neither "split on first" nor "split on last" is
    correct on its own.

    The target is validated here; the type string is not (its parser owns that, and it is
    optional in the grammar so that return-type inference can be added later without
    changing the meaning of a value that used to be rejected).
    """
    if not isinstance(value, str):
        raise ValueError(
            f"Native function configuration value must be a string, got "
            f"{type(value).__name__}."
        )
    stripped = value.strip()
    if not stripped:
        raise ValueError("Native function configuration value must not be empty.")

    in_quotes = False
    separator = -1
    for index, char in enumerate(stripped):
        if char == '"':
            in_quotes = not in_quotes
        elif char == ":" and not in_quotes:
            separator = index
            break

    if separator == -1:
        target, type_string = stripped, None
    else:
        target = stripped[:separator].strip()
        type_string = stripped[separator + 1 :].strip() or None

    validate_native_target(target)
    return target, type_string


def conf_key_for(name: str) -> str:
    """The conf key that registers ``name`` as a native function alias."""
    return f"{CONF_PREFIX}{name}"
