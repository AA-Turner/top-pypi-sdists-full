import copy
import logging
import re
import threading
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from typing import FrozenSet, List, Optional, Set, Tuple, Union

from chtoolset import query as chquery
from lru import LRU
from toposort import toposort

from tinybird.ch_utils.constants import COPY_ENABLED_TABLE_FUNCTIONS, ENABLED_TABLE_FUNCTIONS

# VALID_REMOTE is used to explicitly vet queries sent to sql_toolset. In this module, when a table used in a query has
# VALID_REMOTE in the database portion (as in (VALID_REMOTE, "select * from cluster(tinybird, public.t_blabla)"), the
# query is not blocked, even if the rhs (the "select * ..." bit) is not found in the various collections of allowed tables.
VALID_REMOTE = "VALID_REMOTE"


class InvalidFunction(ValueError):
    def __init__(self, msg: str = "", table_function_name: str = ""):
        if any([fn for fn in COPY_ENABLED_TABLE_FUNCTIONS if fn in msg]):
            msg = msg.replace("is restricted", "is restricted to Copy Pipes")

        if table_function_name:
            if table_function_name in COPY_ENABLED_TABLE_FUNCTIONS:
                self.msg = f"The {table_function_name} table function is only allowed in Copy Pipes"
            else:
                self.msg = f"The query uses disabled table functions: '{table_function_name}'"
        else:
            self.msg = msg
        super().__init__(self.msg)


class InvalidResource(ValueError):
    def __init__(self, database: str, table: str, default_database: str = ""):
        if default_database and database == default_database:
            database = ""
        self.msg = f"{database}.{table}" if database else table
        self.msg = f"Resource '{self.msg}' not found"
        super().__init__(self.msg)
        self.database = database
        self.table = table


class UnoptimizedJoinException(Exception):
    def __init__(self, sql: str):
        self.sql = sql
        self.msg = f"Materialized node SQL contains a join that is not optimized: {sql}"
        self.documentation = (
            "/docs/work-with-data/optimization/opt201-fix-mistakes#understanding-the-materialized-join-issue"
        )
        super().__init__(self.msg)


ChQueryTable = Tuple[Optional[str], Optional[str], Optional[str]]


def get_left_table(sql: str, default_database: Optional[str] = None) -> ChQueryTable:
    if default_database is None:
        left_table = chquery.get_left_table(sql)
    else:
        left_table = chquery.get_left_table(sql, default_database=default_database)
    return left_table


def format_sql(sql: str) -> str:
    return chquery.format(sql)


def explain_plan(sql: str) -> str:
    return chquery.explain_ast(sql)


def has_join(sql: str) -> bool:
    return any(line.rstrip().startswith("TableJoin") for line in explain_plan(sql).split())


def has_unoptimized_join(sql: str, left_table: Optional[Union[Tuple[str, str], Tuple[str, str, str]]] = None) -> None:
    """
    Check if a SQL query contains an unoptimized join.
    A join is considered optimized if the right table is filtered by the left table's data.

    Args:
        sql: The SQL query to check
        left_table: Optional tuple of (database, table) for the left table

    Raises:
        UnoptimizedJoin: If an unoptimized join is found
    """
    # TODO: We should check that we are filtering the right table by the left table's data
    # TODO: We should check if using EXPLAIN AST is better than using regex

    number_of_joins = sum(1 for line in explain_plan(sql).split() if line.rstrip().startswith("TableJoin"))
    if number_of_joins == 0:
        return

    if not left_table:
        left_table = chquery.get_left_table(sql)
        if not left_table:
            return

    # Find all JOIN clauses with subqueries
    # This pattern matches anything between JOIN and ON/USING
    join_pattern = r"(?:LEFT\s+|RIGHT\s+|INNER\s+|FULL\s+OUTER\s+)?JOIN\s*\((.*?)\)\s+(?:AS\s+\w+)?\s*(?:ON|USING)"

    # Find all joins with subqueries
    join_matches = list(re.finditer(join_pattern, sql, re.IGNORECASE | re.DOTALL))

    if number_of_joins != len(join_matches):
        logging.debug(f"number_of_joins: {number_of_joins}, join_matches: {join_matches}")
        raise UnoptimizedJoinException(sql)

    # If no joins with subqueries found, probably is an unoptimized join
    if not join_matches:
        raise UnoptimizedJoinException(sql)

    # Check if the left table is referenced in the subquery
    left_table_ref = f"{left_table[0]}.{left_table[1]}"

    for match in join_matches:
        subquery = match.group(1)  # Get the captured subquery
        logging.debug(f"subquery: {subquery} left_table_ref: {left_table_ref}")
        if left_table_ref not in subquery:
            raise UnoptimizedJoinException(sql)


