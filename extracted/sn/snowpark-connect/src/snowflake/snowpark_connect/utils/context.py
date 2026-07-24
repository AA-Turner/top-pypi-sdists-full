#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os
import re
import threading
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Iterator, Mapping, Optional

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.type_support import (
    set_integral_types_for_client_default,
)
from snowflake.snowpark_connect.typed_column import TypedColumn

# TODO: remove session id from context when we host SAS in Snowflake server

_spark_session_id = ContextVar[str]("_spark_session_id")
_plan_id_map = ContextVar[Mapping[int, DataFrameContainer]]("_plan_id_map")
_alias_map = ContextVar[Mapping[str, DataFrameContainer | None]]("_alias_map")
_spark_version = ContextVar[str]("_spark_version")
_is_aggregate_function = ContextVar(
    "_is_aggregate_function", default=("default", False)
)
_grouping_by_scala_udf_key = ContextVar[bool](
    "_grouping_by_scala_udf_key", default=False
)
_is_evaluating_sql = ContextVar[bool]("_is_evaluating_sql", default=False)
_is_evaluating_join_condition = ContextVar(
    "_is_evaluating_join_condition", default=("default", False, [], [])
)
_is_processing_order_by = ContextVar[bool]("_is_processing_order_by", default=False)
_is_processing_aliased_relation = ContextVar[bool](
    "_is_processing_aliased_relation", default=False
)
_is_analyze_plan_request = ContextVar[bool]("_is_analyze_plan_request", default=False)
_execute_root_plan_id = ContextVar[int | None]("_execute_root_plan_id", default=None)
# Tracks the plan_id of the relation node currently being translated. Updated
# by map_relation for every node so that error_plan_id in request_summary
# and null-type-fallback telemetry can point to the exact plan node.
_current_plan_id = ContextVar[int | None]("_current_plan_id", default=None)

_sql_aggregate_function_count = ContextVar[int](
    "_contains_aggregate_function", default=0
)

# We have to generate our own plan IDs that are different from Spark's.
# Spark plan IDs start at 0, so pick a "big enough" number to avoid overlaps.
_STARTING_SQL_PLAN_ID = 0x80000000

_next_sql_plan_id = ContextVar[int]("_next_sql_plan_id")


@dataclass
class _SqlScopeFrame:
    """One lexical scope in the SQL plan-name resolution stack.

    - ``names`` maps a FROM-clause relation qualifier to its plan_id (or
      AMBIGUOUS_PLAN_ID) for this scope only.
    - ``reg_db`` tracks the database/schema active when each name was
      registered, used for same-table collision detection: an unqualified "t1"
      registered in context "mydb1" has identity "mydb1.t1", which equals the
      explicitly qualified "mydb1.t1" -> same table -> not ambiguous.
    - ``is_boundary`` is True when entering this scope crossed a subquery
      correlation boundary (push_sql_scope(is_boundary=True)).  It is False for
      same-query-level scopes (push_sql_scope), across which outer names remain
      fully visible.  Correlated resolution may cross at most one boundary,
      matching Spark's single-level correlation.
    """

    names: dict[str, int] = field(default_factory=dict)
    reg_db: dict[str, str | None] = field(default_factory=dict)
    is_boundary: bool = False


# Stack of lexical scopes for spark.sql() plan-name resolution.  The bottom of
# the stack is the outermost query; the top is the current scope.  Registration
# targets the top frame (isolating each subquery namespace); resolution walks
# the stack downward (making outer names visible), crossing at most one subquery
# boundary.  There is always at least one base frame (seeded in
# clear_context_data).
_sql_plan_scope_stack: ContextVar[list[_SqlScopeFrame]] = ContextVar(
    "_sql_plan_scope_stack"
)

# Sentinel plan_id indicating that a qualifier maps to more than one relation.
# When get_sql_plan() returns this value the caller must raise AMBIGUOUS_REFERENCE.
AMBIGUOUS_PLAN_ID = -1
_sql_named_args = ContextVar[dict[str, expressions_proto.Expression]]("_sql_named_args")
_sql_pos_args = ContextVar[dict[int, expressions_proto.Expression]]("_sql_pos_args")

