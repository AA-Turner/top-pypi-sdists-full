from g3hardware import format_type, is_isle_head_type
from g3tables import PLCCompositionIOTable

from ._logger import logger
from .type_hinting import HWIsleDict, HWModuleDict


def get_hardware_connections(table: PLCCompositionIOTable) -> list[HWIsleDict]:
    connections: list[HWIsleDict] = []
    isle: HWIsleDict | None = None
    logger.info('Extracting hardware connections from PLCCompositionIOTable')
    for module_type, cabinet, name_suffix in table.iter_plc_units():
        module_type = format_type(module_type)
        module_dict: HWModuleDict = {
            'type': module_type,
            'cabinet': cabinet,
            'name_suffix': name_suffix
            }
        if is_isle_head_type(module_type):
            isle = {'head': module_dict, 'tail': []}
            connections.append(isle)
        elif isle is None:
            continue
        else:
            isle['tail'].append(module_dict)
    return connections
