"""Moved to `probe.mcp.tools.reads.entity`; this path stays importable for one release."""

# restructure-shim: probe.mcp.tools.reads.entity
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.tools.reads.entity")
