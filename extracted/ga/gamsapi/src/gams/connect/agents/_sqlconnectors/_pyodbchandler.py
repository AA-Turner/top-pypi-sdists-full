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


class PyodbcConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default"]
    QUOTE_CHAR = ["[]", '""', "``"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:
        import pyodbc as sql

        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

    def create_transaction(self) -> None:
        """Autocommit = False by default. One can change this directly by setting the option in the >connection< dictionary."""
        pass

    def _check_table_exists(self, tableName, schema):
        tableExists = False
        rawTableName = self._strip_escape_chars(
            tableName=tableName, quote_chars=self.QUOTE_CHAR
        )
        for ele in self._conn.tables().fetchall():
            if ele[2].lower() == rawTableName.lower():
                tableExists = True

        return tableExists

    def _create_table(self, df, tableName, schema, ifExists, **kwargs):
        """
        Drops an exisiting table and creates a new table with the same name. Uses specific SQL queries for each DBMS flavour.
        """
        dtype_map: dict = kwargs["dtype_map"]
        col_encloser: str = kwargs["columnEncloser"]
        tableCols = ""
        for col, dtype in df.dtypes.items():
            new_col = (
                f"{col_encloser[0]}{col}{col_encloser[1]}"
                if len(col_encloser) > 1
                else f"{col_encloser[0]}{col}{col_encloser[0]}"
            )
            if dtype == "float64":
                tableCols += f"{new_col} {dtype_map.get('float', 'FLOAT')},"
            elif dtype == "int64":
                tableCols += f"{new_col} {dtype_map.get('integer', 'BIGINT')},"
            elif dtype in ["object", "category"]:
                tableCols += f"{new_col} {dtype_map.get('text', 'TEXT')},"

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

    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict) -> None:
        placeHolder = "?," * (len(df.columns) - 1)
        tableName = writeFunction_args["name"]
        if df.isnull().values.any():  # replace NaN with None, for SQL NULL
            df = df.astype(object).where(pd.notnull(df), None)
        df_list = list(df.itertuples(index=False, name=None))
        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName
        query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "?)"

        if len(df_list) > 0:
            self._conn.executemany(query, df_list)

        elif self._traceValue > 1:
            self._traceLog(
                f"Empty symbol. No rows were inserted in table >{tableName}<."
            )
