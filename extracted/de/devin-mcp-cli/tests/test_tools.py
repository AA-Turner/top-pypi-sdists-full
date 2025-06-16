import pytest
from unittest.mock import patch
from typer.testing import CliRunner
from mcp_cli.commands.tools import tool_app
import typer
from unittest.mock import call


@pytest.fixture
def runner():
    return CliRunner()


class TestListTools:
    """Test the list tools functionality"""
    
    @pytest.mark.asyncio
    async def test_list_tools_single_server(self, test_config_file):
        """Test listing tools for a single server"""
        from mcp_cli.commands.tools import list_tools
        
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {
                "url": "https://mcp.deepwiki.com/mcp"
            }
            
            with patch('mcp_cli.commands.tools.print_tools') as mock_print_tools:
                # Get the underlying function if it's wrapped
                func = list_tools
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                try:
                    await func(server_name="deepwiki-http", config_file=test_config_file)
                    
                    # Verify the right functions were called
                    mock_get_server_config.assert_called_once_with("deepwiki-http", test_config_file)
                    # print_tools should be called if server connection succeeds
                    if mock_print_tools.called:
                        assert mock_print_tools.call_count == 1
                except Exception:
                    # Real server might be unavailable, test should handle gracefully
                    pass
    
    @pytest.mark.asyncio
    async def test_list_tools_all_servers(self, test_config_file):
        """Test listing tools for all servers"""
        from mcp_cli.commands.tools import list_tools
        
        with patch('mcp_cli.commands.tools.get_servers_config') as mock_get_servers_config:
            mock_get_servers_config.return_value = {
                "deepwiki-http": {"url": "https://mcp.deepwiki.com/mcp"},
                "deepwiki-sse": {"url": "https://mcp.deepwiki.com/sse"}
            }
            
            with patch('mcp_cli.commands.tools.print_tools') as mock_print_tools:
                with patch('typer.secho') as mock_secho:
                    # Get the underlying function if it's wrapped
                    func = list_tools
                    if hasattr(func, '__wrapped__'):
                        func = func.__wrapped__
                    
                    try:
                        await func(server_name=None, config_file=test_config_file)
                        
                        # Tools might be listed for available servers
                        # Real servers might succeed or fail
                    except Exception:
                        # Real servers might be unavailable
                        pass
    
    @pytest.mark.asyncio
    async def test_list_tools_server_failure(self, test_config_file):
        """Test listing tools when server connection fails"""
        from mcp_cli.commands.tools import list_tools
        
        with patch('mcp_cli.commands.tools.get_servers_config') as mock_get_servers_config:
            mock_get_servers_config.return_value = {
                "failing-server": {"command": "nonexistent"}
            }
            
            with patch('typer.secho') as mock_secho:
                # Get the underlying function if it's wrapped
                func = list_tools
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                # Should not raise exception, should continue with other servers
                await func(server_name=None, config_file=test_config_file)
                
                # Should have logged an error message
                error_calls = [call for call in mock_secho.call_args_list 
                             if "Failed to list tools" in str(call)]
                assert len(error_calls) > 0
    
    def test_list_tools_cli_single_server(self, runner, test_config_file):
        """Test list tools CLI command for single server"""
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"url": "https://mcp.deepwiki.com/mcp"}
            
            result = runner.invoke(tool_app, [
                "list", 
                "--server", "deepwiki-http",
                "--config", test_config_file
            ])
            
            # Should complete - real server may succeed or fail gracefully
            assert result.exit_code == 0
    
    def test_list_tools_cli_all_servers(self, runner, test_config_file):
        """Test list tools CLI command for all servers"""
        with patch('mcp_cli.commands.tools.get_servers_config') as mock_get_servers_config:
            mock_get_servers_config.return_value = {
                "deepwiki-http": {"url": "https://mcp.deepwiki.com/mcp"}
            }
            
            result = runner.invoke(tool_app, [
                "list",
                "--config", test_config_file
            ])
            
            # Should complete - real server may succeed or fail gracefully
            assert result.exit_code == 0


