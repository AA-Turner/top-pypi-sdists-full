"""Moved to `probe.sdk.delivery.journal` (agent:7); this path stays importable for one release."""

# restructure-shim: probe.sdk.delivery.journal
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.journal")
