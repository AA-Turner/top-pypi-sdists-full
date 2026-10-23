#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Opt-in plan breaks in front of long chains of window projections.

A pipeline that adds window columns one ``withColumn`` at a time compiles to one
query with one nested SELECT per window stage. When that query is deep, or when
its base carries large expressions (big CASE chains, regex extraction), the
Snowflake compiler can spend minutes on it or fail with incident 370001
(SNOW-4285855). Large query breakdown does not help such plans: their complexity
score is small (a few thousand) and grows along a single chain, so at most one
cut is possible at any bounds.

With ``snowpark.connect.window.materializeChainDepth`` or
``snowpark.connect.window.materializeInputComplexity`` set, a projection that
adds window functions first materializes its input into a temporary table when
the input is already deep or heavy. This is the automatic form of the manual
``df = df.cache(); df.count()`` plan break. It only happens while an
``ExecutePlan`` maps a root relation or a write: AnalyzePlan (schema, columns)
never materializes, and the tables are dropped when that ExecutePlan ends.
Inside an open transaction it never materializes either: creating the temporary
table is DDL, which would commit the user's transaction.
"""

import re
from typing import Any

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.message import Message

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.query_plan_analysis_utils import (
    PlanNodeCategory,
    get_complexity_score,
)
from snowflake.snowpark._internal.compiler.utils import is_active_transaction
from snowflake.snowpark_connect.config import (
    get_window_materialize_chain_depth,
    get_window_materialize_input_complexity,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.context import (
    add_request_window_chain_table,
    clean_request_window_chain_tables,
    get_request_window_chain_tables,
    is_analyze_plan_request,
    is_window_chain_materialization_allowed,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_OVER_CLAUSE = re.compile(r"\bover\s*\(", re.IGNORECASE)


def is_window_chain_materialization_enabled() -> bool:
    return (
        get_window_materialize_chain_depth() > 0
        or get_window_materialize_input_complexity() > 0
    )


def expression_has_window(message: Message) -> bool:
    """True when a Spark Connect expression contains a window function.

    ``expr("... OVER (...)")`` strings count too, by a textual check.
    """
    if isinstance(message, expressions_proto.Expression):
        kind = message.WhichOneof("expr_type")
        if kind == "window":
            return True
        if kind == "expression_string":
            return bool(_OVER_CLAUSE.search(message.expression_string.expression))
    for field, value in message.ListFields():
        if field.type != FieldDescriptor.TYPE_MESSAGE:
            continue
        if isinstance(value, Message):
            items = (value,)
        elif field.message_type.GetOptions().map_entry:
            items = value.values()
        else:
            items = value
        if any(
            isinstance(item, Message) and expression_has_window(item) for item in items
        ):
            return True
    return False


def _window_count(node: Any) -> int:
    return node.cumulative_node_complexity.get(PlanNodeCategory.WINDOW, 0)


def unmaterialized_window_depth(df: snowpark.DataFrame) -> int:
    """Number of nested plan nodes that compute a window function.

    The walk stops at tables (a materialized cache or LQB partition is a leaf),
    so only window stages that would be compiled into the same query count.
    """
    root = getattr(df, "_select_statement", None) or df._plan
    depths: dict[int, int] = {}

    def depth(node: Any) -> int:
        key = id(node)
        if key in depths:
            return depths[key]
        depths[key] = 0
        children = list(getattr(node, "children_plan_nodes", None) or [])
        own_windows = _window_count(node) - sum(_window_count(c) for c in children)
        result = (1 if own_windows > 0 else 0) + max(
            (depth(child) for child in children), default=0
        )
        depths[key] = result
        return result

    return depth(root)


def maybe_materialize_window_input(
    container: DataFrameContainer,
    expressions: list[expressions_proto.Expression],
) -> DataFrameContainer:
    """Materialize ``container`` before a projection that adds window functions.

    Returns ``container`` unchanged unless one of the window materialization
    configs is set, this is an ExecutePlan mapping a root or a write, the
    projection has a window function, and the input has at least
    ``materializeChainDepth`` unmaterialized window stages or a complexity score
    of at least ``materializeInputComplexity``. Inside an open transaction it is
    also returned unchanged, as large query breakdown does: ``cache_result()``
    runs DDL, which would commit the transaction.
    """
    chain_depth = get_window_materialize_chain_depth()
    input_complexity = get_window_materialize_input_complexity()
    if chain_depth <= 0 and input_complexity <= 0:
        return container
    if is_analyze_plan_request() or not is_window_chain_materialization_allowed():
        return container
    if not container.can_be_materialized:
        return container
    if not any(expression_has_window(exp) for exp in expressions):
        return container

    df = container.dataframe
    depth = unmaterialized_window_depth(df)
    if chain_depth > 0 and depth >= chain_depth:
        reason = f"window depth {depth} >= {chain_depth}"
    else:
        score = get_complexity_score(df._plan) if input_complexity > 0 else 0
        if input_complexity <= 0 or score < input_complexity:
            return container
        reason = f"complexity {score} >= {input_complexity}"

    if is_active_transaction(df.session):
        logger.info(
            f"Skipped window input materialization ({reason}): open transaction"
        )
        return container

    schema = df.schema
    table = df.cache_result()
    add_request_window_chain_table(table.table_name)
    logger.info(f"Materialized window input into {table.table_name} ({reason})")
    return container.with_materialized_dataframe(table, schema)


def drop_window_chain_tables(session: snowpark.Session) -> None:
    """Drop the tables this request materialized. Failures are logged only."""
    tables = get_request_window_chain_tables()
    if not tables:
        return
    from snowflake.snowpark_connect.utils.internal_query import (
        collect_without_telemetry,
    )

    for name in tables:
        try:
            collect_without_telemetry(session.sql(f"DROP TABLE IF EXISTS {name}"))
        except Exception as e:
            logger.warning(f"Failed to drop window materialization table {name}: {e}")
    clean_request_window_chain_tables()
