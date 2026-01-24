#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)


def map_alias(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Returns an aliased dataframe in which the columns can now be referenced to using col(<df alias>, <column name>).
    """
    alias: str = rel.subquery_alias.alias
    # we set reuse_parsed_plan=False because we need new expr_id for the attributes (output columns) in aliased snowpark dataframe
    # reuse_parsed_plan will lead to ambiguous column name for operations like joining two dataframes that are aliased from the same dataframe
    input_container = without_internal_columns(
        map_relation(rel.subquery_alias.input, reuse_parsed_plan=False)
    )
    qualifiers = [
        {ColumnQualifier((alias,))} for _ in input_container.column_map.columns
    ]

    return DataFrameContainer.create_with_column_mapping(
        dataframe=input_container.dataframe,
        spark_column_names=input_container.column_map.get_spark_columns(),
        snowpark_column_names=input_container.column_map.get_snowpark_columns(),
        column_metadata=input_container.column_map.column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=input_container.column_map.get_parent_column_name_map(),
        alias=alias,
        equivalent_snowpark_names=input_container.column_map.get_equivalent_snowpark_names(),
    )
