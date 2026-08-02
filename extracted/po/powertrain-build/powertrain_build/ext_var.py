# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module containing classes for VCC - Supplier signal interface."""

from powertrain_build.types import byte_size_string, get_bitmask
from powertrain_build.a2l import A2l
from powertrain_build.problem_logger import ProblemLogger


class ExtVarBase(ProblemLogger):
    """Generate a2l- and c-files.

    These which declares all variables in the interface that the
    supplier platform writes to.

    This is needed due to legacy handling of the interfaces between units.
    Note that all variables sent from the VCC SPM to the platform should be declared in
    the function that produces the signal!
    """

    INPORT_INDEX = 0
    OUTPORT_INDEX = 1

    __data_type_size = {
        "Float32": "4",
        "UInt32": "4",
        "Int32": "4",
        "UInt16": "2",
        "Int16": "2",
        "UInt8": "1",
        "Int8": "1",
        "Bool": "1",
    }

    def __init__(self, variable_dict, prj_cfg, unit_cfg, user_defined_types, integrity_level, polyspace_comments):
        """Constructor.

        Args:
            variable_dict (dict): dictionary with signal information.
            prj_cfg (BuildProjConfig): Build project class holding where files should be stored.
            user_defined_types (UserDefinedTypes): Class holding user defined data types.
            integrity_level (dict): integrity level of the unit from 'A' to 'D' or 'QM'.
            polyspace_comments (dict): Whether to insert polyspace comments for the variable definitions.
        """
        super().__init__()
        self.set_integrity_level(integrity_level)
        self._var_dict = variable_dict
        self._ext_vars = {}
        self._prj_cfg = prj_cfg
        self._unit_cfg = unit_cfg
        self._enumerations = user_defined_types.get_enumerations()
        self._common_header_files = user_defined_types.common_header_files
        self._polyspace_comments = polyspace_comments

    def set_integrity_level(self, integrity_level):
        """Set integrity level of code generation.

        Args:
            integrity_level (dict): integrity level of the unit from 'A' to 'D' or 'QM'
        """
        self._disp_start = integrity_level["CVC"]["DISP"]["START"]
        self._disp_end = integrity_level["CVC"]["DISP"]["END"]
        self._decl_start = integrity_level["PREDECL"]["DISP"]["START"]
        self._decl_end = integrity_level["PREDECL"]["DISP"]["END"]

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

    def _get_bitmask(self, data_type):
        """Get bitmask of a data type.
        Enumeration bitmasks are derived from the underlying data type.

        Args:
            data_type (str): Data type.
        Returns:
            get_bitmask(powertrain_build.types.get_bitmask): Return result of powertrain_build.types.get_bitmask.
        """
        if data_type in self._enumerations:
            return get_bitmask(self._enumerations[data_type]["underlying_data_type"])
        return get_bitmask(data_type)

    def _restruct_input_data(self):
        """Restructure all the input variables per data-type.

        This will be used for declaring the variables and generating the
        A2L-file
        """
        external_inports = {}
        external_outports = {}
        for external_port_type in self.EXTERNAL_INPORT_TYPES:
            if external_port_type in self._var_dict:
                for var, data in self._var_dict[external_port_type].items():
                    data_type_size = self._get_byte_size_string(data[self.TYPE_NAME])
                    external_inports.setdefault(data_type_size, {})[var] = data
        for external_port_type in self.EXTERNAL_OUTPORT_TYPES:
            if external_port_type in self._var_dict:
                for var, data in self._var_dict[external_port_type].items():
                    data_type_size = self._get_byte_size_string(data[self.TYPE_NAME])
                    external_outports.setdefault(data_type_size, {})[var] = data
        self._ext_vars = external_inports, external_outports

    def _a2l_dict(self):
        """Return a dict defining all parameters for a2l-generation."""
        res = {"vars": {}, "function": "VcExtVar"}
        for inp in self.EXTERNAL_INPORT_TYPES:
            if inp in self._var_dict:
                for var, data in self._var_dict[inp].items():
                    if data[self.TYPE_NAME] in self._enumerations:
                        data_type = self._enumerations[data[self.TYPE_NAME]]["underlying_data_type"]
                    else:
                        data_type = data[self.TYPE_NAME]

                    resv = res["vars"]
                    resv.setdefault(var, {})["a2l_data"] = self.get_a2l_format(data)
                    resv[var]["array"] = []
                    resv[var]["function"] = ["VcEc"]
                    resv[var]["var"] = {"cvc_type": "CVC_DISP", "type": data_type, "var": var}
        return res

    def _get_array_declaration(self, var, width):
        """Get array declaration string from width information.

        Args:
            var (str): Variable name.
            width (int or list): Width information.
        Returns:
            array (str): Array declaration string.
        """
        array = ""
        widths = [width] if not isinstance(width, list) else width
        if len(widths) != 1 or widths[0] != 1:
            for w in widths:
                if w > 1:
                    if not isinstance(w, int):
                        self.critical(f'{var} widths must be integers. Got "{type(w)}"')
                    array += f'[{w}]'
                elif w < 0:
                    self.critical(f'{var} widths can not be negative. Got "{w}"')
        return array

    def _generate_c_file(self, path):
        """Generate the c-file defining all the supplier input signals."""
        polyspace_variable_comment = "Used in project but possibly not in current polyspace set up"
        header = path.with_suffix(".h").name
        var_set = set()
        with path.open("w") as fh_c:
            fh_c.write(f'#include "{header}"\n')
            fh_c.write(f'#include "{self._disp_start}"\n\n')
            if self._polyspace_comments:
                fh_c.write(f'/* polyspace-begin VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n\n')
            for data_type_s, ext_vars in self._ext_vars[self.INPORT_INDEX].items():
                fh_c.write(f"/* Variables of size {data_type_s} bytes */\n\n")
                for var in sorted(ext_vars.keys()):
                    data = ext_vars[var]
                    if var not in var_set:
                        array = self._get_array_declaration(var, data.get("width", 1))
                        if array:
                            init_value = data["init"] if data["init"] != 0 else "{0}"
                        else:
                            init_value = data["init"]
                        fh_c.write(f"CVC_DISP {data[self.TYPE_NAME]} {var}{array} = {init_value};\n")
                        var_set.add(var)
                fh_c.write("\n")
            if self._polyspace_comments:
                fh_c.write(f'/* polyspace-end VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n')
            fh_c.write(f'\n#include "{self._disp_end}"\n')
            self.info("Generated %s", path.name)

    def _generate_h_file(self, path):
        """Generate header file externally declaring interface signals."""
        filename = path.stem
        guard = f"{filename.upper()}_H"
        var_set = set()
        with path.open("w") as fh_c:
            fh_c.write(f"#ifndef {guard}\n")
            fh_c.write(f"#define {guard}\n")
            fh_c.write("#define CVC_DISP\n")
            fh_c.write(self._unit_cfg.base_types_headers)

            for common_header_file in self._common_header_files:
                fh_c.write(f'#include "{common_header_file}"\n')
            fh_c.write("\n")

            fh_c.write(f'#include "{self._decl_start}"\n')
            fh_c.write("/* VCC Inports */\n")
            for data_type_s, ext_vars in self._ext_vars[self.INPORT_INDEX].items():
                fh_c.write(f"/* Variables of size {data_type_s} bytes */\n\n")
                for var in sorted(ext_vars.keys()):
                    if var not in var_set:
                        data = ext_vars[var]
                        array = self._get_array_declaration(var, data.get("width", 1))
                        fh_c.write(f"extern CVC_DISP {data[self.TYPE_NAME]} {var}{array};\n")
                        var_set.add(var)
                fh_c.write("\n")

            fh_c.write("/* VCC Outports */\n")
            for data_type_s, ext_vars in self._ext_vars[self.OUTPORT_INDEX].items():
                fh_c.write(f"/* Variables of size {data_type_s} bytes */\n\n")
                for var in sorted(ext_vars.keys()):
                    if var not in var_set:
                        data = ext_vars[var]
                        array = self._get_array_declaration(var, data.get("width", 1))
                        fh_c.write(f"extern CVC_DISP {data[self.TYPE_NAME]} {var}{array};\n")
                        var_set.add(var)
                fh_c.write("\n")
            fh_c.write(f'#include "{self._decl_end}"\n')
            fh_c.write("#endif\n")
            self.info("Generated %s", path.name)

    def generate_files(self, path):
        """Generate the c- and a2l-file for defining all the supplier input variables."""
        self._restruct_input_data()
        if not self._ext_vars[0] and not self._ext_vars[1]:
            self.info(f"Skipping {path.name} as there were no corresponding vars.")
            return
        self._generate_c_file(path.with_suffix(".c"))
        self._generate_h_file(path.with_suffix(".h"))
        a2l_dict = self._a2l_dict()
        a2l = A2l(a2l_dict, self._prj_cfg)
        a2l.gen_a2l(path.with_suffix(".a2l"))


