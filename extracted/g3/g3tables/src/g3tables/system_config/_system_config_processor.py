import json
import os

from g3core import G3Core
from g3tables import (
    SWDefinitionTable, PLCCompositionIOTable, VisualizationTable
)

from ._g3core_updater import SWSystemDictG3CoreUpdater
from ._hw_connections import get_hardware_connections
from ._iomap_updater import (
    SWSystemDictControlIOMapUpdater, SWSystemDictTestIOMapUpdater
)
from ._logger import logger  # noqa: F401
from .type_hinting import SystemDict


class SystemConfigProcessor:
    def __init__(
        self,
        system_name: str | None = None,
        sw_table: SWDefinitionTable | None = None,
        io_table: PLCCompositionIOTable | None = None,
        visu_table: VisualizationTable | None = None,
        g3core: G3Core | None = None
    ) -> None:
        self.system_name = system_name
        self.sw_table = sw_table
        self.io_table = io_table
        self.visu_table = visu_table
        self.g3core = g3core
        self._system_dict: SystemDict = {
            'Hardware': [], 'Software': {}, 'Visu': {}
            }

    def _process_sw_table(self) -> None:
        if self.sw_table is None:
            return
        if self.g3core is None:
            raise ValueError('G3Core not provided')
        if not self.system_name:
            raise ValueError('System name not provided')
        sw_system_dict = self.sw_table.to_dict(self.system_name)
        SWSystemDictG3CoreUpdater(sw_system_dict, self.g3core).validate()
        SWSystemDictTestIOMapUpdater(sw_system_dict, self.g3core).update()
        self._system_dict['Software'] = sw_system_dict

    def _process_io_table(self) -> None:
        if self.io_table is None:
            return
        if self._system_dict['Software']:
            SWSystemDictControlIOMapUpdater(
                self._system_dict['Software'],
                iomap=self.io_table.get_iomapping(),
                sl81xx_name=self.io_table.get_sl81xx_name(),
                g3core=self.g3core
            ).update()
        self._system_dict['Hardware'] = get_hardware_connections(self.io_table)

    def _process_visu_table(self) -> None:
        if self.visu_table is None:
            return
        table = self.visu_table
        visu = table.project_types
        if '' in visu:
            del visu['']
        for data in [
            table.gate_tables,
            table.heating_tables,
            table.requestor_tables
        ]:
            for type_, subtype_data in data.items():  # type: ignore
                type_data = visu.setdefault(
                    type_,
                    {'type': type_, 'restricted_to': None, 'vars': {}}
                    )
                type_data['type_variants'] = subtype_data
        self._system_dict['Visu'] = visu

    def to_dict(self) -> SystemDict:
        self._process_sw_table()
        self._process_io_table()
        self._process_visu_table()
        return self._system_dict

    def to_file(
        self,
        dirpath: str = '.',
        filename: str = 'SystemConfig.json',
        update_if_exists: bool = False
    ) -> None:
        dirpath = dirpath if dirpath != '.' else os.getcwd()
        system_dict = self.to_dict()
        filepath = os.path.join(dirpath, filename)
        if not update_if_exists or not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(system_dict, file, indent=4)
        elif not os.path.isfile(filepath):
            raise TypeError(
                f'Path "{filepath}" exists, but does not lead to a file.'
                )
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                system_dict_old = json.load(file)
            if not isinstance(system_dict_old, dict):
                raise TypeError(
                    f'System configuration file "{filepath}" has unexpected '
                    f'structure.'
                    )
            system_dict_old.update(system_dict)
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(system_dict_old, file, indent=4)
