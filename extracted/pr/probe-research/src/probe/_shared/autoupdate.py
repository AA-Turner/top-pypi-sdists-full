"""Moved to `probe.shared.updates.autoupdate` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.autoupdate
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.autoupdate")
