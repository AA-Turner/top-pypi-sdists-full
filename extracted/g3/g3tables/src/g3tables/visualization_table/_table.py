import pandas as pd
import logging
import typing
import warnings

from ..utils.gdrive import get_table_data_from_gdrive


logger = logging.getLogger('g3tables.visualization_table')


DEVICE_TYPES = {
    "System": "System_G3",
    "SystemSafety": "SystemSafety_G3",
    "Zone": "Zone_G3",
    "Gate": "Gate_G3",
    "Route": "Route_G3",
    "Zone.Track": "Track",
    "Detector.TrackCircuit": "TC_G3",
    "Detector.Pantograph": "PD_G3",
    "Detector.MassDetector": "MD_G3",
    "Detector.UltrasonicSensor": "US_G3",
    "Detector.VirtualDetector": "VD_G3",
    "PointMachine.PME": "PME_G3",
    "PointMachine.PMM": "PMM_G3",
    "Signal": "Signal_G3",
    "Signal.Symbol": "SignalSymbol_G3",
    "DoorDisplay7": "DoorDisplay7_G3",
    "Requestor.Digital": "RequestorDigital",
    "Requestor.RoutingTable": "RoutingTable_G3",
    "Requestor.Vecom": "VecomController_G3",
    "Requestor.Vecom.Loop": "VecomLoop_G3",
    "Requestor.DRR": "DRRController_G3",
    "Requestor.DRR.Transceiver": "DRRTransceiver_G3",
    "Requestor.SPIE": "SPIEController_G3",
    "Requestor.SPIE.Loop": "SPIELoop_G3",
    "Requestor.Vetra": "Vetra_G3",
    "Requestor.AWA": "AWA_G3",
    "Cabinet": "Cabinet_G3",
    "Cabinet.UPS": "CabinetUps_G3",
    "Cabinet.RFID": "CabinetRFID_G3",
    "Cabinet.Fuse": "CabinetFuse_G3",
    "Cabinet.Convertor": "CabinetConvertor_G3",
    "Cabinet.MonitoringModule": "CabinetModule_G3",
    "Heating": "Heating_G3",
    "Heating.Contactor": "HeatingContactor_G3",
    "Heating.Contactor.Rod": "HeatingRod_G3",
    "Matrix": "MPS_G3",
    "GPIO": "GPIO_G3" 
}


class SHVVarDict(typing.TypedDict):
    name: str
    is_blacklisted: bool
    is_deleted: bool


class SHVProjectTypeDict(typing.TypedDict):
    type: str
    restricted_to: str | None
    vars: dict[str, SHVVarDict]
    type_variants: typing.NotRequired[dict[str, dict]]


GateTypeVariantTableDict: typing.TypeAlias = dict[str, tuple[list[str], int]]

HeatingTypeVariantTableDict: typing.TypeAlias = dict[str, list[str]]

RequestorTypeVariantTableDict: typing.TypeAlias = dict[str, list[str]]


