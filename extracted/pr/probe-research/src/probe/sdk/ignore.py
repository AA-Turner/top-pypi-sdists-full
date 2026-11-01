"""Moved to `probe.sdk.recording_rules.ignore` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.recording_rules.ignore
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.recording_rules.ignore")