def format_where_for_mutation_command(where_clause: str) -> str:
    """
    >>> format_where_for_mutation_command("numnights = 99")
    'DELETE WHERE numnights = 99'
    >>> format_where_for_mutation_command("\\nnumnights = 99")
    'DELETE WHERE numnights = 99'
    >>> format_where_for_mutation_command("reservationid = 'foo'")
    "DELETE WHERE reservationid = \\\\'foo\\\\'"
    >>> format_where_for_mutation_command("reservationid = '''foo'")
    "DELETE WHERE reservationid = \\\\'\\\\\\\\\\\\'foo\\\\'"
    >>> format_where_for_mutation_command("reservationid = '\\\\'foo'")
    "DELETE WHERE reservationid = \\\\'\\\\\\\\\\\\'foo\\\\'"
    """
    formatted_condition = chquery.format(f"""SELECT {where_clause}""").split("SELECT ")[1]
    formatted_condition = formatted_condition.replace("\\", "\\\\").replace("'", "''")
    quoted_condition = chquery.format(f"SELECT '{formatted_condition}'").split("SELECT ")[1]
    return f"DELETE WHERE {quoted_condition[1:-1]}"


# Functions that take table/dictionary names as string literal arguments.
# Normalizing these would cause incorrect cache hits since different table names
# would map to the same cache key.
# See: https://clickhouse.com/docs/en/sql-reference/functions/other-functions#joinget
#      https://clickhouse.com/docs/en/sql-reference/functions/ext-dict-functions
#      https://clickhouse.com/docs/en/sql-reference/table-functions/cluster
#      https://clickhouse.com/docs/en/sql-reference/table-functions/remote
_FUNCTIONS_WITH_TABLE_NAME_ARGS = re.compile(
    r"\b(?:joinGet|joinGetOrNull|dictGet\w*|dictHas|dictIsIn|hasColumnInTable|remote|cluster|clusterAllReplicas)\s*\(",
    re.IGNORECASE,
)


def _normalize_sql_for_cache(sql: str) -> str:
    """Normalize SQL for cache key purposes.

    Uses normalize_query_keep_names which replaces literal values with placeholders
    while preserving table/column names, so queries with the same structure share
    cache entries.

    However, some functions like joinGet(), dictGet*, remote(), cluster(), and
    clusterAllReplicas() take table/dictionary names as arguments. Normalizing these
    would incorrectly map different tables to the same cache key, so we fall back to
    using the original SQL for such queries.

    >>> _normalize_sql_for_cache("SELECT * FROM events WHERE id = 'alice'")
    'SELECT * FROM events WHERE id = ?'
    >>> _normalize_sql_for_cache("SELECT * FROM events WHERE id = 123 AND name = 'bob'")
    'SELECT * FROM events WHERE id = ? AND name = ?'
    >>> _normalize_sql_for_cache("SELECT * FROM events")
    'SELECT * FROM events'
    >>> _normalize_sql_for_cache("SELECT joinGet('my_table', 'col', id) FROM t")
    "SELECT joinGet('my_table', 'col', id) FROM t"
    >>> _normalize_sql_for_cache("SELECT dictGet('my_dict', 'value', id) FROM t")
    "SELECT dictGet('my_dict', 'value', id) FROM t"
    >>> _normalize_sql_for_cache("SELECT * FROM remote('host', db, table)")
    "SELECT * FROM remote('host', db, table)"
    >>> _normalize_sql_for_cache("SELECT * FROM cluster('cluster_name', db, table)")
    "SELECT * FROM cluster('cluster_name', db, table)"
    >>> _normalize_sql_for_cache("not valid sql at all")
    'not valid sql at all'
    """
    # Skip normalization for queries with functions that have table names as arguments
    if _FUNCTIONS_WITH_TABLE_NAME_ARGS.search(sql):
        return sql

    try:
        return chquery.normalize_query_keep_names(sql)
    except Exception:
        return sql


