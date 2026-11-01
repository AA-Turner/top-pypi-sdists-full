"""Moved to `probe.sdk.hardware.resources.system` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.resources.system
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.resources.system")
