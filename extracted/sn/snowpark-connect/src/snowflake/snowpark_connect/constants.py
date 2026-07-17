#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

DEFAULT_CONNECTION_NAME = "spark-connect"
DEFAULT_CONNECTION_NAME_IN_SPCS = "default"
DEFAULT_SNOWPARK_SUBMIT_CONNECTION_NAME = "snowpark-submit"

STRUCTURED_TYPES_ENABLED = True

# UDF evaluation types (mirrors pyspark.rdd.PythonEvalType)
SQL_SCALAR_PANDAS_UDF_EVAL_TYPE = 200  # @pandas_udf Series→Series (vectorized)
SQL_SCALAR_PANDAS_ITER_UDF_EVAL_TYPE = (
    204  # @pandas_udf Iterator[Series]→Iterator[Series]
)
MAP_IN_ARROW_EVAL_TYPE = 207  # mapInArrow Iterator[RecordBatch]→Iterator[RecordBatch]

COLUMN_METADATA_COLLISION_KEY = "{expr_id}_{key}"

DUPLICATE_KEY_FOUND_ERROR_TEMPLATE = "Duplicate key found: {key}. You can set spark.sql.mapKeyDedupPolicy to LAST_WIN to deduplicate map keys with last wins policy."

SPARK_VERSION = "3.5.3"
