#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re

import pyspark.sql.connect.proto.base_pb2 as proto_base

from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.type_mapping import (
    SNOWPARK_TYPE_NAME_TO_PYSPARK_TYPE_NAME,
)


def _remove_quotes_from_nested_fields(tree_string: str) -> str:
    """
    Remove quotes from nested field names in the schema tree string.

    Snowpark's _format_schema uses quote_name() which adds quotes to preserve case.
    Native Spark doesn't add quotes in printSchema() output.
    Only nested fields (those with indentation like ' |   |--') need unquoting.
    Top-level fields are already translated via translate_columns.

    e.g. ' |   |-- "review": array' -> ' |   |-- review: array'
    """
    lines = tree_string.split("\n")
    result = []
    for line in lines:
        if " |  " in line and ' |-- "' in line:
            line = re.sub(r'\|-- "([^"]+)":', r"|-- \1:", line)
        result.append(line)
    return "\n".join(result)


def map_tree_string(
    request: proto_base.AnalyzePlanRequest,
) -> proto_base.AnalyzePlanResponse:
    # TODO: tracking the difference with pyspark in SNOW-1853347
    tree_string = request.tree_string
    snowpark_df_container = map_relation(tree_string.plan.root)

    if snowpark_df_container.has_zero_columns():
        return proto_base.AnalyzePlanResponse(
            session_id=request.session_id,
            tree_string=proto_base.AnalyzePlanResponse.TreeString(
                tree_string="root\n",
            ),
        )

    filtered_container = without_internal_columns(snowpark_df_container)
    display_df = filtered_container.dataframe
    filtered_column_mapping = filtered_container.column_map.snowpark_to_spark_map()

    snowpark_tree_string = display_df._format_schema(
        level=tree_string.level if tree_string.HasField("level") else None,
        translate_columns=filtered_column_mapping,
        translate_types=SNOWPARK_TYPE_NAME_TO_PYSPARK_TYPE_NAME,
    )

    # Remove quotes from nested field names
    snowpark_tree_string = _remove_quotes_from_nested_fields(snowpark_tree_string)

    # workaround for the capitalization of nullable boolean value.
    snowpark_tree_string = snowpark_tree_string.replace(
        "nullable = True", "nullable = true"
    )
    snowpark_tree_string = snowpark_tree_string.replace(
        "nullable = False", "nullable = false"
    )
    proto_tree_string = proto_base.AnalyzePlanResponse.TreeString(
        tree_string=f"{snowpark_tree_string}\n",
    )
    return proto_base.AnalyzePlanResponse(
        session_id=request.session_id, tree_string=proto_tree_string
    )
