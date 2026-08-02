# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module for handling user defined data types, such as enumerations."""

import re
import time
from ruamel.yaml import YAML
from copy import deepcopy
from pathlib import Path
from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.unit_configs import UnitConfigs


class UserDefinedTypes(ProblemLogger):
    """A class for accessing the project’s user defined data types (see :doc:`user_defined_types`)."""

    FILE_PREFIXES = ['udt_']  # Add more as needed
    UNDERLYING_DATA_TYPES = {  # Add more as needed
        'target_link': {
            'u32': 'UInt32',
            'i32': 'Int32',
            'u16': 'UInt16',
            'i16': 'Int16',
            'u8': 'UInt8',
            'i8': 'Int8'
        },
        'embedded_coder': {
            'u32': 'uint32_T',
            'i32': 'int32_T',
            'u16': 'uint16_T',
            'i16': 'int16_T',
            'u8': 'uint8_T',
            'i8': 'int8_T'
        }
    }
    SIMULINK_DATA_TYPES = {  # Add more as needed
        'target_link': {
            'Simulink.IntEnumType': 'Int32',
            'uint32': 'UInt32',
            'int32': 'Int32',
            'uint16': 'UInt16',
            'int16': 'Int16',
            'uint8': 'UInt8',
            'int8': 'Int8'
        },
        'embedded_coder': {
            'Simulink.IntEnumType': 'int32_T',
            'uint32': 'uint32_T',
            'int32': 'int32_T',
            'uint16': 'uint16_T',
            'int16': 'int16_T',
            'uint8': 'uint8_T',
            'int8': 'int8_T'
        }
    }

    def __init__(self, build_prj_config, unit_configs):
        """Class Initialization.

        Args:
            build_prj_config (BuildProjConfig): Instance holding information of where to find units configs to parse.
            unit_configs (UnitConfigs): Unit definitions.
        """
        super().__init__()
        if not isinstance(build_prj_config, BuildProjConfig) or not isinstance(unit_configs, UnitConfigs):
            err = (
                'Input arguments should be an instance of:'
                f'BuildProjConfig, not {type(build_prj_config)}'
                f'AND/OR UnitConfigs, not {type(unit_configs)}'
            )
            raise TypeError(err)

        start_time = time.time()
        self.info('  Start parsing files with user defined data types')
        self._build_prj_cfg = build_prj_config
        self._unit_configs = unit_configs
        self.enums_per_unit = {}
        self.common_enums = self._read_enums_from_definitions()
        self.structs_per_unit = {}
        self._parse_all_user_defined_types()
        self.common_header_files = []
        # Must run last to be able to compare with TL/EC data types
        self.all_enums = self._get_enumerations()
        self._interface_data_types = self._parse_interface_data_types()
        self.info('  Finished parsing files with user defined data types (in %4.2f s)', time.time() - start_time)

    @staticmethod
    def convert_interface_enum_to_simulink(interface_enum, underlying_data_type=None):
        """ Given an interface enumeration, convert it to a simulink parsed version.

        Args:
            interface_enum ([dict]): Interface enumeration definition.
            underlying_data_type (str): Underlying data type, usually not available for interface enumerations.
        Returns
            simulink_enum (dict): Simulink enumeration definition.
        """
        members = {}
        default_value = None
        # Assuming interface enumerations start at 0 counting upwards
        for idx, enum_member in enumerate(interface_enum):
            if 'default' in enum_member:
                default_value = enum_member['in']
            else:
                members[enum_member['in']] = idx
        simulink_enum = {
            'underlying_data_type': underlying_data_type,
            'members': members,
            'default_value': default_value
        }
        return simulink_enum

    def _parse_interface_data_types(self):
        """ Get interface data types.
        Also, runs validation tests.

        Returns:
            interface_data_types (dict): Specification interface data types.
        """
        interface_data_types = {}
        interface_data_types_path = Path(self._build_prj_cfg.get_root_dir(), 'conf.local', 'interface_data_types.yml')

        if not interface_data_types_path.is_file():
            self.warning('Cannot extract interface data types. File not found: %s', str(interface_data_types_path))
            return interface_data_types

        self.info('  Parsing file: %s', str(interface_data_types_path))
        with interface_data_types_path.open(mode='r', encoding='utf-8') as fh:
            yaml = YAML(typ='safe', pure=True)
            interface_data_types_yaml = yaml.load(fh)
            interface_data_types_tmp = interface_data_types_yaml['types']
        # Add more as needed
        if 'enums' in interface_data_types_tmp:
            valid_interface_enumerations = self._validate_interface_enumerations(interface_data_types_tmp['enums'])
            interface_data_types['enums'] = valid_interface_enumerations
        return interface_data_types

    def _parse_all_user_defined_types(self):
        """Parse all files containing user defined data types."""
        src_dirs = self._build_prj_cfg.get_unit_src_dirs()
        for unit, src_dir in src_dirs.items():
            self._parse_unit_user_defined_types(unit, src_dir)

    def _parse_unit_user_defined_types(self, unit, unit_src_dir):
        """Parse unit defined types for a given unit.

        Files to parse are found using expected prefixes, see FILE_PREFIXES.
        Data types to parse can be added as needed.

        Args:
            unit (str): Current unit/model name.
            unit_src_dir (str): Unit sourcecode directory.
        """
        self.enums_per_unit[unit] = {}
        self.structs_per_unit[unit] = {}
        found_files = [Path(unit_src_dir, unit.split('__')[0] + '.h')]
        for file_prefix in self.FILE_PREFIXES:
            found_files.extend(Path(unit_src_dir).glob(file_prefix + '*.h'))
        for found_file in found_files:
            self.debug('  Parsing file: %s', str(found_file))
            self._parse_target_link_enum(unit, found_file)
            self._parse_target_link_struct(unit, found_file)
        self._validate_project_enumerations()
        self._validate_project_structs()

    def _parse_target_link_struct(self, unit, header_file: Path):
        """Parse structs generated by TargetLink, given a header file.

        Args:
            unit (str): Current unit/model name.
            header_file (Path): Header file to parse.
        """
        with header_file.open(mode='r', encoding='ISO-8859-1') as hf_fh:
            header_file_content = hf_fh.read()
        structs = re.findall(
            r'^struct ([A-Za-z0-9_]+) {\s*\n'
            r'((?:\s*\w+ \w+;\s*\n)*)'
            r'};',
            header_file_content,
            flags=re.M
        )

        for struct_name, struct_content in structs:
            struct_members = re.findall(r'\s*(\w+) (\w+);', struct_content, flags=re.M)
            struct_dict = {
                'members': {variable: data_type for data_type, variable in struct_members}
            }

            if struct_name in self.structs_per_unit[unit]:
                if self.structs_per_unit[unit][struct_name]['members'] == struct_dict['members']:
                    self.info('Struct %s is multiply defined in %s, although they are consistent.', struct_name, unit)
                else:
                    self.critical('Found inconsistent multiply defined struct: %s, units: %s.', struct_name, [unit])
            else:
                self.structs_per_unit[unit][struct_name] = struct_dict.copy()

    def _validate_project_structs(self):
        """Checks for inconsistencies in struct definitions for all units in the project."""
        structs = {}
        for unit, struct_names in self.structs_per_unit.items():
            for struct_name, struct_data in struct_names.items():
                if struct_name in structs:
                    structs[struct_name]['units'].append(unit)
                    if not structs[struct_name]['members'] == struct_data['members']:
                        self.critical(
                            'Found inconsistent multiply defined struct: %s, units: %s.',
                            struct_name,
                            structs[struct_name]['units']
                        )
                else:
                    structs[struct_name] = struct_data.copy()
                    structs[struct_name]['units'] = [unit]

    def _validate_interface_enumerations(self, interface_enumerations):
        """ Given a specification for enumerations

        Args:
            interface_enumerations (dict): Interface enumerations.
        Returns
            valid_interface_enumerations (dict): Specification, valid interface enumerations.
        """
        valid_interface_enumerations = {}
        for enum_name, enum_data in interface_enumerations.items():
            if enum_name in valid_interface_enumerations:
                self.critical('%s is multiply defined in interface enumeration definitions.', enum_name)
            elif enum_name not in self.all_enums:
                self.critical('%s is not defined in the project', enum_name)
            else:
                converted = self.convert_interface_enum_to_simulink(
                    enum_data,
                    self.all_enums[enum_name]['underlying_data_type']
                )
                is_consistent = self._compare_enum_definitions(
                    self.all_enums[enum_name]['units'],
                    enum_name,
                    converted,
                    self.all_enums[enum_name]
                )
                if is_consistent:
                    valid_interface_enumerations[enum_name] = enum_data
        return valid_interface_enumerations

    def _validate_project_enumerations(self):
        """Checks for inconsistencies in enum definitions for all units in the project."""
        enumerations = {}
        for unit, enum_names in self.enums_per_unit.items():
            for enum_name, enum_data in enum_names.items():
                if enum_name in enumerations:
                    enumerations[enum_name]['units'].append(unit)
                    self._compare_enum_definitions(
                        enumerations[enum_name]['units'],
                        enum_name,
                        enumerations[enum_name],
                        enum_data
                    )
                else:
                    enumerations[enum_name] = enum_data.copy()
                    enumerations[enum_name]['units'] = [unit]

    def _compare_enum_definitions(self, units, enum_name, enum_one, enum_two):
        """Compare two enumeration definitions.

        Args:
            units ([str]): List of units using given enumerations.
            enum_name (str): Name of enumeration.
            enum_one (dict): Enumeration one to compare.
            enum_two (dict): Enumeration two to compare.
        Returns:
            is_consistent_enums (bool): True/False depending on enum consistency.
        """
        is_consistent_enums = True
        error_message = f'Found inconsistent multiply defined enumeration: {enum_name}, units: {units}.\n'
        if enum_one['underlying_data_type'] != enum_two['underlying_data_type']:
            is_consistent_enums = False
            error_message += (
                'underlying_data_type differs: '
                f"{enum_one['underlying_data_type']} vs. {enum_two['underlying_data_type']}.\n"
            )

        enum_one_members = list(enum_one['members'].items())
        enum_two_members = list(enum_two['members'].items())
        if len(enum_one_members) != len(enum_two_members):
            is_consistent_enums = False
            error_message += (
                f'Number of enum members differs: {len(enum_one_members)} vs. {len(enum_two_members)}.\n'
            )
        else:
            for idx, enum_one_member in enumerate(enum_one_members):
                if enum_one_member[0] != enum_two_members[idx][0] or enum_one_member[1] != enum_two_members[idx][1]:
                    is_consistent_enums = False
                    error_message += (
                        f'Enum member definition differs: {enum_one_members[idx]} vs. {enum_two_members[idx]}.\n'
                    )

        if enum_one['default_value'] != enum_two['default_value']:
            is_consistent_enums = False
            error_message += (
                'default_value differs: '
                f"{enum_one['default_value']} vs. {enum_two['default_value']}.\n"
            )

        if not is_consistent_enums:
            self.critical(error_message)

        return is_consistent_enums

    def _parse_target_link_enum(self, unit, header_file: Path):
        """Parse enumerations generated by TargetLink, given a header file.

        Args:
            unit (str): Current unit/model name.
            header_file (Path): Header file to parse.
        """
        with header_file.open(mode='r', encoding='ISO-8859-1') as hf_fh:
            header_file_content = hf_fh.read()
        enums = re.findall(
            r'^typedef enum ([A-Za-z0-9]+)_tag {\s*\n'
            r'((?:\s*\w+ = [-+]?\d+,?\s*\n)*)'
            r'} \1;',
            header_file_content,
            flags=re.M
        )

        for enum_name, enum_content in enums:
            enum_members_tmp = re.findall(r'\s*(\w+) = ([-+]?\d+)', enum_content, flags=re.M)
            enum_members = [(k, int(v)) for k, v in enum_members_tmp]
            if enum_name in self.common_enums:
                underlying_data_type = self.common_enums[enum_name]['underlying_data_type']
            else:
                self.warning('Calculating underlying data type for: %s', str(enum_name))
                underlying_data_type = self._calculate_underlying_data_type(unit, enum_name, enum_members)
            enum_dict = {
                'underlying_data_type': underlying_data_type,
                'members': {},
                'default_value': self.get_default_enum_value(unit, enum_name)
            }
            for key, value in enum_members:
                enum_dict['members'][key] = value

            if enum_name in self.enums_per_unit[unit]:
                is_consistent_enums = self._compare_enum_definitions(
                    [unit],
                    enum_name,
                    self.enums_per_unit[unit][enum_name],
                    enum_dict
                )
                if is_consistent_enums:
                    self.info(
                        'Enumeration %s is multiply defined in %s, although they are consistent.',
                        enum_name,
                        unit
                    )
            else:
                self.enums_per_unit[unit][enum_name] = enum_dict.copy()

    def _calculate_underlying_data_type(self, unit, enum_name, enum_members):
        """Calculate best fitting data type given an enum definition.

        Args:
            unit (str): Current unit/model name.
            enum_name (str): Current enum name.
            enum_members (list(tuple)): List of enum members, name value pairs.
        Returns:
            underlying_data_type (str): Best fitting data type.
        """
        code_generator = self._unit_configs.get_unit_code_generator(unit)
        enum_member_values = [member_value for member_name, member_value in enum_members]
        min_value = min(enum_member_values)
        max_value = max(enum_member_values)

        # TODO Consider forcing signed like CS (or ARXML, from database?) does, seems to be int8 specifically
        underlying_data_type = None
        if min_value >= 0:
            if max_value <= 255:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['u8']
            elif max_value <= 65535:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['u16']
            elif max_value <= 4294967295:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['u32']
        elif min_value >= -128:
            if max_value <= 127:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i8']
            elif max_value <= 32767:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i16']
            elif max_value <= 2147483647:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i32']
        elif min_value >= -32768:
            if max_value <= 32767:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i16']
            elif max_value <= 2147483647:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i32']
        elif min_value >= -2147483648:
            if max_value <= 2147483647:
                underlying_data_type = self.UNDERLYING_DATA_TYPES[code_generator]['i32']

        if underlying_data_type is None:
            self.critical(
                'Unhandled enum size, name: %s, min: %s, max: %s. Valid types are uint8/16 and int8/16',
                enum_name,
                min_value,
                max_value
            )

        return underlying_data_type

    def _read_enums_from_definitions(self):
        """ Reads all enums from .m files where they are defined. Requires projectInfo.enumDefDir in
        ProjectCfg.json file.
        Files defining simulink class enumerations are expected to follow a template.

        Returns:
            common_enums (dict): Dictionary containing all enums defined in the enum definition directory.
        """
        common_enums = {}
        if self._build_prj_cfg.get_enum_def_dir() is None:
            self.warning(
                'Cannot parse enumerations from .m files. Missing "enumDefDir" in project config.'
            )
            return {}

        enum_files = Path(self._build_prj_cfg.get_enum_def_dir()).rglob('*.m')
        for enum_file in enum_files:
            with enum_file.open(mode='r', encoding='ISO-8859-1') as fh:
                enum_file_content = fh.read()
            enum_name = enum_file.stem

            members_part = re.search(
                r'\s+enumeration\s*\n'
                r'(\s*%.*|\s*\w+\s*\(\d+\)\s*(%.*)?\n)+'
                r'\s+end',
                enum_file_content,
                flags=re.MULTILINE
            )
            if not members_part:
                self.warning('Cannot extract enumeration members from %s', str(enum_file))
                continue
            members = re.findall(r'(\w+)\s*\((\d+)\)', members_part.group(0))
            member_dict = {enum_name + '_' + member[0]: int(member[1]) for member in members}
            enum_members = [(member_name, member_value) for member_name, member_value in member_dict.items()]

            get_default_value = re.search(
                r'function ([A-Za-z0-9]+) = getDefaultValue\(\)[\s\n]*'
                r'\1 = [A-Za-z0-9]+\.([A-Za-z0-9_]+);[\s\n]*'
                r'end',
                enum_file_content,
                flags=re.MULTILINE
            )
            if get_default_value is None:
                self.warning('Cannot extract default enumeration values in: %s', str(enum_file))
                continue
            default_value = get_default_value.groups()[1]
            default_member = f'{enum_name}_{default_value}'

            calculate_underlying_data_type = re.search(
                r'function ([A-Za-z0-9]+) = calculateUnderlyingDataType\(\)[\s\n]*'
                r'\1 = (true|false);[\s\n]*'
                r'end',
                enum_file_content,
                flags=re.MULTILINE
            )
            get_storage_type = re.search(
                r'classdef[\s]+[A-Za-z0-9]+[\s]*<[\s]*([A-Za-z0-9\.]+)[\s\n]*',
                enum_file_content,
                flags=re.MULTILINE
            )
            if get_storage_type is None:
                self.warning('Cannot extract storage type in: %s', str(enum_file))
                if calculate_underlying_data_type is None or calculate_underlying_data_type.groups()[1] == 'false':
                    self.warning('Calculating underlying data type for: %s', str(enum_file))
                    underlying_data_type = self._calculate_underlying_data_type('target_link', enum_name, enum_members)
                else:
                    underlying_data_type = self._calculate_underlying_data_type('target_link', enum_name, enum_members)
            else:
                underlying_data_type = self.SIMULINK_DATA_TYPES['target_link'][get_storage_type.groups()[0]]

            common_enums[enum_name] = {
                "underlying_data_type": underlying_data_type,
                "default_value": default_member,
                "members": member_dict
            }

        return common_enums

    def _get_enumerations(self):
        """Get all enumeration defined in the project, together with unit usage.

        Information already provided in self._validate_project_enumerations during initialization.

        Returns:
            enumerations (dict): Enumerations defined in the projects, including unit usage.
        """
        enumerations = {}
        for unit, enum_names in self.enums_per_unit.items():
            for enum_name, enum_data in enum_names.items():
                if enum_name in enumerations:
                    enumerations[enum_name]['units'].append(unit)
                else:
                    enumerations[enum_name] = deepcopy(enum_data)
                    enumerations[enum_name]['units'] = [unit]
        if self._build_prj_cfg.get_code_generation_config("includeAllEnums"):
            for enum_name, enum_data in self.common_enums.items():
                if enum_name not in enumerations:
                    self.warning(
                        "Enumeration %s is not used in any unit. Included since 'includeAllEnums' is set in config.",
                        enum_name
                    )
                    enumerations[enum_name] = deepcopy(enum_data)
                    enumerations[enum_name]['units'] = []
        return enumerations

    def get_default_enum_value(self, unit, enum_name):
        """Get default value of given enumeration name by searching in the unit configuration.

        Args:
            unit (str): Current unit/model name.
            enum_name (str): Name of an enumeration.
        Returns:
            default_value_str (str): Default value (string) for the given enumeration name.
                None if value could not be extracted.
        """
        # The config file is generated in one go, stop when first occurrence is found, cannot differ
        per_unit_cfg = self._unit_configs.get_per_unit_cfg()
        if unit in per_unit_cfg:
            u_cfg = per_unit_cfg[unit]
        else:
            # Should not happen
            self.warning(
                'Cannot extract default enumeration value for %s in %s. Unit is missing in the unit configuration.',
                enum_name,
                unit
            )
            return None

        for signal_type in ['inports', 'outports', 'local_vars', 'calib_consts']:
            for signal_data in u_cfg[signal_type].values():
                if enum_name == signal_data['type'] and 'default' in signal_data:
                    return f"{enum_name.upper()}_{signal_data['default'].upper()}"

        self.warning(
            'Cannot extract default enumeration value for %s in %s. '
            'Either the enumeration or its default value is missing in the unit configuration file. ',
            enum_name,
            unit
        )
        common_default = self.common_enums.get(enum_name, {}).get('default_value', None)
        if common_default is not None:
            return common_default.upper()
        return None

    def get_enumerations(self):
        """Get all enumeration defined in the project, together with unit usage.

        Returns:
            self.all_enums (dict): Enumerations defined in the projects, including unit usage.
        """
        return self.all_enums

    def get_interface_data_types(self):
        """Returns all interface data types"""
        return deepcopy(self._interface_data_types)

    def get_structs(self):
        """Get all structs defined in the project, together with unit usage.

        Information already provided in self._validate_project_structs during initialization.

        Returns:
            structs (dict): Structs defined in the projects, including unit usage.
        """
        structs = {}
        for unit, struct_names in self.structs_per_unit.items():
            for struct_name, struct_data in struct_names.items():
                if struct_name in structs:
                    structs[struct_name]['units'].append(unit)
                else:
                    structs[struct_name] = deepcopy(struct_data)
                    structs[struct_name]['units'] = [unit]
        return structs

    def _get_header_file_header(self, guard: str):
        """Get header for common header files.

        Args:
            guard (str): Guard for common header files.
        Returns:
            header (str): Header for common header files.
        """
        return (
            f'#ifndef {guard}\n'
            f'#define {guard}\n'
            f'{self._unit_configs.base_types_headers}'
        )

    def _generate_struct_header_file(self, file_path: Path):
        """ Generates a header file declaring all TargetLink structs used in the project.

        Args:
            file_path (Path): Path to file to generate.
        """
        structs = self.get_structs()
        guard = f"{file_path.stem.upper()}_H"
        with file_path.open('w') as fh:
            fh.write(self._get_header_file_header(guard))
            fh.write('#include "VcEnumerations.h"\n')  # struct members may be of enum type
            fh.write('/* VCC Structs */\n')
            for struct_name, struct_data in structs.items():
                fh.write('\n')
                fh.write(f'struct {struct_name} {{\n')
                for variable, data_type in struct_data['members'].items():
                    fh.write(f"   {data_type} {variable};\n")
                fh.write('};\n')
            fh.write(f'#endif /* {guard} */\n')

    def _generate_enum_header_file(self, file_path: Path):
        """ Generates a header file declaring all TargetLink enumerations used in the project.

        Args:
            file_path (Path): Path to file to generate.
        """
        enumerations = self.get_enumerations()
        rte_interface_enums = self._build_prj_cfg.get_code_generation_config("mapToRteEnums")
        if not self._build_prj_cfg.get_enum_def_dir() and rte_interface_enums:
            self.warning(
                "No enum definition directory specified. Cannot generate all enums in decinition directory."
            )
            rte_interface_enums = False
        guard = f"{file_path.stem.upper()}_H"
        with file_path.open('w') as fh:
            fh.write(self._get_header_file_header(guard))
            if rte_interface_enums:
                composition_name = self._build_prj_cfg.get_composition_config("softwareComponentName")
                fh.write(f'#include "Rte_{ composition_name }_Type.h"\n')
            fh.write('/* VCC Enumerations */\n')
            for enum_name, enum_data in enumerations.items():
                members = enum_data['members']
                member_strs = ', \n'.join([f"   {member.upper()} = {value}" for member, value in members.items()])
                enum_definition = (
                    f'\n'
                    f'typedef enum {enum_name}_tag {{\n'
                    f'{member_strs} \n'
                    f'}} {enum_name};\n'
                )
                if rte_interface_enums:
                    enum = self.common_enums[enum_name]
                    one_member = next(iter(enum["members"]))
                    rte_translation = '\n'.join(
                        f"#define {member.upper()} {member}" for member in enum["members"].keys()
                    )
                    enum_definition = (
                        f'\n'
                        f'#ifndef {one_member}\n'
                        f'{enum_definition}\n'
                        f'#else\n'
                        f'{rte_translation}\n'
                        f'#endif /* {one_member} */\n'
                    )
                fh.write(enum_definition)
            fh.write(f'#endif /* {guard} */\n')

    def generate_common_header_files(self):
        """ Generates common header files.

        These headers can be included in general files such as VcDummy_spm.h or VcExtVar.h.

        Returns:
            common_header_files (list(Path)): List of names of generated files.
        """
        src_dir = self._build_prj_cfg.get_src_code_dst_dir()
        enum_file_path = Path(src_dir, 'VcEnumerations.h')
        struct_file_path = Path(src_dir, 'VcStructs.h')
        self._generate_enum_header_file(enum_file_path)
        self._generate_struct_header_file(struct_file_path)
        self.common_header_files.extend([enum_file_path.name, struct_file_path.name])
