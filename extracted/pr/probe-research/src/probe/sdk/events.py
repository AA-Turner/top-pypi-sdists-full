"""Moved to `probe.sdk.reads.events` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.reads.events
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.reads.events")
