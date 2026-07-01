#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation


def map_alias(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Returns an aliased dataframe in which the columns can now be referenced to using col(<df alias>, <column name>).
    """
    alias: str = rel.subquery_alias.alias
    # we set reuse_parsed_plan=False because we need new expr_id for the attributes (output columns) in aliased snowpark dataframe
    # reuse_parsed_plan will lead to ambiguous column name for operations like joining two dataframes that are aliased from the same dataframe
    input_container = map_relation(rel.subquery_alias.input, reuse_parsed_plan=False)

    # Mirror Spark's `SubqueryAlias.metadataOutput` rule: alias propagates only
    # non-qualified-access-only metadata attributes (with the new qualifier),
    # and propagates them only when the child is a `LeafNode` or another
    # `SubqueryAlias` — see
    # `sql/catalyst/.../basicLogicalOperators.scala::SubqueryAlias.metadataOutput`.
    # In SCOS, qualified-access-only columns live in the same physical
    # DataFrame, so we drop them here at every alias boundary; the new
    # qualifier wouldn't reach them anyway.
    input_container = input_container.without_qualified_access_only_columns()

    # Build all lists from the same source (all columns) to ensure matching lengths
    columns = input_container.column_map.columns
    spark_column_names = [c.spark_name for c in columns]
    snowpark_column_names = [c.snowpark_name for c in columns]
    qualifiers = [{ColumnQualifier((alias,))} for _ in columns]
    column_is_internal = [c.is_internal for c in columns]
    column_is_qualified_access_only = [c.is_qualified_access_only for c in columns]
    equivalent_snowpark_names = [c.equivalent_snowpark_names for c in columns]

    return DataFrameContainer.create_with_column_mapping(
        dataframe=input_container.dataframe,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        column_metadata=input_container.column_map.column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=input_container.column_map.get_parent_column_name_map(),
        column_is_internal=column_is_internal,
        column_is_qualified_access_only=column_is_qualified_access_only,
        alias=alias,
        equivalent_snowpark_names=equivalent_snowpark_names,
    )
