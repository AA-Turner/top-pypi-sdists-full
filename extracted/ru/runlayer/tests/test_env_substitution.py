"""Tests for environment variable substitution."""

import os
import tempfile
from pathlib import Path
import pytest

from runlayer_cli.env_substitution import load_env_vars, substitute_env_vars


def test_load_env_vars_from_os_environ():
    """Test loading environment variables from os.environ."""
    # Set a test variable
    os.environ["TEST_VAR"] = "test_value"
    try:
        env_vars = load_env_vars()
        assert "TEST_VAR" in env_vars
        assert env_vars["TEST_VAR"] == "test_value"
    finally:
        # Clean up
        del os.environ["TEST_VAR"]


def test_load_env_vars_from_file():
    """Test loading environment variables from .env file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("ENV_FILE_VAR=env_file_value\n")
        f.write("ANOTHER_VAR=another_value\n")
        env_file_path = f.name

    try:
        env_vars = load_env_vars(env_file_path)
        assert env_vars["ENV_FILE_VAR"] == "env_file_value"
        assert env_vars["ANOTHER_VAR"] == "another_value"
    finally:
        Path(env_file_path).unlink()


def test_load_env_vars_file_overrides_os_environ():
    """Test that .env file values override os.environ."""
    os.environ["OVERRIDE_VAR"] = "os_value"
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("OVERRIDE_VAR=file_value\n")
            env_file_path = f.name

        try:
            env_vars = load_env_vars(env_file_path)
            assert env_vars["OVERRIDE_VAR"] == "file_value"
        finally:
            Path(env_file_path).unlink()
    finally:
        del os.environ["OVERRIDE_VAR"]


def test_load_env_vars_file_not_found():
    """Test that missing .env file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError) as exc_info:
        load_env_vars("nonexistent.env")
    assert "not found" in str(exc_info.value).lower()


def test_load_env_vars_auto_discover():
    """Test automatic discovery of .env file in search directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file_path = Path(tmpdir) / ".env"
        env_file_path.write_text("AUTO_VAR=auto_value\n")

        # Search in tmpdir
        env_vars = load_env_vars(search_dir=Path(tmpdir))

        assert env_vars["AUTO_VAR"] == "auto_value"


def test_load_env_vars_auto_discover_current_dir():
    """Test automatic discovery of .env file in current directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            # Change to tmpdir
            import os

            os.chdir(tmpdir)
            env_file_path = Path(".env")
            env_file_path.write_text("CURRENT_DIR_VAR=current_value\n")

            # Auto-discover without explicit path or search_dir
            env_vars = load_env_vars()

            assert env_vars["CURRENT_DIR_VAR"] == "current_value"
        finally:
            os.chdir(original_cwd)