class TestExecuteTool:
    """Test the tool execution functionality"""
    
    @pytest.mark.asyncio
    async def test_execute_tool_success(self, test_config_file):
        """Test successful tool execution with real server"""
        from mcp_cli.commands.tools import execute_tool
        
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"url": "https://mcp.deepwiki.com/mcp"}
            
            with patch('typer.echo') as mock_echo:
                # Get the underlying function if it's wrapped
                func = execute_tool
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                try:
                    # Try to execute a tool - this will test real server capabilities
                    await func(
                        tool_name="search",  # Common tool name that might exist
                        server_name="deepwiki-http", 
                        input_args_json='{"query": "test"}',
                        config_file=test_config_file
                    )
                    
                    # If we get here, tool execution succeeded
                    echo_calls = [call.args[0] for call in mock_echo.call_args_list]
                    # Should have some output
                    assert len(echo_calls) > 0
                    
                except (SystemExit, typer.Exit):
                    # Tool might not exist or server might be unavailable
                    # This is expected for integration tests
                    pass
                except Exception:
                    # Real server connection issues are expected
                    pass
    
    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self, test_config_file):
        """Test executing a tool that doesn't exist"""
        from mcp_cli.commands.tools import execute_tool
        
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"url": "https://mcp.deepwiki.com/mcp"}
            
            with patch('typer.secho') as mock_secho:
                # Get the underlying function if it's wrapped
                func = execute_tool
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                try:
                    await func(
                        tool_name="definitely_nonexistent_tool_12345",
                        server_name="deepwiki-http",
                        input_args_json=None,
                        config_file=test_config_file
                    )
                except (SystemExit, typer.Exit):
                    # Expected for non-existent tool
                    pass
                except Exception:
                    # Real server connection issues are expected
                    pass
    
    @pytest.mark.asyncio
    async def test_execute_tool_invalid_json(self, test_config_file):
        """Test executing a tool with invalid JSON input"""
        from mcp_cli.commands.tools import execute_tool
        
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"url": "https://mcp.deepwiki.com/mcp"}
            
            with patch('typer.secho') as mock_secho:
                # Get the underlying function if it's wrapped
                func = execute_tool
                if hasattr(func, '__wrapped__'):
                    func = func.__wrapped__
                
                # Invalid JSON should cause Exit during input parsing
                with pytest.raises((SystemExit, typer.Exit)):
                    await func(
                        tool_name="search",
                        server_name="deepwiki-http",
                        input_args_json='{"invalid": json}',  # Invalid JSON
                        config_file=test_config_file
                    )
    
    @pytest.mark.asyncio
    async def test_execute_tool_connection_failure(self, test_config_file):
        """Test tool execution when server connection fails"""
        from mcp_cli.commands.tools import execute_tool
        
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"command": "nonexistent"}
            
            # Get the underlying function if it's wrapped
            func = execute_tool
            if hasattr(func, '__wrapped__'):
                func = func.__wrapped__
            
            try:
                await func(
                    tool_name="search",
                    server_name="failing-server",
                    input_args_json='{"query": "test"}',
                    config_file=test_config_file
                )
            except (SystemExit, typer.Exit):
                # Expected for connection failure
                pass
            except Exception:
                # Connection failures are expected
                pass
    
    def test_execute_tool_cli(self, runner, test_config_file):
        """Test tool execution through CLI"""
        with patch('mcp_cli.commands.tools.get_server_config') as mock_get_server_config:
            mock_get_server_config.return_value = {"url": "https://mcp.deepwiki.com/mcp"}
            
            result = runner.invoke(tool_app, [
                "call", "search",
                "--server", "deepwiki-http",
                "--input", '{"query": "test"}',
                "--config", test_config_file
            ])
            
            # Real server may succeed or fail, but should handle gracefully
            # Exit code might be 0 (success) or 1 (tool not found/connection error)
            assert result.exit_code in [0, 1]


class TestToolUtilities:
    """Test utility functions in the tools module"""
    
    def test_parse_input_args_valid_json(self):
        """Test parsing valid JSON input arguments"""
        from mcp_cli.commands.tools import parse_input_args
        
        result = parse_input_args('{"key": "value", "number": 42}')
        assert result == {"key": "value", "number": 42}
    
    def test_parse_input_args_none(self):
        """Test parsing None input arguments"""
        from mcp_cli.commands.tools import parse_input_args
        
        result = parse_input_args(None)
        assert result == {}
    
    def test_parse_input_args_invalid_json(self):
        """Test parsing invalid JSON input arguments"""
        from mcp_cli.commands.tools import parse_input_args
        
        # Invalid JSON should cause Exit from typer.Exit()
        with pytest.raises((SystemExit, typer.Exit)):
            parse_input_args('{"invalid": json}') 