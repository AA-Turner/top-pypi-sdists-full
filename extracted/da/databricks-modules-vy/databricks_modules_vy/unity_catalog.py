from __future__ import annotations
from .logging import lp
#from modules.extend_class import extend_class
from pyspark.sql import DataFrame, SparkSession
from delta.tables import DeltaTable
import re

spark = SparkSession.builder.appName("module").getOrCreate()


def write_to_uc(
    df: DataFrame,
    target: str,
    mode: str = "overwrite",
    overwrite_schema: bool = False,
    raise_schema_mismatch_exception: bool = False,
    autoformat_columns: bool = False,
    table_description: str = "",
    comments: dict = None,
    partition_cols: str | list[str] = None,
    vacuum: bool = True,
    vacuum_retention_hours: int = 24 * 7,
) -> None:
    """
    Writes a DataFrame to an underlying persistent table in Unity Catalog (UC).

    Parameters:
        df (DataFrame): The DataFrame to be written to the table.
        target (str): The name of the table to write the DataFrame into.
        mode (str, optional): The write mode. Defaults to "overwrite".
        overwrite_schema (bool, optional): Wheter to overwrite the existing schema. Defaults to True.
        raise_schema_mismatch_exception (bool, optional): Whether schema mismatch should raise exception. Defaults to False.
        autoformat_columns (bool, optional): If True, column names are auto formatted to snake_case. Defaults to False.
        table_description (str, optional): Description to associate with the table. Defaults to "".
        comments (dict, optional): Dictionary of column names and column comments. Defaults to None.
        partition_cols (str or list, optional): List of column names to partition the table by. Defaults to None.
        vacuum (bool, optional): Whether to run a VACUUM operation after writing the DataFrame. Defaults to True.
        vacuum_retention_hours (int, optional): The retention period in hours for the VACUUM operation. Defaults to 24*2 (2 days).

    Returns:
        None

    Raises:
        Exception: If an error occurs during the write operation.
    """
    # Convert the partition_cols to a list if it's a single string
    if isinstance(partition_cols, str):
        partition_cols = [partition_cols]

    try:
        if autoformat_columns:
            df = format_columns(df)

        if not overwrite_schema:
            schema_match = _schemas_match(df, target)
            if schema_match == "Table does not exist":
                lp("Table does not exist.")
            elif schema_match in ["Missing columns", "Mismatch datatype", "New columns"]:
                if raise_schema_mismatch_exception:
                    raise Exception(f"Schema mismatch: {schema_match}")
                lp("Setting overwrite_schema = True")
                overwrite_schema = True

        # Store existing comments before writing
        current_comments = _get_column_comments(target)

        lp(f"Writing ({mode}) table to Unity Catalog at {target} ...")
        if partition_cols:
            df.write.mode(mode).option("overwriteSchema", overwrite_schema).partitionBy(
                partition_cols
            ).saveAsTable(target)
        else:
            df.write.mode(mode).option("overwriteSchema", overwrite_schema).saveAsTable(target)

        if table_description:
            lp("Commenting table ...")
            spark.sql(f"COMMENT ON TABLE {target} IS '{table_description}'")

        if comments:
            if autoformat_columns:
                comments = _format_comments_columns(comments)
            _apply_comments(target, table_description, comments, overwrite_schema, current_comments)

        if vacuum:
            uc_vacuum(target, vacuum_retention_hours)

    except Exception as e:
        lp(f"Write to uc: exception: {e}")
        raise


