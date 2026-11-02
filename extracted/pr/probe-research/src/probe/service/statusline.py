"""Moved to `probe.service.jobs.statusline` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.jobs.statusline
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.jobs.statusline")
