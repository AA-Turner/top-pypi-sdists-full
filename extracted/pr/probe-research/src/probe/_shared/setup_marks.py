"""Moved to `probe.shared.updates.setup_marks` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.setup_marks
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.setup_marks")
