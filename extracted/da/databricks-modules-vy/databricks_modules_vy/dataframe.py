from pyspark.sql import DataFrame
from pyspark.sql.functions import *
import re


def shape(df):
    return print((df.count(), len(df.columns)))


def snake_headers(df, subset="all"):
    def _camel2snake(name):
        return name[0].lower() + re.sub(r"(?!^)[A-Z]", lambda x: "_" + x.group(0).lower(), name[1:])

    if subset == "all":
        list_cols = df.columns
    else:
        list_cols = subset

    for c in list_cols:
        df = df.withColumnRenamed(c, _camel2snake(c))
    return df


def add_metadata(
    df, source_system, timestamp_added=current_timestamp(), timestamp_updated=current_timestamp()
):
    """Adds standardized metadata to a dataframe, given the source system

    Args:
        source_system (string): The source system the row originates from. If several system applies, pick a 'main' system.
        timestamp_added (timestamp): The timestamp when the row was added to the data warehouse / data lake.
        timestamp_updated (timestamp): The timestamp when the row was last updated.

    Returns:
        DataFrame: The modified data frame with the new columns. If any of the columns exist, they will be overwritten.
    """
    return (
        df.withColumn("zx_timestamp_added", from_utc_timestamp(timestamp_added, "Europe/Oslo"))
        .withColumn("zx_timestamp_updated", from_utc_timestamp(timestamp_updated, "Europe/Oslo"))
        .withColumn("zx_source_system", lit(source_system))
    )


# From: https://stackoverflow.com/questions/39758045/how-to-perform-union-on-two-dataframes-with-different-amounts-of-columns-in-spark
# WORKS WELL.
# IMPROVE NOTATION ACCORDING TO OUR STANDARDS?
def _order_df_and_add_missing_cols(df, columns_order_list, df_missing_fields):
    """return ordered dataFrame by the columns order list with null in missing columns"""
    if not df_missing_fields:  # no missing fields for the df
        return df.select(columns_order_list)
    else:
        columns = []
        for colName in columns_order_list:
            if colName not in df_missing_fields:
                columns.append(colName)
            else:
                columns.append(lit(None).alias(colName))
        return df.select(columns)


def _add_missing_columns(df, missing_column_names):
    """Add missing columns as null in the end of the columns list"""
    list_missing_columns = []
    for col in missing_column_names:
        list_missing_columns.append(lit(None).alias(col))

    return df.select(df.schema.names + list_missing_columns)


def _order_and_union_d_fs(left_df, right_df, left_list_miss_cols, right_list_miss_cols):
    """return union of data frames with ordered columns by left_df."""
    left_df_all_cols = _add_missing_columns(left_df, left_list_miss_cols)
    right_df_all_cols = _order_df_and_add_missing_cols(
        right_df, left_df_all_cols.schema.names, right_list_miss_cols
    )
    return left_df_all_cols.union(right_df_all_cols)


def union_d_fs(left_df, right_df):
    """Union between two dataFrames, if there is a gap of column fields,
    it will append all missing columns as nulls"""
    # Check for None input
    if left_df is None:
        raise ValueError("left_df parameter should not be None")
    if right_df is None:
        raise ValueError("right_df parameter should not be None")
        # For data frames with equal columns and order- regular union
    if left_df.schema.names == right_df.schema.names:
        return left_df.union(right_df)
    else:  # Different columns
        # Save dataFrame columns name list as set
        left_df_col_list = set(left_df.schema.names)
        right_df_col_list = set(right_df.schema.names)
        # Diff columns between left_df and right_df
        right_list_miss_cols = list(left_df_col_list - right_df_col_list)
        left_list_miss_cols = list(right_df_col_list - left_df_col_list)
        return _order_and_union_d_fs(left_df, right_df, left_list_miss_cols, right_list_miss_cols)
