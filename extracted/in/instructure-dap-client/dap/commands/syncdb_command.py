import argparse
from typing import List, Optional

from ..actions.sync_db import sync_db
from ..arguments import Arguments
from ..dap_types import Credentials, Format, IncrementalQuery
from .abstract_db_command import AbstractDbCommandRegistrar
from .base import ArgumentRegistrar
from .commands import SetDefaultsRegistrar


def parse_syncdb(args: Arguments) -> IncrementalQuery:
    return IncrementalQuery(
        format=Format.JSONL,
        mode=None,
        since=args.since,
        until=None,
    )


class SyncDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        arguments.append(SetDefaultsRegistrar(parse_query=parse_syncdb))
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "syncdb",
                help="Performs an incremental query and persists the result in the database for given table(s).",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "syncdb"

    async def _execute_impl(self, args: Arguments) -> None:
        await sync_db(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
            connection_string=args.connection_string,
            namespace=args.namespace,
            table_names=args.table,
        )
