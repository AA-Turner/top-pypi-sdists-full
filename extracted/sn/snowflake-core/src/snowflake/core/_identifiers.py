from __future__ import annotations

import re
import warnings

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, NewType, TypeAlias, TypeGuard

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from snowflake.core.exceptions import InvalidIdentifierError

from ._internal.utils import DOUBLE_QUOTE, SNOWFLAKE_QUOTED_ID_RE, is_valid_identifier, quote_name, unquote_name


if TYPE_CHECKING:
    from snowflake.connector import SnowflakeConnection


# See https://docs.snowflake.com/en/sql-reference/identifiers-syntax for identifier syntax
UNQUOTED_IDENTIFIER_REGEX = r"([a-zA-Z_])([a-zA-Z0-9_$]{0,254})"
QUOTED_IDENTIFIER_REGEX = r'"((""|[^"]){0,255})"'
VALID_IDENTIFIER_REGEX = f"(?:{UNQUOTED_IDENTIFIER_REGEX}|{QUOTED_IDENTIFIER_REGEX})"


class FQN:
    """Represents an object identifier, supporting fully qualified names.

    The instance supports builder pattern that allows updating the identifier with database and
    schema from different sources.

    .. deprecated:: 1.14.0
        ``FQN`` is deprecated and will be removed in a future release.
        Please use :class:`snowflake.core.QualifiedIdentifier` instead.

    Examples
    ________
    >>> fqn = FQN.from_string("my_schema.object").using_connection(conn)

    >>> fqn = FQN.from_string("my_name").set_database("db").set_schema("foo")
    """

    def __init__(self, database: str | None, schema: str | None, name: str, signature: str | None = None) -> None:
        warnings.warn(
            "The 'FQN' class is deprecated and will be removed in a future release. "
            "Please use 'QualifiedIdentifier' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
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
            return NotImplemented
        return self.identifier == other.identifier

    @classmethod
    def from_string(cls, identifier: str) -> FQN:
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
            raise InvalidIdentifierError(identifier)

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
        return cls(name=unqualified_name, schema=schema, database=database, signature=signature)

    def set_database(self, database: str | None) -> FQN:
        if database:
            self._database = database
        return self

    def set_schema(self, schema: str | None) -> FQN:
        if schema:
            self._schema = schema
        return self

    def set_name(self, name: str) -> FQN:
        self._name = name
        return self

    def using_connection(self, conn: SnowflakeConnection) -> FQN:
        """Update the instance with database and schema from connection."""
        # Update the identifier only it if wasn't already a qualified name
        if conn.database and not self.database:
            self.set_database(conn.database)
        if conn.schema and not self.schema:
            self.set_schema(conn.schema)
        return self

    def to_dict(self) -> dict[str, str | None]:
        """Return the dictionary representation of the instance."""
        return {"name": self.name, "schema": self.schema, "database": self.database}


# Equality is by Snowflake identity, not original spelling, so ``eq=False``.
@dataclass(frozen=True, eq=False, slots=True)
class Identifier:
    """Represents a Snowflake object identifier.

    The original spelling is preserved, while equality and hashing follow Snowflake's
    identifier rules. Unlike :data:`IdentifierString`, instances representing the same
    Snowflake object compare equal.

    Raises
    ------
    ValueError
        If *value* is not a valid SQL identifier.
    TypeError
        If *value* is not an :data:`IdentifierLike`.
    """

    _original_spelling: str
    _normalized_spelling: str = field(init=False, repr=False)

    def __new__(cls, value: IdentifierLike) -> Identifier:
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            # ``slots=True`` makes the decorator return a new class object, so the zero-argument
            # ``super()`` in this body would resolve against the pre-decoration class.
            return object.__new__(cls)
        raise TypeError(f"Invalid type for Identifier: {type(value)}")

    def __init__(self, value: IdentifierLike) -> None:
        if isinstance(value, type(self)):
            return
        raw_identifier = str(value)
        if not is_valid_identifier(raw_identifier):
            raise ValueError(
                f"{raw_identifier} is not a valid SQL identifier."
                "Please refer to the documentation for what constitutes a valid identifier."
            )
        object.__setattr__(self, "_original_spelling", raw_identifier)
        object.__setattr__(self, "_normalized_spelling", quote_name(raw_identifier))

    @classmethod
    def from_canonical_name(cls, name: CanonicalName) -> Identifier:
        """Build an :class:`Identifier` that resolves to *name*.

        Parameters
        ----------
        name : CanonicalName
            Canonical (case-sensitive, unquoted) Snowflake object name.

        Returns
        -------
        Identifier
            An identifier whose spelling resolves to *name*.
        """
        return cls(name.to_identifier_string())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Identifier):
            return other._normalized_spelling == self._normalized_spelling
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._normalized_spelling)

    def __str__(self) -> str:
        return self._original_spelling

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._original_spelling!r})"

    def to_identifier_string(self) -> IdentifierString:
        """Return this identifier's current spelling as an :data:`IdentifierString`.

        Unlike :class:`Identifier` equality, the result compares character-for-character.
        Equivalent spellings of the same Snowflake object (for example ``foo``, ``FOO``,
        and ``"FOO"``) are distinct values.

        Returns
        -------
        IdentifierString
            The current spelling as a plain :class:`str` at runtime but with a distinct type for linting.
        """
        return IdentifierString(self._original_spelling)

    def with_quoted_spelling(self) -> Identifier:
        """Return an :class:`Identifier` whose spelling is quoted.

        Unquoted identifiers are quoted with :func:`quote_name`. Already quoted
        identifiers keep their existing spelling. Identity is unchanged.

        Returns
        -------
        Identifier
            An identifier whose original spelling is a double-quoted Snowflake identifier.
        """
        return Identifier(quote_name(self.to_identifier_string()))

    def with_normalized_spelling(self) -> Identifier:
        """Return an :class:`Identifier` whose spelling is a normalized form.

        Normalized here means the spelling for two logically equivalent identifiers is the same.
        Identity is unchanged.

        Returns
        -------
        Identifier
            An identifier with normalized spelling.
        """
        return self.with_quoted_spelling()


