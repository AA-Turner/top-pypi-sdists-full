"""Moved to `probe.cli.imports.jobs.ui` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.jobs.ui
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.jobs.ui")
