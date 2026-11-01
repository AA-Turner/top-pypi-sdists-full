"""Moved to `probe.sdk.hardware.resources.openmetrics` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.hardware.resources.openmetrics
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.hardware.resources.openmetrics")
