import argparse
from typing import List, Type
import pkg_resources
from spotml.commands.abstract_command import AbstractCommand
from spotml.commands.aws import AwsCommand
from spotml.commands.download import DownloadCommand
from spotml.commands.exec import ExecCommand
from spotml.commands.handle_error_runs import HandleErroredRunCommand
from spotml.commands.run import ManageCommand
from spotml.commands.handle_scheduled_run import HandleScheduledRunCommand
from spotml.commands.run_locally import RunLocallyCommand
from spotml.commands.sh import ShCommand
from spotml.commands.start import StartCommand
from spotml.commands.status import StatusCommand
from spotml.commands.stop import StopCommand
from spotml.commands.handle_active_run import HandleActiveRunCommand
from spotml.commands.sync import SyncCommand


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='store_true', help='Display the version of the spotml')

    command_classes = [
       StartCommand,
       StopCommand,
       StatusCommand,
       ShCommand,
       ManageCommand,
       RunLocallyCommand,
       HandleScheduledRunCommand,
       HandleActiveRunCommand,
       HandleErroredRunCommand,
       ExecCommand,
       SyncCommand,
       DownloadCommand,
       AwsCommand,
    ] + _get_custom_commands()

    # add commands to the parser
    add_subparsers(parser, command_classes)

    return parser


def add_subparsers(parser: argparse.ArgumentParser, command_classes: List[Type[AbstractCommand]]):
    """Adds commands to the parser."""
    subparsers = parser.add_subparsers()
    for command_class in command_classes:
        command = command_class()
        subparser = subparsers.add_parser(command.name, help=command.description, description=command.description)
        subparser.set_defaults(command=command, parser=subparser)
        command.configure(subparser)


def _get_custom_commands() -> List[Type[AbstractCommand]]:
    """Returns custom commands that integrated through entry points."""
    return [entry_point.load() for entry_point in pkg_resources.iter_entry_points('spotml.commands')]