def test_load_env_vars_explicit_overrides_auto_discover():
    """Test that explicit env_file_path overrides auto-discovery."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .env in search dir
        search_env = Path(tmpdir) / ".env"
        search_env.write_text("SEARCH_VAR=search_value\n")

        # Create explicit .env file
        explicit_env = Path(tmpdir) / "explicit.env"
        explicit_env.write_text("EXPLICIT_VAR=explicit_value\n")

        # Explicit file should be used, not auto-discovered one
        env_vars = load_env_vars(
            env_file_path=str(explicit_env), search_dir=Path(tmpdir)
        )

        assert env_vars["EXPLICIT_VAR"] == "explicit_value"
        # Search dir .env should not be loaded when explicit path is provided
        assert (
            "SEARCH_VAR" not in env_vars or env_vars.get("SEARCH_VAR") != "search_value"
        )


def test_substitute_env_vars_basic():
    """Test basic ${VAR} substitution."""
    yaml_content = "api_key: ${API_KEY}\nurl: ${BASE_URL}"
    env_vars = {"API_KEY": "secret123", "BASE_URL": "https://api.example.com"}

    result = substitute_env_vars(yaml_content, env_vars)

    assert "api_key: secret123" in result
    assert "url: https://api.example.com" in result
    assert "${API_KEY}" not in result
    assert "${BASE_URL}" not in result


def test_substitute_env_vars_with_default():
    """Test ${VAR:-default} syntax."""
    yaml_content = "log_level: ${LOG_LEVEL:-info}\nport: ${PORT:-8080}"
    env_vars = {}  # Variables not set

    result = substitute_env_vars(yaml_content, env_vars)

    assert "log_level: info" in result
    assert "port: 8080" in result


def test_substitute_env_vars_with_default_override():
    """Test ${VAR:-default} uses actual value when set."""
    yaml_content = "log_level: ${LOG_LEVEL:-info}"
    env_vars = {"LOG_LEVEL": "debug"}

    result = substitute_env_vars(yaml_content, env_vars)

    assert "log_level: debug" in result
    assert "info" not in result


def test_substitute_env_vars_with_default_empty_string():
    """Test ${VAR:-default} uses default when value is empty string."""
    yaml_content = "log_level: ${LOG_LEVEL:-info}"
    env_vars = {"LOG_LEVEL": ""}  # Empty string

    result = substitute_env_vars(yaml_content, env_vars)

    assert "log_level: info" in result  # Uses default because empty


def test_substitute_env_vars_with_default_dash_only():
    """Test ${VAR-default} only uses default if unset (not if empty)."""
    yaml_content = "log_level: ${LOG_LEVEL-info}"
    env_vars = {}  # Variable not set

    result = substitute_env_vars(yaml_content, env_vars)

    assert "log_level: info" in result


def test_substitute_env_vars_with_default_dash_empty_string():
    """Test ${VAR-default} keeps empty string (doesn't use default)."""
    yaml_content = "log_level: ${LOG_LEVEL-info}"
    env_vars = {"LOG_LEVEL": ""}  # Empty string

    result = substitute_env_vars(yaml_content, env_vars)

    assert "log_level: " in result  # Keeps empty string
    assert "info" not in result


def test_substitute_env_vars_missing_required():
    """Test that missing required variable raises ValueError."""
    yaml_content = "api_key: ${REQUIRED_VAR}"
    env_vars = {}

    with pytest.raises(ValueError) as exc_info:
        substitute_env_vars(yaml_content, env_vars)
    assert "REQUIRED_VAR" in str(exc_info.value)
    assert "not set" in str(exc_info.value).lower()


def test_substitute_env_vars_preserve_double_dollar():
    """Test that $$VAR sequences are preserved (not substituted)."""
    yaml_content = "webhook_url: $$DEPLOYMENT_URL/webhook"
    env_vars = {"DEPLOYMENT_URL": "should_not_be_used"}

    result = substitute_env_vars(yaml_content, env_vars)

    # Double dollar sign should be preserved
    assert "$$DEPLOYMENT_URL" in result
    assert "should_not_be_used" not in result


def test_substitute_env_vars_multiple_occurrences():
    """Test that same variable can be used multiple times."""
    yaml_content = "api_url: ${BASE_URL}/api\nwebhook_url: ${BASE_URL}/webhook"
    env_vars = {"BASE_URL": "https://example.com"}

    result = substitute_env_vars(yaml_content, env_vars)

    assert "api_url: https://example.com/api" in result
    assert "webhook_url: https://example.com/webhook" in result


def test_substitute_env_vars_complex_yaml():
    """Test substitution in complex YAML structure."""
    yaml_content = """name: my-service
env:
  API_KEY: ${API_KEY}
  DATABASE_URL: ${DATABASE_URL}
  LOG_LEVEL: ${LOG_LEVEL:-info}
  DEBUG: ${DEBUG:-false}
build:
  context: ${BUILD_CONTEXT:-.}
"""
    env_vars = {
        "API_KEY": "secret123",
        "DATABASE_URL": "postgres://localhost/db",
        "DEBUG": "true",
    }

    result = substitute_env_vars(yaml_content, env_vars)

    assert "API_KEY: secret123" in result
    assert "DATABASE_URL: postgres://localhost/db" in result
    assert "LOG_LEVEL: info" in result  # Uses default
    assert "DEBUG: true" in result
    assert "BUILD_CONTEXT:-." in result or "context: ." in result  # Uses default


def test_substitute_env_vars_mixed_syntax():
    """Test mixing required and default variables."""
    yaml_content = """
required: ${REQUIRED_VAR}
with_default: ${OPTIONAL_VAR:-default_value}
with_dash_default: ${ANOTHER_VAR-another_default}
"""
    env_vars = {
        "REQUIRED_VAR": "required_value",
        "OPTIONAL_VAR": "provided_value",
    }

    result = substitute_env_vars(yaml_content, env_vars)

    assert "required: required_value" in result
    assert "with_default: provided_value" in result
    assert "with_dash_default: another_default" in result  # Uses default


def test_load_env_vars_with_utf8_bom():
    """Test that UTF-8 BOM is stripped from .env files (PowerShell default)."""
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".env", delete=False) as f:
        f.write(b"\xef\xbb\xbfFIRST_VAR=first_value\nSECOND_VAR=second_value\n")
        env_file_path = f.name

    try:
        env_vars = load_env_vars(env_file_path)
        assert env_vars["FIRST_VAR"] == "first_value"
        assert env_vars["SECOND_VAR"] == "second_value"
    finally:
        Path(env_file_path).unlink()


def test_substitute_env_vars_no_substitution_needed():
    """Test YAML with no variable references."""
    yaml_content = "name: my-service\nversion: 1.0.0"
    env_vars = {}

    result = substitute_env_vars(yaml_content, env_vars)

    assert result == yaml_content


def test_substitute_env_vars_empty_yaml():
    """Test empty YAML content."""
    yaml_content = ""
    env_vars = {}

    result = substitute_env_vars(yaml_content, env_vars)

    assert result == ""
