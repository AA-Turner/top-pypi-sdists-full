"""Moved to `probe.service.actions.statuscache` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.actions.statuscache
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.actions.statuscache")
