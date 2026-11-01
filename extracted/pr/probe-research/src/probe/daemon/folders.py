"""Moved to `probe.daemon.session.session` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.session.session
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.session.session")