# Cache for sql_get_used_tables using normalized SQL as key.
# Uses lru-dict (C extension) for a fast LRU implementation.
_sql_get_used_tables_cache: LRU = LRU(2**13)
_sql_get_used_tables_cache_lock = threading.Lock()
_sql_get_used_tables_cache_hits = 0
_sql_get_used_tables_cache_misses = 0


def sql_get_used_tables_cache_info() -> dict:
    """Return cache statistics for sql_get_used_tables."""
    with _sql_get_used_tables_cache_lock:
        return {
            "hits": _sql_get_used_tables_cache_hits,
            "misses": _sql_get_used_tables_cache_misses,
            "size": len(_sql_get_used_tables_cache),
            "maxsize": _sql_get_used_tables_cache.get_size(),
        }


def sql_get_used_tables_cache_clear() -> None:
    """Clear the sql_get_used_tables cache."""
    global _sql_get_used_tables_cache_hits, _sql_get_used_tables_cache_misses
    with _sql_get_used_tables_cache_lock:
        _sql_get_used_tables_cache.clear()
        _sql_get_used_tables_cache_hits = 0
        _sql_get_used_tables_cache_misses = 0


def _sql_get_used_tables_impl(
    sql: str,
    raising: bool,
    default_database: str,
    table_functions: bool,
    function_allow_list: Optional[FrozenSet[str]],
    function_deny_list: Optional[FrozenSet[str]],
    settings_allow_list: Optional[FrozenSet[str]],
    settings_deny_list: Optional[FrozenSet[str]],
) -> tuple[List[Tuple[str, str, str]], bool]:
    """Extract tables from SQL (uncached implementation).

    Returns a tuple of (result, cacheable) where cacheable indicates whether the
    result is safe to store in the cache.
    """
    try:
        _function_allow_list = list() if function_allow_list is None else list(function_allow_list)
        _function_deny_list = list() if function_deny_list is None else list(function_deny_list)
        _settings_allow_list = list() if settings_allow_list is None else list(settings_allow_list)
        _settings_deny_list = list() if settings_deny_list is None else list(settings_deny_list)

        tables: List[Tuple[str, str, str]] = chquery.tables(
            sql,
            default_database=default_database,
            function_allow_list=_function_allow_list,
            function_deny_list=_function_deny_list,
            query_settings_allow_list=_settings_allow_list,
            query_settings_deny_list=_settings_deny_list,
        )
        if not table_functions:
            tables = [(t[0], t[1], "") for t in tables if t[0] or t[1]]

        return tables, True
    except ValueError as e:
        if raising:
            msg = str(e)
            if "is restricted. Contact support@tinybird.co" in msg:
                raise InvalidFunction(msg=msg) from e
            elif "Unknown function tb_secret" in msg:
                raise InvalidFunction(msg="Unknown function tb_secret. Usage: {{tb_secret('secret_name')}}") from e
            elif "Unknown function tb_var" in msg:
                raise InvalidFunction(msg="Unknown function tb_var. Usage: {{tb_var('var_name')}}") from e
            raise
        # Do not cache this fallback result: the returned sql string can contain
        # sensitive literal values, and the normalized cache key could collide
        # across different queries.
        return [(default_database, sql, "")], False


