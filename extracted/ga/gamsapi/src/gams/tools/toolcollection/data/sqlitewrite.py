#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2026 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2026 GAMS Software GmbH <support@gams.com>
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

from gams.tools.toolcollection.tooltemplate import ToolTemplate
from gams.connect import ConnectDatabase
from gams import transfer as gt
from collections import defaultdict


def scalar_symbol_template():
    """
    Template for maintaining scalar symbols within a dictionary.
    Intended to support potential future implementations of SpecialSymbols, subclasses of base symbols
    """
    return {"sym_name": [], "sym_recs": []}


class Sqlitewrite(ToolTemplate):

    def __init__(self, system_directory, tool):
        super().__init__(system_directory, tool)
        self.title = "sqlitewrite: This tool exports GAMS symbols to a sqlite database file(.db)."
        self.add_namedargdef(
            "gdxIn=<gdx_filename>",
            "fnExist",
            "Specify the input file",
            shell_req=True,
        )
        self.add_namedargdef(
            "o=<sqlite_filename>",
            "str",
            "Specify the output sqlite file",
        )
        self.add_namedargdef(
            "ids=<string>",
            "str",
            "Specify the symbols to be read separated by commas.",
            argdefault=False,
        )
        self.add_namedargdef(
            "expltext=<Y/N>",
            "str",
            "Specify if the explanatory text for set elements are also exported to the database table. Default = N",
            argdefault=False,
        )
        self.add_namedargdef(  # SQLWriter can append to exisiting tables with `ifExists`
            "append=<Y/N>",
            "str",
            "Specify whether to write new symbols to new tables in an existing database. Adding to existing tables is not allowed. Default: Create a new database file.",
            argdefault=False,
        )
        self.add_namedargdef(
            "unstack=<Y/N>",
            "str",
            "Specify if the last index column will be used as a header row.",
            argdefault=False,
        )
        self.add_namedargdef(
            "fast=<Y/N>",
            "str",
            "Specify if the tool should accelerate data inserts using some non-standard pragmas. Enabling this compromises data consistency in the event of a program crash.",
            argdefault=False,
        )
        self.add_namedargdef(
            "small=<Y/N>",
            "str",
            "Specify if the UELs are stored in a separate table resulting in a smaller database. A user-friendly SQL VIEW is created to hide the complexity of the joins.",
            argdefault=False,
        )

    def check_bool_args(self, key):
        """
        Helper function to convert the argVal of a boolean type argument to Boolean True/False.

        Raise Exception if the input is not y/n.
        """
        if key in self.namedargs:
            value = self.namedargs_val(key)
            if value.lower() in ["y", "yes"]:
                return True
            elif value.lower() in ["n", "no"]:
                return False
            self.tool_error(f"Wrong flag, {key}: {value}", print_help=False)

        return False

    @staticmethod
    def combine_scalars(m: gt.Container, scalar_dict, scalar_name, pd_concat):
        df = pd_concat(scalar_dict["sym_recs"], ignore_index=True)
        df.insert(0, "name", scalar_dict["sym_name"])
        dom = ["name"]
        if scalar_name in ["scalarvariables", "scalarequations"]:
            dom.append("attribute")
            df = df.melt(id_vars="name", var_name="attribute", value_name="value")
        m.addParameter(name=scalar_name, domain=dom, records=df)

    def execute(self):
        if self.dohelp():
            return

        self.process_args()

        if self.namedargs_val("o"):
            sqlite_file = self.namedargs_val("o")
        elif not self.namedargs_val("o") and self.namedargs_val("gdxin"):
            sqlite_file = self.namedargs_val("gdxin").rsplit(".gdx", 1)[0] + ".db"
        else:
            self.tool_error(f"Option >o< not specified.")

        append = self.check_bool_args("append")
        small = self.check_bool_args("small")

        if small and append:
            self.tool_error(
                f"Options >small< and >append< are enabled. Appending to an existing database with option >small< enabled is not allowed."
            )

        if not append:
            import os

            try:
                os.remove(sqlite_file)
            except FileNotFoundError:  # if not found, create the file
                pass
            except PermissionError as e:
                self.tool_error(
                    f"Unable to delete {sqlite_file}.\n{e}", print_help=False
                )
            except Exception as e:
                self.tool_error(
                    f"An error occurred while deleting file >{sqlite_file}<:\n{e}",
                    print_help=False,
                )

        skip_text = not self.check_bool_args("expltext")
        unstack = self.check_bool_args("unstack")
        fast = self.check_bool_args("fast")

        id_list = None  # reads all if ids is not set
        if "ids" in self.namedargs:
            id_list = self.namedargs_val("ids").split(",")

        cdb = ConnectDatabase(self._tools._system_directory, ecdb=self._tools._ecdb)
        m: gt.Container = cdb.container
        self.read_id_inputs(m, inputs=id_list)

        symbols = []
        scalar_data = defaultdict(scalar_symbol_template)
        cc = m.data.copy()  # the following loop adds new symbols

        for name, sym in cc.items():
            if sym.dimension == 0:
                if isinstance(sym, gt.Parameter):
                    sym_type = "Parameter"
                elif isinstance(sym, gt.Equation):
                    sym_type = "Equation"
                elif isinstance(sym, gt.Variable):
                    sym_type = "Variable"
                else:
                    continue
                scalar_data[sym_type]["sym_name"].append(sym.name)
                scalar_data[sym_type]["sym_recs"].append(sym.records)
            elif isinstance(sym, (gt.Variable, gt.Equation)):
                if sym.records is not None:
                    dom = list(sym.records.columns[: sym.dimension])
                    df = sym.records.melt(
                        id_vars=dom, var_name="attribute", value_name="value"
                    )
                else:
                    ### The old tool creates a blank table for symbols with no records
                    df = None
                m.addParameter(
                    name=f"{name}_all",
                    # NOTE: using sym.domain causes validity issues later on in SQLWriter
                    domain=[dom if isinstance(dom, str) else dom.name for dom in sym.domain] + ["attribute"],
                    records=df,
                )
                symbols.append(
                    {
                        "name": f"{name}_all",
                        "tableName": name if small else f"[{name}]",
                        "unstack": True,
                    }
                )

            elif isinstance(sym, gt.Alias):
                pass
            else:
                symbols.append(
                    {
                        "name": name,
                        "tableName": name if small else f"[{name}]",
                    }
                )
        if any(data["sym_name"] for data in scalar_data.values()):
            from pandas import concat as pd_concat
        if scalar_data["Parameter"]["sym_name"]:
            self.combine_scalars(
                m,
                scalar_dict=scalar_data["Parameter"],
                scalar_name="scalars",
                pd_concat=pd_concat,
            )
            symbols.append({"name": "scalars", "tableName": "scalars"})
        if scalar_data["Variable"]["sym_name"]:
            self.combine_scalars(
                m,
                scalar_dict=scalar_data["Variable"],
                scalar_name="scalarvariables",
                pd_concat=pd_concat,
            )
            symbols.append(
                {
                    "name": "scalarvariables",
                    "tableName": "scalarvariables",
                    "unstack": True,
                }
            )
        if scalar_data["Equation"]["sym_name"]:
            self.combine_scalars(
                m,
                scalar_dict=scalar_data["Equation"],
                scalar_name="scalarequations",
                pd_concat=pd_concat,
            )
            symbols.append(
                {
                    "name": "scalarequations",
                    "tableName": "scalarequations",
                    "unstack": True,
                }
            )
        sqlite_params = {
            "connection": {"database": sqlite_file},
            "connectionArguments": {"__globalCommit__": True},
            "trace": self.namedargs_val("trace"),
            "skipText": skip_text,
            "unstack": unstack,
            "small": small,
            "fast": fast,
            "ifExists": "fail" if append else "replace",
            "symbols": symbols,
        }
        try:
            cdb.execute({"SQLWriter": sqlite_params})
        except Exception as e:
            self.tool_error(f"{e.__class__.__name__}: {e}", print_help=False)
