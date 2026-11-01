"""Moved to `probe.sdk.capture.lineage.c_readers` (agent:11); this path stays importable for one release."""

# restructure-shim: probe.sdk.capture.lineage.c_readers
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.capture.lineage.c_readers")
