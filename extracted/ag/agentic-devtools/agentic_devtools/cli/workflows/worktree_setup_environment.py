"""Worktree setup capability helpers."""

from __future__ import annotations

from .worktree_setup_cleanup import _sanitize_worktree_setup_diagnostic
from .worktree_setup_repository import WorktreeSetupResult, WorktreeSetupScriptResult

_DEFAULT_SETUP_SCRIPT_TIMEOUT_SECONDS = 1800


def setup_worktree_environment(
    issue_key: str,
    branch_prefix: str = "feature",
    branch_name: str | None = None,
    use_existing_branch: bool = False,
    open_vscode: bool = True,
    defer_path_settings: bool = False,
    defer_task_permission_settings: bool = False,
    target_setup_timeout: int = _DEFAULT_SETUP_SCRIPT_TIMEOUT_SECONDS,
) -> WorktreeSetupResult:
    """
    Complete worktree setup: create worktree and open VS Code.

    This is the main entry point for setting up a new development environment
    for an issue. It:
    1. Creates a git worktree for the issue
    2. Injects ``.vscode/settings.json`` with Git for Windows PATH entries (Windows only)
    3. Injects ``.vscode/settings.json`` with Python Scripts directory PATH entries (all platforms)
    4. Injects ``task.allowAutomaticTasks: "on"`` into the VS Code settings
    5. Runs ``.agdt/agentic-devtools-worktree-setup.py`` if present
    6. Opens VS Code with the workspace file only after target setup succeeds

    When ``defer_path_settings`` is True, steps 2-3 are left to the caller.
    When ``defer_task_permission_settings`` is True, step 4 is left to the
    caller. Background workflow setup may defer both so any nested auto-execute
    command sees a clean tracked workspace file; the caller applies these
    settings only after the nested command succeeds and before VS Code opens.

    Args:
        issue_key: The issue key (e.g., "PROJECT-1234")
        branch_prefix: Prefix for the branch name (default: "feature").
            Ignored if branch_name is provided.
        branch_name: Exact branch name to use. If provided, branch_prefix is ignored.
            Used for PR review workflows where the branch already exists on origin.
        use_existing_branch: If True and branch_name is provided, checkout the
            existing branch from origin instead of creating a new one.
        open_vscode: Whether to open VS Code (default: True)
        defer_path_settings: Leave PATH settings injection to the caller
            (default: False).
        defer_task_permission_settings: Leave automatic-task permission
            injection to the caller (default: False).
        target_setup_timeout: Maximum time in seconds for the target setup
            script (default: 1800).

    Returns:
        WorktreeSetupResult with success status and details.  A present target
        setup script that fails returns an unsuccessful result and prevents VS
        Code from opening.
    """
    from .worktree_setup import (
        create_worktree,
        inject_git_path_settings,
        inject_python_path_settings,
        inject_task_permission_settings,
        open_vscode_workspace,
        run_worktree_setup_script,
    )

    if target_setup_timeout < 0:
        raise ValueError("target_setup_timeout must be non-negative")
    # Step 1: Create worktree
    result = create_worktree(
        issue_key=issue_key,
        branch_prefix=branch_prefix,
        branch_name=branch_name,
        use_existing_branch=use_existing_branch,
    )

    if not result.success:
        return result

    # Step 2: Inject VS Code settings for Windows Git PATH
    if not defer_path_settings:
        inject_git_path_settings(result.worktree_path)

    # Step 3: Inject VS Code settings for Python/agdt-* Scripts PATH (all platforms)
    if not defer_path_settings:
        inject_python_path_settings(result.worktree_path)

    # Step 4: Inject task.allowAutomaticTasks permission for runOn:folderOpen tasks
    if not defer_task_permission_settings:
        inject_task_permission_settings(result.worktree_path)

    # Step 5: Run project-specific worktree setup script if present
    script_result = run_worktree_setup_script(
        result.worktree_path,
        timeout_seconds=target_setup_timeout,
    )
    if isinstance(script_result, WorktreeSetupScriptResult):
        script_status = script_result.status
        if script_status not in {"missing", "succeeded", "failed"}:
            script_status = "failed"
            script_result = WorktreeSetupScriptResult(
                status="failed",
                error_message="target setup script returned an invalid status",
                category="execution",
            )
    else:
        # Keep callers that mock the historical no-return helper compatible.
        script_status = "succeeded"

    if script_status == "failed":
        category = script_result.category or "execution"
        error_message = _sanitize_worktree_setup_diagnostic(
            f"{category}: {script_result.error_message or 'target setup script failed'}"
        )
        result.success = False
        result.target_setup_status = "failed"
        result.target_setup_exit_code = (
            str(script_result.exit_code)
            if script_result.exit_code is not None
            else "timeout"
            if category == "timeout"
            else "blocked"
        )
        result.target_setup_error = error_message
        result.error_message = _sanitize_worktree_setup_diagnostic(f"target setup script failure: {error_message}")
        return result

    result.target_setup_status = script_status
    result.target_setup_exit_code = (
        str(script_result.exit_code)
        if isinstance(script_result, WorktreeSetupScriptResult) and script_result.exit_code is not None
        else "0"
    )
    result.target_setup_error = None

    # Step 6: Open VS Code
    if open_vscode:
        result.vscode_opened = open_vscode_workspace(result.worktree_path)

    return result
