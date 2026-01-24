"""CLI adapter exposing test environment detection via rich-click interface.

Purpose
-------
Expose test environment detection functions via a command-line interface
using rich-click for beautiful terminal output. The CLI exposes the core
library functionality for shell scripting and CI/CD pipelines.

Contents
--------
* :data:`CLICK_CONTEXT_SETTINGS` – shared Click settings for consistent help.
* :func:`cli` – root command group with global options.
* :func:`cli_info` – print package metadata.
* :func:`cli_check` – check if any test environment is active.
* :func:`cli_pytest` – check if pytest is active.
* :func:`cli_doctest` – check if doctest is active.
* :func:`cli_setup` – check if setup.py is active.
* :func:`cli_hello` – emit greeting message (demo command).
* :func:`cli_fail` – trigger intentional failure (testing command).
* :func:`main` – entry point for console scripts.

System Role
-----------
The CLI is the primary adapter for shell scripting and CI/CD integration.
It wraps the core detect_testenv module and provides exit codes for
programmatic usage.
"""

from __future__ import annotations

from typing import Optional, Sequence

import rich_click as click
from rich.console import Console
from rich.traceback import Traceback, install as install_rich_traceback

from . import __init__conf__
from .behaviors import emit_greeting, raise_intentional_failure
from .lib_detect_testenv import (
    is_doctest_active,
    is_pytest_active,
    is_setup_active,
    is_setup_test_active,
    is_testenv_active,
)

#: Shared Click context flags for consistent help output.
CLICK_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}  # noqa: C408

#: Console for rich output
console = Console()


@click.group(
    help=__init__conf__.title,
    context_settings=CLICK_CONTEXT_SETTINGS,
    invoke_without_command=True,
)
@click.version_option(
    version=__init__conf__.version,
    prog_name=__init__conf__.shell_command,
    message=f"{__init__conf__.shell_command} version {__init__conf__.version}",
)
@click.option(
    "--traceback/--no-traceback",
    is_flag=True,
    default=True,
    help="Show full Python traceback on errors (default: enabled)",
)
@click.pass_context
def cli(ctx: click.Context, traceback: bool) -> None:
    """Root command storing global flags.

    When invoked without a subcommand, checks if any test environment is active.

    Examples
    --------
    >>> from click.testing import CliRunner
    >>> runner = CliRunner()
    >>> result = runner.invoke(cli, ["check"])
    >>> result.exit_code in (0, 1)
    True
    """
    # Store traceback preference in context
    ctx.ensure_object(dict)
    ctx.obj["traceback"] = traceback

    # If no subcommand, run the check command by default
    if ctx.invoked_subcommand is None:
        ctx.invoke(cli_check)


@cli.command("info", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_info() -> None:
    """Print resolved metadata so users can inspect installation details."""
    __init__conf__.print_info()


@cli.command("check", context_settings=CLICK_CONTEXT_SETTINGS)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress output, use exit code only",
)
@click.option(
    "--arg-string",
    type=str,
    default=None,
    help="Custom argument string to check instead of sys.argv",
)
def cli_check(quiet: bool, arg_string: Optional[str]) -> None:
    """Check if any test environment is active (pytest, doctest, or setup.py test).

    Exit codes:
        0 = Test environment detected (success)
        1 = No test environment detected (negative result)
        2 = Error occurred (failure)

    Examples:
        lib_detect_testenv check
        lib_detect_testenv check --quiet && echo "In test mode"
        lib_detect_testenv check --arg-string "pytest test.py"
    """
    try:
        is_active = is_testenv_active(arg_string=arg_string)

        if not quiet:
            if is_active:
                console.print("[green]✓[/green] Test environment detected", style="bold")
            else:
                console.print("[yellow]✗[/yellow] No test environment detected", style="bold")

        raise SystemExit(0 if is_active else 1)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error:[/red] {e}", style="bold")
        raise SystemExit(2)


@cli.command("pytest", context_settings=CLICK_CONTEXT_SETTINGS)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress output, use exit code only",
)
@click.option(
    "--arg-string",
    type=str,
    default=None,
    help="Custom argument string to check instead of sys.argv",
)
def cli_pytest(quiet: bool, arg_string: Optional[str]) -> None:
    """Check if pytest is active.

    Exit codes:
        0 = pytest detected (success)
        1 = pytest not detected (negative result)
        2 = Error occurred (failure)

    Examples:
        lib_detect_testenv pytest
        lib_detect_testenv pytest --quiet && echo "Running under pytest"
        lib_detect_testenv pytest --arg-string "/path/to/pytest/__main__.py"
    """
    try:
        is_active = is_pytest_active(arg_string=arg_string)

        if not quiet:
            if is_active:
                console.print("[green]✓[/green] pytest detected", style="bold")
            else:
                console.print("[yellow]✗[/yellow] pytest not detected", style="bold")

        raise SystemExit(0 if is_active else 1)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error:[/red] {e}", style="bold")
        raise SystemExit(2)


