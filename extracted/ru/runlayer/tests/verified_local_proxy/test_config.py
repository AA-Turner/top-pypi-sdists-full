"""Tests for configuration module."""

import pytest

from runlayer_cli.verified_local_proxy.config import (
    VERIFICATION_CONFIGS,
    VerificationConfig,
    load_verification_config,
)
from runlayer_cli.verified_local_proxy.exceptions import ConfigurationError


class TestVerificationConfig:
    """Tests for VerificationConfig model."""

    def test_target_url_default_path(self):
        """Test target_url property with default path."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test Server",
            target_port=8000,
        )
        assert config.target_url == "http://127.0.0.1:8000/mcp"

    def test_target_url_custom_path(self):
        """Test target_url property with custom path."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test Server",
            target_port=3845,
            target_path="/sse",
        )
        assert config.target_url == "http://127.0.0.1:3845/sse"

    def test_target_url_custom_host(self):
        """Test target_url property with custom host."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test Server",
            target_host="localhost",
            target_port=8080,
            target_path="/api",
        )
        assert config.target_url == "http://localhost:8080/api"

    def test_optional_verification_fields(self):
        """Test that verification fields are optional."""
        config = VerificationConfig(
            server_id="test",
            display_name="Test Server",
            target_port=8000,
        )
        assert config.macos_authority is None
        assert config.expected_binary_paths == []

    def test_full_config(self):
        """Test config with all fields populated."""
        config = VerificationConfig(
            server_id="com.example/test",
            display_name="Example Test Server",
            target_host="127.0.0.1",
            target_port=9000,
            target_path="/mcp",
            macos_authority="Developer ID Application: Example Inc (ABC123)",
            expected_binary_paths=["/Applications/Example.app"],
        )
        assert config.server_id == "com.example/test"
        assert config.macos_authority == "Developer ID Application: Example Inc (ABC123)"


class TestLoadVerificationConfig:
    """Tests for load_verification_config function."""

    def test_load_figma_config(self):
        """Test loading the hardcoded Figma config."""
        config = load_verification_config("com.figma/desktop-mcp")
        assert config.server_id == "com.figma/desktop-mcp"
        assert config.display_name == "Figma Desktop MCP"
        assert config.target_port == 3845
        assert config.target_path == "/mcp"
        assert "T8RA8NE3B7" in config.macos_authority

    def test_load_unknown_config(self):
        """Test that loading unknown config raises error."""
        with pytest.raises(ConfigurationError) as exc_info:
            load_verification_config("com.unknown/nonexistent")

        assert "Unknown server_id" in str(exc_info.value)
        assert "com.unknown/nonexistent" in str(exc_info.value)

    def test_available_servers_in_error_message(self):
        """Test that error message lists available servers."""
        with pytest.raises(ConfigurationError) as exc_info:
            load_verification_config("invalid")

        error_msg = str(exc_info.value)
        for server_id in VERIFICATION_CONFIGS.keys():
            assert server_id in error_msg


class TestHardcodedConfigs:
    """Tests for hardcoded verification configs."""

    def test_figma_config_exists(self):
        """Test that Figma config is in hardcoded configs."""
        assert "com.figma/desktop-mcp" in VERIFICATION_CONFIGS

    def test_figma_config_has_required_fields(self):
        """Test that Figma config has all verification fields."""
        config = VERIFICATION_CONFIGS["com.figma/desktop-mcp"]

        # macOS verification
        assert config.macos_authority is not None
        assert "Figma" in config.macos_authority
        assert "T8RA8NE3B7" in config.macos_authority

        # Expected paths
        assert len(config.expected_binary_paths) > 0
        assert any(".app" in p for p in config.expected_binary_paths)
