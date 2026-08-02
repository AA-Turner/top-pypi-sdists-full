# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module with generation utils."""

import argparse
from ruamel.yaml import YAML
from pathlib import Path
from powertrain_build.interface.application import Application, get_internal_domain
from powertrain_build.interface.base import filter_signals
from powertrain_build.lib import logger

LOGGER = logger.create_logger("CSP interface generation utils")


def add_base_args(parser: argparse.ArgumentParser):
    """ Base parser that adds config argument.

    Returns:
        parser (ArgumentParser): Base parser
    """
    parser.add_argument("config", help="The project configuration file", type=Path)


def get_client_name(args, app):
    """ Get client name for app.

    Args:
        app (Application): Parsed project configuration
    Returns:
        name (str): Name of the project
    """
    return args.client_name if args.client_name else app.name


def process_app(config):
    """ Get an app specification for the current project

    Entrypoint for external scripts.

    Args:
        config (pathlib.Path): Path to the ProjectCfg.json
    Returns:
        app (Application): powertrain-build project
    """
    app = Application()
    app.parse_definition(config)
    return app


def get_interface(app, interface_type):
    """Get interface(hal/dp/zc/service) to application

    Args:
        app (Application): Pybuild project
        interface_type (BaseApplication): A type of interface
    Returns:
        spec (obj): obj for hal/dp/zc/service class
    """
    spec = {}
    rasters = app.get_rasters()
    LOGGER.debug("Rasters: %s", rasters)
    translation_files = app.get_translation_files()
    interface_type.parse_definition(translation_files)
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
    # TODO We read all yaml files at once, should we "add_signals" for all rasters at once?
    # For example, service.check_endpoints will miss endpoint mismatches that reside in different rasters.
    for raster in rasters:
        interface_type.name = raster.name
        interface_type.clear_signal_names()
        interface_type.add_signals(
            filter_signals(raster.insignals, internal), "insignals", properties_from_json)
        interface_type.add_signals(raster.outsignals, "outsignals", properties_from_json)
        LOGGER.debug("Current communication interface: %s", interface_type)
        spec[raster.name] = interface_type.to_dict()
    return spec


def get_method_interface(app):
    """ Get method interface
    Args:
        app (Application): Application
    Returns:
        spec (dict): Specification for csp methods
    """
    spec = {}

    for method in app.get_methods():
        method_spec = {}
        method_spec['name'] = method.name
        method_spec['primitive'] = method.get_primitive(method.name)
        method_spec['namespace'] = method.namespace
        if method.description:
            method_spec['description'] = method.description
        inports = {}
        outports = {}
        for signal in method.signals:
            signal_spec = {
                'primitive': method.get_primitive(signal.name),
                'type': signal.properties['type'],
                'variable_type': signal.properties['type'],
                'variable': signal.name,
                'range': signal.properties['range'],
                'init': 0,
                'description': '',
                'unit': ''
            }
            if signal in method.outsignals:
                outports[signal.name] = signal_spec
            else:
                inports[signal.name] = signal_spec

        ports = {'in': inports, 'out': outports}
        method_spec['ports'] = ports
        spec[method.name] = method_spec
    return spec


def write_to_file(content, output, is_yaml=False):
    """ Write to cmake.

    Args:
        content (str): cmake
        output (Path): File to write.
        yaml (bool): Dump yaml
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as file_handler:
        if is_yaml:
            yaml = YAML()
            yaml.dump(content, file_handler)
        else:
            file_handler.write(content)
