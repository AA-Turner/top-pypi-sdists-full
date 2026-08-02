# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for generation of c- and a2l-file with dummy signal declarations."""

import powertrain_build.build_defs as bd

from powertrain_build.types import byte_size_string, get_bitmask
from powertrain_build.a2l import A2l
from powertrain_build.problem_logger import ProblemLogger


class DummyVar(ProblemLogger):
    """Generate c- and a2l-files which declares all missing variables in the interfaces.

    TODO: Please remove this file! Only used while testing.
    """

    def __init__(self, unit_cfg, ext_dict, res_dict, prj_cfg, user_defined_types, polyspace_comments):
        """Initialize instance of class."""
        super().__init__()
        self._unit_cfg = unit_cfg
        self._unit_vars = unit_cfg.get_per_cfg_unit_cfg()
        self._ext_dict = ext_dict
        self._res_dict = res_dict
        self._ext_vars = {}
        self._int_vars = {}
        self._prj_cfg = prj_cfg
        self._enumerations = user_defined_types.get_enumerations()
        self._common_header_files = user_defined_types.common_header_files
        self._polyspace_comments = polyspace_comments

    def _get_byte_size_string(self, data_type):
        """Get byte size of a data type as string.
        Enumeration byte sizes are derived from the underlying data type.

        Args:
            data_type (str): Data type.
        Returns:
            byte_size_string(powertrain_build.types.byte_size_string): Return result of
                                                                       powertrain_build.types.byte_size_string.
        """
        if data_type in self._enumerations:
            return byte_size_string(self._enumerations[data_type]["underlying_data_type"])
        return byte_size_string(data_type)

    def _restruct_input_data(self):
        """Restructure all the input variables per data-type.

        This will be used for declaring the variables and generating the
        A2L-file
        """
        ext_out = {
            var: data
            for ioclass, vardict in self._ext_dict.items()
            if ioclass.endswith("-Output")
            for var, data in vardict.items()
        }
        ext_ = {}
        for var in self._res_dict["sigs"]["ext"]["missing"]:
            self.debug("ext: %s", var)
            if var in ext_out:
                data = ext_out[var]
                self.debug("ext_data: %s", data)
                ext_[var] = data
        int_ = {}
        for unit in self._res_dict["sigs"]["int"]:
            for var in self._res_dict["sigs"]["int"][unit]["missing"]:
                if var not in ext_ and var in self._unit_vars["inports"]:
                    data = self._unit_vars["inports"][var][unit]
                    int_[var] = data
        for var, data in int_.items():
            data_type_size = self._get_byte_size_string(data["type"])
            self._int_vars.setdefault(data_type_size, {})[var] = data
        for var, data in ext_.items():
            data_type_size = self._get_byte_size_string(data["type"])
            self._ext_vars.setdefault(data_type_size, {})[var] = data

    def _a2l_dict(self):
        """Return a dict defining all parameters for a2l-generation."""
        res = {"vars": {}, "function": "VcDummy"}
        for inp in [self._ext_vars]:
            for sizes in inp.values():
                for var, data in sizes.items():
                    if data["type"] in self._enumerations:
                        data_type = self._enumerations[data["type"]]["underlying_data_type"]
                    else:
                        data_type = data["type"]

                    resv = res["vars"]
                    resv.setdefault(var, {})["a2l_data"] = {
                        "bitmask": get_bitmask(data_type),
                        "description": data.get("description", ""),
                        "lsb": "2^0",
                        "max": data.get("max"),
                        "min": data.get("min"),
                        "offset": "0",
                        "unit": data["unit"],
                        "x_axis": None,
                        "y_axis": None,
                    }
                    resv[var]["array"] = []
                    resv[var]["function"] = ["VcEc"]
                    resv[var]["var"] = {"cvc_type": "CVC_DISP", "type": data_type, "var": var}
        return res

    @classmethod
    def _generate_var_defs(cls, fh_c, vars, enums, comment):
        """Generate the variable definitions."""
        fh_c.write(f"\n{comment}\n\n")
        for varsize in sorted(vars.keys(), reverse=True):
            fh_c.write(f"/* Variables of size {varsize} bytes */\n\n")
            var_defs = vars[varsize]
            for var in sorted(var_defs.keys()):
                data = var_defs[var]
                if data["type"] in enums:
                    if enums[data["type"]]["default_value"] is not None:
                        init_value = enums[data["type"]]["default_value"]
                    else:
                        cls.warning('Initializing enumeration %s to "zero".', data["type"])
                        init_value = [k for k, v in enums[data["type"]]["members"].items() if v == 0][0]
                    fh_c.write(f"{data['type']} {var} = {init_value};\n")
                else:
                    fh_c.write(f"{data['type']} {var} = {0};\n")
        fh_c.write("\n")

    @classmethod
    def _generate_var_initialization(cls, fh_c, vars, comment):
        """Generate the variable initializations."""
        fh_c.write(f"\n{comment}\n\n")
        fh_c.write("\nvoid RESTART_VcDummy(void)\n{\n")
        for varsize in sorted(vars.keys(), reverse=True):
            var_defs = vars[varsize]
            for var in sorted(var_defs.keys()):
                fh_c.write(f"    {var} = {0};\n")
        fh_c.write("}\n")

    def _generate_c_file(self, filename):
        """Generate the c-file defining all missing input variables."""
        polyspace_variable_comment = "Used in project but possibly not in current polyspace set up"
        general_includes = ""
        general_includes += self._unit_cfg.base_types_headers
        for common_header_file in self._common_header_files:
            general_includes += f'#include "{common_header_file}"\n'
        general_includes += "\n"

        with open(filename, "w", encoding="utf-8") as fh_c:
            fh_c.write(general_includes)
            fh_c.write(f'#include "{bd.CVC_DISP_START}"\n\n')
            if self._polyspace_comments:
                fh_c.write(f'/* polyspace-begin VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n')
            self._generate_var_defs(fh_c, self._ext_vars, self._enumerations, "/** Missing external signals **/")
            if self._polyspace_comments:
                fh_c.write(f'/* polyspace-end VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n')
            fh_c.write(f'\n#include "{bd.CVC_DISP_END}"\n')
            self.info("Generated %s", filename)

    def generate_file(self, filename):
        """Generate the files for defining all missing input variables."""
        self._restruct_input_data()
        self._generate_c_file(filename + ".c")
        a2l_dict = self._a2l_dict()
        A2l(a2l_dict, self._prj_cfg).gen_a2l(filename + ".a2l")