def sql_get_used_tables_cached(
    sql: str,
    raising: bool = False,
    default_database: str = "",
    table_functions: bool = True,
    function_allow_list: Optional[FrozenSet[str]] = None,
    function_deny_list: Optional[FrozenSet[str]] = None,
    settings_allow_list: Optional[FrozenSet[str]] = None,
    settings_deny_list: Optional[FrozenSet[str]] = None,
) -> List[Tuple[str, str, str]]:
    """More like: get used sql names

    Returns a list of tuples: (database_or_namespace, table_name, table_func).

    Uses normalized SQL as cache key to improve hit ratio for templated queries.
    The normalization replaces literal values with placeholders while preserving
    table/column names, so queries with the same structure share cache entries.

    >>> sql_get_used_tables("SELECT 1 FROM the_table")
    [('', 'the_table', '')]
    >>> sql_get_used_tables("SELECT 1 FROM the_database.the_table")
    [('the_database', 'the_table', '')]
    >>> sql_get_used_tables("SELECT * from numbers(100)")
    [('', '', 'numbers')]
    >>> sql_get_used_tables("SELECT * FROM table1, table2")
    [('', 'table1', ''), ('', 'table2', '')]
    >>> sql_get_used_tables("SELECT * FROM table1, table2", table_functions=False)
    [('', 'table1', ''), ('', 'table2', '')]
    >>> sql_get_used_tables("SELECT * FROM numbers(100)", table_functions=False)
    []
    >>> sql_get_used_tables("SELECT * FROM table1, numbers(100)", table_functions=False)
    [('', 'table1', '')]
    >>> sql_get_used_tables("SELECT * FROM `d_d3926a`.`t_976af08ec4b547419e729c63e754b17b`", table_functions=False)
    [('d_d3926a', 't_976af08ec4b547419e729c63e754b17b', '')]
    """
    global _sql_get_used_tables_cache_hits, _sql_get_used_tables_cache_misses

    # Build cache key using normalized SQL
    normalized_sql = _normalize_sql_for_cache(sql)
    cache_key = (
        normalized_sql,
        raising,
        default_database,
        table_functions,
        function_allow_list,
        function_deny_list,
        settings_allow_list,
        settings_deny_list,
    )

    # Single lookup with hit/miss tracking
    with _sql_get_used_tables_cache_lock:
        cached_value = _sql_get_used_tables_cache.get(cache_key)
        if cached_value is not None:
            _sql_get_used_tables_cache_hits += 1
            return cached_value
        _sql_get_used_tables_cache_misses += 1

    # Compute outside lock to avoid blocking other threads
    result, cacheable = _sql_get_used_tables_impl(
        sql,
        raising,
        default_database,
        table_functions,
        function_allow_list,
        function_deny_list,
        settings_allow_list,
        settings_deny_list,
    )

    if cacheable:
        # Store result in cache
        with _sql_get_used_tables_cache_lock:
            _sql_get_used_tables_cache.setdefault(cache_key, result)

    return result


def sql_get_used_tables(
    sql: str,
    raising: bool = False,
    default_database: str = "",
    table_functions: bool = True,
    function_allow_list: Optional[FrozenSet[str]] = None,
    function_deny_list: Optional[FrozenSet[str]] = None,
    settings_allow_list: Optional[FrozenSet[str]] = None,
    settings_deny_list: Optional[FrozenSet[str]] = None,
) -> List[Tuple[str, str, str]]:
    """More like: get used sql names

    Returns a list of tuples: (database_or_namespace, table_name, table_func).
    """
    function_allow_hashable_list = frozenset() if function_allow_list is None else function_allow_list
    function_deny_hashable_list = frozenset() if function_deny_list is None else function_deny_list
    settings_allow_hashable_list = frozenset() if settings_allow_list is None else settings_allow_list
    settings_deny_hashable_list = frozenset() if settings_deny_list is None else settings_deny_list
    return copy.copy(
        sql_get_used_tables_cached(
            sql,
            raising,
            default_database,
            table_functions,
            function_allow_list=function_allow_hashable_list,
            function_deny_list=function_deny_hashable_list,
            settings_allow_list=settings_allow_hashable_list,
            settings_deny_list=settings_deny_hashable_list,
        )
    )


class ReplacementsDict(dict):
    def __init__(self, *args, enabled_table_functions=None, **kwargs):
        self.enabled_table_functions = enabled_table_functions
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        v = super().__getitem__(key)
        if isinstance(v, tuple):
            k, r = v
            if callable(r):
                r = r(self.enabled_table_functions)
                super().__setitem__(key, (k, r))
            return k, r
        if callable(v):
            v = v(self.enabled_table_functions)
            super().__setitem__(key, v)
        return v


