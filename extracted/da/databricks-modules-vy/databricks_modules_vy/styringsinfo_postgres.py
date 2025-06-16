# Necessary imports
from pyspark.sql import DataFrame, SparkSession
from pyspark.dbutils import DBUtils
from datetime import datetime
from .logging import lp
from pyspark.sql.functions import col, current_date, datediff, expr, last_day, to_date
from pyspark.sql import functions as F
from .unity_catalog import uc_table

# Creating a SparkSession
spark = SparkSession.builder.appName("module").getOrCreate()

# Creating a DBUtils object
dbutils = DBUtils(spark)


def get_aws_rds_connection_details(scope: str):
    """
    Returns the AWS RDS connection details based on the provided secret scope.

    Args:
        scope (str): The name of the secret scope.

    Returns:
        tuple: A tuple containing the JDBC URL, username, and password.
    """
    USERNAME = dbutils.secrets.get(scope, "username")
    PASSWORD = dbutils.secrets.get(scope, "password")
    HOSTNAME = dbutils.secrets.get(scope, "hostname")
    PORT = dbutils.secrets.get(scope, "jdbc_port")
    DATABASE = dbutils.secrets.get(scope, "database")
    JDBC_URL = f"jdbc:postgresql://{HOSTNAME}:{PORT}/{DATABASE}"

    return JDBC_URL, USERNAME, PASSWORD


def write_to_postgres(df: DataFrame, table_name: str, scope: str):
    """
    Writes the given DataFrame to the specified table in AWS RDS. Uses mode="overwrite" with truncate for all tables without postfix "_freeze", and uses mode="append" for all tables with postfix "_freeze".

    Args:
        df (DataFrame): The DataFrame to write.
        table_name (str): The name of the table in AWS RDS.
        scope (str): The secret scope to retrieve connection details from.
    """
    # Get the AWS RDS connection details
    JDBC_URL, USERNAME, PASSWORD = get_aws_rds_connection_details(scope)

    # Set the truncate and mode options based on the table name
    if table_name.endswith("_freeze"):
        truncate_option = "false"
        mode = "append"
    else:
        truncate_option = "true"
        mode = "overwrite"

    try:
        # Write DataFrame to AWS RDS
        df.write.mode(mode).format("jdbc").option("truncate", truncate_option).options(
            url=JDBC_URL,
            driver="org.postgresql.Driver",
            dbtable=table_name,
            user=USERNAME,
            password=PASSWORD,
        ).save()
    except Exception as e:
        print(f"Exception: {e}")
        if "java.sql.SQLRecoverableException" in str(e):
            # If SQLRecoverableException occurs, wait and retry after some time
            SLEEP_TIME_IN_MINUTES = 10
            print(
                f"Got a SQLRecoverableException, will try again after {SLEEP_TIME_IN_MINUTES} minutes"
            )
            time.sleep(SLEEP_TIME_IN_MINUTES * 60)

            # Retry writing DataFrame to AWS RDS
            df.write.mode(mode).format("jdbc").option("truncate", truncate_option).options(
                url=JDBC_URL,
                driver="org.postgresql.Driver",
                dbtable=table_name,
                user=USERNAME,
                password=PASSWORD,
            ).save()
        else:
            raise


def write_to_postgres_freeze(df: DataFrame, df_dim: DataFrame, table_name: str, scope: str):
    """
    Writes a subset of rows (the newest freeze data for each KPI) from the provided DataFrame to a separate table, postfixed with "freeze". The function also checks which rows exist in the destination table and only writes the rows that do not exist. This ensures that data for each KPI is only written to the freeze table once per month, when the data for a given KPI is considered to be complete.

    Args:
        df (DataFrame): The DataFrame to write. Same dataframe as the unfrozen dataframe.
        df_dim (DataFrame): The DataFrame holding the freeze date information.
        table_name (str): The name of the freeze table to be populated in AWS RDS.
        scope (str): The secret scope to retrieve connection details from.
    """
    # Calculate the last day of the month and store this in "period_end" column
    df = df.withColumn("period_end", last_day(to_date(col("period_id").cast("string"), "yyyyMM")))

    # Calculate the number of days since the period ended
    df = df.withColumn("days_since_period_end", F.datediff(F.current_date(), F.col("period_end")))

    # Select columns from df_dim and postfix them with _dim
    df_dim_join = df_dim.select(
        col("kpi_id").alias("kpi_id_dim"), col("kpi_freeze_day").alias("kpi_freeze_day_dim")
    )

    # Join the KPI fact DataFrame (df) with the freeze date DataFrame (df_dim) on the specified columns to ensure only data for KPI's where the current date is between the freeze_date and 20 days after is kept. This is done to ensure that only new data is frozen, and that it only happens after the data is ready for freezing. Then drop columns which are no longer needed.

    df = df.join(
        df_dim_join,
        (df["kpi_id"] == df_dim_join["kpi_id_dim"])
        & (expr("days_since_period_end BETWEEN kpi_freeze_day_dim AND kpi_freeze_day_dim + 20")),
        "inner",
    ).drop(
        "kpi_is_current", "kpi_id_dim", "kpi_freeze_day_dim", "period_end", "days_since_period_end"
    )

    # Read existing data from the freeze table
    existing_df = read_from_postgres(table_name, scope)

    # Perform an anti-join to exclude rows that already exist in the database table
    df = df.join(existing_df, on=["kpi_id", "reporting_unit_id", "period_id"], how="anti")

    # Check if df is empty after the anti-join, and skip the write operation if df is empty
    if df.isEmpty():
        print("No new rows to write to the freeze table. The write operation was skipped")
        return

    # Write the filtered DataFrame to the freeze table using the write_to_postgres function
    write_to_postgres(df, table_name, scope)


def read_from_postgres(table_name: str, scope: str) -> DataFrame:
    """
    Reads data from AWS RDS using JDBC.

    Args:
        table_name (str): The name of the table in AWS RDS.
        scope (str): The secret scope to retrieve connection details from.

    Returns:
        DataFrame: The DataFrame containing the data from the table.
    """
    # Get the AWS RDS connection details
    JDBC_URL, USERNAME, PASSWORD = get_aws_rds_connection_details(scope)

    # Create a SparkSession
    spark = SparkSession.builder.getOrCreate()

    # Read data from AWS RDS using JDBC
    df = (
        spark.read.format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", table_name)
        .option("user", USERNAME)
        .option("password", PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .load()
    )

    return df