# Used to store the df before the last projection operation
_df_before_projection = ContextVar[DataFrameContainer | None](
    "_df_before_projection", default=None
)
_outer_dataframes = ContextVar[list[DataFrameContainer]]("_parent_dataframes")

_spark_client_type_regex = re.compile(r"spark/(?P<spark_version>\d+\.\d+\.\d+)")
_is_python_client = ContextVar[bool]("_is_python_client", default=True)
_current_operation = ContextVar[str]("_current_operation", default="default")
_resolving_fun_args = ContextVar[bool]("_resolving_fun_args", default=False)
_resolving_lambda_fun = ContextVar[bool]("_resolving_lambdas", default=False)
_current_lambda_params = ContextVar[list[str]]("_current_lambda_params", default=[])

_is_window_enabled = ContextVar[bool]("_is_window_enabled", default=False)
_is_in_udtf_context = ContextVar[bool]("_is_in_udtf_context", default=False)
_accessing_temp_object = ContextVar[bool]("_accessing_temp_object", default=False)
_should_skip_file_read_cache_result = ContextVar[bool](
    "_should_skip_file_read_cache_result", default=False
)

# Thread-safe lock for JPype JClass creation to prevent access violations
_jpype_jclass_lock = threading.Lock()


@contextmanager
def get_jpype_jclass_lock() -> Iterator[None]:
    """
    Context manager that acquires the JPype JClass lock on Windows platforms.
    On non-Windows (os.name != 'nt'), it yields without acquiring the lock.
    """
    if os.name == "nt":
        with _jpype_jclass_lock:
            yield
    else:
        yield


# Lateral Column Alias helpers
# We keep a thread-local mapping from alias name -> TypedColumn that is
# populated incrementally while the projection list is being processed.
# The map is cleared at the beginning of every `map_project` call and read
# by `map_unresolved_attribute` as a last-resort resolver.

_lca_alias_map: ContextVar[dict[str, TypedColumn]] = ContextVar(
    "_lca_alias_map",
    default={},
)

_view_process_context = ContextVar("_view_process_context", default=[])


@contextmanager
def push_processed_view(name: str):
    _view_process_context.set(_view_process_context.get() + [name])
    yield
    _view_process_context.set(_view_process_context.get()[:-1])


def get_processed_views() -> list[str]:
    return _view_process_context.get()


def register_processed_view(name: str) -> None:
    context = _view_process_context.get()
    context.append(name)
    _view_process_context.set(context)


_request_external_tables = ContextVar[list[str]]("_used_external_tables", default=[])


def register_request_external_table(name: str) -> None:
    _request_external_tables.set(_request_external_tables.get() + [name])


def get_request_external_tables() -> list[str]:
    return _request_external_tables.get()


def clean_request_external_tables() -> None:
    _request_external_tables.set([])


# Context variable to track current grouping columns for grouping_id() function
_current_grouping_columns: ContextVar[list[str]] = ContextVar(
    "_current_grouping_columns",
    default=[],
)

# Context variable to capture all original_attr_name values during subquery resolution
# This is a stack of lists to handle nested subqueries correctly
_captured_attribute_names: ContextVar[list[list[str]]] = ContextVar(
    "_captured_attribute_names",
    default=[],
)

# Context variable to track if we're resolving a subquery expression
_is_resolving_subquery_exp: ContextVar[bool] = ContextVar(
    "_is_resolving_subquery_exp",
    default=False,
)


def clear_lca_alias_map() -> None:
    _lca_alias_map.set({})


def _normalize(name: str) -> str:
    from snowflake.snowpark_connect.config import global_config

    return name if global_config.spark_sql_caseSensitive else name.lower()


def register_lca_alias(name: str, typed_col: TypedColumn) -> None:
    alias_map = _lca_alias_map.get()
    alias_map[_normalize(name)] = typed_col
    _lca_alias_map.set(alias_map)


def resolve_lca_alias(name: str) -> Optional[TypedColumn]:
    return _lca_alias_map.get().get(_normalize(name))


def set_current_grouping_columns(columns: list[str]) -> None:
    """Set the current grouping columns for grouping_id() function.

    TODO: This should use a push/pop mechanism to properly handle nested queries
    with GROUP BY. Currently, nested queries may interfere with parent queries.
    Also need to add clearing in clear_context_data() to prevent cross-request contamination.
    """
    _current_grouping_columns.set(columns)