def upsert_to_uc(
    df: DataFrame,
    target: str,
    upsert_keys: str | list[str],
    autoformat_columns: bool = False,
    table_description: str = "",
    comments: dict = None,
    vacuum: bool = True,
    vacuum_retention_hours: int = 24 * 7,
    upsert_many: bool = False,
) -> None:
    """
    Performs an upsert (merge) operation on a DataFrame into an underlying persistent table in Unity Catalog (UC).
    After the upsert, it optionally runs a VACUUM operation to optimize table storage.

    Parameters:
        df (DataFrame): The DataFrame to be upserted into the table.
        target (str): The name of the table to perform the upsert on.
        upsert_keys (list or str): Column names or single column name used as the keys for upsert matching.
        autoformat_columns (bool, optional): If True, column names are auto formatted to snake_case. Defaults to False.
        table_description (str, optional): Description to associate with the table. Defaults to "".
        comments (dict, optional): Dictionary of column names and column comments. Defaults to None.
        vacuum (bool, optional): Whether to run a VACUUM operation after upsert. Defaults to True.
        vacuum_retention_hours (int, optional): The retention period in hours for the VACUUM operation. Defaults to 24*2 (2 days).
        upsert_many (bool, optional): Set to true if the target may match several rows from the source. Defaults to False.

    Returns:
        None

    Raises:
        Exception: If an error occurs during the upsert operation.
    """
    # Check if table exists
    try:
        _ = spark.sql(f"DESCRIBE {target}")
    except:
        lp("Table does not exist.")
        write_to_uc(
            df,
            target=target,
            overwrite_schema=True,
            table_description=table_description,
            comments=comments,
            vacuum=vacuum,
            vacuum_retention_hours=vacuum_retention_hours,
        )
        return

    # Convert the upsert_keys to a list if it's a single string
    if isinstance(upsert_keys, str):
        upsert_keys = [upsert_keys]

    try:
        # Format column names
        if autoformat_columns:
            df = format_columns(df)
            upsert_keys = [_format_column_name(key) for key in upsert_keys]

        schema_match = _schemas_match(df, target)
        if schema_match != "Match":
            raise Exception("Upsert failed - Schema mismatch")

        # Store existing comments before writing
        current_comments = _get_column_comments(target)

        # Retrieve target as a DeltaTable
        target_table = DeltaTable.forName(spark, target)

        # Create conditions for the join
        merge_condition = " AND ".join([f"target.{key} = source.{key}" for key in upsert_keys])

        if upsert_many:
            (
                target_table.alias("target")
                .merge(df.alias("source"), merge_condition)
                .whenMatchedDelete()
                .execute()
            )

            # Do it again for insert
            target_table = DeltaTable.forName(spark, target)
            (
                target_table.alias("target")
                .merge(df.alias("source"), merge_condition)
                .whenNotMatchedInsertAll()
                .execute()
            )
        else:
            (
                target_table.alias("target")
                .merge(df.alias("source"), merge_condition)
                .whenMatchedUpdateAll()
                .whenNotMatchedInsertAll()
                .execute()
            )

        if table_description:
            lp("Commenting table ...")
            spark.sql(f"COMMENT ON TABLE {target} IS '{table_description}'")

        if comments:
            if autoformat_columns:
                comments = _format_comments_columns(comments)
            _apply_comments(target, table_description, comments, False, current_comments)

        if vacuum:
            uc_vacuum(target, vacuum_retention_hours)
    except Exception as e:
        lp(f"Failed upsert to UC: {e}")
        raise


