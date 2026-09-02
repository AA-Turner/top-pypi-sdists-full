"""
InnoDay MCP Server Package

Model Context Protocol server for InnoDay platform integration with Claude Code.
"""

from .server import app, run_server

__all__ = ["app", "run_server"]
