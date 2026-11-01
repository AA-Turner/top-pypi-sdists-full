"""Moved to `probe.sdk.reads.notes_cap` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.reads.notes_cap
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.reads.notes_cap")
