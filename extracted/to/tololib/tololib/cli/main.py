import logging
from argparse import ArgumentParser
from sys import stdout
from typing import Dict

from .common import Command
from .device_simulator import DeviceSimulatorCommand
from .discover import DiscoverCommand
from .get_settings import GetSettingsCommand
from .get_status import GetStatusCommand


def main() -> int:
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "-l", "--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO"
    )

    commands: Dict[str, Command] = {}
    command_parser = argument_parser.add_subparsers(title="command", dest="command", required=True)
    for command_name, command_class in [
        ("discover", DiscoverCommand),
        ("device-simulator", DeviceSimulatorCommand),
        ("get-settings", GetSettingsCommand),
        ("get-status", GetStatusCommand),
    ]:
        commands[command_name] = command_class(command_parser.add_parser(command_name))

    args = argument_parser.parse_args()

    # configure logging
    log_handler = logging.StreamHandler(stdout)
    log_handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(name)-44s [%(levelname)s] %(message)s"))
    logging.basicConfig(handlers=[log_handler], level=logging.getLevelName(args.log_level))

    # execute command
    command = commands[args.command]
    return command(args)
