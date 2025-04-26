import argparse
from typing import List, Optional

from ..actions.init_db import init_db
from ..arguments import Arguments
from ..dap_types import Credentials
from .abstract_db_command import AbstractDbCommandRegistrar
from .base import ArgumentRegistrar


class InitDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "initdb",
                help="Performs a snapshot query and persists the result in the database for given table(s).",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "initdb"

    async def _execute_impl(self, args: Arguments) -> None:
        await init_db(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
            connection_string=args.connection_string,
            namespace=args.namespace,
            table_names=args.table,
        )
