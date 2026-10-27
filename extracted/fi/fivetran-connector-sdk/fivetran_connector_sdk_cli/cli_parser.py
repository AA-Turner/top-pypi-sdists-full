import argparse
import os
import sys

from fivetran_connector_sdk_common import __version__
from fivetran_connector_sdk_common.constants import (
    VALID_COMMANDS, DEFAULT_PYTHON_VERSION, SUPPORTED_PYTHON_VERSIONS, TEMPLATE_CONNECTOR_PATH, PACKAGE_SUBCOMMANDS
)
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_cli.cli_helpers import suggest_correct_command, telemetry
from fivetran_connector_sdk_cli.connector_helper import attempted_command_from_argv, safe_option_names_from_argv
from fivetran_connector_sdk_common.logger import Logging

# Single source of truth for each command's one-line help text, so the argument
# parser and the fivetran_cli plugin adapter (plugin.py) can never drift apart.
COMMAND_DESCRIPTIONS = {
    "version": "Show fivetran_connector_sdk version and exit",
    "init": "Initialize a new connector project",
    "debug": "Run connector locally in debug mode",
    "run": "Run connector locally and write to the Iceberg catalog in destination.json",
    "deploy": "Deploy connector to Fivetran",
    "package": "Package connector code into a zip file",
    "reset": "Reset connector state",
    "configuration": "Interactively collect configuration values or run setup tests",
    "help": "Show this help message and exit",
}


class _UnsupportedDebugProxyAction(argparse.Action):
    """Reject proxy flags when they are passed to a command that runs the connector on this machine."""

    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, "_reject_proxy_flags", False):
            command = parser.prog.rsplit(" ", 1)[-1]  # the command whose sub-parser met it: `debug` or `run`
            parser.error(
                f"Proxy Agent routing is not supported with `fivetran {command}`. "
                f"`{option_string}` is only supported with `fivetran deploy`. "
                f"Please run `fivetran {command}` from a machine that can reach the source directly."
            )
        setattr(namespace, self.dest, values)


def _add_force(subparser):
    subparser.add_argument("-f", "--force", action="store_true", help=argparse.SUPPRESS)

def _add_yes(subparser):
    subparser.add_argument("--yes", action="store_true", help="Automatically answers yes to all confirmation prompts")

def _add_state(subparser, hidden=False):
    subparser.add_argument("--state", type=str, default=None, metavar="<state>",
                           help=argparse.SUPPRESS if hidden else "Path to state JSON file")

def _add_configuration(subparser, help_text=None):
    subparser.add_argument("--configuration", type=str, default=None, metavar="<configuration>",
                           help=help_text if help_text else "Path to configuration JSON file")

def _add_destination_file(subparser):
    subparser.add_argument("--destination-file", type=str, default=None, metavar="<destination-file>",
                           help="Path to destination JSON file. Defaults to destination.json in the project folder")

def _add_api_key(subparser):
    subparser.add_argument("--api-key", type=str, default=None, metavar="<api-key>",
                           help="Provide your base64-encoded API key for deployment")

def _add_destination(subparser):
    subparser.add_argument("--destination", type=str, default=None, metavar="<destination>",
                           help="Destination name (aka 'group name')")

def _add_connection(subparser):
    subparser.add_argument("--connection", type=str, default=None, metavar="<connection>",
                           help="Connection name (aka 'destination schema')")

def _add_python_version(subparser):
    subparser.add_argument("--python-version", "--python", type=str, metavar="<python-version>",
                           help=f"Supported Python versions you can use: {SUPPORTED_PYTHON_VERSIONS}. Defaults to {DEFAULT_PYTHON_VERSION}")

def _add_hd_agent_id(subparser):
    subparser.add_argument("--hybrid-deployment-agent-id", type=str, metavar="<hybrid-deployment-agent-id>",
                           help="Hybrid Deployment agent ID. Defaults to the destination's default agent.")

def _add_proxy_id(subparser, hidden=False):
    if subparser.get_default("_reject_proxy_flags"):
        subparser.add_argument(
            "--proxy-id",
            nargs="?",
            const="",
            default=None,
            metavar="<proxy-id>",
            action=_UnsupportedDebugProxyAction,
            help=argparse.SUPPRESS if hidden else "Proxy Agent ID for routing connector traffic through a Proxy Agent",
        )
        return

    subparser.add_argument("--proxy-id", type=str, default=None, metavar="<proxy-id>",
                           help=argparse.SUPPRESS if hidden else "Proxy Agent ID for routing connector traffic through a Proxy Agent")

def _add_proxy_host_config_key(subparser, hidden=False):
    if subparser.get_default("_reject_proxy_flags"):
        subparser.add_argument(
            "--proxy-host-config-key",
            nargs="?",
            const="",
            default=None,
            metavar="<proxy-host-config-key>",
            action=_UnsupportedDebugProxyAction,
            help=argparse.SUPPRESS if hidden else "Configuration key that contains the host details to proxy",
        )
        return

    subparser.add_argument("--proxy-host-config-key", type=str, default=None, metavar="<proxy-host-config-key>",
                           help=argparse.SUPPRESS if hidden else "Configuration key that contains the host details to proxy")


