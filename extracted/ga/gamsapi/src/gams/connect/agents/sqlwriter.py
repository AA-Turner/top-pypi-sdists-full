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

from gams.connect.agents.connectagent import ConnectAgent
from gams.connect.connectvalidator import ConnectValidator
import gams.transfer as gt
import pandas as pd


class SQLWriter(ConnectAgent):

    def __init__(self, cdb, inst, agent_index):
        super().__init__(cdb, inst, agent_index)
        self._parse_options(self._inst)

    def _parse_options(self, inst):
        # global options
        self._input_cnctn = inst["connection"]  # input db credentials/path thru user.
        self._cnctn_type = inst["connectionType"]
        self._connection_args = self._dict_get(inst, "connectionArguments", {})
        self._ifExists = inst["ifExists"]
        self._schema_name = inst["schemaName"]
        self._to_sql_args = inst["toSQLArguments"]
        self._trace = inst["trace"]
        self._insertMethod = inst["insertMethod"]
        self._unstack = inst["unstack"]
        self._value_sub = inst["valueSubstitutions"]
        self._dtype_map = inst["dTypeMap"]
        self._col_encloser = inst["columnEncloser"]
        self._skip_text = inst["skipText"]
        self._fast = (
            False if self._cnctn_type != "sqlite" else inst["fast"]
        )  # NO effect for rest of the connectionTypes
        self._small = (
            False if self._cnctn_type != "sqlite" else inst["small"]
        )  # NO effect for rest of the connectionTypes
        self._symbols = inst["symbols"]  # symbol option
        self._write_all = self._symbols == "all"
        self._sqlitewrite_globalCommit = self._connection_args.pop(
            "__globalCommit__", False
        )

    def _open(self):
        if self._cnctn_type == "sqlalchemy":
            if self._insertMethod == "default":
                import sqlalchemy

                con_str = sqlalchemy.engine.URL.create(**self._input_cnctn)
                self._engine = sqlalchemy.create_engine(
                    con_str, **self._connection_args
                )
                self._conn = self._engine.connect()
            else:
                self._connect_error(
                    f"Use of insertMethod: >{self._insertMethod}< is not supported with SQLALCHEMY."
                )

        else:
            if self._cnctn_type == "pyodbc":
                import pyodbc as sql

            elif self._cnctn_type == "access":
                import pyodbc as sql
                from pathlib import Path

                if not Path(
                    self._input_cnctn["DBQ"]
                ).is_file():  # if .accdb file does not exist at the provided loc in DBQ, then create a new .accdb file
                    self._create_accdb(dbpath=self._input_cnctn["DBQ"])
                    if self._trace > 1:
                        self._cdb.print_log(
                            f'Created a new .accdb file: >{self._input_cnctn["DBQ"]}<'
                        )
            elif self._cnctn_type == "postgres":
                import psycopg2 as sql

                self._pg_autocommit = self._connection_args.pop("autocommit", False)

            elif self._cnctn_type == "mysql":
                import pymysql as sql

                self._connection_args.update(
                    {"local_infile": True}
                )  # set local_infile to true for bulkInsert symbol option
            elif self._cnctn_type == "sqlserver":
                import pymssql as sql
            else:  # sqlite3 by default
                import sqlite3 as sql
                from pathlib import Path

                if self._small and Path(self._input_cnctn["database"]).is_file():
                    self._connect_error(
                        f"SQLite database file >{self._input_cnctn['database']}< already exists. Option small can only be enabled when writing a new SQLite database file."
                    )
            self._engine = sql.connect(**self._input_cnctn, **self._connection_args)
            self._conn = self._engine.cursor()

    def _create_transaction(self):
        """
        Helper function to start a SQL transaction.
        The >connectionTypes< which are not included here start a transaction implicitly.
        This helps in rolling back the changes made within a transaction in the event of a failure.
        This is useful when we commit globally once instead of committing each symbol.

        connectionType:pythonLibrary
            postgres:pyscopg2, mysql:pymysql, sqlserver:pymssql and pyodbc:pyodbc have autocommit = False by default

        mysql:pymysql
            DDL is autocommitted and as a result all the changes made till then also get committed.

        sqlserver:pymssql,postgres:pyscopg2
            postgres and sqlserver are transaction safe.
            Any change within a transaction does not get committed in case of a failure.

        sqlite:sqlite3
            Creates a blank table for the first symbol. Setting the transaction to begin resolves it.
            This also makes sqlite's behavior different when autocommit is True.
            It does not commit anything even when autocommit is True and failure occurs.

        sqlalchemy:sqlalchemy
            follows the default behavior of specific database
        """
        if self._cnctn_type == "sqlalchemy":
            self._conn.begin()

        if self._cnctn_type == "sqlite":
            self._conn.execute("BEGIN")

        if self._cnctn_type == "postgres":
            self._engine.autocommit = self._pg_autocommit

    def _create_new_table(self, df, tableName, schema, dtype_map, ifExists):
        """
        Drops an exisiting table and creates a new table with the same name. Uses specific SQL queries for each DBMS flavour.
        """
        tableCols = ""
        if self._cnctn_type in [
            "access",
            "sqlserver",
            "sqlite",
        ]:  # MS-Access text columns must be of datatype `VARCHAR` & All three should enclose colNames within []
            for col, dtype in df.dtypes.items():
                if dtype == "float64":
                    tableCols += f"[{col}] FLOAT,"
                elif dtype == "int64":
                    tableCols += f"[{col}] BIGINT,"
                elif dtype in ["object", "category"]:
                    tableCols += f"[{col}] VARCHAR(255),"

        elif self._cnctn_type == "mysql":
            for col, dtype in df.dtypes.items():
                if dtype == "float64":
                    tableCols += f"`{col}` DOUBLE,"
                elif dtype == "int64":
                    tableCols += f"`{col}` BIGINT,"
                elif dtype in ["object", "category"]:
                    tableCols += f"`{col}` TEXT,"

        elif self._cnctn_type == "postgres":
            for col, dtype in df.dtypes.items():
                if dtype == "float64":
                    tableCols += f'"{col}" FLOAT,'
                elif dtype == "int64":
                    tableCols += f'"{col}" BIGINT,'
                elif dtype in ["object", "category"]:
                    tableCols += f'"{col}" TEXT,'

        else:  # support for pyodbc
            for col, dtype in df.dtypes.items():
                new_col = (
                    f"{self._col_encloser[0]}{col}{self._col_encloser[1]}"
                    if len(self._col_encloser) > 1
                    else f"{self._col_encloser[0]}{col}{self._col_encloser[0]}"
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
                if self._cnctn_type == "sqlserver":
                    self._conn.execute(
                        f"""IF OBJECT_ID('{tableName}', 'U') IS NOT NULL DROP TABLE {tableName};"""
                    )

                elif self._cnctn_type in ["mysql", "postgres", "sqlite"]:
                    self._conn.execute(f"""DROP TABLE IF EXISTS {tableName};""")

                else:  # for ms-access and pyodbc
                    if self._check_table(tableName, schema=None):
                        self._conn.execute(f"""DROP TABLE {tableName};""")
            except Exception as e:
                self._connect_error(
                    f"Cannot drop table >{tableName}<.\nException from {type(e).__module__}: {type(e).__name__}> {e}"
                )

        if tableName == "[UEL$]":
            self._conn.execute(
                f"""CREATE TABLE [UEL$]( uni TEXT, element_text INTEGER PRIMARY KEY ASC);"""
            )
        else:
            self._conn.execute(f"""CREATE TABLE {tableName}({tableCols});""")
        if self._trace > 1:
            self._cdb.print_log(
                f"Created new table: >{tableName}< with columns: >{tableCols}<"
            )

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

    def _check_table(self, tableName, schema):
        """
        Helper function, returns True if `tableName` already exists in the DBMS.
        """

        def strip_escape_chars(db_type: str, table_name: str):
            """
            Helper function to strip an enclosed `tableName`.
            For example, strip_escape_chars("sqlite", "[new_table]") ==> new_table

            ["mysql","sqlite","access","pyodbc"]:
                These >db_types< are sensitive to the use of escape characters in their SQL queries.
                That is, the query would not find "[new_table]" even if "new_table" exist in the database.

            ["postgres","sqlserver"]:
                These are insensitive to the use of escape characters in the table name.
                The SQL query for both the DBs handle enclosed tableNames efficiently.
            """
            escChar = {
                "mysql": ["``"],
                "sqlite": ["[]", '""', "``"],
                "access": ["[]", '""', "``"],
                "pyodbc": ["[]", '""', "``"],
            }

            if db_type in escChar:
                for esc in escChar[db_type]:
                    if table_name.startswith(esc[0]) and table_name.endswith(esc[-1]):
                        return table_name[1:-1]

            return table_name

        rawTableName = strip_escape_chars(
            db_type=self._cnctn_type, table_name=tableName
        )
        qualified_table_name = f"{schema}.{tableName}" if schema else tableName
        tableExists = False

        queries = {
            "mysql": f"""SELECT table_name FROM information_schema.tables WHERE table_name = '{rawTableName}'""",
            "postgres": f"""SELECT to_regclass('{qualified_table_name}')""",
            "sqlite": f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{rawTableName}'""",
            "sqlserver": f"""SELECT OBJECT_ID('{qualified_table_name}', 'U') AS ObjectID;""",
        }

        queries["mysql"] += f""" AND table_schema = '{schema}';""" if schema else ";"

        if self._cnctn_type in queries:
            self._conn.execute(queries[self._cnctn_type])

        elif self._cnctn_type in ["pyodbc", "access"]:
            for ele in self._conn.tables().fetchall():
                if ele[2].lower() == rawTableName.lower():
                    tableExists = True
            return tableExists

        res = self._conn.fetchone()
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
            self._connect_error(f"{e}")

    def _write_native_sql(self, df, insertMethod, writeFunction_args):
        """
        The default write function when `insertMethod`= `default`.
        Uses the executemany method for inserting the rows in the DBMS.
        Applicable for SQLite, MySQL, SQL-Server, MS-Access and Pyodbc
        """
        placeHolder = "?," * (len(df.columns) - 1)
        tableName = writeFunction_args["name"]
        if df.isnull().values.any():  # replace NaN with None, for SQL NULL
            df = df.astype(object).where(pd.notnull(df), None)
        df_list = list(
            df.itertuples(index=None, name=None)
        )  # sql server does not accept nested lists, it has to be tuples
        if writeFunction_args["schema"]:
            tableName = writeFunction_args["schema"] + "." + tableName
        query = f"INSERT INTO {tableName} VALUES(" + placeHolder + "?)"
        if self._cnctn_type in ["mysql", "sqlserver"]:
            query = query.replace("?", "%s")
        if len(df_list) > 0:
            self._conn.executemany(query, df_list)

        elif self._trace > 1:
            self._cdb.print_log(
                f"Empty symbol. No rows were inserted in table >{tableName}<."
            )

    def _writefile_to_access(self, df, writeFunction_args):
        """
        Uses MS-Access' make-table query to create a new table from csv.
        This does not require the table to be present in the database file.
        Thus, `ifExists` behavior changes accordingly.
        """
        ifExists = writeFunction_args["if_exists"]
        tableName = writeFunction_args["name"]
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
                        self._conn.execute(f"""DROP TABLE {tableName};""")
                        self._conn.execute(
                            f"SELECT * INTO [{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                    except:
                        self._conn.execute(
                            f"SELECT * INTO [{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                elif (
                    ifExists == "append"
                ):  # creates a temp table `randomTemp_<tableName>` in the same db file, inserts the result of newly created temp table into the existing table
                    if self._check_table(tableName, schema=None):
                        self._conn.execute(
                            f"SELECT * INTO [randomTemp_{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                        self._conn.execute(
                            f"INSERT INTO {tableName} SELECT * FROM [randomTemp_{tableName}];"
                        )
                        self._conn.execute(f"DROP TABLE [randomTemp_{tableName}];")
                    else:
                        self._connect_error(
                            f"Table >{tableName}< does not exists and ifExists is set to `append`."
                        )
                elif ifExists == "fail":
                    if not self._check_table(tableName, schema=None):
                        self._conn.execute(
                            f"SELECT * INTO [{tableName}] FROM [text;HDR=Yes;FMT=Delimited(,);"
                            + f"Database={tmpdirname}].{filename};"
                        )
                    else:
                        self._connect_error(
                            f"Table >{tableName}< already exist and ifExists is set to `fail`."
                        )

    def _write_to_postgres(self, df, insertMethod, writeFunction_args):
        """
        Helper function for handling insertion into Postgres DBs.
        default: uses .execute_batch with page_size=100 (fixed and default)
        bulkInsert: uses the .copy_expert method to stream a csv file into the DB
        """
        tableName = writeFunction_args["name"]
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

    def _writefile_to_sql(self, df, insertMethod, writeFunction_args):
        """
        Function to import data from file to MySQL and SQL Server DBMS
        MySQL: uses `LOAD DATA LOCAL INFILE` query to import csv, provided the infile option (OPT_LOCAL_INFILE = 1) is enabled in the DBMS
        SQL Server: `bcp`, uses the bulk-copy-program utility to import a txt file given the following exists on the system. 1)bcp utility, 2)Relevant ODBC driver. This works when operating on a remote dbms server.
                    `bulkInsert`, uses the `BULK INSERT` query to import a csv file. Does not work if operating on a Remote DBMS server.
        """
        import tempfile

        tableName = writeFunction_args["name"]
        with tempfile.TemporaryDirectory() as tmpdirname:
            with tempfile.NamedTemporaryFile(
                mode="w", dir=tmpdirname, delete=False, suffix=".csv"
            ) as fp:
                df.to_csv(fp.name, index=False, header=False)
                fp.flush()
                fp.seek(0)
                fp.close()
                if writeFunction_args["schema"]:
                    tableName = writeFunction_args["schema"] + "." + tableName

                if self._cnctn_type == "mysql":
                    import sys

                    filepath = fp.name.replace("\\", "/")
                    setVals = ", ".join(
                        ["@" + str(i + 1) for i in range(len(df.columns))]
                    )
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
                elif self._cnctn_type == "sqlserver":
                    if insertMethod == "bulkInsert":
                        self._conn.execute(
                            f"""BULK INSERT {tableName}
                                FROM "{fp.name}"
                                WITH (FORMAT = 'CSV', FIRSTROW = 1,KEEPIDENTITY)"""
                        )
                    elif insertMethod == "bcp":
                        from subprocess import run, PIPE
                        from shutil import which

                        self._engine.commit()  # this requires the table to be commited and present in the database. Only then we can start a new transaction.
                        cmd = f"""bcp {tableName} in "{fp.name}" -U "{self._input_cnctn['user']}" -P "{self._input_cnctn['password']}" -S "{self._input_cnctn['host']},{self._input_cnctn['port']}" -q -c -t "," -d {self._input_cnctn['database']}"""
                        if self._trace > 1:
                            self._cdb.print_log(f"Command to be executed: {cmd}\n")
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
                                self._connect_error(
                                    f"Error occured while running bcp utility.\n {cmd_res.stdout}"
                                )
                        else:
                            self._connect_error("bcp utility not found on the system.")

    def _write_sql(
        self,
        df,
        insertMethod,
        to_sql_args,
        writeFunction_args,
    ):
        """
        Main function to process the incoming write request. Depending on the provided `connectionType` and `insertMethod`, dispatches a pre-defined write function.
        """
        if self._cnctn_type == "sqlalchemy":
            if self._trace > 2:
                self._cdb.print_log(f"DataFrame before .to_sql():\n{df}")
            if self._trace > 1:
                self._cdb.print_log(f"to_sql_args: >{to_sql_args}<")
            df.to_sql(con=self._conn, **to_sql_args)

        else:
            if self._trace > 2:
                self._cdb.print_log(f"DataFrame before writing:\n{df}")
            if self._trace > 1:
                self._cdb.print_log(f"writeFunction_args: >{writeFunction_args}<")

            try:
                dispatcher = {
                    "sqlite": {
                        "default": self._write_native_sql,
                    },
                    "postgres": {
                        "default": self._write_to_postgres,
                        "bulkInsert": self._write_to_postgres,
                    },
                    "mysql": {
                        "default": self._write_native_sql,
                        "bulkInsert": self._writefile_to_sql,
                    },
                    "sqlserver": {
                        "default": self._write_native_sql,
                        "bcp": self._writefile_to_sql,
                        "bulkInsert": self._writefile_to_sql,
                    },
                    "pyodbc": {"default": self._write_native_sql},
                    "access": {
                        "default": self._write_native_sql,
                        "bulkInsert": self._writefile_to_access,
                    },
                }
                writeFunction = dispatcher[self._cnctn_type][insertMethod]
            except KeyError as err:
                self._connect_error(
                    f"insertMethod >{err}< is not valid for connection type >{self._cnctn_type}<. Valid insertion methods are >{list(dispatcher[self._cnctn_type].keys())}<"
                )

            tableName = writeFunction_args["name"]
            schema = writeFunction_args["schema"]
            dtype_map = writeFunction_args["dtype_map"]

            if (
                writeFunction.__name__ == "_writefile_to_access"
            ):  # done separately because access has unique `ifexists` methods
                self._writefile_to_access(df, writeFunction_args)
            else:
                if writeFunction_args["if_exists"] == "replace":
                    self._create_new_table(
                        df=df,
                        tableName=tableName,
                        schema=schema,
                        dtype_map=dtype_map,
                        ifExists="replace",
                    )
                    writeFunction(df, insertMethod, writeFunction_args)

                elif writeFunction_args["if_exists"] == "append":
                    if self._check_table(tableName=tableName, schema=schema):
                        writeFunction(df, insertMethod, writeFunction_args)
                    else:
                        self._connect_error(
                            f"Table >{tableName}< does not exist in the database and ifExists is set to >append<."
                        )

                elif writeFunction_args["if_exists"] == "fail":
                    if not self._check_table(tableName=tableName, schema=schema):
                        self._create_new_table(
                            df=df,
                            tableName=tableName,
                            schema=schema,
                            dtype_map=dtype_map,
                            ifExists="fail",
                        )
                        writeFunction(df, insertMethod, writeFunction_args)
                    else:
                        self._connect_error(
                            f"Table >{tableName}< already exists in the database and ifExists is set to >fail<."
                        )

    def execute(self):
        if self._trace > 0:
            self._log_instructions(self._inst, self._inst_raw)
            self._describe_container(self._cdb.container, "Connect Container:")

        self._open()

        try:

            if self._fast:
                ### Needs to be done before the beginning of a transaction
                ### Tried the following PRAGMAs but little to no effect:
                ### PRAGMA threads = 8; SQLite 3.15+
                ### PRAGMA cache_size = -200000;
                ### PRAGMA temp_store = MEMORY; for temporary objects
                self._conn.execute("PRAGMA synchronous = OFF;")
                self._conn.execute("PRAGMA journal_mode = OFF;")

            self._create_transaction()

            if self._write_all:
                self._symbols = []
                sym_schema = self._cdb.load_schema(self)["symbols"]["oneof"][1]["schema"]["schema"]
                v = ConnectValidator(sym_schema)
                for name, sym in self._cdb.container.data.items():
                    if type(sym) in [gt.Set, gt.Parameter]:
                        sym_inst = v.validated({"name": name, "tableName": name})
                        if sym_inst is None:
                            self._connect_error(
                                f"Validation for symbol >{name}< failed: {v.errors}"
                            )
                        sym_inst = v.normalize_of_rules(sym_inst)
                        self._symbols.append(sym_inst)

            symbols_raw = self._symbols.copy()
            sym_list = []
            for s in self._symbols:
                sym_name = s["name"]
                self._symbols_exist_cdb(sym_name, should_exist=True)
                self._update_sym_inst(s, self._inst)
                sym_list.append(s["name"])

            write_container = self._cdb.container
            if self._small:  # Currently only True if cnct_type = "sqlite"
                write_container = gt.Container(system_directory=self._system_directory)
                write_container.read(self._cdb.container, symbols=sym_list)
                self._conn.execute("PRAGMA page_size = 1024;")
                self._sqlite_create_uel_table(cc=write_container)
                self._create_new_table(
                    df=self._uel_table_df,
                    tableName="[UEL$]",
                    schema=self._schema_name,
                    dtype_map=None,
                    ifExists="fail",
                )
                self._write_native_sql(
                    df=self._uel_table_df,
                    insertMethod="default",
                    writeFunction_args={
                        "name": "[UEL$]",
                        "schema": self._schema_name,
                    },
                )
                if not self._sqlitewrite_globalCommit:
                    self._engine.commit()

            elif self._cnctn_type == "sqlite" and self._check_table(
                tableName="UEL$", schema=self._schema_name
            ):
                self._cdb.print_log(
                    f"WARNING: The table >UEL$< already exists in the database file. It appears that the database was created with the small option enabled.\nAppending to or replacing a pre-existing table may lead to unexpected results."
                )

            for sym, sym_raw in zip(self._symbols, symbols_raw):
                if self._trace > 0:
                    self._log_instructions(
                        sym, sym_raw, description=f"Write symbol >{sym['name']}<:"
                    )

                sym_name = sym["name"]
                table_name = sym["tableName"]
                schema = sym["schemaName"]
                exists = sym["ifExists"]
                unstack = sym["unstack"]
                value_sub = sym["valueSubstitutions"]
                dtype_map = self._dict_get(sym, "dTypeMap", {})
                insertMethod = sym["insertMethod"]
                skip_text = sym["skipText"]

                if self._small and table_name == "UEL$":
                    self._connect_error(
                        f"tableName >UEL$< is not allowed. >UEL$< is a preserved tableName with small set to >True<."
                    )

                gt_sym = write_container[sym_name]

                if self._trace > 2:
                    self._cdb.print_log(
                        f"Connect Container symbol={sym_name}:\n {gt_sym.records}\n"
                    )

                if not isinstance(gt_sym, gt.Set) and not isinstance(
                    gt_sym, gt.Parameter
                ):
                    self._connect_error(
                        f"Symbol type >{type(gt_sym)}< of symbol >{sym_name}< is not supported. Supported symbol types are set and parameter."
                    )

                dim = gt_sym.dimension
                df = self._sym_records_no_none(gt_sym).copy(deep=True)
                sym_type = "par" if isinstance(gt_sym, gt.Parameter) else "set"
                value = "value" if sym_type == "par" else "element_text"

                if value_sub:
                    df = self._apply_value_substitutions(df, value_sub, sym_type)
                    if self._trace > 2:
                        self._cdb.print_log(f"After value substitution:\n{df}")

                if unstack and dim > 0:
                    if (
                        sym_type == "set" and skip_text
                    ):  # replace all element_text by Y when exporting a true table
                        df.loc[:, value] = "Y"
                    elif (
                        sym_type == "set"
                    ):  # replace empty element_text by Y when exporting a true table
                        df.loc[df[value] == "", value] = "Y"
                    cols = list(df.columns)
                    if dim > 1:
                        df = df.pivot(index=cols[0:-2], columns=cols[-2], values=value)
                        df.reset_index(inplace=True, drop=False)
                    elif len(df) > 0:
                        df = df.set_index(cols[0]).T.reset_index(drop=True)
                    else:
                        self._connect_error(
                            f"unstack: >{unstack}< on 1-dimensional symbol with empty DataFrame not allowed."
                        )
                    df.rename_axis(
                        [None], axis=1, inplace=True
                    )  # remove column index names
                    if self._trace > 2:
                        self._cdb.print_log(f"DataFrame after unstack:\n{df}")

                elif dim > 0:
                    df.sort_values(df.columns[:-1].tolist(), inplace=True)
                    if self._trace > 2:
                        self._cdb.print_log(f"DataFrame after sort:\n{df}")
                    if sym_type == "set" and skip_text:
                        df = df.drop(columns="element_text")

                to_sql_args = {
                    "name": table_name,
                    "schema": schema,
                    "if_exists": exists,
                    "index": False,
                }
                to_sql_args.update(self._dict_get(sym, "toSQLArguments", {}))

                writeFunction_args = {
                    "name": table_name,
                    "schema": schema,
                    "if_exists": exists,
                    "dtype_map": dtype_map,
                }

                if self._small and dim > 0:
                    dim_after_unstack = dim - 1 if unstack else dim
                    col = df.columns[:dim_after_unstack]
                    df[col] = df[col].astype("int64")
                    writeFunction_args.update({"name": f"[{table_name}$]"})

                self._write_sql(
                    df,
                    insertMethod,
                    to_sql_args,
                    writeFunction_args,
                )

                # After the parent tables <tableName$> are created. Views for the symbol name are to be created.
                if self._small and dim > 0:
                    self._sqlite_create_view(
                        table_name, dim_after_unstack, df.columns.tolist()
                    )

                if not self._sqlitewrite_globalCommit:
                    # Commit each symbol
                    if self._cnctn_type == "sqlalchemy":
                        self._conn.commit()
                    else:
                        self._engine.commit()

            if self._sqlitewrite_globalCommit:
                self._engine.commit()
                # Commit all symbols at once. If failure, nothing gets committed.
                # ATM, ONLY FOR SQLITEWRITE TOOL

        except Exception:
            if self._cnctn_type == "sqlalchemy":
                self._conn.rollback()
            else:
                self._engine.rollback()
            raise

        finally:
            if self._cnctn_type == "sqlalchemy":
                self._engine.dispose()
            else:
                self._conn.close()
