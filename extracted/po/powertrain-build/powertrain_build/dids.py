# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module containing classes for DID definitions.

This module is used to parse DID definition files and merge with the unit definitions to find DIDs in a project.
It then generates the DID definition c-files for the supplier DID API.
"""

import csv
import os
from pathlib import Path
from ruamel.yaml import YAML
from powertrain_build import build_defs
from powertrain_build.lib.helper_functions import deep_dict_update
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.types import byte_size, get_ec_type, get_float32_types
from powertrain_build.unit_configs import CodeGenerators


def get_dids_in_prj(unit_cfgs):
    """Return a dict with DIDs in the currently included SW-Units.

    Args:
        unit_cfgs (UnitConfigs): Unit definitions.
    Returns:
        error_message (str): Message in case something went wrong.
        dict: a dict with all dids in the project, in the below format:

    ::

        {'DID_VARIABLE_NAME': {
            'handle': 'VcRegCh/VcRegCh/Subsystem/VcRegCh/1000_VcRegCh/1600_DID/Gain14',
            'configs': ['all'],
            'type': 'UInt32',
            'unit': '-',
            'lsb': 1,
            'max': 20,
            'min': 0,
            'offset': 0,
            'description': 'Actual Regen State',
            'name': 'DID_VARIABLE_NAME',
            'class': 'CVC_DISP'
            }
        }
    """
    dids_prj = {}
    error_messages = []
    unit_cfg = unit_cfgs.get_per_unit_cfg()
    for unit, data in unit_cfg.items():
        dids = data.get('dids')
        if dids is None:
            error_messages.append(f'No "dids" key in unit config for {unit}.')
            continue
        for name, did in dids.items():
            dids_prj[name] = did
    return error_messages, dids_prj


class DIDs(ProblemLogger):
    """A class for handling of DID definitions."""

    def __init__(self, build_cfg, unit_cfgs):
        """Parse DID definition files referenced by project config.

        Args:
            build_cfg (BuildProjConfig): Project configuration
            unit_cfgs (UnitConfigs): Unit definitions
        """
        super().__init__()
        self._build_cfg = build_cfg
        self._unit_cfgs = unit_cfgs
        did_filename = self._build_cfg.get_did_cfg_file_name()
        cfg_dir = self._build_cfg.get_prj_cfg_dir()
        did_f32_cfg_file = os.path.join(cfg_dir, did_filename + '_Float32.csv')
        did_u32_cfg_file = os.path.join(cfg_dir, did_filename + '_UInt32.csv')
        self._dids_f32 = self._load_did_config_files(did_f32_cfg_file)
        self._dids_u32 = self._load_did_config_files(did_u32_cfg_file)
        self.fh_h = None
        self.fh_c = None
        get_did_error_messages, self._did_dict = get_dids_in_prj(unit_cfgs)
        self._did_defs = self.get_did_config()
        self._float32_types = get_float32_types()
        if get_did_error_messages:
            self.critical('\n'.join(get_did_error_messages))

    def _load_did_config_files(self, config_file):
        """Load the did config files."""
        dids = {}
        with open(config_file, mode='r', encoding='utf-8') as did_fh:
            csv_did = csv.reader(did_fh, delimiter=';')
            did = list(csv_did)
            dids['dids'] = {row[0]: int(row[1], 16) for row in did[3:]}
            dids['start_did'] = int(did[1][0], 16)
            dids['end_did'] = int(did[1][1], 16)
        self._check_dids(dids)
        return dids

    @staticmethod
    def _check_dids(dids):
        """Check that all dids are within the start and end values."""
        start_did = dids['start_did']
        end_did = dids['end_did']

        for var, did in dids['dids'].items():
            if did < start_did:
                raise ValueError(f'{var} has a too low did 0x{did:X} start did is 0x{start_did:X}')
            if did > end_did:
                raise ValueError(f'{var} has a too high did 0x{did:X} start did is 0x{start_did:X}')

    def gen_did_def_files(self, filename):
        """Generate the VcDidDefinitions.c & h files used by the Did-API."""
        with open(filename + '.h', 'w', encoding="utf-8") as self.fh_h:
            with open(filename + '.c', 'w', encoding="utf-8") as self.fh_c:
                dids_f32, dids_u32, errors = self._check_and_reformat_dids()
                self._gen_did_def_c_file(dids_f32, dids_u32, errors)
                self._gen_did_def_h_file(dids_f32, dids_u32)
        return errors

    def _check_and_reformat_dids(self):
        """Check that DIDs are defined and create two new dicts."""
        dids_f32 = {}
        dids_u32 = {}
        did_def_f32s = self._did_defs['Float32']['dids']
        did_def_u32s = self._did_defs['UInt32']['dids']
        errors = []
        for sig in sorted(self._did_dict.keys()):
            did = self._did_dict[sig]
            if did['type'] in self._float32_types:
                if sig in did_def_f32s:
                    dids_f32[did_def_f32s[sig]] = did
                else:
                    msg = f'Did for Float32 signal "{sig}" not defined'
                    self.critical(msg)
                    errors.append(msg)
            else:
                if sig in did_def_u32s:
                    dids_u32[did_def_u32s[sig]] = did
                else:
                    msg = f'Did for UInt32 signal "{sig}" not defined'
                    self.critical(msg)
                    errors.append(msg)
        return (dids_f32, dids_u32, errors)

    def _get_datatypes(self):
        tl_types = ['UInt8', 'Int8', 'UInt16', 'Int16', 'UInt32', 'Int32', 'Float32', 'Bool']
        data_types_tl = [f'{tl_type}_' for tl_type in tl_types]
        data_types_ec = [f'{get_ec_type(tl_type)}_' for tl_type in tl_types]
        if len(self._unit_cfgs.code_generators) > 1:
            self.warning('Cannot generate DIDs for more than one generator.'
                         'Defaulting to TargetLink')
            return ', '.join(data_types_tl)
        if CodeGenerators.target_link in self._unit_cfgs.code_generators:
            return ', '.join(data_types_tl)
        return ', '.join(data_types_ec)

    def _get_type(self, tl_type):
        if CodeGenerators.target_link in self._unit_cfgs.code_generators:
            return tl_type
        return get_ec_type(tl_type)

    def _gen_did_def_h_file(self, dids_f32, dids_u32):
        """Generate the VcDidDefinitions.h files used by the Did-API."""
        _, f_name = os.path.split(self.fh_h.name)
        header_def_name = f_name.upper().replace('.', '_')
        self.fh_h.write(f'#ifndef {header_def_name}\n')
        self.fh_h.write(f'#define {header_def_name}\n\n')
        self.fh_h.write(self._unit_cfgs.base_types_headers)
        self.fh_h.write(f'enum Datatypes {{{self._get_datatypes()}}};\n\n')
        self.fh_h.write(f'#define DID_DATASTRUCT_LEN_FLOAT32 {len(dids_f32)}\n')
        self.fh_h.write(f'#define DID_DATASTRUCT_LEN_UINT32 {len(dids_u32)}\n\n')
        uint16_type = self._get_type('UInt16')
        float32_type = self._get_type('Float32')
        self.fh_h.write('struct DID_Mapping_UInt32 {\n\t'
                        f'{uint16_type} DID;'
                        '\n\tvoid* data;\n\tenum Datatypes type;\n};\n\n')
        self.fh_h.write('struct DID_Mapping_Float32 {\n\t'
                        f'{uint16_type} DID;'
                        '\n\t'
                        f'{float32_type}* data;'
                        '\n};\n\n')

        self.fh_h.write(f'#include "{build_defs.PREDECL_START}"\n')

        self.fh_h.write('extern const struct DID_Mapping_UInt32 DID_data_struct_UInt32[];\n')
        self.fh_h.write('extern const struct DID_Mapping_Float32 DID_data_struct_Float32[];\n')

        self.fh_h.write('/* Floats */\n')

        for key in sorted(dids_f32.keys()):
            did = dids_f32[key]
            self.fh_h.write(f'extern {did["type"]} {did["name"]}; /* Did id: 0x{key:X} */\n')

        self.fh_h.write('/* Integers & Bools */\n')

        for key in sorted(dids_u32.keys()):
            did = dids_u32[key]
            self.fh_h.write(f'extern {did["type"]} {did["name"]}; /* Did id: 0x{key:X} */\n')

        self.fh_h.write(f'#include "{build_defs.PREDECL_END}"\n')
        self.fh_h.write(f'\n#endif /* {header_def_name} */\n')

    def _gen_did_def_c_file(self, dids_f32, dids_u32, errors):
        """Generate the VcDidDefinitions.c files used by the Did-API."""
        _, filename = os.path.split(self.fh_h.name)
        self.fh_c.write(f'#include "{filename}"\n\n')
        self.fh_c.write(f'#include "{build_defs.CVC_CODE_START}"\n\n')
        self.fh_c.write('/* The table shall be sorted in ascending Did is order!\n'
                        ' If not the search algorithm does not work */\n')
        self.fh_c.write('const struct DID_Mapping_Float32 DID_data_struct_Float32[] = {\n')

        keys = sorted(dids_f32.keys())
        for key in keys:
            did = dids_f32[key]
            if key == keys[-1]:
                delim = ' '
            else:
                delim = ','
            self.fh_c.write('\t{0x%X, &%s}%c /* %s */ \n' %
                            (key, did['name'], delim, did['handle']))
        if not keys:
            self.fh_c.write('\t{0x0000, 0L} /* Dummy entry */ \n')
        self.fh_c.write('};\n\n')

        self.fh_c.write('const struct DID_Mapping_UInt32 DID_data_struct_UInt32[] = {\n')
        keys = sorted(dids_u32.keys())
        for key in keys:
            did = dids_u32[key]
            if key == keys[-1]:
                delim = ' '
            else:
                delim = ','
            self.fh_c.write('\t{0x%X, &%s, %s_}%c /* %s */ \n' %
                            (key, did['name'], did['type'], delim, did['handle']))

        if not keys:
            self.fh_c.write(f'\t{{0x0000, 0L, {self._get_type("UInt32")}_}} /* Dummy entry */ \n')
        self.fh_c.write('};\n\n')

        if errors:
            self.fh_c.write('/* *** DIDs not in the definition file! ****\n')
            for error in errors:
                self.fh_c.write(f'{error}\n')
            self.fh_c.write('*/\n')

        self.fh_c.write(f'\n#include "{build_defs.CVC_CODE_END}"\n')
        self.fh_c.write('\n/*------------------------------------------------------'
                        '----------------------*\\\n  END OF FILE\n\\*-------------'
                        '---------------------------------------------------------------*/')

    def gen_did_carcom_extract(self, filename):
        """Generate the csv-file used for carcom database import."""
        with open(filename, 'w', encoding="utf-8") as carcom_file:
            for sig in sorted(self._did_dict.keys()):
                did = self._did_dict[sig]
                carcom_file.write(self._format_did_csv_line(did))

    @staticmethod
    def _convert_value(value, type, default_value=0):
        if value in ['', '-']:
            return type(default_value)
        return type(value)

    @staticmethod
    def _hex_location(value):
        return hex(value).upper().lstrip('0X')

    def _format_did_csv_line(self, did):
        """Format the line based on the did.

        Arguments:
        did (dict): DID data
        """
        did_line = '{' + '};{'.join(['location',
                                     'description',
                                     'name',
                                     'name',
                                     'bytes',
                                     'offset',
                                     'bits',
                                     'data_type',
                                     'nine',
                                     'ten',
                                     'low',
                                     'high',
                                     'scaling',
                                     'compare',
                                     'unit',
                                     'sixteen',
                                     'service',
                                     'eighteen',
                                     'sessions']) + '}\n'
        float_format = '06'
        compare = ''
        did_bytes = 4
        did_offset = 0  # Always use 0. Not sure why.
        did_bits = 8 * did_bytes
        service = 17
        sessions = '22: 01 02 03'
        unknown = ''  # Fields were empty in old system
        did_def_f32s = self._did_defs['Float32']['dids']
        did_def_u32s = self._did_defs['UInt32']['dids']
        if did['name'] in did_def_f32s:
            location = self._hex_location(did_def_f32s[did['name']])
        elif did['name'] in did_def_u32s:
            location = self._hex_location(did_def_u32s[did['name']])
        else:
            self.warning('Could not find location for %s', did['name'])
            location = unknown
        if did['type'] in self._float32_types:
            did_type = '4-byte float'
            scaling = 'x*1'
        else:
            did_type = 'Unsigned'
            u32_scaling_base = '(x-2147483647){{operator}}{{lsb:{float_format}}} {{sign}} {{offset:{float_format}}}'
            u32_scaling = u32_scaling_base.format(float_format=float_format)
            offset = self._convert_value(did['offset'], float, 0)
            if offset > 0:
                sign = '+'
            else:
                sign = '-'
            lsb = self._convert_value(did['lsb'], float, 1)
            if lsb > 0:
                operator = '*'
            else:
                operator = '/'
                lsb = 1.0/lsb  # Why we do this, I do not know.
            scaling = u32_scaling.format(operator=operator,
                                         lsb=lsb,
                                         sign=sign,
                                         offset=offset)

        return did_line.format(location=location,
                               name=did['name'],
                               description=did['description'],
                               bytes=did_bytes,
                               offset=did_offset,
                               bits=did_bits,
                               data_type=did_type,
                               nine=unknown,
                               ten=unknown,
                               low=did['min'],
                               high=did['max'],
                               scaling=scaling,
                               compare=compare,
                               unit=did['unit'],
                               sixteen=unknown,
                               service=service,
                               eighteen=unknown,
                               sessions=sessions)

    def get_did_config(self):
        """Return a dict with the defined DIDs for all configs.

        Returns:
            dict: a dict with the DIDs defined for all configs

        """
        # self._checkConfig()
        return {'Float32': self._dids_f32, 'UInt32': self._dids_u32}


class HIDIDs(ProblemLogger):
    """A class for handling of HI DID definitions."""

    def __init__(self, build_cfg, unit_cfgs):
        """Init.

        Args:
            build_cfg (BuildProjConfig): Project configuration
            unit_cfgs (UnitConfigs): Unit definitions
        """
        super().__init__()
        self._build_cfg = build_cfg
        self._unit_cfgs = unit_cfgs
        self.file_name = 'VcDIDAPI'
        self.did_dict = self._compose_did_data()

    def _load_did_config_files(self, config_file):
        """Load the did config files.

        Args:
            config_file (str): Path to DID configuration file.
        Returns:
            dids (dict): Parsed DIDs from the configuration file.
        """
        dids = {}
        config_file_path = Path(config_file)
        if config_file_path.exists():
            with config_file_path.open(mode='r', encoding='utf-8') as did_fh:
                yaml = YAML(typ='safe', pure=True)
                dids = self._verify_did_config_dict(yaml.load(did_fh))
        else:
            self.warning(f'Unable to parse DIDs. Cannot find file: {config_file_path.as_posix()}.')
        return dids

    def _verify_did_config_dict(self, dids):
        """Verify the structure of the dict from the DID configuration file.
        Missing keys will be added but also produce critical errors.

        Args:
            dids (dict): DIDs parsed from DID configuration file.
        Returns:
            (dict): Updated DID dict.
        """
        optional_keys = {
            'nr_of_bytes',
        }
        expected_keys = {
            'id',
            'data_type',
            'function_type',
        }
        expected_function_type_keys = {
            'read_data',
            'read_data_max',
            'read_data_min',
            'condition_check',
            'condition_check_max',
            'condition_check_min',
        }
        for did, did_data in dids.items():
            did_keys = set(did_data.keys())
            used_optional_keys = did_keys & optional_keys
            unknown_keys = did_keys - (expected_keys | optional_keys)
            missing_keys = expected_keys - did_keys
            for key in used_optional_keys:
                self.info(f'Using optional key {key} for DID {did}.')
            for key in unknown_keys:
                self.warning(f'Ignoring unknown element {key} for DID {did}.')
                del did_data[key]
            for key in missing_keys:
                self.critical(f'DID {did} is missing element {key}.')
                did_data[key] = '<missing>'
            if did_data['function_type'] not in expected_function_type_keys:
                self.critical(f"DID {did} lists unknown function type {did_data['function_type']}")
                did_data['function_type'] = '<missing>'
        return dids

    def _compose_did_data(self):
        """Gather and merge DID data from project simulink models and DID configuration file.

        Returns:
            did_dict (dict): Dict containing project DID data.
        """
        get_did_error_messages, project_dids = get_dids_in_prj(self._unit_cfgs)
        if get_did_error_messages:
            self.critical('\n'.join(get_did_error_messages))
            return {}

        did_filename = self._build_cfg.get_did_cfg_file_name()
        config_directory = self._build_cfg.get_prj_cfg_dir()
        did_config_file = os.path.join(config_directory, did_filename)
        dids = self._load_did_config_files(did_config_file)

        did_dict = self.verify_dids(project_dids, dids)
        for data in did_dict.values():
            data['function'] = self.compose_did_function(data)

        return did_dict

    @staticmethod
    def compose_did_function(did_data):
        """Compose DID function calls.
        Args:
            did_data (dict): Dict describing a DID in the project.
        Returns:
            function (str): Function to generate for given DID.
        """
        did_id = did_data["id"]
        data_type = did_data["data_type"]
        type_to_function_map = {
            '<missing>': f'DID_{did_id}_Missing({data_type} *Data)',
            'read_data': f'DID_{did_id}_Runnable_ReadData({data_type} *Data)',
            'read_data_max': f'DID_{did_id}_Runnable_MAX_ReadData({data_type} *Data)',
            'read_data_min': f'DID_{did_id}_Runnable_MIN_ReadData({data_type} *Data)',
            'condition_check': f'DID_{did_id}_Runnable_ConditionCheckRead({data_type} *ErrorCode)',
            'condition_check_max': f'DID_{did_id}_Runnable_MAX_ConditionCheckRead({data_type} *ErrorCode)',
            'condition_check_min': f'DID_{did_id}_Runnable_MIN_ConditionCheckRead({data_type} *ErrorCode)'
        }
        return type_to_function_map[did_data['function_type']]

    def verify_dids(self, project_dids, dids):
        """Verify the DIDs.

        * Model DIDs must be defined in DID configuration file.
        * ID numbers can only appear once per function type.

        Args:
            project_dids (dict): DIDs listed in project/simulink models.
            dids (dict): DIDs listed in the DID configuration file.
        Returns:
            valid_dids (dict): Validated DIDs listed in both DID configuration file as well as project.
        """
        valid_dids = {}
        did_id_usage = {}

        if not project_dids:
            for did in dids:
                self.warning(f'Ignoring DID {did}, not defined in any model.')
            return valid_dids

        for name in project_dids:
            if name not in dids:
                self.warning(f'DID {name} not defined in DID defintion file.')
                continue

            did_id = dids[name]['id']
            function_type = dids[name]['function_type']
            if did_id in did_id_usage:
                if function_type in did_id_usage[did_id]:
                    self.critical(
                        f'ID {did_id} is '
                        f'already used for DID {did_id_usage[did_id][function_type]} of '
                        f'function type {function_type}.'
                    )
                    continue
                did_id_usage[did_id][function_type] = name
            else:
                did_id_usage[did_id] = {function_type: name}

            valid_dids[name] = deep_dict_update(dids[name], project_dids[name])

        return valid_dids

    def get_header_file_content(self):
        """Get content for the DID API header file.

        Returns:
            (list(str)): List of lines to write to DID API header file.
        """
        name = self._build_cfg.get_a2l_cfg()['name']
        header_guard = f'{self.file_name.upper()}_H'
        header = [
            f'#ifndef {header_guard}\n',
            f'#define {header_guard}\n',
            '\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{name}.h"\n',
            '\n'
        ]
        footer = [f'\n#endif /* {header_guard} */\n']

        if not self.did_dict:
            return header + footer

        body = [f'#include "{build_defs.PREDECL_DISP_ASIL_D_START}"\n']
        for did_data in self.did_dict.values():
            define = did_data["class"].split('/')[-1]  # E.q. for ASIL D it is ASIL_D/CVC_DISP_ASIL_D
            body.append(f'extern {define} {did_data["type"]} {did_data["name"]};\n')
        body.append(f'#include "{build_defs.PREDECL_DISP_ASIL_D_END}"\n')

        body.append(f'\n#include "{build_defs.PREDECL_CODE_ASIL_D_START}"\n')
        for did_data in self.did_dict.values():
            body.append(f'void {did_data["function"]};\n')
        body.append(f'#include "{build_defs.PREDECL_CODE_ASIL_D_END}"\n')

        return header + body + footer

    def get_source_file_content(self):
        """Get content for the DID API source file.

        Returns:
            (list(str)): List of lines to write to DID API source file.
        """
        header = [
            f'#include "{self.file_name}.h"\n',
            '\n'
        ]

        if not self.did_dict:
            return header

        body = [f'#include "{build_defs.CVC_CODE_ASIL_D_START}"\n']
        for did, did_data in self.did_dict.items():
            size = f'{did_data["nr_of_bytes"]}' if 'nr_of_bytes' in did_data else f'sizeof({did_data["data_type"]})'
            if 'ConditionCheckRead' in did_data["function"]:
                argument = 'ErrorCode'
            else:
                argument = 'Data'
            body.extend([
                f'void {did_data["function"]}\n',
                '{\n',
                f'    memcpy({argument}, &{did}, {size});\n',
                '}\n'
            ])
        body.append(f'#include "{build_defs.CVC_CODE_ASIL_D_END}"\n')

        return header + body

    def generate_did_files(self):
        """Generate required DID API files.
        Only use for some projects, which doesn't copy static code."""
        file_contents = {
            '.h': self.get_header_file_content(),
            '.c': self.get_source_file_content()
        }
        src_dst_dir = self._build_cfg.get_src_code_dst_dir()
        for extension, content in file_contents.items():
            file_path = Path(src_dst_dir, self.file_name + extension)
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(content)


