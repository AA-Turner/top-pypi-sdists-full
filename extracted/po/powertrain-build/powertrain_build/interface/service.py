# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for handling the Service abstraction."""


import re

from powertrain_build.interface.base import filter_signals
from powertrain_build.interface.csp_api import CspApi
from powertrain_build.interface.application import get_internal_domain
from powertrain_build.lib import logger

LOGGER = logger.create_logger("service")


def get_service(app, client_name, interface):
    """Get service implementation specification"""
    rasters = app.get_rasters()
    LOGGER.debug("Rasters: %s", rasters)
    translation_files = app.get_translation_files()

    sfw = ServiceFramework(app)
    sfw.filter = f"{client_name}_internal"
    sfw.name = f"{client_name}_{interface}"
    sfw.parse_definition(translation_files)
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
        external_signals = filter_signals(raster.insignals, internal)
        sfw.add_signals(
            external_signals,
            "insignals",
            properties_from_json,
        )
        sfw.add_signals(raster.outsignals, "outsignals", properties_from_json)
    return sfw.to_model(interface)


def get_service_list(app):
    """Get service list from app

    Args:
        app (Application): Pybuild project

    Returns:
        (str): a string containing the translated service list
    """
    translation_map = app.get_service_mapping()
    cmake = ''
    for proxy, service in translation_map.items():
        lib = re.sub('-', '_', service + '_lib' + proxy + '_service_proxy').upper()
        include = re.sub('-', '_', service + '_include_dir').upper()
        cmake += f"LIST(APPEND extra_libraries ${{{lib}}})\n"
        cmake += f"LIST(APPEND EXTRA_INCLUDE_DIRS ${{{include}}})\n"
    return cmake


