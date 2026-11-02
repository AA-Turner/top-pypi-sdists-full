"""Moved to `probe.service.hooks.queue` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.hooks.queue
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.hooks.queue")
