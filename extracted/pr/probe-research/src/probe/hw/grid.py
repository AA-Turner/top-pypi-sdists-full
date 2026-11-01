"""Moved to `probe.sdk.hardware.grid` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.grid
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.grid")
