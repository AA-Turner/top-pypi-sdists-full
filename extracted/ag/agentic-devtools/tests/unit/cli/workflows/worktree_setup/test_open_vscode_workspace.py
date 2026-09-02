"""Tests for OpenVscodeWorkspace."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.worktree_setup import (
    open_vscode_workspace,
)

_MODULE = "agentic_devtools.cli.workflows.worktree_setup"


class TestOpenVscodeWorkspace:
    """Tests for open_vscode_workspace function."""

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.subprocess.CREATE_NEW_PROCESS_GROUP", 0x200, create=True)
    @patch(f"{_MODULE}.subprocess.DETACHED_PROCESS", 0x8, create=True)
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value="/repos/PROJECT-1234/my-project.code-workspace")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_opens_vscode_on_windows(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """Test opening VS Code on Windows uses shell=True and creationflags."""
        mock_platform.return_value = "Windows"
        mock_popen.return_value = MagicMock()

        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is True
        mock_popen.assert_called_once()
        call_kwargs = mock_popen.call_args[1]
        assert call_kwargs["shell"] is True
        assert call_kwargs["creationflags"] == 0x8 | 0x200

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value="/repos/PROJECT-1234/my-project.code-workspace")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_opens_vscode_on_linux(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """Test opening VS Code on Linux."""
        mock_platform.return_value = "Linux"
        mock_popen.return_value = MagicMock()

        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is True
        mock_popen.assert_called_once()

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value="/repos/PROJECT-1234/my-project.code-workspace")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_opens_vscode_on_darwin(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """Test opening VS Code on macOS."""
        mock_platform.return_value = "Darwin"
        mock_popen.return_value = MagicMock()

        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is True
        mock_popen.assert_called_once()

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_opens_folder_when_workspace_not_found(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """Test that VS Code opens at the worktree root when no workspace file exists."""
        mock_platform.return_value = "Linux"
        mock_popen.return_value = MagicMock()

        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is True
        mock_popen.assert_called_once()
        call_args = mock_popen.call_args[0][0]
        assert "/repos/PROJECT-1234" in call_args

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value="/repos/PROJECT-1234/my-project.code-workspace")
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_handles_popen_exception(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """Test handling Popen exception."""
        mock_platform.return_value = "Windows"
        mock_popen.side_effect = OSError("code not found")

        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is False

    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    @patch(f"{_MODULE}.is_vscode_available", return_value=False)
    def test_returns_false_when_vscode_not_available(self, mock_available, mock_in_test, capsys):
        """Test that False is returned gracefully when VS Code is not on PATH."""
        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is False
        captured = capsys.readouterr()
        assert "VS Code not found on PATH" in captured.err

    def test_skips_launch_in_pytest_environment(self, capsys):
        """Test that launch is skipped when _in_test_environment returns True.

        During pytest runs, _in_test_environment() returns True by default,
        so no additional mocking is needed.
        """
        result = open_vscode_workspace("/repos/PROJECT-1234")

        assert result is False
        captured = capsys.readouterr()
        assert "Detected test environment (PYTEST_CURRENT_TEST)" in captured.out

    # ------------------------------------------------------------------
    # #2162: VS Code must not inherit the leaked main-repo state-dir env
    # ------------------------------------------------------------------

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_pins_worktree_state_dir_in_vscode_env(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """VS Code env pins AGENTIC_DEVTOOLS_STATE_DIR to the worktree scope (#2162).

        Prevents the integrated-terminal agdt-* commands from resolving to the
        inherited main-repo scope (which lacks the workflow state) and triggering
        a duplicate-session re-initiation.
        """
        mock_platform.return_value = "Linux"
        mock_popen.return_value = MagicMock()
        scope_dir = Path("/wt/.agdt/workflows/ama/DFLY-2998")
        mock_resolve.return_value = (scope_dir / "state.json", "")

        with patch.dict(
            os.environ,
            {"AGENTIC_DEVTOOLS_STATE_DIR": "/main-repo/.agdt/workflows/ama/DFLY-2998"},
            clear=False,
        ):
            result = open_vscode_workspace("/wt")

        assert result is True
        env = mock_popen.call_args[1]["env"]
        assert env["AGENTIC_DEVTOOLS_STATE_DIR"] == str(scope_dir)
        mock_resolve.assert_called_once_with("/wt")

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_strips_state_dir_env_when_resolution_fails(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """When worktree state cannot be resolved, the leaked state-dir env var is stripped."""
        mock_platform.return_value = "Linux"
        mock_popen.return_value = MagicMock()

        with patch.dict(
            os.environ,
            {"AGENTIC_DEVTOOLS_STATE_DIR": "/main-repo/.agdt/workflows/ama/DFLY-2998"},
            clear=False,
        ):
            result = open_vscode_workspace("/wt")

        assert result is True
        env = mock_popen.call_args[1]["env"]
        assert "AGENTIC_DEVTOOLS_STATE_DIR" not in env

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.subprocess.CREATE_NEW_PROCESS_GROUP", 0x200, create=True)
    @patch(f"{_MODULE}.subprocess.DETACHED_PROCESS", 0x8, create=True)
    @patch(f"{_MODULE}.platform.system", return_value="Windows")
    @patch(f"{_MODULE}.find_workspace_file", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree", return_value=(None, ""))
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_refuses_windows_metachar_paths(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available, capsys
    ):
        """Reject paths with cmd.exe metacharacters on Windows to prevent injection."""
        result = open_vscode_workspace("/repos/PROJECT&1234")

        assert result is False
        mock_popen.assert_not_called()
        captured = capsys.readouterr()
        assert "cmd.exe metacharacters" in captured.err

    @patch(f"{_MODULE}.is_vscode_available", return_value=True)
    @patch(f"{_MODULE}.subprocess.Popen")
    @patch(f"{_MODULE}.platform.system")
    @patch(f"{_MODULE}.find_workspace_file", return_value=None)
    @patch(f"{_MODULE}._resolve_state_context_in_worktree")
    @patch(f"{_MODULE}._in_test_environment", return_value=False)
    def test_always_strips_legacy_helpers_env(
        self, mock_in_test, mock_resolve, mock_find, mock_platform, mock_popen, mock_available
    ):
        """The legacy AGDT_AI_HELPERS_STATE_DIR is always removed from the VS Code env."""
        mock_platform.return_value = "Linux"
        mock_popen.return_value = MagicMock()
        mock_resolve.return_value = (Path("/wt/.agdt/workflows/ama/DFLY-2998/state.json"), "")

        with patch.dict(
            os.environ,
            {"AGDT_AI_HELPERS_STATE_DIR": "/main-repo/legacy"},
            clear=False,
        ):
            result = open_vscode_workspace("/wt")

        assert result is True
        env = mock_popen.call_args[1]["env"]
        assert "AGDT_AI_HELPERS_STATE_DIR" not in env
