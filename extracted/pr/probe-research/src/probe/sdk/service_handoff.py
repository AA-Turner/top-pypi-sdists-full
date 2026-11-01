"""Moved to `probe.sdk.delivery.outbox.drainers.service_handoff` (agent:7); this path stays importable for one release."""

# restructure-shim: probe.sdk.delivery.outbox.drainers.service_handoff
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.outbox.drainers.service_handoff")
