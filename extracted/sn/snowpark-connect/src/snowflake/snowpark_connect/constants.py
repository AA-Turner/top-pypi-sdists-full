#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

DEFAULT_CONNECTION_NAME = "spark-connect"
DEFAULT_CONNECTION_NAME_IN_SPCS = "default"
DEFAULT_SNOWPARK_SUBMIT_CONNECTION_NAME = "snowpark-submit"

SERVER_SIDE_SESSION_ID = "321"

STRUCTURED_TYPES_ENABLED = True

# UDF evaluation types
MAP_IN_ARROW_EVAL_TYPE = 207  # eval_type for mapInArrow operations

COLUMN_METADATA_COLLISION_KEY = "{expr_id}_{key}"

DUPLICATE_KEY_FOUND_ERROR_TEMPLATE = "Duplicate key found: {key}. You can set spark.sql.mapKeyDedupPolicy to LAST_WIN to deduplicate map keys with last wins policy."

SPARK_VERSION = "3.5.3"
