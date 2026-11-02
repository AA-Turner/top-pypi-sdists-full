"""Moved to `probe.cli.lifecycle.service_calls` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.lifecycle.service_calls
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.lifecycle.service_calls")
