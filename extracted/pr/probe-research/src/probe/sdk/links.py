"""Moved to `probe.sdk.reads.links` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.reads.links
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.reads.links")