def autoloader_batch_to_uc(
    df: DataFrame,
    target: str,
    checkpoint_path: str,
    mode: str = "append",
    merge_schema: bool = True,
    raise_schema_mismatch_exception: bool = False,
    autoformat_columns: bool = False,
    table_description: str = "",
    comments: dict = None,
    partition_cols: str | list[str] = None,
    vacuum: bool = True,
    vacuum_retention_hours: int = 24 * 7,
) -> None:
    """
    Streams a DataFrame to an underlying persistent table (autoloader) in Unity Catalog (UC) using the trigger availableNow=True.
    After the streamingQuery termination, it optionally runs a VACUUM operation to optimize table storage.

    Parameters:
        df (DataFrame): The DataFrame to be streamed to the table.
        target (str): The name of the table to stream the DataFrame into.
        checkpoint_path (str): Location for storing checkpoint and schema. Typically in s3.
        mode (str, optional): The output mode. Defaults to "append".
        merge_schema (bool, optional): Whether to merge incoming schema changes into existing schema. Defaults to True.
        raise_schema_mismatch_exception (bool, optional): Whether schema mismatch should raise exception. Defaults to False.
        autoformat_columns (bool, optional): If True, column names are auto formatted to snake_case. Defaults to False.
        table_description (str, optional): Description to associate with the table. Defaults to "".
        comments (dict, optional): Dictionary of column names and column comments. Defaults to None.
        partition_cols (str or list, optional): List of column names to partition the table by. Defaults to None.
        vacuum (bool, optional): Whether to run a VACUUM operation after writing the DataFrame. Defaults to True.
        vacuum_retention_hours (int, optional): The retention period in hours for the VACUUM operation. Defaults to 24*2 (2 days).

    Returns:
        None

    Raises:
        Exception: If an error occurs during the write operation.
    """
    # Convert the partition_cols to a list if it's a single string
    if isinstance(partition_cols, str):
        partition_cols = [partition_cols]

    try:
        if autoformat_columns:
            df = df.format_columns()

        if not merge_schema:
            schema_match = _schemas_match(df, target)
            if schema_match == "Table does not exist":
                lp("Table does not exist.")
            elif schema_match in ["Missing columns", "Mismatch datatype", "New columns"]:
                if raise_schema_mismatch_exception:
                    raise Exception(f"Schema mismatch: {schema_match}")
                lp("Setting merge_schema = True")
                merge_schema = True

        # Store existing comments before writing
        current_comments = _get_column_comments(target)

        lp(f"Streaming ({mode}) table to Unity Catalog at {target} ...")
        if partition_cols:
            autoloader = (
                df.writeStream.option("checkpointLocation", checkpoint_path)
                .option("mergeSchema", merge_schema)
                .trigger(availableNow=True)
                .outputMode(mode)
                .partitionBy(partition_cols)
                .toTable(target)
            )
        else:
            autoloader = (
                df.writeStream.option("checkpointLocation", checkpoint_path)
                .option("mergeSchema", merge_schema)
                .trigger(availableNow=True)
                .outputMode(mode)
                .toTable(target)
            )
        autoloader.awaitTermination()

        if table_description:
            lp("Commenting table ...")
            spark.sql(f"COMMENT ON TABLE {target} IS '{table_description}'")

        if comments:
            if autoformat_columns:
                comments = _format_comments_columns(comments)
            _apply_comments(target, table_description, comments, merge_schema, current_comments)

        if vacuum:
            uc_vacuum(target, vacuum_retention_hours)

    except Exception as e:
        lp(f"Write to uc: exception: {e}")
        raise


def uc_vacuum(target: str, vacuum_retention_hours: int = 24 * 7) -> None:
    """
    Run a VACUUM operation on a Unity Catalog (UC) table to optimize storage.

    Parameters:
        target (str): The name of the table to run the VACUUM operation on.
        vacuum_retention_hours (int, optional): The retention period in hours for the VACUUM operation. Defaults to 24*7 (1 week).

    Returns:
        None
    """
    lp(f"Vacuuming table with {vacuum_retention_hours} retention hours ...")
    spark.sql(f"VACUUM {target} RETAIN {vacuum_retention_hours} HOURS")


def uc_query(query: str) -> DataFrame:
    """
    Executes a SQL query on the Spark session.

    Parameters:
        query (str): The SQL query to be executed.

    Returns:
        DataFrame: The result of the query.

    """
    return spark.sql(query)


def uc_table(table: str) -> DataFrame:
    """
    Retrieves a DataFrame representing a table from Unity Catalog (UC).

    Parameters:
        target (str): The name of the table to retrieve.

    Returns:
        DataFrame: The DataFrame representing the requested table.

    """
    return spark.table(table)


def _get_column_comments(target: str) -> dict:
    """
    Fetches comments for all columns of a table from Unity Catalog.

    Parameters:
        target (str): The name of the table.

    Returns:
        dict: A dictionary with column names as keys and their comments as values.
    """
    try:
        comments_df = spark.sql(f"DESCRIBE TABLE {target}")
    except Exception:
        # Table does not exist
        return False

    comments_dict = {}
    for row in comments_df.collect():
        col_name, col_type, col_comment = row
        comments_dict[col_name] = col_comment
    return comments_dict


