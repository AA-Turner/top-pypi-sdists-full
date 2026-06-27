"""Unit tests for the airbyte_ops_mcp module."""

import pytest

import airbyte_ops_mcp


class TestAirbyteAdminMcp:
    """Test cases for the main module."""

    @pytest.mark.unit
    def test_hello(self):
        """Test the hello function."""
        result = airbyte_ops_mcp.hello()
        assert result == "Hello from airbyte-internal-ops!"
        assert isinstance(result, str)

    @pytest.mark.unit
    def test_version_attribute(self):
        """Test that __version__ is derived from package metadata."""
        assert hasattr(airbyte_ops_mcp, "__version__")
        assert isinstance(airbyte_ops_mcp.__version__, str)
        assert airbyte_ops_mcp.__version__ != ""

    @pytest.mark.unit
    def test_all_exports(self):
        """Test that __all__ contains expected exports."""
        expected_exports = ["hello", "__version__"]
        assert hasattr(airbyte_ops_mcp, "__all__")
        assert all(item in airbyte_ops_mcp.__all__ for item in expected_exports)
