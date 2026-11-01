"""Moved to `probe.shared.updates.uninstall_barrier` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.uninstall_barrier
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.uninstall_barrier")
