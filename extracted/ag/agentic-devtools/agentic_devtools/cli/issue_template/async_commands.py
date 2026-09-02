"""Background task wrapper and CLI entry point for agdt-render-issue.

Validates state, prints task ID and output path immediately,
then spawns the render command as a background task.
"""

from __future__ import annotations

import argparse
import sys

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.state import get_state_dir, get_value, set_value
from agentic_devtools.task_state import print_task_tracking_info

_COMMANDS_MODULE = "agentic_devtools.cli.issue_template.commands"
_OUTPUT_FILENAME = "issue.md"


def render_issue_async(template: str | None = None) -> None:
    """Render issue.md as a background task.

    Stores the optional template path in state, validates that issue_key
    is present, prints the task ID and output path immediately, then
    spawns render_issue_command in the background.

    Args:
        template: Optional path to a template file override.
    """
    if template is not None:
        set_value("issue_template.template_path", template)

    issue_key = get_value("issue_key")
    if not issue_key:
        issue_key = get_value("jira.issue_key")
    if not issue_key:
        print(
            "Error: issue_key is required. Use: agdt-set issue_key <KEY>",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = get_state_dir() / _OUTPUT_FILENAME
    task = run_function_in_background(
        module_path=_COMMANDS_MODULE,
        function_name="render_issue_command",
        command_display_name="agdt-render-issue",
    )

    print_task_tracking_info(task)
    print(f"Output will be written to: {output_path}")


def render_issue_async_cli() -> None:
    """CLI entry point for agdt-render-issue.

    Parses --template flag and delegates to render_issue_async.
    """
    parser = argparse.ArgumentParser(
        prog="agdt-render-issue",
        description="Render a NormalizedIssue to issue.md using templates.",
    )
    parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Path to a template file override (bypasses template selection).",
    )
    args = parser.parse_args()
    render_issue_async(template=args.template)
