#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake import snowpark
from snowflake.snowpark_connect.utils import context


def is_df_name(name_to_check: str, check_outer_df: bool = True) -> bool:
    """
    Checks if the given name matches the current DataFrame or any outer DataFrames.

    Args:
        name_to_check: The name to check against DataFrame aliases or table names.
        check_outer_df: If True, checks outer DataFrames.

    Returns:
        True if the name matches any DataFrame, False otherwise.
    """
    # Check if the current DataFrame matches the name
    if check_df_name_match(context.get_df_before_projection(), name_to_check):
        return True
    # Then check if any of the outer DataFrames match the name
    if check_outer_df and any(
        check_df_name_match(outer_df, name_to_check)
        for outer_df in context.get_outer_dataframes()
    ):
        return True
    return False


def check_df_name_match(df: snowpark.DataFrame | None, name_to_check: str) -> bool:
    """
    Checks if the given name matches the DataFrame's alias or table name.

    Args:
        df: The Snowpark DataFrame to check. Can be None.
        name_to_check: The name to compare against the DataFrame's alias or table name.

    Returns:
        True if the name matches the DataFrame's alias or table name, False otherwise.
    """
    if df is None:
        return False
    if df._alias:
        if df._alias == name_to_check:
            return True
    elif (
        hasattr(df, "_table_name")
        and df._table_name
        and df._table_name == name_to_check
    ):
        return True
    return False
