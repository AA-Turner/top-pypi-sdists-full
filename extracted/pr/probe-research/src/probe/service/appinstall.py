"""Moved to `probe.service.updater.app` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.updater.app
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.updater.app")
