"""Moved to `probe.shared.notes.sync` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.notes.sync
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.notes.sync")
