# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

from argparse import ArgumentParser, Namespace
from typing import List, Optional

import powertrain_build.check_interface
import powertrain_build.create_conversion_table
import powertrain_build.interface.export_global_vars
import powertrain_build.interface.generate_adapters
import powertrain_build.interface.generate_hi_interface
import powertrain_build.interface.generate_service
import powertrain_build.interface.generate_wrappers
import powertrain_build.interface.model_yaml_verification
import powertrain_build.interface.update_model_yaml
import powertrain_build.interface.update_call_sources
import powertrain_build.replace_compu_tab_ref
import powertrain_build.signal_inconsistency_check
from powertrain_build import __version__
from powertrain_build.config import ProcessHandler
from powertrain_build.lib import logger
from powertrain_build.wrapper import PyBuildWrapper

LOGGER = logger.create_logger(__file__)


def parse_args(argv: Optional[List[str]] = None) -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(
        prog="powertrain-build",
        description="Powertrain-build",
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    command_subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

    wrapper_parser = command_subparsers.add_parser(
        "wrapper",
        help=PyBuildWrapper.PARSER_HELP,
    )
    PyBuildWrapper.add_args(wrapper_parser)

    config_parser = command_subparsers.add_parser(
        "config",
        help=ProcessHandler.PARSER_HELP,
    )
    ProcessHandler.configure_parser(config_parser)

    check_interface_parser = command_subparsers.add_parser(
        "check-interface",
        help=powertrain_build.check_interface.PARSER_HELP,
    )
    powertrain_build.check_interface.configure_parser(check_interface_parser)

    create_conversion_table_parser = command_subparsers.add_parser(
        "create-conversion-table",
        help=powertrain_build.create_conversion_table.PARSER_HELP,
    )
    powertrain_build.create_conversion_table.configure_parser(create_conversion_table_parser)

    replace_compu_tab_ref_parser = command_subparsers.add_parser(
        "replace-compu-tab-ref",
        help=powertrain_build.replace_compu_tab_ref.PARSER_HELP,
    )
    powertrain_build.replace_compu_tab_ref.configure_parser(replace_compu_tab_ref_parser)

    signal_inconsistency_check_parser = command_subparsers.add_parser(
        "signal-inconsistency-check",
        help=powertrain_build.signal_inconsistency_check.PARSER_HELP,
    )
    powertrain_build.signal_inconsistency_check.configure_parser(signal_inconsistency_check_parser)

    interface_parser = command_subparsers.add_parser(
        "interface",
        help="Interface commands",
    )
    interface_subparsers = interface_parser.add_subparsers(
        title="Interface commands",
        dest="interface_command",
        required=True,
    )

    export_global_vars_parser = interface_subparsers.add_parser(
        "export-global-vars",
        help=powertrain_build.interface.export_global_vars.PARSER_HELP,
    )
    powertrain_build.interface.export_global_vars.configure_parser(export_global_vars_parser)

    generate_adapters_parser = interface_subparsers.add_parser(
        "generate-adapters",
        help=powertrain_build.interface.generate_adapters.PARSER_HELP,
    )
    powertrain_build.interface.generate_adapters.configure_parser(generate_adapters_parser)

    generate_hi_interface_parser = interface_subparsers.add_parser(
        "generate-hi-interface",
        help=powertrain_build.interface.generate_hi_interface.PARSER_HELP,
    )
    powertrain_build.interface.generate_hi_interface.configure_parser(generate_hi_interface_parser)

    generate_service_parser = interface_subparsers.add_parser(
        "generate-service",
        help=powertrain_build.interface.generate_service.PARSER_HELP,
    )
    powertrain_build.interface.generate_service.configure_parser(generate_service_parser)

    generate_wrappers_parser = interface_subparsers.add_parser(
        "generate-wrappers",
        help=powertrain_build.interface.generate_wrappers.PARSER_HELP,
    )
    powertrain_build.interface.generate_wrappers.configure_parser(generate_wrappers_parser)

    model_yaml_verification_parser = interface_subparsers.add_parser(
        "model-yaml-verification",
        help=powertrain_build.interface.model_yaml_verification.PARSER_HELP,
    )
    powertrain_build.interface.model_yaml_verification.configure_parser(model_yaml_verification_parser)

    update_model_yaml_parser = interface_subparsers.add_parser(
        "update-model-yaml",
        help=powertrain_build.interface.update_model_yaml.PARSER_HELP,
    )
    powertrain_build.interface.update_model_yaml.configure_parser(update_model_yaml_parser)

    update_call_sources_parser = interface_subparsers.add_parser(
        "update-call-sources",
        help=powertrain_build.interface.update_call_sources.PARSER_HELP,
    )
    powertrain_build.interface.update_call_sources.configure_parser(update_call_sources_parser)

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> Namespace:
    """Run main function."""
    args = parse_args(argv)
    return args.func(args)
