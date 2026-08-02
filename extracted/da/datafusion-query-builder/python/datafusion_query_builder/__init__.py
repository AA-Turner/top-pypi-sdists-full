"""Programmatic builder for DataFusion SQL — the dialect DataFusion parses.

A thin Python façade over a Rust core (`sqlparser`-backed). Build expressions and queries with a
datafusion-python / Polars-style API; render to SQL text with ``.to_sql()``.

    from datafusion_query_builder import col, lit, table
    from datafusion_query_builder import functions as f

    q = (
        table("records")
        .filter((col("env") == "prod") & (col("kind") == "span"))
        .select(
            f.time_bucket("60 seconds", col("start_timestamp")).alias("time"),
            f.approx_distinct(col("trace_id")).alias("request_count"),
        )
        .group_by(col("time"))
        .order_by(col("time").asc())
        .limit(200)
    )
    sql = q.to_sql()
"""

from ._native import (
    Expr,
    Query,
    QueryBuilderError,
    SortExpr,
    UnparsableSqlError,
    and_,
    col,
    functions,
    lit,
    not_,
    or_,
    param,
    query,
    raw,
    table,
    when,
)

# `f` is the conventional short alias for the functions namespace (matches datafusion-python).
f = functions

__all__ = [
    'Expr',
    'Query',
    'QueryBuilderError',
    'SortExpr',
    'UnparsableSqlError',
    'and_',
    'col',
    'f',
    'functions',
    'lit',
    'not_',
    'or_',
    'param',
    'query',
    'raw',
    'table',
    'when',
]
