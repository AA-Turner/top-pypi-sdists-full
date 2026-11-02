"""Moved to `probe.service.sessions.capture_gate` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.sessions.capture_gate
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.sessions.capture_gate")
