"""Moved to `probe.cli.imports.jobs.messages` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.jobs.messages
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.jobs.messages")
