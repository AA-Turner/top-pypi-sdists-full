"""
Unit tests for Space loader.
"""

import pytest
import tempfile
import yaml
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from tooluniverse.space import SpaceLoader


class TestSpaceLoader:
    """Test SpaceLoader class."""
    
    def test_space_loader_initialization(self):
        """Test SpaceLoader can be initialized."""
        loader = SpaceLoader()
        assert loader is not None
    
    def test_load_local_file(self):
        """Test loading a local YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml_content = """
name: Test Config
version: 1.0.0
description: Test description
tools:
  include_tools: [tool1, tool2]
"""
            f.write(yaml_content)
            f.flush()
            
            loader = SpaceLoader()
            config = loader.load(f.name)
            
            assert config['name'] == 'Test Config'
            assert config['version'] == '1.0.0'
            assert config['description'] == 'Test description'
            assert 'tools' in config
        
        # Clean up
        Path(f.name).unlink()
    
    def test_load_invalid_yaml_file(self):
        """Test loading an invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            invalid_yaml = """
name: Test Config
version: 1.0.0
invalid_field: value
"""
            f.write(invalid_yaml)
            f.flush()
            
            loader = SpaceLoader()
            
            with pytest.raises(ValueError, match="Configuration validation failed"):
                loader.load(f.name)
        
        # Clean up
        Path(f.name).unlink()
    
    def test_load_missing_file(self):
        """Test loading a missing file."""
        loader = SpaceLoader()
        
        with pytest.raises(ValueError, match="Space file not found"):
            loader.load("nonexistent.yaml")
    
    @patch('tooluniverse.space.loader.hf_hub_download')
    def test_load_huggingface_repo(self, mock_hf_download):
        """Test loading from HuggingFace repository."""
        # Mock HuggingFace download
        mock_hf_download.return_value = str(Path(__file__).parent / "test_data" / "test_config.yaml")
        
        # Create test file
        test_file = Path(__file__).parent / "test_data" / "test_config.yaml"
        test_file.parent.mkdir(exist_ok=True)
        with open(test_file, 'w') as f:
            yaml.dump({
                'name': 'HF Test Config',
                'version': '1.0.0',
                'description': 'Test from HuggingFace',
                'tools': {'include_tools': ['tool1']}
            }, f)
        
        loader = SpaceLoader()
        config = loader.load("hf://test-user/test-repo")
        
        assert config['name'] == 'HF Test Config'
        assert config['version'] == '1.0.0'
        
        # Clean up
        test_file.unlink()
        test_file.parent.rmdir()
    
    @patch('requests.get')
    def test_load_http_url(self, mock_get):
        """Test loading from HTTP URL."""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
name: HTTP Test Config
version: 1.0.0
description: Test from HTTP
tools:
  include_tools: [tool1, tool2]
"""
        mock_get.return_value = mock_response
        
        loader = SpaceLoader()
        config = loader.load("https://example.com/config.yaml")
        
        assert config['name'] == 'HTTP Test Config'
        assert config['version'] == '1.0.0'
        assert 'tools' in config
    
    def test_load_with_validation_error(self):
        """Test loading with validation error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            invalid_config = """
name: Test Config
# Missing required version field
description: Test description
"""
            f.write(invalid_config)
            f.flush()
            
            loader = SpaceLoader()
            
            with pytest.raises(ValueError, match="Configuration validation failed"):
                loader.load(f.name)
        
        # Clean up
        Path(f.name).unlink()
