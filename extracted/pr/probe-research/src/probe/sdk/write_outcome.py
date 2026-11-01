"""Moved to `probe.sdk.values.write_outcome` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.values.write_outcome
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.values.write_outcome")
