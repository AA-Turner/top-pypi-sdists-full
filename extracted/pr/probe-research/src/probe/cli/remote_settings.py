"""Moved to `probe.cli.lifecycle.remote_settings` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.lifecycle.remote_settings
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.lifecycle.remote_settings")