def get_current_grouping_columns() -> list[str]:
    """Get the current grouping columns for grouping_id() function."""
    return _current_grouping_columns.get()


def capture_attribute_name(attr_name: str) -> None:
    """Capture an original_attr_name during expression resolution."""
    stack = _captured_attribute_names.get()
    if stack:
        stack[-1].append(attr_name)
        _captured_attribute_names.set(stack)


def get_captured_attribute_names() -> list[str]:
    """Get the list of captured attribute names from the current top of the stack."""
    stack = _captured_attribute_names.get()
    return stack[-1] if stack else []


def is_resolving_subquery_exp() -> bool:
    """
    Returns True if currently resolving a subquery expression.
    """
    return _is_resolving_subquery_exp.get()


@contextmanager
def resolving_subquery_exp():
    """
    Context manager that captures all original_attr_name values during subquery expression resolution.
    Sets a flag to indicate we're in a subquery context and pushes a new list onto the stack.
    When the context exits, pops the list from the stack.
    """
    stack = _captured_attribute_names.get()
    stack.append([])
    _captured_attribute_names.set(stack)
    token = _is_resolving_subquery_exp.set(True)
    try:
        yield
    finally:
        stack = _captured_attribute_names.get()
        if stack:
            stack.pop()
            _captured_attribute_names.set(stack)
        _is_resolving_subquery_exp.reset(token)


def set_spark_session_id(value: str) -> None:
    """Set the Spark session ID for the current context"""
    _spark_session_id.set(value)


def get_spark_session_id() -> str:
    """Get the Spark session ID for the current context."""
    return _spark_session_id.get(None)


def set_plan_id_map(plan_id: int, container: DataFrameContainer) -> None:
    """Set the plan id map for the current context."""
    _plan_id_map.get()[plan_id] = container


def get_plan_id_map(plan_id: int) -> DataFrameContainer | None:
    """Get the plan id map for the current context."""
    return _plan_id_map.get().get(plan_id)


def gen_sql_plan_id() -> int:
    next = _next_sql_plan_id.get()
    _next_sql_plan_id.set(next + 1)
    return next


def get_spark_version() -> str:
    """
    Get the spark version for the current context, as sent by the client in `client_type`.
    """
    return _spark_version.get()


def get_is_python_client() -> bool:
    """
    Returns True if the current request comes from a Python client.
    """
    return _is_python_client.get()


def set_spark_version(client_type: str) -> None:
    """
    Set the client spark version for the current context.
    Takes a single `client_type: str` argument in format as sent by pyspark, e.g.
    "_SPARK_CONNECT_PYTHON spark/3.5.3 os/darwin python/3.11.11" and extracts the spark version - 3.5.3 in this case.
    """
    match = _spark_client_type_regex.search(client_type)
    version = match.group("spark_version") if match else ""
    _spark_version.set(version)

    # enable integral types (only if config is "client_default")

    is_python_client = "_SPARK_CONNECT_PYTHON" in client_type
    _is_python_client.set(is_python_client)
    set_integral_types_for_client_default(is_python_client)


def get_is_aggregate_function() -> tuple[str, bool]:
    """
    Gets the value of _is_aggregate_function for the current context, defaults to False.
    """
    return _is_aggregate_function.get()


def set_is_aggregate_function(is_agg: tuple[str, bool]) -> None:
    """
    Sets the value of _is_aggregate_function for the current context.
    """
    _is_aggregate_function.set(is_agg)


def get_is_evaluating_sql() -> bool:
    """
    Gets the value of _is_evaluating_sql for the current context, defaults to False.
    """
    return _is_evaluating_sql.get()


@contextmanager
def push_evaluating_sql_scope():
    """
    Context manager that sets a flag indicating if a sql statement is being resolved.
    """
    prev = _is_evaluating_sql.get()
    try:
        _is_evaluating_sql.set(True)
        yield
    finally:
        _is_evaluating_sql.set(prev)


def get_grouping_by_scala_udf_key() -> bool:
    """
    Gets the value of _grouping_by_scala_udf_key for the current context, defaults to False.
    """
    return _grouping_by_scala_udf_key.get()


