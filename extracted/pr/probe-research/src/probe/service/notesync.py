"""Moved to `probe.service.jobs.notesync` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.jobs.notesync
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.jobs.notesync")
