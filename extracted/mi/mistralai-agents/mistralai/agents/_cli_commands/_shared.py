"""Helpers every `agents` command renders with."""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


@contextmanager
def loading_spinner(description: str) -> Iterator[Callable[[str], None]]:
    # Show a spinner the instant a command starts, before the ~2s SDK/engine import runs, so every
    # command feels reactive. transient=True erases the spinner on exit, so command output/errors are
    # emitted cleanly after the `with` block closes (no residual frame). Yields a set_stage callback so
    # the caller can relabel the spinner as it moves through real stages (loading SDK, discovering agent).
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=Console(),
        refresh_per_second=30,
    ) as progress:
        task_id = progress.add_task(f"[bold blue]{description}", start=True)

        def set_stage(stage: str) -> None:
            progress.update(task_id, description=f"[bold blue]{stage}")

        yield set_stage


def fail(*lines: str) -> typer.Exit:
    # The first line with text is the error, in red; the lines after it say what to do, in the default color.
    # A caller may lead with a blank line to set the error apart. Click strips the color off a non-terminal.
    error_shown = False
    for line in lines:
        is_error = not error_shown and bool(line)
        typer.secho(line, err=True, fg=typer.colors.RED if is_error else None)
        error_shown = error_shown or is_error
    return typer.Exit(1)


def can_prompt() -> bool:
    return sys.stdin.isatty()
