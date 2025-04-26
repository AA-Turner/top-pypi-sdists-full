import argparse

from ..arguments import EnumAction
from ..dap_types import Format
from .base import ArgumentRegistrar


class TableArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--table",
            required=True,
            help="Table name or comma separated list of table names whose data to fetch. Use 'all' to fetch all tables in the namespace.",
        )


class FormatArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--format",
            type=Format,
            action=EnumAction,
            default=Format.JSONL,
            help="Data output format.",
        )


class OutputDirectoryArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--output-directory",
            metavar="DIR",
            default="downloads",
            help="Directory where the query result will be downloaded to. Can be an absolute or relative path.",
        )


class NamespaceArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--namespace",
            required=True,
            help="Identifies the data source.",
        )
