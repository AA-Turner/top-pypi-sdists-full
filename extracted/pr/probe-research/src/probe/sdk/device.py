"""Moved to `probe.sdk.settings.device` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.settings.device
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.settings.device")
