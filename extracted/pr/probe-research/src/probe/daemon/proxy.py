"""Moved to `probe.daemon.host.proxy` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.host.proxy
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.host.proxy")