class ZCDIDs(ProblemLogger):
    """A class for handling of ZC DID definitions."""

    def __init__(self, build_cfg, unit_cfgs):
        """Init.

        Args:
            build_cfg (BuildProjConfig): Project configuration
            unit_cfgs (UnitConfigs): Unit definitions
        """
        super().__init__()
        self._build_cfg = build_cfg
        self._unit_cfgs = unit_cfgs
        self._valid_dids = None
        prefix = self._build_cfg.get_scheduler_prefix()
        self.operation_file_name = 'VcDIDAPI'
        self.sender_receiver_file_name = f'{prefix}UpdatingDIDValues'
        self.project_dids = self._get_project_dids()

    @property
    def valid_dids(self):
        return self._valid_dids

    @valid_dids.setter
    def valid_dids(self, yaml_dids):
        """Return a set of DIDs appearing in both the project and the project yaml file.

        Args:
            yaml_dids (dict): DIDs listed in the DID configuration yaml file.
        Returns:
            valid_dids (dict): Validated DIDs listed in both DID configuration yaml file as well as project.
        """
        self._valid_dids = {}

        dids_not_in_yaml = set(self.project_dids.keys()) - set(yaml_dids.keys())
        for did in dids_not_in_yaml:
            self.critical(f'DID {did} not defined in project diagnostics yaml file.')

        for did, did_data in yaml_dids.items():
            if did_data.get('manual', False):
                self._valid_dids[did] = {k: v for k, v in did_data.items() if k != "manual"}
                continue
            if did not in self.project_dids:
                self.warning(f'Ignoring DID {did}, not defined in any model.')
                continue
            data_type = self.project_dids[did]['type']
            if not data_type.startswith('UInt'):
                self.warning(f'Ignoring DID {did} of type {data_type}, only unsigned integers are supported.')
                continue
            self._valid_dids[did] = did_data

    def _get_project_dids(self):
        """Return a dict with DIDs defined in the project.
        Throws a critical error if something goes wrong.

        Returns:
            project_dids (dict): a dict with all dids in the project.
        """
        get_did_error_messages, project_dids = get_dids_in_prj(self._unit_cfgs)
        if get_did_error_messages:
            self.critical('\n'.join(get_did_error_messages))
            return {}
        return project_dids

    def _get_sender_receiver_reverse_bytes_function_declaration(self):
        """Get content for the declaration of the function that reverses the byte order of the S/R DID values.

        Returns:
            (str): Line resulting in the reverse byte order function declaration.
        """
        return '\nstatic UInt32 ReverseBytes(UInt32 value, UInt8 byteSize);\n'

    def _get_sender_receiver_reverse_bytes_function(self):
        """Get content for the function that reverses the byte order of the S/R DID values.

        Returns:
            (list(str)): List of lines resulting in the reverse byte order function.
        """
        return [
            f'#include "{build_defs.CVC_CODE_ASIL_D_START}"\n',
            'static UInt32 ReverseBytes(UInt32 value, UInt8 byteSize)\n',
            '{\n',
            '  UInt32 result = 0U;\n',
            '  for (UInt8 i = 0; i < byteSize; i++) {\n',
            '    result = (result << 8) | ((value >> (8 * i)) & 0xFF);\n',
            '  }\n',
            '  return result;\n',
            '}\n',
            f'#include "{build_defs.CVC_CODE_ASIL_D_END}"\n'
        ]

    def _get_sender_receiver_header_file_content(self):
        """Get content for the S/R DID API header file.

        The function in this file is a runnable generated by yaml2arxml.

        Returns:
            (bool): True if any S/R DIDs are defined.
            (list(str)): List of lines to write to the S/R DID API header file.
        """
        name = self._build_cfg.get_composition_config("softwareComponentName")
        header_guard = f'{self.sender_receiver_file_name.upper()}_H'
        header = [
            f'#ifndef {header_guard}\n',
            f'#define {header_guard}\n',
            '\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{name}.h"\n',
            '\n'
        ]
        footer = [f'\n#endif /* {header_guard} */\n']

        if not self.valid_dids:
            return False, header + footer

        variable_declarations = []
        function_declarations = []
        sender_receiver_dids_exist = False
        for did, did_data in self.valid_dids.items():
            project_did_data = self.project_dids[did]
            if did_data.get('PortType', 'dummy') not in ['BOTH', 'SENDER-RECEIVER']:
                continue  # C/R DIDs are handled in _get_operation... functions
            if not project_did_data['type'].startswith('UInt'):
                self.warning(
                    f'Ignoring DID {did} of type {project_did_data["type"]}, only unsigned integers are supported.'
                )
                continue
            sender_receiver_dids_exist = True
            define = self.project_dids[did]["class"].split('/')[-1]  # E.q. for ASIL D it is ASIL_D/CVC_DISP_ASIL_D
            variable_declarations.append(
                f'extern {define} {self.project_dids[did]["type"]} {self.project_dids[did]["name"]};\n'
            )
            function_declarations.append(
                f'extern UInt8 Rte_Write_DataServices_DID_{did}_data({project_did_data["type"]} {did});\n'
            )

        function_declarations.append(f'\nvoid Run_{self.sender_receiver_file_name}(void);\n')
        function_declarations.append(self._get_sender_receiver_reverse_bytes_function_declaration())

        body = [
            f'#include "{build_defs.PREDECL_DISP_ASIL_D_START}"\n',
            *variable_declarations,
            f'#include "{build_defs.PREDECL_DISP_ASIL_D_END}"\n',
            f'\n#include "{build_defs.PREDECL_CODE_ASIL_D_START}"\n',
            *function_declarations,
            f'#include "{build_defs.PREDECL_CODE_ASIL_D_END}"\n',
        ]

        return sender_receiver_dids_exist, header + body + footer

    def _get_sender_receiver_source_file_content(self):
        """Get content for the S/R DID API source file.

        The function in this file is a runnable generated by yaml2arxml.

        Returns:
            (bool): True if any S/R DIDs are defined.
            (list(str)): List of lines to write to the S/R DID API source file.
        """
        header = [
            f'#include "{self.sender_receiver_file_name}.h"\n',
            '\n'
        ]

        if not self.valid_dids:
            return False, header

        sender_receiver_dids_exist = False
        body = [
            f'#include "{build_defs.CVC_CODE_ASIL_D_START}"\n',
            f'void Run_{self.sender_receiver_file_name}(void)\n',
            '{\n'
        ]
        for did, did_data in self.valid_dids.items():
            project_did_data = self.project_dids[did]
            if did_data.get('PortType', 'dummy') not in ['BOTH', 'SENDER-RECEIVER']:
                continue  # C/R DIDs are handled in _get_operation... functions
            if not project_did_data['type'].startswith('UInt'):
                self.warning(
                    f'Ignoring DID {did} of type {project_did_data["type"]}, only unsigned integers are supported.'
                )
                continue
            sender_receiver_dids_exist = True
            did_byte_size = byte_size(project_did_data['type'])
            body.append(f'  Rte_Write_DataServices_DID_{did}_data(ReverseBytes({did}, {did_byte_size}));\n')
        body.extend([
            '}\n',
            f'#include "{build_defs.CVC_CODE_ASIL_D_END}"\n'
        ])
        body.append('\n')
        body.extend(self._get_sender_receiver_reverse_bytes_function())

        return sender_receiver_dids_exist, header + body

    def _get_operation_data(self, operation, did_data):
        """Get operation function data of supported operations.

        Args:
            operation (str): Operation to get data for.
            did_data (dict): DID data.
        Returns:
            (dict): Operation function data.
        """
        array_size = byte_size(did_data['type'])
        if array_size > 1:
            read_data_declaration = f'UInt8 Run_{did_data["name"]}_ReadData(UInt8 Data[{array_size}])'
            read_data_definition = (
                '{\n'
                f'  for (UInt8 i = 0U; i < {array_size}; i++) {{\n'
                f'    Data[{array_size} - 1 - i] = ({did_data["name"]} >> (8 * i)) & 0xFF;\n'
                '  }\n'
                '  return 0U;\n'
                '}\n'
            )
        else:
            read_data_declaration = f'UInt8 Run_{did_data["name"]}_ReadData(UInt8 *Data)'
            read_data_definition = (
                '{\n'
                f'  *Data = {did_data["name"]};\n'
                '  return 0U;\n'
                '}\n'
            )
        operation_data = {
            'ReadData': {
                'declaration': read_data_declaration,
                'body': read_data_definition,
            }
        }
        if operation not in operation_data:
            return None
        return operation_data[operation]

    def _get_operation_header_file_content(self):
        """Get content for the DID API header file.

        Returns:
            (list(str)): List of lines to write to the DID API header file.
        """
        name = self._build_cfg.get_composition_config("softwareComponentName")
        header_guard = f'{self.operation_file_name.upper()}_H'
        header = [
            f'#ifndef {header_guard}\n',
            f'#define {header_guard}\n',
            '\n',
            '#include "tl_basetypes.h"\n',
            f'#include "Rte_{name}.h"\n',
            '\n'
        ]
        footer = [f'\n#endif /* {header_guard} */\n']

        if not self.valid_dids:
            return header + footer

        variable_declarations = []
        function_declarations = []
        for did, did_data in self.valid_dids.items():
            if did_data.get('PortType', 'dummy') == 'SENDER-RECEIVER':
                continue  # S/R DIDs are handled in _get_sender_receiver... functions
            define = self.project_dids[did]["class"].split('/')[-1]  # E.q. for ASIL D it is ASIL_D/CVC_DISP_ASIL_D
            variable_declarations.append(
                f'extern {define} {self.project_dids[did]["type"]} {self.project_dids[did]["name"]};\n'
            )
            for operation in did_data["operations"]:
                operation_data = self._get_operation_data(operation, self.project_dids[did])
                if operation_data is None:
                    self.warning(
                        f'Will not generate code for unsupported operation {operation}. Add manually for DID {did}.'
                    )
                    continue
                function_declarations.append(operation_data['declaration'] + ';\n')

        body = [
            f'#include "{build_defs.PREDECL_DISP_ASIL_D_START}"\n',
            *variable_declarations,
            f'#include "{build_defs.PREDECL_DISP_ASIL_D_END}"\n',
            f'\n#include "{build_defs.PREDECL_CODE_ASIL_D_START}"\n',
            *function_declarations,
            f'#include "{build_defs.PREDECL_CODE_ASIL_D_END}"\n',
        ]

        return header + body + footer

    def _get_operation_source_file_content(self):
        """Get content for the DID API source file.

        Returns:
            (list(str)): List of lines to write to the DID API source file.
        """
        header = [
            f'#include "{self.operation_file_name}.h"\n',
            '\n'
        ]

        if not self.valid_dids:
            return header

        body = [f'#include "{build_defs.CVC_CODE_ASIL_D_START}"\n']
        for did, did_data in self.valid_dids.items():
            if did_data.get('PortType', 'dummy') == 'SENDER-RECEIVER':
                continue  # S/R DIDs are handled in _get_sender_receiver... functions
            for operation in did_data["operations"]:
                operation_data = self._get_operation_data(operation, self.project_dids[did])
                if operation_data is None:
                    continue  # Warning already given in header generation
                body.append(operation_data['declaration'] + '\n' + operation_data['body'])
        body.append(f'#include "{build_defs.CVC_CODE_ASIL_D_END}"\n')

        return header + body

    def generate_did_files(self):
        """Generate required DID API files.
        Only use for some projects, which doesn't copy static code."""
        if self.valid_dids is None:
            includeDiagnostics = self._build_cfg.get_composition_config("includeDiagnostics")
            if includeDiagnostics in ["manual", "manual_dids"]:
                self.warning(f'includeDiagnostics is set to {includeDiagnostics}, not generating DID files.')
                return
            self.critical('Valid DIDs not set. Cannot generate DID files.')
            return

        src_dst_dir = self._build_cfg.get_src_code_dst_dir()

        # CLIENT-SERVER DIDs
        file_contents = {
            '.h': self._get_operation_header_file_content(),
            '.c': self._get_operation_source_file_content()
        }
        for extension, content in file_contents.items():
            file_path = Path(src_dst_dir, self.operation_file_name + extension)
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(content)

        # SENDER-RECEIVER DIDs
        sender_receiver_dids_exist_header, header_contents = self._get_sender_receiver_header_file_content()
        sender_receiver_dids_exist_source, source_contents = self._get_sender_receiver_source_file_content()
        if sender_receiver_dids_exist_header and sender_receiver_dids_exist_source:
            file_path = Path(src_dst_dir, self.sender_receiver_file_name + '.h')
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(header_contents)
            file_path = Path(src_dst_dir, self.sender_receiver_file_name + '.c')
            with file_path.open(mode='w', encoding='utf-8') as file_handler:
                file_handler.writelines(source_contents)
