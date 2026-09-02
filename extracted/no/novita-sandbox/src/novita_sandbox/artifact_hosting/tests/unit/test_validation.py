"""Unit tests for validation utilities."""

import pytest

from novita_sandbox.artifact_hosting.utils.validation import (
    validate_environment_variables,
    validate_project_name,
)


class TestEnvironmentVariableValidation:
    """Tests for environment variable validation."""
    
    def test_valid_environment_variables(self):
        """Test that valid environment variable keys pass validation."""
        env_vars = {
            "API_KEY": "value1",
            "NODE_ENV": "production",
            "_PRIVATE_KEY": "secret",
            "VAR123": "value",
        }
        # Should not raise
        validate_environment_variables(env_vars)
    
    def test_empty_environment_variables(self):
        """Test that empty dict passes validation."""
        validate_environment_variables({})
    
    def test_empty_key_raises_error(self):
        """Test that empty key raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_environment_variables({"": "value"})
    
    def test_key_starting_with_number_raises_error(self):
        """Test that key starting with number raises ValueError."""
        with pytest.raises(ValueError, match="Invalid environment variable key"):
            validate_environment_variables({"123_INVALID": "value"})
    
    def test_key_with_hyphen_raises_error(self):
        """Test that key with hyphen raises ValueError."""
        with pytest.raises(ValueError, match="Invalid environment variable key"):
            validate_environment_variables({"KEY-WITH-HYPHEN": "value"})
    
    def test_key_with_space_raises_error(self):
        """Test that key with space raises ValueError."""
        with pytest.raises(ValueError, match="Invalid environment variable key"):
            validate_environment_variables({"KEY WITH SPACE": "value"})
    
    def test_value_not_validated(self):
        """Test that values are not validated (can be any string)."""
        # Should not raise, even with unusual values
        validate_environment_variables({
            "VALID_KEY": "",
            "ANOTHER_KEY": "value with spaces",
            "JSON_KEY": '{"nested": {"data": 123}}',
            "URL_KEY": "https://example.com/path?query=value",
        })


class TestProjectNameValidation:
    """Tests for project name validation."""
    
    def test_valid_project_names(self):
        """Test that valid project names pass validation."""
        valid_names = [
            "my-app",
            "project123",
            "a" * 3,  # Minimum length
            "a" * 63,  # Maximum length
            "my-project-name",
        ]
        for name in valid_names:
            validate_project_name(name)  # Should not raise
    
    def test_empty_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_project_name("")
    
    def test_too_short_name_raises_error(self):
        """Test that name shorter than 3 chars raises ValueError."""
        with pytest.raises(ValueError, match="between 3 and 63 characters"):
            validate_project_name("ab")
    
    def test_too_long_name_raises_error(self):
        """Test that name longer than 63 chars raises ValueError."""
        with pytest.raises(ValueError, match="between 3 and 63 characters"):
            validate_project_name("a" * 64)
    
    def test_name_starting_with_number_raises_error(self):
        """Test that name starting with number raises ValueError."""
        with pytest.raises(ValueError, match="must start with a lowercase letter"):
            validate_project_name("123project")
    
    def test_name_starting_with_uppercase_raises_error(self):
        """Test that name starting with uppercase raises ValueError."""
        with pytest.raises(ValueError, match="must start with a lowercase letter"):
            validate_project_name("Project")
    
    def test_name_with_underscore_raises_error(self):
        """Test that name with underscore raises ValueError."""
        with pytest.raises(ValueError, match="lowercase letters, numbers, and hyphens"):
            validate_project_name("my_project")
    
    def test_name_with_space_raises_error(self):
        """Test that name with space raises ValueError."""
        with pytest.raises(ValueError, match="lowercase letters, numbers, and hyphens"):
            validate_project_name("my project")
