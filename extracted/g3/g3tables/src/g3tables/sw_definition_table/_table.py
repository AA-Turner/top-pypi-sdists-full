import pandas as pd
import logging
import re
import typing
import warnings

from unidecode import unidecode

from ..utils import Interval, to_nested_dict
from ..utils.gdrive import get_table_data_from_gdrive


logger = logging.getLogger('g3tables.sw_definition_table')


class SWDefinitionTable:
    """
    `SWDefinitionTable` is a representation of the G3 Project SW Defintion
    table. It allows access to the data of the 'Common' sheet and software zone
    configuration sheets in the form of a `pandas.DataFrame` dictionary.

    Note that the "Title", "Identification", and "Worksheet explanation" sheets
    are not represented within  the dictionary.
    """
    NAME_PATTERN_01 = 'project_sw_definition'
    NAME_PATTERN_02 = 'system_sw_definition'
    NAME_PATTERN_03 = 'sw_definition'
    """
    The pattern that the name of the SW Definition table must match to be
    automatically recognized in a Google Drive folder.
    """
    EXCLUDED_SHEETS = ['Title', 'Identification', 'Worksheet explanation']
    """
    Sheets that are not represented in the data dictionary of
    a `SWDefinitionTable` instance.
    """

    def __init__(self, data: dict[str, pd.DataFrame]) -> None:
        """
        Standard initializer of a `SWDefinitionTable` instance. Although it
        can be used directly, alternative class constructors `from_local` and
        `from_gdrive` are adviced instead.

        Args:
            data (dict[str, pd.DataFrame]): a dict, where keys are\
            sheets names and values are the `pandas.DataFrame` objects\
            representing the sheet data.
        """
        self._data = data

    @classmethod
    def is_name_valid(cls, name: str) -> bool:
        """
        Check if the provided name matches the SW Definition table
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
        Create a `SWDefinitionTable` instance from a local Excel file.

        Args:
            local_path (str): The local file path to the Excel file containing\
                the SW Definition table.

        Returns:
            Self: An instance of `SWDefinitionTable` initialized\
                with data from the specified local Excel file.
        """
        logger.info('Reading SW Definition table from local path: %s', path)
        formatter = SWDefinitionSheetFormatter
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            sheets_all = pd.read_excel(path, sheet_name=None)
            sheets = formatter.remove_excluded_sheets(sheets_all)
        for sheet_name, sheet_data in sheets.items():
            sheets[sheet_name] = formatter.process_sheet_init(sheet_data)
        return cls(sheets)

    @classmethod
    def from_gdrive(cls, gdrive_table_name: str) -> typing.Self:
        """
        Create a `SWDefinitionTable` instance from a Google Drive file.

        Args:
            gdrive_table_name (str): The name of the table in Google Drive\
                containing the SW Definition table.

        Returns:
            SWDefinitionTable: An instance of `SWDefinitionTable` initialized\
                with data from the specified Google Drive file.
        """
        logger.info(
            'Reading SW Definition table from Google Drive: %s',
            gdrive_table_name
            )
        sheets_all = get_table_data_from_gdrive(
            gdrive_table_name,
            exclude_sheets=cls.EXCLUDED_SHEETS
            )
        formatter = SWDefinitionSheetFormatter
        sheets = formatter.remove_excluded_sheets(sheets_all)  # type: ignore
        for sheet_name, sheet_data in sheets.items():
            sheets[sheet_name] = formatter.process_sheet_init(sheet_data)
        return cls(sheets)

    @classmethod
    def load(cls, path: str) -> typing.Self:
        """
        Load a SW Definition table from a local file or Google Drive.

        Args:
            path (str): Path to the SW Definition table file. If the path ends\
                with '.xlsx', the table is loaded from a local file.\
                Otherwise, the table is loaded from Google Drive.

        Returns:
            typing.Self: An instance of `SWDefinitionTable` initialized with\
                data from the specified file.
        """
        if path.endswith('.xlsx'):
            return cls.from_local(path)
        return cls.from_gdrive(path)

    @property
    def sheet_names(self) -> list[str]:
        """Names of the sheets contained within the SW Definition table."""
        return [name for name in self._data.keys()]

    def get_sheet_data(self, sheet_name: str) -> pd.DataFrame:
        """
        Retrieves data for a specific sheet.

        Args:
            sheet_name (str): The name of the sheet to retrieve.

        Returns:
            pd.DataFrame: The data associated with the sheet.

        Raises:
            KeyError: If the specified sheet is not found in the data.
        """
        try:
            return self._data[sheet_name]
        except KeyError as err:
            err.add_note('Sheet was not found')
            raise err

    def get_system_sheets(self, system_name: str) -> dict[str, pd.DataFrame]:
        """
        Gets the sheets' data associated with a given system name. Note that
        the system name is not validated.

        Args:
            system_name (str): The name of the system for which to retrieve\
                sheets.

        Returns:
            dict[str, pd.DataFrame]: A dictionary of sheets belonging to\
                the given system.
        """
        sheets = {}
        for sheet_name, sheet_data in self._data.items():
            if sheet_name != 'Common':
                system_connector = self.get_connected_system(sheet_name)
                if system_connector != system_name:
                    continue
            sheets[sheet_name] = sheet_data
        if len(sheets) < 2:
            logger.error(
                'No zone sheets were found for system "%s". Aborting',
                system_name
                )
            exit(1)
        return sheets

    def get_connected_devices(
        self, zone_name: str, connector: str
    ) -> list[str]:
        """
        Retrieve connected device names based on the zone name and the type of
        connector. For instance, `get_connected_devices('Z01', 'gate')` returns
        a list of gate devices, which are connected to any other device via
        "control/connector/gate".

        Args:
            zone_name (str): Name of the zone sheet to look up.
            connector (str): Type of connector to find (gate, cabinet, etc.).

        Returns:
            list[str]: List of connected devices found.
        """
        logger.debug(
            'Getting connected device names for zone "%s" and connector '
            '"control/connector/%s"', zone_name, connector
            )
        zone_data = self.get_sheet_data(zone_name)
        conn_rows = zone_data.xs(f'control/connector/{connector}', level='Key')
        values = []
        column_index = 1
        while True:
            if column_index not in zone_data:
                break
            column_values = conn_rows[column_index]
            for cell_value in column_values.to_list():
                if not cell_value:
                    continue
                if cell_value not in values:
                    values.append(cell_value)
            column_index += 1
        return values

    def get_connected_system(self, zone_name: str) -> str:
        """
        Get the name of the system to which the specified zone belonds to.

        Args:
            zone_name (str): Name of the zone to query for system connector.

        Returns:
            str: The connected system connector.

        Raises:
            AttributeError: If no system connector is found or
            if it's ambiguous.
        """
        system_connector = self.get_connected_devices(zone_name, 'system')
        logger.debug(
            'Retrieved the system connector "%s" for zone "%s".',
            system_connector, zone_name
            )
        if not system_connector:
            raise AttributeError(
                f'Sheet "{zone_name}" does not have a system connector.'
                )
        if len(system_connector) > 1:
            connectors = ", ".join(system_connector)
            raise AttributeError(
                f'Sheet "{zone_name}" system connector is ambiguous '
                f'({len(system_connector)} connectors found: {connectors}).'
                )
        return system_connector[-1]

    def get_connected_commfunc_brc(self, zone_name: str) -> str | None:
        """
        Get the name of the BRC comm function connector if a TrackCircuit
        detector is present in the specified zone. If no TrackCircuit detector
        is found, the method returns None.

        Args:
            zone_name (str): Name of the zone to query for\
                the BRC comm function.

        Returns:
            str | None: The name of the BRC comm function connector if a\
                TrackCircuit detector is present, otherwise None.
        """
        logger.debug(
            'Looking for a BRC comm function within the "Common" sheet.'
            )
        common_data = self.get_sheet_data('Common')
        commfunc_row = common_data.loc[('CommFunction', 'general/name'), 1:]
        commfunc_brc = None
        column_index = 1
        while True:
            if column_index not in commfunc_row:
                break
            cell_value = commfunc_row[column_index]
            if cell_value and 'brc' in str(cell_value).lower():
                commfunc_brc = cell_value
                break
            column_index += 1
        if not commfunc_brc:
            logger.debug(
                'No BRC comm function was found within the "Common" sheet.'
                )
            return None
        assert isinstance(commfunc_brc, str)
        logger.debug('Found a BRC comm function within the "Common" sheet.')
        logger.debug(
            'Looking for a TrackCircuit detector within zone "%s".', zone_name
            )
        zone_data = self.get_sheet_data(zone_name)
        detector_type_row = zone_data.loc[('Detector', 'general/type'), 1:].squeeze()
        assert isinstance(detector_type_row, pd.Series)
        column_index = 1
        while True:
            if column_index not in detector_type_row:
                break
            cell_value = detector_type_row[column_index]
            assert isinstance(cell_value, str)
            if not cell_value:
                break
            if cell_value.lower() == 'trackcircuit':
                logger.debug(
                    'Found a TrackCircuit detector within zone "%s".',
                    zone_name
                    )
                return commfunc_brc
            column_index += 1
        logger.debug(
            'No TrackCircuit detector was found within zone "%s".', zone_name
            )
        return None

    def get_connected_commfuncs(self, zone_name: str) -> list[str]:
        """
        Get the names of the communication function block instances
        which are utilized within the specified zone.

        Args:
            zone_name (str): Name of the zone to query.

        Returns:
            list[str]: List of communication function connectors.
        """
        # get comm func connectors that are represented in the Zone sheets
        logger.debug(
            'Retrieving the comm function connectors for zone "%s".', zone_name
            )
        commfunc_connectors = self.get_connected_devices(zone_name, 'comm')
        logger.debug(
            'Retrieved the comm function connectors "%s" for zone "%s".',
            commfunc_connectors, zone_name
            )
        # evaluate whether to add the 'CommBRC' connector
        logger.debug(
            'Evaluating whether to add a BRC comm function connector '
            'for zone "%s".', zone_name
            )
        commfunc_brc = self.get_connected_commfunc_brc(zone_name)
        if commfunc_brc:
            logger.debug(
                'Adding the "%s" BRC comm function connector to the comm '
                'function connectors for zone "%s".', commfunc_brc, zone_name
                )
            commfunc_connectors.append(commfunc_brc)
        else:
            logger.debug(
                'No BRC comm function connector is added to the comm '
                'function connectors for zone "%s".', zone_name
                )
        return commfunc_connectors

    def get_cabinet_names(self, zone_name: str) -> list[str]:
        """
        Retrieve the names of cabinets present in the specified zone.

        Args:
            zone_name (str): Name of the zone to query for cabinet names.

        Returns:
            list[str]: List of the found cabinet names.
        """
        logger.debug('Retrieving cabinet names for zone "%s".', zone_name)
        zone_data = self.get_sheet_data(zone_name)
        conn_row = zone_data.loc[('Cabinet', 'general/name'), 1:].squeeze()
        assert isinstance(conn_row, pd.Series)
        values: list[str] = []
        column_index = 1
        while True:
            if column_index not in zone_data:
                break
            cell_value = conn_row[column_index]
            assert isinstance(cell_value, str)
            if cell_value and (cell_value not in values):
                values.append(cell_value)
            column_index += 1
        logger.debug(
            'Retrieved cabinet names "%s" for zone "%s"', values, zone_name
            )
        return values

    def to_dict(self, system_name: str) -> dict[str, dict]:
        """
        Converts the system sheets' data to a pure tree-like dictionary
        representation.

        Args:
            system_name (str): The name of the system for which to generate\
                the dictionary.

        Returns:
            dict[str, dict]: The dictionary representation of the system's\
                sheets' data.
        """
        # get unprocessed system sheets related to the system
        sheets = self.get_system_sheets(system_name)
        # process zone sheets and gather connected comm functions
        zone_sheets_converted: dict[str, dict] = {}
        commfunc_names = []
        for sheet_name, sheet_data in sheets.items():
            if sheet_name == 'Common':
                continue
            converter = SWDefinitionSheetToNestedDictConverter(sheet_data)
            commfunc_names.extend(self.get_connected_commfuncs(sheet_name))
            zone_sheets_converted[sheet_name] = converter.to_dict()
        # process the 'Common' sheet
        commom_data = sheets['Common']
        converter = SWDefinitionCommonSheetToNestedDictConverter(commom_data)
        common_sheet_converted = {
            'Common': converter.to_dict_common(system_name, commfunc_names)
            }
        # update the dict with the process 'Common' sheets with the processed
        # zone sheets (this way, the 'Common' key appears first in the dict)
        common_sheet_converted.update(zone_sheets_converted)
        # expand all the remaining slash-separated keys
        # to create a true nested dict structure
        nested = to_nested_dict(common_sheet_converted, keysep='/')
        # update the varnames of child devices
        SWDefinitionSheetFormatter.update_varnames(nested)
        return nested


