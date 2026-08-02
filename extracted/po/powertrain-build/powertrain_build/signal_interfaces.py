# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Signal interface module.

Module for parsing the external signal interface definition files, and
checking the signal interfaces between Supplier and VCC sw,
and also internally between VCC sw-units.
"""
import re
import csv
import time
import copy
from pprint import pformat
from pathlib import Path
from collections import defaultdict

from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.feature_configs import FeatureConfigs
from powertrain_build.lib.helper_functions import deep_dict_update
from powertrain_build.problem_logger import ProblemLogger
from powertrain_build.types import get_ec_type
from powertrain_build.unit_configs import UnitConfigs, CodeGenerators
from powertrain_build.user_defined_types import UserDefinedTypes


class CsvReaderCounter:
    """Csv wrapper to keep track of file row."""

    def __init__(self, _csvreader):
        """Init."""
        self.csvreader = _csvreader
        self.counter = 0

    def __iter__(self):
        """Iterate."""
        return self

    def __next__(self):
        """Next."""
        self.counter += 1
        return next(self.csvreader)

    def get_count(self):
        """Get current row number."""
        return self.counter


class InterfaceValueException(Exception):
    """Exception for errors interface list."""

    def __init__(self, signal_name, erroneous_field):
        """Init."""
        self.erroneous_field = erroneous_field
        self.signal_name = signal_name


class SignalInterfaces(ProblemLogger):
    """Base class for signal interfaces."""

    def __init__(self, unit_cfg, model_names=None):

        self._unit_cfg = unit_cfg
        self._signals_ext_nok = {'inports': {}, 'outports': {}}
        self._signals_ext_ok = {'inports': {}, 'outports': {}}
        self._result = self.__ddict_factory()

        if model_names is None:
            self.models_to_check = set()
        else:
            self.models_to_check = set(model_names)

    def get_external_outputs(self):
        """Get the external outputs.

        Should be implemented by the subclasses.

        Returns:
            dict: External outputs
        """
        raise NotImplementedError

    def get_external_inputs(self):
        """Get the internal outputs.

        Should be implemented by the subclasses.

        Returns:
            dict: Internal outputs
        """
        raise NotImplementedError

    @classmethod
    def __ddict_factory(cls):
        """Generate recursive defaultdict."""
        return defaultdict(cls.__ddict_factory)

    @property
    def should_all_models_be_checked(self):
        """True if there are no specific models to be checked

        :rtype: bool
        """
        return len(self.models_to_check) == 0

    def should_check_model(self, model_name):
        """True if MODEL_NAME is in SELF.MODEL_NAMES

        :rtype: bool
        """
        return self.should_all_models_be_checked or model_name in self.models_to_check

    def contains_model_to_check(self, model_names):
        """True if MODEL_NAMES contains a model in SELF.MODEL_NAMES

        :param model_names: iterable
        :rtype: bool
        """
        return any((m in self.models_to_check for m in model_names))

    @staticmethod
    def _eq_var(var_a, var_b, par):
        """Check if variables are equal, with some modifications.

        par contains the key for which type of parameter is compared
        E.g. nan is equal to '-' and ''. Furthermore, all variables
        are converted to strings before making the comparison.
        """
        a_s = str(var_a)
        b_s = str(var_b)
        if par in ['min', 'max']:
            a_s = re.sub('nan', '-', a_s)
            b_s = re.sub('nan', '-', b_s)
            if re.match(r'[-+.0-9eE]+', a_s) and re.match(r'[-+.0-9eE]+', b_s):
                try:
                    a_f = float(var_a)
                    b_f = float(var_b)
                    return a_f == b_f
                except ValueError:
                    pass
        return a_s == b_s

    def _check_var_def(self, ext_def, unit_def):
        """Check that the parameters for the variable definitions are the same.

        Check that the parameters are the same for all units that use the parameter.
        """
        res = {}
        ignored_parameters = ['class', 'configs', 'handle', 'default', 'description', 'unit']
        for unit, unit_definitions in unit_def.items():
            for parameter, definition in ext_def.items():
                if parameter in ignored_parameters or parameter not in unit_definitions:
                    continue
                unit_definition = unit_definitions[parameter]
                if not self._eq_var(definition, unit_definition, parameter):
                    res.setdefault(unit, {})[parameter] = f"{definition} != {unit_definition}"

        return res if res else None

    def _add_incons_to_ext_dict(self, res, var, incons):
        """Add inconsistencies to the ext dict."""
        if incons is not None:
            for unit, incon in incons.items():
                if self.should_check_model(unit):
                    if var in res['inconsistent_defs'][unit]:
                        res['inconsistent_defs'][unit][var].update(incon)
                    else:
                        res['inconsistent_defs'][unit][var] = incon

    def _add_incons_to_dict(self, res, var, incons):
        """Add iconsistent data to a dict."""
        if incons is not None:
            for unit, incon in incons.items():
                if self.should_check_model(unit):
                    if var in res[unit]['inconsistent_defs']:
                        res[unit]['inconsistent_defs'][var].update(incon)
                    else:
                        res[unit]['inconsistent_defs'][var] = incon

    def _gen_int_outp_set(self, tot_unit_cfg):
        """Generate a set of signals to check for internal output parameters."""
        tot_cfg = tot_unit_cfg.get('outports', {})
        external_ports = {**self._signals_ext_ok['outports'], **self._signals_ext_nok['outports']}

        # only check outports that are not defined in the external io definition
        non_ext_outp = set(tot_cfg.keys()) - set(external_ports.keys())
        return non_ext_outp

    def _gen_int_inp_set(self, tot_unit_cfg):
        """Generate a set of signals to check for internal input parameters."""
        tot_cfg = tot_unit_cfg.get('inports', {})
        external_ports = {**self._signals_ext_ok['inports'], **self._signals_ext_nok['inports']}

        # only check inports that are not defined in the external io definition
        non_ext_inp = set(tot_cfg.keys()) - set(external_ports.keys())
        return non_ext_inp

    def _gen_unit_var_dict(self, res, chk_type, variables, in_out):
        """Generate a dict with vars as keys, and units in which they are used as a list."""
        tot_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        for var in variables:
            for unit in tot_cfg[in_out][var]:
                if self.should_check_model(unit):
                    if var in res[unit][chk_type]:
                        res[unit][chk_type][var] = {}
                    else:
                        res[unit][chk_type][var] = {}

    def _check_external_outp(self):
        """Check that all external outputs (VCC -> supplier).

        Check that all external outputs are produced,
        that consumed signals (Supplier -> VCC) are defined as inputs
        in the external IO definition file, and that the signal
        definitions are consistent between io and unit definitions.
        """
        ext_out = self.get_external_outputs()
        tot_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        res = self._result['sigs']['ext']
        # check that all output signals are produced by VCC SW
        if 'outports' in tot_cfg:
            for _, data in ext_out.items():
                for var, var_def in data.items():
                    if var not in tot_cfg['outports']:
                        res['missing'][var] = {}
                        self._signals_ext_nok['outports'][var] = var_def
                    else:
                        self._signals_ext_ok['outports'][var] = var_def
                        tmp = self._check_var_def(var_def, tot_cfg['outports'][var])
                        self._add_incons_to_ext_dict(res, var, tmp)

    def _check_external_inp(self):
        """Check all external input signals.

        Check that outputs are produced and,
        that consumed signals are defined as inputs
        in the external IO definition file.
        """
        ext_inp = self.get_external_inputs()
        # self.debug('ext_inp: %s', pformat(ext_inp))
        tot_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        res = self._result['sigs']['ext']
        # check that all input signals are used by VCC SW
        if 'inports' in tot_cfg:
            for data in ext_inp.values():
                for var, var_def in data.items():
                    if var not in tot_cfg['inports']:
                        if var not in res['unused']:
                            res['unused'][var] = {}
                        self._signals_ext_nok['inports'][var] = var_def
                    else:
                        self._signals_ext_ok['inports'][var] = var_def
                        tmp = self._check_var_def(var_def, tot_cfg['inports'][var])
                        self._add_incons_to_ext_dict(res, var, tmp)

    def _check_internal_io(self):
        """Check internal signal io.

        Function which checks that:
        1. all signals consumed in models, are produced
        in antoher model.
        2. all outputs are consumed (warning)
        3. check that all signal definitions are the same as the producing unit.
        4. a signal is only produced in one model (per prj).
        this function return a tuple with the above content

        TODO:
            Shall we add a check for multiple inputs of the same signal?*
        """
        tot_cfg = self._unit_cfg.get_per_cfg_unit_cfg()
        internal_inport_signals = self._gen_int_inp_set(tot_cfg)
        internal_outport_signals = self._gen_int_outp_set(tot_cfg)
        all_outports = set(tot_cfg.get('outports', {}).keys())
        res = self._result['sigs']['int']
        # 1. all signals consumed in models, are produced in another model.
        missing = internal_inport_signals - all_outports
        self._gen_unit_var_dict(res, 'missing', missing, 'inports')  # error!
        # 2. all outputs are consumed (warning)
        unused = internal_outport_signals - internal_inport_signals
        self._gen_unit_var_dict(res, 'unused', unused, 'outports')  # warning?
        # 3. check that all signal definitions are the same as the producing
        # unit.
        input_signals_to_check = internal_inport_signals - missing
        for signal in input_signals_to_check:
            unit_key = list(tot_cfg['outports'][signal].keys())
            # if output is defined in multiple functions, test #4 will catch this
            if len(unit_key) == 1:
                outport_def = tot_cfg['outports'][signal][unit_key[0]]
                tmp = self._check_var_def(outport_def,
                                          tot_cfg['inports'][signal])
                self._add_incons_to_dict(res, signal, tmp)

        # 4. check that we have not screwed up any of the consuming models
        external_signals_to_check = internal_outport_signals - unused
        for signal in external_signals_to_check:
            unit_keys = list(tot_cfg['inports'][signal].keys())
            my_outport_definition = tot_cfg['outports'][signal]
            for unit_key in unit_keys:
                others_inport_def = tot_cfg['inports'][signal][unit_key]
                tmp = self._check_var_def(others_inport_def,
                                          my_outport_definition)
                self._add_incons_to_dict(res, signal, tmp)

        # 5. there should only be one outport per config.
        multiple_defs = []
        if 'outports' in tot_cfg:
            multiple_defs = [x for x in tot_cfg['outports']
                             if len(tot_cfg['outports'][x]) > 1]
        self._gen_unit_var_dict(res, 'multiple_defs', multiple_defs, 'outports')

    def _check_config(self):
        """Check the interfaces given a certain project config.

        The result of the checks is stored in the dict self._result
        """
        # reset the handled external signals for each configuration
        self._signals_ext_ok = {'inports': {}, 'outports': {}}
        # has to be done in this order since there is an implicit dependency
        # to self._signals_ext_ok
        self._check_external_outp()
        self._check_external_inp()
        self._check_internal_io()

    def check_config(self):
        """Check configurations for specific project.

        Returns:
            dict: the result of the check with the following format

        ::

            {
                "sigs": { "ext": {"missing": {},
                                  "unused": {},
                                  "inconsistent_defs": {}},
                          "int": {"UNIT_NAME": {"missing": {},
                                                "unused": {},
                                                "multiple_defs": {}
                                                "inconsistent_defs": {}}
                }
            }

        """
        self._result = self.__ddict_factory()
        self._check_config()
        # self.debug("%s", pformat(self._result))
        # restore the current conofiguration

        return self._result


class YamlSignalInterfaces(SignalInterfaces):
    """Interface configurations defined in yaml files."""

    @staticmethod
    def from_config_file(project_config_path):
        """Create a YamlSignalInterfaces instance from a project config file.

        Args:
            project_config_path (str): path to the project config file

        Returns:
            YamlSignalInterfaces: instance of YamlSignalInterfaces
        """
        build_project_config = BuildProjConfig(project_config_path)
        feature_cfg = FeatureConfigs(build_project_config)
        unit_config = UnitConfigs(build_project_config, feature_cfg)
        user_defined_types = UserDefinedTypes(build_project_config, unit_config)

        return YamlSignalInterfaces(
            prj_cfg=build_project_config,
            unit_cfg=unit_config,
            feature_cfg=feature_cfg,
            user_defined_types=user_defined_types
        )

    def __init__(self, prj_cfg, unit_cfg, feature_cfg, user_defined_types, model_names=None):
        """Class initializer.

        Args:
            prj_cfg (BuildProjConfig): configures which units are active in the current project.
            unit_cfg (UnitConfigs): class instance containing all the unit configuration parameters.
            feature_cfg (FeatureConfig): Feature configs from SPM_Codeswitch_Setup.
            user_defined_types (UserDefinedTypes): Class holding user defined data types.
            model_names (set): models that should be included in the check, default is all models
        """
        super().__init__(unit_cfg, model_names=model_names)

        # Postpone imports to here to work on machines without PyYaml installed
        from powertrain_build.interface.base import filter_signals
        from powertrain_build.interface.application import Application, get_internal_domain
        from powertrain_build.interface.generation_utils import get_interface, get_method_interface
        from powertrain_build.interface.hal import HALA
        from powertrain_build.interface.device_proxy import DPAL
        from powertrain_build.interface.zone_controller import ZCAL
        from powertrain_build.interface.service import ServiceFramework

        app = Application()
        app.pybuild['build_cfg'] = prj_cfg
        app.name = app.pybuild['build_cfg'].name
        app.pybuild['feature_cfg'] = feature_cfg
        app.pybuild['unit_vars'] = unit_cfg.get_per_unit_cfg_total()
        app.pybuild['user_defined_types'] = user_defined_types

        translation_files = app.get_translation_files()

        ecu_supplier = prj_cfg.get_ecu_info()[0]
        self.zc_spec = {}
        self.hal_spec = {}
        self.dp_spec = {}
        self.sfw_spec = {}
        self.sa_spec = {}
        self.service_spec = {}
        self.mthd_spec = {}
        if prj_cfg.get_code_generation_config(item='generateYamlInterfaceFile'):
            zc_app = ZCAL(app)
            self.zc_spec = get_interface(app, zc_app)
            self.composition_spec = zc_app.composition_spec
        elif ecu_supplier == 'HI':
            hi_app = DPAL(app)
            self.dp_spec = get_interface(app, hi_app)
        else:
            hala = HALA(app)
            dp = DPAL(app)
            swf = ServiceFramework(app)
            hala.parse_definition(translation_files)
            self.dp_spec = get_interface(app, dp)
            self.sfw_spec = get_interface(app, swf)
            self.mthd_spec = get_method_interface(app)
            self.service_spec = self.get_availability(app, unit_cfg.code_generators)
            rasters = app.get_rasters()
            self.debug('Rasters: %s', rasters)
            internal = get_internal_domain(rasters)
            properties_from_json = [
                {"destination": "min", "source": "min", "default": "-"},
                {"destination": "max", "source": "max", "default": "-"},
                {"destination": "variable_type", "source": "type"},
                {"destination": "offset", "source": "offset", "default": "-"},
                {"destination": "factor", "source": "lsb", "default": 1},
                {"destination": "description", "source": "description"},
                {"destination": "unit", "source": "unit", "default": "-"},
            ]
            for raster in rasters:
                hala.name = raster.name
                hala.clear_signal_names()
                hala.add_signals(filter_signals(raster.insignals, internal), 'insignals', properties_from_json)
                hala.add_signals(raster.outsignals, 'outsignals', properties_from_json)
                self.debug('Current HALA: %s', hala)
                self.hal_spec[raster.name] = hala.to_dict()

    @staticmethod
    def get_availability(app, code_generators={CodeGenerators.target_link}):
        """Get the availability of services.

        Args:
            app (Application): Application instance
            code_generators (set): Code generators to include in the availability check

        Returns:
            dict: Availability of services
        """
        tl_type = 'Bool'
        variable_type = tl_type if CodeGenerators.target_link in code_generators else get_ec_type(tl_type)
        services = app.get_service_mapping()
        spec = {}
        for interface, service in services.items():
            camel_interface = ''.join(part.title() for part in interface.split('_'))
            spec[interface] = {
                'variable': f'yVcSfw_B_{camel_interface}IsAvailable',
                'variable_type': variable_type,
                'property_type': 'bool',
                'service': service,
                'default': 0,
                'length': 1,
                'property': 'inherent',
                'offset': '-',
                'factor': 1,
                'range': {'min': '0', 'max': '1'},
                'init': 0,
                'description': f'Availability of {interface} in {service}',
                'unit': '-',
                'group': None,
                'model': interface
            }
        return spec

    def get_externally_defined_ports(self):
        """Get ports defined by suppliers."""
        outports = []
        for raster in self.dp_spec.values():
            for spec in raster['consumer']:
                outports.append(spec['variable'])
        for raster in self.hal_spec.values():
            for spec in raster['consumer']:
                outports.append(spec['variable'])
        for raster in self.sfw_spec.values():
            for spec in raster['consumer']:
                outports.append(spec['variable'])
        for raster in self.sa_spec.values():
            for spec in raster['consumer']:
                outports.append(spec['variable'])
        for raster in self.zc_spec.values():
            for spec in raster['consumer']:
                outports.append(spec['variable'])
        return outports

    def get_external_io(self):
        """Get the variable definitions for the signal IO for a given config.

        Returns:
            dict: Variable definitions for the supplier in-/out-put signals for the configuration
        """
        def normalize_spec(spec):
            """ Convert Yaml spec to normal pybuild spec.

            Arguments:
                spec (dict): Yaml specification of signal
            Returns:
                spec (dict): Pybuild specification of signal
            """
            spec2 = copy.copy(spec)  # copy by value
            spec2['type'] = spec['variable_type']
            spec2['min'] = spec['range']['min']
            spec2['max'] = spec['range']['max']
            return spec2

        def set_spec(target):
            new_spec = normalize_spec(spec)
            if new_spec.get('debug'):
                debug[target][spec['variable']] = new_spec
            elif spec.get('dependability'):
                dependability[target][spec['variable']] = new_spec
            else:
                normal[target][spec['variable']] = new_spec

        normal = {}
        dependability = {}
        secure = {}  # Only supported by CSV interfaces
        debug = {}

        for field in ['input', 'output', 'status']:
            normal[field] = {}
            dependability[field] = {}
            debug[field] = {}

        spec_confs = [self.dp_spec, self.sfw_spec, self.sa_spec, self.hal_spec, self.zc_spec]
        for spec_conf in spec_confs:
            for raster in spec_conf.values():
                for spec in raster['consumer']:
                    set_spec("input")
                for spec in raster['producer']:
                    set_spec("output")
        for spec in self.service_spec.values():
            set_spec('status')
        for method_data in self.mthd_spec.values():
            for _, spec in method_data['ports']['out'].items():
                set_spec('input')
            for _, spec in method_data['ports']['in'].items():
                set_spec('output')
        return normal, dependability, secure, debug

    def get_external_signals(self, find_output=True):
        """Get the external signals.

        Args:
            find_output (bool): True if output signals should be returned, False if input signals should be returned

        Returns:
            dict: External signals
        """
        io_type = self.get_external_io()  # (normal, dependability, secure (unsupported), debug)
        directional_io = defaultdict(dict)
        for io in io_type:
            for signal_type, signals in io.items():
                if find_output and signal_type == 'output':
                    directional_io[signal_type].update(signals)
                elif not find_output and signal_type == 'input':
                    directional_io[signal_type].update(signals)
        return directional_io

    def get_external_outputs(self):
        return self.get_external_signals(True)

    def get_external_inputs(self):
        return self.get_external_signals(False)


class CsvSignalInterfaces(SignalInterfaces):
    """Interface configurations for all units and all configs.

    Provides methods for retrieving the currently
    used signal configurations of a unit.
    """

    convs = (('~=', '!='), ('~', ' not '), ('!', ' not '), (r'\&\&', ' and '),
             (r'\|\|', ' or '))
    # Common excel sheet definitions, adapted for CVS.
    VAR_COL = 0  # Variable name
    DATA_COL = 2  # Type, min, max, unit, comment, init
    PROJ_COL = 9  # Variable number of projects
    HEADER_ROW = 3  # which row the header info is found
    DATA_ROW = 5  # the row which data starts
    WS_NAMES = ['EMS-Output', 'EMS-Input', 'LIN-Output', 'LIN-Input',
                'CAN-Output', 'CAN-Input', 'Private CAN-Output',
                'Private CAN-Input']

    def __init__(self, prj_cfg, unit_cfg, models=None):
        """Class initializer.

        Args:
            prj_cfg (BuildProjConfig): configures which units are active in the
                                              current project
            unit_cfg (UnitConfigs): class instance containing all the unit
                                    configuration parameters
            models (str or list): Models to get interface for. default: 'all'

        """
        super().__init__(unit_cfg, model_names=models)
        self.interfaces = {}

        self.__prjs = {}
        self.__out_dict = {}
        self.__all_prjs = set()
        self.__prj2col = {}
        self.__prj_col_range = {}

        prj2index = {}
        self.name = prj_cfg.get_prj_config()
        file_path = prj_cfg.get_if_cfg_dir()
        self._prj_cfg = prj_cfg
        self._parse_io_cnfg(file_path)
        for k in self.__prj2col:
            self.__prj2col[k] = prj2index

    def _parse_io_cnfg(self, interface_directory):
        """Parse the CSV config files."""
        start_time = time.time()
        self.info('******************************************************')
        self.info('Start parsing SPM-Interface definition files')
        for ws_name in self.WS_NAMES:
            self.debug("read sheet %s start", ws_name)
            file_path = Path(interface_directory, ws_name + '.csv')
            try:
                with open(file_path, newline='') as fhandle:
                    if ws_name not in self.interfaces:
                        self.interfaces.update({ws_name: {}})
                    interface = self.interfaces[ws_name]
                    csvreader = csv.reader(fhandle, delimiter=';', strict=True)
                    csvreader = CsvReaderCounter(csvreader)
                    try:
                        for _ in range(self.HEADER_ROW-1):
                            next(csvreader)
                        row = next(csvreader)
                        # TODO: Find why excel export script sometimes skips first field
                        #       on each line if field is empty.
                        #       Workaround:
                        row = row[1:] if row[0] == '' else row
                        try:
                            col = self._get_proj_col(row)
                        except IndexError:
                            self.warning('Project %s not defined in %s', self.name, file_path.stem)
                            continue

                        for _ in range(self.HEADER_ROW, self.DATA_ROW-1):
                            next(csvreader)
                    except StopIteration:
                        self.critical('File %s has bad format, not enough header rows', file_path.stem)
                    for row in csvreader:
                        row = row[1:] if row[0] == '' else row
                        try:
                            signal, data = self._get_var_def(row)
                            data.update({'element_index': csvreader.get_count()})
                        except InterfaceValueException as interface_exception:
                            self.critical('Missing value for key "%s" in list "%s" at index "%s"',
                                          interface_exception.erroneous_field,
                                          file_path.stem, csvreader.get_count())
                            continue
                        if signal not in interface:
                            interface.update({signal: data})
                        interface[signal]['IOType'] = row[col].lower()
                self.debug("read sheet %s end", ws_name)
            except FileNotFoundError:
                self.info('Project %s does not have a %s', self.name, ws_name)
        self.info('Finished parsing SPM-Interface definition file (in %4.2f s)', time.time() - start_time)

    def __repr__(self):
        """Get string representation of object."""
        return pformat(self.__out_dict)

    def _get_proj_col(self, row):
        """Get the projects in the config document.

        Parses supplied worksheet row and finds all the projects defined, and
        stores the result in the class variable __all_prjs.
        Furthermore, a dict prj2col, maps the project name to a list index
        in the prj key in the __out_dict dict, and
        sets the class variables __prj2col, and __prj_col_range contains
        a list with column indexes in the excel sheet, used for parsing the
        excel, the result is stored in the interal __out_dict

        interfaces example:

        ::

            {
                'CAN-Input': {
                    'sVCcm_D_HvacCoolgEnaRe': {
                        'IOType': 'd'
                        'description': 'Enable Ac rear HVAC',
                        'init': 0,
                        'max': 1,
                        'min': 0,
                        'type': 'UInt8',
                        'unit': '-'
                    }
                }
            }

        """
        col = self.PROJ_COL
        while row[col] is not None and row[col] != '':
            if row[col] == self.name:
                return col
            col += 1
            if col > 200:
                break

        raise IndexError

    @staticmethod
    def _get_var_def(row):
        """Get the variable definition from a row in a sheet.

        Returns:
            dict: with var definitions

        """
        keys = ['type', 'min', 'max', 'unit', 'description', 'init']

        vals = []
        for col in [0, 2, 3, 4, 5, 6, 7]:
            val = row[col]
            if isinstance(val, str):
                val = val.strip()
                if re.fullmatch('[+-]?[0-9]+', val):
                    val = int(val)
                elif re.fullmatch('[+-]?[0-9.,]+', val):
                    val = float(val.replace(',', '.'))
            vals.append(val)
        critical_attributes = ['type']
        signal_name = vals[0]
        signal_attributes = dict(zip(keys, vals[1:]))
        for field in critical_attributes:
            if signal_attributes[field] == '':
                raise InterfaceValueException(signal_name, field)
        return signal_name, signal_attributes

    def get_raw_io_cnfg(self):
        """Get the raw IO-Config parsed from the config file.

        Returns:
            dict: raw configuration information from the config file

        dict example:

        ::

            {
                'CAN-Input': {
                    'sVCcm_D_HvacCoolgEnaRe': {
                        'description': 'Enable Ac rear HVAC',
                        'init': 0,
                        'max': 1,
                        'min': 0,
                        'project_def': 'D',
                        'type': 'UInt8',
                        'unit': '-'
                    }
                }
            }


        """
        return self.interfaces

    def get_io_config(self):
        """Get an IO-Config for a specific project.

        Returns:
            tuple: a tuple with three dicts - (nrm_dict, dep_dict, dbg_dict)

        """
        normal = {}
        dep = {}
        secure = {}
        debug = {}
        for interface_name, interface in self.interfaces.items():
            normal[interface_name] = {}
            dep[interface_name] = {}
            secure[interface_name] = {}
            debug[interface_name] = {}
            for signal_name, signal in interface.items():
                prj_def = signal.get('IOType', '-')
                if prj_def in 'xd':
                    normal[interface_name][signal_name] = copy.deepcopy(signal)
                elif prj_def in 's':
                    dep[interface_name][signal_name] = copy.deepcopy(signal)
                elif prj_def == 'sc':
                    secure[interface_name][signal_name] = copy.deepcopy(signal)
                if prj_def in 'd':
                    debug[interface_name][signal_name] = copy.deepcopy(signal)
        return normal, dep, secure, debug

    def get_external_io(self):
        """Get the variable definitions for the signal IO for a given config.

        Returns:
            dict: Variable definitions for the supplier in-/out-put signals for the configuration

        """
        return self.get_io_config()

    def get_external_inputs(self):
        """Get variable definitions for the supplier signal Inputs.

        Returns:
            dict: variable definitions for the supplier input signals

        """
        cfg, cfg_dep, cfg_sec = self.get_io_config()[:3]
        deep_dict_update(cfg, cfg_dep)
        deep_dict_update(cfg, cfg_sec)
        out = {}
        for key, value in cfg.items():
            if re.match('.*Input$', key) is not None:
                out[key] = value
        return out

    def get_external_outputs(self):
        """Get variable definitions for the supplier signal Outputs.

        Returns:
            dict: variable definitions for the supplier output signals

        """
        cfg, cfg_dep, cfg_sec = self.get_io_config()[:3]
        deep_dict_update(cfg, cfg_dep)
        deep_dict_update(cfg, cfg_sec)
        out = {}
        for key, value in cfg.items():
            if re.match(r'.*Output$', key) is not None:
                out[key] = value
        return out

    def get_externally_defined_ports(self):
        """Get ports defined by suppliers."""
        externally_defined_ports = set()
        external_outports = self.get_external_outputs()
        for external_ports in external_outports.values():
            externally_defined_ports.update(external_ports)
        external_inports = self.get_external_inputs()
        for external_ports in external_inports.values():
            externally_defined_ports.update(external_ports)
        return list(externally_defined_ports)