class VisualizationTable:
    """
    `VisualizationTable` is a representation of the G3 Project Visualization
    table. It allows access to the data of the 'Parameters', 'Gate table',
    'Heating table', and 'Requestor table' sheets in the form of a
    `pandas.DataFrame` dictionary.

    Note that the "Title", "Identification", and "Worksheet explanation" sheets
    are not represented within the dictionary.
    """
    NAME_PATTERN_01 = 'project_hmi_visualization'
    NAME_PATTERN_02 = 'system_hmi_visualization'
    NAME_PATTERN_03 = 'hmi_visualization'
    """
    The pattern that the name of the SW Definition table must match to be
    automatically recognized in a Google Drive folder.
    """
    EXCLUDED_SHEETS = [
        'Title', 'Identification', 'Worksheet explanation', 'Users'
        ]
    """
    Sheets that are not represented in the data dictionary of
    a `SWDefinitionTable` instance.
    """

    def __init__(
        self,
        parameters_sheet_data: pd.DataFrame,
        gate_table_sheet_data: pd.DataFrame,
        heating_table_sheet_data: pd.DataFrame,
        requestor_table_sheet_data: pd.DataFrame
    ) -> None:
        """
        Standard initializer of a `VisualizationTable` instance. Although it
        can be used directly, alternative class constructors `from_local` and
        `from_gdrive` are adviced instead.

        Args:
            data (dict[str, pd.DataFrame]): a dict, where keys are\
            sheets names and values are the `pandas.DataFrame` objects\
            representing the sheet data.
        """
        self._params_data = parameters_sheet_data
        self._gate_data = gate_table_sheet_data
        self._heating_data = heating_table_sheet_data
        self._req_data = requestor_table_sheet_data

    @classmethod
    def is_name_valid(cls, name: str) -> bool:
        """
        Check if the provided name matches the Visualization table
        name pattern.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        name_formatted = name.strip().replace(' ', '_').casefold()
        return ( (cls.NAME_PATTERN_01 in name_formatted) or (cls.NAME_PATTERN_02 in name_formatted) or (cls.NAME_PATTERN_03 in name_formatted) )

    @classmethod
    def from_local(cls, path: str) -> typing.Self:
        """
        Create a `VisualizationTable` instance from a local Excel file.

        Args:
            local_path (str): The local file path to the Excel file containing\
                the Visualization table data.

        Returns:
            Self: An instance of `VisualizationTable` initialized\
                with data from the specified local Excel file.
        """
        logger.info('Reading Visualization table from local path: %s', path)
        xls = pd.ExcelFile(path)
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=UserWarning)
            parameters_sheet = pd.read_excel(
                xls, header=2, sheet_name='Parameters'
                )
            gate_table_sheet = pd.read_excel(
                xls, header=2, sheet_name='Gate table'
                )
            heating_table_sheet = pd.read_excel(
                xls, header=2, sheet_name='Heating table'
                )
            requestor_table_sheet = pd.read_excel(
                xls, header=2, sheet_name='Requestor table'
                )
        params_formatter = VisualizationTableFormatter.format_params_sheet
        table_formatter = VisualizationTableFormatter.format_table_sheet
        return cls(
            parameters_sheet_data=params_formatter(parameters_sheet),
            gate_table_sheet_data=table_formatter(gate_table_sheet),
            heating_table_sheet_data=table_formatter(heating_table_sheet),
            requestor_table_sheet_data=table_formatter(requestor_table_sheet),
            )

    @classmethod
    def from_gdrive(cls, gdrive_table_name: str) -> typing.Self:
        """
        Create a `VisualizationTable` instance from a Google Drive file.

        Args:
            gdrive_table_name (str): The name of the table in Google Drive\
                containing the Visualization table.

        Returns:
            SWDefinitionTable: An instance of `VisualizationTable` initialized\
                with data from the specified Google Drive file.
        """
        logger.info(
            'Reading Visualization table from Google Drive: %s',
            gdrive_table_name
            )
        sheets_all = get_table_data_from_gdrive(
            gdrive_table_name, header_row=3, exclude_sheets=cls.EXCLUDED_SHEETS
            )
        parameters_sheet = sheets_all['Parameters']
        gate_table_sheet = sheets_all['Gate table']
        heating_table_sheet = sheets_all['Heating table']
        requestor_table_sheet = sheets_all['Requestor table']
        params_formatter = VisualizationTableFormatter.format_params_sheet
        table_formatter = VisualizationTableFormatter.format_table_sheet
        return cls(
            parameters_sheet_data=params_formatter(parameters_sheet),
            gate_table_sheet_data=table_formatter(gate_table_sheet),
            heating_table_sheet_data=table_formatter(heating_table_sheet),
            requestor_table_sheet_data=table_formatter(requestor_table_sheet),
            )

    @classmethod
    def load(cls, path: str) -> typing.Self:
        """
        Load a Visualization table from a local file or Google Drive.

        Args:
            path (str): Path to the Visualization table file. If the path ends\
                with '.xlsx', the table is loaded from a local file.\
                Otherwise, the table is loaded from Google Drive.

        Returns:
            typing.Self: An instance of `VisualizationTable` initialized with\
                data from the specified file.
        """
        if path.endswith('.xlsx'):
            return cls.from_local(path)
        return cls.from_gdrive(path)

    @property
    def params_data(self) -> pd.DataFrame:
        """'Parameters' sheet data of the Visualization table."""
        return self._params_data

    @property
    def gate_table_data(self) -> pd.DataFrame:
        """'Gate table' sheet data of the Visualization table."""
        return self._gate_data

    @property
    def heating_table_data(self) -> pd.DataFrame:
        """'Heating table' sheet data of the Visualization table."""
        return self._heating_data

    @property
    def requestor_table_data(self) -> pd.DataFrame:
        """'Requestor table' sheet data of the Visualization table."""
        return self._req_data

    @staticmethod
    def _new_shv_project_type_dict(
        module_type: str, restricted_to: str | None
    ) -> SHVProjectTypeDict:
        return {
            'type': module_type,
            'restricted_to': restricted_to,
            'vars': {}
            }

    @staticmethod
    def _new_shv_var_dict(
        shv_var_name: str, is_blacklisted: bool, is_deleted: bool
    ) -> SHVVarDict:
        return {
            'name': shv_var_name,
            'is_blacklisted': is_blacklisted,
            'is_deleted': is_deleted
            }

    @property
    def project_types(self) -> dict[str, SHVProjectTypeDict]:
        """Dictionary of project types and their SHV variables."""
        project_types: dict[str, SHVProjectTypeDict] = {}
        for _, row in self._params_data.iterrows():
            # create or fetch existing project_type_data dictionary
            project_type = row['Project type']
            project_subtype = row['Project subtype']
            if project_subtype:
                module_type, restricted_to = project_subtype, project_type
            else:
                module_type, restricted_to = project_type, None
            project_type_data = project_types.setdefault(
                module_type,
                self._new_shv_project_type_dict(module_type, restricted_to)
                )
            # create shv variable data dictionary
            if not (shv_var := row['SHV variable']):
                continue
            project_type_data['vars'][shv_var] = self._new_shv_var_dict(
                shv_var_name=shv_var,
                is_blacklisted=row['Available only in SHVspy'],
                is_deleted=row['x']
                )
        return project_types

    def _get_table_data(
        self, data: pd.DataFrame, start_idx: int
    ) -> dict[str, dict]:
        columns = VisualizationTableFormatter.get_sorted_columns(
            table_data=data.iloc[:, start_idx:]
            )
        tables: dict[str, dict] = {}
        i = 0
        for _, row in data.iterrows():
            type_ = row['Project type']
            type_variant = row['SHV visu type variant'] or 'default'
            table = {type_variant: columns[int(i)]}
            tables.setdefault(type_, {}).update(table)
            i += 1
        return tables

    @property
    def gate_tables(self) -> dict[str, GateTypeVariantTableDict]:
        """Dictionary of gate tables and their columns."""
        tables = self._get_table_data(self._gate_data, start_idx=4)
        for _, row in self._gate_data.iterrows():
            type_ = row['Project type']
            type_variant = row['SHV visu type variant'] or 'default'
            row_count = int(row['Row count'])
            columns = tables[type_][type_variant]
            tables[type_][type_variant] = (columns, row_count)
        return tables

    @property
    def heating_tables(self) -> dict[str, HeatingTypeVariantTableDict]:
        """Dictionary of heating tables and their columns."""
        return self._get_table_data(self._heating_data, start_idx=3)

    @property
    def requestor_tables(self) -> dict[str, RequestorTypeVariantTableDict]:
        """Dictionary of requestor tables and their columns."""
        return self._get_table_data(self._req_data, start_idx=3)


class VisualizationTableFormatter:

    @staticmethod
    def fill_in_device_types(device):
        if device in DEVICE_TYPES:
            return DEVICE_TYPES[device]
        logger.warning(
            f'Could not retrieve SHV Device type for module "{device}".'
            )
        return ''

    @staticmethod
    def format_params_sheet(params_sheet: pd.DataFrame) -> pd.DataFrame:
        # drop rows where the 'Module (device)' column value is empty
        params_sheet = params_sheet.fillna('').astype(str, copy=True)
        params_sheet_mask = (params_sheet['Module (device)'] != '')
        params_sheet = params_sheet[params_sheet_mask]
        # create the 'Project type' column
        formatter = VisualizationTableFormatter.fill_in_device_types
        params_sheet.insert(
            loc=1,
            column='Project type',
            value=params_sheet['Module (device)'].apply(formatter)
            )
        # format the 'x' column to bool
        params_sheet.loc[:, 'x'] = params_sheet['x'].apply(
            lambda cell_val: bool(cell_val)
        )
        # format the 'Available only in SHVspy' column to bool
        col_name = 'Available only in SHVspy'
        params_sheet.loc[:, col_name] = params_sheet[col_name].apply(
            lambda cell_val: cell_val == 'TRUE'
        )
        return params_sheet

    @staticmethod
    def format_table_sheet(table_sheet: pd.DataFrame) -> pd.DataFrame:
        # drop rows where the 'Module (device)' column value is empty
        table_sheet = table_sheet.fillna('').astype(str, copy=True)
        empty_module_mask = table_sheet['Module (device)'].str.fullmatch('')
        table_sheet = table_sheet[~empty_module_mask]
        # create the 'Project type' column
        formatter = VisualizationTableFormatter.fill_in_device_types
        table_sheet.insert(
            loc=0,
            column='Project type',
            value=table_sheet['Module (device)'].apply(formatter)
            )
        return table_sheet

    @staticmethod
    def get_sorted_columns(table_data: pd.DataFrame) -> list[list[str]]:

        def sort_columns_by_row_values(row):
            sorted_values = sorted(
                [
                    (col, val) for col, val in row.items()
                    if val and int(val) != 0
                ],
                key=lambda x: x[1]
                )
            return [col for col, _ in sorted_values]

        data_sorted = table_data.apply(sort_columns_by_row_values, axis=1)
        return data_sorted.values.tolist()
