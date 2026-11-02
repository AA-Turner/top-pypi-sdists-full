"""Moved to `probe.service.sessions.sessions` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.sessions.sessions
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.sessions.sessions")
