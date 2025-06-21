import re
import psycopg2
import psycopg2.extras as extras
import psycopg2.sql as sql
import pandas as pd
import numpy as np
import os
from psycopg2.extensions import register_adapter, AsIs

register_adapter(np.int64, AsIs)


def connect(params_dic):
    """Connect to the PostgreSQL database server"""

    conn = psycopg2.connect(params_dic)
    return conn


def insert_batch(
    conn, dbLlist, table, onconflict="", page_size=100, default_commit=True
):
    """
    Using psycopg2.extras.execute_batch() to insert the dataframe
    """

    df = pd.DataFrame(dbLlist)
    df = df.replace({np.nan: None})
    tuples = [tuple(x) for x in df.to_numpy()]

    list_cols = list(df.columns)

    for index, item in enumerate(list_cols):
        if "/" in item:
            list_cols[index] = f'"{list_cols[index].lower()}"'

    cols = ",".join(list_cols)
    query_placeholders = ", ".join(["%s"] * len(list_cols))

    detect_sql_injection(table)
    detect_sql_injection(cols)
    detect_sql_injection(query_placeholders)

    query = "INSERT INTO %s(%s) VALUES(%s) %s" % (
        table,
        cols,
        query_placeholders,
        onconflict,
    )
    cursor = conn.cursor()

    try:
        extras.execute_batch(cursor, query, tuples, page_size)
        if default_commit:
            conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        if default_commit:
            conn.rollback()
        cursor.close()
        raise error


def copy(
    conn,
    table_name,
    copy_list,
    file_name="copy_temp_file.csv",
    copy_config=None,
    default_commit=True,
):
    if file_name == 'copy_temp_file.csv':
        random = np.random.randint(0, 100000)
        file_name = f"copy_temp_file_{random}.csv"
    
    if os.path.exists(file_name) and os.path.isfile(file_name):
        os.remove(file_name)

    df = pd.DataFrame(copy_list)
    if copy_config is not None:
        if copy_config["force_columns_to_int"] is not None:
            for col in copy_config["force_columns_to_int"]:
                df[col] = df[col].astype(float).astype("Int64")

    df = df.replace({np.nan: None})
    cols = ",".join(list(df.columns))
    df.to_csv(file_name, index=False, header=False, sep=";")
    cursor = conn.cursor()

    detect_sql_injection(table_name)
    detect_sql_injection(cols)

    try:
        with open(file_name, encoding="utf8") as f:
            cursor.copy_expert(
                "COPY %s (%s) FROM STDIN DELIMITER as ';' NULL as ''"
                % (table_name, cols),
                f,
            )
        if default_commit:
            conn.commit()
        cursor.close()
        os.remove(file_name)
    except (Exception, psycopg2.DatabaseError) as error:
        if default_commit:
            conn.rollback()
        cursor.close()
        raise error


def select(conn, str, params=None):
    cur = conn.cursor()
    try:
        cur.execute(str, params)
        row = cur.fetchall()
        cur.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        cur.close()
        raise error


def execute(conn, str, default_commit=True, params=None):
    cur = conn.cursor()
    try:
        cur.execute(str, params)
        if default_commit:
            conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        if default_commit:
            conn.rollback()
        cur.close()
        raise error
    
def execute_vacuum(conn, table_name, full = False):
    cur = conn.cursor()
    try:
        detect_sql_injection(table_name)
        conn.autocommit = True
        if full is True:
            cur.execute(f"VACUUM FULL {table_name};")
        else:
            cur.execute(f"VACUUM {table_name};")
        conn.autocommit = False
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.autocommit = False
        cur.close()
        raise error
    
def detect_sql_injection(input_string):
    if not input_string or not isinstance(input_string, str):
        return False 

    sql_patterns = [
        r"(--|\#|\/\*)",  # Comments SQL
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|GRANT|REVOKE|TRUNCATE)\b)",  # Danger Commands SQL
        r"(\b(OR|AND)\b\s*\d?\s*=\s*\d?)",  # Conditions booleans like OR 1=1
        r"(\bUNION\b.*\bSELECT\b)",  # Attacks like UNION SELECT
        r"('.+--)",  # "" before comments""
        r"([\"']\s*OR\s*[\"']?\d+=[\"']?\d+)",  # Injection OR '1'='1'
        r"(\bEXEC\s*\()",  # Remote execution
    ]

    normalized_string = input_string.lower().strip()

    for pattern in sql_patterns:
        if re.search(pattern, normalized_string, re.IGNORECASE):
            raise ValueError("SQL Injection detected")
        

    return input_string
