"""Moved to `probe.shared.reports` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.reports
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.reports")
