from __future__ import annotations

import datetime
import re
import time
import typing as t

import humanize

if t.TYPE_CHECKING:
    from sqlglot.expressions import (
        Create as CreateStatement,
    )
    from sqlglot.expressions import (
        Expr as SqlglotExpr,
    )
    from sqlglot.expressions import (
        Expression as SqlglotExpression,
    )
    from sqlglot.expressions import (
        Table as SqlglotTable,
    )


def str_to_bool(s: str | None) -> bool:
    """
    Convert a string to a boolean. distutils is being deprecated and it is recommended to implement your own version:
    https://peps.python.org/pep-0632/

    Unlike distutils, this actually returns a bool and never raises. If a value cannot be determined to be true
    then false is returned.
    """
    if not s:
        return False
    return s.lower() in ("true", "1", "t", "y", "yes", "on")


def to_bool(value: t.Any) -> bool:
    """Coerce a bool, int, or string to a boolean.

    Unlike str_to_bool, this accepts bools and ints directly (strings are delegated to
    str_to_bool) and raises ValueError for any other type rather than silently
    returning False.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return str_to_bool(value)
    if isinstance(value, int):
        return bool(value)
    raise ValueError(
        f"Cannot convert value of type {type(value).__name__} to bool: {value!r}. "
        "Expected bool, int, or string (e.g., 'true', 'false', 'yes', 'no')."
    )


def current_epoch_millis() -> int:
    """Return the current time in milliseconds since Unix epoch."""
    return time.time_ns() // 1_000_000


def extract_select_from_ctas(create: CreateStatement) -> SqlglotExpression:
    """Extract the query from a CREATE TABLE / VIEW AS statement.

    The query body may be a single SELECT or a set operation (UNION / INTERSECT /
    EXCEPT), optionally wrapped in parentheses.

    Args:
        create: The CTAS statement.

    Returns:
        The extracted query expression.
    """
    from sqlglot import exp

    if not isinstance(create.expression, (exp.Subquery, exp.Query)):
        raise ValueError(
            "Invalid CREATE statement. Only CREATE ... AS SELECT statements are supported"
        )
    query = create.expression
    return unwrap_subquery(query)


def unwrap_subquery(query: SqlglotExpression) -> SqlglotExpression:
    """Unwrap a query wrapped in one or more parenthesized subquery layers.

    Strips outer ``exp.Subquery`` wrappers that act purely as parentheses
    (i.e. ``is_wrapper`` is ``True``) and returns the inner expression.
    If the expression is not a wrapping subquery it is returned unchanged.

    Args:
        query: The expression to unwrap.

    Returns:
        The innermost non-wrapper expression.
    """
    from sqlglot import exp

    while isinstance(query, exp.Subquery) and query.is_wrapper:
        query = query.this
    return query


def is_udtf_argument_query(query: SqlglotExpr) -> bool:
    """True for a query passed directly to a UDTF other than UNNEST / LATERAL, e.g. EXPLODE((SELECT ...)).

    sqlglot's scope builder treats these as scope boundaries but only traverses the arguments of
    UNNEST and LATERAL, so their tables are invisible to `traverse_scope` and `qualify`.
    """
    from sqlglot import exp

    return isinstance(query.parent, exp.UDTF) and not isinstance(
        query.parent, (exp.Unnest, exp.Lateral)
    )


def expose_udtf_argument_subqueries(expression: SqlglotExpr) -> None:
    """Wrap every `is_udtf_argument_query` query in parentheses, in place, so sqlglot scopes it
    like any other subquery."""
    from sqlglot import exp

    for query in list(expression.find_all(exp.Query)):
        if is_udtf_argument_query(query):
            # Re-parent the original node rather than a copy, so nested matches still found by this loop stay in
            # the tree
            paren = exp.Paren()
            query.replace(paren)
            paren.set("this", query)


def extract_fqn_parts(fqn: str, dialect: str) -> t.Tuple[str, str, str]:
    """
    Given a fully-qualified table name string, eg:

     - "CATALOG"."SCHEMA"."TABLE"
     - catalog.schema."TABLE"
     - catalog."schema"."table"

    break it into its constituent parts (catalog, schema, table).

    If the input string is not fully qualified (i.e doesn't contain 3 parts), an error will be raised.

    Args:
        fqn: Fully-qualified table name string
        dialect: Which SQLGlot dialect to use to interpret the fqn

    Returns:
        A 3-tuple containing the catalog, schema and table name extracted from input fqn.

        Note that if the input part was quoted, the quotes are preserved on the output part
        to prevent a call to normalize_identifiers() from incorrectly changing it
    """
    from sqlglot import exp

    parsed = exp.to_table(fqn, dialect=dialect)

    # we need the underlying exp.Identifier objects to preserve quotes
    catalog, schema, name = (
        parsed.args.get("catalog"),
        parsed.args.get("db"),
        parsed.args.get("this"),
    )

    if not catalog or not schema or not name:
        raise ValueError(f"The supplied fqn: '{fqn}' is not fully qualified")

    if not isinstance(catalog, exp.Expression):
        raise ValueError(f"Expecting SQLGlot expression for catalog, got: {catalog}")

    if not isinstance(schema, exp.Expression):
        raise ValueError(f"Expecting SQLGlot expression for schema, got: {schema}")

    if not isinstance(name, exp.Expression):
        raise ValueError(f"Expecting SQLGlot expression for name, got: {name}")

    return catalog.sql(dialect=dialect), schema.sql(dialect=dialect), name.sql(dialect=dialect)


def normalize_stage_reference(
    table: SqlglotTable, dialect: str, default_catalog: str, default_schema: t.Optional[str]
) -> t.Optional[SqlglotTable]:
    """Normalize a Snowflake named stage reference into the form used as its dependency name.

    sqlglot parses `@db.schema.stage/path (PATTERN => '...')` as a table whose name is the raw
    stage text. The stage name is qualified with the defaults and normalized like a table name.
    The path (case-sensitive) and pattern are kept since they scope the files read; other options
    are dropped. Rendering the result with `.sql(dialect=...)` gives the dependency name, and
    normalizing that again returns the same name. The location is single quoted only when the
    path needs it, e.g. `'@"DB"."SCH"."STG"/my folder/'`.

    Returns:
        The normalized stage reference, or None if `table` is not a named stage reference,
        e.g. a table, a user stage (`@~`) or a table stage (`@%t`).
    """
    from sqlglot import exp
    from sqlglot.errors import ParseError
    from sqlglot.optimizer.normalize_identifiers import normalize_identifiers
    from sqlglot.optimizer.qualify_columns import quote_identifiers

    if not isinstance(table.this, (exp.Var, exp.Literal)) or not table.this.name.startswith("@"):
        return None
    location = table.this.name[1:]
    if location.startswith(("~", "%")):
        return None

    # The stage name ends at the first "/" outside double quotes
    in_quotes = False
    name_end = len(location)
    for i, char in enumerate(location):
        if char == '"':
            in_quotes = not in_quotes
        elif char == "/" and not in_quotes:
            name_end = i
            break
    name, path = location[:name_end], location[name_end:]

    try:
        stage = exp.to_table(name, dialect=dialect)
    except ParseError:
        return None
    if not stage.name:
        return None
    if not stage.db and default_schema:
        stage.set("db", exp.parse_identifier(default_schema, dialect=dialect))
    if stage.db and not stage.catalog:
        stage.set("catalog", exp.parse_identifier(default_catalog, dialect=dialect))
    stage = quote_identifiers(normalize_identifiers(stage, dialect=dialect), dialect=dialect)

    location = f"@{stage.sql(dialect=dialect)}{path}"
    # An unquoted location can't contain these, see Snowflake's _parse_location_path in sqlglot
    needs_quotes = re.search(r"[\s,()']|--|/\*", path)
    pattern = table.args.get("pattern")
    return exp.Table(
        this=exp.Literal.string(location) if needs_quotes else exp.Var(this=location),
        pattern=pattern.copy() if pattern else None,
    )


def format_as_localtime(dt: datetime.datetime) -> str:
    local_dt = dt.astimezone()  # convert to localtime
    return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")


def format_epoch_relative(epoch: t.Optional[int]) -> str:
    if epoch is None:
        return "no data"

    as_dt = datetime.datetime.fromtimestamp(epoch / 1000, tz=datetime.timezone.utc)
    return f"{humanize.naturaltime(as_dt)}, {format_as_localtime(as_dt)}"
