import pytest
import tempfile
import json
import os
from unittest.mock import patch
import typer
from mcp_cli.config import load_config, get_servers_config, get_server_config
import click

class TestLoadConfig:
    """Test the configuration loading functionality"""
    
    def test_load_config_valid_file(self, test_config_file):
        """Test loading a valid configuration file"""
        config = load_config(test_config_file)
        
        assert config is not None
        assert "mcpServers" in config
        assert "deepwiki-sse" in config["mcpServers"]
        assert "deepwiki-http" in config["mcpServers"]
        assert "deepwiki-stdio" in config["mcpServers"]
    
    def test_load_config_nonexistent_file(self):
        """Test loading a non-existent configuration file"""
        with patch('os.getenv') as mock_getenv:
            # Mock the environment variable to return None so it doesn't interfere
            mock_getenv.return_value = None
            
            with pytest.raises((typer.Exit, click.exceptions.Exit)):
                load_config("/nonexistent/config.json")
    
    def test_load_config_invalid_json(self):
        """Test loading an invalid JSON configuration file"""
        # Create a temporary file with invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('{"invalid": json}')  # Invalid JSON
            invalid_config_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                load_config(invalid_config_path)
        finally:
            os.unlink(invalid_config_path)
    
    def test_load_config_default_path(self):
        """Test loading config with default path behavior"""
        with patch('os.getenv') as mock_getenv:
            # Mock the environment variable to return None
            mock_getenv.return_value = None
            
            with pytest.raises(typer.Exit):
                load_config(None)  # Should use default path


class TestGetServersConfig:
    """Test the servers configuration retrieval"""
    
    def test_get_servers_config_valid(self, test_config_file):
        """Test getting servers config from valid file"""
        servers_config = get_servers_config(test_config_file)
        
        assert "deepwiki-sse" in servers_config
        assert "deepwiki-http" in servers_config
        assert "deepwiki-stdio" in servers_config
        
        # Verify structure
        assert servers_config["deepwiki-sse"]["url"] == "https://mcp.deepwiki.com/sse"
        assert servers_config["deepwiki-http"]["url"] == "https://mcp.deepwiki.com/mcp"
    
    def test_get_servers_config_no_mcp_servers_key(self):
        """Test getting servers config when mcpServers key is missing"""
        # Create config without mcpServers key
        invalid_config = {"otherKey": "value"}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(invalid_config, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError) as exc_info:
                get_servers_config(config_path)
            
            # Should show error about missing servers
            assert "MCP servers configuration" in str(exc_info.value)
        finally:
            os.unlink(config_path)
    
    def test_get_servers_config_empty_servers(self):
        """Test getting servers config when mcpServers is empty"""
        # Create config with empty mcpServers
        empty_servers_config = {"mcpServers": {}}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(empty_servers_config, f)
            config_path = f.name
        
        try:
            with pytest.raises(ValueError) as exc_info:
                get_servers_config(config_path)
            
            # Should show error about empty servers
            assert "MCP servers configuration" in str(exc_info.value)
        finally:
            os.unlink(config_path)


class TestGetServerConfig:
    """Test individual server configuration retrieval"""
    
    def test_get_server_config_existing_server(self, test_config_file):
        """Test getting config for an existing server"""
        server_config = get_server_config("deepwiki-stdio", test_config_file)
        
        assert server_config["command"] == "npx"
        assert server_config["args"] == ["-y", "mcp-deepwiki@latest"]
    
    def test_get_server_config_nonexistent_server(self, test_config_file):
        """Test getting config for a non-existent server"""
        with pytest.raises(typer.Exit):
            get_server_config("nonexistent-server", test_config_file)
    
    def test_get_server_config_url_server(self, test_config_file):
        """Test getting config for a URL-based server"""
        server_config = get_server_config("deepwiki-http", test_config_file)
        
        assert server_config["url"] == "https://mcp.deepwiki.com/mcp"
    
    def test_get_server_config_with_mocked_servers_config(self):
        """Test get_server_config with mocked servers config"""
        mock_servers = {
            "server1": {"command": "python"},
            "server2": {"command": "node"}
        }
        
        with patch('mcp_cli.config.get_servers_config') as mock_get_servers:
            mock_get_servers.return_value = mock_servers
            
            result = get_server_config("server1", "/fake/config.json")
            
            assert result == {"command": "python"}
            mock_get_servers.assert_called_once_with("/fake/config.json")


class TestConfigIntegration:
    """Test configuration integration scenarios"""
    
    def test_config_chain_load_to_get_servers(self, test_config_file):
        """Test the full chain from load_config to get_servers_config"""
        # This test verifies the integration works end-to-end
        servers_config = get_servers_config(test_config_file)
        
        # Should have all three test servers
        assert len(servers_config) == 3
        assert all(server in servers_config for server in 
                  ["deepwiki-sse", "deepwiki-http", "deepwiki-stdio"])
    
    def test_config_with_environment_variables(self):
        """Test configuration that includes environment variable references"""
        config_with_env = {
            "mcpServers": {
                "env-server": {
                    "command": "python",
                    "env": {
                        "API_KEY": "$MY_API_KEY",
                        "HOST": "$MY_HOST"
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(config_with_env, f)
            config_path = f.name
        
        try:
            servers_config = get_servers_config(config_path)
            
            # Should preserve environment variable references
            assert servers_config["env-server"]["env"]["API_KEY"] == "$MY_API_KEY"
            assert servers_config["env-server"]["env"]["HOST"] == "$MY_HOST"
        finally:
            os.unlink(config_path)
    
    def test_config_with_complex_args(self):
        """Test configuration with complex command arguments"""
        complex_config = {
            "mcpServers": {
                "complex-server": {
                    "command": "uv",
                    "args": [
                        "run", 
                        "--directory", 
                        "/path/to/server",
                        "server.py",
                        "--flag",
                        "--option=value"
                    ],
                    "env": {}
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(complex_config, f)
            config_path = f.name
        
        try:
            server_config = get_server_config("complex-server", config_path)
            
            # Should preserve all arguments in order
            expected_args = ["run", "--directory", "/path/to/server", "server.py", "--flag", "--option=value"]
            assert server_config["args"] == expected_args
        finally:
            os.unlink(config_path) 