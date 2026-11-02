"""Help text with styled headings and names on a terminal."""

from collections.abc import Iterable

import click


class PrettyHelp(click.HelpFormatter):
    """Color what a reader scans for; redirected help stays plain because styling is stripped off terminals."""

    def write_heading(self, heading: str) -> None:
        """Section titles stand out from their entries."""
        super().write_heading(click.style(heading, bold=True))

    def write_usage(self, prog: str, args: str = "", prefix: str | None = None) -> None:
        """The command line itself is the brightest thing on the page."""
        super().write_usage(click.style(prog, fg="cyan", bold=True), args, prefix)

    def write_dl(self, rows: Iterable[tuple[str, str]], col_max: int = 30, col_spacing: int = 2) -> None:
        """Command and option names are colored; their descriptions keep the default tone."""
        styled = [(click.style(name, fg="cyan"), text) for name, text in rows]
        super().write_dl(styled, col_max, col_spacing)
