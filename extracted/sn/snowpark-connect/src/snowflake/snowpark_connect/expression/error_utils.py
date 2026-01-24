#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.column import Column
from snowflake.snowpark.types import DataType, StringType


def raise_error_helper(return_type: DataType, error_class=None):
    error_class_str = (
        f":{error_class.__name__}"
        if error_class and hasattr(error_class, "__name__")
        else ""
    )

    def _raise_fn(*msgs: Column) -> Column:
        return snowpark_fn.cast(
            snowpark_fn.abs(
                snowpark_fn.concat(
                    snowpark_fn.lit(f"[snowpark-connect-exception{error_class_str}]"),
                    *(msg.try_cast(StringType()) for msg in msgs),
                )
            ).cast(StringType()),
            return_type,
        )

    return _raise_fn
