"""Moved to `probe.service.hooks.hooks` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.hooks.hooks
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.hooks.hooks")
