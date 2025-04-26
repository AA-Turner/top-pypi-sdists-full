import argparse
import logging

from ..arguments import environment_default
from .base import ArgumentRegistrar


def log_level_name(level: int) -> str:
    name: str = logging.getLevelName(level)
    return name.lower()


class _HelpAction(argparse._HelpAction):
    def __call__(self, parser, namespace, values, option_string=None):  # type: ignore
        parser.print_help()
        print()

        # get subparsers from parser
        subparsers_actions = [
            action
            for action in parser._actions
            if isinstance(action, argparse._SubParsersAction)
        ]

        for subparsers_action in subparsers_actions:
            # print subparsers' help
            for choice, subparser in subparsers_action.choices.items():
                print("Command '{}'".format(choice))
                print(subparser.format_help())

        parser.exit()


# Argument registrar classes
class BaseUrlArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--base-url",
            metavar="URL",
            help="Base URL of the DAP API.",
            action=environment_default("DAP_API_URL"),  # type: ignore
        )


class OAuthCredentialsArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--client-id",
            metavar="ClientID",
            help="OAuth client ID obtained from the Identity Service.",
            action=environment_default("DAP_CLIENT_ID"),  # type: ignore
        )

        parser.add_argument(
            "--client-secret",
            metavar="ClientSecret",
            help="OAuth client secret obtained from the Identity Service.",
            action=environment_default("DAP_CLIENT_SECRET"),  # type: ignore
        )


class LogLevelArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--loglevel",
            choices=[
                log_level_name(level)
                for level in (
                    logging.DEBUG,
                    logging.INFO,
                    logging.WARN,
                    logging.ERROR,
                )
            ],
            default=log_level_name(logging.INFO),
            help="Sets log verbosity.",
        )
        parser.add_argument(
            "--logfile",
            metavar="LogFile",
            help="Sets the path of the file to save logs to.",
        )


class HelpArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--help", "-h", action=_HelpAction, help="Show this help message and exit."
        )
