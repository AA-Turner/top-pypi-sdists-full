# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""This module is used to parse the core definition files.

Also provides methods to filter the definitions per project.
"""

import os
import time
from collections import defaultdict
from pathlib import Path
from ruamel.yaml import YAML
from powertrain_build import build_defs
from powertrain_build.xlrd_csv import WorkBook
from powertrain_build.problem_logger import ProblemLogger


class Core(ProblemLogger):
    """A class holding core configuration data."""

    __wrk_sheets = {'EventIDs': {'mdl_col': 0,
                                 'id_col': 1,
                                 'desc_col': 2,
                                 'fid_col': 3,
                                 'com_col': 4,
                                 'data_col': 5},
                    'FunctionIDs': {'mdl_col': 0,
                                    'id_col': 1,
                                    'desc_col': 2,
                                    'com_col': 3,
                                    'data_col': 4},
                    'IUMPR': {'mdl_col': 0,
                              'id_col': 1,
                              'desc_col': 2,
                              'fid_col': 3,
                              'com_col': 4,
                              'data_col': 5},
                    'Mode$06': {'mdl_col': 0,
                                'id_col': 1,
                                'desc_col': 2,
                                'fid_col': 3,
                                'UAS_col': 4,
                                'com_col': 5,
                                'data_col': 6},
                    'Ranking': {'mdl_col': 0,
                                'id_col': 1,
                                'desc_col': 2,
                                'fid_col': 3,
                                'com_col': 4,
                                'data_col': 5}}

    _NoFid = '_NoFid'

    def __init__(self, project_cfg, unit_cfgs):
        """Parse the config files to an internal representation.

        Args:
            project_cfg (BuildProjConfig): Project configuration
            unit_cfgs (UnitConfigs): Unit definitions
        """
        super().__init__()
        self._prj_cfg = project_cfg
        self._unit_cfgs = unit_cfgs
        self._csv_files = None
        self._read_csv_files(self._prj_cfg.get_prj_cfg_dir())
        self._parse_core_config()

    def _read_csv_files(self, config_path):
        """Metod for reading the core csv confgiuration files."""
        self.info('******************************************************')
        self.info('Start parsing the core configuration files')
        start_time = time.time()
        csv_file_names = []
        for sheet in self.__wrk_sheets:
            fname = os.path.join(config_path,
                                 'CoreIdNameDefinition_' + sheet + '.csv')
            self.debug('Core csv: %s', fname)
            csv_file_names.append(fname)
        self._csv_files = WorkBook(csv_file_names)
        self.info('Finished parsing the core configuration files (in %4.2f s)', time.time() - start_time)

    def _parse_core_config(self):
        """Parse core IDs for all projects."""
        # Parse sheet by sheet
        tmp_ids = {}
        for sheet_name, cols in self.__wrk_sheets.items():
            worksheet = self._csv_files.sheet_by_name(sheet_name)
            prj_row = worksheet.row(1)
            curr_sheet = tmp_ids[sheet_name] = {}
            for prj_col in range(cols['data_col'], len(prj_row)):
                prj = prj_row[prj_col].value
                curr_id = curr_sheet[prj] = {}
                for curr_row in range(2, worksheet.nrows):
                    row = worksheet.row(curr_row)
                    val = row[prj_col].value
                    if val and val.strip() in 'xX':
                        func_tmp = row[cols['id_col']].value.strip()
                        if func_tmp != '':
                            if sheet_name == 'Mode$06':
                                uas_val = row[cols['UAS_col']].value
                                if isinstance(uas_val, float):
                                    uas_val = int(uas_val)
                                curr_id[func_tmp] = (row[cols['desc_col']].value,
                                                     str(uas_val))
                            else:
                                curr_id[func_tmp] = row[
                                    cols['desc_col']].value
        # Reformat from Sheet->Proj->Id to Proj->Sheet->Id
        self._ids = defaultdict(dict)
        for s_name, s_data in tmp_ids.items():
            for p_name, p_data in s_data.items():
                self._ids[p_name][s_name] = p_data

    def get_core_ids_proj(self, project):
        """Get the core IDs for a project.

        Returns:
            dict: Core IDs

        """
        core_ids = self._ids[project]
        # Check for unused core symbols
        for sheet_name, sheet_data in core_ids.items():
            for id_ in sheet_data:
                if not self._unit_cfgs.check_if_in_per_cfg_unit_cfg('core', id_):
                    self.debug('Core symbol not used in current project: %s/%s', sheet_name, id_)
        # Check for undefined core symbols in unit configs
        ucfg = self._unit_cfgs.get_per_cfg_unit_cfg()
        for id_ in ucfg.get('core', {}):
            for _, core_sheet in core_ids.items():
                if id_ in core_sheet:
                    break
            else:
                self.warning('Core symbol not defined for current project: %s', id_)
        return core_ids

    def get_current_core_config(self):
        """Return all the core configuration parameters for the current project.

        Returns:
            dict: All the core configuration parameters

        """
        return self.get_core_ids_proj(self._prj_cfg.get_prj_config())


class HICore(ProblemLogger):
    """A class holding HI core configuration data."""

    DTC_DEFINITION_FILE_NAME = 'DTCs.yaml'
    FILE_NAME = 'VcCoreSupplierAbstraction'

    def __init__(self, project_cfg, unit_cfgs):
        """Parse the config files to an internal representation.

        Args:
            project_cfg (BuildProjConfig): Project configuration.
            unit_cfgs (UnitConfigs): Unit definitions.
        """
        super().__init__()
        self._prj_cfg = project_cfg
        self._unit_cfgs = unit_cfgs
        self.diagnostic_trouble_codes = self.get_diagnostic_trouble_codes()

    def _get_project_dtcs(self):
        """Return a set with DTCs in the currently included SW-Units.

        Returns:
            (set): Set of DTCs in the currently included SW-Units.
        """
        project_dtcs = set()
        unit_cfg = self._unit_cfgs.get_per_unit_cfg()
        for unit, data in unit_cfg.items():
            event_data = data.get('core', {}).get('Events')
            if event_data is None:
                self.critical(f'No "core" or "core.Events" key in unit config for {unit}.')
                continue
            project_dtcs |= set(event_data.keys())
        return project_dtcs

    def _read_dtc_yaml_file(self):
        """Return a set with DTCs loaded from the project DTC yaml file.

        Returns:
            (set): Set of DTCs loaded from the DTC yaml file.
        """
        diagnostic_trouble_codes = {}
        dtc_definition_file_path = Path(self._prj_cfg.get_prj_cfg_dir(),  self.DTC_DEFINITION_FILE_NAME)
        if dtc_definition_file_path.exists():
            with dtc_definition_file_path.open(mode='r', encoding='utf-8') as dtc_fh:
                yaml = YAML(typ='safe', pure=True)
                diagnostic_trouble_codes = yaml.load(dtc_fh)
        else:
            self.warning(
                'Unable to generate DTC function calls. '
                f'Cannot find file: {dtc_definition_file_path.as_posix()}.'
            )
        return diagnostic_trouble_codes

    def get_diagnostic_trouble_codes(self):
        """Return a set of DTCs appearing in both the project and the project yaml file.

        Returns:
            (dict): Dict of DTCs, project yaml dict where the keys also appear in the project.
        """
        project_dtcs = self._get_project_dtcs()
        yaml_dtc_dict = self._read_dtc_yaml_file()
        yaml_dtcs = set(yaml_dtc_dict.keys())
        dtcs_not_in_project = yaml_dtcs - project_dtcs
        dtcs_not_in_yaml = project_dtcs - yaml_dtcs
        for key in dtcs_not_in_project:
            self.warning(f'Ignoring DTC {key} since it does not appear in any model.')
            del yaml_dtc_dict[key]
        for key in dtcs_not_in_yaml:
            self.warning(f'Ignoring DTC {key} since it does not appear in the project DTC yaml file.')
        return yaml_dtc_dict

    def get_header_content(self):
        """Get content for the DTC header file.

        Returns:
            (list(str)): List of lines to write to the DTC header file.
        """
        name = self._prj_cfg.get_a2l_cfg()['name']
        header_guard = f'{self.FILE_NAME.upper()}_H'
        header = [
            f'#ifndef {header_guard}\n',
            f'#define {header_guard}\n',
            '\n',
            '/* Core API Supplier Abstraction */\n',
            '\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{name}.h"\n',
            '\n'
        ]
        footer = [f'\n#endif /* {header_guard} */\n']

        if not self.diagnostic_trouble_codes:
            return header + footer

        body = [
            '/* enum EventStatus {passed=0, failed=1, prepassed=2, prefailed=3} */\n',
            '#define Dem_SetEventStatus(EventName, EventStatus)',
            '  ',
            f'{self.FILE_NAME}_##EventName##_SetEventStatus(EventStatus)\n'
        ]
        body.append(f'\n#include "{build_defs.PREDECL_CODE_ASIL_D_START}"\n')
        for dtc_name in self.diagnostic_trouble_codes:
            body.append(f'UInt8 {self.FILE_NAME}_{dtc_name}_SetEventStatus(UInt8 EventStatus);\n')
        body.append(f'#include "{build_defs.PREDECL_CODE_ASIL_D_END}"\n')
        return header + body + footer

    def get_source_content(self):
        """Get content for the DTC source file.

        Returns:
            (list(str)): List of lines to write to the DTC source file.
        """
        header = [
            f'#include "{self.FILE_NAME}.h"\n',
            '\n'
        ]

        if not self.diagnostic_trouble_codes:
            return header

        body = [f'#include "{build_defs.CVC_CODE_ASIL_D_START}"\n']
        for dtc_name, dtc_id in self.diagnostic_trouble_codes.items():
            # hex function removes leading 0, below solution zero pads to 6 digits
            dtc_hex_str = f"0x{dtc_id:06X}"
            body.extend([
                f'UInt8 {self.FILE_NAME}_{dtc_name}_SetEventStatus(UInt8 EventStatus)\n',
                '{\n',
                f'    Rte_Call_Event_DTC_{dtc_hex_str}_SetEventStatus(EventStatus);\n',
                '    return 0;\n',
                '}\n',
                '\n'
            ])
        body.append(f'#include "{build_defs.CVC_CODE_ASIL_D_END}"\n')

        return header + body

    def generate_dtc_files(self):
        """Generate required HI Core header files.
        Only use for some projects, which doesn't copy static code."""
        file_contents = {
            '.h': self.get_header_content(),
            '.c': self.get_source_content()
        }
        src_dst_dir = self._prj_cfg.get_src_code_dst_dir()
        for extension, content in file_contents.items():
            file_path = Path(src_dst_dir, self.FILE_NAME + extension)
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(content)