def _add_template(subparser):
    subparser.add_argument("--template", type=str, default=TEMPLATE_CONNECTOR_PATH, metavar="<template>",
                           help="Initialize a connector project from a template. Defaults to a path in fivetran/community_connectors. Use the examples/ prefix to reference a template from fivetran/connector_sdk")

def _add_project_path(subparser):
    subparser.add_argument("project_path", nargs='?', default=os.getcwd(),
                           help="Path to connector project directory (optional, defaults to current directory)")

def _add_naming(subparser):
    subparser.add_argument("--naming", type=str, default=None, metavar="<naming>",
                           help="Naming strategy for the connection schema. Options: FIVETRAN | SOURCE. Defaults to FIVETRAN.")

def _add_deploy_package_id(subparser, hidden=False):
    subparser.add_argument("--package-id", type=str, default=None, metavar="<package-id>",
                           help=argparse.SUPPRESS if hidden else
                                "ID of an existing package to use for this connection, skipping upload of new code")

def _add_options_file(subparser):
    subparser.add_argument("--options-file", type=str, default=None, metavar="<options-file>",
                           help="Path to a local deployment options file that holds your deployment settings")

def _add_profile(subparser):
    subparser.add_argument("--profile", type=str, default="default", metavar="<profile>",
                           help="Profile to use from the deployment options file. Defaults to 'default'")

def _add_non_interactive(subparser):
    subparser.add_argument("--non-interactive", action="store_true", help="Automatically accepts the default choice for all confirmation prompts")

def _add_test(subparser):
    subparser.add_argument("--test", action="store_true",
                           help="Run all setup tests defined in configuration_form(). Only valid with the 'configuration' command.")

def _add_disable_encryption(subparser):
    subparser.add_argument("--disable-encryption", action="store_true",
                           help="Disable encryption for sensitive fields (not recommended when working with AI)")

def _add_package_id(subparser):
    subparser.add_argument("package_id", type=str, help="Unique ID of the package")

def _add_package_list_limit(subparser):
    subparser.add_argument("--limit", type=int, default=None, metavar="<limit>",
                           help="Maximum number of packages to list")


def _add_package_command(subparsers):
    return subparsers.add_parser("package", help=COMMAND_DESCRIPTIONS["package"],
                                 usage="fivetran package [project_path] [options]")

def create_argument_parser():
    command = _get_command()
    if command == "package":
        return _create_package_parser()
    return _create_argument_parser()

def _create_argument_parser():
    parser = _create_base_parser()
    parser.add_argument("--version", action="store_true",
                        help="Print the version of the fivetran_connector_sdk and exit")

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    subparsers.add_parser("version", help=COMMAND_DESCRIPTIONS["version"],
                          usage="fivetran version")

    init_subparser = subparsers.add_parser("init", help=COMMAND_DESCRIPTIONS["init"],
                                           usage="fivetran init [project_path] [options]")
    _add_project_path(init_subparser)
    _add_template(init_subparser)
    _add_force(init_subparser)
    _add_non_interactive(init_subparser)
    _add_yes(init_subparser)

    debug_subparser = subparsers.add_parser("debug", help=COMMAND_DESCRIPTIONS["debug"],
                                            usage="fivetran debug [project_path] [options]")
    debug_subparser.set_defaults(_reject_proxy_flags=True)
    _add_project_path(debug_subparser)
    _add_configuration(debug_subparser)
    _add_state(debug_subparser)
    _add_naming(debug_subparser)
    _add_proxy_id(debug_subparser, hidden=True)
    _add_proxy_host_config_key(debug_subparser, hidden=True)

    run_subparser = subparsers.add_parser("run", help=COMMAND_DESCRIPTIONS["run"],
                                          usage="fivetran run [project_path] [options]")
    run_subparser.set_defaults(_reject_proxy_flags=True)
    _add_project_path(run_subparser)
    _add_configuration(run_subparser)
    _add_state(run_subparser)
    _add_naming(run_subparser)
    _add_destination_file(run_subparser)
    _add_proxy_id(run_subparser, hidden=True)
    _add_proxy_host_config_key(run_subparser, hidden=True)

    deploy_subparser = subparsers.add_parser("deploy", help=COMMAND_DESCRIPTIONS["deploy"],
                                             usage="fivetran deploy [project_path] [options]")
    _add_project_path(deploy_subparser)
    _add_api_key(deploy_subparser)
    _add_destination(deploy_subparser)
    _add_connection(deploy_subparser)
    _add_configuration(deploy_subparser, "Path to configuration JSON file. On redeploy, existing configuration is preserved if none is provided.")
    _add_python_version(deploy_subparser)
    _add_hd_agent_id(deploy_subparser)
    _add_proxy_id(deploy_subparser)
    _add_proxy_host_config_key(deploy_subparser)
    _add_state(deploy_subparser, hidden=True)
    _add_naming(deploy_subparser)
    _add_deploy_package_id(deploy_subparser, hidden=True)
    _add_options_file(deploy_subparser)
    _add_profile(deploy_subparser)
    _add_force(deploy_subparser)
    _add_non_interactive(deploy_subparser)
    _add_yes(deploy_subparser)

    _add_package_command(subparsers)

    reset_subparser = subparsers.add_parser("reset", help=COMMAND_DESCRIPTIONS["reset"],
                                            usage="fivetran reset [project_path] [options]")
    _add_project_path(reset_subparser)
    _add_force(reset_subparser)
    _add_non_interactive(reset_subparser)
    _add_yes(reset_subparser)

    configuration_subparser = subparsers.add_parser(
        "configuration",
        help=COMMAND_DESCRIPTIONS["configuration"],
        usage="fivetran configuration [project_path] [options]",
    )
    _add_project_path(configuration_subparser)
    _add_test(configuration_subparser)
    _add_disable_encryption(configuration_subparser)
    _add_force(configuration_subparser)
    _add_non_interactive(configuration_subparser)
    _add_yes(configuration_subparser)

    subparsers.add_parser("help", help=COMMAND_DESCRIPTIONS["help"],
                          usage="fivetran help")
    return parser


