"""Moved to `probe.analytics` (agent:4); this path stays importable for one release."""

# restructure-shim: probe.analytics
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.analytics")
