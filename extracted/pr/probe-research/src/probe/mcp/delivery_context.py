"""Moved to `probe.mcp.delivery.context` (agent:17); this path stays importable for one release."""

# restructure-shim: probe.mcp.delivery.context
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.delivery.context")
