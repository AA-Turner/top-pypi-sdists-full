# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Module for reading unit configuration files."""
import json
import os
import time
from pprint import pformat

from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.versioncheck import Version


class CodeGenerators:
    """Enum for code generators."""
    target_link = 'target_link'
    embedded_coder = 'embedded_coder'


class UnitConfigs(ProblemLogger):
    """A class for accessing the project’s unit definitions (see :doc:`unit_config`).

    Provides methods for retrieving the all definitions of a unit and all existing units.
    """

    CONFIG_SKIP_LIST = ['VcDebugSafe', 'VcDebug', 'VcDebugOutputSafe', 'VcDebugOutput']

    def __init__(self, build_prj_config, feature_config):
        """Class Initialization.

        Args:
            build_prj_config (BuildProjConfig): A class instance which holds
                                                the information of where to find units configs to parse
            feature_config (FeatureConfigs): Class instance project feature definitions

        """
        super().__init__()
        if not isinstance(build_prj_config, BuildProjConfig):
            raise TypeError('build_prj_config argument is not an'
                            ' instance of BuildProjConfig')
        self._build_prj_config = build_prj_config
        self._feature_cfg = feature_config
        self._raw_per_unit_configs = {}
        self._per_unit_configs = {}
        self._per_type_unit_configs = {}
        self._if_define_dict = {}
        self._missing_configs = set()
        self._empty_config_def = set()
        self._parse_all_unit_configs()
        self._per_type_unit_signals()
        self.code_generators = self._get_code_generators()
        self.base_types_headers = self._get_base_types_headers()

        # write the summary of error (to avoid repeating error messages)
        for unit in self._missing_configs:
            self.critical('%s is missing config files', unit)
        for var, unit in self._empty_config_def:
            self.warning('%s in unit %s, has empty config_def!'
                         'probably goto-block, missing a corresponing from-block.',
                         var, unit)

    def __repr__(self):
        """Get string representation of object."""
        return pformat(self._per_type_unit_configs)

    def _parse_all_unit_configs(self):
        """Parse all unit config files."""
        start_time = time.time()
        self.info('  Start loading unit_cfg json files')
        cfg_dirs = self._build_prj_config.get_unit_cfg_dirs()
        for unit, cfg_dir in cfg_dirs.items():
            self._parse_unit_config(unit, cfg_dir)
        self.info('  Finished loading unit_cfg json files (in %4.2f s)', time.time() - start_time)

    def _parse_unit_config(self, unit, cfg_dir):
        """Parse one unit config file."""
        file_ = os.path.join(cfg_dir, f'config_{unit}.json')
        with open(file_, 'r', encoding="utf-8") as fhndl:
            self.debug('Loading json file %s', unit)
            try:
                tmp_ucfg = json.load(fhndl)
                if not Version.is_compatible(tmp_ucfg.get('version', '0.0.0')):
                    raise ValueError(f'Incompatible config file version for unit {unit}.')
                if unit in self._raw_per_unit_configs:
                    self.critical("Conflicting Unit name %s: Units need to have unique names", unit)
                self._raw_per_unit_configs[unit] = tmp_ucfg
            except json.JSONDecodeError as ex:
                self.critical('Error reading config file %s: %s', file_, ex)
                return
        for include_unit in tmp_ucfg.get('includes', []):
            self.debug('%s includes %s in %s', unit, include_unit, cfg_dir)
            self._parse_unit_config(include_unit, cfg_dir)

    def _filter_io_nvm_feat(self):
        """Remove all parameters not defined in the prj_config.

        Parameters can be removed via not active feature in the unit, or
        the entire unit is not included in the project.

        Args:
            config (str): the name of the configuration

        the format of the data-dict::

            {'UnitName': {'class': 'CVC_EXT',
                          'configs': [['Vc_D_CodegenHev '
                                      '== 2',
                                      'Vc_D_CodegenHev '
                                      '> 0']],
                          'description': 'HV battery cooling request',
                          'handle': 'VcPpmPsm/VcPpmPsm/Subsystem/'
                                    'VcPpmPsm/yVcBec_B_ChillerCoolReq',
                          'lsb': 1,
                          'max': 3,
                          'min': 0,
                          'name': 'sVcBec_D_HvBattCoolgReq',
                          'offset': 0,
                          'type': 'UInt8',
                          'unit': '-'}
            }

        """
        res = {}
        self.debug('_filter_io_nvm_feat: Feature Cfg')
        for unit in self._build_prj_config.get_included_units():
            self._filter_io_nvm_feat_unit(unit, res)
        if not res:
            self.warning('No units configured for project')
        return res

    def _filter_core_config(self, u_def_data):
        """Handle core configs."""
        f_core = {}
        for core_type, core_data in u_def_data.items():
            f_core[core_type] = {}
            for key, value in core_data.items():
                if key != 'IllegalBlk':
                    # Matlab sets core:{type:{name:{API_blk:[{path, config}]}}}
                    # config.py - core:{type:{name:{configs}}}
                    configs = value.get('configs', [cfg for blk in value['API_blk'] for cfg in blk['config']])
                    if self._feature_cfg.check_if_active_in_config(configs):
                        f_core[core_type][key] = value
        return f_core

    def _filter_io_nvm_feat_unit(self, unit, res):
        """Handle one unit config with respect to the filtering in :_filter_io_nvm_feat:."""
        try:
            u_data = self._raw_per_unit_configs[unit]
        except KeyError:
            # Some units in the raster should not have config files
            if unit not in self.CONFIG_SKIP_LIST:
                self.debug('_filter_io_nvm_feat_unit: cfg missing: %s', unit)
                self._missing_configs.add(unit)
            return
        for u_def_type, u_def_data in u_data.items():
            res.setdefault(unit, {}).setdefault(u_def_type, {})
            if u_def_type == 'dids':
                f_dids = {k: v for k, v in u_def_data.items()
                          if self._feature_cfg.check_if_active_in_config(v['configs'])}
                res[unit][u_def_type] = f_dids
            elif u_def_type == 'core':
                res[unit][u_def_type] = self._filter_core_config(u_def_data)
            elif u_def_type == 'pre_procs':
                # the pre_proc key does not have configuration attributes
                res[unit]['pre_procs'] = u_def_data
            elif u_def_type == 'integrity_level':
                res[unit]['integrity_level'] = u_def_data
            elif u_def_type == 'code_generator':
                res[unit]['code_generator'] = u_def_data
            elif u_def_type == 'version':
                res[unit]['version'] = u_def_data
            elif u_def_type == 'csp':
                csp_data = {}
                if 'methods' in u_def_data:
                    csp_data = {'methods': {}}
                    for method_name, method_data in u_def_data['methods'].items():
                        if self._feature_cfg.check_if_active_in_config(method_data['configs']):
                            csp_data['methods'][method_name] = method_data
                res[unit][u_def_type] = csp_data
            elif u_def_type == 'includes':
                # List of configs for handwritten code
                for included_unit in u_def_data:
                    self.debug('%s includes %s', unit, included_unit)
                    self._filter_io_nvm_feat_unit(included_unit, res)
            else:
                for var, var_pars in u_def_data.items():
                    # TODO: remove this code when the bug in the matlab code is removed.
                    if var_pars['configs'] == []:
                        self.debug('Adding %s', unit)
                        self._empty_config_def.add((var, unit))
                    if self._feature_cfg.check_if_active_in_config(var_pars['configs']):
                        res[unit][u_def_type].setdefault(var, {}).update(var_pars)

    @staticmethod
    def _update_io_nvm(dict_, unit, data_type, variables):
        """Change the struct for in out and nvm variables.

        The resulting new struct is stored in the dict dict_
        """
        for var, var_pars in variables.items():
            dict_.setdefault(data_type, {}).setdefault(var, {}).setdefault(unit, var_pars)

    def _update_dids(self, unit, key, data, feat_cfg=None):
        """Change the struct for in out and nvm variables."""
        # TODO: Add functionality

    @staticmethod
    def _update_core(dict_, unit, data_type, core_ids):
        """Change the struct for in core parameters."""
        for _, core_data in core_ids.items():
            for var, var_pars in core_data.items():
                dict_.setdefault(data_type, {}).setdefault(var, {}).setdefault(unit, var_pars)

    def _update_pre_procs(self, unit, key, data, feat_cfg=None):
        """Change the struct for in pre_processor parameters."""
        # TODO: Add functionality

    def _per_type_unit_signals(self):
        """Change the structure of the data to aggregate all unit configs.

        Returns:
            dict: a structure per config type instead of per unit

        """
        # loop over all projects and store the active items in each configuration
        self._per_unit_configs = self._filter_io_nvm_feat()
        dict_ = self._per_type_unit_configs = {}
        for unit, udata in self._per_unit_configs.items():
            for data_type, variables in udata.items():
                if data_type in ['core']:
                    self._update_core(dict_, unit, data_type, variables)
                elif data_type in ['dids']:
                    self._update_dids(dict_, unit, data_type, variables)
                elif data_type in ['pre_procs']:
                    self._update_pre_procs(dict_, unit, data_type, variables)
                elif data_type in ['outports', 'inports', 'dids', 'nvm', 'local_vars', 'calib_consts', 'csp']:
                    self._update_io_nvm(dict_, unit, data_type, variables)
                else:
                    dict_.setdefault(data_type, {}).setdefault(unit, udata)

    def check_if_in_unit_cfg(self, unit, symbol):
        """Check if the symbol is defined in the unit config file."""
        for data in self._raw_per_unit_configs[unit].values():
            if isinstance(data, dict):
                if symbol in data:
                    return True
        return False

    def get_per_cfg_unit_cfg(self):
        """Get all io-signals and core-ids for all units.

        Get all io-signals and core-ids for all units, where all inports, outport, etc,
        are aggregated from all unit definition files.

        Returns:
            dict: a dict with the below format::

            {
                'inports/outports/nvm/core': {
                    'VARIABLE_NAME': {
                        'UNIT_NAME': {
                            'class': 'CVC_EXT',
                            'configs': [['all']],
                            'description': 'Power Pulse ',
                            'handle': 'VcPemAlc/VcPemAlc/Subsystem/VcPemAlc/yVcVmcPmm_B_SsActive9',
                            'lsb': 1,
                            'max': 800,
                            'min': 0,
                            'name': 'sVcAesPp_Pw_PwrPls',
                            'offset': 0,
                            'type': 'UInt16',
                            'unit': 'W'
                            }
                        }
                    }
                }
            }

        The top level keys are 'inports', 'outports', 'nvm' and 'core'

        """
        return self._per_type_unit_configs

    def check_if_in_per_cfg_unit_cfg(self, cfg, symbol):
        """Check if the symbol is defined in the aggregated unit config files."""
        return (
                cfg in self._per_type_unit_configs and
                symbol in self._per_type_unit_configs[cfg])

    def get_per_unit_cfg(self):
        """Get io-signals for all units, per unit, for a given project.

        If 'all' is given as a project, all signals, regardless of configuration,
        is returned.

        Returns:
            dict: a dict with the below format::

            {'NAME_OF_UNIT': {
                'core': {'Events': {},
                         'FIDs': {},
                         'IUMPR': {},
                         'Ranking': {},
                         'TstId': {}},
                'dids': {},
                'inports': {'VARIABLE_NAME': {'class': 'CVC_DISP',
                                                        'configs': [['all']],
                                                        'description': 'Torque '
                                                                        'arbitraion '
                                                                        'state',
                                                        'handle': 'VcPemAlc/VcPemAlc/...',
                                                        'lsb': 1,
                                                        'max': 9,
                                                        'min': 0,
                                                        'name': 'rVcPemAlc_D_AuxLoadEvent',
                                                        'offset': 0,
                                                        'type': 'UInt8',
                                                        'unit': '-'}
                            },
                'outports' : {},
                'nvm' : {}
                }
            }

        """
        return self._per_unit_configs

    def get_per_unit_cfg_total(self):
        """Get total io-signals configuration for all units, per unit, for a given project.

        Does not remove signals disabled by code switches.

        Returns:
            dict: a dict with the below format::

            {'NAME_OF_UNIT': {
                'core': {'Events': {},
                         'FIDs': {},
                         'IUMPR': {},
                         'Ranking': {},
                         'TstId': {}},
                'dids': {},
                'inports': {'VARIABLE_NAME': {'class': 'CVC_DISP',
                                                        'configs': [['all']],
                                                        'description': 'Torque '
                                                                        'arbitraion '
                                                                        'state',
                                                        'handle': 'VcPemAlc/VcPemAlc/...',
                                                        'lsb': 1,
                                                        'max': 9,
                                                        'min': 0,
                                                        'name': 'rVcPemAlc_D_AuxLoadEvent',
                                                        'offset': 0,
                                                        'type': 'UInt8',
                                                        'unit': '-'}
                            },
                'outports' : {},
                'nvm' : {}
                }
            }

        """
        res = {}
        for unit in self._build_prj_config.get_included_units():
            try:
                res[unit] = self._raw_per_unit_configs[unit]
            except KeyError:
                continue
        return res

    def get_unit_config(self, unit):
        """Get config for a unit.

        Arguments:
        unit (str): Unit to get config for
        """
        return self._raw_per_unit_configs[unit]

    @staticmethod
    def get_base_name(unit):
        """Get base name of unit."""
        return unit.partition('__')[0]

    def get_unit_code_generator(self, unit):
        """Get code generator for a given a unit (model).

        Args:
            unit (str): Current unit/model name.
        Returns:
            code_generator (str): Code generator used for given model.
        """
        per_unit_cfg = self.get_per_unit_cfg()
        if unit in per_unit_cfg and 'code_generator' in per_unit_cfg[unit]:
            code_generator = per_unit_cfg[unit]['code_generator']
        else:
            # Default to target_link
            code_generator = CodeGenerators.target_link
        return code_generator

    def _get_code_generators(self):
        per_unit_cfg = self.get_per_unit_cfg()
        code_generators = set()
        for _, config in per_unit_cfg.items():
            if 'code_generator' in config:
                code_generators.add(config['code_generator'])
            else:
                # Default to target_link
                code_generators.add(CodeGenerators.target_link)
        return code_generators

    def _get_base_types_headers(self):
        general_includes = ''
        if CodeGenerators.embedded_coder in self.code_generators:
            general_includes += '#include "rtwtypes.h"\n'
        if CodeGenerators.target_link in self.code_generators:
            general_includes += '#include "tl_basetypes.h"\n'
        return general_includes
