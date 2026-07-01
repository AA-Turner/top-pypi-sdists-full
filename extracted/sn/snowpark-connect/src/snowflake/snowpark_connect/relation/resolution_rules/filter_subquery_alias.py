#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""FilterOverSubqueryAlias resolution rule.

map_subquery_alias does not physically wrap the DataFrame in an alias or
subquery.  For certain plan shapes (e.g. TpcdsQ53) filtering directly on the
result causes a Snowpark SQL compilation error.  Inserting a select("*")
gives Snowpark enough structural separation to compile cleanly.

Using .alias() is intentionally avoided because it triggers extra DESCRIBE
queries.
"""

from __future__ import annotations

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer


class _FilterOverSubqueryAlias:
    name = "FilterOverSubqueryAlias"
    rel_type = "filter"

    def applies_to(self, rel: relation_proto.Relation) -> bool:
        return rel.filter.input.WhichOneof("rel_type") == "subquery_alias"

    def apply(self, rel: relation_proto.Relation) -> DataFrameContainer | None:
        from snowflake.snowpark_connect.expression.map_expression import (
            map_single_column_expression,
        )
        from snowflake.snowpark_connect.expression.typer import ExpressionTyper
        from snowflake.snowpark_connect.relation.map_relation import map_relation

        input_container = map_relation(rel.filter.input)
        input_df = input_container.dataframe

        typer = ExpressionTyper(input_df)
        _, condition = map_single_column_expression(
            rel.filter.condition, input_container.column_map, typer
        )
        result = input_df.select("*").filter(condition.col)
        return DataFrameContainer(
            result,
            input_container.column_map,
            input_container.table_name,
            input_container.alias,
            cached_schema_getter=lambda: input_df.schema,
        )


filter_over_subquery_alias = _FilterOverSubqueryAlias()
