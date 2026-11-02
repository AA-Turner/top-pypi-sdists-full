"""Worktree setup capability helpers."""

from __future__ import annotations

from pathlib import Path

from .worktree_setup_helpers import _quote_recovery_argument


def get_worktree_continuation_prompt(
    issue_key: str,
    workflow_name: str,
    user_request: str | None = None,
    additional_params: dict | None = None,
    model: str | None = None,
    headless: bool = False,
) -> str:
    """
    Generate a prompt for continuing a workflow after worktree setup.

    This generates a copy/paste-ready command for the appropriate continuation
    path: a new VS Code window in the default mode, or a terminal-based
    headless restart command when VS Code integration is disabled.

    Args:
        issue_key: The issue key
        workflow_name: The workflow name (e.g., "work-on-jira-issue", "pull-request-review")
        user_request: The user's explanation/request for what they want
            (AI will use this to populate Jira fields appropriately)
        additional_params: Additional parameters to include in the command
            (e.g., {"pull_request_id": "12345"})
        model: Optional Copilot model identifier to preserve in the
            continuation command.
        headless: Whether the continuation command should preserve headless mode.

    Returns:
        A formatted prompt string for the continuation path.
    """
    # Build the base command for each workflow
    workflow_base_commands = {
        "work-on-jira-issue": "agdt-initiate-work-on-jira-issue-workflow",
        "pull-request-review": "agdt-initiate-pull-request-review-workflow",
        "apply-pull-request-review-suggestions": "agdt-initiate-apply-pr-suggestions-workflow",
        "create-jira-issue": "agdt-initiate-create-jira-issue-workflow",
        "create-jira-epic": "agdt-initiate-create-jira-epic-workflow",
        "create-jira-subtask": "agdt-initiate-create-jira-subtask-workflow",
        "update-jira-issue": "agdt-initiate-update-jira-issue-workflow",
        "optimize-issue-for-ai-agent": "agdt-initiate-optimize-issue-for-ai-agent-workflow",
        "break-down-issue-into-subtasks": "agdt-initiate-break-down-issue-into-subtasks-workflow",
    }

    base_command = workflow_base_commands.get(workflow_name, "")

    if not base_command:
        if headless:
            return f"Continue working on issue {issue_key} in the current terminal."
        return f"Continue working on issue {issue_key} in the new VS Code window."

    # Build the full command with all parameters
    command_parts = [base_command, f"--issue-key {issue_key}"]

    # Add user-request if provided (for create workflows)
    if user_request:
        # Escape quotes in the value for shell safety
        escaped_request = user_request.replace('"', '\\"')
        command_parts.append(f'--user-request "{escaped_request}"')

    # Add additional parameters if provided
    if additional_params:
        param_order = ["parent_key", "pull_request_id"]
        for param_name in param_order:
            if param_name in additional_params and additional_params[param_name]:
                value = str(additional_params[param_name])
                # Escape quotes in the value for shell safety
                escaped_value = value.replace('"', '\\"')
                cli_param = param_name.replace("_", "-")
                command_parts.append(f'--{cli_param} "{escaped_value}"')

    if isinstance(model, str) and model.strip():
        command_parts.append(f"--model {_quote_recovery_argument(model.strip())}")
    if headless:
        command_parts.append("--headless")

    full_command = " ".join(command_parts)

    if headless:
        return f"""
================================================================================
📋 WORKFLOW CONTINUATION
================================================================================

The headless Copilot session should start automatically in the background.
If it did not start, run this command from the worktree to continue in headless mode:

```
{full_command}
```

This command is a fallback — normally the background session starts automatically.
================================================================================"""

    # Generate a friendly description of what to do
    return f"""
================================================================================
📋 WORKFLOW CONTINUATION
================================================================================

A Copilot session will start automatically in the new VS Code window.
If the session doesn't start, paste this command in the VS Code AI chat:

```
{full_command}
```

This command is a fallback — normally the session starts automatically.
================================================================================"""


def _wait_for_prompt_file(
    prompt_path: Path,
    timeout: float = 300,
    poll_interval: float = 5.0,
) -> bool:
    """
    Poll for a prompt file to appear on disk.

    The file may be written by a background process started by the
    auto-execute command, so we wait up to *timeout* seconds for it
    to be created.

    Args:
        prompt_path: Absolute path to the expected prompt file.
        timeout: Maximum seconds to wait (default: 300; accepts fractional seconds).
        poll_interval: Seconds between checks (default: 5).

    Returns:
        True when the file exists; False if the timeout was reached.
    """
    import time

    elapsed = 0.0
    while elapsed < timeout:
        if prompt_path.exists():
            return True
        time.sleep(poll_interval)
        elapsed += poll_interval
    return prompt_path.exists()
