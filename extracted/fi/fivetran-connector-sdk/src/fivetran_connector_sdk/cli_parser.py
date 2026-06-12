import argparse
import os
import sys

from fivetran_connector_sdk.constants import (
    VALID_COMMANDS, DEFAULT_PYTHON_VERSION, SUPPORTED_PYTHON_VERSIONS, TEMPLATE_CONNECTOR_PATH
)
from fivetran_connector_sdk.helpers import print_library_log, suggest_correct_command
from fivetran_connector_sdk.logger import Logging


def _add_force(subparser):
    subparser.add_argument("-f", "--force", action="store_true", help="Deprecated; use --non-interactive")

def _add_state(subparser, hidden=False):
    subparser.add_argument("--state", type=str, default=None, metavar="<state>",
                           help=argparse.SUPPRESS if hidden else "Path to state JSON file")

def _add_configuration(subparser):
    subparser.add_argument("--configuration", type=str, default=None, metavar="<configuration>",
                           help="Path to configuration JSON file")

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


def _add_template(subparser):
    subparser.add_argument("--template", type=str, default=TEMPLATE_CONNECTOR_PATH, metavar="<template>",
                           help="Initialize a sample connector project from repository path")

def _add_project_path(subparser):
    subparser.add_argument("project_path", nargs='?', default=os.getcwd(),
                           help="Path to connector project directory (optional, defaults to current directory)")

def _add_naming(subparser):
    subparser.add_argument("--naming", type=str, default=None, metavar="<naming>",
                           help="Naming strategy for the connection schema. Options: FIVETRAN | SOURCE. Defaults to FIVETRAN.")

def _add_non_interactive(subparser):
    subparser.add_argument("--non-interactive", action="store_true", help="Use non-interactive mode")

def create_argument_parser():
    parser = argparse.ArgumentParser(
        prog="fivetran", allow_abbrev=False, add_help=True,
        usage="fivetran <command> <project_path> [options]",
        description="A command-line tool for developing and deploying Fivetran connectors.",
        epilog="For more information, refer to: https://fivetran.com/docs/connector-sdk/technical-reference/connector-sdk-commands",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--version", action="store_true",
                        help="Print the version of the fivetran_connector_sdk and exit")

    # Set a default at the top level so the attribute always exists on the namespace
    # subparsers that register --force override it when the user passes the flag.
    parser.set_defaults(force=False)
    parser.set_defaults(non_interactive=False)

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    subparsers.add_parser("version", help="Show fivetran_connector_sdk version and exit",
                          usage="fivetran version")

    init_subparser = subparsers.add_parser("init", help="Initialize a new connector project",
                                           usage="fivetran init [project_path] [options]")
    _add_project_path(init_subparser)
    _add_template(init_subparser)
    _add_force(init_subparser)
    _add_non_interactive(init_subparser)

    debug_subparser = subparsers.add_parser("debug", help="Run connector locally in debug mode",
                                            usage="fivetran debug [project_path] [options]")
    _add_project_path(debug_subparser)
    _add_configuration(debug_subparser)
    _add_state(debug_subparser)
    _add_naming(debug_subparser)

    deploy_subparser = subparsers.add_parser("deploy", help="Deploy connector to Fivetran",
                                             usage="fivetran deploy [project_path] [options]")
    _add_project_path(deploy_subparser)
    _add_api_key(deploy_subparser)
    _add_destination(deploy_subparser)
    _add_connection(deploy_subparser)
    _add_configuration(deploy_subparser)
    _add_python_version(deploy_subparser)
    _add_hd_agent_id(deploy_subparser)
    _add_state(deploy_subparser, hidden=True)
    _add_naming(deploy_subparser)
    _add_force(deploy_subparser)
    _add_non_interactive(deploy_subparser)

    package_subparser = subparsers.add_parser("package", help="Package connector code into a zip file",
                                              usage="fivetran package [project_path] [options]")
    _add_project_path(package_subparser)
    _add_force(package_subparser)
    _add_non_interactive(package_subparser)

    reset_subparser = subparsers.add_parser("reset", help="Reset connector state",
                                            usage="fivetran reset [project_path] [options]")
    _add_project_path(reset_subparser)
    _add_force(reset_subparser)
    _add_non_interactive(reset_subparser)

    subparsers.add_parser("help", help="Show this help message and exit",
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
        sys.exit(1)
