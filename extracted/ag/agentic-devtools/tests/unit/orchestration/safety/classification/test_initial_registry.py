"""Tests for the initial builtin tool classification registry."""

from __future__ import annotations

from agentic_devtools.orchestration.safety.classification import (
    ActionClassification,
    build_default_registry,
)


class TestInitialRegistry:
    """Verify all builtin tools are classified per FR-002."""

    def test_all_builtins_classified(self) -> None:
        """Every registered builtin must have a classification entry."""
        registry = build_default_registry()
        expected_tools = {
            "git_stage_all",
            "git_save_work",
            "git_push",
            "git_force_push",
            "git_get_current_branch",
            "git_current_branch",
            "git_get_status",
            "jira_add_comment",
            "jira_get_issue",
            "get_issue_context",
            "azure_devops_create_pr",
            "azure_devops_reply_to_thread",
            "azure_devops_resolve_thread",
            "azure_devops_approve_pull_request",
            "github_get_pr_state",
            "github_get_pr_checks_status",
            "github_add_comment",
            "filesystem_read_file",
            "filesystem_write_file",
            "filesystem_list_directory",
            "testing_run_tests",
            "testing_run_pattern",
            "state_get",
            "state_set",
            "reply_to_pull_request_thread",
        }
        assert expected_tools.issubset(registry.tool_names)

    def test_git_force_push_is_destructive(self) -> None:
        registry = build_default_registry()
        entry = registry.get("git_force_push")
        assert entry.classification == ActionClassification.destructive

    def test_read_only_tools(self) -> None:
        registry = build_default_registry()
        read_only_tools = [
            "git_get_current_branch",
            "git_current_branch",
            "git_get_status",
            "jira_get_issue",
            "get_issue_context",
            "github_get_pr_state",
            "github_get_pr_checks_status",
            "filesystem_read_file",
            "filesystem_list_directory",
            "state_get",
        ]
        for tool_name in read_only_tools:
            entry = registry.get(tool_name)
            assert entry.classification == ActionClassification.read_only, f"{tool_name} should be read_only"

    def test_external_mutation_tools(self) -> None:
        registry = build_default_registry()
        external_tools = [
            "git_save_work",
            "git_push",
            "jira_add_comment",
            "azure_devops_create_pr",
            "azure_devops_reply_to_thread",
            "azure_devops_resolve_thread",
            "azure_devops_approve_pull_request",
            "github_add_comment",
            "reply_to_pull_request_thread",
        ]
        for tool_name in external_tools:
            entry = registry.get(tool_name)
            assert entry.classification == ActionClassification.external_mutation, (
                f"{tool_name} should be external_mutation"
            )

    def test_local_mutation_tools(self) -> None:
        registry = build_default_registry()
        local_tools = [
            "git_stage_all",
            "filesystem_write_file",
            "testing_run_tests",
            "testing_run_pattern",
            "state_set",
        ]
        for tool_name in local_tools:
            entry = registry.get(tool_name)
            assert entry.classification == ActionClassification.local_mutation, f"{tool_name} should be local_mutation"