class ServiceFramework(CspApi):
    """Service Framework abstraction layer"""

    def __repr__(self):
        """String representation of SWFL"""
        return (
            f"<SWFL {self.name}"
            f" app_side insignals: {len(self.signal_names['app']['insignals'])}"
            f" app_side outsignals: {len(self.signal_names['app']['outsignals'])}>"
        )

    def get_map_file(self):
        """Get service translation map file

        Returns:
            (Path): service translation map file
        """
        return self.base_application.get_services_file()

    def get_map(self):
        """Get service translation map

        Returns:
            (dict): service translation map
        """
        return self.base_application.get_service_mapping()

    def check_endpoints(self):
        """Check and crash if signal endpoint contains both produces and consumes signals."""
        endpoints = {}
        for signal_name, signal_specs in self.translations.items():
            if signal_name in self.signal_names["app"]['insignals']:
                consumed = True
            elif signal_name in self.signal_names["app"]['outsignals']:
                consumed = False
            else:
                continue
            for signal_spec in signal_specs:
                endpoint = signal_spec[self.position.endpoint.value]
                api = signal_spec[self.position.api.value]
                key = (api, endpoint)
                if key not in endpoints:
                    endpoints[key] = {
                        "consumed": consumed,
                        "signals": set()
                    }
                endpoints[key]["signals"].add(signal_name)
                assert consumed == endpoints[key]["consumed"], \
                    f"Signal endpoint {endpoint} for {api} contains both consumed and produced signals"

    def extract_endpoint_definitions(self, raw):
        """Extract endpoint definitions from yaml file.

        Args:
            raw (dict): Raw yaml file
        Returns:
            (dict): Endpoint definitions
        """
        self.parse_api_definitions(raw.get("service", {}))

    @staticmethod
    def extract_definition(definition):
        """Extract definition from yaml file.
        Returns the properties and methods for a service.

        Args:
            definition (dict): Definition from yaml file
        Returns:
            (dict): Specifications for a service
        """
        specifications = {}
        specifications['properties'] = definition.get('properties', [])
        specifications['methods'] = definition.get('methods', [])
        return specifications

    def to_model(self, client):
        """Method to generate dict to be saved as yaml
        Args:
            client (str): Name of the client in signal comm
        Returns:
            spec (dict): Signal model for using a service
        """
        properties, types = self.properties_service_model(client)
        descriptions = {
            'internal': {
                'brief': "Internal interface for associated application.",
                'full': "This interface should only be used by the associated application."
            },
            'external': {
                'brief': "External interface.",
                'full': "This interface should be used by modules wanting to interact with the associated application."
            },
            'observer': {
                'brief': "Read-only interface.",
                'full': "This interface can be used by anyone wanting information from the associated application."
            },
        }
        model = {"name": self.name,
                 "version": "${SERVICE_VERSION}",
                 "description": descriptions[client],
                 "properties": properties,
                 "types": types}
        return model

    def properties_service_model(self, client):
        """Generate properties and types for a service

        Args:
            client (str): Name of the client in signal comm

        Returns:
            (list): List of properties
            (list): List of types
        """
        properties = {}
        types = {}
        accessors = {}
        if client == 'internal':
            accessors['insignals'] = 'r-'
            accessors['outsignals'] = '-w'
        elif client == 'external':
            accessors['insignals'] = '-w'
            accessors['outsignals'] = 'r-'
        else:
            accessors['insignals'] = 'r-'
            accessors['outsignals'] = 'r-'

        properties_in, types_in = self._properties_service_model(
            self.signal_names["app"]["insignals"],
            accessors['insignals'])
        properties_out, types_out = self._properties_service_model(
            self.signal_names["app"]["outsignals"],
            accessors['outsignals'])

        properties = properties_in + properties_out
        types = types_in + types_out
        return properties, types

    def _specifications(self, signal_names):
        """ Iterate over signal specifications for allowed services

        Args:
            signal_names (list): allowed signals
        Yields:
            specification (dict): Specification for a signal for an allowed service
        """
        for _, spec in self._generator(signal_names, unique_names=False):
            yield spec

    def _properties_service_model(self, signal_names, accessors):
        """ Placeholder
        """
        properties = []
        endpoint_members = {}
        endpoint_types = {}
        for signal_spec in self._specifications(signal_names):
            interface = signal_spec[self.position.api.value]
            if self.skip_interface(interface):
                continue
            endpoint = signal_spec[self.position.endpoint.value]
            primitive = signal_spec[self.position.property_name.value]
            if endpoint not in endpoint_members and primitive is not None:
                endpoint_members[endpoint] = []
            if primitive is not None:
                if endpoint not in endpoint_types:
                    endpoint_types[endpoint] = {
                        'name': endpoint,
                        'kind': 'struct',
                        'description': {
                            'brief': endpoint,
                            "full": "Generated from project without custom description"
                        },
                        'members': []
                    }
                endpoint_members[endpoint].append({
                    'name': primitive,
                    'type': primitive,
                })
                endpoint_types[endpoint]['members'].append({
                    'name': primitive,
                    'type': signal_spec[self.position.property_type.value],
                })
            else:
                primitive_type = signal_spec[self.position.property_type.value]
                primitive_desc = signal_spec[self.position.description.value]
                primitive_unit = signal_spec[self.position.unit.value]
                properties.append(
                    {
                        'name': endpoint,
                        'type': primitive_type,
                        'unit': primitive_unit,
                        'accessors': accessors,
                        'description': {
                            'brief': endpoint,
                            'full': primitive_desc,
                        }
                    }
                )
        for endpoint_name in sorted(endpoint_members):
            properties.append(
                {
                    'name': endpoint_name,
                    'type': endpoint_name,
                    'unit': 'struct',
                    'accessors': accessors,
                    'description': {
                        'brief': endpoint_name,
                        "full": "Generated from project without custom description"},
                }
            )
        return_types = []
        for endpoint_name, endpoint_type in endpoint_types.items():
            return_types.append(endpoint_type)
        return properties, return_types

    def skip_interface(self, interface):
        """ Filter services not in list.

        Args:
            service (str): interface
        Returns:
            skip (bool): Skip this interface
        """
        if self.filter is None:
            LOGGER.debug('No interface filter. Allowing everyone.')
            return False
        if interface in self.filter:
            LOGGER.debug('%s is in %s', interface, self.filter)
            return False
        return True
