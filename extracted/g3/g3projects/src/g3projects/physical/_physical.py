import json
import os
import shutil
import logging

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from textwrap import indent

from g3tables.system_config import SWSystemDictWrapper
from g3tables.system_config.type_hinting import SystemDict

from ..utils import (
    format_template, write_to_file, read_existing_file
)

from g3hardware import HardwareModule, HardwareIsle, format_type, is_cpu_type


logger = logging.getLogger('g3project_builder.physical')


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


def makedirs_physical(system_name: str) -> str:
    path = os.path.join(
        os.getcwd(),
        'Physical',
        system_name
        )
    os.makedirs(os.path.join(path, 'CPU'), exist_ok=True)
    return path


# TODO: Would be nice to move to some kind of wrapper

def is_safety_configuration(config_hw: list[dict]) -> bool:
    for isle in config_hw:
        if ('SL8101' in isle['head']['type'] or 'SL8100' in isle['head']['type']):
            return True
    return False


def get_hardware_module_name(module_type: str, config_hw: list[dict]) -> str:
    module_types = [m.strip().lower() for m in module_type.split(",")]

    for isle in config_hw:
        isle_type = isle['head']['type'].lower()
        for mtype in module_types:
            if mtype in isle_type:
                return "CPU"
    raise ValueError(f'Module "{module_type}" data was not found')



def get_cpu_module_name_default(module_name) -> str:
    module_name_formatted = format_type(module_name)
    if not is_cpu_type(module_name_formatted):
        raise ValueError(f'Module "{module_name}" is not a CPU module')
    return module_name_formatted

# END TODO ##


# Hardware.hw #

def create_hw_isles(config_hw: dict, **kwargs) -> HardwareIsle | None:
    isles: list[HardwareIsle] = []
    for isle_data in config_hw:
        module_type = isle_data['head']['type']
        cabinet = isle_data['head']['cabinet']
        name_suffix = isle_data['head']['name_suffix']
        head = HardwareModule.new(
            type_=module_type,
            name_suffix=f"{cabinet}_{name_suffix}",
            **kwargs
            )
        tail = []
        for module_data in isle_data['tail']:
            module_type = module_data['type']
            cabinet = module_data['cabinet']
            name_suffix = module_data['name_suffix']
            module = HardwareModule.new(
                type_=module_type,
                name_suffix=f"{cabinet}_{name_suffix}",
                **kwargs
                )
            tail.append(module)
        isles.append(HardwareIsle(head, *tail))
    # move the CPU isle to the start of the isle list
    cpu_isle_i = -1
    for i, isle in enumerate(isles):
        if is_cpu_type(isle.head.type_):
            cpu_isle_i = i
            break
    if cpu_isle_i == -1:
        raise ValueError(
            "CPU module was not found in the hardware configuration"
            )
    if cpu_isle_i != 0:
        isles.insert(0, isles.pop(cpu_isle_i))
    # connect the isles
    for i, isle in enumerate(isles[:-1]):
        isle.next_isle = isles[i + 1]
    if not isles:
        return None
    return isles[0]


def generate_hardware_hw_contents(
    config_hw: dict, project_name: str, system_name: str, cp1584_name: str, ftp1_pswd_hash: str, ftp2_pswd_hash: str
) -> str:
    kwargs = {
        'cpuname': cp1584_name,
        'cpuhostname': ("plc-"+project_name+"-"+system_name).lower(),
        'cpuconfigurationid': (project_name+"-"+system_name).lower(),
        'ftpuserpassword1': ftp1_pswd_hash,
        'ftpuserpassword2': ftp2_pswd_hash
        }
    if not (hw_isle := create_hw_isles(config_hw, **kwargs)):
        return ''

    return hw_isle.to_str()


# END Hardware.hw #


# Iomap.iom #


def generate_iomap_iom_contents(system: SWSystemDictWrapper) -> list[str]:
    iomap_lines = []
    for zone, _, device_path, device_data in system.iter_devices_system():
        if zone == 'Common':
            if 'control' in device_data:
                if 'config' in device_data['control']:
                    if 'name' in device_data['control']['config']:
                        if ( ('SystemSafety' in device_data['control']['config']['name'] ) or ( 'systemSafety' in device_data['control']['config']['name'] ) ):
                            for key, value in device_data['control'].get('iomap', {}).items():
                                device_varname = system.get_device_varname(device_data)
                                device = f'fb{device_varname}'
                                #zone_taskname = device_data['control']['config']['system']
                                zone_taskname = "System"
                                iomap_line = f'::{zone_taskname}:{device}.{key} AT {value};'
                                iomap_lines.append(indent(iomap_line, '    '))
            continue
        zone_taskname = system.get_zone_taskname(zone)
        for key, value in device_data['control'].get('iomap', {}).items():
            device_varname = system.get_device_varname(device_data)
            if (
                (
                    'RequestorDigital' in device_path and
                    'inputs' in key and
                    'Safety' not in key
                ) or
                (
                    'GPIO' in device_path
                )
            ):
                device = device_varname
            else:
                device = f'fb{device_varname}'
            iomap_line = f'::{zone_taskname}:{device}.{key} AT {value};'
            iomap_lines.append(indent(iomap_line, '    '))
    return iomap_lines

