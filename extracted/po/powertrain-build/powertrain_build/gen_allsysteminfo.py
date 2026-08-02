# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module to generate AllSystemInfo.mat for compatibility purposes with DocGen."""

import os
from copy import deepcopy
from numpy import array
from scipy.io import savemat
from powertrain_build.signal_interfaces import SignalInterfaces
from powertrain_build.unit_configs import UnitConfigs
from powertrain_build.lib.helper_functions import merge_dicts
from powertrain_build.problem_logger import ProblemLogger


def _get_signals_by_type(signal_conf, signal_type):
    """Get signals by type ('missing', 'unused', 'inconsistent_defs' or 'multiple_defs').

    Args:
        signal_conf (dict): Configuration from SignalInterfaces with the following format
        {
            "missing": {"signal_name" : ["VED4_GENIII", "VEP4_GENIII"]}
            "unused": {}
            "multiple_defs": {}
            "inconsistent_defs": {}
        }

    Returns:
        dict: with the following format
        {
            "signal_name" : {'VarStatus' : 'Not Used', 'SignalType' : "signal_type"}
        }

    """
    result = {}
    for signal_name in signal_conf[signal_type].keys():
        signal = {signal_name: {'VarStatus': 'Not Used', 'SignalType': signal_type}}
        result.update(signal)
    return result


class GenAllSystemInfo(ProblemLogger):
    """Class to generate AllSystemInfo.mat for compatibility purposes with DocGen."""

    _signal_types = ['missing', 'unused']

    def __init__(self, signal_if, unit_cfg):
        """Class to generate a matlab struct AllSystemInfo for compatibility with the old document generation.

        Args:
            signal_if: an initialized SignalInterfaces object to access signal configurations
        """
        if not isinstance(signal_if, SignalInterfaces):
            raise TypeError
        if not isinstance(unit_cfg, UnitConfigs):
            raise TypeError
        self.signal_if = signal_if
        self.unit_cfg = unit_cfg
        self._signals_without_source = {}
        self._core_ids = {}
        self._file_info = {}
        self._dids = {}

    def __repr__(self):
        """Get string representation of object."""
        return f'if: {self.signal_if}\n uc: {self.unit_cfg}'

    def build(self):
        """Build AllSystemInfo.mat for docgen compatibility."""
        self.info('******************************************************')
        self.info('%s - Getting signals without source', __name__)
        signals_tmp = self.get_signals_without_source()
        for signal_name, signal_data in signals_tmp.items():
            if '.' in signal_name:
                struct_name = signal_name.split('.')[0]
                if struct_name not in self._signals_without_source:
                    self.info(
                        f'{__name__} - Found struct signal: {signal_name}, adding struct name only ({struct_name}). '
                        'Remaining members will be ignored.'
                    )
                    self._signals_without_source[struct_name] = signal_data
            else:
                self._signals_without_source[signal_name] = signal_data

        self.info('%s - Getting CoreIDs', __name__)
        self._core_ids = self.get_core_ids()

        self.info('%s - Generating FileInfo', __name__)
        self._file_info = self._gen_dummy_file_info()

        self.info('%s - Getting DIDs', __name__)
        self._dids = self.get_dids()

        output_path = os.path.abspath(os.path.join('Models', 'CodeGenTmp'))
        self.info('%s - Creating CodeGenTmp directory', __name__)
        self.create_codegen_tmp_dir(output_path)

        self.info('%s - Building AllSystemInfo', __name__)
        self._build_all_system_info(output_path)

    def create_codegen_tmp_dir(self, path):
        """Create CodeGenTmp directory if it does not exist.

        Args:
            path (str): directory to create.
        """
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            self.info('%s - Directory already exist at %s', __name__, path)

    def _build_all_system_info(self, path):
        """Build AllSystemInfo.mat for DocGen compatibility.

        Args:
            path (str): directory path to place the output file.
        """
        absolute_path = os.path.abspath(os.path.join(path, 'AllSystemInfo.mat'))
        all_system_info = {
            'SystemData': self._signals_without_source,
            'CoreIDs': self._core_ids,
            'FileInfo': self._file_info,
            'DIDs': self._dids
        }

        all_system_info_scipy = {'AllSystemInfo': all_system_info}
        savemat(absolute_path, all_system_info_scipy, long_field_names=True, do_compression=True)
        self.info('%s - AllSystemInfo placed at %s', __name__, absolute_path)

    def get_core_ids(self):
        """Get core IDs for specified project.

        Returns:
            dict: DID as a dict with the following format
            {
                "unit name" : {}
            }

        """
        result = {}
        unit_configs = self.unit_cfg.get_per_unit_cfg()
        for unit, configs in unit_configs.items():
            result[unit] = deepcopy(configs['core'])
        for unit, configs in result.items():
            for core_id, core_id_dict in configs.items():
                for identifier, data_dict in core_id_dict.items():
                    for tl_field, tl_data in data_dict.items():
                        # Turn lists into numpy.array, required to get matlab cell arrays instead of char arrays.
                        # char arrays make DocGen crash.
                        if isinstance(tl_data, list):
                            configs[core_id][identifier][tl_field] = array(tl_data, dtype=object)
                        else:
                            configs[core_id][identifier][tl_field] = tl_data
        return result

    def get_dids(self):
        """Get DIDs for specified project.

        Returns:
            dict: DID as a dict with the following format
            {
                "unit name" : {}
            }

        """
        result = {}
        unit_configs = self.unit_cfg.get_per_unit_cfg()
        for unit, configs in unit_configs.items():
            dids_list = []
            for signal_values in configs['dids'].values():
                signal_values_allsysteminfo_keys = {
                        'sig_name': signal_values['name'],
                        'sig_desc': signal_values['description'],
                        'blk_name': signal_values['handle'],
                        'data_type': signal_values['type'],
                        'unit': signal_values['unit'],
                        'lsb': signal_values['lsb'],
                        'offset': signal_values['offset']
                        }
                dids_list.append(signal_values_allsysteminfo_keys)
            result.update({unit: dids_list})

        return result

    def _gen_dummy_file_info(self):
        """Generate dummy FileInfo struct for compatibility purposes."""
        result = {}
        for key in self._core_ids:
            result.update({key: ''})
        return result

    def get_signals_without_source(self):
        """Get missing and unused signals from project configuration.

        Returns:
            dict: result with the following format
            {
                "signal_name" : "signal_type"
            }

        """
        prj_conf = self.signal_if.check_config()
        result = self._get_external_signals(prj_conf)
        temp_signals = self._get_internal_signals(prj_conf)
        result = merge_dicts(result, temp_signals, merge_recursively=True)
        return result

    def _get_external_signals(self, prj_conf):
        signals_conf = prj_conf['sigs']['ext']
        return self._get_signals_by_types(signals_conf)

    def _get_internal_signals(self, prj_conf):
        result = {}
        signals_conf = prj_conf['sigs']['int']
        for sig_conf in signals_conf.values():
            temp_signals = self._get_signals_by_types(sig_conf)
            result = merge_dicts(result, temp_signals, merge_recursively=True)
        return result

    def _get_signals_by_types(self, signal_conf):
        """Get signals by multiple types and merge them into one dictionary, see _get_signals_by_type() for docs."""
        result = {}
        for signal_type in self._signal_types:
            temp_signals = _get_signals_by_type(signal_conf, signal_type)
            if temp_signals:
                result = merge_dicts(result, temp_signals, merge_recursively=True)
        return result