class ZCCore(ProblemLogger):
    """A class holding ZC core configuration data."""

    FILE_NAME = 'VcCoreSupplierAbstraction'

    def __init__(self, project_cfg, unit_cfgs):
        """Parse the config files to an internal representation.

        Args:
            project_cfg (BuildProjConfig): Project configuration.
            unit_cfgs (UnitConfigs): Unit definitions.
        """
        super().__init__()
        self._prj_cfg = project_cfg
        self._unit_cfgs = unit_cfgs
        self.project_dtcs = self._get_project_dtcs()

    def _get_project_dtcs(self):
        """Return a set with DTCs in the currently included SW-Units.

        Returns:
            (set): Set of DTCs in the currently included SW-Units.
        """
        project_dtcs = set()
        unit_cfg = self._unit_cfgs.get_per_unit_cfg()
        for unit, data in unit_cfg.items():
            event_data = data.get('core', {}).get('Events')
            if event_data is None:
                self.critical(f'No "core" or "core.Events" key in unit config for {unit}.')
                continue
            project_dtcs |= set(event_data.keys())
        return project_dtcs

    def get_diagnostic_trouble_codes(self, event_data):
        """Return a set of DTCs appearing in both the project and the project yaml file.

        Args:
            event_data (dict): Diagnositc event data.
        Returns:
            (dict): Dict of DTCs, project yaml dict where the keys also appear in the project.
        """
        valid_dtcs = {}

        dtcs_not_in_yaml = self.project_dtcs - set(event_data.keys())
        for key in dtcs_not_in_yaml:
            self.warning(f'Ignoring DTC {key} since it does not appear in the project diagnostics yaml file.')

        for dtc_name, dtc_data in event_data.items():
            if dtc_name not in self.project_dtcs and not dtc_data.get("manual", False):
                self.warning(f'Ignoring DTC {dtc_name}, not defined in any model.')
                continue
            valid_dtcs[dtc_name] = {k: v for k, v in dtc_data.items() if k != "manual"}
        return valid_dtcs

    def get_header_content(self):
        """Get content for the DTC header file.

        Returns:
            (list(str)): List of lines to write to the DTC header file.
        """
        name = self._prj_cfg.get_composition_config("softwareComponentName")
        header_guard = f'{self.FILE_NAME.upper()}_H'
        header = [
            f'#ifndef {header_guard}\n',
            f'#define {header_guard}\n',
            '\n',
            '/* Core API Supplier Abstraction */\n',
            '\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{name}.h"\n',
            '\n'
        ]
        footer = [f'\n#endif /* {header_guard} */\n']

        body = [
            '/* EventStatus is an enumeration with members {passed=0, failed=1, prepassed=2, prefailed=3} */\n',
            '#define Dem_SetEventStatus(EventName, EventStatus)',
            '  ',
            'Rte_Call_Event_##EventName##_SetEventStatus(EventStatus)\n'
        ]
        return header + body + footer

    def generate_dtc_files(self):
        """Generate required ZC Core header files.
        Only use for some projects, which doesn't copy static code."""
        includeDiagnostics = self._prj_cfg.get_composition_config("includeDiagnostics")
        if includeDiagnostics in ["manual", "manual_dtcs"]:
            self.warning(f'includeDiagnostics is set to {includeDiagnostics}, not generating DTC files.')
            return
        file_contents = {
            '.h': self.get_header_content()
        }
        src_dst_dir = self._prj_cfg.get_src_code_dst_dir()
        for extension, content in file_contents.items():
            file_path = Path(src_dst_dir, self.FILE_NAME + extension)
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(content)
