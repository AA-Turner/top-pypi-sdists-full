"""Import self-test for sage.core module.

This test ensures that all public exports from sage.core are importable.
If this test fails, the sage module is broken.
"""

from __future__ import annotations

import pytest


class TestCoreImports:
    """Test that all core module imports work."""

    def test_core_module_importable(self):
        """Test that sage.core is importable."""
        import sage.core

        assert sage.core is not None

    def test_error_classes_importable(self):
        """Test that error classes are importable."""
        from sage.core.errors import (
            ErrorHandler,
            SageError,
            SageException,
        )

        assert SageException is not None
        assert SageError is not None
        assert ErrorHandler is not None

    def test_sage_exception_is_exception(self):
        """Test that SageException is a proper Exception subclass."""
        from sage.core.errors import SageException

        assert issubclass(SageException, Exception)

        # Test it can be raised and caught
        with pytest.raises(SageException):
            raise SageException("test error")

    def test_discovery_importable(self):
        """Test that discovery module is importable."""
        from sage.core.discovery import (
            FileDiscovery,
            discover_files,
        )

        assert FileDiscovery is not None
        assert discover_files is not None

    def test_task_priority_importable(self):
        """Test that task priority module is importable."""
        from sage.core.task_priority import TaskPrioritizer

        assert TaskPrioritizer is not None

    def test_shell_importable(self):
        """Test that shell module is importable."""
        from sage.core.shell import (
            safe_shell_exec,
        )

        assert safe_shell_exec is not None

    def test_request_classifier_importable(self):
        """Test that request classifier module is importable."""
        from sage.core.request_classifier import (
            RequestClassifier,
            RequestType,
        )

        assert RequestClassifier is not None
        assert RequestType is not None

    def test_context_persistence_importable(self):
        """Test that context persistence module is importable."""
        from sage.core.context_persistence import (
            ContextPersistenceManager,
        )

        assert ContextPersistenceManager is not None

    def test_grounded_search_importable(self):
        """Test that grounded search module is importable."""
        from sage.core.grounded_search import (
            GroundedSearch,
        )

        assert GroundedSearch is not None

    def test_tool_validation_importable(self):
        """Test that tool validation module is importable."""
        from sage.core.tool_validation import (
            ToolExecutor,
            ToolType,
        )

        assert ToolExecutor is not None
        assert ToolType is not None

    def test_response_generator_importable(self):
        """Test that response generator module is importable."""
        from sage.core.response_generator import (
            ResponseQualityValidator,
        )

        assert ResponseQualityValidator is not None

    def test_agent_behavior_importable(self):
        """Test that agent behavior module is importable."""
        from sage.core.agent_behavior import (
            AgentBehaviorController,
        )

        assert AgentBehaviorController is not None


class TestDevOpsImports:
    """Test that devops module imports work."""

    def test_devops_module_importable(self):
        """Test that sage.devops is importable."""
        import sage.devops

        assert sage.devops is not None

    def test_devops_exports(self):
        """Test that devops exports are available."""
        from sage.devops import CICDMonitor, GitHubOps, GitOps

        assert CICDMonitor is not None
        assert GitHubOps is not None
        assert GitOps is not None

    def test_git_ops_instantiable(self):
        """Test that GitOps can be instantiated."""
        from pathlib import Path

        from sage.devops import GitOps

        # Should work with any path (will fail validation if not git repo)
        try:
            ops = GitOps(Path.cwd())
            assert ops is not None
        except ValueError:
            # Expected if not in a git repo
            pass


class TestCommandsImports:
    """Test that commands module imports work."""

    def test_commands_importable(self):
        """Test that sage.core.commands is importable."""
        from sage.core.commands import (
            execute_argv,
            execute_command,
            parse_command,
            validate_command,
        )

        assert execute_command is not None
        assert execute_argv is not None
        assert parse_command is not None
        assert validate_command is not None

    def test_parse_command_basic(self):
        """Test basic command parsing."""
        from sage.core.commands import parse_command

        parsed = parse_command("ls -la")
        assert parsed.is_valid
        assert parsed.executable == "ls"
        assert parsed.args == ["-la"]

    def test_validate_blocks_dangerous(self):
        """Test that dangerous commands are blocked."""
        from sage.core.commands import validate_command

        # Should block sudo
        result = validate_command("sudo rm -rf /")
        assert not result.allowed

        # Should block rm -rf /
        result = validate_command("rm -rf /")
        assert not result.allowed


class TestPublicAPI:
    """Test that the public API is stable."""

    def test_core_exports_exist(self):
        """Test that expected exports exist in sage.core."""
        import sage.core

        # Check key exports
        expected_exports = [
            "FileDiscovery",
            "TaskPrioritizer",
            "safe_shell_exec",
        ]

        for export in expected_exports:
            assert hasattr(sage.core, export), f"Missing export: {export}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
