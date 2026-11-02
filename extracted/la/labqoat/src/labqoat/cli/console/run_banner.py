"""The first thing a run prints: what it is and where to open it."""

import click


class RunBanner:
    """People get a titled header with a link; agents get the exact identity on one line."""

    @staticmethod
    def lines(style: str, run: str, name: str, link: str) -> list[str]:
        """Name the run, abbreviate its identity for reading and keep it whole for machines."""
        if style == "compact":
            return [" ".join(part for part in ("run", run, name) if part)]
        title = click.style("◆ ", fg="cyan", bold=True) + click.style(name or "run", bold=True)
        return ["", f"{title}  {click.style(run[:8], dim=True)}", click.style(f"  {link}", dim=True), ""]
