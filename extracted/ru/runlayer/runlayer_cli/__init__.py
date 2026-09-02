"""Runlayer CLI - Run MCP servers via HTTP transport."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("runlayer")
except PackageNotFoundError:
    __version__ = "unknown"