IdentifierString = NewType("IdentifierString", str)
IdentifierString.__doc__ = """The string spelling of a Snowflake object identifier.

A :class:`~typing.NewType` of :class:`str`, so at runtime a value is a plain
:class:`str` (and can be bound by the Snowflake connector). Type checkers treat it
as distinct from an arbitrary string. Construct with a spelling already represented
as :class:`str`; convert an :class:`Identifier` or :class:`CanonicalName` with
:meth:`Identifier.to_identifier_string` or :meth:`CanonicalName.to_identifier_string`.

Use :meth:`CanonicalName.resolve_from_identifier` to resolve a spelling to its :class:`CanonicalName`.
"""


IdentifierLike: TypeAlias = Identifier | IdentifierString | str
"""A value that can be converted to an :class:`Identifier`.

Strings by default are treated as identifiers rather than canonical names.
Use :class:`CanonicalName` to represent a canonical name.
"""


def is_identifier_like(value: object) -> TypeGuard[IdentifierLike]:
    """Return whether *value* is an :data:`IdentifierLike` at runtime.

    This behaves like what we'd want ``isinstance(value, IdentifierLike)`` to be,
    which unfortunately doesn't work because ``IdentifierString`` is a ``NewType``.
    """
    return isinstance(value, (Identifier, str))


