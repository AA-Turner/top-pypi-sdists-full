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


class AccessConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default", "bulkInsert"]
    QUOTE_CHAR = ["[]", '""', "``"]

    @staticmethod
    def _create_accdb(dbpath):
        """
        Creates an MS-Access (.accdb) file/database at provided dbpath.
        """
        import win32com.client as win32

        Access = win32.Dispatch("Access.Application")
        Access.NewCurrentDataBase(dbpath)
        Access.CloseCurrentDataBase()
        Access.Quit()  # required in order to remove access application from python memory
        del Access

    def connect(self, connection_details, connection_args, **kwargs) -> None:
        import pyodbc as sql

        isWrite: bool = kwargs.get("isWrite", True)

        if isWrite:
            from pathlib import Path

            if not Path(
                connection_details["DBQ"]
            ).is_file():  # if .accdb file does not exist at the provided loc in DBQ, then create a new .accdb file
                self._create_accdb(dbpath=connection_details["DBQ"])
                if self._traceValue > 1:
                    self._traceLog(
                        f'Created a new .accdb file: >{connection_details["DBQ"]}<'
                    )
        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

    def create_transaction(self):
        """AccessConnector utilizes PyODBC to connect to the database file.
        Therefore, autocommit can be enabled via the connection dictionary."""
        pass

    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        tableExists = False
        rawTableName = self._strip_escape_chars(
            tableName=tableName, quote_chars=self.QUOTE_CHAR
        )
        for ele in self._conn.tables().fetchall():
            if ele[2].lower() == rawTableName.lower():
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
                if self._check_table_exists(tableName, schema=None):
                    self._conn.execute(f"""DROP TABLE {tableName};""")
            except Exception as e:
                self._raise_error(
                    f"Cannot drop table >{tableName}<.\nException from {type(e).__module__}: {type(e).__name__}> {e}"
                )

        self._conn.execute(f"""CREATE TABLE {tableName}({tableCols});""")
        if self._traceValue > 1:
            self._traceLog(
                f"Created new table: >{tableName}< with columns: >{tableCols}<"
            )

    def _execute_write(self, df: pd.DataFrame, writeFunction_args: dict):
        insertMethod = writeFunction_args["insertMethod"]

        if insertMethod == "default":
            return super()._execute_write(df, writeFunction_args)
        elif insertMethod == "bulkInsert":
            self._write_file_to_access(
                df=df,
                tableName=writeFunction_args["name"],
                ifExists=writeFunction_args["if_exists"],
            )

    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict):
        tableName = writeFunction_args["name"]
        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName

        placeHolder = "?," * (len(df.columns) - 1)
        if df.isnull().values.any():  # replace NaN with None, for SQL NULL
            df = df.astype(object).where(pd.notnull(df), None)
        df_list = list(
            df.itertuples(index=False, name=None)
        )  # sql server does not accept nested lists, it has to be tuples

        query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "?)"
        if len(df_list) > 0:
            self._conn.executemany(query, df_list)

        elif self._traceValue > 1:
            self._traceLog(
                f"Empty symbol. No rows were inserted in table >{tableName}<."
            )

    def _write_file_to_access(self, df: pd.DataFrame, tableName: str, ifExists: str):
        """
        Uses MS-Access' make-table query to create a new table from csv.
        This does not require the table to be present in the database file.
        Thus, `ifExists` behavior changes accordingly.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdirname:
            with tempfile.NamedTemporaryFile(
                mode="w", dir=tmpdirname, delete=False, suffix=".csv"
            ) as fp:
                df.to_csv(fp.name, index=False)
                fp.flush()
                fp.seek(0)
                fp.close()
                filename = fp.name.split("\\")[-1]
                if ifExists == "replace":
                    try:
                        # DROP TABLE IF EXISTS ELSE PASS
                        self._conn.execute(f"""DROP TABLE {tableName};""")
                    except:
                        pass
                    self._conn.execute(
                        f"SELECT * INTO [{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                        + f"Database={tmpdirname}].{filename};"
                    )
                elif (
                    ifExists == "append"
                ):  # creates a temp table `randomTemp_<tableName>` in the same db file, inserts the result of newly created temp table into the existing table
                    if self._check_table_exists(tableName, schema=None):
                        self._conn.execute(
                            f"SELECT * INTO [randomTemp_{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                        self._conn.execute(
                            f"INSERT INTO {tableName} SELECT * FROM [randomTemp_{tableName}];"
                        )
                        self._conn.execute(f"DROP TABLE [randomTemp_{tableName}];")
                    else:
                        self._raise_error(
                            f"Table >{tableName}< does not exists and ifExists is set to `append`."
                        )
                elif ifExists == "fail":
                    if not self._check_table_exists(tableName, schema=None):
                        self._conn.execute(
                            f"SELECT * INTO [{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                    else:
                        self._raise_error(
                            f"Table >{tableName}< already exist and ifExists is set to `fail`."
                        )

    def close(self):
        self._conn.close()
        self._engine.close()
