"""
agentic-devtools: Agentic devtools integrate Jira, DevOps & more.

This package provides simple CLI commands that can be easily auto-approved
by VS Code AI assistants.
"""

import importlib.metadata

try:
    from agentic_devtools._version import __version__ as __version__
except ModuleNotFoundError as exc:
    if exc.name != "agentic_devtools._version":
        raise
    try:
        __version__ = importlib.metadata.version("agentic-devtools")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "0+unknown"
