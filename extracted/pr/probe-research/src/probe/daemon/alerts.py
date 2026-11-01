"""Moved to `probe.daemon.worker.alerts` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.worker.alerts
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.worker.alerts")
