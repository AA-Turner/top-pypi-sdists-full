#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from typing import Optional, Tuple

from pyspark.errors import AnalysisException

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.context import get_spark_session_id

_temp_views = SynchronizedDict[Tuple[str, str], DataFrameContainer]()


def register_temp_view(name: str, df: DataFrameContainer, replace: bool) -> None:
    normalized_name = _normalize(name)
    current_session_id = get_spark_session_id()
    for key in list(_temp_views.keys()):
        if _normalize(key[0]) == normalized_name and key[1] == current_session_id:
            if replace:
                _temp_views.remove(key)
                break
            else:
                exception = AnalysisException(
                    f"[TEMP_TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create the temporary view `{name}` because it already exists."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

    _temp_views[(name, current_session_id)] = df


def unregister_temp_view(name: str) -> bool:
    normalized_name = _normalize(name)

    for key in _temp_views.keys():
        normalized_key = _normalize(key[0])
        if normalized_name == normalized_key and key[1] == get_spark_session_id():
            pop_result = _temp_views.remove(key)
            return pop_result is not None
    return False


def get_temp_view(name: str) -> Optional[DataFrameContainer]:
    normalized_name = _normalize(name)
    for key in _temp_views.keys():
        normalized_key = _normalize(key[0])
        if normalized_name == normalized_key and key[1] == get_spark_session_id():
            return _temp_views.get(key)
    return None


def get_temp_view_normalized_names() -> list[str]:
    return [
        _normalize(key[0])
        for key in _temp_views.keys()
        if key[1] == get_spark_session_id()
    ]


def _normalize(name: str) -> str:
    from snowflake.snowpark_connect.config import global_config

    return name if global_config.spark_sql_caseSensitive else name.lower()
