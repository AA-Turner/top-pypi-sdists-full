"""Moved to `probe.sdk.hardware.wiring` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.wiring
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.wiring")
