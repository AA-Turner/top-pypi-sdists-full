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

import gams.transfer as gt
from gams.connect.agents.connectagent import ConnectAgent
from gams.connect.agents._sqlconnectors import (
    AccessConnector,
    MySQLConnector,
    PostgresConnector,
    PyodbcConnector,
    SQLAlchemyConnector,
    SQLiteConnector,
    SQLServerConnector,
)
from gams.connect.agents._sqlconnectors._databasehandler import ConnectionType
from gams.connect.connectvalidator import ConnectValidator


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
            False if self._cnctn_type != ConnectionType.SQLITE.value else inst["fast"]
        )  # NO effect for rest of the connectionTypes
        self._small = (
            False if self._cnctn_type != ConnectionType.SQLITE.value else inst["small"]
        )  # NO effect for rest of the connectionTypes
        self._symbols = inst["symbols"]  # symbol option
        self._write_all = self._symbols == "all"
        self._sqlitewrite_globalCommit = self._connection_args.pop(
            "__globalCommit__", False
        )
        self._handler = self._get_handler(self._cnctn_type)

    def _get_handler(
        self, cnctn_type
    ) -> (
        SQLiteConnector
        | SQLAlchemyConnector
        | PyodbcConnector
        | MySQLConnector
        | PostgresConnector
        | SQLServerConnector
        | AccessConnector
    ):
        handlers = {
            ConnectionType.SQLITE.value: SQLiteConnector,
            ConnectionType.SQLALCHEMY.value: SQLAlchemyConnector,
            ConnectionType.PYODBC.value: PyodbcConnector,
            ConnectionType.MYSQL.value: MySQLConnector,
            ConnectionType.POSTGRES.value: PostgresConnector,
            ConnectionType.SQLSERVER.value: SQLServerConnector,
            ConnectionType.ACCESS.value: AccessConnector,
        }
        handler_class = handlers[cnctn_type]

        return handler_class(
            error_callback=self._connect_error,
            printLog_callback=self._cdb.print_log,
            trace=self._trace,
        )

    def _open(self):
        options = {
            "_sqlitewrite_globalCommit": self._sqlitewrite_globalCommit,
            "small": self._small,
            "fast": self._fast,
        }
        self._handler.connect(
            connection_details=self._input_cnctn,
            connection_args=self._connection_args,
            **options,
        )

    def execute(self):
        if self._trace > 0:
            self._log_instructions(self._inst, self._inst_raw)
            self._describe_container(self._cdb.container, "Connect Container:")

        self._handler.validate_insert_method(method=self._insertMethod)
        self._open()

        try:
            self._handler.create_transaction()

            if self._write_all:
                self._symbols = []
                sym_schema = self._cdb.load_schema(self)["symbols"]["oneof"][1][
                    "schema"
                ]["schema"]
                v = ConnectValidator(sym_schema)
                for name, sym in self._cdb.container.data.items():
                    if type(sym) in [gt.Set, gt.Parameter]:
                        sym_inst = v.validated({"name": name, "tableName": name})  # type: ignore
                        if sym_inst is None:
                            self._connect_error(
                                f"Validation for symbol >{name}< failed: {v.errors}"  # type: ignore
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

            pre_write_args = {
                # only implemented for sqlite, pre_write_procedures must return the container
                "container": self._cdb.container,
                "directory": self._system_directory,
                "sym_list": sym_list,
            }
            write_container = self._handler.pre_write_procedures(**pre_write_args)

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
                self._handler.validate_insert_method(method=insertMethod)

                if self._small and table_name == "UEL$":
                    self._connect_error(
                        "tableName >UEL$< is not allowed. >UEL$< is a preserved tableName with small set to >True<."
                    )

                gt_sym = write_container[sym_name]

                if self._trace > 2:
                    self._cdb.print_log(
                        f"Connect Container symbol={sym_name}:\n {gt_sym.records}\n"  # type: ignore
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

                writeFunction_args = {
                    "name": table_name,
                    "schema": schema,
                    "if_exists": exists,
                    "insertMethod": insertMethod,
                    "columnEncloser": self._col_encloser,
                    "dtype_map": dtype_map,
                    "toSQLArguments": self._dict_get(sym, "toSQLArguments", {}),
                    "index": False,
                }

                dim_after_unstack = None
                if self._small and dim > 0:
                    dim_after_unstack = dim - 1 if unstack else dim
                    col = df.columns[:dim_after_unstack]
                    df[col] = df[col].astype("int64")
                    writeFunction_args.update({"name": f"[{table_name}$]"})

                self._handler.write_dataframe(df, writeFunction_args)

                post_write_args = {
                    "tableName": table_name,
                    "dim_after_unstack": dim_after_unstack,
                    "colList": df.columns.tolist(),
                    "dim": dim,
                }
                self._handler.post_write_procedures(
                    **post_write_args
                )  # only implemented for sqlite

                if not self._sqlitewrite_globalCommit:
                    self._handler.commit()

            if self._sqlitewrite_globalCommit:
                self._handler.commit()

        except Exception:
            self._handler.rollback()
            raise

        finally:
            self._handler.close()
