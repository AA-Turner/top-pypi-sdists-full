"""Tests for script_generators constants."""

from agentic_devtools.cli.setup.script_generators.constants import (
    COMPLETE_SETUP_FILENAME,
    CONFIGURED_SETUP_FILENAME,
    ORCHESTRATOR_MARKER,
    REPO_SPECIFIC_FILENAME,
    REQUIRED_SETUP_FILENAME,
    ROOT_ENTRY_POINT_FILENAME,
    TOOL_REGISTRY,
)


class TestConstants:
    """Tests for script_generators constants module."""

    def test_orchestrator_marker_is_string(self):
        """ORCHESTRATOR_MARKER is a non-empty string."""
        assert isinstance(ORCHESTRATOR_MARKER, str)
        assert len(ORCHESTRATOR_MARKER) > 0

    def test_filenames_end_with_py(self):
        """All filename constants end with .py."""
        assert REQUIRED_SETUP_FILENAME.endswith(".py")
        assert CONFIGURED_SETUP_FILENAME.endswith(".py")
        assert COMPLETE_SETUP_FILENAME.endswith(".py")
        assert ROOT_ENTRY_POINT_FILENAME.endswith(".py")
        assert REPO_SPECIFIC_FILENAME.endswith(".py")

    def test_tool_registry_is_dict(self):
        """TOOL_REGISTRY is a non-empty dict with expected structure."""
        assert isinstance(TOOL_REGISTRY, dict)
        assert len(TOOL_REGISTRY) > 0
        for name, entry in TOOL_REGISTRY.items():
            assert "install_argv" in entry
            assert "check_cmd" in entry
            assert "description" in entry
