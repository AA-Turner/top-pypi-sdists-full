"""Manage assets via the labqoat API."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from labqoat.cli.cli_context import CliContext
    from labqoat.json_document import JsonDocument

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class DownloadCommand:
    """Manage assets via the labqoat API."""

    name = "download"

    @staticmethod
    def callback(**kwargs: object) -> None:
        """Execute the command."""
        context = ContextAccessor.current()
        result = DownloadCommand.run(context, kwargs)
        ResultWriter().write_dict(result)

    @staticmethod
    def run(context: CliContext, kwargs: Mapping[str, object]) -> JsonDocument:
        """Run the domain operation and return JSON data."""
        from labqoat.cli.command_runner import CommandRunner

        return CommandRunner.assets_download(context, kwargs)

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Build the Click command."""
        return StrictCommand(
            cls.name,
            callback=cls.callback,
            help="Download, checksum-verify, and save one asset.",
            params=[
                click.Argument(["reference"], type=str),
                click.Option(
                    ["--output"],
                    type=click.Path(dir_okay=False, path_type=str),
                    required=True,
                    help="Destination file.",
                ),
            ],
        )
