"""
Apache Spark Utility Methods
"""
import os
import logging
import pyspark.sql.types as ps_types
import pyspark.sql.functions as psf
from . import s3_utils

# Setup s3 keys
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')


def create_spark_schema(column_headers, column_types):
    """
    This method will create the pyspark schema provited types and
    column headers.

    Returns:
        pyspark schema
    """
    columns = zip(column_headers, column_types)
    schema = ps_types.StructType([
        ps_types.StructField(
            col_name,
            getattr(ps_types, col_type)(),
            True)
        for (col_name, col_type) in columns])

    return schema


def rename_cols(spark_df, column_map):
    """
    This method will rename a spark dataframes columns provided a column map.

    Args:
        spark_df (pyspark.sql.dataframe.DataFrame): data
        column_map (dict): rename column mapping

    Returns:
        modified spark dataframe with new column headers
    """
    for old_col_header, new_col_header in column_map.items():
        spark_df = spark_df.withColumnRenamed(
            old_col_header, new_col_header)

    return spark_df


def get_equivalent_spark_type(pandas_type):
    """
    This method will retrieve the corresponding spark type given a pandas
    type.

    Source: https://stackoverflow.com/questions/37513355

    Args:
        pandas_type (str): pandas data type

    Returns:
        spark data type
    """
    type_map = {
        'datetime64[ns]': ps_types.TimestampType(),
        'int64': ps_types.LongType(),
        'int32': ps_types.IntegerType(),
        'float64': ps_types.DoubleType(),
        'float32': ps_types.FloatType()}
    if pandas_type not in type_map:
        return ps_types.StringType()

    return type_map[pandas_type]


def pandas_to_spark(spark, pandas_df):
    """
    This method will return a spark dataframe given a pandas dataframe.

    Args:
        spark (pyspark.sql.session.SparkSession): pyspark session
        pandas_df (pandas.core.frame.DataFrame): pandas DataFrame

    Returns:
        equivalent spark DataFrame
    """
    columns = list(pandas_df.columns)
    types = list(pandas_df.dtypes)
    p_schema = ps_types.StructType([
        ps_types.StructField(
            column, get_equivalent_spark_type(str(pandas_type)))
        for column, pandas_type in zip(columns, types)])

    return spark.createDataFrame(pandas_df, p_schema)


def get_distinct_values(spark_df, column_header):
    """
    Get the list of distinct values within a DataFrame column.

    Args:
        spark_df (pyspark.sql.dataframe.DataFrame): data table
        column_header (str): header string for desired column

    Returns:
        list of distinct values from the column
    """
    distinct_values = spark_df.select(column_header).distinct().rdd.flatMap(
        lambda x: x).collect()

    return distinct_values


def get_distinct_values_sql(sql_context, table_name, column_header):
    """
    Get the list of distinct values within a SQL table.

    Args:
        sql_context (pyspark.sql.context.SQLContext): spark SQL context
        table_name (str): table name of column
        column_header (str): header string for desired column

    Returns:
        list of distinct values from the column
    """
    query = f"SELECT DISTINCT {column_header} FROM {table_name}"
    distinct_values = sql_context.sql(query).rdd.flatMap(
        lambda x: x).collect()

    return distinct_values


def convert_timestamp(
        df, column_header, timezone="UTC", new_column_header=None):
    """
    This method will convert an integer column to a timestamp.

    Args:
        df (pyspark.sql.dataframe.DataFrame): dataframe object
        column_header (str): name of column header
        timezone (str): which timezone to convert to
        new_column_header (str): optional new column header for timestamp

    Returns:
        modified DataFrame with converted timestamp column
    """
    if not new_column_header:
        new_column_header = column_header
    # Convert milliseconds to timestamp column
    df = df.withColumn(
        new_column_header,
        psf.to_utc_timestamp(
            psf.from_unixtime(
                psf.col(column_header) / 1000, 'yyyy-MM-dd HH:mm:ss'),
            timezone))

    return df


