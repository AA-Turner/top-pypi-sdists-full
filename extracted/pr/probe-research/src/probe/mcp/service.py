"""Moved to `probe.mcp.tools` (agent:17); this path stays importable for one release."""

# restructure-shim: probe.mcp.tools
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.tools")