@dataclass(frozen=True, slots=True, eq=True)
class QualifiedIdentifier:
    """Represents a Snowflake object identifier with optional schema and database qualifiers.

    Components are :class:`Identifier` instances, so equality and hashing follow Snowflake's
    identifier rules. The name may be unqualified, schema-qualified, or database-qualified.
    When a database is set without a schema, the SQL form uses double-dot notation
    (``database..name``).

    Parameters
    ----------
    name : IdentifierLike
        Object name identifier.
    schema : IdentifierLike or None, optional
        Schema qualifier, if any.
    database : IdentifierLike or None, optional
        Database qualifier, if any.

    Raises
    ------
    ValueError
        If any provided component is not a valid SQL identifier.
    TypeError
        If any provided component is not an :data:`IdentifierLike`.

    Examples
    --------
    >>> qi = QualifiedIdentifier.from_string("my_schema.object").using_connection(conn)

    >>> qi = QualifiedIdentifier("my_name").with_database("db").with_schema("foo")
    """

    _name: Identifier
    _schema: Identifier | None = None
    _database: Identifier | None = None

    def __init__(
        self,
        name: IdentifierLike,
        schema: IdentifierLike | None = None,
        database: IdentifierLike | None = None,
    ) -> None:
        object.__setattr__(self, "_name", Identifier(name))
        object.__setattr__(self, "_schema", Identifier(schema) if schema is not None else None)
        object.__setattr__(self, "_database", Identifier(database) if database is not None else None)

    @property
    def name(self) -> Identifier:
        return self._name

    @property
    def schema(self) -> Identifier | None:
        return self._schema

    @property
    def database(self) -> Identifier | None:
        return self._database

    def __str__(self) -> str:
        """Return the SQL spelling of this qualified identifier."""
        if self.database is not None and self.schema is not None:
            return f"{self.database}.{self.schema}.{self.name}"
        if self.database is not None:
            return f"{self.database}..{self.name}"
        if self.schema is not None:
            return f"{self.schema}.{self.name}"
        return str(self.name)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, schema={self.schema!r}, database={self.database!r})"

    def with_name(self, name: IdentifierLike) -> QualifiedIdentifier:
        """Return a copy with *name* replaced.

        Parameters
        ----------
        name : IdentifierLike
            New object name identifier.

        Returns
        -------
        QualifiedIdentifier
            A new instance with the updated name.
        """
        return QualifiedIdentifier(name=name, schema=self.schema, database=self.database)

    def with_schema(self, schema: IdentifierLike | None) -> QualifiedIdentifier:
        """Return a copy with *schema* replaced.

        Parameters
        ----------
        schema : IdentifierLike or None
            New schema qualifier, or ``None`` to clear it.

        Returns
        -------
        QualifiedIdentifier
            A new instance with the updated schema.
        """
        return QualifiedIdentifier(name=self.name, schema=schema, database=self.database)

    def with_database(self, database: IdentifierLike | None) -> QualifiedIdentifier:
        """Return a copy with *database* replaced.

        Parameters
        ----------
        database : IdentifierLike or None
            New database qualifier, or ``None`` to clear it.

        Returns
        -------
        QualifiedIdentifier
            A new instance with the updated database.
        """
        return QualifiedIdentifier(name=self.name, schema=self.schema, database=database)

    def with_quoted_spelling(self) -> QualifiedIdentifier:
        """Return a copy whose components use quoted spellings.

        Returns
        -------
        QualifiedIdentifier
            A new instance with quoted component spellings. Identity is unchanged.
        """
        return QualifiedIdentifier(
            name=self.name.with_quoted_spelling(),
            schema=self.schema.with_quoted_spelling() if self.schema is not None else None,
            database=self.database.with_quoted_spelling() if self.database is not None else None,
        )

    def with_normalized_spelling(self) -> QualifiedIdentifier:
        """Return a copy whose components use normalized spellings.

        Returns
        -------
        QualifiedIdentifier
            A new instance with normalized component spellings. Identity is unchanged.
        """
        return self.with_quoted_spelling()

    def using_connection(self, conn: SnowflakeConnection) -> QualifiedIdentifier:
        """Return a copy filled in with database and schema from *conn* when unset.

        Parameters
        ----------
        conn : SnowflakeConnection
            Connection whose current database and schema may supply missing qualifiers.

        Returns
        -------
        QualifiedIdentifier
            A new instance with qualifiers taken from *conn* where this instance had none.
        """
        result = self
        if conn.database and result.database is None:
            result = result.with_database(conn.database)
        if conn.schema and result.schema is None:
            result = result.with_schema(conn.schema)
        return result

    def to_dict(self) -> dict[str, str | None]:
        """Return the dictionary representation of the instance.

        Returns
        -------
        dict of str to str or None
            Mapping with keys ``name``, ``schema``, and ``database``.
        """
        return {
            "name": str(self.name),
            "schema": str(self.schema) if self.schema is not None else None,
            "database": str(self.database) if self.database is not None else None,
        }

    @classmethod
    def from_string(cls, raw_qualified_identifier: str) -> QualifiedIdentifier:
        """Parse ``[[database.]schema.]name`` or ``database..name`` into a :class:`QualifiedIdentifier`.

        Parameters
        ----------
        raw_qualified_identifier : str
            Object name in the form ``name``, ``schema.name``, ``database.schema.name``,
            or ``database..name``. Callables with signature suffixes are not accepted.

        Returns
        -------
        QualifiedIdentifier
            Parsed qualified identifier.

        Raises
        ------
        InvalidIdentifierError
            If *identifier* does not meet identifier requirements.
        """
        qualifier_pattern = (
            rf"(?:"
            rf"(?P<database>{VALID_IDENTIFIER_REGEX})\.(?P<schema>{VALID_IDENTIFIER_REGEX})\."
            rf"(?P<three_part_name>{VALID_IDENTIFIER_REGEX})"
            rf"|(?P<database_only>{VALID_IDENTIFIER_REGEX})\.\.(?P<double_dot_name>{VALID_IDENTIFIER_REGEX})"
            rf"|(?P<schema_only>{VALID_IDENTIFIER_REGEX})\.(?P<two_part_name>{VALID_IDENTIFIER_REGEX})"
            rf"|(?P<name_only>{VALID_IDENTIFIER_REGEX})"
            rf")"
        )
        result = re.fullmatch(qualifier_pattern, raw_qualified_identifier)
        if result is None:
            raise InvalidIdentifierError(raw_qualified_identifier)

        if result.group("three_part_name") is not None:
            return cls(
                name=result.group("three_part_name"),
                schema=result.group("schema"),
                database=result.group("database"),
            )
        if result.group("double_dot_name") is not None:
            return cls(
                name=result.group("double_dot_name"),
                schema=None,
                database=result.group("database_only"),
            )
        if result.group("two_part_name") is not None:
            return cls(
                name=result.group("two_part_name"),
                schema=result.group("schema_only"),
                database=None,
            )
        return cls(name=result.group("name_only"), schema=None, database=None)


