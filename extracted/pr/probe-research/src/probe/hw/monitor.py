"""Moved to `probe.sdk.hardware.hardware` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.hardware
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.hardware")
