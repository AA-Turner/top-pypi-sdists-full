"""Moved to `probe.service.jobs.imports` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.jobs.imports
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.jobs.imports")
