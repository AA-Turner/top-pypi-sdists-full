#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
import re
from typing import Any, TypeVar

from pyspark.errors import AnalysisException

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark_connect.config import (
    auto_uppercase_column_identifiers,
    auto_uppercase_non_column_identifiers,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

QUOTED_SPARK_IDENTIFIER = re.compile(r"^`[^`]*(?:``[^`]*)*`$")
UNQUOTED_SPARK_IDENTIFIER = re.compile(r"^\w+$")


def unquote_spark_identifier_if_quoted(spark_name: str) -> str:
    if UNQUOTED_SPARK_IDENTIFIER.match(spark_name):
        return spark_name

    if QUOTED_SPARK_IDENTIFIER.match(spark_name):
        return spark_name[1:-1].replace("``", "`")

    exception = AnalysisException(f"Invalid name: {spark_name}")
    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
    raise exception


def spark_to_sf_single_id_with_unquoting(
    name: str, use_auto_upper_case: bool = False
) -> str:
    """
    Transforms a spark name to a valid snowflake name by quoting and potentially uppercasing it.
    Unquotes the spark name if necessary. Will raise an AnalysisException if given name is not valid.
    """
    return (
        spark_to_sf_single_id(unquote_spark_identifier_if_quoted(name))
        if use_auto_upper_case
        else quote_name_without_upper_casing(unquote_spark_identifier_if_quoted(name))
    )


def spark_to_sf_single_id(name: str, is_column: bool = False) -> str:
    """
    Transforms a spark name to a valid snowflake name by quoting and potentially uppercasing it.
    Assumes that the given spark name doesn't contain quotes,
    meaning it's either already unquoted, or didn't need quoting.
    """
    name = quote_name_without_upper_casing(name)
    should_uppercase = (
        auto_uppercase_column_identifiers()
        if is_column
        else auto_uppercase_non_column_identifiers()
    )
    return name.upper() if should_uppercase else name


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


# See https://docs.snowflake.com/en/sql-reference/identifiers-syntax for identifier syntax
UNQUOTED_IDENTIFIER_REGEX = r"([a-zA-Z_])([a-zA-Z0-9_$]{0,254})"
QUOTED_IDENTIFIER_REGEX = r'"((""|[^"]){0,255})"'
VALID_IDENTIFIER_REGEX = f"(?:{UNQUOTED_IDENTIFIER_REGEX}|{QUOTED_IDENTIFIER_REGEX})"


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
