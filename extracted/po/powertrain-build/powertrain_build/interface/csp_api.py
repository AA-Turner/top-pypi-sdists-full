# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for CSP API abstraction."""

import enum
from ruamel.yaml import YAML
from abc import abstractmethod
from powertrain_build.interface.base import BaseApplication, Signal
from powertrain_build.lib import logger

LOGGER = logger.create_logger("service")


class MissingApi(Exception):
    """Exception to raise when api is missing"""
    def __init__(self, api, map_file):
        self.message = f"Api {api} missing from {map_file}"


class BadYamlFormat(Exception):
    """Exception to raise when in/out signal is not defined."""
    def __init__(self, api, signal_name):
        self.message = f"Signal {signal_name} for {api} should be set as insignal or outsignal."


class CspApi(BaseApplication):
    """Abstraction for HAL and SFW"""
    position = enum.Enum(
        'Position',
        names=[
            "property_name",
            "property_type",
            "variable_type",
            "offset",
            "factor",
            "default",
            "length",
            "min",
            "max",
            "enum",
            "init",
            "description",
            "unit",
            "endpoint",
            "api",
            "variant",
            "strategy",
            "debug",
            "dependability"
        ]
    )

    def __init__(self, base_application, read_strategy='Always'):
        """Create the interface object

        Args:
            base_application (BaseApplication): Primary object of an interface
                                                Usually a raster, but can be an application or a model too.
        """
        self.name = ""
        self.translations = {}
        self.api_side = False
        # we only care when generating models for csp.
        self.filter = None
        self.signal_names = {
            "api": {"insignals": set(), "outsignals": set()},
            "app": {"insignals": set(), "outsignals": set()},
        }
        self.base_application = base_application
        self.map_file = self.get_map_file()
        self.api_map = self.get_map()
        self.translations_files = []
        self.signal_primitives_list = []
        self.default_read_strategy = read_strategy

    def get_signal_properties(self, signal):
        """Get signal properties for signal

        Calls self.base_application to get signal properties

        Args:
            signal (Signal): Signal to get properties for
        """
        self.base_application.get_signal_properties(signal)

    def _get_signals(self):
        """Read signals"""
        self.parse_definition(self.translations_files)

    @property
    def insignals(self):
        return self.get_signals(self.hal_name, 'insignals')

    @property
    def outsignals(self):
        return self.get_signals(self.hal_name, 'outsignals')

    def get_signals(self, api, signal_type='insignals'):
        """Get signals to and from an api abstraction

        self.api_side configures if we look at the api side.
        If it is set to False, we look at the application side.

        Args:
            api (str): Name of the api
            signal_type (str): insignals or outsignals
        Returns:
            signals (list): Signals in the interface
        """
        if self.api_side:
            signal_names = self.signal_names['api'][signal_type]
        else:
            signal_names = self.signal_names['app'][signal_type]

        signals = []
        for signal_name, specs in self.translations.items():
            for spec in specs:
                signal = None
                if api is not None:
                    if spec['api'] == api:
                        if self.api_side:
                            if spec['property'] in signal_names:
                                signal = Signal(spec['property'], self)
                        else:
                            if signal_name in signal_names:
                                signal = Signal(signal_name, self)
                else:
                    if self.api_side:
                        if spec['property'] in signal_names:
                            signal = Signal(spec['property'], self)
                    else:
                        if signal_name in signal_names:
                            signal = Signal(signal_name, self)
                if signal is not None:
                    signals.append(signal)
        return signals

    def clear_signal_names(self):
        """Clear signal names

        Clears defined signal names (but not signal properties).
        """
        self.signal_names = {
            "api": {"insignals": set(), "outsignals": set()},
            "app": {"insignals": set(), "outsignals": set()},
        }

    def parse_definition(self, definition):
        """Parses all definition files

        Args:
            definition (list(Path)): Definition files
        """
        for translation in definition:
            raw = self.read_translation(translation)
            self.extract_endpoint_definitions(raw)

    @staticmethod
    def get_api_name(api_name):
        """Return the api name

        Args:
            api_name (str): Name of the api

        Returns:
            (str): Name of the api
        """
        return api_name

    def verify_api(self, api_name):
        """Verify that the api is in the map

        Args:
            api_name (str): Name of the api
        """
        if api_name not in self.api_map:
            raise MissingApi(api_name, self.map_file)

    def add_signals(self, signals, signal_type='insignals', properties=None):
        """Add signal names and properties to already set ones

        Args:
            signals (list(Signals)): Signals to use
            signal_type (str): 'insignals' or 'outsignals'
            properties (list(str)): signal definition properties, default = []
        """
        opposite = {'insignals': 'outsignals', 'outsignals': 'insignals'}
        api_type = opposite[signal_type]
        properties = [] if properties is None else properties
        for signal in signals:
            LOGGER.debug("Adding signal: %s", signal)
            temp_set = set()
            for translation in self.translations.get(signal.name, []):
                temp_list = list(translation)
                api_name = translation[self.position.api.value]
                variant_name = translation[self.position.variant.value]
                endpoint = translation[self.position.endpoint.value]
                api_signal = translation[self.position.property_name.value]
                self.check_signal_property(api_name, variant_name, endpoint,
                                           api_signal, signal_type)
                self.signal_names['api'][api_type].add(api_signal)
                for enum_property in properties:
                    LOGGER.debug("Modifying property: %s", enum_property)
                    value = signal.properties[enum_property["source"]]
                    if value == "-":
                        value = enum_property["default"]
                    temp_list[
                        self.position[enum_property["destination"]].value
                    ] = value
                temp_set.add(tuple(temp_list))
                self.translations[signal.name] = temp_set
            self.signal_names['app'][signal_type].add(signal.name)
        self.check_endpoints()
        LOGGER.debug('Registered signal names: %s', self.signal_names)

    def check_signal_property(self, api, variant, endpoint, property_name, signal_type):
        """Check if we have only one signal written for the same property.

        Args:
            api (str): interface name
            variant (str): variant value. "properties" or "methods" for service
                           "hals" for hal
            endpoint (str): signal endpoint
            property_name (str): signal property
            signal_type (str): 'insignals' or 'outsignals'
        """
        primitive_value = ""
        for value in [api, variant, endpoint, property_name]:
            if value:
                if primitive_value == "":
                    primitive_value = value
                else:
                    primitive_value = primitive_value + '.' + value
        if primitive_value == "":
            raise Exception("The primitive does not contain any value!")
        directional_primitive = f"{primitive_value}.{signal_type}"
        self.check_property(directional_primitive, signal_type)

    def check_property(self, property_spec, signal_type):
        """Check if we have only one signal written for the same property.

        Args:
            property_spec (str): property specification
            signal_type (str): 'insignals' or 'outsignals'
        """
        if property_spec in self.signal_primitives_list:
            error_msg = (f"You can't write {property_spec} as "
                         f"{signal_type} since this primitive has been used."
                         " Run model_yaml_verification to identify exact models.")
            raise Exception(error_msg)
        self.signal_primitives_list.append(property_spec)

    @abstractmethod
    def check_endpoints(self):
        """Should be implemented by subclasses."""

    @staticmethod
    def read_translation(translation_file):
        """Read specification of the format:

        service:
          interface:
            properties:
              - endpoint_name:
                - signal: name
                  property: name
                - signal: name
                  property: name
        hal:
          hal_name:
            - primitive_endpoint:
              - insignal: name
          hal_name:
            - struct_endpoint:
              - insignal: name1
                property: member1
              - insignal: name2
                property: member2
          ecm:
            - signal: name
        signals:
          tvrl:
            - signal: name
              property: can_name
              offset: offset
              factor: scaling

        Args:
            translation_file (Path): file with specs

        Returns:
            yaml_data (dict): Loaded YAML data as dict, empty if not found
        """
        if not translation_file.is_file():
            LOGGER.warning("No file found for %s", translation_file)
            return {}
        with open(translation_file, encoding="utf-8") as translation:
            yaml = YAML(typ='safe', pure=True)
            raw = yaml.load(translation)
        return raw

    def parse_api_definitions(self, api_definitions):
        """Parses group definitions.

        Args:
            api_definitions (dict): endpoints in parsed yaml file.
        """
        for api_from_spec, definition in api_definitions.items():
            for variant, variant_endpoints in self.extract_definition(definition).items():
                for endpoints in variant_endpoints:
                    for endpoint, signals in endpoints.items():
                        self.parse_property_definitions({api_from_spec: signals}, endpoint, variant)

    def parse_property_definitions(self, endpoint_definitions, endpoint, variant):
        """Parse signal definitions.

        Args:
            endpoint_definitions (dict): parsed yaml file.
            endpoint (str): Name of the endpoint to use
        """
        def _get_property_name(specification):
            """ Handle cases when there are no propery name.

            If there is no property name, the "group" is set to the signal.
            This should be used when the property is not a struct in the interface api.

            Args:
                specification (dict): signal specification
            Returns:
                property_name (str): name of the potential internal property
            """
            property_name = specification.get('property', '')
            if not property_name:
                return None
            return property_name

        enumerations = self.base_application.enumerations

        for api, specifications in endpoint_definitions.items():
            self.verify_api(api)
            for specification in specifications:
                in_out_signal = [key for key in specification.keys() if 'signal' in key]
                base_signal = None
                signal_name = None
                if "in" in in_out_signal[0]:
                    for signal in self.base_application.insignals:
                        if signal.name == specification["insignal"]:
                            base_signal = signal
                            signal_name = signal.name
                elif "out" in in_out_signal[0]:
                    for signal in self.base_application.outsignals:
                        if signal.name == specification["outsignal"]:
                            base_signal = signal
                            signal_name = signal.name
                else:
                    raise BadYamlFormat(api, specification[in_out_signal[0]])
                if base_signal is None:
                    continue
                base_properties = self.base_application.get_signal_properties(
                    base_signal
                )

                if base_properties["type"] in enumerations:
                    underlying_data_type = enumerations[base_properties['type']]['underlying_data_type']
                    interface_type = underlying_data_type
                    if 'init' not in specification:
                        if enumerations[base_properties['type']]['default_value'] is not None:
                            init_value = enumerations[base_properties['type']]['default_value']
                        else:
                            LOGGER.warning('Initializing enumeration %s to "zero".', base_properties['type'])
                            init_value = [
                                k for k, v in enumerations[base_properties['type']]['members'].items() if v == 0
                            ][0]
                    else:
                        init_value = specification.get("init", 0)
                else:
                    interface_type = base_properties["type"]
                    init_value = specification.get("init", 0)

                if "out" in in_out_signal[0] and "strategy" in specification:
                    LOGGER.warning('Cannot set read strategy for outsignal %s, using "Always".', signal_name)
                    strategy = "Always"
                else:
                    strategy = specification.get("strategy", self.default_read_strategy)
                if strategy not in self.read_strategies:
                    LOGGER.warning('Invalid strategy %s, using "Always" instead.', strategy)
                    strategy = self.default_read_strategy

                if signal_name not in self.translations:
                    self.translations[signal_name] = set()
                self.translations[signal_name].add(
                    (
                        "enum_0",  # Enum starts at position 1.
                        _get_property_name(specification),
                        interface_type,
                        specification.get("type"),
                        specification.get("offset"),
                        specification.get("factor"),
                        specification.get("default"),
                        specification.get("length"),
                        specification.get("min"),
                        specification.get("max"),
                        specification.get("enum"),
                        init_value,
                        specification.get("description"),
                        specification.get("unit"),
                        endpoint,
                        api,
                        variant,
                        strategy,
                        specification.get("debug", False),
                        specification.get("dependability", False)
                    )
                )

    def spec_to_dict(self, signal_spec, signal_name):
        """Convert signal specification to dict

        Args:
            signal_spec (dict): signal specification
            signal_name (str): signal name
        Returns:
            (dict): signal specification as dict
        """
        return {
            'variable': signal_name,
            'variable_type': signal_spec[self.position.variable_type.value],
            'property': signal_spec[self.position.property_name.value],
            'property_type': signal_spec[self.position.property_type.value],
            "default": signal_spec[self.position.default.value],
            "length": signal_spec[self.position.length.value],
            'offset': signal_spec[self.position.offset.value],
            'factor': signal_spec[self.position.factor.value],
            'range': {
                'min': signal_spec[self.position.min.value],
                'max': signal_spec[self.position.max.value]
            },
            'init': signal_spec[self.position.init.value],
            'description': signal_spec[self.position.description.value],
            'unit': signal_spec[self.position.unit.value],
            'endpoint': signal_spec[self.position.endpoint.value],
            'api': self.get_api_name(signal_spec[self.position.api.value]),
            'variant': signal_spec[self.position.variant.value],
            'strategy': signal_spec[self.position.strategy.value],
            'debug': signal_spec[self.position.debug.value],
            'dependability': signal_spec[self.position.dependability.value]
        }

    def to_dict(self, client="app"):
        """Method to generate dict to be saved as yaml

        Returns:
            spec (dict): Signalling specification
        """
        spec = {"consumer": [], "producer": []}
        direction = {
            "app": ["consumer", "producer"],
            "api": ["producer", "consumer"]}
        for signal_name, signal_spec in self._generator(self.signal_names["app"]["insignals"]):
            spec[direction[client][0]].append(
                self.spec_to_dict(signal_spec, signal_name)
            )
        for signal_name, signal_spec in self._generator(self.signal_names["app"]["outsignals"]):
            spec[direction[client][1]].append(
                self.spec_to_dict(signal_spec, signal_name)
            )
        return spec

    def _generator(self, signal_names, unique_names=False):
        """Iterate over signals for allowed services

        If unique_names is True, the iterator does not yield the same signal twice
        if unique_names is False, it yields each allowed signal spec with the signal name

        Args:
            signal_names (list): allowed signals
        Yields:
            name (str): Name of the signal
            specification (dict): signal specification for allowed service
        """
        for signal_name, specifications in (
                (name, spec) for name, spec in sorted(
                    self.translations.items())
                if name in signal_names):
            for specification in specifications:
                if unique_names:
                    yield signal_name, specification
                    break
                yield signal_name, specification
