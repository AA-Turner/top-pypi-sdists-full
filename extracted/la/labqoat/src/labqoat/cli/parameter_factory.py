"""Reusable strict Click parameter declarations for canonical commands."""

from __future__ import annotations

from collections.abc import Sequence

import click

from labqoat.cli.reference_argument import ReferenceArgument


class ParameterFactory:
    """Create consistent positional arguments and bounded filter options."""

    @staticmethod
    def argument(name: str) -> click.Argument:
        """Create one required text argument; record references also accept a unique shortened identifier."""
        kind = ReferenceArgument.kinds.get(name)
        return click.Argument([name], type=str if kind is None else ReferenceArgument(kind), required=True)

    @staticmethod
    def limit(default: int = 100, maximum: int | None = 500) -> click.Option:
        """Create a positive bounded page-size option."""
        return click.Option(
            ["--limit"],
            type=click.IntRange(min=1, max=maximum),
            default=default,
            show_default=True,
        )

    @staticmethod
    def text_option(name: str, required: bool = False) -> click.Option:
        """Create a text-valued long option."""
        return click.Option([f"--{name.replace('_', '-')}", name], type=str, required=required)

    @staticmethod
    def time_option(name: str) -> click.Option:
        """Create a timezone-aware ISO-8601 option."""
        from labqoat.cli.timezone_type import TimezoneType

        return click.Option([f"--{name.replace('_', '-')}", name], type=TimezoneType())

    @staticmethod
    def path_argument(name: str, exists: bool = False, file_only: bool = False) -> click.Argument:
        """Create one filesystem path argument."""
        return click.Argument(
            [name],
            type=click.Path(path_type=str, exists=exists, dir_okay=not file_only),
            required=True,
        )

    @staticmethod
    def integer_option(name: str, minimum: int | None = None, default: int | None = None) -> click.Option:
        """Create an integer-valued long option."""
        return click.Option(
            [f"--{name.replace('_', '-')}", name],
            type=click.IntRange(min=minimum),
            default=default,
            show_default=default is not None,
        )

    @staticmethod
    def choice_option(
        name: str,
        choices: Sequence[str],
        default: str | None = None,
    ) -> click.Option:
        """Create a closed-choice long option."""
        return click.Option(
            [f"--{name.replace('_', '-')}", name],
            type=click.Choice(tuple(choices)),
            default=default,
            show_default=default is not None,
        )

    @staticmethod
    def yes() -> click.Option:
        """Create the noninteractive deletion-confirmation flag."""
        return click.Option(["--yes"], is_flag=True, default=False)

    @staticmethod
    def all_projects() -> click.Option:
        """Create the flag that widens a list from the selected project to every project."""
        return click.Option(
            ["--all-projects"],
            is_flag=True,
            flag_value="true",
            default=None,
            help="List every project's rows instead of only the selected project's.",
        )

    @staticmethod
    def follow() -> click.Option:
        """Create the shared operational log-following flag."""
        return click.Option(["-f", "--follow"], is_flag=True, help="Stream log entries until interrupted.")
