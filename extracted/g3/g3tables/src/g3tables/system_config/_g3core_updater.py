# lasciate ogni speranza, voi ch'entrate

import os
import typing

from g3core import G3Core

from .type_hinting import (
    SWDeviceDict,
    SWModuleDict,
    SWSystemDict
)
from ._sw_system_dict_wrapper import SWSystemDictWrapper
from ._logger import logger

if typing.TYPE_CHECKING:
    from g3core.st_parser import STStruct, STFunctionBlock, STVariable


class SWSystemDictG3CoreUpdater:
    ROUTE_ELEMENT_FB = {
        'pointmachine': 'fRoute_PM',
        'detector': 'fRoute_detector',
        'crossing': 'fRoute_crossing',
        'route': 'fRoute_subroute'
        }
    ROUTE_PM_POSITIONS = {
        'l': 'ROUTE_DIRECTION_LEFT',
        'r': 'ROUTE_DIRECTION_RIGHT',
        'default': 'ROUTE_DIRECTION_NONE'
        }

    def __init__(
        self,
        system: SWSystemDict,
        g3core: G3Core,
    ) -> None:
        self.wrapper = SWSystemDictWrapper(system)
        self.g3core = g3core

    def _update_device_connector_control_var(
        self,
        var: 'STVariable',
        zone_name: str,
        device_type: str,
        device_data: SWDeviceDict,
        connectors: dict[str, str | typing.Any]
    ) -> None:
        match var.name:
            case 'dev':
                var.value = device_data['general']['varname']
            case 'comm':
                connected_commfunc = connectors.get('comm')
                if connected_commfunc:
                    var.value = connected_commfunc
            case 'system':
                var.value = 'System'
            case 'zone':
                zone_data = self.wrapper.find_device(
                    zone_name, 'Zone', zone_name
                    )
                if zone_data is None:
                    logger.warning(
                        'Could not find data for Zone "%s". '
                        'Connector will be set to NULL.',
                        zone_name
                        )
                    var.value = None
                    return
                zone_varname = zone_data['general']['varname']
                var.value = zone_varname
            case 'fromCabinet':
                if 'fromCabinet' not in connectors:
                    logger.warning(
                        '%s "%s": "fromCabinet" connector is empty. '
                        'Connector will be set to NULL.',
                        device_type.capitalize(),
                        device_data["general"]["name"]
                        )
                    var.value = None
                    return
                connected_cabinet_data = self.wrapper.find_device(
                    zone_name,
                    'Cabinet',
                    connectors['fromCabinet']
                    )
                if not connected_cabinet_data:
                    logger.warning(
                        '%s "%s": "fromCabinet" connector is empty. '
                        'Connector will be set to NULL.',
                        device_type.capitalize(),
                        device_data["general"]["name"]
                        )
                    var.value = None
                    return
                connected_cabinet_varname = (
                    connected_cabinet_data['general']['varname']
                    )
                device_type = device_type.lower().capitalize()
                var.value = f'{connected_cabinet_varname}.to{device_type}'
            case _:
                if var.name not in connectors:
                    logger.warning(
                        '%s "%s": "%s" connector is added automatically '
                        'without a reference to any device.',
                        device_type.capitalize(),
                        device_data["general"]["name"],
                        var.name
                        )
                    var.value = None
                    return
                connected_device_name = connectors[var.name]
                if not connected_device_name:
                    logger.warning(
                        '%s "%s": "%s" connector is empty.',
                        device_type.capitalize(),
                        device_data["general"]["name"],
                        var.name
                        )
                    var.value = None
                    return
                if any(
                    req_type in device_type.lower()
                    for req_type in ['vecom', 'spie', 'drr']
                ) and var.name == 'controller':
                    req_type_tmp = device_type
                    req_type = device_type.removesuffix('Loop')
                    if(req_type == req_type_tmp):
                        req_type = device_type.removesuffix('Transceiver')
                    connected_device_type = f'{req_type}Controller'
                else:
                    name = f'{var.name[0].capitalize()}{var.name[1:]}'
                    connected_device_type = name
                connected_device_data = self.wrapper.find_device(
                    zone_name,
                    connected_device_type,
                    connected_device_name
                    )
                if not connected_device_data:
                    device_connector_path = (
                        f'{device_type}/{device_data["general"]["name"]}/'
                        f'control/connector/{var.name}'
                        )
                    logger.warning(
                        f'Could not find data for {connected_device_type} '
                        f'"{connected_device_name}" connected at '
                        f'"{device_connector_path}". '
                        f'Connector will be set to NULL.'
                        )
                    var.value = None
                else:
                    connected_device_varname = (
                        connected_device_data['general']['varname']
                        )
                    var.value = connected_device_varname

    def update_device_connectors_control(
        self,
        zone_name: str,
        device_type: str,
        device_data: SWDeviceDict,
        fb: 'STFunctionBlock'
    ) -> None:
        connectors = device_data['control'].get('connector', {})
        connectors_filtered = {}
        for conn_name, conn_value in connectors.items():
            if any(conn_name == var.name for var in fb.var_in_out):
                connectors_filtered[conn_name] = conn_value
            else:
                logger.warning(
                    '%s "%s": "%s" function block does not have a "%s" '
                    'IN_OUT variable. The connector will be removed. ',
                    device_type.capitalize(),
                    device_data["general"]["name"],
                    fb.name,
                    conn_name
                    )
        connectors = connectors_filtered
        for var in fb.var_in_out:
            self._update_device_connector_control_var(
                var, zone_name, device_type, device_data, connectors
                )
            connectors[var.name] = var.value
        device_data['control']['connector'] = connectors

    def update_device_connectors_test(
        self,
        zone_name: str,
        device_type: str,
        device_data: SWDeviceDict,
        fb: 'STFunctionBlock'
    ) -> None:
        if 'connector' not in device_data['test']:
            device_data['test']['connector'] = {}
        for var in fb.var_in_out:
            match var.name:
                case 'dev':
                    var.value = f"Test_{device_data['general']['varname']}"
                case 'comm':
                    control_commfunc = (
                        device_data['control']['connector'].get('comm')
                        )
                    if control_commfunc:
                        var.value = f"Test_{control_commfunc}"
                case 'system':
                    if device_type == 'System':
                        var.value = 'System'
                    else:
                        var.value = 'TestSystem'
                case _:
                    if var.name not in device_data['test']['connector']:
                        logger.warning(
                            'test/connector/%s: Reference to connected device '
                            'is empty.', var.name
                            )
                        continue
                    control_device_data = self.wrapper.find_device(
                        zone_name,
                        var.name.capitalize(),
                        device_data['control']['connector'][var.name]
                        )
                    if not control_device_data:
                        raise ValueError  # do warning here
                    connected_device_varname = (
                        f"Test_{control_device_data['general']['varname']}"
                        )
                    var.value = connected_device_varname
            device_data['test']['connector'][var.name] = var.value

    def update_device_config_control(
        self,
        zone_name: str,
        device_data: SWDeviceDict,
        config_struct: 'STStruct'
    ) -> None:
        if 'config' not in device_data['control']:
            device_data['control']['config'] = {}
        for var in config_struct.members:
            match var.name:
                case 'taskName':
                    value = self.wrapper.get_zone_taskname(zone_name)
                    var.value = value
                case 'varName':
                    value = self.wrapper.get_device_varname(device_data)
                    var.value = value
                # this is a hotfix to handle nested config data in Comm:SHV
                case 'parentBroker':
                    value = device_data['control']['config'][var.name]
                    assert isinstance(value, dict)
                    assert list(value.keys()) == ['connection']
                    assert isinstance(value['connection'], dict)
                    assert list(value['connection'].keys()) == [
                        'serverAddress', 'serverPort'
                        ]
                    server_addr = value['connection']['serverAddress']
                    if not server_addr or not isinstance(server_addr, str):
                        server_addr = "nirvana.elektroline.cz"
                        logger.warning(
                            '"parentBroker/connection/serverAddress": cannot '
                            'format value "%s" to data type "string". '
                            'Default value "%s" will be used instead.',
                            server_addr, server_addr
                            )
                    value['connection']['serverAddress'] = server_addr
                    server_port = value['connection']['serverPort']
                    try:
                        server_port = int(server_port)
                        if server_port <= 0:
                            raise ValueError("Value must be a positive number")
                    except ValueError as err:
                        server_port = 3756
                        logger.warning(
                            '"parentBroker/connection/serverPort": cannot '
                            'format value "%s" to data type "int" (%s). '
                            'Default value "%s" will be used instead.',
                            server_port, err, server_port
                            )
                    value['connection']['serverPort'] = server_port
                    var.value = value
                case _:
                    if var.name in device_data['control']['config']:
                        value = device_data['control']['config'][var.name]
                        var.value = value
            device_data['control']['config'][var.name] = var.to_py()

    def update_device_config_test(
        self,
        zone_name: str,  # for method signature consistency
        device_data: SWDeviceDict,
        config_struct: 'STStruct'
    ) -> None:
        if 'config' not in device_data['test']:
            device_data['test']['config'] = {}
        for var in config_struct.members:
            if var.name in device_data['test']['config']:
                var.value = device_data['test']['config'][var.name]
            elif var.value is None:
                logger.warning(
                    'test/config/%s: config parameter is empty.', var.name
                    )
            device_data['test']['config'][var.name] = var.to_py()

    def prefill_device_iomap_test(
        self, device_data: SWDeviceDict, fb: 'STFunctionBlock'
    ) -> None:
        if 'test' not in device_data:
            device_data['test'] = {}
        if 'iomap' not in device_data['test']:
            device_data['test']['iomap'] = {}
        for var in fb.var_input + fb.var_out:
            if var.name.startswith('in'):
                varname = f'out{var.name[2:]}'
            elif var.name.startswith('out'):
                varname = f'in{var.name[3:]}'
            else:
                logger.warning(
                    'Variable "%s" in function block "%s" has an unexpected '
                    'prefix (expected "in" or "out" prefix). Variable will be '
                    'added to the iomap as is.', var.name, fb.name
                    )
                varname = var.name
            device_data['test']['iomap'][var.name] = varname

    def update_device(
        self,
        zone_name: str,
        device_type: str,
        device_domain: typing.Literal['control', 'test'],
        device_data: SWDeviceDict
    ) -> None:
        logger.info(
            'Looking for %s "%s" %s function block type', device_type,
            self.wrapper.get_device_name(device_data), device_domain
            )
        fb_name = device_data[device_domain]['function']
        # validate if the function block name is specified
        if not fb_name:
            logger.warning(
                '%s function block type of %s "%s" is not specified. '
                'Device %s config data cannot be validated.',
                device_domain.capitalize(), device_type,
                self.wrapper.get_device_name(device_data), device_domain
                )
            return
        # add the test device varname to the general data
        if device_domain == 'test':
            varname_test = f"Test_{device_data['general']['varname']}"
            device_data['general']['varname_test'] = varname_test
        # get fb data corresponding to the specified fb name
        try:
            fb_path, fb = self.g3core.find_function_block(fb_name)
        except (KeyError, ValueError):
            logger.warning(
                '%s function block type of %s "%s" was not found in G3 Core '
                'files. Device %s config data cannot be validated.',
                device_domain.capitalize(), device_type,
                self.wrapper.get_device_name(device_data), device_domain
                )
            return
        # prefill test iomap keys with VAR_IN and VAR_OUT fb members
        if device_domain == 'test':
            logger.info(
                'Prefilling test VAR_IN and VAR_OUT keys for %s "%s"',
                device_type, self.wrapper.get_device_name(device_data)
                )
            self.prefill_device_iomap_test(device_data, fb)
        # update function block VAR_IN_OUT variables ("connectors")
        updader = getattr(self, f'update_device_connectors_{device_domain}')
        updader(zone_name, device_type, device_data, fb)
        # get the "dev" VAR_IN variable
        vars_dev = [var for var in fb.var_in_out if var.name == 'dev']
        if not vars_dev:
            logger.info(
                '"dev" member was not found in %s function block "%s". '
                'Device config data will be discarded.', device_domain, fb.name
                )
            device_data[device_domain]['config'] = {}
            device_data[device_domain]['devType'] = ''
            return
        var_dev = vars_dev[0]
        # get the "dev" struct data (raises an error if unsuccessful)
        dev_struct_path, dev_struct = self.g3core.find_struct(
            var_dev.dtype,  # the name of the struct
            search_here_first=f'{os.path.dirname(fb_path)}/Types.typ'
            )
        # update "dev" struct name in the device control data
        device_data[device_domain]['devType'] = dev_struct.name
        # get the "config" member (also a struct) of the "dev" struct
        try:
            memb_config = [
                memb for memb in dev_struct.members if memb.name == 'config'
                ][0]
        except IndexError:
            logger.info(
                '"config" member was not found in %s function block "%s". '
                'Device config data will be discarded.', device_domain, fb.name
                )
            device_data[device_domain]['config'] = {}
            return
        # get the "config" struct data (raises an error if unsuccessful)
        config_struct_path, config_struct = self.g3core.find_struct(
            memb_config.dtype, search_here_first=dev_struct_path
            )
        updader = getattr(self, f'update_device_config_{device_domain}')
        updader(zone_name, device_data, config_struct)

    def update_route_layout(self, route_data: SWDeviceDict) -> None:
        # remove and store the "route_elements" key value
        layout_str: str = route_data['general'].pop('route_elements')
        if not layout_str:
            route_data['general']['layout'] = []
            route_data['general']['length'] = 0
            return
        # define standard element length
        pm_len = 4
        det_len = 8
        cross_len = 2
        space_len = 2
        element_startoffset = 2
        route_len = 0
        # process the "route_elements" key value
        layout = []
        for element in layout_str.split(','):
            element = element.strip(' ')
            kwargs = {}  # additional element-specific key-value data pairs
            # get the element type and params
            if '@' in element:
                position, element_name = element.split('@')
                position = self.ROUTE_PM_POSITIONS.get(
                    position.lower(), self.ROUTE_PM_POSITIONS['default']
                    )
                element_type = 'pointmachine'
                element_len = pm_len
                kwargs['position'] = position
            elif '#' in element:
                element_name = f"CROSSING{element.lstrip('#')}"
                element_type = 'crossing'
                element_len = cross_len
            elif '$' in element:
                tmp, element_name = element.split('$')
                element_type = 'route'
                element_len = det_len
            else:
                element_name = element
                element_type = 'detector'
                element_len = det_len
            # create and save the element data dict
            element_endoffset = element_startoffset + element_len
            element_data = {
                'name': element_name,
                'type': element_type,
                'function': self.ROUTE_ELEMENT_FB[element_type],
                'startoffset': element_startoffset,
                'endoffset': element_endoffset,
                }
            element_data.update(kwargs)
            layout.append(element_data)
            element_startoffset = element_endoffset + space_len
        # save the created list of layout elements
        route_len = element_startoffset
        route_data['general']['layout'] = layout
        route_data['general']['length'] = route_len

    def _validate_module(
        self,
        zone_name: str,
        module_name: str,
        module_data: SWModuleDict,
        ignore: list[str] | None = None
    ) -> None:
        if ignore and module_name in ignore:
            logger.debug(
                'Module data validation for "%s/%s" is ignored',
                zone_name, module_name
                )
            return
        logger.info(
            'Validating module data for "%s/%s"', zone_name, module_name
            )
        for device_name, device_data in module_data.items():
            logger.info(
                'Validating control device data for "%s/%s/%s"',
                zone_name, module_name, device_name
                )
            self.update_device(
                zone_name, module_name, 'control', device_data
                )
            logger.info(
                'Validating test device data for "%s/%s/%s"',
                zone_name, module_name, device_name
                )
            self.update_device(
                zone_name, module_name, 'test', device_data
                )
            if module_name == 'Route':
                logger.info(
                    'Updating route "%s/%s/%s" layout data',
                    zone_name, module_name, device_name
                    )
                self.update_route_layout(device_data)
            logger.debug(
                'Validating children device data for device "%s/%s/%s"',
                zone_name, module_name, device_name
                )
            children = device_data.setdefault('children', {})
            if children:
                for child_module_name, child_module_data in children.items():
                    self._validate_module(
                        zone_name, child_module_name, child_module_data, ignore
                        )

    def validate(self) -> None:
        logger.info(
            'Validating system data for "%s"',
            self.wrapper.get_system_name()
            )
        for zone_name, zone_data in self.wrapper.system_dict.items():
            logger.info('Validating zone data for "%s"', zone_name)
            for module_name, module_data in zone_data.items():
                self._validate_module(
                    zone_name,
                    module_name,
                    module_data,
                    ignore=['Project', 'System']
                    )