class CanonicalName:
    """Canonical name of an object in Snowflake.

    A canonical name is the actual name of an object, case-sensitive and unquoted.
    """

    def __init__(self, value: str):
        self._value = value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._value!r})"

    @classmethod
    def resolve_from_identifier(cls, identifier: IdentifierLike) -> CanonicalName:
        """Resolve an identifier spelling to the canonical name Snowflake would store.

        See https://docs.snowflake.com/en/sql-reference/identifiers-syntax#label-identifier-casing
        for the resolution rules. Construction of :class:`Identifier` performs the validation.

        Parameters
        ----------
        identifier : IdentifierLike
            Identifier spelling or :class:`Identifier` instance.

        Returns
        -------
        CanonicalName
            Canonical (case-sensitive, unquoted) name for the identifier.

        Raises
        ------
        ValueError
            If *identifier* is not a valid SQL identifier.
        TypeError
            If *identifier* is not an :data:`IdentifierLike`.
        """
        spelling = str(Identifier(identifier))
        if SNOWFLAKE_QUOTED_ID_RE.match(spelling):
            return cls(unquote_name(spelling).replace(DOUBLE_QUOTE + DOUBLE_QUOTE, DOUBLE_QUOTE))
        return cls(spelling.upper())

    def to_identifier_string(self) -> IdentifierString:
        """Produce an identifier string which would resolve to this canonical name.

        Returns
        -------
        IdentifierString
            An identifier string that resolves to this canonical name.
            It is possible that many different identifier strings could resolve to this canonical name.
        """
        # Canonical names are case-preserved; quote without applying unquoted uppercasing.
        return IdentifierString(quote_name(self._value, keep_case=True))

    def __eq__(self, other: object) -> bool:
        # Comparison against IdentifierLike is intentionally not implemented.
        # The user must explicitly convert before comparing.
        # It would be awkward to have them compare equal in collections and such,
        # and equivalent CanonicalName and identifier instances would need to hash
        # to the same value.
        if isinstance(other, CanonicalName):
            return other._value == self._value
        return NotImplemented

    def __add__(self, other: object) -> CanonicalName:
        if isinstance(other, CanonicalName):
            return CanonicalName(self._value + other._value)
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(cls),
                core_schema.no_info_after_validator_function(cls, core_schema.str_schema()),
            ]
        )
