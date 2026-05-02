import typing

from .type_hinting import (
    SWDeviceDict,
    SWModuleDict,
    SWSystemDict
)


class SWSystemDictWrapper:
    ZONE_TASKNAME_MAXLEN = 10

    def __init__(self, system: SWSystemDict) -> None:
        self.system_dict = system

    @property
    def common_data(self) -> dict:
        return {
            module: data
            for module, data in self.system_dict.get('Common', {}).items()
            if module not in ['Project']
            }

    @property
    def comm_data(self) -> dict:
        return {
            module: data
            for module, data in self.system_dict.get('Common', {}).items()
            if module not in ['Project', 'System', 'SystemSafety']
            }

    @property
    def redmine_data(self) -> dict[str, str]:
        for device_data in self.system_dict['Common']['Project'].values():
            return device_data['redmine']  # type: ignore
        return {}

    @property
    def zone_names(self) -> list[str]:
        return [
            name for name in list(self.system_dict.keys()) if name != 'Common'
            ]

    @property
    def zone_tasknames(self) -> list[str]:
        return [
            self.get_zone_taskname(name) for name in self.zone_names
            ]

    def get_zone_taskname(self, zone_name: str) -> str:
        if len(self.system_dict.keys()) < 3:  # not a multizone
            taskname = "Zone"
        else:
            zone_data = self.system_dict[zone_name]['Zone'][zone_name]
            varname = zone_data['general']['name']
            taskname = varname[:self.ZONE_TASKNAME_MAXLEN].strip('_')
        return taskname

    def has_system_safety(self) -> bool:
        return bool(self.system_dict['Common'].get('SystemSafety'))

    def has_shv(self) -> bool:
        return bool(self.system_dict['Common'].get('SHV'))

    def has_elesys(self) -> bool:
        return bool(self.system_dict['Common'].get('Elesys'))

    def get_project_name(self) -> str:
        for key in self.system_dict['Common']['Project'].keys():
            return key
        raise KeyError('Project data is empty.')

    def get_system_name(self) -> str:
        for key in self.system_dict['Common']['System'].keys():
            return key
        raise KeyError('System data is empty.')

    def get_project_libraries(self) -> list[str]:
        project_name = self.get_project_name()
        project_data = self.system_dict['Common']['Project'][project_name]
        libraries = project_data['general'].get('specificLibraries', '')
        assert isinstance(libraries, str)
        return [lib.strip() for lib in libraries.split(',')]

    @staticmethod
    def is_device_safety(device_data: SWDeviceDict) -> bool:
        func = device_data.get('control', {}).get('function', '').lower()
        return ('safety' in func) and ('non' not in func)

    @staticmethod
    def get_device_name(device_data: SWDeviceDict) -> str:
        return device_data['general']['name']

    @staticmethod
    def get_device_varname(device_data: SWDeviceDict) -> str:
        return device_data['general']['varname']

    @staticmethod
    def get_device_control_fb(device_data: SWDeviceDict) -> str | None:
        return device_data['control'].get('function')

    @staticmethod
    def get_device_test_fb(device_data: SWDeviceDict) -> str | None:
        return device_data['test'].get('function')

    @staticmethod
    def get_connected_device_type(connector_key: str) -> str:
        return connector_key.split('/').pop().capitalize()

    def _find_device(
        self,
        module_data: dict[str, SWModuleDict],
        connected_device_type: str,
        connected_device_name: str
    ) -> SWDeviceDict | None:
        try:
            devices = module_data[connected_device_type]
            if connected_device_name not in devices:
                return None
            return devices[connected_device_name]
        except KeyError:
            for devices in module_data.values():
                for device_data in devices.values():
                    device = self._find_device(
                        device_data.get('children', {}),
                        connected_device_type,
                        connected_device_name
                        )
                    if device is not None:
                        return device
            return None

    def find_device(
        self,
        zone_name: str,
        connected_device_type: str,
        connected_device_name: str
    ) -> SWDeviceDict | None:
        device = self._find_device(
            self.system_dict[zone_name],
            connected_device_type,
            connected_device_name
            )
        if device is not None:
            return device
        device = self._find_device(
            self.system_dict['Common'],
            connected_device_type,
            connected_device_name
            )
        return device

    def _collect_device(
        self,
        device_type: str,
        device_name: str,
        device_data: SWDeviceDict,
        device_path_prefix: str,
    ) -> typing.Iterator[tuple[str, str, SWDeviceDict]]:
        """->parent_device_path, device_path, device_data"""
        device_path = f'{device_type}/{device_name}'
        if device_path_prefix:
            device_path = f'{device_path_prefix}/{device_path}'
        yield (device_path_prefix, device_path, device_data)
        children = device_data.get('children')
        if children:
            for ch_module_name, ch_module_data in children.items():
                yield from self._collect_module(
                    ch_module_name, ch_module_data, device_path
                    )

    def _collect_module(
        self,
        module_name: str,
        module_data: SWModuleDict,
        module_path_prefix: str,
    ) -> typing.Iterator[tuple[str, str, SWDeviceDict]]:
        """->parent_device_path, device_path, device_data"""
        for device_name, device_data in module_data.items():
            yield from self._collect_device(
                module_name,
                device_name,
                device_data,
                module_path_prefix,
                )

    def iter_devices_zone(
        self, zone_name: str
    ) -> typing.Iterator[tuple[str, str, SWDeviceDict]]:
        """->parent_device_path, device_path, device_data"""
        zone_data = self.system_dict[zone_name]
        for module_name, module_data in zone_data.items():
            yield from self._collect_module(module_name, module_data, '')

    def iter_devices_system(
        self
    ) -> typing.Iterator[tuple[str, str, str, SWDeviceDict]]:
        """->zone, parent_device_path, device_path, device_data"""
        for zone_name in self.system_dict:
            for parent_path, path, data in self.iter_devices_zone(zone_name):
                yield (zone_name, parent_path, path, data)

    def flatten(self) -> dict[str, SWDeviceDict]:
        return {
            f'{zone_name}/{device_path}': device_data
            for zone_name, _, device_path, device_data
            in self.iter_devices_system()
            }
