# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-

"""Python module for abstracting Pybuild applications"""
from pathlib import Path
import json

from powertrain_build.interface.base import BaseApplication, Signal, MultipleProducersError, Domain, Interface
from powertrain_build.lib import logger
from powertrain_build.build_proj_config import BuildProjConfig
from powertrain_build.feature_configs import FeatureConfigs
from powertrain_build.unit_configs import UnitConfigs
from powertrain_build.user_defined_types import UserDefinedTypes


LOGGER = logger.create_logger("application")


def get_raster_to_raster_interfaces(rasters):
    """Generate a list of Interfaces for internal raster-to-raster signals.

    Args:
        rasters (list): Input rasters (from app.get_rasters())
    Returns:
        interfaces (list(interfaces)): List of unique raster-to-raster-interfaces.
    """
    raster_pairs = []
    for current_raster in rasters:
        for corresponding_raster in [r for r in rasters if r != current_raster]:
            # If we have interface a_b, no need to produce b_a.
            if (corresponding_raster, current_raster) not in raster_pairs:
                raster_pairs.append((current_raster, corresponding_raster))

    return [Interface(raster[0], raster[1]) for raster in raster_pairs]


def get_internal_domain(rasters):
    """ Create an internal domain of signals

    Loops through all raster<->raster communications and adds them to a domain object

    Args:
        rasters (list(Raster)): rasters to calculate communication for
    Returns:
        domain (Domain): signals belonging to the same domain
    """
    internal = Domain()
    internal.set_name("internal")
    for interface in get_raster_to_raster_interfaces(rasters):
        internal.add_interface(interface)

    return internal


def get_active_signals(signals, feature_cfg):
    """ Filter out inactive signals. """
    LOGGER.debug('Filtering %s', signals)
    return [signal for signal in signals if feature_cfg.check_if_active_in_config(signal.properties['configs'])]


