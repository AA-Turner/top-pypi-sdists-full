"""Moved to `probe.service.actions.caller` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.actions.caller
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.actions.caller")
