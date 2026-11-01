"""Moved to `probe.daemon.worker.bite.bite` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.worker.bite.bite
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.worker.bite.bite")
