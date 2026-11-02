"""Moved to `probe.cli.wizard.state.status` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.state.status
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.state.status")
