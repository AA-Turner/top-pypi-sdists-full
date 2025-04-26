import argparse

from ..timestamp import valid_utc_datetime
from .base import ArgumentRegistrar


class SinceArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--since",
            metavar="DATETIME",
            required=True,
            help="Start timestamp for an incremental query. Examples: 2022-06-13T09:30:00Z or 2022-06-13T09:30:00+02:00.",
            type=valid_utc_datetime,
        )


class UntilArgumentRegistrar(ArgumentRegistrar):
    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--until",
            metavar="DATETIME",
            required=False,
            help="End timestamp for an incremental query. Examples: 2022-06-13T09:30:00Z or 2022-06-13T09:30:00+02:00.",
            type=valid_utc_datetime,
        )
