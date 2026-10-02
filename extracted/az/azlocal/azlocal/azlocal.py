#!/usr/bin/env python

"""
Utility to help you configure the `az` CLI tool to talk to the LocalStack Emulator.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from . import __version__
from .constants import AZURE_CONFIG_DIR_ENV
from .shared import (
    AZURE_CONFIG_DIR,
    LS_HOST,
    check_emulator_is_running,
    get_proxy_endpoint,
    get_proxy_env_vars,
    prepare_environment,
    run_in_background,
)

DEFAULT_CLOUD_NAME = "AzureCloud"
CUSTOM_CLOUD_NAME = "LocalStack"


HELP_TEXT_START_INTERCEPTION = """
Configure the Azure CLI to route requests to the LocalStack Emulator, instead of using the real Azure cloud.

See also: azlocal stop-interception.
"""

HELP_TEXT_STOP_INTERCEPTION = """
Restore the Azure CLI configuration to its original state.
Disables redirection to the local emulator and re-configures the CLI to send commands to the official Azure platform management REST API.

See also: azlocal start-interception.
"""


def usage() -> None:
    print(__doc__.strip())


def run_in_current_process(cmd: list[str], env: dict[str, str] | None = None) -> None:
    """
    Replaces this process with the AZ CLI process, with the given command and environment
    """
    os.execvpe(cmd[0], cmd, env)  # type: ignore[arg-type]


def run(cmd: list[str], verbose: bool) -> tuple[str, str]:
    if verbose:
        print(f"Executing command '{cmd}'...")
    process = subprocess.run(cmd, capture_output=True)
    if verbose and process.stdout:
        print(process.stdout.decode())
    if verbose and process.stderr:
        print(process.stderr.decode())
    if process.returncode:
        if not verbose and process.stderr:
            # Only print this if provided, and if it hasn't been printed already
            print(process.stderr.decode())
        exit(process.returncode)
    return process.stdout.decode(), process.stderr.decode()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter, exit_on_error=False
    )
    parser.add_argument("-v", "--version", action="store_true")

    help_endpoint_arg = """The local endpoint URL of the LocalStack instance.

