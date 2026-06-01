import time

from .logging import lp
from pyspark.sql import DataFrame, SparkSession
from pyspark.dbutils import DBUtils

spark = SparkSession.builder.appName("module").getOrCreate()
dbutils = DBUtils(spark)


def oracle_jdbc_url(system):
    str_oracle_system = f"ORACLE_{system}"
    USERNAME = dbutils.secrets.get(str_oracle_system, "username")
    PASSWORD = dbutils.secrets.get(str_oracle_system, "password")
    HOSTNAME = dbutils.secrets.get(str_oracle_system, "hostname")
    JDBC_PORT = dbutils.secrets.get(str_oracle_system, "jdbc_port")
    SID = dbutils.secrets.get(str_oracle_system, "sid")
    return f"jdbc:oracle:thin:{USERNAME}/{PASSWORD}@{HOSTNAME}:{JDBC_PORT}:{SID}"


# Common read table function
def oracle_table(
    system, 
    tablename, 
    schema=None,
    *,
    partition_column=None,
    lower_bound=None,
    upper_bound=None,
    num_partitions=None,
    fetch_size=None,
):
    jdbc_url = oracle_jdbc_url(system)
    lp(f"jdbc_url: {jdbc_url}")
    lp(f"tablename: {tablename}")

    reader = (
        spark.read.format("jdbc")
        .option("driver", "oracle.jdbc.driver.OracleDriver")
        .option("url", jdbc_url)
        .option("dbtable", tablename)
    )

    if schema:
        reader = reader.option("customSchema", schema)

    if (
        partition_column is not None
        and lower_bound is not None
        and upper_bound is not None
        and num_partitions is not None
    ):
        reader = (
            reader.option("partitionColumn", partition_column)
            .option("lowerBound", lower_bound)
            .option("upperBound", upper_bound)
            .option("numPartitions", num_partitions)
        )

    if fetch_size is not None:
        reader = reader.option("fetchSize", fetch_size)

    return reader.load()



# Writes a new table to Oracle. Creates the table if it does not exist.
def write_to_oracle(self, system, table_name, mode="overwrite"):
    jdbc_url = oracle_jdbc_url(system)

    try:
        self.write.mode(mode).format("jdbc").options(
            driver="oracle.jdbc.driver.OracleDriver", url=jdbc_url, dbtable=table_name
        ).save()
    except Exception as e:
        print(f"Exception: {e}")
        if "java.sql.SQLRecoverableException" in str(e):
            SLEEP_TIME_IN_MINUTES = 10
            print(
                f"Got a SQLRecoverableException, will try again after {SLEEP_TIME_IN_MINUTES} minutes"
            )
            time.sleep(SLEEP_TIME_IN_MINUTES * 60)

            self.write.mode(mode).format("jdbc").options(
                driver="oracle.jdbc.driver.OracleDriver", url=jdbc_url, dbtable=table_name
            ).save()
        else:
            raise


# A query sent to jdbc by wrapping it in an CTE and send the query with the parameter "dbtable"

def oracle_query(
    system: str,
    query: str,
    schema: str | None = None,
    *,
    partition_column: str | None = None,
    lower_bound: int | None = None,
    upper_bound: int | None = None,
    num_partitions: int | None = None,
    fetch_size: int | None = None,
) -> DataFrame:
    """
    Run an Oracle query via JDBC and return a DataFrame.

    The query is wrapped as a subquery and passed as the `dbtable` argument to JDBC.
    Additional JDBC tuning parameters (partitioning, fetch_size) are optional and
    forwarded to `oracle_table`.

    Args:
        system: Oracle system key, e.g. 'DATAMART_PROD'.
        query: SQL query string to execute in Oracle.
        schema: Optional Spark schema string (customSchema).
        partition_column: Column used for JDBC partitioning.
        lower_bound: Inclusive lower bound for partition_column.
        upper_bound: Exclusive upper bound for partition_column.
        num_partitions: Number of JDBC partitions to create.
        fetch_size: JDBC fetchSize hint (rows per batch).

    Returns:
        A Spark DataFrame containing the query result.
    """
    lp(query)
    dbtable = f"({query}) CTE"

    try:
        df = oracle_table(
            system=system,
            tablename=dbtable,
            schema=schema,
            partition_column=partition_column,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            num_partitions=num_partitions,
            fetch_size=fetch_size,
        )
    except Exception as e:
        print(f"Exception: {e}")
        if "java.sql.SQLRecoverableException" in str(e):
            SLEEP_TIME_IN_MINUTES = 10
            print(
                f"Got a SQLRecoverableException, will try again after "
                f"{SLEEP_TIME_IN_MINUTES} minutes"
            )
            time.sleep(SLEEP_TIME_IN_MINUTES * 60)

            df = oracle_table(
                system=system,
                tablename=dbtable,
                schema=schema,
                partition_column=partition_column,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                num_partitions=num_partitions,
                fetch_size=fetch_size,
            )
        else:
            raise

    return df
