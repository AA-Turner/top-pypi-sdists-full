# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module containing cvc classes for VCC - defines and includes for memory sections."""

import time
from pathlib import Path
from powertrain_build import build_defs
from powertrain_build.problem_logger import ProblemLogger


class MemorySection(ProblemLogger):
    """Handle headers for CVC_* definitions."""

    calibration_definitions = [
        'CVC_CAL',
        'CVC_CAL_ASIL_A',
        'CVC_CAL_ASIL_B',
        'CVC_CAL_ASIL_C',
        'CVC_CAL_ASIL_D',
        'CVC_CAL_MERGEABLE_ASIL_A',
        'CVC_CAL_MERGEABLE_ASIL_B',
        'CVC_CAL_MERGEABLE_ASIL_C',
        'CVC_CAL_MERGEABLE_ASIL_D'
    ]
    measurable_definitions = [
        'CVC_DISP',
        'CVC_DISP_ASIL_A',
        'CVC_DISP_ASIL_B',
        'CVC_DISP_ASIL_C',
        'CVC_DISP_ASIL_D'
    ]

    def __init__(self, build_cfg, unit_cfg, polyspace_comments):
        super().__init__()
        self.build_cfg = build_cfg
        self.unit_cfg = unit_cfg
        self.mem_map_config = self.build_cfg.get_memory_map_config()
        self.include_header_guards = self.mem_map_config['includeHeaderGuards']
        self.mem_map_include = f'#include "{self.mem_map_config["memMapPrefix"]}_MemMap.h"\n'
        self.xcp_enabled = self.build_cfg.get_xcp_enabled()
        self.use_volatile_globals = self.build_cfg.get_use_volatile_globals()
        self.polyspace_comments = polyspace_comments

    @staticmethod
    def _get_mem_map_section(section):
        return 'STOP' if section == 'END' else section

    def _get_header(self, section_file, ignore_include_header_guards=False):
        if not self.include_header_guards and not ignore_include_header_guards:
            if self.polyspace_comments:
                return [
                    '/* polyspace-begin MISRA2012:D4.10 [Justified:Low] "N/A due to how TargetLink generates code" */\n'
                ]
            return []
        section_file_header_guard = section_file.split('.')[0].upper()
        return [
            f'#ifndef {section_file_header_guard}_H\n',
            f'#define {section_file_header_guard}_H\n\n'
        ]

    def _get_footer(self, section_file, ignore_include_header_guards=False):
        if not self.include_header_guards and not ignore_include_header_guards:
            if self.polyspace_comments:
                return [
                    '/* polyspace-end MISRA2012:D4.10 [Justified:Low] "N/A due to how TargetLink generates code" */\n'
                ]
            return []
        section_file_header_guard = section_file.split('.')[0].upper()
        return [f'\n#endif /* {section_file_header_guard}_H */\n']

    def _get_calibration_rte_macro_expansion(self, section_file):
        macros = self._get_header(section_file, True)
        config = self.unit_cfg.get_per_cfg_unit_cfg()
        valid_configs = ["outports", "local_vars", "calib_consts"]
        for valid_config in valid_configs:
            for signal_name, unit_info in config.get(valid_config, {}).items():
                swc_name = self.build_cfg.get_composition_config("softwareComponentName")
                define_str = f'#define {signal_name} Rte_CData_{swc_name}_{signal_name}()'
                if signal_name.startswith("m") and not signal_name.endswith("_r") and not signal_name.endswith("_c"):
                    define_str += f"->dt_{signal_name}"
                define_str += "\n"
                for info in unit_info.values():  # Should be length 1 for cal
                    if "CVC_CAL" in info["class"]:
                        macros.append(define_str)
        macros.extend(self._get_footer(section_file, True))
        return macros

    def _get_cal(self, section):
        cvc_undefines = [f'#undef {definition}\n' for definition in self.calibration_definitions]
        if section == 'START':
            volatile_string = 'volatile' if self.use_volatile_globals else ''
            cvc_defines = [f'#define {definition} {volatile_string}\n' for definition in self.calibration_definitions]
        else:
            cvc_defines = []
        section_type = 'cal' if self.xcp_enabled else 'disp'
        memory_section_handling = [
            self.mem_map_config['projectDefines'][self._get_mem_map_section(section)][section_type] + '\n'
        ]
        if self.mem_map_config['includeMemMapForCalibration'] or not self.xcp_enabled:
            memory_section_handling.append(self.mem_map_include)
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_disp(self, section):
        cvc_undefines = [f'#undef {definition}\n' for definition in self.measurable_definitions]
        if section == 'START':
            volatile_string = 'volatile' if self.use_volatile_globals else ''
            cvc_defines = [f'#define {definition} {volatile_string}\n' for definition in self.measurable_definitions]
        else:
            cvc_defines = []
        memory_section_handling = [
            self.mem_map_config['projectDefines'][self._get_mem_map_section(section)]['disp'] + '\n',
            self.mem_map_include
        ]
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_code(self, section):
        cvc_undefines = []
        cvc_defines = []
        memory_section_handling = [
            self.mem_map_config['projectDefines'][self._get_mem_map_section(section)]['code'] + '\n',
            self.mem_map_include
        ]
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_const(self, section):
        cvc_undefines = []
        cvc_defines = []
        memory_section_handling = [
            self.mem_map_config['projectDefines'][self._get_mem_map_section(section)]['const'] + '\n',
            self.mem_map_include
        ]
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_nvm(self, section):
        cvc_undefines = []
        cvc_defines = []
        memory_section_handling = [
            self.mem_map_config['projectDefines'][self._get_mem_map_section(section)]['nvm'] + '\n',
            self.mem_map_include
        ]
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_rest(self):
        cvc_undefines = []
        cvc_defines = []
        memory_section_handling = [
            self.mem_map_include
        ]
        return cvc_undefines, cvc_defines, memory_section_handling

    def _get_predecl(self):
        cvc_undefines = []
        cvc_defines = []
        memory_section_handling = []
        return cvc_undefines, cvc_defines, memory_section_handling

    def generate_cvc_header(self, section, section_file):
        """Generate CVC headers.

        Args:
            section (str): Name of the CVC section
            section_file (str): Name of the header file
        Returns:
            lines_to_write (list(str)): Lines to write to given section file.
        """
        header = self._get_header(section_file)
        footer = self._get_footer(section_file)
        if '_CAL_' in section_file:
            cvc_undefines, cvc_defines, memory_section_handling = self._get_cal(section)
        elif '_DISP_' in section_file:
            cvc_undefines, cvc_defines, memory_section_handling = self._get_disp(section)
        elif not section_file.startswith('PREDECL_'):
            if section_file.startswith('CVC_CAL') or section_file.startswith('CVC_DISP'):
                self.critical('Should not find CVC_CAL/DISP here. Check logic. File: %s.', section_file)
            elif section_file.startswith('CVC_CODE'):
                cvc_undefines, cvc_defines, memory_section_handling = self._get_code(section)
                use_rte_macro_expansion = self.build_cfg.get_code_generation_config("useCalibrationRteMacroExpansion")
                if section == 'START' and use_rte_macro_expansion:
                    # header and footer are part of the expansion
                    header = []
                    footer = []
                    # RTE header should be included before memmap
                    swc_name = self.build_cfg.get_composition_config("softwareComponentName")
                    rte_inclusion = [f'#include "Rte_{swc_name}.h"\n']
                    macro_expansion = self._get_calibration_rte_macro_expansion(section_file)
                    memory_section_handling = rte_inclusion + memory_section_handling + macro_expansion
            elif section_file.startswith('CVC_CONST'):
                cvc_undefines, cvc_defines, memory_section_handling = self._get_const(section)
            else:
                cvc_undefines, cvc_defines, memory_section_handling = self._get_rest()
        else:
            cvc_undefines, cvc_defines, memory_section_handling = self._get_predecl()

        return header + cvc_undefines + cvc_defines + memory_section_handling + footer

    def generate_required_header_files(self):
        """Generate required header files to delivery folder.

        Generate required header files such as memory protection files.
        NOTE: Currently, only one ASIL level can be selected for an SWC.
        """
        self.info('******************************************************')
        self.info('Start generating required header files')
        start_time = time.time()
        src_dst_dir = self.build_cfg.get_src_code_dst_dir()
        for section_dict in build_defs.PREDECL_EXTRA.values():
            for section_file in section_dict.values():
                header = self._get_header(section_file)
                footer = self._get_footer(section_file)
                with Path(src_dst_dir, section_file).open('w', encoding="utf-8") as header_file_handler:
                    header_file_handler.writelines(header + footer)

        for asil_dict in build_defs.ASIL_LEVEL_MAP.values():
            for type_dict in asil_dict.values():
                for section_dict in type_dict.values():
                    for section, section_file in section_dict.items():
                        lines_to_write = self.generate_cvc_header(section, section_file)
                        with Path(src_dst_dir, section_file).open('w', encoding="utf-8") as header_file_handler:
                            header_file_handler.writelines(lines_to_write)

        for nvm_dict in build_defs.NVM_LEVEL_MAP.values():
            for section_dict in nvm_dict.values():
                for section, section_file in section_dict.items():
                    section_config = self.mem_map_config['projectDefines'][self._get_mem_map_section(section)]
                    if "nvm" in section_config:
                        lines_to_write = self._get_nvm(section)[2]
                    else:
                        lines_to_write = []
                    header = self._get_header(section_file)
                    footer = self._get_footer(section_file)
                    with Path(src_dst_dir, section_file).open('w', encoding="utf-8") as header_file_handler:
                        header_file_handler.writelines(header + lines_to_write + footer)
        self.info('Finished generating required header files (in %4.2f s)', time.time() - start_time)
