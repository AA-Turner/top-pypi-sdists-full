from teradataml import DataFrame

from .connections import execute_sql_in_context


def store_byom_tmp(
    context, table: str, model_version: str, model_bytes: bytes
) -> DataFrame:
    """
    Store a byom model in a temporary table so we can use it

    :param context: get_context()
    :param table: temp table name to use
    :param model_version: model version
    :param model_bytes: model bytes
    :return: DataFrame of model
    """
    execute_sql_in_context(
        context,
        f"""
        CREATE VOLATILE TABLE {table}(
            model_id VARCHAR(255),
            model BLOB(2097088000)
        ) ON COMMIT PRESERVE ROWS;
        """,
    )

    execute_sql_in_context(
        context,
        f"INSERT INTO {table}(model_id, model) values(?,?)",
        (model_version, model_bytes),
    )

    return DataFrame.from_query(f"""
        SELECT model_id, model FROM {table} 
            WHERE model_id='{model_version}'
        """)


def check_if_table_exists(context, database: str, name: str, table_kind: str) -> bool:
    """
    Check if the table/view/etc exists in the database

    :param context: sqlalchemy context/engine
    :param database: the database
    :param name: the table/view/etc name
    :param table_kind: 'V' for view, 'T' for table etc.
    :return: (bool) True if exists, False otherwise
    """
    rs = execute_sql_in_context(
        context,
        f"""
    SELECT * FROM DBC.TABLES WHERE 
        TABLENAME ='{name}' AND 
        tablekind = '{table_kind}' AND 
        databasename='{database}'
    """,
    )

    return rs.rowcount >= 1
