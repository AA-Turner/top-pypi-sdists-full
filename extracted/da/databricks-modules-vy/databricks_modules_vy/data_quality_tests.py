from pyspark.sql import DataFrame
from .logging import bold_lp, success_lp, error_lp
#from modules.extend_class import extend_class
from pyspark.sql.functions import *


def test_uniqueness_of_columns(df, columns, raise_exception=True):
    """
    Checks if all values in each specified column are unique. If the test fails for any column,
    the invalid rows are shown, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):           The DataFrame to be tested.
        columns (str or list of str):     The column(s) to be checked for uniqueness.
        raise_exception (bool):           Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking for unique values...")
    for c in columns:
        df_test = df.groupBy(c).agg(count("*").alias("n")).filter("n > 1")
        duplicate_count = df_test.count()
        if duplicate_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: Column '{c}' contains {duplicate_count} duplicate values."
                )
            else:
                error_lp(f"Test failed: Column '{c}' contains {duplicate_count} duplicate values.")
        else:
            success_lp(f"Column '{c}' is unique.")


def test_for_null_values(df, columns, raise_exception=True):
    """
    The function checks if there exist null values in each specified column. If the test fails for any column,
    the invalid rows are shown, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        columns (str or list of str):  The column(s) to be checked for null values.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking for null values...")
    for c in columns:
        df_test = df.filter(f"{c} is null")
        null_count = df_test.count()
        if null_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: Column '{c}' contains {null_count} null values."
                )
            else:
                error_lp(f"Test failed: Column '{c}' contains {null_count} null values.")
        else:
            success_lp(f"Column '{c}' does not contain null values.")


def test_empty_dataframe(df, raise_exception=True):
    """
    Checks if a DataFrame is empty. If the test fails, it shows an error message
    and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    bold_lp("Checking for empty dataframe...")
    if df.count() == 0:
        if raise_exception:
            raise AssertionError("Test failed: DataFrame is empty.")
        else:
            error_lp("Test failed: DataFrame is empty.")
    else:
        success_lp("DataFrame is not empty")


def validate_empty_dataframe(df, df_name="DataFrame", raise_exception=True):
    """
    Use this function if you're using Spark 3.3 or later.

    Validate that a PySpark DataFrame has any rows.

    Parameters:
    - df: The DataFrame to validate.
    - df_name: Name of the DataFrame (optional, for logging).
    - raise_exception (bool):   Whether an exception should be raised or not.

    Raises:
    - ValueError: If the DataFrame is empty.
    """
    if df.isEmpty():
        if raise_exception:
            raise AssertionError(f"Test failed: {df_name} is empty.")
        else:
            error_lp(f"Test failed: {df_name} is empty.")
    else:
        success_lp(f"{df_name} is not empty")


def test_value_range(df, columns, min_value=None, max_value=None, raise_exception=True):
    """
    Checks if the values in a column are within a specified range. If the test fails,
    it shows the invalid rows, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):         The DataFrame to be tested.
        columns (str or list):          The column(s) to be checked for value range.
        min_value (numeric, optional):  The minimum value of the range (inclusive). If not provided,
                                        the minimum value is set to negative infinity.
        max_value (numeric, optional):  The maximum value of the range (inclusive). If not provided,
                                        the maximum value is set to infinity.
        raise_exception (bool):         Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    if min_value is None:
        min_value = float("-inf")
    if max_value is None:
        max_value = float("inf")

    bold_lp("Checking for value ranges...")
    for c in columns:
        df_test = df.filter(f"{c} < {min_value} or {c} > {max_value}")
        invalid_count = df_test.count()
        if invalid_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: {invalid_count} values in column '{c}' are outside the range [{min_value}, {max_value}]."
                )
            else:
                error_lp(
                    f"Test failed: {invalid_count} values in column '{c}' are outside the range [{min_value}, {max_value}]."
                )
        else:
            success_lp(
                f"All values in column '{c}' are within the range [{min_value}, {max_value}]."
            )


