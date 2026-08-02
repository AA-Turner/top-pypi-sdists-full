# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Python module used for calculating interfaces for CSP HI"""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from powertrain_build.interface import generation_utils
from powertrain_build.interface.device_proxy import DPAL
from powertrain_build.lib.helper_functions import recursive_default_dict, to_normal_dict

OP_READ = 'read'
OP_WRITE = 'write'

PARSER_HELP = "Generate HI YAML interface file."


def generate_hi_interface(args, hi_interface):
    """Generate HI YAML interface file.

    Args:
        args (Namespace): Arguments from command line.
        hi_interface (dict): HI interface dict based on HIApplication and generation_utils.get_interface.
    Returns:
        result (dict): Aggregated signal information as a dict.
    """

    io_translation = {
        'consumer': OP_READ,
        'producer': OP_WRITE
    }
    result = recursive_default_dict()
    for raster_data in hi_interface.values():
        for direction, signals in raster_data.items():
            hi_direction = io_translation[direction]
            for signal in signals:
                domain = signal['domain']
                group = signal['group']
                name = signal['variable']
                property_name = signal['property']
                if group is None:
                    port_name = signal['port_name'] or property_name
                    result[hi_direction]['signals'][domain][port_name]['data'][property_name] = name
                else:
                    port_name = signal['port_name'] or group
                    result[hi_direction]['signal_groups'][domain][port_name][group]['data'][property_name] = name
    generation_utils.write_to_file(to_normal_dict(result), args.output, is_yaml=True)


def generate_hi_interface_cli(args: argparse.Namespace):
    """CLI entrypoint for generating HI YAML interface file.

    Args:
        args (Namespace): Arguments from command line.
    """
    app = generation_utils.process_app(args.config)
    hi_app = DPAL(app)
    interface = generation_utils.get_interface(app, hi_app)
    generate_hi_interface(args, interface)


def configure_parser(parser: argparse.ArgumentParser):
    """Configure parser for generating HI YAML interface file."""
    generation_utils.add_base_args(parser)
    parser.add_argument(
        "output",
        help="Output file with interface specifications.",
        type=Path
    )
    parser.set_defaults(func=generate_hi_interface_cli)


def main(argv: Optional[List[str]] = None):
    """ Main function for stand alone execution.
    Mostly useful for testing and generation of dummy hal specifications.
    """
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