# END Iomap.iom #


def generate_physical_files(system_config_path: str, ftp1_pswd_hash: str, ftp2_pswd_hash: str, sfdomain_pswd_hash: str) -> None:
    system = get_system_dict(system_config_path)
    sw_system_wrapper = SWSystemDictWrapper(system['Software'])
    project_name = sw_system_wrapper.get_project_name()
    system_name = sw_system_wrapper.get_system_name()
    zone_tasknames = sw_system_wrapper.zone_tasknames
    physical_path = makedirs_physical(system_name)
    # create Physical.pkg file

    object_type_configuration = ".//ns:Object[@Type='Configuration']"
    namespace_type_configuraiton = {'ns': 'http://br-automation.co.at/AS/Physical'}

    system_names = read_existing_file(os.path.dirname(physical_path)+"\Physical.pkg", object_type_configuration, namespace_type_configuraiton)

    if system_name not in system_names:
        system_names += [system_name]

    if 'Core' in system_names:
        system_names.remove('Core')

    write_to_file(
        os.path.dirname(physical_path),
        'Physical.pkg',
        format_template(env, 'physical_pkg.tpl', system_names=system_names)
        )
    # create Config.pkg file
    write_to_file(
        physical_path,
        'Config.pkg',
        format_template(env, 'config_pkg.tpl', cpu_type='CPU')
        )
    # create Hardware.hw and Hardware.hwl files
    try:
        cpu_name = get_hardware_module_name(
            'cp1584,cp1684,cp3687X', system['Hardware']  # type: ignore
            )
        hardware_hw = generate_hardware_hw_contents(
            system['Hardware'], project_name, system_name, cpu_name, ftp1_pswd_hash, ftp2_pswd_hash  # type: ignore
            )
    except ValueError:
        logger.warning(
            'Hardware configuration does not contain a CPU module. '
            'Hardware.hw file will not be generated.'
            )
        hardware_hw = ''
    write_to_file(
        physical_path,
        'Hardware.hw',
        format_template(env, 'hardware_hw.tpl', hardware=hardware_hw)
        )
    write_to_file(
        physical_path,
        'Hardware.hwl',
        ''  # create an empty hwl file is enough
        )
    # create Cpu.pkg file
    is_safety = is_safety_configuration(system['Hardware'])  # type: ignore
    physical_cp1584_path = os.path.join(physical_path, 'CPU')
    write_to_file(
        physical_cp1584_path,
        'Cpu.pkg',
        format_template(env, 'cpu_pkg.tpl', add_mapp_safety=is_safety)
        )
    # optionally copy mappSafety:
    if is_safety:
        mapp_safety_path_src = os.path.join(
            os.path.dirname(physical_path), 'Core', 'CPU', 'mappSafety'
            )
        mapp_safety_path_dst = os.path.join(
            physical_path, 'CPU', 'mappSafety'
            )
        shutil.copytree(
            mapp_safety_path_src, mapp_safety_path_dst, dirs_exist_ok=True
            )
        for path in (
            os.path.join(mapp_safety_path_dst, '.git'),
            os.path.join(mapp_safety_path_dst, '.gitignore')
        ):
            if os.path.isfile(path):
                os.remove(path)
        sl_name = get_hardware_module_name(
            'sl8100,sl8101', system['Hardware']  # type: ignore
            )
        write_to_file(
            mapp_safety_path_dst,
            'Config.sfdomain',
            format_template(env, 'config_sfdomain.tpl', sl81xx_name=sl_name, sfdomainpassword=sfdomain_pswd_hash)
            )
    # create IoMap.iom file
    iomap = generate_iomap_iom_contents(sw_system_wrapper)
    write_to_file(
        physical_cp1584_path,
        'IoMap.iom',
        format_template(env, 'iomap_iom.tpl', iomap=iomap)
        )
    # create Zone.sw file
    tasks: dict[str, list[tuple[str, str]]] = {
        'tasks_cyclic1': [],
        'tasks_cyclic2': [
            ('Comm', f'{project_name}.{system_name}.Comm.prg')
            ],
        'tasks_cyclic3': [
            ('System', f'{project_name}.{system_name}.System.prg')
            ],
        'tasks_cyclic4': []
    }
    tasks_cyclic4 = tasks['tasks_cyclic4']
    for taskname in zone_tasknames:
        tasks_cyclic4.append(
            (taskname, f'{project_name}.{system_name}.{taskname}.prg')
            )
    libraries_list = sw_system_wrapper.get_project_libraries()
    libraries: list[tuple[str, str]] = []
    for lib in libraries_list:
        lib_cou, lib_name = lib.split('.')
        libraries.append(
            (lib_name, f'Libraries.Specific.{lib_cou}.{lib_name}.lby')
        )
    write_to_file(
        physical_cp1584_path,
        'Zone.sw',
        format_template(env, 'zone_sw.tpl', **tasks, libraries=libraries)
        )