class SWDefinitionSheetFormatter:
    """
    Utility class to format and process sheets from SWDefinitionTable.
    It provides methods for formatting keys, modules, and device names.
    """

    @classmethod
    def remove_excluded_sheets(
        cls, sheets: dict[str | int, pd.DataFrame]
    ) -> dict[str, pd.DataFrame]:
        """
        Removes sheets that are listed in `SWDefinitionTable`'s
        `EXCLUDED_SHEETS` from the input dictionary of sheets.

        Args:
            sheets (dict[str | int, pd.DataFrame]): The original dictionary
            containing all sheets.

        Returns:
            dict[str, pd.DataFrame]: A filtered dictionary containing only the
            sheets that are not in `EXCLUDED_SHEETS`.
        """
        excluded = SWDefinitionTable.EXCLUDED_SHEETS
        excluded_str = ", ".join(f"'{sheet}'" for sheet in excluded)
        logger.debug('Removing SW Defintion table sheets "%s".', excluded_str)
        return {
            str(sheet_name): sheet_data for
            sheet_name, sheet_data in sheets.items()
            if sheet_name not in excluded
            }

    @staticmethod
    def format_module_key(key: str) -> str:
        """
        Converts CamelCase, replaces all non-alphanumeric characters with
        underscores, removes leading/trailing underscores, and reduces multiple
        underscores to a single underscore.

        Args:
            key (str): The string to be sanitized.

        Returns:
            str: The sanitized string, transformed to lowercase and with all
            non-alphanumeric characters replaced with underscores.
        """
        # replace CamelCase words with underscore-separated words
        sanitized_key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key)
        # replace any non-alphanumeric character with an underscore
        sanitized_key = re.sub(r'[^a-z0-9_]', '_', key.lower())
        # remove leading/trailing underscores
        sanitized_key = sanitized_key.strip('_')
        # replace multiple underscores with a single underscore
        sanitized_key = re.sub('_+', '_', sanitized_key)
        # add 'general' prefix to the formatted key
        sanitized_key = f'general/{sanitized_key}'
        return sanitized_key

    @staticmethod
    def format_module_name(module_name: str) -> tuple[str, str]:
        """
        Split the module name into metamodule and module parts.

        Args:
            module_name (str): The original module name.

        Returns:
            tuple[str, str]: The metamodule and module parts of the name.
        """
        if ':' not in module_name:  # No metamodule present
            if '.' in module_name:
                metamodule = ':'.join(module_name.split('.'))
            elif '/' in module_name:
                metamodule = ':'.join(module_name.split('/'))
            else:
                metamodule = module_name
            return metamodule, module_name
        parts = module_name.split(':')
        return ':'.join(parts[:-1]), parts[-1]

    @staticmethod
    def format_module_separator(module: str) -> str:
        """
        Replace '.' with '/' in module names.

        Args:
            module (str): Original module name.

        Returns:
            str: Module name with '/' instead of '.'.
        """
        formatted = module.replace('.', '/')
        logger.debug('Formatting module name: "%s" -> "%s"', module, formatted)
        return formatted

    @classmethod
    def _format_device_names(cls, sheet: pd.DataFrame) -> pd.DataFrame:
        """
        Helper method for the `process_sheet` method to format names and
        connectors in the device data columns.

        Args:
            sheet (pd.DataFrame): The sheet DataFrame being processed.

        Returns:
            pd.DataFrame: The updated sheet DataFrame with
            formatted names and connectors.
        """
        name_key = 'general/name'
        conn_key = 'control/connector/'
        name_mask = sheet.index.get_level_values('Key') == name_key
        conn_mask = sheet.index.get_level_values('Key').str.contains(conn_key)
        column_index = 1
        while True:
            if column_index not in sheet:
                break
            name_column = sheet.loc[name_mask, column_index]
            conn_column = sheet.loc[conn_mask, column_index]
            sheet.loc[name_mask, column_index] = name_column.apply(
                cls.format_device_name)
            sheet.loc[conn_mask, column_index] = conn_column.apply(
                cls.format_device_connector)
            column_index += 1
        return sheet

    @classmethod
    def process_sheet_init(cls, sheet: pd.DataFrame) -> pd.DataFrame:
        """
        Process a DataFrame representing a sheet, dropping irrelevant data
        and formatting columns and cells.

        Args:
            sheet (pd.DataFrame): The original sheet DataFrame.

        Returns:
            pd.DataFrame: The processed sheet DataFrame.
        """
        logger.debug("Processing sheet data.")
        sheet = sheet.copy()
        # drop empty columns ...
        logger.debug("Dropping empty columns.")
        # ... where all cells are NaN
        sheet.dropna(axis='columns', how='all', inplace=True)
        # ... and where all cells are empty string values
        empty_cols = (sheet == '').all()
        sheet = sheet.drop(columns=empty_cols[empty_cols].index)
        # drop rows where either 'Key' or 'Parameter' values are empty
        logger.debug(
            "Dropping rows where both 'Key' and 'Parameter' values are empty.")
        sheet.dropna(subset=['Key', 'Parameter'], how='all', inplace=True)
        mask = (sheet['Key'] == '') & (sheet['Parameter'] == '')
        sheet = sheet[~mask]
        # format column name to int (if applicable) to maintain consistency
        logger.debug("Converting column names to integer type if applicable.")
        sheet.rename(
            columns=lambda col: int(col) if str(col).isnumeric() else col,
            inplace=True
            )
        # fill in all empty cells' values with an emplty string
        logger.debug("Filling empty cells with empty string value ('').")
        sheet = sheet.fillna('')
        # format sheet values to string to maintain consistency
        sheet = sheet.applymap(lambda cell: str(cell).strip())
        # change 'Module' values separator to '/', creare 'Metamodule' column
        logger.debug("Formatting 'Module' column values.")
        sheet[['Metamodule', 'Module']] = sheet['Module'].apply(
            lambda x: cls.format_module_name(x)).to_list()
        sheet['Module'] = sheet['Module'].apply(cls.format_module_separator)
        # split multikeys (values is 'Key' with a comma) to multiple rows
        sep = r'\s*,\s*'
        sheet = sheet.assign(Key=sheet['Key'].str.split(sep)).explode('Key')
        # substitute missing 'Key' values from the 'Parameter' values
        logger.debug(
            "Substituting missing 'Key' values from the 'Parameter' column.")
        subs_keys = sheet['Parameter'].apply(cls.format_module_key)
        sheet['Key'] = sheet['Key'].fillna(subs_keys)
        mask = sheet['Key'] == ''
        sheet.loc[mask, 'Key'] = subs_keys[mask]
        # set multiindex to 'Module' + 'Key' columns
        logger.debug("Setting multiindex to ['Module', 'Key'].")
        sheet = sheet.set_index(['Module', 'Key'])
        sheet = sheet.sort_index()
        return sheet

    @classmethod
    def process_sheet_dict_conv(cls, sheet: pd.DataFrame) -> pd.DataFrame:
        """
        Process a DataFrame representing a sheet, dropping irrelevant data
        and formatting columns and cells.

        Args:
            sheet (pd.DataFrame): The original sheet DataFrame.

        Returns:
            pd.DataFrame: The processed sheet DataFrame.
        """
        sheet = sheet.copy()
        # format "name" and "connector" the values in the device columns
        # to exclude non-alphanumerical values
        logger.debug("Formatting device names and connectors.")
        sheet = cls._format_device_names(sheet)
        # drop columns with irrelevant data
        logger.debug(
            "Dropping 'Parameter', 'Role', and 'Description' columns.")
        sheet.drop(columns=['Parameter', 'Role', 'Description'], inplace=True)
        logger.debug("Removing rows with 'notes' in the 'Key' column.")
        mask = sheet.index.get_level_values('Key').str.contains('notes')
        sheet = sheet[~mask]
        # replace 'yes' and 'no' with corresponding boolean values
        logger.debug("Converting 'yes' and 'no' values to boolean.")
        sheet = sheet.replace(['YES', 'Yes', 'yes'], True)
        sheet = sheet.replace(['NO', 'No', 'no'], False)
        return sheet

    @staticmethod
    def format_device_name(name: str, log: bool = True) -> str:
        """
        Process a string by removing all non-alphanumeric characters from
        the entire string (whitespaces and hyphens are replaced with
        underscores).

        Example:
        >>> process_string("1TC-21 *Var1")
        "1TC_21_Var1"

        Args:
            name (str): The input string to process.

        Returns:
            str: The processed string.
        """
        # Convert non-ASCII letters to their ASCII variants
        formatted = unidecode(name)
        # Replace all non-alphanumeric characters with underscores
        formatted = re.sub(r'[^a-zA-Z0-9]', '_', formatted)
        # Replace consecutive underscores with a single one
        formatted = re.sub(r'__+', '_', formatted)
        if formatted != name and log:
            logger.debug('Updated device name: "%s" -> "%s"', name, formatted)
        return formatted

    @classmethod
    def format_device_varname(cls, varname: str, log: bool = True) -> str:
        """
        Transform a variable name by moving leading digits to the end, 
        replacing non-alphanumeric characters, and standardizing the format.

        Example:
            >>> format_device_varname("3G01")
            "G01_3"

        Args:
            varname (str): The input string to process.

        Returns:
            str: The processed string.
        """
        match = re.match(r'^(\d+)(.*)', varname)
        if match:
            digits, rest = match.groups()
        else:
            digits, rest = '', varname

        cleaned = cls.format_device_name(rest, log=False)

        if digits:
            formatted = f"{cleaned}_{digits}"
        else:
            formatted = cleaned

        if formatted != varname and log:
            logger.debug('Updated device varname: "%s" -> "%s"', varname, formatted)

        return formatted

    @classmethod
    def _update_varnames(
        cls, device_data: dict[str, dict], parent_varname: str = ''
    ) -> None:
        varname_old = device_data.get('general', {}).get('varname')
        if varname_old is None:
            # continue
            return
        if parent_varname:
            varname_new = f'{parent_varname}_{varname_old}'
            device_data['general']['varname'] = varname_new
            logger.debug(
                'Updated device varname: "%s" -> "%s"',
                varname_old, varname_new
                )
        else:
            varname_new = varname_old
        children = device_data.get('children')
        if children:
            for child_module in children.values():
                for child_device in child_module.values():
                    cls._update_varnames(child_device, varname_new)

    @classmethod
    def update_varnames(cls, nested_structure: dict[str, dict]) -> None:
        """
        Update the variable names in the nested structure by appending
        their parent varnames.

        Args:
            nested_structure (dict[str, dict]): The original nested dictionary
            structure.
        """
        special_varnames = {
            "Zone": "Zone",
            "System": "System",
            "SystemSafety": "SystemSafety"
            }
        logger.debug("Updating varnames in the nested structure.")
        for zone_name, zone_data in nested_structure.items():
            for module_name, module_data in zone_data.items():
                for device_data in module_data.values():
                    if module_name in special_varnames:
                        varname = special_varnames[module_name]
                        device_data['general']['varname'] = varname
                    else:
                        cls._update_varnames(device_data)
        logger.debug("Finished updating varnames in the nested structure.")

    @staticmethod
    def format_device_connector(connector: str, log: bool = True) -> str:
        """
        Process a string interval by removing all non-alphanumeric characters
        from each interval item (whitespaces and hyphens are replaced with
        underscores).

        Example:
        >>> format_device_connector("1TC-21 *Var1, 1TC-21 *Var2")
        "1TC_21_Var1, 1TC_21_Var1"

        Args:
            connector (str): The input string interval to process.

        Returns:
            str: The processed string interval.
        """
        try:
            interval = Interval(connector)
        except TypeError as err:
            logger.warning(
                'Could not split a connector to the parent device names "%s" '
                '(%s). The connector will be treated as a single device.',
                connector, str(err)
                )
            return SWDefinitionSheetFormatter.format_device_name(connector)
        formatted = ", ".join(
            SWDefinitionSheetFormatter.format_device_name(i) for i in interval
            )
        if formatted != connector and log:
            logger.debug(
                'Updated device connectors: "%s" -> "%s"', connector, formatted
                )
        return formatted


