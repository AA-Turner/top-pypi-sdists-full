# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for labelsplit files."""
import glob
import re
import json
import sys
from xml.etree import ElementTree
from pathlib import Path
from powertrain_build.feature_configs import FeatureConfigs
from powertrain_build.unit_configs import UnitConfigs
from powertrain_build.signal_interfaces import CsvSignalInterfaces
from powertrain_build.lib import helper_functions, logger

LOGGER = logger.create_logger(__file__)


class LabelSplit:
    """ Provides common LabelSplit functions for multiple repos.
    """
    def __init__(self, project, build_cfg, cfg_json, cmt_source_folder):
        """Read project configuration file to internal an representation.

        Args:
            project (str): Project name.
            build_cfg(BuildProjConfig): configures which units are active in the current project and where
                                        the code switch files are located.
            cfg_json(Path): Path to label split configuration file.
            cmt_source_folder (Path): Path to CMT source folder.
        """
        super().__init__()
        self.project = project
        self.build_cfg = build_cfg
        project_a2l_file_path = Path(self.build_cfg.get_src_code_dst_dir(),
                                     self.build_cfg.get_a2l_name())
        self.feature_cfg = FeatureConfigs(self.build_cfg)
        self.unit_cfg = UnitConfigs(self.build_cfg, self.feature_cfg)
        self.csv_if = CsvSignalInterfaces(self.build_cfg, self.unit_cfg)
        self.project_a2l_symbols = self.get_project_a2l_symbols(project_a2l_file_path)
        self.labelsplit_cfg = self.read_json(cfg_json)
        self.cmt_source_folder = cmt_source_folder

    @staticmethod
    def read_json(cfg_json):
        """Read label split configuration file from given location
           If the file does not exsit in the given location, program
           exits with error message.

        Args:
            cfg_json(Path): Path to label split configuration file
        Returns:
            labelsplit_cfg (dict): Dict of given file content
        """
        labelsplit_cfg = None
        if cfg_json.exists():
            with cfg_json.open() as json_file:
                labelsplit_cfg = json.load(json_file)
            return labelsplit_cfg
        LOGGER.error('Cannot find label split config file: %s', cfg_json)
        sys.exit(1)

    @staticmethod
    def get_project_a2l_symbols(project_a2l_file_path):
        """Get a list of calibration symbols found in a given project A2L file.

        Args:
            project_a2l_file_path (Path): Path to project A2L file.
        Returns:
            symbols_in_a2l (list): List of calibration symbols found in the project A2L file.
        """
        symbols_in_a2l = []

        with project_a2l_file_path.open() as a2l_fh:
            a2l_text = a2l_fh.read()

        calibration_blocks = re.findall(r'(?:\s*\n)*(\s*/begin (CHARACTERISTIC|AXIS_PTS)[\n\s]*'
                                        r'(\w+)([\[\d+\]]*).*?\n.*?/end \2)',
                                        a2l_text,
                                        flags=re.M | re.DOTALL)

        for blk in calibration_blocks:
            symbols_in_a2l.append(blk[2])

        return symbols_in_a2l

    @staticmethod
    def get_sgp_symbols(sgp_file: Path):
        """Get symbols and symbol_groups found in a given _sgp.xml file.

        Example output: {sVcExample: [(3, EC_EX_1), (4, EC_EX_2)]}, where the indices are column indices:
        1 -> symbol name (therefore not in list of symbol groups).
        2 -> diesel group.
        3 -> petrol group.
        4 -> hybrid group.
        5 -> subsystem (therefore not in list of symbol groups).

        Args:
            sgp_file (Path): Path to an _sgp.xml file.
        Returns:
            found_sgp_symbols (dict): A symbol to symbol_groups dictionary found in the sgp_file.
        """
        tree = ElementTree.parse(sgp_file)
        root = tree.getroot()
        search_string = '{{urn:schemas-microsoft-com:office:spreadsheet}}{tag}'
        label_sheet = root.find(search_string.format(tag='Worksheet'))
        table = label_sheet.find(search_string.format(tag='Table'))
        rows = table.findall(search_string.format(tag='Row'))

        found_sgp_symbols = {}
        for row in rows:
            symbol = None
            column_counter = 1
            cells = row.findall(search_string.format(tag='Cell'))
            for cell in cells:
                data = cell.find(search_string.format(tag='Data'))
                if data is not None:
                    # Sometimes there are spaces in the symbol cell
                    # Sometimes there is a weird \ufeff character (VcDebug_sgp.xml) in the symbol cell
                    value = data.text.replace(' ', '').replace('\ufeff', '')
                    if symbol is None:
                        symbol = value
                        found_sgp_symbols[symbol] = []
                    else:
                        new_index = search_string.format(tag='Index')
                        if new_index in cell.attrib:
                            column_counter = int(cell.attrib[new_index])
                        found_sgp_symbols[symbol].append((column_counter, value))
                column_counter += 1

        return found_sgp_symbols

    def get_sgp_symbol_group(self, symbol_groups_by_index):
        """Match _sgp.xml file indices (symbol groups) with a given project.

        Args:
            symbol_groups_by_index (list(tuple)): List of (index, symbol_group) pairs.
        Returns:
            symbol_group (str): The symbol group corresponding to the given project.
        """
        symbol_group = ''
        symbol_dict = self.labelsplit_cfg.get("SGP_SYMBOL_GROUPS")
        symbol_list = [val for key, val in symbol_dict.items() if key in self.project]
        if len(symbol_list) >= 1:
            for index, group in symbol_groups_by_index:
                if index == symbol_list[0]:
                    symbol_group = group
        else:
            LOGGER.error('Cannot match symbol group type for project: %s', self.project)
        return symbol_group

    def get_interface_symbols_and_groups(self, interface_dict, in_symbol_sgp_dict, out_symbol_sgp_dict):
        """Get a list of (symbol, symbol_group) pairs found in given interface and sgp files.

        Args:
            interface_dict (dict): interface to symbol map, matching a certain IO type.
            in_symbol_sgp_dict (dict): An input symbol to symbol_groups dictionary found in an sgp_file,
                to be compared with interface_dict inputs.
            out_symbol_sgp_dict (dict): An output symbol to symbol_groups dictionary found in an sgp_file,
                to be compared with interface_dict outputs.
        Returns:
            symbols_and_groups (list(tuple)): List of (symbol, symbol_group) pairs in: interface and sgp file.
        """
        symbols_and_groups = []
        for interface, symbol_data in interface_dict.items():
            for symbol in symbol_data.keys():
                debug_name = re.sub(r'\w(\w+)', r'c\1_db', symbol)
                switch_name = re.sub(r'\w(\w+)', r'c\1_sw', symbol)
                if 'Input' in interface and debug_name in in_symbol_sgp_dict and switch_name in in_symbol_sgp_dict:
                    debug_symbol_group = self.get_sgp_symbol_group(in_symbol_sgp_dict[debug_name])
                    switch_symbol_group = self.get_sgp_symbol_group(in_symbol_sgp_dict[switch_name])
                    symbols_and_groups.extend([(debug_name, debug_symbol_group), (switch_name, switch_symbol_group)])
                elif 'Output' in interface and debug_name in out_symbol_sgp_dict and switch_name in out_symbol_sgp_dict:
                    debug_symbol_group = self.get_sgp_symbol_group(out_symbol_sgp_dict[debug_name])
                    switch_symbol_group = self.get_sgp_symbol_group(out_symbol_sgp_dict[switch_name])
                    symbols_and_groups.extend([(debug_name, debug_symbol_group), (switch_name, switch_symbol_group)])
        return symbols_and_groups

    def get_debug_symbols_and_groups(self):
        """Get a list of (symbol, symbol_group) pairs found in project interface and VcDebug*_sgp.xml files.

        Returns:
            debug_symbols_and_groups (list(tuple)): List of (symbol, symbol_group) pairs in:
                interface and VcDebug*_sgp.xmlfiles.
        """
        _unused, dep, _unused_two, debug = self.csv_if.get_io_config()
        sgp_file_dict = self.labelsplit_cfg.get("SGP_FILE")
        debug_sgp_file = Path(sgp_file_dict.get('cfg_folder'), sgp_file_dict.get('debug'))
        debug_output_sgp_file = Path(sgp_file_dict.get('cfg_folder'), sgp_file_dict.get('debug_output'))
        dep_sgp_file = Path(sgp_file_dict.get('cfg_folder'), sgp_file_dict.get('dep'))
        dep_output_sgp_file = Path(sgp_file_dict.get('cfg_folder'), sgp_file_dict.get('dep_output'))
        debug_sgp_symbols = self.get_sgp_symbols(debug_sgp_file)
        debug_output_sgp_symbols = self.get_sgp_symbols(debug_output_sgp_file)
        dep_sgp_symbols = self.get_sgp_symbols(dep_sgp_file)
        dep_output_sgp_symbols = self.get_sgp_symbols(dep_output_sgp_file)

        symbols_and_groups_tmp = []
        debug_tmp = self.get_interface_symbols_and_groups(debug,
                                                          debug_sgp_symbols,
                                                          debug_output_sgp_symbols)
        dep_tmp = self.get_interface_symbols_and_groups(dep,
                                                        dep_sgp_symbols,
                                                        dep_output_sgp_symbols)
        symbols_and_groups_tmp.extend(debug_tmp)
        symbols_and_groups_tmp.extend(dep_tmp)

        debug_symbols_and_groups = []
        for symbol, symbol_group in symbols_and_groups_tmp:
            if symbol_group == '':
                LOGGER.info('Debug symbol %s is missing symbol group and will be removed.', symbol)
            else:
                debug_symbols_and_groups.append((symbol, symbol_group))

        return debug_symbols_and_groups

    def check_unit_par_file(self, unit):
        """Check <unit>_par.m file for default sgp symbol group.

        Args:
            unit (str): Current unit/model name.
        Returns:
            has_sgp_default (Bool): True/False if unit is associated with default sgp value.
            default_symbol_group (str): Name of default symbol group.
        """
        has_sgp_default = False
        default_symbol_group = ''
        base_search_string = r'SgpDefault\.{unit}\.[A-Za-z]+\s*=\s*[\'\"]([A-Za-z_]+)[\'\"]'
        search_string = base_search_string.format(unit=unit)

        non_existent_par_file = Path('non_existent_par_file.m')
        found_par_files = glob.glob('Models/*/' + unit + '/' + unit + '_par.m')
        if len(found_par_files) > 1:
            LOGGER.warning('Found more than one _par.m file, using %s', found_par_files[0])
        par_file = Path(found_par_files[0]) if found_par_files else non_existent_par_file

        if self.labelsplit_cfg.get("special_unit_prefixes"):
            for special_prefix in self.labelsplit_cfg.get("special_unit_prefixes"):
                if unit.startswith(special_prefix) and not par_file.is_file():
                    # Some units require special handling.
                    if '__' in unit:
                        parent = unit.replace('__', 'Mdl__')
                    else:
                        parent = unit + 'Mdl'
                    found_par_files = glob.glob('Models/*/' + parent + '/' + parent + '_par.m')
                    par_file = Path(found_par_files[0]) if found_par_files else Path(non_existent_par_file)
                    # Default symbol group is based on c-file name
                    c_name = re.sub('(Mdl)?(__.*)?', '', unit)
                    search_string = base_search_string.format(unit=c_name)

        if par_file.is_file():
            with par_file.open(encoding="latin-1") as par_fh:
                par_text = par_fh.read()
                sgp_default_match = re.search(search_string, par_text)
                if sgp_default_match is not None:
                    has_sgp_default = True
                    default_symbol_group = sgp_default_match.group(1)
        else:
            LOGGER.info('Missing _par file for model: %s', unit)

        return has_sgp_default, default_symbol_group

    def get_unit_sgp_file(self, unit):
        """Get path to <unit>_sgp.xml file.

        Args:
            unit (str): Current unit/model name.
        Returns:
            sgp_file (Path): Path to <unit>_sgp.xml file.
        """
        non_existent_sgp_file = Path('non_existent_sgp_file.xml')
        found_sgp_files = glob.glob('Models/*/' + unit + '/' + unit + '_sgp.xml')
        if len(found_sgp_files) > 1:
            LOGGER.warning('Found more than one _sgp.xml file, using %s', found_sgp_files[0])
        sgp_file = Path(found_sgp_files[0]) if found_sgp_files else Path(non_existent_sgp_file)

        if self.labelsplit_cfg.get("special_unit_prefixes"):
            for special_prefix in self.labelsplit_cfg.get("special_unit_prefixes"):
                if unit.startswith(special_prefix) and not sgp_file.is_file():
                    # Some units require special handling.
                    if '__' in unit:
                        parent = unit.replace('__', 'Mdl__')
                    else:
                        parent = unit + 'Mdl'
                    found_sgp_files = glob.glob('Models/*/' + parent + '/' + parent + '_sgp.xml')
                    sgp_file = Path(found_sgp_files[0]) if found_sgp_files else Path(non_existent_sgp_file)

        return sgp_file

    def get_unit_symbols_and_groups(self, unit, calibration_symbols):
        """Get a list of (symbol, symbol_group) pairs found in A2L, <unit>_sgp/par and config_<unit>.json files.

        Args:
            unit (str): Current unit/model name.
            calibration_symbols (list): All calibration symbols for the unit (from config_<unit>.json).
        Returns:
            unit_symbols_and_groups (list(tuple)): List of (symbol, symbol_group) pairs in: A2L, _sgp/_par and
            config files.
        """
        unit_symbols_and_groups = []
        has_sgp_default, default_symbol_group = self.check_unit_par_file(unit)
        sgp_file = self.get_unit_sgp_file(unit)

        if sgp_file.is_file():
            found_sgp_symbols = self.get_sgp_symbols(sgp_file)
        else:
            found_sgp_symbols = {}
            LOGGER.info('Missing _sgp file for model: %s', unit)

        for symbol in calibration_symbols:
            if symbol not in self.project_a2l_symbols:
                LOGGER.info('Symbol %s not in project A2L file and will be removed.', symbol)
                continue

            if symbol in found_sgp_symbols:
                symbol_group = self.get_sgp_symbol_group(found_sgp_symbols[symbol])
                unit_symbols_and_groups.append((symbol, symbol_group))
            elif has_sgp_default:
                if symbol.endswith('_sw') or symbol.endswith('_db'):
                    LOGGER.info('Debug symbol %s not in sgp file and will be removed.', symbol)
                else:
                    unit_symbols_and_groups.append((symbol, default_symbol_group))
            else:
                LOGGER.info('Symbol %s missing in _sgp file and lack SgpDefault value.', symbol)

        return unit_symbols_and_groups

    def get_calibration_constants(self):
        """Get all calibration symbols for each unit in the project.

        Returns:
            calibration_symbols_per_unit (dict): A unit to symbol list dictionary.
        """
        security_variables = self.labelsplit_cfg.get("security_variables")
        u_conf_dict = self.unit_cfg.get_per_cfg_unit_cfg()

        safe_calibration_symbols = {}
        for symbol, symbol_data in u_conf_dict['calib_consts'].items():
            if symbol not in security_variables:
                safe_calibration_symbols.update({symbol: symbol_data})

        calibration_symbols_per_unit = {}
        for symbol, symbol_data in safe_calibration_symbols.items():
            for unit, unit_data in symbol_data.items():
                if 'CVC_CAL' in unit_data['class']:
                    if unit in calibration_symbols_per_unit:
                        calibration_symbols_per_unit[unit].append(symbol)
                    else:
                        calibration_symbols_per_unit[unit] = [symbol]

        return calibration_symbols_per_unit

    def get_symbols_and_groups(self):
        """Get a list of (symbol, symbol_group) pairs found in A2L, <unit>_sgp/par and config_<unit>.json files.

        Returns:
            exit_code (int): 0/1 based on successful collection of symbols and symbol groups.
            all_symbols_and_groups (dict): A symbol to symbol_group dictionary for all A2L, _sgp/_par and config files,
        """
        exit_code = 0
        calibration_symbols_per_unit = self.get_calibration_constants()
        debug_symbols = self.get_debug_symbols_and_groups()

        all_symbol_and_group_pairs = []
        if self.labelsplit_cfg.get("project_symbols"):
            special_project_dict = self.labelsplit_cfg.get("project_symbols")
            pair_list = [val for key, val in special_project_dict.items() if key in self.project]
            if len(pair_list) == 1:
                symbol_and_group_pairs_list = pair_list[0].items()
                all_symbol_and_group_pairs += symbol_and_group_pairs_list
            elif len(pair_list) > 1:
                LOGGER.error('Project %s has does not follow the name rule', self.project)
                return 1, {}

        all_symbol_and_group_pairs.extend(debug_symbols)

        for unit, symbols in calibration_symbols_per_unit.items():
            if self.labelsplit_cfg.get("special_units"):
                special_unit_dict = self.labelsplit_cfg.get("special_units")
                if unit in special_unit_dict.keys():
                    # Some units require special handling.
                    LOGGER.warning('Found %s, assuming %s is used.', unit, special_unit_dict.get(unit))
                    labels = self.get_unit_symbols_and_groups(special_unit_dict.get(unit), symbols)
                else:
                    labels = self.get_unit_symbols_and_groups(unit, symbols)
            else:
                labels = self.get_unit_symbols_and_groups(unit, symbols)
            all_symbol_and_group_pairs.extend(labels)

        symbol_to_group_dict = {}
        for symbol, symbol_group in all_symbol_and_group_pairs:
            if symbol in symbol_to_group_dict:
                if symbol_to_group_dict[symbol] != symbol_group:
                    LOGGER.error('Symbol %s multiply defined with different symbol groups.', symbol)
                    exit_code = 1
            else:
                symbol_to_group_dict[symbol] = symbol_group

        return exit_code, symbol_to_group_dict

    def generate_label_split_xml_file(self, symbols_and_groups):
        """Generate a label split file, given a directory plus labels and groups to add.

        Args:
            symbols_and_groups (dict): A symbol to symbol_group dictionary given a project.
        Returns:
            exit_code (int): 0/1 based on successful generation of Labelsplit.xls.
        """
        errors = []
        project_root_dir = self.build_cfg.get_root_dir()
        cmt_output_folder = helper_functions.create_dir(Path(project_root_dir, 'output', 'CMT'))
        start_file_name = Path(self.cmt_source_folder, 'template_labelsplit_sgp_start.xml_')
        row_count_file_name = Path(cmt_output_folder, 'labelsplit_rowcount.xml_')
        start_2_file_name = Path(self.cmt_source_folder, 'template_labelsplit_sgp_start_2.xml_')
        label_split_rows_filename = Path(cmt_output_folder, 'labelsplit_rows.xml_')
        end_file_name = Path(self.cmt_source_folder, 'template_labelsplit_sgp_end.xml_')
        files_to_merge = [start_file_name, row_count_file_name, start_2_file_name,
                          label_split_rows_filename, end_file_name]

        with row_count_file_name.open('w', encoding="utf-8") as rc_fh:
            rc_fh.write(f'{len(symbols_and_groups) + 1}')  # header + data

        with label_split_rows_filename.open('w', encoding="utf-8") as lsrf_fh:
            for symbol, symbol_group in symbols_and_groups.items():
                if symbol_group == '':
                    errors.append(f'Missing symbol group for symbol: {symbol}')
                elif symbol_group == 'VCC_SPM_DEBUG':
                    LOGGER.info('Ignoring undistributed debug symbol: %s', symbol)
                else:
                    lsrf_fh.write(
                        '   <Row ss:AutoFitHeight="0">\n'
                        f'    <Cell><Data ss:Type="String">{symbol}'
                        '</Data><NamedCell ss:Name="_FilterDatabase"/></Cell>\n'
                        f'    <Cell ss:Index="5"><Data ss:Type="String">{symbol_group}'
                        '</Data><NamedCell ss:Name="_FilterDatabase"/></Cell>\n'
                        '   </Row>\n'
                    )

        if errors:
            LOGGER.error('\n'.join(errors))
            return 1

        output_file_name = Path(project_root_dir, 'output', 'CMT', 'Labelsplit.xls')
        with output_file_name.open('w', encoding="utf-8") as output_fh:
            for file_name in files_to_merge:
                with file_name.open(encoding="utf-8") as input_fh:
                    content = input_fh.read()
                    output_fh.write(content)
        LOGGER.info('Delivery to: %s', str(output_file_name))
        return 0
