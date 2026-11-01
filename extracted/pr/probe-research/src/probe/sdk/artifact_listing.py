"""Moved to `probe.sdk.artifact.listing` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.artifact.listing
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.artifact.listing")
