"""
OneEnv Scaffolding API Test Suite

This module contains comprehensive tests for the new Scaffolding API functionality.
"""

import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from typing import Dict, List, Any

# Import the modules to test
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import oneenv
from oneenv.core import ScaffoldingTemplateProcessor, generate_env_file_content
from oneenv.models import EnvOption, EnvVarConfig, validate_scaffolding_format


class TestScaffoldingAPI:
    """Test suite for the main Scaffolding API functions."""
    
    def setup_method(self):
        """Setup method run before each test."""
        # Create a fresh processor for each test
        self.processor = ScaffoldingTemplateProcessor()
        
        # Mock data for testing
        self.mock_options = [
            EnvOption(
                category="Database",
                option="sqlite",
                env={
                    "DATABASE_URL": EnvVarConfig(
                        description="SQLite database URL",
                        default="sqlite:///app.db",
                        required=True,
                        importance="critical"
                    )
                }
            ),
            EnvOption(
                category="Database", 
                option="postgres",
                env={
                    "DATABASE_URL": EnvVarConfig(
                        description="PostgreSQL connection URL",
                        default="postgresql://user:pass@localhost:5432/dbname",
                        required=True,
                        importance="critical"
                    ),
                    "DATABASE_POOL_SIZE": EnvVarConfig(
                        description="Connection pool size",
                        default="10",
                        required=False,
                        importance="optional"
                    )
                }
            ),
            EnvOption(
                category="VectorStore",
                option="chroma",
                env={
                    "CHROMA_HOST": EnvVarConfig(
                        description="Chroma host",
                        default="localhost",
                        required=True,
                        importance="important"
                    ),
                    "CHROMA_PORT": EnvVarConfig(
                        description="Chroma port",
                        default="8000",
                        required=False,
                        importance="optional"
                    )
                }
            )
        ]
    
    def test_get_all_template_structure_empty(self):
        """Test get_all_template_structure with no templates."""
        structure = oneenv.get_all_template_structure()
        assert isinstance(structure, dict)
        assert structure == {}
    
    @patch('oneenv.core._scaffolding_processor')
    def test_get_all_template_structure_with_data(self, mock_processor):
        """Test get_all_template_structure with mock data."""
        mock_processor.load_all_scaffolding_templates.return_value = None
        mock_processor.get_template_structure.return_value = {
            "Database": ["sqlite", "postgres"],
            "VectorStore": ["chroma"]
        }
        
        structure = oneenv.get_all_template_structure()
        
        assert structure == {
            "Database": ["sqlite", "postgres"],
            "VectorStore": ["chroma"]
        }
        mock_processor.load_all_scaffolding_templates.assert_called_once()
        mock_processor.get_template_structure.assert_called_once()
    
    def test_has_category_with_invalid_args(self):
        """Test has_category with invalid arguments."""
        # Test with non-string argument
        with pytest.raises(TypeError, match="Category must be string"):
            oneenv.has_category(123)
        
        # Test with empty string
        with pytest.raises(ValueError, match="Category cannot be empty"):
            oneenv.has_category("")
        
        # Test with whitespace-only string
        with pytest.raises(ValueError, match="Category cannot be empty"):
            oneenv.has_category("   ")
    
    @patch('oneenv.core._scaffolding_processor')
    def test_has_category_valid(self, mock_processor):
        """Test has_category with valid arguments."""
        mock_processor.load_all_scaffolding_templates.return_value = None
        mock_processor.has_category.return_value = True
        
        result = oneenv.has_category("Database")
        
        assert result is True
        mock_processor.load_all_scaffolding_templates.assert_called_once()
        mock_processor.has_category.assert_called_once_with("Database")
    
    def test_get_options_with_invalid_args(self):
        """Test get_options with invalid arguments."""
        # Test with non-string argument
        with pytest.raises(TypeError, match="Category must be string"):
            oneenv.get_options(123)
        
        # Test with empty string
        with pytest.raises(ValueError, match="Category cannot be empty"):
            oneenv.get_options("")
        
        # Test with non-existent category
        with pytest.raises(ValueError, match="Category 'NonExistent' not found"):
            oneenv.get_options("NonExistent")
    
    @patch('oneenv.core._scaffolding_processor')
    def test_get_options_valid(self, mock_processor):
        """Test get_options with valid arguments."""
        mock_processor.load_all_scaffolding_templates.return_value = None
        mock_processor.get_options.return_value = ["sqlite", "postgres"]
        
        result = oneenv.get_options("Database")
        
        assert result == ["sqlite", "postgres"]
        mock_processor.load_all_scaffolding_templates.assert_called_once()
        mock_processor.get_options.assert_called_once_with("Database")
    
    def test_generate_template_with_invalid_args(self):
        """Test generate_template with invalid arguments."""
        # Test with non-string dest
        with pytest.raises(TypeError, match="dest must be string"):
            oneenv.generate_template(123, [])
        
        # Test with non-list generation_range
        with pytest.raises(TypeError, match="generation_range must be list"):
            oneenv.generate_template("", "invalid")
        
        # Test with invalid generation_range item
        with pytest.raises(ValueError, match="must be dict.*Expected format"):
            oneenv.generate_template("", ["invalid"])
        
        # Test with missing category key
        with pytest.raises(ValueError, match="missing required key 'category'.*Expected format"):
            oneenv.generate_template("", [{"option": "test"}])
        
        # Test with empty category
        with pytest.raises(ValueError, match="must be non-empty string"):
            oneenv.generate_template("", [{"category": ""}])
        
        # Test with empty option
        with pytest.raises(ValueError, match="must be non-empty string if provided"):
            oneenv.generate_template("", [{"category": "Database", "option": ""}])
    
    @patch('oneenv.core._scaffolding_processor')
    def test_generate_template_valid(self, mock_processor):
        """Test generate_template with valid arguments."""
        mock_processor.load_all_scaffolding_templates.return_value = None
        mock_processor.generate_by_selection.return_value = {
            "DATABASE_URL": {
                "config": EnvVarConfig(
                    description="Test database URL",
                    default="test://localhost",
                    required=True
                ),
                "category": "Database",
                "option": "postgres"
            }
        }
        
        generation_range = [{"category": "Database", "option": "postgres"}]
        result = oneenv.generate_template("", generation_range)
        
        assert isinstance(result, str)
        assert "DATABASE_URL=test://localhost" in result
        assert "Test database URL" in result
        mock_processor.load_all_scaffolding_templates.assert_called_once()
        mock_processor.generate_by_selection.assert_called_once_with(generation_range)
    
    def test_generate_template_file_output(self):
        """Test generate_template with file output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Mock the processor to return empty data
            with patch('oneenv.core._scaffolding_processor') as mock_processor:
                mock_processor.load_all_scaffolding_templates.return_value = None
                mock_processor.generate_by_selection.return_value = {}
                
                result = oneenv.generate_template(tmp_path, [])
                
                # Check that file was created and has expected content
                assert os.path.exists(tmp_path)
                with open(tmp_path, 'r') as f:
                    content = f.read()
                    assert content == result
        
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_generate_template_file_permission_error(self):
        """Test generate_template with permission error."""
        invalid_path = "/root/invalid/path/test.env"
        
        with patch('oneenv.core._scaffolding_processor') as mock_processor:
            mock_processor.load_all_scaffolding_templates.return_value = None
            mock_processor.generate_by_selection.return_value = {}
            
            with pytest.raises(PermissionError, match="Cannot write to file"):
                oneenv.generate_template(invalid_path, [])


class TestScaffoldingTemplateProcessor:
    """Test suite for the ScaffoldingTemplateProcessor class."""
    
    def setup_method(self):
        """Setup method run before each test."""
        self.processor = ScaffoldingTemplateProcessor()
        
        # Create mock options
        self.mock_options = [
            EnvOption(
                category="Database",
                option="sqlite",
                env={
                    "DATABASE_URL": EnvVarConfig(
                        description="SQLite database URL",
                        default="sqlite:///app.db",
                        required=True,
                        importance="critical"
                    )
                }
            ),
            EnvOption(
                category="Database", 
                option="postgres",
                env={
                    "DATABASE_URL": EnvVarConfig(
                        description="PostgreSQL connection URL",
                        default="postgresql://user:pass@localhost:5432/dbname",
                        required=True,
                        importance="critical"
                    ),
                    "DATABASE_POOL_SIZE": EnvVarConfig(
                        description="Connection pool size",
                        default="10",
                        required=False,
                        importance="optional"
                    )
                }
            ),
            EnvOption(
                category="VectorStore",
                option="chroma",
                env={
                    "CHROMA_HOST": EnvVarConfig(
                        description="Chroma host",
                        default="localhost",
                        required=True,
                        importance="important"
                    )
                }
            )
        ]
    
    def test_get_template_structure(self):
        """Test get_template_structure method."""
        self.processor.env_options = self.mock_options
        
        structure = self.processor.get_template_structure()
        
        expected = {
            "Database": ["postgres", "sqlite"],
            "VectorStore": ["chroma"]
        }
        assert structure == expected
    
    def test_has_category(self):
        """Test has_category method."""
        self.processor.env_options = self.mock_options
        
        assert self.processor.has_category("Database") is True
        assert self.processor.has_category("VectorStore") is True
        assert self.processor.has_category("NonExistent") is False
    
    def test_get_options(self):
        """Test get_options method."""
        self.processor.env_options = self.mock_options
        
        db_options = self.processor.get_options("Database")
        vs_options = self.processor.get_options("VectorStore")
        empty_options = self.processor.get_options("NonExistent")
        
        assert set(db_options) == {"postgres", "sqlite"}
        assert vs_options == ["chroma"]
        assert empty_options == []
    
    def test_generate_by_selection_specific_option(self):
        """Test generate_by_selection with specific option."""
        self.processor.env_options = self.mock_options
        
        generation_range = [{"category": "Database", "option": "postgres"}]
        result = self.processor.generate_by_selection(generation_range)
        
        assert "DATABASE_URL" in result
        assert "DATABASE_POOL_SIZE" in result
        assert result["DATABASE_URL"]["option"] == "postgres"
        assert result["DATABASE_POOL_SIZE"]["option"] == "postgres"
    
    def test_generate_by_selection_all_options(self):
        """Test generate_by_selection with all options in category."""
        self.processor.env_options = self.mock_options
        
        generation_range = [{"category": "Database"}]  # No option = all options
        result = self.processor.generate_by_selection(generation_range)
        
        # Should have prefixed variable names for all options
        assert "POSTGRES_DATABASE_URL" in result
        assert "POSTGRES_DATABASE_POOL_SIZE" in result
        assert "SQLITE_DATABASE_URL" in result
        
        # Check that different options are represented
        postgres_vars = [k for k, v in result.items() if v["option"] == "postgres"]
        sqlite_vars = [k for k, v in result.items() if v["option"] == "sqlite"]
        
        assert len(postgres_vars) == 2  # DATABASE_URL and DATABASE_POOL_SIZE
        assert len(sqlite_vars) == 1   # DATABASE_URL only
    
    def test_generate_by_selection_multiple_categories(self):
        """Test generate_by_selection with multiple categories."""
        self.processor.env_options = self.mock_options
        
        generation_range = [
            {"category": "Database", "option": "sqlite"},
            {"category": "VectorStore", "option": "chroma"}
        ]
        result = self.processor.generate_by_selection(generation_range)
        
        assert "DATABASE_URL" in result
        assert "CHROMA_HOST" in result
        assert result["DATABASE_URL"]["option"] == "sqlite"
        assert result["CHROMA_HOST"]["option"] == "chroma"


class TestValidateScaffoldingFormat:
    """Test suite for scaffolding format validation."""
    
    def test_valid_scaffolding_format(self):
        """Test validation with valid scaffolding format."""
        valid_data = [
            {
                "category": "Database",
                "option": "sqlite",
                "env": {
                    "DATABASE_URL": {
                        "description": "SQLite database URL",
                        "default": "sqlite:///app.db",
                        "required": True
                    }
                }
            }
        ]
        
        # Should not raise any exception
        assert validate_scaffolding_format(valid_data) is True
    
    def test_invalid_scaffolding_format_not_list(self):
        """Test validation with non-list data."""
        invalid_data = {"not": "a list"}
        
        with pytest.raises(ValueError, match="Template must be a list of options"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_empty_list(self):
        """Test validation with empty list."""
        invalid_data = []
        
        with pytest.raises(ValueError, match="Template cannot be empty"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_missing_keys(self):
        """Test validation with missing required keys."""
        invalid_data = [
            {
                "category": "Database",
                # Missing "option" and "env"
            }
        ]
        
        with pytest.raises(ValueError, match="Missing required keys"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_empty_category(self):
        """Test validation with empty category."""
        invalid_data = [
            {
                "category": "",
                "option": "sqlite",
                "env": {
                    "DATABASE_URL": {
                        "description": "SQLite database URL"
                    }
                }
            }
        ]
        
        with pytest.raises(ValueError, match="category must be non-empty string"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_duplicate_category_option(self):
        """Test validation with duplicate category/option pairs."""
        invalid_data = [
            {
                "category": "Database",
                "option": "sqlite",
                "env": {
                    "DATABASE_URL": {
                        "description": "SQLite database URL"
                    }
                }
            },
            {
                "category": "Database",
                "option": "sqlite",  # Duplicate
                "env": {
                    "ANOTHER_VAR": {
                        "description": "Another variable"
                    }
                }
            }
        ]
        
        with pytest.raises(ValueError, match="Duplicate category/option pair"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_empty_env(self):
        """Test validation with empty env."""
        invalid_data = [
            {
                "category": "Database",
                "option": "sqlite",
                "env": {}  # Empty env
            }
        ]
        
        with pytest.raises(ValueError, match="env must be non-empty dictionary"):
            validate_scaffolding_format(invalid_data)
    
    def test_invalid_scaffolding_format_missing_description(self):
        """Test validation with missing description in env variable."""
        invalid_data = [
            {
                "category": "Database",
                "option": "sqlite",
                "env": {
                    "DATABASE_URL": {
                        # Missing "description"
                        "default": "sqlite:///app.db"
                    }
                }
            }
        ]
        
        with pytest.raises(ValueError, match="missing description"):
            validate_scaffolding_format(invalid_data)


class TestGenerateEnvFileContent:
    """Test suite for generate_env_file_content function."""
    
    def test_generate_env_file_content_basic(self):
        """Test basic env file content generation."""
        variables = {
            "DATABASE_URL": {
                "config": EnvVarConfig(
                    description="Database connection URL",
                    default="sqlite:///app.db",
                    required=True,
                    importance="critical"
                ),
                "category": "Database",
                "option": "sqlite"
            },
            "DEBUG_MODE": {
                "config": EnvVarConfig(
                    description="Enable debug mode",
                    default="false",
                    required=False,
                    choices=["true", "false"],
                    importance="important"
                ),
                "category": "General",
                "option": "default"
            }
        }
        
        content = generate_env_file_content(variables)
        
        # Check that content contains expected elements
        assert "CRITICAL: Essential Settings" in content
        assert "IMPORTANT: Settings to Configure" in content
        assert "# ----- Database (sqlite) -----" in content
        assert "# ----- General (default) -----" in content
        assert "DATABASE_URL=sqlite:///app.db" in content
        assert "DEBUG_MODE=false" in content
        assert "Database connection URL" in content
        assert "Enable debug mode" in content
        assert "Required" in content
        assert "Choices: true, false" in content
    
    def test_generate_env_file_content_empty(self):
        """Test env file content generation with empty variables."""
        variables = {}
        
        content = generate_env_file_content(variables)
        
        assert content == ""
    
    def test_generate_env_file_content_sorting(self):
        """Test that generated content is properly sorted."""
        variables = {
            "ZEBRA_VAR": {
                "config": EnvVarConfig(description="Zebra variable", default="zebra", importance="important"),
                "category": "Zoo",
                "option": "animals"
            },
            "ALPHA_VAR": {
                "config": EnvVarConfig(description="Alpha variable", default="alpha", importance="important"),
                "category": "Alpha",
                "option": "letters"
            }
        }
        
        content = generate_env_file_content(variables)
        
        # Alpha should come before Zoo (alphabetical within importance levels)
        alpha_pos = content.find("# ----- Alpha (letters) -----")
        zoo_pos = content.find("# ----- Zoo (animals) -----")
        assert alpha_pos < zoo_pos
        
        # Variables within groups should also be sorted
        assert "ALPHA_VAR=alpha" in content
        assert "ZEBRA_VAR=zebra" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])