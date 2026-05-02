import argparse
import functools
import os
import logging
import typing

from g3core import G3Core

from ..plc_composition_io_table import PLCCompositionIOTable
from ..sw_definition_table import SWDefinitionTable
from ..visualization_table import VisualizationTable
from ..utils.gdrive import list_tables_from_gdrive
from ._system_config_processor import SystemConfigProcessor
from ._logger import logger


class InputArgValidators:

    @classmethod
    def gdrive_folder(cls, folder: typing.Any) -> tuple[str, str | None]:
        """folder@system -> folder, system"""
        folder = cls.is_str(folder, 'Google Drive folder')
        folder_data: list[str] = folder.split('@')
        if len(folder_data) == 1:
            folder, system = folder_data[0].strip(), None
        elif len(folder_data) == 2:
            folder, system = folder_data[0].strip(), folder_data[1].strip()
        else:
            raise ValueError('Invalid Google Drive folder format.')
        if not folder:
            raise ValueError('Google Drive folder name cannot be empty.')
        if not system:
            raise ValueError('System name cannot be empty.')
        return folder, system

    @classmethod
    def sw_table_path(cls, path: typing.Any) -> tuple[str, str]:
        """path@system -> path, system"""
        path = cls.is_str(path, 'SW Definition table path')
        path_data: list[str] = path.split('@')
        if len(path_data) != 2:
            raise ValueError('Invalid SW Definition table path format.')
        path, system_name = path_data[0].strip(), path_data[1].strip()
        if not path:
            raise ValueError('SW Definition table path cannot be empty.')
        if not system_name:
            raise ValueError('System name cannot be empty.')
        return path, system_name

    @classmethod
    def io_table_path(cls, path: typing.Any) -> tuple[str, set[str]]:
        """path@cabinet1+cabinet2 -> path, [cabinet1, cabinet2]"""
        path = cls.is_str(path, 'PLC Composition IO table path')
        path_data: list[str] = path.split('@')
        if len(path_data) == 1:
            path = path_data[0].strip()
            sheets = set()
        elif len(path_data) == 2:
            path = path_data[0].strip()
            sheets = set((sh.strip() for sh in path_data[1].split('+') if sh))
        else:
            raise ValueError('Invalid PLC Composition IO table path format.')
        if not path:
            raise ValueError('PLC Composition IO table path cannot be empty.')
        return path, sheets

    @classmethod
    def visu_table_path(cls, path: typing.Any) -> str:
        """path -> path"""
        path = cls.is_str(path, 'Visualization table path')
        if not path:
            raise ValueError('Visualization table path cannot be empty.')
        return path

    @classmethod
    def g3core_path(cls, path: typing.Any) -> tuple[str, str]:
        if path is None:
            return 'remote', 'master'  # default fallback
        path = cls.is_str(path, 'G3Core library path')
        path_data: list[str] = path.split('@')
        if len(path_data) == 1:
            path = path_data[0].strip()
            if path == 'remote':
                return path, 'master'
            elif os.path.isdir(path):
                return path, ''
            raise ValueError(
                f'Specified local G3Core library directory "{path}" '
                f'does not exist.'
                )
        elif len(path_data) == 2:
            path, branch = path_data[0].strip(), path_data[1].strip()
            if path != 'remote':
                raise ValueError(
                    'Local G3Core directory path got an unexpected branch '
                    'specification. An @-separated path can only be used with '
                    'the "remote" prefix, e.g., "remote@master".'
                    )
            return path, branch
        else:
            raise ValueError('Invalid G3Core directory path format.')

    @staticmethod
    def is_str(arg: typing.Any, arg_name: str) -> str:
        if not isinstance(arg, str):
            raise TypeError(
                f'Invalid {arg_name} type: "{type(arg).__name__}" '
                f'(expected type "str").'
                )
        return arg

    @classmethod
    def is_system_name_valid(
        cls, name_sw_table: str, name_gdrive: str
    ) -> str | None:
        if name_sw_table and name_gdrive:
            if name_sw_table == name_gdrive:
                return cls.is_str(name_sw_table, 'system name')
            raise ValueError(
                f'Specified system name is ambiguous (SW Definition table: '
                f'"{name_sw_table}", Google Drive folder: "{name_gdrive}").'
                )
        if not name_sw_table and not name_gdrive:
            return None
        if name_sw_table and not name_gdrive:
            return cls.is_str(name_sw_table, 'system name')
        if not name_sw_table and name_gdrive:
            return cls.is_str(name_gdrive, 'system name')
        raise ValueError(
            f'Unexpected system name (SW Definition table: '
            f'"{name_sw_table}", Google Drive folder: "{name_gdrive}").'
            )  # should not happen


