"""Moved to `probe.sdk.reads.reads` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.reads.reads
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.reads.reads")