@cli.command("doctest", context_settings=CLICK_CONTEXT_SETTINGS)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress output, use exit code only",
)
@click.option(
    "--arg-string",
    type=str,
    default=None,
    help="Custom argument string to check instead of sys.argv",
)
def cli_doctest(quiet: bool, arg_string: Optional[str]) -> None:
    """Check if doctest is active.

    Exit codes:
        0 = doctest detected (success)
        1 = doctest not detected (negative result)
        2 = Error occurred (failure)

    Examples:
        lib_detect_testenv doctest
        lib_detect_testenv doctest --quiet && echo "Running under doctest"
        lib_detect_testenv doctest --arg-string "docrunner.py"
    """
    try:
        is_active = is_doctest_active(arg_string=arg_string)

        if not quiet:
            if is_active:
                console.print("[green]✓[/green] doctest detected", style="bold")
            else:
                console.print("[yellow]✗[/yellow] doctest not detected", style="bold")

        raise SystemExit(0 if is_active else 1)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error:[/red] {e}", style="bold")
        raise SystemExit(2)


@cli.command("setup", context_settings=CLICK_CONTEXT_SETTINGS)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress output, use exit code only",
)
@click.option(
    "--arg-string",
    type=str,
    default=None,
    help="Custom argument string to check instead of sys.argv",
)
@click.option(
    "--test-only",
    is_flag=True,
    help="Check for 'setup.py test' specifically (not just setup.py)",
)
def cli_setup(quiet: bool, arg_string: Optional[str], test_only: bool) -> None:
    """Check if setup.py is active.

    By default checks for any setup.py execution. Use --test-only to check
    specifically for 'setup.py test'.

    Exit codes:
        0 = setup.py detected (success)
        1 = setup.py not detected (negative result)
        2 = Error occurred (failure)

    Examples:
        lib_detect_testenv setup
        lib_detect_testenv setup --test-only
        lib_detect_testenv setup --quiet && echo "Running under setup.py"
        lib_detect_testenv setup --arg-string "setup.py test"
    """
    try:
        if test_only:
            is_active = is_setup_test_active(arg_string=arg_string)
            name = "setup.py test"
        else:
            is_active = is_setup_active(arg_string=arg_string)
            name = "setup.py"

        if not quiet:
            if is_active:
                console.print(f"[green]✓[/green] {name} detected", style="bold")
            else:
                console.print(f"[yellow]✗[/yellow] {name} not detected", style="bold")

        raise SystemExit(0 if is_active else 1)
    except Exception as e:
        if not quiet:
            console.print(f"[red]Error:[/red] {e}", style="bold")
        raise SystemExit(2)


@cli.command("hello", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_hello() -> None:
    """Emit a greeting message.

    This is a demonstration command showing successful execution.

    Examples:
        lib_detect_testenv hello
    """
    emit_greeting()


@cli.command("fail", context_settings=CLICK_CONTEXT_SETTINGS)
def cli_fail() -> None:
    """Trigger an intentional failure for testing error handling.

    This command always raises a RuntimeError to demonstrate error handling
    and traceback display. Useful for testing CLI error flows.

    Examples:
        lib_detect_testenv fail
        lib_detect_testenv --no-traceback fail
    """
    raise_intentional_failure()


def main(
    argv: Optional[Sequence[str]] = None,
) -> int:
    """Execute the CLI and return the exit code.

    This is the entry point used by console scripts and python -m execution.

    Parameters
    ----------
    argv:
        Optional sequence of CLI arguments. None uses sys.argv.

    Returns
    -------
    int
        Exit code: 0 for success, non-zero for errors.

    Examples
    --------
    >>> main(["hello"])
    Hello World
    0
    """
    # Check if --no-traceback flag is in arguments (default is to show traceback)
    import sys as _sys

    argv_list = list(argv) if argv else _sys.argv[1:]
    show_traceback = "--no-traceback" not in argv_list

    # Install rich traceback with locals if requested
    if show_traceback:
        install_rich_traceback(show_locals=True)

    try:
        # Use standalone_mode=False to catch exceptions ourselves
        cli(args=argv, standalone_mode=False, prog_name=__init__conf__.shell_command)
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else (1 if e.code else 0)
    except Exception as exc:
        if show_traceback:
            # Show full rich traceback with locals
            tb = Traceback.from_exception(
                type(exc),
                exc,
                exc.__traceback__,
                show_locals=True,
                width=120,
            )
            console.print(tb)
        else:
            # Show simple error message without traceback
            from rich.style import Style

            error_style = Style(color="red", bold=True)
            console.print(f"Error: {type(exc).__name__}: {exc}", style=error_style)
        return 1
