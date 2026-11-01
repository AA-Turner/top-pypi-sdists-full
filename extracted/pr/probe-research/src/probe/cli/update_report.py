"""Moved to `probe.shared.updates.update_report` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.update_report
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.update_report")
