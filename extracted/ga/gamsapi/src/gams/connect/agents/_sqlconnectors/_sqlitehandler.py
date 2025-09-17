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
from gams import transfer as gt
from gams.connect.agents._sqlconnectors._databasehandler import DatabaseConnector


class SQLiteConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default"]
    QUOTE_CHAR = ["[]", '""', "``"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:

        import sqlite3 as sql

        isWrite: bool = kwargs.get("isWrite", True)
        self._globalCommit: bool = kwargs.get("_sqlitewrite_globalCommit", False)
        self._smallFlag: bool = kwargs.get("small", False)
        self._fastFlag: bool = kwargs.get("fast", False)

        if isWrite:
            from pathlib import Path

            if self._smallFlag and Path(connection_details["database"]).is_file():
                self._raise_error(
                    f"SQLite database file >{connection_details['database']}< already exists.\
                        Option small can only be enabled when writing a new SQLite database file."
                )

        self._engine = sql.connect(**connection_details, **connection_args)
        self._conn = self._engine.cursor()

        if self._fastFlag and isWrite:
            self._special_pragma_control()

    def _special_pragma_control(self):
        ### Needs to be done before the beginning of a transaction
        ### Tried the following PRAGMAs but little to no effect:
        ### PRAGMA threads = 8; SQLite 3.15+
        ### PRAGMA cache_size = -200000;
        ### PRAGMA temp_store = MEMORY; for temporary objects
        self._conn.execute("PRAGMA synchronous = OFF;")
        self._conn.execute("PRAGMA journal_mode = OFF;")

    def create_transaction(self) -> None:
        self._conn.execute("BEGIN")

    def _check_table_exists(self, tableName: str, schema: str | None) -> bool:
        tableExists = False
        rawTableName = self._strip_escape_chars(
            tableName=tableName, quote_chars=self.QUOTE_CHAR
        )
        query = f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{rawTableName}'"""
        self._conn.execute(query)

        res = self._conn.fetchone()

        # TODO: check type(res) for sqlite
        ### res can be = (obj,) | None | (None,)
        if isinstance(res, tuple):
            if res[0]:
                tableExists = True

        return tableExists

    def _sqlite_create_uel_table(self, cc: gt.Container):
        """
        Fetches the UELs in use for each symbol and creates a mapping from each UEL to an integer.
        The UELs are then renamed to their corresponding integer mappings.
        This function is SQLite specific and is called only when small=True.

        Parameter:
            cc (gt.Container): The input gt.Container containing symbols and UELs to process.
        """
        uel_list = cc.getUELs(ignore_unused=True)
        uel_list = pd.Series(
            data=[str(i) for i in range(1, len(uel_list) + 1)], index=uel_list
        )
        cc.renameUELs(uel_list.to_dict(), allow_merge=True)
        self._uel_table_df = uel_list.reset_index()
        self._uel_table_df.columns = ["uni", "element_text"]

    def _sqlite_create_view(self, viewName, dim, df_cols):
        """
        Creates user-friendly SQL views with the same name as the original table provided for the symbols.
        If the column headers are part of the UEL table, they are mapped to their corresponding names in the views.
        This function is SQLite specific and is called only when small=True.

        Parameter:
            viewName (str)  : The original table name to be used as the name for the view.
            dim (int)       : Dimension of the symbol
            df_cols (list)  : Columns of the symbol
        """
        cols_to_match = df_cols[:dim]
        numeric_cols = {ele: ele for ele in df_cols[dim:]}
        match_headers = self._uel_table_df[
            self._uel_table_df["element_text"].isin(numeric_cols.keys())
        ]
        match_headers = match_headers.set_index("element_text")["uni"].to_dict()
        numeric_cols.update(match_headers)
        tableName = f"[{viewName}$]"
        select_query = ", ".join(
            [f"UEL{i}.[uni] AS [{ele}]" for i, ele in enumerate(cols_to_match, 1)]
            + [
                f"{tableName}.[{key}] AS [{col_name}]"
                for key, col_name in numeric_cols.items()
            ]
        )
        join_query = "".join(
            [
                f"\nINNER JOIN [UEL$] AS UEL{i} ON {tableName}.[{ele}] = UEL{i}.[element_text]"
                for i, ele in enumerate(cols_to_match, 1)
            ]
        )
        final_query = f"CREATE VIEW [{viewName}] AS SELECT {select_query} FROM {tableName} {join_query};"
        try:
            self._conn.execute(f"DROP VIEW IF EXISTS [{viewName}];")
            self._conn.execute(final_query)
        except Exception as e:
            self._raise_error(f"{e}")

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

        if tableName == "[UEL$]":
            self._conn.execute(
                """CREATE TABLE [UEL$]( uni TEXT, element_text INTEGER PRIMARY KEY ASC);"""
            )

            if self._traceValue > 1:
                self._traceLog(f"Created new table: >{tableName}<.")
        else:
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
        placeHolder = "?," * (len(df.columns) - 1)
        tableName = writeFunction_args["name"]
        if df.isnull().values.any():  # replace NaN with None, for SQL NULL
            df = df.astype(object).where(pd.notnull(df), None)
        df_list = list(
            df.itertuples(index=False, name=None)
        )  # sql server does not accept nested lists, it has to be tuples
        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName
        query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "?)"
        if len(df_list) > 0:
            self._conn.executemany(query, df_list)

        elif self._traceValue > 1:
            self._traceLog(
                f"Empty symbol. No rows were inserted in table >{tableName}<."
            )

    def pre_write_procedures(self, **kwargs) -> gt.Container:
        try:
            container = kwargs["container"]
            directory = kwargs["directory"]
            sym_list = kwargs["sym_list"]
        except KeyError as e:
            self._raise_error(f"Key error in pre_write_procedures: {e}.")

        if self._smallFlag:
            write_container = gt.Container(system_directory=directory)
            write_container.read(container, symbols=sym_list)
            self._conn.execute("PRAGMA page_size = 1024;")
            self._sqlite_create_uel_table(cc=write_container)
            self._create_table(
                df=self._uel_table_df,
                tableName="[UEL$]",
                schema=None,
                ifExists="fail",
            )
            self._insert_data(
                df=self._uel_table_df,
                writeFunction_args={
                    "name": "[UEL$]",
                    "schema": None,
                },
            )
            if not self._globalCommit:
                self._engine.commit()

            return write_container

        elif self._check_table_exists(tableName="UEL$", schema=None):
            message = (
                "WARNING: The table >UEL$< already exists in the database file. "
                "It appears that the database was created with the small option enabled. "
                "Appending to or replacing a pre-existing table may lead to unexpected results."
            )
            self._traceLog(message)

        return container

    def post_write_procedures(self, **kwargs) -> None:
        tableName = kwargs["tableName"]
        dim_after_unstack = kwargs["dim_after_unstack"]
        colList = kwargs["colList"]
        dim = kwargs["dim"]
        # After the parent tables <tableName$> are created. Views for the symbol name are to be created.
        if self._smallFlag and dim > 0:
            self._sqlite_create_view(
                viewName=tableName, dim=dim_after_unstack, df_cols=colList
            )
