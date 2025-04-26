import argparse

from ..arguments import environment_default
from .base import ArgumentRegistrar


class DatabaseConnectionStringArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--connection-string",
            metavar="DBCONNSTR",
            action=environment_default("DAP_CONNECTION_STRING"),  # type: ignore
            help="The connection string used to connect to the target database.",
        )
