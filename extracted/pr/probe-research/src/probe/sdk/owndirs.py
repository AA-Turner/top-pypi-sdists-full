"""Moved to `probe.sdk.capture.owndirs` (agent:11); this path stays importable for one release."""

# restructure-shim: probe.sdk.capture.owndirs
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.capture.owndirs")
