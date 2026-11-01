"""Moved to `probe.sdk.values.values` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.values.values
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.values.values")