@contextmanager
def grouping_by_scala_udf_key(value: bool):
    """
    Context manager that conditionally sets a flag indicating grouping by scala_udf key.
    Only activates the flag when value=True, otherwise leaves the current context unchanged
    """
    prev = _grouping_by_scala_udf_key.get()
    try:
        if value:
            _grouping_by_scala_udf_key.set(True)
        yield
    finally:
        _grouping_by_scala_udf_key.set(prev)


def get_is_processing_order_by() -> bool:
    """
    Gets the value of _is_processing_order_by for the current context, defaults to False.
    """
    return _is_processing_order_by.get()


@contextmanager
def push_processing_order_by_scope():
    """
    Context manager that sets a flag indicating if ORDER BY expressions are being evaluated.
    This enables optimizations like reusing already-computed UDF columns.
    """
    prev = _is_processing_order_by.get()
    try:
        _is_processing_order_by.set(True)
        yield
    finally:
        _is_processing_order_by.set(prev)


def get_is_processing_aliased_relation() -> bool:
    return _is_processing_aliased_relation.get()


@contextmanager
def push_processing_aliased_relation_scope(process_aliased_relation: bool):
    """
    Context manager that sets a flag indicating if an aliased relation is being resolved.
    """
    prev = _is_processing_aliased_relation.get()
    try:
        _is_processing_aliased_relation.set(process_aliased_relation)
        yield
    finally:
        _is_processing_aliased_relation.set(prev)


def get_is_evaluating_join_condition() -> tuple[str, bool, list, list]:
    """
    Gets the value of _is_evaluating_join_condition for the current context, defaults to False.
    """
    return _is_evaluating_join_condition.get()


@contextmanager
def push_evaluating_join_condition(join_type, left_keys, right_keys):
    """
    Context manager that sets a flag indicating if a join statement is being resolved.
    """
    prev = _is_evaluating_join_condition.get()
    try:
        _is_evaluating_join_condition.set((join_type, True, left_keys, right_keys))
        yield
    finally:
        _is_evaluating_join_condition.set(prev)


@contextmanager
def push_sql_scope(is_boundary: bool = False):
    """
    Creates a new plan-name scope frame on the SQL scope stack.

    Registration targets the new top frame, so each scope's relation names are
    isolated for collision detection.  Resolution (get_sql_plan) walks the stack
    downward, so outer names remain visible.

    ``is_boundary`` selects the scope kind:

    - ``False`` (default) -- a same-query-level scope, e.g. in
      `SELECT x, (SELECT 1 AS x)` the two `x`s are different variables.  Outer
      plan names stay fully visible via get_sql_plan()'s downward walk.

    - ``True`` -- a subquery correlation boundary for SubqueryAlias complex
      children and expression-level subqueries (EXISTS, ScalarSubquery,
      InSubquery, FunctionTableSubquery).  Inner table registrations cannot
      collide with identically-named outer relations, get_sql_plan() crosses at
      most one boundary (matching Spark's single-level correlation), and deeper
      frames remain available to is_out_of_scope_correlated_qualifier() so it
      can distinguish a grandparent reference (which Spark rejects) from a
      genuinely fully-qualified name.
    """
    stack = _sql_plan_scope_stack.get()
    stack_token = _sql_plan_scope_stack.set(
        stack + [_SqlScopeFrame(is_boundary=is_boundary)]
    )
    agg_token = _sql_aggregate_function_count.set(0)
    try:
        yield
    finally:
        _sql_aggregate_function_count.reset(agg_token)
        _sql_plan_scope_stack.reset(stack_token)


@contextmanager
def push_operation_scope(operation: str):
    """
    Context manager that sets the current operation scope for column name resolution.
    Example:
    with push_operation_scope('filter'):
        df.filter(col('historical_name') > 0)  # Historical names allowed in filter
    """
    token = _current_operation.set(operation)
    try:
        yield
    finally:
        _current_operation.reset(token)


@contextmanager
def resolving_lambda_function(param_names: list[str] = None):
    """
    Context manager that sets a flag indicating lambda function is being resolved.
    Also tracks the lambda parameter names for validation.
    """
    prev = _resolving_lambda_fun.get()
    prev_params = _current_lambda_params.get()
    try:
        _resolving_lambda_fun.set(True)
        if param_names is not None:
            _current_lambda_params.set(param_names)
        yield
    finally:
        _resolving_lambda_fun.set(prev)
        _current_lambda_params.set(prev_params)


