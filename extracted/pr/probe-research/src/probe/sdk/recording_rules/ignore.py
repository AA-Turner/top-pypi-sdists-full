"""Moved to `probe.sdk.recording_rules.recording_rules` (2026-11-04); this path stays importable for one release."""

# restructure-shim: probe.sdk.recording_rules.recording_rules
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.recording_rules.recording_rules")
