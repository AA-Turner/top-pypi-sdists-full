"""Moved to `probe.analytics.core` (agent:4); this path stays importable for one release."""

# restructure-shim: probe.analytics.core
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.analytics.core")