class SWDefinitionModule:
    """
    `SWDefinitionModule` provides utility methods for extracting data regarding
    a SW Defintion table module based on various conditions and rules (for
    instance, parent module names and connectors).

    Attributes:
        name_last (str): The last part of the full module name.
        name_full (str): The full hierarchical name of the module.
        parent_name_last (str): The last part of the full parent module name.
        parent_name_full (str): The full hierarchical name of the parent
        module.
        parent_connector (str): The connector associated with the parent
        module.
    """

    def __init__(self, module_name: str) -> None:
        """
        Initialize the SWDefinitionModule object.

        Args:
            module_name (str): The full name of the module, e.g. Signal/Symbol.
        """
        self.name_full = module_name
        self.name_last = module_name.split('/').pop()
        self.parent_name_full, self.parent_name_last = (
            self._get_parent_module_name(module_name)
            )
        self.parent_connector = (
            self.get_connector_key_for_module(self.parent_name_last)
            )

    @staticmethod
    def _get_parent_module_name(module_name: str) -> tuple[str, str]:
        """
        Internal default method to extract parent module names.

        Args:
            module_name (str): The name of the module.

        Returns:
            tuple[str, str]: The full and the last name of the parent module.
        """
        if '/' not in module_name:  # filter out devices with no parent
            return '', ''
        module_split = module_name.split('/')
        parent_module_name_full = "/".join(module_split[:-1])
        parent_module_name_last = module_split[-2]
        return parent_module_name_full, parent_module_name_last

    @classmethod
    def get_connector_key_for_module(cls, connected_module_name: str) -> str:
        """
        Generate the connector key string for the connected module. For
        example, for `connected_module_name="Gate"`, the return value is
        `'control/connector/gate'`.

        Args:
            connected_module_name (str): The name of the connected module.

        Returns:
            str: The connector key string.
        """
        if not connected_module_name:
            return ''
        if 'controller' in connected_module_name.lower():
            return 'control/connector/controller'
        return f'control/connector/{connected_module_name.lower()}'


