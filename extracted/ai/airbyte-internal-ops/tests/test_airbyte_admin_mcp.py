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
    def test_get_version(self):
        """Test the get_version function."""
        version = airbyte_ops_mcp.get_version()
        assert version == "0.1.0"
        assert isinstance(version, str)

    @pytest.mark.unit
    def test_version_attribute(self):
        """Test the __version__ attribute."""
        assert hasattr(airbyte_ops_mcp, "__version__")
        assert airbyte_ops_mcp.__version__ == "0.1.0"

    @pytest.mark.unit
    def test_all_exports(self):
        """Test that __all__ contains expected exports."""
        expected_exports = ["hello", "get_version", "__version__"]
        assert hasattr(airbyte_ops_mcp, "__all__")
        assert all(item in airbyte_ops_mcp.__all__ for item in expected_exports)
