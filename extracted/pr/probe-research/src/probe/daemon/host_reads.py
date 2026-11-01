"""Moved to `probe.daemon.host.reads` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.host.reads
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.host.reads")