class SWDefinitionDevice:
    """
    `SWDefinitionDevice` provides utility methods for extracting and
    manipulating data from a SW Definition device.

    Attributes:
        data (dict[str, typing.Any | dict]): The dictionary containing all
        relevant device data.
    """
    def __init__(self, device_data: dict[str, typing.Any | dict]) -> None:
        """
        Initialize the SWDefinitionDevice object with provided device data.

        Args:
            device_data (dict[str, typing.Any | dict]): The data dictionary
            containing device information.
        """
        self.data = device_data

    def get_device_name(self) -> str:
        """
        Get the device name based on available keys.

        Returns:
            str: The name of the device.

        Raises:
            KeyError: If no suitable key is found in the data dictionary.
        """
        try:
            name = self.data['general/name']
            assert isinstance(name, str)
            return name
        except KeyError as err:
            err.add_note('Device name was not found.')
            raise err


class SWDefinitionSheetToNestedDictConverter:
    """
    `SWDefinitionSheetToNestedDictConverter` is responsible for converting
    a given software definition sheet, which is in the `DataFrame` format,
    into a nested dictionary structure.
    """
    def __init__(self, sheet_data: pd.DataFrame) -> None:
        """
        Initialize the SWDefinitionSheetToNestedDictConverter object with
        the sheet data.

        Args:
            sheet_data (pd.DataFrame): The software definition sheet data.
        """
        self.data = sheet_data

    def preprocess_sheet_data(self) -> None:
        """
        Preprocess the sheet data to make it suitable for conversion into
        a nested dictionary.

        This method makes a copy of the original DataFrame stored in
        the `data` attribute, processes it using the
        the `SWDefinitionSheetFormatter.process_sheet_dict_conv` method,
        and updates the `data` attribute with the processed data.
        This preprocessing step is necessary before initializing devices and
        constructing the nested dictionary.
        """
        data = SWDefinitionSheetFormatter.process_sheet_dict_conv(self.data)
        self.data = data

    def init_devices_in_column(
        self, column_data: pd.Series
    ) -> dict[str, SWDefinitionDevice]:
        """
        Initialize devices in a given column of a DataFrame.

        This method processes a column from the whole sheet DataFrame
        to create a dictionary of SWDefinitionDevice objects. Note that
        the column data is indexed by a multiindex of the module name and
        the key as a result of preprocessing with `preprocess_sheet_data`.

        It is assumed that one column of the sheet DataFrame contains zero or
        one device data, so the created dictionary is one-to-one mapping of
        the module name keys to SWDefinitionDevice objects.

        Args:
            column_data (pd.Series): Data of a single column in the DataFrame.

        Returns:
            dict[str, SWDefinitionDevice]: A dictionary where the key is
            the module name and the value is an instance of SWDefinitionDevice.
        """
        nested_structure: dict[str, typing.Any | dict] = {}
        for (module, key), value in column_data.to_dict().items():
            if module not in nested_structure:
                nested_structure[module] = {}
            nested_structure[module][key] = value
            metatype_key = 'general/metatype'
            metatype_value = self.data['Metamodule'][module][key]
            nested_structure[module][metatype_key] = metatype_value
        return {
            module_name: SWDefinitionDevice(device_data)
            for module_name, device_data in nested_structure.items()
            }

    @staticmethod
    def update_device_name(device_data: SWDefinitionDevice) -> None:
        """
        Update the device name and variable name in a SWDefinitionDevice
        object.

        The method takes a SWDefinitionDevice object, formats its name and
        varname according to the predefined rules, and updates the object's
        data.

        Args:
            device_data (SWDefinitionDevice): The device object to be updated.
        """
        formatted_name = SWDefinitionSheetFormatter.format_device_name(
            name=device_data.get_device_name()
        )
        formatted_varname = SWDefinitionSheetFormatter.format_device_varname(
            varname=formatted_name
        )
        device_data.data['general/name'] = formatted_name
        if 'control/config/name' in device_data.data:
            device_data.data['control/config/name'] = formatted_name
        device_data.data['general/varname'] = formatted_varname

    def init_nested_structure(
        self
    ) -> dict[str, list[dict[str, typing.Any | dict]]]:
        """
        Initialize a nested structure to store device data as.

        This method iterates over device columns in the DataFrame,
        initializes devices and updates their names. Finally,
        it returns a nested dictionary containing the processed device data.

        Returns:
            dict[str, list[dict[str, typing.Any | dict]]]: A nested dictionary
            containing the device data.
        """
        nested_structure: dict[str, list] = {}
        col_idx = 1
        while True:
            if col_idx not in self.data:
                break
            devices = self.init_devices_in_column(self.data[col_idx])
            # prepare a list structure to store device data dicts
            for module_name in devices.keys():
                if module_name not in nested_structure:
                    nested_structure[module_name] = []
            # update name and varname in device data dicts
            for device_data in devices.values():
                self.update_device_name(device_data)
            for module_name, device_data in devices.items():
                if device_data.get_device_name():
                    nested_structure[module_name].append(device_data.data)
            col_idx += 1
        return nested_structure

    def remove_empty_modules(
        self,
        nested_structure: dict[str, list[dict[str, typing.Any | dict]]]
    ) -> None:
        """
        Remove modules that have no associated device data from
        the nested structure.

        This method iterates over the nested structure and identifies modules
        that do not have any device data (empty lists). It removes these
        modules from the structure to ensure the final nested dictionary only
        contains modules with relevant data.

        Args:
            nested_structure (dict[str, list[dict[str, typing.Any | dict]]]):
            The nested dictionary structure containing the module and device
            data.
        """
        to_remove = []
        for module_name, device_list in nested_structure.items():
            if not device_list:
                to_remove.append(module_name)
        for module_name in to_remove:
            del nested_structure[module_name]

    def add_child_device_data_to_parent_device_data(
        self,
        child_device: SWDefinitionDevice,
        child_module: SWDefinitionModule,
        nested_structure: dict[str, list[dict[str, typing.Any | dict]]]
    ) -> bool:
        """
        Identify the parent devices of a given child device and add the child
        device's data to the data structure of each of these parent devices.
        Note that the added child device data dictionary object is the same
        object as the original child device data dictionary.

        Args:
            child_device (SWDefinitionDevice): The child device object
            whose data needs to be added.
            child_module (SWDefinitionModule): The child module object
            associated with the child device.
            nested_structure (dict[str, list[dict[str, typing.Any | dict]]]):
            The nested dictionary structure containing all the device data.
        """
        # get the str parent device list, e.g. "par1, par3-par5",
        # and verify it is a string value
        if child_module.parent_connector not in child_device.data:
            logger.warning(
                'Device "%s" of type "%s" was identified as a potential child '
                'device, but parent connector "%s" was not found within '
                'the device data.', child_device.get_device_name(),
                child_module.name_full, child_module.parent_connector
                )
            return False
        assert isinstance(parent_device_names_str := (
            child_device.data[child_module.parent_connector]
        ), str)
        try:
            parent_device_names: typing.Iterable
            parent_device_names = Interval(parent_device_names_str)
        except TypeError:
            parent_device_names = [parent_device_names_str]
        # if a child device does not have any parent device assigned to it,
        # notify the user with a warning
        if not parent_device_names:
            child_device_name = child_device.get_device_name()
            logger.warning(
                'Device "%s" of type "%s" is not connected to any parent '
                'device of type "%s"', child_device_name,
                child_module.name_full, child_module.parent_name_full
                )
        # get the list of parent devices of the given child device
        parent_module_device_list = [
            device
            for device in nested_structure[child_module.parent_name_full]
            if device['general/name'] in parent_device_names
            ]
        # add the child device data to each parent device data
        for parent_device_data in parent_module_device_list:
            children_module_data = parent_device_data.setdefault(
                'children', {})
            children_device_data = children_module_data.setdefault(
                child_module.name_last, {})
            assert isinstance(children_device_data, dict)
            child_device_name = child_device.get_device_name()
            children_device_data[child_device_name] = child_device.data
        return True

    @staticmethod
    def copy_child_device_data(
        child_device_data: dict[str, dict | typing.Any],
        parent_module: SWDefinitionModule,
        parent_device: SWDefinitionDevice
    ) -> dict[str, dict | typing.Any]:
        parent_connector_key = SWDefinitionModule.get_connector_key_for_module(
                connected_module_name=parent_module.name_last)
        parent_device_name = parent_device.get_device_name()
        child_device_data_copy = dict(child_device_data)
        child_device_data_copy[parent_connector_key] = parent_device_name
        return child_device_data_copy

    def copy_children_device_data_within_parent_device_data(
        self,
        parent_module: SWDefinitionModule,
        parent_device: SWDefinitionDevice
    ) -> None:
        children_module_data = parent_device.data.setdefault('children', {})
        for module_data in children_module_data.values():
            assert isinstance(module_data, dict)
            for device_name, device_data in module_data.items():
                module_data[device_name] = self.copy_child_device_data(
                        device_data, parent_module, parent_device
                        )

    def format_nested_structure(
        self,
        nested_structure: dict[str, list[dict[str, typing.Any | dict]]]
    ) -> dict[str, dict]:
        """
        Integrate child device data into their respective parent devices and
        reorganize data from a list of device data to a nested dictionary with
        hierarchical device relations.

        Args:
            nested_structure (dict[str, list[dict[str, typing.Any | dict]]]):
            The initial structure with the raw device data.

        Returns:
            dict[str, dict]: The formatted nested dictionary structure.
        """
        # add child device references to their respective parent devices
        # (these child devices are removed later once they are copied)
        modules_to_remove = set()
        for module_name, device_list in nested_structure.items():
            module = SWDefinitionModule(module_name)
            if not module.parent_connector:  # is not a child module
                continue
            for device_data in device_list:
                device = SWDefinitionDevice(device_data)
                if self.add_child_device_data_to_parent_device_data(
                    device, module, nested_structure
                ):
                    modules_to_remove.add(module_name)
        # make child device data dicts under the 'children' key unique
        # (copy child device dicts)
        for module_name, device_list in nested_structure.items():
            module = SWDefinitionModule(module_name)
            for device_data in device_list:
                device = SWDefinitionDevice(device_data)
                self.copy_children_device_data_within_parent_device_data(
                    module, device
                    )
        # reorganize data to a homogenious nested dictionary from
        # a list of dictionaries
        nested_structure_formatted = {}
        for module_name, device_list in nested_structure.items():
            device_dict = {}
            for device_data in device_list:
                device_dict[device_data['general/name']] = device_data
            nested_structure_formatted[module_name] = device_dict
        # remove the original child device data
        for module_name in modules_to_remove:
            del nested_structure_formatted[module_name]
        return nested_structure_formatted

    @staticmethod
    def filter_devices(
        device_dict: dict[str, dict],
        preserve_devices: typing.Iterable[str],
        raise_if_filtered_all: bool = False
    ) -> dict[str, dict]:
        """
        Filter the devices in the dictionary based on a list of device names
        to preserve.

        Args:
            device_dict (dict[str, dict]): The dictionary containing device
            data.
            preserve_devices (typing.Iterable[str]): An iterable of device
            names to be preserved.
            raise_if_filtered_all (bool): A flag to raise an error if
            all devices are filtered out.

        Returns:
            dict[str, dict]: A dictionary containing only the data of devices
            listed in preserve_devices.
        """
        filtered_data = {}
        for device_name, device_data in device_dict.items():
            if device_name in preserve_devices:
                filtered_data[device_name] = device_data
        # if there were devices to preserve, but none of the devices in
        # the provided device_dict matched, and the filetered_data is empty
        if not filtered_data and raise_if_filtered_all and preserve_devices:
            devices = ", ".join(preserve_devices)
            raise KeyError(f'None of the devices "{devices}" were found')
        return filtered_data

    def to_dict(self) -> dict[str, dict]:
        """
        Convert the sheet data into a nested dictionary structure.

        This method acts as the main interface for converting the sheet data
        into a nested dictionary. It sequentially calls other methods
        to preprocess the data, initialize the nested structure, remove empty
        modules, and format the structure, resulting in a nested dictionary
        representation of the sheet data.

        Returns:
            dict[str, dict]: The nested dictionary structure containing
            the processed device data.
        """
        self.preprocess_sheet_data()
        devices_list = self.init_nested_structure()
        self.remove_empty_modules(devices_list)
        devices_dict = self.format_nested_structure(devices_list)
        return devices_dict


