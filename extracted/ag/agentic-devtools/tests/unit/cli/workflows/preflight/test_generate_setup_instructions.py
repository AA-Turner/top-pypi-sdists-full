"""Tests for GenerateSetupInstructions."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.git.worktree_paths import WorktreePathResolution
from agentic_devtools.cli.workflows.preflight import (
    PreflightResult,
    generate_setup_instructions,
)


class TestGenerateSetupInstructions:
    """Tests for generate_setup_instructions function."""

    def test_includes_failure_reasons(self):
        """Test that failure reasons are included."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=False,
            folder_name="wrong-folder",
            branch_name="main",
            issue_key="PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "PROJECT-1850" in instructions
        assert "Issues Detected" in instructions

    def test_includes_worktree_command_when_folder_wrong(self):
        """Test that worktree command is included when folder is wrong."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "git worktree add" in instructions
        assert "PROJECT-1850" in instructions

    def test_includes_branch_command_when_only_branch_wrong(self):
        """Test that branch command is included when only branch is wrong."""
        result = PreflightResult(
            folder_valid=True,
            branch_valid=False,
            folder_name="PROJECT-1850",
            branch_name="main",
            issue_key="PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "git switch -c" in instructions
        assert "feature/PROJECT-1850" in instructions

    def test_uses_current_worktree_path_when_only_branch_wrong(self):
        """Branch-only setup keeps the current worktree path for the VS Code command."""
        result = PreflightResult(
            folder_valid=True,
            branch_valid=False,
            folder_name="PROJECT-1850",
            branch_name="main",
            issue_key="PROJECT-1850",
            repo_root="/repos/wt/PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "code /repos/wt/PROJECT-1850/agdt-platform-management.code-workspace" in instructions

    def test_includes_vscode_command(self):
        """Test that VS Code open command is included."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=False,
            folder_name="wrong",
            branch_name="main",
            issue_key="PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "code .." in instructions
        assert "agdt-platform-management.code-workspace" in instructions

    def test_both_valid_skips_worktree_and_branch(self):
        """When both folder and branch are valid, no setup commands are shown."""
        result = PreflightResult(
            folder_valid=True,
            branch_valid=True,
            folder_name="PROJECT-1850",
            branch_name="feature/PROJECT-1850/implementation",
            issue_key="PROJECT-1850",
        )

        instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "git worktree add" not in instructions
        assert "git switch -c" not in instructions
        assert "Open in VS Code" in instructions

    @pytest.mark.parametrize(
        ("worktree_path", "worktree_folder"),
        [
            ("/repos/wt/PROJECT-1850", "wt"),
            ("/repos/custom/PROJECT-1850", "custom"),
            ("/repos/PROJECT-1850", None),
        ],
    )
    def test_uses_resolved_worktree_path_for_commands(self, worktree_path, worktree_folder):
        """Setup commands use the resolver path for default, custom, and legacy layouts."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
            repo_root="/repos/agentic-devtools",
        )
        with patch(
            "agentic_devtools.cli.workflows.preflight.resolve_worktree_path",
            return_value=WorktreePathResolution(
                repos_parent="/repos",
                worktree_path=worktree_path,
                normalized_issue_key="PROJECT-1850",
                worktree_folder=worktree_folder,
                configured_parent_dir="/repos/wt" if worktree_folder else None,
            ),
        ):
            instructions = generate_setup_instructions("PROJECT-1850", result)

        assert f"git worktree add {worktree_path}" in instructions
        assert f"code {worktree_path}/agdt-platform-management.code-workspace" in instructions

    def test_resolves_invalid_folder_from_main_checkout(self):
        """Invalid-folder setup resolves a new worktree from the main checkout."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
            repo_root="/repos/wt/current",
        )
        with (
            patch(
                "agentic_devtools.cli.workflows.preflight.get_git_main_repo_root",
                return_value="/repos/agentic-devtools",
            ),
            patch(
                "agentic_devtools.cli.workflows.preflight.resolve_worktree_path",
                return_value=WorktreePathResolution(
                    repos_parent="/repos",
                    worktree_path="/repos/wt/PROJECT-1850",
                    normalized_issue_key="PROJECT-1850",
                    worktree_folder="wt",
                    configured_parent_dir="/repos/wt",
                ),
            ) as resolve_path,
        ):
            instructions = generate_setup_instructions("PROJECT-1850", result)

        resolve_path.assert_called_once_with("/repos/agentic-devtools", "PROJECT-1850")
        assert "git worktree add /repos/wt/PROJECT-1850" in instructions

    def test_falls_back_to_relative_path_when_main_checkout_is_unavailable(self):
        """Invalid-folder setup keeps the legacy path if the main checkout is unavailable."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
            repo_root="/repos/wt/current",
        )
        with patch(
            "agentic_devtools.cli.workflows.preflight.get_git_main_repo_root",
            return_value=None,
        ):
            instructions = generate_setup_instructions("PROJECT-1850", result)

        assert "git worktree add ../PROJECT-1850" in instructions

    def test_quotes_paths_with_spaces_for_both_commands(self):
        """Setup commands quote resolved paths containing spaces."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
            repo_root="/repos/agentic-devtools",
        )
        worktree_path = "/repos/team wt/PROJECT-1850"
        with patch(
            "agentic_devtools.cli.workflows.preflight.resolve_worktree_path",
            return_value=WorktreePathResolution(
                repos_parent="/repos",
                worktree_path=worktree_path,
                normalized_issue_key="PROJECT-1850",
                worktree_folder="team wt",
                configured_parent_dir="/repos/team wt",
            ),
        ):
            instructions = generate_setup_instructions("PROJECT-1850", result)

        assert f"git worktree add '{worktree_path}'" in instructions
        assert f"code '{worktree_path}/agdt-platform-management.code-workspace'" in instructions

    def test_quotes_windows_paths_with_apostrophes_for_both_commands(self):
        """Windows setup commands use PowerShell quoting for configurable paths."""
        result = PreflightResult(
            folder_valid=False,
            branch_valid=True,
            folder_name="wrong-folder",
            branch_name="feature/PROJECT-1850/test",
            issue_key="PROJECT-1850",
            repo_root=r"C:\repos\agentic-devtools",
        )
        worktree_path = r"C:\repos\team's wt\PROJECT-1850"
        with (
            patch(
                "agentic_devtools.cli.workflows.preflight.resolve_worktree_path",
                return_value=WorktreePathResolution(
                    repos_parent=r"C:\repos",
                    worktree_path=worktree_path,
                    normalized_issue_key="PROJECT-1850",
                    worktree_folder="team's wt",
                    configured_parent_dir=r"C:\repos\team's wt",
                ),
            ),
            patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"),
        ):
            instructions = generate_setup_instructions("PROJECT-1850", result)

        quoted_path = "'C:\\repos\\team''s wt\\PROJECT-1850'"
        quoted_workspace = "'C:\\repos\\team''s wt\\PROJECT-1850/agdt-platform-management.code-workspace'"
        assert f"git worktree add {quoted_path}" in instructions
        assert f"code {quoted_workspace}" in instructions
