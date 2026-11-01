"""Moved to `probe.sdk.values.tags` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.values.tags
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.values.tags")
