"""Moved to `probe.daemon.lanes.run_alerts` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.lanes.run_alerts
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.lanes.run_alerts")