def is_lambda_being_resolved() -> bool:
    """
    Returns True if lambda function is being resolved.
    """
    return _resolving_lambda_fun.get()


def get_current_lambda_params() -> list[str]:
    """
    Returns the current lambda parameter names.
    """
    return _current_lambda_params.get()


@contextmanager
def resolving_fun_args():
    """
    Context manager that sets a flag indicating function arguments are being resolved.
    """
    prev = _resolving_fun_args.get()
    try:
        _resolving_fun_args.set(True)
        yield
    finally:
        _resolving_fun_args.set(prev)


@contextmanager
def not_resolving_fun_args():
    """
    Context manager that sets a flag indicating function arguments are *not* being resolved.
    """
    prev = _resolving_fun_args.get()
    try:
        _resolving_fun_args.set(False)
        yield
    finally:
        _resolving_fun_args.set(prev)


def is_function_argument_being_resolved() -> bool:
    """
    Returns True if function arguments are being resolved.
    """
    return _resolving_fun_args.get()


def get_current_operation_scope() -> str:
    """
    Returns the current operation scope for column name resolution.
    """
    return _current_operation.get()


def _get_current_registration_db() -> str | None:
    """Return the current Spark/SQL database for table identity computation.

    Reads the Snowflake session's current schema, which is the authoritative
    source of truth: every Spark `USE <db>` command is translated to
    `session.sql("USE SCHEMA <db>")`, so the session schema always reflects the
    most recent USE across requests.
    """
    try:
        from snowflake.snowpark import Session

        session = Session.get_active_session()
        if session is not None:
            schema = session.get_current_schema()
            if schema:
                return _normalize(schema.strip('"'))
    except Exception:
        pass
    return None


def _table_identity(name: str, reg_db: str | None) -> str:
    """Canonical table identity used for same-table collision detection.

    For a 1-part unqualified name "t1" registered with db="mydb1" the identity
    is "mydb1.t1".  For an already-qualified name "mydb1.t1" the identity is
    just the normalised name itself.  This lets the collision check distinguish
    "same table, different plan occurrence" from "two tables with same short name".
    """
    parts = name.split(".")
    if len(parts) == 1 and reg_db:
        return f"{reg_db}.{name}"
    return name


def set_sql_plan_name(name: str, plan_id: int) -> None:
    """Register a FROM-clause relation `name` → `plan_id` for qualifier lookup.

    Collisions are resolved into AMBIGUOUS_PLAN_ID using table identity (db +
    table), so that a self-join of the same physical table is distinguished from
    two genuinely different tables that merely share a short name.  See
    _table_identity for how unqualified names are expanded with the current db.
    """
    plan_map = _sql_plan_scope_stack.get()[-1].names
    reg_db_map = _sql_plan_scope_stack.get()[-1].reg_db
    name = _normalize(name)
    current_db = _get_current_registration_db()
    new_identity = _table_identity(name, current_db)

    def same_table_at(key: str) -> bool:
        # Does the relation currently registered under `key` denote the same
        # physical table as the one we are registering now?
        return _table_identity(key, reg_db_map.get(key)) == new_identity

    # --- Register the full name --------------------------------------------
    existing = plan_map.get(name)
    if existing is None:
        plan_map[name] = plan_id
        reg_db_map[name] = current_db
    elif existing not in (plan_id, AMBIGUOUS_PLAN_ID):
        if same_table_at(name):
            # Same table re-registered at the same key (e.g. a copied scope
            # for a CTE/subquery shadowing the outer relation): keep the
            # latest plan_id rather than flagging ambiguity.
            plan_map[name] = plan_id
            reg_db_map[name] = current_db
        else:
            plan_map[name] = AMBIGUOUS_PLAN_ID

    # --- Register the short last-part of a multi-part name -----------------
    # e.g. "mydb1.t1" also registers "t1" so an unqualified SELECT qualifier
    # can find this relation.
    parts = name.split(".")
    if len(parts) <= 1:
        return
    short = parts[-1]
    # The short alias inherits the db embedded in the qualified name itself
    # ("mydb1" for "mydb1.t1"), independent of the active session schema.
    alias_db = parts[-2]
    existing_short = plan_map.get(short)
    if existing_short is None:
        plan_map[short] = plan_id
        reg_db_map[short] = alias_db
    elif existing_short != plan_id:
        if same_table_at(short):
            # Self-join: `FROM t1, mydb1.t1` after `USE mydb1` — both sides are
            # the same physical table, so EVERY qualifier (short or fully
            # qualified) is ambiguous.
            plan_map[short] = AMBIGUOUS_PLAN_ID
            plan_map[name] = AMBIGUOUS_PLAN_ID
        else:
            # Different tables sharing a short name (e.g. `mydb2.t1` vs
            # `mydb1.t1`): only the short qualifier is ambiguous; the fully
            # qualified name still resolves to its unique source.
            plan_map[short] = AMBIGUOUS_PLAN_ID


