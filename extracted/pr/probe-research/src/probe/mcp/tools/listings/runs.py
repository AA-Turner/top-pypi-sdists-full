"""Moved to `probe.mcp.tools.reads.listings.runs`; this path stays importable for one release."""

# restructure-shim: probe.mcp.tools.reads.listings.runs
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.tools.reads.listings.runs")
