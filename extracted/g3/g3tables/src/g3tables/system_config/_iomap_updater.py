import itertools

from g3core import G3Core, STVariable

from .type_hinting import (
    SWDeviceDict,
    SWModuleDict,
    SWSystemDict
)
from ._sw_system_dict_wrapper import SWSystemDictWrapper
from ._logger import logger


class SWSystemDictControlIOMapUpdater:
    EXCLUDED_FOR_SAFETY_IOMAP = []

    def __init__(
        self,
        system: SWSystemDict,
        iomap: dict[str, dict[str, str]] | None,
        sl81xx_name: str | None,
        g3core: G3Core | None
    ) -> None:
        self.wrapper = SWSystemDictWrapper(system)
        self.iomap = iomap
        self.sl81xx_name = sl81xx_name
        self.g3core = g3core
        self._counters = self._create_iomap_counters()

    @staticmethod
    def _create_iomap_counters() -> dict:
        return {
            "inFromSafety": {
                "UDINT": itertools.count(1),
                "UINT": itertools.count(1)
            },
            "outToSafety": {
                "UDINT": itertools.count(1001),
                "UINT": itertools.count(1001)
            },
            "inAuthKey": {
                "INT": itertools.count(1)
            },
            "inAuthBusy": {
                "BOOL": itertools.count(1)
            },
            "inAuthResult": {
                "BOOL": itertools.count(2)
            },
            "outAuthKey": {
                "INT": itertools.count(1001)
            },
            "outAuthCmd": {
                "INT": itertools.count(1002)
            }
        }

    def _update_iomap_device(
        self, device_data: SWDeviceDict, iomap_key: str
    ) -> None:
        if not self.iomap:
            return
        iomap = self.iomap.get(iomap_key)
        if iomap is None:
            return
        iomap_dict = device_data['control'].setdefault('iomap', {})
        for key, value in iomap.items():
            iomap_dict[key] = value

    def _generate_safety_hardware_mapping(self, var: STVariable) -> str:
        assert self.sl81xx_name is not None
        match var.name, var.dtype:
            case 'inFromSafety', 'UINT':
                prefix = '%IW'
            case 'inFromSafety', 'UDINT':
                prefix = '%ID'
            case 'inAuthKey', 'INT':
                prefix = '%IW'
            case 'inAuthBusy', 'BOOL':
                prefix = '%IX'
            case 'inAuthResult', 'BOOL':
                prefix = '%IX'
            case 'outAuthKey', 'INT':
                prefix = '%QW'
            case 'outAuthCmd', 'INT':
                prefix = '%QW'
            case 'outToSafety', 'UINT':
                prefix = '%QW'
            case 'outToSafety', 'UDINT':
                prefix = '%QD'
            case _:
                logger.warning(
                    'Unable to generate safety IO mapping for variable "%s" '
                    'of type "%s"', var.name, var.dtype
                    )
                return ''
        counter = self._counters[var.name][var.dtype]
        if (var.name == "inAuthBusy") or (var.name == "inAuthResult") :
            return (
                f'{prefix}."{self.sl81xx_name}".{var.dtype}'
                f'{next(counter):05}'
                )
        else:
            return (
                f'{prefix}."{self.sl81xx_name}".{var.dtype}'
                f'{next(counter):04}'
                )

    def _update_iomap_device_safety(
        self, device_type: str, device_data: SWDeviceDict
    ) -> None:
        device_name = self.wrapper.get_device_name(device_data)
        # get the control fb name
        fb_name = self.wrapper.get_device_control_fb(device_data)
        if not fb_name:
            if not self.sl81xx_name:
                return
            logger.warning(
                '%s "%s" function block name was not found in the config data.'
                ' safety IO mapping to harware module "%s" cannot be added.',
                device_type, device_name, self.sl81xx_name
                )
            return
        # check if device is a safety device (from fb name)
        if 'safety' not in fb_name.lower() or 'non' in fb_name.lower():
            logger.debug(
                '%s "%s" is not a safety device. safety IO mapping to harware '
                'module "%s" is not needed.',
                device_type, device_name, self.sl81xx_name
                )
            return
        # check if SL8101 module and G3 Core library data is provided
        if self.sl81xx_name is None:
            logger.warning(
                'Unable to generate safety IO mapping for %s "%s" '
                '(X20cSL81xx harware module name was not found).',
                device_type, device_name
                )
            return
        logger.info(
            'Generating safety IO mapping to harware module "%s" for '
            '%s "%s".', self.sl81xx_name, device_type, device_name
            )
        if self.g3core is None:
            logger.warning(
                'Unable to generate safety IO mapping for %s "%s" '
                '(G3 Core library files were not found).',
                device_type, device_name
                )   # G3 Core check is inside this func because it may not be
            return  # needed if the project is not safety
        # find the fb data
        try:
            _, control_fb = self.g3core.find_function_block(fb_name)
        except ValueError as err:
            logger.warning(
                'Unable to generate safety IO mapping for %s "%s" (%s).',
                device_type, device_name, str(err)
                )
            return
        # generate and fill in the safety module io mapping
        iomap_dict = device_data['control'].setdefault('iomap', {})
        for var in control_fb.var_input:
            if var.name == "inFromSafety":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "inFromSafety" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['inFromSafety'] = hardware_signal
                    break
        for var in control_fb.var_out:
            if var.name == "outToSafety":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "outToSafety" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['outToSafety'] = hardware_signal
                    break
        for var in control_fb.var_input:
            if var.name == "inAuthKey":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "inAuthKey" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['inAuthKey'] = hardware_signal
                    break 
        for var in control_fb.var_input:
            if var.name == "inAuthBusy":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                print(hardware_signal)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "inAuthBusy" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['inAuthBusy'] = hardware_signal
                    break        
        for var in control_fb.var_input:
            if var.name == "inAuthResult":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                print(hardware_signal)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "inAuthResult" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['inAuthResult'] = hardware_signal
                    break    
        for var in control_fb.var_out:
            if var.name == "outAuthKey":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "outAuthKey" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['outAuthKey'] = hardware_signal
                    break    
        for var in control_fb.var_out:
            if var.name == "outAuthCmd":
                hardware_signal = self._generate_safety_hardware_mapping(var)
                if hardware_signal:
                    logger.info(
                        'Mapping %s "%s" "outAuthCmd" connector to "%s".',
                        device_type, device_name, hardware_signal
                        )
                    iomap_dict['outAuthCmd'] = hardware_signal
                    break    

    def _update_iomap_module(
        self,
        module_name: str,
        module_data: SWModuleDict,
        ignore: list[str] | None = None
    ) -> None:
        for device_name, device_data in module_data.items():
            if ignore is None or module_name not in ignore:
                iomap_key = f'{module_name}/{device_name}'
                self._update_iomap_device(device_data, iomap_key)
                self._update_iomap_device_safety(module_name, device_data)
            children = device_data.get('children')
            if children:
                for ch_module_name, ch_module_data in children.items():
                    self._update_iomap_module(
                        f'{module_name}/{ch_module_name}',
                        ch_module_data,
                        ignore=ignore
                        )

    def _update_iomap_module_cabinet(
        self,
        module_data: SWModuleDict,
        ignore: list[str] | None = None
    ) -> None:
        for cabinet_name, cabinet_data in module_data.items():
            iomap_key = f'Cabinet/{cabinet_name}'
            if ignore is None or 'Cabinet' not in ignore:
                self._update_iomap_device(cabinet_data, iomap_key)
            children = cabinet_data.get('children')
            assert children is not None
            for ch_module_name, ch_module_data in children.items():
                if ignore and ch_module_name in ignore:
                    continue
                for ch_device_name, ch_device_data in ch_module_data.items():
                    ch_iomap_key = (
                        f'{iomap_key}/{ch_module_name}/{ch_device_name}'
                        )
                    self._update_iomap_device(ch_device_data, ch_iomap_key)
                    self._update_iomap_device_safety(
                        ch_module_name, ch_device_data
                        )

    def update(self) -> None:
        for zone_name, zone_data in self.wrapper.system_dict.items():
            if zone_name == 'Common':  # nothing to update in the 'Common' data
                for module_name, module_data in zone_data.items():
                    if module_name == 'SystemSafety':
                        self._update_iomap_module(
                            module_name,
                            module_data,
                            ignore=self.EXCLUDED_FOR_SAFETY_IOMAP
                            )
                continue
            for module_name, module_data in zone_data.items():
                if module_name == 'Cabinet':
                    self._update_iomap_module_cabinet(module_data)
                else:
                    self._update_iomap_module(
                        module_name,
                        module_data,
                        ignore=self.EXCLUDED_FOR_SAFETY_IOMAP
                        )


class SWSystemDictTestIOMapUpdater:
    def __init__(self, system: SWSystemDict, g3core: G3Core) -> None:
        self.wrapper = SWSystemDictWrapper(system)
        self.g3core = g3core

    def update(self) -> None:
        pass