class ExtVarCsv(ExtVarBase):
    """Handles variable dicts from CSV files.

    Variable dict shall have the following format and is generated by the
    :doc:`CsvSignalInterfaces <signal_interfaces>` class::

        {
            'CAN-Input': {
                'signal1': {
                    'IOType': 'd',
                    'description': 'Some description',
                    'init': 0,
                    'max': 1,
                    'min': 0,
                    'type': 'UInt8',
                    'unit': '-'
                },
                'signal2': {
                    ...
                }
            },
            'CAN-Output': {
                'signal3': {
                    ...
                }
            },
            'xxx-Input': ...,
            'xxx-Output': ...
        }
    """

    EXTERNAL_INPORT_TYPES = ["EMS-Input", "CAN-Input", "Private CAN-Input", "LIN-Input"]
    EXTERNAL_OUTPORT_TYPES = ["EMS-Output", "CAN-Output", "Private CAN-Output", "LIN-Output"]
    TYPE_NAME = "type"

    def get_a2l_format(self, data):
        """Get a2l format.

        Args:
            data (dict): Data dictionary.
        Returns:
            dict: A2l format dictionary.
        """
        return {
            "bitmask": self._get_bitmask(data[self.TYPE_NAME]),
            "description": data["description"],
            "lsb": "2^0",
            "max": data["max"],
            "min": data["min"],
            "offset": "0",
            "unit": data["unit"],
            "x_axis": None,
            "y_axis": None,
        }


