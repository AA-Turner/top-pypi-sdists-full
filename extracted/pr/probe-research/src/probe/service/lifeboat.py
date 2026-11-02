"""Moved to `probe.service.updater.lifeboat` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.updater.lifeboat
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.updater.lifeboat")
