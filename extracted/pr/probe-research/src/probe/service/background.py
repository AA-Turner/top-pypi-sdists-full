"""Moved to `probe.service.jobs.background.background` (agent:16, hot path); this path stays importable for one release."""

# restructure-shim: probe.service.jobs.background.background
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.jobs.background.background")
