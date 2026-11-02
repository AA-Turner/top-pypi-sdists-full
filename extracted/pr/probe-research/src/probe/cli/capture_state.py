"""Moved to `probe.cli.capture.state` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.capture.state
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.capture.state")