def get_sql_plan(name: str) -> int | None:
    """Resolve a FROM-clause qualifier to its plan_id across the scope stack.

    Searches from the current (top) scope downward so that outer table
    qualifiers -- e.g. `bonus.emp_name` referenced inside an EXISTS or scalar
    subquery -- still resolve, without the outer scope's names polluting inner
    collision detection.  Same-query-level frames (push_sql_scope) are traversed
    freely; correlated resolution crosses at most ONE subquery boundary, matching
    Spark, which correlates a subquery to its single enclosing query rather than
    arbitrary grandparents.
    """
    normalized = _normalize(name)
    boundaries_crossed = 0
    for frame in reversed(_sql_plan_scope_stack.get()):
        result = frame.names.get(normalized)
        if result is not None:
            return result
        if frame.is_boundary:
            boundaries_crossed += 1
            if boundaries_crossed >= 2:
                break
    return None


def is_out_of_scope_correlated_qualifier(name: str) -> bool:
    """Return True if `name` is a relation alias visible only beyond the single
    correlation level Spark allows -- i.e. in a grandparent scope reachable only
    after crossing a second subquery boundary.

    Such a reference is an out-of-scope correlated reference.  Spark rejects it
    with UNRESOLVED_COLUMN for a no-FROM scalar subquery (e.g. the inner
    `(SELECT d.d_budget)` of a doubly-nested correlated subquery), whereas
    Snowflake would happily resolve the correlation and return a result.  The
    caller uses this to raise a Spark-compatible AnalysisException instead of
    silently diverging.

    The check is scoped to the no-FROM case (empty current scope) so that
    references resolvable within the current or immediate-parent scope -- and
    genuinely fully-qualified names that appear in no scope at all -- are left
    untouched.
    """
    normalized = _normalize(name)
    stack = _sql_plan_scope_stack.get()
    if stack[-1].names:
        # The current subquery has its own FROM-clause relations; defer to the
        # normal resolution / fully-qualified passthrough behaviour.
        return False
    boundaries_crossed = 0
    for frame in reversed(stack):
        if frame.is_boundary:
            boundaries_crossed += 1
        if boundaries_crossed >= 2 and normalized in frame.names:
            return True
    return False


def add_sql_aggregate_function() -> None:
    _sql_aggregate_function_count.set(_sql_aggregate_function_count.get() + 1)


def get_sql_aggregate_function_count() -> int:
    return _sql_aggregate_function_count.get()


def set_sql_args(
    named: dict[str, expressions_proto.Expression],
    pos: dict[int, expressions_proto.Expression],
) -> None:
    _sql_named_args.set(named)
    _sql_pos_args.set(pos)


def get_sql_named_arg(name: str) -> expressions_proto.Expression:
    return _sql_named_args.get()[name]


def get_sql_pos_arg(pos: int) -> expressions_proto.Expression:
    return _sql_pos_args.get()[pos]


def set_df_before_projection(df: DataFrameContainer | None) -> None:
    """
    Sets the current DataFrame container in the context.
    This is used to track the DataFrame container in the current context.
    """
    _df_before_projection.set(df)


def get_df_before_projection() -> DataFrameContainer | None:
    """
    Returns the current DataFrame container if set, otherwise None.
    This is used to track the DataFrame container in the current context.
    """
    return _df_before_projection.get()


