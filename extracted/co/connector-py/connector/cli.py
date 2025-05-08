import asyncio
import copy
import gzip
import json
import logging
import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from datetime import datetime, timezone
from typing import Any

from connector.config import config
from connector.httpx_rewrite import proxy_settings
from connector.logging import set_logger_config
from connector.oai.integration import Integration
from connector.pydantic import get_pydantic_model
from connector.utils import proxy_utils

logger = logging.getLogger("integration-connectors.sdk")

# Hacking commands
# ----------------


def _prep_hacking_command(args: Namespace):
    data = vars(args)
    data.pop("command")
    data.pop("func")
    return data


def http_integration_server(
    integration: Integration, port: int = 8000, reload: bool = False, use_proxy: bool = False
):
    from connector.http_server import runserver

    try:
        runserver(port=port, reload=reload, integration=integration, use_proxy=use_proxy)
    except KeyboardInterrupt:
        pass


def build_executable(path: str) -> None:
    try:
        subprocess.run(["pyinstaller", "--version"], check=True)
    except FileNotFoundError:
        print("PyInstaller not found in PATH. Please pip install pyinstaller")
        return

    command = [
        "pyinstaller",
        path,
        "--noconsole",
        "--onefile",
        "--clean",
        "--paths=projects/libs/python/connector-sdk",
    ]
    if __file__ not in "site-packages":
        command.append("--paths=projects/libs/python/connector-sdk")
    subprocess.run(command)


def create_integration_hacking_parser(integration: Integration, parser: ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="command")

    http_server_parser = subparsers.add_parser(
        "http-server",
        help="Run this connector as an HTTP server.",
        description="\n".join(
            [
                "Run this connector as an HTTP server.",
                " - You can call capabilities via POST /<capability name> with the input JSON as the request body.",
                " - API docs are at /docs",
                " - The OpenAPI spec is at /openapi.json",
            ]
        ),
        formatter_class=RawDescriptionHelpFormatter,
    )
    http_server_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="The port to run the server on."
    )
    http_server_parser.add_argument(
        "--reload", action="store_true", help="Enable hot reload for the server."
    )
    http_server_parser.add_argument(
        "--use-proxy", "--sip", action="store_true", help="Use the Lumos SIP to proxy requests."
    )
    http_server_parser.set_defaults(
        func=lambda args: http_integration_server(integration, **_prep_hacking_command(args))
    )

    build_executable_parser = subparsers.add_parser(
        "build-executable",
        help=(
            "Create a single file executable with PyInstaller. Provide the path to your library's"
            " main.py file."
        ),
    )
    build_executable_parser.add_argument("path", type=str, help="The path to the main.py file.")
    build_executable_parser.set_defaults(
        func=lambda args: build_executable(**_prep_hacking_command(args))
    )

    return None


# Actual Commands
# ---------------


def get_result_file_path(args: Namespace) -> str | None:
    if not args.result_file_path:
        return None
    result_file_path = args.result_file_path.strip('"').strip("'")
    if not result_file_path.endswith(".gz"):
        raise ValueError("The result file name must end with the .gz extension.")
    return result_file_path


def get_json_value(args: Namespace) -> str | None:
    if not args.json and not args.json_file:
        return None
    if args.json_file:
        with open(args.json_file.strip('"').strip("'")) as f:
            return f.read()
    return args.json


def capability_executor(integration: Integration, args: Namespace):
    """Executes a command from the CLI."""
    # validate that a valid gzip file name was provided
    result_file_path = get_result_file_path(args)

    if args.command == "info":
        output = json.dumps(integration.info().model_dump(), sort_keys=True)
    else:
        json_value = get_json_value(args)
        if json_value is None:
            raise ValueError("No JSON value provided")
        if args.use_proxy:
            with proxy_settings(
                proxy_url=proxy_utils.get_proxy_url(),
                proxy_headers={
                    "X-Lumos-Proxy-Auth": proxy_utils.get_proxy_token_sync().token,
                },
            ):
                output = asyncio.run(integration.dispatch(args.command, json_value))
        else:
            output = asyncio.run(integration.dispatch(args.command, json_value))

    if result_file_path:
        logger.info(f"Attempting to open file name: {result_file_path}")
        with open(result_file_path, "w") as result_file:
            logger.info(f"File opened to write: {result_file_path}")
            logger.info("compressing result")
            output_bytes = output.encode("utf-8")
            gzipped_result = gzip.compress(output_bytes)
            logger.info("writing compressed result to file")
            result_file.buffer.write(gzipped_result)
            logger.info("compressed result written to file")
        logger.info(f"Result saved to {args.result_file_path}")
    else:
        logger.info("Result printing to console")
        print(output)

    logger.info("Command completed")


CAPABILITY_PREFIX = "\n      "


