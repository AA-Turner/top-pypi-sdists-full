import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional

import sqlglot
from sqlglot.tokens import TokenType

from sagemaker_studio.sql_engine.resource_fetching_definition import (
    ResourceFetchingDefinition,
    SQLAlchemyMetadataAction,
)

logger = logging.getLogger(__name__)

# Read-only sqlglot statement keys. INSERT ... SELECT ("insert") and CTAS ("create") fall out.
_ROW_LIMITABLE_STATEMENT_TYPES = frozenset({"SELECT", "UNION", "INTERSECT", "EXCEPT"})

# Every opted-in dialect takes a trailing LIMIT n.
_ROW_LIMIT_CLAUSE = "LIMIT"

# The statement_type split_query assigns when sqlglot could not parse the statement.
_UNCLASSIFIED_STATEMENT_TYPE = "UNKNOWN"

# Logged only when no parse can classify a statement; deliberate exclusions stay silent.
_ROW_LIMIT_NOT_APPLIED = (
    "Row limit not applied: could not parse this statement (statement_type=%s, dialect=%s); "
    "it is submitted as written, without the requested limit of %s rows"
)

# A quoted string parses in every position a placeholder can occupy, including after
# TIMESTAMP or DATE, where a bare placeholder does not parse at all.
_PLACEHOLDER_MASK = "'0'"


def _is_name(text: str) -> bool:
    """True for [A-Za-z_][A-Za-z0-9_]*, the placeholder names athena_v4 binds."""
    return text.isascii() and text.isidentifier()


def _mask_placeholders(statement: str, dialect: Optional[str]) -> str:
    """
    Return a copy of ``statement`` with each placeholder replaced by a literal.

    Masks ``?``, ``:name``, ``$1``, ``$name`` and ``@name``. The copy is only parsed for
    classification, never submitted. Placeholders are found by token, so ``::`` casts and
    markers inside string literals are left alone.
    """
    tokens = sqlglot.Dialect.get_or_raise(dialect).tokenize(statement)
    spans = []
    for marker, following in zip(tokens, [*tokens[1:], None]):
        if marker.token_type is TokenType.PLACEHOLDER:
            spans.append((marker.start, marker.end + 1))
            continue
        if marker.token_type not in (TokenType.COLON, TokenType.PARAMETER):
            continue
        # The name must be the very next token, touching the marker. Raw text, not
        # token.text, so a quoted identifier like :"x" is not taken for a name.
        if following is None or following.start != marker.end + 1:
            continue
        name = statement[following.start : following.end + 1]
        is_position = marker.token_type is TokenType.PARAMETER and name.isdigit()
        # A keyword after the marker is still a name: :date tokenizes as DATE, not VAR.
        if _is_name(name) or is_position:
            spans.append((marker.start, following.end + 1))

    # Reversed, so each replacement leaves the offsets of the earlier ones valid.
    for start, end in reversed(spans):
        statement = statement[:start] + _PLACEHOLDER_MASK + statement[end:]
    return statement


@dataclass
class SqlStatement:
    """Represents a SQL statement with its type."""

    statement: str
    statement_type: str


