"""An unlisted visit to the goat, which knows what is running and reacts to whoever is watching."""

from __future__ import annotations

import sys
from functools import partial

import click

from labqoat.cli.bleat_report import BleatReport
from labqoat.cli.bleat_session import BleatSession
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.key_queue import KeyQueue
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.goat import Goat
from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand


class BleatCommand(StrictCommand):
    """Report the herd of running runs: as JSON, as a still drawing, or as a goat that answers keys."""

    def __init__(self) -> None:
        """Construct the command, kept out of help so it is found rather than read about."""
        super().__init__("bleat", help="Ask the goat what has been running longest.", hidden=True)

    def invoke(self, ctx: click.Context) -> object:
        """Read the herd once, then show it in the way the invocation and the terminal allow."""
        context = ContextAccessor.current()
        client = context.management()
        try:
            report = BleatReport.read(client)
            if context.output_mode == "json":
                ResultWriter().write_dict(report)
            elif self.watched():
                keys = KeyQueue()
                keys.start()
                BleatSession(sys.stdout, partial(BleatReport.read, client), keys.next).run(report)
            else:
                click.echo("\n".join([Goat.still(), "", "meh.", "", *BleatReport.lines(report)]))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def watched() -> bool:
        """Whether someone is at a terminal that can both show the goat move and send it keys."""
        return OutputStyle.interactive(sys.stdout) and sys.stdin.isatty()
