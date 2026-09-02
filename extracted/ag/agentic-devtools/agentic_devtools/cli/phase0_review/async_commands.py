"""Background-task wrapper for the Phase 0 factual review."""

from agentic_devtools.background_tasks import run_function_in_background
from agentic_devtools.task_state import print_task_tracking_info

_COMMANDS_MODULE = "agentic_devtools.cli.phase0_review.commands"


def phase0_review_async() -> None:
    """Start the read-only Phase 0 review in a background task."""
    task = run_function_in_background(
        module_path=_COMMANDS_MODULE,
        function_name="phase0_review_command",
        command_display_name="agdt-phase0-review",
    )
    print_task_tracking_info(task, "Reviewing Phase 0 issue.md")
