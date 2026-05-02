import json
import os
import shutil
import logging
import typing

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from textwrap import indent

from g3core import G3Core
from g3tables.system_config import SWSystemDictWrapper
from g3tables.system_config.type_hinting import SystemDict, SWDeviceDict


from ..utils import (
    format_template, combine_str, remove_multiple_newlines, write_to_file, read_existing_file
)


logger = logging.getLogger('g3project_builder.logical')


env = Environment(
    loader=FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates/')
        ),
    keep_trailing_newline=False,
    trim_blocks=True,
    )
env.globals['timestamp'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def get_system_dict(path: str) -> SystemDict:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


# ZONE #


def delete_config_keys_with_default_values(
    system_data: SWSystemDictWrapper, g3core: G3Core
) -> None:
    for *_, path, device_data in system_data.iter_devices_system():
        # find devType struct
        if not (dev_type := device_data.get('control', {}).get('devType')):
            continue
        struct_path, typ_struct = g3core.find_struct(dev_type)
        try:
            memb_config = [
                memb for memb in typ_struct.members if memb.name == 'config'
                ][0]
        except IndexError:
            raise
        struct_path, config_struct = g3core.find_struct(
            memb_config.dtype, search_here_first=struct_path
            )
        # find device config dict
        config_data = device_data['control'].get('config', {})
        config_data_updated = {}
        for config_key, config_value in config_data.items():
            matched = False
            for member in config_struct.members:
                if member.name == config_key:
                    if (
                        member.value != config_value and
                        config_value is not None
                    ):
                        config_data_updated[config_key] = {
                            'value': config_value,
                            'dtype': member.dtype
                            }
                    else:
                        logger.info(
                            'Key "%s" at "%s/control/config" contains default '
                            'value of the "%s" member of the "%s" config '
                            'struct and will be ignored', config_key, path,
                            member.name, config_struct.name
                            )
                    matched = True
                    break
            if not matched:
                logger.warning(
                    'Key "%s" at "%s/control/config" was not matched with any '
                    'member of the "%s" config struct and will be ignored',
                    config_key, path, config_struct.name
                    )
        config_data.clear()
        config_data.update(config_data_updated)


# ST Declarations - ! these ideally need to go to G3Core ! #

def get_fb_declaration(
    device_data: SWDeviceDict,
    device_domain: typing.Literal['control', 'test']
) -> str:
    if device_domain == 'control':
        varname = device_data['general']['varname']
        fb_name = SWSystemDictWrapper.get_device_control_fb(device_data)
    elif device_domain == 'test':
        varname = device_data['general'].get('varname_test')
        if not varname:
            name = device_data['general']['name']
            logger.warning('Test domain varname is missing for %s', name)
            return ''
        fb_name = SWSystemDictWrapper.get_device_test_fb(device_data)
    else:
        raise ValueError(f'Invalid device domain: {device_domain}')
    if not fb_name:
        logger.warning(
            'Could not generate function block declaration for %s',
            device_data['general']['name']
            )
        return ''
    return f'fb{varname} : {fb_name.strip()};'


def get_dev_struct_declaration(
    device_data: SWDeviceDict,
    device_domain: typing.Literal['control', 'test']
) -> str:

    def format_dict_recursive(d: dict):
        elements = []
        for key, value in d.items():
            if isinstance(value, dict):
                value_str = format_dict_recursive(value)
                elements.append(
                    f"{key} := {value_str}"
                    )
            else:
                elements.append(
                    f"{key} := '{value}'"
                    if isinstance(value, str)
                    else f"{key} := {value}"
                    )
        return f"({', '.join(elements)})"

    def format_value(value_data) -> str:
        try:
            dtype = value_data['dtype'].lower()
            value = value_data['value']
        except KeyError:
            name = device_data['general']['name']
            logger.warning('Could not format dev struct value at %s', name)
            return ''

        if value is None:
            return ''

        if isinstance(value, dict):
            return format_dict_recursive(value)
        elif (
            ("char" in dtype or "string" in dtype) and
            not str(value).startswith("'")
        ):
            return f"'{value}'"
        elif "time" in dtype and not str(value).startswith('T#'):
            return f'T#{value}'
        elif "bool" in dtype:
            if value is True:
                return "TRUE"
            else:
                return "FALSE"
        elif "int" in dtype or "word" in dtype:
            return str(int(value))
        elif "real" in dtype:
            return str(float(value))
        else:
            return str(value)

    if device_domain == 'control':
        varname = device_data['general']['varname']
        dev_struct_type = device_data['control'].get('devType')
        config = device_data['control']['config']
    elif device_domain == 'test':
        if not device_data['general'].get('varname_test'):
            return ''
        varname = device_data['general']['varname_test']
        dev_struct_type = device_data['test'].get('devType')
        config = device_data['test']['config']
    else:
        raise ValueError(f'Invalid device domain: {device_domain}')
    if not dev_struct_type:
        name = device_data['general']['name']
        logger.warning(
            'Could not generate struct declaration for %s', name
            )
        return ''
    config_values_formatted = []
    for memb_name, memb_value_data in config.items():
        if (memb_value := format_value(memb_value_data)):
            config_values_formatted.append((memb_name, memb_value))
    config_vals = ", ".join(
        f'{memb_name} := {memb_value}'
        for memb_name, memb_value in config_values_formatted
        )
    if not config_vals:
        return f'{varname} : {dev_struct_type};'
    return f'{varname} : {dev_struct_type} := (config := ({config_vals}));'


def get_fb_assignment(
    device_data: SWDeviceDict,
    device_domain: typing.Literal['control', 'test']
) -> str:
    if device_domain == 'control':
        varname = device_data['general']['varname']
        connected_fbs = device_data['control'].get('connector')
    elif device_domain == 'test':
        if not device_data['general'].get('varname_test'):
            return ''
        varname_control = device_data['general']['varname']
        varname = device_data['general']['varname_test']
        connected_fbs = device_data['test'].get('connector')
    else:
        raise ValueError(f'Invalid device domain: {device_domain}')
    if not connected_fbs:
        return ''
    fb_assignment_lines = []
    for conn_name, conn_fb in connected_fbs.items():
        if conn_fb:
            if device_domain == 'control':
                conn_fb_ptr = f"&{conn_fb}"
            else:  # varname_control is needed only for a test domain device
                conn_fb_ptr = f"&fb{varname_control}.{conn_fb}"
        else:
            logger.warning('Connector "%s" not set.', conn_name)
            conn_fb_ptr = "NULL"
        conn_assignment = f'fb{varname}.{conn_name} = {conn_fb_ptr};'
        fb_assignment_lines.append(conn_assignment)
    return '\n'.join(fb_assignment_lines)


def get_fb_call(
    device_data: SWDeviceDict,
    device_domain: typing.Literal['control', 'test']
) -> str:
    if device_domain == 'control':
        varname = device_data['general']['varname']
        fb_name = SWSystemDictWrapper.get_device_control_fb(device_data)
    elif device_domain == 'test':
        if not device_data['general'].get('varname_test'):
            return ''
        varname = device_data['general']['varname_test']
        fb_name = SWSystemDictWrapper.get_device_test_fb(device_data)
    else:
        raise ValueError(f'Invalid device domain: {device_domain}')
    if not fb_name:
        name = device_data['general']['name']
        logger.warning(
            'Could not generate function block call for %s', name
            )
        return ''
    return f'{fb_name}(&fb{varname});'


def get_route_layout_declaration(device_data: SWDeviceDict) -> str:
    route_name = device_data['general']['varname']
    route_layout_data = device_data['general']['layout']
    declaration_lines = []
    for route_element_data in route_layout_data:
        name = route_element_data['name']
        func = route_element_data['function']
        if route_element_data['type'] == 'pointmachine':
            pos = route_element_data['position']
            line = f'{func}({pos}, &{name}.toRoute, &{route_name});'
        else:
            line = f'{func}(&{name}.toRoute, &{route_name});'
        declaration_lines.append(line)
    return "\n".join(declaration_lines)

# ST Declarations  - END #


def generate_zone_files_contents(
    system_config: SWSystemDictWrapper, zone_name: str, gen_test: bool = False
) -> tuple[str, str]:
    varibales_var = ''
    main_c = ''

    zone_devices = []
    gate_devices = []
    route_devices = []
    other_devices = []

    for _, path, device_data in system_config.iter_devices_zone(zone_name):
        if 'Zone' in path:
            zone_devices.append((path, device_data))
        elif 'Gate' in path:
            gate_devices.append((path, device_data))
        elif 'Route' in path:
            route_devices.append((path, device_data))
        else:
            other_devices.append((path, device_data))

    sorted_devices = zone_devices + gate_devices + route_devices + other_devices

    for path, device_data in sorted_devices:
        
        if not system_config.get_device_control_fb(device_data):
            logger.warning('function block type is missing for "%s"', path)
            continue
        varibales_var = combine_str(
            varibales_var,
            get_fb_declaration(device_data, 'control'),
            get_dev_struct_declaration(device_data, 'control'),
            )
        main_c = combine_str(
            main_c,
            get_fb_assignment(device_data, 'control'),
            get_fb_call(device_data, 'control'),
            )
        if 'Route' in path:
            route_fb = SWSystemDictWrapper.get_device_control_fb(device_data)
            if route_fb and 'NonSafety' in route_fb:
                main_c = combine_str(
                    main_c,
                    get_route_layout_declaration(device_data),
                    )
        if gen_test:
            varibales_var = combine_str(
                varibales_var,
                get_fb_declaration(device_data, 'test'),
                get_dev_struct_declaration(device_data, 'test'),
                )
            main_c = combine_str(
                main_c,
                get_fb_assignment(device_data, 'test'),
                get_fb_call(device_data, 'test'),
                )
    return (
        indent(remove_multiple_newlines(varibales_var), '    '),
        indent(remove_multiple_newlines(main_c), '    ')
        )

# ZONE END #


# COMM #

def generate_comm_files_contents(
    system_config: SWSystemDictWrapper, gen_test: bool = False
) -> tuple[str, str]:
    varibales_var = ''
    main_c = ''
    for *_, device_data in system_config.iter_devices_zone('Common'):
        if device_data['general']['metatype'] != 'Comm':
            continue
        varibales_var = combine_str(
            varibales_var,
            get_fb_declaration(device_data, 'control'),
            )
        main_c = combine_str(
            main_c,
            get_fb_assignment(device_data, 'control'),
            get_fb_call(device_data, 'control'),
            )
        if gen_test:
            varibales_var = combine_str(
                varibales_var,
                get_fb_declaration(device_data, 'test'),
                )
            main_c = combine_str(
                main_c,
                get_fb_assignment(device_data, 'test'),
                get_fb_call(device_data, 'test'),
                )
    return (
        indent(remove_multiple_newlines(varibales_var), '    '),
        indent(remove_multiple_newlines(main_c), '    ')
        )

# COMM END #


# SYSTEM #

def generate_system_files_contents(
    system_config: SWSystemDictWrapper
) -> tuple[str, str]:
    context = {
        'has_system_safety': system_config.has_system_safety(),
        'has_shv': system_config.has_shv(),
        'has_elesys': system_config.has_elesys()
        }
    main_c = format_template(env, 'main_c_system.tpl', **context)
    varibales_var = format_template(env, 'variables_var_system.tpl', **context)
    return (
        indent(remove_multiple_newlines(varibales_var), '    '),
        indent(remove_multiple_newlines(main_c), '    ')
        )

# SYSTEM END #


# ZONE.VAR #

def generate_zone_var_contents(
    system_config: SWSystemDictWrapper, gen_test: bool = False
) -> str:
    zone_var = ''
    for *_, device_data in system_config.iter_devices_zone('Common'):
        if device_data['general']['metatype'] == 'Project':
            continue
        zone_var = combine_str(
            zone_var,
            get_dev_struct_declaration(device_data, 'control'),
            )
        if gen_test:
            zone_var = combine_str(
                zone_var,
                get_dev_struct_declaration(device_data, 'test'),
                )
    return indent(remove_multiple_newlines(zone_var), '    ')


# ZONE.VAR END #


def makedirs_logical(
    project_name: str, system_name: str, zone_name: str
) -> str:
    path = os.path.join(
        os.getcwd(),
        'Logical',
        project_name,
        system_name,
        zone_name
        )
    os.makedirs(path, exist_ok=True)
    return path


# general TODO: add update file logic


def generate_main_variables_ansic_files(
    project_name: str,
    system_name: str,
    folder_name: str,
    program_cyclic: str,
    variables: str
) -> str:
    folder_path = makedirs_logical(
        project_name, system_name, folder_name
        )
    write_to_file(
        folder_path,
        'main.c',
        format_template(env, 'main_c.tpl', program_cyclic=program_cyclic)
        )
    write_to_file(
        folder_path,
        'Variables.var',
        format_template(env, 'variables_var.tpl', variables=variables)
        )
    write_to_file(
        folder_path,
        'ANSIC.prg',
        format_template(env, 'ansic_prg.tpl')
        )
    return folder_path


def generate_logical_files(
    system_config_path: str, gen_test: bool = False
) -> None:
    g3core = G3Core.from_local('./Logical/Libraries')
    system = get_system_dict(system_config_path)
    sw_system_wrapper = SWSystemDictWrapper(system['Software'])
    project_name = sw_system_wrapper.get_project_name()
    system_name = sw_system_wrapper.get_system_name()
    delete_config_keys_with_default_values(sw_system_wrapper, g3core)
    # create Zones folder files
    zone_tasknames: list[str] = []
    for zone_name in system['Software']:
        if zone_name == 'Common':
            continue
        varibales_var, main_c = generate_zone_files_contents(
            sw_system_wrapper, zone_name, gen_test
            )
        zone_taskname = sw_system_wrapper.get_zone_taskname(zone_name)
        zone_tasknames.append(zone_taskname)
        generate_main_variables_ansic_files(
            project_name, system_name, zone_taskname, main_c, varibales_var
            )
    # create Comm folder files
    varibales_var, main_c = generate_comm_files_contents(
        sw_system_wrapper, gen_test
        )
    generate_main_variables_ansic_files(
        project_name, system_name, 'Comm', main_c, varibales_var
        )
    # create System folder files
    varibales_var, main_c = generate_system_files_contents(sw_system_wrapper)
    path = generate_main_variables_ansic_files(
        project_name, system_name, 'System', main_c, varibales_var
        )
    system_folder_path = os.path.dirname(path)
    project_folder_path = os.path.dirname(system_folder_path)
    logical_folder_path = os.path.dirname(project_folder_path)
    # create Zone.var file
    zone_var = generate_zone_var_contents(sw_system_wrapper)
    write_to_file(
        system_folder_path,
        'Zone.var',
        format_template(env, 'variables_var.tpl', variables=zone_var)
        )
    # create config.txt file
    redmine_data = sw_system_wrapper.redmine_data
    context = {
        'redmine_project_name': redmine_data['projectName'],
        'redmine_project_folder_id': redmine_data['projectFolderID']
    }
    write_to_file(
        project_folder_path,
        'config.txt',
        format_template(
            env, 'config_txt.tpl', **context
            )
        )
    # create Package.pkg files
    write_to_file(
        system_folder_path,
        'Package.pkg',
        format_template(
            env, 'package_pkg_system.tpl', zone_names=zone_tasknames
            )
        )
    
    object_type_package = ".//ns:Object[@Type='Package']"
    namespace_type_package = {'ns': 'http://br-automation.co.at/AS/Package'}

    
    system_names = read_existing_file(project_folder_path+"\Package.pkg", object_type_package, namespace_type_package)

    if sw_system_wrapper.get_system_name() not in system_names:
        system_names += [sw_system_wrapper.get_system_name()]

    write_to_file(
        project_folder_path,
        'Package.pkg',
        format_template(
            env, 'package_pkg_project.tpl', system_names=system_names
            )
        )
    project_names = [sw_system_wrapper.get_project_name()]
    write_to_file(
        logical_folder_path,
        'Package.pkg',
        format_template(
            env, 'package_pkg_logical.tpl', project_names=project_names
            )
        )

    # remove the "Logical/Project" directory
    logical_default_project_path = os.path.join(logical_folder_path, 'Project')
    if os.path.isdir(logical_default_project_path):
        shutil.rmtree(logical_default_project_path)