class ExtVarYaml(ExtVarBase):
    """Handles variable dicts from Yaml files.

    Variable dict shall have the following format and is generated by the
    :doc:`YamlSignalInterfaces <signal_interfaces>` class::

        {
            'input': {
                'sVcIhfa_D_WhlMotSysFrntLimnIndcn': {},
                'sVcIhfa_D_WhlMotSysFrntModSts': {},
                'sVcIhfa_I_WhlMotSysFrntIdc': {},
                'sVcIhfa_U_UDcDcActHiSide1': {},
                'sVcIhfa_U_WhlMotSysFrntUdc': {}
            },
            'output': {},
            'status': {},
        }
    """

    EXTERNAL_INPORT_TYPES = ["input", "status"]
    EXTERNAL_OUTPORT_TYPES = ["output"]
    TYPE_NAME = "variable_type"

    def get_a2l_format(self, data):
        """Get a2l format.

        Args:
            data (dict): Data dictionary.
        Returns:
            dict: A2l format dictionary.
        """
        return {
            "bitmask": self._get_bitmask(data[self.TYPE_NAME]),
            "description": data["description"],
            "lsb": "2^0",
            "max": data["range"]["max"],
            "min": data["range"]["min"],
            "offset": "0",
            "unit": data["unit"],
            "x_axis": None,
            "y_axis": None,
        }