def intercept_unknown_command():
    """Preserve suggest_correct_command for typos and scan sys.argv for the first positional token
    if it matches a known subcommand we normalize its case and return;
    if it does not, route through suggest_correct_command
    """
    for argv_index, token in enumerate(sys.argv[1:], start=1):
        if token.startswith("-"):
            continue
        token_lower = token.lower()
        if token_lower in VALID_COMMANDS:
            sys.argv[argv_index] = token_lower
            return
        if not suggest_correct_command(token):
            print_library_log(f"invalid command: {token}, see `fivetran help`",
                              Logging.Level.SEVERE)
        telemetry.send_cli_usage(attempted_command_from_argv(sys.argv[1:]),
                                 safe_option_names_from_argv(create_argument_parser(), sys.argv[1:]), 1, __version__)
        sys.exit(1)

def _get_command():
    if len(sys.argv) <= 1 or sys.argv[1].startswith("-"):
        return None
    return sys.argv[1].lower()

def _create_base_parser():
    parser = argparse.ArgumentParser(
        prog="fivetran", allow_abbrev=False, add_help=True,
        usage="fivetran <command> <project_path> [options]",
        description="A command-line tool for developing and deploying Fivetran connectors.",
        epilog="For more information, refer to: https://fivetran.com/docs/connector-sdk/technical-reference/connector-sdk-commands",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.set_defaults(force=False)
    parser.set_defaults(non_interactive=False)
    parser.set_defaults(yes=False)
    parser.set_defaults(test=False)
    return parser

def _add_package_subparsers(package_subparser):
    subparsers = package_subparser.add_subparsers(dest="subcommand", metavar="<operation>", required=True,
                                                  prog="fivetran package")
    pkg_create = subparsers.add_parser(
        "create",
        help="Upload a new package",
        description="Upload a new package",
        usage="fivetran package create [project_path] [options]",
    )
    _add_project_path(pkg_create)
    _add_api_key(pkg_create)
    _add_force(pkg_create)
    _add_non_interactive(pkg_create)
    _add_yes(pkg_create)

    pkg_update = subparsers.add_parser(
        "update",
        help="Update an existing package",
        description="Update an existing package",
        usage="fivetran package update <package_id> [project_path] [options]",
    )
    _add_package_id(pkg_update)
    _add_project_path(pkg_update)
    _add_api_key(pkg_update)
    _add_force(pkg_update)
    _add_non_interactive(pkg_update)
    _add_yes(pkg_update)

    pkg_list = subparsers.add_parser(
        "list",
        help="List packages in the account",
        description="List packages in the account",
        usage="fivetran package list [options]",
    )
    _add_api_key(pkg_list)
    _add_package_list_limit(pkg_list)

def _create_package_parser():
    parser = _create_base_parser()
    parser.set_defaults(version=False)

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    package_subparser = _add_package_command(subparsers)
    package_subcommand = _normalize_package_subcommand()
    if package_subcommand is not None:
        _add_package_subparsers(package_subparser)
    else:
        _add_local_package_arguments(package_subparser)
    return parser

def _normalize_package_subcommand():
    if len(sys.argv) <= 2 or sys.argv[2].startswith("-"):
        return None
    package_subcommand = sys.argv[2].lower()
    if package_subcommand not in PACKAGE_SUBCOMMANDS:
        return None
    sys.argv[2] = package_subcommand
    return package_subcommand

def _add_local_package_arguments(package_subparser):
    _add_project_path(package_subparser)
    _add_force(package_subparser)
    _add_non_interactive(package_subparser)
    _add_yes(package_subparser)
    package_subparser.set_defaults(subcommand=None)
