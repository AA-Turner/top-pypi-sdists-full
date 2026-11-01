"""Moved to `probe.shared.notes.drafts` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.notes.drafts
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.notes.drafts")
