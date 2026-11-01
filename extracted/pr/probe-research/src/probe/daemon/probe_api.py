"""Moved to `probe.daemon.session.probe_api` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.session.probe_api
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.session.probe_api")