def tables_or_sql(replacement: dict, table_functions=False, function_allow_list=None) -> set:
    try:
        return set(
            sql_get_used_tables(
                replacement[1],
                default_database=replacement[0],
                raising=True,
                table_functions=table_functions,
                function_allow_list=frozenset(function_allow_list),
            )
        )
    except Exception as e:
        if replacement[1][0] == "(":
            raise e
        return {replacement}


def _separate_as_tuple_if_contains_database_and_table(definition: str) -> Union[str, Tuple[str, str]]:
    if "." in definition:
        database_and_table_separated = definition.split(".")
        return database_and_table_separated[0], database_and_table_separated[1]
    return definition


def replacements_to_tuples(replacements: dict) -> dict:
    parsed_replacements = {}
    for k, v in replacements.items():
        parsed_replacements[_separate_as_tuple_if_contains_database_and_table(k)] = (
            _separate_as_tuple_if_contains_database_and_table(v)
        )
    return parsed_replacements


@lru_cache(maxsize=2**15)
def replace_tables_chquery_cached(
    sql: str,
    sorted_replacements: Optional[tuple] = None,
    default_database: str = "",
    output_one_line: bool = False,
    timestamp: Optional[datetime] = None,
    function_allow_list: Optional[FrozenSet[str]] = None,
    settings_allow_list: Optional[FrozenSet[str]] = None,
) -> str:
    replacements = dict(sorted_replacements) if sorted_replacements else {}
    _function_allow_list = list() if function_allow_list is None else list(function_allow_list)
    _settings_allow_list = list() if settings_allow_list is None else list(settings_allow_list)
    return chquery.replace_tables(
        sql,
        replacements,
        default_database=default_database,
        one_line=output_one_line,
        function_allow_list=_function_allow_list,
        query_settings_allow_list=_settings_allow_list,
    )


