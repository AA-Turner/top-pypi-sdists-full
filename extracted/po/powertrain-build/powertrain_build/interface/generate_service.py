# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

# -*- coding: utf-8 -*-
"""Python module used for calculating interfaces for CSP"""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from powertrain_build.interface.service import get_service
from powertrain_build.lib import logger
from powertrain_build.interface import generation_utils

LOGGER = logger.create_logger("CSP service")

PARSER_HELP = "Generate CSP service models"


def configure_parser(parser: argparse.ArgumentParser):
    """Configure parser for CSP service generation"""
    generation_utils.add_base_args(parser)
    parser.add_argument(
        "--client-name",
        help="Name of the context object in CSP. Defaults to project name."
    )
    parser.add_argument(
        "output",
        help="Output directory for service models",
        type=Path
    )
    parser.set_defaults(func=generate_service_cli)


def generate_service_cli(args: argparse.Namespace):
    """CLI function for CSP service generation"""
    app = generation_utils.process_app(args.config)
    client_name = generation_utils.get_client_name(args, app)
    service(args, app, client_name)


def main(argv: Optional[List[str]] = None):
    """ Main function for stand alone execution.
    Mostly useful for testing and generation of dummy hal specifications
    """
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


def service(args, app, client_name):
    """ Generate specifications for pt-scheduler wrappers.

    Args:
        args (Namespace): Arguments from command line
        app (Application): Application to generate specifications for
        client_name (str): Signal client name
    """
    model_internal = get_service(app, client_name, 'internal')
    model_external = get_service(app, client_name, 'external')
    model_observer = get_service(app, client_name, 'observer')
    generation_utils.write_to_file(model_internal, Path(args.output, 'model', 'internal.yaml'), is_yaml=True)
    generation_utils.write_to_file(model_external, Path(args.output, 'model', 'external.yaml'), is_yaml=True)
    generation_utils.write_to_file(model_observer, Path(args.output, 'model', 'observer.yaml'), is_yaml=True)


if __name__ == "__main__":
    main(sys.argv[1:])
