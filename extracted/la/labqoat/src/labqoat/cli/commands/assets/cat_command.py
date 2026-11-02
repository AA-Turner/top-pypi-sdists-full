"""``lab asset cat``: print a small text asset, such as a JSON report, without saving it first."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from labqoat.assets_client import AssetsClient


class CatCommand:
    """Read one verified text asset of at most a mebibyte to standard output."""

    name = "cat"
    limit = 1_048_576

    @staticmethod
    def callback(reference: str) -> None:
        """Print the asset's text exactly as stored."""
        client = ContextAccessor.current().assets()
        try:
            click.echo(CatCommand.text(client, reference), nl=False)
        finally:
            client.close()

    @classmethod
    def text(cls, client: AssetsClient, reference: str) -> str:
        """The asset's text after checking its size, its digest and that it is UTF-8."""
        record = client.get(reference)
        download = f"lab asset download {reference} --output FILE"
        if record.byte_size > cls.limit:
            mebibytes = record.byte_size / cls.limit
            raise CliFailure(
                f"{reference} is {mebibytes:.1f} MiB; lab asset cat prints at most 1 MiB. Use {download}.", 1
            )
        data = client.download(reference)
        if hashlib.sha256(data).hexdigest() != record.sha256:
            raise CliFailure(f"The bytes of {reference} do not match its digest; retry.", 1)
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise CliFailure(f"{reference} is not text ({record.media_type}). Use {download}.", 1) from error

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Build the Click command."""
        return StrictCommand(
            cls.name,
            callback=cls.callback,
            help="Print a small text asset (a JSON report, a log, a config) without saving it.",
            params=[click.Argument(["reference"], type=str)],
        )
