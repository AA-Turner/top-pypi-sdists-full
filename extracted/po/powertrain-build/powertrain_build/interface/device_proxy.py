# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Python module used for reading device proxy arxml:s"""
from ruamel.yaml import YAML
import enum
from powertrain_build.interface.base import BaseApplication, Signal
from powertrain_build.lib import logger

LOGGER = logger.create_logger("device_proxy")


class MissingDevice(Exception):
    """Exception to raise when device is missing"""
    def __init__(self, dp):
        self.message = f"Device proxy {dp} missing from deviceDomains.json"


class BadYamlFormat(Exception):
    """Exception to raise when in/out signal is not defined."""
    def __init__(self, message):
        self.message = message


class DPAL(BaseApplication):
    """Device Proxy abstraction layer"""

    dp_position = enum.Enum(
        "Position",
        names=[
            "domain",
            "property",
            "variable_type",
            "property_interface_type",
            "property_manifest_type",
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
            "group",
            "strategy",
            "debug",
            "dependability",
            "port_name"
        ],
    )

    def __repr__(self):
        """String representation of DPAL"""
        return (
            f"<DPAL {self.name}"
            f" app_side insignals: {len(self.signal_names['other']['insignals'])}"
            f" app_side outsignals: {len(self.signal_names['other']['outsignals'])}>"
        )

    def __init__(self, base_application):
        """Create the interface object

        Args:
            base_application (BaseApplication): Primary object of an interface
                                                Usually a raster, but can be an application or a model too.
        """
        self.name = ""
        self.dp_translations = {}
        # We do not care about domain when looking from a project perspective,
        # we only care when generating manifests for csp.
        self.domain_filter = None
        self.signal_names = {
            "dp": {"insignals": set(), "outsignals": set()},
            "other": {"insignals": set(), "outsignals": set()},
        }
        self.e2e_sts_signals = set()
        self.base_application = base_application
        self.translations_files = []
        self.device_domain = base_application.get_domain_mapping()
        self.signal_primitives_list = []

    def clear_signal_names(self):
        """Clear signal names

        Clears defined signal names (but not signal properties).
        """
        self.signal_names = {
            "dp": {"insignals": set(), "outsignals": set()},
            "other": {"insignals": set(), "outsignals": set()},
        }

    def add_signals(self, signals, signal_type="insignal", properties=[]):
        """Add signal names and properties

        Args:
            signals (list(Signals)): Signals to use
            signal_type (str): 'insignals' or 'outsignals'
            properties (list(str)): signal definition properties, default = []
        """
        opposite = {"insignals": "outsignals", "outsignals": "insignals"}
        dp_type = opposite[signal_type]
        for signal in signals:
            LOGGER.debug("Adding signal: %s", signal)
            temp_set = set()
            for translation in self.dp_translations.get(signal.name, []):
                temp_list = list(translation)
                domain = translation[self.dp_position.domain.value]
                group = translation[self.dp_position.group.value]
                dp_signal = translation[self.dp_position.property.value]
                self.check_signal_property(domain, group, dp_signal, signal_type)
                self.signal_names["dp"][dp_type].add(dp_signal)
                for enum_property in properties:
                    LOGGER.debug("Modifying property: %s", enum_property)
                    value = signal.properties[enum_property["source"]]
                    if value == "-":
                        value = enum_property["default"]
                    temp_list[
                        self.dp_position[enum_property["destination"]].value
                    ] = value
                temp_set.add(tuple(temp_list))
                self.dp_translations[signal.name] = temp_set
            self.signal_names["other"][signal_type].add(signal.name)
        for e2e_sts_signal_name in self.e2e_sts_signals:
            if e2e_sts_signal_name not in self.signal_names["other"]["insignals"]:
                LOGGER.warning("E2E check signal %s not used in any model.", e2e_sts_signal_name)
                self.signal_names["other"][signal_type].add(e2e_sts_signal_name)
        self.check_groups()
        LOGGER.debug("Registered signal names: %s", self.signal_names)

    def check_signal_property(self, domain, group, property_name, signal_type):
        """Check if we have only one signal written for the same property.

        Args:
            domain (str): signal domain
            group (str): signal group
            property_name (str): signal property
            signal_type (str): 'insignals' or 'outsignals'
        """
        primitive_value = ""
        for value in [domain, group, property_name]:
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

    def check_groups(self):
        """Check and crash if signal group contains both produces and consumes signals."""
        groups = {}
        for signal_name, signal_specs in self.dp_translations.items():
            if signal_name in self.signal_names["other"]['insignals']:
                consumed = True
            elif signal_name in self.signal_names["other"]['outsignals']:
                consumed = False
            else:
                continue
            for signal_spec in signal_specs:
                group = signal_spec[self.dp_position.group.value]
                if group is None:
                    continue
                domain = signal_spec[self.dp_position.domain.value]
                key = (domain, group)
                if key not in groups:
                    groups[key] = {"consumed": consumed,
                                   "signals": set()}
                groups[key]["signals"].add(signal_name)
                assert consumed == groups[key]["consumed"], \
                    f"Signal group {group} for {domain} contains both consumed and produced signals"

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

    def parse_group_definitions(self, signal_groups):
        """Parse group definitions.

        Args:
            signal_groups (dict): parsed yaml file.
        """
        for dp_name, group_definitions in signal_groups.items():
            for group in group_definitions:
                port_name = None
                if 'portname' in group:
                    port_name = group.pop('portname')
                for group_name, signals in group.items():
                    self.parse_signal_definitions({dp_name: signals}, group_name, port_name)

    def parse_signal_definitions(self, signals_definition, group=None, port_name=None):
        """Parse signal definitions.

        Args:
            signals_definition (dict): parsed yaml file.
            group (str): Name of signal group, if signal belongs to a group.
            port_name (str): Name of signal port, if there is one.
        """
        enumerations = self.base_application.enumerations
        for dp_name, dp_specification in signals_definition.items():
            for specification in dp_specification:
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
                    raise BadYamlFormat(f"in/out signal for {dp_name} is missing.")
                if base_signal is None:
                    continue
                base_properties = self.base_application.get_signal_properties(
                    base_signal
                )
                if base_properties["type"] in enumerations:
                    underlying_data_type = enumerations[base_properties['type']]['underlying_data_type']
                    interface_type = underlying_data_type
                    manifest_type = underlying_data_type
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
                    manifest_type = base_properties["type"]
                    init_value = specification.get("init", 0)

                if "out" in in_out_signal[0] and "strategy" in specification:
                    LOGGER.warning('Cannot set read strategy for outsignal %s, using "Always".', signal_name)
                    strategy = "Always"
                else:
                    strategy = specification.get("strategy", "Always")
                if strategy not in self.read_strategies:
                    LOGGER.warning('Invalid strategy %s, using "Always" instead.', strategy)
                    strategy = "Always"

                if group is not None and specification.get("portname", None) is not None:
                    raise BadYamlFormat(f"Port name should be on group level not signal level: {dp_name}")
                port_name_tmp = port_name if port_name is not None else specification.get("portname", None)

                is_safe_signal = specification.get("dependability", False)

                if signal_name not in self.dp_translations:
                    self.dp_translations[signal_name] = set()
                domain = self._get_domain(dp_name)
                self.dp_translations[signal_name].add(
                    (
                        "enum_0",  # read from this tuple using the dp_position enum. Enum starts at 1 though.
                        domain,
                        specification["property"],
                        specification.get("type"),
                        interface_type,
                        manifest_type,
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
                        group,
                        strategy,
                        specification.get("debug", False),
                        is_safe_signal,
                        port_name_tmp
                    )
                )

                enable_e2e_sts = self.base_application.pybuild['build_cfg'].get_enable_end_to_end_status_signals()
                if enable_e2e_sts and is_safe_signal and group is not None:
                    e2e_sts_property = f"{group}E2eSts"
                    e2e_sts_signal_name = f"sVc{domain}_D_{e2e_sts_property}"

                    if signal_name == e2e_sts_signal_name:
                        raise BadYamlFormat(f"Don't put E2E status signals ({signal_name}) in yaml interface files.")

                    if e2e_sts_signal_name not in self.dp_translations:
                        self.dp_translations[e2e_sts_signal_name] = set()
                        self.dp_translations[e2e_sts_signal_name].add(
                            (
                                "enum_0",  # read from this tuple using the dp_position enum. Enum starts at 1 though.
                                domain,
                                e2e_sts_property,
                                "UInt8",
                                "UInt8",
                                "UInt8",
                                0,
                                1,
                                None,
                                None,
                                0,
                                255,
                                None,
                                255,
                                f"E2E status code for E2E protected signal (group) {signal_name}.",
                                None,
                                group,
                                strategy,
                                False,
                                is_safe_signal,
                                port_name_tmp
                            )
                        )
                        self.e2e_sts_signals.add(e2e_sts_signal_name)

    def parse_definition(self, definition):
        """Parses all definition files

        Args:
            definition (list(Path)): Definition files
        """

        for translation in definition:
            raw = self.read_translation(translation)
            self.parse_signal_definitions(raw.get("signals", {}))
            self.parse_group_definitions(raw.get("signal_groups", {}))

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

    def _get_domain(self, device_proxy):
        """Get domain for device proxy

        Args:
            device_proxy (str): Name of device proxy
        Returns:
            domain (str): Name of the domain
        """
        if device_proxy not in self.device_domain:
            raise MissingDevice(device_proxy)
        return self.device_domain[device_proxy]

    def _allow_domain(self, domain):
        """Check if device proxy is in current domain_filter

        If there is no filter, the device is seen as part of the filter

        Args:
            domain (str): Name of the domain
        Returns:
            filtered (bool): True if device is not filtered away
        """
        return self.domain_filter is None or domain in self.domain_filter

    def get_signals(self, signal_type="insignals"):
        """Get signals to and from a dp abstraction

        If it is set to False, we look at the application side.

        Args:
            signal_type (str): insignals or outsignals
        Returns:
            signals (list): Signals in the interface
        """
        signal_names = self.signal_names["other"][signal_type]

        signals = []
        for name in self._allowed_names(signal_names):
            signals.append(Signal(name, self))
        return signals

    @property
    def insignals(self):
        """ Signals going to the device proxy. """
        return self.get_signals("insignals")

    @property
    def outsignals(self):
        """ Signals sent from the device proxy. """
        return self.get_signals("outsignals")

    def dp_spec_to_dict(self, signal_spec, signal_name):
        """Convert signal specification to dict.

        Args:
            signal_spec (tuple): Signal specification
            signal_name (str): Signal name
        Returns:
            signal_spec (dict): Signal specification
        """
        return {
            "variable": signal_name,
            "variable_type": signal_spec[self.dp_position.variable_type.value],
            "property_type": signal_spec[self.dp_position.property_interface_type.value],
            "domain": signal_spec[self.dp_position.domain.value],
            "default": signal_spec[self.dp_position.default.value],
            "length": signal_spec[self.dp_position.length.value],
            "property": signal_spec[self.dp_position.property.value],
            "offset": signal_spec[self.dp_position.offset.value],
            "factor": signal_spec[self.dp_position.factor.value],
            "range": {
                "min": signal_spec[self.dp_position.min.value],
                "max": signal_spec[self.dp_position.max.value],
            },
            "init": signal_spec[self.dp_position.init.value],
            "description": signal_spec[self.dp_position.description.value],
            "unit": signal_spec[self.dp_position.unit.value],
            "group": signal_spec[self.dp_position.group.value],
            "strategy": signal_spec[self.dp_position.strategy.value],
            "debug": signal_spec[self.dp_position.debug.value],
            "dependability": signal_spec[self.dp_position.dependability.value],
            "port_name": signal_spec[self.dp_position.port_name.value]
        }

    @classmethod
    def dp_spec_for_manifest(cls, signal_spec):
        """Convert signal specification to dict for a signal manifest.

        Args:
            signal_spec (tuple): Signal specification
        Returns:
            signal_spec (dict): Signal specification
        """
        spec = {
            "name": signal_spec[cls.dp_position.property.value],
            "type": signal_spec[cls.dp_position.property_manifest_type.value],
        }
        for key, value in {
            "default": cls.dp_position.default.value,
            "length": cls.dp_position.length.value,
            "enum": cls.dp_position.enum.value,
            "description": cls.dp_position.description.value,
            "unit": cls.dp_position.unit.value,
        }.items():
            if signal_spec[value] is not None:
                spec[key] = signal_spec[value]
        if (
            signal_spec[cls.dp_position.min.value] is not None
            and signal_spec[cls.dp_position.max.value] is not None
            and cls.dp_position.enum.value is not None
        ):
            spec["range"] = {
                "min": signal_spec[cls.dp_position.min.value],
                "max": signal_spec[cls.dp_position.max.value],
            }
        return spec

    def to_dict(self):
        """Method to generate dict to be saved as yaml

        Returns:
            spec (dict): Signalling specification
        """
        spec = {"consumer": [], "producer": []}
        for signal_name, signal_spec in self._allowed_names_and_specifications(
                self.signal_names["other"]["insignals"]):
            spec['consumer'].append(
                self.dp_spec_to_dict(signal_spec, signal_name)
            )
        for signal_name, signal_spec in self._allowed_names_and_specifications(
                self.signal_names["other"]["outsignals"]):
            spec['producer'].append(
                self.dp_spec_to_dict(signal_spec, signal_name)
            )
        return spec

    def to_manifest(self, client_name):
        """Method to generate dict to be saved as yaml
        Args:
            client_name (str): Name of the client in signal comm
        Returns:
            spec (dict): Signal manifest for using a Device proxy
        """
        manifest = {"name": client_name}
        manifest["consumes"] = self.insignals_dp_manifest(client_name)
        manifest["produces"] = self.outsignals_dp_manifest(client_name)
        manifest = self.cleanup_dp_manifest(manifest)
        if "consumes" not in manifest and "produces" not in manifest:
            return None
        return {"signal_info": {"version": 0.2, "clients": [manifest]}}

    def _generator(self, signal_names, unique_names=False):
        """Iterate over signals for allowed devices

        If unique_names is True, the iterator does not yield the same signal twice
        if unique_names is False, it yields each allowed signal spec with the signal name

        Args:
            signal_names (list): allowed signals
        Yields:
            name (str): Name of the signal
            specification (dict): signal specification for allowed device
        """
        for signal_name, specifications in (
                (name, spec) for name, spec in self.dp_translations.items()
                if name in signal_names):
            for specification in (
                    spec for spec in specifications
                    if self._allow_domain(spec[self.dp_position.domain.value])):
                if unique_names:
                    yield signal_name, specification
                    break
                yield signal_name, specification

    def _allowed_names(self, signal_names):
        """ Iterate over signal names for allowed devices

        Args:
            signal_names (list): allowed signals
        Yields:
            name (str): Signal name
        """
        for name, _ in self._generator(signal_names, unique_names=True):
            yield name

    def _allowed_specifications(self, signal_names):
        """ Iterate over signal specifications for allowed devices

        Args:
            signal_names (list): allowed signals
        Yields:
            specification (dict): Specification for a signal for an allowed device
        """
        for _, spec in self._generator(signal_names, unique_names=False):
            yield spec

    def _allowed_names_and_specifications(self, signal_names):
        """ Iterate over signal specifications for allowed devices

        Args:
            signal_names (list): allowed signals
        Yields:
            name (str): Signal name
            specification (dict): Specification for the signal for an allowed device
        """
        for name, spec in self._generator(signal_names, unique_names=False):
            yield name, spec

    def insignals_dp_manifest(self, client_name):
        """ Create consumes part of manifest for reading signals from device proxies
        Args:
            client_name (str): Name of the client in signal comm
        """
        consumes = [{"name": client_name, "signal_groups": []}]
        signal_names = self.signal_names["other"]["insignals"]
        consumed_groups = set()
        for signal_spec in self._allowed_specifications(signal_names):
            group = signal_spec[self.dp_position.group.value]
            if group is not None:
                consumed_groups.add(group)
            else:
                consumes[0]["signal_groups"].append(
                    {"name": signal_spec[self.dp_position.property.value]}
                )
        for group in consumed_groups:
            consumes[0]["signal_groups"].append(
                {"name": group}
            )
        return consumes

    def outsignals_dp_manifest(self, client_name):
        """ Update manifests for writing signals to device proxies
        Args:
            client_name (str): Name of the client in signal comm
        """
        produces = [{"name": client_name, "signals": [], "signal_groups": []}]
        signal_names = self.signal_names["other"]["outsignals"]
        group_signals = {}
        for signal_spec in self._allowed_specifications(signal_names):
            group = signal_spec[self.dp_position.group.value]
            if group is not None:
                if group not in group_signals:
                    group_signals[group] = []
                group_signals[group].append(
                    self.dp_spec_for_manifest(signal_spec)
                )
            else:
                produces[0]["signals"].append(
                    self.dp_spec_for_manifest(signal_spec)
                )
        for group_name, signals in group_signals.items():
            produces[0]["signal_groups"].append(
                    {"name": group_name,
                     "signals": list(signals)}
            )
        return produces

    @staticmethod
    def cleanup_dp_manifest(manifest):
        """ Remove empty device proxies.
        Args:
            manifest (dict): Device proxy configurations
        """
        if not manifest["produces"][0]["signal_groups"]:
            del manifest["produces"][0]["signal_groups"]
        if not manifest["produces"][0]["signals"]:
            del manifest["produces"][0]["signals"]
        if list(manifest["produces"][0].keys()) == ["name"]:
            del manifest["produces"]
        if not manifest["consumes"][0]["signal_groups"]:
            del manifest["consumes"]
        return manifest