def convert_to_pandas(spark_df):
    """
    This function will safely convert a spark DataFrame to a pandas DataFrame.

    Source: https://stackoverflow.com/questions/76072664

    Args:
        spark_df (pyspark.sql.dataframe.DataFrame): spark DataFrame

    Returns:
        pandas DataFrame
    """
    # Iterate over columns and convert each timestamp column to a string
    timestamp_cols = []
    for column in spark_df.schema:
        if column.dataType == ps_types.TimestampType():
            # Append column header to list
            timestamp_cols.append(column.name)
            # Set column to string using date_format function
            spark_df = spark_df.withColumn(
                column.name,
                psf.date_format(column.name, "yyyy-MM-dd HH:mm:ss"))
    # Convert to a pandas DataFrame and reset timestamp columns
    pandas_df = spark_df.toPandas()
    for column_header in timestamp_cols:
        pandas_df[column_header] = pandas_df[
            column_header].astype("datetime64[ns]")

    return pandas_df


def save_spark_df_to_s3(
        spark_df, output_location, file_format="csv", separator=",",
        use_pandas=False, header=True, partition_by=[], repartition={},
        replace_where=[], mode="overwrite", max_records_per_file=None,
        exact_records_per_file=None
    ):
    """
    This method will save a Spark DataFrame to a provided s3 location.

    TODO: Break this out and simplify it.

    Args:
        spark_df (pyspark.sql.dataframe.DataFrame):
        output_location (str): output s3 location
        file_format (str): file format to save dataframe to
        separator (str): column delimiter
        use_pandas (bool): whether to convert to pandas and save

    Returns:
        None
    """
    # If the spark DataFrame is small then convert to pandas
    if use_pandas:
        # Convert to pandas
        pandas_df = convert_to_pandas(spark_df)
        # Write result to specified s3 location
        s3_utils.write_pandas_df(
            S3_ACCESS_KEY, S3_SECRET_KEY, output_location, pandas_df,
            file_format=file_format, sep=separator, header=header)
        # Log save information
        logging.info("{row_count} rows unloaded to {output_location}".format(
            row_count=pandas_df.shape[0], output_location=output_location))
    # Otherwise, use spark to write
    else:
        # If exact number of records per file is passed, find number of
        # partitions needed to accomplish this
        if exact_records_per_file is not None:
            # If 0 or less this is invalid
            if exact_records_per_file <= 0:
                print("Invalid exact number of records per file provided.")
            # Otherwise get the number of partitions by dividing the number of
            # total records by the number of records per file
            else:
                total_records = spark_df.count()
                repartition["n_partitions"] = round(
                    total_records / exact_records_per_file)
        # Repartition result DataFrame provided arguments
        if repartition:
            args = []
            # Add number of partitions first if applicable
            if "n_partitions" in repartition:
                args.append(repartition["n_partitions"])
            # Add columns headers if applicable
            if "column_headers" in repartition:
                args += [psf.col(c) for c in repartition["column_headers"]]
            # Repartition
            spark_df = spark_df.repartition(*args)
        # Setup options
        options_dict = {}
        # Setup max records if provided
        if max_records_per_file:
            options_dict["maxRecordsPerFile"] = max_records_per_file
        # Setup general parameters based on output file format
        if file_format in ('parquet', 'delta'):
            options_dict["mergeSchema"] = "true"
            if (
                file_format == 'delta' and
                replace_where and
                mode == 'overwrite'
            ):
                options_dict["replaceWhere"] = " AND ".join(replace_where)
        elif file_format == 'csv':
            options_dict["delimiter"] = separator
            options_dict["header"] = str(header).lower()
        # Write data to s3
        if partition_by:
            spark_df \
                .write \
                .format(file_format) \
                .partitionBy(partition_by) \
                .mode(mode) \
                .options(**options_dict) \
                .save(output_location)
        else:
            spark_df \
                .write \
                .format(file_format) \
                .mode(mode) \
                .options(**options_dict) \
                .save(output_location)
        # Log output location
        logging.info(f"Data unloaded to {output_location}")

    return
