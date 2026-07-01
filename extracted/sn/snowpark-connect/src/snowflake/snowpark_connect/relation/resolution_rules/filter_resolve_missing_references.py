#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""ResolveMissingReferencesInFilter resolution rule.

Mirrors Spark's ResolveMissingReferences analyzer rule for the plan shape:
    select(...).distinct().where(<dropped cols>)

A plain select keeps dropped columns physically reachable via the parent
column_map, so the normal filter path already handles
    select(...).where(<dropped cols>)
But distinct() physically deduplicates away non-selected columns, so the
filter condition can no longer reach them.

Strategy: augment the descendant projection with the missing attributes,
re-apply distinct on the original keys, filter where the columns are visible,
then project back to the original output columns.
"""

from __future__ import annotations

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)

# ---------------------------------------------------------------------------
# Proto-tree helpers (no Snowflake connection required)
# ---------------------------------------------------------------------------


def iter_unresolved_attributes(
    message: expressions_proto.Expression,
):
    """Yield every unresolved_attribute leaf in an expression proto tree."""
    if (
        isinstance(message, expressions_proto.Expression)
        and message.WhichOneof("expr_type") == "unresolved_attribute"
    ):
        yield message
    for field, value in message.ListFields():
        if field.type != field.TYPE_MESSAGE:
            continue
        values = value if field.label == field.LABEL_REPEATED else [value]
        for item in values:
            yield from iter_unresolved_attributes(item)


def is_distinct_over_project(filter_input: relation_proto.Relation) -> bool:
    """True when filter_input is a Deduplicate directly over a Project."""
    return (
        filter_input.WhichOneof("rel_type") == "deduplicate"
        and filter_input.deduplicate.input.WhichOneof("rel_type") == "project"
    )


def collect_missing_filter_attributes(
    condition: expressions_proto.Expression,
    input_container: DataFrameContainer,
) -> list[expressions_proto.Expression]:
    """Return condition references absent from input_container.column_map.

    Plan-qualified references (those carrying a plan_id) are unsafe to
    re-introduce here — they resolve against a specific descendant plan.
    When any such reference is found we return [] so the whole condition
    falls back to the normal path.
    """
    normalize = (lambda s: s) if global_config.spark_sql_caseSensitive else str.lower
    available = {normalize(c.spark_name) for c in input_container.column_map.columns}

    missing: dict[str, expressions_proto.Expression] = {}
    for attr in iter_unresolved_attributes(condition):
        unresolved = attr.unresolved_attribute
        name_parts = split_fully_qualified_spark_name(unresolved.unparsed_identifier)
        if any(normalize(part) in available for part in name_parts):
            continue
        if unresolved.HasField("plan_id"):
            return []
        missing.setdefault(unresolved.unparsed_identifier, attr)
    return list(missing.values())


def _apply_deduplicate_for_missing_refs(
    dedup: relation_proto.Deduplicate,
    augmented_container: DataFrameContainer,
    original_snowpark_cols: list[str],
) -> DataFrameContainer:
    """Re-apply distinct/dropDuplicates over the augmented projection.

    Keys stay the original output columns (mirroring Spark, where Deduplicate
    keys are unchanged when missing attributes are pushed into its child), so
    re-introduced columns do not affect distinctness.
    """
    if dedup.HasField("all_columns_as_keys") and dedup.all_columns_as_keys:
        keys = original_snowpark_cols
    else:
        keys = augmented_container.column_map.get_snowpark_column_names_from_spark_column_names(
            list(dedup.column_names)
        )
    deduped = augmented_container.dataframe.drop_duplicates(*keys)
    return DataFrameContainer(
        deduped,
        augmented_container.column_map,
        augmented_container.table_name,
        augmented_container.alias,
        cached_schema_getter=lambda: augmented_container.dataframe.schema,
    )


# ---------------------------------------------------------------------------
# Rule
# ---------------------------------------------------------------------------


class _ResolveMissingReferencesInFilter:
    name = "ResolveMissingReferencesInFilter"
    rel_type = "filter"

    def applies_to(self, rel: relation_proto.Relation) -> bool:
        return is_distinct_over_project(rel.filter.input)

    def apply(self, rel: relation_proto.Relation) -> DataFrameContainer | None:
        from snowflake.snowpark_connect.expression.map_expression import (
            map_single_column_expression,
        )
        from snowflake.snowpark_connect.expression.typer import ExpressionTyper
        from snowflake.snowpark_connect.relation.map_column_ops import map_project
        from snowflake.snowpark_connect.relation.map_relation import map_relation

        input_container = map_relation(rel.filter.input)

        missing_attrs = collect_missing_filter_attributes(
            rel.filter.condition, input_container
        )
        if not missing_attrs:
            return None

        dedup = rel.filter.input.deduplicate
        project_rel = dedup.input

        synth_project = relation_proto.Relation()
        synth_project.CopyFrom(project_rel)
        synth_project.project.expressions.extend(missing_attrs)
        augmented_container = map_project(synth_project)

        original_snowpark_cols = input_container.column_map.get_snowpark_columns()
        working_container = _apply_deduplicate_for_missing_refs(
            dedup, augmented_container, original_snowpark_cols
        )

        typer = ExpressionTyper(working_container.dataframe)
        _, condition = map_single_column_expression(
            rel.filter.condition, working_container.column_map, typer
        )
        result = working_container.dataframe.filter(condition.col).select(
            *original_snowpark_cols
        )

        input_df = input_container.dataframe
        return DataFrameContainer(
            result,
            input_container.column_map,
            input_container.table_name,
            input_container.alias,
            cached_schema_getter=lambda: input_df.schema,
        )


resolve_missing_references_in_filter = _ResolveMissingReferencesInFilter()
