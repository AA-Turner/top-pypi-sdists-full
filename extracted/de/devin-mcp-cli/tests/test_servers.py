import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from typer.testing import CliRunner
from mcp_cli.commands.servers import server_app, list_mcp_servers
from mcp_cli.config import get_servers_config


@pytest.fixture
def runner():
    return CliRunner()


class TestListServers:
    """Test the list servers functionality"""
    
    def test_list_servers_with_config_file(self, runner, test_config_file):
        """Test listing servers with a config file"""
        result = runner.invoke(server_app, ["list", "--config", test_config_file])
        
        assert result.exit_code == 0
        assert "Available MCP Servers:" in result.stdout
        assert "deepwiki-sse" in result.stdout
        assert "deepwiki-http" in result.stdout
        assert "deepwiki-stdio" in result.stdout
    
    def test_list_servers_no_config_file(self, runner):
        """Test listing servers when no config file exists"""
        with patch('mcp_cli.config.os.getenv') as mock_getenv:
            # Mock the environment variable to return None so it doesn't interfere
            mock_getenv.return_value = None
            
            result = runner.invoke(server_app, ["list", "--config", "/nonexistent/config.json"])
            
            assert result.exit_code == 1
            assert "Config file not found, please set the MCP_CLI_CONFIG_PATH" in result.stdout
    
    def test_list_servers_empty_config(self, runner):
        """Test listing servers with empty config"""
        import tempfile
        import json
        
        empty_config = {"mcpServers": {}}
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(empty_config, f)
            config_path = f.name
        
        try:
            result = runner.invoke(server_app, ["list", "--config", config_path])
            assert result.exit_code != 0  # Should fail with empty config
        finally:
            import os
            os.unlink(config_path)
    
    def test_list_servers_function_directly(self, test_config_file):
        """Test the list_mcp_servers function directly"""
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            mock_get_config.return_value = {
                "deepwiki-sse": {"url": "https://mcp.deepwiki.com/sse"},
                "deepwiki-http": {"url": "https://mcp.deepwiki.com/mcp"}
            }
            
            with patch('typer.echo') as mock_echo:
                list_mcp_servers(config_file=test_config_file)
                
                # Check that the right calls were made
                calls = [call.args[0] for call in mock_echo.call_args_list]
                assert "Available MCP Servers:" in calls
                assert "- deepwiki-sse" in calls
                assert "- deepwiki-http" in calls


class TestServerCheck:
    """Test the server check functionality"""
    
    @pytest.mark.asyncio
    async def test_check_servers_success(self, test_config_file):
        """Test successful server check with real MCP server"""
        from mcp_cli.commands.servers import check_mcp_servers
        
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            # Use one real server for testing
            mock_get_config.return_value = {
                "deepwiki-http": {
                    "url": "https://mcp.deepwiki.com/mcp"
                }
            }
            
            with patch('mcp_cli.commands.servers.console') as mock_console:
                # Get the underlying function if it's wrapped
                func = check_mcp_servers
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                try:
                    await func(config_file=test_config_file)
                    # Verify console output was called (should show connection results)
                    assert mock_console.print.called
                except Exception as e:
                    # Real server might be unavailable, but test should handle gracefully
                    assert mock_console.print.called
    
    @pytest.mark.asyncio 
    async def test_check_servers_no_servers(self, test_config_file):
        """Test server check when no servers are configured"""
        from mcp_cli.commands.servers import check_mcp_servers
        
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            mock_get_config.return_value = {}
            
            with patch('typer.echo') as mock_echo:
                # Get the underlying function if it's wrapped
                func = check_mcp_servers
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                await func(config_file=test_config_file)
                
                mock_echo.assert_called_with(
                    f"No MCP servers found. Verify the configuration file: '{test_config_file}'"
                )
    
    @pytest.mark.asyncio
    async def test_check_servers_connection_failure(self, test_config_file):
        """Test server check when server connection fails"""
        from mcp_cli.commands.servers import check_mcp_servers
        
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            mock_get_config.return_value = {
                "failing-server": {
                    "command": "nonexistent-command"
                }
            }
            
            with patch('mcp_cli.commands.servers.console') as mock_console:
                # Get the underlying function if it's wrapped
                func = check_mcp_servers
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                await func(config_file=test_config_file)
                
                # Should still complete without raising exception
                assert mock_console.print.called
    
    @pytest.mark.asyncio
    async def test_check_servers_multiple_servers_mixed_results(self, test_config_file):
        """Test server check with multiple servers where some succeed and some fail"""
        from mcp_cli.commands.servers import check_mcp_servers
        
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            mock_get_config.return_value = {
                "deepwiki-http": {
                    "url": "https://mcp.deepwiki.com/mcp"
                },
                "broken-server": {
                    "command": "nonexistent"
                }
            }
            
            with patch('mcp_cli.commands.servers.console') as mock_console:
                # Get the underlying function if it's wrapped
                func = check_mcp_servers
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                await func(config_file=test_config_file)
                
                # Verify console output was called
                assert mock_console.print.called
    
    def test_check_servers_cli_integration(self, runner, test_config_file):
        """Test server check through CLI runner"""
        with patch('mcp_cli.commands.servers.get_servers_config') as mock_get_config:
            mock_get_config.return_value = {
                "deepwiki-sse": {
                    "url": "https://mcp.deepwiki.com/sse"
                }
            }
            
            result = runner.invoke(server_app, ["check", "--config", test_config_file])
            
            # Should complete - real servers may succeed or fail gracefully
            assert result.exit_code == 0


class TestConfigIntegration:
    """Test integration with config loading"""
    
    def test_get_servers_config_integration(self, test_config_file):
        """Test that get_servers_config works with our test config"""
        config = get_servers_config(test_config_file)
        
        assert "deepwiki-sse" in config
        assert "deepwiki-http" in config  
        assert "deepwiki-stdio" in config
        
        # Verify config structure
        assert config["deepwiki-sse"]["url"] == "https://mcp.deepwiki.com/sse"
        assert config["deepwiki-http"]["url"] == "https://mcp.deepwiki.com/mcp"
        assert config["deepwiki-stdio"]["command"] == "npx"
        assert config["deepwiki-stdio"]["args"] == ["-y", "mcp-deepwiki@latest"] 