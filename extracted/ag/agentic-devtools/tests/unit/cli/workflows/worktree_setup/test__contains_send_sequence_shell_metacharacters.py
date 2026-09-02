"""Tests for _contains_send_sequence_shell_metacharacters."""

import pytest

from agentic_devtools.cli.workflows.worktree_setup import (
    _contains_send_sequence_shell_metacharacters,
)


class TestContainsSendSequenceShellMetacharacters:
    """Tests for the _contains_send_sequence_shell_metacharacters helper."""

    @pytest.mark.parametrize(
        "value",
        [
            # cmd.exe metacharacters (superset of _contains_windows_cmd_metacharacters)
            "/repos/project&name",
            "/repos/project|name",
            "/repos/project<name",
            "/repos/project>name",
            "/repos/project^name",
            "/repos/project%name",
            "/repos/project!name",
            "/repos/project\nname",
            "/repos/project\rname",
            "/repos/project;name",
            '/repos/project"name',
            "/repos/project'name",
            # PowerShell / bash injection characters
            "/repos/project$name",
            "$(Start-Process calc)",
            "`whoami`",
            "!PAYLOAD!",
            # marker-derived fallback values
            "run-$(date +%s)-id",
        ],
    )
    def test_returns_true_for_dangerous_values(self, value):
        """Returns True when value contains any dangerous shell metacharacter."""
        assert _contains_send_sequence_shell_metacharacters(value) is True

    @pytest.mark.parametrize(
        "value",
        [
            "/repos/normal-project/workspace",
            "abc123",
            "my-run-id",
            "Start a new session",
            "",
        ],
    )
    def test_returns_false_for_safe_values(self, value):
        """Returns False when value contains no dangerous shell metacharacters."""
        assert _contains_send_sequence_shell_metacharacters(value) is False
