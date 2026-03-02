import dlt

from sqlalchemy import create_engine

from dlt.sources.sql_database import sql_table
from dlthub.sources.mssql import (
    create_change_tracking_table,
    get_current_change_tracking_version,
)


def single_table_initial_load(connection_url: str, schema_name: str, table_name: str) -> None:
    """Performs initial full load and sets up tracking version and incremental loads"""
    # Create a new pipeline
    pipeline = dlt.pipeline(
        pipeline_name=f"{schema_name}_{table_name}_sync",
        destination="duckdb",
        dataset_name=schema_name,
    )

    # Explicit database connection
    engine = create_engine(connection_url, isolation_level="SNAPSHOT")

    # Initial full load
    initial_resource = sql_table(
        credentials=engine,
        schema=schema_name,
        table=table_name,
        reflection_level="full",
        write_disposition="merge",
    )

    # Get current tracking version before you run the pipeline to make sure
    # you do not miss any records,
    tracking_version = get_current_change_tracking_version(engine)
    print(f"will track from: {tracking_version}")  # noqa

    # Run the pipeline for initial load
    # NOTE: we always drop data and state from the destination on initial load
    print(pipeline.run(initial_resource, refresh="drop_resources"))  # noqa

    # Incremental loading resource
    incremental_resource = create_change_tracking_table(
        credentials=engine,
        table=table_name,
        schema=schema_name,
        initial_tracking_version=tracking_version,
    )

    # Run the pipeline for incremental load
    print(pipeline.run(incremental_resource))  # noqa


def single_table_incremental_load(connection_url: str, schema_name: str, table_name: str) -> None:
    """Continues loading incrementally"""
    # make sure you use the same pipeline and dataset names in order to continue incremental
    # loading.
    pipeline = dlt.pipeline(
        pipeline_name=f"{schema_name}_{table_name}_sync",
        destination="duckdb",
        dataset_name=schema_name,
    )

    engine = create_engine(connection_url, isolation_level="SNAPSHOT")
    # we do not need to pass tracking version anymore
    incremental_resource = create_change_tracking_table(
        credentials=engine,
        table=table_name,
        schema=schema_name,
    )
    print(pipeline.run(incremental_resource))  # noqa


if __name__ == "__main__":
    # change tracking already enabled here
    test_db = "my_database83ed099d2d98a3ccfa4beae006eea44c"
    # a test run with a local mssql instance
    connection_url = (
        f"mssql+pyodbc://sa:Strong%21Passw0rd@localhost:1433/{test_db}"
        "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    single_table_initial_load(
        connection_url,
        "my_dlt_source",
        "app_user",
    )
    single_table_incremental_load(
        connection_url,
        "my_dlt_source",
        "app_user",
    )