def replace_tables(
    sql: str,
    replacements: dict,
    default_database: str = "",
    check_functions: bool = False,
    only_replacements: bool = False,
    valid_tables: Optional[Set[Tuple[str, str]]] = None,
    output_one_line: bool = False,
    timestamp: Optional[datetime] = None,
    function_allow_list: Optional[FrozenSet[str]] = None,
    settings_allow_list: Optional[FrozenSet[str]] = None,
    original_replacements: Optional[dict] = None,
) -> str:
    """
    Given a query and a list of table replacements, returns the query after applying the table replacements.
    It takes into account dependencies between replacement subqueries (if any)
    It also validates the sql to verify it's valid and doesn't use unknown or prohibited functions
    """
    hashable_list = frozenset() if function_allow_list is None else function_allow_list
    hashable_settings_list = frozenset() if settings_allow_list is None else settings_allow_list
    if not replacements:
        # Always call replace_tables to do validation and formatting
        return replace_tables_chquery_cached(
            sql,
            None,
            output_one_line=output_one_line,
            timestamp=timestamp,
            function_allow_list=hashable_list,
            settings_allow_list=hashable_settings_list,
        )

    _replaced_with = set()
    _replacements = ReplacementsDict()
    for k, r in replacements.items():
        rk = k if isinstance(k, tuple) else (default_database, k)
        _replacements[rk] = r if isinstance(r, tuple) else (default_database, r)
        _replaced_with.add(r)

    if original_replacements:
        # Some replacements have been expanded by filters and turned to a query str, but we need to send the original
        # ones to is_invalid_resource()
        for r in original_replacements.values():
            _replaced_with.add(r)

    deps: defaultdict = defaultdict(set)
    _tables = sql_get_used_tables(
        sql,
        default_database=default_database,
        raising=True,
        table_functions=check_functions,
        function_allow_list=function_allow_list,
        settings_allow_list=settings_allow_list,
    )
    seen_tables = set()
    table: Union[Tuple[str, str], Tuple[str, str, str]]
    if function_allow_list is None:
        _enabled_table_functions = ENABLED_TABLE_FUNCTIONS
    else:
        _enabled_table_functions = ENABLED_TABLE_FUNCTIONS.union(set(function_allow_list))
    _replacements.enabled_table_functions = frozenset(_enabled_table_functions)
    while _tables:
        table = _tables.pop()
        if len(table) == 3:
            first_table, second_table, last_table = table
            if last_table and last_table not in _enabled_table_functions:
                raise InvalidFunction(table_function_name=last_table)
            if first_table or second_table:
                table = (first_table, second_table)
            else:
                continue
        seen_tables.add(table)
        if table in _replacements:
            replacement = _replacements[table]
            dependent_tables = tables_or_sql(
                replacement, table_functions=check_functions, function_allow_list=_enabled_table_functions
            )
            deps[table] |= {(d[0], d[1]) for d in dependent_tables}
            for dependent_table in list(dependent_tables):
                if len(dependent_table) == 3:
                    if (
                        dependent_table[2]
                        and dependent_table[2] not in _enabled_table_functions
                        and not (dependent_table[2] in ["cluster"] and replacement[0] == VALID_REMOTE)
                    ):
                        raise InvalidFunction(table_function_name=dependent_table[2])
                    if dependent_table[0] or dependent_table[1]:
                        dependent_table = (dependent_table[0], dependent_table[1])
                    else:
                        continue
                if dependent_table not in seen_tables:
                    _tables.append(dependent_table)
        else:
            deps[table] |= set()
    deps_sorted = list(reversed(list(toposort(deps))))

    if not deps_sorted:
        return replace_tables_chquery_cached(
            sql,
            None,
            output_one_line=output_one_line,
            timestamp=timestamp,
            function_allow_list=hashable_list,
            settings_allow_list=hashable_settings_list,
        )

    for current_deps in deps_sorted:
        current_replacements = {}
        for r in current_deps:
            if r in _replacements:
                replacement = _replacements[r]
                current_replacements[r] = replacement
            else:
                if only_replacements:
                    continue
                database, table_name = r
                if (
                    table_name
                    and default_database != ""
                    and is_invalid_resource(r, database, default_database, _replaced_with, valid_tables)
                ):
                    logging.info(
                        "Resource not found in replace_tables in sql_toolset: %s",
                        {
                            "r": r,
                            "default_database": default_database,
                            "_replaced_with": _replaced_with,
                            "valid_tables": valid_tables,
                        },
                    )
                    raise InvalidResource(database, table_name, default_database=default_database)

        if current_replacements:
            # We need to transform the dictionary into something cacheable, so a sorted tuple of tuples it is
            r = tuple(sorted([(k, v) for k, v in current_replacements.items()]))
            sql = replace_tables_chquery_cached(
                sql,
                r,
                default_database=default_database,
                output_one_line=output_one_line,
                timestamp=timestamp,
                function_allow_list=hashable_list,
                settings_allow_list=hashable_settings_list,
            )
        else:
            sql = replace_tables_chquery_cached(
                sql,
                None,
                output_one_line=output_one_line,
                timestamp=timestamp,
                function_allow_list=hashable_list,
                settings_allow_list=hashable_settings_list,
            )

    # Fix for empty database names in JOINs - remove empty backticks like ``.table_name
    # that are generated when chquery.replace_tables processes tuples with empty database names
    sql = sql.replace("``.", "")

    return sql


def is_invalid_resource(
    r: Tuple[str, str],
    database: str,
    default_database: str,
    _replaced_with: Set[Tuple[str, str]],
    valid_tables: Optional[Set[Tuple[str, str]]] = None,
) -> bool:
    return is_invalid_resource_from_other_workspace(
        r, database, default_database, _replaced_with, valid_tables
    ) or is_invalid_resource_from_current_workspace(r, database, default_database, _replaced_with, valid_tables)


def is_invalid_resource_from_other_workspace(
    r: Tuple[str, str],
    database: str,
    default_database: str,
    _replaced_with: Set[Tuple[str, str]],
    valid_tables: Optional[Set[Tuple[str, str]]],
) -> bool:
    # return database not in [default_database, "tinybird", VALID_REMOTE] and r not in _replaced_with
    return bool(
        database not in [default_database, "tinybird", VALID_REMOTE]
        and valid_tables
        and r not in valid_tables
        and r not in _replaced_with
    )


def is_invalid_resource_from_current_workspace(
    r: Tuple[str, str],
    database: str,
    default_database: str,
    _replaced_with: Set[Tuple[str, str]],
    valid_tables: Optional[Set[Tuple[str, str]]],
) -> bool:
    return bool(database == default_database and valid_tables and r not in valid_tables and r not in _replaced_with)
