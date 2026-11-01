"""Moved to `probe.shared.reads.mcp_bridge` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.reads.mcp_bridge
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.reads.mcp_bridge")
