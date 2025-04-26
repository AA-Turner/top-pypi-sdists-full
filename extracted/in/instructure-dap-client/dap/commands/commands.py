import argparse
from typing import Callable, List, Optional

from .. import __version__
from ..api import DAPClient
from ..arguments import Arguments
from ..dap_types import Credentials, IncrementalQuery, SnapshotQuery, TableQuery
from .base import ArgumentRegistrar, CommandRegistrar


def parse_snapshot(args: Arguments) -> SnapshotQuery:
    return SnapshotQuery(format=args.format, mode=None)


def parse_incremental(args: Arguments) -> IncrementalQuery:
    return IncrementalQuery(
        format=args.format, mode=None, since=args.since, until=args.until
    )


class SetDefaultsRegistrar(ArgumentRegistrar):
    def __init__(self, parse_query: Callable[[Arguments], TableQuery]) -> None:
        self.parse_query = parse_query

    def register(self, parser: argparse.ArgumentParser) -> None:
        parser.set_defaults(parse_query=self.parse_query)


class DapCommandRegistrar(CommandRegistrar):
    async def execute(self, args: Arguments) -> bool:
        executed = await super().execute(args)
        if not executed:
            raise NotImplementedError(f"failed to run command: {args.command}")
        return executed

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        parser = argparse.ArgumentParser(
            description="Invokes the DAP API to fetch table snapshots and incremental updates.",
            epilog="For more information, check out the OpenAPI specification for DAP API: https://data-access-platform-api.s3.amazonaws.com/index.html",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=False,
        )
        parser.prog = "dap"
        parser.add_argument(
            "--version", action="version", version="%(prog)s " + __version__
        )
        return parser

    def _create_subparsers(
        self, parser: Optional[argparse.ArgumentParser]
    ) -> Optional[argparse._SubParsersAction]:
        if parser is not None:
            return parser.add_subparsers(
                help="Command to execute, e.g. initiate a snapshot or an incremental query, or get list of tables.",
                required=True,
                dest="command",
            )
        else:
            return None


class SnapshotCommandRegistrar(CommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        arguments.append(SetDefaultsRegistrar(parse_query=parse_snapshot))
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "snapshot",
                help="Performs a snapshot query.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "snapshot"

    async def _execute_impl(self, args: Arguments) -> None:
        query = args.parse_query(args)
        async with DAPClient(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
        ) as session:
            await session.download_tables_data(
                args.namespace,
                args.table,
                query,
                args.output_directory,
            )


class IncrementalCommandRegistrar(CommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        arguments.append(SetDefaultsRegistrar(parse_query=parse_incremental))
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "incremental",
                help="Performs an incremental query with a given start, and (optionally) end timestamp.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "incremental"

    async def _execute_impl(self, args: Arguments) -> None:
        query = args.parse_query(args)
        async with DAPClient(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
        ) as session:
            await session.download_tables_data(
                args.namespace,
                args.table,
                query,
                args.output_directory,
            )


class ListCommandRegistrar(CommandRegistrar):
    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "list",
                help="Lists the name of all tables available for querying in the specified namespace.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "list"

    async def _execute_impl(self, args: Arguments) -> None:
        async with DAPClient(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
        ) as session:
            tables = await session.get_tables(args.namespace)
            for t in tables:
                print(t)


class SchemaCommandRegistrar(CommandRegistrar):
    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "schema",
                help="Returns the JSON schema that records in the table conform to.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "schema"

    async def _execute_impl(self, args: Arguments) -> None:
        async with DAPClient(
            base_url=args.base_url,
            credentials=Credentials.create(
                client_id=args.client_id, client_secret=args.client_secret
            ),
        ) as session:
            await session.download_tables_schema(
                args.namespace, args.table, args.output_directory
            )
