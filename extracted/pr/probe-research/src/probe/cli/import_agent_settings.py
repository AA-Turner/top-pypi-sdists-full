"""Moved to `probe.cli.imports.agent_settings` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.agent_settings
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.agent_settings")
