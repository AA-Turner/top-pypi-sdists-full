"""Worktree setup capability helpers."""

from __future__ import annotations

import sys
from dataclasses import dataclass

from agentic_devtools.cli.git.core import GitError

from .worktree_setup_cleanup import _sanitize_worktree_setup_diagnostic, check_worktree_exists
from .worktree_setup_environment import setup_worktree_environment
from .worktree_setup_helpers import _quote_recovery_argument, generate_workflow_branch_name


@dataclass
class PlaceholderIssueResult:
    """Result of placeholder issue creation."""

    success: bool
    issue_key: str | None = None
    error_message: str | None = None


def create_placeholder_issue(
    project_key: str,
    issue_type: str = "Task",
    parent_key: str | None = None,
) -> PlaceholderIssueResult:
    """
    Create a placeholder Jira issue with minimal fields.

    This creates an issue with a placeholder summary and description
    that will be updated later in the workflow.

    Args:
        project_key: Jira project key (e.g., "PROJECT")
        issue_type: Issue type (Task, Epic, Sub-task)
        parent_key: Parent issue key (required for Sub-task type)

    Returns:
        PlaceholderIssueResult with success status and issue key
    """
    try:
        from ..jira.create_commands import create_issue_sync

        # Generate placeholder values
        placeholder_summary = f"[Placeholder] {issue_type} created via workflow"
        placeholder_description = (
            "This issue was created as a placeholder by the workflow automation.\n\n"
            "Please update the summary, description, and other fields as needed."
        )
        placeholder_labels = ["workflow-placeholder"]

        # For Epic, we need an epic name
        epic_name = None
        if issue_type.lower() == "epic":
            epic_name = placeholder_summary

        print(f"Creating placeholder {issue_type} in project {project_key}...")

        result = create_issue_sync(
            project_key=project_key,
            summary=placeholder_summary,
            issue_type=issue_type,
            description=placeholder_description,
            labels=placeholder_labels,
            epic_name=epic_name,
            parent_key=parent_key,
        )

        issue_key = result.get("key")
        if issue_key:
            print(f"✅ Placeholder {issue_type} created: {issue_key}")
            return PlaceholderIssueResult(success=True, issue_key=issue_key)
        else:
            return PlaceholderIssueResult(
                success=False,
                error_message="API did not return an issue key",
            )

    except Exception as e:
        return PlaceholderIssueResult(
            success=False,
            error_message=str(e),
        )


def create_placeholder_and_setup_worktree(
    project_key: str,
    issue_type: str = "Task",
    parent_key: str | None = None,
    workflow_name: str = "create-jira-issue",
) -> tuple[bool, str | None]:
    """
    Create a placeholder issue and set up a worktree for it.

    This is the main entry point for create workflows that need both
    issue creation and environment setup.

    Args:
        project_key: Jira project key (e.g., "PROJECT")
        issue_type: Issue type (Task, Epic, Sub-task)
        parent_key: Parent issue key (required for Sub-task type)
        workflow_name: Name of the workflow for branch-name generation

    Returns:
        Tuple of (success, issue_key). If success is True, issue_key contains
        the created issue key. If success is False, issue_key is None unless
        placeholder issue creation succeeded before setup failed.
    """
    print(f"\n{'=' * 80}")
    print(f"CREATE WORKFLOW: {workflow_name}")
    print("=" * 80)

    # Step 1: Create placeholder issue
    print("\n📝 Step 1: Creating placeholder Jira issue...")
    issue_result = create_placeholder_issue(
        project_key=project_key,
        issue_type=issue_type,
        parent_key=parent_key,
    )

    if not issue_result.success:
        print(f"\n❌ Failed to create placeholder issue: {issue_result.error_message}")
        return False, None

    issue_key = issue_result.issue_key
    if issue_key is None:
        return False, None
    print(f"   Issue key: {issue_key}")

    # Set the issue key in state for later use
    from ...state import set_value

    set_value("jira.issue_key", issue_key)

    # Step 2: Set up worktree environment
    print("\n🔧 Step 2: Setting up worktree environment...")

    # Check if worktree already exists (unlikely for new issue, but check anyway)
    try:
        existing_path = check_worktree_exists(issue_key)
    except (GitError, FileNotFoundError, OSError, ValueError) as exc:
        error_message = f"Unable to verify existing worktree: {_sanitize_worktree_setup_diagnostic(exc)}"
        print(f"\n❌ {error_message}", file=sys.stderr)
        return False, issue_key
    if existing_path:
        print(f"   Worktree already exists at: {existing_path}")
        return True, issue_key

    # Generate branch name based on issue type and workflow
    branch_name = generate_workflow_branch_name(
        issue_key=issue_key,
        issue_type=issue_type,
        workflow_name=workflow_name,
        parent_key=parent_key,
    )

    # Create new worktree with generated branch name
    result = setup_worktree_environment(
        issue_key=issue_key,
        branch_name=branch_name,
        open_vscode=False,
    )

    if result.success:
        print("\n✅ Environment setup complete!")
        print(f"   Worktree: {result.worktree_path}")
        print(f"   Branch: {result.branch_name}")
        return True, issue_key
    else:
        print(f"\n❌ Worktree setup failed: {result.error_message}")
        print(f"   Issue {issue_key} was created but environment setup failed.")
        print("   Please set up the worktree manually:")
        if result.worktree_path:
            print(
                "   git worktree add "
                f"{_quote_recovery_argument(result.worktree_path)} -b {_quote_recovery_argument(branch_name)}"
            )
        else:
            print(
                "   Resolve the 'worktree_folder' project.json setting "
                f"reported above, then run: git worktree add <path> -b {_quote_recovery_argument(branch_name)}"
            )
        return False, issue_key
