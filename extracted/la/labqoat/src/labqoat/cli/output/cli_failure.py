"""Click failure carrying one stable process exit code."""

from __future__ import annotations

import click
from typing import IO
import sys

from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.output.output_style import OutputStyle
from labqoat.json_document import JsonDocument


class CliFailure(click.ClickException):
    """Rendered command failure with an explicit exit status."""

    def __init__(
        self,
        message: str,
        exit_code: int,
        problem: JsonDocument | None = None,
        resource_id: str | None = None,
        *,
        reported: bool = False,
    ) -> None:
        """Store the message and requested exit status."""
        super().__init__(message)
        self._exit_code = exit_code
        self.problem = problem
        self.resource_id = resource_id
        self.reported = reported
        context = click.get_current_context(silent=True)
        self.mode = self.output_mode(context)
        self.key = context.meta.get("mutation_key") if context is not None else None

    @staticmethod
    def output_mode(context: click.Context | None) -> str:
        """Read presentation even when root configuration failed before constructing a client."""
        if context is None:
            return "human"
        root = context.find_root()
        return str(root.meta.get("output_mode", getattr(root.obj, "output_mode", "human")))

    def show(self, file: IO[str] | None = None) -> None:
        """Write one failure to stderr unless the person already saw it; machine modes always get the document."""
        if self.mode == "human":
            if not self.reported:
                self.explain(file or sys.stderr)
            return
        writer = JsonWriter(stream=file or sys.stderr, pretty=self.mode == "pretty")
        writer.write(
            {
                "exit_code": self.exit_code,
                "message": self.format_message(),
                "problem": self.problem,
                "resource_id": self.resource_id,
                "key": self.key,
            }
        )

    def explain(self, stream: IO[str]) -> None:
        """A marked message for a person, with the key that makes a retry safe; one tagged line for a pipe."""
        if OutputStyle.current(stream) == "compact":
            click.echo(f"error {self.format_message()}", file=stream)
            return
        click.echo(f"{click.style('✗', fg='red', bold=True)} {self.format_message()}", file=stream)
        if self.key is not None:
            click.echo(click.style(f"  retry safely with --key {self.key}", dim=True), file=stream)

    @property
    def exit_code(self) -> int:
        """Return the stable exit status."""
        return self._exit_code

    @exit_code.setter
    def exit_code(self, value: int) -> None:
        """Set the stable exit status."""
        self._exit_code = value
