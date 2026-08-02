# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module containing classes for model out-port interfaces."""
import os
from operator import itemgetter
import math

import powertrain_build.build_defs as bd
from powertrain_build import signal
from powertrain_build.a2l import A2l
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.types import byte_size, get_bitmask


class DummySpm(ProblemLogger):
    """Generate c-files which defines missing outport variables in the model out-port interface.

    The models declare all in-ports as 'external' and powertrain-build will then
    generate any missing outports in the correct #if/#endif guards here.
    One c-file per outport origin model should be generated.

    * Generate c-code from matlab/TL script with #if/#endif guards.
      - Pro: Is generated at the same time as other code and placed in model src folder.
      - Pro: Generic code. Will be cached together with TL-generated code.
      - Con: m-script
    * Generate c-code from python with only needed variables. No preprocessor directives.
      - Pro: Python
      - Pro: Simpler c-file with only used variables.
      - Con: Not generic! Not cached?

    """

    __asil_level_map = {
        'A': (bd.CVC_DISP_ASIL_A_START, bd.CVC_DISP_ASIL_A_END),
        'B': (bd.CVC_DISP_ASIL_B_START, bd.CVC_DISP_ASIL_B_END),
        'C': (bd.CVC_DISP_ASIL_C_START, bd.CVC_DISP_ASIL_C_END),
        'D': (bd.CVC_DISP_ASIL_D_START, bd.CVC_DISP_ASIL_D_END),
        'QM': (bd.CVC_DISP_START, bd.CVC_DISP_END)}

    def __init__(
        self, missing_outports, prj_cfg, feature_cfg, unit_cfg, user_defined_types, basename, polyspace_comments
    ):
        """Constructor.

        Args:
            missing_outports (list): undefined outports based on unit config variables.
            prj_cfg (BuildProjConfig): Build project class holding where files should be stored.
            feature_cfg (FeatureConfig): Feature configs from SPM_Codeswitch_Setup.
            unit_cfg (UnitConfigs): Class holding all unit interfaces.
            user_defined_types (UserDefinedTypes): Class holding user defined data types.
            basename (str): the basename of the outvar, used for .c and .a2l creation.
            polyspace_comments (bool): Whether to insert polyspace comments for the variable definitions.

        See :doc:`Unit config <unit_config>` for information on the 'outport' dict.
        """
        super().__init__()
        self._prj_cfg = prj_cfg
        self._feature_cfg = feature_cfg
        self._unit_cfg = unit_cfg
        self._enumerations = user_defined_types.get_enumerations()
        self._common_header_files = user_defined_types.common_header_files
        self._name = basename
        self._polyspace_comments = polyspace_comments
        self.use_volatile_globals = prj_cfg.get_use_volatile_globals()
        self._missing_outports = self._restruct_input_data(missing_outports)

    def _get_byte_size(self, data_type):
        """Get byte size of a data type.
        Enumeration byte sizes are derived from the underlying data type.

        Args:
            data_type (str): Data type.
        Returns:
            byte_size(powertrain_build.types.byte_size): Return result of powertrain_build.types.byte_size.
        """
        if data_type in self._enumerations:
            return byte_size(self._enumerations[data_type]['underlying_data_type'])
        return byte_size(data_type)

    def _restruct_input_data(self, outports):
        """Restructure all the input variables per data-type."""
        outports.sort(key=itemgetter('name'))
        outports.sort(key=lambda var: self._get_byte_size(var['type']), reverse=True)
        new_outports = {}
        for outport in outports:
            integrity_level = outport.get('integrity_level', 'QM')
            if integrity_level == 'QM':
                outport['cvc_type'] = 'CVC_DISP'
            else:
                outport['cvc_type'] = f'ASIL_{integrity_level}/CVC_DISP_ASIL_{integrity_level}'
            if integrity_level in new_outports:
                new_outports[integrity_level].append(outport)
            else:
                new_outports.update({integrity_level: [outport]})
        return new_outports

    def _a2l_dict(self, outports):
        """Return a dict defining all parameters for a2l-generation."""
        res = {
            'vars': {},
            'function': 'VcDummy_spm'
        }

        for outport in [port for sublist in outports.values() for port in sublist]:
            var = outport['name']

            if outport['type'] in self._enumerations:
                data_type = self._enumerations[outport['type']]['underlying_data_type']
            else:
                data_type = outport['type']

            resv = res['vars']
            resv.setdefault(var, {})['a2l_data'] = {
                    'bitmask': get_bitmask(data_type),
                    'description': outport.get('description', ''),
                    'lsb': '2^{}'.format(int(math.log2(outport.get('lsb', 1)))
                                         if outport.get('lsb') not in ['-', '']
                                         else 0),
                    'max': outport.get('max'),
                    'min': outport.get('min'),
                    'offset': -(outport.get('offset', 0) if outport.get('offset') not in ['-', ''] else 0),
                    'unit': outport['unit'],
                    'x_axis': None,
                    'y_axis': None}
            resv[var]['function'] = ['VcEc']
            resv[var]['var'] = {'cvc_type': outport['cvc_type'],
                                'type': data_type,
                                'var': var}
            resv[var]['array'] = outport.get('width', 1)
            res.update({'vars': resv})
        return res

    def generate_code_files(self, dst_dir):
        """Generate code and header files.

        Args:
            dst_dir (str): Path to destination directory.

        """
        h_file_path = os.path.join(dst_dir, f'{self._name}.h')
        self._generate_h_file(h_file_path, self._missing_outports)
        c_file_path = os.path.join(dst_dir, f'{self._name}.c')
        self._generate_c_file(c_file_path, self._missing_outports)

    def generate_a2l_files(self, dst_dir):
        """Generate A2L files.

        Args:
            dst_dir (str): Path to destination directory.

        """
        filename = f"{os.path.join(dst_dir, self._name)}.a2l"
        a2l_dict = self._a2l_dict(self._missing_outports)
        a2l = A2l(a2l_dict, self._prj_cfg)
        a2l.gen_a2l(filename)

    def _generate_h_file(self, file_path, outports):
        """Generate header file.

        Args:
            file_path (str): File path to generate.
        """
        file_name = os.path.basename(file_path).split('.')[0]
        with open(file_path, 'w', encoding="utf-8") as fh:
            fh.write(f'#ifndef {file_name.upper()}_H\n')
            fh.write(f'#define {file_name.upper()}_H\n')

            fh.write(self._unit_cfg.base_types_headers)
            fh.write('#include "VcCodeSwDefines.h"\n')
            for common_header_file in self._common_header_files:
                fh.write(f'#include "{common_header_file}"\n')

            for integrity_level in outports.keys():
                disp_start = bd.PREDECL_ASIL_LEVEL_MAP[integrity_level]['DISP']['START']
                disp_end = bd.PREDECL_ASIL_LEVEL_MAP[integrity_level]['DISP']['END']
                fh.write('\n')
                fh.write(f'#include "{disp_start}"\n')
                for outport in outports[integrity_level]:
                    if outport['class'] not in signal.INPORT_CLASSES:
                        self.warning(f'inport {outport["name"]} class {outport["class"]} is not an inport class')

                    array = ''
                    width = outport['width']
                    if not isinstance(width, list):
                        width = [width]
                    if len(width) != 1 or width[0] != 1:
                        for w in width:
                            if w > 1:
                                if not isinstance(w, int):
                                    self.critical(f'{outport["name"]} widths must be integers. Got "{type(w)}"')
                                array += f'[{w}]'
                            elif w < 0:
                                self.critical(f'{outport["name"]} widths can not be negative. Got "{w}"')
                    if self.use_volatile_globals:
                        fh.write(f"extern volatile {outport['type']} {outport['name']}{array};\n")
                    else:
                        fh.write(f"extern {outport['type']} {outport['name']}{array};\n")
                fh.write(f'#include "{disp_end}"\n')

            fh.write(f'#endif /* {file_name.upper()}_H */\n')

    def _generate_c_file(self, file_path, outports):
        """Generate C-file for inports that are missing outports except for supplier ports."""
        polyspace_variable_comment = "Used in project but possibly not in current polyspace set up"
        file_name = os.path.basename(file_path).split('.')[0]
        base_header = f'#include "{file_name}.h"\n'

        with open(file_path, 'w', encoding="utf-8") as fh_c:
            fh_c.write(base_header)
            if self._polyspace_comments:
                fh_c.write(f'\n/* polyspace-begin VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n')
            for integrity_level in outports.keys():
                disp_start = bd.CVC_ASIL_LEVEL_MAP[integrity_level]['DISP']['START']
                disp_end = bd.CVC_ASIL_LEVEL_MAP[integrity_level]['DISP']['END']
                fh_c.write('\n')
                fh_c.write(f'#include "{disp_start}"\n')
                for outport in outports[integrity_level]:
                    if outport['class'] not in signal.INPORT_CLASSES:
                        self.warning(f'inport {outport["name"]} class {outport["class"]} is not an inport class')

                    width = outport['width']
                    if outport['type'] in self._enumerations:
                        if self._enumerations[outport['type']]['default_value'] is not None:
                            init_value = self._enumerations[outport['type']]['default_value']
                        else:
                            self.warning('Initializing enumeration %s to "zero".', outport['type'])
                            init_value = [
                                k for k, v in self._enumerations[outport['type']]['members'].items() if v == 0
                            ][0]
                        if width != 1:
                            self.critical(f'{outport["name"]} enumeration width must be 1. Got "{width}"')
                        fh_c.write(f"{outport['type']} {outport['name']} = {init_value};\n")
                    else:
                        if not isinstance(width, list):
                            width = [width]
                        if len(width) == 1 and width[0] == 1:
                            array = ' = 0'
                        else:
                            array = ''
                            for w in width:
                                if w > 1:
                                    if not isinstance(w, int):
                                        msg = f'{outport["name"]} widths must be integers. Got "{type(w)}"'
                                        self.critical(msg)
                                    array += f'[{w}]'
                                elif w < 0:
                                    self.critical(f'{outport["name"]} widths can not be negative. Got "{w}"')
                        if self.use_volatile_globals:
                            fh_c.write(f'volatile {outport["type"]} {outport["name"]}{array};\n')
                        else:
                            fh_c.write(f'{outport["type"]} {outport["name"]}{array};\n')
                fh_c.write(f'#include "{disp_end}"\n')
            if self._polyspace_comments:
                fh_c.write(f'\n/* polyspace-end VARIABLE:* [Justified: Low] "{polyspace_variable_comment}" */\n')

    def generate_files(self, dst_dir):
        """Generate the files for defining all missing input variables."""
        self.generate_code_files(dst_dir)
        self.generate_a2l_files(dst_dir)
