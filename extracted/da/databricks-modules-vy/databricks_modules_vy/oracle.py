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
def oracle_table(system, tablename, schema=None):
    jdbc_url = oracle_jdbc_url(system)
    lp(f"jdbc_url: {jdbc_url}")
    lp(f"tablename: {tablename}")
    if schema:
        return (
            spark.read.format("jdbc")
            .options(
                driver="oracle.jdbc.driver.OracleDriver",
                url=jdbc_url,
                dbtable=tablename,
                customSchema=schema,
            )
            .load()
        )
    else:
        return (
            spark.read.format("jdbc")
            .options(driver="oracle.jdbc.driver.OracleDriver", url=jdbc_url, dbtable=tablename)
            .load()
        )


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
def oracle_query(system, query, schema=None):
    lp(query)
    try:
        df = oracle_table(system, f"({query}) CTE", schema)
    except Exception as e:
        print(f"Exception: {e}")
        if "java.sql.SQLRecoverableException" in str(e):
            SLEEP_TIME_IN_MINUTES = 10
            print(
                f"Got a SQLRecoverableException, will try again after {SLEEP_TIME_IN_MINUTES} minutes"
            )
            time.sleep(SLEEP_TIME_IN_MINUTES * 60)

            df = oracle_table(system, f"({query}) CTE", schema)
        else:
            raise

    return df