def test_uniqueness_of_combination(df, columns, raise_exception=True):
    """
    Checks if there are any duplicate combinations of values in specified columns.
    If the test fails, it shows the invalid rows, and if `raise_exception` is `True`,
    an exception is raised.

    Parameters:
        df (pyspark.DataFrame):       The DataFrame to be tested.
        columns (list):        The column(s) to be checked for unique combinations.
        raise_exception (bool):       Whether an exception should be raised or not.
    """
    bold_lp("Checking unique combinations...")
    df_test = df.groupBy(*columns).count().filter("count > 1")
    duplicate_count = df_test.count()
    if duplicate_count > 0:
        df_test.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {duplicate_count} duplicate combinations found in columns: {columns}."
            )
        else:
            error_lp(
                f"Test failed: {duplicate_count} duplicate combinations found in columns: {columns}."
            )
    else:
        success_lp(f"No duplicate combinations found in columns: {columns}.")


def test_missing_values(df, columns, raise_exception=True):
    """
    Checks if specified columns contain any missing values (null or NaN). If the test fails,
    it shows the invalid rows, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        columns (str or list):    The column(s) to be checked for missing values.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking for missing values...")
    for c in columns:
        df_test = df.filter(f"{c} is null or isnan({c})")
        missing_count = df_test.count()
        if missing_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: Column '{c}' contains {missing_count} missing values."
                )
            else:
                error_lp(f"Test failed: Column '{c}' contains {missing_count} missing values.")
        else:
            success_lp(f"Column '{c}' does not contain missing values.")


def test_string_length(df, columns, min_length, max_length, raise_exception=True):
    """
    Checks if the length of strings in specified columns falls within the specified range.
    If the test fails, it shows the invalid rows, and if `raise_exception` is `True`,
    an exception is raised.

    Parameters:
        df (pyspark.DataFrame):       The DataFrame to be tested.
        columns (str or list):        The column(s) to be checked for string length.
        min_length (int):             The minimum allowed length (inclusive).
        max_length (int):             The maximum allowed length (inclusive).
        raise_exception (bool):       Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking string lengths...")
    for c in columns:
        df_test = df.filter(f"length({c}) < {min_length} or length({c}) > {max_length}")
        invalid_count = df_test.count()
        if invalid_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: {invalid_count} string lengths in column '{c}' is outside the range [{min_length}, {max_length}]."
                )
            else:
                error_lp(
                    f"Test failed: {invalid_count} string lengths in column '{c}' is outside the range [{min_length}, {max_length}]."
                )
        else:
            success_lp(
                f"All string lengths in column '{c}' are within the range [{min_length}, {max_length}]."
            )


def test_list_size(df, columns, min_size, max_size, raise_exception=True):
    """
    Checks if the list size in specified columns falls within the specified range.
    If the test fails, it shows the invalid rows, and if `raise_exception` is `True`,
    an exception is raised.

    Parameters:
        df (pyspark.DataFrame):       The DataFrame to be tested.
        columns (str or list):        The column(s) to be checked for list size.
        min_size (int):               The minimum allowed size (inclusive).
        max_size (int):               The maximum allowed size (inclusive).
        raise_exception (bool):       Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking list sizes...")
    for c in columns:
        df_test = df.filter(f"size({c}) < {min_size} or size({c}) > {max_size}")
        invalid_count = df_test.count()
        if invalid_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: {invalid_count} list sizes in column '{c}' is outside the range [{min_size}, {max_size}]."
                )
            else:
                error_lp(
                    f"Test failed: {invalid_count} list sizes in column '{c}' is outside the range [{min_size}, {max_size}]."
                )
        else:
            success_lp(
                f"All list sizes in column '{c}' are within the range [{min_size}, {max_size}]."
            )


def test_column_data_type(df, columns, data_type, raise_exception=True):
    """
    Checks if values in specified columns match the specified data type. If the test fails,
    it shows the invalid rows, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        columns (str or list):    The column(s) to be checked for data type.
        data_type (str):          The expected data type of the columns.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    if isinstance(columns, str):
        columns = [columns]

    bold_lp("Checking column data types...")
    for c in columns:
        df_test = df.filter(f"typeof({c}) != '{data_type}'")
        invalid_count = df_test.count()
        if invalid_count > 0:
            df_test.show(truncate=False)
            if raise_exception:
                raise AssertionError(
                    f"Test failed: {invalid_count} values in column '{c}' do not match the expected data type '{data_type}'."
                )
            else:
                error_lp(
                    f"Test failed: {invalid_count} values in column '{c}' do not match the expected data type '{data_type}'."
                )
        else:
            success_lp(f"All values in column '{c}' match the expected data type '{data_type}'.")


