"""Moved to `probe.sdk.delivery.transport` (agent:7); this path stays importable for one release."""

# restructure-shim: probe.sdk.delivery.transport
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.transport")
