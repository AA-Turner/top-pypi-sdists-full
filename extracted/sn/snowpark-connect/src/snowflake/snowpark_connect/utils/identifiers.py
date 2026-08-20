#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import re
from typing import Any, TypeVar

from pyspark.errors import AnalysisException

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.cld_context import (
    CLDInfo,
    get_cld_info,
    get_current_cld_context,
    get_multipart_backtick_flags,
    is_cld_unified_identifier_rules_enabled,
    is_double_quoted,
    is_in_cld_context,
    record_multipart_backtick_flags,
    set_current_cld_context,
    should_use_cld_identifier_rules,
    transform_identifier_for_snowflake,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# Re-export CLD utilities for convenience
__all__ = [
    "CLDInfo",
    "get_cld_info",
    "get_current_cld_context",
    "get_multipart_backtick_flags",
    "is_double_quoted",
    "is_cld_unified_identifier_rules_enabled",
    "is_in_cld_context",
    "record_multipart_backtick_flags",
    "set_current_cld_context",
    "should_use_cld_identifier_rules",
    "transform_identifier_for_snowflake",
    "is_backtick_quoted",
    "strip_backtick_quotes_if_quoted",
    "unquote_spark_identifier_if_quoted",
    "spark_to_sf_single_id",
    "spark_to_sf_single_id_with_unquoting",
    "spark_multipart_name_to_snowflake",
    "split_fully_qualified_spark_name",
    "split_fully_qualified_spark_name_with_quoting",
    "FQN",
]

QUOTED_SPARK_IDENTIFIER = re.compile(r"^`[^`]*(?:``[^`]*)*`$")
UNQUOTED_SPARK_IDENTIFIER = re.compile(r"^\w+$")


def is_backtick_quoted(name: str) -> bool:
    """Check if an identifier is wrapped in backticks."""
    return QUOTED_SPARK_IDENTIFIER.match(name) is not None


def unquote_spark_identifier_if_quoted(spark_name: str) -> str:
    """Strip surrounding backticks from a Spark identifier (if any).

    Pure function — does not mutate any request-level state. Callers that
    need to know whether the input was originally backtick-quoted should
    detect that themselves (e.g. via `is_backtick_quoted(spark_name)`)
    before calling and thread the result explicitly to
    `transform_identifier_for_snowflake` / `spark_to_sf_single_id`.

    Removed the prior side effect of marking the unquoted name in a
    request-global set (see Felix's PR #4052 review on cld_context.py:113):
    that side channel caused cross-contamination between identifiers
    sharing a leaf name (e.g. a backtick-quoted column `foo` would change
    rendering of an unquoted table `foo` later in the same request).
    """
    if UNQUOTED_SPARK_IDENTIFIER.match(spark_name):
        return spark_name

    if QUOTED_SPARK_IDENTIFIER.match(spark_name):
        unquoted = spark_name[1:-1].replace("``", "`")
        logger.debug(
            "Backtick-quoted identifier detected: original=%r -> unquoted=%r",
            spark_name,
            unquoted,
        )
        return unquoted

    exception = AnalysisException(f"Invalid name: {spark_name}")
    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
    raise exception


def strip_backtick_quotes_if_quoted(name: str) -> str:
    """Strip surrounding backticks from a raw Spark column-name string if present.

    Unlike :func:`unquote_spark_identifier_if_quoted`, this is lenient: names
    that are neither valid unquoted identifiers nor properly backtick-quoted
    (e.g. ``Watt-hr``) are returned unchanged instead of raising. This matches
    how Spark's stat/na DataFrame APIs (approxQuantile, corr, cov, describe,
    freqItems, crosstab, dropna, replace) parse their raw string column
    arguments: a backtick-quoted name is unquoted, everything else is taken
    verbatim.
    """
    if is_backtick_quoted(name):
        return name[1:-1].replace("``", "`")
    return name


def spark_to_sf_single_id_with_unquoting(
    name: str, use_auto_upper_case: bool = False
) -> str:
    """
    Transforms a spark name to a valid snowflake name by quoting and potentially uppercasing it.
    Unquotes the spark name if necessary. Will raise an AnalysisException if given name is not valid.

    Detects the backtick-quoted status at this call site (no request-global
    side channel) and threads the flag through to the downstream identifier
    transformer.
    """
    was_backticked = is_backtick_quoted(name)
    unquoted = unquote_spark_identifier_if_quoted(name)
    if use_auto_upper_case:
        return spark_to_sf_single_id(unquoted, is_backtick_quoted=was_backticked)
    return quote_name_without_upper_casing(unquoted)


def spark_to_sf_single_id(
    name: str,
    is_backtick_quoted: bool | None = None,
    is_cld: bool | None = None,
    is_column: bool = False,
) -> str:
    """
    Transforms a spark name to a valid snowflake name by quoting and potentially uppercasing it.
    Assumes that the given spark name doesn't contain quotes,
    meaning it's either already unquoted, or didn't need quoting.

    For CLD (Catalog-Linked Databases), follows special rules:
    - Default: no double quotes unless backtick-quoted or caseSensitive=True
    - Uppercase unless caseSensitive=True

    For non-CLD (standard Snowflake):
    - Default: always double quotes
    - Uppercase unless caseSensitive=True

    Args:
        name: The identifier name
        is_backtick_quoted: True if originally backtick-quoted in Spark.
                           If None, checks the request context.
        is_cld: True if this is for a CLD context.
                If None, uses the current request context.
        is_column: True if the identifier is a column name. Currently routed
                   through `transform_identifier_for_snowflake` unchanged;
                   reserved for column-specific transformation rules.
    """
    return transform_identifier_for_snowflake(
        name=name,
        is_backtick_quoted=is_backtick_quoted,
        is_cld=is_cld,
        is_column=is_column,
    )


def spark_multipart_name_to_snowflake(
    qualified_name: str,
    is_cld: bool | None = None,
) -> str:
    """Transform a dot-separated Spark table identifier string to Snowflake SQL.

    Parses per-part backtick flags from ``qualified_name`` itself (same approach
    as ``map_read_table.get_table_from_name``) so DataFrame write paths honor
    customer backtick quoting without relying on the SQL AST backtick map.
    """
    parts, backtick_flags = split_fully_qualified_spark_name_with_quoting(
        qualified_name
    )
    return ".".join(
        spark_to_sf_single_id(part, is_backtick_quoted=flag, is_cld=is_cld)
        for part, flag in zip(parts, backtick_flags)
    )


def split_fully_qualified_spark_name(qualified_name: str | None) -> list[str]:
    """
    Splits a fully qualified Spark identifier into its component parts.

    A dot (.) is used as a delimiter only when occurring outside a quoted segment.
    A quoted segment is wrapped in single backticks. Inside a quoted segment,
    any occurrence of two consecutive backticks is treated as a literal backtick.
    After splitting, any token that was quoted is unescaped:
      - The external backticks are removed.
      - Any double backticks are replaced with a single backtick.

    Examples:
      "a.b.c"
         -> ["a", "b", "c"]

      "`a.somethinh.b`.b.c"
         -> ["a.somethinh.b", "b", "c"]

      "`a$b`.`b#c`.d.e.f.g.h.as"
         -> ["a$b", "b#c", "d", "e", "f", "g", "h", "as"]

      "`a.b.c`"
         -> ["a.b.c"]

      "`a``b``c.d.e`"
         -> ["a`b`c", "d", "e"]

      "asdfasd" -> ["asdfasd"]
    """
    if qualified_name in ("``", "", None):
        # corner case where empty string is denoted by an empty string. We cannot have emtpy string
        # in fully qualified name.
        return [""]
    assert isinstance(qualified_name, str), qualified_name

    parts = []
    token_chars = []
    in_quotes = False
    i = 0
    n = len(qualified_name)

    while i < n:
        ch = qualified_name[i]
        if ch == "`":
            # If current char is a backtick:
            if i + 1 < n and qualified_name[i + 1] == "`":
                # If next char is also a backtick, unescape the backtick character by replacing `` with `.
                token_chars.append("`")
                i += 2
                continue
            else:
                # Toggle the in_quotes state and skip backtick in the token.
                in_quotes = not in_quotes
                i += 1
        elif ch == "." and not in_quotes:
            # Dot encountered outside of quotes: finish the current token.
            parts.append("".join(token_chars))
            token_chars = []
            i += 1
        else:
            token_chars.append(ch)
            i += 1

    if token_chars:
        parts.append("".join(token_chars))

    return parts


def split_fully_qualified_spark_name_with_quoting(
    qualified_name: str | None,
) -> tuple[list[str], list[bool]]:
    """Same shape as `split_fully_qualified_spark_name`, but also returns
    per-part backtick-quoted flags derived directly from the input string.

    Returns `(parts, was_backtick_quoted)` where `parts[i]` is the unquoted
    form and `was_backtick_quoted[i]` is True iff that part appeared inside
    backticks in `qualified_name`. The flags travel with the parts list so
    callers can pass them positionally to `transform_identifier_for_snowflake`,
    avoiding the name-only request-global tracking that was prone to
    cross-contamination.
    """
    if qualified_name in ("``", "", None):
        return [""], [False]
    assert isinstance(qualified_name, str), qualified_name

    parts: list[str] = []
    flags: list[bool] = []
    token_chars: list[str] = []
    in_quotes = False
    current_quoted = False
    i = 0
    n = len(qualified_name)

    while i < n:
        ch = qualified_name[i]
        if ch == "`":
            if i + 1 < n and qualified_name[i + 1] == "`":
                token_chars.append("`")
                i += 2
                continue
            if not in_quotes:
                current_quoted = True
            in_quotes = not in_quotes
            i += 1
        elif ch == "." and not in_quotes:
            parts.append("".join(token_chars))
            flags.append(current_quoted)
            token_chars = []
            current_quoted = False
            i += 1
        else:
            token_chars.append(ch)
            i += 1

    if token_chars or current_quoted:
        parts.append("".join(token_chars))
        flags.append(current_quoted)

    return parts, flags


# See https://docs.snowflake.com/en/sql-reference/identifiers-syntax for identifier syntax
UNQUOTED_IDENTIFIER_REGEX = r"([a-zA-Z_])([a-zA-Z0-9_$]{0,254})"
QUOTED_IDENTIFIER_REGEX = r'"((""|[^"]){0,255})"'
VALID_IDENTIFIER_REGEX = f"(?:{UNQUOTED_IDENTIFIER_REGEX}|{QUOTED_IDENTIFIER_REGEX})"
_VALID_UNQUOTED_SNOWFLAKE_IDENTIFIER = re.compile(rf"\A{UNQUOTED_IDENTIFIER_REGEX}\Z")


def is_valid_unquoted_snowflake_identifier(name: str) -> bool:
    """True when ``name`` can appear unquoted in Snowflake SQL."""
    return bool(_VALID_UNQUOTED_SNOWFLAKE_IDENTIFIER.match(name))


def cld_identifier_needs_snowflake_quotes(
    bare_name: str,
    *,
    is_backtick_quoted: bool = False,
    spark_case_sensitive: bool = False,
) -> bool:
    """Whether a bare Spark name needs Snowflake double-quotes under CLD rules.

    Quoting is driven by Snowflake identifier validity and
    ``spark.sql.caseSensitive``, with a backtick supplement: Spark backticks are
    not a case-sensitivity signal, but a backtick-quoted name that is not a
    simple ``\\w+`` identifier may wrap characters that must be quoted in
    Snowflake (e.g. dots, spaces). Simple backtick names like `` `foo` `` do
    not force quotes.
    """
    if spark_case_sensitive:
        return True
    if not is_valid_unquoted_snowflake_identifier(bare_name):
        return True
    if is_backtick_quoted and not UNQUOTED_SPARK_IDENTIFIER.match(bare_name):
        return True
    return False


Self = TypeVar("Self", bound="FQN")


class FQN:
    """Represents an object identifier, supporting fully qualified names.

    The instance supports builder pattern that allows updating the identifier with database and
    schema from different sources.

    Examples
    ________
    >>> fqn = FQN.from_string("my_schema.object").using_connection(conn)

    >>> fqn = FQN.from_string("my_name").set_database("db").set_schema("foo")
    """

    def __init__(
        self,
        database: str | None,
        schema: str | None,
        name: str,
        signature: str | None = None,
    ) -> None:
        self._database = database
        self._schema = schema
        self._name = name
        self.signature = signature

    @property
    def database(self) -> str | None:
        return self._database

    @property
    def schema(self) -> str | None:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @property
    def prefix(self) -> str:
        if self.database:
            return f"{self.database}.{self.schema if self.schema else 'PUBLIC'}"
        if self.schema:
            return f"{self.schema}"
        return ""

    @property
    def identifier(self) -> str:
        if self.prefix:
            return f"{self.prefix}.{self.name}"
        return self.name

    def __str__(self) -> str:
        return self.identifier

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FQN):
            exception = AnalysisException(f"{other} is not a valid FQN")
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception
        return self.identifier == other.identifier

    @classmethod
    def from_string(cls, identifier: str) -> Self:
        """Take in an object name in the form [[database.]schema.]name and return a new :class:`FQN` instance.

        Raises:
            InvalidIdentifierError: If the object identifier does not meet identifier requirements.
        """
        qualifier_pattern = (
            rf"(?:(?P<first_qualifier>{VALID_IDENTIFIER_REGEX})\.)?"
            rf"(?:(?P<second_qualifier>{VALID_IDENTIFIER_REGEX})\.)?"
            rf"(?P<name>{VALID_IDENTIFIER_REGEX})(?P<signature>\(.*\))?"
        )
        result = re.fullmatch(qualifier_pattern, identifier)

        if result is None:
            exception = AnalysisException(f"{identifier} is not a valid identifier")
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception

        unqualified_name = result.group("name")
        if result.group("second_qualifier") is not None:
            database = result.group("first_qualifier")
            schema = result.group("second_qualifier")
        else:
            database = None
            schema = result.group("first_qualifier")

        signature = None
        if result.group("signature"):
            signature = result.group("signature")
        return cls(
            name=unqualified_name, schema=schema, database=database, signature=signature
        )

    def set_database(self, database: str | None) -> Self:
        if database:
            self._database = database
        return self

    def set_schema(self, schema: str | None) -> Self:
        if schema:
            self._schema = schema
        return self

    def set_name(self, name: str) -> Self:
        self._name = name
        return self

    def to_dict(self) -> dict[str, str | None]:
        """Return the dictionary representation of the instance."""
        return {"name": self.name, "schema": self.schema, "database": self.database}