def test_pattern_matching(df, column, pattern, raise_exception=True):
    """
    Checks if values in a string column match the specified pattern using regular expressions.
    If the test fails, it shows the invalid rows, and if `raise_exception` is `True`,
    an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        column (str):             The string column to be checked for pattern matching.
        pattern (str):            The regular expression pattern to match against.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    bold_lp("Checking matching patterns...")
    df_test = df.filter(~col(column).rlike(pattern))
    invalid_count = df_test.count()
    if invalid_count > 0:
        df_test.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {invalid_count} values in column '{column}' do not match the specified pattern '{pattern}'."
            )
        else:
            error_lp(
                f"Test failed: {invalid_count} values in column '{column}' do not match the specified pattern '{pattern}'."
            )
    else:
        success_lp(f"All values in column '{column}' match the specified pattern '{pattern}'.")


def test_column_value_existence(df, column, reference_df, reference_column, raise_exception=True):
    """
    Checks if values in a column exist in another DataFrame's column. If the test fails,
    it shows the invalid rows, and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):           The DataFrame to be tested.
        column (str):                     The column to be checked for value existence.
        reference_df (pyspark.DataFrame):  The reference DataFrame.
        reference_column (str):           The column in the reference DataFrame.
        raise_exception (bool):           Whether an exception should be raised or not.
    """
    bold_lp("Checking column value existence...")
    df_test = df.join(reference_df, df[column] == reference_df[reference_column], "left_anti")
    invalid_count = df_test.count()
    if invalid_count > 0:
        df_test.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {invalid_count} values in column '{column}' do not exist in the reference DataFrame's column '{reference_column}'."
            )
        else:
            error_lp(
                f"Test failed: {invalid_count} values in column '{column}' do not exist in the reference DataFrame's column '{reference_column}'."
            )
    else:
        success_lp(
            f"All values in column '{column}' exist in the reference DataFrame's column '{reference_column}'."
        )


def test_greater_than(df, col_A, col_B, raise_exception=True):
    """
    Performs a pairwise comparison between two columns in a DataFrame to check if col_A > col_B for each row.
    If the test fails, it shows the invalid rows, and if raise_exception is True, an exception is raised.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        col_A (str): The first column to be compared.
        col_B (str): The second column to be compared.
        raise_exception (bool): Whether an exception should be raised or not.
    """
    bold_lp(f"Checking if {col_A} > {col_B}...")
    invalid_rows = df.filter(col(col_A) <= col(col_B))
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(f"Test failed: {invalid_count} rows where {col_A} <= {col_B}")
        else:
            error_lp(f"Test failed: {invalid_count} rows where {col_A} <= {col_B}")
    else:
        success_lp(f"{col_A} <= {col_B}")


def test_greater_than_or_equal(df, col_A, col_B, raise_exception=True):
    """
    Performs a pairwise comparison between two columns in a DataFrame to check if col_A >= col_B for each row.
    If the test fails, it shows the invalid rows, and if raise_exception is True, an exception is raised.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        col_A (str): The first column to be compared.
        col_B (str): The second column to be compared.
        raise_exception (bool): Whether an exception should be raised or not.
    """
    bold_lp(f"Checking if {col_A} >= {col_B}...")
    invalid_rows = df.filter(col(col_A) < col(col_B))
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(f"Test failed: {invalid_count} rows where {col_A} < {col_B}")
        else:
            error_lp(f"Test failed: {invalid_count} rows where {col_A} < {col_B}")
    else:
        success_lp(f"{col_A} >= {col_B}")


def test_equal(df, col_A, col_B, raise_exception=True):
    """
    Performs a pairwise comparison between two columns in a DataFrame to check if col_A == col_B for each row.
    If the test fails, it shows the invalid rows, and if raise_exception is True, an exception is raised.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        col_A (str): The first column to be compared.
        col_B (str): The second column to be compared.
        raise_exception (bool): Whether an exception should be raised or not.
    """
    bold_lp(f"Checking if {col_A} == {col_B}...")
    invalid_rows = df.filter(~(col(col_A) == col(col_B)))
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(f"Test failed: {invalid_count} rows where {col_A} != {col_B}")
        else:
            error_lp(f"Test failed: {invalid_count} rows where {col_A} != {col_B}")
    else:
        success_lp(f"{col_A} == {col_B}")


def test_not_equal(df, col_A, col_B, raise_exception=True):
    """
    Performs a pairwise comparison between two columns in a DataFrame to check if col_A == col_B for each row.
    If the test fails, it shows the invalid rows, and if raise_exception is True, an exception is raised.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        col_A (str): The first column to be compared.
        col_B (str): The second column to be compared.
        raise_exception (bool): Whether an exception should be raised or not.
    """
    bold_lp(f"Checking if {col_A} != {col_B}...")
    invalid_rows = df.filter((col(col_A) == col(col_B)))
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(f"Test failed: {invalid_count} rows where {col_A} == {col_B}")
        else:
            error_lp(f"Test failed: {invalid_count} rows where {col_A} == {col_B}")
    else:
        success_lp(f"{col_A} != {col_B}")


def test_values_in_set(df, column, values, raise_exception=True):
    """
    Checks if values in a column match a set of input values. If the test fails, it shows the invalid rows
    and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        column (str):             The column to be checked for matching values.
        values (list or set):     The set of input values to compare against.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    bold_lp(f"Checking if values in '{column}' match the provided set of values...")
    invalid_rows = df.filter(~df[column].isin(values))
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {invalid_count} rows in column '{column}' do not match the provided set of values."
            )
        else:
            error_lp(
                f"Test failed: {invalid_count} rows in column '{column}' do not match the provided set of values."
            )
    else:
        success_lp(f"All values in column '{column}' match the provided set of values.")