def _schemas_match(df: DataFrame, target: str) -> str:
    """
    Compares the schema of a DataFrame with the schema of an existing table.
    Raises an exception if schemas do not match, specifying the mismatch details.

    Parameters:
        df (DataFrame): The DataFrame whose schema is to be compared.
        target (str): The name of the table.

    Returns:
        bool: True if the schemas match, otherwise raises an exception.
    """
    # Attempt to read zero rows from the target table to get its schema
    if spark.catalog.tableExists(target):
        table_df = spark.read.table(target).limit(0)
    else:
        # Table does not exist
        return "Table does not exist"

    # Extract schema from the table and the DataFrame
    table_schema = {col.name: col.dataType.simpleString() for col in table_df.schema}
    df_schema = {col.name: col.dataType.simpleString() for col in df.schema}

    # Identify mismatches
    new_columns = []
    mismatch_datatype = []
    for col_name, col_type in df_schema.items():
        if col_name not in table_schema:
            new_columns.append(col_name)
        elif col_type != table_schema[col_name]:
            mismatch_datatype.append(
                f"Data type mismatch for column {col_name}: DataFrame has {col_type}, table has {table_schema[col_name]}"
            )

    missing_columns = []
    for col_name in table_schema:
        if col_name not in df_schema:
            missing_columns.append(col_name)

    # If any mismatches, log them and return status code
    if missing_columns:
        lp(f"Missing columns in DataFrame: {', '.join(missing_columns)}")
        return "Missing columns"
    if mismatch_datatype:
        lp(f"Mismatch: {', '.join(mismatch_datatype)}")
        return "Mismatch datatype"
    if new_columns:
        lp(f"New columns in DataFrame: {', '.join(new_columns)}")
        return "New columns"

    return "Match"


def _apply_comments(
    target: str,
    table_description: str,
    comments: dict,
    overwrite_schema: bool,
    current_comments: dict,
) -> None:
    lp("Commenting columns ...")
    if overwrite_schema or not current_comments:
        # If schema is overwritten or there are no comments currently, reapply all comments
        for col, comment in comments.items():
            spark.sql(f"ALTER TABLE {target} CHANGE {col} COMMENT '{comment}'")
    else:
        # If schema is not overwritten, only apply comments that have changed or are new
        for col, comment in comments.items():
            if col not in current_comments or comment != current_comments[col]:
                spark.sql(f"ALTER TABLE {target} CHANGE {col} COMMENT '{comment}'")


def _format_column_name(column_name: str) -> str:
    """
    Converts a column name to snake_case.

    Parameters:
    column_name (str): The name of the column to be formatted.

    Returns:
    str: The formatted column name in snake_case.
    """
    # Replace any non-alphanumeric character with an underscore
    formatted_name = re.sub(r"\W+", "_", column_name)
    # Convert to lowercase
    formatted_name = formatted_name.lower()
    return formatted_name


def _format_comments_columns(col_comment_dict: dict) -> dict:
    """
    Formats column names and associates them with comments based on a provided dictionary.

    Parameters:
    col_comment_dict (dict): Dictionary with column names as keys and comments as values.

    Returns:
    dict: A dictionary with formatted column names as keys and comments as values.
    """
    formatted_dict = {
        _format_column_name(col_name): comment for col_name, comment in col_comment_dict.items()
    }
    return formatted_dict


def format_columns(df: DataFrame, verbose: bool = True) -> DataFrame:
    """
    Formats all column names in a DataFrame to snake_case.
    Delta tables can't have column names with ' ,;{}()\n\t='

    Parameters:
    df (DataFrame): The DataFrame with column names to be formatted.
    verbose (bool): Prints info about the formatting if true. Defaults to true

    Returns:
    DataFrame: The DataFrame with formatted column names in snake_case.
    """
    if verbose:
        lp("Formatting column names ...")
    formatted_columns = []
    for column_name in df.columns:
        formatted_name = _format_column_name(column_name)
        if column_name != formatted_name:
            formatted_columns.append(f"{column_name} -> {formatted_name}")
        df = df.withColumnRenamed(column_name, formatted_name)
    if formatted_columns and verbose:
        lp(f"Formatted columns: {', '.join(formatted_columns)}")
    return df