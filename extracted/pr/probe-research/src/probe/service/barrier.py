"""Moved to `probe.service.updater.quiet.barrier` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.updater.quiet.barrier
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.updater.quiet.barrier")
