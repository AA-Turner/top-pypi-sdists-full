"""Moved to `probe.shared.notes.team_note` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.notes.team_note
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.notes.team_note")
