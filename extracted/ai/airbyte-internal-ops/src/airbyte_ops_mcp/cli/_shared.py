# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared utilities for CLI commands."""

from __future__ import annotations

import json
import sys
from typing import Any, NoReturn

from rich.console import Console
from rich.table import Table

console = Console()
error_console = Console(stderr=True)


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    console.print_json(json.dumps(data, indent=2, default=str))


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    error_console.print(f"[red]Error:[/red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]{message}[/green]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]Warning:[/yellow] {message}")


def print_table(
    title: str,
    columns: list[str],
    rows: list[list[str]],
) -> None:
    """Print data as a formatted table."""
    table = Table(title=title)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def exit_with_error(message: str, code: int = 1) -> NoReturn:
    """Print an error message and exit with the given code."""
    print_error(message)
    sys.exit(code)