class InputArgs(typing.TypedDict):
    gdrive_folder: str | None
    sw_table_path: str | None
    system_name: str | None
    io_table_path: str | None
    io_table_sheets: set[str] | None
    visu_table_path: str | None
    g3core_path: str
    g3core_branch: str
    update: bool
    output_path: str
    log_level: str


def get_input_args() -> InputArgs:
    parser = argparse.ArgumentParser(
        description=(
            'Create a JSON representation of a G3 System configuration data.'
            )
        )
    parser.add_argument(
        '-g',
        '--gdrive_folder',
        type=InputArgValidators.gdrive_folder,
        required=False,
        default=(None, None),
        help=(
            'Remote Google Drive repository folder name (e.g., "Prg015") '
            'with Project G3 project tables. The tables in the folder are '
            'identified automatically. Any automatically collected table name '
            'is overridden by a corresponding explicitly provided argumement. '
            'Format as follows: "<gdrive_folder>@<system_name>", e.g., '
            '"Prg015@Zone01".'
            )
        )
    parser.add_argument(
        '-sw',
        '--swtable-path',
        type=InputArgValidators.sw_table_path,
        required=False,
        default=(None, None),
        help=(
            'Path to the SW Definition Table. The path ending with ".xlsx" '
            'is considered to be a local file path. Otherwise, the path '
            'is considered to be a Google Drive table name. If the name '
            'contains whitespace, it should be enclosed in quotes. '
            'Format as follows: "<table_path>@<system_name>"., e.g., '
            '"SWDef_Prg015.xlsx@Zone01" or '
            '"Prg015 G3 project SW definition EID00012345"@Zone01.'
            )
        )
    parser.add_argument(
        '-io',
        '--iotable-path',
        type=InputArgValidators.io_table_path,
        required=False,
        default=(None, []),
        help=(
            'Path to the PLC Composition and IO table. The path ending with '
            '".xlsx" is considered to be a local file path. Otherwise, '
            'the path is considered to be a Google Drive table name. If '
            'the name contains whitespace, it should be enclosed in quotes.'
            'If the cabinet names are not provided, they are extracted from '
            'the SW Definition Table data. '
            'Format as follows: '
            '1) "<table_path>" (no sheet names provided, e.g., '
            '"Prg015_HW.xlsx" or '
            '"Prg015 PLC composition and IO Table EID00012345"); '
            '2) "<table_path>@<cabinet_name>" (one sheet name provided, e.g., '
            '"Prg015_HW.xlsx@SIG01" or '
            '"Prg015 PLC composition and IO Table EID00012345"@SIG01); '
            '3) "<table_path>@<cabinet_name1>+<cabinet_name2>+<cabinet_name3>"'
            ' (two or more sheet names provided, e.g., ).'
            '"Prg015_HW.xlsx@SIG01+SIG02" or '
            '"Prg015 PLC composition and IO Table EID00012345"@SIG01+SIG02); '
            )
        )
    parser.add_argument(
        '-v',
        '--visutable-path',
        type=InputArgValidators.visu_table_path,
        required=False,
        default=None,
        help=(
            'Path to the Visualization table. The path ending with ".xlsx" is '
            'considered to be a local file path. Otherwise, the path is '
            'considered to be a Google Drive table name. If the name contains '
            'whitespace, it should be enclosed in quotes. Format as follows: '
            '"<table_path>", e.g., "Visu_Prg015.xlsx" or '
            '"Prg015 G3 project Visualization EID00012345".'
            )
        )
    parser.add_argument(
        '-c',
        '--g3core-path',
        type=InputArgValidators.g3core_path,
        required=False,
        default=('remote', 'master'),
        help=(
            'Path to the G3 Core library files. Format as follows: '
            '1) "<local_path>", e.g., "C:/.../SystemG3Core"; '
            '2) "remote" (default brach "master" is used); '
            '3) "remote@<branch>" (the branch may be referred by its name or '
            'by its hash), e.g., "remote@master", "remote@Mil014", or '
            '"remote@f02ddf805d25c2f8d61edd11a06f8e28e4b447bd".'
            )
        )
    parser.add_argument(
        '-u',
        '--update',
        action='store_true',
        help=(
            'Update an existing JSON configuration file, only adding new '
            'key-value pairs and preserving existing data.'
            )
        )
    parser.add_argument(
        '-o',
        '--output-path',
        type=str,
        required=False,
        default=os.getcwd(),
        help='Path to the directory to save the JSON configuration file to.'
        )
    parser.add_argument(
        '--log-level',
        type=str,
        required=False,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level.'
        )
    args = parser.parse_args()
    sw_table_path, sw_table_system_name = args.swtable_path
    io_table_path, io_table_sheets = args.iotable_path
    g3core_path, g3core_branch = args.g3core_path
    gdrive_folder, gdrive_system_name = args.gdrive_folder
    try:
        system_name = InputArgValidators.is_system_name_valid(
            sw_table_system_name, gdrive_system_name
            )
    except Exception as e:
        logger.error(e)
        raise SystemExit from e
    return {
        'gdrive_folder': gdrive_folder,
        'sw_table_path': sw_table_path,
        'system_name': system_name,
        'io_table_path': io_table_path,
        'io_table_sheets': io_table_sheets,
        'visu_table_path': args.visutable_path,
        'g3core_path': g3core_path,
        'g3core_branch': g3core_branch,
        'update': args.update,
        'output_path': args.output_path,
        'log_level': args.log_level
        }


