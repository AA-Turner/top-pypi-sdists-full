# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Output helpers for agents CLI."""

import json
import sys
from typing import Any

import click
from rich.console import Console as _RichConsole  # noqa: TID251
from rich.markup import escape


class Console(_RichConsole):
    """Rich Console configured with project-wide defaults (soft_wrap=True)."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("soft_wrap", True)
        super().__init__(*args, **kwargs)


def emit(data: dict) -> None:
    """Write structured data to stdout."""
    print(json.dumps(data), file=sys.stdout)


def print_error(message: str) -> None:
    """Print an error message to stderr with a red "❌ Error:" prefix."""
    # escape() so text like "[cyan]" or "[0]" in the message is shown as-is.
    Console(stderr=True, highlight=False).print(
        f"[bold red]❌ Error:[/bold red] {escape(message)}"
    )


def print_click_exception(e: click.ClickException) -> None:
    """Show a ClickException like Click does, but with a red "❌ Error:" prefix."""
    if isinstance(e, click.UsageError) and e.ctx is not None:
        hint = ""
        if e.ctx.command.get_help_option(e.ctx) is not None:
            hint = f"Try '{e.ctx.command_path} {e.ctx.help_option_names[0]}' for help.\n"
        click.echo(f"{e.ctx.get_usage()}\n{hint}", err=True, color=e.ctx.color)
    print_error(e.format_message())