@contextmanager
def push_outer_dataframe(df: DataFrameContainer):
    _outer_dataframes.get().append(df)
    yield
    _outer_dataframes.get().pop()


def get_outer_dataframes() -> list[DataFrameContainer]:
    return _outer_dataframes.get()


def is_analyze_plan_request() -> bool:
    return _is_analyze_plan_request.get()


def set_is_analyze_plan_request(value: bool) -> None:
    _is_analyze_plan_request.set(value)


def get_execute_root_plan_id() -> int | None:
    return _execute_root_plan_id.get()


def set_execute_root_plan_id(value: int | None) -> None:
    _execute_root_plan_id.set(value)


def get_current_plan_id() -> int | None:
    return _current_plan_id.get()


@contextmanager
def active_plan_id(plan_id: int | None) -> Iterator[None]:
    """Context manager that tracks the active plan_id for the duration of a
    map_relation call, handling both normal returns and exceptions correctly.

    On normal return: the previous plan_id is restored via ContextVar.reset so
    that the *caller's* plan_id is active again (fixes the "stale child id after
    nested call returns" bug).

    On exception: the exception is tagged with `_scos_plan_id` the *first* time
    it passes through this context manager so that report_request_failure can
    report the innermost origin plan node even after the ContextVar is reset.
    """
    if plan_id is None:
        yield
        return
    token = _current_plan_id.set(plan_id)
    try:
        yield
    except Exception as e:
        if not hasattr(e, "_scos_plan_id"):
            e._scos_plan_id = plan_id
        raise
    finally:
        _current_plan_id.reset(token)


def clear_context_data() -> None:
    _spark_session_id.set(None)
    _plan_id_map.set({})
    _alias_map.set({})

    _request_external_tables.set([])
    _view_process_context.set([])
    _next_sql_plan_id.set(_STARTING_SQL_PLAN_ID)
    _sql_plan_scope_stack.set([_SqlScopeFrame()])
    _sql_aggregate_function_count.set(0)
    _sql_named_args.set({})
    _sql_pos_args.set({})
    _is_aggregate_function.set(("default", False))
    _df_before_projection.set(None)
    _outer_dataframes.set([])
    _is_analyze_plan_request.set(False)
    _execute_root_plan_id.set(None)
    _current_plan_id.set(None)
    _should_skip_file_read_cache_result.set(False)

    # Reset CLD ContextVars so state from a previous RPC handled by the same
    # worker thread (sync gRPC server) does not leak into this request.
    # Imported here to avoid an import cycle between context.py and cld_context.py.
    from snowflake.snowpark_connect.utils.cld_context import reset_request_cld_state

    reset_request_cld_state()


@contextmanager
def temporary_window_expression():
    """
    Temporarily sets the 'is_window_enabled' attribute of the given typer to True.

    Yields:
        None: The context manager only yields control; it does not return a value.
    -------

    """
    _is_window_enabled.set(True)
    try:
        yield
    finally:
        _is_window_enabled.set(False)


def is_window_enabled():
    return _is_window_enabled.get()


def get_is_in_udtf_context() -> bool:
    """
    Gets the value of _is_in_udtf_context for the current context, defaults to False.
    """
    return _is_in_udtf_context.get()


@contextmanager
def push_udtf_context():
    """
    Context manager that sets a flag indicating UDTF arguments are being processed.
    """
    token = _is_in_udtf_context.set(True)
    try:
        yield
    finally:
        _is_in_udtf_context.reset(token)


def get_should_skip_file_read_cache_result() -> bool:
    return _should_skip_file_read_cache_result.get()


@contextmanager
def should_skip_file_read_cache_result(active: bool = True):
    """
    Context manager that, when *active*, tells file reading operations to skip ``cache_result()``
    materialization. This flag is used by write operations so that operations ending in a
    ``saveAsTable`` can generate a single CTAS directly from the staged file instead of going through
    a redundant temporary table.
    """
    prev = _should_skip_file_read_cache_result.get()
    try:
        if active:
            _should_skip_file_read_cache_result.set(True)
        yield
    finally:
        _should_skip_file_read_cache_result.set(prev)
