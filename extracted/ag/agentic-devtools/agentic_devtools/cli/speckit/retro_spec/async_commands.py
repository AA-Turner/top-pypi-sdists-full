"""Background wrapper and CLI entry point for agdt-speckit-retro-spec.

Spawns the retro-spec command as a background task and provides the
argparse CLI entry point.
"""

from __future__ import annotations

import argparse

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.cli.speckit.nest.async_commands import positive_int
from agentic_devtools.task_state import print_task_tracking_info

_COMMANDS_MODULE = "agentic_devtools.cli.speckit.retro_spec.commands"


def retro_spec_async_command() -> None:
    """CLI entry point for agdt-speckit-retro-spec.

    Parses arguments and spawns the retro-spec command as a background task.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-retro-spec",
        description="Generate a retroactive spec from implementation artifacts.",
    )
    parser.add_argument(
        "--issue",
        type=positive_int,
        required=True,
        help="The closed issue number to generate a spec for.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print the generated spec without writing files or creating commits.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output path for the spec file (skips hierarchy placement).",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        default=False,
        help="Create a git commit after writing the spec.",
    )
    parser.add_argument(
        "--specs-root",
        type=str,
        default=None,
        help=argparse.SUPPRESS,
    )

    args = parser.parse_args()

    task = run_function_in_background(
        module_path=_COMMANDS_MODULE,
        function_name="retro_spec_command",
        command_display_name="agdt-speckit-retro-spec",
        func_kwargs={
            "issue_number": args.issue,
            "specs_root": args.specs_root,
            "dry_run": args.dry_run,
            "output": args.output,
            "commit": args.commit,
        },
    )

    print_task_tracking_info(task)
