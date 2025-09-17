#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2025 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2025 GAMS Software GmbH <support@gams.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import pandas as pd
from gams.connect.agents._sqlconnectors._databasehandler import DatabaseConnector


class PostgresConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default", "bulkInsert"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:

        import psycopg2 as sql

        if kwargs.get("isWrite", True):
            # autocommit is relevant only for SQLWriter
            self._pg_autocommit = connection_args.pop("autocommit", False)

        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

    def create_transaction(self):
        self._engine.autocommit = self._pg_autocommit

    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        tableExists = False

        # striping escape characters is not required. SQLSServer is insensitive to use of escape character.
        qualified_table_name = f"{schema}.{tableName}" if schema else tableName

        query = f"""SELECT to_regclass('{qualified_table_name}')"""
        self._conn.execute(query)
        res = self._conn.fetchone()
        # TODO: check for POSTGRES type(res)
        ### res can be = (obj,) | None | (None,)
        if isinstance(res, tuple):
            if res[0]:
                tableExists = True

        return tableExists

    def _create_table(
        self,
        df: pd.DataFrame,
        tableName: str,
        schema: str | None,
        ifExists: str,
        **kwargs,
    ) -> None:
        """
        Drops an exisiting table and creates a new table with the same name. Uses specific SQL queries for each DBMS flavour.
        """
        tableCols = ""
        for col, dtype in df.dtypes.items():
            if dtype == "float64":
                tableCols += f'"{col}" FLOAT,'
            elif dtype == "int64":
                tableCols += f'"{col}" BIGINT,'
            elif dtype in ["object", "category"]:
                tableCols += f'"{col}" TEXT,'

        tableCols = tableCols[:-1]

        if schema:
            tableName = schema + "." + tableName

        if ifExists == "replace":
            try:
                self._conn.execute(f"""DROP TABLE IF EXISTS {tableName};""")
            except Exception as e:
                self._raise_error(
                    f"Cannot drop table >{tableName}<.\nException from {type(e).__module__}: {type(e).__name__}> {e}"
                )

        self._conn.execute(f"""CREATE TABLE {tableName}({tableCols});""")
        if self._traceValue > 1:
            self._traceLog(
                f"Created new table: >{tableName}< with columns: >{tableCols}<"
            )

    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict):
        """
        default: uses .execute_batch with page_size=100 (fixed and default)
        bulkInsert: uses the .copy_expert method to stream a csv file into the DB
        """
        tableName = writeFunction_args["name"]
        insertMethod = writeFunction_args["insertMethod"]

        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName

        if insertMethod == "bulkInsert":
            import io

            s_buf = io.StringIO()
            df.to_csv(s_buf, index=False, header=False)
            s_buf.seek(0)
            colNames = ", ".join(f'"{ele}"' for ele in df.columns)
            query = f"""COPY {tableName} ({colNames}) FROM STDIN WITH CSV"""
            self._conn.copy_expert(query, file=s_buf)
        elif insertMethod == "default":
            from psycopg2.extras import execute_batch

            placeHolder = "%s," * (len(df.columns) - 1)
            query = f"INSERT INTO  {tableName} VALUES(" + placeHolder + "%s)"
            if df.isnull().values.any():  # replace NaN with None, for SQL NULL
                df = df.astype(object).where(pd.notnull(df), None)
            df_list = df.values.tolist()
            execute_batch(self._conn, query, df_list)