class Application(BaseApplication):
    """ Object for holding information about a pybuild project """
    def __init__(self):
        self.name = None
        self.pybuild = {'build_cfg': None,
                        'feature_cfg': None,
                        'unit_vars': {}}
        self._insignals = None
        self._outsignals = None
        self._signals = None
        self._raster_definitions = []
        self._services = None
        self._methods = []
        self._enumerations = None
        self._structs = None

    def parse_definition(self, definition):
        """ Parse ProjectCfg.json, get code switch values and read config.json files.
        Add the information to the object.

        Args:
            definition (Path): Path to ProjectCfg.json
        """
        self.pybuild['build_cfg'] = BuildProjConfig(str(definition))
        self.name = self.pybuild['build_cfg'].name
        self.pybuild['feature_cfg'] = FeatureConfigs(self.pybuild['build_cfg'])
        unit_cfg = UnitConfigs(self.pybuild['build_cfg'], self.pybuild['feature_cfg'])
        self.pybuild['unit_vars'] = unit_cfg.get_per_unit_cfg()
        self.pybuild['user_defined_types'] = UserDefinedTypes(self.pybuild['build_cfg'], unit_cfg)

    def get_domain_names(self):
        """ Get domain names. """
        return self.pybuild['build_cfg'].device_domains.values()

    def get_domain_mapping(self):
        """ Get device to signal domain mapping. """
        return self.pybuild['build_cfg'].device_domains

    def get_methods(self):
        """ Get csp methods. """
        if self._signals is None:
            self._get_signals()
        return self._methods

    @property
    def enumerations(self):
        """ Get enumerations defined in the project. """
        if self._enumerations is None:
            self._enumerations = self.pybuild['user_defined_types'].get_enumerations()
        return self._enumerations

    @property
    def structs(self):
        """ Get structs defined in the project. """
        if self._structs is None:
            self._structs = self.pybuild['user_defined_types'].get_structs()
        return self._structs

    @property
    def services(self):
        """ Get interface to service mapping. """
        if self._services is None:
            services_file = self.get_services_file()
            self._services = self.pybuild['build_cfg'].get_services(services_file)
        return self._services

    def get_service_mapping(self):
        """ Get interface to service mapping. """
        return self.services

    def get_services_file(self):
        """ Get path to file specifying interface to service mapping. """
        return self.pybuild['build_cfg'].services_file

    def get_name(self, definition):
        """ Parse ProjectCfg.json and return the specified project name """
        if self.name is None:
            return BuildProjConfig(str(definition)).name
        return self.name

    def _get_signals(self):
        """ Calculate parse all inport and outports of all models """
        self._insignals = set()
        self._outsignals = set()
        defined_ports = {'inports': set(), 'outports': set()}
        for unit, data in self.pybuild['unit_vars'].items():
            self.parse_ports(data, defined_ports, self.pybuild['feature_cfg'], unit)
            self.parse_csp_methods(data, self.pybuild['feature_cfg'], unit)

    def parse_ports(self, port_data, defined_ports, feature_cfg, unit):
        """ Parse ports for one model, based on code switch values.
        Modifies the defined_ports dict and the object.

        Args:
            port_data (dict): port data for a model/unit
            defined_ports (set): all known signals
            feature_cfg (FeatureConfigs): pybuild parsed object for code switches
            unit (string): Name of model/unit
        """
        if self._signals is None:
            self._signals = {}
        for port_type, outport in {'outports': True, 'inports': False}.items():
            for port_name, data in port_data.get(port_type, {}).items():
                # Get what signals we are dealing with
                if not feature_cfg.check_if_active_in_config(data['configs']):
                    continue
                if port_name not in self._signals:
                    signal = Signal(port_name, self)
                    self._signals.update({port_name: signal})
                else:
                    signal = self._signals[port_name]
                # Add information about which models are involved while we are reading it
                if outport:
                    try:
                        signal.set_producer(unit)
                    except MultipleProducersError as mpe:
                        LOGGER.debug(mpe.message)
                        signal.force_producer(unit)
                    self._outsignals.add(port_name)
                else:
                    signal.consumers = unit
                    self._insignals.add(port_name)
                defined_ports[port_type].add(port_name)

    def parse_csp_methods(self, port_data, feature_cfg, unit):
        """ Parse csp methods.

        Args:
            port_data (dict): port data for a model/unit.
            feature_cfg (FeatureConfigs): pybuild parsed object for code switches
            unit (string): Name of model/unit
        """
        if self._signals is None:
            self._signals = {}
        methods = port_data.get('csp', {}).get('methods', {})
        for method_name, data in methods.items():
            if feature_cfg.check_if_active_in_config(data['configs']):
                method = Method(self, unit)
                method.parse_definition((method_name, data))
                self._methods.append(method)

    def get_signal_properties(self, signal):
        """ Get properties for the signal from powertrain_build definition.

        Args:
            signal (Signal): Signal object
        Returns:
            properties (dict): Properties of the signal in pybuild
        """
        # Hack: Take the first consumer or producer if any exists
        for producer in signal.producer:
            return self.pybuild['unit_vars'][producer]['outports'][signal.name]
        for consumer in signal.consumers:
            return self.pybuild['unit_vars'][consumer]['inports'][signal.name]
        return {}

    def get_rasters(self):
        """ Get rasters parsed from powertrain_build.

        Returns:
            rasters (list): rasters parsed from powertrain_build
        """
        if self._signals is None:
            self._get_signals()
        raster_definition = self.pybuild['build_cfg'].get_units_raster_cfg()
        rasters = []
        for raster_field, raster_content in raster_definition.items():
            if raster_field in ['SampleTimes']:
                continue
            for name, content in raster_content.items():
                if name in ['NoSched']:
                    continue
                raster = Raster(self)
                raster.parse_definition((name, content, self._signals))
                rasters.append(raster)
        return rasters

    def get_models(self):
        """ Get models and parse their config files.

        Returns:
            models (list(Model)): config.jsons parsed
        """
        rasters = self.get_rasters()
        # Since one model can exist in many rasters. Find all unique model names first.
        cfg_dirs = self.pybuild['build_cfg'].get_unit_cfg_dirs()
        model_names = set()
        for raster in rasters:
            model_names = model_names.union(raster.models)
        models = []
        for model_name in model_names:
            if model_name not in cfg_dirs:
                LOGGER.debug("%s is generated code. It does not have a config.", model_name)
                continue
            model = Model(self)
            cfg_dir = cfg_dirs[model_name]
            config = Path(cfg_dir, f'config_{model_name}.json')
            model.parse_definition((model_name, config))
            models.append(model)
        return models

    def get_translation_files(self):
        """ Find all yaml files in translation file dirs.

        Returns:
            translation_files (list(Path)): translation files
        """
        translation_files = []
        cfg_dirs = self.pybuild['build_cfg'].get_translation_files_dirs()
        for cfg_dir in cfg_dirs.values():
            cfg_path = Path(cfg_dir)
            translation_files.extend(cfg_path.glob('*.yaml'))
        translation_files = list(set(translation_files))
        return translation_files


class Raster(BaseApplication):
    """ Object for holding information about a raster """
    def __init__(self, app):
        """Construct a new Raster object.

        Args:
            app (powertrain_build.interface.application.Application): Pybuild project raster is part of
        """
        self.app = app
        self.name = str()
        self._insignals = None
        self._outsignals = None
        self._available_signals = None
        self.models = set()

    def parse_definition(self, definition):
        """ Parse the definition from powertrain_build.

        Args:
            definition (tuple):
                name (string): Name of the raster
                content (list): Models in the raster
                app_signals (dict): All signals in all rasters
        """
        self.name = definition[0]
        self.models = set(definition[1])
        self._available_signals = definition[2]

    def _get_signals(self):
        """ Add signals from the project to the raster if they are used here

        Modifies the object itself.
        """
        self._insignals = set()
        self._outsignals = set()
        self._signals = {}
        if self._available_signals is None:
            return
        for signal in self._available_signals.values():
            for consumer in signal.consumers:
                if consumer in self.models:
                    self._signals.update({signal.name: signal})
                    self._insignals.add(signal.name)
            if isinstance(signal.producer, set):
                for producer in signal.producer:
                    if producer in self.models:
                        self._signals.update({signal.name: signal})
                        self._outsignals.add(signal.name)
            else:
                if signal.producer in self.models:
                    self._signals.update({signal.name: signal})
                    self._outsignals.add(signal.name)

    def get_signal_properties(self, signal):
        """ Get properties for the signal from powertrain_build definition.

        Args:
            signal (Signal): Signal object
        Returns:
            properties (dict): Properties of the signal in pybuild
        """
        for producer in signal.producer:
            if producer in self.app.pybuild['unit_vars']:
                return self.app.get_signal_properties(signal)
        return {}


