"""Cli for cache"""

from typing import TYPE_CHECKING, Any

import os
import argparse

from dlt._workspace.cli import SupportsCliCommand, echo as fmt

from dlthub.common.cli import add_project_opts
from dlthub.project.pipeline_manager import EntityFactory
from dlthub.project.cli.helpers import project_from_args_with_cli_output

if TYPE_CHECKING:
    from dlthub.cache.cache import Cache
else:
    Cache = Any


class CacheCommand(SupportsCliCommand):
    command = "cache"
    help_string = "Manage dlthub project local data cache. Experimental."
    description = """
Commands to manage local data cache for dlthub project.

**This is an experimental feature and will change substantially in the future.**

**Do not use in production.**
"""

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        add_project_opts(parser)

        operation_parser = parser.add_subparsers(
            title="Available subcommands", dest="operation", required=True
        )

        # add all ops
        operation_parser.add_parser("info", help="Shows cache info")

        operation_parser.add_parser("show", help="Connects to cache engine")

        operation_parser.add_parser("drop", help="Drop the cache")

        operation_parser.add_parser("populate", help="Populate the cache from the defined inputs")

        operation_parser.add_parser("flush", help="Flush the cache to the defined outputs")

        operation_parser.add_parser(
            "create-persistent-secrets",
            help="Create persistent secrets on cache for remote access.",
        )

        operation_parser.add_parser(
            "clear-persistent-secrets",
            help="Clear persistent secrets from cache for remote access.",
        )

    def cache_basic_info(self, cache: Cache) -> bool:
        cache_location = cache.cache_location
        fmt.echo("Cache query engine: %s" % fmt.bold("duckdb"))
        fmt.echo("Local cache path: %s" % fmt.bold(cache_location))
        if not os.path.exists(cache_location):
            fmt.warning("Cache not yet initialized")
            return False
        return True

    def execute(self, args: argparse.Namespace) -> None:
        run_context = project_from_args_with_cli_output(args)

        factory = EntityFactory(run_context.project)

        # individual pond ops
        cache = factory.get_cache(".")
        if args.operation == "drop":
            cache.drop()
        elif args.operation == "create-persistent-secrets":
            cache.create_persistent_secrets()
        elif args.operation == "clear-persistent-secrets":
            cache.clear_persistent_secrets()
        elif args.operation == "populate":
            cache.populate()
        elif args.operation == "flush":
            cache.flush()
        elif args.operation == "info":
            self.cache_basic_info(cache)
        elif args.operation == "show":
            if self.cache_basic_info(cache):
                fmt.echo("Launching duckdb console...")
                import subprocess

                subprocess.call(["duckdb", cache.cache_location])
