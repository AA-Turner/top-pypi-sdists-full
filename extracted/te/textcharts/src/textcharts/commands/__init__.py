"""Shared command layer for textcharts CLI and MCP interfaces.

Provides a unified command surface: registry of chart types, input parsing,
command execution, and introspection APIs. Both CLI and MCP delegate here.
"""

from textcharts.commands.executor import execute_command
from textcharts.commands.registry import (
    CommandInfo,
    describe_command,
    get_command,
    get_input_schema,
    list_commands,
)

__all__ = [
    "CommandInfo",
    "describe_command",
    "execute_command",
    "get_command",
    "get_input_schema",
    "list_commands",
]
