"""Moved to `probe.shared.reads.reads` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.reads.reads
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.reads.reads")
