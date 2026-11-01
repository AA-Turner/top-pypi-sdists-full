"""Moved to `probe.shared.updates.updates` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.updates
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.updates")
