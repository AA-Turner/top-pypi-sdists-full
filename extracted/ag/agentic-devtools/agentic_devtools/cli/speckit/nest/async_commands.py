"""Background wrapper and CLI entry point for agdt-speckit-nest.

Spawns the nest command as a background task and provides the argparse
CLI entry point.
"""

from __future__ import annotations

import argparse
import sys

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.task_state import print_task_tracking_info

from .commands import nest_command

_COMMANDS_MODULE = "agentic_devtools.cli.speckit.nest.commands"


def positive_int(value: str) -> int:
    """Parse a CLI argument that must be a positive integer issue number.

    Args:
        value: The raw CLI argument value.

    Returns:
        The parsed integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not an integer greater
            than zero.
    """
    try:
        parsed = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a positive integer issue number, got: {value!r}") from None
    if parsed <= 0:
        raise argparse.ArgumentTypeError(f"expected a positive integer issue number, got: {parsed}")
    return parsed


def nest_async_command() -> None:
    """CLI entry point for agdt-speckit-nest.

    Parses arguments and spawns the nest command as a background task.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-nest",
        description="Preview a spec migration plan; --execute asks for confirmation before queueing the migration.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Preview the plan, require an affirmative prompt response, then queue the migration.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Compute and display plan without making any changes.",
    )
    parser.add_argument(
        "--scope",
        type=positive_int,
        default=None,
        help="Limit migration to this issue number and its descendants.",
    )
    parser.add_argument(
        "--issue",
        type=positive_int,
        default=None,
        help="Alias for --scope. Takes precedence over --scope when both are given.",
    )
    parser.add_argument(
        "--owner",
        type=str,
        default=None,
        help="GitHub repository owner (auto-detected from git remote if omitted).",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="GitHub repository name (auto-detected from git remote if omitted).",
    )
    parser.add_argument(
        "--specs-root",
        type=str,
        default=None,
        help="Path to the specs/ directory (defaults to ./specs).",
    )

    args = parser.parse_args()

    # --issue is an alias for --scope and wins when both are supplied.
    scope = args.issue if args.issue is not None else args.scope
    approved_plan_fingerprint: str | None = None

    if args.execute and not args.dry_run:
        # Preview the computed plan before requesting confirmation so users
        # can explicitly approve the migration they are about to run.
        try:
            approved_plan_fingerprint = nest_command(
                specs_root=args.specs_root,
                execute=False,
                dry_run=True,
                scope=scope,
                owner=args.owner,
                repo=args.repo,
            )
        except SystemExit as exc:
            if exc.code not in (None, 0):
                raise
            return
        if approved_plan_fingerprint is None:
            return
        try:
            answer = input("Execute this migration plan in a background task? [y/N] ")
        except (EOFError, OSError):
            print("Migration cancelled: confirmation was not available.", file=sys.stderr)
            return
        if answer.strip().lower() not in {"y", "yes"}:
            print("Migration cancelled.", file=sys.stderr)
            return

    task = run_function_in_background(
        module_path=_COMMANDS_MODULE,
        function_name="nest_command",
        command_display_name="agdt-speckit-nest",
        func_kwargs={
            "specs_root": args.specs_root,
            "execute": args.execute,
            "dry_run": args.dry_run,
            "scope": scope,
            "owner": args.owner,
            "repo": args.repo,
            "expected_plan_fingerprint": approved_plan_fingerprint,
        },
    )

    print_task_tracking_info(task)
