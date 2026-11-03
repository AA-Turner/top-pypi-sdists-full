"""Moved to `probe.mcp.tools.reads.listings.workspaces`; this path stays importable for one release."""

# restructure-shim: probe.mcp.tools.reads.listings.workspaces
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.tools.reads.listings.workspaces")
