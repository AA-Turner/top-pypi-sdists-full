import argparse
from typing import List, Optional

from ..actions.drop_db import drop_db
from ..arguments import Arguments
from .abstract_db_command import AbstractDbCommandRegistrar
from .base import ArgumentRegistrar


class DropDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "dropdb",
                help="Drops table(s) from the database.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "dropdb"

    async def _execute_impl(self, args: Arguments) -> None:
        await drop_db(
            connection_string=args.connection_string,
            namespace=args.namespace,
            table_names=args.table,
        )
