"""MCP Server entry point."""

import asyncio
import logging
import sys

from fastmcp import FastMCP

from datafold_mcp.auth import DatafoldAuth
from datafold_mcp.client import DatafoldClient
from datafold_mcp.config import Config
from datafold_mcp.tools.data_sources import register_data_source_tools
from datafold_mcp.tools.datadiff import register_datadiff_tools
from datafold_mcp.tools.query import register_query_tools

logger = logging.getLogger(__name__)


def _setup_logging(config: Config) -> None:
    """Configure logging based on config settings."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = getattr(logging, config.log_level.upper(), logging.INFO)

    handlers: list[logging.Handler] = []

    if config.log_file:
        # Log to file
        file_handler = logging.FileHandler(config.log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    else:
        # Log to stderr (stdout is used by MCP protocol)
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(stderr_handler)

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers,
    )


def create_server() -> FastMCP:
    """Create and configure the Datafold MCP server."""
    config = Config.from_env()
    _setup_logging(config)

    auth = DatafoldAuth(api_key=config.api_key)
    client = DatafoldClient(host=config.host, auth=auth, timeout=config.timeout)

    # Verify connection before starting server
    # Ensure event loop exists for compatibility with Windows and Python 3.10+
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No event loop running, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(client.verify_connection())
    mcp = FastMCP("datafold")

    register_query_tools(mcp, client)
    register_data_source_tools(mcp, client)
    register_datadiff_tools(mcp, client)

    host_log = config.host
    logger.info(f"Initialized Datafold MCP server for {host_log}")
    return mcp


def main() -> None:
    """Main entry point for the MCP server."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
