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


class MySQLConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default", "bulkInsert"]
    QUOTE_CHAR = ["``"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:
        import pymysql as sql

        isWrite: bool = kwargs.get("isWrite", True)

        if isWrite:
            connection_args.update(
                {"local_infile": True}
            )  # set local_infile to true for bulkInsert symbol option when writing

        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

    def create_transaction(self):
        """DDL is autocommitted and as a result all the changes made till then also get committed"""
        pass

    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        tableExists = False
        rawTableName = self._strip_escape_chars(
            tableName=tableName, quote_chars=self.QUOTE_CHAR
        )
        query = f"""SELECT table_name FROM information_schema.tables WHERE table_name = '{rawTableName}'"""
        query += f"""AND table_schema = '{schema}';""" if schema else ";"

        self._conn.execute(query)

        res = self._conn.fetchone()

        # TODO: check type(res) for mysql
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
                tableCols += f"`{col}` DOUBLE,"
            elif dtype == "int64":
                tableCols += f"`{col}` BIGINT,"
            elif dtype in ["object", "category"]:
                tableCols += f"`{col}` TEXT,"

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

    def _write_file_to_mysql(self, df: pd.DataFrame, tableName: str):
        """
        Function to import data from file to MySQL DBMS
        Uses `LOAD DATA LOCAL INFILE` query to import csv, provided the infile option (OPT_LOCAL_INFILE = 1) is enabled in the DBMS
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

                import sys

                filepath = fp.name.replace("\\", "/")
                setVals = ", ".join(["@" + str(i + 1) for i in range(len(df.columns))])
                linending = "\r\n" if sys.platform == "win32" else "\n"
                query = f"""LOAD DATA LOCAL INFILE "{filepath}" INTO TABLE {tableName} 
                            FIELDS TERMINATED BY ','
                            ENCLOSED BY '"'
                            LINES TERMINATED BY '{linending}'
                            ({setVals})"""
                set_variables = ", ".join(
                    [
                        "`{0}`=NULLIF(@{1},'')".format(col, i + 1)
                        for i, col in enumerate(df.columns)
                    ]
                )
                query += "SET " + set_variables + ";"
                self._conn.execute(query)

    def _insert_data(self, df: pd.DataFrame, writeFunction_args: dict):
        tableName = writeFunction_args["name"]
        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName

        if writeFunction_args["insertMethod"] == "default":
            placeHolder = "%s," * (len(df.columns) - 1)
            if df.isnull().values.any():  # replace NaN with None, for SQL NULL
                df = df.astype(object).where(pd.notnull(df), None)
            df_list = list(
                df.itertuples(index=False, name=None)
            )  # sql server does not accept nested lists, it has to be tuples
            query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "%s)"

            if len(df_list) > 0:
                self._conn.executemany(query, df_list)

            elif self._traceValue > 1:
                self._traceLog(
                    f"Empty symbol. No rows were inserted in table >{tableName}<."
                )
        elif writeFunction_args["insertMethod"] == "bulkInsert":
            self._write_file_to_mysql(df=df, tableName=tableName)