class DatabaseTransformer(ABC):
    """
    Abstract base class for database connection transformers.

    This class defines the interface for transforming connection configurations
    into SQLAlchemy-compatible formats. Each concrete implementation handles
    a specific database type and its connection requirements.
    """

    # Opt-in: True only where the dialect's native row limit is a trailing LIMIT n.
    supports_row_limit: ClassVar[bool] = False

    @classmethod
    @abstractmethod
    def get_dialect(cls) -> Optional[str]:
        """
        Get the SQL dialect for this database type.

        Used by sqlglot for parsing SQL statements. Return None if
        generic SQL parsing is sufficient.

        Returns:
            Optional[str]: Dialect name (e.g., "redshift", "postgres") or None
                for generic SQL parsing.

        Raises:
            NotImplementedError: Must be implemented by concrete subclasses.
        """

    @staticmethod
    @abstractmethod
    def get_required_fields() -> List[str]:
        """
        Get the list of required fields for this database connection type.

        Returns:
            List[str]: List of field names that must be present in the
                connection data for successful transformation.

        Raises:
            NotImplementedError: Must be implemented by concrete subclasses.
        """

    @staticmethod
    def get_loggers() -> List[str]:
        """
        Get the list of loggers used for this database connection type.

        Returns:
            List[str]: List of loggers that are used for this database connection type.
        """
        return []

    @staticmethod
    @abstractmethod
    def to_sqlalchemy_config(connection_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform connection data into SQLAlchemy configuration.

        Converts database-specific connection parameters into a format
        suitable for SQLAlchemy engine creation, including connection
        strings and connection arguments.

        Args:
            connection_data (Dict[str, Any]): Raw connection configuration data.

        Returns:
            Dict[str, Any]: SQLAlchemy configuration dictionary containing:
                - connection_string: SQLAlchemy-compatible connection string
                - connect_args: Additional connection arguments (optional)

        Raises:
            NotImplementedError: Must be implemented by concrete subclasses.
            ValueError: If required fields are missing from connection_data.
        """

    @staticmethod
    def validate_required_fields(
        required_fields: List[str], connection_data: Dict[str, Any]
    ) -> None:
        """
        Validate that all required fields are present in connection data.

        Args:
            required_fields (List[str]): List of field names that must be present.
            connection_data (Dict[str, Any]): Connection data to validate.

        Raises:
            ValueError: If any required field is missing or empty in connection_data.
        """
        for field in required_fields:
            if not connection_data.get(field):
                raise ValueError(f"{field} is required for connection")

    @staticmethod
    @abstractmethod
    def get_resources_action(
        resource_type: Optional[str], parents: Optional[Dict[str, str]] = None
    ) -> ResourceFetchingDefinition:
        """
        Build a definition for metadata-based resource discovery.

        Returns a `ResourceFetchingDefinition` configured to use SQLAlchemy’s
        Inspector for listing resources, based on the requested `resource_type`.
        If `resource_type` is `None`, it defaults to the database level.

        This method does **not** read `parents`; any required parent context
        (e.g., schema when listing tables) is supplied later by the consumer
        when executing the definition.

        Args:
          resource_type: Which level to discover. Supported values:
            `"DATABASE"`, `"TABLE"`, `"COLUMN"`. If `None`, treated as `"DATABASE"`.
          parents: Optional mapping of parent identifiers. Ignored here, kept
            for syntax purposes.

        Returns:
          A `ResourceFetchingDefinition` in SQLAlchemy-metadata mode with:
            - `GET_TABLE_NAMES` for `"TABLE"` (children: `("COLUMN",)`),
            - `GET_COLUMN_NAMES` for `"COLUMN"` (children: `()`),
            - `GET_SCHEMA_NAMES` for `"DATABASE"` or `None` (children: `("TABLE",)`).

        Raises:
          ValueError: If `resource_type` is not one of the supported values.
        """
        match resource_type:
            case "TABLE":
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_TABLE_NAMES,
                    default_type="TABLE",
                    children=("COLUMN",),
                )
            case "COLUMN":
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_COLUMN_NAMES,
                    default_type="COLUMN",
                    children=(),
                )
            case "DATABASE" | None:
                return ResourceFetchingDefinition.from_sqlalchemy_metadata(
                    SQLAlchemyMetadataAction.GET_SCHEMA_NAMES,
                    default_type="DATABASE",
                    children=("TABLE",),
                )
            case other:
                raise ValueError(f"Unsupported resource type: {other!r}")

    @staticmethod
    def get_required_resource_parent(parents: dict, required_type: str):
        """
        Return a required parent identifier from a mapping.

        Ensures the given parent resource (e.g., `"DATABASE"`, `"SCHEMA"`, `"TABLE"`)
        is present in the `parents` mapping used to scope resource discovery. If the
        key is missing, a clear `KeyError` is raised.

        Args:
          parents: Mapping of parent resource kinds to their identifiers
            (e.g., `{"DATABASE": "dev", "SCHEMA": "public"}`).
          required_type: The required parent key to look up (e.g., `"SCHEMA"`).

        Returns:
          The identifier associated with `parent`.

        Raises:
          KeyError: If `parent` is not found in `d`.
        """
        if parents is None:
            return None
        elif required_type in parents:
            return parents[required_type]
        else:
            raise KeyError(f"Required parent type '{required_type}' not found in provided parents.")

    @staticmethod
    def get_execution_metadata(cursor: Any) -> Optional[Dict[str, Any]]:
        """Extract engine-specific execution metadata from a DBAPI cursor.

        Override in subclasses to return metadata such as external query IDs,
        execution stats, data scanned, etc. The default implementation returns
        None (no metadata available).

        Args:
            cursor: The raw DBAPI cursor after query execution.

        Returns:
            Dict with engine-specific metadata, or None if not available.
        """
        return None

    @classmethod
    def split_query(cls, query: str) -> List[SqlStatement]:
        """
        Split a SQL query into individual statements using sqlglot.

        Splits on real semicolon tokens and returns each statement's original
        text; sqlglot is used only for boundaries and statement_type, since
        re-rendering via stmt.sql() can rewrite valid SQL (e.g. Redshift
        ``USING ICEBERG``).

        This method can be overridden by subclasses if sqlglot does not
        support the specific database type.

        Args:
            query (str): The SQL query to split.

        Returns:
            List[SqlStatement]: List of SQL statement objects with statement and type.
        """
        try:
            # Use the dialect's own tokenizer (e.g. Redshift `$$` bodies);
            # Tokenizer(dialect=...) falls back to generic rules.
            dialect = sqlglot.Dialect.get_or_raise(cls.get_dialect())
            boundaries = [
                token
                for token in dialect.tokenize(query)
                if token.token_type is TokenType.SEMICOLON
            ]
            statements: List[SqlStatement] = []
            start = 0
            for boundary in [*boundaries, None]:
                end = boundary.start if boundary is not None else len(query)
                statement = query[start:end].strip()
                start = boundary.end + 1 if boundary is not None else len(query)
                # Skip empty and comment-only chunks.
                if not statement or not dialect.tokenize(statement):
                    continue
                try:
                    parsed = dialect.parse(statement)[0]
                    statement_type = parsed.key.upper() if parsed and parsed.key else "UNKNOWN"
                except Exception:
                    statement_type = "UNKNOWN"
                statements.append(SqlStatement(statement=statement, statement_type=statement_type))
            return statements
        except Exception:
            # Fallback to simple semicolon splitting if sqlglot fails
            return [
                SqlStatement(statement=stmt.strip(), statement_type="UNKNOWN")
                for stmt in query.split(";")
                if stmt.strip()
            ]

    @classmethod
    def apply_row_limit(
        cls,
        statement: str,
        statement_type: str,
        limit_query_results: Optional[int] = None,
    ) -> str:
        """
        Return ``statement`` with a row limit appended, or unchanged.

        sqlglot decides eligibility only; the clause is appended as text, so the author's
        parameters, comments and syntax survive verbatim. An existing limit is never lowered.

        Args:
            statement (str): One SQL statement, as produced by split_query.
            statement_type (str): The matching SqlStatement.statement_type.
            limit_query_results (Optional[int]): Requested maximum rows. None disables
                the transform.

        Returns:
            str: ``statement`` followed by the row-limit clause, or ``statement`` unchanged.
        """
        if not cls.supports_row_limit:
            return statement
        # bool is an int subclass, and formatting True would append "LIMIT True".
        if isinstance(limit_query_results, bool) or not isinstance(limit_query_results, int):
            return statement
        if limit_query_results <= 0:
            return statement
        dialect = cls.get_dialect()
        # Usually a placeholder blocked split_query's parse; classify a masked copy instead.
        masked = statement_type == _UNCLASSIFIED_STATEMENT_TYPE
        if not masked and statement_type not in _ROW_LIMITABLE_STATEMENT_TYPES:
            return statement

        try:
            node = sqlglot.parse_one(
                _mask_placeholders(statement, dialect) if masked else statement, dialect=dialect
            )
        except Exception:
            logger.warning(
                _ROW_LIMIT_NOT_APPLIED,
                statement_type,
                dialect,
                limit_query_results,
                exc_info=True,
            )
            return statement

        if masked and node.key.upper() not in _ROW_LIMITABLE_STATEMENT_TYPES:
            return statement

        # Never lower an existing limit. args["limit"] covers LIMIT, FETCH FIRST and TOP.
        if node.args.get("limit") is not None:
            return statement
        # LIMIT must precede FOR UPDATE, so a locking read has no appendable position.
        if node.args.get("locks"):
            return statement
        # SELECT ... INTO creates a table, so a limit here would truncate what it writes.
        if node.args.get("into") is not None:
            return statement
        # Spark wants LIMIT before OFFSET, so an offset leaves no portable trailing position.
        if node.args.get("offset") is not None:
            return statement

        # The newline is load-bearing: a trailing line comment would swallow the clause.
        return f"{statement}\n{_ROW_LIMIT_CLAUSE} {limit_query_results}"

    @classmethod
    def apply_row_limits(
        cls,
        statements: List[SqlStatement],
        limit_query_results: Optional[int] = None,
    ) -> List[SqlStatement]:
        """
        Apply apply_row_limit to each statement, preserving order, count and type.

        Args:
            statements (List[SqlStatement]): Statements as produced by split_query.
            limit_query_results (Optional[int]): Requested maximum rows per statement.

        Returns:
            List[SqlStatement]: Statements in the same order, each limited or unchanged.
        """
        return [
            SqlStatement(
                statement=cls.apply_row_limit(
                    item.statement, item.statement_type, limit_query_results
                ),
                statement_type=item.statement_type,
            )
            for item in statements
        ]
