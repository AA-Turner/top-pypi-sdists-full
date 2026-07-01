#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""ResolveSortOverAggregate resolution rule.

Mirrors Spark's ResolveReferences/ResolveAggregateFunctions behavior for ORDER BY
after aggregation: an ORDER BY placed on top of a groupBy().agg() can reference
pre-aggregation columns (e.g. ``ORDER BY year(date)`` when the aggregated output
only exposes the ``year`` alias) or aggregate aliases.

SCOS attaches AggregateMetadata to the aggregated container; when present, sort
expressions are resolved through a HybridColumnMap that can see both the
pre-aggregation input and the aggregated output. Otherwise they resolve against
the input column map directly (the plain ``map_sort`` behavior).

The metadata is only known after resolving the input, so this rule owns all sort
resolution: applies_to is broad (any sort) and apply resolves the input exactly
once, then picks hybrid vs plain resolution. Resolving once is important -- the
plan-id cache copy in map_relation does not carry AggregateMetadata, so a
decline-then-fallback path would resolve the input twice and diverge for ORDER BY
expressions that reuse aggregate outputs (e.g. GROUPING over a ROLLUP/CUBE).
"""

from __future__ import annotations

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark.column import Column
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer


class _ResolveSortOverAggregate:
    name = "ResolveSortOverAggregate"
    rel_type = "sort"

    def applies_to(self, rel: relation_proto.Relation) -> bool:
        # AggregateMetadata is only known after resolving the input (and survives
        # pass-through ops like hint/collect_metrics that return the same
        # container), so we cannot gate on input rel_type alone. This rule owns
        # all sorts; the hybrid-vs-plain decision is made in apply().
        return True

    def apply(self, rel: relation_proto.Relation) -> DataFrameContainer | None:
        from snowflake.snowpark_connect.expression.hybrid_column_map import (
            create_hybrid_column_map_for_order_by,
        )
        from snowflake.snowpark_connect.relation.map_column_ops import (
            build_sorted_container,
            plain_sort,
        )
        from snowflake.snowpark_connect.relation.map_relation import map_relation

        sort = rel.sort
        input_container = map_relation(sort.input)

        aggregate_metadata = getattr(input_container, "_aggregate_metadata", None)
        if aggregate_metadata is None:
            return plain_sort(sort, input_container)

        hybrid_map = create_hybrid_column_map_for_order_by(
            aggregate_metadata=aggregate_metadata,
            aggregated_df=input_container.dataframe,
            aggregated_column_map=input_container.column_map,
        )

        def resolve_child(child: expressions_proto.Expression) -> Column:
            _, typed_column = hybrid_map.resolve_expression(child)
            return typed_column.col

        return build_sorted_container(sort, input_container, resolve_child)


resolve_sort_over_aggregate = _ResolveSortOverAggregate()
