"""Moved to `probe.daemon.session.scope` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.session.scope
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.session.scope")