class Model(BaseApplication):
    """ Object for holding information about a model """
    def __init__(self, app):
        self.app = app
        self.name = str()
        self.config = None
        self._insignals = None
        self._outsignals = None
        self._signal_specs = None

    def get_signal_properties(self, signal):
        """ Get properties for the signal from powertrain_build definition.

        Args:
            signal (Signal): Signal object
        Returns:
            properties (dict): Properties of the signal in pybuild
        """
        if self._signal_specs is None:
            self._get_signals()
        if signal.name in self._signal_specs:
            return self._signal_specs[signal.name]
        return {}

    def _get_signals(self):
        """ Add signals from the project to the model if they are used here

        Modifies the object itself.
        Entrypoint for finding signals from the base class.
        """
        self._insignals = set()
        self._outsignals = set()
        self._signals = {}
        self._signal_specs = {}
        self._parse_unit_config(self.config)

    def _parse_unit_config(self, path):
        """ Parse a unit config file.

        Broken out of get_signals to be recursive for included configs.
        """
        cfg = self._load_json(path)
        for signal_spec in cfg['inports'].values():
            signal = Signal(signal_spec['name'], self)
            self._insignals.add(signal.name)
            self._signals.update({signal.name: signal})
            self._signal_specs[signal.name] = signal_spec
        for signal_spec in cfg['outports'].values():
            signal = Signal(signal_spec['name'], self)
            self._outsignals.add(signal.name)
            self._signals.update({signal.name: signal})
            self._signal_specs[signal.name] = signal_spec
        for include_cfg in cfg.get('includes', []):
            LOGGER.debug('%s includes %s in %s', self.name, include_cfg, path.parent)
            include_path = Path(path.parent, f'config_{include_cfg}.json')
            self._parse_unit_config(include_path)

    @staticmethod
    def _load_json(path):
        """ Small function that opens and loads a json file.

        Exists to be mocked in unittests
        """
        with open(path, encoding="utf-8") as fhndl:
            return json.load(fhndl)

    def parse_definition(self, definition):
        """ Parse the definition from powertrain_build.

        Args:
            definition (tuple):
                name (string): Name of the model
                configuration (Path): Path to config file
        """
        self.name = definition[0]
        self.config = definition[1]
        self._get_signals()


class Method(BaseApplication):
    """ Object for holding information about a csp method call """
    def __init__(self, app, unit):
        """Construct a new Method object.

        Args:
            app (powertrain_build.interface.application.Application): Pybuild project raster is part of.
            unit (str): Model that the method is defined in.
        """
        self.app = app
        self.unit = unit
        self.name = str()
        self.namespace = str()
        self.adapter = str()
        self.description = None
        self._signals = {}
        self._insignals = set()
        self._outsignals = set()
        self._primitives = {}
        self._properties = {}

    def parse_definition(self, definition):
        """ Parse the definition from powertrain_build.

        Args:
            definition (tuple):
                name (string): Name of the model
                configuration (dict): Configuration of method
        """
        name = definition[0]
        configuration = definition[1]
        self.name = name
        self.adapter = configuration['adapter']
        self.namespace = configuration['namespace']
        self._primitives[name] = configuration['primitive']
        if 'description' in configuration:
            self.description = configuration['description']
        signals = configuration.get('ports', {})
        outsignals = signals.get('out', {})
        for signal_name, signal_data in outsignals.items():
            signal = self._add_signal(signal_name)
            signal.consumers = name
            signal.set_producer(name)
            self._primitives[signal_name] = signal_data['primitive']
            self._properties[signal_name] = signal_data
            self._outsignals.add(signal_name)
        insignals = signals.get('in', {})
        for signal_name, signal_data in insignals.items():
            signal = self._add_signal(signal_name)
            signal.consumers = name
            signal.set_producer(name)
            self._insignals.add(signal_name)
            self._primitives[signal_name] = signal_data['primitive']
            self._properties[signal_name] = signal_data

    def _add_signal(self, signal_name):
        """ Add a signal used by the method.

        Args:
            signal_name (str): Name of the signal
        """
        if signal_name not in self._signals:
            signal = Signal(signal_name, self)
            self._signals.update({signal_name: signal})
        else:
            signal = self._signals[signal_name]
        return signal

    def get_signal_properties(self, signal):
        """ Get properties for the signal from csp method configuration.

        Args:
            signal (Signal): Signal object
        Returns:
            properties (dict): Properties of the signal in pybuild
        """
        return self._properties[signal.name]

    def get_primitive(self, primitive_name):
        """ Get primitive.

        Args:
            primitive_name (str): Name of primitive part
        Returns:
            primitive (str): Primitive
        """
        return self._primitives[primitive_name]
