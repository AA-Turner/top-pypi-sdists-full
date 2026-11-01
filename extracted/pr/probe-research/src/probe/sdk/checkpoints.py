"""Moved to `probe.sdk.run.readback.readback` (agent:10); this path stays importable for one release."""

# restructure-shim: probe.sdk.run.readback.readback
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.run.readback.readback")
