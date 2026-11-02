"""Moved to `probe.cli.lifecycle.write_gate` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.lifecycle.write_gate
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.lifecycle.write_gate")