class SWDefinitionCommonSheetToNestedDictConverter(
    SWDefinitionSheetToNestedDictConverter
):
    def to_dict(self) -> dict[str, dict]:
        """
        Raises a `NotImplementedError` to indicate that the `to_dict_common`
        method should be used for processing "Common" sheets instead of
        the regular `to_dict` method from the parent class. Such sheets have
        specific processing requirements that  are handled by
        the `to_dict_common` method  with a different signature.

        Raises:
            NotImplementedError: Indicates the use of `to_dict_common`
            for "Common" sheets.
        """
        raise NotImplementedError(
            '"to_dict_common" method must be used to process the Common sheet'
            )

    def update_system_data(
        self, system_name: str, common_data: dict
    ) -> None:
        """
        Update the system data within the "Common" sheet data structure.

        This method updates various attributes of the system data, such as
        'varname', 'control/function', 'control/connector', and
        'control/config/name', based on the provided system name.

        Args:
            system_name (str): The name of the system to be updated.
            common_data (dict): The "Common" sheet data structure where
            the system data is located.
        """
        system_data = common_data['System'][system_name]
        system_data['general/varname'] = 'System'
        system_data['control/function'] = 'fSystem_System'
        system_data['control/devType'] = 'SystemType'
        system_data['control/connector'] = {}
        system_data['control/config/name'] = system_name
        system_safety_data = system_data.get('Safety')
        if system_safety_data:
            system_safety_device_data = system_safety_data['SystemSafety']
            system_safety_device_data['control/function'] = 'fSafety_SafetyCPU'

    def get_project_name(self, common_data: dict) -> str:
        """
        Extract the project name from the common data structure.

        Args:
            common_data (dict): The common data structure containing
            the project information.

        Returns:
            str: The extracted project name.
        """
        project_data: dict = common_data['Project']
        project_key: str = list(project_data.keys()).pop()
        project_name = project_key.split('/').pop()
        return project_name

    def update_shv_device_id(
        self, project_name: str, system_name: str, common_data: dict
    ) -> None:
        """
        Update the SHV device ID in the common data structure.

        This method constructs and updates the SHV "deviceID" key using
        the project name and system name.

        Args:
            project_name (str): The name of the project.
            system_name (str): The name of the system.
            common_data (dict): The common data structure where
            the SHV device ID is to be updated.
        """
        broker = f'{project_name}{system_name}-broker'
        try:
            common_data['SHV']['SHV']['control/config/deviceID'] = broker.lower()
        except KeyError:
            logger.warning('Failed to update SHV Device ID broker name.')

    def to_dict_common(
        self, system_name: str, commfunc_names: list[str]
    ) -> dict[str, dict]:
        """
        Convert the "Common" sheet data into a nested dictionary structure for
        a specific system.

        This method extends the `to_dict` method from the parent class to
        include additional processing steps specific to "Common" sheets.
        It filters and updates system and communication function data based on
        the provided system name and communication function names.

        Args:
            system_name (str): The name of the system to be processed.
            commfunc_names (list[str]): A list of communication function names
            used within the system.

        Returns:
            dict[str, dict]: The nested dictionary structure containing the
            processed "Common" sheet data.
        """
        data = super().to_dict()
        system_name_formatted = (
            SWDefinitionSheetFormatter.format_device_name(system_name)
            )
        if 'System' in data:
            data['System'] = self.filter_devices(
                data['System'],
                [system_name_formatted],
                raise_if_filtered_all=True
                )
        if 'CommFunction' in data:
            data['CommFunction'] = self.filter_devices(
                data['CommFunction'],
                commfunc_names
            )
        self.update_system_data(system_name_formatted, data)
        project_name = self.get_project_name(data)
        self.update_shv_device_id(project_name, system_name_formatted, data)
        return data