Alternatively, use an environment variable to configure this:
LOCALSTACK_HOST=https://{endpoint}:{port}"""

    commands = parser.add_subparsers(dest="command")
    start_interception_parser = commands.add_parser(
        "start-interception",
        description=HELP_TEXT_START_INTERCEPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    start_interception_parser.add_argument(
        "-e",
        "--endpoint",
        metavar="LOCALSTACK_HOST",
        required=False,
        help=help_endpoint_arg,
        default=LS_HOST,
    )
    start_interception_parser.add_argument("--verbose", action=argparse.BooleanOptionalAction)

    stop_interception_parser = commands.add_parser(
        "stop-interception",
        description=HELP_TEXT_STOP_INTERCEPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    stop_interception_parser.add_argument("--verbose", action=argparse.BooleanOptionalAction)

    try:
        args, unknown = parser.parse_known_args()

        if args.version:
            print(__version__)
        elif args.command == "start-interception":
            use_custom_cloud(endpoint=args.endpoint, verbose=args.verbose)
        elif args.command == "stop-interception":
            use_regular_cloud(verbose=args.verbose)
        else:
            parser.print_help()

    except argparse.ArgumentError as e:
        # User invoked azlocal without any arguments
        # Assume that the user wants to use any of the known commands
        if "the following arguments are required" in str(e):
            parser.print_help()
            exit(0)

        # Backwards compatibility
        # The user could invoke the CLI as if it were an 'az' replacement:
        #    azlocal group list
        # If that's the case, we redirect the existing 'az' command via a proxy to our Emulator
        run_as_separate_process()


def use_custom_cloud(endpoint: str, verbose: bool) -> None:
    check_emulator_is_running()

    # Create the CustomCloud first
    create_custom_cloud(emulator_endpoint=endpoint, verbose=verbose)
    # Configure the CLI to use our CustomCloud
    run(["az", "cloud", "set", "--name", CUSTOM_CLOUD_NAME, "--only-show-errors"], verbose=verbose)
    # Our endpoint is not whitelisted, so we need to disable the endpoint validation
    run(["az", "config", "set", "core.instance_discovery=false", "--only-show-errors"], verbose=verbose)
    # Login
    run(
        ["az", "login", "--service-principal", "-u", "any-app", "-p", "any-pass", "--tenant", "anytenant"],
        verbose=verbose,
    )
    print(
        "LocalStack interception started. Azure CLI commands are now routed to LocalStack for Azure REST API.\n"
        "Run 'azlocal stop-interception' to restore traffic to Azure management endpoints."
    )


def use_regular_cloud(verbose: bool) -> None:
    # Configure the endpoint to use the default cloud
    run(["az", "cloud", "set", "--name", DEFAULT_CLOUD_NAME], verbose=verbose)
    # Re-enable instance discovery
    run(["az", "config", "set", "core.instance_discovery=true", "--only-show-errors"], verbose=verbose)
    print(
        "LocalStack interception stopped. Azure CLI commands are now routed to Azure management REST API.\n"
        "Run 'azlocal start-interception' to redirect traffic back to LocalStack for Azure."
    )


def create_custom_cloud(emulator_endpoint: str, verbose: bool) -> None:
    register_or_update = "register"

    stdout, _ = run(["az", "cloud", "list", "--query", "[].name"], verbose=verbose)
    if CUSTOM_CLOUD_NAME in stdout:
        # This cloud has already been created earlier
        # The endpoints exposed by our Emulator may have changed in the meantime though
        # That's why we always update the existing cloud
        register_or_update = "update"

    cloud_config = {
        # Note that some endpoints have an additional slash
        # This is in-line with the output of the Azure cloud config
        # Because of this, the AZ CLI will append a path without a slash
        # If we do not add the slash ourselves, we get a path like:
        # https://azure.localhost.localstack.cloud:4566subscriptions/00000000
        "endpoints": {
            "activeDirectory": emulator_endpoint,
            "activeDirectoryResourceId": emulator_endpoint,
            "activeDirectoryGraphResourceId": emulator_endpoint,
            "management": f"{emulator_endpoint}/",
            "microsoftGraphResourceId": f"{emulator_endpoint}/",
            "resourceManager": f"{emulator_endpoint}/",
            "logAnalyticsResourceId": emulator_endpoint,
        }
    }

    run(
        [
            "az",
            "cloud",
            register_or_update,
            "--name",
            CUSTOM_CLOUD_NAME,
            "--cloud-config",
            json.dumps(cloud_config),
        ],
        verbose=verbose,
    )


def run_as_separate_process() -> None:
    """
    Constructs a command line string and calls "az" as an external process.
    """

    cmd_args = list(sys.argv)
    cmd_args[0] = "az"
    if ("--help" in cmd_args) or ("--version" in cmd_args):
        # Early exit - if we only want to know the version/help, we don't need LS to be running
        run_in_current_process(cmd_args, None)
        return

    check_emulator_is_running()

    proxy_endpoint = get_proxy_endpoint()

    env_dict = prepare_environment(proxy_endpoint)

    env_dict[AZURE_CONFIG_DIR_ENV] = AZURE_CONFIG_DIR
    if not os.path.exists(AZURE_CONFIG_DIR):
        # Create the config directory
        Path(AZURE_CONFIG_DIR).mkdir(parents=True, exist_ok=True)

        # Prepare necessary arguments to ensure `az ..` commands are run against this config directory
        az_args_list = [f"{key}={val}" for key, val in get_proxy_env_vars(proxy_endpoint).items()]
        az_args_list.append(f"{AZURE_CONFIG_DIR_ENV}={AZURE_CONFIG_DIR}")
        az_arg = " ".join(az_args_list)

        # Turn off telemetry
        survey_command = f"{az_arg} az config set output.show_survey_link=no --only-show-errors"
        run_in_background(survey_command)
        telemetry_command = f"{az_arg} az config set core.collect_telemetry=false --only-show-errors"
        run_in_background(telemetry_command)

        # Login to ensure the config directory has credentials
        login_command = f"{az_arg} az login --service-principal -u any-app -p any-pass --tenant any-tenant"
        run_in_background(login_command)

    # Hijack the login command
    # When creating our custom config dir, we automatically log in - so this is not necessary anymore
    if len(cmd_args) == 2 and cmd_args[1] == "login":
        print("Login Succeeded")
        return

    # Hijack the ACR login command
    if len(cmd_args) > 1 and cmd_args[1] == "acr" and "login" in cmd_args:
        print("Login Succeeded")
        return

    # run the command
    run_in_current_process(cmd_args, env_dict)


if __name__ == "__main__":
    main()
