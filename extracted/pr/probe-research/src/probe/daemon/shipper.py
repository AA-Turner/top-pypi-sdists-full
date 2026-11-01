"""Moved to `probe.daemon.trace.shipper` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.trace.shipper
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.trace.shipper")
