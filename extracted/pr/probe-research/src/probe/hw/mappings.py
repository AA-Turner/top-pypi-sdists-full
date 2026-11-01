"""Moved to `probe.sdk.hardware.mappings` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.mappings
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.mappings")