def collect_capabilities(integration: Integration, no_print: bool = False) -> ArgumentParser:
    """
    Collect all methods from an Integration class and create a CLI
    command for each.
    """
    executed = os.path.basename(sys.argv[0])
    capability_helps: list[str] = []
    capability_helps = sorted(integration.capabilities.keys())
    parser = ArgumentParser(
        description=f"Lumos integration CLI for {integration.description_data.user_friendly_name}",
        usage=f"""{executed} CAPABILITY [--json JSON STRING] [--json-file JSON FILEPATH] [--result-file-path FILEPATH]

    Examples:

    {executed} info
        Print the Info schema for how to call this connector, and what it supports. This is the only
        capability that takes no arguments.

    {executed} validate_credentials --json '{"{}"}'
        Check if you're passing enough auth credentials and settings to connect to the underlying
        app tenant.

    All capabilities except 'info' require a JSON argument or a JSON file argument.

    A typical JSON argument looks like

    {"{"}
        "auth": {"{...}"},
        "settings": {"{...}"},
        "request": {"{...}"}
    {"}"}

    All capabilities:

{CAPABILITY_PREFIX}{CAPABILITY_PREFIX.join([c for c in capability_helps])}

""",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparser = subparsers.add_parser("info", description=integration.info.__doc__)
    _add_arguments_to_subparser(subparser)
    subparser.set_defaults(func=lambda args: capability_executor(integration, args))

    for capability_name, capability in integration.capabilities.items():
        subparser = subparsers.add_parser(capability_name, description=capability.__doc__)

        try:
            get_pydantic_model(capability.__annotations__)
        except ValueError:
            pass
        else:
            group = subparser.add_mutually_exclusive_group(required=True)
            group.add_argument("--json", type=str, help="JSON input")
            group.add_argument("--json-file", type=str, help="JSON file input")
            _add_arguments_to_subparser(subparser)

        subparser.set_defaults(func=lambda args: capability_executor(integration, args))

    hacking_subparser = subparsers.add_parser("hacking")
    create_integration_hacking_parser(integration, hacking_subparser)

    return parser


def _add_arguments_to_subparser(subparser: ArgumentParser):
    subparser.add_argument(
        "--result-file-path",
        type=str,
        help=(
            "The path to the file to save the result to. If this file already exists, "
            "its content will be overwritten. If not provided, the result will be "
            "printed to the console. The result file will be gzip compressed so the "
            "input file name should end with the .gz extension."
        ),
        default=None,
    )
    subparser.add_argument(
        "--use-proxy",
        "--sip",
        action="store_true",
        help="Use the Lumos SIP to proxy requests. This should not be used by non-Lumos developers.",
    )


def run_integration(
    integration: Integration,
    no_print: bool = False,
) -> None:
    set_logger_config(integration.app_id)
    logger.info("Running command started at %s", datetime.now(timezone.utc))
    try:
        """Run a command from the CLI, integration version."""
        parser = collect_capabilities(integration, no_print)
        args = parser.parse_args()
        try:
            logger.info("Command arguments: %s", build_loggable_args(args, integration))
        except Exception:
            logger.exception("Error building loggable arguments")
        if not args.command:
            print("No command passed in", file=sys.stderr)
            parser.print_help(file=sys.stderr)
            sys.exit(1)
        args.func(args)
    except Exception as e:
        logger.error(
            f"Error running command exception class: {e.__class__.__name__} exception: {e}"
        )
        logger.error("Stack trace:", exc_info=True)
        raise e
    logger.info("Command completed at %s", datetime.now(timezone.utc))


def build_loggable_args(args: Namespace, integration: Integration) -> dict[str, Any]:
    loggable_args = copy.deepcopy(args.__dict__)
    if loggable_args.get("json"):
        json_obj = json.loads(args.json)
        redact_json_obj(json_obj, get_integration_secret_fields(integration))
        loggable_args["json"] = json_obj
    return loggable_args


BASE_REDACTED_LOG_KEYS = [
    "password",
    "secret",
    "token",
    "api_key",
    "api_token",
    "api_secret",
    "access_token",
    "refresh_token",
    "secret",
    "client_secret",
    "consumer_secret",
    "token_secret",
]


def get_integration_secret_fields(integration: Integration) -> list[str]:
    all_secret_fields = []
    secret_settings_fields = [
        name
        for name, field_info in integration.settings_model.model_fields.items()
        # Mypy doesn't recognize the None check here
        if field_info.json_schema_extra is not None and field_info.json_schema_extra.get("x-secret")  # type: ignore
    ]
    all_secret_fields.extend(secret_settings_fields)

    integration_auth_model = integration.auth
    if integration_auth_model is not None:
        secret_auth_fields = [
            name
            for name, field_info in integration_auth_model.model_fields.items()
            if field_info.json_schema_extra is not None
            and field_info.json_schema_extra.get("x-secret")  # type: ignore
        ]
        all_secret_fields.extend(secret_auth_fields)
    return all_secret_fields


def redact_json_obj(json_obj: dict[str, Any], secret_fields: list[str]) -> None:
    # redacts keys in the json object that are in the REDACTED_KEYS set
    # acts on the object in place
    redacted_keys = {
        k.lower()
        for k in BASE_REDACTED_LOG_KEYS + config.additional_redacted_log_keys + secret_fields
    }
    for key, value in json_obj.items():
        if isinstance(value, dict):
            redact_json_obj(value, secret_fields)
        elif isinstance(value, list):
            for item in value:
                redact_json_obj(item, secret_fields)
        elif isinstance(value, str):
            if key.lower() in redacted_keys:
                json_obj[key] = "REDACTED"
