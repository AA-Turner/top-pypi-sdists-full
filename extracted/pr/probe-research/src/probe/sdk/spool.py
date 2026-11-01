"""Moved to `probe.sdk.delivery.spool` (agent:7); this path stays importable for one release."""

# restructure-shim: probe.sdk.delivery.spool
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.spool")
