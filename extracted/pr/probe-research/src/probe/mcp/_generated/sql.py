"""Moved to `probe.mcp.generated.sql` (agent:2); this path stays importable for one release."""

# restructure-shim: probe.mcp.generated.sql
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.mcp.generated.sql")
