"""Moved to `probe.daemon.lanes.session_messages` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.lanes.session_messages
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.lanes.session_messages")
