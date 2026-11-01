"""Moved to `probe.shared.feedback.feedback` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.feedback.feedback
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.feedback.feedback")