class InputArgsProcessor:
    def __init__(self, args: InputArgs) -> None:
        self._args = args

    @functools.cached_property
    def g3core(self) -> G3Core:
        g3core_path = self._args['g3core_path']
        g3core_branch = self._args['g3core_branch']
        if g3core_path == 'remote':
            return G3Core.from_giltab(branch=(g3core_branch or 'master'))
        if g3core_branch:
            raise ValueError(
                'Local G3Core directory path got an unexpected branch '
                'specification. An @-separated path should be used '
                'with the "remote" prefix, e.g., "remote@master".'
                )
        return G3Core.from_local(g3core_path)

    @functools.cached_property
    def gdrive_tables(self) -> list[str]:
        gdrive_folder = self._args['gdrive_folder']
        if not gdrive_folder:
            return []
        return list_tables_from_gdrive(project=gdrive_folder)

    @functools.cached_property
    def sw_table(self) -> SWDefinitionTable | None:
        table_path = self._args['sw_table_path']
        if table_path:
            return SWDefinitionTable.load(table_path)
        for table in self.gdrive_tables:
            if SWDefinitionTable.is_name_valid(table):
                return SWDefinitionTable.from_gdrive(table)
        return None

    @functools.cached_property
    def io_sheets(self) -> set[str]:
        # check if io sheets are provided by the user
        if self._args['io_table_sheets']:
            return self._args['io_table_sheets']
        # try parsing the sheets (as cabinet names) from the sw table
        system = self._args['system_name']
        sheets: set[str] = set()
        if not self.sw_table or not system:
            return sheets
        zone_names = self.sw_table.get_system_sheets(system).keys()
        for zone_name in zone_names:
            if zone_name == 'Common':
                continue
            for cabinet_name in self.sw_table.get_cabinet_names(zone_name):
                sheets.add(cabinet_name)
        return sheets

    @functools.cached_property
    def io_table(self) -> PLCCompositionIOTable | None:
        if not self.io_sheets:
            return None
        table_path = self._args['io_table_path']
        if table_path:
            return PLCCompositionIOTable.load(table_path, self.io_sheets)
        for table in self.gdrive_tables:
            if PLCCompositionIOTable.is_name_valid(table):
                return PLCCompositionIOTable.from_gdrive(table, self.io_sheets)
        return None

    @functools.cached_property
    def visu_table(self) -> VisualizationTable | None:
        table_path = self._args['visu_table_path']
        if table_path:
            return VisualizationTable.load(table_path)
        for table in self.gdrive_tables:
            if VisualizationTable.is_name_valid(table):
                return VisualizationTable.from_gdrive(table)
        return None


def main() -> None:
    args = get_input_args()
    logging.basicConfig(
        level=args['log_level'],
        format='[%(name)s] %(levelname)s:%(message)s'
        )
    args_processor = InputArgsProcessor(args)
    data_processor = SystemConfigProcessor(
        system_name=args['system_name'],
        sw_table=args_processor.sw_table,
        io_table=args_processor.io_table,
        visu_table=args_processor.visu_table,
        g3core=args_processor.g3core
        )
    os.makedirs(args['output_path'], exist_ok=True)
    data_processor.to_file(
        dirpath=args['output_path'],
        filename='SystemConfig.json',
        update_if_exists=args['update']
        )
