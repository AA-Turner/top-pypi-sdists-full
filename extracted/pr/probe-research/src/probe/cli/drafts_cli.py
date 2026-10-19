"""`probe draft edit` and `probe file preview`: two local file commands.

    probe draft edit <path>     change a checked-out summary or note draft in
                                place: the old and the new text on stdin
                                (`probe.drafts.EDIT_FORMAT`), the old found
                                exactly once
    probe file preview <path>   what a data file holds, without running it: a
                                CSV/TSV's header and first rows, a JSON
                                document's shape, a Parquet or NumPy file's
                                schema and first values (`probe.daemon.reader`)

Neither talks to Probe. The Probe daemon's `bash` answers both in its own
process (`daemon.tools._local_command`), with its own read rules; here they
run as anyone's command.
"""

from __future__ import annotations

import sys
from pathlib import Path

import typer

draft_app = typer.Typer(no_args_is_help=True, help="change a checked-out summary or note draft")
file_app = typer.Typer(no_args_is_help=True, help="look at a local file without running it")


@draft_app.command("edit")
def draft_edit(path: str = typer.Argument(..., help="the draft (`probe summary checkout` printed it)")) -> None:
    """Replace one exact piece of a draft. The change comes on stdin:

    <<<<<<< OLD / the text as it is now / ======= NEW / what replaces it / >>>>>>> END"""
    from probe import drafts

    stdin = None if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
    code, text = drafts.edit(path, stdin, Path.cwd())
    print(text, file=sys.stdout if code == 0 else sys.stderr)
    raise typer.Exit(code)


@file_app.command("preview")
def file_preview(path: str = typer.Argument(..., help="a CSV/TSV, JSON, Parquet or NumPy file")) -> None:
    """A data file's shape and first rows, nothing run (never a pickle)."""
    from probe.daemon import reader

    text = reader.render(Path(path).expanduser())
    print(text)
    raise typer.Exit(1 if text.startswith("not read:") else 0)
