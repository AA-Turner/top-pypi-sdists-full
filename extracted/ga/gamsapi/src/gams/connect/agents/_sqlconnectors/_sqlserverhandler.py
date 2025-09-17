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


class SQLServerConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default", "bulkInsert", "bcp"]
    QUOTE_CHAR = ["``"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:

        import pymssql as sql

        self._bcp_credentials = connection_details
        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

    def create_transaction(self):
        """sqlserver is transaction safe.
        Any change within a transaction does not get committed in case of a failure."""
        pass

    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        tableExists = False

        # striping escape characters is not required. SQLSServer is insensitive to use of escape character.
        qualified_table_name = f"{schema}.{tableName}" if schema else tableName

        query = f"""SELECT OBJECT_ID('{qualified_table_name}', 'U') AS ObjectID;"""
        self._conn.execute(query)
        res = self._conn.fetchone()
        # TODO: check for SQLSERVER type(res)
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
                tableCols += f"[{col}] FLOAT,"
            elif dtype == "int64":
                tableCols += f"[{col}] BIGINT,"
            elif dtype in ["object", "category"]:
                tableCols += f"[{col}] VARCHAR(255),"

        tableCols = tableCols[:-1]

        if schema:
            tableName = schema + "." + tableName

        if ifExists == "replace":
            try:
                self._conn.execute(
                    f"""IF OBJECT_ID('{tableName}', 'U') IS NOT NULL DROP TABLE {tableName};"""
                )
            except Exception as e:
                self._raise_error(
                    f"Cannot drop table >{tableName}<.\nException from {type(e).__module__}: {type(e).__name__}> {e}"
                )

        self._conn.execute(f"""CREATE TABLE {tableName}({tableCols});""")
        if self._traceValue > 1:
            self._traceLog(
                f"Created new table: >{tableName}< with columns: >{tableCols}<"
            )

    def _write_file_to_sqlserver(
        self, df: pd.DataFrame, tableName: str, insertMethod: str
    ):
        """
        Function to import data from file to SQL Server DBMS:
            - `bcp`, uses the bulk-copy-program utility to import a txt file given the following exists on the system. 1)bcp utility, 2)Relevant ODBC driver. This works when operating on a remote dbms server.
            - `bulkInsert`, uses the `BULK INSERT` query to import a csv file. Does not work if operating on a Remote DBMS server.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdirname:
            with tempfile.NamedTemporaryFile(
                mode="w", dir=tmpdirname, delete=False, suffix=".csv"
            ) as fp:
                df.to_csv(fp.name, index=False, header=False)
                fp.flush()
                fp.seek(0)
                fp.close()
                if insertMethod == "bulkInsert":
                    self._conn.execute(
                        f"""BULK INSERT {tableName}
                            FROM "{fp.name}"
                            WITH (FORMAT = 'CSV', FIRSTROW = 1,KEEPIDENTITY)"""
                    )
                elif insertMethod == "bcp":
                    from shutil import which
                    from subprocess import PIPE, run

                    self._engine.commit()  # this requires the table to be commited and present in the database. Only then we can start a new transaction.
                    cmd = f"""bcp {tableName} in "{fp.name}" -U "{self._bcp_credentials['user']}" -P "{self._bcp_credentials['password']}" -S "{self._bcp_credentials['host']},{self._bcp_credentials['port']}" -q -c -t "," -d {self._bcp_credentials['database']}"""
                    if self._traceValue > 1:
                        self._traceLog(f"Command to be executed: {cmd}\n")
                    if which(
                        "bcp"
                    ):  # check if bcp is present on the system, returns path if present else None
                        cmd_res = run(
                            cmd,
                            stdout=PIPE,
                            stderr=PIPE,
                            universal_newlines=True,
                            shell=True,
                        )  # shell=True is required for successful run on Linux
                        if cmd_res.returncode != 0:
                            self._raise_error(
                                f"Error occured while running bcp utility.\n {cmd_res.stdout}"
                            )
                    else:
                        self._raise_error("bcp utility not found on the system.")

    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict):
        tableName = writeFunction_args["name"]
        insertMethod = writeFunction_args["insertMethod"]

        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName

        if insertMethod == "default":
            placeHolder = "%s," * (len(df.columns) - 1)
            if df.isnull().values.any():  # replace NaN with None, for SQL NULL
                df = df.astype(object).where(pd.notnull(df), None)
            df_list = list(
                df.itertuples(index=False, name=None)
            )  # sql server does not accept nested lists, it has to be tuples
            query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "%s)"
            if len(df_list) > 0:
                self._conn.executemany(query, df_list)  # type: ignore

            elif self._traceValue > 1:
                self._traceLog(
                    f"Empty symbol. No rows were inserted in table >{tableName}<."
                )
        elif insertMethod in ["bulkInsert", "bcp"]:
            self._write_file_to_sqlserver(
                df=df, tableName=tableName, insertMethod=insertMethod
            )