def test_for_numeric_values(df, column, raise_exception=True):
    """
    Checks if there exists numeric values in the column. If numeric values exists, the test fails and if `raise_exception` is `True`, an exception is raised.

    Parameters:
        df (pyspark.DataFrame):   The DataFrame to be tested.
        column (str):             The column to be checked for numeric values.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    bold_lp(f"Checking for numeric values in '{column}'...")
    invalid_rows = df.filter(df[column].cast("int").isNotNull())
    invalid_count = invalid_rows.count()
    if invalid_count > 0:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {invalid_count} rows in column '{column}' contain numeric values."
            )
        else:
            error_lp(
                f"Test failed: {invalid_count} rows in column '{column}' contain numeric values."
            )
    else:
        success_lp(f"All values in column '{column}' are non-numeric.")


def test_count_is_equal(df1, df2, raise_exception=True):
    """
    Compares two dataframes to check if the row counts are equal.

    Parameters:
        df1 (pyspark.DataFrame):  The DataFrame to be tested.
        df2 (pyspark.DataFrame):  The DataFrame to be tested against.
        raise_exception (bool):   Whether an exception should be raised or not.
    """
    bold_lp("Checking if count is equal...")
    count_df1 = df1.count()
    count_df2 = df2.count()

    if count_df1 != count_df2:
        if raise_exception:
            raise AssertionError(
                f"Test failed: count doesn't match. df1: {count_df1}, df2: {count_df2}"
            )
        else:
            error_lp(f"Test failed: count doesn't match. df1: {count_df1}, df2: {count_df2}")
    else:
        success_lp("The count matches.")


def test_for_substring(df, col1, col2, raise_exception=True):
    """
    Compares two columns of a dataframe and checks that the col2 exists as a substring of col1.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        col1 (str):             The column to search for a substring in
        col2 (str):             The column (with substring) to test for in col1
        raise_exception (bool): Whether an exception should be raised or not.
    """

    bold_lp(f"Checking if substring of '{col2}' exists as substrings in '{col1}'")
    invalid_rows = df.filter(~expr(f"locate({col2}, {col1}) > 0"))
    invalid_count = invalid_rows.count()

    if invalid_count:
        invalid_rows.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {invalid_count} rows in column '{col2}' were not identified as substrings in '{col1}'"
            )
        else:
            error_lp(
                f"Test failed: {invalid_count} rows in column '{col2}' were not identified as substrings in '{col1}'"
            )
    else:
        success_lp(f"All values in '{col2}' were found as substrings in '{col1}'")


def test_documented_columns(df, comments, raise_exception=True):
    """
    Checks if the columns documented in comments match the columns of the DataFrame.

    Parameters:
        df (pyspark.DataFrame): The DataFrame to be tested.
        comments (list, dict): List or dictionary of strings representing the documented columns.
        raise_exception (bool): Whether an exception should be raised or not.
    """

    bold_lp("Checking if comments match df ...")
    df_columns_set = set(df.columns)
    comments_set = set(comments)

    if (unrecognized_columns := comments_set - df_columns_set) | (
        undocumented_columns := df_columns_set - comments_set
    ):
        error_message = f"""
        Found undocumented columns.
        Cols found in df but not in comments: {', '.join(undocumented_columns) if undocumented_columns else 'None'}
        Cols found in comments but not in df: {', '.join(unrecognized_columns) if unrecognized_columns else 'None'}
        """

        if raise_exception:
            raise AssertionError(error_message)

        error_lp(error_message)
    else:
        success_lp("All comments match the columns of the df")

def test_for_missing_elements_in_sequence(
    df,
    partition_cols,
    stop_sequence_col,
    start_sequence=None,
    stop_sequence=None,
    raise_exception=True,
):
    """
    Checks if there are any missing elements in a sequence column.

    Parameters:
        df (pyspark.DataFrame):          The DataFrame to be tested.
        partition_cols list):            The columns identifying the partition.
        stop_sequence_col (str):         The column specifying the sequence.
        start_sequence (int, optional):  Manual entry for first element in sequence.
        stop_sequence (int, optional):   Manual entry for last element in sequence.
        raise_exception (bool):          Whether an exception should be raised or not.
    """

    # Get the min and max of the sequence in the partition
    df_partition_ranges = df.groupBy(partition_cols).agg(
        min(stop_sequence_col).alias("min_seq"), max(stop_sequence_col).alias("max_seq")
    )

    if start_sequence is not None:
        df_partition_ranges = df_partition_ranges.withColumn("min_seq", lit(start_sequence))

    if stop_sequence is not None:
        df_partition_ranges = df_partition_ranges.withColumn("max_seq", lit(stop_sequence))

    # Generate the full sequence for each partition
    df_expanded = df_partition_ranges.withColumn(
        "expected_sequences", expr("sequence(min_seq, max_seq)")
    )

    # Explode to get each expected stop as a separate row, and join with the original data
    df_expanded = df_expanded.select(
        *partition_cols, explode("expected_sequences").alias(stop_sequence_col)
    )

    # Finds missing stops by keeping rows that have no match in the original data
    df_joined = df_expanded.join(df, on=[*partition_cols, stop_sequence_col], how="left_anti")

    # Count missing rows
    missing_count = df_joined.count()

    if missing_count > 0:
        df_joined.show(truncate=False)
        if raise_exception:
            raise AssertionError(
                f"Test failed: {missing_count} missing elements in the sequence for column '{stop_sequence_col}' in the partition defined by '{partition_cols}'"
            )
        else:
            error_lp(
                f"Test failed: {missing_count} missing elements in the sequence for column '{stop_sequence_col}' in the partition defined by '{partition_cols}'"
            )
    else:
        success_lp(
            f"All elements are present in the sequence for column '{stop_sequence_col}' for each partition defined by '{partition_cols}'"
        )
