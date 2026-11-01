"""Moved to `probe.sdk.delivery.outbox.drainers.in_process` (agent:7); this path stays importable for one release."""

# restructure-shim: probe.sdk.delivery.outbox.drainers.in_process
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.outbox.drainers.in_process")
