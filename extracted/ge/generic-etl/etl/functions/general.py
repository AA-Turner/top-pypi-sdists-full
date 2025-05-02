import logging
import os
import subprocess
from pathlib import Path

import pandas as pd

from etl.utils.database import Database
from etl.utils.exceptions import NotSupported

logger = logging.getLogger(__name__)


def execute_sql(
    connection: str, file_output: str, sql: str, secrets: dict, output: str = "csv", **_
) -> None:
    """Execute SQL

    param :title, str: Title about to be ran
    param :step, Step: Step object
    param :secrets, dict: Connection information
    param :output, str, 'csv': Output file type
    """
    df = None

    with Database(secrets, connection) as database:
        df = database.execute(sql)

    save_frame(df, file_output, output)


def save_frame(df: pd.DataFrame, filename: str, output_type: str = "csv", **_):
    if df is not None:
        p = Path(filename)
        p.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving {filename}")

        if output_type == "csv":
            df.to_csv(filename)
        elif output_type == "hdfs":
            df.to_hdf(filename)
        elif output_type == "parquet":
            df.to_parquet(filename)
        else:
            raise NotSupported(f"{output_type}")


def merge_csv(csv_one: str, csv_two: str, column: str, out: str, **_) -> None:
    """Merges based on the item"""

    one: pd.DataFrame = pd.read_csv(csv_one)
    two: pd.DataFrame = pd.read_csv(csv_two)
    out: pd.DataFrame = pd.merge(one, two, on=column)
    save_frame(out, out, "csv")

    # chunk_container: pd.DataFrame = pd.read_csv("filename", chunksize=5000)
    # for chunk in chunk_container:
    #     chunk.to_csv("output", mode="a", index=False)


def move_frame(
    connection: str,
    target_tables: str,
    target_connection: str,
    schema: str,
    secrets: dict,
    sql: str,
    **_,
) -> None:
    """Moves data from one table to other tables

    param :title, str: Title about to be ran
    param :step, Step: Step object
    param :secrets, dict: Connection information
    """
    with Database(secrets, connection) as source:
        with Database(secrets, target_connection) as target:
            for df_chunk in pd.read_sql_query(sql, source.engine, chunksize=10):
                for table in target_tables:
                    inital = True
                    if inital:
                        target.execute(basic="delete", table=table)
                        inital = False

                    logger.info("Moving data")
                    df_chunk.to_sql(
                        table,
                        target.engine,
                        schema=schema,
                        method="multi",
                        index=False,
                        if_exists="append",
                    )


def sub_run(app: str, io: str) -> None:
    """Runs command on a subprocess

    param :step, Step: Step object
    param :output, str, 'csv': Output file type
    """
    logger.info(subprocess.call([app, io]))
